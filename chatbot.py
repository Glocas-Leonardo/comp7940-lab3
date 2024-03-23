## this file is based on version 13.7 of python telegram chatbot
## and version 1.26.18 of urllib3
## chatbot.py
from telegram import Update
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
CallbackContext)
import os
# import configparser
import logging
import redis
from ChatGPT_HKBU import HKBU_ChatGPT
from Google_Route import Route

global redis1
def main():
	# Load your token and create an Updater for your Bot
	# config = configparser.ConfigParser()
	# config.read('config.ini')
	# updater = Updater(token=(config['TELEGRAM']['ACCESS_TOKEN']), use_context=True)
	updater = Updater(token=(os.environ['ACCESS_TOKEN']),use_context=True)
	dispatcher = updater.dispatcher
	global redis1
	redis1 = redis.Redis(host=(os.environ['HOST']),
						 password=(os.environ['PASSWORD']),
						 port=(os.environ['REDISPORT']))

	# You can set this logging module,
	# so you will know when and why things do not work as expected
	logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
	level=logging.INFO)
	# register a dispatcher to handle message:here we register an echo dispatcher
	# echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
	# dispatcher.add_handler(echo_handler)

	# dispatcher for chatgpt
	global chatgpt
	# chatgpt = HKBU_ChatGPT(config)
	chatgpt = HKBU_ChatGPT()
	chatgpt_handler = MessageHandler(Filters.text & (~Filters.command), equiped_chatgpt)
	dispatcher.add_handler(chatgpt_handler)

	global google_route
	google_route = Route()
	dispatcher.add_handler(CommandHandler("route", route))

	# on different commands - answer in Telegram
	dispatcher.add_handler(CommandHandler("add", add))
	dispatcher.add_handler(CommandHandler("help", help_command))
	dispatcher.add_handler(CommandHandler("hello", hello))

	# To start the bot:
	updater.start_polling()
	updater.idle()

def equiped_chatgpt(update, context):
	global chatgpt
	reply_message = chatgpt.submit(update.message.text)
	logging.info("Update: " + str(update))
	logging.info("context: " + str(context))
	context.bot.send_message(chat_id=update.effective_chat.id, text=reply_message)

def echo(update, context):
	reply_message = update.message.text.upper()
	logging.info("Update: " + str(update))
	logging.info("context: " + str(context))
	context.bot.send_message(chat_id=update.effective_chat.id, text= reply_message)

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def help_command(update: Update, context: CallbackContext) -> None:
	"""Send a message when the command /help is issued."""
	update.message.reply_text('Helping you helping you.')

def add(update: Update, context: CallbackContext) -> None:
	"""Send a message when the command /add is issued."""
	try:
		global redis1
		logging.info(context.args[0])
		msg = context.args[0] 	# /add keyword <-- this should store the keyword
		redis1.incr(msg)

		update.message.reply_text('You have said ' + msg + ' for ' + redis1.get(msg).decode('UTF-8') + ' times.')

	except (IndexError, ValueError):
		update.message.reply_text('Usage: /add <keyword>')

def route(update: Update, context: CallbackContext) -> None:
	"""Send a message when the command /route is issued."""
	try:
		global redis1
		global google_route
		logging.info(context.args[0])
		start_add = context.args[0]
		logging.info(context.args[1])
		end_add = context.args[1]
		directions_result = google_route.query_route(start_add,end_add)
		legs = directions_result[0]['legs']
		for leg in legs:
			Start_Address = leg['start_address']

		update.message.reply_text('Start Address:' + Start_Address)

	except (IndexError, ValueError):
		update.message.reply_text('Usage: /route <start address> <end address>')

def hello(update: Update, context: CallbackContext) -> None:
	"""Send a message when the command /hello is issued."""
	try:
		global redis1
		logging.info(context.args[0])
		msg = context.args[0]  # /hello keyword <-- this should store the keyword

		update.message.reply_text('Good day,' + msg + '!')

	except (IndexError, ValueError):
		update.message.reply_text('Usage: /hello <keyword>')

if __name__ == '__main__':
	main()