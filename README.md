# Interactive Interface for Visualizing and Editing MusicXML Transcriptions

Full source code of my Bachelor's final project, including all files required to run the application.

This project transcribes piano monophonic audio files (MP3 or MIDI) into MusicXML scores and provides an interactive interface for viewing, editing, and applying musical effects.

## Key Features

- Convert audio files into MusicXML scores for display and manipulation.  
- Edit scores by inserting, deleting, or modifying notes and other musical parameters.  
- Apply built-in filters or import custom Python plugins for new effects.  
- Listen to changes in real-time through the interface.  

> **Note:** Automatic musical transcription remains a challenging research area. This tool allows users to review and correct possible transcription errors before saving, ensuring greater accuracy.

## Built With

- **Core Engine:** Python (`music21`, `pygame`, `PyQt5`)  
- **Frontend:** JavaScript, HTML, SVG, jQuery  
- **Score Rendering:** [VexFlow](https://github.com/0xfe/vexflow)  
- **UI Enhancements:** [Superfish.js](https://github.com/joeldbirch/superfish) + MegaFish menus  


## Demonstration Video
Watch the project in action in this short demo:

[![Demo Video](assets/demo_img.png)](https://youtu.be/34K5PG9SdkM)


## Installation
> **Note:** Currently compatible with **Windows only**.

1. Install [WSL (Windows Subsystem for Linux)](https://learn.microsoft.com/en-us/windows/wsl/install) by following the instructions on the official page.
2. Install [WaoN](https://kichiki.github.io/waon/).
3. Install the required Python packages by running:

````
pip install -r requirements.txt
````

## Usage

### Setup

To try the transformations from MP3 to MusicXML:

1. Make sure you have installed the **WaoN** program.  
2. Ensure that WaoN is accessible from your WSL environment. Update the path in your code as needed:

```python
linux_command = f"/home/home/WaoN/waon -i {file_source} -o {file_target}"
```

To test the selection of new plugins, update the plugin path in your code:
```python
file_path = f'C:\\Users\\adasa\\Documents\\UPC\\TFG\\dropdown_buttons\\tfg (3)\\tfg\\plugins\\{name}.py'
```
### Interface
Once installed, you can launch the application and use the menu options shown in the [demonstration video](https://youtu.be/34K5PG9SdkM).

#### File
- **Open**: load an MP3, MIDI, or MusicXML file.
- **Save / Save As**: export your score.  
- **Select Converter Plug-in**: choose a custom converter by uploading your Python plugin file into the `plugins` folder. Then, from the menu (**File → Select Converter Plug-in**), enter the plugin’s filename in the dialog box to load it.

#### Sound Control
- **Play / Stop**: listen to the current score or stop playback.  

#### Edit
- **Select All**: select all notes in the score.
- **Unselect All**: clear the current selection. 

#### Score Control
- **Change Interval**: transpose selected notes by an integer value between -12 and 12.
- **Mirror Melody**: reverse the melody of the selected notes.
- **Remove Notes**: delete selected notes  
- **Add Note**: insert a note by choosing letter, accidental (♭, ♯), and octave. 
- **Change Time Signature (at start)**: set a new time signature by entering values such as 2/4, 3/4, etc. 
  *Note: this only changes the written time signature and does not alter the distribution of notes within measures.*  
- **Change Key Signature (at start)**: set a new key signature using a dropdown menu that lists each major key together with its relative minor (sharing the same key signature).



## Future Development

- Transform the application into a web service.  
- Integrate AI-based technologies to improve transcription accuracy.
- Add support for polyphony (multiple simultaneous notes or instruments).  
