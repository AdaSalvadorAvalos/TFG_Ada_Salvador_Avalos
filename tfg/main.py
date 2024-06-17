import os
import json

from MainControl import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWebChannel import QWebChannel

class PythonBridge(QObject):
    @pyqtSlot(str)
    def handleMessage(self, message):
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
        json_code = self.m_main_control.IntervalChange(num,selection)
        command = f"g_python_com.HandleMessage('OnLoadFile','{json_code}','','')"
        self.executeJavaScript(command)

    def SelectPlugin(self,name):
        self.m_main_control.SelectPlugin(name)
        command = f"g_python_com.HandleMessage('alert','Plugin updated','','')"
        self.executeJavaScript(command)

    def change_time_signature_at_start(self,new_time_sig):
        json_code = self.m_main_control.change_time_signature_at_start(new_time_sig)
        command = f"g_python_com.HandleMessage('OnLoadFile','{json_code}','','')"
        self.executeJavaScript(command)

    def change_key_signature_at_start(self,new_key_sig):
        json_code = self.m_main_control.change_key_signature_at_start(new_key_sig)
        command = f"g_python_com.HandleMessage('OnLoadFile','{json_code}','','')"
        self.executeJavaScript(command)



    def RemoveNotes(self,selection):
        json_code = self.m_main_control.RemoveNotes(selection)
        command = f"g_python_com.HandleMessage('OnLoadFile','{json_code}','','')"
        self.executeJavaScript(command)

    def AddNote(self,p_measure_id,p_x,p_y,p_width,p_height,p_note,staff,duration,octave, accidental):
        json_code = self.m_main_control.AddNote(p_measure_id,p_x,p_y,p_width,p_height,p_note,staff,duration,octave,accidental)
        command = f"g_python_com.HandleMessage('OnLoadFile','{json_code}','','')"
        self.executeJavaScript(command)

    def MirrorEffect(self):
        json_code = self.m_main_control.MirrorEffect()
        command = f"g_python_com.HandleMessage('OnLoadFile','{json_code}','','')"
        self.executeJavaScript(command)

    def show_save_file_dialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "All Files (*);;Text Files (*.txt)", options=options)
        return file_path

    
    def SaveAs(self):
        try:
            
            path = self.show_save_file_dialog()
            self.m_main_control.SaveAs(path)
                
            QMessageBox.information(self, "File Saved", f"File saved successfully to {path}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not save file: {e}")


    def LoadFile(self):

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
        # Define the JavaScript function call with parameter
           
        # Execute the JavaScript code
        self.webview.page().runJavaScript(js_code)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = WebViewWindow()
    window.show()
    sys.exit(app.exec_())
