from .settings import *

# 使用内存数据库进行测试
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# 禁用密码哈希，加快测试速度
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

# 禁用调试模式
DEBUG = False

# 使用简单的密钥
SECRET_KEY = 'test-key-not-for-production'

# 禁用CORS检查
CORS_ALLOW_ALL_ORIGINS = True

# 禁用JWT令牌过期
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
} 