#!/usr/bin/env python3
module_path = <path_to_module_folder>
import sys
sys.path.append(module_path)
from telegram import TelegramEventLoop
import jetlyrics
import azlyrics
import songmeanings
import os

site_list = [azlyrics, songmeanings, jetlyrics]

token = <your_access_token>
control_id = <your_acccount_control_id>
cache_folder = './lyrics_cache/'

tel = TelegramEventLoop(token, confile = 'lyricsbot.conf')


def sendLyrics(cmd, msg):
	text = msg.text[len(cmd):]
	file_path = cache_folder + '_'.join(text.split()).lower()
	infile = False
	print("Searching for " + text)
	tel.sendChatAction(msg.chat_id, 'typing')
	infile = os.path.isfile(file_path)
	if infile :
		f = open(file_path, 'r')
		lyric = f.read()
		f.close()
	else :
		for x in site_list:
			lyric = x.get_lyric(text)
			if lyric == 'Error':
				continue
			else:
				f = open(file_path, 'w')
				f.write(lyric)
				f.close()
				break
	print('Sending')
	if tel.sendLargeMessage(msg.chat_id, lyric) == None:
		print(tel.last_error)
	print('Sent')

def intro(cmd, msg):
	intro = "Hello " + msg.sender.firstname +" Welcome to the Lyrics Bot\n\
Type /lyrics <song-name> to get Lyrics"
	if tel.sendMessage(msg.chat_id, intro) == None:
			print(tel.last_error)

def goodbye(cmd, msg):
	bye = "Good Bye"
	if tel.sendMessage(msg.chat_id, bye) == None:
			print(tel.last_error)

def doExit(cmd, msg):
	if msg.chat_id == control_id:
		tel.doExit()
def main():
	tel.addHandler('/lyrics', sendLyrics)
	tel.addHandler('/start', intro)
	tel.addHandler('/exit', doExit)
	tel.addHandler('/stop', goodbye)
	return tel.mainLoop()
if __name__ == '__main__':
	main()
