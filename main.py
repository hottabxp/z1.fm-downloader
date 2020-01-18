"""
    z1.fm downloader.
    Sergey Karbivnichiy 2020
"""
import requests
import os
from urllib3.exceptions import InsecureRequestWarning
import urllib3

from bs4 import BeautifulSoup
from pathlib import Path

version = '0.1.2'
url_ = 'https://z1.fm/new?sort=date'
download_dir = str(Path.home())+'/Музыка/z1.fm/'

headers = {	'user-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:72.0)'
            ' Gecko/20100101 Firefox/72.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;'
            'q=0.9,image/webp,*/*;q=0.8',
            'Referer': 'https://z1.fm/'
            }

all_songs = []


def get_songs(url):
    responce = requests.get(url)
    soup = BeautifulSoup(responce.text, "html.parser")
    container = soup.find('section', {'id': "container"})
    songs = container.find_all('div', {'class': 'songs-list-item'})

    for song in songs[1:]:
        title = song.find('div', {'class', 'song-name'}).text.strip()
        artist = song.find('div', {'class': 'song-artist'}).text.strip()
        url = song.find('span', {'class': 'song-download'})
        all_songs.append((artist, title, url['data-url']))
    return all_songs


def download_song(song_url, filename):
    urllib3.disable_warnings(category=InsecureRequestWarning)
    data = requests.get('https://z1.fm'+song_url, headers=headers, verify=False, stream=True)
    with open(download_dir+filename.replace('/', '|')+'.part', 'wb') as file:
        file.write(data.content)
    os.rename(f'{download_dir}{filename}.part', f'{download_dir}{filename}.mp3')


songs = get_songs(url_)
count = 1

for song in songs:
    url = song[2]
    artist = song[0]
    title = song[1]
    print(f'Скачивается:{str(count)} из {str(len(songs))} {artist} - {title}')
    if not(os.path.exists(f'{download_dir}{artist} - {title}.mp3')):
        download_song(url, f'{artist} - {title}')
    else:
        pass
    count += 1
