import telebot
from telebot import types
import yfinance as yf
from stocker.stocker import Stocker
from DBConnector.simpleDB import *
from My_CNN_network.simpleCNN import call_network
from utils.Config import TOKEN

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def help_command(massage):
    user_from_db = get_user(massage.chat.id)
    if not user_from_db:
        user_from_db = add_new_user(massage.chat.id, massage.from_user.first_name)
        bot.send_message(massage.chat.id,
                         "Здравствуйте, <b>{0.first_name}</b>."
                         "\nВведите тикер акций (до {1}  штук) через запятую, затем нажмите /done"
                         "\nОзнакомиться с тикерами можно здесь👇".format(
                             massage.from_user, user_from_db.type_count), parse_mode='html')
        bot.send_message(massage.chat.id, "https://finance.yahoo.com")
    else:
        bot.send_message(massage.chat.id, "Здравствуйте, <b>{0.first_name}</b>."
                                          "\nВы уже общались с ботом, чтобы посмотреть свой портфель нажмите /my_bag."
                                          "\nЧтобы получить последние новости нажмите /info."
                                          "\nЧтобы изменить свой портфель нажмите /change.".format(massage.from_user),
                         parse_mode='html')


@bot.message_handler(commands=['help'])
def help_command(massage):
    user_from_db = get_user(massage.chat.id)
    bot.send_message(massage.chat.id, "Введите тикеры акций (до {}  штук) через запятую, затем нажмите /done"
                                      "\nОзнакомиться с тикерами можно здесь👇".format(
        user_from_db.type_count - len(user_from_db.stocks)))
    bot.send_message(massage.chat.id, "https://finance.yahoo.com")


@bot.message_handler(commands=['done'])
def set_of_stock(massage):
    try:
        user_from_db = get_user(massage.chat.id)
        if user_from_db.stocks:
            r = ", ".join([stock.name for stock in user_from_db.stocks])
            bot.send_message(massage.chat.id,
                             "Ваш портфель акций: {0}.\nНажмите /info, чтобы начать получать информацию о них!"
                             "\nИли /change, чтобы повторить ввод.".format(r))
        else:
            bot.send_message(massage.chat.id, "{0.first_name}, вы ещё не задали свой портфель."
                                              "\nВведите тикеры акций (до {1}  штук) через запятую, "
                                              "затем нажмите /done".format(massage.from_user, user_from_db.type_count))
    except:
        bot.send_message(massage.chat.id, "Упс, что-то пошло не так😢")


@bot.message_handler(commands=['info'])
def get_info(massage):
    try:
        user_from_db = get_user(massage.chat.id)
        if user_from_db.stocks:
            bot.send_message(massage.chat.id, "Пожалуйста, подождите немного, я ищу 🔎")
            send_info(user_from_db.stocks, user_from_db.user_id)
        else:
            bot.send_message(massage.chat.id, "{0.first_name}, вы ещё не задали свой портфель."
                                              "\nВведите тикеры акций (до {1}  штук) через запятую, "
                                              "затем нажмите /done".format(massage.from_user, user_from_db.type_count))
    except:
        bot.send_message(massage.chat.id, "Упс, что-то пошло не так😢")


@bot.message_handler(commands=['role'])
def get_info(massage):
    try:
        user_from_db = get_user(massage.chat.id)
        max_count = get_max_type_count()
        if max_count == user_from_db.type_count:
            bot.send_message(massage.chat.id,
                             "Поздравляю, у вас наилучший тип пользователя - {}.".format(user_from_db.type_name))
        else:
            keyboard = types.InlineKeyboardMarkup(row_width=2)
            types_of_user = get_types(user_from_db.type_count)
            for type_of_user in types_of_user:
                keyboard.add(types.InlineKeyboardButton(str(type_of_user), callback_data=str(type_of_user.type_name)))
            msg = "Ваш тип пользователя {}. Вы можете улучшить его!"
            bot.send_message(massage.chat.id, msg.format(user_from_db.type_name), reply_markup=keyboard)
    except Exception as e:
        print(e)
        bot.send_message(massage.chat.id, "Упс, что-то пошло не так😢")


@bot.message_handler(commands=['info_by_ticker'])
def get_info(massage):
    try:
        user_from_db = get_user(massage.chat.id)
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        for stock in user_from_db.stocks:
            keyboard.add(
                types.InlineKeyboardButton(stock.ticker, callback_data='info ' + stock.ticker))
        msg = "Выберите тикер для которого вы хотите поучить информацию:"
        bot.send_message(massage.chat.id, msg.format(user_from_db.type_name), reply_markup=keyboard)
    except Exception as e:
        print(e)
        bot.send_message(massage.chat.id, "Упс, что-то пошло не так😢")


