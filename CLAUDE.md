# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install for development
pip install -e ".[dev]"

# Run all tests
pytest

# Run a single test file or specific test
pytest tests/test_utils.py
pytest tests/test_utils.py::TestFormatTimestamp::test_format_timestamp_hours
```

No linting tool is configured in `pyproject.toml`. The `.github/agents/lint-agent.md` references `ruff` as the intended linter if one is added.

## Architecture

The package lives under `src/whisper_captions/` with two modules:

- **`cli.py`** — The entry point (`whisper_captions.cli:main`). Owns argument parsing, orchestration, and any ffmpeg calls that read/write video files.
- **`utils.py`** — Pure utility functions with no side effects: timestamp formatting, SRT file writing, filename extraction, and video path expansion. These are also the public library API.

### Data flow

```
main()
  └─ expand_video_paths()     # validate inputs; expand directories to sorted file lists
  └─ get_audio()              # extract audio via ffmpeg → PCM 16-bit mono 16 kHz WAV in tempdir
  └─ get_subtitles()          # call model.transcribe() on each WAV, write .srt via write_srt()
  └─ [if not srt_only]        # burn subtitles into video with ffmpeg subtitles filter
```

`get_subtitles()` accepts a `transcribe: callable` so the Whisper call is injected, keeping the function testable without a real model.

### Key conventions

- **Boolean CLI args** use `str2bool()` (accepts `"true"`/`"false"` case-insensitively) rather than `store_true`/`store_false`. All boolean flags must follow this pattern.
- **Supported video formats** are defined in the `VIDEO_EXTENSIONS` set in `utils.py`. Extension matching is always case-insensitive (`.lower()`).
- **SRT output** always uses `always_include_hours=True` in `format_timestamp()` so timestamps are `HH:MM:SS,mmm`. The `-->` token in subtitle text is replaced with `->` to avoid breaking the SRT format.
- Audio is always extracted to the system temp directory (`tempfile.gettempdir()`), not the output directory.

## Dependencies

Runtime: `openai-whisper`, `ffmpeg-python` (Python wrapper around the `ffmpeg` binary, which must be on `PATH`).  
Dev: `pytest>=7.0.0`.

CI tests against Python 3.9, 3.10, 3.11, and 3.12. PyPI releases are triggered by creating a GitHub release.
