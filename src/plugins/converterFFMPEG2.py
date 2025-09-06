"""
converterFFMPEG2.py

This module implements the Converter class, for audio-to-MusicXML conversion
using ffmpeg, WaoN (via WSL), and the music21 library.

It provides functionality to:
- Convert MP3 or other audio files into WAV format using ffmpeg.
- Generate MIDI files from WAV using WaoN (through WSL) and librosa/pretty_midi as fallback.
- Parse the resulting MIDI file into a MusicXML score with music21.
- Save the final MusicXML file for use in the interactive transcription interface.
"""
import subprocess
from converterBase import ConverterBase
import ffmpeg
import os 

from pydub import AudioSegment
from pydub.playback import play

from music21 import converter

import librosa
import pretty_midi
import numpy as np

class Converter(ConverterBase):
      """
      Converter for handling MP3 → WAV → MIDI → MusicXML conversion.

      This class extends the base Converter class and defines a pipeline that:
      1. Uses ffmpeg to convert MP3 files into WAV.
      2. Runs WaoN (via WSL) to convert WAV into MIDI.
      3. Parses the MIDI file with music21 to create a score.
      4. Saves the score as MusicXML for downstream processing.

      Attributes:
            name (str): Identifier of the plugin, set to "ffmpeg_plugin2".
      
      Methods:
        Convert(file_source, file_target):
            Performs the full audio-to-MusicXML conversion pipeline.
        ConvertToMidi(file_source, file_target):
            Converts a WAV file to MIDI via WaoN using WSL.
      """

      
      def __init__(self):
            """Initialize the converter and set its plugin name."""
            super().__init__('ffmpeg_plugin2')
     
      
      def Convert(self, file_source, file_target):
            """
            Convert an audio file to MusicXML.

            Args:
                  file_source (str): Path to the input audio file (e.g., MP3).
                  file_target (str): Path to the output MusicXML file.

            Workflow:
                  - Convert the input file to WAV using ffmpeg.
                  - Convert the WAV to MIDI with WaoN (via WSL).
                  - Parse the MIDI into a music21 score.
                  - Save the score as MusicXML at 'file_target'.
            """
            try:
                  file_name, file_extension = os.path.splitext(file_target)
                  # Use ffmpeg to convert MP3 to WAV

                  if os.path.exists(file_name + ".wav"):  
                        os.remove(file_name + ".wav") 

                  if os.path.exists(file_name + ".mid"):  
                        os.remove(file_name + ".mid") 
                        
                  if os.path.exists(file_name + ".xml"):  
                        os.remove(file_name + ".xml")       


                  ffmpeg.input(file_source).output(file_name + ".wav").run()

                  self.ConvertToMidi(file_name + ".wav", file_name + ".mid")
            
                  score = converter.parse(file_name + ".mid")

                  score.write("xml", file_target)
            except Exception as e:
            
                  print("An error occurred:", e)

      def ConvertToMidi(self, file_source, file_target):
            """
            Convert a WAV file to MIDI using WaoN and librosa/pretty_midi fallback.

            Args:
                  file_source (str): Path to the input WAV file.
                  file_target (str): Path to the output MIDI file.

            Workflow:
                  - Executes WaoN (via WSL) to generate a MIDI file from the WAV input.
                  - As a fallback, applies librosa's pYIN pitch estimation and pretty_midi
                  to generate a MIDI approximation.
            """
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

      

            try:
                  y, sr = librosa.load(file_source)

                  # Estimate pitch using the pYIN algorithm
                  f0, voiced_flag, voiced_probs = librosa.pyin(y, fmin=librosa.note_to_hz('C2'), fmax=librosa.note_to_hz('C7'))

                  # Convert pitch to MIDI note numbers
                  midi_notes = librosa.hz_to_midi(f0)

                  # Create a PrettyMIDI object
                  midi_data = pretty_midi.PrettyMIDI()

                  # Create an Instrument instance
                  instrument = pretty_midi.Instrument(program=0)  # Use program 0 for a piano sound

                  # Add notes to the Instrument instance
                  for time, note_number in enumerate(midi_notes):
                  # Ignore notes with MIDI note number 0 (unpitched)
                        if not np.isnan(note_number):
                              note = pretty_midi.Note(
                                    velocity=100,  # arbitrary velocity value
                                    pitch=int(note_number),
                                    start=time * (60 / 120),  # Convert time index to seconds
                                    end=(time + 1) * (60 / 120)  # Convert time index to seconds
                              )
                              instrument.notes.append(note)

                  # Add the instrument to the MIDI data
                  midi_data.instruments.append(instrument)

                  # Save the MIDI data to a file
                  
                  midi_data.write(file_target)
            except Exception as e:
      
                  print("An error occurred:", e)