import sys
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog
from UI.ui_main_window import Ui_MainWindow  # Import the generated UI Python code
from contextlib import suppress
import os
import webbrowser
import pyMeow as pm
import helper

GITHUB_URL: str = "https://github.com/CodeDuckers/JeffInjector/tree/main"
YOUTUBE_URL: str = "https://www.youtube.com/@codeduckers"
DISCORD_URL: str = "https://discord.gg/gcUGZjx8Rs"

IS_PROD: bool = True  # mark this flag to True before building

# pyside6-uic UI/main_window.ui -o UI/ui_main_window.py
# pyside6-rcc resources/jeff_profile.qrc -o jeff_profile_rc.py
# pyinstaller --onefile --icon=resources/JEFF.ico --name "JeffInjector" --windowed main.py

class MainWindow(QMainWindow):
    dll_path: str = None

    def __init__(self):
        super().__init__()

        # Set up the UI from the .ui file
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # region Setup default values
        # image_path: str = os.path.abspath("resources/JEFF_smaller.png") if not IS_PROD else "JEFF_smaller.png"
        # self.ui.jeff_image.setPixmap(QPixmap(image_path))
        self.ui.inject_status_label.setText("")
        self.ui.ac_status_label.setText("Anti-Cheat Status")
        self.ui.remove_dlls_label.setText("Remove DLLs")
        # endregion

        # region Setup Hyperlinks
        self.ui.github_link_label.setText(f'<a href="{GITHUB_URL}">GitHub</a>')
        self.ui.github_link_label.setOpenExternalLinks(True)
        self.ui.github_link_label.linkActivated.connect(lambda: webbrowser.open(GITHUB_URL))
        
        self.ui.youtube_link_label.setText(f'<a href="{YOUTUBE_URL}">Youtube</a>')
        self.ui.youtube_link_label.setOpenExternalLinks(True)
        self.ui.youtube_link_label.linkActivated.connect(lambda: webbrowser.open(YOUTUBE_URL))
        
        self.ui.discord_link_label.setText(f'<a href="{DISCORD_URL}">Discord</a>')
        self.ui.discord_link_label.setOpenExternalLinks(True)
        self.ui.discord_link_label.linkActivated.connect(lambda: webbrowser.open(DISCORD_URL))
        link_style = "background-color: rgb(177, 144, 151); color: rgb(189, 226, 235); border-radius: 5px;"
        self.ui.github_link_label.setStyleSheet(link_style)
        self.ui.youtube_link_label.setStyleSheet(link_style)
        self.ui.discord_link_label.setStyleSheet(link_style)

        # region Setup Button Connections
        self.ui.select_dll_button.clicked.connect(self.open_file_dialog)
        self.ui.inject_dll_button.clicked.connect(self.inject_dll)
        self.ui.remove_dlls_button.clicked.connect(self.remove_dlls)
        self.ui.ac_status_button.clicked.connect(self.disable_ac)
        # endregion

    def open_file_dialog(self):
        """
        Open the file dialog and get the selected file path
        """
        file_path, _ = QFileDialog.getOpenFileName(self, "Select a File", "", "DLL Files (*.dll);")
        
        if file_path:
            file_name = os.path.basename(file_path)

            self.ui.select_dll_button.setText(f"{file_name}")

            self.dll_path = file_path
        else:
            self.ui.select_dll_button.setText("Select")

    def inject_dll(self):
        """
        Inject the selected DLL into the target process
        """
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

        self.ui.inject_status_label.setText("Success" if success else "Failed")
        
    def remove_dlls():
        """
        Remove the DLLs that can cause crashes and issues
        """
        steam_path = os.path.expandvars(r"%PROGRAMFILES(X86)%\Steam")
        vdf_path = os.path.join(steam_path, "steamapps", "libraryfolders.vdf")
        libraries = [os.path.join(steam_path, "steamapps")]
        
        with suppress(Exception):
            try:
                with open(vdf_path, encoding="utf-8") as f:
                    for line in f:
                        parts = line.strip().strip('"').split('"')
                        if len(parts) >= 3 and parts[0].isdigit():
                            new_lib = os.path.join(parts[1].replace("\\\\", "\\"), "steamapps")
                            libraries.append(new_lib)
            except Exception as e:
                print(f"Error reading VDF file: {e}")  # Debug print for any errors reading VDF file
    
        install_path = None
        for lib in libraries:
            manifest = os.path.join(lib, f"appmanifest_2767030.acf")
            if os.path.exists(manifest):
                with suppress(Exception):
                    try:
                        with open(manifest, encoding="utf-8") as f:
                            for line in f:
                                if '"installdir"' in line:
                                    install_path = os.path.join(lib, "common", line.split('"')[-2])
                                    print(f"Install Path: {install_path}")  # Debug print for install_path
                                    break
                    except Exception as e:
                        print(f"Error reading manifest: {e}")  # Debug print for errors reading manifest
            if install_path:
                break
            
        if install_path is None:
            print("Install Path not found.")  # Debug print if no install_path is found
            return
    
        files = {
            "amd_fidelityfx_dx12.dll",
            "sl.interposer.dll",
            "sl.dlss_g.dll",
            "sl.reflex.dll"
        }
        print(f"Files to remove: {files}")  # Debug print for files to remove
    
        for root, _, filenames in os.walk(install_path):
            for filename in filenames:
                if filename in files:
                    print(f"Found DLL: {filename}")  # Debug print for found DLL
                    path = os.path.join(root, filename)
                    with suppress(Exception):
                        # os.remove(path)
                        print(f"Path to remove: {path}")  # Debug print the path instead of removing
    def disable_ac(self):
        """
        Disable the Anti-Cheat by terminating the heartbeat and AcSDK threads
        """
        try:
            process = pm.open_process("Marvel-Win64-Shipping.exe")
        except Exception as e:
            print(e)
            self.ui.ac_status_button.setText(f"Error")
            return
        
        heartbeat_success: bool = helper.terminate_thread_by_name("Marvel-Win64-Shipping.exe", "RTHeartBeat")
        acSDK_success: bool = helper.terminate_thread_by_name("Marvel-Win64-Shipping.exe", "AcSDKThread")
        if heartbeat_success and acSDK_success:
            self.ui.ac_status_button.setText("Disabled")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
