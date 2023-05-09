import plotly.graph_objects as go
import plotly.express as px
import data as d
import name_space as nm
import pandas as pnd

figures_cache: dict[str, go.Figure] = {}


def indicator(achieved: float,
              target: float,
              ly_achieved: float,
              label: str,
              sales_as: d.SalesAs = d.SalesAs(d.SalesAs.value)) -> go.Figure:
    # progress_over_time = progression_over_time_mile_stone(actual_progress=actual,
    #                                                       target_progress=target, )
    gauge_range = sorted([target, achieved, ly_achieved])[-1] * 1.04
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
               'increasing': {'color': d.get_delta_color(.9)}},
        domain={'x': [0.35, .65], 'y': [0, 0.4]},
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
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',
                      margin=dict(t=80, l=0, r=0, b=15))
    return fig


def sunburst(parents: list[str],
             labels: list[str],
             values: list[float],
             colors: list[str],
             rfcs: list[float]) -> go.Figure:
    fig = heat_map_sunburst(parents=parents,
                            labels=labels,
                            values=values,
                            rfcs=rfcs)
    fig.add_trace(go.Sunburst(
        values=values,
        labels=labels,
        parents=parents,
        branchvalues='total',
        insidetextorientation='radial',
        textinfo='value+label+percent root',
        visible=False,
        marker=dict(
            colors=colors
        )
    ))
    fig.layout.update(
        updatemenus=[go.layout.Updatemenu(
            type="buttons", direction="right", active=1, x=0.5, y=1.2,
            buttons=list([dict(label="Heatmap", method="update",
                               args=[{"visible": [True, False]}, {"title": "Heatmap"}]),
                          dict(label="Repartition", method="update",
                               args=[{"visible": [False, True]}, {"title": "Repartition"}])]))])

    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', )
    return fig


def heat_map_sunburst(parents: list[str],
                      labels: list[str],
                      values: list[float],
                      rfcs: list[float]) -> go.Figure:
    progress = [(r / rfcs[i] * 100) for i, r in enumerate(values)]
    fig = px.sunburst(names=labels,
                      parents=parents,
                      values=values,
                      color=progress,
                      color_continuous_scale='rdylgn',
                      range_color=[0, 100],
                      )
    fig.update_traces({'insidetextorientation': 'radial'})
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',
                      margin=dict(t=0, l=0, r=0, b=30),
                      coloraxis=dict(colorbar=dict(title='Achievments<Br>Rate (%)')), )
    return fig


def water_fall(name: str,
               measure: list[str],
               x_labels: list[str],
               text: list[str],
               values: list[float],
               colors: list[str]) -> go.Figure:
    fig = go.Figure(go.Waterfall(
        orientation="v",
        measure=measure,
        x=x_labels,
        textposition="outside",
        text=text,
        y=values,
        connector={"line": {"color": "rgb(63, 63, 63)"}},
    ))
    # for color, y, x in zip(colors, values, x_labels):
    #     fig.add_shape(type='rect',
    #                   xref='x',
    #                   yref='y',
    #                   x0=x,
    #                   # x1=x,
    #                   y0=0,
    #                   y1=y,
    #                   # y1=y,
    #                   label=dict(text=f"G:\n"),
    #                   fillcolor=color)
    fig.update_layout(
        showlegend=False
    )
    fig.update_layout(title=dict(text=name),
                      paper_bgcolor='rgba(0,0,0,0)',
                      margin=dict(l=0, r=0))
    return fig


def stocks_hist_bar(time: list[pnd.Timestamp],
                    quarantine_y: list[int],
                    available_y: list[int]) -> go.Figure:
    fig = go.Figure()
    quarantine_bar_trace: go.Bar = go.Bar(
        x=time,
        y=quarantine_y,
        name='Quarantine Stock',
        marker_color='indianred'
    )
    fig.add_trace(quarantine_bar_trace)
    fig.add_trace(go.Bar(
        x=time,
        y=available_y,
        name='Available Stock',
        marker_color='lightsalmon'
    ))

    # Here we modify the tickangle of the xaxis, resulting in rotated labels.
    fig.update_layout(barmode='overlay', xaxis_tickangle=-45, paper_bgcolor='rgba(0,0,0,0)')
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)')
    return fig


def sales_hist_bar(months: list[pnd.Timestamp],
                   targets: list[float],
                   cy_actuals: list[float],
                   ly_actuals: list[float],
                   sku: str = None,
                   sales_as: d.SalesAs = None) -> go.Figure:
    # months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
    #           'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    # targets = [25, 14, 26, 15, 20, 20, 16, 15, 12, 16, 14, 17]
    # actuals = [20, 14, 25, 16, 18, 22, 19, 15, 12, 16, 14, 17]
    # ly_actuals = [19, 14, 22, 14, 16, 19, 15, 14, 10, 12, 12, 16]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=months,
        y=cy_actuals,
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
        growth = (cy_actuals[idx] - ly_actuals[idx]) / ly_actuals[idx]
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
