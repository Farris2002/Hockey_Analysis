## Hockey Analysis

cleaning.py is a file that reorganizes the raw data to be in a more 
suitable format. Currently only did it for the tracking.csv files. Could be easily altered for the other file types as well.

the hockey_analysis notebook is scratch work messing with the data

the make_point_video.py is a py file that converts a tracking.csv file into a video of the players positions over time, with the teams colored separately and the puck colored black. 

### Issues with the video (and the data set)

The only time stamps we have are given by the clock, which is accurate to a second. However, for each second, for each player, we have multiple (around 10 ish) x,y coordinates. The trackers on the players record their positions more frequently than one second intervals. While this is very good, it also poses a problem in matching the x,y coordinates of the different players within the same time stamp. i.e. if we have two x,y coordinates for each player within the same time stamp, how do we know how to math the coordinates between players? 

Just looking at the data set in pandas (in the notebook), I notice that each time stamp has a different number of rows. When t=0, we have around 100 entries, but for t=1 we have several hundred. Warrants further investigation and may cause issues with analysis. It seems reasonable that the data collectors on the players helmets aren't synced up, so they are recording data at different times/frequencies, but large discrepencies as seen may be a little more than just that. Maybe we're lucky and I cleaned the data incorrectly somehow or am missing something simple. 

## New Tracking.csv format

"time" column has time passed in seconds since the game started.

"player_id" column is one letter followed by an integer. The letter is P = puck, H = home, or A = away for what team they are on. The integer is their unqiue id as given in the original csv.  

"x" is the x coordinate.

"y" is the y coordinate.

"goal" is G if the row is representing a goal or otherwise empty.
