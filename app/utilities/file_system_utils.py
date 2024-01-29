import os
import re

def create_file_directory(video_dir):
    new_dir = os.path.join(video_dir)
    os.makedirs(new_dir, exist_ok=True)
    return new_dir

def create_annotated_directory(video_dir):
    annotated_dir = os.path.join(video_dir, 'annotated')
    os.makedirs(annotated_dir, exist_ok=True)
    return annotated_dir

def get_image_filenames(new_frames_path):
    return [os.path.join(new_frames_path, f) for f in os.listdir(new_frames_path) if f.endswith(".png")]

def write_error_log(new_frames_path, errors):
    if errors:
        with open(f"{new_frames_path}/pose_landmark_errors.txt", "w") as file:
            for error in errors:
                file.write(f"{error}\n")

def parse_video_filename(image_file_path):
    image_filename = os.path.basename(image_file_path)
    parts = image_filename.split('_')
    second = int(parts[0])
    frame_no = int(parts[1].split('.')[0])
    return image_filename, second, frame_no

def remove_filename_prefixes(source_dir, prefix_pattern):
    for filename in os.listdir(source_dir):
        if filename.lower().endswith('.png') and re.match(prefix_pattern, filename):
            new_filename = re.sub(prefix_pattern, '', filename)
            old_path = os.path.join(source_dir, filename)
            new_path = os.path.join(source_dir, new_filename)
            os.rename(old_path, new_path)
            print(f"Renamed '{filename}' to '{new_filename}'")
            
def clean_pose_name(name):
    name = re.sub(r'-(lft|rgt|lft-inv|rgt-inv)$', '', name)  # Remove specific suffixes
    name = name.replace('-', ' ')  # Replace hyphens with spaces
    return name