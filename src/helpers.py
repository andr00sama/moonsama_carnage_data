import asyncio
import aiohttp
import sys
import gc
import time
from datetime import datetime
from tiny import create_entry, read_entry
from async_request_manager import HttpClient
import requests

"""
Calculates the size of an object in bytes.
This function uses the `gc` module to traverse the object's references and calculate its size.

Args:
    obj (object): The object to calculate the size of.
    
Returns:
    int: The size of the object in bytes.
"""
def get_obj_size(obj):
    marked = {id(obj)}
    obj_q = [obj]
    sz = 0
    while obj_q:
        sz += sum(map(sys.getsizeof, obj_q))

        # Lookup all the object referred to by the object in obj_q.
        # See: https://docs.python.org/3.7/library/gc.html#gc.get_referents
        all_refr = ((id(o), o) for o in gc.get_referents(*obj_q))

        # Filter object that are already marked.
        # Using dict notation will prevent repeated objects.
        new_refr = {o_id: o for o_id, o in all_refr if o_id not in marked and not isinstance(o, type)}

        # The new obj_q will be the ones that were not marked,
        # and we will update marked with their ids so we will
        # not traverse them again.
        obj_q = new_refr.values()
        marked.update(new_refr.keys())
    return sz

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

def url_carnage_final(gameId):
    return "https://mcapi.moonsama.com/game/minecraft-carnage-{}/carnage-stats/result/final".format(gameId) 

def url_carnage_gganbu(gameId):
    return "https://mcapi.moonsama.com/game/minecraft-carnage-{}/carnage-stats/result/gganbu".format(gameId)

# async def fetch_carnage_gganbu_players(gameId, players):
#     all_urls = []
#     participants_each_week = asyncio.run(batch_fetch(["https://mcapi.moonsama.com/game/minecraft-carnage-{}/carnage-stats/result/final".format(date.date()) for date in dates]))
#     for idx, date in enumerate(dates):
#         urls = ["https://mcapi.moonsama.com/game/minecraft-carnage-{}/carnage-stats/result/gganbu?player={}".format(date.date(), participant) for participant in participants_each_week[idx].keys()]
#         all_urls.append(urls)
#     return all_urls

"""
Retrieves data for a specific game_id from the database. If the data is not available, it fetches the data using 
`fetch_carnage_final()`, `fetch_carnage_gganbu()`, and `fetch_carnage_gganbu_players()` and stores it in the database.

Args:
    game_id (str): The game_id of the data to retrieve.
    
Returns:
    dict: A dictionary containing the data for the specified game_id. 
    The dictionary will contain the following keys:
        game_id (str): The game_id of the data.
        data (dict): A dictionary containing the data for the game.
            final (list): The final data for the game
            gganbu_players (list): The gganbu players data for the game
            gganbu (list): The gganbu data for the game
"""
def get_data_by_gameid(game_id):
    data = read_entry(game_id) # reading game_id from database
    if not data: 
        # sync requests 
        players_final_rss = requests.get("https://mcapi.moonsama.com/game/minecraft-carnage-{}/carnage-stats/result/final".format(game_id)).json()
        all_gganbu = requests.get("https://mcapi.moonsama.com/game/minecraft-carnage-{}/carnage-stats/result/final".format(game_id)).json()
        participants = players_final_rss.keys()
        # async because we have to query each player 
        async_client = HttpClient()
        players_gganbu = asyncio.run(async_client.batch_fetch(["https://mcapi.moonsama.com/game/minecraft-carnage-{}/carnage-stats/result/gganbu?player={}".format(game_id, participant) for participant in participants]))
        # resultant data
        data = {
            'game_id': game_id,
            'data': {
                'final': players_final_rss,
                'gganbu_players': players_gganbu,
                'gganbu': all_gganbu
            }
        }
        print(data)
        # store it 
        create_entry(game_id, player_rss=players_final_rss, players_gganbu=players_gganbu, all_gganbu=all_gganbu) # can specify arguments to avoid having to remember positions peeps
    return data

def init_db_data():
    pass

def get_and_load_dictionary(url):
    import requests, json
    return json.load(requests.get(input).text)

