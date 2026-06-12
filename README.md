# whisper-captions

Automatically generate subtitles for any video — and optionally burn them in — using [OpenAI's Whisper](https://openai.com/blog/whisper) and `ffmpeg`.

[![Run Tests](https://github.com/willtheorangeguy/whisper-captions/actions/workflows/test.yml/badge.svg)](https://github.com/willtheorangeguy/whisper-captions/actions/workflows/test.yml)
[![PyPI](https://img.shields.io/pypi/v/whisper-captions)](https://pypi.org/project/whisper-captions/)
[![Python versions](https://img.shields.io/pypi/pyversions/whisper-captions)](https://pypi.org/project/whisper-captions/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## What it does

`whisper-captions` takes one or more video files (or whole directories of them), extracts the audio, transcribes it locally with Whisper, and writes an `.srt` subtitle file for each video. It can also produce a new video with the subtitles burned in. Everything runs on your machine — no API keys, no uploads.

## Prerequisites

- **Python 3.9+**
- **[ffmpeg](https://ffmpeg.org/)** available on your `PATH`:

  ```bash
  # Windows (winget or chocolatey)
  winget install ffmpeg
  choco install ffmpeg

  # macOS (homebrew)
  brew install ffmpeg

  # Ubuntu / Debian
  sudo apt update && sudo apt install ffmpeg
  ```

## Installation

```bash
pip install whisper-captions
```

Or install the latest development version straight from GitHub:

```bash
pip install git+https://github.com/willtheorangeguy/whisper-captions.git
```

## Usage

Generate an `.srt` subtitle file for a video (the default behavior):

```bash
whisper-captions video.mp4
```

Process several videos, or an entire folder of them, in one go:

```bash
whisper-captions episode1.mp4 episode2.mp4
whisper-captions ./videos -o ./subtitles
```

Burn the subtitles directly into a new video file:

```bash
whisper-captions video.mp4 --srt_only false -o ./output
```

Translate foreign-language audio into English subtitles:

```bash
whisper-captions video.mp4 --task translate
```

### Options

| Option | Default | Description |
| --- | --- | --- |
| `video` | _(required)_ | One or more video files, or directories containing videos (`.mp4`, `.mkv`, `.webm`, `.avi`, `.mov`). |
| `--model` | `turbo` | Whisper model to use. Smaller models are faster; larger models are more accurate. See the [model table](https://github.com/openai/whisper#available-models-and-languages). |
| `--output_dir`, `-o` | `.` | Directory to save the outputs. |
| `--srt_only` | `true` | Only generate the `.srt` file; skip creating a subtitled video. Set to `false` to burn subtitles into the video. |
| `--output_srt` | `false` | When creating subtitled videos, also keep the `.srt` files. |
| `--task` | `transcribe` | `transcribe` keeps the original language; `translate` produces English subtitles. |
| `--language` | `auto` | Source language of the audio (e.g. `en`, `fr`, `ja`). Detected automatically by default. |
| `--verbose` | `false` | Print progress and debug messages. |

> **Note:** The first run downloads the selected Whisper model (~1.5 GB for `turbo`). Subsequent runs use the cached copy. If you don't have a GPU, try a smaller model such as `small` or `base` for faster transcription.

## Using it as a library

The transcription utilities can be imported directly:

```python
from whisper_captions.utils import write_srt, expand_video_paths

import whisper

model = whisper.load_model("turbo")
result = model.transcribe("audio.wav")

with open("output.srt", "w", encoding="utf-8") as srt:
    write_srt(result["segments"], file=srt)
```

## Development

```bash
git clone https://github.com/willtheorangeguy/whisper-captions.git
cd whisper-captions
pip install -e ".[dev]"
pytest
```

Releases are published to PyPI automatically by the [publish workflow](.github/workflows/publish.yml) when a GitHub release is created.

## License

This project is open-source and licensed under the MIT License — see [LICENSE](LICENSE) for details.
