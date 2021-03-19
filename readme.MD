Scrape Wunderground allows to scrape historical weather data from https://www.wunderground.com. 


Two CSV files are created. 
* temps.csv is all the data points for the day (from the time stamped tables).
* NumEntries.csv shows how many entries/rows are in each dataframe per date. This csv is created because there are several dates that have incomplete data (ex: 1 row with only wind speed). The dates with 24 or more rows tend to look more reliable



Variable to set:

* date - the starting date to start scraping
* pagesToScrape -  The number of dates in a row to scrape
* prefixURL - The city/location of data to grab minus the date. Ex: 'https://www.wunderground.com/history/daily/KSDF/date/' . The date will be appended each time through the loop
* You can also set sleepTime (different values in the try and except blocks) if you unhappy with the settings. (10 seconds is listed in robots.txt as of March 2020)