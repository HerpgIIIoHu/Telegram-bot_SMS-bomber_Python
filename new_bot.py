from email import message
import logging, asyncio
import config
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from db import DataBase
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
import datetime, random
import bomb
from threading import Thread
from pyqiwip2p import QiwiP2P
from aiogram.utils.callback_data import CallbackData
API_TOKEN = config.API_TOKEN
logging.basicConfig(level=logging.INFO)
PayQiwi = QiwiP2P(auth_key=config.QIWI_TOKEN)
db = DataBase(config.DB)
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

#Время для разных функций
now = datetime.datetime.now()#Текущая дата
nows = ("{}.{}.{}  {}:{}".format(now.day, now.month, now.year, now.hour, now.minute))
date_for_db = ("{}-{}-{}  {}:{}".format(now.day, now.month, now.year, now.hour, now.minute+10))
date_for_bomb = ("{}-{}-{}-{}.{}".format(now.day, now.month, now.year, now.hour, now.minute-10))
update_date = ("{}-{}-{}-{}.{}".format(now.day, now.month, now.year, now.hour, now.minute))
####################################################################################async 

class Message_users(StatesGroup):
    summa_popolneniya = State()
    number_spam = State()


async def isNumber(_str):
    try:
        int(_str)
        return True
    except Exception as e:
        return False

async def num(phone):
    if ((phone[0:2] == "+7" and len(phone[1:]) == 11) or (phone[0:4] == '+380' and len(phone[4:]) == 12)):
        return True
    else:
        return False
    ############################################################
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if not db.user_exist(message.from_user.id):
        db.add_user(message.from_user.id)
        await message.answer(f'<strong>Приветствуем тебя у нас на портале</strong>\nТы успешно занесен в нашу базу!\nНажми /help чтобы перейти к основному меню', parse_mode="html")
    else:
        await message.answer("<strong>Нажмите</strong> <b>/help\n</b><i>Чтобы перейти к основному меню</i>", parse_mode="html")
        
@dp.message_handler(content_types=['contact'])
async def contact(message):
    if message.contact != None:
        db.set_userPhone(message.chat.id, message.contact.phone_number)

@dp.message_handler(content_types=["text"])
async def handle_text(message):
    
    if message.text.strip() == "/help":
        
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        
        Info_user = types.KeyboardButton("👤Личная информация")
        what_know_how = types.KeyboardButton("ℹ️Что я умею?")
        Spam = types.KeyboardButton("💣Запустить бомбер")
        markup.row(Info_user, Spam)
        markup.row(what_know_how)
        
        await message.answer('<b>Нажми: </b>', reply_markup=markup, parse_mode='html')
    
    elif message.text.strip() == '👤Личная информация' :
        
        markup2 = types.InlineKeyboardMarkup(row_width=2)
        item1 = types.InlineKeyboardButton("💵Пополнить баланс💵", callback_data="top_up")
        markup2.add(item1)
        answer = f"<b>Мой аккаунт</b>\n<i>Вся необходимая информация о вашем профиле\n\n</i><strong>Тебя зовут:</strong> {message.from_user.first_name}\n<strong>Твой ID:</strong> {message.from_user.id}\n<strong>Ваш логин:</strong> @{message.from_user.username}\n<strong>Баланс:</strong> {db.user_money(message.from_user.id)} руб."
        await message.answer(answer, parse_mode='html', reply_markup= markup2)
        
    
    elif message.text.strip() == "ℹ️Что я умею?":
        answer = "<strong>Пока что я сам не знаю(\nНо в скором времени здесь будет полная информация обо мне</strong>"
        await message.answer(answer, parse_mode='html')
    elif message.text.strip() == "💣Запустить бомбер":
        markup_s = types.InlineKeyboardMarkup(row_width=3)
        markup_s.add(types.InlineKeyboardButton("Начать бомбить", callback_data="bomb"))
        await message.answer("<i>Введите номер телефона жертвы:\nНачиная с </i><b>+7</b> <i>или</i> <b>+380</b><i>!!!</i>", parse_mode='html',reply_markup=markup_s)  
        
@dp.callback_query_handler(text = "top_up")
async def callback(call: types.CallbackQuery):
    # p = open("img.jpg", 'rb')#Добавляем фото и открываем его# Посылаем фото боту для отправки и подписываем его caption
    await bot.answer_callback_query(call.id, "Пополнение баланса от 10 рублей!", show_alert=True)#Уведомление пользователю
    await Message_users.summa_popolneniya.set()
    await call.message.answer("Введите сумму пополнения💰🤑:")
        
