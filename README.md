# AutoClipper 🎬

An automated video clipping tool that combines scene detection, audio transcription, highlight candidate selection, and video clip generation.

**Status:** Early Working Prototype (v0.1.0)

## ✨ Features

- **Scene Detection:** Detects scene changes using PySceneDetect.
- **Audio Transcription:** Converts video speech into text using OpenAI Whisper.
- **Highlight Selection:** Finds candidate highlights using keyword-based text scoring.
- **Automatic Clip Generation:** Exports selected segments as individual MP4 clips.
- **Person Detection:** Experimental person detection using YOLO11n.
- **Original Video Format:** Preserves the source aspect ratio and video dimensions during export.

## 🛠️ Technologies Used

- Python
- PySceneDetect
- OpenAI Whisper
- Ultralytics YOLO11n
- OpenCV
- FFmpeg

## 📁 Project Structure

```text
AutoClipper/
├── main.py
├── config.py
├── scene_detector.py
├── transcriber.py
├── highlight_ai.py
├── clip_generator.py
├── person_detector.py
├── requirements.txt
├── .gitignore
└── README.md
```

## ⚙️ Requirements

- Python 3.13
- FFmpeg
- Git
- Sufficient RAM and storage for video processing

## 🚀 Installation

Clone the repository:

```bash
git clone https://github.com/pomegranatepython-cmd/AutoClipper.git
cd AutoClipper
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

Install Python dependencies:

```bash
python -m pip install -r requirements.txt
```

Make sure FFmpeg is installed and available in your system PATH.

## ▶️ Usage

Place your input video inside the `input` folder.

Run the complete pipeline:

```bash
python main.py input/test.mp4
```

Individual modules can also be run separately:

```bash
python scene_detector.py input/test.mp4
python transcriber.py input/test.mp4
python highlight_ai.py transcripts/test.json
python clip_generator.py input/test.mp4 clips/test_highlights.json
```

Generated clips are saved in the `output` folder.

## ⚠️ Current Limitations

- Highlight selection currently uses keyword-based scoring, not semantic understanding.
- Transcription accuracy depends on audio quality and language.
- Person detection is experimental.
- The project is an early prototype and may require manual configuration.
- It does not currently guarantee viral or engaging clips.

## 🔮 Future Plans

- Improved multilingual transcription.
- Smarter highlight detection.
- Better person tracking.
- Audio enhancement.
- Improved processing performance.
- A more user-friendly interface.

## 🙌 Acknowledgements

AutoClipper integrates several existing open-source technologies. Their respective authors and maintainers deserve credit.

See third-party license information before redistribution or commercial use.

## 📜 License

License information is currently under review. No project license has been selected yet.
