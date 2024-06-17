from converterBase import ConverterBase
from music21 import converter

class ConverterMusic21(ConverterBase):
    def __init__(self):
         super().__init__("music21")
    
    def Convert(self, file_source, file_target):
        midi_file = file_source
        # Convert MIDI to MusicXML using music21
        self = converter.parse(midi_file)
        # Get the filename from file_source and change the extension to xml
        file_target = self.split('.')[0] + ".xml"
        self.write("xml", file_target)
        
        # print(f"MusicXML file generated: {file_target}")


