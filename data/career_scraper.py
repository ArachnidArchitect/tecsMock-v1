import requests
import pandas as pd 
from bs4 import BeautifulSoup

URL = "https://www.southafricaeducation.info/career-options"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.google.com/"
}

response = requests.get(URL, headers=headers)


array = []
if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")
    
    theLinks = soup.find(id="TheLinks")
    

    if theLinks:
        for career in theLinks:
            array.append(career.text.strip())
    else:
        print("there is no data here. check the structure of the page again.")

    array.pop()
    array.pop(2)
    array.pop(1)
    array.pop(0)
    print(len(array))

    dict = {"name": array}

    df = pd.DataFrame(dict)

    print(df)
    df.to_csv('careers_in_sa.csv')