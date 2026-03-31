# 视频分析工作台 API 约定文档 v1.0

## 文档概述

本文档定义视频分析工作台的核心API约定，包括视频上传、任务创建和推理接口。API采用RESTful风格，基于FastAPI实现，遵循JSON标准交互格式。

---

## 1. 通用约定

### 1.1 API 版本

所有API均采用URL路径版本控制，当前版本为 `v1`：

```
/api/v1/{resource}/{action}
```

### 1.2 设计理念

**任务与推理的解耦设计**：

1. **任务 (Task)**：表示一个视频处理作业，包含视频源、视频配置、输出配置。任务是视频链路的抽象，建立从输入到输出的完整通路。

2. **推理 (Inference)**：表示在任务链路上的模型推理操作。一个任务可以绑定多个推理会话，支持动态变更模型。

| 场景 | 说明 |
|------|------|
| 无模型任务 | 创建任务时不指定模型，仅建立视频转码链路，原样输出视频 |
| 单模型任务 | 创建任务时指定模型，链路包含推理，输出带检测框的视频 |
| 动态推理 | 任务创建后，通过推理接口动态绑定/切换模型，支持分段推理 |

### 1.3 请求头约定

| 请求头 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| Content-Type | string | 是 | 值为 `application/json` |
| Accept | string | 否 | 值为 `application/json` |
| X-Request-ID | string | 否 | 请求追踪ID |

### 1.3 响应格式约定

**成功响应：**

```json
{
  "code": 0,
  "message": "success",
  "data": { ... },
  "request_id": "req-xxx-xxx"
}
```

**错误响应：**

```json
{
  "code": 400,
  "message": "具体错误描述",
  "detail": { ... },
  "request_id": "req-xxx-xxx"
}
```

**状态码说明：**

| 状态码 | 说明 |
|--------|------|
| 0 | 成功 |
| 400 | 请求参数错误 |
| 404 | 资源不存在 |
| 409 | 资源冲突 |
| 422 | 业务逻辑错误 |
| 500 | 服务器内部错误 |

### 1.4 分页约定

列表类接口支持分页，通用参数：

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| page | int | 1 | 页码 |
| page_size | int | 20 | 每页数量 |

响应包含分页元数据：

```json
{
  "data": [...],
  "pagination": {
    "page": 1,
    "page_size": 20,
    "total": 100,
    "total_pages": 5
  }
}
```

---

## 2. 视频上传接口

### 2.1 上传视频文件

**接口信息：**

| 属性 | 值 |
|------|------|
| 方法 | POST |
| 路径 | `/api/v1/videos/upload` |
| Content-Type | multipart/form-data |
| 认证 | 否 |

**请求参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| file | binary | 是 | 视频文件（最大2GB） |
| name | string | 否 | 自定义视频名称，默认使用原文件名 |
| tags | array[string] | 否 | 视频标签，用于分类 |

**支持的视频格式：**

```
MP4, AVI, MOV, MKV, FLV, WMV, WebM
```

**请求示例：**

```bash
curl -X POST "http://localhost:8000/api/v1/videos/upload" \
  -H "Accept: application/json" \
  -F "file=@/path/to/video.mp4" \
  -F "name=测试视频" \
  -F "tags=[\"安防\", \"室内\"]"
```

**成功响应（201）：**

```json
{
  "code": 0,
  "message": "视频上传成功",
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "测试视频.mp4",
    "original_name": "video.mp4",
    "type": "file",
    "path": "/data/videos/550e8400-e29b-41d4-a716-446655440000.mp4",
    "size": 104857600,
    "duration": 120.5,
    "width": 1920,
    "height": 1080,
    "fps": 30.0,
    "codec": "h264",
    "status": "ready",
    "tags": ["安防", "室内"],
    "created_at": "2026-03-31T10:00:00Z",
    "updated_at": "2026-03-31T10:00:00Z"
  }
}
```

**错误响应：**

| 状态码 | 说明 | 示例 |
|--------|------|------|
| 400 | 文件为空 | `{"code": 400, "message": "文件不能为空"}` |
| 400 | 文件类型不支持 | `{"code": 400, "message": "不支持的视频格式: .exe"}` |
| 400 | 文件大小超限 | `{"code": 400, "message": "文件大小超过2GB限制"}` |
| 500 | 上传失败 | `{"code": 500, "message": "文件保存失败"}` |

### 2.2 获取视频列表

**接口信息：**

| 属性 | 值 |
|------|------|
| 方法 | GET |
| 路径 | `/api/v1/videos` |

