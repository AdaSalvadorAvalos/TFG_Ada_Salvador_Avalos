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

    

    def __init__(self):
        pygame.init()
         
        self.plugin_load = "ffmpeg"
        # Initialize variables to store the current playback position
        # self.playback_position = 0
    
    def SelectPlugin(self,name):
        if name == "":
            self.plugin_load = "converterFFMPEG"
        else:
            self.plugin_load = name
        
    def Save(self):
        # Write the score to the specified file in MusicXML format
        self.score.write('musicxml', fp= self.m_current_file_name )


    def SaveAs(self,filename):
        self.m_current_file_name  = filename
        self.Save()

         # Save the current playback position
        # self.playback_position = pygame.mixer.music.get_pos() / 1000  # Convert milliseconds to seconds

    def Stop(self):
         pygame.mixer.music.stop()

         # Save the current playback position
        # self.playback_position = pygame.mixer.music.get_pos() / 1000  # Convert milliseconds to seconds

    def Play(self):
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
        guid = uuid.uuid4()
        guid_str = str(guid)
        return guid_str
    

    def GetNote(self,note_id):
        for n in self.score.recurse().getElementsByClass(note.Note):
            if hasattr(n, 'internal_id') and n.internal_id == note_id:
                return n
        return None

    def NoteChange(self,note,num):
        try:
            note.pitch.transpose(num, inPlace=True)
        except Exception as e:
    # Handle any exception
            print(f"An error occurred: {e}")

      

    def IntervalChange(self,num,selection):
          
        for note_id in selection:
                note = self.GetNote(note_id)
                self.NoteChange(note,num)


        return self.GetJSON()

    def NoteRemove(self,note):
        parent_measure = note.getContextByClass(stream.Measure)

        # Remove the note from its measure 
        parent_measure.remove(note)

        # self.score.remove(note)
        # del note

    def RemoveNotes(self,selection):
        for note_id in selection:
            note = self.GetNote(note_id)
            self.NoteRemove(note)
        return self.GetJSON()

    def GetMeasure(self, p_measure_id):
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

        self.score.flatten().keySignature._setSharps(new_key_sig)   
        return self.GetJSON()


    def GetJSON(self):
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

        # MIRAR SI ES XML

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

