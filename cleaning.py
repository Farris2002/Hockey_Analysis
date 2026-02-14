import numpy as np

import oat_python as oat
import plotly.graph_objects as go
import pandas as pd



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
        




df = pd.read_csv("data_files/2024-10-25.Team.H.@.Team.G.-.Tracking.csv")

df=df.dropna(subset=["Game Clock"])

clock_split = df["Game Clock"].str.split(":", expand=True)
minutes = clock_split[0].astype(int)
seconds = clock_split[1].astype(int)

df["time"] = (19 - minutes + (60 - seconds)/60)

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
    "Period",
    "goal"
]]

print(out.iloc[0])

out.to_csv("data_files/cleaned/2024-10-25.Team.H.@.Team.G.-.Tracking_CLEAN.csv", index=False)

print("Wrote output_timeseries.csv")



