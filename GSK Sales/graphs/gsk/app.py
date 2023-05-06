import os

from dash import Dash, Input, Output
import layout
import data as d

current_dir = os.path.abspath(os.curdir)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
grandparent_dir = os.path.abspath(os.path.join(parent_dir, os.pardir))

GSK_SALES_DIR: str = f'{grandparent_dir}{os.sep}output'
GSK_SALES_FILE_NAME: str = f'{GSK_SALES_DIR}{os.sep}GSK SALES.xlsx'
d.load(GSK_SALES_FILE_NAME)

app = Dash(__name__)
app.layout = layout.Dash.get()


@app.callback(
    Output(layout.IDs.mtd_sales_indicator, 'figure'),
    Output(layout.IDs.qtd_sales_indicator, 'figure'),
    Output(layout.IDs.std_sales_indicator, 'figure'),
    Output(layout.IDs.ytd_sales_indicator, 'figure'),
    Output(layout.IDs.aug_mtd_sales_indicator, 'figure'),
    Output(layout.IDs.aug_qtd_sales_indicator, 'figure'),
    Output(layout.IDs.aug_std_sales_indicator, 'figure'),
    Output(layout.IDs.aug_ytd_sales_indicator, 'figure'),
    Output(layout.IDs.clam_mtd_sales_indicator, 'figure'),
    Output(layout.IDs.clam_qtd_sales_indicator, 'figure'),
    Output(layout.IDs.clam_std_sales_indicator, 'figure'),
    Output(layout.IDs.clam_ytd_sales_indicator, 'figure'),
    Output(layout.IDs.sales_repartition_sunburst, 'figure'),
    Output(layout.IDs.sales_repartition_waterfall, 'figure'),
    Output(layout.IDs.sales_evolution_bar, 'figure'),
    Output(layout.IDs.stocks_evolution_bar, 'figure'),
    Input(layout.IDs.radio_b_sales_as, 'value'),
)
def update(value):
    sales_as = d.SalesAs(value)
    return (
        layout.FiguresUpdater.update_progress_section('MTD', 'ALL', None, None,
                                                      sales_as),
        layout.FiguresUpdater.update_progress_section('QTD', 'ALL', None, None,
                                                      sales_as),
        layout.FiguresUpdater.update_progress_section('STD', 'ALL', None, None,
                                                      sales_as),
        layout.FiguresUpdater.update_progress_section('YTD', 'ALL', None, None,
                                                      sales_as),
        layout.FiguresUpdater.update_progress_section('MTD', 'AUGMENTIN', None, None,
                                                      sales_as),
        layout.FiguresUpdater.update_progress_section('QTD', 'AUGMENTIN', None, None,
                                                      sales_as),
        layout.FiguresUpdater.update_progress_section('STD', 'AUGMENTIN', None, None,
                                                      sales_as),
        layout.FiguresUpdater.update_progress_section('YTD', 'AUGMENTIN', None, None,
                                                      sales_as),
        layout.FiguresUpdater.update_progress_section('MTD', 'CLAMOXYL', None, None,
                                                      sales_as),
        layout.FiguresUpdater.update_progress_section('QTD', 'CLAMOXYL', None, None,
                                                      sales_as),
        layout.FiguresUpdater.update_progress_section('STD', 'CLAMOXYL', None, None,
                                                      sales_as),
        layout.FiguresUpdater.update_progress_section('YTD', 'CLAMOXYL', None, None,
                                                      sales_as),
        layout.FiguresUpdater.update_sunburst_section(sales_as),
        layout.FiguresUpdater.update_waterfall_section(sales_as),
        layout.FiguresUpdater.update_sales_evolution_bar(sales_as),
        layout.FiguresUpdater.update_stocks_evolution_bar(sales_as),
    )


app.run_server(debug=True)
