import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
import json

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

scope = ['https://spreadsheets.google.com/feeds']

credentials = ServiceAccountCredentials.from_json_keyfile_name('/Users/kevindenny/Documents/django_nimbus/nimbus/nimbus-charts-00bde45ffdb8.json', scope)

gc = gspread.authorize(credentials)

def get_headers(sheet):
    headers = sheet.row_values(1)
    cleansed_headers = []

    for h in headers:
        if h.strip() != '':
            cleansed_headers.append(h)

    return cleansed_headers


def read_data(sheet, headers):
    new_json = []
    list_of_lists = sheet.get_all_values()
    for i, row in enumerate(list_of_lists):
        if i > 0:
            new_row = {}
            for ho in headers:
                hitem = str(row[headers.index(ho)])
                hitem_nop = hitem.replace('%','')
                if is_number(hitem):
                    new_row[ho] = float(hitem)
                elif is_number(hitem_nop):
                    new_row[ho] = (float(hitem_nop) / 100.0)
                elif (hitem == ''):
                    new_row[ho] = 0
                else:
                    new_row[ho] = hitem
            new_json.append(new_row)
    
    return new_json

def get_keyed_json_object(url, sheet_name, key_field):
    init_data = get_json_array(url, sheet_name)
    keyed_json = {}
    for row in init_data:
        this_key = row[key_field]
        nrow = row
        del nrow[key_field]
        keyed_json[this_key] = nrow

    jfile_name = sheet_name + '_keyed.json'
    with open(jfile_name, 'wb') as ofile:
        json.dump(keyed_json, ofile)
    
    return keyed_json



def get_json_array(url, sheet_name):
    sheet_file = gc.open_by_url(url)
    worksheet = sheet_file.worksheet(sheet_name)
    headers = get_headers(worksheet)
    data = read_data(worksheet, headers)

    jfile_name = sheet_name + '.json'
    with open(jfile_name, 'wb') as ofile:
        json.dump(data, ofile)

    return data



sheet_url = 'https://docs.google.com/spreadsheets/d/1jyWzlila-hzJJAF2rWGfbbCELwW3gx2wVQlIWS8lB5Y'
sheet_name = 'Sheet1'


new_data = get_json_array(sheet_url, sheet_name)

