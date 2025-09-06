"""
DataScoreElement.py

This module defines the 'DataScoreElement' class, which represents a single musical
element in a score, such as a note, rest, or other symbol. The class includes
attributes for element type, duration, pitch, position, and other metadata, and
provides a method to convert the element to a dictionary suitable for JSON serialization.
"""
import json
from fractions import Fraction

class DataScoreElement:
    """
    Represents a single musical element in a score.

    'DataScoreElement' stores information about a note, rest, or other musical
    symbol, including its type, duration, pitch, position, voice, and measure. It
    provides a method to convert the element into a dictionary format for JSON
    serialization.

    Attributes:
        type (str): The type of element, e.g., "note" or "rest".
        duration (float or Fraction): The duration of the element in beats.
        pitch (str): The pitch of the element, e.g., "C4".
        position (float or Fraction): The position of the element within the measure.
        signature (str): Optional attribute for additional element metadata.
        voice (int): Voice number for piano notation.
        measure_id (int): The measure number in which the element occurs.
        id (str): Unique identifier for the element.

    Methods:
        to_dict():
            Converts the element into a dictionary compatible with JSON serialization,
            converting 'Fraction' objects to floats where necessary.
    """
    def __init__(self):
        """Initialize a musical element with default empty or zero values."""
        self.type = ""
        self.duration = 0
        self.pitch = ""
        self.position = 0
        self.signature = ""
        self.voice = 0
        self.measure_id = 0
        self.id = ""

    def to_dict(self):
        """
        Convert the element to a dictionary for JSON serialization.

        Returns:
            dict: A dictionary representation of the element, with durations and positions
                  converted to floats if they are 'Fraction' instances.
        """   
        return {
            "type": self.type,
            "duration": float(self.duration) if isinstance(self.duration, Fraction) else self.duration,
            "pitch": self.pitch,
            "pos": float(self.position) if isinstance(self.position, Fraction) else self.position,
            "v": self.voice,
            "m": self.measure_id,
            "id": self.id
        }      
       

# class DataScoreEncoder(json.JSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, DataScoreElement):
#             return obj.to_dict()
#         return json.JSONEncoder.default(self, obj)