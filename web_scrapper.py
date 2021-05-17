import os
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import pandas as pd

#new changes
#add to develop

url = "http://electionevents.in/"

map = r'Map/'
if not os.path.exists(map):os.mkdir(map)
voter = r'Voter/'
if not os.path.exists(voter):os.mkdir(voter)


response = requests.get(url)
soup= BeautifulSoup(response.text, "html.parser")
file_name = {}
for link in soup.select("a[href$='.pdf']"):

    finalward = 's3FinalWards'
    voterlist = 's2voterList'

    if voterlist in link['href']:
        print(link)
        filename = os.path.join(voter, link['href'].split('/')[-1])
        file_name[link['href'].split('/')[-1]] = 'failed'
        with open(filename, 'wb') as f:
            f.write(requests.get(urljoin(url, link['href'])).content)
        file_name[link['href'].split('/')[-1]] = 'success'
    elif finalward in link['href']:
        print(link)
        filename = os.path.join(map,link['href'].split('/')[-1])
        file_name[link['href'].split('/')[-1]] = 'failed'
        with open(filename, 'wb') as f:
            f.write(requests.get(urljoin(url,link['href'])).content)
        file_name[link['href'].split('/')[-1]] = 'success'

files_downloaded = pd.DataFrame(file_name.items(),columns=['Filename','status'])
files_downloaded.to_csv('Files Downloaded.csv',index=False)
