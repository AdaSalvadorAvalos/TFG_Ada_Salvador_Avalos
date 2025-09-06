"""
ConverterMusic21.py

This module defines the 'ConverterMusic21' class, which converts MIDI files to MusicXML.
The resulting MusicXML files are used for visualization and editing in the interactive
interface. The class leverages the 'music21' library to parse MIDI files and write
MusicXML outputs.
"""
from converterBase import ConverterBase
from music21 import converter

class ConverterMusic21(ConverterBase):
    """
    Converter class for transforming MIDI files into MusicXML.

    Inherits from 'ConverterBase' and overrides the 'Convert' method to process
    an input MIDI file and produce a MusicXML file suitable for visualization
    and further editing in the interface.

    Methods:
        Convert(file_source, file_target):
            Converts a MIDI file to a MusicXML file using music21.
            - Parses the MIDI file into a music21 stream object.
            - Determines the target filename by replacing the original extension with '.xml'.
            - Writes the MusicXML file to the specified location.
    """
    def __init__(self):
         """Initialize the converter with the name 'music21'."""
         super().__init__("music21")
    
    def Convert(self, file_source, file_target):
        """
        Convert a MIDI file to MusicXML using music21.

        Args:
            file_source (str): Path to the input MIDI file.
            file_target (str): Desired path for the output MusicXML file.
        """
        midi_file = file_source
        # Convert MIDI to MusicXML using music21
        self = converter.parse(midi_file)
        # Get the filename from file_source and change the extension to xml
        file_target = self.split('.')[0] + ".xml"
        self.write("xml", file_target)
        
        # print(f"MusicXML file generated: {file_target}")


