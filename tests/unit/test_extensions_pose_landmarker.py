import pytest
from unittest.mock import patch, MagicMock
from app.extensions.pose_landmarker import initialize_landmarker, generate_pose_landmark_dictionary
import pandas as pd

@pytest.fixture
def mock_vision(mocker):
    return mocker.patch("app.extensions.pose_landmarker.vision")

@pytest.fixture
def mock_files():
    with patch('app.extensions.pose_landmarker.create_annotated_directory') as mock_create_dir,\
         patch('app.extensions.pose_landmarker.get_image_filenames') as mock_get_filenames,\
         patch('app.extensions.pose_landmarker.write_error_log') as mock_write_error_log,\
         patch('pandas.DataFrame.to_csv') as mock_to_csv:
        mock_create_dir.return_value = '/path/to/annotated_dir'
        mock_get_filenames.return_value = ['image1.jpg', 'image2.jpg']
        mock_write_error_log.return_value = None
        mock_to_csv.return_value = None
        yield

@pytest.fixture
def mock_landmarker():
    # Mocking landmarker-related functions
    with patch('app.extensions.pose_landmarker.initialize_landmarker') as mock_initialize,\
         patch('app.extensions.pose_landmarker.batch_process_video_images') as mock_batch_video,\
         patch('app.extensions.pose_landmarker.batch_process_static_images') as mock_batch_static:
        mock_initialize.return_value = MagicMock()
        mock_batch_video.return_value = ([], [])
        mock_batch_static.return_value = ([], [])
        yield

def test_initialize_landmarker_success(mock_vision):
    model_path = "valid/path/to/model"
    landmarker = initialize_landmarker(model_path)
    assert landmarker is not None
    mock_vision.PoseLandmarker.create_from_options.assert_called_once()

def test_initialize_landmarker_failure(mock_vision):
    model_path = "invalid/path/to/model"
    mock_vision.PoseLandmarker.create_from_options.side_effect = Exception("Error")
    with pytest.raises(Exception):
        initialize_landmarker(model_path)

def test_generate_pose_landmark_dictionary_static(mock_files, mock_landmarker):
    source_dir = '/path/to/source'
    model_path = '/path/to/model'
    result = generate_pose_landmark_dictionary(source_dir, model_path, is_video=False)
    assert result is True

def test_generate_pose_landmark_dictionary_video(mock_files, mock_landmarker):
    source_dir = '/path/to/source'
    model_path = '/path/to/model'    
    result = generate_pose_landmark_dictionary(source_dir, model_path, is_video=True)
    assert result is True