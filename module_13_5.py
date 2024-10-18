from aiogram import Bot, Dispatcher, types, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
import asyncio

# Вставьте ваш токен
API_TOKEN = ' '

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

router = Router()
dp.include_router(router)

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Рассчитать"), KeyboardButton(text="Информация")]
    ],
    resize_keyboard=True
)

@router.message(Command("start"))
async def start_command(message: Message, state: FSMContext):
    await message.answer("Нажми 'Рассчитать' для начала расчета калорий или 'Информация' для получения данных.", reply_markup=keyboard)
    await state.update_data(greeted=True)

@router.message(lambda message: message.text == "Рассчитать")
async def set_age(message: Message, state: FSMContext):
    await message.answer("Введите свой возраст:")
    await state.set_state(UserState.age)

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

        # Расчет калорий по формуле Миффлина - Сан Жеора для женщин
        calories = 10 * weight + 6.25 * growth - 5 * age - 161
        await message.answer(f"Ваша норма калорий {calories:.2f} ккал в день.")
        await state.clear()
    except ValueError:
        await message.answer("Пожалуйста, введите корректный вес (число).")

@router.message(lambda message: message.text == "Информация")
async def info_command(message: Message):
    await message.answer("Этот бот помогает рассчитать норму калорий на день. Нажмите 'Рассчитать', чтобы начать.")

@router.message(lambda message: True)
async def any_message(message: Message, state: FSMContext):
    user_state = await state.get_state()
    greeted = await state.get_data()

    if user_state is None and not greeted.get("greeted"):
        await message.answer("Привет! Я бот, помогающий твоему здоровью. Нажми /start для запуска бота")
        await state.update_data(greeted=True)

async def main():
    print("Запуск бота...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())