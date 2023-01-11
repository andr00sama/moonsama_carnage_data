from tinydb import TinyDB, Query

carnage_stats_db = TinyDB('weekly_carnage_data.json')

def get_week_carnage(date):
    Week = Query()
    return carnage_stats_db.get(Week.date == date)

def get_all_weeks_carnage():
    return carnage_stats_db.all()

def insert_weeks_carnage(weeks):
    carnage_stats_db.insert_multiple(weeks)

def insert_week_carnage(week):
    carnage_stats_db.insert(week)

