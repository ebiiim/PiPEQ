#!/bin/sh
cd "$(dirname "$0")" || exit

pyinstaller --onefile pipeq.py
pyinstaller --onefile recorder.py
pyinstaller --onefile get_devices.py
mv dist/recorder dist/pipeq-recorder
mv dist/get_devices dist/pipeq-get-devices

cp install.sh dist/install.sh
cp config.txt dist/config.txt
