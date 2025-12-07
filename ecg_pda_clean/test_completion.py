"""
Test PDA Scanpath Completion with Accuracy Metrics

This script tests incomplete scanpath completion and calculates accuracy.
"""

from completion import ScanpathCompleter
from pda import PushdownAutomaton


def test_completion_with_accuracy():
    """
    Test incomplete scanpath completion and show accuracy
    """
    print("\n" + "="*80)
    print("ECG SCANPATH COMPLETION TEST WITH ACCURACY")
    print("="*80)

    completer = ScanpathCompleter()
    pda = PushdownAutomaton()

    # Test cases: (incomplete_scanpath, expected_complete_scanpath, description)
    test_cases = [
        {
            'incomplete': ['R', 'Rh', 'Ax'],
            'description': 'Only rhythm analysis completed',
            'expected': ['R', 'Rh', 'Ax', 'Q', 'Detail', 'ST', 'T', 'R']
        },
        {
            'incomplete': ['R', 'Rh', 'Ax', 'Q'],
            'description': 'Started QRS but didn\'t finish',
            'expected': ['R', 'Rh', 'Ax', 'Q', 'Detail', 'ST', 'T', 'R']
        },
        {
            'incomplete': ['R', 'Rh', 'Ax', 'Q', 'Detail'],
            'description': 'QRS complete, missing repolarization',
            'expected': ['R', 'Rh', 'Ax', 'Q', 'Detail', 'ST', 'T', 'R']
        },
        {
            'incomplete': ['R', 'Rh', 'Ax', 'Q', 'Detail', 'V1', 'V2'],
            'description': 'With lead details, missing ST/T',
            'expected': ['R', 'Rh', 'Ax', 'Q', 'Detail', 'V1', 'V2', 'ST', 'T', 'R']
        },
        {
            'incomplete': ['R', 'Rh', 'Ax', 'Q', 'Detail', 'ST'],
            'description': 'Missing T wave only',
            'expected': ['R', 'Rh', 'Ax', 'Q', 'Detail', 'ST', 'T', 'R']
        },
        {
            'incomplete': ['R'],
            'description': 'Just started examination',
            'expected': ['R', 'Rh', 'Ax', 'Q', 'Detail', 'ST', 'T', 'R']
        },
    ]

    total_tests = len(test_cases)
    successful_completions = 0

    for i, test in enumerate(test_cases, 1):
        print(f"\n{'─'*80}")
        print(f"TEST {i}/{total_tests}: {test['description']}")
        print(f"{'─'*80}")

        incomplete = test['incomplete']
        expected = test['expected']

        print(f"\n Incomplete Scanpath:")
        print(f"   {' → '.join(incomplete)}")
        print(f"   Length: {len(incomplete)} tasks")

        # Check if incomplete
        pda.reset()
        pda.process_sequence(incomplete)
        is_complete = pda.accepts()
        missing_tasks = pda.get_missing_tasks()

        print(f"\nPDA Analysis:")
        print(f"   State: {pda.current_state}")
        print(f"   Stack: {pda.stack}")
        print(f"   Is Complete: {' Yes' if is_complete else ' No'}")
        if missing_tasks:
            print(f"   Missing Tasks: {missing_tasks[:5]}")

        # Attempt completion
        print(f"\nRunning Completion...")
        completed = completer.complete_scanpath(incomplete)

        print(f"\n Completed Scanpath:")
        print(f"   {' → '.join(completed)}")
        print(f"   Length: {len(completed)} tasks")
        print(f"   Added: {len(completed) - len(incomplete)} tasks")

        # Validate completion
        pda.reset()
        is_valid = pda.process_sequence(completed)
        is_accepted = pda.accepts()

        print(f"\nValidation:")
        print(f"   Valid Sequence: {'Yes' if is_valid else ' No'}")
        print(f"   Accepted by PDA: {' Yes' if is_accepted else 'No'}")
        print(f"   Final State: {pda.current_state}")
        print(f"   Final Stack: {pda.stack}")

        # Calculate accuracy
        if is_accepted and len(pda.stack) == 1:
            successful_completions += 1
            print(f"   Result: SUCCESSFUL COMPLETION")
        else:
            print(f"   Result: PARTIAL COMPLETION")
            remaining = pda.get_missing_tasks()
            if remaining:
                print(f"   Still Missing: {remaining[:3]}")

        # Compare with expected
        if expected:
            print(f"\n Comparison with Expected:")
            print(f"   Expected: {' → '.join(expected)}")
            if completed == expected:
                print(f"   Match: Perfect Match")
            else:
                print(f"   Match: Different from expected")
                print(f"   Similarity: {calculate_similarity(completed, expected):.1f}%")

    # Overall accuracy
    print(f"\n{'='*80}")
    print(f"OVERALL RESULTS")
    print(f"{'='*80}")
    print(f"\n Accuracy Metrics:")
    print(f"   Total Tests: {total_tests}")
    print(f"   Successful Completions: {successful_completions}")
    print(f"   Accuracy: {(successful_completions/total_tests)*100:.1f}%")
    print(f"   Failed: {total_tests - successful_completions}")

    print(f"\n Notes:")
    print(f"   - Successful = PDA accepts the completed scanpath")
    print(f"   - Incomplete scanpaths are detected by stack state")
    print(f"   - Completion is based on clinical examination protocols")
    print(f"   - Perfect completion requires stack = ['Z0'] and accepting state")
    print()


