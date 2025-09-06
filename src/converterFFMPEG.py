"""
ConverterFFMPEG.py

This module defines the 'ConverterFFMPEG' class, which converts monophonic audio files
(MP3 or WAV) to MusicXML scores. It uses FFmpeg to handle audio conversion and integrates
with a Wave-to-Notes transcription tool via WSL to generate MIDI files. The resulting score
is cleaned and simplified to single-note melodies for easier editing and visualization.
"""

import subprocess
from converterBase import ConverterBase
import ffmpeg
import os 
from music21 import converter,note,pitch,meter,stream,chord

# ConvertToMidiOld
import librosa
import pretty_midi
import numpy as np
from pydub import AudioSegment
from pydub.playback import play
import re

class ConverterFFMPEG(ConverterBase):
      """
    Converter class that transforms audio files to MusicXML using FFmpeg and WaoN.

    Inherits from 'ConverterBase' and overrides the 'Convert' method to perform
    the following transformations:
    1. Converts MP3 input to WAV using FFmpeg, deleting existing WAV, MIDI, or XML
       files to avoid conflicts.
    2. Converts the WAV file to MIDI using the Wave-to-Notes transcriber via WSL.
    3. Cleans the MIDI score with 'CleanScore', flattening chords into single notes.
    4. Writes the MusicXML file.
    5. Post-processes the MusicXML to remove empty chord nodes and voice tags, ensuring
       compatibility with the interface and piano register mapping.

    Attributes:
        max_duration (float): Maximum note/rest duration allowed when cleaning the score.

    Methods:
        Convert(file_source, file_target):
            Performs the full audio-to-MusicXML conversion pipeline.
        ConvertToMidi(file_source, file_target):
            Converts a WAV file to MIDI via WaoN using WSL.
        CleanScore(score):
            Flattens chords to single notes and enforces maximum note/rest durations.
        CleanInFile(file_target):
            Post-processes the MusicXML file to remove empty chord and voice nodes.
    """
      def __init__(self):
            super().__init__('ffmpeg')
            self.max_duration = 4.0
   
      def CleanScore(self, score):
            """Flatten chords to single notes and limit durations of notes/rests."""
            for part in score.parts:
                  for measure in part.getElementsByClass('Measure'):
                        flat_measure = measure.flatten().notesAndRests

                        for element in flat_measure:
                              duration = min(element.quarterLength, self.max_duration)
                              if isinstance(element, chord.Chord):
                                    # Convert chord to a single note (e.g., the root pitch of the chord)
                                    root_pitch = element.root().nameWithOctave
                                    new_note = note.Note(root_pitch, quarterLength=duration)
                                    # Replace the chord with the new note
                                    measure.insert(element.offset, new_note)
                                    measure.remove(element)
                                   # measure.replace(element, new_note)
                              elif isinstance(element, note.Note):
                                    # Ensure the note's duration does not exceed the max duration
                                    element.quarterLength = duration
                              elif isinstance(element, note.Rest):
                                    # Ensure the rest's duration does not exceed the max duration
                                    element.quarterLength = duration
            

            for part in score.parts:
                  for measure in part.getElementsByClass('Measure'):
                        # Flatten voices within notes and chords of the measure
                        for element in measure.notesAndRests:
                              if hasattr(element, 'flat'):
                                    element.flat.replace(element)
            return score
   
      def CleanInFile(self,file_target):
            """Remove empty chord and voice nodes from a MusicXML file."""
            with open(file_target, 'r', encoding='utf-8') as file:
                  file_contents = file.read()
            
            file_contents = file_contents.replace('<chord />', '')

            pattern = r'<voice>\d+</voice>'

            file_contents = re.sub(pattern, '', file_contents)


            with open(file_target, 'w', encoding='utf-8') as file:
                  file.write(file_contents)

      def Convert(self, file_source, file_target):
            """Full audio-to-MusicXML conversion pipeline, including cleaning and post-processing."""
            try:
                  file_name, file_extension = os.path.splitext(file_target)
                  # Use ffmpeg to convert MP3 to WAV

                  if file_source.endswith(".mp3"):

                        if os.path.exists(file_name + ".wav"):  
                              os.remove(file_name + ".wav") 

                        if os.path.exists(file_name + ".mid"):  
                              os.remove(file_name + ".mid") 
                        
                  if os.path.exists(file_name + ".xml"):  
                        os.remove(file_name + ".xml")       

                  if file_source.endswith(".mp3"):
                        ffmpeg.input(file_source).output(file_name + ".wav").run()

                        self.ConvertToMidi(file_name + ".wav", file_name + ".mid")
                  
                        score = converter.parse(file_name + ".mid")
                  else:
                        score = converter.parse(file_source)

                  score = self.CleanScore(score)

                  score.write("xml", file_target)

                  self.CleanInFile(file_target)


            except Exception as e:
            
                  print("An error occurred:", e)

      def ConvertToMidi(self, file_source, file_target):
            """Convert WAV to MIDI using WaoN via WSL."""
            file_source = file_source.replace("C:", "/mnt/c")
            file_source = file_source.replace("\\", "/")

            file_target = file_target.replace("C:", "/mnt/c")
            file_target = file_target.replace("\\", "/")


            # Define the Linux command to be executed
           # linux_command = f"/home/home/WaoN/waon -i {file_source} -o {file_target} -b 36"
            linux_command = f"/home/home/WaoN/waon -i {file_source} -o {file_target}"
           # linux_command = f"./WaoN/waon -i {file_source} -o {file_target}"

            #linux_command = f"cp {file_source} {file_target}"

            try:
                  # Execute the Linux command using WSL
                 # subprocess.run(["wsl", linux_command], shell=True)   
                  subprocess.run(f"wsl {linux_command}", shell=True)   

            except Exception as e:
      
                  print("An error occurred:", e)

     