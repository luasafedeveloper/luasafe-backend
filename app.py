from flask import Flask, request, render_template, jsonify, session
from config import Config
from models import db, Key, Script, Blacklist, Setting
from utils.detector import is_browser
from datetime import datetime, timedelta
import random
import string
import requests
import functools

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all()
    defaults = {
        "kill_switch": "false",
        "ad_gate": "true",
        "log_stream": "true",
        "discord_webhook_url": "",
        "featured_script": "loader.lua"
    }
    for k, v in defaults.items():
        if not Setting.query.filter_by(key=k).first():
            db.session.add(Setting(key=k, value=v))
    db.session.commit()

def get_setting(key, default=""):
    s = Setting.query.filter_by(key=key).first()
    return s.value if s else default

def set_setting(key, value):
    s = Setting.query.filter_by(key=key).first()
    if s:
        s.value = value
    else:
        db.session.add(Setting(key=key, value=value))
    db.session.commit()

def send_discord_webhook(title, description, color=0xffffff):
    webhook_url = get_setting("discord_webhook_url", "")
    if not webhook_url:
        return
    data = {
        "embeds": [{
            "title": title,
            "description": description,
            "color": color,
            "timestamp": datetime.utcnow().isoformat()
        }]
    }
    try:
        requests.post(webhook_url, json=data, timeout=5)
    except:
        pass

def get_host():
    host = request.host.lower().split(":")[0]
    return host

# --- 관리자 인증 가드 데코레이터 ---
def admin_required(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('is_admin'):
            return jsonify({'success': False, 'message': 'Unauthorized Access'}), 401
        return f(*args, **kwargs)
    return decorated_function

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def domain_router(path):
    host = get_host()
    if "mineminyeehack" in host:
        return "<h1>비정상적인 접근입니다.</h1>", 403

    # /admin 경로 또는 관리자 도메인 접속 시 관리자 페이지 반환
    if path == "admin" or path.startswith("admin/") or "lua-scriptluarmor" in host:
        if path.startswith("api/"):
            pass
        else:
            return render_template("admin/index.html")

    if path.startswith("api/"):
        pass
    else:
        return render_template("user/index.html")

    return render_template("user/index.html")

# --- 보안 스크립트 로더 (POST 방식 수신 및 엄격한 HWID 검증) ---
@app.route('/loader.lua', methods=['POST', 'GET'])
def loader():
    if is_browser(request):
        return 'game:GetService("Players").LocalPlayer:Kick("[Mineminyee] Browser access denied.");'

    data = request.get_json(silent=True)
    if not data:
        data = request.form 
    
    if not data and request.args:
        data = request.args

    key_str = str(data.get('key', '')).strip()
    client_hwid = str(data.get('hwid', '')).strip()

    print(f"[DEBUG] Received Key: '{key_str}', HWID: '{client_hwid}'")

    if get_setting("kill_switch") == "true":
        return 'game:GetService("Players").LocalPlayer:Kick("[Mineminyee] Kill switch is currently enabled.");'
    
    if not client_hwid or client_hwid.lower() == "unknown":
        return 'game:GetService("Players").LocalPlayer:Kick("[Mineminyee] Security Error: Invalid HWID detected.");'

    if not key_str:
        return 'game:GetService("Players").LocalPlayer:Kick("[Mineminyee] Error: Key parameter is missing.");'

    key_obj = Key.query.filter_by(key=key_str).first()
    if not key_obj or not key_obj.is_valid():
        return 'game:GetService("Players").LocalPlayer:Kick("[Mineminyee] Invalid or expired key!");'
    
    if key_obj.hwid == "UNBOUND" or not key_obj.hwid:
        key_obj.hwid = client_hwid
    elif key_obj.hwid != client_hwid:
        return 'game:GetService("Players").LocalPlayer:Kick("[Mineminyee] Key is bound to another device!");'
    
    key_obj.exec_count += 1
    db.session.commit()
    
    target_script_name = getattr(key_obj, 'script_name', None) or get_setting("featured_script", "loader.lua")
    script = Script.query.filter_by(name=target_script_name, active=True).first()
    if not script:
        script = Script.query.filter_by(active=True).first()
        
    if not script:
        return 'game:GetService("Players").LocalPlayer:Kick("[Mineminyee] No active script available!");'
    
    protected_wrapper = f"""
-- [Mineminyee Secure Execution Protected]
-- Target: {script.name}
pcall(function()
    {script.lua_code}
end)
"""
    return protected_wrapper

# --- 관리자 API (세션 가드 적용) ---
@app.route('/api/admin/login', methods=['POST'])
def admin_login():
    data = request.get_json() or {}
    if data.get('username') == 'mineminyee' and data.get('password') == 'sk521400^^':
        session['is_admin'] = True
        return jsonify({'success': True})
    return jsonify({'success': False, 'message': '아이디 또는 비밀번호 틀림'}), 401

@app.route('/api/admin/logout', methods=['POST'])
def admin_logout():
    session.pop('is_admin', None)
    return jsonify({'success': True})

@app.route('/api/admin/scripts/add', methods=['POST'])
@admin_required
def add_script_api():
    data = request.get_json() or {}
    name = data.get('name', '').strip()
    description = data.get('description', '').strip()
    lua_code = data.get('lua_code', '')
    
    if not name:
        return jsonify({'success': False, 'message': '스크립트 이름을 입력하세요.'}), 400
        
    script = Script.query.filter_by(name=name).first()
    if script:
        script.description = description
        script.lua_code = lua_code
    else:
        script = Script(name=name, description=description, tier_required="VIP", lua_code=lua_code, active=True)
        db.session.add(script)
        
    db.session.commit()
    return jsonify({'success': True})

@app.route('/api/admin/scripts/delete', methods=['POST'])
@admin_required
def delete_script_api():
    data = request.get_json() or {}
    script = Script.query.get(data.get('id'))
    if script:
        db.session.delete(script)
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'success': False, 'message': '스크립트를 찾을 수 없습니다.'}), 404

