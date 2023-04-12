from datetime import datetime

import pandas as pnd
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output, State

import periods
from src import name_space as nm

data_dict = pnd.read_excel('/home/nazim/Devs/GSK Sales/output/GSK SALES.xlsx', sheet_name=None)
sales_df_22 = data_dict['2022']
sales_df_23 = data_dict['2023']
update_date = pnd.to_datetime(sales_df_23[nm.GSK.ColName.UPDATED_ON].values[0])
WEEK_DATES_DICO_23: dict[str, pnd.Timestamp] = periods.PeriodsDates.get_weeks_ends(update_date)
WEEK_DATES_DICO_22: dict[str, pnd.Timestamp] = periods.PeriodsDates.get_weeks_ends(pnd.Timestamp(2022, 12, 31))
BRANDS_LIST: list[str] = sales_df_23[nm.GSK.ColName.BRAND].unique().tolist()

DTD_DATES: list[dict[str, pnd.Timestamp]] = [
    {'label': f'{pnd.to_datetime(value).day}/{pnd.to_datetime(value).month}/{pnd.to_datetime(value).year}',
     'value': value} for
    value in sales_df_23[sales_df_23[
                             nm.GSK.ColName.PERIOD_TYPE] == nm.GSK.Naming.PERIOD_TYPE_DAILY][
        nm.GSK.ColName.DATE].unique()]

WTD_DATES: list[dict[str, pnd.Timestamp]] = [{'label': label, 'value': value} for (label, value) in
                                             periods.PeriodsDates.get_weeks_ends(sales_df_23[sales_df_23[
                                                                                                 nm.GSK.ColName.PERIOD_TYPE] == nm.GSK.Naming.PERIOD_TYPE_Weekly][
                                                                                     nm.GSK.ColName.DATE].max()).items()]

MTD_DATES: list[dict[str, pnd.Timestamp]] = [{'label': value.strftime('%B'), 'value': value} for value in sales_df_23[
    sales_df_23[nm.GSK.ColName.PERIOD_TYPE] == nm.GSK.Naming.PERIOD_TYPE_MTD].groupby(
    sales_df_23[nm.GSK.ColName.DATE].dt.month)[nm.GSK.ColName.DATE].max().tolist()]

QTD_DATES: list[dict[str, pnd.Timestamp]] = [{'label': f'Q{value.quarter}', 'value': value} for value in sales_df_23[
    sales_df_23[nm.GSK.ColName.PERIOD_TYPE] == nm.GSK.Naming.PERIOD_TYPE_QTD].groupby(
    sales_df_23[nm.GSK.ColName.DATE].dt.month)[nm.GSK.ColName.DATE].max().tolist()]

STD_DATES: list[dict[str, pnd.Timestamp]] = [
    {'label': f'S{(value.quarter if value.quarter in [1, 2] else 2)}', 'value': value} for value in sales_df_23[
        sales_df_23[nm.GSK.ColName.PERIOD_TYPE] == nm.GSK.Naming.PERIOD_TYPE_STD].groupby(
        sales_df_23[nm.GSK.ColName.DATE].dt.month)[nm.GSK.ColName.DATE].max().tolist()]

YTD_DATES: list[dict[str, pnd.Timestamp]] = [{'label': value.strftime('%B'), 'value': value} for value in sales_df_23[
    sales_df_23[nm.GSK.ColName.PERIOD_TYPE] == nm.GSK.Naming.PERIOD_TYPE_YTD].groupby(
    sales_df_23[nm.GSK.ColName.DATE].dt.month)[nm.GSK.ColName.DATE].max().tolist()]

PERIOD_TYPES: list[str] = [p_type if len(p_type) == 3 else p_type.capitalize() for p_type in
                           sales_df_23[nm.GSK.ColName.PERIOD_TYPE].unique().tolist()]

