import requests
from bs4 import BeautifulSoup

def drive_download(url):

    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}

    response= requests.get(url.strip(), headers=headers, timeout=10)

    soup = BeautifulSoup(response.text, features="lxml")
    
    # Scrape gdrive file id
    data_ids = soup.find_all(attrs={"data-id": True})

    for data in data_ids:

        file_name = data.text
        data_id = data['data-id']

        # With file id, generate download url
        complete_url = "https://drive.google.com/u/0/uc?id=" + data_id + "&export=download"

        # With download url, scrape direct download link and download it
        response = requests.get(complete_url.strip(), headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, features="lxml")

        form = soup.select("#downloadForm")
        link = form[0]['action']

        with open(file_name, "wb") as file:
            print("Downloading " + file_name + "...")
            response = requests.get(link)
            file.write(response.content)