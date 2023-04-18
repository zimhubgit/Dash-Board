from datetime import datetime

import pandas as pnd
import plotly.graph_objects as go
from dash import html, Dash, dcc, Output, Input

import parametres.src.name_space as nm


class DashScreen:
    def __init__(self, name: str, div: html.Div):
        self.name: str = name
        self.Div: html.Div = div


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
            raise Exception('Sales as error')


sales_as_vol: SalesAs = SalesAs(SalesAs.volume)
sales_as_val: SalesAs = SalesAs(SalesAs.value)


class PeriodsDates:

    @staticmethod
    def get_weeks_ends(end_date: pnd.Timestamp) -> dict[str, pnd.Timestamp]:
        start_date = datetime(year=end_date.year, month=1, day=1, hour=16)
        year_weeks_dates: pnd.DatetimeIndex = pnd.date_range(start_date, end_date, freq='W-THU')
        weeks_dict: [str, pnd.Timestamp] = {}
        month = 1
        week_number = 1
        for week in year_weeks_dates:
            if week.month != month:
                month = week.month
                week_number = 1
            week.strftime('%B')
            key: str = f"{week.strftime('%B')} - W{week_number} (au {week.day}/{week.month})"
            week_number = week_number + 1
            weeks_dict.update({key: week})
        return weeks_dict


class GskData:
    actual: str = 'actual'
    target: str = 'target'
    sales = pnd.read_excel('/home/nazim/Dev Projects/Dash Board/GSK Sales/output/GSK SALES.xlsx', sheet_name=None)
    actual_year = '2023'
    last_year = '2022'
    update_date = pnd.to_datetime(sales['2023'][nm.GSK.ColName.UPDATED_ON].values[0])

    @staticmethod
    def achievements(sales_df: pnd.DataFrame, sales_as: SalesAs, sku: str, period_type: str, date: pnd.Timestamp) -> \
            dict[str, float]:
        achievements: dict[str, float] = {}
        data_df = sales_df[sales_df[nm.GSK.ColName.PERIOD_TYPE] == period_type]
        data_df = data_df[data_df[nm.GSK.ColName.SKU] == sku]
        data_df[nm.GSK.ColName.DATE] = pnd.to_datetime(data_df[nm.GSK.ColName.DATE])
        data_df = data_df[data_df[nm.GSK.ColName.DATE] == date]
        if data_df.empty:
            achievements.update({GskData.actual: 0,
                                 GskData.target: 0,
                                 },
                                )
            return achievements

        achievements.update({GskData.actual: data_df[sales_as.achieved].values[0],
                             GskData.target: data_df[sales_as.rfc].values[0],
                             },
                            )
        return achievements

    @staticmethod
    def actual_sales() -> pnd.DataFrame:
        return GskData.sales[GskData.actual_year]

    @staticmethod
    def ly_sales() -> pnd.DataFrame:
        return GskData.sales[GskData.last_year]