@dp.callback_query_handler(text = "top_ups")
async def callback(call: types.CallbackQuery):
    # p = open("img.jpg", 'rb')#Добавляем фото и открываем его# Посылаем фото боту для отправки и подписываем его caption
    await bot.answer_callback_query(call.id, "Пополнение баланса от 10 рублей!", show_alert=True)#Уведомление пользователю
    await Message_users.summa_popolneniya.set()
    await call.message.answer("Введите сумму пополнения💰🤑:")
        
@dp.callback_query_handler(text_contains = "check_")
async def callback(call: types.CallbackQuery):
    bill = call.data[6:]
    info = db.get_check(bill_id=bill)
    if info != False:
        try:
            if (PayQiwi.check(bill_id=bill).status) == "PAID":
                user_money = db.user_money(call.from_user.id)
                money = int(info[2])
                db.set_money(call.from_user.id, user_money+money)
                db.set_date(call.from_user.id, "Оплачен")
                date_check = "Оплачен"
                db.add_checks(call.from_user.id, money, nows, date_check)
                await call.message.answer("✅Счет успешно пополнен)👌")
                
            else:
                await call.message.answer("❌Счет не оплачен❌")
        except Exception as e:
            print(e)

    else:
        await call.answer("🤷‍♂️Счет не найден🤷‍♂️")
            
@dp.callback_query_handler(text = "bomb")
async def callback(call: types.CallbackQuery):
    await Message_users.number_spam.set()
    await call.message.answer("Вводи номер📲:")
        

@dp.message_handler(state=Message_users.number_spam)
async def process_message(message: types.Message, state: FSMContext):

    async with state.proxy() as data:
        data = message
    
    await state.finish()
    await doomb_number(data)


@dp.message_handler(state=Message_users.summa_popolneniya)
async def process_message(message: types.Message, state: FSMContext):

    async with state.proxy() as data:
        data = message
    await popolnenie_balansa(data)
    await state.finish()
    
async def doomb_number(message):
    await spam(message)
    
            
async def popolnenie_balansa(message):
    await bot_mess(message)
    

async def bot_mess(message):
    if await isNumber(message.text):
        message_money = int(message.text)#Образали строки начали идти с 0 элемента и забили на последний
        if message_money >= 10:
            date_check = "Не оплачен"
            comment = str(message.from_user.id) + "_" + str(random.randint(1000, 6000))
            bill = PayQiwi.bill(amount=message_money, lifetime = 10, comment = comment)
            db.add_check(message.from_user.id, message_money, bill.bill_id, nows, date_check)
            markup = types.InlineKeyboardMarkup(row_width=3)
            items = types.InlineKeyboardButton(text="⏳Оплатить⏳", url=bill.pay_url)
            items2 = types.InlineKeyboardButton(text="🧮Проверить оплату🧮", callback_data="check_"+bill.bill_id, )
            markup.add(items)
            markup.add(items2)
            await message.answer(f"💲Пополнение баланса на сумму {message_money} рублей💲:", reply_markup=markup)   
        else:
            await message.answer("⚠️Пополнение баланса от 10 рублей⚠️\n<i>Нажмите</i> <b>Пополнить баланс</b> <i>еще раз, чтобы ввести сумму пополнения заново</i>", parse_mode="html")
    
    else:
        await message.answer("Вводите только цифры!\n<i>Нажмите</i> <b>Пополнить баланс</b> <i>еще раз, чтобы ввести сумму пополнения заново</i>", parse_mode="html")

    
      
async def spam(message):
    try:
        if await num(message.text) != False:
            phone = message.text
            
            user_money = db.user_money(message.from_user.id)
            await message.answer("Номер введен корректно✅")
            if user_money >= 5:
                db.add_data_zapuska(update_date, message.chat.id)
                await message.answer("Бомбер запущен на 10 минут)")
                db.set_money(message.from_user.id, user_money-5)
                
                Thread(target=bomb.bomb, args=(phone,)).start()
            else:
                mar = types.InlineKeyboardMarkup()
                mar.add(types.InlineKeyboardButton("💳Пополнить баланс💳", callback_data="top_ups"))
                await message.answer("Недостаточно средств<b>\nОдин запуск стоит 5 рублей</>", reply_markup=mar, parse_mode="html")
            
        else:
            await message.answer("🚫Номер телефона введен не верно🚫\n<i>Нажмите</i> <b>Начать бомбить</b> <i>еще раз,чтобы прейти к вводу номера</i>", parse_mode="html")
    
    except Exception as e:
        print(e)
        
        
async def close_spam(phone):
    await message.answer(f"Спам номера <strong>{phone}</strong> закончен", parse_mode="html")
    
 
    
if __name__ == '__main__':
    
    executor.start_polling(dp)