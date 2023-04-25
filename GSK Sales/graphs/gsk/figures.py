import plotly.graph_objects as go
import data


def indicator(achieved: float, target: float, ly_achieved: float, label: str,
              sales_as: data.SalesAs = data.SalesAs(data.SalesAs.value)) -> go.Figure:
    # progress_over_time = progression_over_time_mile_stone(actual_progress=actual,
    #                                                       target_progress=target, )
    gauge_range = sorted([target, achieved, ly_achieved])[-1] * 1.1
    fig = go.Figure()
    fig.add_trace(go.Indicator(
        mode="number+gauge+delta", value=achieved,
        domain={'x': [0, 1], 'y': [0.5, 1]},
        delta={'reference': target, 'position': "top"},
        title={'text': f"<b>{label}</b><br><span style='color: gray; font-size:0.8em'>{sales_as.name}</span>",
               'font': {"size": 14}},
        gauge={
            'axis': {'range': [None, gauge_range]},
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 1, 'value': target},

            'bgcolor': 'white',
            'steps': [
                {'range': [0, ly_achieved], 'color': '#DDDDDD'}],
            'bar': {'color': '#10BA4D'}}))
    fig.add_trace(go.Indicator(
        mode='delta',
        value=((achieved + target) / target * 100) if target != 0 else 0,
        delta={'reference': 100, 'suffix': '%',
               'increasing': {'color': data.get_delta_color(.9)}},
        domain={'x': [0.25, .75], 'y': [0.2, 0.5]}
    ))
    return fig


def sunburst() -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Sunburst(
        values=[1000, 2000, 3000, 6000],
        labels=['Augmentin', 'Clamoxyl', 'Ventoline', 'Flixotide'],
        parents=['', '', '', ''],
        branchvalues='total',
        insidetextorientation='radial',
    ))

    return fig


def water_fall() -> go.Figure:
    fig = go.Figure(go.Waterfall(
        name="20", orientation="v",
        measure=["relative", "relative", "relative", "relative", "total"],
        x=["Augmentin", "Clamoxyl", "Ventoline", "Flixotide", 'Total'],
        textposition="outside",
        text=["1000", "2000", "3000", "6000", "Total"],
        y=[1000, 2000, 3000, 6000, 0],
        connector={"line": {"color": "rgb(63, 63, 63)"}},
    ))

    fig.update_layout(
        # showlegend=True
    )
    return fig
