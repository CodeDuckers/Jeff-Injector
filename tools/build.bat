cd ..
pip install -r requirements.txt
pyinstaller --onefile --icon=resources/JEFF.ico --name "JeffInjector" --windowed main.py
start dist