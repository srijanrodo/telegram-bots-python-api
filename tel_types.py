import json

msg_types = ['text', 'audio', 'video', 'contact', 'location']

def opt_args(obj, arg, default = None, ret_type = None):
	if arg in obj:
		if ret_type is not None:
			return ret_type(obj[arg])
		return obj[arg]
	return default

class User:
	def __init__(self, user_dict):
		self.id = user_dict['id']
		self.firstname = user_dict['first_name']
		self.username = user_dict['username']

class GroupChat:
	def __init__(self, grp):
		self.id = grp['id']
		self.title = grp['title']

class Message:
	def __init__(self, msg_dict):
		self.message_id = msg_dict['message_id']
		self.sender = self.from_ = User(msg_dict['from'])
		self.chat_id = msg_dict['chat']['id']
		
		if 'title' in msg_dict['chat']:
			self.chat = GroupChat(msg_dict['chat'])
		else:
			self.chat = User(msg_dict['chat'])
		
		self.date = msg_dict['date']
		self.msg_type = 'other'

		for x in msg_types:
			if x in msg_dict:
				self.msg_type = x
				break
		self.forward_from = opt_args(msg_dict, 'forward_from', ret_type = User)
		self.forward_date = opt_args(msg_dict, 'forward_date')
		self.reply_to_message = opt_args(msg_dict, 'reply_to_message', ret_type = Message)
		self.text = opt_args(msg_dict, 'text')
		self.video = opt_args(msg_dict, 'video', ret_type = Video)
		self.audio = opt_args(msg_dict, 'audio', ret_type = Audio)
		self.photo = [PhotoSize(x) for x in opt_args(msg_dict, 'photo', default = [])]
		self.document = opt_args(msg_dict, 'document', ret_type = Document)
		self.sticker = opt_args(msg_dict, 'sticker', ret_type = Sticker)
		self.location = opt_args(msg_dict, 'location ', ret_type = Location)
		self.contact = opt_args(msg_dict, 'contact', ret_type = Contact)
		self.new_chat_participant = opt_args(msg_dict, 'new_chat_participant', ret_type = User)
		self.left_chat_participant = opt_args(msg_dict, 'left_chat_participant', ret_type = User)
		self.new_chat_title = opt_args(msg_dict, 'new_chat_title')
		self.new_chat_photo = [PhotoSize(x) for x in opt_args(msg_dict, 'new_chat_photo', default = [])]
		self.delete_chat_photo = opt_args(msg_dict, 'delete_chat_photo', default = False)
		self.group_chat_photo = opt_args(msg_dict, 'group_chat_photo', default = False)

class Update(Message):
	def __init__(self, update_dict):
		super().__init__(update_dict['message'])
		self.update_id = update_dict['update_id']
		

class InputFile:
	def __init__(self, file_path, file_name = None,is_it_reload = False):
		if is_it_reload is True:
			self.file_id = file_n
		else :
			try:
				self.file_o = open(file_path, 'rb')
			except FileNotFoundError:
				self.file_o = None
			self.file_id = None
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
		self.mime_type = opt_args(audio, 'mime_type')
		self.file_size = opt_args(audio,'file_size')

class Document:
	def __init__(self, document):
		self.file_id = document['file_id']
		self.thumb = PhotoSize(document['thumb'])
		self.mime_type = opt_args(document, 'mime_type')
		self.file_size = opt_args(document,'file_size')
		self.file_name = opt_args(document,'file_name')

class Sticker:
	def __init__(self, sticker):
		self.file_id = sticker['file_id']
		self.width = sticker['width']
		self.height = sticker['height']
		self.thumb = PhotoSize(sticker['thumb'])
		self.file_size = opt_args(sticker,'file_size')

class Video:
	def __init__(self, video):
		self.file_id = video['file_id']
		self.width = video['width']
		self.height = video['height']
		self.duration = video['duration']
		self.thumb = PhotoSize(video['thumb'])
		self.mime_type = opt_args(video,'mime_type')
		self.file_size = opt_args(video,'file_size')
		self.caption = opt_args(video,'caption')

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

class UserProfilePhotos:
	def __init__(self, upp_dict):
		self.total_count = upp_dict['total_count']
		self.photos = [[PhotoSize(y) for y in x] for x in upp_dict['photos']]

class ReplyMarksUps:
	def __init__(self, selective = False):
		self.data = {'selective' : selective}
	def stringify(self):
		self.json_str = json.dumps(self.data)

class ReplyKeyboardMarkup(ReplyMarksUps):
	def __init__(self, keyboard, resize_keyboard = False, one_time_keyboard = False,\
	selective = False):
		super().__init__(selective)
		self.data['keyboard'] = keyboard
		self.data['resize_keyboard'] = resize_keyboard
		self.data['one_time_keyboard'] = one_time_keyboard
		self.stringify()

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