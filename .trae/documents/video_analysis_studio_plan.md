# 视频分析工作台项目计划

## 项目概述

构建一个以核心视频分析链路为中心的视频分析工作台，支持视频上传、模型选择、任务管理和带检测框视频输出播放。

核心链路：`视频上传/输入 → 视频源管理 → 模型选择 → 发起视频分析任务 → GStreamer Pipeline 处理 → 输出带目标检测框的视频 → 播放输出`

## 技术理念

### 1.1 端到端场景优先
从具体的使用场景出发设计功能，而非从独立的功能模块出发。

### 1.2 配置驱动
通过 YAML 配置声明式地定义系统组件和 Pipeline，而非硬编码。

### 1.3 预定义 Pipeline + 策略模式
- GStreamer Pipeline 是预定义的
- 根据任务配置选择匹配的 Pipeline 执行
- 支持 Python 层的多线程、多模型批量推理

---

## 项目结构

```
video-analysis-studio/
├── plans/             # 项目设计和规划文档
├── specs/             # 技术规范文档
├── frontend/          # 前端代码
│   ├── public/        # 静态资源
│   ├── src/          # 源代码
│   │   ├── components/ # 组件
│   │   ├── pages/      # 页面
│   │   ├── services/   # API 服务
│   │   ├── hooks/      # 自定义 hooks
│   │   ├── types/      # TypeScript 类型
│   │   └── utils/      # 工具函数
│   ├── package.json
│   ├── tsconfig.json
│   └── vite.config.ts
├── backend/           # 后端代码
│   ├── src/           # 源代码
│   │   ├── api/       # API 路由
│   │   ├── services/  # 业务逻辑
│   │   ├── models/    # 模型模块
│   │   ├── pipelines/ # Pipeline 模块
│   │   ├── processor/ # 视频处理器
│   │   ├── executor/  # 任务执行器
│   │   ├── config/    # 配置管理
│   │   └── utils/     # 工具函数
│   ├── main.py        # 应用入口
│   └── requirements.txt
├── config/            # 配置文件
│   └── app.yaml      # 主配置文件
├── examples/          # 示例代码
│   └── simple_yolo_detection/
└── tests/            # 测试代码
```

## 核心功能模块（精简版）

### 1. 视频源管理
- **本地视频上传**: 支持本地视频文件上传到服务器
- **视频源选择**: 选择要分析的视频源（上传的文件）
- **视频信息**: 视频基本信息展示（分辨率、时长等）

### 2. 模型管理
- **模型注册**: 注册可用的 AI 检测模型（YOLO 等）
- **模型选择**: 在发起任务时选择使用的模型
- **模型配置**: 置信度阈值、IoU 阈值等参数配置

### 3. 任务管理
- **任务创建**: 选择视频源 + 选择模型 + 配置参数
- **任务控制**: 启动、停止任务
- **任务状态**: 运行状态、进度显示

### 4. 视频输出与播放
- **带框视频输出**: 输出带有目标检测框的视频
- **视频播放**: 在前端播放检测后的视频流
- **输出格式**: 支持 RTMP、HLS、文件输出

---

## 技术栈

### 前端
- **语言**: TypeScript
- **框架**: React 18+
- **构建工具**: Vite
- **状态管理**: React Context + useReducer
- **路由**: React Router
- **UI 组件库**: Ant Design
- **HTTP 客户端**: Axios

### 后端
- **语言**: Python 3.9+
- **Web 框架**: FastAPI
- **视频处理**: GStreamer
- **模型推理**: Ultralytics YOLO
- **并发处理**: Python threading
- **依赖管理**: pip

---

## 核心链路流程

```
┌─────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────┐
│  视频上传/   │    │  Python Workers │    │  Model Engine   │    │  GStreamer  │
│  视频源输入   │ -> │  (多线程并发)    │ -> │  (YOLO/自定义)   │ -> │   输出      │
└─────────────┘    └─────────────────┘    └─────────────────┘    └─────────────┘
      ↓                    ↓                      ↓                    ↓
  视频源管理            帧处理队列              模型推理              输出目标
  (File/RTSP)         (Concurrent)          (批量推理)           (RTMP/HLS/File)
       │                                                                    │
       │                                                                    ▼
       │              ┌─────────────────────────────────────────────────┐
       │              │              前端视频播放器                      │
       │              │         (播放带目标检测框的视频)                   │
       └──────────────►              └─────────────────────────────────────────────────┘
```