mode_dict: [str, dict[str, str]] = dict(
    units=dict(actual=nm.GSK.ColName.UNIT_SALES, target=nm.GSK.ColName.RFC_UNIT_COL),
    values=dict(actual=nm.GSK.ColName.VALUE_SALES, target=nm.GSK.ColName.RFC_VALUE_COL))

periods_options: dict[str, list[dict[str, pnd.Timestamp]]] = dict(DAILY=DTD_DATES,
                                                                  WEEKLY=WTD_DATES,
                                                                  MTD=MTD_DATES,
                                                                  QTD=QTD_DATES,
                                                                  STD=STD_DATES,
                                                                  YTD=YTD_DATES)

app = Dash(__name__)

app.layout = html.Div([
    html.Div(children=[
        html.H4('Paramétres'),
        html.Label('Data source:'),
        dcc.Dropdown(
            id='data_source_id',
            options=['GSK', 'AT PHARMA', 'IQVIA'],
            value=['GSK'],
            multi=True
        ),
        html.Br(),
        html.Label('Sales in:'),
        dcc.RadioItems(
            id="val_unit_radios_id",
            options=[{'label': 'Values', 'value': 'values'}, {'label': 'Units', 'value': 'units'}],
            value='units',
            inline=True,
            labelStyle={"font-size": "10px",
                        # "min-height":"1rem",
                        },
        ),
        html.Br(),
        html.Label('Periods:'),
        html.Div([
            dcc.RadioItems(
                id='periods_id',
                options=[{'label': value, 'value': value.upper()} for value in PERIOD_TYPES],
                value=nm.GSK.Naming.PERIOD_TYPE_MTD,
                inline=True,
                labelStyle={"font-size": "10px",
                            # "min-height":"1rem",
                            },
                inputStyle={"font-size": "10px",
                            # "min-height":"1rem",
                            },
            ),
        ]),
        html.Br(),
        dcc.Dropdown(
            id='month_id',
            options=periods_options,
            value=update_date,
            searchable=True,
            clearable=False
        ),
        html.Br(),
        html.Label('Brands'),
        dcc.Dropdown(
            id='brand_id',
            options=BRANDS_LIST,
            value=BRANDS_LIST[0],
            searchable=True,
            clearable=False
        ),
        # html.Button(
        #     id='period_button_id',
        #     n_clicks=0,
        #     children='Show'
        # )
    ], style={'padding': 10, 'flex': 1}),
    html.Hr(),
    html.Div(children=[
        html.Div(children=[
            html.H4('Réalisations'),
            dcc.Graph(id='graph'),
        ], style={'padding': 10, 'flex': 1}),
        html.Hr(),
        html.Div(children=[
            html.H4('Répartition des réalisations'),
            dcc.Graph(id='sunburst_id'),
        ], style={'padding': 10, 'flex': 1})],
        style={'padding': 10, 'flex': 4.5, 'display': 'flex', 'flex-direction': 'row'}),
    html.Hr(),
], style={'display': 'flex', 'flex-direction': 'row'})


@app.callback(
    Output('val_unit_radios_id', 'options'),
    Input('data_source_id', 'value'))
def get_sales_options(value):
    if 'AT PHARMA' in value:
        return [{'label': 'Values', 'value': 'values', 'disabled': True}, {'label': 'Units', 'value': 'units'}]
    else:
        return [{'label': 'Values', 'value': 'values'}, {'label': 'Units', 'value': 'units'}]


@app.callback(
    Output('month_id', 'options'),
    Output('month_id', 'value'),
    Input('periods_id', 'value'))
def get_period_type_elements(value):
    return periods_options[value], list(periods_options[value][0].values())[0]


@app.callback(
    Output("graph", "figure"),
    Input("val_unit_radios_id", "value"),
    # Input('period_button_id', 'n_clicks'),
    State('periods_id', 'value'),
    Input('month_id', 'value'),
    Input('brand_id', 'value'))
def update_indicator_chart(value, input1, input2, input3):
    return indicator_figure(value, input1, input2, input3)


