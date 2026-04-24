import os
import sys
import logging
import time
import threading
from pathlib import Path
from typing import Optional

import cv2
import numpy as np
import yaml
from ultralytics import YOLO

import gi
gi.require_version("Gst", "1.0")
gi.require_version("GstApp", "1.0")
from gi.repository import Gst, GstApp, GLib, GObject

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

Gst.init(None)


class VideoAnalyzer:
    def __init__(self, config_path: str):
        self.config = self._load_config(config_path)
        self.yolo_model = None
        self.car_class_id = 2

        self.pipeline: Optional[Gst.Pipeline] = None
        self.appsink: Optional[GstApp.AppSink] = None
        self.appsrc: Optional[GstApp.AppSrc] = None

        self.video_width = self.config["gstreamer"]["video_width"]
        self.video_height = self.config["gstreamer"]["video_height"]
        self.fps = self.config["gstreamer"]["fps"]

        self.frame_interval = self.config["video"]["frame_interval"]
        self.current_frame_count = 0
        self.lastprocessed_frame = 0

        self.main_loop: Optional[GLib.MainLoop] = None
        self.is_eos = False

        self._frame_lock = threading.Lock()

    def _load_config(self, config_path: str) -> dict:
        with open(config_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def load_yolo_model(self):
        model_path = self.config["yolo"]["model_path"]
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"YOLO model not found: {model_path}")
        self.yolo_model = YOLO(model_path)
        logger.info(f"Loaded YOLO model from {model_path}")

    def detect_cars(self, frame: np.ndarray) -> np.ndarray:
        results = self.yolo_model(
            frame,
            conf=self.config["yolo"]["confidence_threshold"],
            classes=[self.car_class_id],
            verbose=False,
        )
        annotated_frame = frame.copy()
        for result in results:
            boxes = result.boxes
            for box in boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                conf = float(box.conf[0])
                cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                label = f"car {conf:.2f}"
                cv2.putText(
                    annotated_frame,
                    label,
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 255, 0),
                    2,
                )
        return annotated_frame

    def _on_appsink_new_sample(self, appsink: GstApp.AppSink) -> Gst.FlowReturn:
        sample = appsink.pull_sample()
        if sample is None:
            return Gst.FlowReturn.EOS

        buf = sample.get_buffer()
        if buf is None:
            return Gst.FlowReturn.ERROR

        success, map_info = buf.map(Gst.MapFlags.READ)
        if not success:
            return Gst.FlowReturn.ERROR

        try:
            frame = np.ndarray(
                (self.video_height, self.video_width, 3),
                buffer=map_info.data,
                dtype=np.uint8,
            )
            frame = frame.copy()

            fps = self.config["video"]["fps"]
            frame_interval_count = int(fps * self.frame_interval)

            if self.current_frame_count % frame_interval_count == 0:
                logger.info(f"Processing frame {self.current_frame_count}")
                annotated_frame = self.detect_cars(frame)
            else:
                annotated_frame = frame

            self._push_frame(annotated_frame)
            self.current_frame_count += 1

        finally:
            buf.unmap(map_info)

        return Gst.FlowReturn.OK

    def _push_frame(self, frame: np.ndarray):
        if self.appsrc is None:
            return

        data = frame.tobytes()
        buf = Gst.Buffer.new_wrapped(data)

        appsrc_buf = self.appsrc.emit("push-buffer", buf)
        if appsrc_buf != Gst.FlowReturn.OK:
            logger.warning(f"push-buffer returned: {appsrc_buf}")

    def _on_appsrc_need_data(self, appsrc: GstApp.AppSrc, _):
        pass

    def _on_appsrc_enough_data(self, appsrc: GstApp.AppSrc):
        pass

    def _on_appsrc_seek_data(self, appsrc: GstApp.AppSrc, segment_type: Gst.Format):
        return True

    def _build_pipeline(self):
        video_path = self.config["video"]["input_path"]
        rtmp_url = (
            f"rtmp://{self.config['rtmp']['host']}:"
            f"{self.config['rtmp']['port']}/{self.config['rtmp']['stream_key']}"
        )

        decode_pipeline_str = (
            f"filesrc location={video_path} ! "
            f"decodebin ! "
            f"video/x-raw,format=BGR ! "
            f"appsink name=sink emit-signals=true"
        )
        logger.info(f"Decode pipeline: {decode_pipeline_str}")

        encode_pipeline_str = (
            f"appsrc name=src ! "
            f"video/x-raw,format=BGR,width={self.video_width},height={self.video_height},"
            f"framerate={self.fps}/1 ! "
            f"videoconvert ! "
            f"video/x-raw,format=I420 ! "
            f"x264enc bitrate={self.config['gstreamer']['bitrate'] // 1000} "
            f"speed-preset=ultrafast tune=zerolatency ! "
            f"video/x-h264,profile=baseline ! "
            f"flvmux name=mux ! "
            f"rtmpsink location={rtmp_url}"
        )
        logger.info(f"Encode pipeline: {encode_pipeline_str}")

        decode_pipeline = Gst.parse_launch(decode_pipeline_str)
        encode_pipeline = Gst.parse_launch(encode_pipeline_str)

        self.appsink = decode_pipeline.get_by_name("sink")
        self.appsink.connect("new-sample", self._on_appsink_new_sample)

        self.appsrc = encode_pipeline.get_by_name("src")
        self.appsrc.set_property("format", Gst.Format.TIME)
        self.appsrc.set_property("is-live", True)
        self.appsrc.connect("need-data", self._on_appsrc_need_data)
        self.appsrc.connect("enough-data", self._on_appsrc_enough_data)
        self.appsrc.connect("seek-data", self._on_appsrc_seek_data)

        self.pipeline = Gst.Pipeline.new("video-analysis-pipeline")

        self.pipeline.add(decode_pipeline)
        self.pipeline.add(encode_pipeline)

        decode_pad = decode_pipeline.get_static_pad("src_0")
        encode_pad = encode_pipeline.get_static_pad("sink")

        if decode_pad and encode_pad:
            decode_pad.link(encode_pad)

    def run(self):
        try:
            self.load_yolo_model()
            self._build_pipeline()

            self.pipeline.set_state(Gst.State.PLAYING)

            self.main_loop = GLib.MainLoop()
            self.main_loop.run()

        except Exception as e:
            logger.error(f"Error: {e}")
            raise
        finally:
            if self.pipeline:
                self.pipeline.set_state(Gst.State.NULL)
            logger.info("Released resources")


def main():
    config_path = Path(__file__).parent / "config.yaml"
    analyzer = VideoAnalyzer(str(config_path))
    analyzer.run()


if __name__ == "__main__":
    main()