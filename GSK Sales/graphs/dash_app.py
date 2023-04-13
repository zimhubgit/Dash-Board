from datetime import datetime

import pandas as pnd
from dash import html, Dash, dcc


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


class DashScreen:
    def __init__(self, name: str, div: html.Div):
        self.name: str = name
        self.Div: html.Div = div


dash_screens: dict[str:DashScreen] = {}


def gsk_div():
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
                                                                             ],
                                                                   ),
                                                          html.Hr(),
                                                          html.Div(title='Sunburst repartition',
                                                                   id=IDs.sunburst_repartition,
                                                                   style={Naming.width: '50%',
                                                                          },
                                                                   children=[html.Label('Sunburst Graph'),
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
    dash_screens.update({Naming.gsk_screen: DashScreen(Naming.gsk_screen, div)})


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
                                             options=[{'label': 'Valeur', 'value': 'GBP'},
                                                      {'label': 'Volume', 'value': 'units'},
                                                      ],
                                             ),
                              html.Hr(),
                              html.Div(title='All periods Overall achievements',
                                       id=IDs.all_periods_overall_achievements,
                                       style={Naming.display: Naming.flex,
                                              Naming.flex_direction: Naming.flex_row,
                                              Naming.height: '30%',
                                              },
                                       children=[html.Div(title='GSK Month',
                                                          id=IDs.gsk_month_indic,
                                                          style={Naming.width: '25%',
                                                                 },
                                                          children=[html.Label('Month Achievements',
                                                                               ),
                                                                    ]
                                                          ),
                                                 html.Hr(),
                                                 html.Div(title='GSK Quarter',
                                                          id=IDs.gsk_quarter_indic,
                                                          style={Naming.width: '25%',
                                                                 },
                                                          children=[html.Label('Quarter Achievements',
                                                                               ),
                                                                    ]
                                                          ),
                                                 html.Hr(),
                                                 html.Div(title='GSK Half',
                                                          id=IDs.gsk_half_indic,
                                                          style={Naming.width: '25%',
                                                                 },
                                                          children=[html.Label('Half year Achievements',
                                                                               ),
                                                                    ]
                                                          ),
                                                 html.Hr(),
                                                 html.Div(title='GSK Year',
                                                          id=IDs.gsk_year_indic,
                                                          style={Naming.width: '25%',
                                                                 },
                                                          children=[html.Label('Year Achievements',
                                                                               ),
                                                                    ]
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
                                                                    nav_bar(),
                                                                    ],
                                                          ),
                                                 html.Hr(),
                                                 html.Div(title='Sales Graphs',
                                                          id=IDs.graphs,
                                                          style={Naming.width: '85%',
                                                                 Naming.padding: '10px'},
                                                          children=[html.H3('Sales Graphs'),
                                                                    dash_screens[Naming.gsk_screen].Div,
                                                                    ],
                                                          ),
                                                 ],
                                       ),
                              ],
                    )


def load():
    gsk_div()


load()

app = Dash(__name__)

app.layout = dash_structure()

app.run_server(debug=True)
