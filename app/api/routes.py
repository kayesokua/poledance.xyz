from flask import Blueprint, send_from_directory, current_app, send_file, send_from_directory
from flask_login import login_required, current_user
import os
import pytz

bp = Blueprint("api", __name__, url_prefix="/api/v1/")
tz = pytz.timezone('UTC')

@bp.route('/uploads/<author_id>/<id>')
@login_required
def serve_uploaded_video(author_id,id):
    filename = f'{id}.mp4'
    filepath = os.path.join(current_app.config['SERVE_UPLOAD_FOLDER'],author_id)
    return send_from_directory(filepath,filename)