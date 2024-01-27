from flask import Blueprint, flash, redirect, render_template, current_app, request, url_for
from flask_login import LoginManager, login_required, logout_user, current_user, login_user

from app.extensions.db import db
from app.models.video import VideoPost
from app.utilities.video_utils import *
from app.utilities.file_system_utils import *
from .forms import NewDancePost, EditDancePost

import pytz
import uuid
from werkzeug.utils import secure_filename

bp = Blueprint("diary", __name__, url_prefix="/diary")
tz = pytz.timezone('UTC')

@bp.route("/", methods=["GET"])
@login_required
def all_dance_entries():
    video_posts = VideoPost.query.filter_by(author_id=current_user.id).order_by(VideoPost.created_on.desc()).all()
    return render_template("home.html", video_posts=video_posts, title="Diary Main")

@bp.route("/new", methods=["GET", "POST"])
@login_required
def new_dance_entry():
    form = NewDancePost()
    
    form.title.data = VideoPost.generate_default_title()
    print(form.title.data)
    
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
                filename=video_path,
                fps=fps,
                duration=duration,
                author_id=current_user.id,
            )
            db.session.add(video_post)
            db.session.commit()
            flash(f"Processed {image_count} frames from the video.")
            return redirect(url_for('diary.new_dance_entry'))
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
        video_post.title = form.title.data
        video_post.description = form.description.data
        video_post.deleted = form.deleted.data

        db.session.commit()
        flash('Video post updated successfully!', 'success')
        return redirect(url_for('accounts.profile'))

    return render_template("form.html", form=form, title="Edit Entry")