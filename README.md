## Hockey Analysis

cleaning.py is a file that reorganizes the raw data to be in a more 
suitable format. Currently only did it for the tracking.csv files. Could be easily altered for the other file types as well.

the hockey_analysis notebook is scratch work messing with the data

the make_point_video.py is a py file that converts a tracking.csv file into a video of the players positions over time, with the teams colored separately and the puck colored black. 


## New Tracking.csv format

"time" column has time passed in seconds since the game started.

"player_id" column is one letter followed by an integer. The letter is P = puck, H = home, or A = away for what team they are on. The integer is their unqiue id as given in the original csv.  

"x" is the x coordinate.

"y" is the y coordinate.

"goal" is G if the row is representing a goal or otherwise empty.
