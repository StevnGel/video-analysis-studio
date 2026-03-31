# 视频分析工作台 v1.0 需求规格说明书

## 1. 项目概述

### 1.1 项目背景

本项目旨在构建一个面向外部客户的视频分析工作台，支持安防监控、交通分析、工业质检等多种场景。系统采用前后端一体架构，核心视频分析链路支持视频输入、模型推理、结果输出播放。项目采用配置驱动设计理念，支持通过YAML声明式定义系统组件和Pipeline。

### 1.2 项目定位

- **核心目标**：构建可扩展的视频分析平台，支持多算法、多任务、多GPU调度的视频实时推理和离线分析
- **目标客户**：外部企业客户（安防监控、交通分析、工业质检等领域的终端用户）
- **技术定位**：基于GStreamer的视频处理框架 + Python多进程模型推理 + React前端

### 1.3 版本规划

| 版本 | 特性 | 预计周期 |
|------|------|----------|
| v1.0 | 核心视频分析链路（本地YOLO推理、文件I/O、离线/实时任务） | TBD |
| v2.0 | API Ray Service调用、rerun-io离线存储 | v1.0后 |
| v3.0 | 3D高斯建模模块 | 后续规划 |

**扩展性预留**：v1.0为所有后续特性预留扩展接口，包括：
- 3D高斯建模模块接口
- rerun-io存储接口
- API Ray Service调用接口
- 多算法（SAM3等）接入接口

---

## 2. 业务需求

### 2.1 目标场景

| 场景 | 描述 | 典型需求 |
|------|------|----------|
| 安防监控 | 实时视频流目标检测、异常行为识别 | 实时推理、低延迟、多路并发 |
| 交通分析 | 车辆检测、流量统计、违章识别 | 高精度、多目标跟踪、离线归档 |
| 工业质检 | 产品缺陷检测、质量评估 | 高精度、ROI区域检测、结果存档 |

### 2.2 核心业务流程

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                              视频分析核心链路                                          │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐         │
│  │   视频输入     │ -> │   模型推理    │ -> │   结果输出    │ -> │   视频播放    │         │
│  │  (文件/RTSP)  │    │  (YOLO/...)  │    │ (文件/RTMP)  │    │  (HLS/Flv)  │         │
│  └──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘         │
│         │                   │                   │                   │                  │
│         v                   v                   v                   v                  │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐         │
│  │  视频源管理   │    │  模型实例池   │    │  离线归档    │    │  任务管理    │         │
│  │              │    │  (多进程+GPU) │    │  (文件系统)   │    │              │         │
│  └──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘         │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 2.3 用户角色

| 角色 | 描述 | 权限 |
|------|------|------|
| 操作员 | 使用系统进行视频分析任务 | 上传视频、创建任务、查看结果 |
| 管理员 | 系统配置管理 | 模型配置、Pipeline管理、系统配置 |

---

## 3. 功能需求

### 3.1 功能模块概览

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                              功能模块架构                                                │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐   │
│  │                              API 层 (FastAPI)                                   │   │
│  │     /api/videos    /api/models    /api/tasks    /api/config    /api/system    │   │
│  └─────────────────────────────────────────────────────────────────────────────────┘   │
│                                         │                                               │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐   │
│  │                              Service 层                                          │   │
│  │  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐           │   │
│  │  │  VideoSource │ │    Model     │ │     Task     │ │    Config    │           │   │
│  │  │   Service    │ │   Service    │ │   Service    │ │   Service    │           │   │
│  │  └──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘           │   │
│  └─────────────────────────────────────────────────────────────────────────────────┘   │
│                                         │                                               │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐   │
│  │                              引擎层                                              │   │
│  │  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐           │   │
│  │  │   Pipeline   │ │   Model      │ │   Task       │ │   Storage    │           │   │
│  │  │   Engine     │ │   Executor   │ │   Scheduler  │ │   Engine     │           │   │
│  │  │  (GStreamer) │ │  (多进程)     │ │  (多GPU)     │ │  (文件系统)  │           │   │
│  │  └──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘           │   │
│  └─────────────────────────────────────────────────────────────────────────────────┘   │
│                                         │                                               │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐   │
│  │                              配置层                                              │   │
│  │           app.yaml    pipelines.yaml    models.yaml    video_formats.yaml       │   │
│  └─────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 3.2 视频源管理

#### 3.2.1 功能列表

