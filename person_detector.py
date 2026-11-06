
from ultralytics import YOLO
import cv2
import json
import sys
from pathlib import Path


SAMPLE_SECONDS = 0.5


def detect_people(video_path):
    print("Loading YOLO model...")
    model = YOLO("yolo11n.pt")

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Could not open video.")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    if fps <= 0:
        print("Invalid video FPS.")
        cap.release()
        return

    sample_interval = max(1, int(fps * SAMPLE_SECONDS))

    print(f"Video: {width}x{height}")
    print(f"FPS: {fps:.2f}")
    print(f"Total frames: {total_frames}")
    print("Starting full-video detection...")

    detections = []
    previous_center = None
    frame_index = 0

    while True:
        success, frame = cap.read()

        if not success:
            break

        if frame_index % sample_interval == 0:
            results = model(
                frame,
                classes=[0],
                conf=0.35,
                verbose=False
            )

            people = []

            for result in results:
                for box in result.boxes:
                    x1, y1, x2, y2 = map(
                        int, box.xyxy[0].tolist()
                    )

                    center_x = (x1 + x2) / 2
                    area = (x2 - x1) * (y2 - y1)
                    confidence = float(box.conf[0])

                    people.append({
                        "bbox": [x1, y1, x2, y2],
                        "center_x": center_x,
                        "area": area,
                        "confidence": confidence
                    })

            selected = None

            if people:
                if previous_center is None:
                    selected = max(
                        people,
                        key=lambda p: p["area"]
                    )
                else:
                    selected = min(
                        people,
                        key=lambda p: abs(
                            p["center_x"] - previous_center
                        )
                    )

                previous_center = selected["center_x"]

            detections.append({
                "frame": frame_index,
                "time": frame_index / fps,
                "center_x": (
                    selected["center_x"]
                    if selected else None
                ),
                "bbox": (
                    selected["bbox"]
                    if selected else None
                ),
                "confidence": (
                    selected["confidence"]
                    if selected else None
                )
            })

            print(
                f"\rAnalyzed: {frame_index}/{total_frames}",
                end=""
            )

        frame_index += 1

    cap.release()

    output = {
        "video": str(video_path),
        "width": width,
        "height": height,
        "fps": fps,
        "total_frames": total_frames,
        "sample_interval": sample_interval,
        "detections": detections
    }

    output_path = Path("tracking_data.json")

    output_path.write_text(
        json.dumps(output, indent=2),
        encoding="utf-8"
    )

    detected = sum(
        1 for item in detections
        if item["center_x"] is not None
    )

    print("\n\nDetection complete!")
    print(f"Samples analyzed: {len(detections)}")
    print(f"Samples with person: {detected}")
    print(f"Saved: {output_path}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python person_detector.py input/video.mp4")
    else:
        detect_people(sys.argv[1])
