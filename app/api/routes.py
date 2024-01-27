from flask import Blueprint, send_from_directory, current_app, render_template, send_from_directory, redirect, url_for
from flask_login import login_required, current_user

import os
import pandas as pd
import pytz


bp = Blueprint("api", __name__, url_prefix="/api/v1/")
tz = pytz.timezone('UTC')

@bp.route('/uploads/<author_id>/<id>')
@login_required
def serve_uploaded_video(author_id,id):
    filename = f'{id}.mp4'
    filepath = os.path.join(current_app.config['SERVE_UPLOAD_FOLDER'],author_id)
    return send_from_directory(filepath,filename)

@bp.route('/dictionary/<category>')
@login_required
def serve_static_dictionary_tricks(category):
    if category == 'tricks':
        title = "Pole Tricks"
        dict_read = pd.read_csv(os.path.join('app','static', 'dictionary', 'tricks', 'pose_data.csv'))
        dict_data = dict_read.to_dict(orient='records')
        
    elif category == 'legs':
        title = "Leg Positions"
        dict_read = pd.read_csv(os.path.join('app','static', 'dictionary', 'positions','legs', 'pose_data.csv'))
        dict_data = dict_read.to_dict(orient='records')
        
    elif category == 'body':
        title = "Body Positions"
        dict_read = pd.read_csv(os.path.join('app','static', 'dictionary', 'positions','body', 'pose_data.csv'))
        dict_data = dict_read.to_dict(orient='records')
        
    elif category == 'grip':
        title = "Grip Positions"
        dict_read = pd.read_csv(os.path.join('app','static', 'dictionary', 'positions','grip', 'pose_data.csv'))
        dict_data = dict_read.to_dict(orient='records')
    else:
        return redirect(url_for('diary.all_dance_entries'))
        
    return render_template("dictionary.html", dict_data=dict_data, title=title)