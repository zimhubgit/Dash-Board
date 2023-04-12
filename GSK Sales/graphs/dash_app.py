from datetime import datetime

import pandas as pnd
from dash import html


class PeriodsDates:

    @staticmethod
    def get_weeks_ends(end_date: pnd.Timestamp) -> dict[str, pnd.Timestamp]:
        start_date = datetime(year=end_date.year, month=1, day=1, hour=16)
        year_weeks_dates: pnd.DatetimeIndex = pnd.date_range(start_date, end_date, freq='W-THU')
        weeks_dict: [str, pnd.Timestamp] = {}
        month = 1
        week_number = 1
        for week in year_weeks_dates:
            if week.month != month:
                month = week.month
                week_number = 1
            week.strftime('%B')
            key: str = f"{week.strftime('%B')} - W{week_number} (au {week.day}/{week.month})"
            week_number = week_number + 1
            weeks_dict.update({key: week})
        return weeks_dict


class Naming:
    children_num = 'NUMBER OF CHILDREN'
    disposition = 'DISPOSITION'
    orientation = 'ORIENTATION'


class DashScreen:
    def __int__(self, name: str, div: html.Div):
        self.name: str = name
        self.Div: html.Div = div
