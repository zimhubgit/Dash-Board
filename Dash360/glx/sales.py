from datetime import datetime

import numpy as np
import pandas as pnd

from name_space import GSK
from parameters import Parameters as Params
from util import Utilities

Ut = Utilities()

COLUMNS_ORDER = [GSK.ColName.DATE, GSK.ColName.PERIOD_TYPE, GSK.ColName.SKU_TYPE,
                 GSK.ColName.SKU_TYPE_ORDER, GSK.ColName.SKU,
                 GSK.ColName.SKU_ORDER, Ut.vars_col_name, Ut.vals_col_name]


class MTDSalesDataset:
    def __init__(self, date: datetime, mtd_sales_df: pnd.DataFrame, keep_all_cols: bool):
        self.keep_all_cols = keep_all_cols
        self.mtd_sales_df: pnd.DataFrame = mtd_sales_df
        self.date: datetime = date
        self._1_load_mtd_dataset()

    def _1_load_mtd_dataset(self):
        self._2_clean_mtd_dataset()
        self._3_set_appropriate_values()
        self._4_set_dtypes()
        self._5_add_missing_data()

    def _2_clean_mtd_dataset(self):
        self._clean1_remove_extra_spaces()
        self._clean2_flatten_columns()
        self._clean3_remove_nan_values()
        self._clean4_remove_junk_data()

    def _clean1_remove_extra_spaces(self):
        self.mtd_sales_df = Ut.clean_df_col_name(self.mtd_sales_df)
        self.mtd_sales_df = Ut.strip_df_data(self.mtd_sales_df)

    def _clean2_flatten_columns(self):
        separator: str = ': -'
        split_by: str = '-'
        cols = self.mtd_sales_df.iloc[0]
        index_vals = cols.index.values
        col_vals = [str(cl) for cl in cols.values]
        self.mtd_sales_df.columns = [
            name.split(split_by)[1] if GSK.Naming.UNNAMED_COLUMN in name else name.replace(split_by, '') for name in
            index_vals + separator + col_vals]
        self.mtd_sales_df.drop(index=0, inplace=True)
        self.mtd_sales_df.reset_index(inplace=True, drop=True)

    def _clean3_remove_nan_values(self):
        self.mtd_sales_df.dropna(inplace=True, how='all')

    def _clean4_remove_junk_data(self):
        total_idx = self.mtd_sales_df[self.mtd_sales_df[GSK.ColName.CODE] == GSK.Naming.TOTAL].index[0]
        self.mtd_sales_df.drop(self.mtd_sales_df.index[total_idx:], inplace=True)

    def _3_set_appropriate_values(self):
        self._set_appropriate_v1_rename_columns()

    def _set_appropriate_v1_rename_columns(self):
        self.mtd_sales_df.rename(inplace=True, columns=Params.MAPPER_COL_NAME_NEW_COL_NAME)
        self.mtd_sales_df.rename(inplace=True,
                                 columns={name: (
                                     GSK.ColName.RFC_UNIT_COL if (name.startswith(GSK.Naming.RFC_UNIT_START) and not (
                                             GSK.Naming.GBP in name)) else name)
                                     for name in self.mtd_sales_df.columns})
        self.mtd_sales_df.rename(inplace=True,
                                 columns={name: (name[:3] if name.startswith(GSK.Naming.NSP_COL_START) else name) for
                                          name in
                                          self.mtd_sales_df.columns})

        if self.keep_all_cols:
            self.mtd_sales_df.rename(inplace=True,
                                     columns={name: (name[:2] if name.startswith(GSK.Naming.WEEK_COL_START) else name)
                                              for
                                              name in
                                              self.mtd_sales_df.columns})
            self.mtd_sales_df.rename(inplace=True,
                                     columns={name: Params.get_column_new_name(name[:11]) if name.startswith(
                                         GSK.Naming.TOTAL_COL_START) else name
                                              for name in self.mtd_sales_df.columns})

    def _4_set_dtypes(self):
        for col in self.mtd_sales_df.columns:
            converted_col = pnd.to_numeric(self.mtd_sales_df[col], errors='coerce')
            if converted_col.notnull().all():
                self.mtd_sales_df[col] = converted_col

    def _5_add_missing_data(self):
        self._add_missing_data1_custom_designations()
        self._add_missing_data2_sku_types()
        self._add_missing_data3_sku_totals()
        self._add_missing_data4_brands()
        self._add_missing_data5_date_col()

    def _add_missing_data1_custom_designations(self):
        self.mtd_sales_df[GSK.ColName.SKU] = self.mtd_sales_df[GSK.ColName.DESIGNATION].apply(
            lambda x: Params.get_sku(x))

    def _add_missing_data2_sku_types(self):
        self.mtd_sales_df[GSK.ColName.SKU_TYPE] = self.mtd_sales_df[GSK.ColName.SKU].apply(
            lambda x: Params.get_sku_type(x))

    def _add_missing_data3_sku_totals(self):
        num_cols_df = self.mtd_sales_df.select_dtypes(include=['number'])
        num_cols_df = num_cols_df.sum()
        all_skus_df = pnd.DataFrame([num_cols_df.values], columns=num_cols_df.index)
        all_skus_df[GSK.ColName.SKU] = GSK.Naming.ALL_SKUs
        self.mtd_sales_df = pnd.concat([self.mtd_sales_df, all_skus_df])

    def _add_missing_data4_brands(self):
        brands_df = self.mtd_sales_df[self.mtd_sales_df[GSK.ColName.SKU_TYPE] == GSK.Naming.SKU_SKU_TYPE].copy()
        brands_df[GSK.ColName.SKU] = brands_df[GSK.ColName.SKU].apply(
            lambda x: Params.get_sku_brand(x))
        brands_df_num_cols = brands_df.select_dtypes(include='number')
        sums_df = brands_df.groupby([GSK.ColName.SKU])[brands_df_num_cols.columns].sum()
        sums_df.reset_index(inplace=True)
        sums_df[GSK.ColName.SKU_TYPE] = GSK.Naming.BRAND_SKU_TYPE
        self.mtd_sales_df = pnd.concat([self.mtd_sales_df, sums_df])

    def _add_missing_data5_date_col(self):
        self.mtd_sales_df[GSK.ColName.DATE] = self.date

    def __stack_sales(self):
        stacked_df: pnd.DataFrame = self.mtd_sales_df.copy()
        self.stacked_sales_df = Ut.melt_df(df=stacked_df,
                                           cols=[GSK.ColName.DATE, GSK.ColName.PERIOD_TYPE,
                                                 GSK.ColName.CODE, GSK.ColName.DESIGNATION,
                                                 GSK.ColName.SKU,
                                                 GSK.ColName.SKU_TYPE, GSK.ColName.BRAND])

    def get_mtd_sales_df(self) -> pnd.DataFrame:
        return self.mtd_sales_df.copy()


