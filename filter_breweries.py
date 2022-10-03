import pandas as pd
import csv

query = 'United States' # PUT LOCATION YOU CARE ABOUT HERE - can be in the general form of 'Bend, OR UNITED STATES' or 'West Coast New Zealand'

df = pd.read_csv('untappd.csv', dtype={'UT_Index':str,'average_rating':str,'num_ratings':str,'Brewery_Name':str,'UT_URL':str}) # load datafile from disk - it's better to make everything a string to start with in case of weird scraping results "like a string N/A"

# Data cleaning / preprocessing
df = df.drop_duplicates(keep='first') # drop duplicate rows (for example, headers if you had to run the scraper more than once or stop/start). Keep first so that the header is at the top like it's supposed to be.
df['average_rating'] = pd.to_numeric(df['average_rating'], errors='coerce') # convert average rating to a float
df = df[df['num_ratings'].notna()] # no NaNs
df = df[df['average_rating'].notna()]
df = df[df['Location'].notna()]
df = df[df['UT_Index'].notna()]
df['num_ratings'] = df['num_ratings'].str.replace(',','') # handle numbers with commas (i.e. 100,000)
df['num_ratings'] = df['num_ratings'].str.replace('M','0000') # handle Untappd's use of "M+" (i.e. 1.74M+) for number of ratings
df['num_ratings'] = df['num_ratings'].str.replace('+','') # see above
df['num_ratings'] = df['num_ratings'].str.replace('.','') # see above
df['num_ratings'] = pd.to_numeric(df['num_ratings'], errors='coerce') # convert the strings for num_ratings into an int

# Filters
df = df[(df['num_ratings'] > 300)] #filter out very small breweries
df = df[(df['average_rating'] >= 3.6)] #filter out bad breweries
df = df[df['Location'].str.contains(query, case=False)] # run the search on location

#Remove the country (Only do if this is US or Canada, else the 'comma-space-capital-capital' pattern makes no sense and you should re-write this and the below section to handle different country patterns (probably two columns: location & country))
df['Location'] = df['Location'].str.replace(' United States', '', case=False)
df = df[df['Location'].str.contains(', [A-Z][A-Z]$', case=True)]

# city/state split - this way avoids the problem of weird cases of more than one comma in the Location cell.  US / Canada formatting only at this point
df['City'] = df['Location'].str.replace(', [A-Z][A-Z]$', '') # take everything before the comma & state
df['State'] = df['Location'].str.replace('^.*, (?=[A-Z][A-Z]$)', '') # remove everything before the state
df = df[df['City'].notna()]
df = df[df['State'].notna()]
df = df[['Brewery_Name','City','State','average_rating','num_ratings','UT_URL']]

# One final de-dupe check (possibly redundant)
df = df.drop_duplicates(subset='UT_URL', keep='first')

df_filename = 'untappd_db.csv'
print("exporting " + df_filename)

df.to_csv(df_filename, index=False, quotechar='"', quoting=csv.QUOTE_ALL, header=True) # export results file