| 功能点 | 优先级 | 描述 |
|--------|--------|------|
| 本地视频上传 | P0 | 支持上传本地视频文件（MP4、AVI、MKV等） |
| 视频信息获取 | P0 | 获取视频分辨率、时长、帧率、编码格式 |
| 视频源列表 | P0 | 列出已上传的视频文件 |
| 视频源删除 | P1 | 删除不再需要的视频文件 |
| RTSP流配置 | P1 | 配置RTSP流地址作为输入源（预留接口） |

#### 3.2.2 视频源数据结构

```python
class VideoSource(BaseModel):
    id: str                              # 视频源ID
    name: str                            # 视频源名称
    type: Literal["file", "rtsp"]        # 视频源类型
    path: str                            # 文件路径或RTSP地址
    width: int                           # 宽度
    height: int                          # 高度
    fps: float                           # 帧率
    duration: float                      # 时长（秒）
    codec: str                           # 编码格式
    size: int                            # 文件大小（字节）
    status: Literal["ready", "processing", "deleted"]  # 状态
    created_at: datetime                 # 创建时间
    updated_at: datetime                 # 更新时间
```

### 3.3 模型管理

#### 3.3.1 架构设计

**核心设计原则**：
1. **多进程实例池**：系统启动时创建多个模型实例（每个GPU一个或多个实例），避免GIL问题
2. **实例获取机制**：任务推理时从实例池获取可用实例，执行完成后归还
3. **抽象接口**：支持本地模型调用和API远程调用（预留接口）

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                            模型管理架构                                                  │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  ┌──────────────────────────────────────────────────────────────────────────────┐      │
│  │                             ModelManager (模型管理器)                         │      │
│  │  ┌─────────────────────────────────────────────────────────────────────────┐  │      │
│  │  │                      ModelInstancePool (模型实例池)                     │  │      │
│  │  │                                                                       │  │      │
│  │  │   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐                │  │      │
│  │  │   │  Instance   │   │  Instance   │   │  Instance   │   ...          │  │      │
│  │  │   │  GPU:0      │   │  GPU:1      │   │  GPU:0      │                │  │      │
│  │  │   │  yolo_v8    │   │  yolo_v8    │   │  yolo_v8    │                │  │      │
│  │  │   │  PID:1234   │   │  PID:1235   │   │  PID:1236   │                │  │      │
│  │  │   └─────────────┘   └─────────────┘   └─────────────┘                │  │      │
│  │  │                                                                       │  │      │
│  │  │   实例状态: available / in_use / loading / error                     │  │      │
│  │  └─────────────────────────────────────────────────────────────────────────┘  │      │
│  └──────────────────────────────────────────────────────────────────────────────┘      │
│                                         │                                               │
│                         ┌───────────────┴───────────────┐                              │
│                         │                               │                              │
│              ┌─────────▼─────────┐          ┌─────────▼─────────┐                   │
│              │  LocalModelLoader  │          │  APIModelLoader  │  ←预留接口        │
│              │  (本地进程加载)    │          │  (Ray Service)   │                   │
│              └───────────────────┘          └──────────────────┘                   │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

#### 3.3.2 模型实例定义

```python
class ModelInstance(BaseModel):
    instance_id: str                      # 实例ID
    model_name: str                       # 模型名称
    model_type: str                       # 模型类型（yolo/sam3/...）
    device: str                           # 设备（cuda:0, cuda:1, cpu）
    process_id: int                       # 进程ID
    status: Literal["loading", "ready", "in_use", "error"]  # 状态
    load_time: datetime                   # 加载时间
    last_used: datetime                   # 最后使用时间
    gpu_memory: int                       # GPU内存占用（MB）

class ModelInstancePool:
    """模型实例池 - 管理系统中所有模型实例"""
    
    def __init__(self, config: ModelPoolConfig):
        self.config = config
        self._instances: Dict[str, ModelInstance] = {}
        self._available_queue: asyncio.Queue = asyncio.Queue()
    
    async def initialize(self):
        """初始化实例池 - 启动时加载模型实例"""
        for gpu_config in self.config.gpu_instances:
            for _ in range(gpu_config.instance_count):
                instance = await self._create_instance(gpu_config)
                self._instances[instance.instance_id] = instance
                await self._available_queue.put(instance.instance_id)
    
    async def acquire(self, model_name: str, timeout: float = 30.0) -> ModelInstance:
        """获取可用实例 - 阻塞等待"""
        instance_id = await asyncio.wait_for(
            self._available_queue.get(),
            timeout=timeout
        )
        instance = self._instances[instance_id]
        instance.status = "in_use"
        return instance
    
    async def release(self, instance_id: str):
        """归还实例"""
        instance = self._instances[instance_id]
        instance.status = "ready"
        instance.last_used = datetime.now()
        await self._available_queue.put(instance_id)
```

