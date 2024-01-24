import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from matplotlib.patches import FancyArrowPatch, Arc
from .file_system_utils import parse_video_filename



def visualize_pose_dimension_lengths(filepath, row, focus_heights):
    fig, axs = plt.subplots(1, 2, figsize=(10, 5))
    
    colors = ['red', 'blue', 'green', 'purple', 'orange','magenta']
    color_index = 0 
    
    axs[0].set_title("Height and Width Visualization")
    
    for label, (height, P1x, P1y, P2x, P2y) in focus_heights.items():
        axs[0].plot([P1x, P2x], [P1y, P2y], color=colors[color_index], linewidth=2)
        axs[0].text(P1x + 0.1, P1y, f"{label}: {height:.2f}")
        axs[0].scatter(P1x, P1y, color=colors[color_index])
        axs[0].scatter(P2x, P2y, color=colors[color_index])
        color_index = (color_index + 1) % len(colors)
        
    axs[0].set_xlim(0, 1)
    axs[0].set_ylim(0, 1)
    axs[0].invert_yaxis()
    axs[0].set_xticks(np.arange(0, 1.05, 0.1))
    axs[0].set_yticks(np.arange(0, 1.05, 0.1))
    axs[0].grid(True)

    filename = filepath + row['image_filename']
    img = Image.open(filename)
    axs[1].imshow(img)
    axs[1].set_title(f"Image with Landmark: {row['image_filename']}")
    axs[1].axis('off')

    plt.show()

def visualize_pose_dimension_angles(filepath, row, focus_angles):
    fig, axs = plt.subplots(1, 2, figsize=(10, 5))
    
    colors = ['red', 'blue', 'green', 'purple', 'orange','magenta']
    color_index = 0 
    
    axs[0].set_title("Angle Visualization")
    
    arrow_length = 1

    for label, (angle, Ax, Ay, Bx, By, Cx, Cy) in focus_angles.items():
        direction = 1 if angle < 180 else -1
        angle_rad = np.radians(angle)
        
        arrow_length = 10
        arrow_end_Ax = Ax + direction * arrow_length * np.cos(angle_rad)
        arrow_end_Ay = Ay + direction * arrow_length * np.sin(angle_rad)
        arrow_end_Cx = Cx + direction * arrow_length * np.cos(angle_rad)
        arrow_end_Cy = Cy + direction * arrow_length * np.sin(angle_rad)
        
        axs[0].add_patch(FancyArrowPatch((Bx, By), (Ax, Ay), arrowstyle='->', color=colors[color_index], mutation_scale=10))
        axs[0].add_patch(FancyArrowPatch((Bx, By), (Cx, Cy), arrowstyle='->', color=colors[color_index], mutation_scale=10))
        axs[0].text(Bx + 0.1, By, f"{label}: {angle:.2f}°")
        axs[0].scatter(Bx, By, color=colors[color_index])
        
        # Compute and draw angle arcs
        AB_rad = np.arctan2(Ay - By, Ax - Bx)
        CB_rad = np.arctan2(Cy - By, Cx - Bx)
        AB_rad_deg = np.degrees(AB_rad) % 360
        CB_rad_deg = np.degrees(CB_rad) % 360
        theta1, theta2 = (CB_rad_deg, AB_rad_deg) if AB_rad_deg < CB_rad_deg else (AB_rad_deg, CB_rad_deg + 360)
        angle_arc = Arc((Bx, By), width=0.2, height=0.2, alpha=0.5, angle=0, theta1=theta1, theta2=theta2, edgecolor=colors[color_index], linewidth=2, linestyle='--')
        axs[0].add_patch(angle_arc)
        color_index = (color_index + 1) % len(colors)
        
    axs[0].set_xlim(0, 1)
    axs[0].set_ylim(0, 1)
    axs[0].invert_yaxis()
    axs[0].set_xticks(np.arange(0, 1.05, 0.1))
    axs[0].set_yticks(np.arange(0, 1.05, 0.1))
    axs[0].grid(True)

    filename = filepath + row['image_filename']
    img = Image.open(filename)
    axs[1].imshow(img)
    axs[1].set_title(f"Image with Landmark: {row['image_filename']}")
    axs[1].axis('off')

    plt.show()

