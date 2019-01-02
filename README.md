# Collecting Singapore Stock Prices from the Internet in Python

One of my first projects in Python. 

Written as function call to do the following:
 1. Determine the stock tickers in the Singapore Stock Exchange (SGX)
 2. Collect data from the Internet.
 3. Consolidate the data in a dataframe, and save it in a local disk.
 4. Analyse and filter the stocks using some efficiency measures (earnings yield, current ratio, etc).
 
 ### Main file:
 
 _CollateFilter.py_\
      Main file to execute the collection.
      Calls functions from the other supporting files.
  
 ### Supporting files:
  
 _getSGXTcikers.py_\
      Collects the active stocks' tickers in SGX.
  
 _Stockanalyse.py_\
      To analyse the collected stocks.   
