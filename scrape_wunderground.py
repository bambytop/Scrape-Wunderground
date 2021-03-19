
import csv
import time
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd





#####Starting date ######
date = datetime.datetime(2011,11,17)

##### The number of dates in a row to scrape
pagesToScrape=365

#####The first part of the url, the date gets appended to the end to get the history information
###### Exapmle: 'https://www.wunderground.com/history/daily/KSDF/date/2004-01-01'
prefixURL = 'https://www.wunderground.com/history/daily/KSDF/date/'



def scrape_page(date, prefixURL, sleepTime, errorOccurs):
        print("")
        print("Function started:", time.strftime("%H:%M:%S", time.localtime()))     
        url = ''.join([prefixURL+str(date.date())])
        print("scraping:", url)

        driver = webdriver.Chrome()
        driver.get(url)
        tables = WebDriverWait(driver,20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table")))

        time.sleep(sleepTime) #obey robots.txt, adds time to reduce errors

        a = pd.read_html(tables[1].get_attribute('outerHTML'))
        df=a[0]
        df = df[df['Time'].notna()] #drops rows
        df.insert(0, 'Date', date, allow_duplicates=True)
        print(df)
        df.to_csv(r'temps.csv', index = False, columns=['Date','Time','Temperature','Dew Point','Humidity','Wind','Wind Speed','Wind Gust','Pressure','Precip.','Condition'], mode='a', header=None)
        print("There are", len(df), "rows for", str(date.date()))
        with open('NumEntries.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            if errorOccurs==False:
                writer.writerow([str(date.date()),len(df)])
            if errorOccurs==True:
                writer.writerow([str(date.date()),len(df),"ERROR"])



for i in range(pagesToScrape): 
    try:
        scrape_page(date,prefixURL,sleepTime=10, errorOccurs=False)
    except IndexError as e:
        # Every so often an IndexError occurs likely due to not allowing enough waiting time. 
        # Instead of increasing the waiting time for each loop, this waits for the error and 
        # then reruns the function with a longer sleepTime. This doesn't cover 2 errors in a row.
        print("AN ERROR OCCURRED", str(e)) 
        scrape_page(date,prefixURL,sleepTime=50, errorOccurs=True)
    except TimeoutException as e:   # spotty wifi
        print("AN ERROR OCCURRED", str(e)) 
        time.sleep(120)  #wait 2 minutes if timoutexception raised and try again, spotty wifi
        scrape_page(date,prefixURL,sleepTime=50, errorOccurs=True)


    date += datetime.timedelta(days=1)   #increments date by one




