# 视频分析工作台 - 重构设计方案

## 一、核心设计理念

### 1.1 端到端场景优先
从具体的使用场景出发设计功能，而非从独立的功能模块出发。

### 1.2 配置驱动
通过 YAML 配置声明式地定义系统组件和 Pipeline，而非硬编码。

### 1.3 预定义 Pipeline + 策略模式
- GStreamer Pipeline 是预定义的
- 根据任务配置选择匹配的 Pipeline 执行
- 支持 Python 层的多线程、多模型批量推理

---

## 二、系统架构

### 2.1 核心链路

```
┌─────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────┐
│  GStreamer  │ -> │  Python Workers │ -> │  Model Engine   │ -> │  GStreamer  │
│   Input     │    │  (多线程并发)    │    │  (YOLO/自定义)   │    │   Output    │
└─────────────┘    └─────────────────┘    └─────────────────┘    └─────────────┘
      ↓                    ↓                      ↓                    ↓
  视频源输入            帧处理队列              模型推理              输出目标
  (File/RTSP)         (Concurrent)          (批量推理)           (RTMP/HLS/File)
```

### 2.2 模块分层

```
┌──────────────────────────────────────────────────────────────┐
│                     API Layer (FastAPI)                      │
├──────────────────────────────────────────────────────────────┤
│                    Service Layer                              │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────────┐ │
│  │ VideoSource │ │   Model     │ │      Task              │ │
│  │   Service   │ │   Service   │ │      Service           │ │
│  └─────────────┘ └─────────────┘ └─────────────────────────┘ │
├──────────────────────────────────────────────────────────────┤
│                  Pipeline Engine                              │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────────┐ │
│  │ GStreamer   │ │   Worker    │ │     Model Engine        │ │
│  │   Manager   │ │   Manager   │ │                         │ │
│  └─────────────┘ └─────────────┘ └─────────────────────────┘ │
├──────────────────────────────────────────────────────────────┤
│                   Config Layer                               │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────────┐ │
│  │  app.yaml   │ │  Pipelines   │ │     Models              │ │
│  │  (主配置)    │ │  (预定义)    │ │     (配置)              │ │
│  └─────────────┘ └─────────────┘ └─────────────────────────┘ │
└──────────────────────────────────────────────────────────────┘
```

---

## 三、配置系统设计

### 3.1 主配置文件 app.yaml

