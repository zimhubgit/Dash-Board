from dash import html, dcc
import plotly.graph_objects as go
import figures as fig
from name_space import NameMap as nm
import data as d


class IDs:
    nav_bar_sect = 'navigation_bar_id'
    radio_b_data_source = 'data_source_radio_id'
    drop_d_brand = 'brand_drop_down_id'
    drop_d_sku = 'sku_drop_down_id'
    radio_b_period_type = 'period_type_radio_id'
    drop_d_period_type_value = 'period_type_value_drop_down_id'
    button_show = 'show_button_id'

    sales_indicator_sect = 'sales_indicators_sect_id'
    mtd_sales_indicator = 'mtd_sales_indicator_id'
    qtd_sales_indicator = 'qtd_sales_indicator_id'
    std_sales_indicator = 'std_sales_indicator_id'
    ytd_sales_indicator = 'ytd_sales_indicator_id'

    sales_repartition_sect = 'sales_repartition_sect_id'
    sales_repartition_sunburst = 'sales_repartition_sunburst_id'
    sales_repartition_waterfall = 'sales_repartition_waterfall_id'

    sales_evolution_sect = 'sales_evolution_sect_id'
    sales_evolution_bar = 'sales_evolution_bar_id'
    stocks_evolution_bar = 'stocks_evolution_bar_id'

    radio = 'radio_id'


class Dash:
    @staticmethod
    def get() -> html.Div:
        return Section.assemble_sections()


