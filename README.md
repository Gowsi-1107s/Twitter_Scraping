# Twitter_Scraping
Scraping Twitter data using Snscrape Library and Creating GUI using Streamlit

AIM
* To scrape Twitter data using the snscrape library.
* To store the collection in MongoDB.
* To display the scraped data in a GUI built with Streamlit. 
* The scraped data is displayed in the GUI and can be uploaded to the database, downloaded as a CSV or JSON file.

REQUIREMENTS

1) Streamlit
2) Pymongo
3) Pandas
4) Snscrape
5) Python 3
6) MongoDB Compass

PROBLEM

Today, data is scattered everywhere in the world. Especially in social media, there may be a big quantity of data on Facebook, Instagram, Youtube, Twitter, etc. This consists of pictures and films on Youtube and Instagram as compared to Facebook and Twitter. To get the real facts on Twitter, you want to scrape the data from Twitter. You Need to Scrape the data like (date, id, url, tweet content, user,reply count, retweet count,language, source, like count etc) from twitter.

WORKFLOW

STEP 1: 

Installing Libraries and Modules
```
	pip install snscrape 
	pip install pandas 
	pip install streamlit 
```

STEP 2: 

Installing Libraries and Modules
```
	import snscrape.modules.twitter as sntwitter
	import pandas as pd
	import streamlit as st
	import datetime
	import pymongo
	import time
```

STEP 3: 

Required Variables
```
	client = pymongo.MongoClient("mongodb://localhost:27017/")  # To connect to MONGODB
	mydb = client["Twitter_Database"]    # To create a DATABASE
	tweets_df = pd.DataFrame()           # TO create a DATAFRAME
	dfm = pd.DataFrame()
```

STEP 4: 

Navigation is used to create pages
```
	nav = st.sidebar.radio('Navigation',["Home", "Twitter Scraping"])   #TO CREATE SIDEEBAR
if nav == "Home":                              #1ST PAGE
    st.title(':blue[TWITTER_SCRAPING]:sunglasses:')
    st.image('https://images.pexels.com/photos/13240228/pexels-photo-13240228.jpeg?auto=compress&cs=tinysrgb&w=600',width=800,output_format="auto")
    
if nav == "Twitter Scraping":                  #2ND PAGE
    option = st.radio('How would you like to search the data in Twitter?',('Keyword', 'Hashtag'))
    
    word = st.text_input('Please enter a '+option, 'Example: Data Science')
    
    start = st.date_input("Select the start date", datetime.date(2020, 1, 1))
    
    end = st.date_input("Select the end date", datetime.date(2023, 4,4))
    
    num_tweet = st.slider('Number of tweets to scrap', 0, 1000, 5)

tweets_list = []
```

STEP 5: 
I have Created a GUI using streamlit that contains the follwing features

Can enter any keyword or Hashtag to be searched,
select the starting date,
select the ending date,
Number of tweets needs to be scrapped.


STEP 6:

Scraping data using TwitterSearchScraper and TwitterHashtagScraper and a dataframe is created to store the entire scraped data. 
```
# SCRAPE DATA USING TwitterSearchScraper
if word:
    if option=='Keyword':
        for i,tweet in enumerate(sntwitter.TwitterSearchScraper(f'{word} + since:{start} until:{end}').get_items()):
            if i>num_tweet:
                break
            tweets_list.append([tweet.date, tweet.id, tweet.url, tweet.content, tweet.user.username,tweet.replyCount, tweet.retweetCount,tweet.lang, tweet.source, tweet.likeCount])
        tweets_df = pd.DataFrame(tweets_list, columns=['Date', 
                                             'ID', 
                                             'Url', 
                                             'Content',
                                             'Username',
                                             'Reply count', 
                                             'Retweet count',
                                             'Language',
                                             'Source', 
                                             'Like count'])
## SCRAPE DATA USING TwitterHashtagScraper
    else:
        for i,tweet in enumerate(sntwitter.TwitterHashtagScraper(f'{word} + since:{start} until:{end}').get_items()):
            if i>num_tweet:
                break            
            tweets_list.append([ tweet.date, tweet.id, tweet.url, tweet.content, tweet.user.username,tweet.replyCount, tweet.retweetCount,tweet.lang, tweet.source, tweet.likeCount])
        tweets_df = pd.DataFrame(tweets_list, columns=[ 'Date', 
                                             'ID', 
                                             'Url', 
                                             'Content',
                                             'Username',
                                             'Reply count', 
                                             'Retweet count',
                                             'Language',
                                             'Source', 
                                             'Like count'])
```

STEP 7:

Now we can download this scraped data in the form of CSV or JSON format.

STEP 8:

The database connection is established using pymongo.
A new collection will be created and data is uploaded into that collection if the user wish to upload.

STEP 9:

Using snscrape and pandas,Tweets get scraped,converted into Dataframe and displayed in tabular format

STEP 10:

To run the app, Navigate to the folder which app is present using CLI and run the command prompt

```
streamlit run Twitter_Scraping.py
```
