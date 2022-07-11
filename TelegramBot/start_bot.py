import os
import django

from bot.bot import bot

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TelegramBot.settings')
django.setup()

if __name__ == "__main__":
    bot()
