#Collating Stock Data
"""
R0: 2017
R1 : 2018-08
	Update SGX stock lists
	Webscrape SGX tickers instead of referring to a file.
"""

import requests, bs4, openpyxl, datetime, os, sys, re
import pandas as pd
import numpy as np

from stockanalyse import * # returns a dictionary of stock tickers (key) company (values)
from getSGXTickers import *

""" 
HELPER FUNCTIONS 
"""
# Creates a list of text from a BS4 elements
def re_list(elem):
	return [t.getText().replace('\n', "").replace(',', "") for t in elem]

	
# Define function to clean the list
def RemoveMBk(ele):
	if ele == '-':
		return None
	elif ele[-1] == 'M':
		ele = ele.replace('M', '')
		return float(ele)
	elif ele[-1] == 'B':
		ele = ele.replace('B', '')
		return  float(ele) *1000
	elif ele[-1] == 'k':
		ele = ele.replace('k', '')
		return float(ele) /1000
	else:
		return ele

		
"""
END OF HELPER FUNCTIONS
"""

path = r'D:\Python\stockPriceUpdate\collatefilter' #need to change this path

os.chdir(path)

# Filepath to save to
filePath = 'Collated Stocks_'+str(datetime.datetime.today().strftime('%y%m%d'))+ '.csv' 

# Get stock symbols
print('Collating stocks symbols...' + '\n')

s = getSGXTickers()
sgxTickers = list(s.keys())
sgxCoyName = [s[i] for i in sgxTickers]

print('Number of Symbols collated: %s'%len(sgxTickers) + '\n')

print('Adding data...' + '\n')

# Create a empty dataframe
stock = pd.DataFrame()




#Add parameters
for i, ticks in enumerate(sgxTickers):
	sys.stdout.write('\rCollating stocks {a}/{b} -- {c}'.format(a = i+1, b = len(sgxTickers), c = ticks))
	sys.stdout.flush()
	url = r"https://www.msn.com/en-us/money/stockdetails/analysis/fi-143.1.{}.SES".format(ticks) #Get URL
	res = requests.get(url)
	res.raise_for_status()
	soup = bs4.BeautifulSoup(res.text, 'lxml')
	elemHeading = soup.select('.heading') #header
	elemValue = soup.select('.value')
	elemFirstCol = soup.select('.first-col') #header
	elemKeyRatio = soup.select('.key-ratio-value')
	
	#Create a header DF
	eleH = re_list(elemHeading)
	eleH2 = re_list(elemFirstCol)
	header = pd.Series(eleH + eleH2)

	#Collate Values
	eleV = re_list(elemValue)
	eleR = re_list(elemKeyRatio)
	p = eleV + eleR
	p = [RemoveMBk(x) for x in p]
	
	#Rename the values columns
	stock['Parameter'] = header
	stock[ticks] = pd.Series(p)
	
#Save as a CSV file
print('\nSaving as a CSV file...\n')
stock.transpose().to_csv(filePath)

print('\nComplete\n')

# Part 2: Filtering
# -----------------

print('Now filtering ...\n')

# Requirements
CurrentRatioReq = 2.0
NetProfitMarginReq = 10
DivYieldReq = 4 #in percentage, optional
peRequired = 5
positive = 0

# Import the CSV file
df2 = pd.read_csv(filePath, skiprows = 1)
#df2 = stock.copy()

df2 = df2[(df2['Current Ratio'] >= CurrentRatioReq) & \
	(df2['Net Profit Margin %'] >= NetProfitMarginReq) & \
	(df2['Current P/E Ratio'] >= peRequired) & (df2['Book Value/Share'] >= positive) & \
	(df2['Return on Capital %'] >= positive) & (df2['Return on Equity %'] >= positive)]

# Obtain the number of row in sliced df2
df2_range = np.arange(df2.shape[0]) + 1

# Sort by P/E in ascending. Smaller P/E == Greater Earnings Yield (e/P)
df2.sort_values(by = ['Current P/E Ratio'], ascending = True, inplace = True)

#Assign Rank
df2['rankByPE'] = df2_range

# Sort by Returns on Capital
df2.sort_values(by = ['Return on Capital %'], ascending = False, inplace = True)

# Assign Rank
df2['rankByROC'] = df2_range

# Sort by Retun on Assets
df2.sort_values(by = ['Return on Assets %'], ascending = False, inplace = True)
df2['rankByROA'] = df2_range

# Sum rank 
df2['PE_ROC'] = df2['rankByPE'] + df2['rankByROC']

# Sum rank
df2['rankAll'] = df2['rankByPE'] + df2['rankByROC'] + df2['rankByROA']

# Get top 30 Stocks by PE and ROC
df2.sort_values(by=['PE_ROC'], ascending = True, inplace = True)

top30 = df2.copy()
selected_fileNameCSV = 'Filtered Stocks_'+str(datetime.datetime.today().strftime('%y%m%d'))+'.csv'
top30.head(30).to_csv(selected_fileNameCSV)


# Analyse Stock
# -------------
price_dict = analyse_stock(top30.head(30))

# Append results to a file
with open('selectedStocks.txt', 'a') as f: #a-mode = append mode
	f.write('\*Selected on {}\n'.format(str(datetime.datetime.today().strftime('%y%m%d'))))
	for i in top30.head(30)['Parameter']:
		f.write('{sym} / [{coy}] / {price}\n'.format(sym = i, coy = s[i], price = price_dict[i]))

print('Filtering Complete!' + '\n')


# Stock Count
# -----------

# Read the results file - for copy
with open('selectedStocks.txt', 'r') as f:
	stocklist = f.readlines()	

stocklist_prev = [x.strip() for x in stocklist]

#Get the unique stock and corresponding counts
unique_prev, counts_prev = np.unique(stocklist_prev, return_counts=True)


