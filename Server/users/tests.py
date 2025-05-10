from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class UserAuthenticationTests(TestCase):
    """用户认证测试"""
    
    def setUp(self):
        """测试前准备工作"""
        self.client = APIClient()
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'Test123456!',
            'password2': 'Test123456!',
            'bio': '测试用户'
        }
        self.user = User.objects.create_user(
            username=self.user_data['username'],
            email=self.user_data['email'],
            password=self.user_data['password']
        )
        self.token_url = reverse('token_obtain_pair')
        self.refresh_url = reverse('token_refresh')
        self.register_url = reverse('user-list')
        self.me_url = reverse('user-me')
        self.logout_url = reverse('user-logout')
    
    def test_user_registration(self):
        """测试用户注册"""
        new_user_data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'New123456!',
            'password2': 'New123456!',
            'bio': '新测试用户'
        }
        response = self.client.post(self.register_url, new_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)  # 原有用户 + 新用户
    
    def test_user_login(self):
        """测试用户登录"""
        login_data = {
            'username': self.user_data['username'],
            'password': self.user_data['password']
        }
        response = self.client.post(self.token_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
    
    def test_token_refresh(self):
        """测试令牌刷新"""
        # 先登录获取令牌
        login_data = {
            'username': self.user_data['username'],
            'password': self.user_data['password']
        }
        login_response = self.client.post(self.token_url, login_data, format='json')
        refresh_token = login_response.data['refresh']
        
        # 使用刷新令牌获取新的访问令牌
        refresh_data = {'refresh': refresh_token}
        response = self.client.post(self.refresh_url, refresh_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
    
    def test_get_user_profile(self):
        """测试获取用户信息"""
        # 先登录获取令牌
        login_data = {
            'username': self.user_data['username'],
            'password': self.user_data['password']
        }
        login_response = self.client.post(self.token_url, login_data, format='json')
        access_token = login_response.data['access']
        
        # 使用访问令牌获取用户信息
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.get(self.me_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user_data['username'])
        self.assertEqual(response.data['email'], self.user_data['email'])
    
    def test_user_logout(self):
        """测试用户登出"""
        # 先登录获取令牌
        login_data = {
            'username': self.user_data['username'],
            'password': self.user_data['password']
        }
        login_response = self.client.post(self.token_url, login_data, format='json')
        refresh_token = login_response.data['refresh']
        
        # 使用刷新令牌登出
        logout_data = {'refresh': refresh_token}
        response = self.client.post(self.logout_url, logout_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)
        
        # 尝试使用已登出的刷新令牌
        refresh_data = {'refresh': refresh_token}
        response = self.client.post(self.refresh_url, refresh_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_password_validation(self):
        """测试密码验证"""
        # 测试密码不匹配
        invalid_data = {
            'username': 'invaliduser',
            'email': 'invalid@example.com',
            'password': 'Valid123456!',
            'password2': 'Different123456!',
            'bio': '无效用户'
        }
        response = self.client.post(self.register_url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)
        
        # 测试密码太短
        short_password_data = {
            'username': 'shortpassuser',
            'email': 'short@example.com',
            'password': 'short',
            'password2': 'short',
            'bio': '短密码用户'
        }
        response = self.client.post(self.register_url, short_password_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)