class GskGraph:
    year_2022 = '2022'

    sales_as: [str, dict[str, str]] = dict(
        volume=dict(actual=nm.GSK.ColName.UNIT_SALES, target=nm.GSK.ColName.RFC_UNIT_COL),
        value=dict(actual=nm.GSK.ColName.VALUE_SALES, target=nm.GSK.ColName.RFC_VALUE_COL))

    @staticmethod
    def gsk_div() -> dict[str, DashScreen]:
        div: html.Div = html.Div(title='GSK',
                                 id=IDs.gsk,
                                 style={Naming.display: Naming.flex,
                                        Naming.flex_direction: Naming.flex_col,
                                        },
                                 children=[html.Div(title='Achievements',
                                                    id=IDs.achievements,
                                                    style={Naming.height: '25%',
                                                           Naming.display: Naming.flex,
                                                           Naming.flex_direction: Naming.flex_row,
                                                           Naming.border: '1px solid black'},
                                                    children=[html.H4('Achievements',
                                                                      style={},
                                                                      ),
                                                              html.Div(title='Overall achievements',
                                                                       id=IDs.overall_achievements,
                                                                       style={Naming.border: '1px solid black',
                                                                              Naming.width: '50%',
                                                                              },
                                                                       children=[html.Label('Overall Achievements'),
                                                                                 dcc.Graph(
                                                                                     id=IDs.sub_overall_indicator),
                                                                                 ],
                                                                       ),
                                                              html.Hr(),
                                                              html.Div(title='Achievements details',
                                                                       id=IDs.detailed_achievements,
                                                                       style={Naming.border: '1px solid black',
                                                                              Naming.width: '50%',
                                                                              },
                                                                       children=[html.Label('Detailed Achievements'),
                                                                                 ],
                                                                       ),
                                                              ],
                                                    ),
                                           html.Hr(),
                                           html.Div(title='Sales repartition',
                                                    id=IDs.achievements_repartition,
                                                    style={Naming.flex_direction: Naming.flex_row,
                                                           Naming.display: Naming.flex,
                                                           Naming.height: '25%',
                                                           },
                                                    children=[html.H4('Sales repartition'),
                                                              html.Div(title='Funnel repartition',
                                                                       id=IDs.funnel_repartition,
                                                                       style={Naming.width: '50%',
                                                                              },
                                                                       children=[html.Label('Funnel Graph'),
                                                                                 dcc.Graph(id=IDs.funnel_graph),
                                                                                 ],
                                                                       ),
                                                              html.Hr(),
                                                              html.Div(title='Sunburst repartition',
                                                                       id=IDs.sunburst_repartition,
                                                                       style={Naming.width: '50%',
                                                                              },
                                                                       children=[html.Label('Sunburst Graph'),
                                                                                 dcc.Graph(id=IDs.sunburst_graph),
                                                                                 ],
                                                                       ),
                                                              ],
                                                    ),
                                           html.Hr(),
                                           html.Div(title='Achievements over time',
                                                    id=IDs.time_achievements,
                                                    children=[html.H4('Achievements in time'),
                                                              ],
                                                    style={Naming.height: '25%',
                                                           },
                                                    ),
                                           html.Hr(),
                                           html.Div(title='Stocks over time',
                                                    id=IDs.stocks,
                                                    children=[html.H4('Stocks / Sales history'),
                                                              ],
                                                    style={Naming.height: '25%',
                                                           },
                                                    )
                                           ],
                                 )
        return {Naming.gsk_screen: DashScreen(Naming.gsk_screen, div)}

    @staticmethod
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

    @staticmethod
    def indicator(achieved: float, target: float, ly_achieved: float, sales_as: SalesAs, label: str) -> go.Figure:
        # progress_over_time = progression_over_time_mile_stone(actual_progress=actual,
        #                                                       target_progress=target, )
        gauge_range = sorted([target, achieved, ly_achieved])[-1] * 1.1
        fig = go.Figure()
        fig.add_trace(go.Indicator(
            mode="number+gauge+delta", value=achieved,
            domain={'x': [0, 1], 'y': [0.5, 1]},
            delta={'reference': target, 'position': "top"},
            title={'text': f"<b>{label}</b><br><span style='color: gray; font-size:0.8em'>{sales_as.name}</span>",
                   'font': {"size": 14}},
            gauge={
                'axis': {'range': [None, gauge_range]},
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 1, 'value': target},

                'bgcolor': 'white',
                'steps': [
                    {'range': [0, ly_achieved], 'color': '#DDDDDD'}],
                'bar': {'color': '#10BA4D'}}))
        fig.add_trace(go.Indicator(
            mode='delta',
            value=((achieved + target) / target * 100) if target != 0 else 0,
            delta={'reference': 100, 'suffix': '%',
                   'increasing': {'color': GskGraph.get_delta_color(.9)}},
            domain={'x': [0.25, .75], 'y': [0.2, 0.5]}
        ))
        return fig

    @staticmethod
    def overall_indicators(sales_as: str) -> tuple[go.Figure, go.Figure, go.Figure, go.Figure]:
        sale_as = sales_as_vol if sales_as == sales_as_vol.name else sales_as_val
        figures: list[go.Figure] = []
        period_types = ['MTD', 'QTR', 'STD', 'YTD']
        sku = nm.GSK.Naming.ALL_SKUs
        actual_sales_df = GskData.actual_sales()
        ly_sales_df = GskData.ly_sales()
        ly_date: pnd.Timestamp
        for period_type in period_types:
            date = actual_sales_df[actual_sales_df[nm.GSK.ColName.PERIOD_TYPE] == period_type][
                nm.GSK.ColName.DATE].max()
            if period_type == 'MTD':
                ly_date = date + pnd.offsets.MonthEnd(0)
            elif period_type == 'QTR':
                ly_date = date + pnd.offsets.QuarterEnd(0)
            elif period_type == 'STD':
                ly_date = pnd.Timestamp(year=date.year - 1, month=6, day=30,
                                        hour=16) if date.quarter < 3 else pnd.Timestamp(year=date.year - 1, month=12,
                                                                                        day=31, hour=16)
                print()
            elif period_type == 'YTD':
                ly_date = date + pnd.offsets.YearEnd(0)
            else:
                raise ValueError()
            actual_data_dict = GskData.achievements(actual_sales_df, sale_as, sku, period_type, date)
            target: float = actual_data_dict[GskData.target]
            achieved: float = actual_data_dict[GskData.actual]
            ly_data_dict = GskData.achievements(ly_sales_df, sale_as, sku, period_type, ly_date)
            ly_achieved: float = ly_data_dict[GskData.actual]

            figures.append(GskGraph.indicator(achieved, target, ly_achieved, sale_as, (period_type + ' Achievements')))

        return figures[0], figures[1], figures[2], figures[3]


