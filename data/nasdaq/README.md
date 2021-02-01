# NASDAQ

Run [nasdaq.py](nasdaq.py) to output a pickled list of tuples that contain the symbols and security names of non-ETF NASDAQ listings. The security names will be formated to remove legal structures i.e. "Public Limited Company".

A temporary file ```nasdaq.txt``` will be downloaded and removed.

NASDAQ provides information on all securities, updated every night and accessed via [NASDAQtrader](ftp://ftp.nasdaqtrader.com/SymbolDirectory). The dataset used is ```nasdaqlisted.txt```. Information of bonds and options is also availible. Note that ```nasdaqtraded.txt``` should be the combination of ```nasdaqlisted.txt``` and ```otherlisted.txt```. More information on the data can be found [here](http://www.nasdaqtrader.com/trader.aspx?id=symboldirdefs).
