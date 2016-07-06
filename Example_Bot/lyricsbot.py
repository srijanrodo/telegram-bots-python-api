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
import tel_types as tt

import_list = [jetlyrics, azlyrics, songmeanings, os, telegram]
site_list = [songmeanings,azlyrics, jetlyrics]

token = '<token>'
bot_name = 'srijan_lyric_bot'
control_id = 37937434
cache_folder = './lyrics_cache/'
spl_cmd = {'/azlyrics':azlyrics, '/jetlyrics':jetlyrics, '/songmeanings':songmeanings}
confile = 'lyricsbot.conf'
timeout = 20
tel = telegram.TelegramEventLoop(token, confile = confile)
tel.setDefaultTimeout(timeout)
pending = {}

def lyricsGetter(cmd, text):
	print("Searching for " + text)
	file_path = cache_folder + '_'.join(text.split()).lower()
	infile = False
	infile = os.path.isfile(file_path)
	if infile and cmd == '/lyrics':
		f = open(file_path, 'r')
		lyric = f.read()
		f.close()
	elif cmd in spl_cmd:
		lyric = spl_cmd[cmd].get_lyric(text)
	else:
		for x in site_list:
			lyric = x.get_lyric(text)
			if lyric == 'Error':
				continue
			else:
				f = open(file_path, 'w')
				f.write(lyric)
				f.close()
				break
	return lyric

def replyBack(cmd, msg):
	mid = msg.message_id
	cid = msg.chat.id
	m = tel.sendMessage(chat_id = cid, text = 'Reply to this message with the query', \
		reply_to_message_id = mid, reply_markup = tt.ForceReply(True, selective = True)) 

	if m == None:
		print(tel.last_error)
		print('Message not sent')
		return False

	key = m.message_id
	pending[key] = cmd

	return True


def sendLyrics(cmd, msg):
	text = msg.text[len(cmd):]
	cmd = cmd.split('@')[0]
	if text.strip() == '':
		return replyBack(cmd, msg)
	tel.sendChatAction(msg.chat.id, 'typing')
	lyric = lyricsGetter(cmd, text)
	print('Sending')
	if tel.sendLargeMessage(chat_id = msg.chat.id, text = lyric) == None:
		print(tel.last_error)
		print('Message not sent')
		return False
	print('Sent')
	return True

def isReplyLyrics(upd):
	msg = upd.message
	if msg == None:
		return False
	if msg.reply_to_message == None:
		return False
	if msg.reply_to_message.message_id not in pending:
		return False
	return True

def replyLyrics(upd):
	msg = upd.message
	text = msg.text
	tel.sendChatAction(msg.chat.id, 'typing')
	lyric = lyricsGetter(pending.pop(msg.reply_to_message.message_id), text)
	print('Sending')
	if tel.sendLargeMessage(chat_id = msg.chat.id, text = lyric) == None:
		print(tel.last_error)
		print('Message not sent')
		return False
	print('Sent')
	return True

def intro(cmd, msg):
	intro = "Hello " + msg.sender.first_name +"\n Welcome to the Lyrics Bot\n\
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

def textChecker(txt):
	def check(msg):
		if msg.message == None:
			return False
		if msg.message.msg_type == 'text':
			cmd = msg.message.text.split()[0]
			if cmd == txt:
				return True
		return False
	return check

def funcDoer(func):
	def proxyFunc(msg):
		cmd = msg.message.text.split()[0]
		return func(cmd, msg.message)
	return proxyFunc

def adder(x, f):
	tel.addHandler(textChecker(x), f)
	tel.addHandler(textChecker(x + '@' + bot_name), f)

def main():
	adder('/lyrics', funcDoer(sendLyrics))
	adder('/lyrics_refresh', funcDoer(sendLyrics))
	for x in spl_cmd:
		adder(x,funcDoer(sendLyrics))
	adder('/start', funcDoer(intro))
	adder('/exit', funcDoer(doExit))
	adder('/stop', funcDoer(goodbye))
	adder('/reload', funcDoer(reImport))
	tel.addHandler(isReplyLyrics, replyLyrics)
	return tel.mainLoop()

if __name__ == '__main__':
	main()
