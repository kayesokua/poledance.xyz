import plotly.express as px
import pandas as pd

def generate_histogram_chart(data, category, duration):
    agg_data = data[category].value_counts().reset_index()
    print(agg_data)
    print(agg_data.columns)
    agg_data.columns = [category, 'count']
    agg_data['duration'] = agg_data['count'] / len(data) * duration
    fig = px.bar(agg_data, x=category, y='duration')
    return fig

def generate_histogram_chart_horizontal(data, category, duration):
    agg_data = data[category].value_counts().reset_index()
    print(agg_data)
    print(agg_data.columns)
    agg_data.columns = [category, 'count']
    agg_data['duration'] = agg_data['count'] / len(data) * duration
    fig = px.bar(agg_data, x='duration', y=category)
    return fig