### 流程说明

1. **视频上传/选择**: 用户上传本地视频文件或配置 RTSP 流地址
2. **模型选择**: 用户选择要使用的检测模型（YOLO v8 等）
3. **任务创建**: 配置任务参数（置信度阈值等）并创建任务
4. **Pipeline 执行**: GStreamer Pipeline 启动，处理视频帧
5. **模型推理**: Python Worker 接收帧，调用模型进行推理
6. **结果绘制**: 在帧上绘制检测框和标签
7. **输出视频**: 通过 RTMP/HLS/文件输出处理后的视频
8. **播放展示**: 前端播放器播放带检测框的视频流

---

## 系统架构

### 2.1 模块分层

```
┌──────────────────────────────────────────────────────────────┐
│                     API Layer (FastAPI)                      │
├──────────────────────────────────────────────────────────────┤
│                    Service Layer                              │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────────┐ │
│  │ VideoSource │ │   Model     │ │         Task            │ │
│  │   Service   │ │   Service   │ │        Service         │ │
│  └─────────────┘ └─────────────┘ └─────────────────────────┘ │
├──────────────────────────────────────────────────────────────┤
│                  Pipeline Engine                              │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────────┐ │
│  │ GStreamer   │ │   Worker    │ │      Model Engine       │ │
│  │   Manager   │ │   Manager   │ │                        │ │
│  └─────────────┘ └─────────────┘ └─────────────────────────┘ │
├──────────────────────────────────────────────────────────────┤
│                   Config Layer                                │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────────┐ │
│  │  app.yaml   │ │  Pipelines  │ │      Models             │ │
│  │  (主配置)    │ │  (预定义)   │ │      (配置)             │ │
│  └─────────────┘ └─────────────┘ └─────────────────────────┘ │
└──────────────────────────────────────────────────────────────┘
```

---

## 配置系统设计

### 主配置文件 app.yaml

```yaml
# 应用基础配置
app:
  name: "video-analysis-studio"
  version: "0.1.0"
  environment: "development"

# GStreamer 全局配置
gstreamer:
  max_pipelines: 10

# Pipeline 预定义配置
pipelines:
  # 文件输入转 RTMP (带 YOLO 检测)
  file_yolo_rtmp:
    name: "文件 YOLO 检测转 RTMP"
    description: "本地视频文件 -> YOLO 检测 -> RTMP 输出"
    type: "detection"
    input:
      type: "file"
      source: "${INPUT_FILE_PATH}"
    launch_template: |
      filesrc location=${INPUT_FILE_PATH} !
      decodebin !
      video/x-raw !
      appsink name=yolo_sink emit-signals=true max-buffers=1 drop=true

      appsrc name=yolo_src format=time caps=video/x-raw,format=I420 !
      queue !
      videoconvert !
      x264enc speed-preset=ultrafast tune=zerolatency key-int-max=30 !
      video/x-h264 !
      h264parse !
      flvmux name=mux !
      rtmpsink location=${OUTPUT_RTMP_URL}
    output:
      type: "rtmp"
      target: "${OUTPUT_RTMP_URL}"
    model: "yolo_v8"

  # RTSP 转 RTMP (带 YOLO 检测)
  rtsp_yolo_rtmp:
    name: "RTSP YOLO 检测转 RTMP"
    description: "RTSP 流 -> YOLO 检测 -> RTMP 输出"
    type: "detection"
    input:
      type: "rtsp"
      source: "${INPUT_RTSP_URL}"
    launch_template: |
      rtspsrc location=${INPUT_RTSP_URL} !
      rtph264depay !
      h264parse !
      avdec_h264 !
      video/x-raw !
      appsink name=yolo_sink emit-signals=true max-buffers=1 drop=true

      appsrc name=yolo_src format=time caps=video/x-raw,format=I420 !
      queue !
      videoconvert !
      x264enc speed-preset=ultrafast tune=zerolatency key-int-max=30 !
      video/x-h264 !
      h264parse !
      flvmux name=mux !
      rtmpsink location=${OUTPUT_RTMP_URL}
    output:
      type: "rtmp"
      target: "${OUTPUT_RTMP_URL}"
    model: "yolo_v8"

  # 文件输入转 HLS (带 YOLO 检测)
  file_yolo_hls:
    name: "文件 YOLO 检测转 HLS"
    description: "本地视频文件 -> YOLO 检测 -> HLS 输出"
    type: "detection"
    input:
      type: "file"
      source: "${INPUT_FILE_PATH}"
    launch_template: |
      filesrc location=${INPUT_FILE_PATH} !
      decodebin !
      video/x-raw !
      appsink name=yolo_sink emit-signals=true max-buffers=1 drop=true

      appsrc name=yolo_src format=time caps=video/x-raw,format=I420 !
      queue !
      videoconvert !
      x264enc speed-preset=ultrafast tune=zerolatency key-int-max=30 !
      video/x-h264,profile=main !
      hlssink location=${HLS_OUTPUT_DIR}/segment_%05d.ts playlist-location=${HLS_OUTPUT_DIR}/playlist.m3u8 target-duration=4
    output:
      type: "hls"
      directory: "${HLS_OUTPUT_DIR}"
    model: "yolo_v8"

# 模型配置
models:
  yolo_v8:
    type: "yolo"
    framework: "ultralytics"
    model_path: "models/yolov8n.pt"
    conf_threshold: 0.25
    iou_threshold: 0.45
    device: "cpu"
    batch_size: 4

# 工作线程配置
workers:
  max_workers: 8
  queue_size: 100
  timeout: 300

# 输出目标配置
outputs:
  rtmp:
    default_server: "rtmp://localhost:1935/live"
    chunk_size: 4096
  hls:
    output_dir: "/tmp/hls"
    segment_duration: 4
    playlist_size: 10
  file:
    output_dir: "/tmp/output"
    format: "mp4"
```

