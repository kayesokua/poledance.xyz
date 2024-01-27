import os
import cv2
import pandas as pd

import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

from app.utilities.file_system_utils import *
from app.utilities.image_utils import *

def initialize_landmarker(model_path):
    base_options = python.BaseOptions(model_asset_path=model_path)
    options = vision.PoseLandmarkerOptions(base_options=base_options, output_segmentation_masks=True)
    return vision.PoseLandmarker.create_from_options(options)

def populate_pose_data_with_landmarks(pose_info, landmarks):
    for idx, landmark in enumerate(landmarks):
        idx_str = str(idx).zfill(2)
        pose_info[f'landmark_{idx_str}_x'] = landmark.x
        pose_info[f'landmark_{idx_str}_y'] = landmark.y
        pose_info[f'landmark_{idx_str}_z'] = landmark.z
        pose_info[f'landmark_{idx_str}_v'] = landmark.visibility
        
def generate_pose_landmark_dictionary(source_dir, model_path, is_video=False):
    annotated_dir = create_annotated_directory(source_dir)
    filenames = get_image_filenames(source_dir)
    landmarker = initialize_landmarker(model_path)

    if is_video:
        pose_data, errors = batch_process_video_images(annotated_dir, filenames, landmarker)
    else:
        pose_data, errors = batch_process_static_images(annotated_dir, filenames, landmarker)
    
    pose_data_df = pd.DataFrame(pose_data)
    pose_data_df.to_csv(f'{source_dir}/pose_data_raw.csv', index=False)
    
    errors = write_error_log(source_dir, errors)
    
    return True

def batch_process_video_images(annotated_dir, filenames, landmarker):
    pose_data = []
    errors = []

    for image_file_path in sorted(filenames):
        
        image_bgr = cv2.imread(image_file_path, cv2.IMREAD_COLOR)
        image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image_rgb)

        image_filename, second, frame_no = parse_video_filename(image_file_path)
        detection_result = landmarker.detect(mp_image)

        if detection_result.pose_landmarks:
            annotate_and_save_image(annotated_dir, image_filename, detection_result, image_rgb, scale=0.4)
            
            for landmarks in detection_result.pose_landmarks:
                pose_info = {
                    'image_filename': image_filename,
                    'secs': second,
                    'frame_no': frame_no
                }
                populate_pose_data_with_landmarks(pose_info, landmarks)
            pose_data.append(pose_info)
        else:
            errors.append(image_file_path)
    
    return pose_data, errors

def batch_process_static_images(annotated_dir, filenames, landmarker):
    
    pose_data = []
    errors = []

    for image_file_path in sorted(filenames):
        
        image_bgr = cv2.imread(image_file_path, cv2.IMREAD_COLOR)
        image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image_rgb)

        image_filename = os.path.basename(image_file_path)        
        pose_name = image_filename.split('.')[0]
        
        detection_result = landmarker.detect(mp_image)
        
        if detection_result.pose_landmarks:
            annotate_and_save_image(annotated_dir, image_filename, detection_result, image_rgb, scale=1)
            
            for landmarks in detection_result.pose_landmarks:
                pose_info = {
                    'image_filename': image_filename,
                    'pose_name': pose_name
                }
                populate_pose_data_with_landmarks(pose_info, landmarks)
            pose_data.append(pose_info)
        else:
            errors.append(image_file_path)
    
    return pose_data, errors