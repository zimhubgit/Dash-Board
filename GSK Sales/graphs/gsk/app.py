from dash import Dash, Input, Output
import layout
import data as d

app = Dash(__name__)
app.layout = layout.Dash.get()


@app.callback(
    Output(layout.IDs.mtd_sales_indicator, 'figure'),
    Output(layout.IDs.qtd_sales_indicator, 'figure'),
    Output(layout.IDs.std_sales_indicator, 'figure'),
    Output(layout.IDs.ytd_sales_indicator, 'figure'),
    Output(layout.IDs.sales_repartition_sunburst, 'figure'),
    Output(layout.IDs.sales_repartition_waterfall, 'figure'),
    Output(layout.IDs.sales_evolution_bar, 'figure'),
    Output(layout.IDs.stocks_evolution_bar, 'figure'),
    Input(layout.IDs.radio, 'value'),
)
def update(value):
    sales_as = d.SalesAs(d.SalesAs.volume)
    return (layout.Update.update_progress_section(sales_as),
            layout.Update.update_progress_section(sales_as),
            layout.Update.update_progress_section(sales_as),
            layout.Update.update_progress_section(sales_as),
            layout.Update.update_sunburst_section(sales_as),
            layout.Update.update_waterfall_section(sales_as),
            layout.Update.update_sales_evolution_bar(sales_as),
            layout.Update.update_stocks_evolution_bar(sales_as),
            )


app.run_server(debug=True)
