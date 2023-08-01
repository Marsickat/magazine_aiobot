from aiogram.types import Message, ReplyKeyboardMarkup

from filters import IsAdmin, IsUser
from loader import dp

catalog = "Каталог"
cart = "Корзина"
delivery_status = "Статус заказа"

settings = "Настройка каталога"
orders = "Заказы"
questions = "Вопросы"


@dp.message_handler(IsAdmin(), commands="menu")
async def admin_menu(message: Message):
    markup = ReplyKeyboardMarkup(selective=True)
    markup.add(settings)
    markup.add(questions, orders)
    await message.answer("Меню", reply_markup=markup)


@dp.message_handler(IsUser(), commands="menu")
async def user_menu(message: Message):
    markup = ReplyKeyboardMarkup(selective=True)
    markup.add(catalog)
    markup.add(cart)
    markup.add(delivery_status)
    await message.answer("Меню", reply_markup=markup)
