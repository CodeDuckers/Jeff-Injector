import sys
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog
from PySide6.QtCore import QCoreApplication, QThread, Signal, QObject
from UI.ui_main_window import Ui_MainWindow  # Import the generated UI Python code
from contextlib import suppress
import os
import webbrowser
import pyMeow as pm
import helper
import time

GITHUB_URL: str = "https://github.com/CodeDuckers/JeffInjector/tree/main"
YOUTUBE_URL: str = "https://www.youtube.com/@codeduckers"
DISCORD_URL: str = "https://discord.gg/gcUGZjx8Rs"
IS_PROD: bool = True  # mark this flag to True before building
DLLS_TO_FIND = {
    "amd_fidelityfx_dx12.dll",
    "sl.interposer.dll",
    "sl.dlss_g.dll",
    "sl.reflex.dll"
}
JEFF_VERSION: str = "v1.0.2"
# pyside6-uic UI/main_window.ui -o UI/ui_main_window.py
# pyside6-rcc resources/jeff_profile.qrc -o jeff_profile_rc.py
# pyinstaller --onefile --icon=resources/JEFF.ico --name "JeffInjector" --windowed main.py

class MainWindow(QMainWindow):
    dll_path: str = None

    def __init__(self):
        super().__init__()

        # Initialize UI from the generated .ui file
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Set default UI text values for status indicators
        self.ui.inject_status_label.setText("")
        self.ui.ac_status_label.setText("Anti-Cheat Status")
        self.ui.remove_dlls_label.setText("Remove DLLs")

        # Set up external hyperlink labels with styling and click behavior
        self.ui.github_link_label.setText(f'<a href="{GITHUB_URL}">GitHub</a>')
        self.ui.github_link_label.setOpenExternalLinks(True)
        self.ui.github_link_label.linkActivated.connect(lambda: webbrowser.open(GITHUB_URL))
        self.ui.youtube_link_label.setText(f'<a href="{YOUTUBE_URL}">Youtube</a>')
        self.ui.youtube_link_label.setOpenExternalLinks(True)
        self.ui.youtube_link_label.linkActivated.connect(lambda: webbrowser.open(YOUTUBE_URL))
        self.ui.discord_link_label.setText(f'<a href="{DISCORD_URL}">Discord</a>')
        self.ui.discord_link_label.setOpenExternalLinks(True)
        self.ui.discord_link_label.linkActivated.connect(lambda: webbrowser.open(DISCORD_URL))

        # Apply consistent styling to all link labels
        link_style = "background-color: rgb(177, 144, 151); color: rgb(189, 226, 235); border-radius: 5px;"
        self.ui.github_link_label.setStyleSheet(link_style)
        self.ui.youtube_link_label.setStyleSheet(link_style)
        self.ui.discord_link_label.setStyleSheet(link_style)

        # Connect buttons to their respective event handlers
        self.ui.select_dll_button.clicked.connect(self.open_file_dialog)
        self.ui.inject_dll_button.clicked.connect(self.inject_dll)
        self.ui.remove_dlls_button.clicked.connect(self.remove_dlls)
        self.ui.ac_status_button.clicked.connect(self.disable_ac)

        # Set application title with version
        self.ui.app_title_label.setText(QCoreApplication.translate("MainWindow", f"Jeff Injector {(JEFF_VERSION)}", None))

        # Populate DLL status count on application startup
        self.count_dlls()

        self.checker_thread.start()

    def closeEvent(self, event):
        self.checker_thread.worker.running = False
        self.checker_thread.quit()
        self.checker_thread.wait()
        super().closeEvent(event)

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
        except Exception as e:
            print(e)
            self.ui.inject_status_label.setText("Unable to find target process")
            return
        success: bool = pm.inject_library(process, self.dll_path)
        self.ui.inject_status_label.setText("Success" if success else "Failed")

    def get_install_path(self):
        """
        Retrieve the installation path of the game by parsing Steam's libraryfolders.vdf and appmanifest
        """
        steam_path = os.path.expandvars(r"%PROGRAMFILES(X86)%\Steam")
        vdf_path = os.path.join(steam_path, "steamapps", "libraryfolders.vdf")
        libraries = [os.path.join(steam_path, "steamapps")]
        with suppress(Exception):
            with open(vdf_path, encoding="utf-8") as f:
                for line in f:
                    parts = line.strip().strip('"').split('"')
                    if len(parts) >= 3 and parts[0].isdigit():
                        libraries.append(os.path.join(parts[1].replace("\\\\", "\\"), "steamapps"))
        for lib in libraries:
            manifest = os.path.join(lib, "appmanifest_2767030.acf")
            if os.path.exists(manifest):
                with suppress(Exception):
                    with open(manifest, encoding="utf-8") as f:
                        for line in f:
                            if '"installdir"' in line:
                                return os.path.join(lib, "common", line.split('"')[-2])
        return None

    def find_dlls(self, install_path):
        """
        Recursively search the install path for known DLL filenames to identify injected DLLs
        """
        results = []
        for root, _, filenames in os.walk(install_path):
            for filename in filenames:
                if filename in DLLS_TO_FIND:
                    results.append(os.path.join(root, filename))
        return results

    def count_dlls(self):
        """
        Count how many known DLLs are present in the installation folder and update the UI accordingly
        """
        install_path = self.get_install_path()
        if install_path is None:
            self.ui.remove_dlls_label.setText(f"Remove DLLs 0 / {len(DLLS_TO_FIND)}")
            return
        found_paths = self.find_dlls(install_path)
        self.ui.remove_dlls_label.setText(f"Remove DLLs {len(found_paths)} / {len(DLLS_TO_FIND)}")
        if len(found_paths) == 0:
            self.ui.remove_dlls_button.setText(QCoreApplication.translate("MainWindow", u"Removed", None))
        else:
            self.ui.remove_dlls_button.setText(QCoreApplication.translate("MainWindow", u"Remove", None))

    def remove_dlls(self):
        """
        Remove all identified DLLs from the game installation directory and refresh the count display
        """
        install_path = self.get_install_path()
        if install_path is None:
            return
        for path in self.find_dlls(install_path):
            with suppress(Exception):
                os.remove(path)
        self.count_dlls()

    def disable_ac(self):
        """
        Disable the Anti-Cheat by terminating the heartbeat and AcSDK threads
        """
        try:
            process = pm.open_process("Marvel-Win64-Shipping.exe")
        except Exception as e:
            print(e)
            self.ui.ac_status_button.setText("Error")
            return
        heartbeat_success: bool = helper.terminate_thread_by_name("Marvel-Win64-Shipping.exe", "RTHeartBeat")
        acSDK_success: bool = helper.terminate_thread_by_name("Marvel-Win64-Shipping.exe", "AcSDKThread")
        if heartbeat_success and acSDK_success:
            self.ui.ac_status_button.setText("Disabled")

