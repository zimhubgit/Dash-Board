import os

from dash import Dash, Input, Output, State
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


@app.callback(Output(layout.IDs.drop_d_sku, 'options'),
              Output(layout.IDs.drop_d_sku, 'value'),
              Input(layout.IDs.drop_d_brand, 'value'))
def update_sku_drop_down(value):
    return (d.data_dict[d.cy_key].skus_map.get(value),
            d.data_dict[d.cy_key].skus_map.get(value)[0],
            )


@app.callback(Output(layout.IDs.drop_d_period_type_value, 'options'),
              Output(layout.IDs.drop_d_period_type_value, 'value'),
              Output(layout.IDs.drop_d_periods_label, 'children'),
              Input(layout.IDs.radio_b_period_type, 'value'))
def update_periods_drop_down(value):
    return (d.data_dict[d.cy_key].periods_map.get(value),
            d.data_dict[d.cy_key].periods_map.get(value)[0],
            f'Selected: {value}')


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
    Output(layout.IDs.sales_evolution_bar, 'figure'),
    Input(layout.IDs.radio_b_sales_as, 'value'),
)
def update_static_indicators(value):
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
        layout.FiguresUpdater.update_sales_evolution_bar(sales_as),
    )


@app.callback(Output(layout.IDs.sales_repartition_waterfall, 'figure'),
              State(layout.IDs.drop_d_brand, 'value'),
              State(layout.IDs.radio_b_period_type, 'value'),
              State(layout.IDs.drop_d_period_type_value, 'value'),
              Input(layout.IDs.radio_b_sales_as, 'value'),
              Input(layout.IDs.button_show, 'n_clicks'),
              )
def update_water_fall(brand, prd_type, prd, sales_as, n_clicks):
    sales_as = d.SalesAs(sales_as)
    return layout.FiguresUpdater.update_waterfall_section(brand, prd_type, prd, sales_as)


@app.callback(Output(layout.IDs.sales_repartition_sunburst, 'figure'),
              State(layout.IDs.radio_b_period_type, 'value'),
              State(layout.IDs.drop_d_period_type_value, 'value'),
              Input(layout.IDs.radio_b_sales_as, 'value'),
              Input(layout.IDs.button_show, 'n_clicks'),
              )
def update_sunburst(prd_type, prd, sales_as):
    sales_as = d.SalesAs(sales_as)
    return layout.FiguresUpdater.update_sunburst_section(prd_type, prd, sales_as)


@app.callback(Output(layout.IDs.stocks_evolution_bar, 'figure'),
              State(layout.IDs.radio_b_period_type, 'value'),
              State(layout.IDs.drop_d_period_type_value, 'value'),
              Input(layout.IDs.button_show, 'n_clicks'),
              )
def update_stock_bars(prd_type, prd):
    return layout.FiguresUpdater.update_stocks_evolution_bar(prd_type, prd)


app.run_server(debug=True)
