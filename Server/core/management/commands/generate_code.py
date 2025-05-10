"""
代码生成命令
"""
from django.core.management.base import BaseCommand
from core.managers import CodeGenerationManager

class Command(BaseCommand):
    help = '生成项目代码'

    def add_arguments(self, parser):
        parser.add_argument('--template', type=str, default='django_vue',
                          help='项目模板类型')
        parser.add_argument('--requirements', type=str, required=True,
                          help='项目需求文件路径')

    def handle(self, *args, **options):
        template_id = options['template']
        requirements_file = options['requirements']

        # 读取需求文件
        with open(requirements_file, 'r', encoding='utf-8') as f:
            requirements = f.read()

        # 初始化代码生成管理器
        manager = CodeGenerationManager(template_id)

        # 生成项目代码
        result = manager.generate_project(requirements)

        # 输出生成结果
        self.stdout.write(self.style.SUCCESS('项目结构：'))
        self.stdout.write(str(result['project_structure']))

        self.stdout.write(self.style.SUCCESS('配置文件：'))
        for filename, content in result['config_files'].items():
            self.stdout.write(f'{filename}:')
            self.stdout.write(content)

        self.stdout.write(self.style.SUCCESS('基础代码：'))
        for filename, content in result['base_code'].items():
            self.stdout.write(f'{filename}:')
            self.stdout.write(content)

        self.stdout.write(self.style.SUCCESS('功能模块：'))
        for module_name, module_code in result['feature_code'].items():
            self.stdout.write(f'{module_name}:')
            self.stdout.write(str(module_code)) 