from dash import html, dcc
import plotly.graph_objects as go
import figures as fig
from name_space import NameMap as nm
import data as d


class IDs:
    sales_indicator_sect = 'sales_indicators_sect_id'
    mtd_sales_indicator = 'mtd_sales_indicator_id'
    qtd_sales_indicator = 'qtd_sales_indicator_id'
    std_sales_indicator = 'std_sales_indicator_id'
    ytd_sales_indicator = 'ytd_sales_indicator_id'

    sales_repartition_sect = 'sales_repartition_sect_id'
    sales_repartition_sunburst = 'sales_repartition_sunburst_id'
    sales_repartition_waterfall = 'sales_repartition_waterfall_id'

    radio = 'radio_id'


class Dash:
    @staticmethod
    def get() -> html.Div:
        return Section.assemble_sections()


class Section:

    @staticmethod
    def assemble_sections() -> html.Div:
        assembled_sections: html.Div = html.Div(style={nm.display: nm.flex,
                                                       nm.flex_direction: nm.flex_col,
                                                       },
                                                children=[Section.__1_sect_header(),
                                                          html.Hr(),
                                                          Section.__2_sect_progress(),
                                                          html.Hr(),
                                                          Section.__3_sect_progress_dist(),
                                                          ]
                                                )
        return assembled_sections

    @staticmethod
    def __1_sect_header() -> html.Div:
        return html.Div(style={nm.height: '15%',
                               nm.border: '1px solid black',
                               nm.bg_color: nm.solid_gsk_orange},
                        children=['GSK Dash Header',
                                  dcc.RadioItems(id=IDs.radio,
                                                 style={},
                                                 options=[{'label': 'Value', 'value': d.SalesAs(d.SalesAs.volume).name},
                                                          {'label': 'Volume', 'value': d.SalesAs(d.SalesAs.value).name},
                                                          ],
                                                 value=d.SalesAs(d.SalesAs.volume).name
                                                 ),
                                  ],
                        )

    @staticmethod
    def __2_sect_progress() -> html.Div:
        return html.Div(style={nm.height: '25%',
                               nm.border: '1px solid black',
                               },
                        children=[html.H4('Achievements',
                                          style={nm.height: '15%'},
                                          ),
                                  html.Div(title='Overall achievements',
                                           id=IDs.sales_indicator_sect,
                                           style={nm.border: '1px solid black',
                                                  nm.height: '10%',
                                                  nm.display: nm.flex,
                                                  nm.disposition: nm.flex_row
                                                  },
                                           children=[html.Div(style={nm.opacity: '1',
                                                                     nm.bg_color: nm.rgba(39, 132, 245, 0.4),
                                                                     nm.width: '25%',
                                                                     nm.padding: '10px',
                                                                     },
                                                              children=[dcc.Graph(id=IDs.mtd_sales_indicator),
                                                                        ],
                                                              ),
                                                     html.Hr(),
                                                     html.Div(style={nm.opacity: '1',
                                                                     nm.bg_color: nm.rgba(39, 132, 245, 0.4),
                                                                     nm.width: '25%',
                                                                     nm.padding: '10px',
                                                                     },
                                                              children=[dcc.Graph(id=IDs.qtd_sales_indicator),
                                                                        ],
                                                              ),
                                                     html.Hr(),
                                                     html.Div(style={nm.opacity: '1',
                                                                     nm.bg_color: nm.rgba(39, 132, 245, 0.4),
                                                                     nm.width: '25%',
                                                                     nm.padding: '10px',
                                                                     },
                                                              children=[dcc.Graph(id=IDs.std_sales_indicator),
                                                                        ],
                                                              ),
                                                     html.Hr(),
                                                     html.Div(style={nm.opacity: '1',
                                                                     nm.bg_color: nm.rgba(39, 132, 245, 0.4),
                                                                     nm.width: '25%',
                                                                     nm.padding: '10px',
                                                                     },
                                                              children=[dcc.Graph(id=IDs.ytd_sales_indicator),
                                                                        ],
                                                              ),
                                                     ],
                                           ),
                                  ],
                        )

    @staticmethod
    def __3_sect_progress_dist() -> html.Div:
        return html.Div(style={nm.height: '25%',
                               nm.border: '1px solid black',
                               },
                        children=[html.H4('Sales distribution',
                                          style={nm.height: '15%'},
                                          ),
                                  html.Div(id=IDs.sales_repartition_sect,
                                           style={nm.border: '1px solid black',
                                                  nm.height: '10%',
                                                  nm.display: nm.flex,
                                                  nm.disposition: nm.flex_row},
                                           children=[html.Div(style={nm.opacity: '1',
                                                                     nm.bg_color: nm.rgba(39, 132, 245, 0.4),
                                                                     nm.width: '50%',
                                                                     nm.padding: '10px',
                                                                     },
                                                              children=[dcc.Graph(id=IDs.sales_repartition_sunburst),
                                                                        ],
                                                              ),
                                                     html.Hr(),
                                                     html.Div(style={nm.opacity: '1',
                                                                     nm.bg_color: nm.rgba(39, 132, 245, 0.4),
                                                                     nm.width: '50%',
                                                                     nm.padding: '10px',
                                                                     },
                                                              children=[dcc.Graph(id=IDs.sales_repartition_waterfall),
                                                                        ],
                                                              )
                                                     ],
                                           ),
                                  ],
                        )


@staticmethod
def __4_sect_progress_hist() -> html.Div:
    pass


@staticmethod
def __5_sect_stock_hist() -> html.Div:
    pass


class Update:
    @staticmethod
    def update_progress_section(sales_as: d.SalesAs) -> go.Figure:
        return fig.indicator(achieved=11000, target=26000, label='MTD Progress', sales_as=d.SalesAs(d.SalesAs.volume),
                             ly_achieved=25000)

    @staticmethod
    def update_sunburst_section(sales_as: d.SalesAs) -> go.Figure:
        return fig.sunburst()

    @staticmethod
    def update_waterfall_section(sales_as: d.SalesAs) -> go.Figure:
        return fig.water_fall()
