import cv2
import rerun as rr
import rerun.blueprint as rrb
from ultralytics import YOLO


def main():
    video_path = "/Users/zengwenhua/py_workspace/video-analysis-studio/data/videos/traffic_video_10.mp4"
    model_path = "/Users/zengwenhua/py_workspace/video-analysis-studio/data/weights/yolov8n.pt"

    rr.init("video_detection_with_rerun", spawn=True)

    model = YOLO(model_path)

    video_asset = rr.AssetVideo(path=video_path)
    rr.log("video", video_asset, static=True)

    frame_timestamps_ns = video_asset.read_frame_timestamps_nanos()

    rr.send_columns(
        "video",
        indexes=[rr.TimeColumn("video_time", duration=1e-9 * frame_timestamps_ns)],
        columns=rr.VideoFrameReference.columns_nanos(frame_timestamps_ns),
    )

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise FileNotFoundError(f"Could not open video file: {video_path}")

    frame_count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame, conf=0.25, verbose=False)

        timestamp_ns = frame_timestamps_ns[frame_count]
        rr.set_time("video_time", timestamp=timestamp_ns * 1e-9)

        for result in results:
            boxes = result.boxes
            if len(boxes) == 0:
                print(f"Frame {frame_count}: No detections")
            for box in boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                conf = float(box.conf[0])
                cls = int(box.cls[0])
                label = model.names[cls]
                print(f"Frame {frame_count}: Detected {label} conf={conf:.2f} bbox=({x1},{y1})-({x2},{y2})")

                rr.log("video/detections", rr.Boxes2D(
                    array=[[x1, y1, x2 - x1, y2 - y1]],
                    array_format=rr.Box2DFormat.XYWH,
                    labels=[f"{label}: {conf:.2f}"],
                    colors=[(0, 255, 0)],
                ))
                rr.log("image/detections", rr.Boxes2D(
                    array=[[x1, y1, x2 - x1, y2 - y1]],
                    array_format=rr.Box2DFormat.XYWH,
                    labels=[f"{label}: {conf:.2f}"],
                    colors=[(0, 255, 0)],
                ))

        frame_count += 1

    cap.release()
    print(f"Processed {frame_count} frames")


if __name__ == "__main__":
    main()