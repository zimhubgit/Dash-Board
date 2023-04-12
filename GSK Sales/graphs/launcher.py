import pandas as pnd

import gsk_sales_figures as graph


def launch():
    data_dict = pnd.read_excel('/home/nazim/Devs/GSK Sales/output/GSK SALES.xlsx', sheet_name=None)
    graph.GSKSalesGraph.set_data(data_dict['2022'], data_dict['2023'])
    load_graphs()


def load_graphs():
    graph.load(pnd.read_excel('/home/nazim/Devs/GSK Sales/input/Sankey.xlsx'))
