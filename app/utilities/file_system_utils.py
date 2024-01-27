import os
import re

def create_file_directory(video_dir):
    new_dir = os.path.join(video_dir)
    os.makedirs(new_dir, exist_ok=True)
    return new_dir

def create_annotated_directory(new_frames_path):
    annotated_dir = os.path.join(new_frames_path, 'annotated')
    os.makedirs(annotated_dir, exist_ok=True)
    return annotated_dir