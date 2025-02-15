import json
import pprint
import random
import pymysql
import datetime
from atproto import Client

def get_user_did(client, handle):
    """Get user did from a handle. Used later to pull fave follows from handles"""
    profile = client.app.bsky.actor.get_profile(params={'actor': handle})
    user_did = profile.did
    print(f"User DID: {user_did}")
    return user_did
    
def pull_followers_for_user(client, did):
    """Pulls followers for a user."""
    results = client.app.bsky.graph.get_follows(params={'actor': did})
    dids = []
    pull_followers_for_user.follower_names = []
    for follow in results.follows:
        print(f"Follow: {follow}")
        print(f"Follow: {follow.did}")
        print(f"Follow: {follow.display_name}")
        dids.append(follow.did)
        pull_followers_for_user.follower_names.append(follow.display_name)
    return dids

def pull_posts_with_x_likes_from_did(client, did, likes_threshold):
    """Pulls last 10 posts from a user's feed and returns the uri for those with more than x likes."""
    acceptable_posts = []
    response = client.app.bsky.feed.get_author_feed(params={'actor': did, 'limit': 10})
    try:
        feed_dict = json.loads(response.json())
    except AttributeError:
        try:
            feed_dict = json.loads(response.text)
        except json.JSONDecodeError:
            feed_dict = json.loads(response.data)
    pprint.pprint(feed_dict)
    feed_list = feed_dict.get('feed', [])
    for index, feed_item in enumerate(feed_list, start=1):
        post = feed_item.get('post', {})
        uri = post.get('uri', '')
        likes = post.get('like_count', 0)
        cid = post.get('cid', '')
        record = post.get('record', {})
        text = record.get('text', '')
        #sanitize for sql insert
        text = text.replace("'", "''")
        post_image = record.get('embed', None)
        #Sanitize for sql insert
        post_image = str(post_image).replace("'", "''")
        #likes = client.app.bsky.feed.get_likes(params={'uri': uri})
        print(f"Post Text: {text}")
        print(f"Post Likes: {likes}")
        if likes >= likes_threshold:
            print(f"Acceptable post by likes: {text}")
            print("Number of likes:", likes)
            reply_root = reply_parent = None
            try:
                reply_root = record.reply.root.uri
                reply_parent = record.reply.parent.uri
            except AttributeError:
                pass
            acceptable_posts.append({'uri': uri, 'cid': cid, 'reply_parent': reply_parent, 'reply_root': reply_root, 'post_text': text, 'likes': likes, 'keyword': None, 'user': did, 'post_image': post_image})
    print(f"Acceptable posts for did: {did}: {acceptable_posts}")
    return acceptable_posts

def pull_posts_with_x_likes_from_keyword_search(client, keywords, block_words):
    """Pulls last 10 posts from a keyword search and returns the uri for those with the most likes as long as they don't contain a block word."""
    acceptable_posts = []
    today = datetime.datetime.utcnow().date()
    today_string = today.isoformat()  # e.g. "2025-01-12"
    # or build a full ISO8601 string:
    today_full_string = f"{today_string}T00:00:00.000Z"
    seven_days_ago = today - datetime.timedelta(days=7)
    seven_days_ago_string = seven_days_ago.isoformat()  # "2025-01-05"
    seven_days_ago_full_string = f"{seven_days_ago_string}T00:00:00.000Z"
    trump = 0
    for keyword in keywords:
        #Get top 10 posts from each keyword for the past 7 days (that don't contain block words)
        posts = client.app.bsky.feed.search_posts(params={'q': keyword, 'sort':'top', 'since': seven_days_ago_full_string, 'until': today_full_string, 'limit': 10})
        print(f"Posts for keyword: {keyword}: {posts}")
        for post in posts.posts:
            #Mental health adjustment for the day
            if "Trump" in post.record.text:
                trump = trump+1
            if trump > 10:
                print("Blocked Trump post")
            elif any(block_word in post.record.text for block_word in block_words):
                print("Blocked post")
            else:
                print(f"Acceptable keyword post for keyword: {keyword}: {post}")
                post_text = post.record.text
                embed = post.record.embed
                print(f"Embed Type: {type(embed)}")
                pprint.pprint(embed)
                print("\n" + "-"*50 + "\n")
                if post.record.embed:
                    post_image = post.record.embed
                else:
                    post_image = None
                #sanitize for sql insert
                post_text = post_text.replace("'", "''")
                post_image = str(post_image).replace("'", "''")
                reply_root = reply_parent = None
                if post.record.reply:
                    reply_root = post.record.reply.root.uri
                    reply_parent = post.record.reply.parent.uri
                acceptable_posts.append({'uri': post.uri, 'cid': post.cid, 'reply_parent': reply_parent, 'reply_root': reply_root, 'post_text': post.record.text, 'likes': post.like_count, 'keyword': keyword, 'user': post.author.did, 'post_image': post_image})
    return acceptable_posts