---

## 后端模块设计

### 配置加载器 (config/loader.py)

```python
import yaml
import re
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

class ConfigLoader:
    """配置加载器
    
    支持:
    - 环境变量替换: ${VAR_NAME}
    - 占位符参数替换
    """
    
    PLACEHOLDER_PATTERN = re.compile(r'\$\{([^}]+)\}')
    
    def __init__(self, config_path: str = "config/app.yaml"):
        self.config_path = Path(config_path)
        self._config: Dict[str, Any] = {}
    
    def load(self) -> Dict[str, Any]:
        """加载配置文件"""
        with open(self.config_path, 'r') as f:
            raw_config = yaml.safe_load(f)
        self._config = self._resolve_env_vars(raw_config)
        return self._config
    
    def _resolve_env_vars(self, config: Any) -> Any:
        """解析环境变量引用 ${VAR}"""
        if isinstance(config, str):
            def replace_env_var(match):
                var_name = match.group(1)
                return os.getenv(var_name, match.group(0))
            return self.PLACEHOLDER_PATTERN.sub(replace_env_var, config)
        elif isinstance(config, dict):
            return {k: self._resolve_env_vars(v) for k, v in config.items()}
        elif isinstance(config, list):
            return [self._resolve_env_vars(item) for item in config]
        return config
    
    def resolve_placeholders(self, template: str, variables: Dict[str, str]) -> str:
        """解析模板中的占位符"""
        def replace_placeholder(match):
            key = match.group(1)
            return variables.get(key, match.group(0))
        return self.PLACEHOLDER_PATTERN.sub(replace_placeholder, template)
```

### 模型基类 (models/base.py)

```python
from abc import ABC, abstractmethod
from typing import Any, Dict, List
from pydantic import BaseModel
import numpy as np

class ModelInput(BaseModel):
    """模型输入"""
    frame: np.ndarray
    timestamp: float
    metadata: Dict[str, Any] = {}

class ModelOutput(BaseModel):
    """模型输出"""
    predictions: List[Dict[str, Any]]
    processing_time: float
    metadata: Dict[str, Any] = {}

class DetectionResult(BaseModel):
    """检测结果"""
    class_id: int
    class_name: str
    confidence: float
    bbox: List[float]  # [x1, y1, x2, y2]

class VideoModel(ABC):
    """视频模型抽象基类"""

    @abstractmethod
    def initialize(self, config: Dict[str, Any]) -> None:
        """初始化模型"""
        pass

    @abstractmethod
    def infer(self, inputs: List[ModelInput]) -> List[ModelOutput]:
        """批量推理"""
        pass

    @abstractmethod
    def release(self) -> None:
        """释放资源"""
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """模型名称"""
        pass
```

