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
    graphs = 'graphs_id'
    parameters = 'parameters_id'
    dashboard = 'dashboard_id'


class DashScreen:
    def __init__(self, name: str, div: html.Div):
        self.name: str = name
        self.Div: html.Div = div


dash_screens: dict[str:DashScreen] = {}


@staticmethod
def gsk_div():
    div: html.Div = html.Div(children=[html.Div(title='Achievements',
                                                id='gsk1',
                                                style={Naming.height: '25%'},
                                                children=[html.Div(style={Naming.display: Naming.flex,
                                                                          Naming.flex_direction: Naming.flex_col},
                                                                   children=[html.Div(title='Overall Achievements',
                                                                                      id='gsk1.1'),
                                                                             html.Div(title='Detailed Achievements',
                                                                                      children=[html.Div(),
                                                                                                ],
                                                                                      ),
                                                                             ],
                                                                   ),
                                                          ],
                                                ),
                                       html.Div(title='Achievements repartition',
                                                id='gsk2',
                                                children=[],
                                                style={Naming.height: '25%'},
                                                ),
                                       html.Div(id='gsk3',
                                                title='Achievements in time',
                                                children=[],
                                                style={Naming.height: '25%'},
                                                ),
                                       html.Div(title='Stocks / Sales history',
                                                id='gsk4',
                                                children=[],
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
                      children=[html.H1('Dashboard',
                                        style={'color': '#fc7b03',
                                               },
                                        ),
                                html.Hr(),
                                html.Div(title='Parameters',
                                         id=IDs.parameters,
                                         style={Naming.width: '20%',
                                                Naming.border: '1px solid black',
                                                },
                                         children=[html.Label('Parameters'),
                                                   ],
                                         ),
                                html.Hr(),
                                html.Div(title='Sales Graphs',
                                         id=IDs.graphs,
                                         style={Naming.width: '80%',
                                                Naming.border: '1px solid black',
                                                },
                                         children=[html.Label('Sales Graphs'),
                                                   dash_screens[Naming.gsk_screen].Div,
                                                   ],
                                         )
                                ],
                      style={Naming.display: Naming.flex,
                             Naming.flex_direction: Naming.flex_row,
                             Naming.height: '100%',
                             Naming.border: '1px solid black',
                             Naming.padding: '10px'},
                      )

app.run_server(debug=True)
