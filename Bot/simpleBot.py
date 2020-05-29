import telebot
from utils.Config import TOKEN
from DBConnector.simpleDB import add_new_user, return_user, del_user
from ParsingFFIN.simpleParsingFFIN import make_all
from My_CNN_network.simpleCNN import call_network

bot = telebot.TeleBot(TOKEN)
res = {}


@bot.message_handler(commands=['start'])
def help_command(massage):
    user_from_db = return_user(massage.chat.id)
    if not user_from_db:
        res.update({massage.chat.id: []})
        bot.send_message(massage.chat.id, "Введите название или тикер акций (до 5  штук), затем нажмите /done"
                                          "\nОзнакомиться с название компаний или их тикерами можно здесь👇")
        bot.send_message(massage.chat.id, "https://ffin.ru/market/directory/data/")
    else:
        res.update({user_from_db[0]: user_from_db[2:]})
        bot.send_message(massage.chat.id, "Здравствуйте, <b>{0.first_name}</b>."
                                          "\nВы уже общались с ботом, чтобы посмотреть свой портфель нажмите /my_bag."
                                          "\nЧтобы получить последние новости нажмите /info."
                                          "\nЧтобы изменить свой портфель нажмите /change.".format(massage.from_user),
                         parse_mode='html')


@bot.message_handler(commands=['help'])
def help_command(massage):
    bot.send_message(massage.chat.id, "Введите название или тикер акций (до 5  штук), затем нажмите /done"
                                      "\nОзнакомиться с название компаний или их тикерами можно здесь👇")
    bot.send_message(massage.chat.id, "https://ffin.ru/market/directory/data/")


@bot.message_handler(commands=['done'])
def set_of_stock(massage):
    try:
        r = ", ".join(res.get(massage.chat.id))
        bot.send_message(massage.chat.id,
                         "Ваш портфель акций: {0}.\nНажмите /info, чтобы начать получать новости о них!"
                         "\nИли /repeat, чтобы повторить ввод.".format(r))
    except:
        bot.send_message(massage.chat.id, "Упс, что-то пошло не так😢")


@bot.message_handler(commands=['repeat'])
def repeat_command(massage):
    res.update({massage.chat.id: []})
    bot.send_message(massage.chat.id, "Введите название или тикер акций (до 5  штук), затем нажмите /done")


@bot.message_handler(commands=['info'])
def get_info(massage):
    try:
        user_from_db = return_user(massage.chat.id)
        if not user_from_db:
            add_new_user(massage.from_user.id, massage.from_user.first_name, res.get(massage.chat.id))
        else:
            res.update({user_from_db[0]: user_from_db[2:]})
        bot.send_message(massage.chat.id, "Пожалуйста, подождите немного, я ищу 🔎")
        new_res=res.get(massage.chat.id)
        if new_res:
            length = len(res.get(massage.chat.id))
            arr = make_all(res.get(massage.chat.id))
            send_info(arr, length, massage.chat.id)
        else:
            bot.send_message(massage.chat.id, "Упс, что-то пошло не так😢\nНажмите /start для начала работы.")
    except:
        bot.send_message(massage.chat.id, "Упс, что-то пошло не так😢\nНажмите /start для начала работы.")


@bot.message_handler(commands=['my_bag'])
def get_bag(massage):
    try:
        user_from_db = return_user(massage.chat.id)
        if not user_from_db:
            bot.send_message(massage.chat.id, "{0.first_name}, вы ещё не задали свой портфель."
                                              "\nВведите название или тикер акций (до 5  штук), "
                                              "затем нажмите /done".format(massage.from_user))
        else:
            r = ", ".join(user_from_db[2:])
            bot.send_message(massage.chat.id,
                             "Ваш портфель акций: {0}.\nНажмите /info, чтобы начать получать новости о них!".format(r))
    except:
        bot.send_message(massage.chat.id, "Упс, что-то пошло не так😢")


