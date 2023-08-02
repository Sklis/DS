import requests
from aiogram import Bot, Dispatcher, executor, types


class Conversion:  # описываем класс конвертации валют
    def __init__(self, url: str):  # метод инициализации
        self.url = url


    def convertUSD2RU(self, value: float): # метод конвертации доллара в рубли
        currency = 'USD'
        response = requests.get(f"{self.url}").json()  # получили информацию с сайта
        currency_rub = value * response['Valute'][currency]['Value']
        return currency_rub


    def convertEUR2RU(self, value: float):  # метод конвертации евро в рубли
        response = requests.get(f"{self.url}").json()  # получили информацию с сайта
        currency_rub = value * response['Valute']['EUR']['Value']
        return currency_rub


if __name__ == '__main__':  # Создание экземпляра класса конвертации
    conv = Conversion(url='https://www.cbr-xml-daily.ru/daily_json.js')


# Создаем экземпляр бота
bot = Bot('6056186870:AAEjkuN91XClmSUbCrrquK1TzFBhz2aWXKs')  # использовали класс ВОТ библиотеки aiogram для создания объекта бота
dp = Dispatcher(bot)  # это для того чтобы наш бот мог принимать и отправлять сообщения
summa = float(0)  # будет глобальная переменная


@dp.message_handler(commands=['start'])  # отслеживаем команду старт
async def start(message: types.Message):  # так как aiogram ассинхронная библиотека, все функции в ней ассинхронные
    await message.answer('Привет! Помогу посчитать сколько рублей в твоих валютных сбережениях. Введи сумму, которую необходимо конвертировать')
# types.Message это параметр, который будет хранить в себе полную информацию относительно чата и о его пользователе
# await - мы будем дожидаться выполнения некоторого действия, в этой функции - отправки сообщения


@dp.message_handler()  # обрабатываем входящий текст с суммой валюты/обозначением валюты
async def info(message: types.Message):
        vvod = message.text
        global summa
        if vvod == 'USD':
            result = conv.convertUSD2RU(summa)
            summa=0
            await message.answer(f'Получается: {round(result, 2)} руб.  Повторим? Вводи сумму, которую необходимо конвертировать')
        elif vvod == 'EUR':
            result = conv.convertEUR2RU(summa)
            summa=0
            await message.answer(f'Получается: {round(result, 2)} руб. Повторим? Вводи сумму, которую необходимо конвертировать')
        else:
            try:
                summa = float(vvod)
            except ValueError:
                summa = 0
                vvod = 0
                await message.answer('Ну ты богач! я не знаю такой суммы, сосредоточься и попробуй еще раз')
                return
            if summa > 0.000000001:
                # await message.answer('Проверка')
                # markup = types.InlineKeyboardMarkup() # для создания встроенных кнопок
                # markup.add(types.InlineKeyboardButton('USD', callback_data= conv.convertUSD2RU(summa))) # прописсываем возвращаемые данные
                # markup.add(types.InlineKeyboardButton('EUR', callback_data= conv.convertEUR2RU(summa)))
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
                buttons = ['USD', 'EUR']
                keyboard.add(*buttons)  # добавление кнопок
                await message.reply('Выбери валюту', reply_markup=keyboard)  # сообщение при создании 2-х кнопок
                return
            else:
                await message.answer('Ну тут совсем мало, не получится конвертировать, попробуй еще раз')
                summa=0
                vvod=0
                return


executor.start_polling(dp)  # чтобы наш бот работал пстоянно

