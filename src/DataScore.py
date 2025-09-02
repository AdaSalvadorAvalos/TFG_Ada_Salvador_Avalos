import json

class DataScore:
    def __init__(self):
        self.elements = []
        self.time_signature = "3/4"
        self.key_signature  = 0


    def to_dict(self):
        return {
            "elements": [element.to_dict() for element in self.elements],
            "time_signature": self.time_signature,
            "key_signature" : self.key_signature 
        }
    
    def get_measure_number(self,dtelement):
        return dtelement.measure_id * 10000 + dtelement.position

    def sort(self):
       self.elements = sorted(self.elements, key=self.get_measure_number)
   
    def addElement(self,element):
        self.elements.append(element)

