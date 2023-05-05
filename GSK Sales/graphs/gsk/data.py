import parametres.src.name_space as nm
import pandas as pnd


class SalesAs:
    value: str = 'Value'
    volume: str = 'Volume'

    def __init__(self, name: str):
        self.name: str = name
        self.rfc: str
        self.achieved: str
        self._set_properties()

    def _set_properties(self):
        if self.name == SalesAs.volume:
            self.rfc = nm.GSK.ColName.RFC_UNIT_COL
            self.achieved = nm.GSK.ColName.UNIT_SALES
        elif self.name == SalesAs.value:
            self.rfc = nm.GSK.ColName.RFC_VALUE_COL
            self.achieved = nm.GSK.ColName.VALUE_SALES
        else:
            raise Exception('"Sales As" error')


class Cache:
    def __init__(self):
        self.data_source_cache: dict[str, pnd.DataFrame] = {}
        self.dataset_dict: dict[str, pnd.DataFrame] = {}

    def clear(self):
        self.dataset_dict = {}
        self.data_source_cache = {}


class Data:

    def __init__(self, year: str, dataset: pnd.DataFrame):
        self.year: str = year
        self.dataset: pnd.DataFrame = dataset
        self.cache: Cache = Cache()

    def filter(self, prd_type: str, brand: str, sku: str,
               date: pnd.Timestamp, end_date: pnd.Timestamp) -> pnd.DataFrame:
        cached_df_key: str = f'{prd_type}:{brand}:{sku}:{str(date)}'
        cached_df = self.cache.dataset_dict.get(cached_df_key)
        if cached_df is not None and not cached_df.empty:
            return cached_df
        df: pnd.DataFrame
        df = self.dataset.copy()
        df = df[df[nm.GSK.ColName.PERIOD_TYPE] == prd_type]
        if end_date is None:
            df = df[df[nm.GSK.ColName.DATE] == date]
        else:
            df = df[(df[nm.GSK.ColName.DATE] >= date) & (df[nm.GSK.ColName.DATE] <= date)]
        if sku is not None:
            df = df[df[nm.GSK.ColName.SKU] == sku]
        else:
            df = df[df[nm.GSK.ColName.BRAND] == sku]
        df = df[df[nm.GSK.ColName.BRAND] == brand]
        self.cache.dataset_dict.update({cached_df_key: df})
        return df

    @staticmethod
    def filter_dataset(dataset: pnd.DataFrame,
                       prd_type: str,
                       brand: str,
                       sku: str,
                       date: pnd.Timestamp,
                       end_date: pnd.Timestamp) -> pnd.DataFrame:

        cached_df_key: str = f'{prd_type}:{brand}:{sku}:{str(date)}'
        cached_df = Cache.dataset_dict.get(cached_df_key)
        if cached_df is not None and not cached_df.empty:
            return cached_df
        df: pnd.DataFrame
        df = dataset.copy()
        df = df[df[nm.GSK.ColName.PERIOD_TYPE] == prd_type]
        if end_date is None:
            df = df[df[nm.GSK.ColName.DATE] == date]
        else:
            df = df[(df[nm.GSK.ColName.DATE] >= date) & (df[nm.GSK.ColName.DATE] <= date)]
        if sku is not None:
            df = df[df[nm.GSK.ColName.SKU] == sku]
        else:
            df = df[df[nm.GSK.ColName.BRAND] == sku]
        df = df[df[nm.GSK.ColName.BRAND] == brand]
        Cache.dataset_dict.update({cached_df_key: df})
        return df


def get_delta_color(progression: float) -> str:
    default_red_color: str = '#FF4136'
    default_green_color: str = '#3D9970'
    dark_green_color: str = '#033301'
    dark_red_color: str = '#690902'
    orange_color: str = '#db9f07'
    blue_color: str = '#2370c2'
    if progression < .20:
        return dark_red_color
    elif progression < .45:
        return default_red_color
    elif progression < .85:
        return orange_color
    elif progression < .95:
        return default_green_color
    elif progression < 1.1:
        return dark_green_color
    else:
        return blue_color


data_dict: dict[str, Data] = {}


def load(data_src_file_name: str):
    data_src_dict = pnd.read_excel(data_src_file_name, sheet_name=None)
    for year_key, source_dataset in data_src_dict.items():
        data_dict.update({year_key: Data(year_key, source_dataset)})
