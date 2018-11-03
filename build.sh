#!/bin/sh
cd "$(dirname "$0")" || exit

pyinstaller --onefile pipeq.py
pyinstaller --onefile recorder.py
mv dist/recorder dist/pipeq-recorder
cp install.sh dist/install.sh
