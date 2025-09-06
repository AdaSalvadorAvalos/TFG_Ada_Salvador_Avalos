"""
ConverterBase.py

This module defines the 'ConverterBase' class, which serves as the foundation
for specific audio-to-MusicXML converters such as 'converterFFMPEG2'.
It provides a constructor for storing a converter name and a placeholder 'Convert' method
that must be implemented by subclasses.
"""

class ConverterBase:
    """
    Base class for audio-to-MusicXML converter classes.

    This class stores a name for the converter and defines a placeholder 'Convert' method 
    to be overridden by subclasses with actual conversion logic.

    Attributes:
        m_name (str): The name of the converter instance.

    Methods:
        Convert(file_source, file_target):
            Placeholder method for converting an audio or MIDI file to MusicXML.
            Subclasses should override this method with actual conversion logic.
    """
    def __init__(self,name):
        self.m_name = name

    def Convert(self, file_source, file_target):
         """Convert a source file to a target file. Must be implemented by subclasses."""
         pass