def calculate_similarity(seq1, seq2):
    """Calculate similarity percentage between two sequences"""
    if not seq1 and not seq2:
        return 100.0
    if not seq1 or not seq2:
        return 0.0

    matches = sum(1 for a, b in zip(seq1, seq2) if a == b)
    max_len = max(len(seq1), len(seq2))
    return (matches / max_len) * 100


def show_example_completion():
    """Show a detailed example of one completion"""
    print("\n" + "="*80)
    print("DETAILED COMPLETION EXAMPLE")
    print("="*80)

    completer = ScanpathCompleter()
    pda = PushdownAutomaton()

    print("\nScenario: Doctor examined rhythm and QRS but was interrupted\n")

    incomplete = ['R', 'Rh', 'Ax', 'Q', 'Detail', 'V1', 'V2', 'V3']

    print(f"Incomplete Scanpath: {' → '.join(incomplete)}")
    print(f"\nWhat the doctor did:")
    print(f"  1. R  - Started rhythm assessment")
    print(f"  2. Rh - Checked heart rate")
    print(f"  3. Ax - Determined electrical axis")
    print(f"  4. Q  - Started QRS complex analysis")
    print(f"  5-8.  - Examined leads V1, V2, V3 in detail")

    # Analyze
    pda.reset()
    pda.process_sequence(incomplete)

    print(f"\n🔍 PDA Analysis:")
    print(f"  Current State: {pda.current_state}")
    print(f"  Stack: {pda.stack}")
    print(f"  Missing: {pda.get_missing_tasks()}")

    # Complete
    print(f"\n🔧 Running PDA Completion...\n")
    completed = completer.complete_scanpath(incomplete)

    print(f"\n Completed Scanpath: {' → '.join(completed)}")

    # Validate
    pda.reset()
    is_valid = pda.process_sequence(completed)

    print(f"\n Validation Result:")
    print(f"  Valid: {is_valid}")
    print(f"  Accepted: {pda.accepts()}")
    print(f"  Final State: {pda.current_state}")

    print(f"\n Summary:")
    print(f"  Input Length: {len(incomplete)} tasks")
    print(f"  Output Length: {len(completed)} tasks")
    print(f"  Tasks Added: {len(completed) - len(incomplete)}")
    print()


if __name__ == "__main__":
    print("\n╔" + "═"*78 + "╗")
    print("║" + " "*15 + "SCANPATH COMPLETION ACCURACY TEST" + " "*30 + "║")
    print("╚" + "═"*78 + "╝")

    # Run detailed example first
    show_example_completion()

    # Run all tests
    test_completion_with_accuracy()

    print("="*80)
    print("TEST COMPLETE")
    print("="*80)
