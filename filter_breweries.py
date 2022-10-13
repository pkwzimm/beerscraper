import pandas as pd
import csv

query = ' United States' # PUT LOCATION YOU CARE ABOUT HERE - can be in the general form of 'Bend, OR UNITED STATES' or 'West Coast New Zealand'
# query = 'Bend, OR' # PUT LOCATION YOU CARE ABOUT HERE - can be in the general form of 'Bend, OR UNITED STATES' or 'West Coast New Zealand'
# query = ", WA UNITED STATES"

df = pd.read_csv('untappd_raw.csv', dtype={'UT_Index':str,'average_rating':str,'num_ratings':str,'Brewery_Name':str,'UT_URL':str})
df = df.drop_duplicates(keep='first')
df['average_rating'] = pd.to_numeric(df['average_rating'], errors='coerce')
df = df[df['num_ratings'].notna()]
df = df[df['average_rating'].notna()]
df = df[df['Location'].notna()]
df = df[df['UT_Index'].notna()]
df['num_ratings'] = df['num_ratings'].str.replace(',','')
df['num_ratings'] = df['num_ratings'].str.replace('M','0000')
df['num_ratings'] = df['num_ratings'].str.replace('+','')
df['num_ratings'] = df['num_ratings'].str.replace('.','')
df['num_ratings'] = pd.to_numeric(df['num_ratings'], errors='coerce')

df = df[(df['num_ratings'] > 300)] #filter out very small breweries
df = df[(df['average_rating'] >= 3.6)] #filter out bad breweries
df = df[df['Location'].str.contains(query, case=False)]

#below is to set up a US-wide list
df['Location'] = df['Location'].str.replace(' United States', '', case=False)
df = df[df['Location'].str.contains(', [A-Z][A-Z]$', case=True)]
# city/state split - this way avoids the problem of weird cases of more than one comma in the Location cell.
df['City'] = df['Location'].str.replace(', [A-Z][A-Z]$', '') # take everything before the comma & state
df['State'] = df['Location'].str.replace('^.*, (?=[A-Z][A-Z]$)', '') # remove everything before the state
# df[['City','State']] = df.Location.str.split(', ', n=1,expand=True) # this works great if you have perfectly orderly data.  But in the real world use the above.
df = df[df['City'].notna()]
df = df[df['State'].notna()]
df['Brewery_Name_NS'] = df['Brewery_Name'].str.replace(' ', '_', case=False)
df = df[['Brewery_Name','Brewery_Name_NS','City','State','average_rating','num_ratings','UT_URL']]
df = df.drop_duplicates(subset='UT_URL', keep='first')

# df_filename = 'untappd-Bend.csv'
# df_filename = 'untappd-WA.csv'
df_filename = 'untappd_db.csv'
# df_filename = 'untappd_filter_results.csv'
print("exporting " + df_filename)

df.to_csv(df_filename, index=False, quotechar='"', quoting=csv.QUOTE_ALL, header=True)
