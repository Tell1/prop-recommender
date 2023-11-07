"""
Script to extract the data from tables in a PDF file.
"""
import camelot

file = "/mnt/c/Users/ssch7/repos/prop-recommender/data/valuergeneral/raw/Current_Property_Sales_Data_File_Format_2001_to_Current.pdf"
tables = camelot.read_pdf(file)

# number of tables extracted
print("Total tables extracted:", tables.n)

for i in range(tables.n):
    print(tables[i].df)
    tables[i].to_csv(f"/mnt/c/Users/ssch7/repos/prop-recommender/data/valuergeneral/raw/fileformat_{i+1}.csv")

