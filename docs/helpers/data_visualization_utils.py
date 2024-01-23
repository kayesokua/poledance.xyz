import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from matplotlib.patches import FancyArrowPatch, Arc

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