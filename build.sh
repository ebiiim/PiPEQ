#!/bin/sh
cd "$(dirname "$0")" || exit

pyinstaller --onefile pipeq.py
pyinstaller --onefile recorder.py
pyinstaller --onefile get_devices.py
pyinstaller --onefile plot_eq.py --hidden-import='PIL._tkinter_finder'
mv dist/recorder dist/pipeq-recorder
mv dist/get_devices dist/pipeq-get-devices
mv dist/plot_eq dist/pipeq-show-eq
cp plot_combined.pl dist/pipeq-plot-eq
cp install.sh dist/install.sh
cp config.txt dist/config.txt
