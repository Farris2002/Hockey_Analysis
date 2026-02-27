## Hockey Analysis

cleaning.py is a file that reorganizes the raw data to be in a more 
suitable format. Currently only did it for the tracking.csv files. Could be easily altered for the other file types as well.

the hockey_analysis notebook is scratch work messing with the data

the make_point_video.py is a py file that converts a tracking.csv file into a video of the players positions over time, with the teams colored separately and the puck colored black. 

### Issues with the video (and the data set)

The only time stamps we have are given by the clock, which is accurate to a second. However, for each second, for each player, we have multiple (around 10 ish) x,y coordinates. The trackers on the players record their positions more frequently than one second intervals. While this is very good, it also poses a problem in matching the x,y coordinates of the different players within the same time stamp. i.e. if we have two x,y coordinates for each player within the same time stamp, how do we know how to math the coordinates between players? 


Ross mentioned that maybe its ordered by the time that they're recorded, which would be sensible. To check this, I made a small script make_images.py that takes a given player_id and time stamp and creates images ordered by the order in the dataframe to scroll through and see if they're ordered. at the files are labeled by timestamp then player_id then an ordering of the dataframe. The player position looks like it may have been ordered by time. the puck data is nonsensical, there's no way a puck could move that much in a one second time frame. 


## New Tracking.csv format

"time" column has time passed in seconds since the game started.

"player_id" column is one letter followed by an integer. The letter is P = puck, H = home, or A = away for what team they are on. The integer is their unqiue id as given in the original csv.  

"x" is the x coordinate.

"y" is the y coordinate.

"goal" is G if the row is representing a goal or otherwise empty.
