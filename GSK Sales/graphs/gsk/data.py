import parametres.src.name_space as nm


class SalesAs:
    value: str = 'Value'
    volume: str = 'Volume'

    def __init__(self, name: str):
        self.name: str = name
        self.rfc: str
        self.achieved: str
        self._set_properties()

    def _set_properties(self):
        if self.name == SalesAs.volume:
            self.rfc = nm.GSK.ColName.RFC_UNIT_COL
            self.achieved = nm.GSK.ColName.UNIT_SALES
        elif self.name == SalesAs.value:
            self.rfc = nm.GSK.ColName.RFC_VALUE_COL
            self.achieved = nm.GSK.ColName.VALUE_SALES
        else:
            raise Exception('Sales as error')


def get_delta_color(progression: float) -> str:
    default_red_color: str = '#FF4136'
    defautl_green_color: str = '#3D9970'
    dark_green_color: str = '#033301'
    dark_red_color: str = '#690902'
    orange_color: str = '#db9f07'
    blue_color: str = '#2370c2'
    if progression < .20:
        return dark_red_color
    elif progression < .45:
        return default_red_color
    elif progression < .85:
        return orange_color
    elif progression < .95:
        return defautl_green_color
    elif progression < 1.1:
        return dark_green_color
    else:
        return blue_color