#### 3.3.3 模型调用接口（抽象）

```python
class VideoModel(ABC):
    """视频模型抽象基类 - 所有模型实现需继承此类"""
    
    @abstractmethod
    async def initialize(self, config: Dict[str, Any]) -> None:
        """初始化模型"""
        pass
    
    @abstractmethod
    async def infer(self, inputs: List[ModelInput]) -> List[ModelOutput]:
        """批量推理 - 异步方法，避免GIL阻塞"""
        pass
    
    @abstractmethod
    async def release(self) -> None:
        """释放资源"""
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        """模型名称"""
        pass


class ModelLoader(ABC):
    """模型加载器抽象基类 - 支持本地和远程加载"""
    
    @abstractmethod
    async def load_model(self, model_name: str, config: Dict[str, Any]) -> VideoModel:
        """加载模型"""
        pass
    
    @abstractmethod
    async def unload_model(self, model_name: str) -> None:
        """卸载模型"""
        pass


class LocalModelLoader(ModelLoader):
    """本地模型加载器 - 多进程加载"""
    
    async def load_model(self, model_name: str, config: Dict[str, Any]) -> VideoModel:
        """使用独立进程加载模型"""
        # 创建子进程
        # 加载模型到子进程
        # 返回模型代理对象
        pass


class APIModelLoader(ModelLoader):
    """API模型加载器 - Ray Service调用（预留接口）"""
    
    async def load_model(self, model_name: str, config: Dict[str, Any]) -> VideoModel:
        """通过API调用远程模型服务"""
        # 连接Ray Service
        # 获取模型代理
        pass
```

#### 3.3.4 功能列表

| 功能点 | 优先级 | 描述 |
|--------|--------|------|
| 模型实例池管理 | P0 | 启动时加载多GPU模型实例，任务时获取实例执行 |
| 本地YOLO推理 | P0 | 实现本地YOLO模型加载和推理 |
| 模型配置 | P0 | 置信度阈值、IoU阈值、batch size等参数配置 |
| 模型列表 | P0 | 列出已注册的可用水模型 |
| 模型实例状态 | P1 | 查看实例GPU占用、状态 |
| API模型调用 | P2 | 预留接口，支持Ray Service调用 |

### 3.4 任务管理

#### 3.4.1 任务类型定义

```python
class TaskType(str, Enum):
    REALTIME = "realtime"     # 实时任务：持续处理实时流
    OFFLINE = "offline"       # 离线任务：处理视频文件

class TaskStatus(str, Enum):
    PENDING = "pending"       # 待执行
    PENDING_WITH_INFERENCE = "pending_with_inference"  # 待执行（带推理）
    QUEUED = "queued"         # 排队中
    RUNNING = "running"       # 运行中
    PAUSED = "paused"         # 暂停
    COMPLETED = "completed"    # 已完成
    FAILED = "failed"         # 失败
    CANCELLED = "cancelled"   # 已取消

class AnalysisTask(BaseModel):
    id: str
    name: str                           # 任务名称
    task_type: TaskType                 # 任务类型
    input_config: InputConfig           # 输入配置（包含视频源）
    output_config: OutputConfig         # 输出配置
    model_config: Optional[ModelConfig] # 模型配置（支持多模型并行）
    status: TaskStatus                  # 任务状态
    progress: float                     # 进度（0-100）
    gpu_device: Optional[str]           # 分配的GPU设备
    result_url: Optional[str]           # 结果输出URL
    priority: int                       # 优先级
    created_at: datetime
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    error_message: Optional[str]

class InputConfig(BaseModel):
    source: VideoSource                 # 视频源（本地或在线）
    resize: Optional[ResizeConfig]     # resize配置
    roi: Optional[ROIConfig]           # ROI区域
    skip_frames: Optional[int]          # 跳帧数
    buffer_size: Optional[int]         # 缓冲区大小
    decode_threads: Optional[int]       # 解码线程数

class VideoSource(BaseModel):
    type: Literal["local", "rtsp", "http", "https"]  # 视频源类型
    id: Optional[str]                  # 本地视频源ID（type=local时必填）
    url: Optional[str]                 # 在线视频地址
    auto_download: Optional[bool]      # 是否自动下载为本地MP4
    timeout: Optional[int]             # 下载超时时间（秒）

class ModelConfig(BaseModel):
    parallel: bool                      # 是否并行推理，默认True
    models: List[ModelItem]             # 模型列表

class ModelItem(BaseModel):
    name: str                           # 模型名称
    config: Optional[InferenceConfig]  # 推理配置
    enabled: bool                       # 是否启用
    for_display: bool                  # 是否用于绘制展示
    draw_config: Optional[DrawConfig]  # 绘制配置

class DrawConfig(BaseModel):
    draw_bbox: bool                    # 绘制边界框
    draw_mask: bool                    # 绘制分割掩码
    draw_label: bool                   # 绘制标签
    draw_confidence: bool              # 绘制置信度
    bbox_color: Optional[str]          # 边界框颜色（十六进制）
    mask_alpha: Optional[float]        # 掩码透明度
    line_thickness: Optional[int]      # 线条厚度
    font_scale: Optional[float]        # 字体大小
    label_prefix: Optional[str]         # 标签前缀
    z_order: Optional[int]             # 绘制层级
```

