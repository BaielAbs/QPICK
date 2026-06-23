from aiogram.filters import Command
from aiogram.types import Message
from aiogram import Router, F
import aiohttp
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

router = Router()
Register = "https://6a2fe782a7f8866418d53f42.mockapi.io/Register"
Order = "https://6a2fe782a7f8866418d53f42.mockapi.io/Orders"

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Info")],
        [KeyboardButton(text="Orders")],
    ],
    resize_keyboard=True
)

@router.message(Command("start"))
async def start(message: Message):
    await message.answer("Это бот по Store Iphone QPick", reply_markup=main_keyboard)

@router.message(F.text == "Orders")
async def orders(message: Message):
    await message.answer("Введите номер заказа")

@router.message(F.text=="Info")
async def info(message: Message):
    await message.answer("📱 Добро пожаловать!\n Этот бот создан для магазина техники QPICK.\n \n С помощью бота вы можете:\n • Просматривать свой товар\n • Узнавать характеристики устройств\n \n 🌐 Наш сайт: ВАША_ССЫЛКА_ЗДЕСЬ\n \n Спасибо, что выбрали нас!\n")


@router.message()
async def find(message: Message):
    order_number = message.text.strip()

    async with aiohttp.ClientSession() as session:
        async with session.get(Order, ssl=False) as response:
            if response.status == 200:
                orders_list = await response.json()
                found = False

                for item in orders_list:
                    if str(item["number"]) == str(order_number):
                        caption_text = (
                            f"Продукт: {item['product']}\n"
                            f"Цена: {item['price']}\n"
                            f"Номер: №{item['number']}\n"
                        )
                        await message.answer_photo(
                            photo=item["img"],
                            caption=caption_text
                        )
                        found = True

                if not found:
                    await message.answer("Заказ не найден")
            else:
                await message.answer("Ошибка сервера при получении заказов")

