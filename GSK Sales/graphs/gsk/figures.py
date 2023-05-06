import plotly.graph_objects as go
import plotly.express as px
import data
import pandas as pnd
import name_space as nm

figures_cache: dict[str, go.Figure] = {}


def indicator(achieved: float,
              target: float,
              ly_achieved: float,
              label: str,
              sales_as: data.SalesAs = data.SalesAs(data.SalesAs.value)) -> go.Figure:
    # progress_over_time = progression_over_time_mile_stone(actual_progress=actual,
    #                                                       target_progress=target, )
    gauge_range = sorted([target, achieved, ly_achieved])[-1] * 1.1
    fig = go.Figure()
    fig.add_trace(go.Indicator(
        mode="number+gauge+delta", value=achieved,
        domain={'x': [0, 1], 'y': [0.5, 1]},
        delta={'reference': target, 'position': "top"},
        title={'text': f"<b>{label}</b><br><span style='color: gray; font-size:0.9em'>{sales_as.name}</span>",
               'font': {"size": 16}},
        gauge={
            'axis': {'range': [None, gauge_range]},
            'threshold': {
                'line': {'color': "green", 'width': 4},
                'thickness': 1, 'value': target},

            'bgcolor': 'white',
            'steps': [
                {'range': [0, ly_achieved], 'color': '#DDDDDD'}],
            'bar': {'color': '#10BA4D'}}))
    # fig.add_annotation(x=.5,
    #                    y=0,
    #                    text='99.5 %',
    #                    showarrow=False,
    #                    font=dict(
    #                        family="Courier New, monospace",
    #                        size=20,
    #                        color="green",
    #                    ),
    #                    # bordercolor="#c7c7c7",
    #                    borderwidth=2,
    #                    borderpad=4,
    #                    bgcolor="#ff7f0e",
    #                    opacity=0.8,
    #                    )
    # fig.add_shape(type='line',
    #               x0=.1,
    #               y0=.35,
    #               x1=.9,
    #               y1=.35,
    #               line=dict(
    #                   color="grey",
    #                   width=.5,
    #               ))
    fig.add_trace(go.Indicator(
        mode='delta',
        value=((achieved + target) / target * 100) if target != 0 else 0,
        delta={'reference': 100, 'suffix': '%',
               'increasing': {'color': data.get_delta_color(.9)}},
        domain={'x': [0.25, .75], 'y': [0, 0.5]}
    ))
    # fig.add_shape(type='line',
    #               x0=.1,
    #               y0=.15,
    #               x1=.9,
    #               y1=.15,
    #               line=dict(
    #                   color="grey",
    #                   width=.5,
    #               ))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)')
    return fig


def sunburst() -> go.Figure:
    fig = color_map_sunburst()
    fig.add_trace(go.Sunburst(
        values=[1000, 2000, 3000, 6000],
        labels=['Augmentin', 'Clamoxyl', 'Ventoline', 'Flixotide'],
        parents=['', '', '', ''],
        branchvalues='total',
        insidetextorientation='radial',
        textinfo='value+label+percent root',
        visible=False,
    ))
    fig.layout.update(
        updatemenus=[go.layout.Updatemenu(
            type="buttons", direction="right", active=1, x=0.5, y=1.2,
            buttons=list([dict(label="Heatmap", method="update",
                               args=[{"visible": [True, False]}, {"title": "Heatmap"}]),
                          dict(label="Repartition", method="update",
                               args=[{"visible": [False, True]}, {"title": "Repartition"}])]))])

    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)')
    return fig


def color_map_sunburst() -> go.Figure:
    actuals = [1000, 2000, 3000, 6000]
    rfc = [1200, 3000, 2000, 6500]
    progress = [(r / rfc[i] * 100) for i, r in enumerate(actuals)]
    sunburst_df: pnd.DataFrame = pnd.DataFrame(data={'SKU': ['Augmentin', 'Clamoxyl', 'Ventoline', 'Flixotide'],
                                                     'SALES VALUE(GBP)': actuals,
                                                     'RFC UNIT': rfc,
                                                     'REALISATIONS': progress})
    fig = px.sunburst(sunburst_df, path=['SKU'],
                      values='SALES VALUE(GBP)', color='REALISATIONS',
                      color_continuous_scale='rdylgn',
                      range_color=[0, 100], )
    fig.update_traces({'insidetextorientation': 'radial'})
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)')
    return fig


def water_fall() -> go.Figure:
    fig = go.Figure(go.Waterfall(
        name="Brands", orientation="v",
        measure=["relative", "relative", "relative", "relative", "total"],
        x=["Augmentin", "Clamoxyl", "Ventoline", "Flixotide", 'Total'],
        textposition="outside",
        text=["1000", "2000", "3000", "6000", "Total"],
        y=[1000, 2000, 3000, 6000, 0],
        connector={"line": {"color": "rgb(63, 63, 63)"}},
    ))

    fig.update_layout(
        showlegend=True
    )
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)')
    return fig


def stocks_hist_bar() -> go.Figure:
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=months,
        y=[20, 14, 25, 16, 18, 22, 19, 15, 12, 16, 14, 17],
        name='Available Stock',
        marker_color='indianred'
    ))
    fig.add_trace(go.Bar(
        x=months,
        y=[19, 14, 22, 14, 16, 19, 15, 14, 10, 12, 12, 16],
        name='Quarentain Stock',
        marker_color='lightsalmon'
    ))

    # Here we modify the tickangle of the xaxis, resulting in rotated labels.
    fig.update_layout(barmode='overlay', xaxis_tickangle=-45, paper_bgcolor='rgba(0,0,0,0)')
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)')
    return fig


def sales_hist_bar() -> go.Figure:
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    targets = [25, 14, 26, 15, 20, 20, 16, 15, 12, 16, 14, 17]
    actuals = [20, 14, 25, 16, 18, 22, 19, 15, 12, 16, 14, 17]
    ly_actuals = [19, 14, 22, 14, 16, 19, 15, 14, 10, 12, 12, 16]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=months,
        y=actuals,
        name='2023',
        marker_color=nm.NameMap.solid_gsk_orange
    ))
    for idx, month in enumerate(months):
        fig.add_shape(type='line',
                      xref='x',
                      yref='y',
                      x0=idx - .9 / 2,
                      y0=targets[idx],
                      x1=idx + .9 / 14,
                      y1=targets[idx],
                      line=dict(
                          color="red",
                          width=2,
                      ),
                      )
        growth = (actuals[idx] - ly_actuals[idx]) / ly_actuals[idx]
        fig.add_shape(type="rect",
                      xref='x', yref='y',
                      fillcolor=nm.NameMap.rgba(198, 244, 229, 0.94) if growth > 0.03 else nm.NameMap.rgba(244, 198,
                                                                                                           198, .94),
                      line=dict(color='seagreen' if growth > 0.03 else 'red'),
                      x0=idx - .9 / 2,
                      y0=1,
                      x1=idx + .9 / 2,
                      y1=3,
                      label=dict(text=f"G:\n{growth:.2f}"), )
    fig.add_trace(go.Bar(
        x=months,
        y=ly_actuals,
        name='2022',
        marker_color='grey'
    ))

    # Here we modify the tickangle of the xaxis, resulting in rotated labels.
    fig.update_layout(barmode='group', xaxis_tickangle=-45)
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)')
    return fig
