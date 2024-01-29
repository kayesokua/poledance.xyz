import plotly.graph_objects as go
import pandas as pd
import numpy as np

def plotly_pose_contact_points(data, idx, spine=True, right_arm=False, left_arm=False, right_leg=False, left_leg=False, save_image=False):
    threshold = 0.04
    row = data.iloc[idx]
    
    x_cols = sorted([col for col in data.columns if col.startswith('landmark_') and col.endswith('_x')])
    y_cols = sorted([col for col in data.columns if col.startswith('landmark_') and col.endswith('_y')])
    x = row[x_cols].values
    y = row[y_cols].values

    fig = go.Figure()

    for i in range(11, 28):
        color = 'magenta' if i % 2 == 0 else 'lime'
        fig.add_trace(go.Scatter(x=[x[i]], y=[y[i]], mode='markers', marker=dict(color=color, size=5)))

    for i in range(11, 28):
        for j in range(i+1, 28):
            if np.hypot(x[i] - x[j], y[i] - y[j]) < threshold:
                fig.add_trace(go.Scatter(x=[x[i], x[j]], y=[y[i], y[j]], mode='lines', line=dict(color='blue', width=2)))

    Scolor  = 'black' if spine else 'gray'
    RAcolor = 'magenta' if right_arm else 'gray'
    LAcolor = 'lime' if left_arm else 'gray'
    RLcolor = 'magenta' if right_leg else 'gray'
    LLcolor = 'lime' if left_leg else 'gray'

    Sx = [row['head_x'], row['chest_x'], row['stomach_x'], row['hip_x']]
    Sy = [row['head_y'], row['chest_y'], row['stomach_y'], row['hip_y']]
    Tx = [row['landmark_11_x'], row['landmark_12_x'], row['landmark_24_x'],row['landmark_23_x'],row['landmark_11_x']]
    Ty = [row['landmark_11_y'], row['landmark_12_y'], row['landmark_24_y'],row['landmark_23_y'],row['landmark_11_y']]
    RAx = [row['landmark_12_x'], row['landmark_14_x'], row['landmark_16_x'], row['knuckles_right_x']]
    RAy = [row['landmark_12_y'], row['landmark_14_y'], row['landmark_16_y'], row['knuckles_right_y']]  
    LAx = [row['landmark_11_x'], row['landmark_13_x'], row['landmark_15_x'], row['knuckles_left_x']]
    LAy = [row['landmark_11_y'], row['landmark_13_y'], row['landmark_15_y'], row['knuckles_left_y']]  
    RLx = [row['landmark_24_x'], row['landmark_26_x'], row['landmark_28_x'],row['landmark_32_x']]
    RLy = [row['landmark_24_y'], row['landmark_26_y'], row['landmark_28_y'],row['landmark_32_y']]
    LLx = [row['landmark_23_x'], row['landmark_25_x'], row['landmark_27_x'],row['landmark_31_x']]
    LLy = [row['landmark_23_y'], row['landmark_25_y'], row['landmark_27_y'],row['landmark_31_y']]
    
    fig.add_trace(go.Scatter(x=Sx, y=Sy, mode='lines+markers', line=dict(color=Scolor, width=2),opacity=0.5, name='Head'))
    fig.add_trace(go.Scatter(x=Tx, y=Ty, mode='lines+markers', line=dict(color='silver', width=2),opacity=0.5, name='Torso'))
    fig.add_trace(go.Scatter(x=RAx, y=RAy, mode='lines+markers', line=dict(color=RAcolor, width=2),opacity=0.5, name='R. Arm'))
    fig.add_trace(go.Scatter(x=RLx, y=RLy, mode='lines+markers', line=dict(color=RLcolor, width=2),opacity=0.5, name='R. Leg'))
    fig.add_trace(go.Scatter(x=LAx, y=LAy, mode='lines+markers', line=dict(color=LAcolor, width=2),opacity=0.5, name='L. Arm'))
    fig.add_trace(go.Scatter(x=LLx, y=LLy, mode='lines+markers', line=dict(color=LLcolor, width=2),opacity=0.5, name='L. Leg'))
 
    fig.add_shape(type="circle", xref="x", yref="y", x0=row['head_x'] - 0.03, y0=row['head_y'] - 0.03,  x1=row['head_x'] + 0.03, y1=row['head_y'] + 0.03, line_color=Scolor, opacity=0.7)
    fig.add_shape(type="circle", xref="x", yref="y", x0=row['landmark_16_x'] - 0.02, y0=row['landmark_16_y'] - 0.02,  x1=row['landmark_16_x'] + 0.02, y1=row['landmark_16_y'] + 0.02, line_color=RAcolor, opacity=0.7)
    fig.add_shape(type="circle", xref="x", yref="y", x0=row['landmark_15_x'] - 0.02, y0=row['landmark_15_y'] - 0.02,  x1=row['landmark_15_x'] + 0.02, y1=row['landmark_15_y'] + 0.02, line_color=LAcolor, opacity=0.7)
    fig.add_shape(type="circle", xref="x", yref="y", x0=row['landmark_28_x'] - 0.02, y0=row['landmark_28_y'] - 0.02,  x1=row['landmark_28_x'] + 0.02, y1=row['landmark_28_y'] + 0.02, line_color=RLcolor, opacity=0.7)
    fig.add_shape(type="circle", xref="x", yref="y", x0=row['landmark_27_x'] - 0.02, y0=row['landmark_27_y'] - 0.02,  x1=row['landmark_27_x'] + 0.02, y1=row['landmark_27_y'] + 0.02, line_color=LLcolor, opacity=0.7)


    fig.update_xaxes(range=[0, 1], showgrid=True, gridwidth=0.5, gridcolor='silver', tickvals=np.arange(0, 1.05, 0.05), ticktext=['']*21)
    fig.update_yaxes(range=[1, 0], showgrid=True, gridwidth=0.5, gridcolor='silver', tickvals=np.arange(0, 1.05, 0.05), ticktext=['']*21)
    fig.update_layout(autosize=True, margin=dict(l=20, r=20, t=20, b=20), plot_bgcolor='white')
    fig.update_layout(showlegend=False)
    
    return fig