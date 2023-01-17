from helpers import *
from tiny import *
import asyncio
import time 

def main():
    pass
    # start_time = time.time()
    # print(fetch_carnage_gganbu_players()) # Execution time: 26.037474393844604 -> Execution time: 0.8401007652282715 by asyncing the participants requests
    # end_time = time.time()
    # execution_time = end_time - start_time
    # print("Execution time:", execution_time)

if __name__ == "__main__":
    main()

def sama_counter(gameId):
    from inputs import raw_gganbu_array, raw_result_array
    week_index = week - 17 # the api functions on gameId; ex: minecraft-carnage-2022-05-08. we also use gameId for our db to prevent having to always map week number to gameId

    moonsama_count = 0
    exosama_count = 0
    gromlinvip_count = 0
    
    # They do not have a lightweight endpoint that just returns players that participated
    participants = get_and_load_dictionary("https://mcapi.moonsama.com/game/minecraft-carnage-{gameId}/carnage-stats/result/original").keys()

    # getting data 
    base_url = "https://mcapi.moonsama.com/game/minecraft-carnage-{gameId}/carnage-stats/result/gganbu?player="
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


    