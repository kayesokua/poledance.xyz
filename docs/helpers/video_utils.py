import cv2
import os

def is_video_openable(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Could not open video at path {video_path}")
        cap.release()
        return False
    cap.release()
    return True

def get_video_properties(video_path):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    duration_in_seconds = total_frames / fps
    frame_interval = int(0.2 * fps)  # 5 frames per second
    cap.release()
    return fps, frame_interval, duration_in_seconds

def save_video_image(frame, output_dir, frame_count, second):
    frame_file_path = os.path.join(output_dir, f'{second:04d}_{frame_count:08d}.png')
    cv2.imwrite(frame_file_path, frame)
    
def process_video_images(video_path, output_dir, interval, fps):
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    image_count = 0
    max_duration_in_seconds = 6 * 60

    while cap.isOpened():
        current_second = int(frame_count / fps)
        if current_second > max_duration_in_seconds:
            break

        ret, frame = cap.read()
        if ret:
            if frame_count % interval == 0:
                save_video_image(frame, output_dir, frame_count, current_second)
                image_count += 1
            frame_count += 1
        else:
            break
    cap.release()
    return image_count