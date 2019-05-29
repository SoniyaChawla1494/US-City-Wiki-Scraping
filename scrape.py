#Dependencies needed:
#1.Requests
#2.BeautifulSoup
#3.Pandas

import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_html(url):
  thepage = requests.get(url)
  bs_soup = BeautifulSoup(thepage.text, "lxml")
  return bs_soup

def start_scraping():
  theurl = "https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population"
  soup = get_html(theurl)
  
  #take entire table html code and extract headers
  table = soup.find('table', {'class':'wikitable sortable'})
  rows=table.find_all('tr')
  columns=[v.text.replace('\n','').replace('[c]','') for v in rows[0].find_all('th')]
  new_page_columns=['Mayor','Area codes','Website','Time zone', 'Summer (DST)'] #Data to be extracted from individual links of cities
  df=pd.DataFrame(columns=columns) #Create Dataframe consisting of all table's data
  df1=pd.DataFrame() #Create Dataframe consisting of all data from individual links of cities


  #create a link for every row. We traverse row by row
  for i in range(1,len(rows)):
    #Extract values for the respective headers from the table and add in the the DataFrame-df
    tds = rows[i].find_all('td')
    values = [td.text.replace('\n','') for td in tds]
    values.pop(6)
    values.pop(8)
    df = df.append(pd.Series(values,index=columns),ignore_index=True)
    
    #Collect link for the particular city
    link= rows[i].find('a')['href']
    url_city="https://en.wikipedia.org"+link
    
    #Scraping from new page
    soup2 = get_html(url_city)
    table2= soup2.find('table', {'class':'infobox geography vcard'})
    rows2=table2.find_all('tr')
    
    #Definitions- Dictionary defined to hold firstly position values using counter in the entire html page by index
    columns2=[] 
    counter=[]
    dct = {'Mayor':'NA','Area codes':'NA','Website':'NA','Time zone':'NA', 'Summer (DST)':'NA'}
    
    #Finding Headers on Individual City Page and its corresponding Data
    for i in range(0,len(rows2)):
      columns3=[v.text.replace('\xa0•\xa0','').replace('(s)','s') for v in rows2[i].find_all('th')]
      columns2.append(columns3)
      result = any(elem in columns3 for elem in new_page_columns)
      if result is True:
        counter.append(i)
        dct[columns3[0].strip()]=i

    #Traversing by the positions of required data we want to extract and overwriting the dictionary by the values
    for key,val in dct.items():
      if val is 'NA':
        continue
      tds = rows2[val].find_all('td')
      a=tds[0].find_all('a')
      values = [atag.text for atag in a]
      if len(values)==0:
        dct[key]="NA"
      else:
        dct[key]=values[0]
    #Appending Individual City Page data to new Dataframe
    df1=df1.append(dct,ignore_index=True)
  
  #Joining the DataFrames and finally creating a CSV of it
  df = df.join(pd.DataFrame(df1, index=df.index))
  df.to_csv("USACities.csv",encoding='utf-8-sig')
  
start_scraping()