### YOLO 模型实现 (models/yolo.py)

```python
from typing import List, Dict, Any
import numpy as np
from ultralytics import YOLO

class YOLOModel(VideoModel):
    """YOLO 模型实现"""

    def __init__(self):
        self._model = None
        self._config = {}

    def initialize(self, config: Dict[str, Any]) -> None:
        """初始化 YOLO 模型"""
        self._config = config
        model_path = config.get("model_path", "yolov8n.pt")
        self._model = YOLO(model_path)

    def infer(self, inputs: List[ModelInput]) -> List[ModelOutput]:
        """批量推理"""
        if not self._model:
            raise RuntimeError("Model not initialized")

        frames = [inp.frame for inp in inputs]
        timestamps = [inp.timestamp for inp in inputs]

        results = self._model(frames, conf=self._config.get("conf_threshold", 0.25),
                            iou=self._config.get("iou_threshold", 0.45))

        outputs = []
        for idx, result in enumerate(results):
            detections = []
            if result.boxes is not None:
                for box in result.boxes:
                    detections.append(DetectionResult(
                        class_id=int(box.cls[0]),
                        class_name=result.names[int(box.cls[0])],
                        confidence=float(box.conf[0]),
                        bbox=box.xyxy[0].tolist()
                    ))

            outputs.append(ModelOutput(
                predictions=[d.model_dump() for d in detections],
                processing_time=result.speed.get("inference", 0),
                metadata={"timestamp": timestamps[idx]}
            ))

        return outputs

    def release(self) -> None:
        """释放资源"""
        del self._model
        self._model = None

    @property
    def name(self) -> str:
        return "YOLO"
```

### 视频处理器 (processor/appsink_handler.py)

```python
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject, GLib
import cv2
import numpy as np

class VideoProcessor:
    """视频处理器 - 连接 GStreamer 和 Python 模型"""

    def __init__(self, model, config: dict):
        self.model = model
        self.config = config
        self.pipeline = None
        self.appsink = None
        self.appsrc = None

    def setup_pipeline(self, launch_str: str):
        """设置 Pipeline"""
        self.pipeline = Gst.parse_launch(launch_str)

        self.appsink = self.pipeline.get_by_name("yolo_sink")
        self.appsrc = self.pipeline.get_by_name("yolo_src")

        self.appsink.connect("new-sample", self.on_new_sample)

    def on_new_sample(self, appsink):
        """appsink 新样本回调 - 从 GStreamer 接收帧"""
        sample = appsink.pull_sample()
        if sample:
            buf = sample.get_buffer()
            caps = sample.get_caps()

            structure = caps.get_structure(0)
            width = structure.get_value("width")
            height = structure.get_value("height")

            success, map_info = buf.map(Gst.MapFlags.READ)
            if success:
                frame = np.ndarray(
                    (height, width, 3),
                    buffer=map_info.data,
                    dtype=np.uint8
                )
                buf.unmap(map_info)

                result = self.model.infer(frame)

                frame = self.draw_detections(frame, result)

                self.send_to_appsrc(frame)

        return Gst.FlowReturn.OK

    def send_to_appsrc(self, frame: np.ndarray):
        """发送处理后的帧到 appsrc"""
        buf = Gst.Buffer.new_wrapped(frame.tobytes())
        buf.pts = Gst.util_get_timestamp()
        buf.duration = 33333333
        ret = self.appsrc.emit("push-buffer", buf)
        if ret != Gst.FlowReturn.OK:
            print(f"push-buffer returned: {ret}")

    def draw_detections(self, frame: np.ndarray, detections: list) -> np.ndarray:
        """在帧上绘制检测结果"""
        for det in detections:
            x1, y1, x2, y2 = det["bbox"]
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            label = f"{det['class_name']}: {det['confidence']:.2f}"
            cv2.putText(frame, label, (int(x1), int(y1)-10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        return frame

    def start(self):
        """启动处理"""
        self.pipeline.set_state(Gst.State.PLAYING)

    def stop(self):
        """停止处理"""
        self.pipeline.set_state(Gst.State.NULL)
```

---

## 开发计划

### 阶段一: 项目初始化 (1 周)
1. 创建项目目录结构
2. 配置前端和后端开发环境
3. 配置 GStreamer 环境
4. 搭建 FastAPI 基础框架

### 阶段二: 核心功能实现 (3 周)

