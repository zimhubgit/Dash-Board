from datetime import datetime

import numpy as np
import pandas as pnd
import plotly.express as px
import plotly.graph_objects as go

from Dash360.utils import name_space as nm


class GSKSalesGraph:
    progresses = [.33, 0.50, .75, .95]
    ACTUAL_DATA: pnd.DataFrame
    LAST_PERIOD_DATA: pnd.DataFrame

    @staticmethod
    def set_data(last_period_data: pnd.DataFrame, act_data: pnd.DataFrame):
        GSKSalesGraph.ACTUAL_DATA = act_data
        GSKSalesGraph.LAST_PERIOD_DATA = last_period_data

    @staticmethod
    def sunburst_figure():
        sunburst_df: pnd.DataFrame = GSKSalesGraph.ACTUAL_DATA[
            GSKSalesGraph.ACTUAL_DATA[nm.GSK.ColName.PERIOD_TYPE] == nm.GSK.Naming.PERIOD_TYPE_MTD]
        index = sunburst_df[nm.GSK.ColName.DATE].max()
        sunburst_df = sunburst_df[sunburst_df[nm.GSK.ColName.DATE] == index]
        sunburst_df = sunburst_df[(~sunburst_df['SALES VALUE(GBP)'].isna()) & (sunburst_df['SALES VALUE(GBP)'] != 0)]
        sunburst_df = sunburst_df[sunburst_df[nm.GSK.ColName.SKU_TYPE].str.contains(nm.GSK.Naming.SKU_SKU_TYPE)]
        sunburst_df['RACINE'] = 'GSK sales GBP(£)'
        sunburst_df['REALISATIONS'] = sunburst_df['SALES VALUE(GBP)'] / sunburst_df['RFC VALUE(GBP)'] * 100
        fig = px.sunburst(sunburst_df, path=['RACINE', nm.GSK.ColName.BRAND, nm.GSK.ColName.SKU],
                          values='SALES VALUE(GBP)', color='REALISATIONS', hover_data=['RFC UNIT'],
                          color_continuous_scale='rdylgn', color_continuous_midpoint=50)
        fig.update_traces({'insidetextorientation': 'radial'})
        fig.show()

    @staticmethod
    def sunburst_parents(data: pnd.DataFrame) -> dict[str, list[str]]:
        parents: list[str] = []
        labels: list[str] = []
        values: list[float] = []
        root: str = data['RACINE'].values[0]
        for idx, row in data.iterrows():
            value = row.loc['SALES VALUE(GBP)']
            if pnd.isna(value) or value == 0:
                continue
            brand = row.loc['BRAND']
            sku_type = row.loc['SKU TYPE']
            sku = row.loc['SKU']
            if 'BRAND - SKU' in sku_type:
                parents.append(root)
                labels.append(sku)
                values.append(value)
            elif 'SKU' in sku_type:
                parents.append(brand)
                labels.append(sku)
                values.append(value)
            elif 'BRAND' in sku_type:
                parents.append(root)
                labels.append(sku)
                values.append(value)
            elif 'ALL' in sku_type:
                parents.insert(0, '')
                labels.insert(0, root)
                values.insert(0, value)
        return {'labels': labels, 'parents': parents, 'values': values}

    @staticmethod
    def sunburst_bis():
        sunburst_df: pnd.DataFrame = GSKSalesGraph.ACTUAL_DATA[
            GSKSalesGraph.ACTUAL_DATA[nm.GSK.ColName.PERIOD_TYPE] == nm.GSK.Naming.PERIOD_TYPE_MTD]
        index = sunburst_df[nm.GSK.ColName.DATE].max()
        sunburst_df = sunburst_df[sunburst_df[nm.GSK.ColName.DATE] == index]
        sunburst_df = sunburst_df[(sunburst_df['SALES VALUE(GBP)'] != 0) & (sunburst_df['SALES VALUE(GBP)'] != 'nan')]
        sunburst_df['RACINE'] = 'GSK sales GBP(£)'
        sunburst_df['REALISATIONS'] = sunburst_df['SALES VALUE(GBP)'] / sunburst_df['RFC VALUE(GBP)'] * 100
        fig = go.Figure()

        labels_dict: dict[str, list[object]] = GSKSalesGraph.sunburst_parents(sunburst_df)
        fig.add_trace(go.Sunburst(
            values=labels_dict.get('values'),
            labels=labels_dict.get('labels'),
            parents=labels_dict.get('parents'),
            branchvalues='total',
            insidetextorientation='radial'))
        fig.show()

    @staticmethod
    def indicator_figure():
        values_dict = GSKSalesGraph.achievement()
        target = values_dict.get('target')
        progress = values_dict.get('progress')
        last_period_progress = values_dict.get('last progress')
        # progress_over_time = GSKSalesGraph.progression_over_time_mile_stone(actual_progress=progress,
        #                                                                     target_progress=target, )

        fig = go.Figure(go.Indicator(
            mode="number+gauge+delta", value=progress,
            domain={'row': 0, 'column': 0},
            delta={'reference': target, 'position': "top"},
            title={'text': "<b>Achievement</b><br><span style='color: gray; font-size:0.8em'>GBP £</span>",
                   'font': {"size": 14}},
            gauge={
                'axis': {'range': [None, (target + (target * .15))]},
                'threshold': {
                    'line': {'color': "red", 'width': 2},
                    'thickness': 1, 'value': target},

                'bgcolor': "white",
                'steps': [
                    {'range': [0, last_period_progress], 'color': "orange"}],
                'bar': {'color': "green"}}))
        fig.update_layout(height=300)
        fig.add_trace(go.Indicator(
            mode='delta',
            value=(progress + target) / target * 100,
            delta={'reference': 100, 'suffix': '% ',
                   'increasing': {'color': GSKSalesGraph.get_delta_color(.7)}},
            domain={'row': 1, 'column': 0}
        ))
        fig.update_layout(grid={'rows': 2, 'columns': 1, 'pattern': "independent"})
        fig.show()

    @staticmethod
    def achievement() -> dict[str, object]:
        data: pnd.DataFrame = GSKSalesGraph.ACTUAL_DATA
        data = data[data[nm.GSK.ColName.PERIOD_TYPE] == nm.GSK.Naming.PERIOD_TYPE_MTD]
        data = data[data[nm.GSK.ColName.DATE].dt.month == 3]
        data = data[data[nm.GSK.ColName.SKU] == nm.GSK.Naming.ALL_SKUs]
        index = data[nm.GSK.ColName.DATE].max()
        row = data[data[nm.GSK.ColName.DATE] == index]
        rfc = row['RFC VALUE(GBP)'].values[0]
        actual = row['SALES VALUE(GBP)'].values[0]

        data: pnd.DataFrame = GSKSalesGraph.LAST_PERIOD_DATA
        data = data[data[nm.GSK.ColName.PERIOD_TYPE] == nm.GSK.Naming.PERIOD_TYPE_MTD]
        data = data[data[nm.GSK.ColName.DATE].dt.month == 3]
        data = data[data[nm.GSK.ColName.SKU] == nm.GSK.Naming.ALL_SKUs]
        index = data[nm.GSK.ColName.DATE].max()
        row = data[data[nm.GSK.ColName.DATE] == index]
        last_progress = row['SALES VALUE(GBP)'].values[0]

        return {'progress': actual, 'target': rfc, 'last progress': last_progress}

    @staticmethod
    def skus_achievements() -> dict[str, object]:
        data: pnd.DataFrame = GSKSalesGraph.ACTUAL_DATA
        data = data[data[nm.GSK.ColName.PERIOD_TYPE] == nm.GSK.Naming.PERIOD_TYPE_MTD]
        data = data[data[nm.GSK.ColName.DATE].dt.month == 3]
        data = data[(data['SALES VALUE(GBP)'] != 0) & (data['SALES VALUE(GBP)'] != np.NaN)]
        index = data[nm.GSK.ColName.DATE].max()
        data = data[data[nm.GSK.ColName.DATE] == index]

        actual = data['SALES VALUE(GBP)'].values.tolist()
        names = data['SKU'].values.tolist()
        return {'sku': names, 'sales': actual}

    @staticmethod
    def get_time_progress(period_type: str) -> dict[str:datetime]:
        time_dict: dict[str, datetime] = {}
        actual_time = GSKSalesGraph.ACTUAL_DATA[nm.GSK.ColName.UPDATED_ON].values[0]
        ref_period: int
        period_df = GSKSalesGraph.ACTUAL_DATA[GSKSalesGraph.ACTUAL_DATA[nm.GSK.ColName.PERIOD_TYPE] == period_type]
        if period_type == nm.GSK.Naming.PERIOD_TYPE_DAILY:
            ref_period = period_df[period_df[nm.GSK.ColName.DATE].dt.month == actual_time.month].max().day

        if period_type == nm.GSK.Naming.PERIOD_TYPE_Weekly:
            ref_period = period_df[period_df[nm.GSK.ColName.DATE].dt.month == actual_time.month].max().week

        if period_type == nm.GSK.Naming.PERIOD_TYPE_MTD:
            ref_period = period_df[period_df[nm.GSK.ColName.DATE].dt.month == actual_time.month].max().month

        if period_type == nm.GSK.Naming.PERIOD_TYPE_QTD:
            ref_period = period_df[period_df[nm.GSK.ColName.DATE].dt.month == actual_time.month].max().quarter

    @staticmethod
    def bar_figure():
        df_act = GSKSalesGraph.ACTUAL_DATA[GSKSalesGraph.ACTUAL_DATA[nm.GSK.ColName.SKU_TYPE].str.contains('BRAND')]
        df_act = df_act[~df_act['SALES VALUE(GBP)'].isna()]
        df_act = df_act[df_act[nm.GSK.ColName.PERIOD_TYPE] == 'MTD']
        act_date = df_act.groupby(df_act['DATE'].dt.month)['DATE'].max()
        df_act = df_act[df_act['DATE'].isin(act_date.values)]

        df_last = GSKSalesGraph.LAST_PERIOD_DATA[
            GSKSalesGraph.LAST_PERIOD_DATA[nm.GSK.ColName.SKU_TYPE].str.contains('BRAND')]
        df_last = df_last[~df_last['SALES VALUE(GBP)'].isna()]
        df_last = df_last[df_last[nm.GSK.ColName.PERIOD_TYPE] == 'MTD']
        last_date = df_last.groupby(df_last['DATE'].dt.month)['DATE'].max()
        df_last = df_last[df_last['DATE'].isin(last_date.values)]

        fig_act = px.bar(df_act, x="DATE", y="SALES VALUE(GBP)", color='SKU')
        fig_last = px.bar(df_last, x="DATE", y="SALES VALUE(GBP)", color='SKU')
        all_fig = go.Figure()
        all_fig.add_trace(fig_act.data[0])
        all_fig.add_trace(fig_last.data[0])
        # all_fig.show()

        fig = go.Figure(data=[go.Bar(name='2023', x=df_act['DATE'].dt.month.values.tolist(),
                                     y=df_act['SALES VALUE(GBP)'].values.tolist()),
                              go.Bar(name='2022', x=df_last['DATE'].dt.month.values.tolist(),
                                     y=df_last['SALES VALUE(GBP)'].values.tolist())
                              ])
        fig.update_layout(barmode='group')
        fig.show()

    @staticmethod
    def stock_bar():
        stock_df: pnd.DataFrame = GSKSalesGraph.ACTUAL_DATA[
            GSKSalesGraph.ACTUAL_DATA[nm.GSK.ColName.PERIOD_TYPE] == nm.GSK.Naming.PERIOD_TYPE_MTD]
        stock_df = stock_df[stock_df['SKU'] == 'AUGMENTIN 1G SCHT']
        fig = go.Figure(data=[go.Bar(name='Stocks', x=stock_df['DATE'], y=stock_df['Stock Total'])])
        # fig.update_layout(barmode='group')
        fig.show()

    @staticmethod
    def sankey_chart(df: pnd.DataFrame):
        source1 = df['SOURCE1'].values.tolist()
        source2 = df['SOURCE2'].values.tolist()
        sources = source1.copy()
        sources.extend(source2)
        sources.extend(source2)
        sources.extend(source2)
        target1 = df['TARGET1'].values.tolist()
        target2 = df['TARGET2'].values.tolist()
        target3 = df['TARGET3'].values.tolist()
        targets = source2.copy()
        targets.extend(target1)
        targets.extend(target2)
        targets.extend(target3)
        values = df['AT PHARMA'].values.tolist()
        values1 = df['Hydrapharm'].values.tolist()
        values2 = df['BIOPURE'].values.tolist()
        values3 = df['SOMEPHARM'].values.tolist()
        values.extend(values1)
        values.extend(values2)
        values.extend(values3)
        labels = df['DESIGNATION'].values.tolist()
        labels.extend(['Hydra Pharm', 'Biopure', 'Somepharm'])

        fig = go.Figure(data=[go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=labels,
                color=['#a6cee3', '#1f78b4', '#b2df8a', '#33a02c', '#fb9a99', '#e31a1c', '#fdbf6f', '#ff7f00',
                       '#cab2d6', '#6a3d9a'] * 2
            ),
            link=dict(
                source=sources,  # indices correspond to labels, eg A1, A2, A1, B1, ...
                target=targets,
                value=values,
                color=['#a6cee3', '#1f78b4', '#b2df8a', '#33a02c', '#fb9a99', '#e31a1c', '#fdbf6f', '#ff7f00',
                       '#cab2d6', '#6a3d9a'] * 2

            ))])

        fig.update_layout(title_text="Basic Sankey Diagram", font_size=10)
        fig.show()

    @staticmethod
    def progression_over_time_mile_stone(start: datetime, end: datetime, actual_date: datetime,
                                         actual_progress: float,
                                         target_progress: float) -> float:
        time_progression = (end - actual_date).days / (end - start).days
        value_progression = actual_progress / target_progress
        return time_progression - value_progression - 1

    @staticmethod
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


def load(df: pnd.DataFrame):
    # GSKSalesGraph.indicator_figure()
    # GSKSalesGraph.sunburst_figure()
    # GSKSalesGraph.sunburst_bis()
    # GSKSalesGraph.bar_figure()
    # GSKSalesGraph.stock_bar()
    GSKSalesGraph.sankey_chart(df)