**查询参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| page | int | 否 | 页码，默认1 |
| page_size | int | 否 | 每页数量，默认20 |
| status | string | 否 | 状态过滤：`ready`, `processing`, `deleted` |
| tags | string | 否 | 标签过滤（逗号分隔） |

**响应示例：**

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "videos": [
      {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "name": "测试视频.mp4",
        "type": "file",
        "size": 104857600,
        "duration": 120.5,
        "width": 1920,
        "height": 1080,
        "status": "ready",
        "created_at": "2026-03-31T10:00:00Z"
      }
    ],
    "pagination": {
      "page": 1,
      "page_size": 20,
      "total": 1,
      "total_pages": 1
    }
  }
}
```

### 2.3 获取视频详情

**接口信息：**

| 属性 | 值 |
|------|------|
| 方法 | GET |
| 路径 | `/api/v1/videos/{video_id}` |

**路径参数：**

| 参数 | 类型 | 说明 |
|------|------|------|
| video_id | string | 视频ID |

**响应示例：**

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "测试视频.mp4",
    "original_name": "video.mp4",
    "type": "file",
    "path": "/data/videos/550e8400-e29b-41d4-a716-446655440000.mp4",
    "size": 104857600,
    "duration": 120.5,
    "width": 1920,
    "height": 1080,
    "fps": 30.0,
    "codec": "h264",
    "status": "ready",
    "tags": ["安防"],
    "metadata": {
      "bitrate": "5000k",
      "audio_codec": "aac",
      "has_audio": true
    },
    "created_at": "2026-03-31T10:00:00Z",
    "updated_at": "2026-03-31T10:00:00Z"
  }
}
```

### 2.4 删除视频

**接口信息：**

| 属性 | 值 |
|------|------|
| 方法 | DELETE |
| 路径 | `/api/v1/videos/{video_id}` |

**路径参数：**

| 参数 | 类型 | 说明 |
|------|------|------|
| video_id | string | 视频ID |

**响应示例：**

```json
{
  "code": 0,
  "message": "视频删除成功",
  "data": {
    "deleted_id": "550e8400-e29b-41d4-a716-446655440000"
  }
}
```

### 2.5 视频数据结构

```typescript
interface VideoSource {
  id: string;                          // 视频源唯一标识 (UUID)
  name: string;                       // 视频显示名称
  original_name: string;              // 原始文件名
  type: "file" | "rtsp";              // 视频源类型
  path: string;                       // 文件路径或RTSP地址
  size: number;                       // 文件大小（字节）
  duration: number;                   // 时长（秒）
  width: number;                      // 视频宽度
  height: number;                     // 视频高度
  fps: number;                        // 帧率
  codec: string;                      // 视频编码
  status: "ready" | "processing" | "deleted";  // 状态
  tags?: string[];                    // 标签
  metadata?: {                        // 额外元数据
    bitrate?: string;
    audio_codec?: string;
    has_audio?: boolean;
  };
  created_at: string;                  // 创建时间 (ISO 8601)
  updated_at: string;                  // 更新时间 (ISO 8601)
}
```

---

## 3. 任务创建接口

### 3.1 创建分析任务

**接口信息：**

| 属性 | 值 |
|------|------|
| 方法 | POST |
| 路径 | `/api/v1/tasks` |
| Content-Type | application/json |

**请求参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| name | string | 是 | 任务名称 |
| task_type | string | 是 | 任务类型：`realtime`（实时）或 `offline`（离线） |
| input_config | object | 是 | 输入配置（包含视频源） |
| output_config | object | 是 | 输出配置 |
| model_config | object | 否 | 模型配置（支持多模型并行） |
| priority | int | 否 | 优先级，0-100，默认50 |

**参数结构说明：**

