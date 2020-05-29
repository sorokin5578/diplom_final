import requests
import re
import datetime
from random import choice
from timeit import default_timer as timer
from bs4 import BeautifulSoup as BS


def return_new_page_ffin(num_page):
    try:
        return requests.get("https://ffin.ru/market/directory/data/?PAGEN_1=" + str(num_page))
    except:
        return []


def get_finviz_page(ticker):
    r = ""
    cnt = 0
    while not (str(r) == '<Response [200]>') or cnt>30:
        try:
            cnt += 1
            prox = get_proxies()
            user = get_user_agent()
            r=requests.get("https://finviz.com/quote.ashx?t=" + ticker, headers=user, proxies=prox)
        except Exception as e:
            print(e.__class__)
            continue
    return r


def get_link_stock(find_string):
    dict_stock = {}
    try:
        len_str = len(find_string)
        for i in range(1, 29):
            r = return_new_page_ffin(i)
            html = BS(r.content, 'html.parser')
            el = html.select("table.directory-list_table")
            ticker = el[0].select("td", text=True)
            count_tic = 2
            for a_tag in el[0].select("a", href=True):
                if not (re.search(r'([A-Za-z0-9_\&\.\,\'\(\)])',
                                  a_tag.text[0])) or "ETF" in a_tag.text:  # a_tag.text[0] or a_tag.text
                    continue
                if len(find_string) == 0:
                    break
                for str_key in find_string:
                    tic = ticker[count_tic].text.replace(u'\n', u'').replace(u' ', u'')
                    if str_key.lower() == a_tag.text.lower() or str_key.lower() == tic.lower():
                        dict_stock.update({str_key: ["https://ffin.ru" + a_tag.get("href"), a_tag.text, tic]})
                        find_string.remove(str_key)
                        continue
                count_tic += 9
            if len(dict_stock) == len_str:
                break
    except:
        get_info_stock("")
    return dict_stock


def get_info_stock(link):
    dict_news = {}
    dict_stock = {}
    try:
        r = requests.get(link)
        html = BS(r.content, 'html.parser')
        el = html.select("table.td-last-right")
        try:
            ticker = html.select_one("h1", class_="quotes-company_title").text.replace(u'\n', u'').replace(u' ', u'')
        except:
            ticker = ""
        try:
            grow_index = el[0].select_one("td.lastTradeChange").text.replace(u'\n', u'').replace(u' ', u'')
            grow = "down"
            if not ("-" in grow_index):
                grow = "up"
        except:
            grow, grow_index = "Неизвестно", ""

        try:
            dict_stock.update({"Последняя сделка": el[0].select_one("td.lastTradePrice").text.replace(u'\n', u'')})
        except:
            dict_stock.update({"Последняя сделка": "Неизвестно"})

        dict_stock.update({"Изменение": [grow, grow_index]})

        try:
            dict_stock.update({"Дата торгов": el[0].select_one("td.lastTradeDate").text.replace(u'\n', u'')})
        except:
            dict_stock.update({"Дата торгов": "Неизвестно"})

        try:
            dict_stock.update({"Потенциал роста": el[0].select_one("td.lastTradePotential").text.replace(u'\n', u'')})
        except:
            dict_stock.update({"Потенциал роста": "Неизвестно"})

        try:
            dict_stock.update({"Рекомендации": el[0].find_all("span", text=True)[0].text})
        except:
            dict_stock.update({"Рекомендации": "Неизвестно"})
        finviz_page = get_finviz_page(ticker[ticker.find("(") + 1:len(ticker) - 1])
        dict_news_finviz = get_news_finviz(finviz_page)
        dict_news.update(dict_news_finviz)
    except:
        return []
    return [dict_stock, dict_news]


def get_news_finviz(r):
    dict_news = {}
    try:
        html = BS(r.content, 'html.parser')
        el = html.select("table.fullview-news-outer")

        for news in el[0].select("tr"):
            news_time = news.next.text
            if re.search(r'[A-Z]', news_time[0]):
                if delta_time_for_finviz_date(news_time):
                    title=news.text.replace(u'\xa0\xa0', u' ').replace(u'\xa0', u' ')
                    link=news.select_one("a",href=True).get("href")
                    dict_news.update({title: link})
                else:
                    break
            else:
                title=news.text.replace(u'\xa0\xa0', u' ').replace(u'\xa0', u' ')
                link=news.select_one("a",href=True).get("href")
                dict_news.update({title: link})
    except:
        return {}
    return dict_news


def delta_time_for_finviz_date(then):
    now = datetime.datetime.today().strftime("%b-%d-%y %H:%M")
    if int(now[7:9]) - int(then[7:9]) == 0:
        if now[0:3] == then[0:3]:
            if int(now[4:6]) - int(then[4:6]) < 1:
                return True
    return False


def get_user_agent():
    try:
        user_agent = open("C:\\Users\\Illia\\PycharmProjects\\diplom_2\\utils\\useragents.txt").read().split('\n')
        return {'User-Agent': choice(user_agent)}
    except:
        return {}


def get_proxies():
    try:
        proxy = open("C:\\Users\\Illia\\PycharmProjects\\diplom_2\\utils\\proxies.txt").read().split('\n')
        return {'http': 'http://' + choice(proxy)}
    except:
        return {}


def make_all(find_str):
    d = get_link_stock(find_str)
    info = []
    for key in d:
        info.append(get_info_stock(d.get(key)[0]))
    return [d, info]
