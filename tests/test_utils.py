"""
Unit tests for the whisper_captions.utils module.
"""
import pytest
import os
import tempfile
from io import StringIO
from whisper_captions.utils import (
    str2bool,
    format_timestamp,
    write_srt,
    filename,
    expand_video_paths,
)


class TestStr2Bool:
    """Test cases for str2bool function."""
    
    def test_str2bool_true(self):
        """Test that 'true' returns True."""
        assert str2bool("true") is True
        assert str2bool("TRUE") is True
        assert str2bool("True") is True
    
    def test_str2bool_false(self):
        """Test that 'false' returns False."""
        assert str2bool("false") is False
        assert str2bool("FALSE") is False
        assert str2bool("False") is False
    
    def test_str2bool_invalid(self):
        """Test that invalid strings raise ValueError."""
        with pytest.raises(ValueError):
            str2bool("yes")
        with pytest.raises(ValueError):
            str2bool("no")
        with pytest.raises(ValueError):
            str2bool("1")


class TestFormatTimestamp:
    """Test cases for format_timestamp function."""
    
    def test_format_timestamp_zero(self):
        """Test formatting zero seconds."""
        assert format_timestamp(0) == "00:00,000"
        assert format_timestamp(0, always_include_hours=True) == "00:00:00,000"
    
    def test_format_timestamp_seconds(self):
        """Test formatting seconds only."""
        assert format_timestamp(5.5) == "00:05,500"
        assert format_timestamp(59.999) == "00:59,999"
    
    def test_format_timestamp_minutes(self):
        """Test formatting minutes and seconds."""
        assert format_timestamp(60) == "01:00,000"
        assert format_timestamp(125.250) == "02:05,250"
    
    def test_format_timestamp_hours(self):
        """Test formatting hours, minutes, and seconds."""
        assert format_timestamp(3600) == "01:00:00,000"
        assert format_timestamp(3661.123) == "01:01:01,123"
        assert format_timestamp(7384.456) == "02:03:04,456"
    
    def test_format_timestamp_always_include_hours(self):
        """Test formatting with always_include_hours flag."""
        assert format_timestamp(30, always_include_hours=True) == "00:00:30,000"
        assert format_timestamp(90, always_include_hours=True) == "00:01:30,000"
    
    def test_format_timestamp_negative_raises_error(self):
        """Test that negative timestamps raise AssertionError."""
        with pytest.raises(AssertionError):
            format_timestamp(-1)


class TestWriteSrt:
    """Test cases for write_srt function."""
    
    def test_write_srt_single_segment(self):
        """Test writing a single subtitle segment."""
        transcript = [
            {
                "start": 0.0,
                "end": 2.5,
                "text": "Hello world"
            }
        ]
        
        output = StringIO()
        write_srt(transcript, output)
        result = output.getvalue()
        
        assert "1" in result
        assert "00:00:00,000 --> 00:00:02,500" in result
        assert "Hello world" in result
    
    def test_write_srt_multiple_segments(self):
        """Test writing multiple subtitle segments."""
        transcript = [
            {
                "start": 0.0,
                "end": 2.5,
                "text": "Hello world"
            },
            {
                "start": 2.5,
                "end": 5.0,
                "text": "How are you?"
            }
        ]
        
        output = StringIO()
        write_srt(transcript, output)
        result = output.getvalue()
        
        assert "1" in result
        assert "2" in result
        assert "Hello world" in result
        assert "How are you?" in result
    
    def test_write_srt_arrow_replacement(self):
        """Test that --> in text is replaced with ->."""
        transcript = [
            {
                "start": 0.0,
                "end": 2.0,
                "text": "This --> that"
            }
        ]
        
        output = StringIO()
        write_srt(transcript, output)
        result = output.getvalue()
        
        assert "This -> that" in result
        assert "This --> that" not in result.split('\n')[2]  # Check in text line only


class TestFilename:
    """Test cases for filename function."""
    
    def test_filename_with_extension(self):
        """Test extracting filename from path with extension."""
        assert filename("/path/to/video.mp4") == "video"
        assert filename("video.avi") == "video"
        assert filename("/home/user/file.txt") == "file"
    
    def test_filename_without_extension(self):
        """Test extracting filename from path without extension."""
        assert filename("/path/to/file") == "file"
        assert filename("document") == "document"
    
    def test_filename_multiple_dots(self):
        """Test filename with multiple dots."""
        assert filename("/path/to/my.video.mp4") == "my.video"
        assert filename("archive.tar.gz") == "archive.tar"
    
    def test_filename_relative_path(self):
        """Test filename with relative path."""
        assert filename("./video.mp4") == "video"
        assert filename("../folder/video.mp4") == "video"
    
    def test_filename_windows_path(self):
        """Test filename with Windows-style path."""
        # os.path.basename handles both Unix and Windows paths
        result = filename("C:\\Users\\Documents\\video.mp4")
        # Result depends on OS, but should work correctly
        assert "video" in result


class TestExpandVideoPaths:
    """Test cases for expand_video_paths function."""

    def test_expand_file_passthrough(self, tmp_path):
        """Test that plain file paths are returned as-is."""
        video = tmp_path / "clip.mp4"
        video.write_bytes(b"")
        assert expand_video_paths([str(video)]) == [str(video)]

    def test_expand_directory(self, tmp_path):
        """Test that a directory expands to the video files it contains."""
        for name in ["b.mp4", "a.mkv", "notes.txt"]:
            (tmp_path / name).write_bytes(b"")
        result = expand_video_paths([str(tmp_path)])
        assert result == [str(tmp_path / "a.mkv"), str(tmp_path / "b.mp4")]

    def test_expand_mixed_files_and_directories(self, tmp_path):
        """Test mixing file and directory arguments."""
        video = tmp_path / "single.mov"
        video.write_bytes(b"")
        folder = tmp_path / "batch"
        folder.mkdir()
        (folder / "clip.mp4").write_bytes(b"")
        result = expand_video_paths([str(video), str(folder)])
        assert result == [str(video), str(folder / "clip.mp4")]

    def test_expand_uppercase_extension(self, tmp_path):
        """Test that extensions are matched case-insensitively."""
        video = tmp_path / "CLIP.MP4"
        video.write_bytes(b"")
        assert expand_video_paths([str(tmp_path)]) == [str(video)]

    def test_expand_empty_directory_raises(self, tmp_path):
        """Test that a directory with no videos raises FileNotFoundError."""
        (tmp_path / "notes.txt").write_bytes(b"")
        with pytest.raises(FileNotFoundError):
            expand_video_paths([str(tmp_path)])

    def test_expand_missing_path_raises(self, tmp_path):
        """Test that a nonexistent path raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            expand_video_paths([str(tmp_path / "missing.mp4")])
