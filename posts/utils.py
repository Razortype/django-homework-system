from datetime import datetime
import requests

def get_timestamp(date):
    dt = datetime(date.year, date.month, date.day)
    return datetime.timestamp(dt)

def seperate_homeworks(homeworks):
    enabled_homeworks = []
    disabled_homeworks = []

    for homework in homeworks:
        if homework.check_expired():
            disabled_homeworks.append(homework)
        else:
            enabled_homeworks.append(homework)
    
    return enabled_homeworks, disabled_homeworks

def left_started_homeworks(homeworks):
    return [i for i in homeworks if i.check_started()]

def check_post_404(post_url):
    r = requests.get(post_url)
    return r.status_code == 404