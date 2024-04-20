from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Text

TOKEN = '7013626156:AAFESd0ZZokfvahCjDM7lP9xJUja18iDOyU'

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    kb = [
        [
            types.KeyboardButton(text="Китайские площадки"),
            types.KeyboardButton(text="Европейские сервисы")
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

    await message.reply("Привет!\nЯ помогу рассчитать стоимость товара, просто нажми на одну из кнопок ниже",
                        reply_markup=keyboard)


@dp.message_handler(Text(equals="Китайские площадки"), state='*')
async def chinese_platforms(message: types.Message, state: types.Chat):
    await state.update_data(type='chinese')
    await message.reply("Укажите стоимость товара в юанях:")


@dp.message_handler(Text(equals="Европейские сервисы"), state='*')
async def european_services(message: types.Message, state: types.Chat):
    await state.update_data(type='european')
    await message.reply("Укажите стоимость товара в евро:")


@dp.message_handler(lambda message: message.text.isdigit(), state='*')
async def process_price(message: types.Message, state: types.Chat):
    data = await state.get_data()
    if 'type' in data:
        price = int(message.text)
        if data['type'] == 'chinese':
            await message.reply(f"Цена товара: {price * 14} рублей")
        elif data['type'] == 'european':
            await message.reply(f"Цена товара: {price * 115} рублей")
    else:
        await message.reply("Ошибка: Не удалось определить тип товара.")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