class Naming:
    children_num = 'NUMBER OF CHILDREN'
    disposition = 'DISPOSITION'
    orientation = 'ORIENTATION'
    flex_direction = 'flex-direction'
    flex_row = 'row'
    flex_col = 'column'
    width = 'width'
    height = 'height'
    display = 'display'
    flex = 'flex'
    border = 'border'
    padding = 'padding'
    gsk_screen = 'GSK'
    text_deco = 'text-decoration'
    underline = 'underline'
    font_weight = 'font-weight'
    bold = 'bold',
    color = 'color'


class IDs:
    sub_brand_indicator = 'sub_brand_indicator_graph_id'
    sub_overall_indicator = 'sub_overall_indicator_graph_id'
    sunburst_graph = 'sunburst_graph_id'
    funnel_graph = 'funnel_graph_id'
    graph_overall_year_indicator = 'graph_indicator_overall_year_id'
    graph_overall_quarter_indicator = 'graph_indicator_overall_quarter_id'
    graph_overall_half_indicator = 'graph_indicator_overall_half_id'
    graph_overall_month_indicator = 'graph_indicator_overall_month_id'
    vol_val_rb = 'vol_val_id'
    gsk_year_indic = 'gsk_year_indicator_id'
    gsk_half_indic = 'gsk_half_indicator_id'
    gsk_quarter_indic = 'gsk_quarter_indicator_id'
    gsk_month_indic = 'gsk_month_indicator_id'
    all_periods_overall_achievements = 'all_periods_overall_id'
    show_b = 'show_button_id'
    periods_dd = 'periods_list_id'
    periods_rb = 'periods_id'
    brands_dd = 'brands_id'
    data_source_dd = 'datasource_id'
    nav_bar = 'nav_bar_id'
    stocks = 'stocks_id'
    time_achievements = 'achievements_in_time_id'
    achievements = 'achievements_id'
    graphs = 'graphs_id'
    parameters = 'parameters_id'
    dashboard = 'dashboard_id'
    gsk = 'gsk_id'
    # Achievements Div
    overall_achievements = 'overall_id'
    overall_indicator = 'overall_indicator_id'
    detailed_achievements = 'detailed_id'
    # Repartition Div
    achievements_repartition = 'repartition_id'
    funnel_repartition = 'sankey_id'
    sunburst_repartition = 'sunburst_id'


