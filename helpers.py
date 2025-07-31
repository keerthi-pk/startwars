import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_with_ssl(url):
    return requests.get(url, verify=False)


def find_row_by_cell_text(rows, nth_col, text):
    for row in rows:
        cells = row.find_elements_by_tag_name("td")
        if cells and cells[nth_col].text == text:
            return row
    return None