@app.route('/api/admin/scripts/toggle', methods=['POST'])
@admin_required
def toggle_script_api():
    data = request.get_json() or {}
    script = Script.query.get(data.get('id'))
    if script:
        script.active = not script.active
        db.session.commit()
        return jsonify({'success': True, 'active': script.active})
    return jsonify({'success': False}), 404

@app.route("/api/admin/scripts")
@admin_required
def admin_scripts():
    scripts = Script.query.all()
    return jsonify([{
        "id": s.id, "name": s.name, "description": s.description, "lua_code": s.lua_code, "active": s.active
    } for s in scripts])

@app.route("/api/admin/keys")
@admin_required
def admin_keys():
    keys = Key.query.order_by(Key.created_at.desc()).all()
    return jsonify([{
        "id": k.id, "key": k.key, "tier": k.tier, "status": k.status, "hwid": k.hwid, "expiry": k.remaining_time(), "execs": k.exec_count
    } for k in keys])

@app.route('/api/admin/keys/delete', methods=['POST'])
@admin_required
def admin_delete_key():
    data = request.get_json() or {}
    key_obj = Key.query.get(data.get('id'))
    if key_obj:
        db.session.delete(key_obj)
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'success': False, 'message': '키를 찾을 수 없습니다.'}), 404

@app.route("/api/admin/generate", methods=["POST"])
@admin_required
def admin_generate():
    try:
        data = request.get_json() or {}
        script_name = data.get("script_name", "loader.lua")
        duration_type = data.get("duration_type", "Hours")
        
        chars = string.ascii_uppercase + string.digits
        random_part = ''.join(random.choices(chars, k=16))
        key_str = f"mineminyee-{random_part[:4]}-{random_part[4:8]}-{random_part[8:12]}"

        if duration_type == "Lifetime":
            expires = None
        else:
            amount = int(data.get("amount", 24))
            if duration_type == "Days":
                expires = datetime.utcnow() + timedelta(days=amount)
            else:
                expires = datetime.utcnow() + timedelta(hours=amount)

        new_key = Key(
            key=key_str,
            tier="Standard",
            status="ACTIVE",
            expires_at=expires,
            discord_id="Admin-Manual"
        )
        
        if hasattr(new_key, 'script_name'):
            new_key.script_name = script_name

        db.session.add(new_key)
        db.session.commit()

        send_discord_webhook("🔑 Key Generated", f"**Key:** `{key_str}`\n**Script:** `{script_name}`\n**Duration:** `{duration_type}`")
        return jsonify({"success": True, "key": key_str})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route("/api/admin/toggle_kill", methods=["POST"])
