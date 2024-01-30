from app import db
import uuid
from datetime import datetime, timedelta

class VideoReport(db.Model):
    __tablename__ = 'reports'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    author_id = db.Column(db.String(36), db.ForeignKey('users.id'))
    video_id = db.Column(db.String(36), db.ForeignKey('videos.id'))
    spin_count = db.Column(db.String(100))
    inversion_count = db.Column(db.String(1000), nullable=True)
    detected_tricks = db.Column(db.String(1000), nullable=True)
    detected_grip = db.Column(db.String(1000), nullable=True)
    detected_legs = db.Column(db.String(1000), nullable=True)
    
    created_on = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    
    deleted = db.Column(db.Boolean, default=False)
    deleted_on = db.Column(db.DateTime, nullable=True)
    scheduled_for_deletion_on = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return '<Report {}>'.format(self.id)
    
    def delete_report(self):
        self.deleted = True
        self.deleted_on = datetime.utcnow()
        self.scheduled_for_deletion_on = datetime.utcnow() + timedelta(days=14)
        db.session.add(self)
        db.session.commit()