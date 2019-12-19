from pyforest import *

def clean():
	FG_df=pd.read_csv('../data/fgplayerdf.csv')
	EV_df=pd.read_csv('../data/EVdf.csv')
	SS_df=pd.read_csv('../data/SSdf.csv')
	shift_df = pd.read_csv('../data/Shiftdf.csv')

	#trim to columns with correlation to Babip
	FG_df = FG_df[['Year','Player','Babip','Team','PA','SB','CS','ISO','Spd','LD','FB','GB','IFFB','IFH','BUH','Pull',
	               'Cent','Oppo','Soft','Med','Hard']]
	#convert rate stats from % to probabilities
	FG_df[['LD','FB','GB','IFFB','IFH','BUH','Pull','Cent','Oppo','Soft','Med','Hard']].apply(lambda x: x/100,inplace=True)
	#sort by player-year
	FG_df.sort_values(by=['Player','Year'],inplace=True)

	#reformat name, trim, rename, convert to prob, sort by player-year
	EV_df['Player'] = [f"{name.split(', ')[1]} {name.split(', ')[0]}" for name in EV_df['name']]
	EV_df = EV_df[['season','Player','anglesweetspotpercent','avg_hit_angle',
	               'avg_hit_speed','brl_percent','ev95percent','fbld','gb']]
	EV_df.rename(columns={'season':'Year','anglesweetspotpercent':'SweetSpot%','avg_hit_angle':'AvgLauchAngle',
	                      'avg_hit_speed':'AvgEV','brl_percent':'Barrel%','ev95percent':'Above95MPH%','fbld':'FBLDAvgEV',
	                      'gb':'GBAvgEV'},inplace=True)
	EV_df[['SweetSpot%','Barrel%','Above95MPH%']].apply(lambda x: x/100,inplace=True)
	EV_df.sort_values(by=['Player','Year'],inplace=True)

	#reformat name, trim, rename, sort by player-year
	SS_df['Player'] = [f"{name.split(', ')[1]} {name.split(', ')[0]}" for name in SS_df['name_display_last_first']]
	SS_df = SS_df[['timeframe','Player','age','hp_to_1b','r_sprint_speed_top50percent_pretty']]
	SS_df.rename(columns={'timeframe':'Year','age':'Age','hp_to_1b':'HometoFirst',
	                      'r_sprint_speed_top50percent_pretty':'AvgSprintSpeed'},inplace=True)
	SS_df.sort_values(by=['Player','Year'],inplace=True)

	#first create a column called PlayerYear in each df and set it as index
	EV_df['PlayerYear'] = EV_df['Year'].apply(lambda x: str(x).split('.')[0]) + ' ' + smallEVdf['Player']
	EV_df.set_index('PlayerYear',inplace=True)
	FG_df['PlayerYear'] = FG_df['Year'].apply(lambda x: str(x).split('.')[0]) + ' ' + smallFGdf['Player']
	FG_df.set_index('PlayerYear',inplace=True)
	SS_df['PlayerYear'] = SS_df['Year'].apply(lambda x: str(x).split('.')[0]) + ' ' + smallSSdf['Player']
	SS_df.set_index('PlayerYear',inplace=True)
	shift_df['PlayerYear'] = shift_df['Year'].apply(lambda x: str(x).split('.')[0]) + ' ' + smallSSdf['Player']
	shift_df.set_index('PlayerYear',inplace=True)

	#finally merge into one combined df
	combineddf = pd.merge(smallFGdf,smallEVdf,how='outer',left_index=True,right_index=True)
	combineddf = pd.merge(combineddf,smallSSdf,how='outer',left_index=True,right_index=True)
	combineddf = pd.merge(combineddf,shiftdf,how='outer',left_index=True,right_index=True)

	#drop any entries with no babip and/or fewer that 300 PA
	combineddf.dropna(subset=['Babip'],inplace=True)
	combineddf = combineddf[combineddf.PA >= 300]

	combineddf.to_csv('../data/trimmeddf.csv')

if __name__ == '__main__':
	clean()
