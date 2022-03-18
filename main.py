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
    redditor = reddit.redditor(user)
    subreddits = dict()

    search_comments(redditor, subreddits)
    search_posts(redditor, subreddits)



    return subreddits


def search_comments(redditor, subreddits):
    return

def search_posts(redditor, subreddits):
    return

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('user', type=str, help='User to be checked')
    parser.add_argument('amount', type=int, default=10, help='Amount of subreddits to be displayed')
    parser.add_argument('search', type=str, default=None, help='Search for particular subreddit instead')
    args = parser.parse_args()

    user = args.user
    amount = args.amount
    search = args.search

    subreddits = generate_subreddits(user)

    if search != None:
        return (bool(search in subreddits))
    else:
        sorted_tuples = sorted(subreddits.items(), key=lambda item: item[1])
        sorted_subreddits = {k: v for k, v in sorted_tuples}

        for i in range(amount):
            subreddit = sorted_subreddits.keys()[i]
            print('{}: {} interactions\n'.format(subreddit, sorted_subreddits[subreddit]))

    return

if __name__ == '__main__':
    main()
