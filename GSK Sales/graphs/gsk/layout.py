from dash import html, dcc
import plotly.graph_objects as go
import figures as fig
from name_space import NameMap as nmap
import parametres.src.name_space as nm
import pandas as pnd

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

    aug_sales_indicator_sect = 'aug_sales_indicators_sect_id'
    aug_mtd_sales_indicator = 'aug_mtd_sales_indicator_id'
    aug_qtd_sales_indicator = 'aug_qtd_sales_indicator_id'
    aug_std_sales_indicator = 'aug_std_sales_indicator_id'
    aug_ytd_sales_indicator = 'aug_ytd_sales_indicator_id'

    clam_sales_indicator_sect = 'clam_sales_indicators_sect_id'
    clam_mtd_sales_indicator = 'clam_mtd_sales_indicator_id'
    clam_qtd_sales_indicator = 'clam_qtd_sales_indicator_id'
    clam_std_sales_indicator = 'clam_std_sales_indicator_id'
    clam_ytd_sales_indicator = 'clam_ytd_sales_indicator_id'

    sales_repartition_sect = 'sales_repartition_sect_id'
    sales_repartition_sunburst = 'sales_repartition_sunburst_id'
    sales_repartition_waterfall = 'sales_repartition_waterfall_id'

    sales_evolution_sect = 'sales_evolution_sect_id'
    sales_evolution_bar = 'sales_evolution_bar_id'
    stocks_evolution_bar = 'stocks_evolution_bar_id'

    radio_b_sales_as = 'sales_as_radio_id'


class Dash:
    @staticmethod
    def get() -> html.Div:
        return Section.assemble_sections()


