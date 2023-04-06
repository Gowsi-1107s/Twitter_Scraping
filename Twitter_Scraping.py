import snscrape.modules.twitter as sntwitter
import pandas as pd
import streamlit as st
import datetime
import pymongo
import time

# REQUIRED VARIABLES
client = pymongo.MongoClient("mongodb://localhost:27017/")  # To connect to MONGODB
mydb = client["Twitter_Database"]    # To create a DATABASE
tweets_df = pd.DataFrame()           # TO CREATE a DATAFRAME
dfm = pd.DataFrame()

# NAVIGATION

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
else:
    st.warning(option,' cant be empty', icon="⚠️")
# DOWNLOAD AS CSV
@st.cache_data # IMPORTANT: Cache the conversion to prevent computation on every rerun
def convert_df(df):    
    return df.to_csv().encode('utf-8')

    # DOWNLOAD AS CSV
if not tweets_df.empty:
    csv = convert_df(tweets_df)
    st.download_button(label="Download data as CSV",data=csv,file_name='Twitter_Scraping.csv',mime='text/csv',)
   
    
    # DOWNLOAD AS JSON
    json_string = tweets_df.to_json(orient ='records')
    st.download_button(label="Download data as JSON",file_name="Twitter_Scraping.json",mime="application/json",data=json_string,)

    # UPLOAD DATA TO DATABASE
    if st.button('Upload Tweets to Database'):
        coll=word
        coll=coll.replace(' ','_')+'_Tweets'
        mycoll=mydb[coll]
        dict=tweets_df.to_dict('records')
        if dict:
            mycoll.insert_many(dict) 
            ts = time.time()
            mycoll.update_many({}, {"$set": {"KeyWord_or_Hashtag": word+str(ts)}}, upsert=False, array_filters=None)
            st.success('Successfully uploaded to database', icon="✅")
            st.balloons()
        else:
            st.warning('Cant upload because there are no tweets', icon="⚠️")

    # SHOW TWEETS
    if st.button('Show Data'):
        st.write(tweets_df)
        st.snow()


            

