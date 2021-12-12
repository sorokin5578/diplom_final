import mysql.connector

from stocker.stocker import Stocker
from utils.classes import *


def get_connection():
    try:
        db = mysql.connector.connect(
            host="localhost",
            port="3306",
            user="root",
            password="root",
            database="maters_diploma"
        )
        return db
    except:
        return None


def add_new_stocks(stock):
    try:
        db = get_connection()
        my_cursor = db.cursor()
        my_cursor.execute("insert into stocks (ticker, name) value (%s, %s)", (stock.ticker, stock.name))
        db.commit()
        return True
    except Exception as e:
        if e.args[0] == 1062:
            return True
        print(e)
        return False
    finally:
        db.close()


def add_stock_for_user(user_id, stock):
    try:
        db = get_connection()
        my_cursor = db.cursor()
        my_cursor.execute("insert into users_stocks (user_id, ticker) value (%s, %s)", (user_id, stock.ticker))
        db.commit()
        return True
    except Exception as e:
        print(e)
        return False
    finally:
        db.close()


def add_new_user(user_id, user_name, stocks=[]):
    try:
        db = get_connection()
        my_cursor = db.cursor()
        my_cursor.execute("insert into users (user_id, user_name) "
                          "value (%s, %s)", (user_id, user_name))
        for stock in stocks:
            my_cursor.execute("insert into users_stocks (user_id, ticker) value (%s, %s)", (user_id, stock.ticker))
        db.commit()
        return get_user(user_id)
    except Exception as e:
        print(e)
    finally:
        db.close()
    return None


def get_stocks_by_user_id(user_id):
    try:
        db = get_connection()
        my_cursor = db.cursor(prepared=True)
        my_cursor.execute(
            "select s.ticker, s.name from users_stocks as us left join stocks as s on s.ticker=us.ticker where us.user_id=%s ",
            [str(user_id)])
        stocks = []
        for x in my_cursor:
            stocks.append(Stock(x[0].upper(), x[1]))
        return stocks
    except Exception as e:
        print(e)
        pass
    finally:
        db.close()
    return []


def get_types(count):
    try:
        db = get_connection()
        my_cursor = db.cursor(prepared=True)
        my_cursor.execute(
            "select type_name, count  from user_type where count>%s ", [str(count)])
        types = []
        for x in my_cursor:
            types.append(Type(x[0], x[1]))
        return types
    except Exception as e:
        print(e)
        pass
    finally:
        db.close()
    return []


def get_user(user_id):
    try:
        db = get_connection()
        my_cursor = db.cursor(prepared=True)
        my_cursor.execute(
            "select u.user_id, u.user_name, ut.type_name, ut.count from users as u left join user_type as ut on ut.type_name=u.type_name where user_id=%s",
            [str(user_id)])
        stocks = get_stocks_by_user_id(user_id)
        for x in my_cursor:
            user = User(x[0], x[1], x[2], x[3], stocks)
            return user
    except Exception as e:
        print(e)
        pass
    finally:
        db.close()
    return None


def edit_user_type(user_id, type_name):
    try:
        db = get_connection()
        my_cursor = db.cursor()
        my_cursor.execute(
            "update users set type_name=%s where user_id=%s",
            (type_name, user_id))
        db.commit()
        return True
    except Exception as e:
        print(e)
        pass
    finally:
        db.close()
    return False


def del_user(user_id):
    try:
        db = get_connection()
        my_cursor = db.cursor(prepared=True)
        my_cursor.execute("delete from users where user_id=%s", [str(user_id)])
        db.commit()
        return True
    except:
        return False
    finally:
        db.close()


def del_stocks_by_user_id(user_id):
    try:
        db = get_connection()
        my_cursor = db.cursor(prepared=True)
        my_cursor.execute("delete from users_stocks where user_id=%s", [str(user_id)])
        db.commit()
        return True
    except:
        return False
    finally:
        db.close()


def get_max_type_count():
    try:
        db = get_connection()
        my_cursor = db.cursor()
        my_cursor.execute("select max(count) from user_type")
        for x in my_cursor:
            return x[0]
    except Exception as e:
        print(e)
        pass
    finally:
        db.close()
    return None



# microsoft = Stocker('GOOGL')
# # # microsoft.predict_future(start_date='2021-12-10', end_date='2022-02-01')
# res = microsoft.predict_future(days=10)
# print(res[0])
# print("="*10)
# print(res[1])
# # # print('{:.2f}'.format(None))