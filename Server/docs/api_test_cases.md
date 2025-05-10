# API 测试用例文档

本文档包含了所有 API 端点的测试用例，用于验证用户认证和用户管理功能的正确性。

## 目录

- [1. 用户注册测试](#1-用户注册测试)
- [2. 用户认证测试](#2-用户认证测试)
- [3. 用户信息测试](#3-用户信息测试)
- [4. 用户登出测试](#4-用户登出测试)

## 1. 用户注册测试

### 1.1 正常注册

- **请求方法**: POST
- **URL**: `http://localhost:8000/api/users/`
- **请求头**:
  ```
  Content-Type: application/json
  ```
- **请求体**:
  ```json
  {
    "username": "testuser",
    "email": "test@example.com",
    "password": "Test123456!",
    "password2": "Test123456!",
    "avatar": null,
    "bio": ""
  }
  ```
- **预期响应**: 201 Created
- **响应体示例**:
  ```json
  {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com",
    "avatar": null,
    "bio": "",
    "date_joined": "2024-03-21T10:00:00Z",
    "last_login": null
  }
  ```

### 1.2 密码不匹配

- **请求方法**: POST
- **URL**: `http://localhost:8000/api/users/`
- **请求头**:
  ```
  Content-Type: application/json
  ```
- **请求体**:
  ```json
  {
    "username": "testuser2",
    "email": "test2@example.com",
    "password": "Test123456!",
    "password2": "Test1234567!",
    "avatar": null,
    "bio": ""
  }
  ```
- **预期响应**: 400 Bad Request
- **响应体示例**:
  ```json
  {
    "password": ["两次密码不匹配"]
  }
  ```

### 1.3 缺少必需字段

- **请求方法**: POST
- **URL**: `http://localhost:8000/api/users/`
- **请求头**:
  ```
  Content-Type: application/json
  ```
- **请求体**:
  ```json
  {
    "username": "testuser",
    "email": "test@example.com",
    "avatar": null,
    "bio": ""
  }
  ```
- **预期响应**: 400 Bad Request
- **响应体示例**:
  ```json
  {
    "password": ["该字段是必填项。"],
    "password2": ["该字段是必填项。"]
  }
  ```

## 2. 用户认证测试

### 2.1 获取令牌

- **请求方法**: POST
- **URL**: `http://localhost:8000/api/token/`
- **请求头**:
  ```
  Content-Type: application/json
  ```
- **请求体**:
  ```json
  {
    "username": "testuser",
    "password": "Test123456!"
  }
  ```
- **预期响应**: 200 OK
- **响应体示例**:
  ```json
  {
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  }
  ```

### 2.2 刷新令牌

- **请求方法**: POST
- **URL**: `http://localhost:8000/api/token/refresh/`
- **请求头**:
  ```
  Content-Type: application/json
  ```
- **请求体**:
  ```json
  {
    "refresh": "你的refresh令牌"
  }
  ```
- **预期响应**: 200 OK
- **响应体示例**:
  ```json
  {
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  }
  ```

### 2.3 验证令牌

- **请求方法**: POST
- **URL**: `http://localhost:8000/api/token/verify/`
- **请求头**:
  ```
  Content-Type: application/json
  ```
- **请求体**:
  ```json
  {
    "token": "你的access令牌"
  }
  ```
- **预期响应**: 200 OK
- **响应体示例**:
  ```json
  {}
  ```

## 3. 用户信息测试

### 3.1 获取当前用户信息

- **请求方法**: GET
- **URL**: `http://localhost:8000/api/users/me/`
- **请求头**:
  ```
  Authorization: Bearer 你的access令牌
  ```
- **预期响应**: 200 OK
- **响应体示例**:
  ```json
  {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com",
    "avatar": null,
    "bio": "",
    "date_joined": "2024-03-21T10:00:00Z",
    "last_login": "2024-03-21T10:30:00Z"
  }
  ```

### 3.2 更新用户信息

- **请求方法**: POST
- **URL**: `http://localhost:8000/api/users/update_profile/`
- **请求头**:
  ```
  Authorization: Bearer 你的access令牌
  Content-Type: application/json
  ```
- **请求体**:
  ```json
  {
    "email": "newemail@example.com",
    "bio": "这是我的新简介"
  }
  ```
- **预期响应**: 200 OK
- **响应体示例**:
  ```json
  {
    "id": 1,
    "username": "testuser",
    "email": "newemail@example.com",
    "avatar": null,
    "bio": "这是我的新简介",
    "date_joined": "2024-03-21T10:00:00Z",
    "last_login": "2024-03-21T10:30:00Z"
  }
  ```

## 4. 用户登出测试

### 4.1 用户登出

- **请求方法**: POST
- **URL**: `http://localhost:8000/api/users/logout/`
- **请求头**:
  ```
  Authorization: Bearer 你的access令牌
  Content-Type: application/json
  ```
- **请求体**:
  ```json
  {
    "refresh": "你的refresh令牌"
  }
  ```
- **预期响应**: 205 Reset Content

## 测试步骤建议

1. 首先测试注册功能，创建一个新用户
2. 使用新创建的用户获取 JWT 令牌
3. 使用获取的令牌测试获取用户信息接口
4. 测试更新用户信息功能
5. 测试令牌刷新功能
6. 最后测试登出功能

## 注意事项

1. 确保服务器已经启动并运行在`localhost:8000`
2. 在测试需要认证的接口时，请将`你的access令牌`替换为实际获取到的令牌
3. 在测试登出功能时，请将`你的refresh令牌`替换为实际获取到的 refresh 令牌
4. 建议按照上述顺序进行测试，因为某些测试可能依赖于前面测试的结果
5. 所有密码必须符合 Django 的密码验证规则：
   - 至少 8 个字符
   - 不能是纯数字
   - 不能是常见密码
   - 不能与用户名相似
   - 不能与个人信息相关
