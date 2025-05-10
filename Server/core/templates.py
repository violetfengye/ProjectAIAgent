"""
代码生成模板系统配置
"""

# 模板分类
TEMPLATE_CATEGORIES = {
    "django_vue": {
        "name": "Django + Vue",
        "description": "前后端分离架构，Django提供RESTful API，Vue负责前端展示",
        "tech_stack": {
            "backend": ["Django", "Django REST framework", "PostgreSQL"],
            "frontend": ["Vue 3", "Vuex", "Vue Router", "Element Plus"],
            "deployment": ["Docker", "Nginx"]
        },
        "features": [
            "用户认证",
            "RESTful API",
            "前后端分离",
            "响应式设计"
        ]
    },
    "django_only": {
        "name": "纯Django",
        "description": "传统Django架构，使用Django模板系统",
        "tech_stack": {
            "backend": ["Django", "SQLite/PostgreSQL"],
            "frontend": ["Django Templates", "Bootstrap"],
            "deployment": ["Gunicorn", "Nginx"]
        },
        "features": [
            "用户认证",
            "Django模板",
            "表单处理",
            "Admin后台"
        ]
    }
}

# 代码生成规则
CODE_GENERATION_RULES = {
    # 用户认证模块规则
    "auth": {
        "models": {
            "User": {
                "fields": [
                    {"name": "username", "type": "CharField", "max_length": 150, "unique": True},
                    {"name": "email", "type": "EmailField", "unique": True},
                    {"name": "password", "type": "CharField", "max_length": 128},
                    {"name": "avatar", "type": "URLField", "max_length": 255, "blank": True, "null": True},
                    {"name": "bio", "type": "TextField", "max_length": 500, "blank": True},
                    {"name": "is_active", "type": "BooleanField", "default": True},
                    {"name": "date_joined", "type": "DateTimeField", "auto_now_add": True}
                ],
                "methods": [
                    "set_password",
                    "check_password",
                    "get_full_name"
                ]
            }
        },
        "serializers": {
            "UserSerializer": {
                "fields": ["id", "username", "email", "avatar", "bio", "date_joined"],
                "read_only_fields": ["date_joined"]
            }
        },
        "views": {
            "UserViewSet": {
                "actions": ["list", "create", "retrieve", "update", "destroy"],
                "permissions": ["IsAuthenticated"],
                "filters": ["username", "email"]
            }
        },
        "urls": {
            "patterns": [
                {"path": "users/", "view": "UserViewSet", "basename": "user"}
            ]
        }
    },
    
    # 项目模块规则
    "project": {
        "models": {
            "Project": {
                "fields": [
                    {"name": "name", "type": "CharField", "max_length": 100},
                    {"name": "description", "type": "TextField", "blank": True},
                    {"name": "owner", "type": "ForeignKey", "to": "User", "on_delete": "CASCADE"},
                    {"name": "collaborators", "type": "ManyToManyField", "to": "User", "blank": True},
                    {"name": "created_at", "type": "DateTimeField", "auto_now_add": True},
                    {"name": "updated_at", "type": "DateTimeField", "auto_now": True},
                    {"name": "is_public", "type": "BooleanField", "default": False},
                    {"name": "status", "type": "CharField", "max_length": 20, "choices": [
                        ("planning", "规划中"),
                        ("in_progress", "进行中"),
                        ("completed", "已完成"),
                        ("archived", "已归档")
                    ], "default": "planning"}
                ],
                "methods": [
                    "add_collaborator",
                    "remove_collaborator",
                    "update_status"
                ]
            }
        },
        "serializers": {
            "ProjectSerializer": {
                "fields": ["id", "name", "description", "owner", "collaborators", 
                          "created_at", "updated_at", "is_public", "status"],
                "read_only_fields": ["created_at", "updated_at"]
            }
        },
        "views": {
            "ProjectViewSet": {
                "actions": ["list", "create", "retrieve", "update", "destroy"],
                "permissions": ["IsAuthenticated"],
                "filters": ["name", "status", "is_public"]
            }
        }
    }
}

# API响应格式规则
API_RESPONSE_RULES = {
    "success": {
        "code": 200,
        "message": "操作成功",
        "data": None
    },
    "error": {
        "code": 400,
        "message": "操作失败",
        "errors": None
    }
}

# 权限规则
PERMISSION_RULES = {
    "IsOwner": {
        "description": "检查用户是否是资源所有者",
        "has_object_permission": "return obj.owner == request.user"
    },
    "IsCollaborator": {
        "description": "检查用户是否是项目协作者",
        "has_object_permission": "return request.user in obj.collaborators.all()"
    }
}

# 中间件规则
MIDDLEWARE_RULES = {
    "AuthenticationMiddleware": {
        "description": "用户认证中间件",
        "process_request": "request.user = auth.get_user(request)"
    },
    "CorsMiddleware": {
        "description": "跨域请求中间件",
        "process_request": "handle_cors(request, response)"
    }
} 