#### 3.4.2 GPU调度策略

**设计原则**：模型实例池统一管理GPU资源，任务获取实例时自动绑定到对应GPU

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                               GPU调度架构                                                │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  ┌─────────────────────────────────────────────────────────────────────────────┐       │
│  │                           TaskScheduler (任务调度器)                         │       │
│  │                                                                              │       │
│  │   任务请求 ──► 选择最佳实例 ──► 绑定GPU ──► 执行推理 ──► 归还实例            │       │
│  │       │            │               │             │              │              │       │
│  │       │            ▼               ▼             ▼              ▼              │       │
│  │       │     ┌─────────────────────────────────────────────────────────┐     │       │
│  │       │     │              ModelInstancePool (模型实例池)              │     │       │
│  │       │     │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐      │     │       │
│  │       │     │  │ Instance0   │  │ Instance1   │  │ Instance2   │      │     │       │
│  │       │     │  │ GPU:0       │  │ GPU:1       │  │ GPU:0       │      │     │       │
│  │       │     │  │ Status:Ready│  │ Status:Busy │  │ Status:Ready│      │     │       │
│  │       │     │  └─────────────┘  └─────────────┘  └─────────────┘      │     │       │
│  │       │     └─────────────────────────────────────────────────────────────┘     │       │
│  └───────────────────────────────────────────────────────────────────────────────────┘       │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

#### 3.4.3 功能列表

| 功能点 | 优先级 | 描述 |
|--------|--------|------|
| 创建分析任务 | P0 | 创建实时或离线分析任务 |
| 启动任务 | P0 | 启动任务执行 |
| 停止任务 | P0 | 停止任务执行 |
| 任务状态查询 | P0 | 查看任务运行状态、进度 |
| 任务列表 | P0 | 列出所有任务 |
| 任务结果获取 | P0 | 获取分析结果输出地址 |
| 任务日志 | P1 | 查看任务执行日志 |

### 3.5 视频配置管理

#### 3.5.1 配置参数清单

**输入配置（InputConfig）**：

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| source | VideoSource | - | 视频源（本地或在线） |
| resize.width | int | 源视频宽度 | resize 宽度 |
| resize.height | int | 源视频高度 | resize 高度 |
| resize.maintain_aspect | bool | true | 保持宽高比 |
| roi.x1 | int | 0 | ROI 区域 x1 |
| roi.y1 | int | 0 | ROI 区域 y1 |
| roi.x2 | int | -1 | ROI 区域 x2（-1 表示全区域） |
| roi.y2 | int | -1 | ROI 区域 y2 |
| skip_frames | int | 0 | 跳帧数（每N帧处理1帧） |
| buffer_size | int | 30 | 缓冲区大小 |
| decode_threads | int | 4 | 解码线程数 |

**视频源（VideoSource）**：

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| source.type | str | - | 视频源类型（local/rtsp/http/https） |
| source.id | string | - | 本地视频源ID（type=local时必填） |
| source.url | string | - | 在线视频地址（type=rtsp/http/https时必填） |
| source.auto_download | bool | true | 是否自动下载为本地MP4 |
| source.timeout | int | 300 | 下载超时时间（秒） |

**输出配置（OutputConfig）**：

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| output.type | str | "file" | 输出类型（file/rtmp/hls） |
| output.path | string | "/data/output" | 输出目录（以任务ID命名） |
| output.rtmp_url | string | - | RTMP 推流地址 |
| output.hls_dir | string | - | HLS 输出目录 |
| output.format.width | int | 源视频宽度 | 输出视频宽度 |
| output.format.height | int | 源视频高度 | 输出视频高度 |
| output.format.fps | float | 源视频帧率 | 输出视频帧率 |
| output.format.codec | str | "h264" | 视频编码（h264、h265） |
| output.format.bitrate | str | "2M" | 输出码率 |
| output.format.gop_size | int | 30 | GOP 大小 |
| output.format.profile | str | "main" | 编码 profile |

