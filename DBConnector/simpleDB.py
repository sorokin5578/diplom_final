import mysql.connector


def get_connection():
    try:
        db = mysql.connector.connect(
            host="localhost",
            port="3306",
            user="root",
            password="root",
            database="users_stocks"
        )
        return db
    except:
        return []


def add_new_user(user_id, user_name, stocks):
    try:
        db = get_connection()
        my_cursor = db.cursor()
        if len(stocks) == 1:
            my_cursor.execute("insert into user_info (id_user, name, 1_stock) "
                              "value (%s, %s ,%s)",
                              (user_id, user_name, stocks[0]))
        elif len(stocks) == 2:
            my_cursor.execute("insert into user_info (id_user, name, 1_stock, 2_stock) "
                              "value (%s, %s ,%s, %s)",
                              (user_id, user_name, stocks[0], stocks[1]))
        elif len(stocks) == 3:
            my_cursor.execute("insert into user_info (id_user, name, 1_stock, 2_stock, 3_stock) "
                              "value (%s, %s ,%s, %s, %s)",
                              (user_id, user_name, stocks[0], stocks[1], stocks[2]))
        elif len(stocks) == 4:
            my_cursor.execute("insert into user_info (id_user, name, 1_stock, 2_stock, 3_stock, 4_stock) "
                              "value (%s, %s ,%s, %s, %s, %s)",
                              (user_id, user_name, stocks[0], stocks[1], stocks[2], stocks[3]))
        elif len(stocks) == 5:
            my_cursor.execute("insert into user_info (id_user, name, 1_stock, 2_stock, 3_stock, 4_stock, 5_stock) "
                              "value (%s, %s ,%s, %s, %s, %s, %s)",
                              (user_id, user_name, stocks[0], stocks[1], stocks[2], stocks[3], stocks[4]))
        db.commit()
        return True
    except:
        return False
    finally:
        db.close()


def return_user(user_id):
    try:
        res = []
        db = get_connection()
        my_cursor = db.cursor()
        my_cursor.execute("select * from user_info where id_user=" +str(user_id))
        for x in my_cursor:
            for j in x:
                res.append(j)
        cnt=0
        for i in res[2:]:
            if i == None:
                cnt += 1
        for j in range(1, cnt + 1):
            res.remove(None)
        return res
    except:
        return []
    finally:
        db.close()


def del_user(user_id):
    try:
        db = get_connection()
        my_cursor = db.cursor()
        my_cursor.execute("delete from user_info where id_user=" +str(user_id))
        db.commit()
        return True
    except:
        return False
    finally:
        db.close()