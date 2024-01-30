from app import db
import uuid
from datetime import datetime, timedelta

class VideoReport(db.Model):
    __tablename__ = 'reports'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    author_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    video_id = db.Column(db.String(36), db.ForeignKey('videos.id'), nullable=False)
    spin_count = db.Column(db.String(100))
    inversion_count = db.Column(db.String(1000), nullable=True)
    detected_tricks = db.Column(db.String(1000), nullable=True)
    detected_grip = db.Column(db.String(1000), nullable=True)
    detected_legs = db.Column(db.String(1000), nullable=True)
    created_on = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    deleted = db.Column(db.Boolean, default=False)
    deleted_on = db.Column(db.DateTime, nullable=True)
    scheduled_for_deletion_on = db.Column(db.DateTime, nullable=True)
    video_post = db.relationship('VideoPost', foreign_keys=[video_id], backref='reports', lazy=True)

    def __repr__(self):
        return '<Report {}>'.format(self.id)
    