from tinydb import TinyDB, Query
import asyncio
import aiohttp
from datetime import datetime
from async_request_manager import HttpClient
import requests
import json
from helpers import *

"""
SHAPE
    Like that of the original API (https://github.dev/moonsama/dev-resources/blob/main/minecraft_interfaces/mcapi/swagger.json)
    {
        gameId {
            gganbu_players
            gganbu
            final 
            leaderboards
            personal_share
            original
        },
        ...,
        ...,
    }

REASON 
    We are just storing data to test and operate locally and new data is not introduced frequently.
    It is typical to store data that we will act on a lot, especially when it changes infrequently. 

METHODS
    One way to ensure that your database is always up to date with the API is to use a caching strategy that periodically refreshes the data from the API. You could set a cache expiration time and check the cache before making a request to the API. If the cache has expired, you would make a request to the API to update the data in the cache and in your database, then return the data from the cache.
    Another way is to use a technique called "polling" in which you regularly check the API (e.g., every hour or every day) for updates and update your database accordingly.
    Webhook.
    Scheduled task or chron job. 


"""

# Initialize the TinyDB database
db = TinyDB('db.json')

# Create a new entry in the database
def create_entry(game_id, players_rss, players_gganbu, all_gganbu):
    db.insert({
        'game_id': game_id,
        'data': {
            'final': players_rss,
            'gganbu_players': players_gganbu,
            'gganbu': all_gganbu
        }
    })

# Inserts many entries into the database
def create_many(entries):
    db.insert_multiple(entries)    

# Read a single entry from the database
def read_entry(game_id):
    entry = Query()
    return db.search(entry.game_id == game_id)

# Update an entry in the database
def update_entry(game_id, players_rss, players_gganbu, all_gganbu):
    entry = Query()
    db.update({
        'game_id': game_id,
        'data': {
            'final': players_rss,
            'gganbu_players': players_gganbu,
            'gganbu': all_gganbu
        }
    }, entry.game_id == game_id)

# Delete an entry from the database
def delete_entry(game_id):
    entry = Query()
    db.remove(entry.game_id == game_id)

"""
Retrieves data for a specific game_id from the database. If the data is not available, it fetches the data using 
`fetch_carnage_final()`, `fetch_carnage_gganbu()`, and `fetch_carnage_gganbu_players()` and stores it in the database.

Args:
    game_id (str): The game_id of the data to retrieve. if datetime object passed, will convert it. 
    
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
    if isinstance(game_id, datetime.date):
        game_id = game_id.date().isoformat()
    data = read_entry(game_id) # reading game_id from database
    if not data: 
        # sync requests 
        players_final_rss = requests.get("https://mcapi.moonsama.com/game/minecraft-carnage-{}/carnage-stats/result/final".format(game_id)).json()
        all_gganbu = requests.get("https://mcapi.moonsama.com/game/minecraft-carnage-{}/carnage-stats/result/gganbu".format(game_id)).json()
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
        # store it 
        create_entry(game_id, player_rss=players_final_rss, players_gganbu=players_gganbu, all_gganbu=all_gganbu) # can specify arguments to avoid having to remember positions peeps
    return data
    
"""
Initializes the database we use by mass fetching from mcapi endpoints.
Subsequent fetches from mcapi are for updating the database and that is accomplished
with functions like get_data_by_gameid().
Args:
Returns:
"""
# improve -> session instantiated in batch_fetch tears down between successive calls. this is a place where having one session might be more efficient.
# better way to do async with all_games_players_gganbu
def init_db_data():
    # try not to 
    with open('./../db.json', 'r') as f:
        data = json.load(f)
        if bool(data) == False:
            return

    # fetches
    game_ids = carnage_dates()
    async_client = HttpClient()
    all_games_players_final_rss = asyncio.run(async_client.batch_fetch(["https://mcapi.moonsama.com/game/minecraft-carnage-{}/carnage-stats/result/final".format(game_id.date()) for game_id in game_ids]))
    all_games_all_gganbu = asyncio.run(async_client.batch_fetch(["https://mcapi.moonsama.com/game/minecraft-carnage-{}/carnage-stats/result/gganbu".format(game_id.date()) for game_id in game_ids]))
    
    # need to async this completely 
    ## a sloppy way might be to async all games and then for each game, async all player calls 
    all_games_players_gganbu = []
    for idx, game_id in enumerate(game_ids):
        players_gganbu = asyncio.run(async_client.batch_fetch(            
            [
                "https://mcapi.moonsama.com/game/minecraft-carnage-{}/carnage-stats/result/gganbu?player={}".format(game_id.date(), participant)
                for participant in all_games_players_final_rss[idx].keys()
            ]
        ))
        all_games_players_gganbu.append(players_gganbu)
    print(len(all_games_players_gganbu))
    
    # consolidate parallel lists
    all_data = [
        {
        'game_id': game_id.date().isoformat(),
        'data': {
            'final': all_games_players_final_rss[idx],
            'gganbu_players': all_games_players_gganbu[idx],
            'gganbu': all_games_all_gganbu[idx]
            }
        }
        for idx, game_id in enumerate(game_ids)
    ]

    # write all games to database
    create_many(all_data)
