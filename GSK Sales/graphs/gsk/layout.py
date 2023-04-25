from dash import html
from name_space import NameMap as nm


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
                                                          ]
                                                )
        return assembled_sections

    @staticmethod
    def __1_sect_header() -> html.Div:
        return html.Div('GSK Dash Header',
                        style={nm.height: '15%',
                               nm.border: '1px solid black',
                               nm.bg_color: nm.solid_gsk_orange},
                        )

    @staticmethod
    def __2_sect_progress() -> html.Div:
        pass

    @staticmethod
    def __3_sect_progress_dist() -> html.Div:
        pass

    @staticmethod
    def __4_sect_progress_hist() -> html.Div:
        pass

    @staticmethod
    def __5_sect_stock_hist() -> html.Div:
        pass
