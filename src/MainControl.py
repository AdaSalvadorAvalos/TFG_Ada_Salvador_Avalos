"""
MainControl.py

This module contains the MainControl class, which implements the core functionality
for manipulating MusicXML scores in the Interactive MusicXML Transcriber and Editor.

The class handles:
- Loading audio or MIDI files and converting them to MusicXML.
- Applying transformations such as note insertion, deletion, interval changes,
  mirroring, and changing key/time signatures.
- Playback of MIDI streams via pygame.
- Generating a JSON representation of the score for the web-based interface.
- Dynamic selection of converter plugins for flexible audio-to-MusicXML conversion.
"""
import json
from music21 import converter,note,pitch,meter,stream,chord,key
from DataScore import DataScore
from DataScoreElement import DataScoreElement
import pygame
import uuid

import os
from converterFactory import ConverterFactory
from converterBase import ConverterBase
from PyQt5.QtWidgets import *



class MainControl():
    """
    Main control class for the MusicXML transcriber/editor.

    This class develops all the specific functionality applicable to the interface.
    It interacts with the music21 library for score processing, pygame for playback,
    and dynamically loaded converter plugins for file conversion.

    Attributes:
        plugin_load (str): The currently selected converter plugin (default 'ffmpeg').
        score (music21.stream.Score): The current MusicXML score loaded or created.
        m_current_file_name (str): Path to the current MusicXML file.
    
    Main Methods:

    - __init__(): Initializes pygame and sets the default converter plugin.
    - SelectPlugin(name): Select a converter plugin for audio-to-MusicXML conversion.
    - Save(): Save the current score to the existing MusicXML file.
    - SaveAs(filename): Save the current score under a new file name.
    - Stop(): Stop MIDI playback.
    - Play(): Play the current score as MIDI using pygame.
    - GenerateGUID(): Generate a unique identifier (GUID) for notes.
    - GetNote(note_id): Retrieve a note from the score by its internal ID.
    - NoteChange(note, num): Transpose a single note by a specified interval.
    - IntervalChange(num, selection): Transpose multiple notes by a given interval.
    - NoteRemove(note): Remove a note from its measure.
    - RemoveNotes(selection): Remove multiple notes from the score.
    - GetMeasure(p_measure_id): Retrieve a measure from the score by its number.
    - calculate_pitch(p_y, p_height, staff): Estimate a pitch based on graphical coordinates.
    - AddNote(p_measure_id, p_x, p_y, p_width, p_height, p_note, staff, duration, octave, accidental):
    Insert a new note into a measure at a specific position.
    - reverse_measures(part): Reverse the order of measures in a part.
    - MirrorEffect(): Apply a mirror effect by reversing the score melody.
    - change_time_signature_at_start(new_time_sig): Replace the starting time signature.
    - change_key_signature_at_start(new_key_sig): Replace the starting key signature.
    - GetJSON(): Generate a JSON representation of the current score, including notes, measures, time, and key signature.
    - LoadFile(name): Load a MusicXML, MP3, or MIDI file into the score, converting to MusicXML if necessary.
    """
    def __init__(self):
        """Initialize pygame and set the default converter plugin."""
        pygame.init()
         
        self.plugin_load = "ffmpeg"
        # Initialize variables to store the current playback position
        # self.playback_position = 0
    
    def SelectPlugin(self,name):
        """
        Select the converter plugin to use.

        Args:
            name (str): The name of the plugin (e.g., 'converterFFMPEG').
        """
        if name == "":
            self.plugin_load = "converterFFMPEG"
        else:
            self.plugin_load = name
        
    def Save(self):
        """Save the current score to the existing MusicXML file."""
        # Write the score to the specified file in MusicXML format
        self.score.write('musicxml', fp= self.m_current_file_name )


    def SaveAs(self,filename):
        """
        Save the current score under a new file name.

        Args:
            filename (str): Path where the score will be saved.
        """
        self.m_current_file_name  = filename
        self.Save()

         # Save the current playback position
        # self.playback_position = pygame.mixer.music.get_pos() / 1000  # Convert milliseconds to seconds

    def Stop(self):
         """Stop MIDI playback."""
         pygame.mixer.music.stop()

         # Save the current playback position
        # self.playback_position = pygame.mixer.music.get_pos() / 1000  # Convert milliseconds to seconds

    def Play(self):
        """Play the current score as MIDI using pygame."""
        # Save the MIDI stream to a temporary file
        temp_midi_file = "temp.mid"
        self.score.write('midi', fp=str(temp_midi_file))
        
        # Load the MIDI file into pygame
        pygame.mixer.music.load(str(temp_midi_file))
        
        # Play the MIDI file
        pygame.mixer.music.play()

        # Play the MIDI file from the saved playback position
        # pygame.mixer.music.play(start=self.playback_position)
        

    def GenerateGUID(self):
        """
        Generate a unique identifier (GUID).

        Returns:
            str: A new UUID string.
        """
        guid = uuid.uuid4()
        guid_str = str(guid)
        return guid_str
    

    def GetNote(self,note_id):
        """
        Find a note in the score by its internal ID.

        Args:
            note_id (str): The unique identifier of the note.

        Returns:
            music21.note.Note or None: The matching note object, if found.
        """
        for n in self.score.recurse().getElementsByClass(note.Note):
            if hasattr(n, 'internal_id') and n.internal_id == note_id:
                return n
        return None

    def NoteChange(self,note,num):
        """
        Transpose a note by a given interval.

        Args:
            note (music21.note.Note): The note to transpose.
            num (int): Number of semitones to transpose.
        """
        try:
            note.pitch.transpose(num, inPlace=True)
        except Exception as e:
    # Handle any exception
            print(f"An error occurred: {e}")

      

    def IntervalChange(self,num,selection):
        """
        Transpose multiple notes by a given interval.

        Args:
            num (int): Number of semitones to transpose.
            selection (list[str]): List of note IDs to transpose.

        Returns:
            str: Updated JSON representation of the score.
        """
        for note_id in selection:
                note = self.GetNote(note_id)
                self.NoteChange(note,num)


        return self.GetJSON()

    def NoteRemove(self,note):
        """
        Remove a note from its measure.

        Args:
            note (music21.note.Note): The note to remove.
        """
        parent_measure = note.getContextByClass(stream.Measure)

        # Remove the note from its measure 
        parent_measure.remove(note)

        # self.score.remove(note)
        # del note

    def RemoveNotes(self,selection):
        """
        Remove multiple notes from the score.

        Args:
            selection (list[str]): List of note IDs to remove.

        Returns:
            str: Updated JSON representation of the score.
        """
        for note_id in selection:
            note = self.GetNote(note_id)
            self.NoteRemove(note)
        return self.GetJSON()

    def GetMeasure(self, p_measure_id):
            """
            Retrieve a measure from the score by its ID.

            Args:
                p_measure_id (int): Measure number.

            Returns:
                music21.stream.Measure or None: The corresponding measure, if found.
            """
            # Find the measure by its number
            measure = None
            for part in self.score.parts:
                for m in part.getElementsByClass('Measure'):
                    if m.number == p_measure_id:
                        measure = m
                        break
                if measure:
                    break
            return measure

    def calculate_pitch(self, p_y, p_height, staff):
        """
        Estimate a pitch from a graphical position.

        Args:
            p_y (float): Y-coordinate of the note.
            p_height (float): Height of the staff area.
            staff (str): Either 'treble' or 'bass'.

        Returns:
            music21.pitch.Pitch: The calculated pitch.
        """
       # p_y = p_height - p_y

       # p_height = 40

        if staff == "treble":
            # Define the pitch range for treble staff (e.g., C4 to B5)
            pitch_range = ['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4', 'C5', 'D5', 'E5', 'F5', 'G5', 'A5', 'B5']
        elif staff == "bass":
            # Define the pitch range for bass staff (e.g., C2 to B3)
            pitch_range = ['C2', 'D2', 'E2', 'F2', 'G2', 'A2', 'B2', 'C3', 'D3', 'E3', 'F3', 'G3', 'A3', 'B3']
        else:
            raise ValueError("Invalid staff type. Expected 'treble' or 'bass'.")

        num_pitches = len(pitch_range)
        
        # Calculate pitch index based on p_y
        pitch_index = int((1 - (p_y / (p_height / 2))) * (num_pitches - 1))
        pitch_index = max(0, min(pitch_index, num_pitches - 1))  # Ensure index is within range
        
        return pitch.Pitch(pitch_range[pitch_index])

    def AddNote(self,p_measure_id,p_x,p_y,p_width,p_height,p_note,staff,duration,octave,accidental):
        """
        Insert a new note into a measure.

        Args:
            p_measure_id (int): Target measure number.
            p_x, p_y (float): Position of the note in the measure.
            p_width, p_height (float): Dimensions of the measure.
            p_note (str): Note name (e.g., 'C').
            staff (str): Staff type ('treble' or 'bass').
            duration (str): Note duration (e.g., 'quarter', 'half').
            octave (str): Octave number.
            accidental (str): Accidental (e.g., '#', '-', '').

        Returns:
            str: Updated JSON representation of the score.
        """
        measure = self.GetMeasure(p_measure_id)

        if measure!=None:
            measure_duration = measure.barDuration.quarterLength
            time_position = (p_x / p_width) * measure_duration
            # Create the note (assuming p_note is a pitch string, e.g., 'C4')
          #  new_note = note.Note(self.calculate_pitch(p_y, p_height, staff), quarterLength=float(p_note))
            if accidental:
                new_note = note.Note(p_note+accidental+octave,type = duration)
            else:
                new_note = note.Note(p_note+octave,type = duration)
            
            # Add the note to the measure at the calculated position
            measure.insert(time_position, new_note)

        return self.GetJSON()

    def reverse_measures(self,part):
            """
            Reverse the order of measures in a part.

            Args:
                part (music21.stream.Part): A score part.

            Returns:
                music21.stream.Part: A new part with reversed measures.
            """
            reversed_part = stream.Part()

            # Get all measures of the part
            measures = list(part.getElementsByClass(stream.Measure))

            # Reverse the measures
            measures.reverse()

            # Append reversed measures to the new part
            for measure in measures:
                reversed_part.append(measure)

            return reversed_part
    
   
    def MirrorEffect(self):
        """
        Apply a mirror effect by reversing the score.

        Returns:
            str: Updated JSON representation of the score.
        """
            # Reverse the measures in the score
        reversed_score = stream.Score()

        for part in self.score.parts:
            reversed_part = stream.Part()
            measures = list(part.getElementsByClass(stream.Measure))
            measures.reverse()

                # Calculate the new offsets for reversed measures
            measure_durations = [measure.duration.quarterLength for measure in measures]
            cumulative_durations = [0] * len(measures)
            
            for i in range(1, len(measures)):
                cumulative_durations[i] = cumulative_durations[i-1] + measure_durations[i-1]
            
            max_offset = sum(measure_durations)


            for i, measure in enumerate(measures):
                reversed_measure = stream.Measure(number=i+1)
                reversed_measure.autoSort = False
                
                elements = list(measure.elements)
                elements.reverse()

                # Calculate the new offsets for reversed elements
                max_element_offset  = max(element.offset for element in elements if ("Note" in element.classes) or ("Rest" in element.classes))
                
                for element in elements:
                    new_offset = max_element_offset  - element.offset
                    reversed_measure.insert(new_offset, element)
                
                new_measure_offset = max_offset - cumulative_durations[i] - measure.duration.quarterLength
                reversed_part.insert(new_measure_offset, reversed_measure)
            

            reversed_part = self.reverse_measures(reversed_part)
            
            reversed_score.append(reversed_part)

        self.score =  reversed_score
        return self.GetJSON()



    def change_time_signature_at_start(self, new_time_sig):
        """
        Replace the time signature at the beginning of the score.

        Args:
            new_time_sig (str): New time signature (e.g., '3/4').
        
        Returns:
            str: Updated JSON representation of the score.
        """
        new_time_signature = meter.TimeSignature(new_time_sig)
        # Insert the new time signature at the start of the stream
       # existing_time_signatures = self.score.getElementsByClass(meter.TimeSignature)
       # if existing_time_signatures:
        time_signatures = self.score.getTimeSignatures()

        # Iterate over the time signatures and print them
        for time_signature in time_signatures:
            self.score.remove(time_signature)
        
        # Insert the new time signature at the start of the stream
        self.score.insert(0, new_time_signature)
        return self.GetJSON()
    
    def change_key_signature_at_start(self, new_key_sig):
        """
        Replace the key signature at the beginning of the score.

        Args:
            new_key_sig (int): Number of sharps (positive) or flats (negative).
        
        Returns:
            str: Updated JSON representation of the score.
        """
        self.score.flatten().keySignature._setSharps(new_key_sig)   
        return self.GetJSON()


    def GetJSON(self):
        """
        Generate a JSON representation of the current score.

        Returns:
            str: JSON string containing all notes, measures, time, and key signature.
        """
        data_score = DataScore() 

        # Parse the MusicXML file
        # self.score.keySignature = key.Key()
        score = self.score

        
        #keysig =score.flat.keySignature.sharps
        try:
            keysig =score.flatten().keySignature.sharps
            data_score.key_signature = keysig
            print("key Signature:", keysig)
        except Exception as e:
            print("An error occurred:", e)

        # Get time signatures from the score
        time_signatures = score.getTimeSignatures()

        # Iterate over the time signatures and print them
        for time_signature in time_signatures:
            print("Time Signature:", time_signature.ratioString)
            data_score.time_signature = time_signature.ratioString

        print("Time Signature:", time_signature.ratioString)

        
        time = 0.0
        position = 0

        for part in score.parts:

            measures = part.getElementsByClass('Measure')
            #sorted_measures = sorted(measures, key=get_measure_number)

            for measure in measures:
                pos = 1
                for element in measure:
                    if "Note" in element.classes:

                        element.internal_id = self.GenerateGUID()
                        

                        dataElement = DataScoreElement()

                        # Handle Note element
                        dataElement.type = "Note"
                        dataElement.id = element.internal_id
                        dataElement.duration = element.duration.quarterLength
                        dataElement.pitch = element.pitch.nameWithOctave
                        dataElement.measure_id =  measure.number
                        if element.pitch.octave<4:
                            dataElement.voice = 1
                        else:
                            dataElement.voice = 2
                        dataElement.position = element.offset
                        pos = pos + 1 
                    # dataElement.position = element.seconds # seconds that lasts the note
                        # dataElement.position = time  # Assign the current time as the position
                        time += element.seconds  # Increment time by the duration of the current note

                        # dataElement.position = time  # Assign the current time as the position
                        # time += dataElement.duration  # Increment time by the duration of the current note
                        # Add other conditions for handling different types of elements if needed
                        # print("Note:", element.pitch, element.duration)
                        print("Note:", dataElement.pitch, dataElement.duration, time)
                    
                        if not("6" in  dataElement.pitch) and  not("7" in  dataElement.pitch):
                           data_score.addElement(dataElement)

        data_score.sort()
        data_dict = data_score.to_dict()

        json_str = json.dumps(data_dict)

        return json_str

    def LoadFile(self, name):
        """
        Load a MusicXML, MP3, or MIDI file into the score.

        Args:
            name (str): Path to the file.

        Returns:
            str: JSON representation of the loaded score.
        """
        # if XML

        if not name.endswith(".xml"):
            converterFactory = ConverterFactory()
            conversor = converterFactory.GetConverter(self.plugin_load) 
            file_name, file_extension = os.path.splitext(name)
            conversor.Convert(name,file_name + ".xml")
            musicxml_file = file_name + ".xml"
        else:
            musicxml_file = name

        score = converter.parse(musicxml_file)
       
        #Test Clean
       # score = self.CleanScore(score)
        # ----------------
    
        self.m_current_file_name = musicxml_file
        self.score = score

        return self.GetJSON()

        #print(json_str)

        #with open('output_file.txt', 'w', encoding='utf-8') as file:
        #    file.write(json_str)

