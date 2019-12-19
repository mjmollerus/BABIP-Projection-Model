from pyforest import *
from bs4 import BeautifulSoup
import requests
from collections import OrderedDict
import json
import re

def getFGPlayerPages(urls):
    
    '''Takes in list of urls of FG leaderboards and returns list of urls of desired player pages'''
    
    player_pages=[]
    
    #get leaderboard html for each page
    for url in urls:
        response=requests.get(url)
        allplayerspage = response.text
        allplayerssoup = BeautifulSoup(allplayerspage)
        
        #get url endings and put in list
        playertable = allplayerssoup.find('table',id="LeaderBoard1_dg1_ctl00").find('tbody').find_all('tr')
        pageurls = []
        for row in playertable:
            player_pages.append(row.find('a').get('href'))
    
    return player_pages

def getFGPlayerStats(playerurls):
    
    '''Takes in list of player urls and returns dataframe of the desired statistics'''
    
    #create columns
    cols = ['Year','Player','Team','Games','PA','SB','ISO','Babip','CS','Spd','GB/FB',
            'LD','GB','FB','IFFB','HR/FB','IFH','BUH','Pull','Cent','Oppo','Soft','Med',
            'Hard','O-Swing','Z-Swing','Swing','O-Contact','Z-Contact','Contact','Zone']
    
    #create list to collect player-year dicts
    dictlist=[]

    for i in range(len(playerurls)):
        
        #create player page soup
        response=requests.get(f'https://www.fangraphs.com/{playerurls[i]}')
        playerpage=response.text
        playersoup=BeautifulSoup(playerpage)

        #iterate through years
        for year in range(2014,2019):
            #create list for each player-year
            entry = []
            #create counters to prevent there from being repeat for multiple teams cases
            counter1,counter2,counter3,counter4,counter5 = 0,0,0,0,0

            #iterate through rows in first table
            for row in playersoup.find('div',id='SeasonStats1_dgSeason11').find_all('tr'):
                #check existence, year, majors, counter
                if (len(row.find_all('td')) == 0 or
                    not row.find_all('td')[0].find('a') or
                    row.find_all('td')[0].find('a').text != str(year) or
                    '(' in row.find_all('td')[1].text or
                    counter1 == year):
                    continue

                #append year to babip
                else:
                    entry.append(year)
                    entry.append(playersoup.find('div',id='content').find('h1').text)
                    entry.append(row.find_all('td')[1].text)
                    entry.append(int(row.find_all('td')[2].text))
                    entry.append(int(row.find_all('td')[3].text))
                    entry.append(int(row.find_all('td')[7].text))
                    entry.append(float(row.find_all('td')[10].text))
                    entry.append(float(row.find_all('td')[11].text))
                    counter1 = year

            #iterate through rows in second table
            for row in playersoup.find('div',id='SeasonStats1_dgSeason1').find_all('tr'):
                #check existence, year, majors, counter
                if (len(row.find_all('td')) == 0 or
                    not row.find_all('td')[0].find('a') or
                    row.find_all('td')[0].find('a').text != str(year) or
                    '(' in row.find_all('td')[1].text or
                    counter2 == year):
                    continue

                #append caught stealing
                else:
                    entry.append(int(row.find_all('td')[20].text))
                    counter2 = year

            #iterate through rows in third table
            for row in playersoup.find('div',id='SeasonStats1_dgSeason2').find_all('tr'):
                #check existence, year, majors, counter
                if (len(row.find_all('td')) == 0 or
                    not row.find_all('td')[0].find('a') or
                    row.find_all('td')[0].find('a').text != str(year) or
                    '(' in row.find_all('td')[1].text or 
                    counter3 == year):
                    continue

                #append Spd
                else:
                    entry.append(float(row.find_all('td')[10].text))
                    counter3 = year

            #iterate through rows in fourth table
            for row in playersoup.find('div',id='SeasonStats1_dgSeason3').find_all('tr'):
                #check existence, year, majors, counter
                if (len(row.find_all('td')) == 0 or
                    not row.find_all('td')[0].find('a') or
                    row.find_all('td')[0].find('a').text != str(year) or
                    '(' in row.find_all('td')[1].text or 
                    counter4 == year):
                    continue

                #append batted ball data
                else:
                    entry.append(float(row.find_all('td')[2].text.split()[0]))
                    entry.append(float(row.find_all('td')[3].text.split()[0]))
                    entry.append(float(row.find_all('td')[4].text.split()[0]))
                    entry.append(float(row.find_all('td')[5].text.split()[0]))
                    entry.append(float(row.find_all('td')[6].text.split()[0]))
                    entry.append(float(row.find_all('td')[7].text.split()[0]))
                    entry.append(float(row.find_all('td')[8].text.split()[0]))
                    entry.append(float(row.find_all('td')[9].text.split()[0]))
                    #check if there's not batted ball data, and if its missing input NaN
                    if not row.find_all('td')[10].text.isspace():
                        entry.append(float(row.find_all('td')[10].text.split()[0]))
                        entry.append(float(row.find_all('td')[11].text.split()[0]))
                        entry.append(float(row.find_all('td')[12].text.split()[0]))
                        entry.append(float(row.find_all('td')[13].text.split()[0]))
                        entry.append(float(row.find_all('td')[14].text.split()[0]))
                        entry.append(float(row.find_all('td')[15].text.split()[0]))
                    else:
                        for i in range(1,7):
                            entry.append(np.NaN)                    
                    counter4 = year

            #iterate through fifth table
            for row in playersoup.find('div',id='SeasonStats1_dgSeason7').find_all('tr'):
                #check existence, year, majors, counter
                if (len(row.find_all('td')) == 0 or
                    not row.find_all('td')[0].find('a') or
                    row.find_all('td')[0].find('a').text != str(year) or
                    '(' in row.find_all('td')[1].text or
                    counter5 == year):
                    continue

                #append plate discipline data
                else:
                    entry.append(float(row.find_all('td')[2].text.split()[0]))
                    entry.append(float(row.find_all('td')[3].text.split()[0]))
                    entry.append(float(row.find_all('td')[4].text.split()[0]))
                    entry.append(float(row.find_all('td')[5].text.split()[0]))
                    entry.append(float(row.find_all('td')[6].text.split()[0]))
                    entry.append(float(row.find_all('td')[7].text.split()[0]))
                    entry.append(float(row.find_all('td')[8].text.split()[0]))
                    counter5 = year
            
            #append entry to playerdf
            entrydict=OrderedDict(zip(cols,entry))
            dictlist.append(entrydict)

    return pd.DataFrame(dictlist)

