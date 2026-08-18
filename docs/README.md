# whisper-captions — Documentation

A CLI that extracts audio from video, transcribes it locally with Whisper, and writes `.srt`
subtitles — optionally burning them into a new video.

```
whisper-captions/
├── src/whisper_captions/
│   ├── cli.py      argument parsing, the pipeline, ffmpeg calls
│   └── utils.py    SRT writing, timestamp formatting, path expansion
├── tests/test_utils.py
└── docs/           this documentation
```

## Pages

- [Quickstart](./quickstart.md) — a first subtitle file
- [Installation](./installation.md) — Python, ffmpeg, and the model download
- [Configuration](./configuration.md) — every option, and which model to pick
- [Architecture](./architecture.md) — extract, transcribe, write, burn
- [API](./api.md) — using the utilities as a library
- [Development](./development.md) — tests and release
- [FAQ](./faq.md) — privacy, speed, accuracy, formats
- [Troubleshooting](./troubleshooting.md) — ffmpeg, models, memory, empty output
- [Roadmap](./roadmap.md) — direction and non-goals
- [Known issues](./internal/known-issues.md) — recorded defects

## Everything runs locally

Whisper runs on your machine. There is no API key, no account, and no upload — the video, the
audio, and the transcript never leave the computer.

The cost is the model download (about 1.5 GB for `turbo`, once) and the transcription time,
which is substantial on a CPU. That trade is the whole point: for anything you would not hand to
a third-party service, local is the only option.

## Read this before burning subtitles in

The burned video is named `{input-basename}.mp4` inside `--output_dir`, which defaults to `.` —
so running burn-in on a file in the current directory **overwrites the source video**. Always
pass a separate `-o`. See [`internal/known-issues.md`](./internal/known-issues.md).
