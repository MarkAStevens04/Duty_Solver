import openpyxl

# Define variable to load the dataframe
dataframe = openpyxl.load_workbook("Excel_Files/Test.xlsx")

# Define variable to read sheet
dataframe1 = dataframe.active

# Iterate the loop to read the cell values
for row in range(1, dataframe1.max_row):
    for col in dataframe1.iter_cols(1, dataframe1.max_column):
        print(col[row].value)
    print(f'-----')