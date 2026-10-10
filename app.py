from flask import Flask, request, render_template, jsonify, session
from config import Config
from models import db, Key, Script, Blacklist, Setting, User
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

def get_host():
    host = request.host.lower().split(":")[0]
    return host

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

    if path == "admin" or path.startswith("admin/") or "lua-scriptluarmor" in host:
        if not path.startswith("api/"):
            return render_template("admin/index.html")

    if not path.startswith("api/"):
        return render_template("user/index.html")
    return render_template("user/index.html")

# --- 파라미터 없는 스마트 로더 처리 ---
@app.route('/loader.lua', methods=['POST', 'GET'])
def loader():
    if is_browser(request):
        return 'game:GetService("Players").LocalPlayer:Kick("[Luasafe] Browser access denied.");'

    if request.method == 'GET':
        lua_payload = '''local s, r = pcall(function()
    return request({
        Url = "https://luasafe-backend.onrender.com/loader.lua",
        Method = "POST",
        Headers = { ["Content-Type"] = "application/json" },
        Body = game:GetService("HttpService"):JSONEncode({
            key = scriptkey,
            hwid = tostring(game:GetService("RbxAnalyticsService"):GetClientId())
        })
    })
end);

if s and r and r.StatusCode == 200 then
    local f, err = loadstring(r.Body);
    if f then f(); else warn("[Luasafe Error] " .. tostring(err)); end
else
    game:GetService("Players").LocalPlayer:Kick("[Luasafe] Auth Failed or Connection Error.");
end;'''
        return lua_payload

    data = request.get_json(silent=True) or request.form or {}
    key_str = str(data.get('key', '')).strip()
    client_hwid = str(data.get('hwid', '')).strip()

    if get_setting("kill_switch") == "true":
        return 'game:GetService("Players").LocalPlayer:Kick("[Luasafe] Kill switch is enabled.");'
    
    if not client_hwid or client_hwid.lower() == "unknown":
        return 'game:GetService("Players").LocalPlayer:Kick("[Luasafe] Security Error: Invalid HWID detected.");'

    if not key_str:
        return 'game:GetService("Players").LocalPlayer:Kick("[Luasafe] Error: Key parameter is missing.");'

    key_obj = Key.query.filter_by(key=key_str).first()
    if not key_obj or not key_obj.is_valid():
        return 'game:GetService("Players").LocalPlayer:Kick("[Luasafe] Invalid or expired key!");'
    
    if key_obj.hwid == "UNBOUND" or not key_obj.hwid:
        key_obj.hwid = client_hwid
    elif key_obj.hwid != client_hwid:
        return 'game:GetService("Players").LocalPlayer:Kick("[Luasafe] Key is bound to another device!");'
    
    key_obj.exec_count += 1
    db.session.commit()
    
    target_script_name = getattr(key_obj, 'script_name', None) or get_setting("featured_script", "loader.lua")
    script = Script.query.filter_by(name=target_script_name, active=True).first()
    if not script:
        script = Script.query.filter_by(active=True).first()
        
    if not script:
        return 'game:GetService("Players").LocalPlayer:Kick("[Luasafe] No active script available!");'
    
    return f"""-- [Luasafe Secure Execution]
pcall(function()
    {script.lua_code}
end)"""

# --- 관리자 로그인 API ---
@app.route('/api/admin/login', methods=['POST'])
def admin_login():
    data = request.get_json() or {}
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()

    if username == 'mineminyee' and password == 'sk521400^^':
        session['is_admin'] = True
        return jsonify({'success': True})

    return jsonify({'success': False, 'message': '관리자 아이디 또는 비밀번호가 틀렸습니다.'}), 401

@app.route('/api/admin/logout', methods=['POST'])
def admin_logout():
    session.pop('is_admin', None)
    return jsonify({'success': True})

# --- 관리자 대시보드 API들 ---
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
    return jsonify({'success': False}), 404

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
    return jsonify([{"id": s.id, "name": s.name, "description": s.description, "lua_code": s.lua_code, "active": s.active} for s in Script.query.all()])

@app.route("/api/admin/keys")
@admin_required
def admin_keys():
    return jsonify([{"id": k.id, "key": k.key, "tier": k.tier, "status": k.status, "hwid": k.hwid, "expiry": k.remaining_time(), "execs": k.exec_count} for k in Key.query.order_by(Key.created_at.desc()).all()])

@app.route('/api/admin/keys/delete', methods=['POST'])
@admin_required
def admin_delete_key():
    data = request.get_json() or {}
    key_obj = Key.query.get(data.get('id'))
    if key_obj:
        db.session.delete(key_obj)
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'success': False}), 404