class Section:

    @staticmethod
    def assemble_sections() -> html.Div:
        assembled_sections: html.Div = html.Div(style={nmap.display: nmap.flex,
                                                       nmap.flex_direction: nmap.flex_row,
                                                       },
                                                children=[html.Div(
                                                    children=[Section.__2_sect_header(),
                                                              Section.__1_nav_bar(),
                                                              ],
                                                ),
                                                    html.Br(),
                                                    html.Div(style={nmap.display: nmap.flex,
                                                                    nmap.flex_direction: nmap.flex_col,
                                                                    nmap.width: '90%',
                                                                    nmap.padding: '10px'
                                                                    },
                                                             children=[Section.__3_sect_progress(
                                                                 IDs.sales_indicator_sect,
                                                                 'GSK',
                                                                 IDs.mtd_sales_indicator,
                                                                 IDs.qtd_sales_indicator,
                                                                 IDs.std_sales_indicator,
                                                                 IDs.ytd_sales_indicator,
                                                                 tile_color=nmap.gsk_orange(.3),
                                                                 shadow_color=nmap.defautl_shadow),
                                                                 Section.__3_sect_progress(
                                                                     IDs.aug_sales_indicator_sect,
                                                                     'Augmentin',
                                                                     IDs.aug_mtd_sales_indicator,
                                                                     IDs.aug_qtd_sales_indicator,
                                                                     IDs.aug_std_sales_indicator,
                                                                     IDs.aug_ytd_sales_indicator,
                                                                     tile_color=nmap.aug_blue(.2),
                                                                     shadow_color=nmap.defautl_shadow),
                                                                 Section.__3_sect_progress(
                                                                     IDs.clam_sales_indicator_sect,
                                                                     'Clamoxyl',
                                                                     IDs.clam_mtd_sales_indicator,
                                                                     IDs.clam_qtd_sales_indicator,
                                                                     IDs.clam_std_sales_indicator,
                                                                     IDs.clam_ytd_sales_indicator,
                                                                     tile_color=nmap.clam_red(.3),
                                                                     shadow_color=nmap.defautl_shadow),
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
                        style={nmap.padding: '10px',
                               # nmap.width: '15%',
                               nmap.bg_color: nmap.rgba(251, 249, 250, 0.94),
                               nmap.shadow: '5px 5px 10px lightgrey',
                               nmap.border_radius: '0px 0px 10px 10px',
                               },
                        children=[html.Label('Data Sources:',
                                             style={nmap.text_deco: nmap.underline,
                                                    nmap.font_weight: nmap.bold,
                                                    nmap.color: 'grey',
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
                                             style={nmap.text_deco: nmap.underline,
                                                    nmap.font_weight: nmap.bold,
                                                    nmap.color: 'grey',
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
                                             style={nmap.text_deco: nmap.underline,
                                                    nmap.font_weight: nmap.bold,
                                                    nmap.color: 'grey',
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
                                             style={nmap.text_deco: nmap.underline,
                                                    nmap.font_weight: nmap.bold,
                                                    nmap.color: 'grey',
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
        return html.Div(style={nmap.height: '3%',
                               nmap.bg_color: nmap.gsk_orange(),
                               nmap.padding: '10px',
                               'margin-top': '20px',
                               nmap.border_radius: '10px 10px 0px 0px',
                               nmap.shadow: '5px 5px 5px lightgrey'
                               },
                        children=['GSK Dash 360',
                                  dcc.RadioItems(id=IDs.radio_b_sales_as,
                                                 style={},
                                                 options=[
                                                     {'label': 'Volume', 'value': d.SalesAs(d.SalesAs.volume).name},
                                                     {'label': 'Value', 'value': d.SalesAs(d.SalesAs.value).name},
                                                 ],
                                                 value=d.SalesAs(d.SalesAs.volume).name
                                                 ),
                                  ],
                        )

    @staticmethod
    def __3_sect_progress(sect_id: str, brand: str, mtd_id: str, qtd_id: str, std_id: str, ytd_id: str, tile_color: str,
                          shadow_color: str) -> html.Div:
        return html.Div(style={
            nmap.padding_bottom: '15px',
        },
            children=[html.H2('Achievements: ' + brand,
                              style={nmap.height: '5%',
                                     # nmap.text_deco: nmap.underline,
                                     nmap.border_radius: '5px',
                                     # nmap.shadow: '2px 2px lightgrey',
                                     nmap.padding: '0px 0px 7px 25px',
                                     'margin': '1px',
                                     },
                              ),
                      html.Div(title='Overall achievements',
                               id=sect_id,
                               style={nmap.display: nmap.flex,
                                      nmap.disposition: nmap.flex_row,
                                      nmap.height: '300px'
                                      },
                               children=[html.Div(style={nmap.opacity: '1',
                                                         nmap.width: '25%',
                                                         nmap.padding: '10px',
                                                         nmap.border_radius: '15px',
                                                         },
                                                  children=[dcc.Graph(id=mtd_id,
                                                                      style={nmap.border_radius: '15px',
                                                                             nmap.bg_color_fig: tile_color,
                                                                             nmap.shadow: shadow_color,
                                                                             nmap.height: '100%',
                                                                             },
                                                                      ),
                                                            ],
                                                  ),
                                         html.Div(style={nmap.opacity: '1',
                                                         nmap.width: '25%',
                                                         nmap.padding: '10px',
                                                         nmap.border_radius: '15px',
                                                         },
                                                  children=[dcc.Graph(id=qtd_id,
                                                                      style={nmap.border_radius: '15px',
                                                                             nmap.bg_color_fig: tile_color,
                                                                             nmap.shadow: shadow_color,
                                                                             nmap.height: '100%',
                                                                             },
                                                                      ),
                                                            ],
                                                  ),
                                         html.Div(style={nmap.opacity: '1',
                                                         nmap.width: '25%',
                                                         nmap.padding: '10px',
                                                         nmap.border_radius: '15px',
                                                         },
                                                  children=[dcc.Graph(id=std_id,
                                                                      style={nmap.border_radius: '15px',
                                                                             nmap.bg_color_fig: tile_color,
                                                                             nmap.shadow: shadow_color,
                                                                             nmap.height: '100%',
                                                                             },
                                                                      ),
                                                            ],
                                                  ),
                                         html.Div(style={nmap.opacity: '1',
                                                         nmap.width: '25%',
                                                         nmap.padding: '10px',
                                                         nmap.border_radius: '15px',
                                                         },
                                                  children=[dcc.Graph(id=ytd_id,
                                                                      style={nmap.border_radius: '15px',
                                                                             nmap.bg_color_fig: tile_color,
                                                                             nmap.shadow: shadow_color,
                                                                             nmap.height: '100%',
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
            nmap.padding: '10px',
        },
            children=[html.H2('Sales distribution',
                              style={nmap.height: '5%',
                                     # nmap.text_deco: nmap.underline,
                                     nmap.border_radius: '5px',
                                     # nmap.shadow: '2px 2px lightgrey',
                                     nmap.padding: '0px 0px 7px 25px',
                                     'margin': '1px',
                                     },
                              ),
                      html.Div(id=IDs.sales_repartition_sect,
                               style={nmap.display: nmap.flex,
                                      nmap.disposition: nmap.flex_row},
                               children=[html.Div(style={nmap.opacity: '1',
                                                         nmap.width: '50%',
                                                         nmap.padding: '10px',
                                                         nmap.border_radius: '15px',
                                                         },
                                                  children=[dcc.Graph(id=IDs.sales_repartition_sunburst,
                                                                      style={nmap.border_radius: '15px',
                                                                             nmap.bg_color_fig: 'white',
                                                                             nmap.shadow: nmap.defautl_shadow,
                                                                             nmap.border: '1px solid lightgrey',
                                                                             },
                                                                      ),
                                                            ],
                                                  ),
                                         html.Div(style={nmap.opacity: '1',
                                                         nmap.width: '50%',
                                                         nmap.padding: '10px',
                                                         nmap.border_radius: '15px',
                                                         },
                                                  children=[dcc.Graph(id=IDs.sales_repartition_waterfall,
                                                                      style={nmap.border_radius: '15px',
                                                                             nmap.bg_color_fig: 'white',
                                                                             nmap.shadow: nmap.defautl_shadow,
                                                                             nmap.border: '1px solid lightgrey',
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
            nmap.padding: '10px',
        },
            children=[html.H2('Sales evolution',
                              style={nmap.height: '5%',
                                     # nmap.text_deco: nmap.underline,
                                     nmap.border_radius: '5px',
                                     # nmap.shadow: '2px 2px lightgrey',
                                     nmap.padding: '0px 0px 7px 25px',
                                     'margin': '1px',
                                     },
                              ),
                      html.Div(id=IDs.sales_evolution_sect,
                               style={nmap.display: nmap.flex,
                                      nmap.disposition: nmap.flex_row,
                                      },
                               children=[html.Div(style={nmap.opacity: '1',
                                                         nmap.width: '50%',
                                                         nmap.padding: '10px',
                                                         nmap.border_radius: '15px',
                                                         },
                                                  children=[dcc.Graph(id=IDs.sales_evolution_bar,
                                                                      style={nmap.border_radius: '15px',
                                                                             nmap.bg_color_fig: 'white',
                                                                             nmap.shadow: nmap.defautl_shadow,
                                                                             nmap.border: '1px solid lightgrey',
                                                                             },
                                                                      ),
                                                            ],
                                                  ),
                                         html.Div(style={nmap.opacity: '1',
                                                         nmap.width: '50%',
                                                         nmap.padding: '10px',
                                                         nmap.border_radius: '15px',
                                                         },
                                                  children=[dcc.Graph(id=IDs.stocks_evolution_bar,
                                                                      style={nmap.border_radius: '15px',
                                                                             nmap.bg_color_fig: 'white',
                                                                             nmap.shadow: nmap.defautl_shadow,
                                                                             nmap.border: '1px solid lightgrey',
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
    def update_progress_section(prd_type: str,
                                brand: str | None,
                                sku: str | None,
                                end_date: pnd.Timestamp | None,
                                sales_as: d.SalesAs) -> go.Figure:
        update: pnd.Timestamp = d.data_dict[d.cy_key].last_update_on
        date: pnd.Timestamp = update
        ly_date = d.Data.translate_date_to_ly_date(date)

        if prd_type == 'QTD':
            date = d.Data.translate_date_qtd_date(date)
            ly_date = d.Data.translate_date_qtd_date(ly_date)
        elif prd_type == 'STD':
            date = d.Data.translate_date_std_date(date)
            ly_date = d.Data.translate_date_std_date(ly_date)
        elif prd_type == 'YTD':
            date = d.Data.translate_date_ytd_date(date)
            ly_date = d.Data.translate_date_ytd_date(ly_date)

        cy_df = d.data_dict[d.cy_key].filter(prd_type, brand, sku, date, end_date)
        ly_df = d.data_dict[d.ly_key].filter(prd_type, brand, sku, ly_date, end_date)
        achieved: float = cy_df[sales_as.achieved].values[0]
        target: float = cy_df[sales_as.rfc].values[0]
        label: str = f'{prd_type} Progression : {update.day}/{update.month}/{update.year}'
        ly_achievement: float = ly_df[sales_as.achieved].values[0]

        return fig.indicator(achieved=achieved, target=target, label=label, sales_as=sales_as,
                             ly_achieved=ly_achievement)

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
