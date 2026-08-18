# whisper-captions — Quickstart

## 1. Install

```bash
pip install whisper-captions
```

You also need [ffmpeg](https://ffmpeg.org/) on your `PATH` — see
[Installation](./installation.md).

## 2. Subtitle a video

```bash
whisper-captions video.mp4
```

Writes `video.srt` beside you, in the current directory.

The **first run downloads the model** — about 1.5 GB for the default `turbo`. It is cached, so
this happens once.

## 3. Expect it to take a while

Transcription is the slow part, and on a CPU it can take longer than the video itself. A smaller
model is dramatically faster:

```bash
whisper-captions video.mp4 --model base
```

See [Configuration](./configuration.md) for the trade.

## 4. Several videos, or a folder

```bash
whisper-captions episode1.mp4 episode2.mp4
whisper-captions ./videos -o ./subtitles
```

Directories are scanned **one level deep** for `.mp4`, `.mkv`, `.webm`, `.avi`, and `.mov`.
Subdirectories are not searched.

Outputs are named after the input's basename, so two files with the same name in different
folders collide — see [`internal/known-issues.md`](./internal/known-issues.md).

## 5. Burn them in

```bash
whisper-captions video.mp4 --srt_only false -o ./output
```

> **Always give `-o` a different directory.** The output is `{name}.mp4` inside `--output_dir`,
> which defaults to `.`, so burning in without `-o` writes over the source video. See
> [`internal/known-issues.md`](./internal/known-issues.md).

## 6. Translate

```bash
whisper-captions video.mp4 --task translate
```

Whisper translates any supported language to **English** subtitles. English is the only target;
`--task transcribe` keeps the original language.

## Then

- [Configuration](./configuration.md) — every option
- [Troubleshooting](./troubleshooting.md) — when ffmpeg or the model misbehaves
