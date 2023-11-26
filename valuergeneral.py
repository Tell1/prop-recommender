"""
Script to convert a .DAT

.DAT file format example:
{
    "RecordA": {
      "recordType": {"type": "A", "size": 1, "required": true, "example": "A"},
      "fileType": {"type": "A", "size": 1, "required": true, "example": "A"},
      "districtCode": {"type": "A", "size": 3, "required": true, "example": "077"},
      "downloadDateTime": {"type": "Date", "size": 16, "required": true, "format": "CCYYMMDD HH24:MI"},
      "submitterUserId": {"type": "A", "size": 35, "required": false}
    },
    "RecordB": {
      "recordType": {"type": "A", "size": 10, "required": true, "example": "B"},
      "districtCode": {"type": "A", "size": 3, "required": true},
      "propertyId": {"type": "A", "size": 10, "required": true},
      "saleCounter": {"type": "A", "size": 7, "required": true},
      ...
    },
    "RecordZ": {
      "recordType": {"type": "A", "size": 1, "required": true, "example": "Z"},
      "totalRecords": {"type": "N", "size": 12, "required": true},
      "totalBRecords": {"type": "N", "size": 12, "required": true},
      "totalCRecords": {"type": "N", "size": 12, "required": true},
      "totalDRecords": {"type": "N", "size": 12, "required": true}
    }
  }
  

.DAT file example:
A;RTSALEDATA;001;20220103 01:00;VALNET;
B;001;4255491;1;20220103 01:01;;;9;GARLAND RD;CESSNOCK;2325;600.9;M;20200928;20211224;572300;R2;R;RESIDENCE;;AAB;;0;AR772723;
C;001;4255491;1;20220103 01:01;8/1258173;
D;001;4255491;1;20220103 01:01;P;;;;;;
D;001;4255491;1;20220103 01:01;V;;;;;;
Z;6;1;1;2;

Output example:
{
    "RecordA": {"recordType": "A", "fileType": "RTSALEDATA", "districtCode": "001", "downloadDateTime": "20220103", "submitterUserId": "VALNET"}
    "RecordB": ...
}

DataFrame/CSV example:

    districtCode propertyId saleCounter area areaType contractDate settlementDate purchasePrice
    0           001   4255491           1  600.9        M   20200928     20211224       572300

"""

"""
TODO: Add unit tests for data conversion
TODO: Extend script to convert multiple DAT files to csv
"""

import json
import pandas as pd


# Define the path to required files
json_structure_file = "format.json"
vg_file = "data/valuergeneral/raw/2022/20220103/001_SALES_DATA_NNME_03012022.DAT"
csv_file = "data/valuergeneral/csv/001_SALES_DATA_NNME.csv"

# Prepare data structures for DAT file parsing into dict
with open(json_structure_file) as file:
    json_structure = json.load(file)

vg_data = {"RecordA": [], "RecordB": [], "RecordC": [], "RecordD": [], "RecordZ": []}

# Function to parse a single line of the file based on the provided record structure
def parse_line(line, record_structure):
    """ Parse a single line of the file based on the provided record structure """
    fields = line.strip().split(';')
    record = {}
    for key in record_structure.keys():
        # Pop the first element if available, else assign None
        record[key] = fields.pop(0) if fields else None
    return record

# iterate over DAT file to convert into dictionary
with open(vg_file, 'r') as file:
    for line in file:
        lineIdx = line[0]
        # print(f"lineIdx:{lineIdx}")
        # print(f"line:{line}")
        # for element in line:
        if lineIdx == 'A':
            record = parse_line(line, json_structure["RecordA"])
            vg_data["RecordA"].append(record)
        elif lineIdx == 'B':
            record = parse_line(line, json_structure["RecordB"])
            vg_data["RecordB"].append(record)
        elif lineIdx == 'C':
            record = parse_line(line, json_structure["RecordC"])
            vg_data["RecordC"].append(record)
        elif lineIdx == 'D':
            record = parse_line(line, json_structure["RecordD"])
            vg_data["RecordD"].append(record)
        elif lineIdx == 'Z':
            record = parse_line(line, json_structure["RecordZ"])
            vg_data["RecordZ"].append(record)


# Print the processed data for each record type
print("Dictonary output:")
for record_type, records in vg_data.items():
    print(f"{record_type}: {records}")

# Convert dict to dataframe and ultimately csv file
dfs = []
for record_type, records in vg_data.items():
    df = pd.DataFrame(records)
    # Drop the 'recordType' column
    if 'recordType' in df.columns:
        df = df.drop('recordType', axis=1)
    dfs.append(df)

# Concatenate all DataFrames horizontally
combined_df = pd.concat(dfs, axis=1)

print("Dataframe output:")
print(combined_df)
with open(csv_file, 'w') as file:
    csv_file = combined_df.to_csv(file)