**模型配置（ModelConfig）**：

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| model_config.parallel | bool | true | 是否并行推理 |
| model_config.models | array | - | 模型列表 |

**模型项（ModelItem）**：

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| model.name | str | - | 模型名称 |
| model.config | object | - | 推理配置 |
| model.enabled | bool | true | 是否启用 |
| model.for_display | bool | true | 是否用于绘制展示 |
| model.draw_config | object | - | 绘制配置 |

**绘制配置（DrawConfig）**：

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| draw_config.draw_bbox | bool | true | 绘制边界框 |
| draw_config.draw_mask | bool | false | 绘制分割掩码 |
| draw_config.draw_label | bool | true | 绘制标签 |
| draw_config.draw_confidence | bool | true | 绘制置信度 |
| draw_config.bbox_color | string | "#00FF00" | 边界框颜色 |
| draw_config.mask_alpha | float | 0.5 | 掩码透明度 |
| draw_config.line_thickness | int | 2 | 线条厚度 |
| draw_config.font_scale | float | 0.8 | 字体大小 |
| draw_config.label_prefix | string | - | 标签前缀 |
| draw_config.z_order | int | 0 | 绘制层级 |

#### 3.5.2 设计说明

**视频源设计**：
- 支持本地视频源（已上传的视频文件）
- 支持在线视频源（RTSP流、HTTP/HTTPS视频）
- 在线视频源自动下载为本地MP4，与任务ID绑定存储

**多模型并行推理**：
- 支持多模型并行推理，默认启用
- 每个模型独立配置推理参数和绘制参数
- 通过 `for_display` 标记是否用于绘制展示

#### 3.5.2 配置文件结构

```yaml
# video_formats.yaml - 视频格式配置
video_formats:
  # 预定义格式配置
  presets:
    # 1080P 高清
    hd_1080p:
      input:
        width: 1920
        height: 1080
        fps: 30
      processing:
        resize:
          width: 640
          height: 640
          maintain_aspect: true
        skip_frames: 0
        batch_size: 4
      output:
        width: 1920
        height: 1080
        fps: 30
        codec: h264
        bitrate: 4M
        preset: ultrafast
    
    # 720P 流畅
    hd_720p:
      input:
        width: 1280
        height: 720
        fps: 25
      processing:
        resize:
          width: 640
          height: 640
          maintain_aspect: true
        batch_size: 8
      output:
        width: 1280
        height: 720
        fps: 25
        codec: h264
        bitrate: 2M
    
    # 工业质检 - 高精度
    industrial_high_precision:
      input:
        width: 3840
        height: 2160
        fps: 30
      processing:
        resize:
          width: 1280
          height: 1280
          maintain_aspect: false
        roi:
          x1: 500
          y1: 500
          x2: 3340
          y2: 1660
        batch_size: 1
      output:
        width: 3840
        height: 2160
        fps: 30
        codec: h265
        bitrate: 10M
    
    # 交通分析 - 车牌识别
    traffic_plate:
      input:
        width: 1920
        height: 1080
        fps: 30
      processing:
        resize:
          width: 1280
          height: 720
        batch_size: 4
      output:
        width: 1920
        height: 1080
        fps: 30
        codec: h264
        bitrate: 3M
```

### 3.6 离线归档

#### 3.6.1 功能设计

| 功能点 | 优先级 | 描述 |
|--------|--------|------|
| 分析结果保存 | P0 | 保存检测框、视频片段到文件系统 |
| 元数据导出 | P0 | 导出 JSON 格式的分析元数据 |
| 归档目录管理 | P1 | 配置归档存储路径 |
| rerun-io接口 | P2 | 预留 rerun-io 存储接口 |

#### 3.6.2 归档数据结构

```python
class ArchiveRecord(BaseModel):
    """归档记录"""
    task_id: str                         # 任务ID
    video_source_id: str                  # 视频源ID
    model_name: str                       # 模型名称
    timestamp: datetime                   # 时间戳
    frame_index: int                     # 帧序号
    frame_data: Optional[str]             # 帧数据文件路径（可选保存）


class DetectionRecord(BaseModel):
    """检测记录"""
    class_id: int
    class_name: str
    confidence: float
    bbox: List[float]                    # [x1, y1, x2, y2]
    tracking_id: Optional[int]           # 跟踪ID


class AnalysisMetadata(BaseModel):
    """分析元数据"""
    version: str = "1.0"
    task_id: str
    video_source: VideoSource
    model_config: Dict[str, Any]
    video_config: VideoConfig
    output_config: OutputConfig
    detections: List[DetectionRecord]
    archive_time: datetime
```

