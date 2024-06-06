import openpyxl

path_original = ''
path_final = ''

def get_origin():
    # Returns the origin for the sheet!
    # 3, 2 would mean row 3 column 2, or cell C3
    # (column indexes by 0, row doesn't)
    return 3, 2

def get_end():
    # Returns the bottom right corner for the sheet!
    # 4, 6 would mean row 4 column 6, or cell G4
    # AL 10
    # Inclue
    return 10, 37


def process_entry(entry):
    val = 0
    if entry:
        entry_array = entry.split()
        try:
            val = int(entry_array[-1])
        except:
            print(f'ERROR ERROR ERROR ERROR ERROR')
            print(f'invalid entry!')
            print(f'entry:{entry}.')
            print(f'entry array:{entry_array}')
            print(f'ERROR ERROR ERROR ERROR ERROR')
    return val


def open_notebook(path):
    # Takes a path to a .xlsx file.
    # Returns tuple of availability, dates, and names.
    global path_original
    path_original = path

    # Define variable to load the dataframe
    dataframe = openpyxl.load_workbook(path)

    # Define variable to read sheet
    dataframe1 = dataframe.active


    # Start by getting all the dates
    dates = []
    availability = []
    availability1 = []
    names = []

    # create data structure for availability!
    # Simultaneously add names to name list
    found_instructions = False
    for row in range(2, dataframe1.max_row):
        for col in dataframe1.iter_cols(1, 1):
            # now we're going through the entire first column!
            # We have to stop once we find the line containing
            # the phrase "Instructions"
            if not found_instructions:
                entry = col[row].value.strip()
                if entry.strip() == "Instructions":
                    found_instructions = True
                else:
                    names.append(entry)
                    availability.append([])
                    availability1.append([])

    r, c = get_origin()
    r_f, c_f = get_end()

    for row in range(r, r_f + 1):
        for col in range(c, c_f + 1):
            availability1[row - r].append(process_entry(dataframe1[row][col].value))

    dataframe.save(path)
    print(f'*****')

    return availability1, dates, names


def save_workbook(availability):
    print(f'inside exporting')
    global path_original
    global path_final
    print(f'path original: {path_original}')
    path_final = 'Excel_Files/Solved_Workbooks/'
    path_final += path_original.split('/')[-1]
    print(f'path final: {path_final}')

    wb = openpyxl.load_workbook(path_original)
    # target = wb['Block 1 Avail. (Apr 26-May 31)']
    # wb.create_sheet('TEST SHEET')
    # wb.copy_worksheet(target)
    sheet = wb.active
    wb.save(path_original)
    # sheet[row][column] ~ sheet[numer][letter]
    r, c = get_origin()
    for row in range(r, min(len(availability) + r, sheet.max_row)):
        for col in range(c, min(len(availability[0]) + c, sheet.max_column)):
            # print(f'row: {row}, column {col}')
            # print(f'value: {availability[row-r][col-c]}')
            if availability[row-r][col-c] == 0:
                sheet[row][col].value = None

    wb.save(path_final)

    

    # final_wb = original_wb.copy_worksheet()
    # final_wb.save(path_final)
    print(f'finished')
    while True:
        pass

    # final_wb = openpyxl.load_workbook(path_final)











if __name__ == "__main__":
    availability, dates, names = open_notebook("Excel_Files/Given_Workbooks/Test.xlsx")

    print(f'-----------------------')
    print(dates)
    print(names)
    print(f'---')
    for row in availability:
        print(row)

    print(len(availability[0]))
