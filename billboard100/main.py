import requests
from bs4 import BeautifulSoup


date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD")
URL = f"https://www.billboard.com/charts/hot-100/{date}/"

response  = requests.get(URL)
yc_web_page = response.text
soup = BeautifulSoup(yc_web_page,"html.parser")

all_songs = soup.select("li ul li h3")
song_names = [song.getText().strip() for song in all_songs]

print(song_names)