---

## 4. 非功能性需求

### 4.1 性能需求

| 指标 | 要求 | 说明 |
|------|------|------|
| 支持并发任务数 | ≥10 路视频 | 同时处理10路以上视频分析任务 |
| GPU 利用率 | ≥80% | 推理时 GPU 利用率 |
| 推理延迟 | ≤100ms/帧 | 单帧推理延迟（1080P） |
| 端到端延迟 | ≤500ms | 实时任务从输入到输出的延迟 |
| 系统启动时间 | ≤30s | 服务启动并加载模型实例的时间 |

### 4.2 可用性需求

| 指标 | 要求 |
|------|------|
| 系统可用性 | 99.9% |
| 故障恢复时间 | ≤5min |
| 模型实例自动恢复 | 支持 |

### 4.3 可扩展性需求

| 维度 | 设计目标 |
|------|----------|
| 算法扩展 | 新增算法只需实现 VideoModel 接口并注册 |
| 视频源扩展 | 支持文件/RTSP/HTTP/WebRTC 等多种输入 |
| 存储扩展 | 支持本地文件系统/对象存储/rerun-io |
| GPU 扩展 | 支持动态添加 GPU 实例 |

### 4.4 技术约束

- Python 3.9+
- GStreamer 1.0+
- CUDA 11.0+（如使用 GPU）
- 后端框架：FastAPI
- 前端框架：React 18+ / TypeScript

---

## 5. MVP 范围定义

### 5.1 MVP 功能清单

| 模块 | 功能点 | MVP 实现 |
|------|--------|----------|
| **视频源管理** | 本地视频上传 | ✅ 实现 |
| | 视频信息获取 | ✅ 实现 |
| | 视频列表/删除 | ✅ 实现 |
| | RTSP 流输入 | 预留接口 |
| **模型管理** | 模型实例池 | ✅ 实现（多进程） |
| | 本地 YOLO 推理 | ✅ 实现 |
| | 模型配置 | ✅ 实现 |
| | API Ray 调用 | 预留接口 |
| **任务管理** | 创建/启动/停止任务 | ✅ 实现 |
| | 实时任务 | ✅ 实现 |
| | 离线任务 | ✅ 实现 |
| | 任务状态查询 | ✅ 实现 |
| **视频配置** | 格式配置化 | ✅ 实现 |
| | 预定义格式 | ✅ 实现（3-5种） |
| | ROI 区域配置 | ✅ 实现 |
| **离线归档** | 文件系统存储 | ✅ 实现 |
| | 元数据导出 | ✅ 实现 |
| | rerun-io 接口 | 预留接口 |

### 5.2 MVP 交付物

1. **后端服务**：支持视频分析完整链路
2. **前端应用**：Web 界面（视频上传、任务管理、结果播放）
3. **配置文件**：app.yaml、video_formats.yaml
4. **技术文档**：API 文档、部署文档

### 5.3 MVP 不包含

- RTSP 实时流输入（v1.1）
- API Ray Service 调用（v2.0）
- rerun-io 存储（v2.0）
- 3D 高斯建模（v3.0）
- 多租户管理
- 用户认证授权

---

## 6. 系统架构（详细设计）

### 6.1 整体架构图

