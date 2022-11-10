
from main.static.components.data import MONTHS


class BaseReport:
    def set_year(_self, year: int):
        _self.year = year

    def set_month(_self, month: int):
        _self.month = month
        _self.set_month_name()

    def set_month_name(_self):
        _self.month_name = MONTHS[_self.month]

    def set_week(_self, week: int):
        _self.week = week
    