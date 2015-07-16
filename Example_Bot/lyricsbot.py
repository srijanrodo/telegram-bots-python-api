#!/usr/bin/env python3

from telegram import TelegramEventLoop
from jetlyrics import get_lyric
from azlyrics import get_lyric as get_lyric_az
import os

token = <token>
control_id = 37937434

tel = TelegramEventLoop(token, confile = 'lyricsbot.conf', control_id = control_id)
cache_folder = './lyrics_cache/'

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
		lyric = get_lyric_az(text)
		if lyric == 'Error':
			lyric = get_lyric(text)
		if lyric is not 'Error':
			f = open(file_path, 'w')
			f.write(lyric)
			f.close()
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

def main():
	tel.addHandler('/lyrics', sendLyrics)
	tel.addHandler('/start', intro)
	tel.addHandler('/exit', tel.doExit)
	tel.addHandler('/stop', goodbye)
	return tel.mainLoop()
if __name__ == '__main__':
	main()
