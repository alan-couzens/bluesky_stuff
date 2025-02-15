import pymysql
from datetime import datetime
from typing import Optional

uri = #put your feed URI that you get from publish_feed.py here
CURSOR_EOF = 'eof'


def handler(cursor: Optional[str], limit: int) -> dict:
    db = pymysql.connect() #put your login details for your sql database here
    db_cursor = db.cursor()
    query = "SELECT * FROM feed_database ORDER BY indexed_at DESC LIMIT " + str(limit)
    db_cursor.execute(query)
    posts = []
    for row in db_cursor:
        post = {}
        post['uri'] = row[1]
        post['cid'] = row[2]
        post['reply_parent'] = row[3]
        post['reply_root'] = row[4]
        post['indexed_at'] = row[5]
        posts.append(post)
    if cursor:
        if cursor == CURSOR_EOF:
            return {
                'cursor': CURSOR_EOF,
                'feed': []
            }
        cursor_parts = cursor.split('::')
        if len(cursor_parts) != 2:
            raise ValueError('Malformed cursor')

        indexed_at, cid = cursor_parts
        indexed_at = datetime.fromtimestamp(int(indexed_at) / 1000)
        #posts = posts.where(((Post.indexed_at == indexed_at) & (Post.cid < cid)) | (Post.indexed_at < indexed_at))
        query = "SELECT * FROM feed_database WHERE (indexed_at = '{}' AND cid < '{}') OR indexed_at < '{}' ORDER BY indexed_at DESC LIMIT {}".format(indexed_at, cid, indexed_at, limit)
        db_cursor.execute(query)
        posts = []
        for row in db_cursor:
            post = {}
            post['uri'] = row[1]
            post['cid'] = row[2]
            post['reply_parent'] = row[3]
            post['reply_root'] = row[4]
            post['indexed_at'] = row[5]
            posts.append(post)
    #print("Posts")
    #print(posts)
    feed = [{'post': post['uri']} for post in posts]

    cursor = CURSOR_EOF
    last_post = posts[-1] if posts else None
    if last_post:
        cursor = "{}::{}".format(int(last_post['indexed_at'].timestamp() * 1000), last_post['cid'])
    #print("cursor")
    #print(cursor)
    #print(feed)
    return {
        'cursor': cursor,
        'feed': feed
    }