@bot.message_handler(commands=['change'])
def change_bag(massage):
    try:
        user_from_db = return_user(massage.chat.id)
        if not user_from_db:
            bot.send_message(massage.chat.id, "{0.first_name}, вы ещё не задали свой портфель."
                                              "\nВведите название или тикер акций (до 5  штук), "
                                              "затем нажмите /done".format(massage.from_user))
        else:
            del_user(massage.chat.id)
            bot.send_message(massage.chat.id, "{0.first_name}, ваш портфель акций был удален."
                                              "\nВведите название или тикер акций (до 5  штук), "
                                              "затем нажмите /done".format(massage.from_user))
            res.update({massage.chat.id: []})
    except:
        bot.send_message(massage.chat.id, "Упс, что-то пошло не так😢")


@bot.message_handler(func=lambda message: True, content_types=['text'])
def listen_msg(massage):
    user_from_db = return_user(massage.chat.id)
    if not user_from_db:
        try:
            if len(res.get(massage.chat.id)) < 4:
                res.get(massage.chat.id).append(massage.text)
                bot.send_message(massage.chat.id,
                                 "Вы вели {0}, введите ещё название или нажмите /done".format(massage.text))
            elif len(res.get(massage.chat.id)) == 4:
                res.get(massage.chat.id).append(massage.text)
                r = ", ".join(res.get(massage.chat.id))
                bot.send_message(massage.chat.id,
                                 "Ваш портфель акций: {0}.\nНажмите /info, чтобы начать получать новости о них!"
                                 "\nИли /repeat, чтобы повторить ввод.".format(r))
            else:
                r = ", ".join(res.get(massage.chat.id))
                bot.send_message(massage.chat.id,
                                 "Ваш портфель акций: {0}.\nНажмите /info, чтобы начать получать новости о них!"
                                 "\nИли /repeat, чтобы повторить ввод.".format(r))
        except:
            bot.send_message(massage.chat.id, "Упс, {0.first_name},что-то пошло не так😢".format(massage.from_user))
    else:
        bot.send_message(massage.chat.id, "Чтобы посмотреть свой портфель нажмите /my_bag."
                                          "\nЧтобы получить последние новости нажмите /info."
                                          "\nЧтобы изменить свой портфель нажмите /change.")


def send_info(arr, length, chat_id):
    cnt = 0
    info_stock = []
    for key in arr[0]:
        info_stock.clear()
        info_stock.append("<b>🏦 Компания:</b> " + arr[0].get(key)[1])
        info_stock.append("Тикер: " + arr[0].get(key)[2])
        info_stock.append("Ссылка: " + arr[0].get(key)[0])
        el = arr[1][cnt]
        if el:
            if el[0]:
                for item1 in el[0]:
                    if item1 == "Изменение":
                        if el[0].get(item1)[0] == "up":
                            info_stock.append(item1 + ": " + el[0].get(item1)[0] + "📈 " + el[0].get(item1)[1])
                        else:
                            info_stock.append(item1 + ": " + el[0].get(item1)[0] + "📉 " + el[0].get(item1)[1])
                        continue
                    info_stock.append(item1 + ": " + el[0].get(item1))
            if el[1]:
                info_stock.append("📰 Новости: ")
                for item2 in el[1]:
                    forecast_num = call_network([item2])
                    if forecast_num[0][0] >= 0.5:
                        info_stock.append("Прогноз: позитивный ✅")
                    else:
                        info_stock.append("Прогноз: негативный ❌")
                    info_stock.append("🗞 " + item2 + " " + el[1].get(item2))
            else:
                info_stock.append("😢 Новостей пока нет ")
        inf = "\n".join(info_stock)
        bot.send_message(chat_id, inf, parse_mode='html')
        cnt += 1
    if length != len(arr[0]):
        bot.send_message(chat_id, "😢 Бот не смог найти все компании, которые вы ввели (проверьте название или тикер)")


bot.polling(none_stop=True)
