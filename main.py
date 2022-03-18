import os
# import requests
import praw

client_id = os.environ['PERSONAL_USE_SCRIPT']
client_secret = os.environ['SECRET']
user_agent = os.environ['USER_AGENT']


# auth = requests.auth.HTTPBasicAuth('<CLIENT_ID>', '<SECRET_TOKEN')

reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent=user_agent
)