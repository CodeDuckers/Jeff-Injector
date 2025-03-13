import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QPushButton
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from UI.ui_main_window import Ui_MainWindow  # Import the generated UI Python code
import os
import webbrowser
import dll

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

        # Find the PID of the target process
        process_name = "Marvel-Win64-Shipping.exe"
        # process_name = "notepad.exe"
        pid = dll.find_process_pid(process_name)
        if pid is None:
            print(f"Process {process_name} not found!")
            return

        print(f"Found process with PID: {pid}")

        # Open the target process with all access
        process_handle = dll.OpenProcess(dll.PROCESS_ALL_ACCESS, False, pid)
        if not process_handle:
            print(f"Unable to open process with PID {pid}")
            return

        # Allocate memory in the target process for the DLL path
        dll_path_bytes = self.dll_path.encode('utf-8')
        allocated_memory = dll.VirtualAllocEx(process_handle, 0, len(dll_path_bytes), dll.MEM_COMMIT | dll.MEM_RESERVE, dll.PAGE_READWRITE)
        if not allocated_memory:
            print("Failed to allocate memory in target process.")
            return

        # Write the DLL path to the allocated memory
        written = dll.ctypes.c_int(0)
        dll.WriteProcessMemory(process_handle, allocated_memory, dll_path_bytes, len(dll_path_bytes), dll.ctypes.byref(written))

        # Create a remote thread in the target process to call LoadLibraryA
        thread_id = dll.ctypes.c_ulong(0)
        remote_thread = dll.CreateRemoteThread(process_handle, None, 0, dll.LoadLibraryA, allocated_memory, 0, dll.ctypes.byref(thread_id))
        if not remote_thread:
            print("Failed to create remote thread.")
            return

        print(f"Successfully injected DLL into process with PID {pid}")
        self.ui.inject_status_label.setText("SUCCESS")

# Run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
