# GStreamer Installation Guide for macOS

## 环境检测结果

当前环境检测结果:
- **操作系统**: macOS 13.2.1 (Darwin 22.3.0)
- **架构**: x86_64
- **Homebrew**: 已安装
- **Python**: 3.11.6
- **GStreamer**: ❌ 未安装

## 安装说明

### 方式一: 使用安装脚本

```bash
cd /Users/zengwenhua/py_workspace/video-analysis-studio/docs
chmod +x install_gstreamer.sh
./install_gstreamer.sh
```

### 方式二: 手动安装

如果脚本执行有问题，可以手动执行以下命令:

#### 1. 安装 GStreamer 核心包

```bash
brew install gstreamer
```

#### 2. 安装插件集

```bash
# 基础插件 (必须)
brew install gst-plugins-base

# 优质插件 (推荐)
brew install gst-plugins-good

# 常用插件
brew install gst-plugins-ugly

# 高级插件
brew install gst-plugins-bad
```

#### 3. 安装 Python 绑定

```bash
brew install pygobject3
pip install PyGObject
```

#### 4. 安装 FFmpeg 插件 (用于编解码)

```bash
brew install gst-libav
```

## 验证安装

安装完成后，运行以下命令验证:

```bash
# 检查 GStreamer 版本
gst-inspect-1.0 --version

# 查看已安装的插件列表
gst-inspect-1.0 -l
```

## 环境变量配置

在 `~/.zshrc` 或 `~/.bashrc` 中添加:

```bash
# GStreamer 插件路径
export GST_PLUGIN_PATH=/usr/local/lib/gstreamer-1.0

# 如果使用 Homebrew 在 Intel Mac 上
export GST_PLUGIN_PATH=/opt/homebrew/lib/gstreamer-1.0
```

然后执行:

```bash
source ~/.zshrc
```

## 常见问题

### 问题: gst-inspect-1.0 找不到

**解决方案**: 确保 `/usr/local/bin` 或 `/opt/homebrew/bin` 在 PATH 中

### 问题: Python 导入 gstreamer 失败

**解决方案**: 
1. 确保已安装 pygobject3
2. 使用虚拟环境时，需要额外配置 GTK 路径

### 问题: 视频编解码问题

**解决方案**: 安装 gst-libav 插件以支持更多编解码格式

## 相关文档

- 安装脚本: [install_gstreamer.sh](install_gstreamer.sh)
- GStreamer 官网: https://gstreamer.freedesktop.org/
- Homebrew GStreamer: https://formulae.brew.sh/formula/gstreamer

## 后续步骤

安装完成后，可继续安装视频分析相关的依赖:

```bash
# OpenCV
brew install opencv
pip install opencv-python

# NumPy (通常已安装)
pip install numpy
```
