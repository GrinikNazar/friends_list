import os
import telebot
import requests
from io import BytesIO
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.types import InputMediaPhoto
from dotenv import load_dotenv


load_dotenv()
bot = telebot.TeleBot(os.getenv("BOT_TOKEN"))
URL = os.getenv('SERVER_URL')


@bot.message_handler(commands=['get_all_friends'])
def get_all_friends(message):
    url = URL + '/friends'
    response = requests.get(url)
    if response.status_code:
        for friend in response.json():
            photo_url = URL + friend['photo_url']
            photo = requests.get(photo_url)
            text = f'Друг: {friend["name"]}\nПрофесія: {friend["profession"]}'

            # Зробив окрему клаву для того щоб можна передати в калбек ID
            keyboard = InlineKeyboardMarkup()
            button = InlineKeyboardButton(text="Дізнатись більше", callback_data=f'id:{friend["id"]}')
            keyboard.add(button)

            bot.send_photo(message.chat.id, BytesIO(photo.content),
                           caption=text,
                           reply_markup=keyboard
                           )


# Обробник кнопки "Дінатись більше" на кожному з друзів
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    if 'id' in call.data.split(':'):
        friend_id = call.data.split(':')[1]
        friend_url = URL + '/friends/' + friend_id
        friend = requests.get(friend_url).json()
        photo_url = URL + friend['photo_url']
        photo = requests.get(photo_url)
        text = (f'Вся інформація про друга\n'
                f'Ім\'я: {friend["name"]}\n'
                f'Професія: {friend["profession"]}\n'
                f'Опис професії: {friend["profession_description"]}\n'
                f'URL:\n{photo_url}'
                )

        bot.edit_message_media(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            media=InputMediaPhoto(
                media=BytesIO(photo.content),
                caption=text
            )
        )


user_state = {}


# Старт
@bot.message_handler(commands=['add_friend'])
def start_step(message):
    user_state[message.chat.id] = {'step': 'name'}
    bot.send_message(message.chat.id, "Введи ім'я друга:")


# Ім'я
@bot.message_handler(func=lambda m: user_state.get(m.chat.id, {}).get('step') == 'name')
def title_step(message):
    user_state[message.chat.id]['name'] = message.text
    user_state[message.chat.id]['step'] = 'profession'
    bot.send_message(message.chat.id, "Професія друга:")


# Професія
@bot.message_handler(func=lambda m: user_state.get(m.chat.id, {}).get('step') == 'profession')
def description_step(message):
    user_state[message.chat.id]['profession'] = message.text
    user_state[message.chat.id]['step'] = 'profession_description'
    bot.send_message(message.chat.id, "Додай опис професії друга")


# Опис професії друга
@bot.message_handler(func=lambda m: user_state.get(m.chat.id, {}).get('step') == 'profession_description')
def description_step(message):
    user_state[message.chat.id]['profession_description'] = message.text
    user_state[message.chat.id]['step'] = 'photo'
    bot.send_message(message.chat.id, "Кинь фотку друга")


# Фото
@bot.message_handler(content_types=['photo'])
def photo_step(message):
    file_info = bot.get_file(message.photo[-1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    files = {'photo': (file_info.file_path.split('/')[-1], downloaded_file)}

    name = user_state[message.chat.id]['name']
    profession = user_state[message.chat.id]['profession']
    profession_description = user_state[message.chat.id]['profession_description']

    backend_url = URL + '/friends/'

    response = requests.post(
        backend_url,
        data={
            "name": name,
            'profession': profession,
            "profession_description": profession_description,
        },
        files=files
    )

    if response.status_code:
        bot.send_message(message.chat.id, "Друга добавлено!")
    else:
        bot.send_message(message.chat.id, f"Помилка: {response.status_code}")

    user_state.pop(message.chat.id, None)


if __name__ == '__main__':
    bot.infinity_polling(timeout=10)
