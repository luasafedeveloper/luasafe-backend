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

def login_required(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user_id'):
            return jsonify({'success': False, 'message': '로그인이 필요합니다.'}), 401
        return f(*args, **kwargs)
    return decorated_function

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def domain_router(path):
    if not path.startswith("api/"):
        return render_template("admin/index.html")
    return render_template("admin/index.html")

# --- 멀티 개발자 지원 스마트 로더 ---
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

    if not client_hwid or client_hwid.lower() == "unknown":
        return 'game:GetService("Players").LocalPlayer:Kick("[Luasafe] Security Error: Invalid HWID.");'

    if not key_str:
        return 'game:GetService("Players").LocalPlayer:Kick("[Luasafe] Error: Key is missing.");'

    key_obj = Key.query.filter_by(key=key_str).first()
    if not key_obj or not key_obj.is_valid():
        return 'game:GetService("Players").LocalPlayer:Kick("[Luasafe] Invalid or expired key!");'
    
    if key_obj.hwid == "UNBOUND" or not key_obj.hwid:
        key_obj.hwid = client_hwid
    elif key_obj.hwid != client_hwid:
        return 'game:GetService("Players").LocalPlayer:Kick("[Luasafe] Key bound to another device!");'
    
    key_obj.exec_count += 1
    db.session.commit()
    
    target_script_name = key_obj.script_name
    script = Script.query.filter_by(owner_id=key_obj.owner_id, name=target_script_name, active=True).first()
    if not script:
        script = Script.query.filter_by(owner_id=key_obj.owner_id, active=True).first()
        
    if not script:
        return 'game:GetService("Players").LocalPlayer:Kick("[Luasafe] No active script available!");'
    
    return f"""-- [Luasafe Secure Execution]
pcall(function()
    {script.lua_code}
end)"""

# --- 개발자 계정 회원가입 / 로그인 / 세션 API ---
@app.route('/api/admin/register', methods=['POST'])
def dev_register():
    data = request.get_json() or {}
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()

    if not username or not password:
        return jsonify({'success': False, 'message': '아이디와 비밀번호를 모두 입력해주세요.'}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({'success': False, 'message': '이미 존재하는 개발자 아이디입니다.'}), 400

    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'success': True, 'message': '개발자 회원가입 완료! 로그인해주세요.'})

@app.route('/api/admin/login', methods=['POST'])
def dev_login():
    data = request.get_json() or {}
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()

    user = User.query.filter_by(username=username, password=password).first()
    if user:
        session['user_id'] = user.id
        session['username'] = user.username
        return jsonify({'success': True, 'username': user.username})

    return jsonify({'success': False, 'message': '아이디 또는 비밀번호가 틀렸습니다.'}), 401

@app.route('/api/admin/check_session')
def dev_check_session():
    if session.get('user_id'):
        return jsonify({'logged_in': True, 'username': session.get('username')})
    return jsonify({'logged_in': False})

@app.route('/api/admin/logout', methods=['POST'])
def dev_logout():
    session.clear()
    return jsonify({'success': True})

# --- 개발자 전용 대시보드 API (본인 데이터만 조회/수정) ---
@app.route('/api/admin/scripts/add', methods=['POST'])
@login_required
def add_script_api():
    user_id = session.get('user_id')
    data = request.get_json() or {}
    name = data.get('name', '').strip()
    description = data.get('description', '').strip()
    lua_code = data.get('lua_code', '')
    
    if not name:
        return jsonify({'success': False, 'message': '스크립트 이름을 입력하세요.'}), 400
        
    script = Script.query.filter_by(owner_id=user_id, name=name).first()
    if script:
        script.description = description
        script.lua_code = lua_code
    else:
        script = Script(owner_id=user_id, name=name, description=description, lua_code=lua_code, active=True)
        db.session.add(script)
    db.session.commit()
    return jsonify({'success': True})

@app.route('/api/admin/scripts/delete', methods=['POST'])
@login_required
def delete_script_api():
    user_id = session.get('user_id')
    data = request.get_json() or {}
    script = Script.query.filter_by(id=data.get('id'), owner_id=user_id).first()
    if script:
        db.session.delete(script)
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'success': False, 'message': '권한이 없습니다.'}), 403

@app.route('/api/admin/scripts/toggle', methods=['POST'])
@login_required
def toggle_script_api():
    user_id = session.get('user_id')
    data = request.get_json() or {}
    script = Script.query.filter_by(id=data.get('id'), owner_id=user_id).first()
    if script:
        script.active = not script.active
        db.session.commit()
        return jsonify({'success': True, 'active': script.active})
    return jsonify({'success': False}), 403

@app.route("/api/admin/scripts")
@login_required
def admin_scripts():
    user_id = session.get('user_id')
    scripts = Script.query.filter_by(owner_id=user_id).all()
    return jsonify([{"id": s.id, "name": s.name, "description": s.description, "lua_code": s.lua_code, "active": s.active} for s in scripts])

@app.route("/api/admin/keys")
@login_required
def admin_keys():
    user_id = session.get('user_id')
    keys = Key.query.filter_by(owner_id=user_id).order_by(Key.created_at.desc()).all()
    return jsonify([{"id": k.id, "key": k.key, "tier": k.tier, "status": k.status, "hwid": k.hwid, "expiry": k.remaining_time(), "execs": k.exec_count, "script_name": k.script_name} for k in keys])

@app.route('/api/admin/keys/delete', methods=['POST'])
@login_required
def admin_delete_key():
    user_id = session.get('user_id')
    data = request.get_json() or {}
    key_obj = Key.query.filter_by(id=data.get('id'), owner_id=user_id).first()
    if key_obj:
        db.session.delete(key_obj)
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'success': False}), 403

@app.route("/api/admin/generate", methods=["POST"])
@login_required
def admin_generate():
    try:
        user_id = session.get('user_id')
        data = request.get_json() or {}
        script_name = data.get("script_name", "")
        duration_type = data.get("duration_type", "Hours")
        amount = int(data.get("amount", 24))
        
        chars = string.ascii_uppercase + string.digits
        random_part = ''.join(random.choices(chars, k=16))
        key_str = f"luasafe-{random_part[:4]}-{random_part[4:8]}-{random_part[8:12]}"

        expires = None if duration_type == "Lifetime" else datetime.utcnow() + timedelta(days=amount if duration_type == "Days" else 0, hours=amount if duration_type == "Hours" else 0)

        new_key = Key(owner_id=user_id, key=key_str, script_name=script_name, tier="Standard", status="ACTIVE", expires_at=expires)
        db.session.add(new_key)
        db.session.commit()
        return jsonify({"success": True, "key": key_str})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
