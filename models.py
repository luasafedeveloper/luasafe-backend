from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class InviteCode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(100), unique=True, nullable=False)
    used = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Script(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    tier_required = db.Column(db.String(50), default="Standard")
    lua_code = db.Column(db.Text, nullable=False)
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Key(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    key = db.Column(db.String(100), unique=True, nullable=False)
    script_name = db.Column(db.String(100), nullable=True)
    tier = db.Column(db.String(50), default="Standard")
    status = db.Column(db.String(20), default="ACTIVE")
    hwid = db.Column(db.String(255), default="UNBOUND")
    exec_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=True)
    last_hwid_reset = db.Column(db.DateTime, nullable=True)

    def is_valid(self):
        if self.status != "ACTIVE":
            return False
        if self.expires_at and datetime.utcnow() > self.expires_at:
            return False
        return True

    def remaining_time(self):
        if not self.expires_at:
            return "Lifetime"
        now = datetime.utcnow()
        if now > self.expires_at:
            return "Expired"
        diff = self.expires_at - now
        days = diff.days
        hours = diff.seconds // 3600
        if days > 0:
            return f"{days} Days"
        return f"{hours} Hours"

class Setting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    key = db.Column(db.String(50), nullable=False)
    value = db.Column(db.Text, nullable=True)

class Blacklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hwid = db.Column(db.String(255), unique=True, nullable=False)
    reason = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
