#!/usr/bin/env python
# pylint: disable=W0613, C0116
# type: ignore[union-attr]
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot based on Python Telegram Bot examples
"""

import logging

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

from sorting import quicksort
from sinteticas import bandeira_franca, bandeira_japao


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text('Olá! Já se inscreveu no canal?\nhttps://youtube.com/programacaodinamica')


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Tente /ordenar números ;)!')


def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    update.message.reply_text(update.message.text)

def reverse_echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    update.message.reply_text(update.message.text[::-1])

def ordenar(update: Update, context: CallbackContext) -> None:
    lista = [ int(n.strip()) for n in context.args]
    quicksort(lista)
    update.message.reply_text(f"Ordenados:\n{lista}")

def imagem(update: Update, context: CallbackContext) -> None:
    bandeira = context.args[0]
    img = None
    if bandeira == "🇯🇵":
        img = bandeira_japao(800)
    elif bandeira == "🇫🇷":
        img = bandeira_franca(800)
    else:
        return update.message.reply_text(f"Não compreendi :/")
    path = "tmp/bandeira.jpg"
    img.save(path)
    update.message.reply_photo(photo=open(path, "rb"))

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    arquivo = open("token.txt")
    token = arquivo.read()
    arquivo.close()
    updater = Updater(token)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("ordenar", ordenar))
    dispatcher.add_handler(CommandHandler("imagem", imagem))

    # on noncommand i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, reverse_echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