```yaml
# 应用基础配置
app:
  name: "video-analysis-studio"
  version: "0.1.0"
  environment: "development"

# Supabase 配置
supabase:
  url: "${SUPABASE_URL}"
  key: "${SUPABASE_KEY}"
  timeout: 30

# GStreamer 全局配置
gstreamer:
  max_pipelines: 10

# Pipeline 预定义配置
# 直接使用 GStreamer launch 字符串格式，预留占位符用于参数替换
# 占位符格式: ${placeholder_name}
pipelines:
  # RTSP 转 RTMP (带 YOLO 检测)
  rtsp_yolo_rtmp:
    name: "RTSP YOLO 检测转 RTMP"
    description: "RTSP 流 -> YOLO 检测 -> RTMP 输出"
    type: "detection"
    input:
      type: "rtsp"
      source: "${INPUT_RTSP_URL}"
    # 直接使用 GStreamer launch 字符串
    # appsink 用于将视频帧传递给 Python 进行模型推理
    # appsrc 用于将处理后的帧传回 GStreamer 继续编码输出
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

  # RTSP 转 HLS (带 YOLO 检测)
  rtsp_yolo_hls:
    name: "RTSP YOLO 检测转 HLS"
    description: "RTSP 流 -> YOLO 检测 -> HLS 输出"
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
      video/x-h264,profile=main !
      hlssink location=${HLS_OUTPUT_DIR}/segment_%05d.ts playlist-location=${HLS_OUTPUT_DIR}/playlist.m3u8 target-duration=4
    output:
      type: "hls"
      directory: "${HLS_OUTPUT_DIR}"
    model: "yolo_v8"

  # 多输入融合示例
  multi_input_fusion:
    name: "多输入融合检测"
    description: "多个 RTSP 流 -> 融合检测 -> RTMP 输出"
    type: "fusion"
    input:
      type: "multi"
      sources:
        - name: "camera_1"
          source: "${INPUT_RTSP_URL_1}"
        - name: "camera_2"
          source: "${INPUT_RTSP_URL_2}"
    launch_template: |
      # 输入流 1
      rtspsrc name=src1 location=${INPUT_RTSP_URL_1} !
      rtph264depay ! h264parse ! avdec_h264 ! video/x-raw,width=640,height=480 !
      queue name=q1 !

      # 输入流 2
      rtspsrc name=src2 location=${INPUT_RTSP_URL_2} !
      rtph264depay ! h264parse ! avdec_h264 ! video/x-raw,width=640,height=480 !
      queue name=q2 !

      # 合并处理
      queue name=q_merge max-size-buffers=1 !
      appsink name=yolo_sink emit-signals=true max-buffers=1 drop=true

      appsrc name=yolo_src format=time caps=video/x-raw,format=I420,width=1280,height=480 !
      queue !
      videoconvert !
      x264enc speed-preset=ultrafast tune=zerolatency !
      flvmux !
      rtmpsink location=${OUTPUT_RTMP_URL}
    output:
      type: "rtmp"
      target: "${OUTPUT_RTMP_URL}"
    model: "custom_fusion"

# 模型配置
models:
  yolo_v8:
    type: "yolo"
    framework: "ultralytics"
    model_path: "models/yolov8n.pt"
    conf_threshold: 0.25
    iou_threshold: 0.45
    device: "cuda"
    batch_size: 4

  custom_fusion:
    type: "fusion"
    models:
      - name: "yolo_v8"
        weight: 0.6
      - name: "resnet50"
        weight: 0.4
    fusion_type: "weighted_average"
    device: "cuda"

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

### 3.2 配置加载机制

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
    - 多输入/多输出配置
    """
    
    PLACEHOLDER_PATTERN = re.compile(r'\$\{([^}]+)\}')
    
    def __init__(self, config_path: str = "config/app.yaml"):
        self.config_path = Path(config_path)
        self._config: Dict[str, Any] = {}
        self._variables: Dict[str, str] = {}
    
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
        """解析模板中的占位符

        Args:
            template: 包含 ${placeholder} 的模板字符串
            variables: 占位符变量字典

        Returns:
            替换后的字符串
        """
        def replace_placeholder(match):
            key = match.group(1)
            return variables.get(key, match.group(0))
        return self.PLACEHOLDER_PATTERN.sub(replace_placeholder, template)

class PipelineConfig:
    """Pipeline 配置类"""

    def __init__(self, name: str, config: Dict[str, Any]):
        self.name = name
        self.description = config.get("description", "")
        self.type = config.get("type", "passthrough")
        self.input_type = config.get("input", {}).get("type")
        self.input_sources = config.get("input", {}).get("sources", [])
        self.launch_template = config.get("launch_template", "")
        self.output_type = config.get("output", {}).get("type")
        self.output_target = config.get("output", {}).get("target")
        self.model_name = config.get("model", "")

    def build_launch(self, variables: Dict[str, str]) -> str:
        """构建最终的 GStreamer launch 字符串

        Args:
            variables: 运行时变量 (如输入URL、输出URL等)

        Returns:
            完整的 GStreamer launch 字符串
        """
        return ConfigLoader().resolve_placeholders(self.launch_template, variables)

    def get_required_variables(self) -> List[str]:
        """获取模板中需要的所有占位符变量"""
        return self.PLACEHOLDER_PATTERN.findall(self.launch_template)

---

## 四、模型模块设计

### 4.1 模型接口定义

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

    @property
    @abstractmethod
    def input_type(self) -> str:
        """输入类型"""
        pass

    @property
    @abstractmethod
    def output_type(self) -> str:
        """输出类型"""
        pass
```

### 4.2 YOLO 模型实现

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

        if "device" in config:
            self._model.to(config["device"])

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

    @property
    def input_type(self) -> str:
        return "video_frame"

    @property
    def output_type(self) -> str:
        return "detections"
```

### 4.3 模型管理器

```python
from typing import Dict, Optional

class ModelManager:
    """模型管理器"""

    def __init__(self):
        self._models: Dict[str, VideoModel] = {}
        self._configs: Dict[str, Dict] = {}

    def register_model(self, name: str, model: VideoModel, config: Dict) -> None:
        """注册模型"""
        self._models[name] = model
        self._configs[name] = config
        model.initialize(config)

    def get_model(self, name: str) -> Optional[VideoModel]:
        """获取模型"""
        return self._models.get(name)

    def release_all(self) -> None:
        """释放所有模型"""
        for model in self._models.values():
            model.release()
        self._models.clear()
```

---

## 五、Pipeline 系统设计

### 5.1 预定义 Pipeline

```python
from enum import Enum
from typing import List, Dict, Any

class PipelineType(Enum):
    """Pipeline 类型"""
    RTSP_TO_RTMP = "rtsp_to_rtmp"
    FILE_TO_RTMP = "file_to_rtmp"
    RTSP_TO_HLS = "rtsp_to_hls"
    FILE_TO_HLS = "file_to_hls"
    RTSP_TO_FILE = "rtsp_to_file"
    FILE_TO_FILE = "file_to_file"

