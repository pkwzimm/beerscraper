# Beer Ratings Scaper

## Project Description:
This is a scraper that will loop over every brewery address in Untappd sequentially, create a database, filter that database, and then host a dashboard online.

### Instructions
#### Order of scripts:
1. untappd-scraper.py \
Scrapes Untappd, outputs untappd.csv **NOTE**: this can take awhile, since it has to wait for the server to respond to ~500k individual pages, if you're scraping the whole thing.
2. filter_breweries.py \
Filters the output file from above by geographic location, average rating, and total rating, outputs untappd_db.csv

#### Dashboard files:
- index.html \
page on which to embed the dashboard
- brewery.js \
D3.js script
- brewery.css \
styling

**Important Note** - You'll need to host the web and data files on a webserver for this to work.  Right now, index.html expects everything else to be in the root directory (so if your uri is example.com/beer/, everything should be in /beer)
