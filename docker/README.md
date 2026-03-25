# Docker 配置说明

本目录包含视频分析工作台的 Docker 配置文件，用于构建和运行后端服务。

## 构建 Docker 镜像

在项目根目录执行以下命令构建 Docker 镜像：

```bash
docker build -f docker/Dockerfile -t video-analysis-studio-backend .
```

## 运行 Docker 容器

构建完成后，使用以下命令运行 Docker 容器：

```bash
docker run -d \
  --name video-analysis-backend \
  -p 8000:8000 \
  -e SUPABASE_URL=your_supabase_url \
  -e SUPABASE_KEY=your_supabase_key \
  video-analysis-studio-backend
```

其中：
- `SUPABASE_URL`：Supabase 项目的 URL
- `SUPABASE_KEY`：Supabase 项目的 API 密钥

## 环境变量

后端服务支持以下环境变量：

| 环境变量 | 描述 | 默认值 |
|---------|------|-------|
| SUPABASE_URL | Supabase 项目 URL | 无（必填） |
| SUPABASE_KEY | Supabase 项目 API 密钥 | 无（必填） |
| HOST | 服务器主机 | 0.0.0.0 |
| PORT | 服务器端口 | 8000 |
| DEBUG | 是否开启调试模式 | True |
| THREAD_POOL_SIZE | 线程池大小 | 4 |
| GST_BUFFER_SIZE | GStreamer 缓冲区大小 | 1024 |
| GST_FRAME_RATE | GStreamer 帧率 | 30 |

## 查看日志

使用以下命令查看容器日志：

```bash
docker logs video-analysis-backend
```

## 停止和删除容器

```bash
# 停止容器
docker stop video-analysis-backend

# 删除容器
docker rm video-analysis-backend
```
