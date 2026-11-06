import json
import sys
from pathlib import Path
from scenedetect import open_video, SceneManager
from scenedetect.detectors import ContentDetector

from config import INPUT_DIR, OUTPUT_DIR

def detect_scenes(video_path):
    video_path = Path(video_path)

    video = open_video(str(video_path))

    manager = SceneManager()
    manager.add_detector(
        ContentDetector(threshold=27.0)
    )

    manager.detect_scenes(video)

    scenes = manager.get_scene_list()

    results = []

    for start, end in scenes:
        results.append({
            "start": start.get_seconds(),
            "end": end.get_seconds(),
            "duration": end.get_seconds() - start.get_seconds()
        })

    output = OUTPUT_DIR / f"{video_path.stem}_scenes.json"

    output.write_text(
        json.dumps(results, indent=2),
        encoding="utf-8"
    )

    print(f"Detected {len(results)} scenes")
    print(f"Saved: {output}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scene_detector.py video.mp4")
    else:
        detect_scenes(sys.argv[1])