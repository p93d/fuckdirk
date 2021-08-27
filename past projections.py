import requests
import pandas as pd
import numpy as np
import json
from tqdm import tqdm




d = {
    'season': [],
    'week': [],
    'player': [],
    'position': [],
    'projected_pts': [],
    'actual_pts': [],
    'actual_stats': []
}





for season in range(2018, 2021):

    for week in range(1, 17):

        url = "https://fantasy.espn.com/apis/v3/games/ffl/seasons/" \
                f"{season}/segments/0/leagues/1198573"


        headers = {
        'X-Fantasy-Filter': '{"players": {"filterStatus": {"value":["FREEAGENT","WAIVERS", "ONTEAM"]}}}'
        }

        cookies = {
            'SWID': '{2C03085F-A371-4FBB-A7DF-972721852987}',
            'espn_s2': 'AEB%2Be%2B0LOib6MWI4cRUFCnwPEvhYFb15XALNMyq' \
                    '%2FlPoiTx1%2FFxv0VwavEM8uOrUkx829L042S9gWNgy76' \
                    '%2F0ylPXN5hOfdFws2UdCeH%2BJ9Z36lGqBagneYz0PcOtpj' \
                    '77uMAZBWZ7hMNv7w0k7Y8f%2Fhfvp9aSeuU2FnOj95eLap3Fa' \
                    'o48VtYWAsUk4WLP6lkLl61etQvz6UPaopGWD70x7TbQRtEoQmLq' \
                    'OWcinQCFpCEG1rrFe4gvDeLcB6L0MD03Nv5BqR2Ik7%2B%2BpHZ7t1am2mQuq'
        }


        r = requests.get(url, headers=headers, cookies=cookies,
                        params={
                            'view': 'kona_player_info',
                            'scoringPeriodId': week
                        })


        data = json.loads(r.text)
        players = data['players']


        for player in players:

            # Add season/week identifier
            d['season'].append(season)
            d['week'].append(week)

            # read player info for name and position
            player_info = player['player']

            d['player'].append(player_info['fullName'])
            d['position'].append(player_info['defaultPositionId'])

            # read players stats to get projected and actual stats
            player_stats = player_info['stats']

            projected_pts = -999
            actual_pts = -999
            actual_stats = ""

            for stats in player_stats:

                if stats['scoringPeriodId'] == week:

                    if stats['statSourceId'] == 1:

                        projected_pts = stats['appliedTotal']

                    if stats['statSourceId'] == 0:

                        actual_pts = stats['appliedTotal']

                        actual_stats = stats['stats']


            d['projected_pts'].append(projected_pts)
            d['actual_pts'].append(actual_pts)
            d['actual_stats'].append(actual_stats)



df = pd.DataFrame.from_dict(d)

df.to_csv('projections.csv')            