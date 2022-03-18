import os
# import requests
import praw
import argparse

client_id = os.environ['PERSONAL_USE_SCRIPT']
client_secret = os.environ['SECRET']
user_agent = os.environ['USER_AGENT']


# auth = requests.auth.HTTPBasicAuth('<CLIENT_ID>', '<SECRET_TOKEN')

reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent=user_agent
)

def generate_subreddits(user):
    subreddits = dict()
    
    search_comments(user, subreddits)
    search_posts(user, subreddits)
    return


def search_comments(user, subreddits):
    return

def search_posts(user, subreddits):
    return

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('user', type=str, help='User to be checked')
    args = parser.parse_args()

    user = args.user

    generate_subreddits(user)

    return

if __name__ == '__main__':
    main()
