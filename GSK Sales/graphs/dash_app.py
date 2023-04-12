from dash import html


class Naming:
    children_num = 'NUMBER OF CHILDREN'
    disposition = 'DISPOSITION'
    orientation = 'ORIENTATION'


class DashScene:
    def __int__(self, name: str, scene: dict[str:dict]):
        self.name: str = name
        self.scene: html.Div = scene

    def load(self):
        self.scene
