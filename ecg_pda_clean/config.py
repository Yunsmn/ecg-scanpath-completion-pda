"""
Configuration for ECG Scanpath PDA
Based on PhysioNet ECG dataset layout
"""

# Lead-level alphabet (12 ECG leads)
LEAD_ALPHABET = [
    'I', 'II', 'III', 
    'aVR', 'aVL', 'aVF',
    'V1', 'V2', 'V3', 'V4', 'V5', 'V6',
    'RHYTHM'  # Rhythm strip at bottom
]

# Task-level alphabet (diagnostic tasks)
TASK_ALPHABET = [
    'R',      # Rate assessment
    'Rh',     # Rhythm evaluation
    'Ax',     # Axis determination
    'P',      # P-wave analysis
    'PR',     # PR interval
    'Q',      # QRS complex
    'ST',     # ST segment
    'T',      # T-wave
    'QT',     # QT interval
    'Detail'  # Detailed morphology inspection
]

# PDA States
PDA_STATES = {
    'qRate': 'Rate Assessment',
    'qRhythm': 'Rhythm Evaluation',
    'qAxis': 'Axis Determination',
    'qMorph': 'Morphology Analysis',
    'qST': 'Repolarization Check',
    'qDetail': 'Detailed Inspection',
    'qEnd': 'Complete'
}

# Stack alphabet
STACK_ALPHABET = ['R', 'Rh', 'Ax', 'QRS', 'ST', 'ExpectRepol', 'Z0']

# Minimum fixation duration (ms)
MIN_FIXATION_DURATION = 100

# AOI Definitions (example for 1366x768 display)
# NOTE: These need calibration for your specific ECG images
AOI_COORDINATES = {
    # Format: 'Lead': (x_min, y_min, x_max, y_max)
    'I':      (50, 100, 250, 200),
    'II':     (280, 100, 480, 200),
    'III':    (510, 100, 710, 200),
    'aVR':    (740, 100, 940, 200),
    'aVL':    (970, 100, 1170, 200),
    'aVF':    (1200, 100, 1350, 200),
    'V1':     (50, 230, 250, 330),
    'V2':     (280, 230, 480, 330),
    'V3':     (510, 230, 710, 330),
    'V4':     (740, 230, 940, 330),
    'V5':     (970, 230, 1170, 330),
    'V6':     (1200, 230, 1350, 330),
    'RHYTHM': (50, 500, 1350, 650)
}
