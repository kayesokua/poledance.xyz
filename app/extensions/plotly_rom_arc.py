import numpy as np
import plotly.graph_objects as go


def plot_range_of_motion_arc(df):
    fig = go.Figure()
    
    angles = [
        'a_head_to_stomach', 'a_chest_to_hip', 'a_mid_hip_to_knees',
        'a_rgt_shoulder_to_wrist', 'a_rgt_shoulder_to_knee', 'a_rgt_hip_to_foot',
        'a_lft_shoulder_to_wrist', 'a_lft_shoulder_to_knee', 'a_lft_hip_to_foot'
    ]

    colors = [
        '#e6194B', '#f58231', '#ffe119', '#bfef45', '#3cb44b',
        '#42d4f4', '#4363d8', '#911eb4', '#f032e6'
    ]

    color_map = {angle: colors[i % len(colors)] for i, angle in enumerate(angles)}


    for angle in angles:
        angle_data = df[df['Angle'] == angle]
        if not angle_data.empty:
            min_angle = angle_data[angle_data['Type'] == 'Min']['Value'].values[0]
            max_angle = angle_data[angle_data['Type'] == 'Max']['Value'].values[0]

            theta = np.linspace(min_angle, max_angle, num=30)
            r_inner = np.zeros_like(theta)
            r_outer = np.ones_like(theta) * 5

            r = np.concatenate([r_inner, r_outer[::-1]])
            theta = np.concatenate([theta, theta[::-1]])

            fig.add_trace(go.Scatterpolar(
                r=r,
                theta=theta,
                fill='toself',
                opacity=0.5,
                name=angle.replace('a_', '').replace('_', ' to '),
                fillcolor=color_map[angle],
                line=dict(color=color_map[angle])
            ))

    fig.update_layout(
        title="Range of Motion: Average and Maximum",
        polar=dict(
            radialaxis=dict(showticklabels=False, ticks=''),
            angularaxis=dict(showticklabels=True, ticks='', direction='clockwise', rotation=90)
        )
    )

    return fig