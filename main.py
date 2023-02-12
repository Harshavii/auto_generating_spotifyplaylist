import requests
import os
import spotipy
from bs4 import BeautifulSoup
year = input("Which year do you want to travel to? Type the year (YYYY) \n")

Id = os.environ['client_id']
# print(Id)
secret = os.environ['client_secret']
# print(secret)
response = requests.get(f"https://www.billboard.com/charts/year-end/{year}/hot-100-songs/")
billboard = response.text
soup = BeautifulSoup(billboard,"html.parser")
titles = []
for t in soup.select(selector="li h3",class_="c-title"):
    titles.append(t.getText().strip())

song_list = titles[0:100]
# print(song_list)
index = 1

# with open("Playlist.txt","w") as file:
#     for heading in titles[0:100]:
#         file.write(f"{index}] {heading}\n")
#         index += 1

#spotify authentication
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="ac1b76c8af0749bfae0287ea1c046fc0",
                                               client_secret="dfad15e947314a11a66df4dc86860b20",
                                               redirect_uri="https://example.com",
                                               scope="playlist-modify-private",
                                               show_dialog=True,
                                               cache_path="tokens.txt"))

user = sp.current_user()
# # print(user)
user_id = user["id"]
# print(user_id)
uris = []
for songs in song_list:
    result = sp.search(q=f"track:{songs} year:{year}",type="track",market="ES",limit=1)
    # print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        uris.append(uri)
    except IndexError:
        print(f"{songs} doesn't exist in Spotify. Skipped.")

# print(uris)
playlist = sp.user_playlist_create(user=user_id, name=f"{year}'s Billboard 100", public=False)
# print(playlist)

sp.playlist_add_items(playlist_id=playlist["id"], items=uris)