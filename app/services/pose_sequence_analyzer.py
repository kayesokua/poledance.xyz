import re

class PoseSequenceAnalyzer:
    def __init__(self, data, ref_tricks):
        self.data = data
        self.ref_tricks = ref_tricks
        self.trick_match_count = 0
        self.trick_undefined_count = 0
        self.spin_count = self.get_total_spin_count()
        self.inversion_count = self.get_total_inversions()
        self.data['pos_trick'] = self.data.apply(self.get_pole_trick, axis=1)
        
    def get_total_spin_count(self):
        spin_count = 0
        faces = self.data['pos_face'].tolist()
    
        for i in range(2, len(faces)):
            if faces[i] != faces[i - 2] and faces[i] == faces[i - 1]:
                spin_count += 1

        return spin_count
        
    def get_total_inversions(self):
        inversion_count = 0
        bodies = self.data['pos_body'].tolist()
        
        for i in range(3, len(bodies)):
            if bodies[i] == 'inversion' and bodies[i - 1] != 'inversion' and bodies[i + 1] != 'inversion':
                inversion_count += 1
        return inversion_count
        
    def get_pole_trick(self, row):
        columns = self.data.columns
        l_cols = [col for col in columns if col.endswith('_x') or col.endswith('_y')]
        d_cols = sorted([col for col in self.data.columns if col.startswith('d_')]) 
        a_cols = sorted([col for col in self.data.columns if col.startswith('a_')])
        scores = {}
        for _, ref_row in self.ref_tricks.iterrows():
            a_score = sum(1 for col in a_cols if abs(row[col] - ref_row[col]) < 35)
            d_score = sum(1 for col in d_cols if abs(row[col] - ref_row[col]) < 0.25)
            l_score = sum(1 for col in l_cols if abs(row[col] - ref_row[col]) < 0.2)
            total_score = a_score + d_score + l_score
            scores[ref_row['pose_name']] = total_score
            
        max_score_pose = max(scores, key=scores.get)
        max_score = scores[max_score_pose]

        if max_score < 20:
            return 'None'
        else:
            suffixes_to_remove = r'(-rgt|-lft|-inv|-rgt-inv|-lft-inv|-center|)$'
            closest_match = re.sub(suffixes_to_remove, '', max_score_pose)
            return closest_match