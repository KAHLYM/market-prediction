import os
import pickle
import shutil

import pandas as pd
import urllib.request as request

from contextlib import closing
from typing import List

NASDAQLISTEDTXT: str = 'nasdaq.txt'

# Get NASDAQ listed stock market symbols
with closing(request.urlopen('ftp://ftp.nasdaqtrader.com/SymbolDirectory/nasdaqlisted.txt')) as r:
    with open(NASDAQLISTEDTXT, 'wb') as f:
        shutil.copyfileobj(r, f)

# Read nasdaqlisted.txt into pandas
nasdaqlisted = pd.read_csv(NASDAQLISTEDTXT, sep='|')

# Delete nasdaqlisted.txt
os.remove(NASDAQLISTEDTXT)

# Drop last row containing invalid metadata
nasdaqlisted.drop(nasdaqlisted.tail(1).index, inplace=True)

# Remove ETFs and test listings
nasdaqlisted = nasdaqlisted[nasdaqlisted['ETF'] != 'Y']
nasdaqlisted = nasdaqlisted[nasdaqlisted['Test Issue'] != 'Y']

def format_security_name(security_name: str) -> str:
    # Remove text that specifies share type
    security_name = security_name.split(' -', 1)[0]

    legal_structure_identifiers = [('Corporation', 'Corp'),
                                   ('Incorporated', 'Inc'),
                                   ('Public Limited Company', 'Plc'),
                                   ('Limited', 'Ltd')]

    # Remove text that specifies legal structure
    for legal_structure_identifier in legal_structure_identifiers:
        security_name = security_name.replace(legal_structure_identifier[0], '')                # Public Limited Company
        security_name = security_name.replace(legal_structure_identifier[1].title() + '.', '')  # Plc.
        security_name = security_name.replace(legal_structure_identifier[1].lower() + '.', '')  # plc.
        security_name = security_name.replace(legal_structure_identifier[1].upper() + '.', '')  # PLC.
        security_name = security_name.replace(legal_structure_identifier[1].title(), '')        # Plc
        security_name = security_name.replace(legal_structure_identifier[1].lower(), '')        # plc
        security_name = security_name.replace(legal_structure_identifier[1].upper(), '')        # PLC
    
    # Remove trailing punctuation/whitespace
    security_name = security_name.replace(',', '')
    security_name = security_name.strip()

    return security_name

# Generate Symbol-SecurityName dictionary
ticker_security_names = {}
for row in nasdaqlisted.itertuples():
    ticker_security_names[row[1]] =  format_security_name(row[2])

# Pickle Symbol-SecurityName list
save_ticker_security_names = open('nasdaq.pickle','wb')
pickle.dump(ticker_security_names, save_ticker_security_names)
save_ticker_security_names.close()
