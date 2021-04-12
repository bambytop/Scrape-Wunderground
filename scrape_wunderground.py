
import csv
import time
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd





#####Starting date ######
date = datetime.datetime(2020,11,9)

##### End Date
endDate = datetime.datetime(2021,3,20)



#####       The first part of the url
######      Example: prefixURL = 'https://www.wunderground.com/history/daily/KSDF/date/'
#######     The date will be appended to this in the url variable

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
            writer.writerow([str(date.date()),len(df)])


errorTracker= 0

while date <= endDate:
    if errorTracker >=10: #if 10 or more errors occur, exit the while loop
        print("There were ", errorTracker, " errors in a row, so the program stopped. Check the NumEntriesFile")
        break

    try:
        scrape_page(date,prefixURL,sleepTime=10, errorOccurs=False)
        date += datetime.timedelta(days=1)   #increments date by one
        errorTracker=0 # returns errorTracker to 0

    #### If the scrape_page() function runs and fails then the date is not incremented

    except IndexError as e:
        print("AN ERROR OCCURRED", str(e)) 
        time.sleep(360)  #wait 
        with open('NumEntries.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["NEW ERROR, did not get df",str(e),str(date.date())])
        errorTracker += 1

    except:   # spotty wifi
        print("AN ERROR OCCURRED") 
        time.sleep(360)  #wait if timoutexception raised and try again, spotty wifi
        with open('NumEntries.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["NEW ERROR, did not get df",str(date.date())])
        errorTracker += 1






