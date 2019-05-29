# US-City-Wiki-Scraping
Scraping data from Wikipedia page of top USA Cities https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population.
This is code coded using BeautifulSoup4 and Requests to parse and extract HTML data from the wiki page.
This code works by extracting data from not only from the fields of the table on the link given but also the individual city pages.
Except the main table on the link,it extracts mayor name,area code,summer(DST),Time zone and website from the individual pages.

The dependencies used for running this Scraper:
1.Requests
2.BeautifulSoup4
3.Pandas
All of these can be installed using pip install requests/bs4/pandas.
The generated CSV is suitable to be uploaded on BigQuery table.

