import os
from praw import Reddit, models
from prawcore import exceptions
from collections import Counter
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

def generate_subreddits(user: str, nsfw: bool) -> Counter:
    '''
    Gather all subreddits the user has commented and posted in,
    and merge the two counters together.
    '''

    redditor = reddit.redditor(user)
    # redditor._fetch()

    # Make sure username is a valid account
    try:
        redditor.id
    except exceptions.NotFound:
        print('Error: u/{} not found'.format(user))
        exit(-1)

    debug_print('Generating subreddits...')
    comment_subs = search_comments(redditor, nsfw)
    post_subs = search_posts(redditor, nsfw)

    debug_print('Merging post and comment history...')
    subreddits = Counter(comment_subs)
    subreddits.update(post_subs)

    return subreddits

def search_comments(redditor: models.Redditor, nsfw: bool) -> Counter:
    '''
    Iterate through all comments made by the user and count the subreddits
    '''

    debug_print('Fetching u/{}\'s comments...'.format(redditor))
    comments = redditor.comments.new(limit=None)

    debug_print('Converting comments to subreddits...')
    # this part is the weak link
    if nsfw:
        subreddit_names = [comment.subreddit.display_name for comment in comments if comment.subreddit.over18]
    else:
        subreddit_names = [comment.subreddit.display_name for comment in comments]

    debug_print('Counting subreddits...')
    subreddits = Counter(subreddit_names)

    return subreddits

def search_posts(redditor: models.Redditor, nsfw: bool) -> Counter:
    '''
    Iterate through all posts made by the user and count the subreddits.
    '''

    debug_print('Fetching u/{}\'s posts...'.format(redditor))
    posts = redditor.submissions.new(limit=None)

    debug_print('Converting posts to subreddits...')
    if nsfw:
        subreddit_names = [post.subreddit.display_name for post in posts if post.subreddit.over18]
    else:
        subreddit_names = [post.subreddit.display_name for post in posts]

    debug_print('Counting subreddits...')
    subreddits = Counter(subreddit_names)

    return subreddits

def main():
    parser = ArgumentParser()
    parser.add_argument('user', type=str, help='User to be checked')
    parser.add_argument('-n', '--nsfw', action='store_true', help='Filter for NSFW subreddits only')
    parser.add_argument('-a', '--amount', type=int, default=10, help='Amount of subreddits to be displayed')
    parser.add_argument('-s', '--search', type=str, default=None, help='Search for particular subreddit instead')
    args = parser.parse_args()

    '''
    IMPROVEMENTS:
    - allow --amount to be none, which will then list all subreddits
    - maybe allow for an option to split up posts and comments
    '''

    user = args.user
    nsfw = args.nsfw
    amount = args.amount
    search = args.search

    # Clean up username
    if 'u/' in user or '/u/' in user:
        user = user.removeprefix('/')
        user = user.removeprefix('u/')

    # Disregard other print statements for search mode
    if search != None:
        global DEBUG
        DEBUG = False
        
        # Clean up subreddit
        if 'r/' in search or '/r/' in search:
            search = search.removeprefix('/')
            search = search.removeprefix('r/')

    # Dictionary containing {subreddit : number of interactions}
    subreddits = generate_subreddits(user, nsfw)

    if search != None:
        if search in subreddits:
            print('u/{} has interacted with r/{} {} times.'.format(user, search, subreddits[search]))
        else:
            print('u/{} does not have any activity in r/{}.'.format(user, search))
    else:
        sorted_subreddits = subreddits.most_common()
        for subreddit in sorted_subreddits[:min(len(sorted_subreddits), amount)]:
            print('{} {} interactions'.format(
                (subreddit[0] + ':').ljust(len(max((x[0] for x in sorted_subreddits), key=len)) + 1),
                str(subreddit[1]).ljust(len(str(sorted_subreddits[0][1])))
            ))

if __name__ == '__main__':
    main()