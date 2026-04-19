import os
import sys
import logging
import time
import subprocess
from pathlib import Path
from typing import Optional

import cv2
import numpy as np
import yaml
from ultralytics import YOLO

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class VideoAnalyzer:
    def __init__(self, config_path: str):
        self.config = self._load_config(config_path)
        self.yolo_model = None
        self.video_cap = None
        self.rtmp_process: Optional[subprocess.Popen] = None
        self.car_class_id = 2

    def _load_config(self, config_path: str) -> dict:
        with open(config_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def load_yolo_model(self):
        model_path = self.config["yolo"]["model_path"]
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"YOLO model not found: {model_path}")
        self.yolo_model = YOLO(model_path)
        logger.info(f"Loaded YOLO model from {model_path}")

    def open_video(self) -> bool:
        video_path = self.config["video"]["input_path"]
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")
        self.video_cap = cv2.VideoCapture(video_path)
        if not self.video_cap.isOpened():
            raise ValueError(f"Failed to open video: {video_path}")
        logger.info(f"Opened video: {video_path}")
        return True

    def open_rtmp_stream(self):
        rtmp_url = (
            f"rtmp://{self.config['rtmp']['host']}:"
            f"{self.config['rtmp']['port']}/{self.config['rtmp']['stream_key']}"
        )
        video_config = self.config["gstreamer"]
        ffmpeg_cmd = [
            "ffmpeg",
            "-re",
            "-f",
            "rawvideo",
            "-vcodec",
            "rawvideo",
            "-pix_fmt",
            "bgr24",
            "-s",
            f"{video_config['video_width']}x{video_config['video_height']}",
            "-r",
            str(video_config["fps"]),
            "-i",
            "-",
            "-c:v",
            "libx264",
            "-preset",
            "ultrafast",
            "-tune",
            "zerolatency",
            "-b:v",
            str(video_config["bitrate"]),
            "-f",
            "flv",
            rtmp_url,
        ]
        self.rtmp_process = subprocess.Popen(
            ffmpeg_cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        logger.info(f"Opened RTMP stream: {rtmp_url}")

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

    def process_video(self):
        frame_interval = self.config["video"]["frame_interval"]
        fps = self.video_cap.get(cv2.CAP_PROP_FPS)
        frame_interval_count = int(fps * frame_interval)
        frame_count = 0
        logger.info(f"Processing video: frame interval = {frame_interval}s")
        while True:
            ret, frame = self.video_cap.read()
            if not ret:
                break
            if frame_count % frame_interval_count == 0:
                logger.info(f"Processing frame {frame_count}")
                annotated_frame = self.detect_cars(frame)
                if self.rtmp_process:
                    self.rtmp_process.stdin.write(
                        annotated_frame.tobytes()
                    )
            frame_count += 1
        logger.info(f"Finished processing {frame_count} frames")

    def release_resources(self):
        if self.video_cap:
            self.video_cap.release()
        if self.rtmp_process:
            self.rtmp_process.stdin.close()
            self.rtmp_process.wait()
        logger.info("Released resources")

    def run(self):
        try:
            self.load_yolo_model()
            self.open_video()
            self.open_rtmp_stream()
            self.process_video()
        except Exception as e:
            logger.error(f"Error: {e}")
            raise
        finally:
            self.release_resources()


def main():
    config_path = Path(__file__).parent / "config.yaml"
    analyzer = VideoAnalyzer(str(config_path))
    analyzer.run()


if __name__ == "__main__":
    main()