@bot.message_handler(commands=['predict_for_60'])
def get_info(massage):
    try:
        user_from_db = get_user(massage.chat.id)
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        for stock in user_from_db.stocks:
            keyboard.add(
                types.InlineKeyboardButton(stock.ticker, callback_data='predict ' + stock.ticker))
        msg = "Выберите тикер для которого вы хотите поучить прогноз на 60 дней:"
        bot.send_message(massage.chat.id, msg.format(user_from_db.type_name), reply_markup=keyboard)
    except Exception as e:
        print(e)
        bot.send_message(massage.chat.id, "Упс, что-то пошло не так😢")


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        key = call.data.split(' ')
        if key[0] == 'user' or key[0] == 'super':
            edit_user_type(call.message.chat.id, call.data)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="Поздравляю, ваш тип пользователя успешно изменен на {}".format(call.data),
                                  reply_markup=None)
        elif key[0] == 'info':
            bot.send_message(call.message.chat.id, "Пожалуйста, подождите немного, я ищу 🔎")
            send_info([Stock(key[1], None)], call.message.chat.id)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="Получить информацию об акции по тикеру - /info_by_ticker",
                                  reply_markup=None)
        else:
            bot.send_message(call.message.chat.id, "Пожалуйста, подождите немного, я считаю 🔎")
            stocker = Stocker(key[1])
            img = open(stocker.predict_future(days=60)[1], 'rb')
            bot.send_message(call.message.chat.id, "Предсказание цены акции {} на ближайшие 60 дней".format(key[1]))
            bot.send_photo(chat_id=call.message.chat.id, photo=img)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="Получить прогноз цены на 60 дней - /predict_for_60",
                                  reply_markup=None)

    except Exception as e:
        print(e)
        bot.send_message(call.message.chat.id, "Упс, что-то пошло не так😢")
        pass


@bot.message_handler(commands=['my_bag'])
def get_bag(massage):
    try:
        user_from_db = get_user(massage.chat.id)
        if not user_from_db.stocks:
            bot.send_message(massage.chat.id, "{0.first_name}, вы ещё не задали свой портфель."
                                              "\nВведите тикеры акций (до {1}  штук) через запятую, "
                                              "затем нажмите /done".format(massage.from_user, user_from_db.type_count))
        else:
            r = ", ".join([stock.name for stock in user_from_db.stocks])
            bot.send_message(massage.chat.id,
                             "Ваш портфель акций: {0}.\nНажмите /info, чтобы начать получать новости о них!".format(r))
    except:
        bot.send_message(massage.chat.id, "Упс, что-то пошло не так😢")


@bot.message_handler(commands=['change'])
def change_bag(massage):
    try:
        user_from_db = get_user(massage.chat.id)
        del_stocks_by_user_id(user_from_db.user_id)
        bot.send_message(massage.chat.id, "{0.first_name}, ваш портфель акций был удален."
                                          "\nВведите тикеры акций (до {1}  штук) через запятую, "
                                          "затем нажмите /done".format(massage.from_user, user_from_db.type_count))
    except:
        bot.send_message(massage.chat.id, "Упс, что-то пошло не так😢")


