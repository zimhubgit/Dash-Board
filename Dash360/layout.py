from datetime import datetime
from dash import html, dcc
import plotly.graph_objects as go
import glx.figures as fig
from glx.name_map import NameMap as nmap
import pandas as pnd
import glx.data as d
from .helpers import name_space as nm


class IDs:
    nav_bar_sect = 'navigation_bar_id'
    radio_b_data_source = 'data_source_radio_id'
    drop_d_brand = 'brand_drop_down_id'
    drop_d_sku = 'sku_drop_down_id'
    radio_b_period_type = 'period_type_radio_id'
    drop_d_period_type_value = 'period_type_value_drop_down_id'
    drop_d_periods_label = 'periods_drop_down_id'
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
                                                    style={nmap.width: '13%',
                                                           },
                                                    children=[Section.__2_sect_header(),
                                                              Section.__1_nav_bar(),
                                                              ],
                                                ),
                                                    html.Br(),
                                                    html.Div(style={nmap.display: nmap.flex,
                                                                    nmap.flex_direction: nmap.flex_col,
                                                                    nmap.width: '87%',
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
                                             style={
                                                 # nmap.text_deco: nmap.underline,
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
                                             style={
                                                 # nmap.text_deco: nmap.underline,
                                                 nmap.font_weight: nmap.bold,
                                                 nmap.color: 'grey',
                                             },
                                             ),
                                  dcc.Dropdown(id=IDs.drop_d_brand,
                                               options=d.data_dict[d.cy_key].brands,
                                               value=d.data_dict[d.cy_key].brands[0],
                                               clearable=False,
                                               searchable=True,
                                               ),
                                  html.Hr(),
                                  html.Br(),
                                  html.Label('SKUs:',
                                             style={
                                                 # nmap.text_deco: nmap.underline,
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
                                             style={
                                                 # nmap.text_deco: nmap.underline,
                                                 nmap.font_weight: nmap.bold,
                                                 nmap.color: 'grey',
                                             },
                                             ),
                                  dcc.RadioItems(id=IDs.radio_b_period_type,
                                                 options=[{'label': 'Months', 'value': 'MTD'},
                                                          {'label': 'Quarters', 'value': 'QTD'},
                                                          {'label': 'Year Halves', 'value': 'STD'},
                                                          {'label': 'Year', 'value': 'YTD'},
                                                          ],
                                                 value='MTD',
                                                 ),
                                  html.Br(),
                                  html.Label(id=IDs.drop_d_periods_label,
                                             children='Selected period: MTD'),
                                  dcc.Dropdown(id=IDs.drop_d_period_type_value,
                                               options=d.data_dict[d.cy_key].periods_map.get('MTD'),
                                               value=d.data_dict[d.cy_key].periods_map.get('MTD')[-1],
                                               clearable=False,
                                               searchable=True,
                                               ),
                                  html.Hr(),
                                  html.Br(),
                                  html.Button(id=IDs.button_show,
                                              style={'background': '#64B5F6'},
                                              children=['Submit'],
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
                                      nmap.height: '250px'
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

        cy_df = d.data_dict[d.cy_key].filter(prd_type=prd_type, brand=brand, sku=sku, date=date, end_date=end_date)
        ly_df = d.data_dict[d.ly_key].filter(prd_type=prd_type, brand=brand, sku=sku, date=ly_date, end_date=end_date)
        achieved: float = cy_df[sales_as.achieved].values[0]
        target: float = cy_df[sales_as.rfc].values[0]
        label: str = f'{prd_type} Progression : {update.day}/{update.month}/{update.year}'
        ly_achievement: float = ly_df[sales_as.achieved].values[0]

        return fig.indicator(achieved=achieved, target=target, label=label, sales_as=sales_as,
                             ly_achieved=ly_achievement)

    @staticmethod
    def update_sunburst_section(prd_type: str,
                                prd: str,
                                sales_as: d.SalesAs) -> go.Figure:
        last_update_date: pnd.Timestamp = d.data_dict[d.cy_key].last_update_on
        if prd_type == 'MTD' and datetime.strptime(prd, "%B").month >= last_update_date.month:
            date: pnd.Timestamp = last_update_date
        else:
            date: pnd.Timestamp = d.Data.date_from_period(prd_type=prd_type, prd=prd)
        data_df: pnd.DataFrame = d.data_dict[d.cy_key].filter(prd_type=prd_type,
                                                              date=date).copy()
        data_df = data_df[(~data_df[sales_as.achieved].isna()) & (data_df[sales_as.achieved] != 0.0)]

        def group_by(sku_type: str):
            if nm.GSK.Naming.SKU_SKU_TYPE == sku_type:
                return 'children'
            elif nm.GSK.Naming.BRAND_SKU_TYPE in sku_type:
                return 'parent'
            else:
                return 'root'

        skus_groups = data_df.set_index(nm.GSK.ColName.SKU_TYPE).groupby(group_by)
        parents_dict: dict[str, pnd.DataFrame] = {}
        for group, group_df in skus_groups:
            parents_dict.update({str(group): group_df.sort_values(sales_as.achieved)})

        children_list: list[str] = ['GSK']
        parents_list: list[str] = ['']
        values_list: list[float] = [parents_dict.get('root')[sales_as.achieved].values[0]]
        colors_list: list[str] = [parents_dict.get('root')[nm.GSK.ColName.COLOR].values[0]]
        rfc_list: list[float] = [parents_dict.get('root')[sales_as.rfc].values[0]]

        parents_df: pnd.DataFrame = parents_dict.get('parent')
        children_df: pnd.DataFrame = parents_dict.get('children')
        for parent in parents_df[nm.GSK.ColName.SKU].tolist():
            parents_list.append('glx')
            children_list.append(parent)
            values_list.append(parents_df[parents_df[nm.GSK.ColName.SKU] == parent][sales_as.achieved].values[0])
            colors_list.append(parents_df[parents_df[nm.GSK.ColName.SKU] == parent][nm.GSK.ColName.COLOR].values[0])
            rfc_list.append(parents_df[parents_df[nm.GSK.ColName.SKU] == parent][sales_as.rfc].values[0])

            parent_children_df = children_df[children_df[nm.GSK.ColName.BRAND] == parent]
            if not parent_children_df.empty:
                for child in parent_children_df[nm.GSK.ColName.SKU].tolist():
                    parents_list.append(parent)
                    children_list.append(child)
                    values_list.append(
                        parent_children_df[parent_children_df[nm.GSK.ColName.SKU] == child][sales_as.achieved].values[
                            0])
                    colors_list.append(
                        parent_children_df[parent_children_df[nm.GSK.ColName.SKU] == child][
                            nm.GSK.ColName.COLOR].values[
                            0])
                    rfc_list.append(
                        parent_children_df[parent_children_df[nm.GSK.ColName.SKU] == child][sales_as.rfc].values[
                            0])
        return fig.sunburst(parents=parents_list,
                            labels=children_list,
                            values=values_list,
                            colors=colors_list,
                            rfcs=rfc_list)

    @staticmethod
    def update_waterfall_section(brand: str,
                                 prd_type: str,
                                 prd: str,
                                 sales_as: d.SalesAs) -> go.Figure:
        last_update_date: pnd.Timestamp = d.data_dict[d.cy_key].last_update_on
        if prd_type == 'MTD' and datetime.strptime(prd, "%B").month >= last_update_date.month:
            date: pnd.Timestamp = last_update_date
        else:
            date: pnd.Timestamp = d.Data.date_from_period(prd_type=prd_type, prd=prd)
        data_df: pnd.DataFrame
        if brand == nm.GSK.Naming.ALL_SKUs:
            data_df = d.data_dict[d.cy_key].filter(prd_type=prd_type,
                                                   sku_type=[nm.GSK.Naming.BRAND_SKU_TYPE,
                                                             nm.GSK.Naming.ALL_SKUs,
                                                             nm.GSK.Naming.SKU_BRAND_SKU_TYPE],
                                                   date=date).copy()
        else:
            data_df = d.data_dict[d.cy_key].filter(prd_type=prd_type,
                                                   brand=brand,
                                                   date=date).copy()

        data_df = data_df[(~data_df[sales_as.achieved].isna()) & (data_df[sales_as.achieved] != 0.0)]
        data_df.sort_values(sales_as.achieved, inplace=True)
        x_labels: list[str] = data_df[nm.GSK.ColName.SKU].tolist()
        values: list[float] = data_df[sales_as.achieved].tolist()
        text: list[str] = [f'{value:.2f}<Br>({(value / values[-1] * 100):.2f}%)' for value in values]
        values[-1] = 0
        measure: list[str] = ['relative' for sku in x_labels[0:-1]]
        measure.append('total')
        colors: list[str] = data_df[nm.GSK.ColName.COLOR].tolist()
        name: str = f'{brand}: {sales_as.name} | {prd}'
        return fig.water_fall(name=name,
                              measure=measure,
                              x_labels=x_labels,
                              text=text,
                              values=values,
                              colors=colors)

    @staticmethod
    def update_sales_evolution_bar(sku: str = None,
                                   sales_as: d.SalesAs = None) -> go.Figure:
        cy_start_date: pnd.Timestamp = d.Data.date_from_period(prd_type='YTD',
                                                               prd=None,
                                                               start_date=True)
        cy_end_date: pnd.Timestamp = d.Data.date_from_period(prd_type='YTD',
                                                             prd=None)
        data_df_cy = d.data_dict[d.cy_key].filter(prd_type='MONTHLY',
                                                  date=cy_start_date,
                                                  end_date=cy_end_date,
                                                  sku=sku)
        ly_start_date: pnd.Timestamp = d.Data.date_from_period(prd_type='YTD',
                                                               prd=None,
                                                               start_date=True,
                                                               current_year=False)
        ly_end_date: pnd.Timestamp = d.Data.date_from_period(prd_type='YTD', prd=None,
                                                             current_year=False)
        data_df_ly = d.data_dict[d.ly_key].filter(prd_type='MONTHLY',
                                                  date=ly_start_date,
                                                  end_date=ly_end_date,
                                                  sku=sku)
        data_df_cy = data_df_cy.sort_values(by=nm.GSK.ColName.DATE)
        data_df_ly = data_df_ly.sort_values(by=nm.GSK.ColName.DATE)
        months: list[pnd.Timestamp] = data_df_ly[nm.GSK.ColName.DATE].tolist()
        targets: list[float] = data_df_cy[sales_as.rfc].tolist()
        cy_actuals: list[float] = data_df_cy[sales_as.achieved].tolist()
        ly_actuals: list[float] = data_df_ly[sales_as.achieved].tolist()
        return fig.sales_hist_bar(months=months,
                                  targets=targets,
                                  cy_actuals=cy_actuals,
                                  ly_actuals=ly_actuals,
                                  )

    @staticmethod
    def update_stocks_evolution_bar(prd_type: str,
                                    prd: str,
                                    sku: str = None) -> go.Figure:
        start_date: pnd.Timestamp = d.Data.date_from_period(prd_type=prd_type, prd=prd, start_date=True)
        end_date: pnd.Timestamp = d.Data.date_from_period(prd_type=prd_type, prd=prd)
        data_df = d.data_dict[d.cy_key].filter(prd_type='DAILY',
                                               date=start_date,
                                               end_date=end_date,
                                               sku=sku)
        data_df = data_df.sort_values(by=nm.GSK.ColName.DATE)
        time: list[pnd.Timestamp] = data_df[nm.GSK.ColName.DATE].tolist()
        quarantine_values = data_df[nm.GSK.ColName.QUARANTINE_STOCK].tolist()
        available_values = data_df[nm.GSK.ColName.AVAILABLE_STOCK].tolist()
        return fig.stocks_hist_bar(time=time,
                                   quarantine_y=quarantine_values,
                                   available_y=available_values)
