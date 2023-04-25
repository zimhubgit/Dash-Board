from dash import Dash
import layout

app = Dash(__name__)
app.layout = layout.Dash.get()
app.run_server(debug=True)