```typescript
interface TaskRequest {
  name: string;
  task_type: "realtime" | "offline";
  input_config: InputConfig;      // 输入配置（包含视频源）
  output_config: OutputConfig;    // 输出配置
  model_config?: ModelConfig;      // 模型配置（可选）
  priority?: number;
}

interface InputConfig {
  source: VideoSource;             // 视频源（本地或在线）
  resize?: {                       // resize 配置
    width: number;
    height: number;
    maintain_aspect?: boolean;
  };
  roi?: {                          // ROI 区域
    x1: number;
    y1: number;
    x2: number;
    y2: number;
  };
  skip_frames?: number;            // 跳帧数
  buffer_size?: number;            // 缓冲区大小
  decode_threads?: number;         // 解码线程数
}

interface VideoSource {
  type: "local" | "rtsp" | "http" | "https";  // 视频源类型
  id?: string;                    // 本地视频源ID（type=local时必填）
  url?: string;                   // 在线视频地址（type=rtsp/http/https时必填）
  auto_download?: boolean;        // 是否自动下载为本地MP4（在线源默认true）
  timeout?: number;               // 下载超时时间（秒）
}

interface OutputConfig {
  type: "file" | "rtmp" | "hls";  // 输出类型
  path?: string;                  // 输出目录（以任务ID命名）
  rtmp_url?: string;              // RTMP 推流地址
  hls_dir?: string;               // HLS 输出目录
  format?: {                      // 视频格式
    width?: number;
    height?: number;
    fps?: number;
    codec?: "h264" | "h265";
    bitrate?: string;
    gop_size?: number;
    profile?: string;
  };
}

interface ModelConfig {
  models: ModelItem[];              // 模型列表（支持多模型并行）
  parallel?: boolean;               // 是否并行推理，默认 true
}

interface ModelItem {
  name: string;                     // 模型名称
  config?: InferenceConfig;         // 推理配置（与推理接口一致）
  enabled: boolean;                 // 是否启用
  for_display?: boolean;           // 是否用于绘制展示
  draw_config?: DrawConfig;         // 绘制配置
}

interface DrawConfig {
  draw_bbox?: boolean;              // 绘制边界框
  draw_mask?: boolean;              // 绘制分割掩码
  draw_label?: boolean;             // 绘制标签
  draw_confidence?: boolean;        // 绘制置信度
  bbox_color?: string;              // 边界框颜色（十六进制）
  mask_alpha?: number;              // 掩码透明度 (0-1)
  line_thickness?: number;          // 线条厚度
  font_scale?: number;              // 字体大小
  label_prefix?: string;            // 标签前缀
  z_order?: number;                 // 绘制层级
}
```

**请求示例 - 本地视频源任务：**

```json
{
  "name": "视频转码任务",
  "task_type": "offline",
  "input_config": {
    "source": {
      "type": "local",
      "id": "550e8400-e29b-41d4-a716-446655440000"
    },
    "resize": {
      "width": 1920,
      "height": 1080
    }
  },
  "output_config": {
    "type": "file",
    "path": "/data/output"
  }
}
```

**请求示例 - 在线视频源任务（自动下载）：**

```json
{
  "name": "在线视频分析任务",
  "task_type": "offline",
  "input_config": {
    "source": {
      "type": "http",
      "url": "https://example.com/video.mp4",
      "auto_download": true,
      "timeout": 300
    },
    "resize": {
      "width": 1280,
      "height": 720
    },
    "skip_frames": 0
  },
  "output_config": {
    "type": "file",
    "path": "/data/output",
    "format": {
      "width": 1920,
      "height": 1080,
      "fps": 30,
      "codec": "h264",
      "bitrate": "4M"
    }
  }
}
```

**请求示例 - RTSP实时流任务：**

```json
{
  "name": "实时监控任务",
  "task_type": "realtime",
  "input_config": {
    "source": {
      "type": "rtsp",
      "url": "rtsp://192.168.1.100:554/stream",
      "auto_download": false
    },
    "buffer_size": 30
  },
  "output_config": {
    "type": "rtmp",
    "rtmp_url": "rtmp://localhost/live/output"
  }
}
```

**请求示例 - 单模型任务（带推理）：**

```json
{
  "name": "安防监控任务",
  "task_type": "offline",
  "input_config": {
    "source": {
      "type": "local",
      "id": "550e8400-e29b-41d4-a716-446655440000"
    },
    "resize": {
      "width": 640,
      "height": 640,
      "maintain_aspect": true
    },
    "skip_frames": 0
  },
  "output_config": {
    "type": "file",
    "path": "/data/output",
    "format": {
      "width": 1920,
      "height": 1080,
      "fps": 30,
      "codec": "h264",
      "bitrate": "4M"
    }
  },
  "model_config": {
    "parallel": true,
    "models": [
      {
        "name": "yolo_v8",
        "enabled": true,
        "for_display": true,
        "config": {
          "confidence_threshold": 0.5,
          "iou_threshold": 0.45,
          "device": "cuda:0"
        },
        "draw_config": {
          "draw_bbox": true,
          "draw_label": true,
          "draw_confidence": true,
          "bbox_color": "#00FF00",
          "line_thickness": 2,
          "label_prefix": "目标"
        }
      }
    ]
  }
}
```

**请求示例 - 多模型并行推理任务：**

