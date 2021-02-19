import json
import os
import pathlib

import pandas as pd

# Retrieve Wikipedia data
table = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')

# Extract table
df = table[0]
df = pd.DataFrame(df, columns=['Symbol', 'Security'])

# Convert DataFrame to JSON dictionary
result = df.to_json(orient='values')
parsed = dict(json.loads(result))

# Save JSON
with open(os.path.join(pathlib.Path(__file__).parent.absolute(), 's&p500.json'), 'w') as outfile:
    json.dump(parsed, outfile)
