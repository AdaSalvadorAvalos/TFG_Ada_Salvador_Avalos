"""
DataScore.py

This module defines the 'DataScore' class, which represents a musical score
using a collection of 'DataScoreElement' objects. The class provides methods
to manage, sort, and serialize score elements, making it suitable for use
in JSON-based workflows or interface visualization.
"""
import json

class DataScore:
    """
    Represents a musical score composed of multiple elements.

    'DataScore' manages a collection of 'DataScoreElement' objects, along with
    basic score metadata such as time signature and key signature. It provides
    methods for adding elements, sorting them, and converting the score to
    dictionary format for JSON serialization.

    Attributes:
        elements (list): List of 'DataScoreElement' objects in the score.
        time_signature (str): The score's time signature (default "3/4").
        key_signature (int): The score's key signature, represented as an integer.

    Methods:
        to_dict():
            Converts the score and its elements into a dictionary.
        get_measure_number(dtelement):
            Generates a unique ID for a given element based on measure and position.
        sort():
            Sorts all elements in the score using the generated unique IDs.
        addElement(element):
            Adds a new 'DataScoreElement' to the score.
    """
    def __init__(self):
        """Initialize an empty score with default time and key signatures."""
        self.elements = []
        self.time_signature = "3/4"
        self.key_signature  = 0


    def to_dict(self):
        """Convert the score and its elements into a dictionary suitable for JSON serialization."""
        return {
            "elements": [element.to_dict() for element in self.elements],
            "time_signature": self.time_signature,
            "key_signature" : self.key_signature 
        }
    
    def get_measure_number(self,dtelement):
        """
        Generate a unique ID for a score element.

        The ID is calculated as: measure_id * 10000 + position.

        Args:
            dtelement: A 'DataScoreElement' object with 'measure_id' and 'position' attributes.

        Returns:
            int: Unique identifier for sorting and ordering elements.
        """
        return dtelement.measure_id * 10000 + dtelement.position

    def sort(self):
       """Sort all elements in the score by their unique measure number."""
       self.elements = sorted(self.elements, key=self.get_measure_number)
   
    def addElement(self,element):
        """Add a new element to the score."""
        self.elements.append(element)

