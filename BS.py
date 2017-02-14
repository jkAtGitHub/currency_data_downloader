#-------------------------------------------------------------------------------
# Name:        Currency Data Downloader
# Purpose:     Downloads Currency Conversion Data from www.xe.com for any given
#              currency for any given day
#
# Author:      Jayakrishnan Vijayaraghavan
#
# Created:     02/12/2017
# Copyright:   (c) jvijayaraghavan 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import pandas as pd
from bs4 import BeautifulSoup
import urllib
import datetime

# -----------------------------------------------------
# Attribute names
# -----------------------------------------------------

#The number of days for which the data is needed
num_days = 10
# Location to save the csv. Prepend r'' before the location
location = r'C:\Personal\Learn\BS.csv'
from_currency = "INR"

# -----------------------------------------------------
# Other Constants
# -----------------------------------------------------
format = "%Y-%m-%d"
url_format = "http://www.xe.com/currencytables/?from={0}&date={1}"
# -----------------------------------------------------
# Date Formatting
# -----------------------------------------------------
#Today
today  = datetime.datetime.today()
#Yesterday
base = today - datetime.timedelta(days = 1)
# List of dates from yesterday until the number of days as a string in the given format
date_list = [(base - datetime.timedelta(days= x)).strftime(format) for x in range(0, num_days)]

d = []

for dt_counter, dt in enumerate(date_list):
    try:
        #For each date, form the url
        url = url_format.format(from_currency, dt)
        #OPen the URL and read content into Beautiful soup
        html = urllib.urlopen(url).read()
        if html is None:
            print('No data available for {0}'.format(dt))
            continue
        print('Processing data for {0}'.format(dt))
        soup = BeautifulSoup(html, "html.parser")
        
        tbl = soup.find_all('table')[0]
        currency_codes = []
        currency_names = []
        inr_per_unit_cur = []
        for th in tbl.findAll('tr')[1:]:

            values = [item.getText().strip() for item in th.findAll('td')]
            currency_code, currency_name, units_per_inr, inr_per_unit = values
            inr_per_unit_cur.append(inr_per_unit)
            currency_codes.append(currency_code)
            currency_names.append(currency_name.encode('utf-8').strip())
            
        if dt_counter == 0:
            d.append(('Currency Codes', currency_codes))
            d.append(('Currency Names', currency_names))
        else:
            if len(currency_codes) != len(d[0][1]):
                cur_na = set(d[0][1]) - set(currency_codes)
                for cur in cur_na:
                    idx = d[0][1].index(cur)
                    inr_per_unit_cur.insert(idx, None)
                    print("The {1} currency value is not available for {0}".format(dt, cur))
        d.append((dt, inr_per_unit_cur))
    except Exception as e:
        print("There was an error in processing info on {0} due to {1}".format(dt, e[0]))
        continue
df = pd.DataFrame.from_items(d)
df.to_csv(location)