class Section:

    @staticmethod
    def assemble_sections() -> html.Div:
        assembled_sections: html.Div = html.Div(style={nm.display: nm.flex,
                                                       nm.flex_direction: nm.flex_row,
                                                       },
                                                children=[Section.__1_nav_bar(),
                                                          html.Br(),
                                                          html.Div(style={nm.display: nm.flex,
                                                                          nm.flex_direction: nm.flex_col,
                                                                          nm.width: '90%',
                                                                          nm.padding: '10px'
                                                                          },
                                                                   children=[Section.__2_sect_header(),
                                                                             html.Hr(),
                                                                             Section.__3_sect_progress(),
                                                                             html.Hr(),
                                                                             Section.__4_sect_progress_dist(),
                                                                             html.Hr(),
                                                                             Section.__5_sect_progress_hist(),
                                                                             ],
                                                                   ),
                                                          ]
                                                )
        return assembled_sections

    @staticmethod
    def __1_nav_bar() -> html.Div:
        return html.Div(id=IDs.nav_bar_sect,
                        style={nm.padding: '10px',
                               nm.width: '10%',
                               nm.bg_color: nm.rgba(251, 249, 250, 0.94),
                               nm.shadow: '5px 5px 10px lightgrey',
                               nm.border_radius: '10px',
                               },
                        children=[html.Label('Data Sources:',
                                             style={nm.text_deco: nm.underline,
                                                    nm.font_weight: nm.bold,
                                                    nm.color: 'grey',
                                                    },
                                             ),
                                  dcc.Dropdown(id=IDs.radio_b_data_source,
                                               options=['GSK', 'AT PHARMA', 'IQVIA'],
                                               value='GSK',
                                               clearable=False,
                                               searchable=True,
                                               multi=True,
                                               ),
                                  html.Hr(),
                                  html.Br(),
                                  html.Label('Brands:',
                                             style={nm.text_deco: nm.underline,
                                                    nm.font_weight: nm.bold,
                                                    nm.color: 'grey',
                                                    },
                                             ),
                                  dcc.Dropdown(id=IDs.drop_d_brand,
                                               options=['All', 'Augmentin', 'Clamoxyl', 'Ventoline', 'Flixotide',
                                                        'Seretide'],
                                               value='All',
                                               clearable=False,
                                               searchable=True,
                                               ),
                                  html.Hr(),
                                  html.Br(),
                                  html.Label('Selected SKU: All',
                                             style={nm.text_deco: nm.underline,
                                                    nm.font_weight: nm.bold,
                                                    nm.color: 'grey',
                                                    },
                                             ),
                                  dcc.Dropdown(id=IDs.drop_d_sku,
                                               options=['All'],
                                               value='All',
                                               clearable=False,
                                               searchable=True,
                                               ),
                                  html.Hr(),
                                  html.Br(),
                                  html.Label('Periods:',
                                             style={nm.text_deco: nm.underline,
                                                    nm.font_weight: nm.bold,
                                                    nm.color: 'grey',
                                                    },
                                             ),
                                  dcc.RadioItems(id=IDs.radio_b_period_type,
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
                                  dcc.Dropdown(id=IDs.drop_d_period_type_value,
                                               options=['Period 1', 'Period 2', 'Period 3'],
                                               value='Period 1',
                                               clearable=False,
                                               searchable=True,
                                               ),
                                  html.Hr(),
                                  html.Br(),
                                  html.Button(id=IDs.button_show,
                                              style={'background': '#64B5F6'},
                                              children=['Afficher'],
                                              n_clicks=0),
                                  ],
                        )

    @staticmethod
    def __2_sect_header() -> html.Div:
        return html.Div(style={nm.height: '5%',
                               nm.bg_color: nm.gsk_orange(),
                               nm.padding: '10px',
                               nm.border_radius: '10px',
                               nm.shadow: '5px 5px 5px lightgrey'
                               },
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
    def __3_sect_progress() -> html.Div:
        return html.Div(style={
            nm.padding: '10px',
        },
            children=[html.H5('Achievements',
                              style={nm.height: '5%',
                                     nm.text_deco: nm.underline,
                                     nm.border_radius: '5px',
                                     nm.shadow: '2px 2px lightgrey',
                                     },
                              ),
                      html.Div(title='Overall achievements',
                               id=IDs.sales_indicator_sect,
                               style={nm.display: nm.flex,
                                      nm.disposition: nm.flex_row,
                                      },
                               children=[html.Div(style={nm.opacity: '1',
                                                         nm.width: '25%',
                                                         nm.padding: '10px',
                                                         nm.border_radius: '15px',
                                                         },
                                                  children=[dcc.Graph(id=IDs.mtd_sales_indicator,
                                                                      style={nm.border_radius: '15px',
                                                                             nm.bg_color_fig: nm.gsk_orange(.5),
                                                                             nm.shadow: nm.defautl_shadow,
                                                                             },
                                                                      ),
                                                            ],
                                                  ),
                                         html.Div(style={nm.opacity: '1',
                                                         nm.width: '25%',
                                                         nm.padding: '10px',
                                                         nm.border_radius: '15px',
                                                         },
                                                  children=[dcc.Graph(id=IDs.qtd_sales_indicator,
                                                                      style={nm.border_radius: '15px',
                                                                             nm.bg_color_fig: 'white',
                                                                             nm.shadow: nm.defautl_shadow,
                                                                             },
                                                                      ),
                                                            ],
                                                  ),
                                         html.Div(style={nm.opacity: '1',
                                                         nm.width: '25%',
                                                         nm.padding: '10px',
                                                         nm.border_radius: '15px',
                                                         },
                                                  children=[dcc.Graph(id=IDs.std_sales_indicator,
                                                                      style={nm.border_radius: '15px',
                                                                             nm.bg_color_fig: 'white',
                                                                             nm.shadow: nm.defautl_shadow,
                                                                             },
                                                                      ),
                                                            ],
                                                  ),
                                         html.Div(style={nm.opacity: '1',
                                                         nm.width: '25%',
                                                         nm.padding: '10px',
                                                         nm.border_radius: '15px',
                                                         },
                                                  children=[dcc.Graph(id=IDs.ytd_sales_indicator,
                                                                      style={nm.border_radius: '15px',
                                                                             nm.bg_color_fig: 'white',
                                                                             nm.shadow: nm.defautl_shadow,
                                                                             },
                                                                      ),
                                                            ],
                                                  ),
                                         ],
                               ),
                      ],
        )

    @staticmethod
    def __4_sect_progress_dist() -> html.Div:
        return html.Div(style={
            nm.padding: '10px',
        },
            children=[html.H5('Sales distribution',
                              style={nm.height: '5%',
                                     nm.text_deco: nm.underline,
                                     nm.border_radius: '5px',
                                     nm.shadow: '2px 2px lightgrey',
                                     },
                              ),
                      html.Div(id=IDs.sales_repartition_sect,
                               style={nm.display: nm.flex,
                                      nm.disposition: nm.flex_row},
                               children=[html.Div(style={nm.opacity: '1',
                                                         nm.width: '50%',
                                                         nm.padding: '10px',
                                                         nm.border_radius: '15px',
                                                         },
                                                  children=[dcc.Graph(id=IDs.sales_repartition_sunburst,
                                                                      style={nm.border_radius: '15px',
                                                                             nm.bg_color_fig: 'white',
                                                                             nm.shadow: nm.defautl_shadow,
                                                                             },
                                                                      ),
                                                            ],
                                                  ),
                                         html.Div(style={nm.opacity: '1',
                                                         nm.width: '50%',
                                                         nm.padding: '10px',
                                                         nm.border_radius: '15px',
                                                         },
                                                  children=[dcc.Graph(id=IDs.sales_repartition_waterfall,
                                                                      style={nm.border_radius: '15px',
                                                                             nm.bg_color_fig: 'white',
                                                                             nm.shadow: nm.defautl_shadow,
                                                                             },
                                                                      ),
                                                            ],
                                                  )
                                         ],
                               ),
                      ],
        )

    @staticmethod
    def __5_sect_progress_hist() -> html.Div:
        return html.Div(style={
            nm.padding: '10px',
        },
            children=[html.H5('Sales evolution',
                              style={nm.height: '5%',
                                     nm.text_deco: nm.underline,
                                     nm.border_radius: '5px',
                                     nm.shadow: '2px 2px lightgrey',
                                     },
                              ),
                      html.Div(id=IDs.sales_evolution_sect,
                               style={nm.display: nm.flex,
                                      nm.disposition: nm.flex_row,
                                      },
                               children=[html.Div(style={nm.opacity: '1',
                                                         nm.width: '50%',
                                                         nm.padding: '10px',
                                                         nm.border_radius: '15px',
                                                         },
                                                  children=[dcc.Graph(id=IDs.sales_evolution_bar,
                                                                      style={nm.border_radius: '15px',
                                                                             nm.bg_color_fig: 'white',
                                                                             nm.shadow: nm.defautl_shadow,
                                                                             },
                                                                      ),
                                                            ],
                                                  ),
                                         html.Div(style={nm.opacity: '1',
                                                         nm.width: '50%',
                                                         nm.padding: '10px',
                                                         nm.border_radius: '15px',
                                                         },
                                                  children=[dcc.Graph(id=IDs.stocks_evolution_bar,
                                                                      style={nm.border_radius: '15px',
                                                                             nm.bg_color_fig: 'white',
                                                                             nm.shadow: nm.defautl_shadow,
                                                                             },
                                                                      ),
                                                            ],
                                                  )
                                         ],
                               ),
                      ],
        )

    @staticmethod
    def __6_sect_stock_hist() -> html.Div:
        pass


class FiguresUpdater:
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

    @staticmethod
    def update_sales_evolution_bar(sales_as: d.SalesAs) -> go.Figure:
        return fig.sales_hist_bar()

    @staticmethod
    def update_stocks_evolution_bar(sales_as: d.SalesAs) -> go.Figure:
        return fig.stocks_hist_bar()