class GskSales:

    def __init__(self, mtd_sales_dict: dict[str, pnd.DataFrame], keep_all_cols: bool):
        self.keep_all_cols = keep_all_cols
        self.gsk_dataset_df: pnd.DataFrame = pnd.DataFrame()
        self.mtd_sales_dict: dict[str, MTDSalesDataset] = {}
        self.updated_on: datetime = None
        self._01_load(mtd_sales_dict)

    def _01_load(self, mtd_sales_dict: dict[str, pnd.DataFrame]):
        self._02_set_mtd_sales(mtd_sales_dict)
        self._03_set_updated_on()
        self._04_concatenate_mtd_sales_df()
        self._05_fill_missing_dates_in_dataset()
        self._06_set_daily_sales_df()
        self._07_set_weekly_sales_df()
        self._08_set_month_sales_df()
        self._09_set_quarter_sales_df()
        self._10_set_semester_sales_df()
        self._11_set_year_sales_df()
        self._12_add_metadata()

    def _02_set_mtd_sales(self, mtd_sales: dict[datetime, pnd.DataFrame]):
        for date, mtd_sales_df in mtd_sales.items():
            if GSK.Naming.END_COL not in date:
                date = date.replace('à', ':').replace(' ', '')
                try:
                    date = pnd.to_datetime(date, format='%d-%m-%y:%HH')
                except:
                    date = date.replace("-", "/", 1).replace("-", "").replace('/', '-')
                    date = date.split(':')[0] + '-22:' + date.split(':')[1]
                    date = pnd.to_datetime(date, format='%d-%m-%y:%HH')
                self.mtd_sales_dict.update({date: MTDSalesDataset(date, mtd_sales_df, self.keep_all_cols)})

    def _03_set_updated_on(self):
        self.updated_on = sorted(list(self.mtd_sales_dict.keys()), key=lambda date: date)[-1]

    def _04_concatenate_mtd_sales_df(self):
        for mtd_sale_dataset in self.mtd_sales_dict.values():
            self.gsk_dataset_df = pnd.concat([self.gsk_dataset_df, mtd_sale_dataset.get_mtd_sales_df()])

    def _05_fill_missing_dates_in_dataset(self):
        if self.gsk_dataset_df[GSK.ColName.DATE].max().year == Params.LAST_PERIOD_YEAR:
            self.gsk_dataset_df[['Stock Quarantaine (Non libéré)',
                                 'Stock Vendable (Libéré)']] = 0
        products: list[str] = self._fill_missing_dates1_products_list()
        # Create a list of DataFrames for each product
        mtd_products_data_df: list[pnd.DataFrame] = []

        start_date, end_date = self._fill_missing_dates2_boundary_indexes()
        for product in products:
            # Filter the DataFrame by product
            mtd_product_df = self.gsk_dataset_df[self.gsk_dataset_df[GSK.ColName.SKU] == product]

            # Create a new DataFrame with a complete range of dates
            index = pnd.date_range(start_date, end_date, freq='D')
            all_mtd_dates_df = pnd.DataFrame({GSK.ColName.DATE: index})

            # Add 'product' column
            all_mtd_dates_df[GSK.ColName.SKU] = product

            # Merge the original DataFrame with the new DataFrame
            mtd_product_data_df = pnd.merge(all_mtd_dates_df, mtd_product_df, how='left',
                                            on=[GSK.ColName.DATE, GSK.ColName.SKU])

            GskSales._fill_missing_mtd_product_values(mtd_product_data_df)
            # Append to the list of DataFrames
            mtd_products_data_df.append(mtd_product_data_df)

        # Concatenate all DataFrames together
        all_gsk_mtd_data_df = pnd.concat(mtd_products_data_df)
        all_gsk_mtd_data_df[GSK.ColName.PERIOD_TYPE] = GSK.Naming.PERIOD_TYPE_MTD
        self.gsk_dataset_df = all_gsk_mtd_data_df

    def _fill_missing_dates1_products_list(self) -> list[str]:
        return self.gsk_dataset_df[GSK.ColName.SKU].unique()

    def _fill_missing_dates2_boundary_indexes(self) -> datetime:
        self.gsk_dataset_df.set_index(GSK.ColName.DATE, inplace=True)
        index = self.gsk_dataset_df.index
        start_date = datetime(index.min().year, index.min().month, 1, index.min().hour).replace(
            hour=Params.SALES_DATA_HOUR)
        end_date = datetime(index.max().year, index.max().month, index.max().day,
                            index.min().hour).replace(
            hour=Params.SALES_DATA_HOUR)
        self.gsk_dataset_df.reset_index(inplace=True)
        return start_date, end_date

    @staticmethod
    def _fill_missing_mtd_product_values(product_df: pnd.DataFrame):
        # Fill missing sales values with the previous available sales values
        ffill_cols = Params.MAPPER_COLUMN_ACTION_UPON.get(GSK.Naming.FORWARD_FILL_ACTION)
        bfill_cols = Params.MAPPER_COLUMN_ACTION_UPON.get(GSK.Naming.BACKWARD_FILL_ACTION)
        zero_fill_cols = Params.MAPPER_COLUMN_ACTION_UPON.get(GSK.Naming.ZERO_ACTION)
        zero_bfill_cols = Params.MAPPER_COLUMN_ACTION_UPON.get(GSK.Naming.ZERO_BACKFILL_ACTION)

        for colmn in ffill_cols:
            product_df[colmn].replace(0, np.NaN, inplace=True)

        product_df[ffill_cols] = product_df.groupby([product_df[GSK.ColName.DATE].dt.year,
                                                     product_df[GSK.ColName.DATE].dt.month])[ffill_cols].fillna(
            method=GSK.Naming.FORWARD_FILL_ACTION)
        product_df[zero_bfill_cols] = product_df[zero_bfill_cols].fillna(0)

        product_df[bfill_cols] = \
            product_df.groupby([product_df[GSK.ColName.DATE].dt.year, product_df[GSK.ColName.DATE].dt.month])[
                bfill_cols].fillna(method=GSK.Naming.BACKWARD_FILL_ACTION)

        available_zero_fill_cols = [col for col in zero_fill_cols if col in product_df.columns.tolist()]

        product_df[available_zero_fill_cols] = \
            product_df.groupby([product_df[GSK.ColName.DATE].dt.year, product_df[GSK.ColName.DATE].dt.month])[
                available_zero_fill_cols].fillna(0)

    def _06_set_daily_sales_df(self):
        self.gsk_dataset_df.sort_values(inplace=True, by=[GSK.ColName.DATE, GSK.ColName.SKU])
        self.gsk_dataset_df.reset_index(inplace=True, drop=True)
        daily_group = self.gsk_dataset_df.groupby(
            [self.gsk_dataset_df[GSK.ColName.DATE].dt.year, self.gsk_dataset_df[GSK.ColName.DATE].dt.month,
             GSK.ColName.SKU])
        daily_df = daily_group[Params.MAPPER_COLUMN_ACTION_UPON.get(GSK.Naming.DIFF_ACTION)].diff().fillna(0)
        daily_df[GSK.ColName.PERIOD_TYPE] = GSK.Naming.PERIOD_TYPE_DAILY
        cols = [GSK.ColName.DATE, GSK.ColName.SKU] + Params.MAPPER_COLUMN_ACTION_UPON.get(GSK.Naming.NO_ACTION)
        daily_df = pnd.merge(self.gsk_dataset_df[cols], daily_df,
                             how='left',
                             left_index=True, right_index=True)
        self.gsk_dataset_df = pnd.concat([self.gsk_dataset_df, daily_df])

    def _07_set_weekly_sales_df(self):
        weekly_sales_df: pnd.DataFrame = self.gsk_dataset_df[
            self.gsk_dataset_df[GSK.ColName.PERIOD_TYPE] == GSK.Naming.PERIOD_TYPE_DAILY].copy()
        weekly_sales_df.sort_values(by=[GSK.ColName.DATE, GSK.ColName.SKU], inplace=True)
        weekly_sales_df.reset_index(drop=True, inplace=True)
        week_sum_cols = Params.MAPPER_COLUMN_ACTION_UPON.get(GSK.Naming.SUM_UP_ACTION)
        weekly_df = weekly_sales_df.groupby(GSK.ColName.SKU).resample(on=GSK.ColName.DATE, rule='W-THU')[
            week_sum_cols].sum().reset_index()
        weekly_df[GSK.ColName.DATE] = weekly_df[GSK.ColName.DATE].apply(
            lambda dt: dt.replace(hour=Params.SALES_DATA_HOUR))
        weekly_df.set_index([GSK.ColName.DATE, GSK.ColName.SKU], inplace=True)
        weekly_sales_df.set_index([GSK.ColName.DATE, GSK.ColName.SKU], inplace=True)
        weekly_df = pnd.merge(weekly_df, weekly_sales_df[Params.MAPPER_COLUMN_ACTION_UPON.get(GSK.Naming.NO_ACTION)],
                              how='left', left_index=True, right_index=True)
        weekly_df[GSK.ColName.PERIOD_TYPE] = GSK.Naming.PERIOD_TYPE_Weekly
        weekly_df.reset_index(inplace=True)
        self.gsk_dataset_df = pnd.concat([self.gsk_dataset_df, weekly_df])

    def _08_set_month_sales_df(self):
        monthly_sales_df: pnd.DataFrame = self.gsk_dataset_df[
            self.gsk_dataset_df[GSK.ColName.PERIOD_TYPE] == GSK.Naming.PERIOD_TYPE_MTD].copy()
        month_dates_list = monthly_sales_df.groupby(monthly_sales_df[GSK.ColName.DATE].dt.month)[
            GSK.ColName.DATE].max().values
        monthly_sales_df = monthly_sales_df[monthly_sales_df[GSK.ColName.DATE].isin(month_dates_list)]
        monthly_sales_df[GSK.ColName.DATE] = monthly_sales_df[GSK.ColName.DATE].apply(
            lambda date: pnd.to_datetime(date) + pnd.offsets.MonthEnd(0))
        monthly_sales_df[GSK.ColName.PERIOD_TYPE] = GSK.Naming.PERIOD_TYPE_MONTHLY

        self.gsk_dataset_df = pnd.concat([self.gsk_dataset_df, monthly_sales_df])

    def _09_set_quarter_sales_df(self):
        monthly_sales_df: pnd.DataFrame = self.gsk_dataset_df[
            self.gsk_dataset_df[GSK.ColName.PERIOD_TYPE] == GSK.Naming.PERIOD_TYPE_MONTHLY].copy()
        quarter_sales_df = monthly_sales_df.groupby(GSK.ColName.SKU).resample(rule='Q', on=GSK.ColName.DATE)[
            Params.MAPPER_COLUMN_ACTION_UPON.get(GSK.Naming.QUARTER_SUM)].sum().reset_index()
        quarter_sales_df[GSK.ColName.DATE] = quarter_sales_df[GSK.ColName.DATE].apply(
            lambda dt: dt.replace(hour=Params.SALES_DATA_HOUR))
        quarter_sales_df = pnd.merge(quarter_sales_df,
                                     monthly_sales_df[[GSK.ColName.DATE, GSK.ColName.SKU, GSK.ColName.NSP]],
                                     on=[GSK.ColName.DATE, GSK.ColName.SKU],
                                     how='left')
        quarter_sales_df[GSK.ColName.PERIOD_TYPE] = GSK.Naming.PERIOD_TYPE_QTD
        self.gsk_dataset_df = pnd.concat([self.gsk_dataset_df, quarter_sales_df])

    def _10_set_semester_sales_df(self):
        monthly_sales_df: pnd.DataFrame = self.gsk_dataset_df[
            self.gsk_dataset_df[GSK.ColName.PERIOD_TYPE] == GSK.Naming.PERIOD_TYPE_MONTHLY].copy()
        hy1_sales_df = monthly_sales_df[monthly_sales_df[GSK.ColName.DATE].dt.month.isin(list(range(1, 7)))]
        if not hy1_sales_df.empty:
            hy1_sales_df = hy1_sales_df.groupby(GSK.ColName.SKU)[
                Params.MAPPER_COLUMN_ACTION_UPON.get(GSK.Naming.QUARTER_SUM)].sum().reset_index()
            hy1_sales_df[GSK.ColName.PERIOD_TYPE] = GSK.Naming.PERIOD_TYPE_STD
            hy1_sales_df[GSK.ColName.DATE] = pnd.Timestamp(year=monthly_sales_df[GSK.ColName.DATE].dt.year.values[0],
                                                           month=6,
                                                           day=30, hour=16)

        hy2_sales_df = monthly_sales_df[monthly_sales_df[GSK.ColName.DATE].dt.month.isin(list(range(7, 13)))]
        if not hy2_sales_df.empty:
            hy2_sales_df = hy2_sales_df.groupby(GSK.ColName.SKU)[
                Params.MAPPER_COLUMN_ACTION_UPON.get(GSK.Naming.QUARTER_SUM)].sum().reset_index()
            hy2_sales_df[GSK.ColName.PERIOD_TYPE] = GSK.Naming.PERIOD_TYPE_STD
            hy2_sales_df[GSK.ColName.DATE] = pnd.Timestamp(year=monthly_sales_df[GSK.ColName.DATE].dt.year.values[0],
                                                           month=12,
                                                           day=31, hour=16)

        half_years_df = pnd.concat([hy1_sales_df, hy2_sales_df])
        semester_sales_df = pnd.merge(half_years_df,
                                      monthly_sales_df[[GSK.ColName.DATE, GSK.ColName.SKU, GSK.ColName.NSP]],
                                      on=[GSK.ColName.DATE, GSK.ColName.SKU],
                                      how='left')

        self.gsk_dataset_df = pnd.concat([self.gsk_dataset_df, half_years_df])

    def _11_set_year_sales_df(self):
        monthly_sales_df: pnd.DataFrame = self.gsk_dataset_df[
            self.gsk_dataset_df[GSK.ColName.PERIOD_TYPE] == GSK.Naming.PERIOD_TYPE_MONTHLY].copy()
        year_sales_df = monthly_sales_df.groupby(GSK.ColName.SKU)[
            Params.MAPPER_COLUMN_ACTION_UPON.get(GSK.Naming.QUARTER_SUM)].sum().reset_index()
        year_sales_df[GSK.ColName.DATE] = pnd.Timestamp(year=self.gsk_dataset_df[GSK.ColName.DATE].dt.year.values[0],
                                                        month=12,
                                                        day=31, hour=Params.SALES_DATA_HOUR)
        year_sales_df = pnd.merge(year_sales_df,
                                  monthly_sales_df[[GSK.ColName.DATE, GSK.ColName.SKU, GSK.ColName.NSP]],
                                  on=[GSK.ColName.DATE, GSK.ColName.SKU],
                                  how='left')
        year_sales_df[GSK.ColName.PERIOD_TYPE] = GSK.Naming.PERIOD_TYPE_YTD
        self.gsk_dataset_df = pnd.concat([self.gsk_dataset_df, year_sales_df])

    def _12_add_metadata(self):
        self.gsk_dataset_df[GSK.ColName.SKU_TYPE] = self.gsk_dataset_df[GSK.ColName.SKU].apply(
            lambda sku: Params.get_sku_type(sku))
        self.gsk_dataset_df[GSK.ColName.SKU_TYPE_ORDER] = self.gsk_dataset_df[GSK.ColName.SKU_TYPE].apply(
            lambda sku_type: Params.get_sku_type_order(sku_type))
        self.gsk_dataset_df[GSK.ColName.SKU_ORDER] = self.gsk_dataset_df[GSK.ColName.SKU].apply(
            lambda sku: Params.get_sku_order(sku))
        self.gsk_dataset_df[GSK.ColName.BRAND] = self.gsk_dataset_df[GSK.ColName.SKU].apply(
            lambda sku: Params.get_sku_brand(sku))
        self.gsk_dataset_df[GSK.ColName.UPDATED_ON] = self.updated_on
        self.gsk_dataset_df[GSK.ColName.COLOR] = self.gsk_dataset_df[GSK.ColName.SKU].apply(
            lambda sku: Params.get_sku_sku_color(sku))


gsk_sales_list: list[GskSales] = []


def load_gsk_sales(sales: list[dict[str, pnd.DataFrame]], keep_all_cols: bool):
    for gsk_sales in sales:
        gsk_sales_list.append(GskSales(gsk_sales, keep_all_cols))
