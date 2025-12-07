"""
Main pipeline: Raw fixations → Lead sequence → Task sequence → PDA → Completion
"""

from typing import List
from aoi_mapper import AOIMapper, Fixation
from task_inference import TaskInferencer
from pda import PushdownAutomaton
from completion import ScanpathCompleter


class ECGScanpathAnalyzer:
    """Complete ECG scanpath analysis pipeline"""
    
    def __init__(self):
        self.aoi_mapper = AOIMapper()
        self.task_inferencer = TaskInferencer()
        self.pda = PushdownAutomaton()
        self.completer = ScanpathCompleter()
    
    def analyze_fixations(self, fixations: List[Fixation]) -> dict:
        """
        Complete analysis pipeline
        
        Args:
            fixations: Raw eye-tracking fixations
            
        Returns:
            Analysis results dictionary
        """
        print("="*60)
        print("ECG SCANPATH ANALYSIS PIPELINE")
        print("="*60)
        
        # Step 1: Fixations → Lead sequence (Algorithm 1)
        print("\n[Step 1] Converting fixations to lead sequence...")
        lead_sequence = self.aoi_mapper.convert_fixations_to_lead_sequence(fixations)
        print(f"Lead sequence: {' → '.join(lead_sequence)}")
        
        # Step 2: Lead → Task inference
        print("\n[Step 2] Inferring diagnostic tasks...")
        task_sequence = self.task_inferencer.infer_tasks(lead_sequence)
        print(f"Task sequence: {' → '.join(task_sequence)}")
        
        # Step 3: PDA processing
        print("\n[Step 3] Processing through PDA...")
        self.pda.reset()
        accepted = self.pda.process_sequence(task_sequence)
        
        # Step 4: Check completeness
        print("\n[Step 4] Checking diagnostic completeness...")
        is_complete = self.pda.accepts()
        missing_tasks = self.pda.get_missing_tasks()
        
        if is_complete:
            print("✅ Examination is COMPLETE")
        else:
            print(f"⚠️  Examination is INCOMPLETE")
            print(f"   Missing tasks: {missing_tasks}")
        
        # Step 5: Generate completion if needed
        completed_sequence = task_sequence
        if not is_complete:
            print("\n[Step 5] Generating completion...")
            completed_sequence = self.completer.complete_scanpath(task_sequence)
        
        # Return results
        return {
            'lead_sequence': lead_sequence,
            'task_sequence': task_sequence,
            'is_complete': is_complete,
            'missing_tasks': missing_tasks,
            'completed_sequence': completed_sequence,
            'pda_history': self.pda.history,
            'final_state': self.pda.current_state,
            'final_stack': self.pda.stack
        }


def main():
    """Example usage"""
    
    # Example 1: Complete expert scanpath
    print("\n" + "="*60)
    print("EXAMPLE 1: Complete Expert Scanpath")
    print("="*60)
    
    complete_fixations = [
        Fixation(320, 120, 210, 1.0),   # II (Rate)
        Fixation(680, 550, 260, 1.5),   # RHYTHM
        Fixation(100, 150, 230, 2.0),   # I (Axis)
        Fixation(1250, 150, 240, 2.5),  # aVF
        Fixation(100, 280, 300, 3.0),   # V1 (QRS)
        Fixation(350, 280, 220, 3.5),   # V2
        Fixation(600, 280, 250, 4.0),   # V3 (ST)
        Fixation(850, 280, 230, 4.5),   # V4 (T-wave)
    ]
    
    analyzer = ECGScanpathAnalyzer()
    results1 = analyzer.analyze_fixations(complete_fixations)
    
    # Example 2: Incomplete novice scanpath
    print("\n\n" + "="*60)
    print("EXAMPLE 2: Incomplete Novice Scanpath")
    print("="*60)
    
    incomplete_fixations = [
        Fixation(320, 120, 210, 1.0),   # II
        Fixation(680, 550, 180, 1.3),   # RHYTHM
        Fixation(100, 280, 300, 2.0),   # V1
        Fixation(350, 280, 320, 2.5),   # V2
        Fixation(600, 280, 290, 3.0),   # V3
        # Missing: axis, ST, T-wave checks
    ]
    
    analyzer2 = ECGScanpathAnalyzer()
    results2 = analyzer2.analyze_fixations(incomplete_fixations)
    
    print("\n" + "="*60)
    print("ANALYSIS COMPLETE")
    print("="*60)


if __name__ == "__main__":
    main()
