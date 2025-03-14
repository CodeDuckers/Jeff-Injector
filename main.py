import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QPushButton
from UI.ui_main_window import Ui_MainWindow  # Import the generated UI Python code
import os
import webbrowser
import pyMeow as pm
import helper

GITHUB_URL: str = "https://github.com/CodeDuckers"
YOUTUBE_URL: str = "https://www.youtube.com/@codeduckers"
DISCORD_URL: str = "https://discord.gg/gcUGZjx8Rs"

# pyside6-uic UI/main_window.ui -o UI/ui_main_window.py
# pyside6-rcc resources/jeff_profile.qrc -o jeff_profile_rc.py

class MainWindow(QMainWindow):
    dll_path: str = None

    def __init__(self):
        super().__init__()

        # Set up the UI from the .ui file
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Setup default values
        self.ui.dll_name_label.setText("No file selected")
        self.ui.ac_status_label.setText("Running")

        # region Setup Hyperlinks
        self.ui.github_label.setText(f'<a href="{GITHUB_URL}">GitHub</a>')
        self.ui.github_label.setOpenExternalLinks(True)
        self.ui.github_label.linkActivated.connect(lambda: webbrowser.open(GITHUB_URL))
        
        self.ui.youtube_label.setText(f'<a href="{YOUTUBE_URL}">Youtube</a>')
        self.ui.youtube_label.setOpenExternalLinks(True)
        self.ui.youtube_label.linkActivated.connect(lambda: webbrowser.open(YOUTUBE_URL))
        
        self.ui.discord_label.setText(f'<a href="{DISCORD_URL}">Discord</a>')
        self.ui.discord_label.setOpenExternalLinks(True)
        self.ui.discord_label.linkActivated.connect(lambda: webbrowser.open(DISCORD_URL))
        # endregion

        # Connect the button to the open file dialog function
        self.ui.browse_dll_button.clicked.connect(self.open_file_dialog)
        self.ui.inject_dll_button.clicked.connect(self.inject_dll)
        self.ui.disable_ac_button.clicked.connect(self.disable_ac)

    def open_file_dialog(self):
        # Open the file explorer and get the selected file path with a filter for DLL files
        file_path, _ = QFileDialog.getOpenFileName(self, "Select a File", "", "DLL Files (*.dll);")
        
        if file_path:
            # Extract the filename from the full path
            file_name = os.path.basename(file_path)

            # If a file is selected, display the file name in the label
            self.ui.dll_name_label.setText(f"{file_name}")

            self.dll_path = file_path
        else:
            # If no file is selected, display "No file selected"
            self.ui.dll_name_label.setText("No file selected")

    def inject_dll(self):
        if self.dll_path is None:
            self.ui.inject_status_label.setText("No DLL selected")
            return

        try:
            process = pm.open_process("Marvel-Win64-Shipping.exe")
            # process = pm.open_process("Notepad.exe")
        except Exception as e:
            print(e)
            self.ui.inject_status_label.setText(f"Unable to find target process")
            return
        
        success: bool = pm.inject_library(process, self.dll_path)
        pm.close_process(process)
        self.ui.inject_status_label.setText("Success" if success else "Failed")
        
    def disable_ac(self):
        try:
            # process = pm.open_process("Marvel-Win64-Shipping.exe")
            process = pm.open_process("Notepad.exe")
        except Exception as e:
            print(e)
            self.ui.ac_status_label.setText(f"Unable to find process")
            return
        
        helper.terminate_thread_by_name("Marvel-Win64-Shipping.exe", "RTHeartBeat")
        helper.terminate_thread_by_name("Marvel-Win64-Shipping.exe", "AcSDKThread")
        self.ui.ac_status_label.setText("Disabled")

# Run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
