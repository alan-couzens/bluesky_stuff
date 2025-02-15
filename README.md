Random Bluesky related stuff that enables the user to build their own personalized social media algorithm to build their own feed.

The first file - bluesky_algo.py is the main algo script that the user can run (either manually or via cron-job) to pull posts they want to see into a database that feed.py will pull from.
Some simple example "rules" are given (pull from followers if like threshold exceeded, pull popular posts from keywords), but it's up to the user to add their own to determine what they want to see.

You'll want to set up your own SQL database named 'feed_database' to push these favorite posts to & update bluesky_algo.py with your login details. 

That's it for this part. Will add feed.py and the Flask app to serve your feed in a bit. 