@app.route("/api/admin/generate", methods=["POST"])
@admin_required
def admin_generate():
    try:
        data = request.get_json() or {}
        script_name = data.get("script_name", "loader.lua")
        duration_type = data.get("duration_type", "Hours")
        chars = string.ascii_uppercase + string.digits
        random_part = ''.join(random.choices(chars, k=16))
        key_str = f"luasafe-{random_part[:4]}-{random_part[4:8]}-{random_part[8:12]}"

        expires = None if duration_type == "Lifetime" else datetime.utcnow() + timedelta(days=int(data.get("amount", 24)) if duration_type == "Days" else 0, hours=int(data.get("amount", 24)) if duration_type == "Hours" else 0)

        new_key = Key(key=key_str, tier="Standard", status="ACTIVE", expires_at=expires, discord_id="Admin-Manual")
        if hasattr(new_key, 'script_name'):
            new_key.script_name = script_name

        db.session.add(new_key)
        db.session.commit()
        return jsonify({"success": True, "key": key_str})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route("/api/admin/toggle_kill", methods=["POST"])
@admin_required
def toggle_kill():
    current = get_setting("kill_switch", "false")
    new_val = "false" if current == "true" else "true"
    set_setting("kill_switch", new_val)
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
    return jsonify({"webhook_url": get_setting("discord_webhook_url"), "kill_switch": get_setting("kill_switch")})

# --- 일반 유저 회원가입 / 로그인 / 세션 관리 API ---
@app.route("/api/user/signup", methods=["POST"])
def user_signup():
    data = request.get_json() or {}
    username = data.get("username", "").strip()
    password = data.get("password", "").strip()

    if not username or not password:
        return jsonify({"success": False, "message": "아이디와 비밀번호를 모두 입력해주세요."}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"success": False, "message": "이미 존재하는 아이디입니다."}), 400

    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"success": True, "message": "회원가입 완료! 로그인해주세요."})

@app.route("/api/user/login", methods=["POST"])
def user_login():
    data = request.get_json() or {}
    username = data.get("username", "").strip()
    password = data.get("password", "").strip()

    user = User.query.filter_by(username=username, password=password).first()
    if not user:
        return jsonify({"success": False, "message": "아이디 또는 비밀번호가 일치하지 않습니다."}), 401

    session['username'] = username

    # 유저 로그인 시 전용 키가 없으면 자동 생성 및 매칭
    existing_key = Key.query.filter_by(discord_id=f"User_{username}").first()
    if not existing_key:
        chars = string.ascii_uppercase + string.digits
        random_part = ''.join(random.choices(chars, k=16))
        key_str = f"luasafe-{random_part[:4]}-{random_part[4:8]}-{random_part[8:12]}"
        expires = datetime.utcnow() + timedelta(days=30)
        existing_key = Key(key=key_str, tier="Standard", status="ACTIVE", expires_at=expires, discord_id=f"User_{username}")
        db.session.add(existing_key)
        db.session.commit()

    return jsonify({"success": True, "key": existing_key.key})

@app.route("/api/user/check_session")
def user_check_session():
    username = session.get('username')
    if not username:
        return jsonify({"logged_in": False})
    
    # 세션에 저장된 유저의 전용 키 찾아 반환
    key_obj = Key.query.filter_by(discord_id=f"User_{username}").first()
    key_str = key_obj.key if key_obj else ""
    return jsonify({"logged_in": True, "username": username, "key": key_str})

@app.route("/api/user/logout", methods=["POST"])
def user_logout():
    session.pop('username', None)
    return jsonify({"success": True})

@app.route("/api/user/scripts")
def user_scripts():
    return jsonify([{"name": s.name, "description": s.description} for s in Script.query.filter_by(active=True).all()])

@app.route("/api/user/lookup", methods=["POST"])
def user_lookup_key():
    data = request.json or {}
    key_str = data.get("key", "").strip()

    if not key_str:
        return jsonify({"success": False, "message": "키를 입력해주세요."}), 400

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
        
    if key_obj.last_hwid_reset and datetime.utcnow() < key_obj.last_hwid_reset + timedelta(days=3):
        return jsonify({"success": False, "message": "HWID 초기화 쿨타임 중입니다. (3일)"}), 400

    key_obj.hwid = "UNBOUND"
    key_obj.last_hwid_reset = datetime.utcnow()
    if new_script and hasattr(key_obj, 'script_name'):
        key_obj.script_name = new_script
    db.session.commit()
    return jsonify({"success": True, "message": "초기화 완료!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
