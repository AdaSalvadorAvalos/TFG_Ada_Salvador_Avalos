import json
from fractions import Fraction

class DataScoreElement:
    def __init__(self):
        self.type = ""
        self.duration = 0
        self.pitch = ""
        self.position = 0
        self.signature = ""
        self.voice = 0
        self.measure_id = 0
        self.id = ""

    def to_dict(self):   
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