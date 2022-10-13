from selenium import webdriver

from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options # options (for running headless)
import csv
import re
import os
import pandas as pd


options = Options()
options.add_argument("--headless")
browser = webdriver.Chrome(options=options) #open up your browser (Ubuntu version, with headless flags)

df = pd.DataFrame(columns=['UT_Index', 'Brewery_Name', 'Location', 'average_rating', 'num_ratings', 'UT_URL'])

# check to make sure you don't delete the datafile if you're ever dumb enough to do so
if os.path.exists('untappd.csv'):
    os.rename('untappd.csv', 'untappd_old.csv')

print("Opening Untappd...")

wait = WebDriverWait(browser, 0)

df_filename = 'untappd.csv'
df.to_csv(df_filename, index=False, quotechar='"', quoting=csv.QUOTE_ALL, header=True)

for i in range(1, 550000): # 530334 was the count as of 10/4/2022
    brewery_url = 'https://untappd.com/brewery/' + str(i)

    try:
        browser.get(brewery_url)
        brewery = []

        ut_index = str(i)

        brewery_name = wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//div[@class='name']/h1"))).text

        # print('Brewery: ' + brewery_name)

        location = wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//div[@class='name']/p[@class='brewery']"))).text

        rating = wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//span[@class='num']"))).text
        rating = re.sub('\(|\)', '', rating)

        num_ratings = wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//div[@class='stats']/p/span[@class='count']"))).text

        ut_url = wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//a[@class='label']"))).get_attribute("href")

        brewery.append([ut_index, brewery_name, location, rating, num_ratings, ut_url])

        print(brewery)

        df_thread = pd.DataFrame(brewery,
                                 columns=['UT_Index', 'Brewery_Name', 'Location', 'average_rating', 'num_ratings',
                                          'UT_URL'])

        # df = pd.concat([df, df_thread], axis=0)

        df_thread.to_csv(df_filename, index=False, quotechar='"', quoting=csv.QUOTE_ALL, header=False, mode='a')

    except:
        print("No brewery at " + brewery_url)
        pass