@admin_required
def toggle_kill():
    current = get_setting("kill_switch", "false")
    new_val = "false" if current == "true" else "true"
    set_setting("kill_switch", new_val)
    send_discord_webhook("⚠️ Kill Switch Toggled", f"Kill Switch: **{new_val.upper()}**", 0xff0000)
    return jsonify({"kill_switch": new_val})

@app.route("/api/admin/settings", methods=["POST"])
@admin_required
def admin_save_settings():
    data = request.json or {}
    if "webhook_url" in data:
        set_setting("discord_webhook_url", data["webhook_url"].strip())
    return jsonify({"success": True})

@app.route("/api/admin/settings/get")
@admin_required
def admin_get_settings():
    return jsonify({
        "webhook_url": get_setting("discord_webhook_url"),
        "kill_switch": get_setting("kill_switch")
    })

# --- 유저 사이트 API ---
@app.route("/api/user/scripts")
def user_scripts():
    scripts = Script.query.filter_by(active=True).all()
    return jsonify([{
        "name": s.name,
        "description": s.description
    } for s in scripts])

@app.route("/api/user/lookup", methods=["POST"])
def user_lookup_key():
    data = request.json or {}
    key_str = data.get("key", "").strip()
    key_obj = Key.query.filter_by(key=key_str).first()
    if not key_obj:
        return jsonify({"success": False, "message": "존재하지 않는 키입니다."}), 404
        
    return jsonify({
        "success": True,
        "key": key_obj.key,
        "tier": key_obj.tier,
        "status": key_obj.status,
        "hwid": key_obj.hwid if key_obj.hwid else "UNBOUND",
        "expiry": key_obj.remaining_time(),
        "execs": key_obj.exec_count,
        "script_name": getattr(key_obj, 'script_name', 'loader.lua')
    })

@app.route("/api/user/reset_hwid", methods=["POST"])
def user_reset_hwid():
    data = request.json or {}
    key_str = data.get("key", "").strip()
    new_script = data.get("script_name", "").strip()
    
    key_obj = Key.query.filter_by(key=key_str).first()
    if not key_obj:
        return jsonify({"success": False, "message": "키를 찾을 수 없습니다."}), 404
        
    if key_obj.last_hwid_reset:
        cooldown_end = key_obj.last_hwid_reset + timedelta(days=3)
        if datetime.utcnow() < cooldown_end:
            remaining_hours = int((cooldown_end - datetime.utcnow()).total_seconds() / 3600)
            return jsonify({
                "success": False, 
                "message": f"HWID 초기화 쿨타임 중입니다. (남은 시간: 약 {remaining_hours}시간)"
            }), 400

    old_hwid = key_obj.hwid
    key_obj.hwid = "UNBOUND"
    key_obj.last_hwid_reset = datetime.utcnow()
    
    if new_script and hasattr(key_obj, 'script_name'):
        key_obj.script_name = new_script

    db.session.commit()
    
    send_discord_webhook(
        "🔄 HWID Reset & Script Update",
        f"**Key:** `{key_obj.key}`\n**New Script:** `{new_script}`\n**Previous HWID:** `{old_hwid}`",
        0xffaa00
    )
    
    return jsonify({"success": True, "message": "HWID 초기화 및 스크립트 변경 완료! (다음 초기화까지 3일 소요)"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
