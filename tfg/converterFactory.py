from converterFFMPEG import ConverterFFMPEG
from converterMusic21 import ConverterMusic21
import importlib.util
import sys

class ConverterFactory():
    def __init__(self):
        ...

    def GetConverter(self, name):
         if name=="ffmpeg":
             return  ConverterFFMPEG()
         elif name=="music21":
             return  ConverterMusic21()
         else:
            #file_path = f'{name}.py'
            file_path = f'C:\\Users\\adasa\\Documents\\UPC\\TFG\\botones_desplegables\\tfg (3)\\tfg\\plugins\\{name}.py'  
            # Load the module dynamically
            spec = importlib.util.spec_from_file_location(name, file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Create an instance of the class Converter1
            converter_instance = module.Converter()

            return converter_instance