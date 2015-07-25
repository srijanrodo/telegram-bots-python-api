#!/usr/bin/env python3
module_path = <path-to-module>
import sys
sys.path.append(module_path)
import telegram
import jetlyrics
import azlyrics
import songmeanings
import os
import imp

import_list = [jetlyrics, azlyrics, songmeanings, os, telegram]
site_list = [songmeanings,azlyrics, jetlyrics]

token = <access_token>
control_id = <control_id_for_reload_and_exit>
cache_folder = './lyrics_cache/'
spl_cmd = {'/azlyrics':azlyrics, '/jetlyrics':jetlyrics, '/songmeanings':songmeanings}
confile = 'lyricsbot.conf'
timeout = 20
tel = telegram.TelegramEventLoop(token, confile = confile)
tel.setDefaultTimeout(timeout)

def sendLyrics(cmd, msg):
	text = msg.text[len(cmd):]
	print("Searching for " + text)
	if text.strip() == '':
		lyric = "Error"
	elif cmd.startswith('/lyrics'):
		file_path = cache_folder + '_'.join(text.split()).lower()
		infile = False
		tel.sendChatAction(msg.chat_id, 'typing')
		infile = os.path.isfile(file_path)
		if infile and cmd == '/lyrics':
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
	else:
		lyric = spl_cmd[cmd].get_lyric(text)
	print('Sending')
	if tel.sendLargeMessage(msg.chat_id, lyric) == None:
		print(tel.last_error)
		print('Message not sent')
		return False
	print('Sent')
	return True

def intro(cmd, msg):
	intro = "Hello " + msg.sender.first_name +" Welcome to the Lyrics Bot\n\
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
def reImport(cmd, msg):
	if msg.chat_id == control_id:
		for x in import_list:
			print('Reloading :' + str(x))
			try:
				imp.reload(x)
			except SyntaxError:
				print("Importing faliled :" + str(x))
		tel = telegram.TelegramEventLoop(token, confile = confile)
		tel.setDefaultTimeout(timeout)


def main():
	tel.addHandler('/lyrics', sendLyrics)
	tel.addHandler('/lyrics_refresh', sendLyrics)
	for x in spl_cmd:
		tel.addHandler(x,sendLyrics)
	tel.addHandler('/start', intro)
	tel.addHandler('/exit', doExit)
	tel.addHandler('/stop', goodbye)
	tel.addHandler('/reload', reImport)
	return tel.mainLoop()
if __name__ == '__main__':
	main()
