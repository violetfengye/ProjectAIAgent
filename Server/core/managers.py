"""
代码生成管理器
"""
import os
from .generators import CodeGenerator
from .templates import TEMPLATE_CATEGORIES

class CodeGenerationManager:
    def __init__(self, template_id='django_vue'):
        self.generator = CodeGenerator(template_id)
        self.template = TEMPLATE_CATEGORIES[template_id]
        
    def generate_project(self, requirements):
        """
        生成整个项目
        """
        # 1. 分析需求
        analysis = self.analyze_requirements(requirements)
        
        # 2. 生成项目结构
        project_structure = self.generate_project_structure()
        
        # 3. 生成配置文件
        config_files = self.generate_config_files()
        
        # 4. 生成基础代码
        base_code = self.generate_base_code()
        
        # 5. 生成功能模块
        feature_code = self.generate_feature_code(analysis)
        
        return {
            'project_structure': project_structure,
            'config_files': config_files,
            'base_code': base_code,
            'feature_code': feature_code
        }
        
    def analyze_requirements(self, requirements):
        """
        分析需求，提取关键信息
        """
        # 这里可以调用DeepSeek API来分析需求
        # 返回分析结果
        return {
            'modules': [
                {
                    'name': 'auth',
                    'features': ['用户注册', '用户登录', '密码重置']
                },
                {
                    'name': 'project',
                    'features': ['项目创建', '项目列表', '项目详情']
                }
            ],
            'dependencies': [
                'django',
                'djangorestframework',
                'django-cors-headers'
            ]
        }
        
    def generate_project_structure(self):
        """
        生成项目目录结构
        """
        if self.template['name'] == "Django + Vue":
            return {
                'backend': {
                    'apps': ['users', 'core'],
                    'config': ['settings', 'urls', 'wsgi'],
                    'tests': ['test_users', 'test_core']
                },
                'frontend': {
                    'src': ['components', 'views', 'store', 'router'],
                    'public': ['index.html'],
                    'tests': ['test_components']
                }
            }
        else:
            return {
                'apps': ['users', 'core'],
                'templates': ['base.html', 'users', 'core'],
                'static': ['css', 'js', 'img'],
                'tests': ['test_users', 'test_core']
            }
            
    def generate_config_files(self):
        """
        生成配置文件
        """
        config_files = {}
        
        # 生成requirements.txt
        config_files['requirements.txt'] = self.generate_requirements()
        
        # 生成settings.py
        config_files['settings.py'] = self.generate_settings()
        
        # 生成urls.py
        config_files['urls.py'] = self.generate_urls()
        
        return config_files
        
    def generate_requirements(self):
        """
        生成依赖文件
        """
        requirements = [
            'django>=4.2.0',
            'djangorestframework>=3.14.0',
            'django-cors-headers>=4.0.0',
            'django-filter>=23.0',
            'psycopg2-binary>=2.9.0',
            'python-dotenv>=1.0.0',
            'pytest>=7.0.0',
            'pytest-django>=4.5.0'
        ]
        
        if self.template['name'] == "Django + Vue":
            requirements.extend([
                'drf-yasg>=1.21.0',
                'django-rest-swagger>=2.2.0'
            ])
            
        return '\n'.join(requirements)
        
    def generate_settings(self):
        """
        生成Django设置文件
        """
        settings = f"""
# Django settings for {self.template['name']} project

import os
from pathlib import Path
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'your-secret-key-here')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'django_filters',
    'users',
    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {{
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {{
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        }},
    }},
]

WSGI_APPLICATION = 'core.wsgi.application'

# Database
DATABASES = {{
    'default': {{
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }}
}}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {{
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    }},
    {{
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    }},
    {{
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    }},
    {{
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    }},
]

# Internationalization
LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST Framework settings
REST_FRAMEWORK = {{
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ),
}}

# JWT settings
SIMPLE_JWT = {{
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,
}}

# CORS settings
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
"""
        return settings
        
    def generate_urls(self):
        """
        生成URL配置文件
        """
        urls = """
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/core/', include('core.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
"""
        return urls
        
    def generate_base_code(self):
        """
        生成基础代码
        """
        base_code = {}
        
        # 生成权限类
        base_code['permissions.py'] = self.generator.generate_permissions()
        
        # 生成中间件
        base_code['middleware.py'] = self.generator.generate_middleware()
        
        # 生成响应格式
        base_code['response.py'] = self.generator.generate_response_format()
        
        return base_code
        
    def generate_feature_code(self, analysis):
        """
        生成功能模块代码
        """
        feature_code = {}
        
        for module in analysis['modules']:
            module_code = self.generator.generate_module(
                module['name'],
                module['features']
            )
            feature_code[module['name']] = module_code
            
        return feature_code 