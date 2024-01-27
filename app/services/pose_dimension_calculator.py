import numpy as np
import pandas as pd
from scipy.stats import mode

class PoseDimensionCalculator:
    
    def __init__(self, data, is_video=False):
        self.data = data
        
        self.enhance_pose_landmarks = self.enhance_pose_landmarks()
        self.data = self.enhance_pose_landmarks

        distances = self.calculate_distances()
        self.data = pd.concat([self.data, distances], axis=1)
        
        angles = self.calculate_connected_joint_range()
        self.data = pd.concat([self.data, angles], axis=1)

        if is_video:
            merged_data = self.calculate_rate_of_change()
            self.data = merged_data
    

    def enhance_pose_landmarks(self):
        enhanced_data = []
        for index, row in self.data.iterrows():
            enhanced_row = self.process_row(row)
            enhanced_row['index'] = index
            enhanced_data.append(enhanced_row)
        enhanced_df = pd.DataFrame(enhanced_data).set_index('index')  # Set the index of the DataFrame
        merged = pd.concat([self.data, enhanced_df], axis=1)  # Merge with the original DataFrame
        return merged

    def process_row(self, row):
        x_cols = sorted([col for col in self.data.columns if col.endswith('_x')])
        y_cols = sorted([col for col in self.data.columns if col.endswith('_y')])
        z_cols = sorted([col for col in self.data.columns if col.endswith('_z')])
        
        x = row[x_cols].values
        y = row[y_cols].values
        z = row[z_cols].values

        enhanced_row = {
            
            'head_x': x[0:10].mean(),
            'head_y': y[0:10].mean(),
            'head_z': z[0:10].mean(),
            'chest_x': x[11:13].mean(),
            'chest_y': y[11:13].mean(), 
            'chest_z': z[11:13].mean(),
            'stomach_x': (x[11:13].mean() + x[23:24].mean()) / 2,
            'stomach_y': (y[11:13].mean() + y[23:24].mean()) / 2,
            'stomach_z': (z[11:13].mean() + z[23:24].mean()) / 2,
            'hip_x': x[23:25].mean(),
            'hip_y': y[23:25].mean(),
            'hip_z': z[23:25].mean(),
            
            'knuckles_right_x': (x[18] + x[20])/2,
            'knuckles_right_y': (y[18] + y[20])/2,
            'knuckles_right_z': (z[18] + z[20])/2,
            'knuckles_left_x': (x[17] + x[19])/2,
            'knuckles_left_y': (y[17] + y[19])/2,
            'knuckles_left_z': (z[17] + z[19])/2,
        }

        return enhanced_row

    def calculate_pose_distance(self, Ax, Ay, Bx, By):
        distance = np.sqrt((self.data[Ax] - self.data[Bx])**2 + (self.data[Ay] - self.data[By])**2)
        return np.round(distance, 4)

    def calculate_distances(self):
        dist = pd.DataFrame(index=self.data.index)
        
        dist['dist_head_to_rgt_knee'] = self.calculate_pose_distance('head_x', 'head_y', 'landmark_26_x', 'landmark_26_y')
        dist['dist_head_to_lft_knee'] = self.calculate_pose_distance('head_x', 'head_y', 'landmark_25_x', 'landmark_25_y')
        dist['dist_head_to_rgt_ankle'] = self.calculate_pose_distance('head_x', 'head_y', 'landmark_28_x', 'landmark_28_y')
        dist['dist_head_to_lft_ankle'] = self.calculate_pose_distance('head_x', 'head_y', 'landmark_27_x', 'landmark_27_y')
        dist['dist_rgt_shoulder_to_wrist'] = self.calculate_pose_distance('landmark_12_x', 'landmark_12_y', 'landmark_16_x', 'landmark_16_y')
        dist['dist_lft_shoulder_to_wrist'] = self.calculate_pose_distance('landmark_11_x', 'landmark_11_y', 'landmark_15_x', 'landmark_15_y')
        dist['dist_rgt_shoulder_to_knee'] = self.calculate_pose_distance('landmark_12_x', 'landmark_12_y', 'landmark_26_x', 'landmark_26_y')
        dist['dist_lft_shoulder_to_knee'] = self.calculate_pose_distance('landmark_11_x', 'landmark_11_y', 'landmark_25_x', 'landmark_25_y')
        dist['dist_rgt_elbow_to_hip'] = self.calculate_pose_distance('landmark_14_x', 'landmark_14_y', 'landmark_24_x', 'landmark_24_y')
        dist['dist_lft_elbow_to_hip'] = self.calculate_pose_distance('landmark_13_x', 'landmark_13_y', 'landmark_23_x', 'landmark_23_y')        
        dist['dist_rgt_hip_to_wrist'] = self.calculate_pose_distance('landmark_24_x', 'landmark_24_y', 'landmark_16_x', 'landmark_16_y')
        dist['dist_lft_hip_to_wrist'] = self.calculate_pose_distance('landmark_23_x', 'landmark_23_y', 'landmark_15_x', 'landmark_15_y')
        
        dist['dist_bet_wrists'] = self.calculate_pose_distance('landmark_16_x', 'landmark_16_y', 'landmark_15_x', 'landmark_15_y')
        dist['dist_bet_elbows'] = self.calculate_pose_distance('landmark_14_x', 'landmark_14_y', 'landmark_13_x', 'landmark_13_y')
        dist['dist_bet_knees'] = self.calculate_pose_distance('landmark_26_x', 'landmark_26_y', 'landmark_25_x', 'landmark_25_y')
        dist['dist_bet_ankles'] = self.calculate_pose_distance('landmark_28_x', 'landmark_28_y', 'landmark_27_x', 'landmark_27_y')
        
        return dist

    def calculate_pose_angle(self, Ax, Ay, Bx, By, Cx, Cy):
        A = self.data[[Ax, Ay]].values
        B = self.data[[Bx, By]].values
        C = self.data[[Cx, Cy]].values
        BA = A - B
        BC = C - B
        angle_BA = np.arctan2(BA[:, 1], BA[:, 0])
        angle_BC = np.arctan2(BC[:, 1], BC[:, 0])
        angle_difference = np.degrees(angle_BC - angle_BA)    
        return np.round(angle_difference, 4)
        
    def calculate_connected_joint_range(self):
        
        angles = pd.DataFrame(index=self.data.index)
        
        angles['a_head_to_stomach'] = self.calculate_pose_angle('head_x', 'head_y', 'chest_x', 'chest_y','stomach_x','stomach_y')
        angles['a_chest_to_hip'] = self.calculate_pose_angle('chest_x', 'chest_y', 'stomach_x', 'stomach_y','hip_x','hip_y')
        angles['a_mid_hip_to_knees'] = self.calculate_pose_angle('landmark_26_x','landmark_26_y','hip_x', 'hip_y','landmark_25_x','landmark_25_y')
        angles['a_rgt_shoulder_to_wrist'] = self.calculate_pose_angle('landmark_12_x', 'landmark_12_y', 'landmark_14_x', 'landmark_14_y', 'landmark_16_x', 'landmark_16_y')
        angles['a_rgt_elbow_to_knuckles'] = self.calculate_pose_angle('landmark_14_x', 'landmark_14_y', 'landmark_16_x', 'landmark_16_y', 'knuckles_right_x', 'knuckles_right_y')               
        angles['a_rgt_thumb_to_knuckles'] = self.calculate_pose_angle('landmark_22_x', 'landmark_22_y', 'landmark_18_x', 'landmark_18_y', 'knuckles_right_x', 'knuckles_right_y')       
        angles['a_rgt_shoulder_to_knee'] = self.calculate_pose_angle('landmark_12_x', 'landmark_12_y', 'landmark_24_x', 'landmark_24_y','landmark_26_x', 'landmark_26_y')
        angles['a_rgt_hip_to_foot'] = self.calculate_pose_angle('landmark_24_x', 'landmark_24_y', 'landmark_26_x', 'landmark_26_y','landmark_28_x', 'landmark_28_y')
        angles['a_rgt_foot_to_ankle'] = self.calculate_pose_angle('landmark_26_x', 'landmark_26_y', 'landmark_28_x', 'landmark_28_y','landmark_32_x', 'landmark_32_y')
        angles['a_lft_shoulder_to_wrist'] = self.calculate_pose_angle('landmark_11_x', 'landmark_11_y', 'landmark_13_x', 'landmark_13_y', 'landmark_15_x', 'landmark_15_y')
        angles['a_lft_elbow_to_knuckles'] = self.calculate_pose_angle('landmark_13_x', 'landmark_13_y', 'landmark_15_x', 'landmark_15_y', 'knuckles_left_x', 'knuckles_left_y')               
        angles['a_lft_thumb_to_knuckles'] = self.calculate_pose_angle('landmark_21_x', 'landmark_21_y', 'landmark_17_x', 'landmark_17_y', 'knuckles_left_x', 'knuckles_left_y')       
        angles['a_lft_shoulder_to_knee'] = self.calculate_pose_angle('landmark_11_x', 'landmark_11_y', 'landmark_23_x', 'landmark_23_y','landmark_25_x', 'landmark_25_y')
        angles['a_lft_hip_to_foot'] = self.calculate_pose_angle('landmark_23_x', 'landmark_23_y', 'landmark_25_x', 'landmark_25_y','landmark_27_x', 'landmark_27_y')
        angles['a_lft_foot_to_ankle'] = self.calculate_pose_angle('landmark_25_x', 'landmark_25_y', 'landmark_27_x', 'landmark_27_y','landmark_31_x', 'landmark_31_y')
        return angles
        
    def calculate_rate_of_change(self):
        secs_counts = self.data.groupby('secs').size()
        fps = secs_counts.max()

        d_cols = sorted([col for col in self.data.columns if col.startswith('dist_')])

        grouped_data = self.data.groupby('secs')[d_cols].mean()
        roc_data = pd.DataFrame(index=grouped_data.index)
        
        for col in d_cols:
            differences = grouped_data[col].diff().fillna(0)
            roc_data[f'r_{col}'] = differences * fps
            
        merged_data = pd.merge(self.data, roc_data, on='secs', how='left')
        return merged_data