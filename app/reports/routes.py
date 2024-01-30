from flask import Blueprint, render_template, current_app, flash, redirect, url_for
from flask_login import login_required, current_user

from app.extensions.db import db
from app.extensions.plotly_visualizations import generate_histogram_chart, generate_histogram_chart_horizontal
from app.extensions.plotly_pose_animation import plotly_dynamic_pose_figure
from app.extensions.plotly_polar_plot import plot_polar_angles
from app.extensions.plotly_dance_timeline import plotly_visualize_timeline
from app.models import VideoPost, VideoReport
from app.services.pose_dimension_calculator import PoseDimensionCalculator
from app.services.pose_spatial_classifier import PoseSpatialClassifier
from app.services.pose_sequence_analyzer import PoseSequenceAnalyzer
from app.services.timeline_visual import generate_timeline_image
from app.utilities.static_files import load_reference_data

import os
from datetime import datetime
import json
import pandas as pd
import plotly
import plotly.express as px
import pytz

bp = Blueprint("reports", __name__, url_prefix="/reports")
tz = pytz.timezone('UTC')

def process_pose_data(source_path, save_path, video_post, tricks, ref_body, ref_legs, ref_grip):
    with open(source_path, 'r') as file:
        pd_read = pd.read_csv(file)
    pd_calculated = PoseDimensionCalculator(pd_read, is_video=True)
    pd_classified = PoseSpatialClassifier(
        pd_calculated.data, ref_body, ref_legs, ref_grip)
    results = PoseSequenceAnalyzer(pd_classified.data, tricks)
    pd_results = results.data
    print("inversion count", results.inversion_count)

    if len(pd_results) > 0:
        pd_results.to_csv(save_path, index=False)
        video_post.is_calculated = True

        top_tricks = pd_results[pd_results['pos_trick'] != 'undefined']['pos_trick'].value_counts().nlargest(3).index.tolist()
        top_legs = pd_results[pd_results['pos_legs'] != 'undefined']['pos_legs'].value_counts().nlargest(3).index.tolist()
        top_grip = pd_results[pd_results['pos_grip'] != 'undefined']['pos_grip'].value_counts().nlargest(3).index.tolist()

        new_report = VideoReport(
            author_id=video_post.author_id,
            video_id=video_post.id,
            spin_count=str(results.spin_count),
            inversion_count=str(results.inversion_count),
            detected_tricks=','.join(top_tricks),
            detected_legs=','.join(top_legs),
            detected_grip=','.join(top_grip),
            created_on=datetime.utcnow()
        )

        db.session.add(video_post)
        db.session.add(new_report)
        db.session.commit()

        return pd_results
    else:
        return None


@bp.route("/<id>/", methods=["GET", "POST"])
@login_required
def overview(id):
    video_post = VideoPost.query.get_or_404(id)
    if not video_post.is_calculated:
        tricks, ref_body, ref_legs, ref_grip = load_reference_data()
        pd_filepath = os.path.join(current_app.config['FRAME_OUTPUT_FOLDER'], video_post.author_id, video_post.id, 'pose_data_raw.csv')
        pd_savepath = os.path.join(current_app.config['FRAME_OUTPUT_FOLDER'], video_post.author_id, video_post.id, 'pose_data.csv')
        pd_results = process_pose_data(pd_filepath, pd_savepath, video_post, tricks, ref_body, ref_legs, ref_grip)        
        annotated_dir = os.path.join(current_app.config['FRAME_OUTPUT_FOLDER'], video_post.author_id, video_post.id, 'annotated')
        generate_timeline_image(annotated_dir, pd_results)        
        timeline_image = generate_timeline_image(annotated_dir, pd_results)
        
        if timeline_image:
            print("timeline image generated")
            
        if pd_results is None:
            flash("Something went wrong")
            return redirect(url_for('diary.all_dance_entries'))
        else:
            return redirect(url_for('reports.overview', id=video_post.id))
    else:
        video_report = VideoReport.query.filter_by(video_id=video_post.id, author_id=video_post.author_id).first()
        
        if video_post.report_id is None:
            video_post.report_id = video_report.id
            db.session.commit()
        
        if not video_report:
            flash("Report not found")
            return redirect(url_for('diary.all_dance_entries'))

        pd_filepath = os.path.join(
            current_app.config['FRAME_OUTPUT_FOLDER'], video_post.author_id, video_post.id, 'pose_data.csv')
        with open(pd_filepath, 'r') as file:
            pd_results = pd.read_csv(file)
            
    fig_timeline = plotly_visualize_timeline(pd_results, video_report.created_on, video_report, 0.12)
    fig_plot = json.dumps(fig_timeline, cls=plotly.utils.PlotlyJSONEncoder)

    pd_data = pd_results.to_dict(orient='records')

    return render_template("report.html", title=f"{video_post.title}",
                           video_post=video_post,
                           pd_data=pd_data,
                           video_report=video_report,
                           fig_plot=fig_plot,
                           pd_filepath=pd_filepath
                           )


def generate_charts(pd_results, duration):
    fig_body = generate_histogram_chart(pd_results, 'pos_body', duration)
    fig_body_hbar = json.dumps(fig_body, cls=plotly.utils.PlotlyJSONEncoder)
    fig_grip = generate_histogram_chart_horizontal(
        pd_results, 'pos_grip', duration)
    fig_grip_hbar = json.dumps(fig_grip, cls=plotly.utils.PlotlyJSONEncoder)
    fig_legs = generate_histogram_chart_horizontal(
        pd_results, 'pos_legs', duration)
    fig_legs_hbar = json.dumps(fig_legs, cls=plotly.utils.PlotlyJSONEncoder)
    fig_tricks = generate_histogram_chart_horizontal(
        pd_results, 'pos_trick', duration)
    fig_tricks_hbar = json.dumps(
        fig_tricks, cls=plotly.utils.PlotlyJSONEncoder)

    return {
        'fig_body_hbar': fig_body_hbar,
        'fig_legs_hbar': fig_legs_hbar,
        'fig_grip_hbar': fig_grip_hbar,
        'fig_tricks_hbar': fig_tricks_hbar
    }


@bp.route("/<id>/animation", methods=["GET", "POST"])
@login_required
def vis_animation(id):
    video_post = VideoPost.query.get_or_404(id)
    pd_filepath = os.path.join(
        current_app.config['FRAME_OUTPUT_FOLDER'], video_post.author_id, video_post.id, 'pose_data.csv')
    data = pd.read_csv(pd_filepath)
    fig = plotly_dynamic_pose_figure(data, right_arm=True,left_arm=True, right_leg=True, left_leg=True)
    fig_render = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template("reports/simple_plot.html",
                           title=f"{video_post.title}",
                           description="Visualize your dance moves as simple shapes to easily spot patterns and improve your technique",
                           fig_render=fig_render,
                           video_post=video_post)


@bp.route("/<id>/motion", methods=["GET", "POST"])
@login_required
def vis_range_of_motion(id):
    video_post = VideoPost.query.get_or_404(id)
    pd_filepath = os.path.join(
        current_app.config['FRAME_OUTPUT_FOLDER'], video_post.author_id, video_post.id, 'pose_data.csv')
    data = pd.read_csv(pd_filepath)
    fig = plot_polar_angles(data)
    fig_render = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template("reports/simple_plot.html",
                           title=f"{video_post.title}",
                           description="The full scope of your movement. In this plot, you will see the range of motion your spine, right and left arms and legs",
                           fig_render=fig_render,
                           video_post=video_post)