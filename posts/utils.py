from datetime import datetime

def get_timestamp(date):
    dt = datetime(date.year, date.month, date.day)
    return datetime.timestamp(dt)