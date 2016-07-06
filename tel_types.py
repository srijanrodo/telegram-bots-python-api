import json
import requests

msg_types = ['text', 'audio', 'video', 'contact', 'location', 'photo', 'sticker', 'voice', 'venue']

def opt_args(obj, arg, default = None, ret_type = None):
	if arg in obj:
		if ret_type is not None:
			return ret_type(obj[arg])
		return obj[arg]
	return default

class User:
	def __init__(self, user_dict):
		self.id = user_dict['id']
		self.first_name = user_dict['first_name']
		self.last_name = opt_args(user_dict, 'last_name', default = '')
		self.username = opt_args(user_dict, 'username', default = '')

class Chat:
	def __init__(self, chat):
		self.id = chat['id']
		self.type = chat['type']
		self.title = opt_args(chat, 'title', default = '')
		self.first_name = opt_args(chat, 'first_name', default = '')
		self.last_name = opt_args(chat, 'last_name', default = '')
		self.username = opt_args(chat, 'username', default = '')

class Message:
	def __init__(self, msg_dict):
		self.message_id = msg_dict['message_id']
		self.sender = self.from_ = opt_args(msg_dict, 'from', default = None, ret_type = User)
		self.chat = Chat(msg_dict['chat'])

		self.date = msg_dict['date']
		self.msg_type = 'other'

		for x in msg_types:
			if x in msg_dict:
				self.msg_type = x
				break
		self.forward_from = opt_args(msg_dict, 'forward_from', ret_type = User)
		self.forward_from_chat = opt_args(msg_dict, 'forward_from_chat', ret_type = Chat)
		self.forward_date = opt_args(msg_dict, 'forward_date')
		self.reply_to_message = opt_args(msg_dict, 'reply_to_message', ret_type = Message)
		self.text = opt_args(msg_dict, 'text')
		self.entities = map(MessageEntity, opt_args(msg_dict, 'entities', default = []))
		self.video = opt_args(msg_dict, 'video', ret_type = Video)
		self.audio = opt_args(msg_dict, 'audio', ret_type = Audio)
		self.photo = map(PhotoSize, opt_args(msg_dict, 'photo', default = []))
		self.document = opt_args(msg_dict, 'document', ret_type = Document)
		self.sticker = opt_args(msg_dict, 'sticker', ret_type = Sticker)
		self.voice = opt_args(msg_dict, 'voice', ret_type = Voice)
		self.caption = opt_args(msg_dict, 'caption', default = '')
		self.location = opt_args(msg_dict, 'location ', ret_type = Location)
		self.venue = opt_args(msg_dict, 'venue', ret_type = Venue)
		self.contact = opt_args(msg_dict, 'contact', ret_type = Contact)
		self.new_chat_member = opt_args(msg_dict, 'new_chat_member', ret_type = User)
		self.left_chat_member = opt_args(msg_dict, 'left_chat_member', ret_type = User)
		self.new_chat_title = opt_args(msg_dict, 'new_chat_title')
		self.new_chat_photo = map(PhotoSize, opt_args(msg_dict, 'new_chat_photo', default = []))
		self.delete_chat_photo = opt_args(msg_dict, 'delete_chat_photo', default = False)
		self.group_chat_created = opt_args(msg_dict, 'group_chat_created', default = False)
		self.supergroup_chat_created = opt_args(msg_dict, 'supergroup_chat_created', default = False)
		self.channel_chat_created = opt_args(msg_dict, 'channel_chat_created', default = False)
		self.migrate_to_chat_id = opt_args(msg_dict, 'migrate_to_chat_id')
		self.migrate_from_chat_id = opt_args(msg_dict, 'migrate_from_chat_id')
		self.pinned_message = opt_args(msg_dict, 'pinned_message', ret_type= Message)

class MessageEntity:
	def __init__(self, msgen):
		self.type = msgen['type']
		self.offset = msgen['offset']
		self.length = msgen['length']
		self.url = opt_args(msgen, 'url')
class Update():
	def __init__(self, update_dict):
		self.update_id = update_dict['update_id']
		self.message = opt_args(update_dict, 'message', ret_type = Message)
		self.edited_message = opt_args(update_dict, 'edited_message', ret_type = Message)
		self.inline_query = opt_args(update_dict, 'inline_query')
		self.chosen_inline_result = opt_args(update_dict, 'chosen_inline_result')
		self.callback_query = opt_args(update_dict, 'callback_query')


