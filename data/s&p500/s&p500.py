import json
import os
import pathlib

import pandas as pd

# Retrieve Wikipedia data
table = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')

# Extract table
df = table[0]
df = pd.DataFrame(df, columns=['Symbol', 'Security'])

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
for row in df.itertuples():
    ticker_security_names[row[1]] =  format_security_name(row[2])

# Save JSON
with open(os.path.join(pathlib.Path(__file__).parent.absolute(), 's&p500.json'), 'w') as outfile:
    json.dump(ticker_security_names, outfile)