```json
{
  "name": "交通分析任务",
  "task_type": "offline",
  "input_config": {
    "source": {
      "type": "local",
      "id": "550e8400-e29b-41d4-a716-446655440000"
    },
    "resize": {
      "width": 1280,
      "height": 720
    }
  },
  "output_config": {
    "type": "file",
    "path": "/data/output"
  },
  "model_config": {
    "parallel": true,
    "models": [
      {
        "name": "yolo_v8",
        "enabled": true,
        "for_display": true,
        "config": {
          "confidence_threshold": 0.5,
          "classes": [2, 3, 5, 7],
          "device": "cuda:0"
        },
        "draw_config": {
          "draw_bbox": true,
          "draw_label": true,
          "bbox_color": "#FF0000",
          "label_prefix": "车辆"
        }
      },
      {
        "name": "plate_recognition",
        "enabled": true,
        "for_display": true,
        "config": {
          "device": "cuda:0"
        },
        "draw_config": {
          "draw_label": true,
          "bbox_color": "#00FFFF",
          "label_prefix": "车牌"
        }
      },
      {
        "name": "pose_estimation",
        "enabled": true,
        "for_display": false,
        "config": {
          "device": "cuda:0"
        }
      }
    ]
  }
}
```
      "width": 1920,
      "height": 1080,
      "fps": 30,
      "codec": "h264",
      "bitrate": "4M"
    }
  },
  "priority": 50
}
```

**请求示例 - 多模型串联任务（模型链配置）：**

```

**成功响应（201）：**
}
```

**成功响应（201）：**

```json
{
  "code": 0,
  "message": "任务创建成功",
  "data": {
    "id": "task-xxx-xxx",
    "name": "安防监控任务",
    "task_type": "offline",
    "video_source_id": "550e8400-e29b-41d4-a716-446655440000",
    "model_name": "yolo_v8",
    "video_config": { ... },
    "output_config": { ... },
    "status": "pending",
    "progress": 0.0,
    "gpu_device": "cuda:0",
    "result_url": null,
    "created_at": "2026-03-31T10:00:00Z",
    "started_at": null,
    "completed_at": null,
    "error_message": null
  }
}
```

**错误响应：**

| 状态码 | 说明 | 示例 |
|--------|------|------|
| 400 | 参数缺失 | `{"code": 400, "message": "缺少必填参数: video_source_id"}` |
| 404 | 视频源不存在 | `{"code": 404, "message": "视频源不存在"}` |
| 404 | 模型不存在 | `{"code": 404, "message": "模型 yolo_v8 不存在"}` |
| 422 | 任务创建失败 | `{"code": 422, "message": "任务创建失败: 磁盘空间不足"}` |

### 3.2 成功响应
  format?: {
    width?: number;
    height?: number;
    fps?: number;
    codec?: "h264" | "h265";
    bitrate?: string;
    gop_size?: number;
    preset?: string;
    profile?: string;
  };
  draw_detection?: boolean;          // 是否在输出视频绘制检测框
  detection_options?: {
    show_labels: boolean;            // 显示类别标签
    show_confidence: boolean;        // 显示置信度
    line_thickness: number;          // 框线厚度
    font_scale: number;              // 字体大小
  };
}
```

### 3.4 预定义视频格式

| 预置名称 | 场景 | 描述 |
|----------|------|------|
| hd_1080p | 高清监控 | 1920x1080, 30fps, h264 4M |
| hd_720p | 流畅监控 | 1280x720, 25fps, h264 2M |
| industrial_high_precision | 工业质检 | 3840x2160, 30fps, h265 10M |
| traffic_plate | 交通分析 | 1920x1080, 30fps, h264 3M |

### 3.5 任务列表

**接口信息：**

| 属性 | 值 |
|------|------|
| 方法 | GET |
| 路径 | `/api/v1/tasks` |

**查询参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| page | int | 否 | 页码 |
| page_size | int | 否 | 每页数量 |
| status | string | 否 | 状态过滤 |
| task_type | string | 否 | 任务类型过滤 |

**响应示例：**

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "tasks": [
      {
        "id": "task-xxx-xxx",
        "name": "安防监控任务",
        "task_type": "offline",
        "video_source_id": "550e8400-...",
        "model_name": "yolo_v8",
        "status": "running",
        "progress": 45.5,
        "gpu_device": "cuda:0",
        "created_at": "2026-03-31T10:00:00Z"
      }
    ],
    "pagination": { ... }
  }
}
```

### 3.6 任务详情

**接口信息：**

| 属性 | 值 |
|------|------|
| 方法 | GET |
| 路径 | `/api/v1/tasks/{task_id}` |

**响应示例：**

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "id": "task-xxx-xxx",
    "name": "安防监控任务",
    "task_type": "offline",
    "video_source_id": "550e8400-...",
    "model_name": "yolo_v8",
    "video_config": { ... },
    "output_config": { ... },
    "status": "running",
    "progress": 45.5,
    "gpu_device": "cuda:0",
    "result_url": "/data/output/task-xxx-xxx.mp4",
    "created_at": "2026-03-31T10:00:00Z",
    "started_at": "2026-03-31T10:01:00Z",
    "completed_at": null,
    "error_message": null,
    "statistics": {
      "frames_processed": 1350,
      "frames_total": 3000,
      "detections_count": 256,
      "avg_fps": 28.5
    }
  }
}
```

