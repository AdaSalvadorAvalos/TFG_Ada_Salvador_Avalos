"""
main.py

Main application script for the Interactive MusicXML Transcriber and Editor.

This module launches a PyQt5-based desktop application with an embedded
QWebEngineView (Chromium-based) to display the HTML/JavaScript interface.
It provides functionality for loading, editing, and saving MusicXML scores
derived from MP3 or MIDI files.

Communication between Python and JavaScript is handled via a JSON-based
bridge (PythonBridge), allowing the web interface to trigger actions
in Python and vice versa. All updates to the interface are executed
through a single method ('g_python_com.HandleMessage') for consistency
and easier future adaptation to a web service.

Classes:
    PythonBridge(QObject):
        Handles incoming JSON messages from JavaScript and dispatches
        events to the appropriate methods in the main application window.

    WebViewWindow(QMainWindow):
        Main window that embeds the web interface. Handles UI actions
        such as loading files, saving, editing notes, applying transformations,
        and communicating updates to JavaScript.
"""

import os
import json

from MainControl import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWebChannel import QWebChannel

class PythonBridge(QObject):
    """
    Facilitates communication between Python and JavaScript.

    Inherits from PyQt5's QObject. The 'handleMessage' method receives messages
    from JavaScript as JSON strings and dispatches them to the appropriate
    methods in the main application window. Acts as an event dispatcher
    based on the 'id' field in the received JSON.

    Methods:
        handleMessage(message):
            Parses a JSON message from JavaScript and calls the corresponding
            method in the 'WebViewWindow' instance.
    """
    @pyqtSlot(str)
    def handleMessage(self, message):
        """Handle a JSON message from JavaScript and dispatch the corresponding event."""
        print(f"Message from JavaScript: {message}")
        obj = json.loads(message)

        # Event Dispatcher     
        if obj['id']=='LoadFile':
            window.LoadFile()
        elif obj['id']=='SelectPlugin':
            window.SelectPlugin(obj['name'])
        elif obj['id']=='Play':
            window.m_main_control.Play()
        elif obj['id']=='Stop':
            window.m_main_control.Stop()
        elif obj['id']=='Save':
            window.m_main_control.Save()
        elif obj['id']=='IntervalChange':
            window.IntervalChange(obj['num'],obj['selection'])
        elif obj['id']=='RemoveNotes':
            window.RemoveNotes(obj['selection'])
        elif obj['id']=='SaveAs':
            window.SaveAs()
        elif obj['id']=='AddNote':
            window.AddNote(obj['measure_id'],obj['x'],obj['y'],obj['width'],obj['height'],obj['note'],obj['staff'],obj['duration'],obj['octave'],obj['accidental'])  
        elif obj['id']=='MirrorEffect':             
            window.MirrorEffect()  
        elif obj['id']=='change_time_signature_at_start':             
            window.change_time_signature_at_start(obj['new_time_sig'])  
        elif obj['id']=='change_key_signature_at_start':             
            window.change_key_signature_at_start(obj['new_key_sig'])  
            


