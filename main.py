from contextlib import suppress
from datetime import datetime
from PySide6.QtCore import QCoreApplication, QThread, Signal, QObject, Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from UI.ui_main_window import Ui_MainWindow  # Import the generated UI Python code
import ctypes
import logging
import os
import pyMeow as pm
import subprocess
import sys
import time
import traceback
import webbrowser
EXE_NAME = "Marvel-Win64-Shipping.exe"
GITHUB_URL: str = "https://github.com/CodeDuckers/JeffInjector/tree/main"
YOUTUBE_URL: str = "https://www.youtube.com/@codeduckers"
DISCORD_URL: str = "https://discord.gg/gcUGZjx8Rs"
IS_PROD: bool = True  # mark this flag to True before building
UNWANTEDFILES_TO_FIND = {
    "amd_fidelityfx_dx12.dll",
    "sl.interposer.dll",
    "sl.dlss_g.dll",
    "sl.reflex.dll"
}
JEFF_VERSION: str = "v1.0.9"

log_dir = "JeffLogs"
os.makedirs(log_dir, exist_ok=True)
timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
log_filename = os.path.join(log_dir, f"jeff_{JEFF_VERSION}-{timestamp}.log")
logging.basicConfig(
    filename=log_filename,
    level=logging.INFO,
    format="[%(asctime)s][%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger()

# pyside6-uic UI/main_window.ui -o UI/ui_main_window.py
# pyside6-rcc resources/jeff_profile.qrc -o jeff_profile_rc.py
# pyinstaller --onefile --icon=resources/JEFF.ico --name "JeffInjector" --windowed main.py

class MainWindow(QMainWindow):
    dll_path: str = None
    def show_unwantedfiles_message(self):
        install_path = self.get_install_path()
        if install_path is None:
            QMessageBox.warning(self, "Unwanted DLLs", "Game install path not found.")
            return
        found_paths = self.find_unwantedfiles(install_path)
        if not found_paths:
            QMessageBox.information(self, "Unwanted DLLs", "No unwanted DLLs found.")
            return
        # Extract just the filenames for display
        found_files = [os.path.basename(p) for p in found_paths]
        msg = "Unwanted DLLs found:\n" + "\n".join(found_files)
        QMessageBox.warning(self, "Unwanted DLLs", msg)

    def __init__(self):
        self._install_path_cache = None
        self._unwantedfiles_cache = None
        self._unwantedfiles_cache_time = 0
        logger.info("MainWindow : __init__ called")
        super().__init__()
        logger.info("MainWindow : UI setup starting")
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.inject_status_label.setText("")
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
        self.ui.select_dll_button.clicked.connect(self.open_file_dialog)
        self.ui.inject_dll_button.clicked.connect(self.inject_dll)
        self.ui.app_title_label.setText(QCoreApplication.translate("MainWindow", f"Jeff Injector {JEFF_VERSION}", None))
        logger.info("MainWindow : UI setup complete")
        self.count_unwantedfiles()
        self.checker_thread = GameCheckerThread(self.ui.ac_status_label, self)
        self.checker_thread.start()
        logger.info("MainWindow : GameCheckerThread started")
        self.checker_thread.worker.inject_visibility_changed.connect(
            self.update_inject_visibility, Qt.QueuedConnection
        )

    def closeEvent(self, event):
        logger.info("MainWindow : closeEvent triggered")
        self.checker_thread.worker.running = False
        self.checker_thread.quit()
        self.checker_thread.wait()
        logger.info("MainWindow : Checker thread stopped")
        super().closeEvent(event)
        logger.info("MainWindow : super().closeEvent called")

    def update_inject_visibility(self, visible: bool):
        try:
            logger.info(f"MainWindow : update_inject_visibility called with visible={visible}")
            btn = getattr(self.ui, "inject_dll_button", None)
            if btn is not None and hasattr(btn, "isVisible") and hasattr(btn, "show") and hasattr(btn, "hide"):
                if visible and not btn.isVisible():
                    btn.show()
                    logger.info("MainWindow : inject_dll_button shown")
                elif not visible and btn.isVisible():
                    btn.hide()
                    logger.info("MainWindow : inject_dll_button hidden")
            else:
                logger.warning("MainWindow : inject_dll_button is not a valid widget")
        except Exception as e:
            logger.error(f"Exception in update_inject_visibility: {e}", exc_info=True)

    def open_file_dialog(self):
        logger.info("MainWindow : open_file_dialog called")
        file_path, _ = QFileDialog.getOpenFileName(self, "Select a File", "", "DLL Files (*.dll);")
        if file_path:
            file_name = os.path.basename(file_path)
            self.ui.select_dll_button.setText(f"{file_name}")
            self.dll_path = file_path
            logger.info(f"MainWindow : DLL selected: {file_path}")
        else:
            self.ui.select_dll_button.setText("Select")
            logger.info("MainWindow : No DLL selected")

    def inject_dll(self):
        logger.info("MainWindow : inject_dll called")
        if self.dll_path is None:
            self.ui.inject_status_label.setText("No DLL selected")
            logger.warning("MainWindow : inject_dll called with no DLL selected")
            return
        try:
            process = pm.open_process(f"{EXE_NAME}")
            logger.info(f"MainWindow : Opened process {EXE_NAME}")
        except Exception as e:
            logger.error(f"MainWindow : Unable to find target process: {e}")
            self.ui.inject_status_label.setText("Unable to find target process")
            return
        try:
            success = pm.inject_library(process, self.dll_path)
            logger.info(f"MainWindow : Injected {self.dll_path} - Success: {success}")
        except Exception as e:
            logger.error(f"MainWindow : Injection failed: {e}")
            success = False
        self.ui.select_dll_button.setText("Select")
        self.dll_path = None
        self.ui.inject_status_label.setText("Success, Jeff will now close!" if success else "Failed")
        if success:
            self.checker_thread.worker.running = False
            self.checker_thread.quit()
            self.checker_thread.wait()
            logger.info("MainWindow : Injection successful, closing in 5 seconds")
            time.sleep(5)
            QCoreApplication.quit()

    def get_install_path(self):
        if self._install_path_cache is not None:
            return self._install_path_cache
        logger.info("MainWindow : get_install_path called")
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
            common_path = os.path.join(lib, "common")
            if os.path.exists(common_path):
                for entry in os.listdir(common_path):
                    if entry.lower() == "marvelrivals":
                        install_path = os.path.join(common_path, entry)
                        logger.info(f"MainWindow : Found MarvelRivals at {install_path}")
                        self._install_path_cache = install_path
                        return install_path
        logger.warning("MainWindow : MarvelRivals not found in any Steam library")
        return None

    def find_unwantedfiles(self, install_path):
        now = time.time()
        if self._unwantedfiles_cache and (now - self._unwantedfiles_cache_time < 5):
            return self._unwantedfiles_cache
        logger.info(f"MainWindow : find_unwantedfiles called for {install_path}")
        results = []
        for root, _, filenames in os.walk(install_path):
            for filename in filenames:
                if filename in UNWANTEDFILES_TO_FIND:
                    found_path = os.path.join(root, filename)
                    results.append(found_path)
                    logger.info(f"MainWindow : Found {filename} at {found_path}")
        logger.info(f"MainWindow : Total unwanted files found: {len(results)}")
        self._unwantedfiles_cache = results
        self._unwantedfiles_cache_time = now
        return results

    def count_unwantedfiles(self):
        logger.info("MainWindow : count_unwantedfiles called")
        install_path = self.get_install_path()
        if install_path is None:
            logger.warning("MainWindow : count_unwantedfiles - install path not found")
            return 0
        found_paths = self.find_unwantedfiles(install_path)
        logger.info(f"MainWindow : count_unwantedfiles - {len(found_paths)} unwanted File(s) found")
        return len(found_paths)

    def remove_unwantedfiles(self):
        logger.info("MainWindow : remove_unwantedfiles called")
        install_path = self.get_install_path()
        if install_path is None:
            logger.warning("MainWindow : remove_unwantedfiles - install path not found")
            return
        for path in self.find_unwantedfiles(install_path):
            try:
                os.remove(path)
                logger.info(f"MainWindow : Removed {path}")
            except Exception as e:
                logger.error(f"MainWindow : Failed to remove {path} - {e}")
        self._unwantedfiles_cache = None
        self.count_unwantedfiles()

class GameCheckerWorker(QObject):
    inject_visibility_changed = Signal(bool)
    status_updated = Signal(str)

    def __init__(self, unwantedfiles_counter, parent=None):
        logger.info("GameCheckerWorker : __init__ called")
        super().__init__(parent)
        self.unwantedfiles_counter = unwantedfiles_counter
        self.running = True
        self.initializing = True
        self.game_start_time = None
        self.jeff_satisfied = False
        self.next_check_time = None
        self.ultTime = 10

    def stop(self):
        logger.info("GameCheckerWorker : stop called")
        self.running = False

    def run(self):
        logger.info("GameCheckerWorker : run loop started")
        while self.running:
            logger.info(f"GameCheckerWorker : run loop tick, jeff_satisfied={self.jeff_satisfied}")
            if self.jeff_satisfied is True:
                self.inject_visibility_changed.emit(True)
                logger.info("GameCheckerWorker : inject_visibility_changed(True) emitted")
            if self.jeff_satisfied is False:
                self.inject_visibility_changed.emit(False)
                logger.info("GameCheckerWorker : inject_visibility_changed(False) emitted")
            game_status = "❌"
            unwantedfiles_count = "??"
            ult_status = "??"
            current_time = time.time()
            self.next_check_time = current_time
            unwantedfiles_count = self.unwantedfiles_counter.count_unwantedfiles()
            logger.info(f"GameCheckerWorker : Unwanted Files count is {unwantedfiles_count}")
            result = subprocess.run(
                ["tasklist", "/FI", f"IMAGENAME eq {EXE_NAME}"],
                capture_output=True,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            if 0 != unwantedfiles_count and f"{EXE_NAME}" in result.stdout:
                logger.warning("GameCheckerWorker : Unwanted Filess found while game running, closing game")
                self.show_unwantedfiles_message()
                subprocess.run(["taskkill", "/F", "/IM", f"{EXE_NAME}"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                sys.exit(0)
            try:
                process = pm.open_process(f"{EXE_NAME}")
                if process is not None:
                    game_status = "✅"
                    logger.info("GameCheckerWorker : Game process found")
                    if self.game_start_time is None:
                        self.game_start_time = current_time
                        logger.info("GameCheckerWorker : game_start_time set")
                    elapsed = current_time - self.game_start_time
                    if elapsed >= self.ultTime:
                        try:
                            self.jeff_satisfied = True
                            logger.info("GameCheckerWorker : ultTime reached, jeff_satisfied set True")
                        except Exception as e:
                            logger.error(f"GameCheckerWorker : Exception in ultTime logic: {e}")
                            if self.initializing:
                                logger.info("GameCheckerWorker : initializing self")
                            else:
                                self.game_start_time = current_time
                    else:
                        percent = min(int((elapsed / self.ultTime) * 100), 100)
                        ult_status = f"Charging Ult! ({percent}%)"
                        logger.info(f"GameCheckerWorker : ult_status updated: {ult_status}")
                else:
                    self.game_start_time = None
                    self.next_check_time = None
                    logger.info("GameCheckerWorker : Game process not found, timers reset")
            except Exception as e:
                if "not found" in str(e).lower() or "no such process" in str(e).lower():
                    logger.info(f"GameCheckerWorker : Process not found: {e}")
                else:
                    logger.error(f"GameCheckerWorker : Exception in process check: {e}")
                if self.initializing:
                    game_status = "??"
            self.status_updated.emit(
                f"Status\n{{Game: {game_status}}}\n{{Ult: {ult_status}}}\n{{Unwanted Files: {unwantedfiles_count}}}"
            )
            logger.info("GameCheckerWorker : status_updated emitted")
            self.initializing = False
            for _ in range(20):
                if not self.running:
                    logger.info("GameCheckerWorker : run loop break requested")
                    break
                QThread.msleep(100)
        logger.info("GameCheckerWorker : run loop exited")

class GameCheckerThread(QThread):

    def __init__(self, ui_label, unwantedfiles_counter):
        logger.info("GameCheckerThread : __init__ called")
        super().__init__()
        self.worker = GameCheckerWorker(unwantedfiles_counter)
        self.worker.status_updated.connect(ui_label.setText, Qt.QueuedConnection)
        logger.info("GameCheckerThread : Worker created and status_updated connected")

    def run(self):
        logger.info("GameCheckerThread : run called")
        self.worker.run()
        logger.info("GameCheckerThread : run finished")

    def stop(self):
        logger.info("GameCheckerThread : stop called")
        self.worker.stop()

if __name__ == "__main__":
    logger.info("__main__ : Application starting")
    try:
        app = QApplication(sys.argv)
        window = MainWindow()
        logger.info("__main__ : MainWindow created")
        window.show()
        logger.info("__main__ : MainWindow shown")
        window.checker_thread.start()
        logger.info("MainWindow : GameCheckerThread started (after show)")
        window.remove_unwantedfiles()
        logger.info("__main__ : remove_unwantedfiles called on startup")
        ret = app.exec()
        logger.info(f"__main__ : app.exec() returned {ret}")
        sys.exit(ret)
    except Exception as e:
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        log_filename = f"jeff-crash{timestamp}.log"
        tb_str = traceback.format_exc()
        with open(log_filename, "w", encoding="utf-8") as f:
            f.write(tb_str)
        logger.error(f"__main__ : Unhandled exception: {e}\nTraceback:\n{tb_str}")
        error_message = f"An unexpected error occurred:\n{e}\n\nSee {log_filename} for details."
        if QApplication.instance() is None:
            app = QApplication(sys.argv)
        QMessageBox.critical(None, "Jeff Injector Crash", error_message)
        sys.exit(1)
