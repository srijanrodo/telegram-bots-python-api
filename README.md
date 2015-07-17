# telegram-bots-python-api
An Interface to the Telegram Bots API in Python 3 using requests library

The API is contained in two files.

# telegram.py
This file contains the Telegram class which provides the methods to access the telegram bots api.
Each method mentioned in https://core.telegram.org/bots/api is provided with the exception of setWebHooks.
An extra method, sendLargeMessage is provided which sends longer than the limit imposed by the bot api (4096 characters). A longer message is broken into multiple messages by this method.
Note: This method breaks the message by lines. So a long message with no linebreaks won't work.

Another class provided here is TelegramEventLoop class which provides a getUpdates based loop and calls functions on receival of particular texts. On non-text messages an external handler may be associated.

Handlers are added with the method: 
addHandler(cmd, func1, func2, ...)
Here cmd is the command (the text a message starts with) that will trigger the functions. Multiple functions may be provided. The functions will be called with two argument. The first one being the triggering command and the second one being a Message object that contained the command.
The loop is broken on calling the doExit method.
The non-text handler is added with setNonTextHandler(func) method where func is the one to be called upon receiving a non-text message. func will be called with the Message object as the single argument.

# tel_types.py
This file contains the data types mentioned in https://core.telegram.org/bots/api .
The received data types contain a dictionary as their sole initialising argument. Most of the data types just convert the values in the dictionary to member variables of the object.
The Message object contains an extra field chat_id (the same as Message.chat.id) for easy access.
Also the form field in the Message object is renamed to from_ (since from is reserved in python). The same object is also represented by the sender field.
The outgoing data types contain the usual initialisation arguments as mentioned in https://core.telegram.org/bots/api . The outgoing type InputFile is used to upload all files. The file_path argument is to be set to the path to the file being uploaded or the file_id of uploaded files. The file_id (for pre-uploaded files) is also represented by InputFile with the is_it_reload argument set as True. For sending file from a url, set the url to the file_path and set is_it_url to True. InputFile contains another optional argument file_name to set the name of the file being uploaded.

# Example_Bot
This folder contains an example bot written using this api. This bot fetches lyrics from AZlyrics.com and lyrics.jetmute.com and presents them to the user. The bot is accessed from http://telegram.me/srijan_lyric_bot .
