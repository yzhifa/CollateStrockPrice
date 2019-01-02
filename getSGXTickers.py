import os, sys, datetime
import re
import numpy as np, pandas as pd

import requests, bs4

def getSGXTickers(save = 'No'):

	save = save.lower()

	# Webscraping
	url = r"https://sginvestors.io/sgx/stock-listing/alpha" #Get URL
	res = requests.get(url)
	res.raise_for_status()
	soup = bs4.BeautifulSoup(res.text, 'lxml')
	elemStockName = soup.select('.stockname') #stockname

	name_list = [nameT.getText().replace("<[\w+\d+]>", "") for nameT in elemStockName]
	name_dict = {}


	for idx, item in enumerate(name_list):
		
		coyname, tic = item.split("SGX")
		coy = coyname[:-2]
		
		idx1 = tic.index(':')
		idx2 = tic.index(')')
		ticker = tic[idx1+1:idx2].replace(" ", "")
		
		name_dict[str(ticker)] = str(coy)

	if save == 'Yes'.lower():
		path = r'D:\Python\stockPriceUpdate'
		os.chdir(path)
		pd.DataFrame(list(name_dict.items()), columns = ['Symbol', 'Coy']).to_csv("allSGXSymbols_{}.csv".format(str(datetime.datetime.today().strftime('%y%m%d')), index = False))
	
	return name_dict


getSGXTickers(save = 'yes')	


