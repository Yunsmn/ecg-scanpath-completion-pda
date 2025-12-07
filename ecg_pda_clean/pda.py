"""
Pushdown Automaton for ECG Scanpath Modeling
"""

from typing import List, Tuple, Optional
from dataclasses import dataclass
from config import PDA_STATES, STACK_ALPHABET


@dataclass
class PDATransition:
    """Represents a PDA transition"""
    from_state: str
    input_symbol: str
    stack_top: str
    to_state: str
    stack_operation: str  # 'push:X', 'pop', 'noop'
    
    def __repr__(self):
        return f"δ({self.from_state}, {self.input_symbol}, {self.stack_top}) → ({self.to_state}, {self.stack_operation})"


class PushdownAutomaton:
    """
    PDA for ECG Scanpath Interpretation
    M = (Q, Σ, Γ, δ, q0, Z0, F)
    """
    
    def __init__(self):
        self.states = list(PDA_STATES.keys())
        self.initial_state = 'qRate'
        self.accepting_states = {'qEnd'}
        self.stack = ['Z0']  # Initial stack
        self.current_state = self.initial_state
        self.transitions = self._define_transitions()
        self.history = []  # Trace of execution
    
    def _define_transitions(self) -> List[PDATransition]:
        """
        Define PDA transition function δ
        Based on Section III.D of the paper
        """
        return [
            # Rate → Rhythm
            PDATransition('qRate', 'R', 'Z0', 'qRhythm', 'push:R'),
            PDATransition('qRate', 'Rh', 'Z0', 'qRhythm', 'noop'),

            # Rhythm → Axis
            PDATransition('qRhythm', 'Rh', 'R', 'qAxis', 'pop'),
            PDATransition('qRhythm', 'Rh', 'Z0', 'qAxis', 'noop'),

            # Axis → Morphology (normal flow)
            PDATransition('qAxis', 'Ax', 'Z0', 'qMorph', 'push:QRS'),
            PDATransition('qAxis', 'Ax', 'R', 'qMorph', 'push:QRS'),

            # Allow skipping Axis and going directly to Q (incomplete examination)
            PDATransition('qAxis', 'Q', 'Z0', 'qMorph', 'push:QRS'),
            PDATransition('qAxis', 'Detail', 'Z0', 'qDetail', 'push:QRS:push:ExpectRepol'),
            PDATransition('qAxis', 'ST', 'Z0', 'qST', 'push:QRS:push:ST'),
            PDATransition('qAxis', 'T', 'Z0', 'qEnd', 'push:QRS'),

            # Morphology (QRS analysis)
            PDATransition('qMorph', 'Q', 'QRS', 'qMorph', 'noop'),

            # Detailed inspection (nested)
            PDATransition('qMorph', 'Detail', 'QRS', 'qDetail', 'push:ExpectRepol'),
            PDATransition('qDetail', 'V1', 'ExpectRepol', 'qDetail', 'noop'),
            PDATransition('qDetail', 'V2', 'ExpectRepol', 'qDetail', 'noop'),
            PDATransition('qDetail', 'V3', 'ExpectRepol', 'qDetail', 'noop'),
            PDATransition('qDetail', 'V4', 'ExpectRepol', 'qDetail', 'noop'),
            PDATransition('qDetail', 'V5', 'ExpectRepol', 'qDetail', 'noop'),
            PDATransition('qDetail', 'V6', 'ExpectRepol', 'qDetail', 'noop'),

            # Detail can appear at end too (additional inspection)
            PDATransition('qDetail', 'Detail', 'ExpectRepol', 'qDetail', 'noop'),

            # Morphology → ST segment
            PDATransition('qMorph', 'ST', 'QRS', 'qST', 'push:ST'),
            PDATransition('qDetail', 'ST', 'ExpectRepol', 'qST', 'pop:push:ST'),

            # ST → T wave → End
            PDATransition('qST', 'T', 'ST', 'qEnd', 'pop'),
            PDATransition('qST', 'QT', 'ST', 'qEnd', 'pop'),

            # End state - handle additional detail checks or pop QRS to reach accept
            PDATransition('qEnd', 'Detail', 'QRS', 'qDetail', 'push:ExpectRepol'),
            PDATransition('qEnd', 'T', 'QRS', 'qEnd', 'pop'),
            PDATransition('qEnd', 'ST', 'QRS', 'qST', 'push:ST'),
            PDATransition('qEnd', 'Q', 'QRS', 'qEnd', 'pop'),

            # Detail → T (after ST is popped from detail state)
            PDATransition('qDetail', 'T', 'QRS', 'qEnd', 'pop'),
        ]
    
    def reset(self):
        """Reset PDA to initial state"""
        self.current_state = self.initial_state
        self.stack = ['Z0']
        self.history = []
    
    def step(self, input_symbol: str) -> bool:
        """
        Process one input symbol
        
        Args:
            input_symbol: Task or lead symbol
            
        Returns:
            True if transition found, False otherwise
        """
        if not self.stack:
            return False
        
        stack_top = self.stack[-1]
        
        # Find matching transition
        transition = self._find_transition(input_symbol, stack_top)
        
        if transition is None:
            print(f" No transition for ({self.current_state}, {input_symbol}, {stack_top})")
            return False
        
        # Execute transition
        self._execute_transition(transition, input_symbol)
        return True
    
    def _find_transition(self, input_symbol: str, stack_top: str) -> Optional[PDATransition]:
        """Find matching transition rule"""
        for trans in self.transitions:
            if (trans.from_state == self.current_state and 
                trans.input_symbol == input_symbol and
                trans.stack_top == stack_top):
                return trans
        return None
    
    def _execute_transition(self, transition: PDATransition, input_symbol: str):
        """Execute a transition"""
        # Record history
        self.history.append({
            'state': self.current_state,
            'input': input_symbol,
            'stack_before': self.stack.copy(),
            'transition': transition
        })

        # Update state
        self.current_state = transition.to_state

        # Stack operation
        if transition.stack_operation == 'pop':
            if self.stack:
                self.stack.pop()
        elif transition.stack_operation == 'noop':
            # No operation
            pass
        elif 'pop:push' in transition.stack_operation:
            # Pop then push
            if self.stack:
                self.stack.pop()
            symbol = transition.stack_operation.split(':')[-1]
            self.stack.append(symbol)
        elif transition.stack_operation.startswith('push:'):
            # Handle single or multiple pushes
            parts = transition.stack_operation.split(':')
            for i in range(1, len(parts)):
                if parts[i] and parts[i] != 'push':
                    self.stack.append(parts[i])
    
    def process_sequence(self, input_sequence: List[str]) -> bool:
        """
        Process entire input sequence
        
        Args:
            input_sequence: List of symbols
            
        Returns:
            True if accepted, False otherwise
        """
        self.reset()
        
        for symbol in input_sequence:
            if not self.step(symbol):
                return False
        
        return self.accepts()
    
    def accepts(self) -> bool:
        """Check if current configuration is accepting"""
        return (self.current_state in self.accepting_states and 
                self.stack == ['Z0'])
    
    def is_incomplete(self) -> bool:
        """Check if scanpath is incomplete"""
        return len(self.stack) > 1 or self.current_state not in self.accepting_states
    
    def get_missing_tasks(self) -> List[str]:
        """Identify missing diagnostic tasks based on stack"""
        missing = []
        
        if 'ExpectRepol' in self.stack:
            missing.extend(['ST', 'T'])
        if 'QRS' in self.stack:
            missing.extend(['Q', 'ST', 'T'])
        if 'ST' in self.stack:
            missing.append('T')
        
        return missing
    
    def print_trace(self):
        """Print execution trace"""
        print("\n=== PDA Execution Trace ===")
        for i, step in enumerate(self.history):
            print(f"\nStep {i+1}:")
            print(f"  State: {step['state']}")
            print(f"  Input: {step['input']}")
            print(f"  Stack before: {step['stack_before']}")
            print(f"  Transition: {step['transition']}")
        
        print(f"\nFinal State: {self.current_state}")
        print(f"Final Stack: {self.stack}")
        print(f"Accepted: {self.accepts()}")
        print(f"Incomplete: {self.is_incomplete()}")


# Example usage
if __name__ == "__main__":
    pda = PushdownAutomaton()
    
    # Complete scanpath
    complete_seq = ['R', 'Rh', 'Ax', 'Q', 'ST', 'T']
    print("Testing complete sequence:", complete_seq)
    result = pda.process_sequence(complete_seq)
    print(f"Accepted: {result}")
    pda.print_trace()
    
    print("\n" + "="*50 + "\n")
    
    # Incomplete scanpath
    incomplete_seq = ['R', 'Rh', 'Ax', 'Q', 'Detail']
    print("Testing incomplete sequence:", incomplete_seq)
    pda.reset()
    result = pda.process_sequence(incomplete_seq)
    print(f"Accepted: {result}")
    print(f"Missing tasks: {pda.get_missing_tasks()}")
    pda.print_trace()
