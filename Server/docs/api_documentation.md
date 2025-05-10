# API 文档

## 1. 认证相关 API

### 1.1 用户注册

- **URL**: `/api/users/`
- **方法**: `POST`
- **描述**: 注册新用户
- **请求体**:

```json
{
  "username": "string",
  "email": "string",
  "password": "string"
}
```

- **响应**:

```json
{
  "id": "integer",
  "username": "string",
  "email": "string",
  "avatar": "string",
  "bio": "string",
  "date_joined": "datetime"
}
```

### 1.2 用户登录

- **URL**: `/api/token/`
- **方法**: `POST`
- **描述**: 获取 JWT 令牌
- **请求体**:

```json
{
  "username": "string",
  "password": "string"
}
```

- **响应**:

```json
{
  "access": "string",
  "refresh": "string"
}
```

### 1.3 获取用户信息

- **URL**: `/api/users/me/`
- **方法**: `GET`
- **描述**: 获取当前用户信息
- **请求头**: `Authorization: Bearer <token>`
- **响应**: 同注册响应

### 1.4 更新用户信息

- **URL**: `/api/users/update_profile/`
- **方法**: `POST`
- **描述**: 更新用户个人信息
- **请求头**: `Authorization: Bearer <token>`
- **请求体**:

```json
{
  "avatar": "string",
  "bio": "string"
}
```

- **响应**: 同注册响应

### 1.5 用户登出

- **URL**: `/api/users/logout/`
- **方法**: `POST`
- **描述**: 注销用户
- **请求头**: `Authorization: Bearer <token>`
- **请求体**:

```json
{
  "refresh": "string"
}
```

- **响应**: 204 No Content

## 2. 项目管理 API

### 2.1 获取项目列表

- **URL**: `/api/projects/`
- **方法**: `GET`
- **描述**: 获取用户可见的项目列表
- **请求头**: `Authorization: Bearer <token>`
- **响应**:

```json
[
  {
    "id": "integer",
    "name": "string",
    "description": "string",
    "owner": "integer",
    "collaborators": ["integer"],
    "created_at": "datetime",
    "updated_at": "datetime",
    "is_public": "boolean",
    "status": "string"
  }
]
```

### 2.2 创建项目

- **URL**: `/api/projects/`
- **方法**: `POST`
- **描述**: 创建新项目
- **请求头**: `Authorization: Bearer <token>`
- **请求体**:

```json
{
  "name": "string",
  "description": "string",
  "is_public": "boolean",
  "status": "string"
}
```

- **响应**: 同项目列表响应中的单个项目

### 2.3 获取项目详情

- **URL**: `/api/projects/{id}/`
- **方法**: `GET`
- **描述**: 获取特定项目的详细信息
- **请求头**: `Authorization: Bearer <token>`
- **响应**: 同项目列表响应中的单个项目

### 2.4 更新项目

- **URL**: `/api/projects/{id}/`
- **方法**: `PUT`
- **描述**: 更新项目信息
- **请求头**: `Authorization: Bearer <token>`
- **请求体**: 同创建项目
- **响应**: 同项目列表响应中的单个项目

### 2.5 删除项目

- **URL**: `/api/projects/{id}/`
- **方法**: `DELETE`
- **描述**: 删除项目
- **请求头**: `Authorization: Bearer <token>`
- **响应**: 204 No Content

### 2.6 添加协作者

- **URL**: `/api/projects/{id}/add_collaborator/`
- **方法**: `POST`
- **描述**: 添加项目协作者
- **请求头**: `Authorization: Bearer <token>`
- **请求体**:

```json
{
  "user_id": "integer"
}
```

- **响应**: 同项目列表响应中的单个项目

### 2.7 移除协作者

- **URL**: `/api/projects/{id}/remove_collaborator/`
- **方法**: `POST`
- **描述**: 移除项目协作者
- **请求头**: `Authorization: Bearer <token>`
- **请求体**:

```json
{
  "user_id": "integer"
}
```

- **响应**: 同项目列表响应中的单个项目

## 3. API 调用流程

### 3.1 用户认证流程

1. 用户注册 (`POST /api/users/`)
2. 用户登录获取令牌 (`POST /api/token/`)
3. 使用令牌访问受保护的 API

### 3.2 项目管理流程

1. 创建项目 (`POST /api/projects/`)
2. 获取项目列表 (`GET /api/projects/`)
3. 查看项目详情 (`GET /api/projects/{id}/`)
4. 更新项目信息 (`PUT /api/projects/{id}/`)
5. 管理项目协作者
   - 添加协作者 (`POST /api/projects/{id}/add_collaborator/`)
   - 移除协作者 (`POST /api/projects/{id}/remove_collaborator/`)
6. 删除项目 (`DELETE /api/projects/{id}/`)

### 3.3 错误处理

所有 API 在发生错误时会返回以下格式的响应：

```json
{
  "detail": "错误描述信息"
}
```

常见 HTTP 状态码：

- 200: 请求成功
- 201: 创建成功
- 204: 删除成功
- 400: 请求参数错误
- 401: 未认证
- 403: 权限不足
- 404: 资源不存在
- 500: 服务器内部错误

### 3.4 认证要求

除了注册和登录 API，其他所有 API 都需要在请求头中包含 JWT 令牌：

```
Authorization: Bearer <access_token>
```

令牌过期后，使用 refresh_token 获取新的 access_token：

```
POST /api/token/refresh/
{
    "refresh": "<refresh_token>"
}
```
