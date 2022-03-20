import os
import praw
import prawcore
import argparse

DEBUG = True

client_id = os.environ['PERSONAL_USE_SCRIPT']
client_secret = os.environ['SECRET']
user_agent = os.environ['USER_AGENT']

reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent=user_agent
)

def debug_print(message):
    if DEBUG:
        print(message)

def generate_subreddits(user):
    redditor = reddit.redditor(user)

    # Make sure username is a valid account
    try:
        redditor.id
    except prawcore.exceptions.NotFound:
        print('Error: user {} not found'.format(user))
        exit(-1)

    debug_print('Generating subreddits...')
    comment_subs = search_comments(redditor)
    post_subs = search_posts(redditor)

    # Choose the smaller dictionary to iterate through for efficiency
    if len(post_subs) >= len(comment_subs):
        subreddits = post_subs
        subreddits_to_append = comment_subs
    else:
        subreddits = comment_subs
        subreddits_to_append = post_subs

    # Merge both dictionaries together.
    debug_print('Merging post and comment history...')
    for subreddit in subreddits_to_append:
        if subreddit in subreddits:
            subreddits[subreddit] += subreddits_to_append[subreddit]
        else:
            subreddits[subreddit] = subreddits_to_append[subreddit]

    return subreddits

def search_comments(redditor):
    debug_print('Searching through all comments...')

    subreddits = dict()
    for comment in redditor.comments.new(limit=None):
        name = comment.subreddit.display_name
        # If comment is in a subreddit that is already listed, increase the count,
        # otherwise create a new entry.
        if name in subreddits:
            subreddits[name] += 1
        else:
            subreddits[name] = 1

    return subreddits

def search_posts(redditor):
    debug_print('Searching through all posts...')

    subreddits = dict()
    for post in redditor.submissions.new(limit=None):
        name = post.subreddit.display_name
        # If post is in a subreddit that is already listed, increase the count,
        # otherwise create a new entry.
        if name in subreddits:
            subreddits[name] += 1
        else:
            subreddits[name] = 1

    return subreddits

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('user', type=str, help='User to be checked')
    parser.add_argument('-n', '--nsfw', type=bool, default=False, nargs='?', help='Filter for NSFW subreddits only')
    parser.add_argument('-a', '--amount', type=int, default=10, nargs='?', help='Amount of subreddits to be displayed')
    parser.add_argument('-s', '--search', type=str, default=None, nargs='?', help='Search for particular subreddit instead')
    args = parser.parse_args()

    user = args.user
    nsfw = args.nsfw
    amount = args.amount
    search = args.search

    # MAKE SORT BY NSFW POSTS

    # Dictionary containing {subreddit : number of interactions}
    subreddits = generate_subreddits(user)

    if search != None:
        return (bool(search in subreddits))
    else:
        # Sort dictionary by most interactions
        debug_print('Sorting subreddits...')
        sorted_tuples = sorted(subreddits.items(), key=lambda item: item[1], reverse=True)
        sorted_subreddits = {k: v for k, v in sorted_tuples}
        subreddits_list = list(sorted_subreddits.keys())

        for i in range(min(len(subreddits_list), amount)):
            subreddit = subreddits_list[i]
            print('{}{} interactions'.format((subreddit + ':').ljust(30), str(sorted_subreddits[subreddit]).ljust(5)))

if __name__ == '__main__':
    main()