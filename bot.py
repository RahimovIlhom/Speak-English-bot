import logging

from aiogram import Bot, Dispatcher, executor, types
from oxfordLookup import getDefinitions
from googletrans import Translator
translator = Translator()

API_TOKEN = '5735017162:AAFavUX-UxWBAdKi9XCz49cj_NAT4xEXAPM'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Botni ishga tushirish"),
            types.BotCommand("help", "Yordam")
        ]
    )

async def on_startup(dispatcher):
    # Buyruqlarni qo'shamiz
    await set_default_commands(dispatcher)

@dp.message_handler(commands=['start'])
async def send_start(message: types.Message):
    """
    '/start' buyruq kelganda javob beruvchi funksiya
    """
    await message.reply("Assalomu alaykum. 'Speak English and translate' botimizga xush kelibsiz!")

@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    """
    '/help' buyruq kelganda javob beruvchi funksiya
    """
    await message.reply("Botimizdan qanday foydalanish mumkin.\n"
                        "Siz biror bir mavzuga doir ma'lumotlar olish uchun sarlavhaa jo'nating.\n"
                        "Tarjima qilish uchun matn jo'nating.")


@dp.message_handler()
async def tarjimon(message: types.Message):
    # old style:
    # await bot.send_message(message.chat.id, message.text)
    language = translator.detect(message.text).lang
    if language == 'en':
        word_id = message.text
    else:
        word_id = translator.translate(message.text, dest='en').text
    lookup = getDefinitions(word_id)
    if lookup:
        await message.reply(f"Word: {word_id}\n"
                            f"Definitions:\n{lookup['definitions']}")
        if lookup.get('audio'):
            await message.reply_voice(lookup['audio'])
    else:
        destr = 'uz' if language == 'en' else 'en'
        await message.reply(translator.translate(message.text, dest=destr).text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)