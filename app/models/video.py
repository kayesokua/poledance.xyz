from app import db
import uuid
from datetime import datetime, timedelta
from .report import VideoReport

class VideoPost(db.Model):
    __tablename__ = 'videos'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(128), nullable=False, default=lambda: VideoPost.generate_default_title())
    description = db.Column(db.String(500), nullable=True)
    instruction = db.Column(db.String(500), nullable=True)
    fps = db.Column(db.Integer, default=0)
    duration = db.Column(db.Float, default=0.0)
    frames_processed = db.Column(db.Integer, default=0)
    frames_error = db.Column(db.Integer, default=0)
    filename = db.Column(db.String(256), nullable=False)
    is_annotated = db.Column(db.Boolean, default=False)
    is_calculated = db.Column(db.Boolean, default=False)
    created_on = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    last_updated_on = db.Column(db.DateTime, default=datetime.utcnow) 
    author_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    deleted = db.Column(db.Boolean, default=False)
    deleted_on = db.Column(db.DateTime, nullable=True)
    scheduled_for_deletion_on = db.Column(db.DateTime, nullable=True)
    report_id = db.Column(db.String(36), db.ForeignKey('reports.id'), nullable=True)
    
    @staticmethod
    def generate_default_title():
        return datetime.utcnow().strftime('%Y.%m.%d') + " choreo"
    
    def delete_post(self):
        self.deleted = True
        self.deleted_on = datetime.utcnow()
        self.scheduled_for_deletion_on = datetime.utcnow() + timedelta(days=14)
        
        report = VideoReport.query.get(self.report_id)
        if report:
            report.deleted = True
            report.deleted_on = datetime.utcnow()
            self.scheduled_for_deletion_on = datetime.utcnow() + timedelta(days=14)
        
            db.session.add(self)
            db.session.commit()
        
    
    