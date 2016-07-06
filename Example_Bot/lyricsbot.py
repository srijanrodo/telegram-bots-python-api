#!/usr/bin/env python3
module_path = '/home/srijan/Code/Python/Telegram'
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

token = '71807785:AAEtvC5XDafHS6UJ-fDc8wsmqdbfJAREpSA'
control_id = 37937434
cache_folder = './lyrics_cache/'
spl_cmd = {'/azlyrics':azlyrics, '/jetlyrics':jetlyrics, '/songmeanings':songmeanings}
confile = 'lyricsbot.conf'
timeout = 20
tel = telegram.TelegramEventLoop(token, confile = confile)
tel.setDefaultTimeout(timeout)

def sendLyrics(cmd, msg):
	text = msg.text[len(cmd):]
	cmd = cmd.split('@')[0]
	print("Searching for " + text)
	if text.strip() == '':
		lyric = "Error"
	elif cmd.startswith('/lyrics'):
		file_path = cache_folder + '_'.join(text.split()).lower()
		infile = False
		tel.sendChatAction(msg.chat.id, 'typing')
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
	if tel.sendLargeMessage(chat_id = msg.chat.id, text = lyric) == None:
		print(tel.last_error)
		print('Message not sent')
		return False
	print('Sent')
	return True

def intro(cmd, msg):
	intro = "Hello " + msg.sender.first_name +" Welcome to the Lyrics Bot\n\
Type /lyrics <song-name> to get Lyrics"
	if tel.sendMessage(chat_id = msg.chat.id, text = intro) == None:
			print(tel.last_error)

def goodbye(cmd, msg):
	bye = "Good Bye"
	if tel.sendMessage(chat_id = msg.chat.id, text = bye) == None:
			print(tel.last_error)

def doExit(cmd, msg):
	if msg.chat.id == control_id:
		tel.doExit()
def reImport(cmd, msg):
	if msg.chat.id == control_id:
		for x in import_list:
			print('Reloading :' + str(x))
			try:
				imp.reload(x)
			except Exception:
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
	tmp = []
	for x in tel.handlers:
		for y in tel.handlers[x]:
			tmp.append((x + '@srijan_lyric_bot', y))
	for (u,v) in tmp:
		tel.addHandler(u,v)
	return tel.mainLoop()
if __name__ == '__main__':
	main()
