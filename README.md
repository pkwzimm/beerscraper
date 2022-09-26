# Beer Ratings Scaper

## Project Description:
This is a scraper that will loop over every brewery address in Untappd sequentially, create a database, filter that database, and then host a dashboard online.

### Instructions
#### Order of scripts:
- untappd-scraper.py \
Scrapes Untappd
- filter_breweries.py \
Filters the output file from above by geographic location, average rating, and total rating.

#### Dashboard files:
- index.html \
page on which to embed the dashboard
- brewery.js \
D3.js script
- brewery.css \
styling
- jquery.3.5.1.min.js \
D3 needs jQuery

**Important Note** - You'll need to host the web and data files on a webserver for this to work.  Right now, they expect everything to be in the root directory.
