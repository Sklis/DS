import requests
import json
from aiogram import Bot, Dispatcher, executor, types


class CurrencyBot:
    def __init__(self, url: str):
        self.url = url

    def convert2RU(self, currency: str, value: float):
        data = requests.get(f"{self.url}").json()
        return round(data['Valute'][currency]['Previous'] * value, 2)

    def convertRU2Currency(self, currency: str, value: float):
        data = requests.get(f"{self.url}").json()
        return round(data['Valute'][currency]['Previous'] / value, 2)

    def currencySearch(self, currency: str):
        data = requests.get(f"{self.url}").json()
        index = 0
        for i in data['Valute']:
            if currency == data['Valute'][i]['CharCode']:
                index = 1
                break
        return index


if __name__ == '__main__':
    cc = CurrencyBot(url='https://www.cbr-xml-daily.ru/daily_json.js')

    bot = Bot('6221700392:AAHKVFkElfXof_LVIUBo-eQptdyl6mYlnt8')
    dp = Dispatcher(bot)

    user_states = {}

    @dp.message_handler(commands=['start'])
    async def start(message):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        buttons = ['💱 Да', '🚫 Нет']
        keyboard.add(*buttons)
        await message.reply(f"Привет {message.from_user.first_name}, ты хочешь конвертировать в рубли?", reply_markup=keyboard)

    @dp.message_handler(commands=['help'])
    async def welcome_help(message):
        await bot.send_message(message.chat.id, 'Цель проекта - создать чат бот, \
                               который умеет взаимодействовать с внешними REST API.\
                               По запросу пользователя бот получает от сервиса актуальную информацию курса валют.\
                               Принимает какое количество и какой валюты в какую конвертировать. Результат выводит на экран.\
                               Введите /start и следуйте указаниям бота...')

    @dp.message_handler()
    async def repeat(message: types.Message):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        buttons = ['💱 Да', '🚫 Нет']
        keyboard.add(*buttons)
        await message.reply(f"Можешь попробовать еще раз", reply_markup=keyboard)

    @dp.message_handler()
    async def handle_currency_index(message: types.Message):
        user_id = message.from_user.id
        if user_id not in user_states:
            user_states[user_id] = {}

        if cc.currencySearch(message.text) == 1:
            user_states[user_id]['currency_index'] = message.text
            await message.answer('Введите сумму для конвертации')
            handle_amount(message)
            return 0
        else:
            await message.answer('Такой валюты не существует')
            await get_currency(message)
            return 1
        
    @dp.message_handler()
    async def handle_amount(message: types.Message):
        user_id = message.from_user.id

        try:
            user_states[user_id]['amount'] = float(message.text)
            return
        
        except ValueError:
            await message.answer('Такой суммы не существует')
            await handle_currency_index(message)
            return

    
    @dp.message_handler()
    async def get_currency_2_rub(message: types.Message, user_id: str):
        if message.text in {'💱 Да', 'Да', 'да'}:
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            buttons = ['USD', 'EUR', 'GBP']
            keyboard.add(*buttons)
            await message.reply('Выбери валюту или укажите индекс нужной Вам валюты', reply_markup=keyboard)
            
            currency_index = await handle_currency_index(message)
            amount = user_states[user_id]['amount']

            if currency_index == 1: 
                result = cc.convert2RU(user_states[user_id]['currency_index'], user_states[user_id]['amount'])
                await message.answer(f"Для покупки {currency_index} в размере {amount}, необходимо {result} рублей + комиссия банка.")
        
        await repeat()

    
    @dp.message_handler()
    async def get_rub_2_currency(message: types.Message, user_id: str):
        if message.text in {'🚫 Нет', 'нет', 'Нет'}:
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            buttons = ['USD', 'EUR', 'GBP']
            keyboard.add(*buttons)
            await message.reply('Выберите в какую валюту конвертировать рубли или введи индекс', reply_markup=keyboard)

            currency_index = await handle_currency_index(message)
            amount = user_states[user_id]['amount']
            
            if currency_index == 1:
                result = cc.convertRU2Currency(currency_index, amount)
                await message.answer(f"При продаже {currency_index} в размере {amount}, необходимо {result} + комиссия банка.")
                
        await repeat()
            
    executor.start_polling(dp, skip_updates=True)
    
