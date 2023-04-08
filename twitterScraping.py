#using streamlit creating UI
#importing all the depencies
from snscrape.modules import twitter
import pandas as pd
import datetime as dt
import streamlit as st
import pymongo
from pymongo import MongoClient

#connecting mongodb creating collectionname using mongoclient
client = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
mydb = client['TwitterScrape']
#mydb.twitterCollection.delete_many({})
collect = mydb.twitterCollection
    
#main function starts
def twitterscrapping():
    if 'key' not in st.session_state:
        st.session_state['key'] = 0
    tweetlist = [] 
    dfTwitter = pd.DataFrame()
    details={}
    recordsdict = {}
    st.title(":blue[Twitter Scrapping]")
    #st.sidebar['Home','Search','Result','Result']
    tab1, tab2, tab3 = st.tabs(["Home", "Search", "Results"])

    with tab1: #Description of Twitter Scrapping,snscrape,MongoDB
        st.write("**:green[Go to Search tab to scrape twitter data]**")

        st.subheader("Twitter Scrapping")
        st.text("This Twitter Scrapping website is developed to extract upto 1000 twitter data \nfrom public Twitter accounts using snscrape library in python and store the\nrecords in mongoDB")

        st.subheader("snscrape")        
        st.text("snscrape is a scraper for social networking services (SNS)\nIt scrapes things like user profiles, hashtags, or searches and returns the discovered\nitems, e.g. the relevant posts. The following services are currently supported:\nFacebook: user profiles, groups, and communities (aka visitor posts)")

        st.subheader("MongoDB")        
        st.text("MongoDB is a non-relational document database that provides support for JSON-like\nstorage. The MongoDB database has a flexible data model that enables you to\nstore unstructured data, and it provides full indexing support, and replication\nwith rich and intuitive APIs.")

    with tab2:
        with st.form(key='myform1'):
            st.subheader(" Search Tweets")
            #1) form inputs from user
            #getting the hashtag or keyword from the user
            st.write("**Enter the User or Hashtag to search (Eg: elonmusk or #elonmusk)**:red[*]")
            Keyword = st.text_input(label="User or Hashtag: ")

            #getting the no of records to be scrapped from the user
            st.write("**Enter no of records to be scrapped, maximum: 1000**:red[*]")
            number = st.number_input(label="Enter the No of records to scrape: ",min_value = 0, max_value = 1000, step = 10)

            st.write("**select the start date and end date**:red[*]")
            sdate = st.date_input(label="Since",key="sdate")
            edate = st.date_input(label="Untill",key="edate")
            #Submitting all the values
            submitt = st.form_submit_button(label='Start Scrape')

            #2)scrape data using twitter.TwitterSearchScraper() method. fetching the scrapped data and append it in list. 
            #created Df using pandas with list 
            query = f'{Keyword}+ since:{sdate} until:{edate}'
            
            if submitt:
                if sdate != edate and sdate < edate:
                        if Keyword != "" and number!= 0:
                            for i,tweet in enumerate(twitter.TwitterSearchScraper(query).get_items()):
                                if i>number:
                                    break

                                #append the results in tweetlist
                                tweetlist.append([tweet.date,tweet.id,tweet.url,tweet.rawContent,tweet.user.username,tweet.replyCount,
                                    tweet.retweetCount,tweet.lang,tweet.source,tweet.likeCount])

                            #create a pandas dataframe named dfTwitter
                            dfTwitter = pd.DataFrame(tweetlist, columns=['date','id','url','content','userName','replyCount','retweetCount','language','source','likeCount'])  

                            details = {"ScrapedWord":Keyword,
                                       "ScrapedDate":dt.date.today().strftime("%m/%d/%Y"),
                                       "ScrapedData":"{} Scraped twitter data from {} to {}".format(number+1,sdate,edate)
                                       }
                            #converting dataframe into dictionary format
                            recordsdict = dfTwitter.to_dict(orient='records') 
                            #writing in the web page
                            st.markdown(f"No.of records scrapped:{len(tweetlist)}")
                            st.write("**:green[*Please see Results tab for scrapped records]**")             
                        else:
                            st.write("**:red[*Please fill mandatory fields]**") 
                else:
                    st.write(":red[start date cannot be more than current date\nstart date ennd date cannot be same]" ) 

            #To download
            @st.cache_data  
            def convert_csv(df):  #function to convert DF to CSV
                # IMPORTANT: Cache the conversion to prevent computation on every rerun
                return df.to_csv().encode('utf-8')
            def convert_json(df):#convert into json form
                jsonfile = df.to_json(orient="records")
                return jsonfile
            
    with tab3:
        if dfTwitter.empty==False:
            collect.delete_many({}) #deleting existing records
            if collect.insert_one(details) and collect.insert_many(recordsdict):
                st.write("**Records uploaded into MongoDB successfully!!!**")
            st.dataframe(dfTwitter)#displaying the dataframe in web page
        else:
            st.write("Scraped record to be shown here...")
        
    with st.sidebar:
                
            if st.header("Download as CSV"):
                csv = convert_csv(dfTwitter)
                st.download_button(
                label="Download data as CSV",
                data=csv,
                file_name='twitt_csv.csv',
                mime='text/csv',
                )
                
                
            if st.header("Download as json"):
                recordjson = convert_json(dfTwitter)
                st.download_button(
                label="Download data as json",
                data=recordjson,
                file_name='twitt_json.json',
                mime='application/json',
                )
                
                                               
twitterscrapping()   

