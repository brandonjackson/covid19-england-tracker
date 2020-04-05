import requests
from bs4 import BeautifulSoup
import xlrd
import json

url = "https://fingertips.phe.org.uk/documents/Historic%20COVID-19%20Dashboard%20Data.xlsx"

response = requests.get(url)
with open('data-from-phe.xlsx', 'wb') as f:
    f.write(response.content)

xl_workbook = xlrd.open_workbook('data-from-phe.xlsx')

sheet_names = xl_workbook.sheet_names()
print('Sheet Names', sheet_names)


utla_sheet = xl_workbook.sheet_by_index(5)
num_cols = utla_sheet.ncols   # Number of columns

# FIND HEADER ROW INDEX
header_row_idx = 0;
for row_idx in range(0, utla_sheet.nrows):    # Iterate through rows
    cell_obj = utla_sheet.cell(row_idx, 0)
    if(cell_obj.value=="Area Code"):
        header_row_idx = row_idx;
        break;

utla_data = {}

for col_idx in range(2, utla_sheet.ncols):    # Iterate through rows
    today = xlrd.xldate.xldate_as_datetime(utla_sheet.cell(header_row_idx, col_idx).value, xl_workbook.datemode).date().isoformat()
    print ('-'*40)
    print(today)
    utla_data[today] = {}
    for row_idx in range(header_row_idx+1, utla_sheet.nrows):    # Iterate through rows
        place = utla_sheet.cell(row_idx, 1).value.strip();
        number_obj = utla_sheet.cell(row_idx, col_idx)  # Get cell object by row, col

        if(place=="England"):
            continue;
        utla_data[today][place] = int(number_obj.value)
        print ('%s: %.0d' % (place, number_obj.value))

print(json.dumps(utla_data))

totals_data = {}

uk_sheet = xl_workbook.sheet_by_index(1)
header_row_idx = 0;
for row_idx in range(0, uk_sheet.nrows):    # Iterate through rows
    cell_obj = uk_sheet.cell(row_idx, 0)
    if(cell_obj.value=="Date"):
        header_row_idx = row_idx
        print(header_row_idx)
        break
for row_idx in range(header_row_idx+1, uk_sheet.nrows):    # Iterate through rows
    today = xlrd.xldate.xldate_as_datetime(uk_sheet.cell(row_idx, 0).value, xl_workbook.datemode).date().isoformat()
    totals_data[today] = {}
    number = int(uk_sheet.cell(row_idx, 2).value)  # Get cell object by row, col
    totals_data[today]["UK"] = number;


regions_sheet = xl_workbook.sheet_by_index(4)
header_row_idx = 0;
for row_idx in range(0, regions_sheet.nrows):    # Iterate through rows
    cell_obj = regions_sheet.cell(row_idx, 0)
    if(cell_obj.value=="Area Code"):
        header_row_idx = row_idx
        break
for col_idx in range(2, regions_sheet.ncols):    # Iterate through rows
    today = xlrd.xldate.xldate_as_datetime(regions_sheet.cell(header_row_idx, col_idx).value, xl_workbook.datemode).date().isoformat()

    for row_idx in range(header_row_idx+1, regions_sheet.nrows):    # Iterate through rows
        place = regions_sheet.cell(row_idx, 1).value.strip();
        if(place==""):
            place = "Unconfirmed"
        number = int(regions_sheet.cell(row_idx, col_idx).value)  # Get cell object by row, col
        totals_data[today][place] = number

print(json.dumps(totals_data))

with open('utla_data.js', 'w') as f:
    f.write("const cases_archive = " + json.dumps(utla_data))
with open('totals_data.js', 'w') as f:
    f.write("const nhs_totals = " + json.dumps(totals_data))

