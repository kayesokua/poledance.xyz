import re
import pandas as pd

class PoseSpatialClassifier:
    def __init__(self, data, ref_body, ref_legs, ref_grip):
        self.data = data
        self.ref_body = ref_body
        self.ref_legs = ref_legs
        self.ref_grip = ref_grip

        self.body_match_count = 0
        self.body_undefined_count = 0

        self.legs_match_count = 0
        self.legs_undefined_count = 0

        self.grip_match_count = 0
        self.grip_undefined_count = 0

        self.data['pos_face'] = self.data.apply(self.get_face_position, axis=1)
        self.data['pos_body'] = self.data.apply(self.get_body_position, axis=1)
        self.data['pos_legs'] = self.data.apply(self.get_legs_position, axis=1)
        self.data['pos_grip'] = self.data.apply(self.get_grip_position, axis=1)

    def get_face_position(self, row):
        return "front" if row["head_z"] < 0 else "back"

    def get_body_position(self, row):
        self.body_match_count += 1
        if row['head_y'] > row['chest_y'] > row['stomach_y'] > row['hip_y']:
            return "inversion"
        elif row['head_y'] < row['chest_y'] < row['stomach_y'] < row['hip_y'] and abs(row['head_x'] - row['hip_x']) < 0.2:
            return "upright"
        elif row['head_y'] < row['hip_y'] and abs(row['head_y'] - row['hip_y']) < 0.2:
            return "horizontal"
        else:
            result = self.get_body_position_undefined(row)
            return result        

    def get_body_position_undefined(self, row):
        self.body_undefined_count += 1
        a_cols = ['a_head_to_stomach', 'a_chest_to_hip']
        
        scores = {}
        for _, ref_row in self.ref_body.iterrows():
            score = sum(abs(row[col] - ref_row[col]) for col in a_cols)
            scores[ref_row['pose_name']] = score
    
        closest_match_spec = min(scores, key=scores.get)
        closest_score = scores[closest_match_spec]
    
        if closest_score > 180:
            return 'unknown'
        else:
            suffixes_to_remove = r'(-rgt|-lft|-inv|-rgt-inv|-lft-inv|-center|)$'
            closest_match = re.sub(suffixes_to_remove, '', closest_match_spec)
            return closest_match
    
    def get_legs_position(self, row):
        l_cols = ['landmark_24_x', 'landmark_24_y', 'landmark_26_x', 'landmark_26_y', 'landmark_28_x', 'landmark_28_y',
                  'landmark_23_x', 'landmark_23_y', 'landmark_25_x', 'landmark_26_y', 'landmark_27_x', 'landmark_27_y',]
        a_cols = ['a_mid_hip_to_knees', 'a_rgt_hip_to_foot', 'a_rgt_foot_to_ankle', 'a_lft_hip_to_foot', 'a_lft_foot_to_ankle']
        d_cols = ['dist_head_to_rgt_ankle','dist_head_to_lft_ankle', 'dist_bet_wrists','dist_bet_knees','dist_bet_ankles']
        
        scores = {}
        for _, ref_row in self.ref_legs.iterrows():
            l_score = sum(1 for col in l_cols if abs(row[col] - ref_row[col]) < 0.25)
            a_score = sum(1 for col in a_cols if abs(row[col] - ref_row[col]) < 35)
            d_score = sum(1 for col in d_cols if abs(row[col] - ref_row[col]) < 0.25)
            total_score = l_score + a_score + d_score
            scores[ref_row['pose_name']] = total_score

        max_score_pose = max(scores, key=scores.get)
        max_score = scores[max_score_pose]

        if max_score < 15:
            return 'None'
        else:
            suffixes_to_remove = r'(-rgt|-lft|-inv|-rgt-inv|-lft-inv|-center|)$'
            closest_match = re.sub(suffixes_to_remove, '', max_score_pose)
            return closest_match
        
    def get_legs_position_undefined(self, row):
        self.legs_undefined_count += 1
        columns = self.data.columns
        l_cols = [col for col in columns if col.endswith('_x') or col.endswith('_y')]
        
        scores = {}
        for _, ref_row in self.ref_legs.iterrows():
            l_score = sum(1 for col in l_cols if abs(row[col] - ref_row[col]) < 0.2)
            total_score = l_score
            scores[ref_row['pose_name']] = total_score

        max_score_pose = max(scores, key=scores.get)
        max_score = scores[max_score_pose]

        if max_score < 5:
            return 'None'
        else:
            suffixes_to_remove = r'(-rgt|-lft|-inv|-rgt-inv|-lft-inv|-center|)$'
            closest_match = re.sub(suffixes_to_remove, '', max_score_pose)
            return closest_match
            
    def get_grip_position(self, row):
        l_cols = ['landmark_12_x', 'landmark_12_y', 'landmark_14_x', 'landmark_14_y', 'landmark_16_x', 'landmark_16_y',
                  'landmark_11_x', 'landmark_11_y', 'landmark_13_x', 'landmark_13_y', 'landmark_15_x', 'landmark_15_y',]
        d_cols = ['dist_rgt_shoulder_to_wrist','dist_lft_shoulder_to_wrist','dist_bet_wrists','dist_bet_elbows','dist_rgt_elbow_to_hip','dist_lft_elbow_to_hip']
        a_cols = ['a_rgt_shoulder_to_wrist', 'a_rgt_elbow_to_knuckles','a_lft_shoulder_to_wrist', 'a_lft_elbow_to_knuckles',]
        
        scores = {}
        for _, ref_row in self.ref_grip.iterrows():
            l_score = sum(1 for col in l_cols if abs(row[col] - ref_row[col]) < 0.25)
            a_score = sum(1 for col in a_cols if abs(row[col] - ref_row[col]) < 35)
            d_score = sum(1 for col in d_cols if abs(row[col] - ref_row[col]) < 0.25)
            total_score = l_score + a_score + d_score
            scores[ref_row['pose_name']] = total_score

        max_score_pose = max(scores, key=scores.get)
        max_score = scores[max_score_pose]

        if max_score < 15:
            return 'None'
        else:
            suffixes_to_remove = r'(-rgt|-lft|-inv|-rgt-inv|-lft-inv|-center|)$'
            closest_match = re.sub(suffixes_to_remove, '', max_score_pose)
            return closest_match

    def get_grip_position_undefined(self, row):
        self.grip_undefined_count += 1
        columns = self.data.columns
        l_cols = [col for col in columns if col.endswith('_x') or col.endswith('_y')]
        
        scores = {}
        for _, ref_row in self.ref_grip.iterrows():
            l_score = sum(1 for col in l_cols if abs(row[col] - ref_row[col]) < 0.2)
            total_score = l_score
            scores[ref_row['pose_name']] = total_score

        max_score_pose = max(scores, key=scores.get)
        max_score = scores[max_score_pose]

        if max_score < 5:
            return 'None'
        else:
            suffixes_to_remove = r'(-rgt|-lft|-inv|-rgt-inv|-lft-inv|-center|)$'
            closest_match = re.sub(suffixes_to_remove, '', max_score_pose)
            return closest_match
            
    def save_transformed_data(self, filename):
        self.data.to_csv(filename, index=False)