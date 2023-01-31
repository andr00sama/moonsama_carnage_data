import aiohttp
import asyncio

async def get(url, session):
    """
    Sends a GET request to the specified URL using the session object.
    Returns the JSON response from the request.

    Args:
        url (str): The URL to send the GET request to.

    Returns:
        dict: The JSON response from the request.
    """
    try:
        async with session.get(url=url) as response:
            resp = await response.json()
            return resp
    except Exception as e:
        print("Unable to get url {} due to {}: {}".format(url, e.__class__, e.with_traceback()))

async def batch_fetch(urls):
    """
    Sends multiple GET requests concurrently to the specified URLs using the
    session object. Returns a list of the JSON responses from the requests.
    
    asyncio.gather() returns the list of responses in the same order that you ordered the urls despite asynchronously performing the requests. 


    Args:
        urls (list): A list of URLs to send GET requests to.

    Returns:
        list: A list of the JSON responses from the requests.
    """
    async with aiohttp.ClientSession() as session:
        res = await asyncio.gather(*[get(url, session) for url in urls])
        return res

