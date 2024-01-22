import os
import cv2
import numpy as np

from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2

def draw_landmarks_on_image(image_rgb, detection_result):
    pose_landmarks_list = detection_result.pose_landmarks
    annotated_image = np.copy(image_rgb)
    for idx, pose_landmarks in enumerate(pose_landmarks_list):
        pose_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
        pose_landmarks_proto.landmark.extend([
            landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in pose_landmarks])
        solutions.drawing_utils.draw_landmarks(
            annotated_image,
            pose_landmarks_proto,
            solutions.pose.POSE_CONNECTIONS,
            solutions.drawing_styles.get_default_pose_landmarks_style())
    return annotated_image

def annotate_and_save_image(annotated_dir, image_filename, detection_result, image_rgb, scale):
    annotated_image = draw_landmarks_on_image(image_rgb, detection_result)
    width, height = int(annotated_image.shape[1] * scale), int(annotated_image.shape[0] * scale)
    resized_image = cv2.resize(annotated_image, (width, height), interpolation=cv2.INTER_AREA)
    annotated_image_rgb = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)
    annotated_image_path = os.path.join(annotated_dir, image_filename)
    cv2.imwrite(annotated_image_path, annotated_image_rgb)