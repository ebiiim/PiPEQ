#!/bin/sh
cd "$(dirname "$0")" || exit

sudo apt install -y sox gnuplot

sudo rm -f /usr/local/bin/pipeq-recorder
sudo rm -f /usr/local/bin/pipeq
sudo ln -s "$(pwd)"/pipeq-recorder /usr/local/bin
sudo ln -s "$(pwd)"/pipeq /usr/local/bin
