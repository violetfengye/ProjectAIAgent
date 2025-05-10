from django.contrib.auth import user_logged_in
from django.utils import timezone
from django.dispatch import receiver

@receiver(user_logged_in)
def update_last_login(sender, request, user, **kwargs):
    """更新用户最后登录时间"""
    user.last_login = timezone.now()
    user.save(update_fields=['last_login']) 