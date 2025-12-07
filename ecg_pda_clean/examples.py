"""
Example: How to use the ECG Scanpath PDA system
"""

from aoi_mapper import AOIMapper, Fixation
from task_inference import TaskInferencer
from pda import PushdownAutomaton
from completion import ScanpathCompleter
from main import ECGScanpathAnalyzer


def example_1_simple_fixations():
    """Example 1: Process simple fixation list"""
    print("="*70)
    print("EXAMPLE 1: Simple Fixation Processing")
    print("="*70)
    
    # Create fixation data
    fixations = [
        Fixation(320, 120, 210, 1.0),
        Fixation(680, 520, 260, 1.5),
        Fixation(100, 150, 230, 2.0),
        Fixation(1250, 150, 240, 2.5),
        Fixation(100, 280, 300, 3.0),
    ]
    
    # Step 1: Map to leads
    mapper = AOIMapper()
    leads = mapper.convert_fixations_to_lead_sequence(fixations)
    print(f"\nLead sequence: {' → '.join(leads)}")
    
    # Step 2: Infer tasks
    inferencer = TaskInferencer()
    tasks = inferencer.infer_tasks(leads)
    print(f"Task sequence: {' → '.join(tasks)}")
    
    # Step 3: Process with PDA
    pda = PushdownAutomaton()
    accepted = pda.process_sequence(tasks)
    print(f"Accepted: {accepted}")
    print(f"Complete: {pda.accepts()}")
    print(f"Missing: {pda.get_missing_tasks()}")
    print()


def example_2_complete_pipeline():
    """Example 2: Use complete analysis pipeline"""
    print("="*70)
    print("EXAMPLE 2: Complete Analysis Pipeline")
    print("="*70)
    
    # Incomplete scanpath
    fixations = [
        Fixation(320, 120, 210, 1.0),   # II
        Fixation(680, 550, 180, 1.3),   # RHYTHM
        Fixation(100, 280, 300, 2.0),   # V1
        Fixation(350, 280, 320, 2.5),   # V2
    ]
    
    # Analyze
    analyzer = ECGScanpathAnalyzer()
    results = analyzer.analyze_fixations(fixations)
    
    print(f"\nResults:")
    print(f"  Complete: {results['is_complete']}")
    print(f"  Missing: {results['missing_tasks']}")
    print(f"  Suggested: {' → '.join(results['completed_sequence'])}")
    print()


def example_3_load_from_csv():
    """Example 3: Load from CSV file"""
    print("="*70)
    print("EXAMPLE 3: Load Fixations from CSV")
    print("="*70)
    
    # You can use pandas to load CSV
    # For this example, we'll manually create data
    
    # Simulated CSV data
    csv_data = """x,y,duration_ms,timestamp
320,120,210,1.0
680,520,260,1.5
100,150,230,2.0"""
    
    # Parse (in real usage, use pandas)
    fixations = [
        Fixation(320, 120, 210, 1.0),
        Fixation(680, 520, 260, 1.5),
        Fixation(100, 150, 230, 2.0),
    ]
    
    # Process
    mapper = AOIMapper()
    leads = mapper.convert_fixations_to_lead_sequence(fixations)
    print(f"\nLead sequence from CSV: {' → '.join(leads)}")
    print()


def example_4_completion():
    """Example 4: Scanpath completion"""
    print("="*70)
    print("EXAMPLE 4: Scanpath Completion")
    print("="*70)
    
    # Incomplete task sequence
    incomplete = ['R', 'Rh', 'Ax', 'Q', 'Detail']
    
    print(f"\nIncomplete: {' → '.join(incomplete)}")
    
    # Complete it
    completer = ScanpathCompleter()
    completed = completer.complete_scanpath(incomplete)
    
    print(f"Completed:  {' → '.join(completed)}")
    
    # Validate
    valid = completer.validate_completion(completed)
    print(f"Valid: {valid}")
    print()


def example_5_pda_trace():
    """Example 5: View PDA execution trace"""
    print("="*70)
    print("EXAMPLE 5: PDA Execution Trace")
    print("="*70)
    
    pda = PushdownAutomaton()
    sequence = ['R', 'Rh', 'Ax', 'Q', 'Detail']
    
    print(f"\nProcessing: {' → '.join(sequence)}")
    pda.process_sequence(sequence)
    
    # Print detailed trace
    pda.print_trace()
    print()


if __name__ == "__main__":
    # Run all examples
    example_1_simple_fixations()
    example_2_complete_pipeline()
    example_3_load_from_csv()
    example_4_completion()
    example_5_pda_trace()
    
    print("="*70)
    print("ALL EXAMPLES COMPLETED")
    print("="*70)
