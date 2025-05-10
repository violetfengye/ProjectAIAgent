# API 调用流程示例

以下是一个完整的项目创建和管理流程示例，展示了如何使用 API 进行项目操作。

## 1. 用户认证流程

### 1.1 用户注册

```http
POST /api/users/
Content-Type: application/json

{
    "username": "testuser",
    "email": "test@example.com",
    "password": "securepassword123"
}
```

响应：

```json
{
  "id": 1,
  "username": "testuser",
  "email": "test@example.com",
  "avatar": null,
  "bio": "",
  "date_joined": "2024-03-31T10:00:00Z"
}
```

### 1.2 用户登录

```http
POST /api/token/
Content-Type: application/json

{
    "username": "testuser",
    "password": "securepassword123"
}
```

响应：

```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

## 2. 项目管理流程

### 2.1 创建新项目

```http
POST /api/projects/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
Content-Type: application/json

{
    "name": "我的第一个项目",
    "description": "这是一个测试项目",
    "is_public": false,
    "status": "planning"
}
```

响应：

```json
{
  "id": 1,
  "name": "我的第一个项目",
  "description": "这是一个测试项目",
  "owner": 1,
  "collaborators": [],
  "created_at": "2024-03-31T10:30:00Z",
  "updated_at": "2024-03-31T10:30:00Z",
  "is_public": false,
  "status": "planning"
}
```

### 2.2 获取项目列表

```http
GET /api/projects/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

响应：

```json
[
  {
    "id": 1,
    "name": "我的第一个项目",
    "description": "这是一个测试项目",
    "owner": 1,
    "collaborators": [],
    "created_at": "2024-03-31T10:30:00Z",
    "updated_at": "2024-03-31T10:30:00Z",
    "is_public": false,
    "status": "planning"
  }
]
```

### 2.3 更新项目信息

```http
PUT /api/projects/1/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
Content-Type: application/json

{
    "name": "更新后的项目名称",
    "description": "更新后的项目描述",
    "status": "in_progress"
}
```

响应：

```json
{
  "id": 1,
  "name": "更新后的项目名称",
  "description": "更新后的项目描述",
  "owner": 1,
  "collaborators": [],
  "created_at": "2024-03-31T10:30:00Z",
  "updated_at": "2024-03-31T10:35:00Z",
  "is_public": false,
  "status": "in_progress"
}
```

### 2.4 添加项目协作者

```http
POST /api/projects/1/add_collaborator/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
Content-Type: application/json

{
    "user_id": 2
}
```

响应：

```json
{
  "id": 1,
  "name": "更新后的项目名称",
  "description": "更新后的项目描述",
  "owner": 1,
  "collaborators": [2],
  "created_at": "2024-03-31T10:30:00Z",
  "updated_at": "2024-03-31T10:40:00Z",
  "is_public": false,
  "status": "in_progress"
}
```

### 2.5 移除项目协作者

```http
POST /api/projects/1/remove_collaborator/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
Content-Type: application/json

{
    "user_id": 2
}
```

响应：

```json
{
  "id": 1,
  "name": "更新后的项目名称",
  "description": "更新后的项目描述",
  "owner": 1,
  "collaborators": [],
  "created_at": "2024-03-31T10:30:00Z",
  "updated_at": "2024-03-31T10:45:00Z",
  "is_public": false,
  "status": "in_progress"
}
```

### 2.6 删除项目

```http
DELETE /api/projects/1/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

响应：

```http
HTTP/1.1 204 No Content
```

## 3. 错误处理示例

### 3.1 未认证访问

```http
GET /api/projects/
```

响应：

```json
{
  "detail": "认证信息未提供。"
}
```

### 3.2 权限不足

```http
DELETE /api/projects/1/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

响应：

```json
{
  "detail": "您没有执行该操作的权限。"
}
```

### 3.3 资源不存在

```http
GET /api/projects/999/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

响应：

```json
{
  "detail": "未找到。"
}
```

## 4. 令牌刷新流程

### 4.1 刷新访问令牌

```http
POST /api/token/refresh/
Content-Type: application/json

{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

响应：

```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```
