from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ChatActions, ReplyKeyboardMarkup, CallbackQuery

from filters import IsUser
from handlers.user.menu import cart
from keyboards.inline.products_from_cart import product_markup
from keyboards.inline.products_from_catalog import product_cb
from loader import dp, db, bot


@dp.message_handler(IsUser(), text=cart)
async def process_cart(message: Message, state: FSMContext):
    cart_data = db.fetchall("SELECT * FROM cart WHERE cid=?", (message.chat.id,))
    if len(cart_data) == 0:
        await message.answer("Ваша корзина пуста.")
    else:
        await bot.send_chat_action(message.chat.id, ChatActions.TYPING)
        async with state.proxy() as data:
            data["products"] = {}
        order_cost = 0
        for _, idx, count_in_cart in cart_data:
            product = db.fetchone("SELECT * FROM products WHERE idx=?", (idx,))
            if product == None:
                db.query("DELETE FROM cart WHERE idx=?", (idx,))
            else:
                _, title, body, image, price, _ = product
                order_cost += price
                async with state.proxy() as data:
                    data["products"][idx] = [title, price, count_in_cart]
                markup = product_markup(idx, count_in_cart)
                text = f"<b>{title}</b>\n\n{body}\n\nЦена: {price} руб."
                await message.answer_photo(photo=image, caption=text, reply_markup=markup)
        if order_cost != 0:
            markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
            markup.add("Оформить заказ")
            await message.answer("Перейти к оформлению?", reply_markup=markup)


@dp.callback_query_handler(IsUser(), product_cb.filter(action="count"))
@dp.callback_query_handler(IsUser(), product_cb.filter(action="increase"))
@dp.callback_query_handler(IsUser(), product_cb.filter(action="decrease"))
async def product_callback_handler(query: CallbackQuery, callback_data: dict, state: FSMContext):
    idx = callback_data["id"]
    action = callback_data["action"]
    if "count" == action:
        async with state.proxy() as data:
            if "products" not in data.keys():
                await process_cart(query.message, state)
            else:
                await query.answer("Количество - " + data["products"][idx][2])
    else:
        async with state.proxy() as data:
            if "products" not in data.keys():
                await process_cart(query.message, state)
            else:
                data["products"][idx][2] += 1 if "increase" == action else -1
                count_in_cart = data["products"][idx][2]
                if count_in_cart == 0:
                    db.query("DELETE FROM cart WHERE cid = ? AND idx = ?", (query.message.chat.id, idx))
                    await query.message.delete()
                else:
                    db.query("UPDATE cart SET quantity = ? WHERE cid = ? AND idx = ?",
                             (count_in_cart, query.message.chat.id, idx))
                    await query.message.edit_reply_markup(product_markup(idx, count_in_cart))
