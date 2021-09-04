import os
import json
import requests
from requests.auth import HTTPBasicAuth


print('Hi! I am GitHub follower bot.')
print('Letting you follow your all followers!')
print('Stating fetching your follower lists...\n')

github_user = os.getenv('github_user')
personal_github_token = os.getenv('personal_github_token')

follower_url = 'https://api.github.com/users/%s/followers?page=' % (github_user)
update_followed_user = 'https://api.github.com/user/following/%s'
page = 1
follower_counter = 0

while True:
    response = requests.get(follower_url + str(page))
    follower_lists = json.loads(response.text)
    follower_lists_len = len(follower_lists)
    if follower_lists_len == 0:
        break
    follower_counter += follower_lists_len
    for follower_info in follower_lists:
        headers = { 'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36' }
        user = follower_info['login']
        response = requests.put(update_followed_user % (user), auth=HTTPBasicAuth(github_user, personal_github_token), headers=headers)
        if response.status_code == 204:
            print('User: %s has been followed!' % user)
    page += 1

file_handler = open('follower_counter.txt', 'w')
file_handler.write(str(follower_counter) + '\n')


print('\nFollowing users from your followed lists are done!')
