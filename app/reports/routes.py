from flask import Blueprint, render_template, current_app
from flask_login import login_required, current_user

from app.extensions.db import db
from app.extensions.plotly_visualizations import generate_histogram_chart, generate_histogram_chart_horizontal
from app.models.video import VideoPost
from app.services.pose_dimension_calculator import PoseDimensionCalculator
from app.services.pose_spatial_classifier import PoseSpatialClassifier
from app.services.pose_sequence_analyzer import PoseSequenceAnalyzer

import os
import json
import pandas as pd
import plotly
import pytz

bp = Blueprint("reports", __name__, url_prefix="/reports")
tz = pytz.timezone('UTC')

@bp.route("/<id>/", methods=["GET", "POST"])
@login_required
def view_dance_report(id):
    video_post = VideoPost.query.get_or_404(id)
    
    if not video_post.is_calculated:
        pd_filepath = os.path.join(current_app.config['FRAME_OUTPUT_FOLDER'],video_post.author_id,video_post.id,'pose_data_raw.csv')
        pd_read = pd.read_csv(pd_filepath)
        pd_savepath = os.path.join(current_app.config['FRAME_OUTPUT_FOLDER'],video_post.author_id,video_post.id,'pose_data.csv')
        pd_data = PoseDimensionCalculator(pd_read, is_video=True)
        pd_data.data.to_csv(pd_savepath, index=False)    
        video_post.is_calculated = True
        db.session.add(video_post)
        db.session.commit()
    else:
        pd_filepath = os.path.join(current_app.config['FRAME_OUTPUT_FOLDER'],video_post.author_id,video_post.id,'pose_data.csv')
        pd_read = pd.read_csv(pd_filepath)
        
        tricks = pd.read_csv(os.path.join('app', 'static', 'dictionary', 'tricks', 'pose_data.csv'))
        ref_body = pd.read_csv(os.path.join('app', 'static', 'dictionary', 'positions','body','pose_data.csv'))
        ref_legs = pd.read_csv(os.path.join('app', 'static', 'dictionary', 'positions','legs','pose_data.csv'))
        ref_grip = pd.read_csv(os.path.join('app', 'static', 'dictionary', 'positions','grip', 'pose_data.csv'))
        
        classified = PoseSpatialClassifier(pd_read, ref_body, ref_legs, ref_grip)
        results = PoseSequenceAnalyzer(classified.data, tricks)
        
        fig_body = generate_histogram_chart(results.data, 'pos_body', video_post.duration)
        fig_body_hbar = json.dumps(fig_body, cls=plotly.utils.PlotlyJSONEncoder)
        
        fig_grip = generate_histogram_chart_horizontal(results.data, 'pos_grip', video_post.duration)
        fig_grip_hbar = json.dumps(fig_grip, cls=plotly.utils.PlotlyJSONEncoder)
        
        fig_legs = generate_histogram_chart_horizontal(results.data, 'pos_legs', video_post.duration)
        fig_legs_hbar = json.dumps(fig_legs, cls=plotly.utils.PlotlyJSONEncoder)
        
        fig_tricks = generate_histogram_chart_horizontal(results.data, 'pos_trick', video_post.duration)
        fig_tricks_hbar = json.dumps(fig_tricks, cls=plotly.utils.PlotlyJSONEncoder)
        
        pd_data = results.data.to_dict(orient='records')
        
        spin_count = results.spin_count
        inversion_count = results.invert_count
        
    
    return render_template("report.html", title=f"{video_post.title}",
                           video_post=video_post,
                           pd_data=pd_data,
                           spin_count=spin_count,
                           inversion_count=inversion_count,
                           fig_body_hbar=fig_body_hbar,
                           fig_legs_hbar=fig_legs_hbar,
                           fig_grip_hbar=fig_grip_hbar,
                           fig_tricks_hbar=fig_tricks_hbar,
    )