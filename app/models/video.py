from app import db
import uuid
from datetime import datetime

class VideoPost(db.Model):
    __tablename__ = 'videos'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    title = db.Column(db.String(128), nullable=False, default=lambda: VideoPost.generate_default_title())
    description = db.Column(db.String(5000), nullable=False)
    
    fps = db.Column(db.Integer, default=0)
    duration = db.Column(db.Float, default=0.0)
    filename = db.Column(db.String(256), nullable=False)
    
    deleted = db.Column(db.Boolean, default=False)

    created_on = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    last_updated_on = db.Column(db.DateTime, nullable=True) 
    
    author_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    
    @staticmethod
    def generate_default_title():
        return datetime.utcnow().strftime('%Y.%m.%d') + " choreography"
    
    