# whisper-captions — Configuration

Command-line options only. No config file and no environment variables.

## Options

| Option | Default | Description |
|---|---|---|
| `video` | required | One or more video files, or directories of them |
| `--model` | `turbo` | Whisper model |
| `--output_dir`, `-o` | `.` | Where outputs go |
| `--srt_only` | `true` | Only write `.srt`; `false` also burns subtitles into a video |
| `--output_srt` | `false` | Keep the `.srt` when producing a subtitled video |
| `--task` | `transcribe` | `transcribe` keeps the language; `translate` produces English |
| `--language` | `auto` | Source language; detected when unset |
| `--verbose` | `false` | Progress and debug output |

Booleans are spelled out: `--srt_only false`, not a bare flag.

### `--output_dir` and burn-in

The burned video is written to `{output_dir}/{input-basename}.mp4`. With the default `.` and an
input in the current directory, **that is the input path** — the source video is overwritten.
Always pass a separate `-o` when using `--srt_only false`. See
[`internal/known-issues.md`](./internal/known-issues.md).

### `--output_srt` currently does nothing

The `.srt` is written to `--output_dir` on every run regardless of this setting. Recorded in
[`internal/known-issues.md`](./internal/known-issues.md).

## Choosing a model

| Model | Speed | Use when |
|---|---|---|
| `tiny` | Fastest | Testing the pipeline |
| `base` | Fast | Clear speech, CPU-only |
| `small` | Moderate | A good CPU compromise |
| `medium` | Slow | Accuracy matters, GPU available |
| `large` | Slowest | Best quality |
| `turbo` | Fast, accurate | The default; needs a GPU to feel fast |

`.en` variants (`base.en`, `small.en`) are English-only and better at English than their
multilingual counterparts of the same size. Selecting one forces `--language en` with a warning.

**On a CPU, drop to `small` or `base`.** The default `turbo` is chosen for GPUs and will feel
much slower without one.

## Language

`--language` accepts any of Whisper's ~100 codes, or `auto`.

Setting it explicitly is worth doing when you know the answer: detection samples only the
opening audio, so a video that starts with music or silence can be detected wrongly and
transcribed as the wrong language throughout.

## Task

- `transcribe` — subtitles in the spoken language.
- `translate` — English subtitles, whatever the source. **English is the only target**; Whisper
  offers no other translation direction.

## Video formats

`.mp4`, `.mkv`, `.webm`, `.avi`, `.mov` when scanning a directory. Named explicitly, any file
ffmpeg can read is fine — the extension list only filters directory scans.

Directories are scanned **one level deep**; subdirectories are not searched.

## Audio extraction

Fixed, and matching what Whisper expects: 16 kHz, mono, `pcm_s16le` WAV, written to the system
temp directory. Not configurable, and not cleaned up afterwards — see
[`internal/known-issues.md`](./internal/known-issues.md).
