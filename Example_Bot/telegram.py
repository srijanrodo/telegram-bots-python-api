import requests
from tel_types import User, Message, Update, UserProfilePhotos
import time

base_url = 'https://api.telegram.org/bot'


class Telegram:
	def __init__(self, token):
		self.call_url = base_url + token + '/'
		self.token = token
		self.me = self.getMe()
		self.text_limit = 4096
		self.last_error = ''
	
	def __method_create__(self, method_name, files = None, data = None):
		url = self.call_url + method_name
		if files is not None:
			return requests.post(url, files = files, data = data)
		else :
			return requests.post(url, data = data)
	def __method_create_json__(self, method_name, files = None, data = None):
		try:
			tmp = self.__method_create__(method_name, files = files, data = data).json()
		except ValueError:
			self.last_error = "Error: Most Probably Network Issue"
			return None
		return tmp
	def getMe(self):
		tmp = self.__method_create_json__('getMe')
		
		if tmp is None:
			return None

		if tmp['ok'] is False:
			self.last_error = tmp['description']
			return None
		
		return User(tmp['result'])

	def getUpdates(self, offset = None, limit = 100, timeout = 0):

		data = {
			'offset':offset,
			'limit':limit,
			'timeout':timeout
		}
		
		tmp = self.__method_create_json__('getUpdates', data = data)
		
		if tmp is None:
			return None
		
		if tmp['ok'] is False:
			self.last_error = tmp['description']
			return None
			
		return [Update(x) for x in tmp['result']]
		
	def sendMessage(self, chat_id, text, disable_web_page_preview = False, \
		reply_to_message_id = None, reply_markup = None):
		data = {
			'chat_id':chat_id,
			'text':text,
			'disable_web_page_preview' : disable_web_page_preview,
			'reply_to_message_id' :reply_to_message_id,
			'reply_markup': None if reply_markup is None else reply_markup.json_str
		}

		tmp = self.__method_create_json__('sendMessage', data = data)
		if tmp is None:
			return None
		if tmp['ok'] is False:
			self.last_error = tmp['description']
			return None
		return Message(tmp['result'])
	def sendLargeMessage(self, chat_id, text, disable_web_page_preview = False, \
		reply_to_message_id = None, reply_markup = None):
		
		while len(text) > self.text_limit:
			send = self.split(text)
			text = text[len(send):]
			if self.sendMessage(chat_id, send, disable_web_page_preview = disable_web_page_preview, \
		reply_to_message_id = reply_to_message_id, reply_markup = reply_markup) is None:
				return None
		
		return self.sendMessage(chat_id, text, disable_web_page_preview = disable_web_page_preview, \
		reply_to_message_id = reply_to_message_id, reply_markup = reply_markup)

	def forwardMessage(self, chat_id, from_chat_id, message_id):
		data = {
			'chat_id' : chat_id,
			'from_chat_id' : from_chat_id,
			'message_id' : message_id
		}

		tmp = self.__method_create_json__('forwardMessage', data = data)

		if tmp is None:
			return None

		if tmp['ok'] is False:
			self.last_error = tmp['description']
			return None
		return Message(tmp['result'])

	def sendFiles(self, chat_id, input_file, file_type, caption = None, \
		reply_to_message_id = None, reply_markup = None):
		if input_file.file_id is input_file.file_o is None:
			self.last_error = 'Error: No File Specified'
			return None
		
		data = {
			'chat_id':chat_id,
			'reply_to_message_id' : reply_to_message_id,
			'reply_markup' : None if reply_markup is None else reply_markup.json_str
		}
		if caption is not None:
			data['caption'] = caption

		if input_file.file_id is not None:
			files = {file_type:(None, input_file.file_id)}
		else :
			files = {file_type: input_file.file_o}
		method_name = 'send' + file_type.title()
		
		tmp = self.__method_create_json__(method_name, data = data)

		if tmp is None:
			return None

		if tmp['ok'] is False:
			self.last_error = tmp['description']
			return None
		return Message(tmp['result'])

	def sendPhoto(self, chat_id, photo, caption = None, \
		reply_to_message_id = None, reply_markup = None):
		return self.sendFiles(chat_id, photo, 'photo', caption = caption, \
		reply_to_message_id = reply_to_message_id, reply_markup = reply_markup)

	def sendVideo(self, chat_id, photo, reply_to_message_id = None, reply_markup = None):
		return self.sendFiles(chat_id, photo, 'video', \
			reply_to_message_id = reply_to_message_id, reply_markup = reply_markup)

	def sendAudio(self, chat_id, photo, reply_to_message_id = None, reply_markup = None):
		return self.sendFiles(chat_id, photo, 'audio', \
			reply_to_message_id = reply_to_message_id, reply_markup = reply_markup)

	def sendDocument(self, chat_id, photo, reply_to_message_id = None, reply_markup = None):
		return self.sendFiles(chat_id, photo, 'document',\
			reply_to_message_id = reply_to_message_id, reply_markup = reply_markup)

	def sendSticker(self, chat_id, photo, reply_to_message_id = None, reply_markup = None):
		return self.sendFiles(chat_id, photo, 'sticker',\
			reply_to_message_id = reply_to_message_id, reply_markup = reply_markup)
	
	def sendLocation(self, chat_id, latitude, longitude, reply_to_message_id = None, \
		reply_markup = None):
		data = {
			'chat_id': chat_id,
			'latitude' : latitude,
			'longitude' : longitude,
			'reply_to_message_id' : reply_to_message_id,
			'reply_markup' : None if reply_markup is None else reply_markup.json_str
		}

		tmp = self.__method_create_json__('sendLocation', data = data)
		if tmp is None:
			return None
		if tmp['ok'] is False:
			self.last_error = tmp['description']
			return None
		return Message(tmp['result'])

	def sendChatAction(self, chat_id, action):
		data = {
			'chat_id' : chat_id,
			'action' : action
		}
		
		tmp = self.__method_create_json__('sendChatAction', data = data)
		if tmp is None:
			return None
		if tmp['ok'] is False:
			self.last_error = tmp['description']
			return None
		return tmp['result']

	def getUserProfilePhotos(self, user_id, offset = 0, limit = 100):
		data = {
			'user_id' : user_id,
			'offset' : offset,
			'limit' : limit
		}
		
		tmp = self.__method_create__('getUserProfilePhotos', data = data)
		if tmp is None:
			return None
		if tmp['ok'] is False:
			self.last_error = tmp['description']
			return None
		return UserProfilePhotos(tmp['result'])
	def split(self, text):
		prev = ''
		new = ''
		for x in text.splitlines():
			prev = new
			new = new + '\n' + x
			if len(new) > self.text_limit:
				break
		return prev

