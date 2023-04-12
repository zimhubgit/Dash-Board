import re

import pandas as pnd


class Utilities:
    QUARTER = 'Quarter'
    SEMESTER = 'Semester'
    MONTH = 'Month'
    MTD = 'MTD'
    WEEK = 'WEEK'
    ALL_PERIODS = 'All'
    YEAR = 'Year'
    DAY = 'Day'

    def __init__(self, var_col_name: str = 'COLUMNS', val_col_name: str = 'VALUES'):
        self.vars_col_name: str = var_col_name
        self.vals_col_name: str = val_col_name

    @staticmethod
    def stack_df(df: pnd.DataFrame, cols: list[str]) -> pnd.DataFrame:
        return df.set_index(cols).stack().reset_index()

    def melt_df(self, df: pnd.DataFrame, cols: list[str]) -> pnd.DataFrame:
        return pnd.melt(df, id_vars=cols, var_name=self.vars_col_name, value_name=self.vals_col_name)

    @staticmethod
    def clean_df_col_name(df: pnd.DataFrame, space_holder: str = ' ') -> pnd.DataFrame:
        df.columns = df.columns.str.strip().str.replace(r'\s+', space_holder, regex=True)
        return df

    @staticmethod
    def strip_df_data(df: pnd.DataFrame) -> pnd.DataFrame:
        return df.applymap(lambda x: re.sub('\s+', ' ', x).strip() if isinstance(x, str) else x)

    @staticmethod
    def create_dictionary(df: pnd.DataFrame, key_cols: str, values_col: str) -> dict[str, str]:
        dictionary: dict[str, str] = {}
        if df[key_cols].dropna().duplicated().sum() > 0:
            raise Exception('Key column contains duplicated values')
        for idx, row in df.iterrows():
            if row[key_cols]:
                dictionary.update({row[key_cols]: row[values_col]})
        return dictionary

    @staticmethod
    def get_last_day_of_the_months(sales_df: pnd.DataFrame, date_col: str) -> pnd.DataFrame:
        return sales_df.groupby([sales_df[date_col].dt.year, sales_df[date_col].dt.month])[
            date_col].max()

    @staticmethod
    def periods_groupby(df: pnd.DataFrame, date_col: str, groups: list[str], agg: dict[str, str],
                        period: str) -> pnd.DataFrame:
        if period in Utilities.ALL_PERIODS:
            quarters_df = Utilities.periods_groupby(df, date_col, groups, agg, Utilities.QUARTER)
            semesters_df = Utilities.periods_groupby(df, date_col, groups, agg, Utilities.SEMESTER)
            return pnd.concat([quarters_df, semesters_df])

        period_col: str = 'PERIODS'
        periods_df: pnd.DataFrame = df.copy()

        if period in Utilities.QUARTER:
            periods_df[period] = periods_df[date_col].dt.quarter
            periods_df[date_col] = Utilities.QUARTER + periods_df[period].astype(str) + ' ' + periods_df[
                date_col].dt.year.astype(
                str)
        elif period in Utilities.SEMESTER:
            periods_df[date_col] = Utilities.SEMESTER + ((df[date_col].dt.month - 1) // 6 + 1).astype(str) + ' ' + \
                                   periods_df[
                                       date_col].dt.year.astype(str)
        else:
            raise Exception('Période indéfinie')

        if any(groups):
            new_group = [date_col] + groups
            periods_df = periods_df.groupby(by=new_group)
        else:
            periods_df = periods_df.groupby(period_col)
        periods_sum = periods_df.agg(agg)
        return periods_sum.reset_index()