class InputFile:
	def __init__(self, file_path, file_name = None,is_it_reload = False, is_it_url = False):
		self.file_id = None
		self.file_o = None
		if is_it_reload is True:
			self.file_id = file_name
		else:
			if is_it_url is True:
				if file_name is None:
					file_name = file_path.split('/')[-1]
				tmp = requests.get(file_path)
				if tmp.status_code == 200:
					f = open(file_name,'wb')
					f.write(tmp.content)
					f.close()
					file_path = file_name
			try:
				self.file_o = open(file_path, 'rb')
			except FileNotFoundError:
				self.file_o = None
		self.file_name = file_name

	def add_file_id(self, file_id):
		self.file_id = file_id

class PhotoSize:
	def __init__(self, photo):
		self.file_id = photo['file_id']
		self.width = photo['width']
		self.height = photo['height']
		self.file_size = opt_args(photo,'file_size')

class Audio:
	def __init__(self, audio):
		self.file_id = audio['file_id']
		self.duration = audio['duration']
		self.performer = opt_args(audio, 'performer')
		self.title = opt_args(audio, 'title')
		self.mime_type = opt_args(audio, 'mime_type')
		self.file_size = opt_args(audio,'file_size')

class Document:
	def __init__(self, document):
		self.file_id = document['file_id']
		self.thumb = opt_args(document, 'thumb', ret_type = PhotoSize)
		self.mime_type = opt_args(document, 'mime_type')
		self.file_size = opt_args(document,'file_size')
		self.file_name = opt_args(document,'file_name')
class Voice:
	def __init__(self, voice):
		self.file_id = voice['file_id']
		self.duration = voice['duration']
		self.mime_type = opt_args(voice, 'mime_type')
		self.file_size = opt_args(voice,'file_size')
class Sticker:
	def __init__(self, sticker):
		self.file_id = sticker['file_id']
		self.width = sticker['width']
		self.height = sticker['height']
		self.thumb = opt_args(sticker, 'thumb', ret_type = PhotoSize)
		self.file_size = opt_args(sticker,'file_size')
		self.emoji = opt_args(sticker, 'emoji')

class Video:
	def __init__(self, video):
		self.file_id = video['file_id']
		self.width = video['width']
		self.height = video['height']
		self.duration = video['duration']
		self.thumb = opt_args(video, 'thumb', ret_type = PhotoSize)
		self.mime_type = opt_args(video,'mime_type')
		self.file_size = opt_args(video,'file_size')

class Contact:
	def __init__(self, contact):
		self.phone_number = contact['phone_number']
		self.first_name = contact['first_name']
		self.last_name = opt_args(contact, 'last_name')
		self.user_id = opt_args(contact,'user_id')

class Location:
	def __init__(self, location):
		self.latitude = location['latitude']
		self.longitude = location['longitude']

class Venue:
	def __init__(self, ven):
		self.location = Location(ven['location'])
		self.title = ven['title']
		self.address = ven['address']
		self.foursquare_id = opt_args(ven, 'foursquare_id')
class UserProfilePhotos:
	def __init__(self, upp_dict):
		self.total_count = upp_dict['total_count']
		self.photos = [[PhotoSize(y) for y in x] for x in upp_dict['photos']]


class File:
	def __init__(self, f):
		self.file_id = f['file_id']
		self.file_size = opt_args(f, 'file_size')
		self.file_path = opt_args(f, 'file_path')
	def getURL(self, token):
		if self.file_path == None:
			return ''
		return 'https://api.telegram.org/file/bot' + token + '/' + self.file_path

class ReplyMarksUps:
	def __init__(self, selective = False):
		self.data = {'selective' : selective}
	def stringify(self):
		self.json_str = json.dumps(self.data)

class ReplyKeyboardMarkup(ReplyMarksUps):
	def __init__(self, keyboard, resize_keyboard = False, one_time_keyboard = False,\
	selective = False):
		super().__init__(selective)
		self.data['keyboard'] = [[y.data for y in x] for x in keyboard]
		self.data['resize_keyboard'] = resize_keyboard
		self.data['one_time_keyboard'] = one_time_keyboard
		self.stringify()

class KeyboardButton:
	def __init__(self, text, request_location = False, request_contact = False):
		self.data = {'text':text}
		self.data['request_contact'] = request_contact
		self.data['request_location'] = request_location

class ReplyKeyboardHide(ReplyMarksUps):
	def __init__(self, hide_keyboard, selective = False):
		super().__init__(selective)
		self.data['hide_keyboard'] = hide_keyboard
		self.stringify()

class ForceReply(ReplyMarksUps):
	def __init__(self, force_reply, selective = False):
		super().__init__(selective)
		self.data['force_reply'] = force_reply
		self.stringify()
