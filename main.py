#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Simple Bot to reply to Telegram messages
# This program is dedicated to the public domain under the CC0 license.
"""
This Bot uses the Updater class to handle the bot.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
# from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup
import logging
from parsing.MessageParser import MessageParser as mp
import parsing.IntentFeedback as gf
from parsing.States import *
from settigns import TOKEN

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


intent_parser = mp()
state = States.STARTED
n_photos = 0


def restart():
    global users_dict_id_to_username, users_to_query, state
    state = States.STARTED
    n_photos = 0
    print "Restarting bot..."


# Define handle for accidents
def shit_happens (bot, update):
    print "Oops you did it again!"


def add_photo(bot, update):
    global n_photos
    if n_photos == 1:
        text = "Let's get a photo from the right now."
    elif n_photos == 2:
        text = "And now one from the left."
    elif n_photos >= 3:
        text = "Great we are done taking evidence!"

    bot.sendMessage(update.message.chat_id, text=text)


def void(bot, update):
    """
    :param bot:
:param update:
    :return: Nothing. This is to handle irrelevant conversations
    """
    print "Nothing"

process_callback = {

    "add_photo" : add_photo,
    "shit_happens" : shit_happens,
    "None" : void,
}


def finalize_schedule(bot, update):
    bot.sendMessage(update.message.chat_id, text="I will calculate your losses and reply to you shortly")
    restart()


def intent_extractor(bot, update):
    """
    :param bot:
    :param update:
    :return: Parses the intent and calls the appropriate callback
    """
    global state, n_photos

    if update.message.photo and state == States.LISTENING:
        # handle photo
        # handle photo
        n_photos += 1
        process_callback["add_photo"](bot,update)
        if n_photos >= 3:
            state = States.FINALIZING
            finalize_schedule(bot, update)
            return

    intent = intent_parser.extract_intent(update.message.text)

    feedback, give_reply, state = gf.give_feedback(intent,state)

    if give_reply:
        bot.sendMessage(update.message.chat_id, text=feedback)

    if state.value < States.FINALIZING.value:
        process_callback[intent](bot,update)
    else:
        finalize_schedule(bot,update)


def error(bot, update, error):
    logger.warn('Update {} caused error {}'.format(update, error))


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Parse text for intent
    # dp.add_handler(MessageHandler([Filters.text], intent_extractor))
    dp.add_handler(MessageHandler([Filters.photo, Filters.text], intent_extractor))

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler('shit_happens', shit_happens))


    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
