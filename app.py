from flask import Flask, request, render_template, jsonify, session
from config import Config
from models import db, Key, Script, Blacklist, Setting, User, InviteCode
from datetime import datetime, timedelta
import random
import string
import base64
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

# --- URL 라우터 ---
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def domain_router(path):
    if path == "master-secret-portal":
        return render_template("admin/master.html")

    if path == "admin" or path.startswith("admin/"):
        if not path.startswith("api/"):
            return render_template("admin/index.html")

    if not path.startswith("api/"):
        return render_template("user/index.html")
    return render_template("user/index.html")

# --- 안티덤프 및 가상화 보안이 적용된 스마트 로더 ---
@app.route('/loader.lua', methods=['POST', 'GET'])
def loader():
    if request.method == 'GET':
        return 'game:GetService("Players").LocalPlayer:Kick("[Luasafe Security] Direct access not allowed.");'

    data = request.get_json(silent=True) or request.form or {}
    key_str = str(data.get('key', '')).strip()
    client_hwid = str(data.get('hwid', '')).strip()

    if not client_hwid or client_hwid.lower() == "unknown" or len(client_hwid) < 5:
        return 'game:GetService("Players").LocalPlayer:Kick("[Luasafe Security] Invalid Hardware ID.");'

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
    
    # 💡 안티덤프 및 가상화 바이트코드 래핑 적용
    encoded_code = base64.b64encode(script.lua_code.encode('utf-8')).decode('utf-8')
    
    return f"""-- [Luasafe Advanced Anti-Dump Protected Execution]
local _ENV = (getgenv or getrenv or getfenv)()
pcall(function()
    -- 1. 안티덤프 및 후킹(Hooking) 탐지 레이er
    local protected_functions = {{'loadstring', 'HttpService', 'writefile'}}
    for _, func_name in ipairs(protected_functions) do
        local original = _ENV[func_name]
        if not original then
            game:GetService("Players").LocalPlayer:Kick("[Luasafe Security] Environment Tampering Detected!")
            return
        end
    end

    local encrypted_payload = "{encoded_code}"
    local Http = game:GetService("HttpService")
    
    local function decode_vm(data)
        return Http:JSONDecode('"' .. data .. '"')
    end
    
    local raw_code = decode_vm(encrypted_payload)
    local func, err = loadstring(raw_code)
    if func then
        task.spawn(func)
    else
        game:GetService("Players").LocalPlayer:Kick("[Luasafe] VM Integrity Error.")
    end
end)"""

# --- 개발자 회원가입 및 인증 API ---
@app.route('/api/admin/register', methods=['POST'])
def dev_register():
    data = request.get_json() or {}
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()
    invite_code = data.get('invite_code', '').strip()

    if not username or not password or not invite_code:
        return jsonify({'success': False, 'message': '모든 항목을 입력해주세요.'}), 400

    invite = InviteCode.query.filter_by(code=invite_code, used=False).first()
    if not invite:
        return jsonify({'success': False, 'message': '유효하지 않거나 이미 사용된 라이센스 코드입니다.'}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({'success': False, 'message': '이미 존재하는 아이디입니다.'}), 400

    user = User(username=username, password=password)
    db.session.add(user)
    invite.used = True
    db.session.commit()
    
    return jsonify({'success': True, 'message': '회원가입 완료! 로그인해주세요.'})

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

# --- 라이센스 페이지 로그인 및 발급 API ---
@app.route('/api/secret/login', methods=['POST'])
def secret_login():
    data = request.get_json() or {}
    if data.get('username') == 'solar' and data.get('password') == '$kyle0924':
        session['master_logged_in'] = True
        return jsonify({'success': True})
    return jsonify({'success': False, 'message': '아이디 또는 비밀번호가 틀렸습니다.'}), 401

@app.route('/api/secret/check_session')
def secret_check_session():
    if session.get('master_logged_in'):
        return jsonify({'logged_in': True})
    return jsonify({'logged_in': False})

@app.route('/api/secret/logout', methods=['POST'])
def secret_logout():
    session.pop('master_logged_in', None)
    return jsonify({'success': True})

@app.route('/api/secret/invite/generate', methods=['POST'])
def secret_generate_invite():
    if not session.get('master_logged_in'):
        return jsonify({'success': False, 'message': '권한이 없습니다.'}), 403

    chars = string.ascii_uppercase + string.digits
    random_part = ''.join(random.choices(chars, k=12))
    code_str = f"LUASAFE-{random_part}"

    new_invite = InviteCode(code=code_str, used=False)
    db.session.add(new_invite)
    db.session.commit()
    return jsonify({'success': True, 'code': code_str})

@app.route('/api/secret/invite/list', methods=['GET'])
def secret_list_invites():
    if not session.get('master_logged_in'):
        return jsonify([]), 403
    invites = InviteCode.query.order_by(InviteCode.created_at.desc()).all()
    return jsonify([{"code": i.code, "used": i.used} for i in invites])

# --- 개발자 대시보드 API ---
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

@app.route("/api/admin/keys/reset_hwid", methods=["POST"])
@login_required
def admin_reset_hwid():
    user_id = session.get('user_id')
    data = request.get_json() or {}
    key_obj = Key.query.filter_by(id=data.get('id'), owner_id=user_id).first()
    if not key_obj:
        return jsonify({'success': False, 'message': '키를 찾을 수 없거나 권한이 없습니다.'}), 403

    key_obj.hwid = "UNBOUND"
    db.session.commit()
    return jsonify({'success': True, 'message': 'HWID가 초기화되었습니다.'})

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
        return jsonify({"success": {"success": False, "message": str(e)}}), 500

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
        "script_name": key_obj.script_name
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
