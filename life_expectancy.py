# -*- coding: utf-8 -*-
"""
Created on Wed Dec 19 15:49:12 2018
@author: Jakub Parcheta
"""


from bs4 import BeautifulSoup
import requests
import pandas as pd

url = 'https://docs.google.com/spreadsheets/d/1dgOdlUEq6_V55OHZCxz5BG_0uoghJTeA6f83br5peNs/pub?range=A1:D70&gid=1&output=html#'

r = requests.get(url)
html_doc = r.text
soup = BeautifulSoup(html_doc, features='html.parser')


datadiv=soup.find("div", {"id": "0"})
elementsfull =[]
row=0
for tr in datadiv.findAll("tr"):

    elements=[]
    column=0
    for td in tr.findAll("td"):
        if(td.text!=''):
            elements.append(td.text)
            column+=1 
    elementsfull.append(elements)            
    row+=1

df = pd.DataFrame(data=elementsfull)

print('DataFrame info:')

print(df.info(verbose=False))


"""
Data cleaning
"""

df = df.drop(df.index[[0,2]])                   # drop first and third row with None values
df.columns = df.iloc[0]                         # set first row as columns names
df = df.drop(df.index[[0]])
df.set_index('LEX, IHME', inplace = True)       # set first column as an index
df.index.name = 'Countries'
df = df.apply(pd.to_numeric, errors='coerce')   # drop all rows with None values
df = df.dropna()
#print(df)

# df.to_csv('Data.csv', sep=',', encoding='utf_8_sig')     # write cleaned data in csv file


"""
Exploring data
"""
# life expectancy growth (differance between 1990 and 2013)

growth = []
for index, row in df.iterrows():           
    differance = row['2013'] - row['1990']
    growth.append([index, round(differance, 2)])

df_2 = pd.DataFrame(growth, columns =['COUNTRIES', 'growth'])
df_2.set_index('COUNTRIES', inplace = True)

# countries where the live expectancy increased radically
df_2.sort_values("growth", axis = 0, ascending = True, inplace = True, na_position ='first')

df_3 = df_2.tail(10)
df_3.name = 'Countries where life expectancy grew exponentially (1990-2013)'
print(df_3.name)

print(df_3)
