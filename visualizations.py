import plotly.express as px
import plotly.graph_objs as go
import plotly.utils
import json
import numpy as np

def create_summary_charts(processed_data):
    summary = processed_data['summary']
    charts = {}

    # Numeric data summary
    for col, stats in summary['numeric_stats'].items():
        fig = go.Figure()
        fig.add_trace(go.Box(y=processed_data['data'][col], name=col))
        fig.update_layout(title=f'Summary of {col}')
        charts[f'{col}_summary'] = fig.to_json()

    # Categorical data summary
    for col, counts in summary['categorical_stats'].items():
        fig = px.bar(x=list(counts.keys()), y=list(counts.values()), title=f'Distribution of {col}')
        charts[f'{col}_summary'] = fig.to_json()

    return charts

def create_custom_plot(data, x_axis, y_axis):
    fig = px.scatter(data, x=x_axis, y=y_axis, title=f'{x_axis} vs {y_axis}')
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

def create_search_result_plot(search_results, search_term):
    if len(search_results) > 10:
        # If there are more than 10 results, show a summary
        summary = search_results.describe()
        fig = go.Figure(data=[go.Table(
            header=dict(values=list(summary.columns)),
            cells=dict(values=[summary[col] for col in summary.columns])
        )])
    else:
        # If there are 10 or fewer results, show all the data
        fig = go.Figure(data=[go.Table(
            header=dict(values=list(search_results.columns)),
            cells=dict(values=[search_results[col] for col in search_results.columns])
        )])
    
    fig.update_layout(title=f"Search Results for '{search_term}'")
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)