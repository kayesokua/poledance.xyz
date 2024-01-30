import os
import cv2
import matplotlib
matplotlib.use('agg')

import matplotlib.pyplot as plt

def generate_timeline_image(annotated_dir, data):
    total_frames = len(data)
    plt.rcParams.update({'font.size': 10})
    plt.rcParams['figure.constrained_layout.use'] = True

    image_files = sorted([f for f in os.listdir(annotated_dir) if f.endswith('.png')])
    
    fig, axs = plt.subplots(1, total_frames, figsize=(total_frames*2, 2))
    if total_frames == 1:
        axs = [axs]
    
    for i, image_file in enumerate(image_files[:total_frames]):        
        img = cv2.imread(os.path.join(annotated_dir, image_file))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        axs[i].imshow(img)
        axs[i].set_title(f"{i}")
        axs[i].axis('off')
        i+=1
    
    for j in range(len(image_files), total_frames):
        axs[j].axis('off')

    plt.tight_layout()
    plt.savefig(f"{annotated_dir}/timeline.png", dpi=150)
    plt.close(fig)
    return True