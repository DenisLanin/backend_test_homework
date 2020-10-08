import datetime as dt


class Record:
    """ Принимает данные, переводит время в нужный формат, добавляет текущее время, если date не указан."""
    date_format = '%d.%m.%Y'

    def __init__(self, amount, comment, date=dt.date.today()):
        self.amount = amount
        self.comment = comment
        if isinstance(date, dt.date):
            self.date = date
        else:
            self.date = dt.datetime.strptime(date, self.date_format).date()


class Calculator:
    """Принемает дневной лимит. Заполняет список self.record данными из класса Record. рассчитывает """

    def __init__(self, limit):
        self.limit = limit
        self.records = []

    # Создает таблицу.
    def add_record(self, record):
        self.records.append(record)

    def get_stats(self, amount_day):
        result = 0
        today = dt.date.today()
        day_delta = today - dt.timedelta(days=amount_day)
        for Record in self.records:
            if day_delta < Record.date <= today:
                result += Record.amount
        return result

    # Статистика за сегодня.
    def get_today_stats(self):
        return self.get_stats(1)

    # Статистика за неделю.
    def get_week_stats(self):
        return self.get_stats(7)


class CashCalculator(Calculator):
    """Определяет валюту, возвращает денежный остаток."""
    RUB_RATE = 1.0
    USD_RATE = 78.23
    EURO_RATE = 92.03

    def get_today_cash_remained(self, currency):
        spent = self.get_today_stats()
        remained = self.limit - spent
        switch_currency = {
            'rub': (self.RUB_RATE, "руб"),
            'usd': (self.USD_RATE, "USD"),
            'eur': (self.EURO_RATE, "Euro")
        }
        if remained == 0:
            return f"Денег нет, держись"
        elif remained < 0:
            return f'Денег нет, держись: твой долг {round(remained, 2)} {switch_currency[currency][1]}'
        else:
            return f'На сегодня осталось {round(remained, 2)} {switch_currency[currency][1]}'


class CaloriesCalculator(Calculator):
    """Рассчитывает остаток и возвращает его."""
    def get_calories_remained(self):
        spent = self.get_today_stats()
        remained = self.limit - spent
        if remained > 0:
            return f'Сегодня можно съесть что-нибудь ещё, но с общей калорийностью не более {remained} кКал'
        else:
            return f'Хватит есть!'


if __name__ == "__main__":
    cash_calculator = CashCalculator(1000)
    cash_calculator.add_record(Record(amount=145, comment="кофе"))
    cash_calculator.add_record(Record(amount=300, comment="Серёге за обед"))
    cash_calculator.add_record(Record(amount=3000, comment="бар в Танин др", date="08.11.2019"))
    print(cash_calculator.get_today_cash_remained('rub'))
