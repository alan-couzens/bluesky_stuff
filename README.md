# Bluesky: Build your own personalized social media algo

**Random Bluesky related stuff that enables the user to build their own personalized social media algorithm that pulls posts according to whatever customized "rules" the user defines into their own feed.**

The first file - bluesky_algo.py is the main algo script that the user can run (either manually or via cron-job) to pull posts they want to see into a database that feed.py will pull from.
Some simple example "rules" are given (pull from followers if like threshold exceeded, pull popular posts from keywords), but it's up to the user to add their own to determine what they want to see. This is the fun bit! :)

You'll want to set up your own SQL database named 'feed_database' to push these favorite posts to & update bluesky_algo.py with your login details. The required columns in your db are: uri, cid, reply_parent, reply_root, indexed_at (see notes on feed.py below)

The second file app.py is the app where you'll serve your feed from. You'll want your own domain, ideally with a subdomain e.g. feed.mydomain.com. This is where your SQL database and your app will live. 

You can use something like PythonAnywhere to host your app for ~$5/mo. Thye make deploying a flask app to the web super easy (https://help.pythonanywhere.com/pages/Flask/)

The app.py file serves 3 endpoints that Bluesky needs to be able to publish the posts from your database as a web feed. Once these endpoints are live on your server, you'll be able to view your personalized feed of posts that are pulled according to your own algorithm's rules under feeds on the site...
![bsky_my_feed](https://github.com/user-attachments/assets/e139ed13-aa64-4839-8a58-4e0d7e9a0d08)


The algos folder contains the logic to build the feed from your database into the format that Bluesky needs. Your database will need to match the columns shown in feed.py (uri, cid, reply_parent, reply_root, indexed_at)

The final step is to publish your feed via publish_feed.py. To do this, go into the .env file, replace all the variables with your details - what you want to call your feed etc. The publish_feed.py file will pull from the info you provide here. Once you run publish_feed.py (as a one time deal) it will return a unique DID for your feed. Once you've got this, go back into your app.py file and plug that DID into the feed_url variable. 

Once you've done that, you can serve your app.py file from your server and your personalized algorithmic feed will just magically show up on your Bluesky app. Every time you run your bluesky_algo.py script (either manually or via cronjob) it will pull new posts into your database and they will be served to your feed. You can change the rules in bluesky_algo.py as you go in accordance with your preferences. 

That's pretty much it! For more detail & a slightly different approach (that pulls feeds into your DB directly from the "Firehose" of all posts), check out https://github.com/MarshalX/bluesky-feed-generator
