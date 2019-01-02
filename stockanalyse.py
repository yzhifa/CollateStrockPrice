import pandas as pd
import numpy as np
import os, re
import datetime

from getSGXTickers import *

"""
Given a list of stock symbols, compute numbers

Extra: Stock dict from getSGXTickers for company name

"""

def analyse_stock(stock_df):

# Read Data - get latest data

	# dir = r"H:\Python\stockPriceUpdate\collatefilter"

	# os.chdir(dir)
	s = getSGXTickers()
	
	data = stock_df.copy()
	stock_para = list(data['Parameter'])
	
	price_dict = {}

	# Read Report Template
	with open("report_temp.txt", "r") as f:
		text = f.read()
		

	# Analysis Loop

	for nameidx, i in enumerate(stock_para):

		to_n = pd.to_numeric
		
		data_para = data[data['Parameter'] ==  i]

		# Preamble
		net_profit = data_para['Net Income'].iloc[0]
		share_outstanding = data_para['Shares Outstanding'].iloc[0]
		EPS = net_profit/share_outstanding

		# Profile
		PER = data_para['Current P/E Ratio'].iloc[0]
		Price = round(PER * EPS, 3) 

		dividends_str = re.findall("\d+.\d+", str(data_para['Last Dividend (Ex-Date)'].iloc[0]))
		if dividends_str:
			dividends = float(dividends_str[0])
		else:
			dividends = 0
		div_yield = round(dividends/Price *100, 3)
		P2Sales = data_para['Price/Sales'].iloc[0]
		P2BV = data_para['Price/Book Value'].iloc[0]
		P2CF = data_para['Price/Cash flow'].iloc[0]
		
		# Profitability
		# EPS
		net_profit_margin =  data_para['Net Profit Margin %'].iloc[0]
		ROE = data_para['Return on Equity %'].iloc[0]
		ROC = data_para['Return on Capital %'].iloc[0]
		ROA = data_para['Return on Assets %'].iloc[0]
		Inv_TO = data_para['Inventory Turnover'].iloc[0]
		Asset_TO = data_para['Asset Turnover'].iloc[0]

		# Financial Strength
		Current_Ratio = data_para['Current Ratio'].iloc[0]
		Quick_Ratio = data_para['Quick Ratio'].iloc[0]
		#Interest_Coverage = data_para['Interest Coverage'].iloc[0]
		Interest_Coverage = "TBD"
		Debt_to_Eq = data_para['Debt/Equity Ratio'].iloc[0]
		BV = data_para['Book Value/Share'].iloc[0]

		# CashFlow
		cashflow = data_para['Cashflow Estimate'].iloc[0]
		
		date = str(datetime.datetime.today().strftime('%y%m%d'))
		
		with open("summary_{date}.txt".format(date = date), "a") as f:
			f.write(text.format(tick = i, coyname = s[i], date = date, \
				PER = PER, Price = Price, dividends = dividends, div_yield = div_yield, \
				P2Sales = P2Sales, P2BV = P2BV, P2CF = P2CF, \
				net_profit = net_profit, net_profit_margin = net_profit_margin, \
				ROE = ROE, ROC = ROC, ROA = ROA, Inv_TO = Inv_TO, Asset_TO = Asset_TO, \
				Current_Ratio = Current_Ratio, Interest_Coverage = Interest_Coverage, Debt_to_Eq = Debt_to_Eq \
				))
				
		price_dict[i] = Price
	
	return price_dict


		
# cwd = r"H:\Python\stockPriceUpdate\collatefilter"
# os.chdir(cwd)

# file = r"Filtered Stocks_180805.csv"
# df = pd.read_csv(file)
# s = getSGXTickers()
# stock_para = list(df['Parameter'])

# analyse_stock(df)