### 3.7 任务数据结构

```typescript
interface AnalysisTask {
  id: string;                        // 任务唯一标识
  name: string;                     // 任务名称
  task_type: "realtime" | "offline"; // 任务类型
  video_source_id: string;          // 视频源ID
  input_config: InputConfig;       // 输入配置
  output_config: OutputConfig;      // 输出配置
  model_config?: ModelConfig;       // 模型配置（多模型并行）
  status: TaskStatus;               // 任务状态
  progress: number;                // 进度 (0-100)
  gpu_device?: string;              // 分配的GPU设备
  result_url?: string;              // 结果输出URL
  priority: number;                 // 优先级
  created_at: string;              // 创建时间
  started_at?: string;             // 开始时间
  completed_at?: string;           // 完成时间
  error_message?: string;           // 错误信息
  statistics?: TaskStatistics;     // 统计信息
}

interface TaskStatistics {
  frames_processed: number;
  frames_total: number;
  detections_count: number;
  avg_fps: number;
  model_results?: {                // 各模型统计
    [modelName: string]: {
      detections_count: number;
      avg_confidence: number;
    };
  };
}

type TaskStatus = 
  | "pending"      // 待执行（无模型任务）
  | "pending_with_inference"  // 待执行（带推理）
  | "queued"       // 排队中
  | "running"      // 运行中
  | "paused"       // 暂停
  | "completed"    // 已完成
  | "failed"       // 失败
  | "cancelled";   // 已取消
```

### 3.8 启动任务

**接口信息：**

| 属性 | 值 |
|------|------|
| 方法 | POST |
| 路径 | `/api/v1/tasks/{task_id}/start` |

**响应示例：**

```json
{
  "code": 0,
  "message": "任务已启动",
  "data": {
    "task_id": "task-xxx-xxx",
    "status": "running",
    "started_at": "2026-03-31T10:00:00Z"
  }
}
```

### 3.9 停止任务

**接口信息：**

| 属性 | 值 |
|------|------|
| 方法 | POST |
| 路径 | `/api/v1/tasks/{task_id}/stop` |

**响应示例：**

```json
{
  "code": 0,
  "message": "任务已停止",
  "data": {
    "task_id": "task-xxx-xxx",
    "status": "cancelled"
  }
}
```

### 3.10 删除任务

**接口信息：**

| 属性 | 值 |
|------|------|
| 方法 | DELETE |
| 路径 | `/api/v1/tasks/{task_id}` |

---

## 4. 推理接口

任务与推理解耦设计的核心是：推理会话独立于任务存在，可以动态绑定到任务上。

### 4.1 为任务绑定/切换模型（核心接口）

**接口信息：**

| 属性 | 值 |
|------|------|
| 方法 | POST |
| 路径 | `/api/v1/tasks/{task_id}/inference` |
| Content-Type | application/json |

**请求参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| model_config | object | 是 | 模型配置（支持多模型） |

**请求参数结构（与任务创建接口一致）：**

```typescript
interface BindInferenceRequest {
  model_config: ModelConfig;  // 与任务创建接口的 model_config 一致
}

interface ModelConfig {
  models: ModelItem[];       // 模型列表（支持多模型并行）
  parallel?: boolean;         // 是否并行推理，默认 true
}

interface ModelItem {
  name: string;               // 模型名称
  config?: InferenceConfig;   // 推理配置
  enabled: boolean;           // 是否启用
  for_display?: boolean;     // 是否用于绘制展示
  draw_config?: DrawConfig;   // 绘制配置
}

interface InferenceConfig {
  confidence_threshold?: number;
  iou_threshold?: number;
  max_det?: number;
  classes?: number[];
  device?: string;
  batch_size?: number;
  half_precision?: boolean;
  track_objects?: boolean;
}

interface DrawConfig {
  draw_bbox?: boolean;
  draw_mask?: boolean;
  draw_label?: boolean;
  draw_confidence?: boolean;
  bbox_color?: string;
  mask_alpha?: number;
  line_thickness?: number;
  font_scale?: number;
  label_prefix?: string;
  z_order?: number;
}
```

