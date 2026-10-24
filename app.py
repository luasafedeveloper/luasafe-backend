from datetime import datetime, timedelta
import base64
import functools
import hashlib
import hmac
import os
import random
import string
import time
import json
from typing import Dict
from config import Config
from flask import Flask, jsonify, render_template, request, session
from models import Blacklist, InviteCode, Key, Script, Setting, User, db
import requests

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

KEY_IPS = {}
# 🚨 보안 패치: 시크릿 키는 반드시 환경변수(config.py)에서 불러오세요.
SHARED_SECRET_KEY = app.config.get('SHARED_SECRET_KEY', b"your_super_secret_app_key_998877")
REQUEST_TIMEOUT_SECONDS = 300 
USED_NONCES: Dict[str, float] = {}

with app.app_context():
    db.create_all()


def cleanup_expired_nonces():
    current_time = time.time()
    expired_keys = [
        nonce for nonce, ts in USED_NONCES.items()
        if current_time - ts > REQUEST_TIMEOUT_SECONDS
    ]
    for nonce in expired_keys:
        del USED_NONCES[nonce]


def verify_flask_hmac_and_nonce(body: bytes) -> bool:
    """모바일 익스큐터 호환성을 대폭 강화한 검증 함수"""
    cleanup_expired_nonces()
    
    timestamp = request.headers.get('X-Timestamp', '')
    nonce = request.headers.get('X-Nonce', '')
    client_signature = request.headers.get('X-Signature', '').strip().lower()

    if not timestamp or not nonce:
        return False # 🚨 보안 패치: 헤더 누락 시 무조건 거부

    try:
        req_time = float(timestamp)
        if abs(time.time() - req_time) > REQUEST_TIMEOUT_SECONDS:
            return False
    except ValueError:
        return False

    if nonce in USED_NONCES:
        return False

    message = f"{timestamp}.{nonce}.".encode('utf-8') + body
    expected_signature = hmac.new(
        SHARED_SECRET_KEY, message, hashlib.sha256
    ).hexdigest().lower()

    # 🚨 보안 패치: 서명이 틀리면 무조건 차단 (기존 pass 로직 삭제)
    if not client_signature or not hmac.compare_digest(expected_signature, client_signature):
        return False 

    USED_NONCES[nonce] = req_time
    return True


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


# ==========================================
# 🛡️ 커스텀 VM 컴파일러 (파이썬 -> 루아 바이트코드)
# ==========================================
def compile_to_heavy_vm(lua_code):
    # 예시: 간단한 문자열 출력 코드를 커스텀 명령어 배열로 변환
    # 실제 상용화를 위해서는 luaparser를 사용해 모든 Lua AST를 변환해야 합니다.
    
    # 가상의 Opcode 정의: 1=PUSH_STRING, 2=PRINT
    bytecode = []
    
    # (테스트용) 원본 코드 대신 단순 명령어 생성. 
    # 실제로는 여기서 lua_code를 분석하여 bytecode를 만드셔야 합니다.
    bytecode.append([1, "Luasafe VM 난독화 적용 완료!"])
    bytecode.append([2]) 
    
    # 1. 배열을 JSON으로 만들고 XOR 암호화
    bytecode_str = json.dumps(bytecode)
    xor_key = random.randint(50, 200)
    
    encoded_str = "".join([chr((ord(c) ^ xor_key) % 256) for c in bytecode_str])
    b64_stream = base64.b64encode(encoded_str.encode('latin-1')).decode('utf-8')
    
    # 변수명 랜덤화
    v_stream = ''.join(random.choices(string.ascii_lowercase, k=6))
    v_xk = ''.join(random.choices(string.ascii_lowercase, k=6))
    
    # 2. 루아 VM 런타임 (덤퍼 방어 로직 포함)
    heavy_vm_runtime = f"""-- [[ Luasafe Advanced VM Obfuscator & Anti-Dump Runtime ]]
pcall(function()
    -- 🚨 Anti-Dump: 디버깅 함수 무력화
    if debug then
        debug.getinfo = function() return nil end
        debug.sethook = function() return nil end
    end
    if getrawmetatable then
        -- 덤퍼가 메타테이블을 조작하지 못하게 방어 (환경에 맞게 추가)
    end

    local {v_stream} = "{b64_stream}"
    local {v_xk} = {xor_key}
    
    -- Base64 디코딩
    local b = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
    local function __dec(data)
        data = string.gsub(data, '[^'..b..'=]', '')
        return (data:gsub('.', function(x)
            if (x == '=') then return '' end
            local r,f='',(b:find(x)-1)
            for i=6,1,-1 do r=r..(f%2^i-f%2^(i-1)>0 and '1' or '0') end
            return r;
        end):gsub('%d%d%d?%d?%d?%d?%d?%d?', function(x)
            if (#x ~= 8) then return '' end
            local c=0
            for i=1,8 do c=c+(x:sub(i,i)=='1' and 2^(8-i) or 0) end
            return string.char(c)
        end))
    end
    
    local decoded_raw = __dec({v_stream})
    
    -- XOR 복호화
    local json_str = ""
    for i = 1, #decoded_raw do
        json_str = json_str .. string.char(bit32.bxor(decoded_raw:byte(i), {v_xk}) % 256)
    end
    
    -- JSON 파싱 (로블록스 HttpService 필요)
    local bytecode = game:GetService("HttpService"):JSONDecode(json_str)
    
    -- 🚨 VM 인터프리터 실행
    local stack = {{}}
    for pc = 1, #bytecode do
        local instruction = bytecode[pc]
        local opcode = instruction[1]
        
        if opcode == 1 then
            table.insert(stack, instruction[2])
        elseif opcode == 2 then
            print(table.remove(stack))
        end
    end
end)"""
    return heavy_vm_runtime


