# PiPEQ - A Parametric Equalizer on Raspberry Pi

[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/ebiiim/PiPEQ/blob/master/LICENSE)
[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2Febiiim%2FPiPEQ.svg?type=shield)](https://app.fossa.io/projects/git%2Bgithub.com%2Febiiim%2FPiPEQ?ref=badge_shield)

## Usage

Install

```bash
curl -L -O https://github.com/ebiiim/PiPEQ/releases/download/v0.2.0/PiPEQ-v0.2.0-linux-armv7l.tar.gz
tar -zxvf PiPEQ-v0.2.0-linux-armv7l.tar.gz
cd PiPEQ
./install.sh
```

Setting

```bash
pipeq-get-devices # get the device id
vi config.txt # edit the config file
```

Run

```bash
pipeq config.txt
```

Config.txt

```toml
[global]
buffer_bytes = 4096
debug = true

[input]
device_id = -1  # -1: default device
rate = 48000
bit = 16

[output]
device_id = -1  # -1: default device
rate = 48000
bit = 16

[eq]
left.type = "roomeq"  # "roomeq": the Room EQ Wizard's format
left.path = "left.txt"  # EQ config file for the left channel
right.type = "roomeq"
right.path = "right.txt"

[curve]
plot = true  # display EQ curves
rotate = 0  # rotate EQ curves by [0, 90, 180, 270] degrees
wait_for_plot = 5

```

Uninstall

```bash
rm -rf /path/to/PiPEQ
sudo rm /usr/loca/bin/pipeq*
```

## Development

Install Dependencies

```bash
sudo apt update
sudo apt upgrade
sudo apt install git python3-pip python3-venv python3-dev python3-tk
sudo apt install portaudio19-dev uuid-runtime
sudo apt install sox gnuplot
```

Install PyInstaller on Raspberry Pi

```bash
git clone https://github.com/pyinstaller/pyinstaller.git
cd pyinstaller
git checkout v3.4
cd bootloader
python ./waf all
cd ..
pip3 install .
```

Build PiPEQ

```bash
git clone https://github.com/ebiiim/PiPEQ.git && cd PiPEQ
pip3 install -r requirements.txt
./build.sh
cd dist
```

## License

MIT

The following applications are called at runtime:

- [SoX](http://sox.sourceforge.net/)
- [gnuplot](http://www.gnuplot.info/)


[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2Febiiim%2FPiPEQ.svg?type=large)](https://app.fossa.io/projects/git%2Bgithub.com%2Febiiim%2FPiPEQ?ref=badge_large)

## Changelog

### 0.2.0 / 2018-11-10

NEW

- EQ curves view

### 0.1.0 / 2018-11-06

Initial release.