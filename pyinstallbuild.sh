#python3 -m venv ./
#source ./bin/activate
#pip3 install reportlab
#pip3 install Pillow
#pip3 install pyinstaller
#pip3 install PyQt5

pyinstaller --noconfirm \
-n ImageToPDF \
-i /Users/meitu/Documents/project/python/ImagesToPdf/logo.png \
--clean \
--windowed \
--specpath=./pyinstallbuild \
--target-architecture=x86_64 \
--onefile \
--noconsole \
src/main.py

#pyinstaller --noconfirm -n ImageToPDF --clean --windowed --specpath=./pyinstallbuild --onefile --noconsole src/main.py