@app.callback(
    Output("sunburst_id", "figure"),
    Input("val_unit_radios_id", "value"),
    # Input('period_button_id', 'n_clicks'),
    State('periods_id', 'value'),
    Input('month_id', 'value'),
    Input('brand_id', 'value'))
def update_sunburst_chart(value, input1, input2, input3):
    return sunburst_chart(value, input1, input2, input3)


def indicator_figure(mode: str, period_type: str,
                     date: pnd.Timestamp, brand: str) -> go.Figure:
    values_dict = achievement(mode, period_type, date, brand)
    target: float = values_dict['target']
    actual: float = values_dict['actual']
    past_actual: float = values_dict['past actual']
    margin: float = .15
    gauge_range = sorted([target, actual, past_actual])[-1] * 1.1
    # progress_over_time = progression_over_time_mile_stone(actual_progress=actual,
    #                                                       target_progress=target, )
    fig = go.Figure()
    fig.add_trace(go.Indicator(
        mode="number+gauge+delta", value=actual,
        domain={'x': [0, 1], 'y': [0.5, 1]},
        delta={'reference': target, 'position': "top"},
        title={'text': f"<b>Achievement</b><br><span style='color: gray; font-size:0.8em'>{mode}</span>",
               'font': {"size": 14}},
        gauge={
            'axis': {'range': [None, gauge_range]},
            'threshold': {
                'line': {'color': "red", 'width': 2},
                'thickness': 1, 'value': target},

            'bgcolor': "white",
            'steps': [
                {'range': [0, past_actual], 'color': "turquoise"}],
            'bar': {'color': "#eb7d34"}}))

    fig.add_trace(go.Indicator(
        mode='delta',
        value=(actual + target) / target * 100,
        delta={'reference': 100, 'suffix': '%',
               'increasing': {'color': get_delta_color(.9)}},
        domain={'x': [0.25, .75], 'y': [0.2, 0.5]}
    ))
    return fig


def sunburst_chart(mode: str, period_type: str,
                   date: pnd.Timestamp, brand: str) -> go.Figure:
    labels_dict: dict[str, list[object]] = sunburst_hierarchy(sunburst_data(mode, period_type, date, brand), mode)
    fig = go.Figure()
    fig.add_trace(go.Sunburst(
        values=labels_dict.get('values'),
        labels=labels_dict.get('labels'),
        parents=labels_dict.get('parents'),
        branchvalues='total',
        insidetextorientation='radial',
    ))

    return fig


def achievement(mode: str, period_type: str, date: pnd.Timestamp, brand: str) -> dict[str, float]:
    period: str = 'MTD' if period_type in ['Daily'] else period_type
    actual_23: float
    target_23: float
    actual_22: float
    timestamp = pnd.to_datetime(date)
    data = sales_df_23[sales_df_23[nm.GSK.ColName.PERIOD_TYPE] == period]
    data = data[data[nm.GSK.ColName.DATE] == timestamp]
    data = data[data[nm.GSK.ColName.SKU] == brand]
    target_23 = data[mode_dict[mode]['target']].values[0]
    actual_23 = data[mode_dict[mode]['actual']].values[0]

    data = sales_df_22[sales_df_22[nm.GSK.ColName.PERIOD_TYPE] == period]
    data = data[data[nm.GSK.ColName.DATE] == timestamp]
    data = data[data[nm.GSK.ColName.SKU] == brand]
    if data.empty:
        actual_22 = 0
    else:
        actual_22 = data[mode_dict[mode]['actual']].values[0]
    return {'actual': actual_23, 'target': target_23, 'past actual': actual_22}


def sunburst_data(mode: str, period_type: str,
                  date: pnd.Timestamp, brand: str) -> dict[str:object]:
    sunburst_df: pnd.DataFrame = sales_df_23[
        sales_df_23[nm.GSK.ColName.PERIOD_TYPE] == period_type]
    if brand != nm.GSK.Naming.ALL_SKUs:
        sunburst_df = sunburst_df[sunburst_df[nm.GSK.ColName.BRAND] == brand]
    sunburst_df = sunburst_df[sunburst_df[nm.GSK.ColName.DATE] == date]
    sunburst_df['RACINE'] = 'GSK Sales'
    sunburst_df['REALISATIONS'] = sunburst_df[mode_dict[mode]['actual']] / sunburst_df[mode_dict[mode]['target']] * 100
    return sunburst_df


