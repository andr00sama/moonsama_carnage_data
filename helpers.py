import asyncio
import aiohttp

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