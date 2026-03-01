
"""

Make a set of images that are one players position within a single 
time frame to see if the coordinates are by defualt ordered. 

The point is to scroll through the images that will be generated
for a given player for a given time stamp ordered by their position
in the data frame and see if it follows a sensible trajectory. If it 
does for enough time stamps and enough players, it's reasonable to assume 
that's the format.    
    
There's probably a more efficient way to test this but I don't see it. 
""" 

from __future__ import annotations

import numpy as np
import pandas as pd
from PIL import Image, ImageDraw

"""
dat is an ordered set of coordinates, name is what to name the images.
The images will be named name_i where i is the iterator over data.     
"""
def df_create_images(w,h,data, name): 
    for i in range(len(data)):
        img = Image.new("RGB", (w,h), "white")
        draw = ImageDraw.Draw(img)
        x,y = data[i]
        x += 100
        y += 50
        px = int(round(4 * x))
        py = int(round(4 * y))
        draw.ellipse([(px-5,py-5),(px+5,py+5)], fill = (255,0,0), outline="red")
        img.save("images/" + name + "_"+ str(i) + ".png")


def extract_points(df,time,player_id):
    mask = (df["time"] == time) & (df["player_id"] == player_id)
    subset = df.loc[mask, ["x", "y"]]
    return subset.values.tolist()

   


df = pd.read_csv("data_files/cleaned/2024-10-25.Team.H.@.Team.G.-.Tracking_CLEAN.csv")


xmin = min(df["x"])
xmax = max(df["x"])
ymin = min(df["y"])
ymax = max(df["y"])
#df = df.drop_duplicates(subset=['player_id', 'time'], keep='first')

time = 200
# Pick a random player_id
players = df.loc[df["time"] == time, "player_id"].dropna().unique()
player_id = np.random.choice(players)
#player_id = "A10"
mask  =(df["time"] == time) & (df["player_id"] == player_id)
print(df.loc[mask])

name  = (str(time) + player_id)
data = extract_points(df,time,player_id)
# Currently, when randomly selecting a player and time there is only one 
# position data, which is different than what I was seeing before.
#  
df_create_images(800,600, data,name)