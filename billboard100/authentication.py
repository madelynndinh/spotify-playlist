import spotipy
import requests
from spotipy.oauth2 import SpotifyOAuth
from bs4 import BeautifulSoup


#setup spotify authentication
CLIENT_ID = "47aae2a48c3e464da4159ae99ecdc48d"
CLIENT_SECRET = "14390c26ba194dca8ba76d71ffa600d7"
REDIRECT_URI = "http://example.com"
OAUTH_AUTHORIZE_URL= 'https://accounts.spotify.com/authorize'
spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=f"{CLIENT_ID}",
                                               client_secret=f"{CLIENT_SECRET}",
                                               redirect_uri=f"{REDIRECT_URI}",
                                               scope="playlist-modify-private",
                                               cache_path=".cache"))

#get user id of spotify acount to prepare playlist creation
user_id = spotify.current_user()["id"]


#scrape data (bilboard 1-100 for givern day
# date = "2024-01-01"
playlistName = input("What do you want to name your playlist? ")
date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
URL = f"https://www.billboard.com/charts/hot-100/{date}/"
response= requests.get(URL)
yc_web_page = response.text
soup = BeautifulSoup(yc_web_page,"html.parser")
all_songs = soup.select("li ul li h3")
artist_for_songs_scrap = soup.select("li ul li span")

#string song name and artist name
song_names = [song.getText().strip() for song in all_songs]
song_artist = [song.getText().strip() for song in artist_for_songs_scrap]
song_artist = [x for x in song_artist if not (x.isdigit()  or x[0] == '-' and x[1:].isdigit())]
song_uris=[]
year = date.split("-")[0]

#create 2d array to combine stripped song name and artist name
songArrray = []
for key in song_names:
    for value in song_artist:
        songArrray.append({'song': key, 'artist': value})
        song_artist.remove(value)
        break

#query spotify api
for entry in songArrray:
    result = spotify.search(q=f"{entry['song']}artist={entry['artist']}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
        print(f"{entry['song']} added...")
    except IndexError:
        print(f"{entry['song']} doesnt exist in Spotify. Skipped")
playlist_id = spotify.user_playlist_create(user=user_id,name=f"{playlistName} - {date}",public=False)["id"]
response = spotify.playlist_add_items(playlist_id=playlist_id,items=song_uris)

print(f"{response} playlist created")
