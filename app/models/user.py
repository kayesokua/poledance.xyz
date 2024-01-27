from datetime import datetime
import uuid
from app import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    
    activated = db.Column(db.Boolean, default=True)
    activated_on = db.Column(db.DateTime(), default=datetime.utcnow)
    
    deactivated = db.Column(db.Boolean, default=False)
    deactivated_on = db.Column(db.Boolean, default=False)
    
    last_updated_on = db.Column(db.DateTime(), default=datetime.utcnow)

    def get_id(self):
        return str(self.id)