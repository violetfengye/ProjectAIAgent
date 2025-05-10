"""
代码生成器
"""
import os
from .templates import (
    TEMPLATE_CATEGORIES,
    CODE_GENERATION_RULES,
    API_RESPONSE_RULES,
    PERMISSION_RULES,
    MIDDLEWARE_RULES
)

class CodeGenerator:
    def __init__(self, template_id='django_vue'):
        self.template = TEMPLATE_CATEGORIES[template_id]
        self.rules = CODE_GENERATION_RULES
        
    def generate_module(self, module_name, requirements=None):
        """生成模块代码"""
        if module_name not in self.rules:
            return self.generate_custom_module(module_name, requirements)
            
        module_rules = self.rules[module_name]
        return {
            'models': self.generate_models(module_rules['models']),
            'serializers': self.generate_serializers(module_rules['serializers']),
            'views': self.generate_views(module_rules['views']),
            'urls': self.generate_urls(module_rules.get('urls', {}))
        }
        
    def generate_models(self, model_rules):
        """生成模型代码"""
        code = []
        for model_name, model_config in model_rules.items():
            # 生成字段
            fields = self.generate_model_fields(model_config['fields'])
            
            # 生成方法
            methods = self.generate_model_methods(model_config['methods'])
            
            # 组合模型代码
            model_code = f"""
class {model_name}(models.Model):
    {fields}
    
    {methods}
    
    class Meta:
        ordering = ['-created_at']
        """
            code.append(model_code)
            
        return '\n'.join(code)
        
    def generate_model_fields(self, fields):
        """生成模型字段"""
        field_code = []
        for field in fields:
            field_str = f"{field['name']} = models.{field['type']}"
            if 'max_length' in field:
                field_str += f"(max_length={field['max_length']})"
            if 'unique' in field:
                field_str += f", unique={field['unique']}"
            if 'blank' in field:
                field_str += f", blank={field['blank']}"
            if 'null' in field:
                field_str += f", null={field['null']}"
            if 'default' in field:
                field_str += f", default={field['default']}"
            if 'choices' in field:
                choices_str = str(field['choices']).replace("'", '"')
                field_str += f", choices={choices_str}"
            field_code.append(f"    {field_str}")
            
        return '\n'.join(field_code)
        
    def generate_model_methods(self, methods):
        """生成模型方法"""
        method_code = []
        for method in methods:
            if method == 'set_password':
                method_code.append("""
    def set_password(self, raw_password):
        self.password = make_password(raw_password)
                """)
            elif method == 'check_password':
                method_code.append("""
    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
                """)
            elif method == 'get_full_name':
                method_code.append("""
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()
                """)
            elif method == 'add_collaborator':
                method_code.append("""
    def add_collaborator(self, user):
        if user not in self.collaborators.all():
            self.collaborators.add(user)
            return True
        return False
                """)
            elif method == 'remove_collaborator':
                method_code.append("""
    def remove_collaborator(self, user):
        if user in self.collaborators.all():
            self.collaborators.remove(user)
            return True
        return False
                """)
            elif method == 'update_status':
                method_code.append("""
    def update_status(self, new_status):
        if new_status in dict(self._meta.get_field('status').choices):
            self.status = new_status
            self.save()
            return True
        return False
                """)
                
        return '\n'.join(method_code)
        
    def generate_serializers(self, serializer_rules):
        """生成序列化器代码"""
        code = []
        for serializer_name, serializer_config in serializer_rules.items():
            fields = serializer_config['fields']
            read_only_fields = serializer_config.get('read_only_fields', [])
            
            serializer_code = f"""
class {serializer_name}(serializers.ModelSerializer):
    class Meta:
        model = {serializer_name.replace('Serializer', '')}
        fields = {fields}
        read_only_fields = {read_only_fields}
            """
            code.append(serializer_code)
            
        return '\n'.join(code)
        
    def generate_views(self, view_rules):
        """生成视图代码"""
        code = []
        for view_name, view_config in view_rules.items():
            actions = view_config['actions']
            permissions = view_config['permissions']
            filters = view_config.get('filters', [])
            
            view_code = f"""
class {view_name}(viewsets.ModelViewSet):
    queryset = {view_name.replace('ViewSet', '')}.objects.all()
    serializer_class = {view_name.replace('ViewSet', 'Serializer')}
    permission_classes = [{', '.join(permissions)}]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = {filters}
    search_fields = ['name', 'description']
    ordering_fields = ['created_at', 'updated_at']
            """
            code.append(view_code)
            
        return '\n'.join(code)
        
    def generate_urls(self, url_rules):
        """生成URL配置代码"""
        if not url_rules:
            return ""
            
        patterns = url_rules.get('patterns', [])
        code = ["urlpatterns = ["]
        
        for pattern in patterns:
            path = pattern['path']
            view = pattern['view']
            basename = pattern.get('basename', '')
            
            if basename:
                code.append(f"    path('{path}', {view}.as_view({{'basename': '{basename}'}})),")
            else:
                code.append(f"    path('{path}', {view}.as_view()),")
                
        code.append("]")
        return '\n'.join(code)
        
    def generate_custom_module(self, module_name, requirements):
        """生成自定义模块代码"""
        # 这里可以调用DeepSeek API来生成自定义模块的代码
        pass
        
    def generate_permissions(self):
        """生成权限类代码"""
        code = []
        for permission_name, permission_config in PERMISSION_RULES.items():
            permission_code = f"""
class {permission_name}(BasePermission):
    {permission_config['description']}
    
    def has_object_permission(self, request, view, obj):
        {permission_config['has_object_permission']}
            """
            code.append(permission_code)
            
        return '\n'.join(code)
        
    def generate_middleware(self):
        """生成中间件代码"""
        code = []
        for middleware_name, middleware_config in MIDDLEWARE_RULES.items():
            middleware_code = f"""
class {middleware_name}:
    {middleware_config['description']}
    
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        {middleware_config['process_request']}
        response = self.get_response(request)
        return response
            """
            code.append(middleware_code)
            
        return '\n'.join(code)
        
    def generate_response_format(self):
        """生成API响应格式代码"""
        return f"""
def api_response(data=None, message="操作成功", code=200, errors=None):
    if errors:
        return {{
            'code': 400,
            'message': message,
            'errors': errors
        }}
    return {{
        'code': code,
        'message': message,
        'data': data
    }}
        """ 