def visualize_pose_coordinates(filepath, row, focus_landmarks):
    fig, axs = plt.subplots(1, 2, figsize=(10, 5))

    colors = ['red', 'blue', 'green', 'purple', 'orange', 'magenta']
    color_index = 0

    axs[0].set_title("Landmark Scatter Visualization")

    for label, (Lx, Ly) in focus_landmarks.items():
        axs[0].scatter(Lx, Ly, color=colors[color_index])
        axs[0].text(Lx + 0.1, Ly, f"{label}")
        color_index = (color_index + 1) % len(colors)

    axs[0].set_xlim(0, 1)
    axs[0].set_ylim(0, 1)
    axs[0].invert_yaxis()
    axs[0].set_xticks(np.arange(0, 1.05, 0.1))
    axs[0].set_yticks(np.arange(0, 1.05, 0.1))
    axs[0].grid(True)

    filename = filepath + row['image_filename']
    img = Image.open(filename)
    axs[1].imshow(img)
    axs[1].set_title(f"Image with Landmark: {row['image_filename']}")
    axs[1].axis('off')

    plt.show()
    
def visualize_video_frames_by_second(annotated_image_path_dir, data):
    import os
    import cv2
    from matplotlib import pyplot as plt

    plt.rcParams.update({'font.size': 16})
    plt.rcParams['figure.constrained_layout.use'] = True
    
    total_seconds = data['secs'].max() + 1
    image_files = sorted([f for f in os.listdir(annotated_image_path_dir) if f.endswith('.png')])
    
    nrows = (total_seconds - 1) // 10 + 1
    ncols = min(total_seconds, 10)
    figh = 8 * nrows
    fig, axs = plt.subplots(nrows, ncols, figsize=(24, figh))
    if nrows == 1:
        axs = [axs]
    
    used_seconds = set()
    plot_count = 0
    for image_file in image_files:
        _, second, _ = parse_video_filename(image_file) 

        if second not in used_seconds:
            used_seconds.add(second)
            row_idx, col_idx = divmod(plot_count, 10)
            img = cv2.imread(os.path.join(annotated_image_path_dir, image_file))
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            axs[row_idx][col_idx].imshow(img)
            axs[row_idx][col_idx].set_title(f"Time: {second}")
            axs[row_idx][col_idx].axis('off')
            plot_count += 1
    
    for i in range(plot_count, nrows * ncols):
        row_idx, col_idx = divmod(i, 10)
        axs[row_idx][col_idx].axis('off')

    plt.show()
    

def visualize_roc_trends(data):
    keys = ['dist_rgt_shoulder_to_wrist', 'dist_lft_shoulder_to_wrist']
    
    grouped_data = {key: data.groupby('secs')[key].mean() for key in keys}
    total_seconds = len(data['secs'].unique())
    nrows = total_seconds // 10 + (total_seconds % 10 > 0)
    
    fig, axs = plt.subplots(nrows, 1, figsize=(24, 4 * nrows), squeeze=False, constrained_layout=True)
    
    for i in range(nrows):
        start_sec = i * 10
        end_sec = start_sec + 10

        for key in keys:
            subset = grouped_data[key][start_sec:end_sec]
            axs[i, 0].plot(subset.index, subset, label=key.capitalize())

            threshold = 0.4
            peaks = subset[np.abs(subset) > threshold]
            axs[i, 0].scatter(peaks.index, peaks, label=f'Peaks > 40% {key.capitalize()}')

        axs[i, 0].grid(True)
        axs[i, 0].set_xlabel('Seconds')
        axs[i, 0].set_ylabel('Rate of Change')
        axs[i, 0].set_yticks(np.arange(-1, 1.1, 0.2))
        axs[i, 0].set_title(f'Rate of Change Analysis: Seconds {start_sec} to {end_sec}')
        axs[i, 0].legend()

    plt.show()

