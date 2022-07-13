# Import Libraries
from itertools import product
from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.error import HTTPError, URLError
import numpy as np
import re
import requests
import pandas as pd
import os


########## URL Test ###########
# URL= "https://en.wikipedia.org/wiki/International_Phonetic_Alphabet_chart_for_English_dialects"
# URL = 'https://en.wikipedia.org/wiki/List_of_largest_manufacturing_companies_by_revenue'
# URL= "https://en.wikipedia.org/wiki/List_of_European_countries_by_population"

def scrape(URL, key_word, non_ASCII, nr_tables, nr_rows, col_list, file_name, path, format):
    ######### Scrape HTML ###########
    response = requests.get(URL)
    ### Verify if URL is valid
    try:
        html = urlopen(URL)
    except HTTPError as e:
        print(e)
    except URLError as e:
        print("The server could not be found!")
    else:
        print("It works! :)")
        ### Instantiate a Beautiful Soup Object
        soup = BeautifulSoup(response.text, 'html.parser')
        ### Scrape all tables from page
        #regex = r"\b(\w*{}\w*)\b".format(key_word)
        tables = soup.findAll("table", {"class": key_word})
        print(len(tables))
        ####### Scrape each table from page #######
        ### Nr of desired table to scrape
        if nr_tables:
            n = nr_tables
        else:
            n = len(tables)
        ### Get each table
        for tn in range(0, n):
            table_el = tables[tn]
            ### Build an empty list for all merged rows
            rowspans = []
            ### Get all rows in the current table
            rows = table_el.find_all('tr')
            ### Nr of desired rows to scrape
            if nr_rows:
                n_rows = nr_rows
            else:
                n_rows = len(rows)
            ### Get only desired rows
            rows = [rows[row] for row in range(n_rows)]

            ### Scan for numbers of cols (including spanned)
            colcount = 0
            for r, row in enumerate(rows):
                cells = row.find_all(['td', 'th'], recursive=False)
                # Ignore the colspan value on the last cell, to prevent creating 'phantom' columns with no actual cells, only extended
                # colspans. This is achieved by hardcoding the last cell width as 1.
                # a colspan of 0 means “fill until the end” but can really only apply
                # to the last cell; ignore it elsewhere.
                colcount = max(colcount,
                               sum(int(c.get('colspan', 1)) or 1 for c in cells[:-1]) + len(cells[-1:]) + len(rowspans)
                               )
                ### Update rowspan ### 0 is a span to the bottom.
                rowspans += [int(c.get('rowspan', 1)) or len(rows) - r for c in cells]
                rowspans = [s - 1 for s in rowspans if s > 1]

            ### Build an empty matrix for all possible cells
            table = [[None] * colcount for row in rows]

            ### Fill matrix from row data
            ### Build an empty dict
            rowspans = {}
            for row, row_elem in enumerate(rows):
                span_offset = 0  # how many columns are skipped due to row and colspans
                for col, cell in enumerate(row_elem.find_all(['td', 'th'], recursive=False)):
                    # Adjust for preceding row and colspans
                    col += span_offset
                    while rowspans.get(col, 0):
                        span_offset += 1
                        col += 1

                    ### Fill table data
                    rowspan = rowspans[col] = int(cell.get('rowspan', 1)) or len(rows) - row
                    colspan = int(cell.get('colspan', 1)) or colcount - col
                    ## next column is offset by the colspan
                    span_offset += colspan - 1
                    value = cell.get_text()
                    value = value.strip()
                    regex = r"\[.*?\]"
                    value = re.sub(regex, '', value)
                    regex = r"/\W+/g"
                    value = re.sub(regex, '', value)
                    if non_ASCII:
                        regex = r'[^\x00-\x7F]'
                        value = re.sub(regex, '', value)

                    for drow, dcol in product(range(rowspan), range(colspan)):
                        try:
                            table[row + drow][col + dcol] = value
                            rowspans[col + dcol] = rowspan
                        except IndexError:
                            ## rowspan or colspan outside the confines of the table
                            pass
                ## update rowspan
                rowspans = {c: s - 1 for c, s in rowspans.items() if s > 1}

            s1 = pd.DataFrame(table)
            ### Define a list with all cols
            if col_list:
                print(col_list)
                col_list0 = [i for i in range(colcount)]
                ### Delete extra cols from data frame
                col_list_del = list(set(col_list0) - set(col_list))
                s1 = s1.drop(s1.columns[col_list_del], axis=1)

            print(s1)
            if format == 'CSV':
                s1.to_csv(os.path.join(path, '{}_{}.csv'.format(file_name, tn)), index=False)
            elif format == 'JSON':
                s1.to_json(os.path.join(path, '{}_{}.json'.format(file_name, tn)), index=True)
            else:
                try: s1.to_sql(os.path.join(path, '{}_{}.myd'.format(file_name, tn)), index=True)
                except Exception as e: continue

### Get URL path section as table name
# URL = 'https://en.wikipedia.org/wiki/List_of_largest_manufacturing_companies_by_revenue'
# page = os.path.split(URL)[1]
# col_list = [0,1,3]
# scrape(URL,'wiki',1,10,col_list,page,'/home/palade/Documents/proiecte/Sisteme de Operare','CSV')
