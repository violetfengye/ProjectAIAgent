from django.db import models
from django.conf import settings

class Project(models.Model):
    """项目模型"""
    name = models.CharField(max_length=100, verbose_name='项目名称')
    description = models.TextField(blank=True, verbose_name='项目描述')
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='owned_projects',
        verbose_name='项目所有者'
    )
    collaborators = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='collaborated_projects',
        blank=True,
        verbose_name='项目协作者'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    is_public = models.BooleanField(default=False, verbose_name='是否公开')
    status = models.CharField(
        max_length=20,
        choices=[
            ('planning', '规划中'),
            ('in_progress', '进行中'),
            ('completed', '已完成'),
            ('archived', '已归档')
        ],
        default='planning',
        verbose_name='项目状态'
    )

    class Meta:
        verbose_name = '项目'
        verbose_name_plural = verbose_name
        ordering = ['-updated_at']

    def __str__(self):
        return self.name
