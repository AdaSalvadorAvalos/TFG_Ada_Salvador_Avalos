"""
ConverterFactory.py

This module defines the 'ConverterFactory' class, which serves as a factory for creating
instances of converter classes. It supports built-in converters ('ConverterFFMPEG' and 
'ConverterMusic21') as well as dynamically loaded custom Python plugin converters.
"""
from converterFFMPEG import ConverterFFMPEG
from converterMusic21 import ConverterMusic21
import importlib.util
import sys

class ConverterFactory():
    """
    Factory class for creating converter instances.

    The 'ConverterFactory' allows creating converter objects without specifying the exact class.
    Built-in converters include 'ConverterFFMPEG' and 'ConverterMusic21'. Custom converters 
    can also be added by placing a Python plugin file in the default plugins folder, which will
    be dynamically loaded at runtime.

    Methods:
        GetConverter(name):
            Returns an instance of a converter based on the provided name.
            - If 'name' is "ffmpeg", returns a 'ConverterFFMPEG' instance.
            - If 'name' is "music21", returns a 'ConverterMusic21' instance.
            - Otherwise, assumes 'name' corresponds to a custom plugin file in the plugins folder.
              Dynamically loads the plugin and returns an instance of its 'Converter' class.

    This dynamic loading mechanism allows developers to extend the application by adding new
    converters without modifying the main code.
    """
    def __init__(self):
        ...

    def GetConverter(self, name):
         """
        Create and return a converter instance based on the provided name.

        Args:
            name (str): The name of the converter to create. Can be "ffmpeg", "music21", or
                        the filename of a custom plugin (without path).

        Returns:
            Converter: An instance of the requested converter class.
         """
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