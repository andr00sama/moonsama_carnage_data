from tinydb import TinyDB, Query

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