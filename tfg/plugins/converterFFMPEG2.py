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
      def __init__(self):
            super().__init__('ffmpeg_plugin2')
     
      
      def Convert(self, file_source, file_target):
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