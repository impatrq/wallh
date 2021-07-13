import os
from replit import db

from telegram import Update #upm package(python-telegram-bot)
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext  #upm package(python-telegram-bot)


from math import ceil
from flask import render_template
from flask import Flask
app = Flask(__name__)

@app.route('/')
@app.route('/<int:page>')
def home(page=None):
    ks = sorted(map(int, db.keys()))
    pages = ceil(len(ks) / 10)
    if page is None: #Default to latest page
        page = pages

    if page < pages:
        next_page = page + 1
    else:
        next_page = None
    if page > 1:
        prev_page = page - 1
    else:
        prev_page = None

    messages = tuple(db[str(key)] for key in ks[(page-1)*10:page*10])

    return render_template('home.html', messages=messages, next_page=next_page, page=page, prev_page=prev_page)


def latest_key():
    ks = db.keys()
    if len(ks):
        return max(map(int, ks))
    else:
        return -1


def help_command(update: Update, context: CallbackContext) -> None:
    htext = '''
    Informanos en que podemos ayudarte
    
'''
    update.message.reply_text(htext)

def start_command(update: Update, context: CallbackContext) -> None:
    htext = '''

/obstruccion (mensaje para que lo muevan de lugar)

/start

/help

/fetch (para ver situación anterior)

'''
    update.message.reply_text(htext)


def log(update: Update, context: CallbackContext) -> None:
    db[str(latest_key() + 1)] = update.message.text


def fetch(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(db.get(str(latest_key()), 'Esta todo bien.'))


def main():
    updater = Updater(os.getenv("TOKEN"))

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start_command))
    dispatcher.add_handler(CommandHandler("obstruccion", objeto_command))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("fetch", fetch))

    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, log))

    updater.start_polling()

    #updater.idle()
    app.run(host='0.0.0.0', port=8080)


if __name__ == '__main__':
    main()