def getPageSoups(urls):

	'''Gets Soups for Baseball Savant Pages'''

    pageSoups = []

    for url in urls:
        response=requests.get(url)
        page = response.text
        soup = BeautifulSoup(page, 'lxml')
        pageSoups.append(soup)
    return pageSoups

def getEVJsons(soups):

	'''Gets EV data'''

    dictlist = []
    
    for soup in soups:
        jsontext = str(soup.find_all('script')[9]).split('var leaderboard_data = [')[1].split(']')[0]
        individuals = jsontext.split(',{')
        for i in range(len(individuals)):
            if i == 0:
                data = re.sub(r'(,"href"(.*)a>")*','',individuals[i])
            else:
                data = '{' + re.sub(r'(,"href"(.*)a>")*','',individuals[i])
            s=json.loads(data)
            dictlist.append(s)
    
    return pd.DataFrame(dictlist)

def getSSJsons(soups):

	'''Gets sprint speed data'''

    dictlist = []
    
    for soup in soups:
        jsontext = str(soup.find_all('script')[9].text.split('[')[1].split(']')[0])
        individual = jsontext.split(',{')
        for i in range(len(individual)):
            if i == 0:
                data = re.sub(r'(,"href"(.*)a>")*','',individual[i])
            else:
                data = '{' + re.sub(r'(,"href"(.*)a>")*','',individual[i])
            s=json.loads(data)
            dictlist.append(s)
    
    return pd.DataFrame(dictlist)

