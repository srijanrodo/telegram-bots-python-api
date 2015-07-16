import requests
import html

src_url = 'http://search.azlyrics.com/search.php?w=songs&q='
s_url = 'http://www.azlyrics.com/lyrics/'
srch = '<!-- Usage of azlyrics.com content by any third-party lyrics provider\
 is prohibited by our licensing agreement. Sorry about that. -->'
attr = "\nLyrics Provided by AZlyrics.com"
srch_len = len(srch)

def get_lyric(song, artist = ''):
	query = song + ' ' + artist
	query = '+'.join(query.split())
	query_url = src_url + query
	search_result = requests.get(query_url)
	song_url = parse_id(search_result.text)
	if(song_url == 'error'):
		return 'Error'
	#print(song_id)
	song_page = requests.get(song_url)
	lyric = parse_lyric(song_page.text)
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
	end = start + text[start:].find('</div>')
	lyric = text[start:end].replace('<br/>','').replace('<br>','').replace('<i>','').replace('</i>','')
	song = text.split("SongName = ")[1].split(';')[0][1:-1] + '\n'*2
	artist = text.split("ArtistName = ")[1].split(';')[0][1:-1].title() + '\n'

	return song + artist + lyric