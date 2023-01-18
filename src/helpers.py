import asyncio
import aiohttp
import sys
import gc
import time
from datetime import datetime
from tiny import create_entry, read_entry, create_many
from async_request_manager import HttpClient
import requests
import json

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

def get_and_load_dictionary(url):
    import requests, json
    return json.load(requests.get(input).text)