def sunburst_hierarchy(data: pnd.DataFrame, mode: str) -> dict[str, list[str]]:
    parents: list[str] = []
    labels: list[str] = []
    values: list[float] = []
    root: str = data['RACINE'].values[0]
    for idx, row in data.iterrows():
        value = row.loc[mode_dict[mode]['actual']]
        if pnd.isna(value) or value == 0:
            continue
        brand = row.loc['BRAND']
        sku_type = row.loc['SKU TYPE']
        sku = row.loc['SKU']
        if 'BRAND - SKU' in sku_type:
            parents.append(root)
            labels.append(sku)
            values.append(value)
        elif 'SKU' in sku_type:
            parents.append(brand)
            labels.append(sku)
            values.append(value)
        elif 'BRAND' in sku_type:
            parents.append(root)
            labels.append(sku)
            values.append(value)
        elif 'ALL' in sku_type:
            parents.insert(0, '')
            labels.insert(0, root)
            values.insert(0, value)
    return {'labels': labels, 'parents': parents, 'values': values}


def get_time_progress(period_type: str) -> dict[str:datetime]:
    pass

    # time_dict: dict[str, datetime] = {}
    # actual_time = ACTUAL_DATA[nm.GSK.ColName.UPDATED_ON].values[0]
    # ref_period: int
    # period_df = ACTUAL_DATA[ACTUAL_DATA[nm.GSK.ColName.PERIOD_TYPE] == period_type]
    # if period_type == nm.GSK.Naming.PERIOD_TYPE_DAILY:
    #     ref_period = period_df[period_df[nm.GSK.ColName.DATE].dt.month == actual_time.month].max().day
    #
    # if period_type == nm.GSK.Naming.PERIOD_TYPE_Weekly:
    #     ref_period = period_df[period_df[nm.GSK.ColName.DATE].dt.month == actual_time.month].max().week
    #
    # if period_type == nm.GSK.Naming.PERIOD_TYPE_MTD:
    #     ref_period = period_df[period_df[nm.GSK.ColName.DATE].dt.month == actual_time.month].max().month
    #
    # if period_type == nm.GSK.Naming.PERIOD_TYPE_QTD:
    #     ref_period = period_df[period_df[nm.GSK.ColName.DATE].dt.month == actual_time.month].max().quarter


def progression_over_time_mile_stone(start: datetime, end: datetime, actual_date: datetime,
                                     actual_progress: float,
                                     target_progress: float) -> float:
    time_progression = (end - actual_date).days / (end - start).days
    value_progression = actual_progress / target_progress
    return time_progression - value_progression - 1


def get_delta_color(progression: float) -> str:
    default_red_color: str = '#FF4136'
    defautl_green_color: str = '#3D9970'
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
        return defautl_green_color
    elif progression < 1.1:
        return dark_green_color
    else:
        return blue_color


def get_quarter_date(period_type: str, year: int) -> pnd.Timestamp:
    if period_type == 'Q1':
        return pnd.Timestamp(year, 3, 31)
    if period_type == 'Q2':
        return pnd.Timestamp(year, 6, 30)
    if period_type == 'Q2':
        return pnd.Timestamp(year, 9, 30)
    if period_type == 'Q4':
        return pnd.Timestamp(year, 12, 31)


def get_half_year_date(period_type: str, year: int) -> pnd.Timestamp:
    if period_type == 'S1':
        return get_quarter_date('Q2', year)
    if period_type == 'S2':
        return get_quarter_date('Q4', year)


# indicator_figure(mode='units', period_type='QTD', date=datetime(2023, 3, 30))
app.run_server(debug=True)
