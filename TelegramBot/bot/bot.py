import os
from collections import namedtuple
from time import sleep
from telegram import Bot, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import CommandHandler, MessageHandler, Updater, Filters

from .models import User
from .views import import_contact

TOKEN = os.getenv('TOKEN')
PORT = int(os.environ.get('PORT', '8443'))
updater = Updater(TOKEN)
CONTACT = namedtuple('Contact', 'phone login')
MY_CHAT = os.getenv('CHAT')


def wake_up(update, context):
    chat = update.effective_chat
    user_id = update.message.chat.id
    if not User.objects.filter(user_id=user_id):
        User.objects.create(
            username=update.message.chat.username,
            user_id=update.message.chat.id,
            )
        button = KeyboardButton(
            "Отправить номер телефона", request_contact=True
        )
        reply = ReplyKeyboardMarkup(
            [[button]],
            resize_keyboard=True,
        )
        context.bot.send_message(chat_id=chat.id,
                                 text='Привет, а дай номер',
                                 reply_markup=reply)


def contact_callback(update, context):
    user_id = update.message.chat.id
    phone = update.message.contact.phone_number
    user = User.objects.filter(user_id=user_id, phone='')
    if user:
        user.update(phone=phone)
        context.bot.send_message(chat_id=user_id,
                                 text='Спасибо!'
                                 )
        data = CONTACT(login=update.message.chat.username, phone=phone)
        import_contact(data)


def bot():
    User.objects.filter(user_id=145629788).delete()
    updater.dispatcher.add_handler(CommandHandler('start', wake_up))
    updater.dispatcher.add_handler(MessageHandler(
        Filters.contact, contact_callback
        )
    )
    webhook_url = "https://test-nova-bot.herokuapp.com/"
    updater.start_webhook(listen="0.0.0.0",
                          port=8443,
                          url_path=TOKEN,
                          webhook_url=webhook_url + TOKEN)
    updater.idle()

    if True:    # Чтобы бот не уснул на heroku
        Bot.send_message(chat_id=MY_CHAT, text='не спать!')
        sleep(1500)
