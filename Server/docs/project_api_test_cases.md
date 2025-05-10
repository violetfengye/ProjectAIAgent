# 项目 API 测试用例文档

本文档包含了项目管理模块的所有 API 端点的测试用例。

## 目录

- [1. 项目创建测试](#1-项目创建测试)
- [2. 项目列表测试](#2-项目列表测试)
- [3. 项目详情测试](#3-项目详情测试)
- [4. 项目更新测试](#4-项目更新测试)
- [5. 项目删除测试](#5-项目删除测试)
- [6. 协作者管理测试](#6-协作者管理测试)

## 1. 项目创建测试

### 1.1 正常创建项目

- **请求方法**: POST
- **URL**: `http://localhost:8000/api/projects/`
- **请求头**:
  ```
  Authorization: Bearer 你的access令牌
  Content-Type: application/json
  ```
- **请求体**:
  ```json
  {
    "name": "测试项目",
    "description": "这是一个测试项目",
    "is_public": false,
    "status": "planning"
  }
  ```
- **预期响应**: 201 Created
- **响应体示例**:
  ```json
  {
    "id": 1,
    "name": "测试项目",
    "description": "这是一个测试项目",
    "owner": {
      "id": 1,
      "username": "testuser",
      "email": "test@example.com",
      "avatar": null
    },
    "collaborators": [],
    "created_at": "2024-03-21T10:00:00Z",
    "updated_at": "2024-03-21T10:00:00Z",
    "is_public": false,
    "status": "planning"
  }
  ```

### 1.2 缺少必需字段

- **请求方法**: POST
- **URL**: `http://localhost:8000/api/projects/`
- **请求头**:
  ```
  Authorization: Bearer 你的access令牌
  Content-Type: application/json
  ```
- **请求体**:
  ```json
  {
    "description": "这是一个测试项目"
  }
  ```
- **预期响应**: 400 Bad Request
- **响应体示例**:
  ```json
  {
    "name": ["该字段是必填项。"]
  }
  ```

## 2. 项目列表测试

### 2.1 获取项目列表

- **请求方法**: GET
- **URL**: `http://localhost:8000/api/projects/`
- **请求头**:
  ```
  Authorization: Bearer 你的access令牌
  ```
- **预期响应**: 200 OK
- **响应体示例**:
  ```json
  {
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
      {
        "id": 1,
        "name": "测试项目",
        "description": "这是一个测试项目",
        "owner": {
          "id": 1,
          "username": "testuser",
          "email": "test@example.com",
          "avatar": null
        },
        "collaborators": [],
        "created_at": "2024-03-21T10:00:00Z",
        "updated_at": "2024-03-21T10:00:00Z",
        "is_public": false,
        "status": "planning"
      }
    ]
  }
  ```

## 3. 项目详情测试

### 3.1 获取项目详情

- **请求方法**: GET
- **URL**: `http://localhost:8000/api/projects/1/`
- **请求头**:
  ```
  Authorization: Bearer 你的access令牌
  ```
- **预期响应**: 200 OK
- **响应体示例**:
  ```json
  {
    "id": 1,
    "name": "测试项目",
    "description": "这是一个测试项目",
    "owner": {
      "id": 1,
      "username": "testuser",
      "email": "test@example.com",
      "avatar": null
    },
    "collaborators": [],
    "created_at": "2024-03-21T10:00:00Z",
    "updated_at": "2024-03-21T10:00:00Z",
    "is_public": false,
    "status": "planning"
  }
  ```

### 3.2 获取不存在的项目

- **请求方法**: GET
- **URL**: `http://localhost:8000/api/projects/999/`
- **请求头**:
  ```
  Authorization: Bearer 你的access令牌
  ```
- **预期响应**: 404 Not Found

## 4. 项目更新测试

### 4.1 更新项目信息

- **请求方法**: POST
- **URL**: `http://localhost:8000/api/projects/1/`
- **请求头**:
  ```
  Authorization: Bearer 你的access令牌
  Content-Type: application/json
  ```
- **请求体**:
  ```json
  {
    "name": "更新后的项目名称",
    "description": "更新后的项目描述",
    "status": "in_progress"
  }
  ```
- **预期响应**: 200 OK
- **响应体示例**:
  ```json
  {
    "id": 1,
    "name": "更新后的项目名称",
    "description": "更新后的项目描述",
    "owner": {
      "id": 1,
      "username": "testuser",
      "email": "test@example.com",
      "avatar": null
    },
    "collaborators": [],
    "created_at": "2024-03-21T10:00:00Z",
    "updated_at": "2024-03-21T10:30:00Z",
    "is_public": false,
    "status": "in_progress"
  }
  ```

## 5. 项目删除测试

### 5.1 删除项目

- **请求方法**: POST
- **URL**: `http://localhost:8000/api/projects/1/`
- **请求头**:
  ```
  Authorization: Bearer 你的access令牌
  Content-Type: application/json
  ```
- **请求体**:
  ```json
  {
    "action": "delete"
  }
  ```
- **预期响应**: 204 No Content

## 6. 协作者管理测试

### 6.1 添加协作者

- **请求方法**: POST
- **URL**: `http://localhost:8000/api/projects/1/add_collaborator/`
- **请求头**:
  ```
  Authorization: Bearer 你的access令牌
  Content-Type: application/json
  ```
- **请求体**:
  ```json
  {
    "user_id": 2
  }
  ```
- **预期响应**: 200 OK
- **响应体示例**:
  ```json
  {
    "id": 1,
    "name": "测试项目",
    "description": "这是一个测试项目",
    "owner": {
      "id": 1,
      "username": "testuser",
      "email": "test@example.com",
      "avatar": null
    },
    "collaborators": [
      {
        "id": 2,
        "username": "collaborator",
        "email": "collaborator@example.com",
        "avatar": null
      }
    ],
    "created_at": "2024-03-21T10:00:00Z",
    "updated_at": "2024-03-21T10:00:00Z",
    "is_public": false,
    "status": "planning"
  }
  ```

### 6.2 移除协作者

- **请求方法**: POST
- **URL**: `http://localhost:8000/api/projects/1/remove_collaborator/`
- **请求头**:
  ```
  Authorization: Bearer 你的access令牌
  Content-Type: application/json
  ```
- **请求体**:
  ```json
  {
    "user_id": 2
  }
  ```
- **预期响应**: 200 OK
- **响应体示例**:
  ```json
  {
    "id": 1,
    "name": "测试项目",
    "description": "这是一个测试项目",
    "owner": {
      "id": 1,
      "username": "testuser",
      "email": "test@example.com",
      "avatar": null
    },
    "collaborators": [],
    "created_at": "2024-03-21T10:00:00Z",
    "updated_at": "2024-03-21T10:00:00Z",
    "is_public": false,
    "status": "planning"
  }
  ```

## 测试步骤建议

1. 首先测试项目创建功能
2. 然后测试获取项目列表和详情
3. 测试更新项目信息
4. 测试协作者管理功能
5. 最后测试删除项目功能

## 注意事项

1. 确保服务器已经启动并运行在`localhost:8000`
2. 在测试需要认证的接口时，请将`你的access令牌`替换为实际获取到的令牌
3. 建议按照上述顺序进行测试，因为某些测试可能依赖于前面测试的结果
4. 在测试协作者管理功能时，需要先创建另一个用户作为协作者
5. 只有项目所有者才能更新项目信息和管理协作者
