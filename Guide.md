# Duty Solver Guide

### Requirements
- Duty schedule spreadsheet ends with .xlsx
- There are two "landmarks" the program will look for.

### Formatting
**Landmarks**: There are three "landmarks" that the program will look for. These are cells that define the edges of the box containing all the data. 
The first landmark goes above the top left corner of the data, and should have the word "points". 
The second landmark goes beside the bottom left corner of the data, and should say "Instructions".
The final landmark is having a column where the date entry is empty. This will be on the right most edge of the data.

### Instructions
1. Ensure the spreadsheet matches the correct format.
2. Make sure the duty availability spreadsheet has the name "TEST.xlsx"
3. Move the  spreadsheet into Excel_Files > Given_Workbooks
4. Run the python program. You will receive a solved schedule in the Solved_Workbooks folder.