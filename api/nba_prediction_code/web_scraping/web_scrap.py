import requests
from bs4 import BeautifulSoup
from pprint import pprint 
import numpy as np


def web_scrap_data():
    url = 'http://www.hoopsstats.com/basketball/fantasy/nba/teamstats'

    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    tables = soup.findAll("table")

    # Filter tables to only those that have exactly one <tr> element
    filtered_tables = [table for table in tables if len(table.find_all('td')) == 21]


    # Initialize a list to store the <td> elements from each table
    td_elements = []

    # Loop through each filtered table
    for idx, table in enumerate(filtered_tables):
        # Find all <td> elements in the table
        tds = table.find_all('td')
        # Add the text from each <td> to the td_texts list
        current_array = [] 
        for td in tds:
            current_array.append(td.get_text(strip=True))    
        td_elements.append(current_array)
    td_elements = td_elements[1:]
    return {sub_array[1]: sub_array[:1] + sub_array[1+1 :] for sub_array in td_elements if len(sub_array) >= 2}