@bot.message_handler(func=lambda message: True, content_types=['text'])
def listen_msg(massage):
    user_from_db = get_user(massage.chat.id)
    max_count_for_current_role = user_from_db.type_count
    current_count = len(user_from_db.stocks)
    try:
        stocks = set([i.strip() for i in str(massage.text).upper().split(",")])
        common_stock = get_common_stock(stocks, user_from_db.stocks)
        if common_stock:
            bot.send_message(massage.chat.id, "{0.first_name}, ваш портфель акций уже содерджит тикер - {1}."
                                              "\nВведите тикеры акций (до {2}  штук) через запятую, "
                                              "затем нажмите /done".format(massage.from_user, common_stock,
                                                                           max_count_for_current_role - current_count))
            return

        if len(stocks) > max_count_for_current_role - current_count:
            additional_string = ''
            if max_count_for_current_role < get_max_type_count():
                additional_string = "\nДля доступа к большему количеству акций вы можете улучшить свой тариф - /role" \
                                    "\nВаш текущий тариф: {}".format(user_from_db.type_name)
            bot.send_message(massage.chat.id, "{0.first_name}, вы пытаетесь добавить слишком много тикеров."
                                              "\nДоступное количество акций для добавления: {1} шт.{2}"
                                              "\nНажмите /info, чтобы начать получать информацию о них!"
                                              "\nИли /change, чтобы повторить ввод.".format(massage.from_user,
                                                                                            max_count_for_current_role - current_count,
                                                                                            additional_string))
            return

        stocks_for_saving = []
        stocks_with_err = []
        tickers = yf.Tickers(" ".join(stocks))
        for stock in stocks:
            st_from_yahoo = tickers.tickers.get(stock)
            if st_from_yahoo and st_from_yahoo.get_info() and st_from_yahoo.get_info().get("symbol"):
                ticker = st_from_yahoo.get_info().get("symbol")
                name = ticker
                if st_from_yahoo.get_info().get("shortName"):
                    name = st_from_yahoo.get_info().get("shortName")
                elif st_from_yahoo.get_info().get("longName"):
                    name = st_from_yahoo.get_info().get("longName")
                stock_obj = Stock(ticker, name)
                is_saved = add_new_stocks(stock_obj)
                if is_saved:
                    stocks_for_saving.append(stock_obj)
                else:
                    stocks_with_err.append(stock_obj)
            else:
                stocks_with_err.append(Stock(stock, stock))

        res_stocks = []
        for stock in stocks_for_saving:
            if add_stock_for_user(user_from_db.user_id, stock):
                res_stocks.append(stock)
            else:
                stocks_with_err.append(stock)

        if res_stocks:
            bot.send_message(massage.chat.id,
                             "Бот сохранил для вас {0}, нажмите /done".format(
                                 ", ".join([i.ticker for i in res_stocks])))

        if stocks_with_err:
            bot.send_message(massage.chat.id,
                             "Бот не смог сохранить для вас {0}, пожалуйста, проверьте тикеры и попробуйте ещё раз."
                             .format(", ".join([i.ticker for i in stocks_with_err])))
    except Exception as e:
        print(e)
        bot.send_message(massage.chat.id, "Упс, {0.first_name},что-то пошло не так😢".format(massage.from_user))


def send_info(stocks, user_id):
    tickers = yf.Tickers(" ".join([stock.ticker for stock in stocks]))
    for stock in stocks:
        try:
            info_stock = []
            ticker = tickers.tickers.get(stock.ticker)
            ticker_info = ticker.get_info()
            ticker_news = ticker.get_news()
            ticker_recommendation = None
            stocker = Stocker(stock.ticker)
            estimate_price = stocker.predict_future(days=3)[0]['estimate'].to_numpy()[0]
            try:
                ticker_recommendation = ticker.get_recommendations(as_dict=True)
            except AttributeError as e:
                pass
            info_stock.append("<b>🏦 Компания:</b> " + str(ticker_info.get("shortName") or "-"))
            info_stock.append("Тикер: " + stock.ticker)
            info_stock.append("Ссылка: " + "https://finance.yahoo.com/quote/".format(stock.ticker))
            info_stock.append(
                "Последняя сделка: " + str(
                    ticker_info.get("currentPrice") or ticker_info.get("regularMarketPrice") or "-"))
            info_stock.append("Рекомендация от Яху Финанс: " + get_last_recommendation(ticker_recommendation))
            info_stock.append("Прогноз на завтра: " + price_to_str(estimate_price))
            if ticker_news:
                info_stock.append("📰 Новости: ")
                for news in ticker_news[:5]:
                    forecast_num = call_network([news.get("title")])
                    if forecast_num[0][0] >= 0.4:
                        info_stock.append("Прогноз: позитивный ✅")
                    else:
                        info_stock.append("Прогноз: негативный ❌")
                    info_stock.append("🗞 " + news.get("title") + " " + news.get("link"))
            else:
                info_stock.append("😢 Новостей пока нет ")
            bot.send_message(user_id, "\n".join(info_stock), parse_mode='html')
        except Exception as e:
            print(repr(e))
            bot.send_message(user_id, "Упс, не удалось найти {}😢".format(stock.ticker))


def get_common_stock(stocks, stocks_from_bd):
    for st in stocks:
        if stocks_from_bd.__contains__(Stock(st, None)):
            return st
    return None


def get_last_recommendation(recommendations):
    if recommendations:
        for recommendation in recommendations.items():
            if recommendation[0] == 'To Grade':
                last_date = max(recommendation[1].keys())
                return recommendation[1].get(last_date)
    return "-"


def price_to_str(price):
    try:
        return '{:.2f}'.format(price)
    except Exception as e:
        return "-"


bot.polling(none_stop=True)