class PipelineConfig:
    """Pipeline 配置"""

    def __init__(self, pipeline_type: PipelineType, config: Dict[str, Any]):
        self.type = pipeline_type
        self.input_type = config.get("input", {}).get("type")
        self.output_type = config.get("output", {}).get("type")
        self.elements = config.get("output", {}).get("elements", [])
        self.processing = config.get("processing", "passthrough")

    @property
    def gstreamer_launch(self) -> str:
        """生成 GStreamer launch 字符串"""
        # 根据 pipeline 类型和配置生成对应的 launch 字符串
        pass
```

### 5.2 Pipeline 注册表

```python
from typing import Dict, Optional

class PipelineRegistry:
    """Pipeline 注册表"""

    def __init__(self):
        self._pipelines: Dict[str, PipelineConfig] = {}

    def register(self, name: str, pipeline_config: PipelineConfig) -> None:
        """注册 Pipeline"""
        self._pipelines[name] = pipeline_config

    def get(self, name: str) -> Optional[PipelineConfig]:
        """获取 Pipeline 配置"""
        return self._pipelines.get(name)

    def list_all(self) -> List[str]:
        """列出所有 Pipeline"""
        return list(self._pipelines.keys())

    def find_by_io_type(self, input_type: str, output_type: str) -> Optional[str]:
        """根据输入输出类型查找 Pipeline"""
        for name, config in self._pipelines.items():
            if config.input_type == input_type and config.output_type == output_type:
                return name
        return None
```

---

## 六、任务执行流程

### 6.1 任务创建

```
用户创建任务 -> 指定 Pipeline -> 指定 Model -> 启动执行
```

### 6.2 任务执行流程

```python
class TaskExecutor:
    """任务执行器"""

    def __init__(self, model_manager: ModelManager, pipeline_registry: PipelineRegistry):
        self.model_manager = model_manager
        self.pipeline_registry = pipeline_registry

    async def execute_task(self, task: Task) -> None:
        """执行任务"""

        # 1. 获取 Pipeline 配置
        pipeline_config = self.pipeline_registry.get(task.pipeline_name)
        if not pipeline_config:
            raise ValueError(f"Pipeline not found: {task.pipeline_name}")

        # 2. 获取 Model
        model = self.model_manager.get_model(task.model_name)
        if not model:
            raise ValueError(f"Model not found: {task.model_name}")

        # 3. 创建 GStreamer Pipeline
        pipeline = self._create_gstreamer_pipeline(pipeline_config, task)

        # 4. 启动 Python Worker 处理
        worker = Worker(
            pipeline=pipeline,
            model=model,
            config=task.config
        )
        worker.start()

        # 5. 监控任务状态
        self._monitor_task(task.id, worker)
```

---

## 七、Examples 设计

### 7.1 示例场景: RTSP 摄像头 -> YOLO 目标检测 -> RTMP 输出

```
examples/
├── simple_yolo_detection/
│   ├── config/
│   │   └── app.yaml           # 示例配置
│   ├── main.py                # 入口脚本
│   ├── models/
│   │   └── yolo_model.py      # YOLO 模型实现
│   ├── pipelines/
│   │   └── pipeline_manager.py
│   └── requirements.txt
```

### 7.2 简单示例脚本

```python
#!/usr/bin/env python3
"""
简单 YOLO 目标检测示例
RTSP -> YOLO 检测 -> RTMP 输出
"""

import sys
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GLib

def main():
    Gst.init(None)

    # Pipeline: RTSP -> 解码 -> YOLO 检测 -> 编码 -> RTMP
    pipeline_str = """
        rtspsrc location=rtsp://localhost:8554/test !
        rtph264depay !
        h264parse !
        avdec_h264 !
        video/x-raw !
        videoconvert !
        x264enc speed-preset=ultrafast tune=zerolatency !
        flvmux !
        rtmpsink location=rtmp://localhost:1935/live/stream
    """

    pipeline = Gst.parse_launch(pipeline_str)
    pipeline.set_state(Gst.State.PLAYING)

    loop = GLib.MainLoop()
    try:
        loop.run()
    except KeyboardInterrupt:
        pipeline.set_state(Gst.State.NULL)

if __name__ == "__main__":
    main()
