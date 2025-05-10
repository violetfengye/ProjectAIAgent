# ProjectAIAgent

## 项目简介

ProjectAIAgent 是一个基于人工智能的软件工程辅助平台，旨在通过 AI 技术提升软件开发全生命周期的效率和质量。该平台集成了需求分析、架构设计、代码生成、测试管理、部署管理等多个功能模块，为开发团队提供全方位的智能化支持。

## 技术架构

- 前端：Vue 3 + TypeScript + Ant Design Vue
- 后端：Django + Python
- AI 集成：OpenAI API

## 主要功能

1. **需求管理**

   - AI 辅助需求分析
   - 需求文档自动生成
   - 需求优先级智能评估

2. **架构设计**

   - 系统架构智能推荐
   - 数据库设计方案生成
   - 技术栈选型建议

3. **代码生成**

   - 基于需求的代码自动生成
   - 代码优化建议
   - 代码质量分析

4. **测试管理**

   - 自动化测试用例生成
   - 测试任务管理
   - 测试报告生成

5. **部署管理**
   - 自动化部署流程
   - 部署环境配置
   - 系统运行状态监控

## 项目结构

```
ProjectAIAgent/
├── Front/                # 前端项目
│   ├── src/             # 源代码
│   │   ├── api/        # API接口
│   │   ├── views/      # 页面组件
│   │   └── utils/      # 工具函数
│   └── package.json    # 依赖配置
└── Server/              # 后端项目
    ├── ai/             # AI相关功能
    ├── projects/       # 项目管理
    ├── users/          # 用户管理
    └── core/           # 核心功能
```

## 开发环境要求

- Node.js >= 16
- Python >= 3.8
- OpenAI API Key

## 快速开始

1. 克隆项目
2. 安装前端依赖：`cd Front && npm install`
3. 安装后端依赖：`cd Server && pip install -r requirements.txt`
4. 配置环境变量：复制`.env.example`为`.env`并填写配置
5. 启动开发服务器：
   - 前端：`cd Front && npm run dev`
   - 后端：`cd Server && python manage.py runserver`

## 贡献指南

欢迎提交 Issue 和 Pull Request 来帮助改进项目。

## 许可证

MIT License
