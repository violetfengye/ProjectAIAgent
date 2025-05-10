from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """自定义用户模型"""
    email = models.EmailField(unique=True, verbose_name='邮箱')
    avatar = models.URLField(max_length=255, blank=True, null=True, verbose_name='头像')
    bio = models.TextField(max_length=500, blank=True, verbose_name='个人简介')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    # 添加related_name解决冲突
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        ordering = ['-date_joined']

    def __str__(self):
        return self.username