class GameCheckerWorker(QObject):
    status_updated = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        """
        Initialize the worker and set a running flag to control loop execution
        """
        self.running = True

    def stop(self):
        """
        Set running to False so the loop in run() exits cleanly
        """
        self.running = False

    def run(self):
        """
        Continuously check if the target game process is running and emit the appropriate status
        """
        while self.running:
            process = None
            with suppress(Exception):
                """
                Suppress any exceptions raised while trying to open the game process
                """
                process = pm.open_process("Marvel-Win64-Shipping.exe")
            if process is not None:
                """
                Emit status with a checkmark if process is found
                """
                self.status_updated.emit("Anti-Cheat Status {Game: ✅}")
            else:
                """
                Emit status with a cross if process is not found
                """
                self.status_updated.emit("Anti-Cheat Status {Game: ❌}")
            for _ in range(50):  # sleep 5s in 100ms steps to exit faster
                if not self.running:
                    break
                QThread.msleep(100)

class GameCheckerThread(QThread):
    def __init__(self, ui_label):
        super().__init__()
        """
        Initialize the thread and connect the worker's signal to the UI label
        """
        self.worker = GameCheckerWorker()
        self.worker.status_updated.connect(ui_label.setText)

    def run(self):
        """
        Start the worker's run loop in the thread
        """
        self.worker.run()

    def stop(self):
        """
        Stop the worker to halt the run loop
        """
        self.worker.stop()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
