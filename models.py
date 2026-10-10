from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Key(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False)
    tier = db.Column(db.String(50), default="Standard")
    status = db.Column(db.String(20), default="ACTIVE")
    hwid = db.Column(db.String(200), default="UNBOUND")
    expires_at = db.Column(db.DateTime, nullable=True)
    exec_count = db.Column(db.Integer, default=0)
    discord_id = db.Column(db.String(100), nullable=True)
    last_hwid_reset = db.Column(db.DateTime, nullable=True)
    script_name = db.Column(db.String(100), default="loader.lua")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def is_valid(self):
        if self.status != "ACTIVE":
            return False
        if self.expires_at and datetime.utcnow() > self.expires_at:
            return False
        return True

    def remaining_time(self):
        if not self.expires_at:
            return "Lifetime"
        diff = self.expires_at - datetime.utcnow()
        if diff.total_seconds() <= 0:
            return "Expired"
        hours = int(diff.total_seconds() / 3600)
        if hours > 24:
            return f"{int(hours / 24)} Days"
        return f"{hours} Hours"

class Script(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(200), nullable=True)
    tier_required = db.Column(db.String(50), default="Standard")
    lua_code = db.Column(db.Text, nullable=False)
    active = db.Column(db.Boolean, default=True)

class Blacklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hwid = db.Column(db.String(200), unique=True, nullable=False)
    reason = db.Column(db.String(200), nullable=True)

class Setting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(50), unique=True, nullable=False)
    value = db.Column(db.Text, nullable=True)
