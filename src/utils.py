import time
from datetime import datetime

"""
Generates a list of datetime objects representing the dates of the game 'carnage' starting from 2022-04-03.
The game finishes at 6pm UTC and player data is not available for that day. 

Returns:
    list: A list of datetime objects representing the dates of the 'carnage' game.
"""
def carnage_dates():
    carnage_start_time = 1649008800000
    carnage_time = carnage_start_time
    now_time = int(time.time()*1000)
    dates = [datetime.fromtimestamp(carnage_start_time/1000)]
    while True:
        carnage_time = carnage_time + 1000 * 60 * 60 * 24 * 7
        if(carnage_time > now_time):
            break
        dates.append(datetime.fromtimestamp(carnage_time/1000))
    return dates
