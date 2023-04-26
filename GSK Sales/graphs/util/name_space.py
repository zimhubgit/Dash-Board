class NameMap:
    @staticmethod
    def rgba(r: int, g: int, b: int, opacity: float = 1):
        return f'rgba({r},{g},{b},{opacity})'

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
