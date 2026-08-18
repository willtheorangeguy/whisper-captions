<!-- Logo -->
<h1 align="center">whisper-captions</h1>

<!-- Copy -->
<h4 align="center">Generate subtitles for any video — locally, with no API key and nothing uploaded.</h4>

<!-- Badges -->
<div align="center">
  <img alt="Run Tests" src="https://github.com/willtheorangeguy/whisper-captions/actions/workflows/test.yml/badge.svg">
  <img alt="PyPI" src="https://img.shields.io/pypi/v/whisper-captions">
  <img alt="Python versions" src="https://img.shields.io/pypi/pyversions/whisper-captions">
  <img alt="GitHub Issues" src="https://img.shields.io/github/issues/willtheorangeguy/whisper-captions">
  <img alt="License" src="https://img.shields.io/github/license/willtheorangeguy/whisper-captions">
</div>

<!-- Navigation -->
<p align="center">
  <a href="#key-features">Key Features</a> •
  <a href="#installation">Installation</a> •
  <a href="#usage">Usage</a> •
  <a href="#documentation">Documentation</a> •
  <a href="#support">Support</a> •
  <a href="#contributing">Contributing</a> •
  <a href="#credits">Credits</a> •
  <a href="#license">License</a>
</p>

## Key Features

- Transcribes with [OpenAI's Whisper](https://openai.com/blog/whisper) **on your machine** — no API key, no account, nothing leaves the computer.
- Writes a standard `.srt` per video, or burns the subtitles into a new file.
- Takes several videos, or a directory of them, in one run.
- Translates foreign-language audio into English subtitles.
- Any Whisper model, from `tiny` to `turbo`, so you can trade accuracy against time.

## Installation

```bash
pip install whisper-captions
```

Needs Python 3.9+ and [ffmpeg](https://ffmpeg.org/) on your `PATH`. See [`docs/installation.md`](docs/installation.md).

## Usage

```bash
whisper-captions video.mp4                          # video.srt
whisper-captions ./videos -o ./subtitles            # a whole folder
whisper-captions video.mp4 --task translate         # English subtitles
whisper-captions video.mp4 --srt_only false -o out  # burn them in
```

> **Use a separate `-o` directory when burning subtitles in.** The burned output is named after the input, so writing to the input's own directory overwrites the source video. See [`docs/internal/known-issues.md`](docs/internal/known-issues.md).

## Documentation

Full documentation lives in [`docs/`](docs/README.md):
[Quickstart](docs/quickstart.md) · [Installation](docs/installation.md) · [Configuration](docs/configuration.md) · [Architecture](docs/architecture.md) · [API](docs/api.md) · [Development](docs/development.md) · [FAQ](docs/faq.md) · [Troubleshooting](docs/troubleshooting.md) · [Roadmap](docs/roadmap.md)

## Support

Open a [GitHub Discussion](https://github.com/willtheorangeguy/whisper-captions/discussions/new) or file an [issue](https://github.com/willtheorangeguy/whisper-captions/issues/new/choose).

## Contributing

Contributions welcome. See the org-wide [Contributing Guide](https://github.com/willtheorangeguy/.github/blob/main/CONTRIBUTING.md) and [Code of Conduct](https://github.com/willtheorangeguy/.github/blob/main/CODE_OF_CONDUCT.md).

## Credits

Transcription by [OpenAI Whisper](https://github.com/openai/whisper); audio and video handled by [ffmpeg](https://ffmpeg.org/) through [ffmpeg-python](https://github.com/kkroening/ffmpeg-python).

## License

MIT — see [`LICENSE.md`](LICENSE.md).
