from datetime import datetime, timedelta
import base64
import functools
import os
import random
import subprocess
import string
import tempfile
from config import Config
from flask import Flask, jsonify, render_template, request, session
from models import Blacklist, InviteCode, Key, Script, Setting, User, db
import requests

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# 서버 메모리 기반 IP 저장소
KEY_IPS = {}

with app.app_context():
    db.create_all()


def login_required(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user_id'):
            return (
                jsonify({'success': False, 'message': '로그인이 필요합니다.'}),
                401,
            )
        return f(*args, **kwargs)
    return decorated_function


# --- URL 라우터 ---
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def domain_router(path):
    if path == 'master-secret-portal':
        return render_template('admin/master.html')

    if path == 'admin' or path.startswith('admin/'):
        if not path.startswith('api/'):
            return render_template('admin/index.html')

    if not path.startswith('api/'):
        return render_template('user/index.html')
    return render_template('user/index.html')


# --- 🔥 [Prometheus VM 연동형 서버사이드 난독화 엔진] ---
def compile_to_heavy_vm(lua_code):
    """
    서버에 설치된 Prometheus Luau Obfuscator CLI를 subprocess로 호출하여
    실제 VM 바이트코드 및 제어 흐름 평탄화가 적용된 난독화 코드를 생성합니다.
    """
    # 1. 원본 Lua 코드를 임시 입력 파일로 저장
    with tempfile.NamedTemporaryFile(mode='w', suffix='.lua', delete=False, encoding='utf-8') as f:
        f.write(lua_code)
        input_path = f.name

    output_path = input_path + ".obfuscated.lua"

    try:
        # 2. Prometheus CLI 실행 (Strong 프리셋 적용)
        # 주의: Render 서버 환경(또는 Dockerfile)에 lua 및 Prometheus 폴더가 세팅되어 있어야 합니다.
        cmd = ["lua", "Prometheus/cli.lua", "--preset", "Strong", "--nocolors", input_path, "-o", output_path]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0 and os.path.exists(output_path):
            with open(output_path, 'r', encoding='utf-8') as f:
                obfuscated_code = f.read()
            
            # 클라이언트(로블록스 익스플로잇)에서 바로 pcall로 감싸서 실행 가능하도록 반환
            final_payload = f"""pcall(function()
    {obfuscated_code}
end)"""
            return final_payload
        else:
            print(f"[Prometheus Compile Error]: {result.stderr}")
            return "warn('[Luasafe VM Error]: Prometheus compilation failed.');"
            
    except Exception as e:
        print(f"[Subprocess Exception]: {str(e)}")
        return f"warn('[Luasafe VM Exception]: {str(e)}');"
        
    finally:
        # 임시 파일 안전하게 정리
        if os.path.exists(input_path):
            os.remove(input_path)
        if os.path.exists(output_path):
            os.remove(output_path)


# --- 스마트 로더 ---
@app.route('/loader.lua', methods=['POST', 'GET'])
def loader():
    if request.method == 'GET':
        lua_payload = """local s, r = pcall(function()
local userKey = Scriptkey or scriptkey or ""
return request({
Url = "https://luasafe-backend.onrender.com/loader.lua",
Method = "POST",
Headers = { ["Content-Type"] = "application/json" },
Body = game:GetService("HttpService"):JSONEncode({
key = userKey,
hwid = tostring(game:GetService("RbxAnalyticsService"):GetClientId())
})
})
end);

if s and r and r.StatusCode == 200 then
local f, err = loadstring(r.Body);
if f then f(); else warn("[Luasafe Error] " .. tostring(err)); end
else
game:GetService("Players").LocalPlayer:Kick("[Luasafe] Auth Failed or Connection Error.");
end;"""
        return lua_payload

    try:
        data = request.get_json(silent=True) or request.form or {}
        key_str = str(data.get('key', '')).strip()
        client_hwid = str(data.get('hwid', '')).strip()

        # 클라이언트 IP 추적
        client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        if client_ip and ',' in client_ip:
            client_ip = client_ip.split(',')[0].strip()

        if not client_hwid or client_hwid.lower() == 'unknown':
            return 'game:GetService("Players").LocalPlayer:Kick("[Luasafe] Security Error: Invalid HWID.");'

        if not key_str:
            return 'game:GetService("Players").LocalPlayer:Kick("[Luasafe] Error: Key is missing.");'

        key_obj = Key.query.filter_by(key=key_str).first()
        if not key_obj or not key_obj.is_valid():
            return 'game:GetService("Players").LocalPlayer:Kick("[Luasafe] Invalid or expired key!");'

        # HWID 검증 및 바인딩
        if key_obj.hwid == 'UNBOUND' or not key_obj.hwid:
            key_obj.hwid = client_hwid
        elif key_obj.hwid != client_hwid:
            return 'game:GetService("Players").LocalPlayer:Kick("[Luasafe] Key bound to another device!");'

        KEY_IPS[key_str] = client_ip
        key_obj.exec_count += 1
        db.session.commit()

        target_script_name = key_obj.script_name
        script = Script.query.filter_by(
            owner_id=key_obj.owner_id, name=target_script_name, active=True
        ).first()
        if not script:
            script = Script.query.filter_by(
                owner_id=key_obj.owner_id, active=True
            ).first()

        if not script:
            return 'game:GetService("Players").LocalPlayer:Kick("[Luasafe] No active script available!");'

        # 🔥 [Prometheus VM 난독화 컴파일러 실행]
        raw_lua = script.lua_code or ""
        vm_packaged_code = compile_to_heavy_vm(raw_lua)
        
        return vm_packaged_code

    except Exception as e:
        return 'game:GetService("Players").LocalPlayer:Kick("[Luasafe Server Error]");'


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
    code_str = f'LUASAFE-{random_part}'

    new_invite = InviteCode(code=code_str, used=False)
    db.session.add(new_invite)
    db.session.commit()
    return jsonify({'success': True, 'code': code_str})


@app.route('/api/secret/invite/list', methods=['GET'])
def secret_list_invites():
    if not session.get('master_logged_in'):
        return jsonify([]), 403
    invites = InviteCode.query.order_by(InviteCode.created_at.desc()).all()
    return jsonify([{'code': i.code, 'used': i.used} for i in invites])


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
        script = Script(
            owner_id=user_id,
            name=name,
            description=description,
            lua_code=lua_code,
            active=True,
        )
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


@app.route('/api/admin/scripts')
@login_required
def admin_scripts():
    user_id = session.get('user_id')
    scripts = Script.query.filter_by(owner_id=user_id).all()
    return jsonify([{
        'id': s.id,
        'name': s.name,
        'description': s.description,
        'lua_code': s.lua_code,
        'active': s.active,
    } for s in scripts])


@app.route('/api/admin/keys')
@login_required
def admin_keys():
    user_id = session.get('user_id')
    keys = Key.query.filter_by(owner_id=user_id).order_by(Key.created_at.desc()).all()
    return jsonify([{
        'id': k.id,
        'key': k.key,
        'tier': k.tier,
        'status': k.status,
        'hwid': k.hwid if k.hwid else 'UNBOUND',
        'ip': KEY_IPS.get(k.key, '미등록'),
        'expiry': k.remaining_time(),
        'execs': k.exec_count,
        'script_name': k.script_name,
    } for k in keys])


@app.route('/api/admin/keys/delete', methods=['POST'])
@login_required
def admin_delete_key():
    user_id = session.get('user_id')
    data = request.get_json() or {}
    key_obj = Key.query.filter_by(id=data.get('id'), owner_id=user_id).first()
    if key_obj:
        if key_obj.key in KEY_IPS:
            del KEY_IPS[key_obj.key]
        db.session.delete(key_obj)
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'success': False}), 403


