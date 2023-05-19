import pandas as pnd
from Dash360.gsk import sales as sls
from Dash360.utils import name_space as nm
from Dash360.utils.parameters import Parameters as Params

DESIGNATION_CONF: pnd.DataFrame
SKU_ORDER_DF: pnd.DataFrame
COLS_CONF: pnd.DataFrame


def launch():
    Params.load_parameters(Params.PARAMETERS_FILE_NAME)
    launch_gsk_sales_process()
    write_gsk_sales()


def launch_gsk_sales_process():
    gsk_sales_list: list[dict[str, pnd.DataFrame]]
    gsk_sales_list = [pnd.read_excel(sales, sheet_name=None) for sales in Params.SALES_FILE_NAME_LIST]
    sls.load_gsk_sales(gsk_sales_list, keep_all_cols=True)


def write_gsk_sales():
    writer: pnd.ExcelWriter = pnd.ExcelWriter(Params.OUTPUT_DATA_FILE_NAME, engine='xlsxwriter')
    for gsk_sales in sls.gsk_sales_list:
        sales_year = gsk_sales.gsk_dataset_df[nm.GSK.ColName.DATE].dt.year.values[0]
        gsk_sales.gsk_dataset_df.to_excel(writer, sheet_name=str(sales_year), index=False)
    writer.close()
