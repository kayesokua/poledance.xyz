import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px

def calculate_time(row, timestamp, increment):
    frame_number = row['frame_no']
    start_time = timestamp + timedelta(seconds=increment * frame_number)
    finish_time = start_time + timedelta(seconds=increment)
    return pd.Series([start_time, finish_time])

def plotly_visualize_timeline(data, timestamp, video_report, increment):

    combined = data.copy()
    combined[['Start', 'Finish']] = combined.apply(lambda row: calculate_time(row, timestamp, increment), axis=1)
    
    detected_tricks = video_report.detected_tricks
    detected_grip = video_report.detected_grip
    detected_legs = video_report.detected_legs
    
    color_map = {
        "None": "gray",
        "front": "gray",
        "back": "cornflowerblue",
        "upright": "gray",
        "inversion": "cornflowerblue",
        "horizontal": "lightseagreen",
        "undefined":"gray",
        } 

    plot_data = []
    for i in range(len(combined) - 1):
        current_trick = combined.iloc[i]['pos_trick']
        trick_resource = str(current_trick) if str(current_trick) in detected_tricks else "None"
        
        current_legs = combined.iloc[i]['pos_legs']
        legs_resource = str(current_legs) if str(current_legs) in detected_legs else "None"
        
        current_grip = combined.iloc[i]['pos_grip']
        grip_resource = str(current_grip) if str(current_grip) in detected_grip else "None"
        
        plot_data.append({
            'Category': 'Body Position',
            'Start': combined.iloc[i]['Finish'],
            'Finish': combined.iloc[i + 1]['Finish'],
            'Resource': combined.iloc[i]['pos_body']
        })
        plot_data.append({
            'Category': 'Face Position',
            'Start': combined.iloc[i]['Finish'],
            'Finish': combined.iloc[i + 1]['Finish'],
            'Resource': combined.iloc[i]['pos_face']
        })
        plot_data.append({
            'Category': 'Legs Position',
            'Start': combined.iloc[i]['Finish'],
            'Finish': combined.iloc[i + 1]['Finish'],
            'Resource': legs_resource
        })
        plot_data.append({
            'Category': 'Grip Position',
            'Start': combined.iloc[i]['Finish'],
            'Finish': combined.iloc[i + 1]['Finish'],
            'Resource': grip_resource 
        }),
        plot_data.append({
            'Category': 'Pole Shapes',
            'Start': combined.iloc[i]['Finish'],
            'Finish': combined.iloc[i + 1]['Finish'],
            'Resource': trick_resource
        })
    
    plot_df = pd.DataFrame(plot_data)
    fig_timeline = px.timeline(plot_df, x_start="Start", x_end="Finish", y="Category", color="Resource", labels={'Category': 'Type'},
                               color_discrete_map=color_map)
    fig_timeline.update_layout(legend=dict(orientation='h'))



    return fig_timeline
