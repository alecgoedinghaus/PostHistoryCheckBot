from collections import Counter
import os
from xml.dom import NotFoundErr
from praw import Reddit
from prawcore import exceptions
from argparse import ArgumentParser

DEBUG = True

client_id = os.environ['PERSONAL_USE_SCRIPT']
client_secret = os.environ['SECRET']
user_agent = os.environ['USER_AGENT']

reddit = Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent=user_agent
)

def debug_print(message):
    if DEBUG:
        print(message)

def generate_subreddits(user, nsfw):
    '''
    Gather all subreddits the user has commented and posted in,
    and merge the two counters together.
    '''

    redditor = reddit.redditor(user)

    # Make sure username is a valid account
    try:
        redditor.id
    except exceptions.NotFound:
        print('Error: user {} not found'.format(user))
        exit(-1)

    debug_print('Generating subreddits...')
    comment_subs = search_comments(redditor, nsfw)
    post_subs = search_posts(redditor, nsfw)

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

def search_comments(redditor, nsfw):
    '''
    Iterate through all comments made by the user and count the subreddits
    '''

    debug_print('Gathering all comments...')
    comments = redditor.comments.new(limit=None)

    debug_print('Converting comments to subreddits...')
    if nsfw:
        subreddit_names = [comment.subreddit.display_name for comment in comments if comment.subreddit.over18]
    else:
        subreddit_names = [comment.subreddit.display_name for comment in comments]

    debug_print('Counting subreddits...')
    subreddits = Counter(subreddit_names)

    return subreddits

def search_posts(redditor, nsfw):
    '''
    Iterate through all posts made by the user and count the subreddits.
    '''

    debug_print('Searching through all posts...')

    subreddits = dict()
    for post in redditor.submissions.new(limit=None):
        name = post.subreddit.display_name

        debug_print('Found post in r/{}, adding to dictionary...'.format(name))

        # If post is in a subreddit that is already listed, increase the count,
        # otherwise create a new entry.
        if nsfw:
            if post.subreddit.over18:
                if name in subreddits:
                    subreddits[name] += 1
                else:
                    subreddits[name] = 1
        else:
            if name in subreddits:
                subreddits[name] += 1
            else:
                subreddits[name] = 1

        debug_print('Successfully added to dictionary...')

    return subreddits

def main():
    parser = ArgumentParser()
    parser.add_argument('user', type=str, help='User to be checked')
    parser.add_argument('-n', '--nsfw', type=bool, default=False, nargs='?', help='Filter for NSFW subreddits only')
    parser.add_argument('-a', '--amount', type=int, default=10, nargs='?', help='Amount of subreddits to be displayed')
    parser.add_argument('-s', '--search', type=str, default=None, nargs='?', help='Search for particular subreddit instead')
    args = parser.parse_args()

    user = args.user
    nsfw = args.nsfw
    amount = args.amount
    search = args.search

    # Dictionary containing {subreddit : number of interactions}
    subreddits = generate_subreddits(user, nsfw)

    if search != None:
        return (bool(search in subreddits))
    else:
        # Sort dictionary by most interactions
        debug_print('Sorting subreddits...')
        sorted_tuples = sorted(subreddits.items(), key=lambda item: item[1], reverse=True)
        sorted_subreddits = {k: v for k, v in sorted_tuples}
        subreddits_list = list(sorted_subreddits.keys())

        # change to: for subreddit in ... then slice list for min of two values
        for i in range(min(len(subreddits_list), amount)):
            subreddit = subreddits_list[i]
            print('{} {}{} interactions'.format((str(i + 1) + '.').ljust(5),
                                                (subreddit + ':').ljust(30),
                                                str(sorted_subreddits[subreddit]).ljust(5)))

if __name__ == '__main__':
    main()