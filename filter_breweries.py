import pandas as pd
import csv

query = 'United States' # PUT LOCATION YOU CARE ABOUT HERE - can be in the general form of 'Bend, OR UNITED STATES' or 'West Coast New Zealand'

df = pd.read_csv('untappd-1.csv', dtype={'average_rating':float})
df['num_ratings'] = df['num_ratings'].str.replace(',','')
df['num_ratings'] = df['num_ratings'].str.replace('M','0000')
df['num_ratings'] = df['num_ratings'].str.replace('+','')
df['num_ratings'] = df['num_ratings'].str.replace('.','')
df['num_ratings'] = pd.to_numeric(df['num_ratings'], errors='coerce')
df = df[df['num_ratings'].notna()]
df = df[df['average_rating'].notna()]
df = df[df['Location'].notna()]

df = df[(df['num_ratings'] > 300)] #filter out very small breweries
df = df[(df['average_rating'] >= 3.6)] #filter out bad breweries
df = df[df['Location'].str.contains(query, case=False)]
df = df.drop_duplicates(subset = ['UT_Index'],keep = 'last').reset_index(drop = True)

#below is to set up a US-wide list
df['Location'] = df['Location'].str.replace(' United States', '', case=False)
df[['City','State']] = df.Location.str.split(', ', expand=True)
df = df[['Brewery_Name','City','State','average_rating','num_ratings','UT_URL']]

df_filename = 'untappd_db.csv'
print("exporting " + df_filename)

df.to_csv(df_filename, index=False, quotechar='"', quoting=csv.QUOTE_ALL, header=True)
