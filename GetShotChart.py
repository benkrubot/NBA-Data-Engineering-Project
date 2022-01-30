from nba_api.stats.endpoints import shotchartdetail
from nba_api.stats.endpoints import hustlestatsboxscore
from nba_api.stats.endpoints import boxscoreadvancedv2
from nba_api.stats.endpoints import boxscoredefensive
from nba_api.stats.endpoints import cumestatsplayer
import pandas as pd
from nba_api.stats.static import players
import json
import numpy as np

headers  = {
    'Connection': 'keep-alive',
    'Accept': 'application/json, text/plain, */*',
    'x-nba-stats-token': 'true',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
    'x-nba-stats-origin': 'stats',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Referer': 'https://stats.nba.com/',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
}

def GetShotChart(x):
  shotchart = shotchartdetail.ShotChartDetail(
  timeout=100,
  headers = headers,
  player_id = x,
  team_id = 0,
  season_type_all_star='Regular Season',
  season_nullable='2020-21',
  context_measure_simple="FGA"
  )
  df = shotchart.shot_chart_detail.get_data_frame()
  #print(df)
  df.to_csv('Lillardshotchart.csv', index=False)

GetShotChart('203081')
