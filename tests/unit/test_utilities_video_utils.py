import pytest
from unittest.mock import MagicMock, patch
from app.utilities.video_utils import is_video_openable, get_video_properties, process_video_images, save_video_image

@pytest.fixture
def mock_cv2():
    with patch('cv2.VideoCapture') as mock_video_capture:
        mock_video_capture.return_value = MagicMock(isOpened=MagicMock())
        yield mock_video_capture

def test_is_video_openable_true(mock_cv2):
    mock_cv2.return_value.isOpened.return_value = True
    assert is_video_openable('path/to/openable/video.mp4') is True

def test_is_video_openable_false(mock_cv2):
    mock_cv2.return_value.isOpened.return_value = False
    assert is_video_openable('path/to/nonexistent/or/corrupt/video.mp4') is False

def test_get_video_properties(mock_cv2):
    mock_cv2.return_value.get.side_effect = [30, 600]
    fps, frame_interval, duration = get_video_properties('path/to/video.mp4')
    assert fps == 30
    assert frame_interval == int(0.2 * fps)  # 5 frames per second
    assert duration == 20  # 600 frames / 30 fps

@patch('app.utilities.video_utils.save_video_image')
def test_process_video_images(mock_save_image, mock_cv2):
    mock_cv2.return_value.read.side_effect = [(True, 'frame')] * 10 + [(False, '')]
    mock_cv2.return_value.get.side_effect = [30, 10]

    interval = 2  # Every 2 frames
    fps = 30
    processed_images = process_video_images('path/to/video.mp4', 'path/to/output', interval, fps)

    assert processed_images == 5  # 10 frames, saving every 2 frames
    assert mock_save_image.call_count == 5