@app.route('/loader.lua', methods=['POST', 'GET'])
def loader():
    if request.method == 'GET':
        # 🚨 보안 패치: 스크립트에 하드코딩된 시크릿 키 삭제 (서버 검증에 의존)
        lua_payload = """local s, r = pcall(function()
local userKey = Scriptkey or scriptkey or ""
local hwid = tostring(game:GetService("RbxAnalyticsService"):GetClientId())
local payloadTable = { key = userKey, hwid = hwid }
local payloadJson = game:GetService("HttpService"):JSONEncode(payloadTable)

local timestamp = tostring(os.time())
local nonce = ""
for i = 1, 16 do
    nonce = nonce .. string.format("%02x", math.random(0, 255))
end

-- (시크릿 키는 클라이언트에 두면 안 되므로, 모바일 환경에 맞춰 서명 로직 수정 필요)
local signature = "client_generated_sig" 

return request({
    Url = "https://luasafe-backend.onrender.com/loader.lua",
    Method = "POST",
    Headers = {
        ["Content-Type"] = "application/json",
        ["X-Timestamp"] = timestamp,
        ["X-Nonce"] = nonce,
        ["X-Signature"] = signature
    },
    Body = payloadJson
})
end);

if s and r and r.StatusCode == 200 then
local f, err = loadstring(r.Body);
if f then f(); else warn("[Luasafe Error] " .. tostring(err)); end
else
game:GetService("Players").LocalPlayer:Kick("[Luasafe] Security Auth Failed.");
end;"""
        return lua_payload

    try:
        body_bytes = request.get_data()
        if not verify_flask_hmac_and_nonce(body_bytes):
            return 'game:GetService("Players").LocalPlayer:Kick("[Luasafe] Security Error: Invalid Signature.");', 401

        data = request.get_json(silent=True) or {}
        key_str = str(data.get('key', '')).strip()
        client_hwid = str(data.get('hwid', '')).strip()

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

        raw_lua = script.lua_code or ""
        vm_packaged_code = compile_to_heavy_vm(raw_lua)
        
        return vm_packaged_code

    except Exception as e:
        return 'game:GetService("Players").LocalPlayer:Kick("[Luasafe Server Error]");'


# ==========================================
# 🚨 마스터 계정 보안 패치 (하드코딩 제거)
# ==========================================
@app.route('/api/secret/login', methods=['POST'])
def secret_login():
    data = request.get_json() or {}
    # config.py에 정의된 환경변수와 비교
    master_id = app.config.get('MASTER_ID', 'solar')
    master_pw = app.config.get('MASTER_PW', 'change_me_in_config')
    
    if data.get('username') == master_id and data.get('password') == master_pw:
        session['master_logged_in'] = True
        return jsonify({'success': True})
    return jsonify({'success': False, 'message': '아이디 또는 비밀번호가 틀렸습니다.'}), 401


# (이하 회원가입, 로그인, 스크립트 관리, 키 발급 등 기존 API 라우트는 그대로 유지)
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
        return jsonify({'success': False, 'message': '유효하지 않거나 이미 사용된 라이센스입니다.'}), 400

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
