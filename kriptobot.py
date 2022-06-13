from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, InlineQueryHandler, CallbackQueryHandler
from bs4 import BeautifulSoup as BS
import requests, random, json

TOKEN = 'TOKEN'
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher


def start(update, _):
    update.message.reply_text(text='/help - ознакомиться со списком команд')


def help(update, _):
    update.message.reply_text(text='Привет!\n\nСписок команд:\n/anekdot - послушать анекдот\n/orel_reshka - орел или решка?\n/currency - узнать актуальный курс разных валют')


def anekdot(update, _):
    r = requests.get('https://www.anekdot.ru/random/anekdot/')
    html = BS(r.content, 'html.parser')
    text = html.find('div', 'text').get_text()
    update.message.reply_text(text=f'{text}\n🤣🤣🤣')


def hot(update, _):
    s = ['Орел!', 'Решка!']
    update.message.reply_text(text=f'{random.choice(s)}')


def buttons_currency(update, _):
    keyboard = [
        [
            InlineKeyboardButton('USD', callback_data='USD'),
            InlineKeyboardButton('EUR', callback_data='EUR'),
        ],
        [
            InlineKeyboardButton('GBP', callback_data='GBP'),
            InlineKeyboardButton('NOK', callback_data='NOK'),
        ],
        [
            InlineKeyboardButton('PLN', callback_data='PLN'),
            InlineKeyboardButton('CHF', callback_data='CHF'),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Пожалуйста, выберите валюту:', reply_markup=reply_markup)


def currency(update, _):
    query = update.callback_query
    response = query.data
    query.answer()

    data = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()
    valute = data['Valute'][response]
    value = round(valute['Value'] / valute['Nominal'], 2)
    name = valute['Name']

    query.edit_message_text(text=f'Валюта: {name}\nАктуальный курс: {value} ₽')


def unknown(update, _):
    update.message.reply_text(text='Эта тема для меня очень сложная. Спросите что-нибудь другое, пожалуйста')


dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('help', help))
dispatcher.add_handler(CommandHandler('anekdot', anekdot))
dispatcher.add_handler(CommandHandler('orel_reshka', hot))
dispatcher.add_handler(CommandHandler('currency', buttons_currency))
dispatcher.add_handler(CallbackQueryHandler(currency))
dispatcher.add_handler(MessageHandler(Filters.text, unknown))
updater.start_polling()
updater.idle()
