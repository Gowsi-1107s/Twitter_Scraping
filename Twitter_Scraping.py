import pandas as pd
import streamlit as st
import snscrape.modules.twitter as sntwitter
import datetime
import time
import pymongo

Client = pymongo.MongoClient("mongodb://localhost:27017/")
db = Client["Twitter_Scraping"]

tweets_df = pd.DataFrame()
df = pd.DataFrame()


st.header(':blue[TWITTER_SCRAPING]')
st.image('https://images.pexels.com/photos/13240228/pexels-photo-13240228.jpeg?auto=compress&cs=tinysrgb&w=600',width=400,output_format="auto")
choice = st.radio(label='How would you like to search the data?',options=['Keyword', 'Hashtag'])
word = st.text_input('Please enter a '+choice, 'Example: Data Science')
start_date = st.date_input("Select the start date", datetime.date(2023, 1, 1))
end_date = st.date_input("Select the end date", datetime.date(2023, 4, 4))
num_tweet = st.slider('How many tweets to scrape', 0, 1000, 10)
tweets_list = []


if word:
    if choice == "Keyword":
        for i,tweet in enumerate(sntwitter.TwitterSearchScraper(f'{word} + since:{start_date} until:{end_date}').get_items()):
            if i>num_tweet:
                break
            tweets_list.append([tweet.id, tweet.date,  tweet.content, tweet.lang, tweet.user.username, tweet.replyCount, tweet.retweetCount,tweet.likeCount, tweet.source, tweet.url ])
        tweets_df = pd.DataFrame(tweets_list, columns=['ID','Date','Content', 'Language', 'Username', 'ReplyCount', 'RetweetCount', 'LikeCount','Source', 'Url'])
    else:
        for i,tweet in enumerate(sntwitter.TwitterHashtagScraper(f'{word} + since:{start_date} until:{end_date}').get_items()):
            if i>num_tweet:
                break            
            tweets_list.append([ tweet.id, tweet.date,  tweet.content, tweet.lang, tweet.user.username, tweet.replyCount, tweet.retweetCount,tweet.likeCount, tweet.source, tweet.url ])
        tweets_df = pd.DataFrame(tweets_list, columns=['ID','Date','Content', 'Language', 'Username', 'ReplyCount', 'RetweetCount', 'LikeCount','Source', 'Url'])
else:
    st.warning(choice,' cant be empty', icon="⚠️")

@st.cache_data
def convert_df(df):    
    return df.to_csv().encode('utf-8')

if not tweets_df.empty:
    col1,col2,col3 = st.columns(3)
    with col1:
        csv = convert_df(tweets_df)
        st.download_button(label="Download data as CSV",data=csv,file_name='Twitter_Scraping.csv',mime='text/csv',)
        
    with col2:
        json_string = tweets_df.to_json(orient ='records')
        st.download_button(label="Download data as JSON",file_name="Twitter_Scraping.json",mime="application/json",data=json_string,)
        
    with col3:
        if st.button('Upload Data to MongoDB Database'):
            coll=word
            coll=coll.replace(' ',' ')
            mycollection=db[coll]
            dict=tweets_df.to_dict('records')
            if dict:
                mycollection.insert_many(dict) 
                ts = time.time()
                mycollection.update_many({}, {"$set": {"KeyWord_or_Hashtag": word+str(ts)}}, upsert=False, array_filters=None)
                st.success('Successfully uploaded to database', icon="✅")
                st.balloons()
            else:
                st.warning('Cant upload because there are no tweets', icon="⚠️")

if st.button('Show Data'):
    st.write(tweets_df)
    st.snow()

with st.expander("click me"):
    st.write(
        "Thank you!!!"
        "Hope you enjoyed Twitter Scraping.")
    


