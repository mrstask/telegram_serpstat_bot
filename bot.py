import os
import telebot
from telebot.types import Message
from flask import Flask, request

from settings import TelegramConf, SerpstatConf, HerokuConf, serpstat_popular_regions, develop, log
from dbhelper import postgres_handler
from helpers import plain_domain, api_key_limit
from my_validators import validate_serpstat_key, validate_domain, validate_regions

server = Flask(__name__)
bot = telebot.TeleBot(token=TelegramConf.API_KEY)
user = bot.get_me()
bot.get_updates()


def registered(func):
    def wrapper(message: Message):
        user_id = message.from_user.id
        if not postgres_handler.get_user(user_id):
            return bot.send_message(message.from_user.id, 'You are not registered, go to /register')
        func(message)
    return wrapper


def has_api_key(func):
    def wrapper(message: Message):
        user_id = message.from_user.id
        if not postgres_handler.get_user(user_id):
            return bot.send_message(message.from_user.id, 'You are not registered, go to /register')
        if not postgres_handler.get_user(user_id)['api_key']:
            message_to_user = 'You have no Serpstat API key to add API key use command /add_key'
            return bot.send_message(message.from_user.id, message_to_user)
        func(message)
    return wrapper


def api_key_has_queries(func):
    def wrapper(message: Message):
        rows = api_key_limit(message.from_user.id)
        if rows == 'Invalid token!':
            return bot.send_message(message.from_user.id, 'Invalid API Key!')
        if rows <= 0:
            return bot.send_message(message.from_user.id, 'Your API key have left NO queries to API')
        func(message)
    return wrapper


@bot.message_handler(commands=['start'])
def handle_text(message: Message):
    message_to_user = '''To register use command /register
To add api key use command /add_key
To view key limits use command /get_limits
To see codes of popular regions /region_codes
To see your data region use command /show_regions
To change domain data region use command /change_regions
To get domain keywords just write plain domain
    '''
    return bot.send_message(message.from_user.id, message_to_user)


@bot.message_handler(commands=['register'])
def register(message: Message):
    user_id = message.from_user.id
    if not postgres_handler.get_user(user_id):
        postgres_handler.add_user(user_id)
        message_to_user = 'Congratulation you are just registered to add API key use command /add_key'
        return bot.send_message(message.from_user.id, message_to_user)
    if not postgres_handler.get_user(user_id)['api_key']:
        message_to_user = 'You have no Serpstat API key to add API key use command /add_key'
        return bot.send_message(message.from_user.id, message_to_user)
    else:
        message_to_user = 'You already registered and you have API key, if you want to update key use command /add_key'
        bot.send_message(message.from_user.id, message_to_user)


# ----------------- OPERATIONS WITH THE KEYS ------------------
@bot.message_handler(commands=['add_key'])
@registered
def add_key(message: Message):
    sent = bot.send_message(message.chat.id, 'Insert API key:')
    bot.register_next_step_handler(sent, add_api_key)


def add_api_key(message: Message):
    if not validate_serpstat_key(message.text):
        message_to_user = 'You are providing invalid API key try again /add_key'
        return bot.send_message(message.chat.id, message_to_user)
    key_id = postgres_handler.get_key_by_value(message.text)  # checking if this key already in db
    if not key_id:
        key_id = postgres_handler.add_key(message.text)
        postgres_handler.update_user_key(message.from_user.id, key_id)
    else:
        postgres_handler.update_user_key(message.from_user.id, key_id['key_id'])
    return bot.send_message(message.chat.id, 'Your key was check your limits /get_limits')


@bot.message_handler(commands=['get_limits'])
@registered
@has_api_key
def get_limits(message: Message):
    user_id = message.from_user.id
    api_key = postgres_handler.get_user(user_id)['api_key']
    SerpstatConf.API_KEY = postgres_handler.get_key_by_id(api_key)['api_key']
    get_key_limits(message)


# ----------------- OPERATIONS WITH THE REGIONS ------------------
@bot.message_handler(commands=['change_regions'])
@registered
def add_region(message: Message):
    sent = bot.send_message(message.chat.id, 'Insert regions separated by comma:')
    bot.register_next_step_handler(sent, set_regions)


def set_regions(message: Message):
    invalid_inputs = validate_regions(message.text)
    if invalid_inputs:
        message_to_user = f'You are providing invalid region codes {invalid_inputs}, see /region_codes'
        return bot.send_message(message.chat.id, message_to_user)
    for region in message.text.split(','):
        postgres_handler.add_region_to_user(message.from_user.id, region)
        bot.send_message(message.chat.id, f'Region {region} was added')
    m = f'All regions were added successfully to see your regions use command /show_regions'
    return bot.send_message(message.chat.id, m)


@bot.message_handler(commands=['region_codes'])
def region_codes(message: Message):
    regions = []
    for region_code in serpstat_popular_regions:
        region_name = postgres_handler.get_region_name(region_code)
        search_engine = 'Google' if region_code.startswith('g') else 'Yandex'
        regions.append(f'{search_engine} {region_name} - {region_code}')
    return bot.send_message(message.chat.id, '\n'.join(regions))


@bot.message_handler(commands=['show_regions'])
@registered
def get_region(message: Message):
    regions = postgres_handler.get_user(message.from_user.id)['regions']
    bot.send_message(message.chat.id, 'Your regions are:')
    for region_code in regions:
        search_engine = 'Google' if region_code.startswith('g') else 'Yandex'
        region_name = postgres_handler.get_region_name(region_code)
        bot.send_message(message.chat.id, f'{search_engine} {region_name}, region code {region_code}')


@bot.message_handler(content_types=['text'])
@registered
@has_api_key
@api_key_has_queries
def handle_message(message: Message):
    user_id = message.from_user.id
    api_key = postgres_handler.get_user(user_id)['api_key']
    SerpstatConf.API_KEY = postgres_handler.get_key_by_id(api_key)['api_key']
    domain = validate_domain(message.text)
    if domain:
        get_keywords(domain, message.chat.id, user_id)
    else:
        bot.send_message(message.chat.id, 'Domain is not valid')


def get_key_limits(message: Message):
    requests_left = api_key_limit(message.from_user.id)
    if requests_left == 'Invalid token!':
        return bot.send_message(message.chat.id, 'Invalid token!')
    message_to_user = f'You have left {requests_left} queries'
    return bot.send_message(message.chat.id, message_to_user)


def get_keywords(domain: str, chat_id: int, user_id: int):
    regions = postgres_handler.get_user(user_id)['regions']
    if not regions:
        return bot.send_message(chat_id, 'You have no regions, to set regions use command /change_regions')
    for se in regions:
        kwd, traff = plain_domain(domain.lower(), se, user_id)
        region_name = postgres_handler.get_region_name(se)
        search_engine = 'Google' if se.startswith('g') else 'Yandex'
        message_to_user = f'{domain} in {search_engine} {region_name} have {kwd} keywords and {traff} monthly traffic'
        bot.send_message(chat_id, message_to_user)


@server.route('/' + TelegramConf.API_KEY, methods=['POST'])
def get_message():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/")
def web_hook():
    bot.remove_webhook()
    bot.set_webhook(url=HerokuConf.APP_URL + TelegramConf.API_KEY)
    return 'Your app is working', 200


if __name__ == '__main__':
    log.debug('starting_main')
    if develop:
        bot.polling(none_stop=True, interval=0)
    else:
        server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
