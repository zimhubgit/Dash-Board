class NameMap:
    @staticmethod
    def rgba(r: int, g: int, b: int, opacity: float = 1):
        return f'rgba({r},{g},{b},{opacity})'

    @staticmethod
    def gsk_orange(opacity: float = 0.7):
        return NameMap.rgba(243, 102, 51, opacity)

    @staticmethod
    def aug_blue(opacity: float = 0.7):
        return NameMap.rgba(92, 152, 251, opacity)

    @staticmethod
    def clam_red(opacity: float = 0.7):
        return NameMap.rgba(238, 14, 14, opacity)

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
    bg_color = 'backgroundColor'
    solid_gsk_orange = rgba(243, 102, 51)
    opacity = 'opacity'
    border_radius = 'border-radius'
    bg_color_fig = 'background-color'
    shadow = 'box-shadow'
    defautl_shadow = '8px 8px 8px lightgrey'
    padding_bottom = 'padding-bottom'
