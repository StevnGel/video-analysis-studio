#!/usr/bin/env python3
"""
File to File Pipeline 示例
视频文件 -> GStreamer 转码 -> 输出视频文件 (无模型)

用法:
    python main.py --config config/task.yaml
    python main.py --input /path/to/input.mp4 --output /path/to/output.mp4
"""

import argparse
import os
import sys
import yaml
import re
import logging

import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GLib, GObject

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class PipelineConfig:
    """Pipeline 配置类"""

    PLACEHOLDER_PATTERN = re.compile(r'\$\{([^}]+)\}')

    def __init__(self, config_path: str):
        self.config_path = config_path
        self._config = {}
        self._pipeline_config = {}

    def load(self) -> dict:
        """加载配置文件"""
        with open(self.config_path, 'r') as f:
            self._config = yaml.safe_load(f)
        return self._config

    def load_pipeline_config(self, pipeline_path: str) -> dict:
        """加载 Pipeline 配置"""
        with open(pipeline_path, 'r') as f:
            self._pipeline_config = yaml.safe_load(f)
        return self._pipeline_config

    def get_pipeline(self, name: str) -> dict:
        """获取指定名称的 Pipeline 配置"""
        pipelines = self._pipeline_config.get('pipelines', {})
        return pipelines.get(name, {})

    def resolve_placeholders(self, template: str, variables: dict) -> str:
        """解析模板中的占位符"""
        def replace_placeholder(match):
            key = match.group(1)
            return variables.get(key, match.group(0))
        return self.PLACEHOLDER_PATTERN.sub(replace_placeholder, template)

    def build_launch_string(self, pipeline_name: str, runtime_vars: dict) -> str:
        """构建 GStreamer launch 字符串"""
        pipeline = self.get_pipeline(pipeline_name)
        if not pipeline:
            raise ValueError(f"Pipeline not found: {pipeline_name}")

        template = pipeline.get('launch_template', '')
        return self.resolve_placeholders(template, runtime_vars)


class GStreamerPipeline:
    """GStreamer Pipeline 管理器"""

    def __init__(self, launch_string: str):
        self.launch_string = launch_string
        self.pipeline = None
        self.loop = None
        self.main_loop_thread = None

    def setup(self):
        """设置 Pipeline"""
        logger.info(f"Creating pipeline: {self.launch_string}")
        self.pipeline = Gst.parse_launch(self.launch_string)

        if not self.pipeline:
            raise RuntimeError("Failed to create pipeline")

        bus = self.pipeline.get_bus()
        bus.add_signal_watch()
        bus.connect("message", self.on_bus_message)

    def on_bus_message(self, bus, message):
        """处理 Bus 消息"""
        msg_type = message.type

        if msg_type == Gst.MessageType.ERROR:
            err, debug = message.parse_error()
            logger.error(f"Pipeline error: {err.message} - {debug}")
            self.stop()
        elif msg_type == Gst.MessageType.WARNING:
            err, debug = message.parse_warning()
            logger.warning(f"Pipeline warning: {err.message} - {debug}")
        elif msg_type == Gst.MessageType.EOS:
            logger.info("End of stream")
            self.stop()
        elif msg_type == Gst.MessageType.STATE_CHANGED:
            if message.src == self.pipeline:
                old, new, pending = message.parse_state_changed()
                logger.info(f"Pipeline state changed: {old.value_nick} -> {new.value_nick}")

    def start(self):
        """启动 Pipeline"""
        ret = self.pipeline.set_state(Gst.State.PLAYING)
        if ret == Gst.StateChangeReturn.FAILURE:
            raise RuntimeError("Failed to set pipeline to PLAYING state")
        logger.info("Pipeline started")

        self.loop = GLib.MainLoop()
        try:
            self.loop.run()
        except KeyboardInterrupt:
            logger.info("Interrupted by user")
            self.stop()

    def stop(self):
        """停止 Pipeline"""
        if self.pipeline:
            logger.info("Stopping pipeline...")
            self.pipeline.set_state(Gst.State.NULL)
            logger.info("Pipeline stopped")

        if self.loop and self.loop.is_running():
            self.loop.quit()


def build_runtime_vars(task_config: dict) -> dict:
    """从任务配置构建运行时变量"""
    input_config = task_config.get('input', {})
    output_config = task_config.get('output', {})
    runtime_config = task_config.get('runtime', {})

    input_source = input_config.get('source', {})
    input_path = input_source.get('path', '')

    output = output_config.get('format', {})
    output_path = runtime_config.get('output_file_path', '')

    output_width = output.get('width', 1920)
    output_height = output.get('height', 1080)
    fps = output.get('fps', 30.0)
    codec = output.get('codec', 'h264')
    bitrate = output.get('bitrate', '4M')

    encoder_preset = 'ultrafast'
    if codec == 'h265':
        encoder_preset = 'ultrafast'

    vars = {
        'INPUT_FILE_PATH': input_path,
        'OUTPUT_FILE_PATH': output_path,
        'OUTPUT_WIDTH': str(output_width),
        'OUTPUT_HEIGHT': str(output_height),
        'VIDEO_FPS': str(fps),
        'VIDEO_BITRATE': bitrate,
        'ENCODER_PRESET': encoder_preset,
    }

    return vars


def main():
    parser = argparse.ArgumentParser(description='File to File Pipeline')
    parser.add_argument('--config', '-c', type=str, default='config/task.yaml',
                        help='Task configuration file')
    parser.add_argument('--pipeline', '-p', type=str,
                        default='config/pipeline.yaml',
                        help='Pipeline configuration file')
    parser.add_argument('--pipeline-name', type=str, default='file_to_file_passthrough',
                        help='Pipeline name')
    parser.add_argument('--input', type=str,
                        help='Input file path (override config)')
    parser.add_argument('--output', type=str,
                        help='Output file path (override config)')
    parser.add_argument('--log-level', type=str, default='INFO',
                        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
                        help='Log level')

    args = parser.parse_args()

    logging.getLogger().setLevel(getattr(logging, args.log_level))

    Gst.init(None)
    logger.info("GStreamer initialized")

    config = PipelineConfig(args.config)
    task_config = config.load()
    config.load_pipeline_config(args.pipeline)

    runtime_vars = build_runtime_vars(task_config)

    if args.input:
        runtime_vars['INPUT_FILE_PATH'] = args.input
    if args.output:
        runtime_vars['OUTPUT_FILE_PATH'] = args.output

    input_path = runtime_vars['INPUT_FILE_PATH']
    output_path = runtime_vars['OUTPUT_FILE_PATH']

    if not input_path:
        logger.error("Input file path not specified")
        sys.exit(1)

    if not output_path:
        logger.error("Output file path not specified")
        sys.exit(1)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    logger.info(f"Input: {input_path}")
    logger.info(f"Output: {output_path}")

    launch_string = config.build_launch_string(args.pipeline_name, runtime_vars)
    logger.info(f"Launch string: {launch_string}")

    pipeline = GStreamerPipeline(launch_string)
    pipeline.setup()
    pipeline.start()

    logger.info("Pipeline finished")


if __name__ == "__main__":
    main()