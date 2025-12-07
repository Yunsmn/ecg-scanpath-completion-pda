# ECG Scanpath PDA - How to Run

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Examples

#### Simple Completion Demo (Recommended First!)
```bash
python simple_completion_demo.py
```
This shows:
- How PDA detects incomplete scanpaths
- Stack-based completion logic
- Manual completion examples
- Completion rules explanation

#### Comprehensive Completion Examples
```bash
python incomplete_scanpath_example.py
```
This demonstrates 7 different incomplete scanpath scenarios and how PDA handles them.

#### Basic Examples
```bash
python examples.py
```
This shows:
- Simple fixation processing
- Complete analysis pipeline
- Loading from CSV
- PDA execution trace

#### Main Analysis
```bash
python main.py
```
Complete ECG scanpath analyzer with fixation processing.

### 3. Run Specific Components

#### Test PDA Directly
```python
from pda import PushdownAutomaton

pda = PushdownAutomaton()
scanpath = ['R', 'Rh', 'Ax', 'Q', 'Detail', 'ST', 'T', 'R']
result = pda.process_sequence(scanpath)
print(f"Valid: {result}")
print(f"Complete: {pda.accepts()}")
```

#### Test Scanpath Completion
```python
from completion import ScanpathCompleter

completer = ScanpathCompleter()
incomplete = ['R', 'Rh', 'Ax', 'Q', 'Detail']
completed = completer.complete_scanpath(incomplete)
print(f"Completed: {' → '.join(completed)}")
```

#### Process Fixations
```python
from aoi_mapper import AOIMapper, Fixation

mapper = AOIMapper()
fixations = [
    Fixation(320, 120, 210, 1.0),
    Fixation(680, 520, 260, 1.5),
]
leads = mapper.convert_fixations_to_lead_sequence(fixations)
print(f"Leads: {' → '.join(leads)}")
```

## Files Overview

### Core Files
- `pda.py` - Pushdown Automaton implementation
- `aoi_mapper.py` - Maps fixation coordinates to ECG leads
- `task_inference.py` - Infers clinical tasks from lead sequences
- `completion.py` - Completes incomplete scanpaths
- `config.py` - Configuration and ECG lead definitions
- `main.py` - Main analysis pipeline

### Example Files
- `simple_completion_demo.py` - **START HERE** - Clear completion demonstrations
- `incomplete_scanpath_example.py` - Comprehensive completion scenarios
- `examples.py` - Basic usage examples
- `example_fixations.csv` - Sample fixation data

### Documentation
- `README.md` - Project overview and documentation
- `requirements.txt` - Python dependencies
- `HOW_TO_RUN.md` - This file

## Expected Output

When running `simple_completion_demo.py`, you'll see:
1. Detection of incomplete vs complete scanpaths
2. Stack evolution during processing
3. Missing task identification
4. Completion suggestions based on clinical protocols

## Troubleshooting

If you get import errors:
```bash
pip install -r requirements.txt
```

If examples don't run:
```bash
python3 simple_completion_demo.py
```

## Next Steps

1. Start with `simple_completion_demo.py` to understand the concepts
2. Try `incomplete_scanpath_example.py` for more scenarios
3. Explore `examples.py` for basic usage patterns
4. Read `README.md` for detailed documentation
5. Modify and experiment with your own scanpaths!
