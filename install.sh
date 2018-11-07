#!/bin/sh
cd "$(dirname "$0")" || exit

sudo apt install -y sox gnuplot

sudo rm -f /usr/local/bin/pipeq
sudo rm -f /usr/local/bin/pipeq-recorder
sudo rm -f /usr/local/bin/pipeq-get-devices
sudo rm -f /usr/local/bin/pipeq-show-eq
sudo rm -f /usr/local/bin/pipeq-plot-eq
sudo ln -s "$(pwd)"/pipeq /usr/local/bin
sudo ln -s "$(pwd)"/pipeq-recorder /usr/local/bin
sudo ln -s "$(pwd)"/pipeq-get-devices /usr/local/bin
sudo ln -s "$(pwd)"/pipeq-show-eq /usr/local/bin
sudo ln -s "$(pwd)"/pipeq-plot-eq /usr/local/bin
