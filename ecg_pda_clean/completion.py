"""
Complete incomplete ECG scanpaths using PDA
"""

from typing import List
from pda import PushdownAutomaton


class ScanpathCompleter:
    """Complete truncated ECG scanpaths"""
    
    def __init__(self):
        self.pda = PushdownAutomaton()
        self.completion_rules = self._define_completion_rules()
    
    def _define_completion_rules(self):
        """Clinical guidelines for completing examinations"""
        return {
            'ExpectRepol': {
                'required': ['ST', 'T'],
                'optional': ['QT'],
                'leads': ['V3', 'V4', 'V5']  # Continue precordial
            },
            'QRS': {
                'required': ['Q', 'ST', 'T'],
                'optional': ['Detail'],
                'leads': ['V1', 'V2', 'V3']
            },
            'ST': {
                'required': ['T'],
                'optional': ['QT'],
                'leads': []
            },
            'R': {
                'required': ['Rh', 'Ax'],
                'optional': [],
                'leads': ['II']
            }
        }
    
    def complete_scanpath(self, partial_sequence: List[str]) -> List[str]:
        """
        Complete an incomplete ECG scanpath
        
        Args:
            partial_sequence: Truncated scanpath
            
        Returns:
            Completed scanpath
        """
        # Process partial sequence
        self.pda.reset()
        for symbol in partial_sequence:
            self.pda.step(symbol)
        
        # Check if complete
        if self.pda.accepts():
            print(" Scanpath is already complete!")
            return partial_sequence
        
        print(f" Incomplete scanpath detected")
        print(f"   Current state: {self.pda.current_state}")
        print(f"   Stack: {self.pda.stack}")
        
        # Generate completion
        completion = self._generate_completion()
        
        # Return full sequence
        full_sequence = partial_sequence + completion
        
        print(f" Generated completion: {' → '.join(completion)}")
        
        return full_sequence
    
    def _generate_completion(self) -> List[str]:
        """Generate completion based on stack state"""
        completion = []
        max_iterations = 50  # Prevent infinite loops
        iterations = 0

        # Process stack from top to bottom
        while len(self.pda.stack) > 1 and iterations < max_iterations:
            iterations += 1
            stack_top = self.pda.stack[-1]

            if stack_top in self.completion_rules:
                rule = self.completion_rules[stack_top]

                # Add required tasks to completion list
                for task in rule['required']:
                    completion.append(task)
                    # Try to step through the PDA with this task
                    success = self.pda.step(task)
                    if not success:
                        # If step fails, we can't continue properly
                        print(f"  Could not process task '{task}' in completion")
                        break
            else:
                # Unknown stack symbol, can't continue
                print(f" Unknown stack symbol '{stack_top}' in completion")
                break

        if iterations >= max_iterations:
            print(f" Completion stopped after {max_iterations} iterations to prevent infinite loop")

        return completion
    
    def validate_completion(self, completed_sequence: List[str]) -> bool:
        """Validate that completed sequence is accepted by PDA"""
        self.pda.reset()
        return self.pda.process_sequence(completed_sequence)


# Example usage
if __name__ == "__main__":
    completer = ScanpathCompleter()
    
    # Incomplete scanpath
    incomplete = ['R', 'Rh', 'Ax', 'Q', 'Detail', 'V1', 'V2']
    
    print("Original sequence:", " → ".join(incomplete))
    print()
    
    # Complete it
    completed = completer.complete_scanpath(incomplete)
    
    print()
    print("Completed sequence:", " → ".join(completed))
    
    # Validate
    is_valid = completer.validate_completion(completed)
    print(f"\nValidation: {' PASS' if is_valid else ' FAIL'}")
