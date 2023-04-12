from datetime import datetime

import pandas as pnd
from dash import html, Dash


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


class IDs:
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


@staticmethod
def gsk_div():
    div: html.Div = html.Div(children=[html.Div(title='Achievements',
                                                id=IDs.gsk,
                                                style={Naming.height: '25%'},
                                                children=[html.H4('Achievements',
                                                                  style={}),
                                                          html.Br(),
                                                          html.Div(id=IDs.achievements,
                                                                   style={Naming.display: Naming.flex,
                                                                          Naming.flex_direction: Naming.flex_row},
                                                                   children=[html.Label('Overall Achievements'),
                                                                             html.Div(title='Overall Achievements',
                                                                                      id=IDs.overall_achievements,
                                                                                      style={}),
                                                                             html.Div(title='Detailed Achievements',
                                                                                      id=IDs.detailed_achievements,
                                                                                      style={},
                                                                                      children=[html.Label(
                                                                                          'Detailed Achievements'),
                                                                                      ],
                                                                                      ),
                                                                             ],
                                                                   ),
                                                          ],
                                                ),
                                       html.Div(title='Achievements repartition',
                                                id=IDs.achievements_repartition,
                                                style={Naming.flex_direction: Naming.flex_row,
                                                       Naming.height: '25%',
                                                       },
                                                children=[html.Div(id=IDs.funnel_repartition,
                                                                   style={Naming.width: '50%',
                                                                          },
                                                                   children=[html.Label('Funnel Graph'),
                                                                             ],
                                                                   ),
                                                          html.Hr(),
                                                          html.Div(id=IDs.sunburst_repartition,
                                                                   style={Naming.width: '50%',
                                                                          },
                                                                   children=[html.Label('Sunburst Graph'),
                                                                             ],
                                                                   ),
                                                          ],
                                                ),
                                       html.Div(id=IDs.time_achievements,
                                                title='Achievements in time',
                                                children=[html.H4('Achievements in time'),
                                                          ],
                                                style={Naming.height: '25%'},
                                                ),
                                       html.Div(title='Stocks / Sales history',
                                                id=IDs.stocks,
                                                children=[html.H4('Stocks / Sales history'),
                                                          ],
                                                style={Naming.height: '25%'},
                                                )
                                       ],
                             style={Naming.display: Naming.flex,
                                    Naming.flex_direction: Naming.flex_col},
                             )
    dash_screens.update({Naming.gsk_screen: DashScreen(Naming.gsk_screen, div)})


def load():
    gsk_div()


load()

app = Dash(__name__)

app.layout = html.Div(id=IDs.dashboard,
                      children=[html.Div('Dashboard',
                                         style={'color': '#fc7b03',
                                                Naming.height: '10%',
                                                Naming.border: '1px solid black',
                                                },
                                         ),
                                html.Div(style={Naming.display: Naming.flex,
                                                Naming.flex_direction: Naming.flex_row,
                                                Naming.height: '90%'
                                                },
                                         children=[html.Div(title='Parameters',
                                                            id=IDs.parameters,
                                                            style={Naming.width: '15%',
                                                                   },
                                                            children=[html.H3('Parameters'),
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
                      style={Naming.display: Naming.flex,
                             Naming.flex_direction: Naming.flex_col,
                             Naming.border: '1px solid black',
                             Naming.padding: '10px',
                             },
                      )

app.run_server(debug=True)