if __name__ == '__main__':
    #Login
    client = Client()
    profile = client.login() #Add your own login details here 'user', 'password'
    #Build list of fave follows to pull all posts from
    fave_follows = ['some_dude.bsky.social', 'another_dude_I_like.bsky.social', 'that_other_person.bsky.social'] #Replace with your own fave follows
    fave_dids = []
    for follow in fave_follows:
        fave_dids.append(get_user_did(client, follow))
    print(f"Fave DIDs: {fave_dids}")
    #Pull posts with more than 10 likes from direct follows (They're not all Bangers! :) & pull all posts from fave follows
    my_follows = pull_followers_for_user(client, client.me.did)
    print(f"My follows: {my_follows}")
    good_posts_from_all_follows = []
    for follow in my_follows:
        try:
            if follow in fave_dids:
                good_post_from_follows = pull_posts_with_x_likes_from_did(client, follow, 0) #Pull all posts from fave follows
                print(f"Fave Post: {good_post_from_follows}")
            else:
                good_post_from_follows = pull_posts_with_x_likes_from_did(client, follow, 10) #Pull posts with more than 10 likes from other follows
            good_posts_from_all_follows.extend(good_post_from_follows)
        except Exception as e:
            print(f"Error: {e}")
    print("Good posts from all follows:", good_posts_from_all_follows)

    #Option: Pull posts with more than 50 likes from follows of follows.

    #Pull top posts from the last 7 days from keyword search (REPLACE WITH YOUR OWN KEYWORDS - whatever you're interested in)
    keywords = ['machine learning', 'python', 'data science', 'artificial intelligence', 'physiology', 'psychology', 'triathlon', 'yoga', 'cybersecurity', 'health']
    block_words = ['porn', 'nsfw', 'naked'] #Replace with your own block words - anything you don't want to see
    good_posts_from_keywords = pull_posts_with_x_likes_from_keyword_search(client, keywords, block_words)
    #Note: Can also search by tag

    #Pull good posts from folks you follow and good posts from your keyword search together
    good_posts_total = good_posts_from_all_follows + good_posts_from_keywords
    #Mix up the order of the posts so you don't get a stack of posts from the same person in order
    random.shuffle(good_posts_total)
    print("Good posts total:", good_posts_total)
    print(f"Number of good posts: {len(good_posts_total)}")
    new_posts_added_to_db = 0
    #Add acceptable posts to database that I can build my feed from.
    db = pymysql.connect() #Add your own database connection here
    cursor = db.cursor()
    for post in good_posts_total:
        #Check if post already exists in database, don't add if it does
        #existing_post = Post.get_or_none(Post.uri == post['uri'])
        query = f"SELECT * FROM feed_database WHERE uri = '{post['uri']}'"
        cursor.execute(query)
        existing_post = cursor.fetchone()
        if existing_post:
            print(f"Post already exists: {existing_post}")
        else:
            #Add post to database
            indexed_at = datetime.datetime.utcnow().isoformat()
            #parameterize query so that it's not vulnerable to SQL injection and can handle special characters
            query = "INSERT INTO feed_database (uri, cid, reply_parent, reply_root, indexed_at, post_text, likes, keyword, user, post_image) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            values = (post['uri'], post['cid'], post['reply_parent'], post['reply_root'], indexed_at, post['post_text'], post['likes'], post['keyword'], post['user'], post['post_image'])
            cursor.execute(query, values)
            print(f"New post added: {query}")
            new_posts_added_to_db += 1
    db.commit()
    print(f"New posts added to database: {new_posts_added_to_db}")   
