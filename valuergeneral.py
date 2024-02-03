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
  
.DAT files structure:
data/valuergeneral/raw/2022/20220103/001_SALES_DATA_NNME_03012022.DAT
data/valuergeneral/raw/2022/20220103/004_SALES_DATA_NNME_03012022.DAT
data/valuergeneral/raw/2022/20220103/005_SALES_DATA_NNME_03012022.DAT
  
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
    "RecordB": {"recordType": "B", "districtCode": "001", "propertyId": "4255491", "saleCounter": "1", "downloadDateTime": "20220103", "propertyName": "", "propertyUnitNumber": "","propertyHouseNumber": 9}
      "propertyStreetName": {"type": "N", "size": 38, "required": false},
      "propertyLocality": {"type": "N", "size": 40, "required": false},
      "propertyPostCode": {"type": "N", "size": 4, "required": false},
      "area": {"type": "N", "size": 7.3, "required": false},
      "areaType": {"type": "N", "size": 1, "required": false},
      "contractDate": {"type": "Date", "size": 8, "required": true, "format": "CCYYMMDD"},
      "settlementDate": {"type": "Date", "size": 8, "required": true, "format": "CCYYMMDD"},
      "purchasePrice": {"type": "N", "size": 12, "required": true},
      "zoning": {"type": "A", "size": 4, "required": false},
      "natureOfProperty": {"type": "A", "size": 1, "required": false},
      "primaryPurpose": {"type": "A", "size": 20, "required": false},
      "strataLotNumber": {"type": "A", "size": 5, "required": false},
      "componentCode": {"type": "A", "size": 3, "required": false},
      "saleCode": {"type": "A", "size": 3, "required": false},
      "percentInterestOfSale": {"type": "A", "size": 3, "required": false},
      "dealingNumber": {"type": "A", "size": 10, "required": true}
    },
}

DataFrame/CSV example:

    districtCode propertyId saleCounter area areaType contractDate settlementDate purchasePrice
    0           001   4255491           1  600.9        M   20200928     20211224       572300

"""

"""
TODO: Add unit tests for data conversion
TODO: Extend script to convert multiple DAT files to csv
"""

import zipfile
import os
import json
import pandas as pd


# Define the path to required files
vg_file = "data/valuergeneral/raw/2022/20220103/001_SALES_DATA_NNME_03012022.DAT"
csv_file = "data/valuergeneral/csv/001_SALES_DATA_NNME.csv"
vg_zip_file = "data/valuergeneral/raw/2022/20220103.zip"
tmp_dat_dir = "data/valuergeneral/tmp"


def parse_dat_file(source_file, vg_data, json_structure):
    """
    Parse a .dat file into a pandas DataFrame based on the provided JSON structure.

    Args:
        source_file (str): The path to the .dat file to be parsed.
        json_structure (dict): The structure of the JSON to be used for parsing.

    Returns:
        pandas.DataFrame: The combined dataframe containing the parsed records.
    """
    print(f"Parsing file: {source_file}")

    # iterate over DAT file to convert into dictionary
    with open(source_file, 'r') as file:
        lines = [line.strip() for line in file.readlines() if line.strip()]  # remove empty lines
        for line in lines:
            vg_data = parse_vg_record(line, vg_data, json_structure)

    # Convert dict to dataframe and ultimately csv file
    dfs = []

    for record_type, records in vg_data.items():
        df = pd.DataFrame(records)
        # Drop the 'recordType' column
        if 'recordType' in df.columns:
            df = df.drop('recordType', axis=1)
            # print(f"Records: {record_type}")
            # print(f"Dataframe: {df}")
        dfs.append(df)

    # Concatenate all DataFrames horizontally
    return pd.concat(dfs, axis=1)

def parse_vg_record(line, vg_data, json_structure):
    """
    Parse VG records from a JSON structure and populate vg_data with the parsed records.

    :param json_structure: The JSON structure used for parsing the records
    :param vg_data: The dictionary to populate with the parsed records
    :param file: The file containing the records to parse
    :return: None
    """
    
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

    return vg_data
    

def parse_line(line, record_structure):
    """
    Parse a line of text based on the given record structure and return a dictionary.
    Input: B;001;4255491;1;20220103 01:01;;;9;GARLAND RD;CESSNOCK;2325;600.9;M;20200928;20211224;572300;R2;R;RESIDENCE;;AAB;;0;AR772723;
    Output: {"recordType": "B", "districtCode": "001", "propertyId": "4255491", "saleCounter": "1", "downloadDateTime": "20220103", "propertyName": "", "propertyUnitNumber": "","propertyHouseNumber": 9}
    
    :param line: The line of text to be parsed.
    :param record_structure: A dictionary representing the structure of the record.
    :return: A dictionary containing the parsed fields based on the record structure.
    """
    fields = line.strip().split(';')
    record = {}
    for key in record_structure.keys():
        # Pop the first element if available, else assign None
        record[key] = fields.pop(0) if fields else None
    return record

def main():
    """
    Prepare data structures for DAT file parsing into dict

    vg_dfs: List of dataframes for each .dat file
    """
    vg_dfs = []
    vg_data = {"RecordA": [], "RecordB": [], "RecordC": [], "RecordD": [], "RecordZ": []}
    json_structure_file = "format.json"
    with open(json_structure_file) as file:
        json_structure = json.load(file)

    # Unzip and iterate over the files
    with zipfile.ZipFile(vg_zip_file, 'r') as zip_ref:

        # Extract all files to a temporary directory
        zip_ref.extractall(tmp_dat_dir)

        # Iterate over the extracted files
        for foldername, subfolders, filenames in os.walk(tmp_dat_dir):
            # print(f"Foldername: {foldername}, Filenames: {filenames}")
            for filename in filenames:
                file_path = os.path.join(foldername, filename)
                
                # Call the parse_dat_file function for each .dat file
                if file_path.endswith('.DAT'):
                    combined_df = parse_dat_file(file_path, vg_data, json_structure)
                    
                    vg_dfs.append(combined_df)

            combined_super_df = pd.concat(vg_dfs, axis=0)
            print(f"Combined Dataframes: {combined_super_df}")


        with open(csv_file, 'w') as file:
            target_file = combined_super_df.to_csv(file)

    print("All files processed.")


if __name__ == "__main__":
    main()