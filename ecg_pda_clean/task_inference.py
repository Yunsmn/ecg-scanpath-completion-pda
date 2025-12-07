"""
Task-level inference: Convert lead sequences to diagnostic task symbols
"""

from typing import List
from config import TASK_ALPHABET


class TaskInferencer:
    """Infers diagnostic tasks from lead-level scanpath"""
    
    def __init__(self):
        self.rules = self._define_rules()
    
    def _define_rules(self):
        """Define clinical interpretation rules"""
        return {
            'rate_rhythm': {
                'leads': ['II', 'RHYTHM'],
                'tasks': ['R', 'Rh']
            },
            'axis': {
                'pattern': ['I', 'aVF'],
                'task': 'Ax'
            },
            'p_wave': {
                'leads': ['II', 'V1'],
                'focus': 'early',
                'task': 'P'
            },
            'pr_interval': {
                'leads': ['II'],
                'task': 'PR'
            },
            'qrs_morphology': {
                'leads': ['V1', 'V2', 'V3', 'V4', 'V5', 'V6'],
                'task': 'Q'
            },
            'repolarization': {
                'leads': ['V1', 'V2', 'V3', 'V4', 'V5', 'V6'],
                'after_qrs': True,
                'tasks': ['ST', 'T']
            }
        }
    
    def infer_tasks(self, lead_sequence: List[str]) -> List[str]:
        """
        Convert lead sequence to task-level symbols
        
        Args:
            lead_sequence: List of lead names
            
        Returns:
            List of task symbols
        """
        task_sequence = []
        i = 0
        
        while i < len(lead_sequence):
            lead = lead_sequence[i]
            
            # Rate/Rhythm detection
            if lead in ['II', 'RHYTHM']:
                if 'R' not in task_sequence:
                    task_sequence.append('R')
                if 'Rh' not in task_sequence:
                    task_sequence.append('Rh')
                i += 1
                continue
            
            # Axis determination (I + aVF pattern)
            if i < len(lead_sequence) - 1:
                if (lead == 'I' and lead_sequence[i+1] == 'aVF') or \
                   (lead == 'aVF' and i > 0 and lead_sequence[i-1] == 'I'):
                    if 'Ax' not in task_sequence:
                        task_sequence.append('Ax')
                    i += 1
                    continue
            
            # QRS morphology (precordial leads)
            if lead in ['V1', 'V2', 'V3', 'V4', 'V5', 'V6']:
                if 'Q' not in task_sequence:
                    task_sequence.append('Q')
                
                # Check for extended detail inspection
                consecutive_v = self._count_consecutive_precordial(lead_sequence, i)
                if consecutive_v >= 2:
                    task_sequence.append('Detail')
                
                # After QRS, expect repolarization
                if self._is_after_qrs(task_sequence):
                    if 'ST' not in task_sequence:
                        task_sequence.append('ST')
                    if 'T' not in task_sequence:
                        task_sequence.append('T')
                
                i += 1
                continue
            
            i += 1
        
        return task_sequence
    
    def _count_consecutive_precordial(self, sequence: List[str], start_idx: int) -> int:
        """Count consecutive precordial lead fixations"""
        count = 0
        precordial = ['V1', 'V2', 'V3', 'V4', 'V5', 'V6']
        
        for i in range(start_idx, len(sequence)):
            if sequence[i] in precordial:
                count += 1
            else:
                break
        return count
    
    def _is_after_qrs(self, task_sequence: List[str]) -> bool:
        """Check if QRS analysis has been performed"""
        return 'Q' in task_sequence or 'Detail' in task_sequence


# Example usage
if __name__ == "__main__":
    lead_seq = ['II', 'RHYTHM', 'I', 'aVF', 'V1', 'V2', 'V3']
    
    inferencer = TaskInferencer()
    tasks = inferencer.infer_tasks(lead_seq)
    print("Task sequence:", " → ".join(tasks))
