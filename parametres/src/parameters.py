import os

import pandas as pnd

import parametres.src.name_space as nm
from utilities.src.util import Utilities as Ut


class Parameters:
    INPUT_DIR: str = f'{os.getcwd()}{os.sep}input{os.sep}'
    SALES_FILE_NAME_LIST: list[str] = [INPUT_DIR + 'SUIVI LIVRAISONS ATP 21  Decembre. 2022.xlsx',
                                       INPUT_DIR + 'SUIVI LIVRAISONS ATP  17  Mai. 2023.xlsx']
    PARAMETERS_FILE_NAME = f'{os.getcwd()}{os.sep}input{os.sep}MAPPER.xlsx'
    OUTPUT_DIR = f'{os.getcwd()}{os.sep}output{os.sep}'
    OUTPUT_DATA_FILE_NAME = OUTPUT_DIR + nm.GSK.Naming.SALES_OUTPUT_FILE_NAME

    LAST_DAY_OF_THE_WEEK = 3
    LAST_PERIOD_YEAR = 2022
    SALES_DATA_HOUR = 16

    DESIGNATION_DF: pnd.DataFrame
    COLUMNS_DF: pnd.DataFrame
    METADATA_DF: pnd.DataFrame

    MAPPER_GSK_DESIGNATION_SKU: dict[str, str]
    MAPPER_COL_NAME_NEW_COL_NAME: dict[str, str]
    MAPPER_SKU_ORDER: dict[str, str]
    MAPPER_SKU_BRAND: dict[str, str]
    MAPPER_BRAND_ORDER: dict[str, str]
    MAPPER_SKU_SKU_TYPE: dict[str, str]
    MAPPER_SKU_TYPE_ORDER: dict[str, str]
    MAPPER_COLUMN_ACTION_UPON: dict[str, list[str]] = {}
    MAPPER_SKU_SKU_COLOR: dict[str, str]

    @staticmethod
    def get_designation_df() -> pnd.DataFrame:
        return Parameters.DESIGNATION_DF

    @staticmethod
    def get_columns_df() -> pnd.DataFrame:
        return Parameters.COLUMNS_DF

    @staticmethod
    def get_metadata_df() -> pnd.DataFrame:
        return Parameters.METADATA_DF

    @staticmethod
    def set_brand_order_mapper():
        map_df = Parameters.METADATA_DF.drop_duplicates(subset=[nm.GSK.ColName.SKU_TYPE])
        Parameters.MAPPER_BRAND_ORDER = Ut.create_dictionary(map_df, key_cols=nm.GSK.ColName.SKU_TYPE,
                                                             values_col=nm.GSK.ColName.SKU_TYPE_ORDER)

    @staticmethod
    def get_brand_order_mapper(brand: str):
        return Parameters.MAPPER_BRAND_ORDER.get(brand)

    @staticmethod
    def set_sku_brand_mapper():
        Parameters.MAPPER_SKU_BRAND = Ut.create_dictionary(Parameters.METADATA_DF, key_cols=nm.GSK.ColName.SKU,
                                                           values_col=nm.GSK.ColName.BRAND)

    @staticmethod
    def get_sku_brand(sku: str):
        return Parameters.MAPPER_SKU_BRAND.get(sku)

    @staticmethod
    def set_column_new_name_mapper():
        new_col_names_df: pnd.DataFrame = Parameters.COLUMNS_DF[
            (Parameters.COLUMNS_DF[nm.GSK.ColName.SOURCE] == nm.GSK.ColName.GSK) & (
                Parameters.COLUMNS_DF[nm.GSK.ColName.NEW].notna())]
        Parameters.MAPPER_COL_NAME_NEW_COL_NAME = Ut.create_dictionary(new_col_names_df, key_cols=nm.GSK.ColName.INPUT,
                                                                       values_col=nm.GSK.ColName.NEW)

    @staticmethod
    def get_column_new_name(col_name: str):
        return Parameters.MAPPER_COL_NAME_NEW_COL_NAME.get(col_name)

    @staticmethod
    def set_sku_mapper():
        Parameters.MAPPER_GSK_DESIGNATION_SKU = Ut.create_dictionary(Parameters.DESIGNATION_DF,
                                                                     key_cols=nm.GSK.ColName.GSK_DESIGNATION,
                                                                     values_col=nm.GSK.ColName.DESIGNATION)

    @staticmethod
    def get_sku(gsk_designation: str) -> str:
        return Parameters.MAPPER_GSK_DESIGNATION_SKU.get(gsk_designation)

    @staticmethod
    def set_sku_order_mapper():
        mapper_df = Parameters.METADATA_DF[Parameters.METADATA_DF[nm.GSK.ColName.SKU_TYPE] != nm.GSK.ColName.BRAND]
        Parameters.MAPPER_SKU_ORDER = Ut.create_dictionary(mapper_df, key_cols=nm.GSK.ColName.SKU,
                                                           values_col=nm.GSK.ColName.SKU_ORDER)

    @staticmethod
    def get_sku_order(sku: str) -> str:
        return Parameters.MAPPER_SKU_ORDER.get(sku)

    @staticmethod
    def set_sku_type_mapper():
        Parameters.MAPPER_SKU_SKU_TYPE = Ut.create_dictionary(Parameters.METADATA_DF, key_cols=nm.GSK.ColName.SKU,
                                                              values_col=nm.GSK.ColName.SKU_TYPE)

    @staticmethod
    def get_sku_type(sku: str) -> str:
        return Parameters.MAPPER_SKU_SKU_TYPE.get(sku)

    @staticmethod
    def set_sku_type_order_mapper():
        mapper_df: pnd.DataFrame = Parameters.METADATA_DF[
            [nm.GSK.ColName.SKU_TYPE, nm.GSK.ColName.SKU_TYPE_ORDER]].copy()
        mapper_df.drop_duplicates(nm.GSK.ColName.SKU_TYPE, inplace=True)
        Parameters.MAPPER_SKU_TYPE_ORDER = Ut.create_dictionary(mapper_df,
                                                                key_cols=nm.GSK.ColName.SKU_TYPE,
                                                                values_col=nm.GSK.ColName.SKU_TYPE_ORDER)

    @staticmethod
    def get_sku_type_order(sku_type: str) -> str:
        return Parameters.MAPPER_SKU_TYPE_ORDER.get(sku_type)

    @staticmethod
    def set_sku_sku_color_mapper():
        mapper_df: pnd.DataFrame = Parameters.METADATA_DF[
            [nm.GSK.ColName.SKU, nm.GSK.ColName.COLOR]].copy()
        mapper_df.drop_duplicates(nm.GSK.ColName.SKU, inplace=True)
        mapper_df.dropna(how='all', inplace=True)
        Parameters.MAPPER_SKU_SKU_COLOR = Ut.create_dictionary(mapper_df,
                                                               key_cols=nm.GSK.ColName.SKU,
                                                               values_col=nm.GSK.ColName.COLOR)

    @staticmethod
    def get_sku_sku_color(sku: str) -> str:
        return Parameters.MAPPER_SKU_SKU_COLOR.get(sku)

    @staticmethod
    def set_column_fillna_method():
        fill_methods = Parameters.COLUMNS_DF[[nm.GSK.ColName.RENAMED_COLUMNS, nm.GSK.ColName.ACTION]].groupby(
            nm.GSK.ColName.ACTION)
        for method, cols in fill_methods:
            Parameters.MAPPER_COLUMN_ACTION_UPON.update(
                {method: cols[nm.GSK.ColName.RENAMED_COLUMNS].values.tolist()})

    @staticmethod
    def get_column_fillna_method(col_name: str) -> dict[str, list[str]]:
        return Parameters.MAPPER_COLUMN_ACTION_UPON

    @staticmethod
    def set_mappers():
        Parameters.set_sku_mapper()
        Parameters.set_column_new_name_mapper()
        Parameters.set_brand_order_mapper()
        Parameters.set_sku_order_mapper()
        Parameters.set_sku_type_order_mapper()
        Parameters.set_sku_type_mapper()
        Parameters.set_sku_brand_mapper()
        Parameters.set_sku_sku_color_mapper()
        Parameters.set_column_fillna_method()

    @staticmethod
    def load_parameters(parameters_file_name: str):
        config_dict = pnd.read_excel(parameters_file_name, sheet_name=None)
        Parameters.DESIGNATION_DF = config_dict.get(nm.Parameters.SheetName.DESIGNATION)
        Parameters.COLUMNS_DF = config_dict.get(nm.Parameters.SheetName.COLUMNS)
        Parameters.METADATA_DF = config_dict.get(nm.Parameters.SheetName.ORDER)
        Parameters.set_mappers()
