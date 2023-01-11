import asyncio
import aiohttp
import sys
import gc

async def get(url, session):
    try:
        async with session.get(url=url) as response:
            resp = await response.json()
            return resp
            # print("Successfully got url {} with resp of length {}.".format(url, len(resp)))
    except Exception as e:
        print("Unable to get url {} due to {}.".format(url, e.__class__))


async def batch_fetch(urls):
    async with aiohttp.ClientSession() as session:
        res = await asyncio.gather(*[get(url, session) for url in urls])
        return res

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

