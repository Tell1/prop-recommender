# prop-recommender
Property recommender to support users with their investment decisions

## Downloading Valuer General datasets.
- [Link to downloads](https://valuation.property.nsw.gov.au/embed/propertySalesInformation)
- [Link to document that describes the structure of the individual files](https://www.valuergeneral.nsw.gov.au/__data/assets/pdf_file/0015/216402/Current_Property_Sales_Data_File_Format_2001_to_Current.pdf)

1. Manually download the files for X years up to the current year.
2. `make setup` to create directory structure
<<<<<<< HEAD
3. `make unzip` to unzip the files in a directory for a given year. (change DIR to path/to/year that contains your .zip files)
4. Convert the .DAT files into a single row of a .CSV, for each .DAT file.
=======
3. `make unzip` to unzip the files in a directory for a given year. (change DIR to path/to/year that contains your .zip files)
>>>>>>> 6b3a7f0a413cb82df78322724d128433fa481b30
