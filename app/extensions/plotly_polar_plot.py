import plotly.graph_objects as go


def plot_polar_angles(data):
    colors = ['#e6194B', '#f58231', '#ffe119', '#bfef45',
              '#3cb44b', '#42d4f4', '#4363d8', '#911eb4', '#f032e6']
    a_cols = ['a_head_to_stomach', 'a_chest_to_hip', 'a_mid_hip_to_knees', 'a_rgt_shoulder_to_wrist',
              'a_rgt_shoulder_to_knee', 'a_rgt_hip_to_foot', 'a_lft_shoulder_to_wrist', 'a_lft_shoulder_to_knee', 'a_lft_hip_to_foot']

    groups = {
        "Spine": ['a_head_to_stomach', 'a_chest_to_hip', 'a_mid_hip_to_knees'],
        "R.Arm": ['a_rgt_shoulder_to_wrist'],
        "L.Arm": ['a_lft_shoulder_to_wrist'],
        "R.Leg": ['a_rgt_shoulder_to_knee', 'a_rgt_hip_to_foot'],
        "L.Leg": ['a_lft_shoulder_to_knee', 'a_lft_hip_to_foot'],
    }

    fig = go.Figure()

    for idx, col in enumerate(a_cols):
        fig.add_trace(go.Scatterpolar(
            r=data.index,
            theta=data[col],
            mode="markers",
            fill="toself",
            name=col,
            marker=dict(size=5, color=colors[idx], line=dict(
                color=colors[idx], width=2), opacity=0.5)
        ))

    buttons = []
    for group_name, group_cols in groups.items():
        visibility = [col in group_cols for col in a_cols]
        buttons.append({
            "label": group_name,
            "method": "update",
            "args": [{"visible": visibility}]
        })

    buttons.append({
        "label": "Show All",
        "method": "update",
        "args": [{"visible": [True] * len(a_cols)}]
    })

    fig.update_layout(
        showlegend=True,
        updatemenus=[{"buttons": buttons,
                      "direction": "down", "showactive": True}],
        plot_bgcolor='white',
        autosize=True, margin=dict(l=20, r=20, t=20, b=20)
    )

    return fig
