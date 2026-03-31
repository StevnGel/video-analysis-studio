# File to File Pipeline 示例

无模型视频转码的 GStreamer Pipeline 示例。

## 目录结构

```
examples/v1/file_to_file/
├── config/
│   ├── pipeline.yaml      # Pipeline 配置 (GStreamer launch 模板)
│   └── task.yaml         # 任务配置 (输入/输出/运行参数)
├── main.py               # 主程序入口
├── requirements.txt     # Python 依赖
└── README.md            # 本文件
```

## 快速开始

### 1. 安装依赖

```bash
# 安装 Python 依赖
pip install -r requirements.txt

# 安装 GStreamer (Ubuntu/Debian)
sudo apt-get install -y \
    libgstreamer1.0-dev \
    libgstreamer-plugins-base1.0-dev \
    gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good \
    gstreamer1.0-plugins-bad \
    gstreamer1.0-plugins-ugly

# 安装 GStreamer (macOS)
brew install gstreamer
```

### 2. 运行

#### 使用配置文件

```bash
cd examples/v1/file_to_file
python main.py --config config/task.yaml
```

#### 使用命令行参数

```bash
python main.py \
    --input /Users/zengwenhua/py_workspace/video-analysis-studio/data/videos/traffic_video_6.mp4 \
    --output /tmp/output.mp4
```

### 3. 查看帮助

```bash
python main.py --help
```

## 配置说明

### task.yaml

```yaml
task:
  name: "任务名称"
  task_type: "offline"  # offline/realtime

input:
  source:
    type: "local"       # local/rtsp/http/https
    path: "输入文件路径"

  resize:
    width: 1920
    height: 1080

output:
  type: "file"          # file/rtmp/hls
  path: "/data/output"
  format:
    width: 1920
    height: 1080
    fps: 30.0
    codec: "h264"
    bitrate: "4M"

runtime:
  output_file_path: "/tmp/output.mp4"
```

### pipeline.yaml

定义了 GStreamer launch 模板，使用 `${placeholder}` 作为占位符。

支持的占位符:
- `INPUT_FILE_PATH`: 输入文件路径
- `OUTPUT_FILE_PATH`: 输出文件路径
- `OUTPUT_WIDTH`: 输出宽度
- `OUTPUT_HEIGHT`: 输出高度
- `VIDEO_FPS`: 帧率
- `VIDEO_BITRANE`: 码率
- `ENCODER_PRESET`: 编码器预设

## 测试

```bash
# 检查 GStreamer 版本
gst-inspect-1.0 --version

# 测试本地视频文件
gst-launch-1.0 filesrc location=/path/to/video.mp4 ! decodebin ! videoconvert ! autovideosink