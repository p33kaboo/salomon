import json
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import hbold, hlink
from main import MyParser

token = ""

bot = Bot(token=token, parse_mode=types.ParseMode.HTML) # parser_mode указывает за форматирование
                                                        # ответного сообщения в HTML
dp = Dispatcher(bot)
parser = MyParser() # создаю объект класса, который занимается сбором данных

# отвечаем на старт комманду инициализацией кнопок
@dp.message_handler(commands="start")
async def start(message: types.Message):
    start_buttons = ["Кроссовки", "Видеокарты","Гречка"] # кнопки, которые нам нужны.м
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True) # создаю обект класса
    keyboard.add(*start_buttons)

    await message.answer("Товары со скидкой", reply_markup=keyboard)

@dp.message_handler(Text(equals="Кроссовки"))
async def get_discount_sneakers(message: types.Message):
    await message.answer("Please waiting...")

    parser.collect_data()

    with open("result_data.json", "r") as file:
        data = json.load(file)

    for item in data:
        card = f"{hlink(item.get('title'), item.get('link'))}\n" \
               f"{hbold('Категория: ')} {item.get('category')}\n" \
               f"{hbold('Цена: ')} {item.get('price')}\n" \
               f"{hbold('Цена со скидкой ')} -{item.get('discount_percent')}%: {item.get('sale')}🔥\n" \
               f"{hbold('Цвет: ')} {item.get('color_name')}" \

        await message.answer(card)

#  уже лютый треш

@dp.message_handler(Text(equals="Видеокарты"))
async def get_discount_sneakers(message: types.Message):
    await message.answer("Пока не реализовано")


@dp.message_handler(Text(equals="Гречка"))
async def get_discount_sneakers(message: types.Message):
    await message.answer("Пока не реализовано")


# запускаем бота
def main():
    executor.start_polling(dp)

if __name__ == "__main__":
    main()

