# TwitterScrpingbySan
_Basic workflow:
	Created a python file 
	Imported all the dependencies
	Using Streamlit API, Created GUI with tabs(Home, Search, Results) and sidebar
	Home:
		it contains defintion for twitter scraping, snscrape, streamlit and mongodb
	Search:
	 	it contains the 	feature to enter the keyword or Hashtag to be searched, select the date range and limit the tweet count need to be scraped.
	Results:
		it dispalys the scrapped results in dataframe format
	Sidebar:
		it contains download button to download the records in various type format (Eg: csv, json)

_Execution:
	Installed the streamlit library using pip install streamlit in command prompt
	started to run the python program by command, streamlit run home.py
	directed to the browser page where the streamlit GUI present.
	in search tab, entered the required features without fail and hit the submit button.
	it internally checks for the inputs entered, scraping starts once all the required features entered are correct.
	By using the “snscrape” Library, Scraped the twitter data from Twitter by passing the Features to the TwitterSearchScraper(features) method. 
	TwitterSearchScraper() method scraped the twitter data for the given features and appended the records into list
	df= pd.Dataframe(), method created Pandas Dataframe from the list of scraped 	records.
	converted the dataframe into dictionary format to Stored the Dataframe into MongoDB by insert_one() and insert_many() methods in pymongo.MogoCLient 
	converted the dataframe into csv by to_csv() method and json by to_json method format.
  dowloadbuttons() of streamlit, downloaded the records into different format like csv, json 
	
		
	
	
	
