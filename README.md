Random Bluesky related stuff that enables the user to build their own personalized social media algorithm to build their own feed.

The first file - bluesky_algo.py is the main algo script that the user can run (either manually or via cron-job) to pull posts they want to see into a database that feed.py will pull from.
Some simple example "rules" are given (pull from followers if like threshold exceeded, pull popular posts from keywords), but it's up to the user to add their own to determine what they want to see.

You'll want to set up your own SQL database named 'feed_database' to push these favorite posts to & update bluesky_algo.py with your login details. 

The second file app.py is the app where you'll serve your feed from. You'll want your own domain, ideally with a subdomain e.g. feed.mydomain.com. This is where your SQL database and your app will live. 

Other than that, algos will contain the logic that pulls from your database and you'll get your feed's personal DID to add to your app.py file after running publish_feed.py. Will upload in a bit, but to skip ahead, go to https://github.com/MarshalX/bluesky-feed-generator. It's all there in more detail. 
