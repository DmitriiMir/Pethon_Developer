from aiogram import Bot, Dispatcher, types, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import asyncio

# Вставьте ваш токен
API_TOKEN = ''

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

router = Router()
dp.include_router(router)

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

inline_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Рассчитать норму калорий", callback_data="calories"),
            InlineKeyboardButton(text="Формулы расчёта", callback_data="formulas")
        ]
    ]
)

products_inline_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Мультивитамины для женщин UltraBalance", callback_data="product_buying"),
            InlineKeyboardButton(text="Инозитол 1000 мг капсулы UltraBalance", callback_data="product_buying"),
            InlineKeyboardButton(text="Витамины для женщин и мужчин", callback_data="product_buying"),
            InlineKeyboardButton(text="Цинк хелат", callback_data="product_buying")
        ],
        [
            InlineKeyboardButton(text="Отмена", callback_data="cancel")
        ]
    ]
)

keyboard = types.ReplyKeyboardMarkup(
    keyboard=[
        [types.KeyboardButton(text="Рассчитать"), types.KeyboardButton(text="Информация")],
        [types.KeyboardButton(text="Купить")]
    ],
    resize_keyboard=True
)

@router.message(Command("start"))
async def start_command(message: Message, state: FSMContext):
    await message.answer(
        "Нажми 'Рассчитать' для начала или 'Информация' для получения данных.",
        reply_markup=keyboard
    )
    await state.update_data(greeted=True)

@router.message(lambda message: message.text == "Рассчитать")
async def main_menu(message: Message):
    await message.answer("Выберите опцию:", reply_markup=inline_keyboard)

@router.callback_query(lambda call: call.data == "formulas")
async def get_formulas(call: CallbackQuery):
    formula_text = (
        "Формула Миффлина-Сан Жеора для женщин:\n"
        "10 * вес (кг) + 6.25 * рост (см) - 5 * возраст (годы) - 161"
    )
    await call.message.answer(formula_text)
    await call.answer()

@router.callback_query(lambda call: call.data == "calories")
async def set_age(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Введите свой возраст:")
    await state.set_state(UserState.age)
    await call.answer()

@router.message(UserState.age)
async def set_growth(message: Message, state: FSMContext):
    try:
        age = int(message.text)
        await state.update_data(age=age)
        await message.answer("Введите свой рост (в см):")
        await state.set_state(UserState.growth)
    except ValueError:
        await message.answer("Пожалуйста, введите корректный возраст (число).")

@router.message(UserState.growth)
async def set_weight(message: Message, state: FSMContext):
    try:
        growth = int(message.text)
        await state.update_data(growth=growth)
        await message.answer("Введите свой вес (в кг):")
        await state.set_state(UserState.weight)
    except ValueError:
        await message.answer("Пожалуйста, введите корректный рост (число).")

@router.message(UserState.weight)
async def send_calories(message: Message, state: FSMContext):
    try:
        weight = int(message.text)
        await state.update_data(weight=weight)

        data = await state.get_data()
        age = data['age']
        growth = data['growth']

        calories = 10 * weight + 6.25 * growth - 5 * age - 161
        await message.answer(f"Ваша норма калорий {calories:.2f} ккал в день.")
        await state.clear()
    except ValueError:
        await message.answer("Пожалуйста, введите корректный вес (число).")

@router.message(lambda message: message.text == "Информация")
async def info_command(message: Message):
    await message.answer(
        "Этот бот помогает рассчитать норму калорий на день. Нажмите 'Рассчитать', чтобы начать."
    )

@router.message(lambda message: message.text == "Купить")
async def get_buying_list(message: Message):
    products = [
        {"name": "Мультивитамины для женщин UltraBalance", "description": "Комплекс витаминов и минералов для взрослых 60 таблеток",
         "price": 1454, "image_url": "https://ir-2.ozone.ru/s3/multimedia-2/wc1000/6607026362.jpg"},
        {"name": "Инозитол 1000 мг капсулы UltraBalance", "description": "БАД комплекс для женского здоровья миоинозитол витамин для женщин и мужчин",
         "price": 1523, "image_url": "https://ir-2.ozone.ru/s3/multimedia-e/wc1000/6764941634.jpg"},
        {"name": "Витамины для женщин и мужчин", "description": "Общий комплекс 13+10, 90 капсул",
         "price": 566, "image_url": "https://ir-2.ozone.ru/s3/multimedia-1-n/wc1000/7076872103.jpg"},
        {"name": "Цинк хелат", "description": "Цинк хелат 25 мг, 90 таблеток / NFO Норвегия",
         "price": 1905, "image_url": "https://ir-2.ozone.ru/s3/multimedia-3/wc1000/6825233847.jpg"}
    ]

    for idx, product in enumerate(products, start=1):
        text = f"Название: {product['name']} | Описание: {product['description']} | Цена: {product['price']} руб."
        await message.answer(text)
        await message.answer_photo(photo=product['image_url'])

    await message.answer("Выберите продукт для покупки:", reply_markup=products_inline_keyboard)

@router.callback_query(lambda call: call.data == "product_buying")
async def send_confirm_message(call: CallbackQuery):
    await call.message.answer("Вы успешно приобрели продукт!")
    await call.answer()

@router.callback_query(lambda call: call.data == "cancel")
async def cancel_purchase(call: CallbackQuery):
    await call.message.answer("Покупка отменена.")
    await call.answer()

@router.message(lambda message: True)
async def any_message(message: Message, state: FSMContext):
    user_state = await state.get_state()
    greeted = await state.get_data()

    if user_state is None and not greeted.get("greeted", False):
        await message.answer(
            "Привет! Я бот, помогающий твоему здоровью. Нажми /start для запуска бота"
        )
        await state.update_data(greeted=True)

async def main():
    print("Запуск бота...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())