import os

def create_annotated_directory(new_frames_path):
    annotated_dir = os.path.join(new_frames_path, 'annotated')
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