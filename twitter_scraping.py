import snscrape.modules.twitter as sntwitter
import streamlit as st
import pandas as pds
import pymongo as pymon
from PIL import Image
import io


st.title("Twitter Scraping")
# Twitter Scraping function
maxTweets = 100

# Creating list
scrapingData = []

# @st.experimental_memo
def convert_csv(df):
    return df.to_csv(index=False).encode('utf-8')

# Using TwitterSearchScraper to scrape data and append tweets to list
def ScrapFun(username,srtDate,endDate):
    for i,tweet in enumerate(sntwitter.TwitterSearchScraper(f'from:{username} since:{srtDate} until:{endDate}').get_items()):
        if i>maxTweets:
            break
        scrapingData.append([tweet.id,tweet.user.username,tweet.url,tweet.rawContent,
                         tweet.replyCount,tweet.retweetCount,tweet.likeCount,tweet.lang,
                         tweet.source,tweet.date,])
    
main_option=["Select Mode","Normal","DateRange","LikeCount","Download"]
main_option_input=st.sidebar.selectbox("Enter Scraping Mode",main_option)




if main_option_input=="Normal":
    username=st.text_input('Enter Scrap Username')
    srtDate="2023-01-01"
    endDate="2023-03-10"
    if st.button('Submit'):
        ScrapFun(username,srtDate,endDate)
        st.sidebar.success('Narmal Data Fetch successfully')
elif main_option_input=="DateRange":
    username=st.text_input('Enter Scrap Username')
    srtDate=st.date_input('Start Date')
    endDate=st.date_input('End Date')
    if st.button('Submit'):
        ScrapFun(username,srtDate,endDate)
        st.sidebar.success('DateRang Data Fetch successfully')
elif main_option_input=="LikeCount":
    username=st.text_input('Enter Scrap Username')
    srtDate=st.date_input('Start Date')
    endDate=st.date_input('End Date')
    if st.button('Submit'):
        ScrapFun(username,srtDate,endDate)
        st.sidebar.success('LikeCount Data Fetch successfully')
elif main_option_input=="Download":
    username=st.text_input('Enter Scrap Username')
    srtDate="2023-01-01"
    endDate="2023-03-10"
    ScrapFun(username,srtDate,endDate)
    frameData = pds.DataFrame(scrapingData, columns=['Tweet Id','Username', 'URL', 'Content', 'Replay Count', 
                                                    'Re Tweet', 'Like Count', 'Lang', 'Source','Datetime'])
    csvFile=convert_csv(frameData)
    st.download_button("Doenload Here",csvFile,"myCsv-Sureshkumar_offl.csv","text/csv",key="download-csv")
    st.sidebar.success('Download successfully')
    
else:
    print("Mayava Error")    
# im =Image.open("https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.pngmart.com%2Fimage%2Ftag%2Felon-musk&psig=AOvVaw3MWZBUAaEHXuiYtQbZJoV3&ust=1678434793878000&source=images&cd=vfe&ved=0CA8QjRxqFwoTCNCKyf-uzv0CFQAAAAAdAAAAABAR")

# st.image(im)    
# Pandas DataFrame convertion
frameData = pds.DataFrame(scrapingData, columns=['Tweet Id','Username', 'URL', 'Content', 'Replay Count', 
                                                    'Re Tweet', 'Like Count', 'Lang', 'Source','Datetime'])

# MongoDB Connection
myclient = pymon.MongoClient("mongodb+srv://mayava:321@cluster0.fvvlr3f.mongodb.net")
db=myclient.mongocluster
rectwt=db.demotweet


# to_dict() method syntax
myDict=frameData.to_dict('list')
rectwt.insert_one(myDict)



frameData









