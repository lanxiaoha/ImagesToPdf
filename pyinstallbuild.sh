source ./bin/activate

pyinstaller --noconfirm \
-n ImageToPDF \
-i /Users/meitu/Documents/project/python/ImagesToPdf/logo.png \
--clean \
--windowed \
--specpath=./pyinstallbuild \
--onefile \
--noconsole \
src/main.py