# BABIP Projection Model

This repo contains the data and code to train a linear model to predict a baseball hitter's batting average on balls in play (BABIP) from peripheral statistics and notebooks demonstrating the process of assembling the data and using the model.

BABIP is a common quick check to see if a player got 'lucky' or 'unlucky', as it is largely beyond the ability of the player to control. However, some players have true talent BABIPs higher or lower than the league average of .300, so this model is useful for determining whether a player 'deserved' a high or low BABIP in a given season.

The data contains a variety of statistics from Fangraphs and Baseball Savant on standard statistics, advanced batting metrics, sprint speed, batted ball profiles, shifting, and other factors.

The model achieves a test R^2 of .54 and a MAE of .02, and should be considered valid for any recent player-season.

## Data

The data folder contains the raw data as scraped from Baseball Savant and Fangraphs and the combined and cleaned data. Any player-season with at least 300 PA from a player with a qualified season from 2014-2018 was included.

### Running the models

The model can be run from the model.py file or in the modeling notebook. To predict the BABIP any player-season not included in the dataset, input the specified data as a Pandas Dataframe using the PredictPlayer() function in the model.py file.
