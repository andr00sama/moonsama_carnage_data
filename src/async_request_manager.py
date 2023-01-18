import aiohttp
import asyncio

class HttpClient:
    """
    The HttpClient class handles sending requests using the aiohttp library.
    """
    async def get(self, url, session):
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

    async def batch_fetch(self, urls):
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
            res = await asyncio.gather(*[self.get(url, session) for url in urls])
            return res

# class HttpClient:
#     """
#     The HttpClient class handles sending requests using the aiohttp library.
#     It uses a single session object to manage connections, which can be closed
#     explicitly by calling the `close()` method.

#     Note that one could simply instantiate session = aiothttp.ClientSession(), use that session,
#     and then call session.close() to accomplish similiar behavior, but it is cleaner containing
#     these methods in one area and allows for more flexibility later on, if needed. 
#     """
#     def __init__(self):
#         """
#         Initializes the HttpClient object with a new aiohttp session.
#         Aiohttp uses connection pooling. 
#         It also uses the asyncio event loop.
#         """
#         self.session = aiohttp.ClientSession()

#     async def get(self, url):
#         """
#         Sends a GET request to the specified URL using the session object.
#         Returns the JSON response from the request.

#         Args:
#             url (str): The URL to send the GET request to.

#         Returns:
#             dict: The JSON response from the request.
#         """
#         try:
#             async with self.session.get(url=url) as response:
#                 resp = await response.json()
#                 return resp
#         except Exception as e:
#             print("Unable to get url {} due to {}".format(url, e.__class__))

#     async def close(self):
#         """
#         Closes the session object and releases any resources associated with it.
#         Note that when you use the async with statement in the get() method, 
#         it will handle releasing the resources related to the specific connection used in that method. 
#         However, the ClientSession object may maintain a pool of open connections that have not been explicitly closed and are still using resources.
#         By calling the close() method, you ensure that all open connections related to the ClientSession object are closed and that any resources associated 
#         with them are released, even if the get() method did not create them. 
#         """
#         await self.session.close()

#     async def batch_fetch(self, urls):
#         """
#         Sends multiple GET requests concurrently to the specified URLs using the
#         session object. Returns a list of the JSON responses from the requests.
        
#         asyncio.gather() returns the list of responses in the same order that you ordered the urls despite asynchronously performing the requests. 


#         Args:
#             urls (list): A list of URLs to send GET requests to.

#         Returns:
#             list: A list of the JSON responses from the requests.
#         """
#         res = await asyncio.gather(*[self.get(url) for url in urls])
#         return res

