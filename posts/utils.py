from posts.models import Post

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

class ValidChecker:

    @staticmethod
    def check_post_valid(post_url, person_github_url):

            post_url = post_url[:-1] if post_url.endswith('/') else post_url

            tests = {
                'Gönderilen ödev size ait olmalıdır': not post_url.startswith(person_github_url),
                'Ödev yerine kendi github hesabınızı koyamazsınız': post_url == person_github_url or post_url == person_github_url+"/",
                'Bu URL daha önce başka bir ödevde kullanılmış': Post.objects.filter(post_url=post_url).exists(),
            }
            
            return [name for name,res in tests.items() if res]

valid_checker = ValidChecker()