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
    Input(layout.IDs.radio, 'value'),
)
def update(value):
    print('im here')
    return (layout.Update.update_progress_section(d.SalesAs(d.SalesAs.volume)),
            layout.Update.update_progress_section(d.SalesAs(d.SalesAs.volume)),
            layout.Update.update_progress_section(d.SalesAs(d.SalesAs.volume)),
            layout.Update.update_progress_section(d.SalesAs(d.SalesAs.volume)))


app.run_server(debug=True)
