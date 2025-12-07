"""
Simple Incomplete Scanpath Completion Demo

This shows how the PDA detects and attempts to complete incomplete ECG scanpaths.
"""

from pda import PushdownAutomaton


def demonstrate_incomplete_detection():
    """
    Demonstrates how PDA detects incomplete scanpaths
    """
    print("\n" + "="*80)
    print("INCOMPLETE SCANPATH DETECTION & COMPLETION DEMO")
    print("="*80)

    pda = PushdownAutomaton()

    # Example scenarios
    scenarios = [
        {
            'name': 'Scenario 1: Complete Examination',
            'scanpath': ['R', 'Rh', 'Ax', 'Q', 'Detail', 'ST', 'T', 'R'],
            'description': 'Full ECG examination with all steps'
        },
        {
            'name': 'Scenario 2: Stopped After Rhythm',
            'scanpath': ['R', 'Rh', 'Ax'],
            'description': 'Only completed rhythm analysis'
        },
        {
            'name': 'Scenario 3: Stopped During QRS',
            'scanpath': ['R', 'Rh', 'Ax', 'Q', 'Detail'],
            'description': 'Checked QRS but missing repolarization'
        },
        {
            'name': 'Scenario 4: Missing T Wave',
            'scanpath': ['R', 'Rh', 'Ax', 'Q', 'Detail', 'ST'],
            'description': 'Has ST but missing T wave'
        },
        {
            'name': 'Scenario 5: Only Rhythm Started',
            'scanpath': ['R'],
            'description': 'Just started rhythm assessment'
        }
    ]

    for scenario in scenarios:
        print(f"\n{'─'*80}")
        print(f" {scenario['name']}")
        print(f"   {scenario['description']}")
        print(f"\n   Scanpath: {' → '.join(scenario['scanpath'])}")

        # Process with PDA
        pda.reset()
        result = pda.process_sequence(scenario['scanpath'])

        # Check state
        print(f"\n   PDA State:  {pda.current_state}")
        print(f"   Stack:      {pda.stack}")
        print(f"   Accepted:   {pda.accepts()}")

        # Get missing tasks
        missing = pda.get_missing_tasks()
        if missing:
            print(f"   Missing:    {missing}")
            print(f"\n   INCOMPLETE - Still needs: {' → '.join(missing[:3])}")
        else:
            print(f"\n    COMPLETE")


def show_stack_based_completion():
    """
    Shows how stack state indicates what's missing
    """
    print("\n" + "="*80)
    print("STACK-BASED COMPLETION LOGIC")
    print("="*80)

    print("""
The PDA uses a stack to track pending tasks:

1. When a task is started, it's pushed to the stack
2. When a task is completed, it's popped from the stack
3. Remaining stack items = incomplete tasks

Example:
    Input:    R → Rh → Ax → Q → Detail

    Stack Evolution:
    ────────────────────────────────────
    Initial:     [Z0]
    After R:     [Z0, R]           # Rhythm started
    After Rh:    [Z0]              # Rhythm completed
    After Ax:    [Z0, QRS]         # QRS assessment queued
    After Q:     [Z0, QRS]         # Still in QRS
    After Detail:[Z0, QRS, ExpectRepol]  # Need to check repolarization

    Stack has: [Z0, QRS, ExpectRepol]
    → Still need to complete: QRS and ExpectRepol (ST, T waves)
""")

    pda = PushdownAutomaton()
    sequence = ['R', 'Rh', 'Ax', 'Q', 'Detail']

    print(f"\nLet's trace this step by step:\n")
    print(f"{'Step':<15} {'Action':<15} {'Stack':<40} {'State':<15}")
    print("─"*85)

    pda.reset()
    print(f"{'START':<15} {'(initial)':<15} {str(pda.stack):<40} {pda.current_state:<15}")

    for i, symbol in enumerate(sequence, 1):
        pda.step(symbol)
        print(f"{'Step ' + str(i):<15} {symbol:<15} {str(pda.stack):<40} {pda.current_state:<15}")

    print(f"\n Final Stack: {pda.stack}")
    print(f"   This tells us: {len(pda.stack)-1} task(s) still pending")
    print(f"   Missing: {pda.get_missing_tasks()}")


def manual_completion_example():
    """
    Shows manual completion of an incomplete scanpath
    """
    print("\n" + "="*80)
    print("MANUAL COMPLETION EXAMPLE")
    print("="*80)

    print("\n Scenario: Doctor interrupted during examination\n")

    incomplete = ['R', 'Rh', 'Ax', 'Q', 'Detail', 'V1', 'V2', 'V3']

    print(f"   Incomplete scanpath: {' → '.join(incomplete)}")

    pda = PushdownAutomaton()
    pda.process_sequence(incomplete)

    print(f"\n   Current state: {pda.current_state}")
    print(f"   Stack: {pda.stack}")
    print(f"   Missing: {pda.get_missing_tasks()}")

    # Suggest completion
    print(f"\n To complete this examination, the doctor should:")
    missing = pda.get_missing_tasks()
    for i, task in enumerate(missing[:5], 1):
        task_descriptions = {
            'ST': 'Check ST segment for elevation/depression',
            'T': 'Evaluate T wave morphology',
            'Q': 'Re-examine QRS complexes',
            'R': 'Final rhythm verification'
        }
        desc = task_descriptions.get(task, f'Perform {task}')
        print(f"   {i}. {task} - {desc}")

    # Create completed version
    completed = incomplete + missing[:2]  # Add first two missing tasks
    print(f"\n After adding missing steps: {' → '.join(completed)}")

    pda.reset()
    pda.process_sequence(completed)
    print(f"   Is complete now? {pda.accepts()}")
    if not pda.accepts():
        print(f"   Still missing: {pda.get_missing_tasks()}")


def completion_rules_explanation():
    """
    Explains the completion rules
    """
    print("\n" + "="*80)
    print("COMPLETION RULES")
    print("="*80)

    print("""
The PDA uses clinical examination protocols to determine completion:

Rule 1: Rhythm Assessment
    R → Rh → Ax
    ├─ R: Start rhythm check
    ├─ Rh: Check heart rate
    └─ Ax: Determine axis

Rule 2: QRS Complex
    Q → [Detail | V1-V6] → ST → T
    ├─ Q: Start QRS examination
    ├─ Detail/Leads: Detailed analysis
    ├─ ST: Check ST segment
    └─ T: Check T wave

Rule 3: Repolarization
    ST → T
    ├─ ST: ST segment evaluation
    └─ T: T wave evaluation

Rule 4: Final Check
    R (final rhythm verification)

 Complete Examination Pattern:
    R → Rh → Ax → Q → [Details/Leads] → ST → T → R
    └────────┘   └───────────────────────────┘   │
     Rhythm           Depolarization/            Final
                      Repolarization             Check
""")


if __name__ == "__main__":
    print("\n╔" + "═"*78 + "╗")
    print("║" + " "*20 + "PDA SCANPATH COMPLETION DEMONSTRATION" + " "*21 + "║")
    print("╚" + "═"*78 + "╝")

    # Run demonstrations
    demonstrate_incomplete_detection()
    show_stack_based_completion()
    manual_completion_example()
    completion_rules_explanation()

    print("\n" + "="*80)
    print(" DEMONSTRATION COMPLETE")
    print("="*80)

    print("""
Key Insights:
  • The PDA stack tracks pending examination tasks
  • Missing tasks can be determined from stack contents
  • Clinical protocols guide the completion process
  • Complete scanpaths result in an empty stack (only Z0)

For automatic completion, see: completion.py and ScanpathCompleter class
""")