class DashBoard:
    dash_screens: dict[str:DashScreen] = {}

    @staticmethod
    def nav_bar() -> html.Div:
        return html.Div(id=IDs.nav_bar,
                        style={Naming.padding: '10px',
                               },
                        children=[html.Label('Data Sources:',
                                             style={Naming.text_deco: Naming.underline,
                                                    Naming.font_weight: Naming.bold,
                                                    Naming.color: 'grey',
                                                    },
                                             ),
                                  dcc.Dropdown(id=IDs.data_source_dd,
                                               options=['GSK', 'AT PHARMA', 'IQVIA'],
                                               value='GSK',
                                               clearable=False,
                                               searchable=True,
                                               multi=True,
                                               ),
                                  html.Hr(),
                                  html.Br(),
                                  html.Label('Brands:',
                                             style={Naming.text_deco: Naming.underline,
                                                    Naming.font_weight: Naming.bold,
                                                    Naming.color: 'grey',
                                                    }),
                                  dcc.Dropdown(id=IDs.brands_dd,
                                               options=['All', 'Augmentin', 'Clamoxyl', 'Ventoline', 'Flixotide',
                                                        'Seretide'],
                                               value='All',
                                               clearable=False,
                                               searchable=True,
                                               ),
                                  html.Hr(),
                                  html.Br(),
                                  html.Label('Periods:',
                                             style={Naming.text_deco: Naming.underline,
                                                    Naming.font_weight: Naming.bold,
                                                    Naming.color: 'grey',
                                                    },
                                             ),
                                  dcc.RadioItems(id=IDs.periods_rb,
                                                 options=[{'label': 'Months', 'value': 'MONTHLY'},
                                                          {'label': 'Weeks', 'value': 'WEEKLY'},
                                                          {'label': 'Days', 'value': 'DTD'},
                                                          {'label': 'Quarters', 'value': 'QTD'},
                                                          {'label': 'Halfs', 'value': 'STD'},
                                                          {'label': 'Year', 'value': 'YTD'},
                                                          ],
                                                 value='MONTHLY',
                                                 ),
                                  html.Br(),
                                  html.Label('Selected period: MTD'),
                                  dcc.Dropdown(id=IDs.periods_dd,
                                               options=['Period 1', 'Period 2', 'Period 3'],
                                               value='Period 1',
                                               clearable=False,
                                               searchable=True,
                                               ),
                                  html.Hr(),
                                  html.Br(),
                                  html.Button(id=IDs.show_b,
                                              style={'background': '#64B5F6'},
                                              children=['Afficher'],
                                              n_clicks=0),
                                  ],
                        )

    @staticmethod
    def dash_structure() -> html.Div:
        return html.Div(id=IDs.dashboard,
                        style={Naming.display: Naming.flex,
                               Naming.flex_direction: Naming.flex_col,
                               Naming.border: '1px solid black',
                               Naming.padding: '10px',
                               },
                        children=[html.Div('Dashboard',
                                           style={'color': '#fc7b03',
                                                  Naming.height: '10%',
                                                  Naming.border: '1px solid black',
                                                  },
                                           ),
                                  html.Hr(),
                                  html.Br(),
                                  dcc.RadioItems(id=IDs.vol_val_rb,
                                                 style={},
                                                 options=[{'label': 'Value', 'value': sales_as_val.name},
                                                          {'label': 'Volume', 'value': sales_as_vol.name},
                                                          ],
                                                 value=sales_as_val.name
                                                 ),
                                  html.Hr(),
                                  html.Div(title='All periods Overall achievements',
                                           id=IDs.all_periods_overall_achievements,
                                           style={Naming.display: Naming.flex,
                                                  Naming.flex_direction: Naming.flex_row,
                                                  Naming.height: '30%',
                                                  },
                                           children=[html.Label('Month Achievements',
                                                                ),
                                                     dcc.Graph(id=IDs.graph_overall_month_indicator,
                                                               style={Naming.width: '25%',
                                                                      Naming.height: '100%',
                                                                      Naming.padding: '10px',
                                                                      },
                                                               ),
                                                     html.Hr(),
                                                     dcc.Graph(id=IDs.graph_overall_quarter_indicator,
                                                               style={Naming.width: '25%',
                                                                      Naming.height: '100%',
                                                                      Naming.padding: '10px',
                                                                      },
                                                               ),
                                                     html.Hr(),
                                                     dcc.Graph(id=IDs.graph_overall_half_indicator,
                                                               style={Naming.width: '25%',
                                                                      Naming.height: '100%',
                                                                      Naming.padding: '10px',
                                                                      },
                                                               ),
                                                     html.Hr(),
                                                     dcc.Graph(id=IDs.graph_overall_year_indicator,
                                                               style={Naming.width: '25%',
                                                                      Naming.height: '100%',
                                                                      Naming.padding: '10px',
                                                                      },
                                                               ),
                                                     ]
                                           ),
                                  html.Hr(),
                                  html.Br(),
                                  html.Div(style={Naming.display: Naming.flex,
                                                  Naming.flex_direction: Naming.flex_row,
                                                  Naming.height: '60%'
                                                  },
                                           children=[html.Div(title='Parameters',
                                                              id=IDs.parameters,
                                                              style={Naming.width: '15%',
                                                                     },
                                                              children=[html.H3('Parameters'),
                                                                        DashBoard.nav_bar(),
                                                                        ],
                                                              ),
                                                     html.Hr(),
                                                     html.Div(title='Sales Graphs',
                                                              id=IDs.graphs,
                                                              style={Naming.width: '85%',
                                                                     Naming.padding: '10px'},
                                                              children=[html.H3('Sales Graphs'),
                                                                        DashBoard.dash_screens[Naming.gsk_screen].Div,
                                                                        ],
                                                              ),
                                                     ],
                                           ),
                                  ],
                        )


DashBoard.dash_screens.update(GskGraph.gsk_div())
app = Dash(__name__)
app.layout = DashBoard.dash_structure()


@app.callback(
    Output(IDs.graph_overall_month_indicator, "figure"),
    Output(IDs.graph_overall_quarter_indicator, "figure"),
    Output(IDs.graph_overall_half_indicator, "figure"),
    Output(IDs.graph_overall_year_indicator, "figure"),
    Input(IDs.vol_val_rb, "value"),
)
def update_indicators(value):
    return GskGraph.overall_indicators(value)
    # return GskGraph.indicator(20, 100, 97, sales_as_vol, 'Month Achievements'), \
    #     GskGraph.indicator(20, 280, 270, sales_as_vol, 'Quarter Achievements'), \
    #     GskGraph.indicator(20, 600, 595, sales_as_vol, 'Semester Achievements'), \
    #     GskGraph.indicator(20, 1100, 1000, sales_as_vol, 'Year Achievements')


# app.run_server(debug=True)
update_indicators('Volume')