```
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│                                     视频分析工作台架构                                       │
├─────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────────────────────┐ │
│  │                                    前端 (React + TypeScript)                          │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │ │
│  │  │  视频上传   │  │  任务创建   │  │  任务监控   │  │  结果播放   │  │   系统配置  │ │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘ │ │
│  └───────────────────────────────────────────────────────────────────────────────────────┘ │
│                                                 │                                           │
│                                          HTTP/REST API                                     │
│                                                 ▼                                           │
│  ┌───────────────────────────────────────────────────────────────────────────────────────┐ │
│  │                                    API Layer (FastAPI)                                 │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │ │
│  │  │ VideoAPI    │  │ ModelAPI    │  │ TaskAPI     │  │ ConfigAPI   │  │ SystemAPI   │ │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘ │ │
│  └───────────────────────────────────────────────────────────────────────────────────────┘ │
│                                                 │                                           │
│  ┌───────────────────────────────────────────────────────────────────────────────────────┐ │
│  │                                    Service Layer                                       │ │
│  │  ┌──────────────────────────┐  ┌──────────────────────────┐  ┌─────────────────────┐│ │
│  │  │     VideoSourceService    │  │       ModelService       │  │      TaskService    ││ │
│  │  │  - 视频上传/存储          │  │  - 模型实例池管理        │  │  - 任务生命周期     ││ │
│  │  │  - 视频信息解析            │  │  - 推理调度              │  │  - 状态管理         ││ │
│  │  └──────────────────────────┘  └──────────────────────────┘  └─────────────────────┘│ │
│  └───────────────────────────────────────────────────────────────────────────────────────┘ │
│                                                 │                                           │
│  ┌───────────────────────────────────────────────────────────────────────────────────────┐ │
│  │                                    Engine Layer                                        │ │
│  │                                                                                         │ │
│  │  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐  ┌───────────────┐  │ │
│  │  │  PipelineEngine  │  │  ModelExecutor   │  │ TaskScheduler    │  │ StorageEngine │  │ │
│  │  │  (GStreamer)     │  │  (多进程推理)     │  │ (任务调度)       │  │ (文件系统)     │  │ │
│  │  │                  │  │                  │  │                  │  │               │  │ │
│  │  │  - Pipeline配置  │  │  - 实例池管理    │  │  - GPU分配       │  │  - 归档存储    │  │ │
│  │  │  - 视频编解码    │  │  - 批量推理      │  │  - 队列管理      │  │  - 结果导出    │  │ │
│  │  │  - 流输出       │  │  - 异步处理      │  │  - 负载均衡      │  │               │  │ │
│  │  └──────────────────┘  └──────────────────┘  └──────────────────┘  └───────────────┘  │ │
│  └───────────────────────────────────────────────────────────────────────────────────────┘ │
│                                                 │                                           │
│  ┌───────────────────────────────────────────────────────────────────────────────────────┐ │
│  │                                    Config Layer                                        │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                  │ │
│  │  │  app.yaml   │  │ models.yaml │  │ pipelines   │  │ video_      │                  │ │
│  │  │  (主配置)    │  │ (模型配置)   │  │ (Pipeline) │  │ formats.yaml│                  │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘                  │ │
│  └───────────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                             │
└─────────────────────────────────────────────────────────────────────────────────────────────┘
```

### 6.2 模块依赖关系

