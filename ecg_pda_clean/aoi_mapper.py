"""
Implementation of Algorithm 1: Convert Fixation Coordinates to Lead-Level Sequence
"""

from typing import List, Tuple, Optional
from config import AOI_COORDINATES, MIN_FIXATION_DURATION


class Fixation:
    """Represents a single eye fixation"""
    def __init__(self, x: float, y: float, duration: float, timestamp: float):
        self.x = x
        self.y = y
        self.duration = duration
        self.timestamp = timestamp
    
    def __repr__(self):
        return f"Fixation(x={self.x}, y={self.y}, d={self.duration}ms, t={self.timestamp})"


class AOIMapper:
    """Maps fixation coordinates to Areas of Interest (ECG leads)"""
    
    def __init__(self, aoi_map: dict = None):
        self.aoi_map = aoi_map or AOI_COORDINATES
    
    def map_to_aoi(self, x: float, y: float) -> Optional[str]:
        """
        Map pixel coordinates to ECG lead (AOI)
        
        Args:
            x: X coordinate (pixels)
            y: Y coordinate (pixels)
            
        Returns:
            Lead name or None if outside all AOIs
        """
        for lead, (x_min, y_min, x_max, y_max) in self.aoi_map.items():
            if x_min <= x <= x_max and y_min <= y <= y_max:
                return lead
        return None
    
    def convert_fixations_to_lead_sequence(
        self, 
        fixations: List[Fixation],
        min_duration: float = MIN_FIXATION_DURATION
    ) -> List[str]:
        """
        Algorithm 1: Convert fixation coordinates to lead-level sequence
        
        Args:
            fixations: List of Fixation objects
            min_duration: Minimum fixation duration in ms (default 100ms)
            
        Returns:
            Lead-level sequence as list of lead names
        """
        lead_sequence = []
        
        # Sort fixations by timestamp
        sorted_fixations = sorted(fixations, key=lambda f: f.timestamp)
        
        for fixation in sorted_fixations:
            # Line 5: Filter short saccades
            if fixation.duration < min_duration:
                continue
            
            # Line 8: Map to AOI
            lead = self.map_to_aoi(fixation.x, fixation.y)
            
            # Line 9-10: Skip if outside AOIs
            if lead is None:
                continue
            
            # Line 12-13: Avoid consecutive duplicates
            if not lead_sequence or lead_sequence[-1] != lead:
                lead_sequence.append(lead)
        
        return lead_sequence


# Example usage
if __name__ == "__main__":
    # Sample fixation data
    fixations = [
        Fixation(320, 120, 210, 1.0),
        Fixation(330, 130, 190, 1.2),
        Fixation(680, 520, 260, 1.5),
        Fixation(480, 220, 230, 2.0),
        Fixation(490, 240, 240, 2.3),
        Fixation(920, 260, 300, 2.8),
        Fixation(940, 280, 220, 3.1),
    ]
    
    mapper = AOIMapper()
    sequence = mapper.convert_fixations_to_lead_sequence(fixations)
    print("Lead sequence:", " → ".join(sequence))