1. **配置系统**
   - 实现 ConfigLoader
   - 编写 app.yaml 配置
   - 环境变量解析

2. **模型模块**
   - 实现 VideoModel 基类
   - 实现 YOLOModel
   - 实现 ModelManager

3. **Pipeline 模块**
   - 实现 PipelineConfig
   - 实现 PipelineRegistry
   - 配置预定义 Pipeline

4. **视频处理模块**
   - 实现 VideoProcessor
   - appsink 帧提取
   - appsrc 帧输出
   - 绘制检测框

5. **任务执行模块**
   - 实现 TaskExecutor
   - 任务状态管理

### 阶段三: API 开发 (1 周)

1. **视频源 API**
   - POST /api/videos/upload - 上传视频
   - GET /api/videos - 获取视频列表
   - GET /api/videos/{id} - 获取视频详情

2. **模型 API**
   - GET /api/models - 获取模型列表
   - GET /api/models/{name} - 获取模型详情

3. **任务 API**
   - POST /api/tasks - 创建任务
   - GET /api/tasks - 获取任务列表
   - GET /api/tasks/{id} - 获取任务详情
   - POST /api/tasks/{id}/start - 启动任务
   - POST /api/tasks/{id}/stop - 停止任务

4. **输出 API**
   - GET /api/tasks/{id}/output - 获取输出流地址

### 阶段四: 前端实现 (2 周)

1. **视频上传页面**
   - 文件上传组件
   - 上传进度显示

2. **任务创建页面**
   - 视频源选择
   - 模型选择
   - 参数配置
   - 任务创建

3. **任务监控页面**
   - 任务状态显示
   - 输出视频播放

4. **视频播放**
   - HLS 播放器集成
   - RTMP 流播放（可选）

### 阶段五: 测试和优化 (1 周)

1. **单元测试**
   - 配置加载器测试
   - 模型推理测试
   - Pipeline 构建测试

2. **集成测试**
   - 端到端测试
   - 视频分析流程测试

3. **优化**
   - 性能优化
   - 错误处理完善

---

## API 设计

### 视频源相关

```
POST /api/videos/upload
- 上传视频文件
- 返回: { video_id, filename, duration, width, height }

GET /api/videos
- 获取视频列表
- 返回: [{ id, filename, duration, width, height, status }]

GET /api/videos/{id}
- 获取视频详情
- 返回: { id, filename, path, duration, width, height, status }
```

### 模型相关

```
GET /api/models
- 获取可用模型列表
- 返回: [{ name, type, description, config }]

GET /api/models/{name}
- 获取模型详情
- 返回: { name, type, description, config }
```

### 任务相关

```
POST /api/tasks
- 创建分析任务
- Body: { video_id, model_name, output_type, config }
- 返回: { task_id, status, output_url }

GET /api/tasks
- 获取任务列表
- 返回: [{ task_id, video_id, model_name, status, created_at }]

GET /api/tasks/{id}
- 获取任务详情
- 返回: { task_id, video_id, model_name, status, progress, output_url }

POST /api/tasks/{id}/start
- 启动任务
- 返回: { task_id, status }

POST /api/tasks/{id}/stop
- 停止任务
- 返回: { task_id, status }

GET /api/tasks/{id}/stream
- 获取播放地址
- 返回: { stream_url, type }
```

---

## 验证清单

- [ ] 配置加载器正常工作
- [ ] YOLO 模型可以初始化和推理
- [ ] Pipeline 注册表可以注册和查找
- [ ] 端到端视频分析流程可以运行
- [ ] 前端可以上传视频
- [ ] 前端可以创建和启动任务
- [ ] 前端可以播放带检测框的视频
- [ ] 代码风格统一
- [ ] 文档更新完成

---

## 成功标准

1. **核心功能完整**: 实现视频上传 → 模型选择 → 分析任务 → 带框视频输出播放的完整链路
2. **流程可运行**: 端到端流程可正常运行
3. **基本可靠性**: 系统稳定运行，错误处理完善
4. **可维护性**: 代码结构清晰

---

## 风险与缓解

1. **GStreamer 集成复杂度**
   - 缓解: 使用预定义 Pipeline，使用成熟示例作为参考

2. **性能风险**
   - 缓解: 优化代码，使用并发处理

3. **模型推理性能**
   - 缓解: 批量推理，GPU 加速（可选）
