import pandas as pnd
import plotly.graph_objects as go

from src.name_space import GSK
from src import gsk_sales as sls


class GraphicsData:
    SALES_DF: list[sls.GskSales]
    sales_2023: pnd.DataFrame

    def __init__(self, sales_df: pnd.DataFrame, name: str):
        self.graphics_sales_df: pnd.DataFrame = sales_df
        self.name: str = name

    @staticmethod
    def achievement() -> int:
        data: pnd.DataFrame = GraphicsData.SALES_DF.gsk_dataset_df
        data = data[data[GSK.ColName.PERIOD_TYPE] == GSK.Naming.PERIOD_TYPE_MTD]
        data = data[data[GSK.ColName.DATE].dt.month == 3]
        data = data[data[GSK.ColName.SKU] == GSK.Naming.ALL_SKUs]
        index = data[GSK.ColName.DATE].max()
        row = data[data[GSK.ColName.DATE] == index]
        rfc = row['RFC(GBP)'].values[0]
        actu = row['LIVRAISONS'].values[0]
        return actu, rfc

    @staticmethod
    def load_graphs_dfs(df: pnd.DataFrame):
        GraphicsData.SALES_DF = df
        achiv, target = GraphicsData.achievement()
        fig = go.Figure(go.Indicator(

            mode="number+gauge+delta", value=achiv,
            domain={'x': [0, 1], 'y': [0, 1]},
            delta={'reference': target, 'position': "top"},
            title={'text': "<b>Achievment</b><br><span style='color: gray; font-size:0.8em'>GBP £</span>",
                   'font': {"size": 14}},
            gauge={
                'axis': {'range': [None, (target + (target * .10))]},
                'threshold': {
                    'line': {'color': "red", 'width': 2},
                    'thickness': 0.75, 'value': target},

                'bgcolor': "white",
                'steps': [
                    {'range': [0, 1500000], 'color': "cyan"},
                    {'range': [1500000, 2500000], 'color': "royalblue"}],
                'bar': {'color': "darkblue"}}))
        fig.update_layout(height=350)
        fig.show()

    @staticmethod
    def load_graphics_data():
        periods_type_group = GraphicsData.SALES_DF.groupby[GSK.ColName.PERIOD_TYPE]
        for period_type, period_type_df in periods_type_group:
            sku_groups = period_type_df.groupby(GSK.ColName.GSK_DESIGNATION)
            for sku, sku_dfs in sku_groups:
                pass


GRAPHICS_DATA_DICT: dict[str, GraphicsData]
