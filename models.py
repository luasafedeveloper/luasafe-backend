from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Key(db.Model):
    __tablename__ = 'key'
    
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(64), unique=True, nullable=False, index=True)
    tier = db.Column(db.String(20), default="Standard")
    status = db.Column(db.String(20), default="ACTIVE")      # ACTIVE / BANNED / EXPIRED
    hwid = db.Column(db.String(64), default="UNBOUND")
    discord_id = db.Column(db.String(32), default="")
    exec_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=True)       # None = Lifetime (평생)
    note = db.Column(db.String(200), default="")
    script_name = db.Column(db.String(100), default="loader.lua") # 키별 전용 스크립트 지정
    last_hwid_reset = db.Column(db.DateTime, nullable=True)  # 3일 HWID 쿨타임 체크용

    def is_valid(self):
        if self.status != "ACTIVE":
            return False
        if self.expires_at and datetime.utcnow() > self.expires_at:
            return False
        return True

    def remaining_time(self):
        if self.expires_at is None:
            return "Lifetime"
        delta = self.expires_at - datetime.utcnow()
        if delta.total_seconds() <= 0:
            return "Expired"
        hours = int(delta.total_seconds() // 3600)
        if hours < 24:
            return f"{hours} Hours"
        days = hours // 24
        return f"{days} Days"


class Script(db.Model):
    __tablename__ = 'script'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=True)
    tier_required = db.Column(db.String(50), default="VIP")
    lua_code = db.Column(db.Text, nullable=False)  # 루아 코드가 저장될 컬럼
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Script {self.name}>"


class Blacklist(db.Model):
    __tablename__ = 'blacklist'

    id = db.Column(db.Integer, primary_key=True)
    hwid = db.Column(db.String(255), unique=True, nullable=False)
    reason = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Setting(db.Model):
    __tablename__ = 'setting'
    
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(50), unique=True, nullable=False)
    value = db.Column(db.String(200), default="")