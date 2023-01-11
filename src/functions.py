from helpers import *
from tiny import *
import asyncio
import time
from datetime import datetime
import json


def main():
    print()
    # weekly carnage per player resource data 
    # weeks = gen_weekly_carnage_urls()[0:10]
    # weekly_carnage_player_rss_data = asyncio.run(batch_fetch(weeks))
    # for idx, week in enumerate(weekly_carnage_player_rss_data):
    #     insert_week_carnage({"week": idx, "data": week})


if __name__ == "__main__":
    main()

def get_and_load_dictionary(input):
    import requests, json
    return json.loads(requests.get(input).text)

def sama_counter(week):
    from inputs import raw_gganbu_array, raw_result_array
    week_index = week - 17
    result_dictionary = get_and_load_dictionary(raw_result_array[week_index])
    moonsama_count = 0
    exosama_count = 0
    gromlinvip_count = 0
    
    # getting data 
    base_url = "https://mcapi.moonsama.com/game/minecraft-carnage-2023-01-08/carnage-stats/result/gganbu?player="
    participants = result_dictionary.keys()
    request_urls = [base_url+player for player in participants]
    gganbu_per_player = asyncio.run(batch_fetch(request_urls))

    for player in gganbu_per_player:
        # have atleast 1 moonsama = moonsama
        if player["power"] > 0:
            moonsama_count+=1
         # 0 moonsamas, atleast 1 exosama = exosama
        elif player["exo_power"] > 0: 
            exosama_count+=1
        # 0 moonsamas, 0 exosamas, but still played = vip ticket
        else:
            gromlinvip_count+=1
    return moonsama_count, exosama_count, gromlinvip_count

def attendance_counter(first_week, last_week):
    from inputs import raw_result_array

    # getting data
    all_weeks_rss_data = asyncio.run(batch_fetch(raw_result_array[first_week-1:last_week+1])) # fetch data for all specified weeks
    
    # print("{} MB".format(get_obj_size(all_weeks_rss_data) * 10**(-6))) # can store all the weekly data 13MB before any compression
    attendance_log = []
    for week in all_weeks_rss_data:
        for player in week.keys():
            attendance_log.append(player)
    attendance_log.sort()
    attendance_name = []
    attendance_number = []
    attendance_final = []
    for player in attendance_log:
        if attendance_name.count(player) == 0:
            attendance_name.append(player)
            attendance_number.append(attendance_log.count(player))
    for names in range (0, len(attendance_number)):
        pair = (attendance_number[names], attendance_name[names])
        attendance_final.append(pair)
    attendance_final.sort()
    attendance_final.reverse()
    return attendance_final

def carnage_dates():
    """ 2022-04-03 first date that carnage api has, game finishes at 6pm UTC
    though player data is not available for that day """
    carnage_start_time = 1649008800000
    carnage_time = carnage_start_time
    now_time = int(time.time()*1000)
    dates = [carnage_time]
    while True:
        carnage_time = carnage_time + 1000 * 60 * 60 * 24 * 7
        if(carnage_time > now_time):
            break
        dates.append(carnage_time)
        # dates = [datetime.fromtimestamp(date/1000) for date in carnage_dates()]
    return dates[::-1]

def gen_weekly_carnage_urls():
    dates_timestamps = carnage_dates()[::-1]
    dates = [datetime.fromtimestamp(date/1000) for date in dates_timestamps]
    return [ 
        "https://mcapi.moonsama.com/game/minecraft-carnage-{}-{:02d}-{:02d}/carnage-stats/result/final".format(week.year, week.month, week.day) 
        for week in dates
    ]

def gen_weekly_gganbu_urls():
    dates = [datetime.fromtimestamp(date/1000) for date in carnage_dates()[::-1]]
    return [ 
        "https://mcapi.moonsama.com/game/minecraft-carnage-{}-{:02d}-{:02d}/carnage-stats/result/gganbu".format(week.year, week.month, week.day)
        for week in dates
    ]


