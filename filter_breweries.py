import pandas as pd
import csv

query = 'United States' # PUT LOCATION YOU CARE ABOUT HERE - can be in the general form of 'Bend, OR UNITED STATES' or 'West Coast New Zealand'

df = pd.read_csv('untappd.csv', dtype={'average_rating':float}) # load datafile from disk
df = df.drop_duplicates() # drop duplicate rows (for example, headers if you had to run the scraper more than once or stop/start)
df['num_ratings'] = df['num_ratings'].str.replace(',','') # handle numbers with commas (i.e. 100,000)
df['num_ratings'] = df['num_ratings'].str.replace('M','0000') # handle Untappd's use of "M+" (i.e. 1.74M+) for number of ratings
df['num_ratings'] = df['num_ratings'].str.replace('+','') # see above
df['num_ratings'] = df['num_ratings'].str.replace('.','') # see above
df['num_ratings'] = pd.to_numeric(df['num_ratings'], errors='coerce') # convert the strings for num_ratings into an int
df = df[df['num_ratings'].notna()] # no NaNs
df = df[df['average_rating'].notna()]
df = df[df['Location'].notna()]

df = df[(df['num_ratings'] > 300)] #filter out very small breweries
df = df[(df['average_rating'] >= 3.6)] #filter out bad breweries
df = df[df['Location'].str.contains(query, case=False)] # run the search on location
df = df.drop_duplicates(subset = ['UT_Index'],keep = 'last').reset_index(drop = True) # check for dupliates with the same index
df = df.drop_duplicates(subset = ['UT_URL'],keep = 'last').reset_index(drop = True) # check for dupliates with the same URL

#below is to set up a US-wide list
df['Location'] = df['Location'].str.replace(' United States', '', case=False) # remove country from the location, unless that's what you care about.
df[['City','State']] = df.Location.str.split(', ', expand=True) # Split cities and states into two columns
df = df[['Brewery_Name','City','State','average_rating','num_ratings','UT_URL']]

df_filename = 'untappd_db.csv'
print("exporting " + df_filename)

df.to_csv(df_filename, index=False, quotechar='"', quoting=csv.QUOTE_ALL, header=True) # export results file
