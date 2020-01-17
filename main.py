"""
	z1.fm downloader.
	Sergey Karbivnichiy 2020
"""
import requests
from bs4 import BeautifulSoup
from lxml import html
from urllib3.exceptions import InsecureRequestWarning
from hurry.filesize import size
import os


version = '0.1.1'

url_ = 'https://z1.fm/new?sort=date'

headers = {	'user-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0',
			'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
			'Referer':'https://z1.fm/'
}

all_songs = []

def get_songs(url):
	responce = requests.get(url)
	soup = BeautifulSoup(responce.text,"html.parser")
	container = soup.find('section',{'id':"container"})
	songs = container.find_all('div',{'class':'songs-list-item'})
	#string = ''
	urls = ''

	for song in songs[1:]:
		title = song.find('div',{'class','song-name'}).text.strip()
		artist = song.find('div',{'class':'song-artist'}).text.strip()
		url = song.find('span',{'class':'song-download'})
		#string += ('{} {} https://z1.fm{}\n'.format(artist,title,url['data-url']))
		all_songs.append((artist,title,url['data-url']))
	return all_songs


def download_song(song_url,filename):
	requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning) 
	data = requests.get('https://z1.fm'+song_url,headers=headers,verify=False,stream=True)
	with open(filename.replace('/','|')+'.part','wb') as file:
		file.write(data.content)
	os.rename(f'{filename}.part',f'{filename}.mp3')


songs = get_songs(url_)

counter = 1

for song in songs:
	#print('Скачивается:'+str(counter)+' из '+str(len(songs))+' '+ song[0]+'-'+song[1])
	print(f'Скачивается:{str(counter)} из {str(len(songs))} {song[0]} - {song[1]}')
	download_song(song[2],song[0]+'-'+song[1])
	counter += 1