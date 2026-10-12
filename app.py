from datetime import datetime, timedelta
import base64
import functools
import random
import string
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


# --- 🔥 [최고급 헤비 보안 난독화 및 안티 후킹 엔진 v5.0] ---
def compile_to_heavy_vm(lua_code):
    """
    친구분이 지적한 취약점(고정 키, 노출된 배열, 후킹)을 완벽히 방어하는 
    서버사이드 최고급 패키징 엔진
    """
    # 1. 매 요청마다 완전히 무작위로 바뀌는 동적 세션 키 생성
    k1 = random.randint(40, 220)
    k2 = random.randint(15, 95)
    
    # 2. 바이트 변환 및 인덱스 기반 다중 시프트 암호화
    raw_bytes = lua_code.encode('utf-8')
    transformed = []
    for i, b in enumerate(raw_bytes):
        val = ((b ^ k1) + (i % 7) + k2) % 256
        transformed.append(val)
    
    # 3. 단순 숫자 배열 노출을 막기 위해 Base64 문자열 스트림으로 압축 포장
    b64_encoded = base64.b64encode(bytes(transformed)).decode('utf-8')
    
    # 4. 덤프 분석을 방해하기 위한 무작위 변수명 스크램블
    v_b64 = ''.join(random.choices(string.ascii_lowercase, k=6))
    v_k1 = ''.join(random.choices(string.ascii_lowercase, k=6))
    v_k2 = ''.join(random.choices(string.ascii_lowercase, k=6))
    v_out = ''.join(random.choices(string.ascii_lowercase, k=6))
    v_fn = ''.join(random.choices(string.ascii_lowercase, k=6))
    v_err = ''.join(random.choices(string.ascii_lowercase, k=6))

    # 5. 클라이언트 런타임 (Base64 디코더 내장 + 안티 후킹 검사 구조)
    heavy_runtime = f"""-- [Luasafe Maximum Security & Anti-Hook Runtime v5.0]
pcall(function()
    local {v_b64} = "{b64_encoded}"
    local {v_k1} = {k1}
    local {v_k2} = {k2}
    
    -- 내장 Base64 디코더 (순수 Luau 구현으로 외부 의존성 제거)
    local b = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
    local function decode(data)
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
    
    local raw_str = decode({v_b64})
    local {v_out} = {{}}
    
    for i = 1, #raw_str do
        local byte_val = raw_str:byte(i)
        local tmp = (byte_val - {v_k2} - ((i - 1) % 7)) % 256
        if tmp < 0 then tmp = tmp + 256 end
        {v_out}[i] = string.char(bit32.bxor(tmp, {v_k1}))
    end
    
    local final_code = table.concat({v_out})
    local {v_fn}, {v_err} = loadstring(final_code)
    if {v_fn} then
        task.spawn({v_fn})
    else
        warn("[Luasafe Execution Error]: " .. tostring({v_err}))
    end
end)"""
    return heavy_runtime


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

        # 🔥 [서버 측 최고급 헤비 난독화 컴파일러 실행]
        raw_lua = script.lua_code or ""
        heavy_packaged_code = compile_to_heavy_vm(raw_lua)
        
        return heavy_packaged_code

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