**请求示例 - 绑定单模型：**

```json
{
  "model_config": {
    "parallel": true,
    "models": [
      {
        "name": "yolo_v8",
        "enabled": true,
        "for_display": true,
        "config": {
          "confidence_threshold": 0.5,
          "device": "cuda:0"
        },
        "draw_config": {
          "draw_bbox": true,
          "draw_label": true,
          "bbox_color": "#00FF00"
        }
      }
    ]
  }
}
```

**请求示例 - 绑定多模型（并行推理）：**

```json
{
  "model_config": {
    "parallel": true,
    "models": [
      {
        "name": "yolo_v8",
        "enabled": true,
        "for_display": true,
        "config": {...},
        "draw_config": {...}
      },
      {
        "name": "sam3",
        "enabled": true,
        "for_display": true,
        "config": {...},
        "draw_config": {...}
      }
    ]
  }
}
```

**成功响应（202）：**

```json
{
  "code": 0,
  "message": "模型已绑定到任务",
  "data": {
    "inference_id": "inf-xxx-xxx",
    "task_id": "task-xxx-xxx",
    "model_config": {...},
    "status": "pending"
  }
}
```

### 4.2 推理会话列表

**接口信息：**

| 属性 | 值 |
|------|------|
| 方法 | GET |
| path | `/api/v1/tasks/{task_id}/inferences` |

**响应示例：**

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "inferences": [
      {
        "inference_id": "inf-001",
        "model_name": "yolo_v8",
        "status": "completed",
        "created_at": "2026-03-31T10:00:00Z",
        "completed_at": "2026-03-31T10:05:00Z",
        "frames_processed": 3000,
        "detections_count": 1250
      },
      {
        "inference_id": "inf-002",
        "model_name": "sam3",
        "status": "running",
        "created_at": "2026-03-31T10:06:00Z",
        "progress": 45.0
      }
    ]
  }
}
```

### 4.3 推理状态查询

**接口信息：**

| 属性 | 值 |
|------|------|
| 方法 | GET |
| 路径 | `/api/v1/inferences/{inference_id}` |

**响应示例：**

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "inference_id": "inf-xxx-xxx",
    "task_id": "task-xxx-xxx",
    "model_name": "yolo_v8",
    "status": "completed",
    "progress": 100,
    "results": {
      "frames": [
        {
          "frame_index": 0,
          "timestamp": 0.0,
          "detections": [
            {
              "class_id": 0,
              "class_name": "person",
              "confidence": 0.92,
              "bbox": [100, 200, 150, 350],
              "tracking_id": 1
            }
          ]
        }
      ],
      "summary": {
        "total_frames": 3000,
        "total_detections": 1250,
        "avg_fps": 28.5
      }
    },
    "result_url": "/data/output/inf-xxx-xxx_result.mp4",
    "created_at": "2026-03-31T10:00:00Z",
    "completed_at": "2026-03-31T10:05:00Z"
  }
}
```

### 4.4 推理配置参数

```typescript
interface InferenceConfig {
  confidence_threshold?: number;     // 置信度阈值 (0-1)，默认 0.25
  iou_threshold?: number;           // IoU 阈值 (0-1)，默认 0.45
  max_det?: number;                  // 最大检测数，默认 300
  classes?: number[];               // 目标类别过滤
  device?: string;                  // 设备选择，如 "cuda:0", "cuda:1", "cpu"
  batch_size?: number;              // 批处理大小
  half_precision?: boolean;         // 半精度推理
  track_objects?: boolean;          // 是否启用目标跟踪
  output_format?: "json" | "bbox" | "video";
}
```

### 4.5 推理结果数据结构

```typescript
interface InferenceResult {
  inference_id: string;
  task_id: string;
  model_name: string;
  status: "pending" | "processing" | "completed" | "failed";
  progress: number;
  results?: {
    frames: FrameResult[];
    summary: InferenceSummary;
  };
  result_url?: string;
  error_message?: string;
  created_at: string;
  completed_at?: string;
}

interface FrameResult {
  frame_index: number;
  timestamp: number;
  detections: Detection[];
}

interface Detection {
  class_id: number;
  class_name: string;
  confidence: number;
  bbox: [number, number, number, number];  // [x1, y1, x2, y2]
  tracking_id?: number;
}

interface InferenceSummary {
  total_frames: number;
  total_detections: number;
  avg_fps: number;
}
```

### 4.6 实时推理流

**接口信息：**

