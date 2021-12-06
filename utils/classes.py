class User:
    def __init__(self, user_id, user_name, type_name, type_count, stocks):
        self.user_id = user_id
        self.user_name = user_name
        self.type_name = type_name
        self.type_count = type_count
        self.stocks = stocks

    def __str__(self):
        return "User: {}, {}, {}, {}, [{}]".format(self.user_id, self.user_name, self.type_name, self.type_count,
                                                   ", ".join([str(x) for x in self.stocks]))


class Stock:
    def __init__(self, ticker, name):
        self.ticker = ticker
        self.name = name

    def __str__(self):
        return "Stock: {}, {}".format(self.ticker, self.name)

    def __eq__(self, other):
        if isinstance(other, Stock):
            return self.ticker == other.ticker
        return NotImplemented


class Type:
    def __init__(self, type_name, count):
        self.type_name = type_name
        self.count = count

    def __str__(self):
        return "{} - {}шт".format(self.type_name, self.count)
