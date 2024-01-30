from flask import Blueprint, flash, redirect, render_template, current_app, request, url_for
from flask_login import login_required, current_user

from app.extensions.db import db
from app.extensions.pose_landmarker import generate_pose_landmark_dictionary
from app.extensions.plotly_rom_arc import plot_range_of_motion_arc
from app.models import VideoPost, VideoReport
from app.utilities.video_utils import *
from app.utilities.file_system_utils import *

from .forms import NewDancePost, EditDancePost

from datetime import datetime
import json
import plotly
import plotly.express as px
import pandas as pd
import pytz
import uuid
import numpy as np
from werkzeug.utils import secure_filename

bp = Blueprint("diary", __name__, url_prefix="/diary")
tz = pytz.timezone('UTC')

@bp.route("/", methods=["GET"])
@login_required
def all_dance_entries():
    video_posts = VideoPost.query.filter_by(author_id=current_user.id, deleted=False).order_by(VideoPost.created_on.desc()).all()
    return render_template("home.html", video_posts=video_posts, title="My Pole Diary")

@bp.route("/summary", methods=["GET"])
@login_required
def all_dance_summary():
    video_posts = VideoPost.query.filter_by(author_id=current_user.id, deleted=False, is_calculated=True).order_by(VideoPost.created_on.desc()).all()
    video_reports = VideoReport.query.filter_by(author_id=current_user.id, deleted=False).order_by(VideoReport.created_on.desc()).all()
    pos_body_counts = pd.Series(dtype=int)
    total_tricks = 0
    total_spins = 0
    total_inversions = 0
    tricks_frequency = {}
    total_duration = 0.0
    range_of_motion = {}
    
    for post in video_posts:
        total_duration += post.duration
        
        csv_path = os.path.join(current_app.config['FRAME_OUTPUT_FOLDER'], post.author_id, post.id, 'pose_data.csv')
        try:
            pose_data = pd.read_csv(csv_path)
            pos_body_counts = pos_body_counts.add(pose_data['pos_body'].value_counts(), fill_value=0)
            
            for col in pose_data.columns:
                if col.startswith('a_') and not col.endswith('_diff'):
                    min_angle = np.mean(pose_data[col])
                    max_angle = np.max(pose_data[col])

                    # Update global min and max
                    if col not in range_of_motion:
                        range_of_motion[col] = {'min': min_angle, 'max': max_angle}
                    else:
                        range_of_motion[col]['min'] = min(range_of_motion[col]['min'], min_angle)
                        range_of_motion[col]['max'] = max(range_of_motion[col]['max'], max_angle)


        except FileNotFoundError:
            pass
        
    for report in video_reports:
        total_spins += int(report.spin_count)
        total_inversions += int(report.inversion_count)
        
        if report.detected_tricks:
            for trick in report.detected_tricks.split(','):
                total_tricks += 1
                tricks_frequency[trick] = tricks_frequency.get(trick, 0) + 1
    
    fig_pos_body = px.pie(pos_body_counts, values=pos_body_counts, names=pos_body_counts.index, title="Body Classifications")
    fig_body = json.dumps(fig_pos_body, cls=plotly.utils.PlotlyJSONEncoder)
    
    tricks_df = pd.DataFrame(list(tricks_frequency.items()), columns=['Trick', 'Count'])
    fig_pos_tricks = px.bar(tricks_df, x='Count', y='Trick', orientation='h', title="Frequency of Tricks")
    fig_tricks = json.dumps(fig_pos_tricks, cls=plotly.utils.PlotlyJSONEncoder)
    
    range_of_motion_df = pd.DataFrame.from_dict(range_of_motion, orient='index').reset_index()
    range_of_motion_df.columns = ['Angle', 'Min', 'Max']
    range_of_motion_df = range_of_motion_df.melt(id_vars=['Angle'], value_vars=['Min', 'Max'], var_name='Type', value_name='Value')

    fig_total_rom = plot_range_of_motion_arc(range_of_motion_df)
    fig_rom = json.dumps(fig_total_rom, cls=plotly.utils.PlotlyJSONEncoder)


    return render_template("summary.html",
                           video_posts=video_posts,
                           video_reports=video_reports,
                           pos_body_counts=pos_body_counts,
                           total_duration=total_duration,
                           total_tricks=total_tricks,
                           tricks_frequency=tricks_frequency,
                           total_spins=total_spins,
                           total_inversions=total_inversions,
                           fig_body=fig_body,
                           fig_tricks=fig_tricks,
                           fig_rom=fig_rom,
                        
                           title="My Dance Summary")

@bp.route("/new", methods=["GET", "POST"])
@login_required
def new_dance_entry():
    form = NewDancePost()
    
    if request.method == 'GET':
        form.title.data = VideoPost.generate_default_title()
    
    if form.validate_on_submit():    
        file_uuid = str(uuid.uuid4())
        filename = secure_filename(f"{file_uuid}.mp4")
        new_video_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], current_user.id)
        create_file_directory(new_video_dir)
        video_path = os.path.join(new_video_dir, filename)
        form.filename.data.save(video_path)
        
        if is_video_openable(video_path):
            fps, frame_interval, duration = get_video_properties(video_path)
            
            processed_dir = os.path.join(current_app.config['FRAME_OUTPUT_FOLDER'], current_user.id, file_uuid)
            create_file_directory(processed_dir)
                        
            image_count = process_video_images(video_path, processed_dir, frame_interval, fps)
                    
            video_post = VideoPost(
                id=file_uuid,
                title=form.title.data,
                description=form.description.data,
                instruction=form.instruction.data,
                filename=video_path,
                fps=fps,
                duration=duration,
                author_id=current_user.id,
            )
            db.session.add(video_post)
            db.session.commit()
            flash(f"Processed {image_count} frames from the video.")
            
            landmarked_dir = os.path.join(current_app.config['FRAME_OUTPUT_FOLDER'], current_user.id, file_uuid)
            model_path = current_app.config['MODEL_PATH']
            is_annotated, total_errors = generate_pose_landmark_dictionary(landmarked_dir, model_path, is_video=True)
            
            if is_annotated:
                video_post.is_annotated = True
                video_post.frames_processed = image_count
                video_post.frames_error = total_errors
                db.session.add(video_post)
                db.session.commit()
            
            return redirect(url_for('diary.all_dance_entries'))
        else:
            flash(f"Something went wrong. :( Please try again. ")
            return redirect(url_for('accounts.profile'))
        
    return render_template("form.html", form=form, title="New Entry")

@bp.route("/<id>/update", methods=["GET", "POST"])
@login_required
def update_dance_entry(id):
    video_post = VideoPost.query.get_or_404(id)
    form = EditDancePost(obj=video_post)
    if form.validate_on_submit():
        if form.deleted.data:
            video_post.delete_post()
            flash('Video post marked as deleted and will be scheduled for deletion in 14 days.', 'success')
        else:
            video_post.title = form.title.data
            video_post.description = form.description.data
            video_post.last_updated_on = tz.localize(datetime.utcnow())
            db.session.commit()
            flash('Video post updated successfully!', 'success')
        return redirect(url_for('diary.all_dance_entries'))
    
    return render_template("form.html", form=form, title="Edit Entry")