| 属性 | 值 |
|------|------|
| 方法 | GET |
| 路径 | `/api/v1/tasks/{task_id}/inference/stream` |

**说明：** 返回 SSE（Server-Sent Events）流式推送推理状态

**事件类型：**

| 事件 | 说明 |
|------|------|
| start | 推理开始 |
| progress | 进度更新 |
| detection | 检测结果 |
| error | 错误信息 |
| complete | 推理完成 |

### 4.7 停止/取消推理

**接口信息：**

| 属性 | 值 |
|------|------|
| 方法 | POST |
| 路径 | `/api/v1/inferences/{inference_id}/stop` |

**响应示例：**

```json
{
  "code": 0,
  "message": "推理已停止",
  "data": {
    "inference_id": "inf-xxx-xxx",
    "status": "cancelled"
  }
}
```

### 4.8 删除推理会话

**接口信息：**

| 属性 | 值 |
|------|------|
| 方法 | DELETE |
| 路径 | `/api/v1/inferences/{inference_id}` |

**说明：** 删除推理会话记录，不影响任务本身

---

## 5. 典型使用场景

### 场景1：仅转码（无模型）

```bash
# 1. 创建无模型任务
curl -X POST "http://localhost:8000/api/v1/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "视频转码任务",
    "task_type": "offline",
    "video_source_id": "550e8400-...",
    "video_config": {"preset": "hd_1080p"},
    "output_config": {"type": "file", "path": "/data/output"}
  }'

# 2. 启动任务
curl -X POST "http://localhost:8000/api/v1/tasks/task-xxx/start"

# 3. 获取输出
curl -X GET "http://localhost:8000/api/v1/tasks/task-xxx/output"
```

### 场景2：创建任务时指定模型

```bash
# 创建任务时直接绑定模型
curl -X POST "http://localhost:8000/api/v1/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "安防监控任务",
    "task_type": "offline",
    "video_source_id": "550e8400-...",
    "model_name": "yolo_v8",
    "video_config": {"preset": "hd_1080p"},
    "output_config": {"type": "file", "path": "/data/output"}
  }'
```

### 场景3：先创建任务，后动态绑定模型

```bash
# 1. 创建无模型任务
curl -X POST "http://localhost:8000/api/v1/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "视频分析任务",
    "task_type": "offline",
    "video_source_id": "550e8400-...",
    "video_config": {"preset": "hd_1080p"},
    "output_config": {"type": "file", "path": "/data/output"}
  }'

# 2. 启动任务（此时为无模型，仅转码）
curl -X POST "http://localhost:8000/api/v1/tasks/task-xxx/start"

# 3. 运行时动态绑定YOLO模型
curl -X POST "http://localhost:8000/api/v1/tasks/task-xxx/inference" \
  -H "Content-Type: application/json" \
  -d '{
    "model_name": "yolo_v8",
    "config": {"confidence_threshold": 0.5},
    "mode": "replace"
  }'

# 4. 运行中切换为SAM3模型（追加模式）
curl -X POST "http://localhost:8000/api/v1/tasks/task-xxx/inference" \
  -H "Content-Type: application/json" \
  -d '{
    "model_name": "sam3",
    "mode": "append"
  }'
```

### 场景4：多模型串联推理

```bash
# 为任务绑定多个模型（串联推理）
curl -X POST "http://localhost:8000/api/v1/tasks/task-xxx/inference" \
  -H "Content-Type: application/json" \
  -d '{
    "model_name": "yolo_v8",
    "mode": "replace"
  }'

# 追加SAM3进行实例分割
curl -X POST "http://localhost:8000/api/v1/tasks/task-xxx/inference" \
  -H "Content-Type: application/json" \
  -d '{
    "model_name": "sam3",
    "mode": "append"
  }'

# 查询所有推理会话
curl -X GET "http://localhost:8000/api/v1/tasks/task-xxx/inferences"
```

---

## 6. 错误码定义

