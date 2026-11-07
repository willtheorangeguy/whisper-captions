import importlib
from pathlib import Path
import sys
import types
from unittest.mock import Mock

import pytest


@pytest.fixture()
def cli(monkeypatch):
    whisper = types.ModuleType("whisper")
    whisper.available_models = lambda: ["turbo"]
    whisper.load_model = Mock()
    ffmpeg = types.ModuleType("ffmpeg")
    ffmpeg.input = Mock()
    ffmpeg.concat = Mock()
    monkeypatch.setitem(sys.modules, "whisper", whisper)
    monkeypatch.setitem(sys.modules, "ffmpeg", ffmpeg)
    sys.modules.pop("whisper_captions.cli", None)
    return importlib.import_module("whisper_captions.cli")


def test_existing_output_is_refused_before_model_load(cli, monkeypatch, tmp_path):
    video = tmp_path / "clip.mp4"
    video.write_bytes(b"original")
    output = tmp_path / "clip.subtitled.mp4"
    output.write_bytes(b"previous output")
    monkeypatch.setattr(sys, "argv", ["whisper-captions", str(video), "-o", str(tmp_path), "--srt_only", "false"])
    with pytest.raises(SystemExit) as error:
        cli.main()
    assert error.value.code == 2
    cli.whisper.load_model.assert_not_called()
    assert video.read_bytes() == b"original"
    assert output.read_bytes() == b"previous output"


def test_burning_uses_distinct_output_and_ffmpeg_no_overwrite(cli, monkeypatch, tmp_path):
    video = tmp_path / "clip.mp4"
    video.write_bytes(b"original")
    monkeypatch.setattr(sys, "argv", ["whisper-captions", str(video), "-o", str(tmp_path), "--srt_only", "false"])
    monkeypatch.setattr(cli, "get_audio", lambda paths: {})
    monkeypatch.setattr(cli, "get_subtitles", lambda *args: {str(video): str(tmp_path / "clip.srt")})
    cli.main()
    graph = cli.ffmpeg.concat.return_value
    graph.output.assert_called_once_with(str(tmp_path / "clip.subtitled.mp4"))
    graph.output.return_value.global_args.assert_called_once_with("-n")
    assert video.read_bytes() == b"original"
