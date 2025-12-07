"""
Example: Incomplete Scanpath Completion with PDA

This demonstrates how the PDA can complete incomplete ECG scanpaths
based on clinical examination patterns.
"""

from completion import ScanpathCompleter
from pda import PushdownAutomaton


def example_1_incomplete_rhythm_analysis():
    """
    Example 1: Incomplete Rhythm Analysis

    Scenario: Doctor started rhythm check but didn't complete it
    Missing: Axis check after rhythm analysis
    """
    print("="*70)
    print("EXAMPLE 1: Incomplete Rhythm Analysis")
    print("="*70)

    completer = ScanpathCompleter()

    # Incomplete: Started rhythm (R) and checked heart rate (Rh) but stopped
    incomplete = ['R', 'Rh']

    print(f"\n Incomplete Scanpath: {' → '.join(incomplete)}")
    print("\n Analysis:")
    print("   - Started: Rhythm assessment")
    print("   - Completed: Heart rate check")
    print("   - Missing: Axis determination")

    # Complete it
    completed = completer.complete_scanpath(incomplete)

    print(f"\n Completed Scanpath: {' → '.join(completed)}")

    # Validate
    is_valid = completer.validate_completion(completed)
    print(f"\n{' VALID' if is_valid else ' INVALID'} - Completion is {'accepted' if is_valid else 'rejected'} by PDA")
    print()


def example_2_incomplete_qrs_examination():
    """
    Example 2: Incomplete QRS Complex Examination

    Scenario: Started QRS analysis but didn't check repolarization
    Missing: ST segment and T wave analysis
    """
    print("="*70)
    print("EXAMPLE 2: Incomplete QRS Examination")
    print("="*70)

    completer = ScanpathCompleter()

    # Incomplete: Checked rhythm, then QRS with detail but stopped
    incomplete = ['R', 'Rh', 'Ax', 'Q', 'Detail']

    print(f"\n Incomplete Scanpath: {' → '.join(incomplete)}")
    print("\n Analysis:")
    print("   - Completed: Rhythm analysis (R → Rh → Ax)")
    print("   - Completed: QRS check with details")
    print("   - Missing: ST segment and T wave analysis")
    print("   - Missing: Final rhythm check")

    # Complete it
    completed = completer.complete_scanpath(incomplete)

    print(f"\n Completed Scanpath: {' → '.join(completed)}")

    # Validate
    is_valid = completer.validate_completion(completed)
    print(f"\n{' VALID' if is_valid else ' INVALID'} - Completion is {'accepted' if is_valid else 'rejected'} by PDA")
    print()


def example_3_incomplete_lead_sequence():
    """
    Example 3: Incomplete Lead Sequence

    Scenario: Examined some precordial leads but didn't complete ST/T analysis
    Missing: ST and T wave checks
    """
    print("="*70)
    print("EXAMPLE 3: Incomplete Lead Sequence")
    print("="*70)

    completer = ScanpathCompleter()

    # Incomplete: Started rhythm, QRS, looked at some leads but didn't check ST/T
    incomplete = ['R', 'Rh', 'Ax', 'Q', 'Detail', 'V1', 'V2']

    print(f"\n Incomplete Scanpath: {' → '.join(incomplete)}")
    print("\n Analysis:")
    print("   - Completed: Rhythm analysis")
    print("   - Completed: QRS analysis with precordial leads (V1, V2)")
    print("   - Missing: ST segment analysis")
    print("   - Missing: T wave analysis")
    print("   - Missing: Final rhythm verification")

    # Complete it
    completed = completer.complete_scanpath(incomplete)

    print(f"\n Completed Scanpath: {' → '.join(completed)}")

    # Validate
    is_valid = completer.validate_completion(completed)
    print(f"\n{' VALID' if is_valid else ' INVALID'} - Completion is {'accepted' if is_valid else 'rejected'} by PDA")
    print()


def example_4_very_incomplete_scanpath():
    """
    Example 4: Very Incomplete Scanpath

    Scenario: Only started rhythm assessment
    Missing: Everything after initial rhythm check
    """
    print("="*70)
    print("EXAMPLE 4: Very Incomplete Scanpath (Early Termination)")
    print("="*70)

    completer = ScanpathCompleter()

    # Very incomplete: Just started
    incomplete = ['R']

    print(f"\n Incomplete Scanpath: {' → '.join(incomplete)}")
    print("\n Analysis:")
    print("   - Started: Rhythm assessment")
    print("   - Missing: Heart rate (Rh)")
    print("   - Missing: Axis (Ax)")
    print("   - Missing: All QRS, ST, T analysis")

    # Complete it
    completed = completer.complete_scanpath(incomplete)

    print(f"\n Completed Scanpath: {' → '.join(completed)}")

    # Validate
    is_valid = completer.validate_completion(completed)
    print(f"\n{' VALID' if is_valid else 'INVALID'} - Completion is {'accepted' if is_valid else 'rejected'} by PDA")
    print()