def getShiftData(url):

	'''Gets shift data'''
    
    response=requests.get(url)
    page = response.text
    soup = BeautifulSoup(page, 'lxml') 
    
    cols = ['Player','Year','Shift%']
    dictlist = []
    
    row_list = soup.find('table',id='search_results').find('tbody').find_all('tr',class_='search_row')
    
    for i in range(0,len(row_list)):
        entry = []
        entry.append(row_list[i].find('td',class_='player_name').text)
        entry.append(row_list[i].find_all('td')[2].text.split('- ')[1])
        entry.append(float(row_list[i].find_all('td')[4].text))
        
        dictlist.append(OrderedDict(zip(cols,entry)))
    
    return pd.DataFrame(dictlist)


if __name__ == '__main__':
	FG_leaderboard_urls = ['https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=y&type=8&season=2018&month=0&season1=2014&ind=0&team=&rost=&age=&filter=&players=&startdate=&enddate=&page=1_50',
                       'https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=y&type=8&season=2018&month=0&season1=2014&ind=0&team=&rost=&age=&filter=&players=&startdate=&enddate=&page=2_50',
                       'https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=y&type=8&season=2018&month=0&season1=2014&ind=0&team=&rost=&age=&filter=&players=&startdate=&enddate=&page=3_50',
                       'https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=y&type=8&season=2018&month=0&season1=2014&ind=0&team=&rost=&age=&filter=&players=&startdate=&enddate=&page=4_50',
                       'https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=y&type=8&season=2018&month=0&season1=2014&ind=0&team=&rost=&age=&filter=&players=&startdate=&enddate=&page=5_50',
                       'https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=y&type=8&season=2018&month=0&season1=2014&ind=0&team=&rost=&age=&filter=&players=&startdate=&enddate=&page=6_50',
                       'https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=y&type=8&season=2018&month=0&season1=2014&ind=0&team=&rost=&age=&filter=&players=&startdate=&enddate=&page=7_50']
	player_urls = getFGPlayerPages(FG_leaderboard_urls)
	FG_df = getFGPlayerStats(player_urls)
	FG_df.to_csv('../data/fgplayerdf.csv')

	EV_urls = ['https://baseballsavant.mlb.com/statcast_leaderboard?year=2019&abs=50&player_type=resp_batter_id',
          'https://baseballsavant.mlb.com/statcast_leaderboard?year=2018&abs=50&player_type=resp_batter_id',
          'https://baseballsavant.mlb.com/statcast_leaderboard?year=2017&abs=50&player_type=resp_batter_id',
          'https://baseballsavant.mlb.com/statcast_leaderboard?year=2016&abs=50&player_type=resp_batter_id',
          'https://baseballsavant.mlb.com/statcast_leaderboard?year=2015&abs=50&player_type=resp_batter_id']
	soups = getPageSoups(urls)
	EV_df = getJsons(soups)
	EV_df.to_csv('../data/EVdf.csv')

	SS_urls = ['https://baseballsavant.mlb.com/sprint_speed_leaderboard?year=2019&position=&team=&min=10',
          'https://baseballsavant.mlb.com/sprint_speed_leaderboard?year=2018&position=&team=&min=10',
          'https://baseballsavant.mlb.com/sprint_speed_leaderboard?year=2017&position=&team=&min=10',
          'https://baseballsavant.mlb.com/sprint_speed_leaderboard?year=2016&position=&team=&min=10',
          'https://baseballsavant.mlb.com/sprint_speed_leaderboard?year=2015&position=&team=&min=10']
	soups = getPageSoups(urls)
	SS_df = getJsons(soups)
	SS_df.to_csv('../data/SSdf.csv')

	shift_url = 'https://baseballsavant.mlb.com/statcast_search?hfPT=&hfAB=&hfBBT=&hfPR=&hfZ=&stadium=&hfBBL=&hfNewZones=&hfGT=R%7C&hfC=&hfSea=2019%7C2018%7C2017%7C2016%7C2015%7C&hfSit=&player_type=batter&hfOuts=&opponent=&pitcher_throws=&batter_stands=&hfSA=&game_date_gt=&game_date_lt=&hfInfield=2%7C3%7C&team=&position=&hfOutfield=&hfRO=&home_road=&hfFlag=&hfPull=&metric_1=&hfInn=&min_pitches=0&min_results=0&group_by=name-year&sort_col=pitches&player_event_sort=h_launch_speed&sort_order=desc&min_pas=30'
	shift_df = getShiftData(shift_url)
	shift_df.to_csv('../data/Shiftdf.csv')

