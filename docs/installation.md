# whisper-captions — Installation

## Requirements

| | |
|---|---|
| Python | 3.9 or newer |
| ffmpeg | On your `PATH` — not a Python package |
| Disk | ~1.5 GB for the `turbo` model, plus temporary WAV files |
| GPU | Optional, but the difference between minutes and hours |

## ffmpeg

Installed separately, and the most common thing missing:

```bash
winget install ffmpeg          # Windows
choco install ffmpeg           # Windows, chocolatey
brew install ffmpeg            # macOS
sudo apt install ffmpeg        # Debian, Ubuntu
```

Confirm with `ffmpeg -version`. `ffmpeg-python` is a **wrapper** — installing it does not install
ffmpeg itself.

## Install

```bash
pip install whisper-captions
```

Latest from source:

```bash
pip install git+https://github.com/willtheorangeguy/whisper-captions.git
```

This pulls in `openai-whisper`, which pulls in PyTorch — a large download whatever else you do.

## GPU support

Whisper uses PyTorch, and on a CUDA GPU it is roughly an order of magnitude faster. If `pip`
installed the CPU-only build, replace it following
[PyTorch's instructions](https://pytorch.org/get-started/locally/) for your CUDA version.

Check:

```python
import torch; print(torch.cuda.is_available())
```

CPU-only is entirely usable with a smaller model — see [Configuration](./configuration.md).

## The model download

The first run fetches the model to `~/.cache/whisper`:

| Model | Approx. size |
|---|---|
| `tiny` | 75 MB |
| `base` | 140 MB |
| `small` | 460 MB |
| `medium` | 1.5 GB |
| `large`, `turbo` | ~1.5 GB and up |

Cached afterwards. Downloading happens **after** audio extraction, so a first run appears to
stall partway through — it is fetching the model.

## Verify

```bash
ffmpeg -version
whisper-captions --help
whisper-captions short-clip.mp4 --model tiny
```

Use `tiny` for the smoke test: it downloads in seconds and transcribes quickly. Accuracy does
not matter for proving the pipeline works.

## Uninstall

```bash
pip uninstall whisper-captions
rm -rf ~/.cache/whisper        # the models, if you want the space back
```

Temporary WAV files in the system temp directory are not cleaned up by the tool — see
[`internal/known-issues.md`](./internal/known-issues.md).
