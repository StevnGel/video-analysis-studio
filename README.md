# 视频分析工作台

视频分析工作台是一个功能强大的视频分析系统，支持视频源管理、模型管理、任务管理、事件处理和配置管理等核心功能。

## 项目结构

```
video-analysis-studio/
├── plans/             # 项目设计和规划文档
├── specs/             # 技术规范文档
├── ui/                # UI 交互设计规划
├── frontend/          # 前端代码
├── backend/           # 后端代码
├── docker/            # Docker 配置
├── tests/             # 测试代码
├── examples/          # 示例代码
└── README.md          # 项目说明
```

## 技术栈

### 前端
- **语言**: TypeScript
- **框架**: React 18+
- **构建工具**: Vite
- **状态管理**: React Context + useReducer
- **路由**: React Router
- **UI 组件库**: Ant Design
- **HTTP 客户端**: Axios
- **Supabase 客户端**: @supabase/supabase-js

### 后端
- **语言**: Python 3.9+
- **Web 框架**: FastAPI
- **视频处理**: GStreamer
- **数据存储**: Supabase (PostgreSQL)
- **认证**: Supabase Auth
- **并发处理**: Python threading

## 核心功能

1. **视频源管理**: 支持文件和流视频源的管理
2. **模型管理**: 支持本地和外部 API 模型的管理
3. **任务管理**: 支持任务的创建、启停、删除和查看
4. **事件管理**: 支持事件的生成、分类、处理和查询
5. **配置管理**: 支持规则配置、场景配置和风险等级配置

## UI 交互设计

为确保前后端功能实现的一致性和用户体验的连贯性，本项目在开发过程中采用前后端并行规划的策略：

- **设计先行**: 在实现具体功能前后端逻辑前，先在 `ui/` 目录规划 UI 交互设计，包括页面布局、组件状态、用户操作流程等
- **前后端对齐**: UI 设计文档作为前后端开发的共同依据，确保 API 接口设计符合 UI 交互需求
- **目录结构**: `ui/` 目录包含各功能模块的交互设计文档，采用 Markdown 格式便于协作和版本管理

## 快速开始

### 后端服务

1. 安装依赖

```bash
cd backend
pip install -r requirements.txt
```

2. 配置环境变量

创建 `.env` 文件，添加以下内容：

```
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
```

3. 启动服务

```bash
python main.py
```

### 前端服务

1. 安装依赖

```bash
cd frontend
npm install
```

2. 启动开发服务器

```bash
npm run dev
```

### Docker 部署

1. 构建 Docker 镜像

```bash
docker build -f docker/Dockerfile -t video-analysis-studio-backend .
```

2. 运行 Docker 容器

```bash
docker run -d \
  --name video-analysis-backend \
  -p 8000:8000 \
  -e SUPABASE_URL=your_supabase_url \
  -e SUPABASE_KEY=your_supabase_key \
  video-analysis-studio-backend
```

## 开发规范

### 前端开发规范
- 使用 TypeScript 严格模式
- 遵循 React 最佳实践
- 组件化开发
- 代码风格统一 (ESLint + Prettier)
- 响应式设计

### 后端开发规范
- 使用 Python 3.9+
- 遵循 PEP 8 代码风格
- 使用 FastAPI 最佳实践
- 模块化设计
- 错误处理和日志记录

## 测试

### 前端测试
- 组件测试 (Jest + React Testing Library)
- 集成测试 (Cypress)

### 后端测试
- 单元测试 (pytest)
- API 测试 (FastAPI TestClient)
- 集成测试

## 文档

- **项目计划**: `plans/` 目录
- **技术规范**: `specs/` 目录
- **API 文档**: 启动后端服务后访问 `/docs`

## 许可证

MIT
