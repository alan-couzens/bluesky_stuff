#Bluesky: Build your own personalized social media algo

**Random Bluesky related stuff that enables the user to build their own personalized social media algorithm on their own feed.**

The first file - bluesky_algo.py is the main algo script that the user can run (either manually or via cron-job) to pull posts they want to see into a database that feed.py will pull from.
Some simple example "rules" are given (pull from followers if like threshold exceeded, pull popular posts from keywords), but it's up to the user to add their own to determine what they want to see. This is the fun bit! :)

You'll want to set up your own SQL database named 'feed_database' to push these favorite posts to & update bluesky_algo.py with your login details. The required columns in your db are: uri, cid, reply_parent, reply_root, indexed_at (see notes on feed.py below)

The second file app.py is the app where you'll serve your feed from. You'll want your own domain, ideally with a subdomain e.g. feed.mydomain.com. This is where your SQL database and your app will live. 

You can use something like PythonAnywhere to host your app for ~$5/mo. Thye make deploying a flask app to the web super easy (https://help.pythonanywhere.com/pages/Flask/)

The app.py file serves 3 endpoints that Bluesky needs to be able to publish the posts from your database as a web feed (which you'll be able to view under your feeds on the site)...
![bsky_my_feed](https://github.com/user-attachments/assets/e139ed13-aa64-4839-8a58-4e0d7e9a0d08)

The algos folder contains the logic to build the feed from your database into the format that bluesky needs. Your database will need to match the columns shown in feed.py (uri, cid, reply_parent, reply_root, indexed_at)

The final step is to publish your feed via publish_feed.py and add the DID that you get back to your app.py (you only have to do this once). Will upload publish_feed.py in a bit, but to skip ahead just go to https://github.com/MarshalX/bluesky-feed-generator where the whole process is outlined in more detail.  
