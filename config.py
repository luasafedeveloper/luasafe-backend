import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "mineminyee-super-secret-key-2026")
    SQLALCHEMY_DATABASE_URI = "sqlite:///mineminyee_luarmor.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # 마스터 암호화 키 (절대 외부에 노출 금지)
    MASTER_SECRET = os.getenv("MASTER_SECRET", "mineminyee_master_key_2026_secure")
    
    # 도메인 설정
    USER_DOMAIN = "http://user-lua.kro.kr:5000"
    ADMIN_DOMAIN = "http://lua-scriptluarmor.kro.kr:5000"
    LOADER_DOMAIN = "http://mineminyee-lua.kro.kr:5000"
    DUMMY_DOMAIN = "http://mineminyeehack.kro.kr:5000"