```

---

## 八、文件结构

```
video-analysis-studio/
├── config/                    # 配置文件目录
│   ├── app.yaml              # 主配置文件 (Pipeline 使用 GStreamer launch 格式)
│   └── models/               # 模型配置
│       ├── yolo.yaml
│       └── fusion.yaml
├── examples/                   # 示例代码
│   └── simple_yolo_detection/
│       ├── config/
│       │   └── app.yaml
│       ├── main.py
│       ├── models/
│       │   ├── __init__.py
│       │   └── yolo_model.py
│       ├── pipelines/
│       │   ├── __init__.py
│       │   └── pipeline_manager.py
│       └── requirements.txt
├── backend/src/
│   ├── config/                # 配置加载
│   │   ├── __init__.py
│   │   ├── loader.py         # ConfigLoader 配置加载器
│   │   └── loader_test.py
│   ├── models/               # 模型模块 (重构)
│   │   ├── __init__.py
│   │   ├── base.py          # VideoModel 抽象基类
│   │   ├── yolo.py          # YOLO 实现
│   │   ├── fusion.py        # 多模型融合实现
│   │   └── manager.py       # ModelManager 模型管理器
│   ├── pipelines/           # Pipeline 模块 (新增)
│   │   ├── __init__.py
│   │   ├── config.py        # PipelineConfig 配置类
│   │   └── registry.py      # PipelineRegistry 注册表
│   ├── processor/           # 视频处理器 (新增)
│   │   ├── __init__.py
│   │   ├── base.py          # 处理器基类
│   │   ├── appsink_handler.py # appsink 帧提取
│   │   └── appsrc_handler.py # appsrc 帧输出
│   ├── executor/             # 任务执行器 (新增)
│   │   ├── __init__.py
│   │   └── task_executor.py
│   ├── api/
│   ├── services/
│   └── utils/
│       └── gstreamer_manager.py  # 保留，基础管道管理
└── specs/
    └── architecture.md      # 架构文档
```

---

## 九、Pipeline 数据流设计

### 9.1 GStreamer 与 Python 的数据交换

```
┌─────────────────────────────────────────────────────────────────┐
│                      GStreamer Pipeline                          │
│                                                                  │
│  [rtspsrc] ─► [rtph264depay] ─► [h264parse] ─► [avdec_h264]   │
│                                                              │
│                                               [appsink]       │
│                                                    │            │
│                                                    ▼            │
│  [rtmpsink] ◄─ [flvmux] ◄─ [h264parse] ◄─ [x264enc] ◄─      │
│                                                              │
│                                               [appsrc]        │
│                                                    │            │
└────────────────────────────────────────────────────┼────────────┘
                                                     │
                                                     ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Python Worker                               │
│                                                                  │
│  appsink ◄──── 帧队列 (Queue)  ◄──── Model Inference           │
│                                                                  │
│  appsrc  ──── 处理后帧队列 ──── 后处理 (绘制框) ──────────────  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 9.2 appsink/appsrc 处理流程

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

        # 获取 appsink 和 appsrc 元素
        self.appsink = self.pipeline.get_by_name("yolo_sink")
        self.appsrc = self.pipeline.get_by_name("yolo_src")

        # 连接 appsink 信号
        self.appsink.connect("new-sample", self.on_new_sample)

    def on_new_sample(self, appsink):
        """appsink 新样本回调 - 从 GStreamer 接收帧"""
        sample = appsink.pull_sample()
        if sample:
            # 获取帧数据
            buf = sample.get_buffer()
            caps = sample.get_caps()

            # 提取帧信息
            structure = caps.get_structure(0)
            width = structure.get_value("width")
            height = structure.get_value("height")

            # 转换为 numpy 数组
            success, map_info = buf.map(Gst.MapFlags.READ)
            if success:
                frame = np.ndarray(
                    (height, width, 3),
                    buffer=map_info.data,
                    dtype=np.uint8
                )
                buf.unmap(map_info)

                # 调用模型推理
                result = self.model.infer(frame)

                # 绘制检测框
                frame = self.draw_detections(frame, result)

                # 发送到 appsrc
                self.send_to_appsrc(frame)

        return Gst.FlowReturn.OK

    def send_to_appsrc(self, frame: np.ndarray):
        """发送处理后的帧到 appsrc"""
        # 创建 GStreamer 缓冲区
        buf = Gst.Buffer.new_wrapped(frame.tobytes())

        # 设置时间戳
        buf.pts = Gst.util_get_timestamp()
        buf.duration = 33333333  # 30fps = 33.33ms

        # 推送缓冲区
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

## 十、验证清单

- [ ] 配置加载器正常工作
- [ ] YOLO 模型可以初始化和推理
- [ ] Pipeline 注册表可以注册和查找
- [ ] 端到端示例可以运行
- [ ] 代码风格统一
- [ ] 文档更新完成