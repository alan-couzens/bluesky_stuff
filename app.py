from flask import Flask, jsonify, request

from algos import algos

app = Flask(__name__)


@app.route('/')
def index():
    return 'ATProto Feed Generator powered by The AT Protocol SDK for Python (https://github.com/MarshalX/atproto).'


@app.route('/.well-known/did.json', methods=['GET'])
def did_json():
    service_did = ' ' #This is the DID for the service from when you run publish_feed.py
    hostname = ' ' #This is wherever you're running the feed from e.g. feed.mydomain.com
    return jsonify({
        '@context': ['https://www.w3.org/ns/did/v1'],
        'id': service_did,
        'service': [
            {
                'id': '#bsky_fg',
                'type': 'BskyFeedGenerator',
                'serviceEndpoint': 'https://'+ hostname
            }
        ]
    })


@app.route('/xrpc/app.bsky.feed.describeFeedGenerator', methods=['GET'])
def describe_feed_generator():
    service_did = ' ' #This is the DID for the service from when you run publish_feed.py
    hostname = ' ' #This is wherever you're running the feed from e.g. feed.mydomain.com
    feeds = [{'uri': uri, 
            "title": "My Awesome Feed", #This is the title of the feed
            "description": "Personal feed of me"} for uri in algos.keys()]
    response = {
        'did': service_did,
        'feeds': feeds 
    }
    return jsonify(response)


@app.route('/xrpc/app.bsky.feed.getFeedSkeleton', methods=['GET'])
def get_feed_skeleton():
    feed = request.args.get('feed', default=None, type=str)
    algo = algos.get(feed)
    if not algo:
        return 'Unsupported algorithm', 400
    try:
        cursor = request.args.get('cursor', default=None, type=str)
        limit = request.args.get('limit', default=20, type=int)
        body = algo(cursor, limit)
    except ValueError:
        return 'Malformed cursor', 400
    return jsonify(body)


if __name__ == '__main__':
    app.run()