```
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│                                  模块依赖关系                                              │
├─────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                             │
│   Config (配置层)                                                                          │
│        │                                                                                   │
│        ▼                                                                                   │
│   ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐                             │
│   │ Pipeline │    │  Model  │    │  Task   │    │ Storage │                             │
│   │  Config  │    │  Config │    │  Config │    │  Config │                             │
│   └────┬────┘    └────┬────┘    └────┬────┘    └────┬────┘                             │
│        │              │              │              │                                    │
│        ▼              ▼              ▼              ▼                                    │
│   ┌─────────────────────────────────────────────────────────────────────────────┐         │
│   │                         Service Layer                                        │         │
│   │  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐  │         │
│   │  │   Video     │    │   Model     │    │   Task      │    │  Config     │  │         │
│   │  │  Service    │    │  Service    │    │  Service    │    │  Service    │  │         │
│   │  └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘  │         │
│   └─────────────────────────────────────────────────────────────────────────────┘         │
│        │              │              │              │                                    │
│        ▼              ▼              ▼              ▼                                    │
│   ┌─────────────────────────────────────────────────────────────────────────────┐         │
│   │                         Engine Layer                                         │         │
│   │  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐  │         │
│   │  │  Pipeline   │    │   Model     │    │  Task       │    │  Storage    │  │         │
│   │  │  Engine     │    │  Executor   │    │  Scheduler  │    │  Engine     │  │         │
│   │  └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘  │         │
│   └─────────────────────────────────────────────────────────────────────────────┘         │
│                                                                                             │
└─────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 7. API 设计

### 7.1 视频源 API

```
POST   /api/v1/videos/upload          上传视频文件
GET    /api/v1/videos                 获取视频列表
GET    /api/v1/videos/{id}            获取视频详情
DELETE /api/v1/videos/{id}            删除视频
```

### 7.2 模型 API

```
GET    /api/v1/models                  获取模型列表
GET    /api/v1/models/{name}          获取模型详情
GET    /api/v1/models/instances       获取模型实例状态
```

### 7.3 任务 API

```
POST   /api/v1/tasks                  创建任务
GET    /api/v1/tasks                  获取任务列表
GET    /api/v1/tasks/{id}             获取任务详情
POST   /api/v1/tasks/{id}/start       启动任务
POST   /api/v1/tasks/{id}/stop        停止任务
DELETE /api/v1/tasks/{id}             删除任务
GET    /api/v1/tasks/{id}/output      获取输出地址
```

### 7.4 推理 API

```
POST   /api/v1/tasks/{id}/inference   为任务绑定/切换模型（支持多模型）
GET    /api/v1/tasks/{id}/inferences 获取任务的所有推理会话
GET    /api/v1/tasks/{id}/inference/stream  推理状态SSE流
GET    /api/v1/inferences/{id}        查询推理状态
POST   /api/v1/inferences/{id}/stop   停止推理
DELETE /api/v1/inferences/{id}        删除推理会话
```

### 7.5 配置 API（已移除预定义preset）

```
GET    /api/v1/config/video-formats    获取视频格式配置（已废弃）
GET    /api/v1/config/pipelines        获取 Pipeline 配置
```

---

**设计说明**：
- 任务参数按领域划分为 input_config、output_config、model_config
- 视频源统一在 input_config.source 中定义
- 推理接口使用与任务创建一致的 model_config 结构
- 移除 preset 预定义配置，所有参数直接开放

---

## 8. 验收标准

### 8.1 功能验收

| 序号 | 验收项 | 通过条件 |
|------|--------|----------|
| 1 | 视频上传 | 可上传 MP4/AVI 文件，成功获取视频信息 |
| 2 | 模型实例池 | 启动时加载多个 GPU 模型实例，可查看实例状态 |
| 3 | 离线任务 | 可创建并执行离线任务，输出带检测框的视频 |
| 4 | 实时任务 | 可创建并执行实时任务，持续输出检测结果 |
| 5 | 任务参数配置 | 通过 API 参数配置输入/输出/模型/绘制配置 |
| 6 | 多模型并行推理 | 支持多模型并行推理，各自独立配置和绘制 |
| 7 | 在线视频源 | 支持 RTSP/HTTP/HTTPS 视频源，自动下载为本地MP4 |
| 8 | 前端播放 | 可在前端播放处理后的视频 |

### 8.2 性能验收

| 序号 | 验收项 | 通过条件 |
|------|--------|----------|
| 1 | 并发能力 | 8 路视频同时推理，GPU 利用率 ≥70% |
| 2 | 推理延迟 | 1080P 单帧推理延迟 ≤100ms |
| 3 | 启动时间 | 服务启动至模型加载完成 ≤30s |

### 8.3 扩展性验收

| 序号 | 验收项 | 通过条件 |
|------|--------|----------|
| 1 | 算法扩展 | 新增模型只需实现接口并注册，无需修改核心代码 |
| 2 | 配置扩展 | 新增视频格式只需在配置文件中添加，无需修改代码 |

---

## 9. 风险与缓解

| 风险 | 影响 | 缓解措施 |
|------|------|----------|
| GIL 性能瓶颈 | 推理性能 | 使用多进程模型实例池 |
| GStreamer 复杂度 | 开发周期 | 使用预定义 Pipeline |
| GPU 资源竞争 | 多任务性能 | 实例池 + 队列调度 |
| 视频格式兼容性 | 功能覆盖 | 配置化支持多种格式 |

---

## 10. 附录

### 10.1 配置示例

```yaml
# app.yaml - 主配置文件
app:
  name: "video-analysis-studio"
  version: "1.0.0"
  environment: "production"

server:
  host: "0.0.0.0"
  port: 8000
  workers: 1

# GPU 实例配置
model_pool:
  gpu_instances:
    - device: "cuda:0"
      instance_count: 2        # 每个 GPU 2 个实例
      model: "yolo_v8"
    - device: "cuda:1"
      instance_count: 2
      model: "yolo_v8"
  instance_timeout: 300       # 实例空闲超时（秒）
  max_queue_size: 100

# 任务配置
task:
  default_timeout: 3600      # 默认任务超时（秒）
  max_concurrent_tasks: 10   # 最大并发任务数
  auto_restart: true         # 任务异常自动重启

# 存储配置
storage:
  video_dir: "/data/videos"
  output_dir: "/data/output"
  archive_dir: "/data/archive"

# 日志配置
logging:
  level: "INFO"
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
```

### 10.2 数据字典

| 字段 | 类型 | 说明 |
|------|------|------|
| video_id | string | 视频源唯一标识 |
| task_id | string | 任务唯一标识 |
| instance_id | string | 模型实例唯一标识 |
| model_name | string | 模型名称 |
| gpu_device | string | GPU 设备标识 |

---

**文档版本**: v1.0  
**创建日期**: 2026-03-31  
**最后更新**: 2026-03-31
