"""

Script to clean the tracking data. 

creates a time-based format.
The columns are time, player_id, x,y, goal

"""


import numpy as np

import oat_python as oat
import plotly.graph_objects as go
import pandas as pd
import os


def make_player_id(row):
    try:
        if row["Player or Puck"] == "Puck":
            return "P"
        elif row["Team"] == "Home":
            return f"H{row['Player Id']}"
        elif row["Team"] == "Away":
            return f"A{row['Player Id']}"
        else:
            return np.nan
    except Exception as e:
        print(f"Error: {e}")
        print(f"Row: {row}")
        print(row)
   
   
# Assign fractional times within each integer second based on Image Id ordering
# AI made this method. Very clever!
def add_fractional_time(group):
   
    # Sort Image Ids and create fractional offsets
    unique_ids = sorted(group['Image Id'].unique())
    num_frames = len(unique_ids)
    
    # Map each Image Id to its fractional position (0/n, 1/n, 2/n, ...)
    id_to_frac = {img_id: i / num_frames for i, img_id in enumerate(unique_ids)}
    
    # Add fractional component to time and round to 5 decimal places
    # NOTE If rounding to 5 does not merge different time stamps in this data 
    # set, but could in others.
    group['time'] = (group['time'] + group['Image Id'].map(id_to_frac)).round(5)
    return group



def clean(df):

    df=df.dropna(subset=["Game Clock"])
    
    df['Image Id'] = df['Image Id'].astype(str).str.extract(r'_(\d+)$').astype(int)                     
    print(df["Image Id"])
    clock_split = df["Game Clock"].str.split(":", expand=True)
    minutes = clock_split[0].astype(int)
    seconds = clock_split[1].astype(int)

    # Converting clock to time passed in seconds since period start.
    base_time = ((19 - minutes)*60 + (60 - seconds))
    
    df["time"] = base_time + (df["Period"] - 1) * 1200
   
    # Create temporary column for grouping by integer time
    df['_time_int'] = df['time'].astype(int)
    df = df.groupby('_time_int', group_keys=False).apply(add_fractional_time)

   
    # Player ID is a letter then an int representing team then id number. So 
    # an away player with id 55 is A55, a puck is just P, or a home player with id 11
    # is H11. this condenses unecessary columns into an easy to understand format.
    df["Player Id"] = df.apply(make_player_id, axis=1)


    df = df.rename(columns={
        "Player Id": "player_id",
        "Rink Location X (Feet)": "x",
        "Rink Location Y (Feet)": "y",
        "Goal Score": "goal"
    })

    print(df.iloc[0])

    out = df[[
        "time",
        "player_id",
        "x",
        "y",
        "goal"
    ]]

    print(out.iloc[0])
    out_name = os.path.basename(tracking).replace(".Tracking.csv",".Tracking_CLEAN.csv")
    out.to_csv("data_files/cleaned/" + out_name, index=False)

    print("Wrote output_timeseries.csv")




#Create list of all tracking files to clean.      
root = "data_files"

trackings = []

for root,_,files in os.walk(root):
    for file in files:
       if file.endswith("Tracking.csv"):
           trackings.append(os.path.join(root,file)) 



#Clean the files.
for tracking in trackings:
    clean(pd.read_csv(tracking))
    
    