@app.route('/api/admin/keys/reset_hwid', methods=['POST'])
@login_required
def admin_reset_hwid():
    user_id = session.get('user_id')
    data = request.get_json() or {}
    key_obj = Key.query.filter_by(id=data.get('id'), owner_id=user_id).first()
    if not key_obj:
        return jsonify({'success': False, 'message': '키를 찾을 수 없습니다.'}), 403

    key_obj.hwid = 'UNBOUND'
    db.session.commit()
    return jsonify({'success': True, 'message': 'HWID가 초기화되었습니다.'})


@app.route('/api/admin/keys/reset_ip', methods=['POST'])
@login_required
def admin_reset_ip():
    user_id = session.get('user_id')
    data = request.get_json() or {}
    key_obj = Key.query.filter_by(id=data.get('id'), owner_id=user_id).first()
    if not key_obj:
        return jsonify({'success': False, 'message': '키를 찾을 수 없습니다.'}), 403

    if key_obj.key in KEY_IPS:
        KEY_IPS[key_obj.key] = '미등록'
    return jsonify({'success': True, 'message': 'IP가 초기화되었습니다.'})


@app.route('/api/admin/generate', methods=['POST'])
@login_required
def admin_generate():
    try:
        user_id = session.get('user_id')
        data = request.get_json() or {}
        script_name = data.get('script_name', '')
        duration_type = data.get('duration_type', 'Hours')
        amount = int(data.get('amount', 24))

        chars = string.ascii_uppercase + string.digits
        random_part = ''.join(random.choices(chars, k=16))
        key_str = f'luasafe-{random_part[:4]}-{random_part[4:8]}-{random_part[8:12]}'

        expires = (
            None
            if duration_type == 'Lifetime'
            else datetime.utcnow()
            + timedelta(
                days=amount if duration_type == 'Days' else 0,
                hours=amount if duration_type == 'Hours' else 0,
            )
        )

        new_key = Key(
            owner_id=user_id,
            key=key_str,
            script_name=script_name,
            tier='Standard',
            status='ACTIVE',
            expires_at=expires,
        )
        db.session.add(new_key)
        db.session.commit()
        return jsonify({'success': True, 'key': key_str})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/user/lookup', methods=['POST'])
def user_lookup_key():
    data = request.json or {}
    key_str = data.get('key', '').strip()

    if not key_str:
        return jsonify({'success': False, 'message': '키를 입력해주세요.'}), 400

    key_obj = Key.query.filter_by(key=key_str).first()
    if not key_obj:
        return jsonify({'success': False, 'message': '존재하지 않는 키입니다.'}), 404

    return jsonify({
        'success': True,
        'key': key_obj.key,
        'tier': key_obj.tier,
        'status': key_obj.status,
        'hwid': key_obj.hwid if key_obj.hwid else 'UNBOUND',
        'ip': KEY_IPS.get(key_obj.key, '미등록'),
        'expiry': key_obj.remaining_time(),
        'execs': key_obj.exec_count,
        'script_name': key_obj.script_name,
    })


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
