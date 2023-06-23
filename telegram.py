import asyncio
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from config import Token, user_id
from main import get_all_to_excel, check_update, get_pages
from excel import to_excel

bot = Bot(token=Token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

id_ = ''
couner = int(0)
url = "123"
urd_add = {}
paused = False

@dp.message_handler(commands="start")
async def start(message: types.Message):
    start_buttons = ["Все товары(файл)", "Непросмотренные товары", "Старт автоматизации", "Стоп автоматизации"]
    keyboad = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboad.add(*start_buttons)
    hello = "Здравствуйте!\n" \
        "Этот бот разработан под Авито. Пожалуйста, настройте все критерии на сайте.\n" \
        "Для работы введите команду <b>/url</b> и укажите рядом ссылку.\n" \
        "Чтобы получить все товары по ссылке в формате Excel - нажмите на кнопку <b>'Все товары(файл)</b>'\n" \
        "Кнопка <b>'Старт автоматизации'</b> позволяет запустить автоматическое обновление товаров по ссылке, новые товары отправляются ботом в сообщении\n" \
        "Кнопка <b>'Стоп автоматизации'</b> останавливает автоматизацию. Чтобы запустить автоматизацию снова - нажмите 'Старт автоматизации'\n" \
        "Кнопка <b>'Непросмотренные товары'</b> позволяет получить те товары, которые были упущены во время остановки автоматизации с помощью кнопки 'Стоп автоматизации'\n" \
        "Если возникнут какие-то вопросы, затруднения - пишите мне в телеграмм или на почту: <u>rojofamily@yandex.ru</u>"
    await message.answer(hello, reply_markup=keyboad)
    if message.text:
        global id_
        id_ = message.from_user.id 
    print(id_)
    return id_

@dp.message_handler(commands=["url"])
async def url_(message: types.Message, ):
    for i in user_id:
        if str(id_) == i:
            global url
            global couner
            url = message.text
            if "https://www.avito.ru/" in url:
                url = url.replace("/url ", '')
                if "?" not in url:
                    url = url + "?p={page}"
                    urd_add
                    print(url)
                elif "?p" not in url:
                    url = url + "&p={page}"
                    print(url)
                else:
                    url = url.replace("p=", "p={page}&")
                    print(url)
                await message.answer("Ссылка успешно сохранена!")
                # couner += 1
                # if url in urd_add.values():
                #     print("Ссылка уже есть!")
                # else:
                #     urd_add[str(couner)] = url
                #     print(urd_add)
                #     await message.answer(f"Ссылка успешно сохранена! Номер ссылки: {couner}")
                #     return couner
            else: print("Ссылка не принята")
            return url
    
# @dp.message_handler(commands=["add_url"])
# async def add_url(message: types.Message):
#     g = couner + 1
#     urd_add[g] = url
#     print(urd_add)
#     return urd_add, couner

# @dp.message_handler(commands=["chk_url"])
# async def check_url(message: types.Message):
#     for k, v in urd_add.items():
#             key = k
#             value = v
#             await message.answer(key, value)

@dp.message_handler(Text(equals="Все товары(файл)"))
async def get_all(message: types.Message):
    for i in user_id:
        if str(id_) == i:
            await message.answer("Пожалуйста, подождите")
            get_pages(url)
            get_all_to_excel(url)
            to_excel()
            file = open('my_book.xlsx', 'rb')
            await bot.send_document(message.chat.id, file)

@dp.message_handler(Text(equals="Непросмотренные товары"))
async def get_news(message: types.Message):
    for i in user_id:
        if str(id_) == i:
            fresh_news = check_update(url)
            if len(fresh_news) >= 1:
                for k, v in sorted(fresh_news.items()):
                    news = f"{v['date_append']}\n" \
                        f"{v['title']}\n" \
                        f"{v['price']}\n" \
                        f"{v['url']}\n" \
                        f"{v['comment']}\n" \
                        f"{v['date']}\n"
                    await message.answer(news)
            else:
                await message.answer("Непросмотренных товаров нет")

@dp.message_handler(Text(equals="Стоп автоматизации"))
async def stop(message: types.Message):
    for i in user_id:
        if str(id_) == i:
            global paused
            paused = True
            await message.answer("Бот остановлен")
            return paused

@dp.message_handler(Text(equals="Старт автоматизации"))
async def message_every_minute(message: types.Message):
    for i in user_id:
        if str(id_) == i:
            await message.answer("Автоматизация начата")
            global paused
            paused = False
            while paused == False:
                        fresh_news = check_update(url)
                        if len(fresh_news) >= 1:
                            for k, v in sorted(fresh_news.items()):
                                news = f"{v['date_append']}\n" \
                                    f"{v['title']}\n" \
                                    f"{v['price']}\n" \
                                    f"{v['url']}\n" \
                                    f"{v['comment']}\n" \
                                    f"{v['date']}\n"
                                await message.answer(news)
                                
                        await asyncio.sleep(20)
            return paused
            

if __name__ == '__main__':
    # loop = asyncio.get_event_loop()
    # loop.create_task(message_every_minute())
    executor.start_polling(dp)
