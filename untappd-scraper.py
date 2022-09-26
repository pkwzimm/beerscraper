from selenium import webdriver
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC # wait until visible is the key here.
from selenium.webdriver.chrome.options import Options #options (for running headless)
import csv
import re # regular expressions
import os # for checking if file exists
import pandas as pd # dataframe util


options = Options()
options.add_argument("--headless") # unless you really want to watch the browser window for several hundred thousand fetches...
browser = webdriver.Chrome(options=options) #open up your browser (Ubuntu version, with headless flags)

df = pd.DataFrame(columns=['UT_Index', 'Brewery_Name', 'Location', 'average_rating', 'num_ratings', 'UT_URL']) # create empty df and set column names

# check to make sure you don't delete the datafile if you're ever dumb enough to do so
if os.path.exists('untappd.csv'):
    os.rename('untappd.csv', 'untappd_old.csv')

print("Opening Untappd...")

wait = WebDriverWait(browser, 0)

df_filename = 'untappd.csv'
df.to_csv(df_filename, index=False, quotechar='"', quoting=csv.QUOTE_ALL, header=False) # create datafile (empty except for header at this point)

for i in range(1, 354455): # untappd has every brewery assigned a number, and this is about as high as they go in 2022.  This will change over time as new breweries are founded.
    brewery_url = 'https://untappd.com/brewery/' + str(i)

    # try-except loop to not fill the csv with empty rows for non-existant brewery numbers (hypothesis is these are no longer active)
    try:
        browser.get(brewery_url)
        brewery = [] # create dict to fill

        ut_index = str(i)

        brewery_name = wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//div[@class='name']/h1"))).text

        location = wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//div[@class='name']/p[@class='brewery']"))).text

        rating = wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//span[@class='num']"))).text
        rating = re.sub('\(|\)', '', rating) # remove the parentheses around the average rating

        num_ratings = wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//div[@class='stats']/p/span[@class='count']"))).text

        ut_url = wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//a[@class='label']"))).get_attribute("href") # note that this is an href attribute, the element's text won't get you the URL.

        brewery.append([ut_index, brewery_name, location, rating, num_ratings, ut_url])

        print(brewery)

        df_thread = pd.DataFrame(brewery,
                                 columns=['UT_Index', 'Brewery_Name', 'Location', 'average_rating', 'num_ratings',
                                          'UT_URL']) # convert dict to a temp df

        df_thread.to_csv(df_filename, index=False, quotechar='"', quoting=csv.QUOTE_ALL, header=False, mode='a') # append df_thread to csv file

    # this almost always means you get a 404 page for no brewery exists, which means the try fails because there is no element found, so we move onto the next number in the list.
    except:
        print("No brewery at " + brewery_url)
        pass