| 错误码 | 错误信息 | HTTP状态码 | 说明 |
|--------|----------|------------|------|
| 0 | success | 200 | 成功 |
| 1001 | VIDEO_NOT_FOUND | 404 | 视频不存在 |
| 1002 | VIDEO_UPLOAD_FAILED | 500 | 视频上传失败 |
| 1003 | VIDEO_DELETE_FAILED | 500 | 视频删除失败 |
| 1004 | VIDEO_FORMAT_UNSUPPORTED | 400 | 不支持的视频格式 |
| 1005 | VIDEO_SIZE_EXCEEDED | 400 | 文件大小超限 |
| 2001 | TASK_NOT_FOUND | 404 | 任务不存在 |
| 2002 | TASK_CREATE_FAILED | 422 | 任务创建失败 |
| 2003 | TASK_START_FAILED | 422 | 任务启动失败 |
| 2004 | TASK_STOP_FAILED | 422 | 任务停止失败 |
| 2005 | TASK_STATUS_INVALID | 400 | 任务状态无效 |
| 3001 | MODEL_NOT_FOUND | 404 | 模型不存在 |
| 3002 | MODEL_LOAD_FAILED | 500 | 模型加载失败 |
| 3003 | MODEL_INSTANCE_UNAVAILABLE | 503 | 模型实例不可用 |
| 4001 | INFERENCE_FAILED | 500 | 推理执行失败 |
| 4002 | INFERENCE_TIMEOUT | 504 | 推理超时 |
| 4003 | INFERENCE_NOT_FOUND | 404 | 推理会话不存在 |
| 5001 | GPU_UNAVAILABLE | 503 | GPU资源不可用 |
| 5002 | GPU_MEMORY_EXHAUSTED | 507 | GPU内存不足 |
| 9999 | INTERNAL_ERROR | 500 | 内部错误 |

---

## 7. 附录

### 7.1 支持的视频格式详情

| 格式 | 扩展名 | 编码支持 | 最大分辨率 | 最大帧率 |
|------|--------|----------|------------|----------|
| MP4 | .mp4 | h264, h265, vp9 | 8K | 120fps |
| AVI | .avi | h264, mpeg4 | 4K | 60fps |
| MOV | .mov | h264, h265, prores | 8K | 120fps |
| MKV | .mkv | h264, h265, vp9 | 8K | 120fps |
| FLV | .flv | h264 | 1080P | 30fps |
| WMV | .wmv | wmv2 | 1080P | 30fps |

### 7.2 模型配置

| 模型名称 | 类型 | 输入尺寸 | 推荐场景 |
|----------|------|----------|----------|
| yolo_v8n | YOLOv8 Nano | 640x640 | 低延迟场景 |
| yolo_v8s | YOLOv8 Small | 640x640 | 通用场景 |
| yolo_v8m | YOLOv8 Medium | 640x640 | 高精度场景 |
| yolo_v8l | YOLOv8 Large | 640x640 | 超高精度 |
| yolo_v8x | YOLOv8 XLarge | 640x640 | 极致精度 |

---

**文档版本**: v1.0  
**创建日期**: 2026-03-31  
**最后更新**: 2026-03-31

# 2. 获取视频ID
# 响应: {"data": {"id": "550e8400-e29b-41d4-a716-446655440000"}}

# 3. 创建任务
curl -X POST "http://localhost:8000/api/v1/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "测试任务",
    "task_type": "offline",
    "video_source_id": "550e8400-e29b-41d4-a716-446655440000",
    "model_name": "yolo_v8",
    "video_config": {
      "preset": "hd_1080p"
    },
    "output_config": {
      "type": "file",
      "path": "/data/output"
    }
  }'

# 4. 启动任务
curl -X POST "http://localhost:8000/api/v1/tasks/task-xxx/start"

# 5. 查询任务状态
curl -X GET "http://localhost:8000/api/v1/tasks/task-xxx"

# 6. 获取结果
curl -X GET "http://localhost:8000/api/v1/tasks/task-xxx/output"
```

---

## 7. 附录

### 7.1 支持的视频格式详情

| 格式 | 扩展名 | 编码支持 | 最大分辨率 | 最大帧率 |
|------|--------|----------|------------|----------|
| MP4 | .mp4 | h264, h265, vp9 | 8K | 120fps |
| AVI | .avi | h264, mpeg4 | 4K | 60fps |
| MOV | .mov | h264, h265, prores | 8K | 120fps |
| MKV | .mkv | h264, h265, vp9 | 8K | 120fps |
| FLV | .flv | h264 | 1080P | 30fps |
| WMV | .wmv | wmv2 | 1080P | 30fps |

### 7.2 模型配置

| 模型名称 | 类型 | 输入尺寸 | 推荐场景 |
|----------|------|----------|----------|
| yolo_v8n | YOLOv8 Nano | 640x640 | 低延迟场景 |
| yolo_v8s | YOLOv8 Small | 640x640 | 通用场景 |
| yolo_v8m | YOLOv8 Medium | 640x640 | 高精度场景 |
| yolo_v8l | YOLOv8 Large | 640x640 | 超高精度 |
| yolo_v8x | YOLOv8 XLarge | 640x640 | 极致精度 |

---

**文档版本**: v1.0  
**创建日期**: 2026-03-31  
**最后更新**: 2026-03-31