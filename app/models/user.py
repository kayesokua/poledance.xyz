from flask_login import UserMixin
from app import db
from datetime import datetime, timedelta
from .video import VideoPost
import uuid

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    activated = db.Column(db.Boolean, default=True)
    activated_on = db.Column(db.DateTime(), default=datetime.utcnow)
    last_login_on = db.Column(db.DateTime(), default=datetime.utcnow)
    deleted = db.Column(db.Boolean, default=False)
    deleted_on = db.Column(db.DateTime, nullable=True)
    scheduled_for_deletion_on = db.Column(db.DateTime, nullable=True)

    def get_id(self):
        return str(self.id)
    
    def delete_user(self):
        self.deleted = True
        self.deleted_on = datetime.utcnow()
        self.scheduled_for_deletion_on = datetime.utcnow() + timedelta(days=7)
        video_posts = VideoPost.query.filter_by(author_id=self.id).all()
        for video_post in video_posts:
            video_post.delete_post()
        db.session.add(self)
        db.session.commit() 