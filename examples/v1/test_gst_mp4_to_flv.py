import os
import sys
import logging
import time
from pathlib import Path

import gi
gi.require_version("Gst", "1.0")
from gi.repository import Gst, GLib

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

Gst.init(None)


def test_mp4_to_flv():
    """测试 MP4 到 FLV 的转换链路"""
    input_path = "/Users/zengwenhua/py_workspace/video-analysis-studio/data/videos/traffic_video_6.mp4"
    output_path = "/Users/zengwenhua/py_workspace/video-analysis-studio/data/output/test_output.flv"
    
    # 确保输出目录存在
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        logger.info(f"Created output directory: {output_dir}")
    
    # 构建 GStreamer 管道
    pipeline_str = (
        f"filesrc location={input_path} ! "
        f"decodebin ! "
        f"videoconvert ! "
        f"video/x-raw,format=I420 ! "
        f"x264enc bitrate=2000 speed-preset=ultrafast tune=zerolatency ! "
        f"video/x-h264,profile=baseline ! "
        f"flvmux ! "
        f"filesink location={output_path}"
    )
    
    logger.info(f"Testing pipeline: {pipeline_str}")
    
    # 创建并启动管道
    pipeline = Gst.parse_launch(pipeline_str)
    
    # 连接消息处理
    bus = pipeline.get_bus()
    bus.add_signal_watch()
    
    def on_message(bus, message):
        t = message.type
        if t == Gst.MessageType.EOS:
            logger.info("End of stream")
            loop.quit()
        elif t == Gst.MessageType.ERROR:
            err, debug = message.parse_error()
            logger.error(f"Error: {err}, Debug: {debug}")
            loop.quit()
    
    bus.connect("message", on_message)
    
    # 启动管道
    pipeline.set_state(Gst.State.PLAYING)
    
    # 运行主循环
    loop = GLib.MainLoop()
    try:
        loop.run()
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
    finally:
        # 停止管道
        pipeline.set_state(Gst.State.NULL)
        logger.info("Pipeline stopped")
    
    # 检查输出文件
    if os.path.exists(output_path):
        file_size = os.path.getsize(output_path)
        logger.info(f"Output file created: {output_path}, Size: {file_size} bytes")
    else:
        logger.error("Output file not created")


if __name__ == "__main__":
    test_mp4_to_flv()