class WebViewWindow(QMainWindow):
    """
    Main application window with embedded web interface.

    Inherits from PyQt5's QMainWindow. Embeds a QWebEngineView to display the
    HTML/JavaScript interface. Handles all UI interactions, including:
        - Loading and saving score files.
        - Sending commands to the JavaScript interface via 'executeJavaScript'.
        - Adding, removing, or modifying notes.
        - Changing time and key signatures.
        - Plugin selection and interval editing.

    Methods:
        executeJavaScript(js_code):
            Sends JavaScript code to the embedded web view for execution.
        LoadFile():
            Opens a file dialog to select a score file and sends it to the interface.
        SaveAs():
            Opens a file dialog to save the current score.
        IntervalChange(num, selection):
            Updates note intervals in the score and refreshes the interface.
        SelectPlugin(name):
            Selects a converter plugin for transformations.
        AddNote(...):
            Adds a note to the score and updates the interface.
        MirrorEffect():
            Mirrors selected notes in the score and updates the interface.
        change_time_signature_at_start(new_time_sig):
            Changes the starting time signature of the score.
        change_key_signature_at_start(new_key_sig):
            Changes the starting key signature of the score.
        RemoveNotes(selection):
            Removes selected notes from the score.
    """
    def __init__(self):
        super().__init__()

        self.m_main_control = MainControl()
        self.webview = QWebEngineView()
  
        self.resizeEvent = self.onResize


       # self.webview.setUrl(QUrl.fromLocalFile("file:///C:/Users/adasa/Documents/UPC/TFG/codigo_pruebas/nav.html"))  # Set the local file path here

        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "html/main.html"))
        local_url = QUrl.fromLocalFile(file_path)
        self.webview.load(local_url)
       # self.webview.setUrl(QUrl.fromLocalFile("file:///nav.html"))  # Set the local file path here


        self.setCentralWidget(self.webview)

        # Expose Python object to JavaScript
        self.webview.page().runJavaScript("""
            window.myPythonObject = {
                callPythonFunction: function(data) {
                    // Call Python function from JavaScript
                    pywebview.handleMessage(data);
                }
            };
        """, QWebEngineScript.MainWorld)

      
        # Create an instance of the PythonBridge
        self.bridge = PythonBridge()

        # Expose the Python object to JavaScript
        self.channel = QWebChannel()
        self.channel.registerObject('pyBridge', self.bridge)
        self.webview.page().setWebChannel(self.channel)

        self.setMinimumSize(800, 800)
        self.setGeometry(0, 0, 800, 800)
        self.setWindowTitle("TFG Ada Salvador Avalos")

       ## QTimer.singleShot(2000, self.executeJavaScript)

    def onResize(self, event):
        # Resize the web view whenever the main window is resized
        self.webview.setFixedSize(event.size())


    def IntervalChange(self,num,selection):
        """
        Update note intervals for the selected notes in the score.

        Args:
            num (int): Interval value to apply.
            selection (list): Selected notes or elements to modify.
        """
        json_code = self.m_main_control.IntervalChange(num,selection)
        command = f"g_python_com.HandleMessage('OnLoadFile','{json_code}','','')"
        self.executeJavaScript(command)

    def SelectPlugin(self,name):
        """
        Select a converter plugin for transformations.

        Args:
            name (str): Name of the plugin to select.
        """
        self.m_main_control.SelectPlugin(name)
        command = f"g_python_com.HandleMessage('alert','Plugin updated','','')"
        self.executeJavaScript(command)

    def change_time_signature_at_start(self,new_time_sig):
        """
        Change the starting time signature of the score.

        Args:
            new_time_sig (str): New time signature (e.g., "4/4").
        """
        json_code = self.m_main_control.change_time_signature_at_start(new_time_sig)
        command = f"g_python_com.HandleMessage('OnLoadFile','{json_code}','','')"
        self.executeJavaScript(command)

    def change_key_signature_at_start(self,new_key_sig):
        """
        Change the starting key signature of the score.

        Args:
            new_key_sig (int): New key signature (number of sharps or flats).
        """
        json_code = self.m_main_control.change_key_signature_at_start(new_key_sig)
        command = f"g_python_com.HandleMessage('OnLoadFile','{json_code}','','')"
        self.executeJavaScript(command)



    def RemoveNotes(self,selection):
        """
        Remove selected notes from the score and update the interface.

        Args:
            selection (list): Notes or elements to remove.
        """
        json_code = self.m_main_control.RemoveNotes(selection)
        command = f"g_python_com.HandleMessage('OnLoadFile','{json_code}','','')"
        self.executeJavaScript(command)

    def AddNote(self,p_measure_id,p_x,p_y,p_width,p_height,p_note,staff,duration,octave, accidental):
        """
        Add a new note to the score and update the interface.

        Args:
            p_measure_id (int): Measure number where the note is added.
            p_x, p_y, p_width, p_height (float): Coordinates and size for placement.
            p_note (str): Note name (e.g., "C").
            staff (int): Staff number for the note.
            duration (float): Duration in beats.
            octave (int): Octave of the note.
            accidental (str): Accidental symbol, if any (e.g., "#", "b").
        """
        json_code = self.m_main_control.AddNote(p_measure_id,p_x,p_y,p_width,p_height,p_note,staff,duration,octave,accidental)
        command = f"g_python_com.HandleMessage('OnLoadFile','{json_code}','','')"
        self.executeJavaScript(command)

    def MirrorEffect(self):
        """
        Apply a mirror effect to the selected notes and update the interface.
        """
        json_code = self.m_main_control.MirrorEffect()
        command = f"g_python_com.HandleMessage('OnLoadFile','{json_code}','','')"
        self.executeJavaScript(command)

    def show_save_file_dialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "All Files (*);;Text Files (*.txt)", options=options)
        return file_path

    
    def SaveAs(self):
        """
        Open a save file dialog to save the current score to a chosen location.

        Displays a success or error message using QMessageBox.
        """
        try:
            
            path = self.show_save_file_dialog()
            self.m_main_control.SaveAs(path)
                
            QMessageBox.information(self, "File Saved", f"File saved successfully to {path}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not save file: {e}")


    def LoadFile(self):
        """
        Open a file dialog to select an existing score file and load it
        into the interface.

        Sends the score data to the JavaScript side using 'g_python_com.HandleMessage'.
        """
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter("All Files (*)")
        if file_dialog.exec_():
            selected_files = file_dialog.selectedFiles()
            print("Selected file:", selected_files[0])
            json_code = self.m_main_control.LoadFile(selected_files[0])
         #   print(json_code)
            command = f"g_python_com.HandleMessage('OnLoadFile','{json_code}','','')"
            #command = "g_python_com.HandleMessage('OnLoadFile','" + json_code + "','','')"
          #  print(command)
            self.executeJavaScript(command)

        #self.executeJavaScript("Start('C#5/q, B4, A4, G#4')")


    def executeJavaScript(self, js_code):
        """
        Execute JavaScript code in the embedded web interface.

        Args:
            js_code (str): JavaScript code to run in the QWebEngineView.
        """
        # Define the JavaScript function call with parameter
           
        # Execute the JavaScript code
        self.webview.page().runJavaScript(js_code)


if __name__ == "__main__":
    """
    Application entry point.

    Initializes the QApplication, creates the main WebViewWindow,
    and starts the PyQt event loop.
    """
    import sys

    app = QApplication(sys.argv)
    window = WebViewWindow()
    window.show()
    sys.exit(app.exec_())
