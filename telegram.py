import requests
from tel_types import User, Message, Update, UserProfilePhotos
import time

base_url = 'https://api.telegram.org/bot'


class Telegram:
	def __init__(self, token):
		self.call_url = base_url + token + '/'
		self.token = token
		self.req_timeout = 5
		self.text_limit = 4096
		self.last_error = ''
		self.me = self.getMe()

	def __method_create__(self, method_name, files = None, data = None):
		url = self.call_url + method_name
		try:
			if files is not None:
				ret = requests.post(url, files = files, data = data, timeout = self.req_timeout)
			else :
				ret = requests.post(url, data = data, timeout = self.req_timeout)
		except requests.exceptions.ConnectionError:
			self.last_error = 'Error: Network Issue'
			ret = None
		except requests.exceptions.Timeout:
			self.last_error = 'Error: Timeout Occured'
			ret = None
		except Exception:
			self.last_error = 'Unknown Error'
			ret = None
		return ret
	def __method_create_json__(self, method_name, files = None, data = None):
		tmp = self.__method_create__(method_name, files = files, data = data)
		if tmp == None:
			ret = None
		else:
			try:
				ret = tmp.json()
			except ValueError:
				self.last_error = "Error: Request Failed (JSON object not returned)"
				ret = None
		return ret
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

	def sendMessage(self, *args, **data):
		if data == {}:
			if len(args) != 1 or type(args[0]) != dict:
				return None
			data = args[0]
		if 'reply_markup' in data:
			data['reply_markup'] = data['reply_markup'].json_str
		tmp = self.__method_create_json__('sendMessage', data = data)
		if tmp is None:
			return None
		if tmp['ok'] is False:
			self.last_error = tmp['description']
			return None
		return Message(tmp['result'])
	def sendLargeMessage(self, **data):
		if 'text' not in data:
			return None
		text = data['text']
		while len(text) > self.text_limit:
			send = self.split(text)
			text = text[len(send):]
			data['text'] = send
			if self.sendMessage(data) is None:
				return None
		data['text'] = text
		return self.sendMessage(data)

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

		tmp = self.__method_create_json__(method_name, data = data, files = files)

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
	def setDefaultTimeout(self, timeout):
		self.req_timeout = timeout

class TelegramEventLoop(Telegram):
	def __init__(self, token, confile = 'telegram.conf'):
		super().__init__(token)
		self.handlers = []
		self.exit = False
		self.nonText = None
		self.confile = confile
	def addHandler(self, check_msg, *funcs):
		for x in funcs:
			self.handlers.append((check_msg, x))
		return check_msg
	def mainLoop(self):
		try:
			f = open(self.confile, 'r')
			last_update = int(f.read())
			f.close()
		except FileNotFoundError:
			last_update = 0
		if self.checkNetworkConnection() is False:
			print('No Connection')
			self.waitForNetworkConnection()
			print('Connection Back')
		while self.exit is False:
			update = self.getUpdates(offset = last_update + 1)
			if update == None:
				update = []
				print(self.last_error)
				if self.checkNetworkConnection() is False:
					print('No Connection')
					self.waitForNetworkConnection()
					print('Connection Back')
			elif update != []:
				last_update = update[0].update_id
			for x in update:
				last_update = max(last_update, x.update_id)
				for (key,foo) in self.handlers:
					if key(x) == True:
						foo(x)

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
	def doExit(self, *arg):
		self.exit = True
	def checkNetworkConnection(self):
		try:
			requests.get('https://www.example.com')
		except requests.exceptions.ConnectionError:
			return False
		return True
	def waitForNetworkConnection(self):
		while self.checkNetworkConnection() is False:
			time.sleep(1)
