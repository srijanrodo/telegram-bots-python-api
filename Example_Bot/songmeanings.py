import requests
import html

src_url = 'http://songmeanings.com/query/?query={0}&type=songtitles'
s_url = 'http://songmeanings.com/songs/view/'
srch = '<div class="holder lyric-box">'
attr = "\n\nLyrics Provided by songmeanings.com"
srch_len = len(srch)
no_avail = 'Due to a publisher block, we are not authorized to display these lyrics.'

def get_lyric(song, artist = ''):
	query = song + ' ' + artist
	query = '%20'.join(query.split())
	query_url = src_url.format(query)
	search_result = requests.get(query_url)
	song_url = parse_id(search_result.text)
	if(song_url == 'error'):
		return 'Error'
	song_page = requests.get(song_url)
	lyric = parse_lyric(song_page.text)
	if lyric == 'Error':
		return lyric
	return html.unescape(lyric) + attr


def parse_id(text):
	start = text.find(s_url)
	end = start + text[start:].find('"')
	if(start < 0):
		return 'error'
	return text[start:end]
def parse_lyric(text):
	start = text.find(srch) + srch_len
	if(start < srch_len):
		return 'Error'
	end = start + text[start:].find('<div')
	lyric = text[start:end].replace('<br/>','').replace('<br>','').replace('<i>','').replace('</i>','')
	if no_avail in lyric:
		return 'Error'
	song_artist = text.split("<title>")[1].split('|')[0] + '\n'*2

	return song_artist + lyric.strip()