def example_5_already_complete():
    """
    Example 5: Already Complete Scanpath

    Scenario: Complete examination - should not add anything
    """
    print("="*70)
    print("EXAMPLE 5: Already Complete Scanpath")
    print("="*70)

    completer = ScanpathCompleter()

    # Complete scanpath
    complete = ['R', 'Rh', 'Ax', 'Q', 'Detail', 'ST', 'T', 'R']

    print(f"\n Scanpath: {' → '.join(complete)}")
    print("\n Analysis:")
    print("   - Complete rhythm analysis")
    print("   - Complete QRS analysis")
    print("   - Complete repolarization (ST, T)")
    print("   - Final rhythm check")

    # Try to complete (should detect it's already complete)
    result = completer.complete_scanpath(complete)

    print(f"\n Result: {' → '.join(result)}")
    print(f"   Length: {len(complete)} → {len(result)}")

    if len(result) == len(complete):
        print("\nNo changes needed - scanpath was already complete!")

    print()


def example_6_compare_incomplete_vs_complete():
    """
    Example 6: Side-by-side comparison

    Shows what PDA does with incomplete vs complete scanpaths
    """
    print("="*70)
    print("EXAMPLE 6: Comparison - Incomplete vs Complete")
    print("="*70)

    pda = PushdownAutomaton()

    # Test incomplete
    incomplete = ['R', 'Rh', 'Ax', 'Q', 'Detail']
    print(f"\n Testing Incomplete: {' → '.join(incomplete)}")

    pda.reset()
    pda.process_sequence(incomplete)
    print(f"   State: {pda.current_state}")
    print(f"   Stack: {pda.stack}")
    print(f"   Accepts: {pda.accepts()}")
    print(f"   Missing: {pda.get_missing_tasks()}")

    # Test complete
    complete = ['R', 'Rh', 'Ax', 'Q', 'Detail', 'ST', 'T', 'R']
    print(f"\nTesting Complete: {' → '.join(complete)}")

    pda.reset()
    pda.process_sequence(complete)
    print(f"   State: {pda.current_state}")
    print(f"   Stack: {pda.stack}")
    print(f"   Accepts: {pda.accepts()}")
    print(f"   Missing: {pda.get_missing_tasks()}")

    print()


def example_7_multiple_incomplete_patterns():
    """
    Example 7: Multiple Incomplete Patterns

    Shows different types of incomplete patterns
    """
    print("="*70)
    print("EXAMPLE 7: Multiple Incomplete Patterns")
    print("="*70)

    completer = ScanpathCompleter()

    patterns = [
        (['R'], "Rhythm only"),
        (['R', 'Rh'], "Rhythm + Heart Rate"),
        (['R', 'Rh', 'Ax'], "Complete rhythm, no QRS"),
        (['R', 'Rh', 'Ax', 'Q'], "Started QRS"),
        (['R', 'Rh', 'Ax', 'Q', 'ST'], "Missing T wave"),
    ]

    for incomplete, description in patterns:
        print(f"\n{'─'*70}")
        print(f"Pattern: {description}")
        print(f"Input:  {' → '.join(incomplete)}")

        completed = completer.complete_scanpath(incomplete)

        print(f"Output: {' → '.join(completed)}")

        is_valid = completer.validate_completion(completed)
        print(f"Valid:  {'' if is_valid else ''}")

    print()


if __name__ == "__main__":
    print("\n")
    print("╔" + "═"*68 + "╗")
    print("║" + " "*15 + "ECG SCANPATH COMPLETION EXAMPLES" + " "*21 + "║")
    print("║" + " "*68 + "║")
    print("║" + "  This demonstrates how the PDA completes incomplete scanpaths  " + " "*4 + "║")
    print("║" + "  based on clinical ECG examination protocols" + " "*24 + "║")
    print("╚" + "═"*68 + "╝")
    print("\n")

    # Run all examples
    example_1_incomplete_rhythm_analysis()
    example_2_incomplete_qrs_examination()
    example_3_incomplete_lead_sequence()
    example_4_very_incomplete_scanpath()
    example_5_already_complete()
    example_6_compare_incomplete_vs_complete()
    example_7_multiple_incomplete_patterns()

    print("="*70)
    print(" ALL COMPLETION EXAMPLES FINISHED")
    print("="*70)
    print("\nKey Takeaways:")
    print("   1. PDA can detect incomplete scanpaths")
    print("   2. Completion is based on clinical examination rules")
    print("   3. Stack state determines what tasks are still needed")
    print("   4. Complete scanpaths are recognized and not modified")
    print()
