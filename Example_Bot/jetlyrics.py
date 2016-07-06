import requests
import html

src_url = 'http://lyrics.jetmute.com/search.php?q='
s_url = 'http://lyrics.jetmute.com/viewlyrics.php?id='
attr = "\nLyrics Provided by lyrics.jetmute.com"

def get_lyric(song, artist = ''):
	query = song + ' ' + artist
	query = '+'.join(query.strip().split())
	query_url = src_url + query
	try:
		search_result = requests.get(query_url)
		song_id = parse_id(search_result.text)
		if(song_id == 'error'):
			return 'Error'
		song_url = s_url + song_id
		song_page = requests.get(song_url)
	except requests.exceptions.ConnectionError:
		return 'Error'
	lyric = parse_lyric(song_page.text)
	if lyric == 'Error':
		return lyric
	return html.unescape(lyric) + attr


def parse_id(text):
	start = text.find('<a href=\'' + s_url) + len('<a href=\'' + s_url)
	end = start + 10
	if(start < len('<a href=\'' + s_url)):
		return 'error'
	l_id = ''.join(x for x in text[start:end] if x.isdigit())
	return l_id
def parse_lyric(text):
	start = text.find('<div id=lyricsText>') + len('<div id=lyricsText>')
	if(start < len('<div id=lyricsText>')):
		return 'Error'
	end = start + text[start:].find('<noscript>')
	lyric = text[start:end].replace('<br />\r<br>', '\n').replace('<br/>','\n').replace('<br />','\n').replace('<br>','\n')
	return lyric