class TelegramEventLoop(Telegram):
	def __init__(self, token, confile = 'telegram.conf', control_id = None):
		super().__init__(token)
		self.handlers = {}
		self.exit = False
		self.nonText = None
		self.control_id = control_id
		self.confile = confile
	def addHandler(self, start_cmd, *funcs):
		start_cmd = start_cmd.strip()
		if start_cmd not in self.handlers:
			self.handlers[start_cmd] = []
		for x in funcs :
			self.handlers[start_cmd].append(x)
		return start_cmd
	def mainLoop(self):
		try:
			f = open(self.confile, 'r')
			last_update = int(f.read())
			f.close()
		except FileNotFoundError:
			last_update = 0
		
		while self.exit is False:
			update  = self.getUpdates(offset = last_update + 1)
			for x in update:
				last_update = max(last_update, x.update_id)
				if x.msg_type == 'text':
					cmd = x.text.split()[0]
					if cmd in self.handlers:
						for func in self.handlers[cmd]:
							func(cmd, x)
				else :
					self.handleNonText(x)
			if update != []:
				f = open(self.confile, 'w')
				f.write(str(last_update))
				f.close()
		print('Exiting')
		return
	def setNonTextHandler(self, func):
		self.nonText = func
	def handleNonText(self, x):
		print("Non-Text Message Arrived\n" + x.msg_type + "\nCalling default Handler")
		if self.nonText is not None:
			return self.nonText(x)
		return
	def doExit(self, cmd, msg):
		if self.control_id is None:
			self.exit = True
		elif msg.chat_id == self.control_id:
			self.exit = True