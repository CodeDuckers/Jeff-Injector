from contextlib import suppress
from PySide6.QtCore import QCoreApplication, QThread, Signal, QObject, Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from UI.ui_main_window import Ui_MainWindow  # Import the generated UI Python code
import os
import pyMeow as pm
import sys
import time
import webbrowser
import ctypes
import subprocess
import traceback
from datetime import datetime
EXE_NAME = "Marvel-Win64-Shipping.exe"
GITHUB_URL: str = "https://github.com/CodeDuckers/JeffInjector/tree/main"
YOUTUBE_URL: str = "https://www.youtube.com/@codeduckers"
DISCORD_URL: str = "https://discord.gg/gcUGZjx8Rs"
IS_PROD: bool = True  # mark this flag to True before building
DLLS_TO_FIND = {
    "amd_fidelityfx_dx12.dll",
    "sl.interposer.dll",
    "sl.dlss_g.dll",
    "sl.reflex.dll",
    "QtWebEngineProcess.exe"
}
JEFF_VERSION: str = "v1.0.7"
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
        # self.ui.remove_dlls_label.setText("UnWanted DLLs")
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
        # Set application title with version
        self.ui.app_title_label.setText(QCoreApplication.translate("MainWindow", f"Jeff Injector {(JEFF_VERSION)}", None))
        # Populate DLL status count on application startup
        self.count_dlls()
        # Pass 'self' (MainWindow) to the GameCheckerThread, as it contains count_dlls
        self.checker_thread = GameCheckerThread(self.ui.ac_status_label, self)
        self.checker_thread.start()
        self.checker_thread.worker.inject_visibility_changed.connect(self.update_inject_visibility)
    def closeEvent(self, event):
        self.checker_thread.worker.running = False
        self.checker_thread.quit()
        self.checker_thread.wait()
        super().closeEvent(event)
    def update_inject_visibility(self, visible: bool):
        if visible:
            self.ui.inject_dll_button.show()
            self.checker_thread.worker.running = False
        else:
            self.ui.inject_dll_button.hide()

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
            process = pm.open_process(f"{(EXE_NAME)}")
        except Exception as e:
            print(e)
            self.ui.inject_status_label.setText("Unable to find target process")
            return
        success = pm.inject_library(process, self.dll_path)
        self.ui.select_dll_button.setText("Select")
        self.dll_path = None
        self.ui.inject_status_label.setText("Success" if success else "Failed")
        if success:
            self.checker_thread.worker.running = False
            self.checker_thread.quit()
            self.checker_thread.wait()
            QCoreApplication.quit()

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
            return 0
        found_paths = self.find_dlls(install_path)
        return len(found_paths)
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
class GameCheckerWorker(QObject):
    inject_visibility_changed = Signal(bool)
    status_updated = Signal(str)
    def __init__(self, dll_counter, parent=None):
        super().__init__(parent)
        self.dll_counter = dll_counter
        self.running = True
        self.initializing = True
        self.game_start_time = None
        self.jeff_satisfied = False
        self.next_check_time = None
        self.ultTime = 15
    def stop(self):
        self.running = False
    def run(self):
        while self.running:
            if self.jeff_satisfied is True:
                self.inject_visibility_changed.emit(True)
                # Show Inject BTN
            if self.jeff_satisfied is False:
                self.inject_visibility_changed.emit(False)
                # Hide Inject BTN
            game_status = "❌"
            dll_count = "??"
            ult_status = "??"
            current_time = time.time()
            self.next_check_time = current_time
            # Dll Check
            dll_count = self.dll_counter.count_dlls()
            result = subprocess.run(
                ["tasklist", "/FI", f"IMAGENAME eq {EXE_NAME}"],
                capture_output=True,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            if 0 != dll_count and f"{(EXE_NAME)}" in result.stdout:
                ctypes.windll.user32.MessageBoxW(0, "Unwanted DLLs: found\nClosing game\nPlease reopen Jeff without the game open", "DLL Warning", 0)
                subprocess.run(["taskkill", "/F", "/IM", f"{(EXE_NAME)}"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                sys.exit(0)
            # Dll Check
            try:
                process = pm.open_process(f"{(EXE_NAME)}")
                if process is not None:
                    game_status = "✅"
                    if self.game_start_time is None:
                        self.game_start_time = current_time
                    elapsed = current_time - self.game_start_time
                    if elapsed >= self.ultTime:
                        try:
                            self.jeff_satisfied = True # Bypass
                        except Exception:
                            if self.initializing:
                                print("initializing self")
                            else:
                                self.game_start_time = current_time
                    else:
                        percent = min(int((elapsed / self.ultTime) * 100), 100)
                        ult_status = f"Charging Ult! ({percent}%)"
                else:
                    self.game_start_time = None
                    self.next_check_time = None
            except Exception:
                if self.initializing:
                    game_status = "??"
            self.status_updated.emit(
                f"Status\n{{Game: {game_status}}}\n{{Ult: {ult_status}}}\n{{Unwanted DLLs: {dll_count}}}"
            )
            self.initializing = False
            for _ in range(20):
                if not self.running:
                    break
                QThread.msleep(100)

class GameCheckerThread(QThread):
    def __init__(self, ui_label, dll_counter):
        """
        Create and configure the game checker thread, wiring UI and control signals
        """
        super().__init__()
        self.worker = GameCheckerWorker(dll_counter)  # Pass the MainWindow instance here
        self.worker.status_updated.connect(ui_label.setText, Qt.QueuedConnection)
    def run(self):
        """
        Start the worker's run loop within this thread
        """
        self.worker.run()
    def stop(self):
        """
        Stop the worker from running
        """
        self.worker.stop()
if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        window = MainWindow()
        window.remove_dlls()
        window.show()
        sys.exit(app.exec())
    except Exception as e:
        # Format timestamp for filename
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        log_filename = f"jeff-crash{timestamp}.log"
        # Get traceback as string
        tb_str = traceback.format_exc()
        # Save to log file
        with open(log_filename, "w", encoding="utf-8") as f:
            f.write(tb_str)
        # Show error in message box
        error_message = f"An unexpected error occurred:\n{e}\n\nSee {log_filename} for details."
        # Ensure QApplication exists for QMessageBox
        if QApplication.instance() is None:
            app = QApplication(sys.argv)
        QMessageBox.critical(None, "Jeff Injector Crash", error_message)
        sys.exit(1)
