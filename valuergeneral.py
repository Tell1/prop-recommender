"""
Script to convert a .DAT
"""

import json


file = "/mnt/c/Users/ssch7/repos/prop-recommender/data/valuergeneral/raw/2022/20220103/001_SALES_DATA_NNME_03012022.DAT"

with open(file) as f:
    lines =f.readlines()
    
# Define the path to the JSON file
meta = "/mnt/c/Users/ssch7/repos/prop-recommender/data/valuergeneral/raw/format.json"

# Open the JSON file and load its contents into a variable
with open(meta) as f:
    mdata = json.load(f)

# Define the record to search for
record = 'A'

# Filter the lines to find the line that starts with the specified record
line = list(filter(lambda l: l[0] == record, lines))[0]

# Print the record information from the JSON data
print(mdata[f'Record {record}'])

# Create an empty dictionary to store the fields
fields = {}

# Iterate over the columns in the line
for i, col in enumerate(line):
    # Print a newline character (for formatting purposes)
    print()
    
    # Get the field name from the JSON data
    fieldname = mdata[f'Record {record}'][i]['Record Type']
    
    # Store the column value in the fields dictionary with the field name as the key
    fields[fieldname] = col

print(fields)