# PiPEQ - A Parametric Equalizer on Raspberry Pi

[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/ebiiim/PiPEQ/blob/master/LICENSE)

## Usage

Install

```bash
curl -L -O https://github.com/ebiiim/PiPEQ/releases/download/v0.1.0/PiPEQ-v0.1.0-linux-armv7l.tar.gz
tar -zxvf PiPEQ-v0.1.0-linux-armv7l.tar.gz
cd PiPEQ
./install.sh
```

Setting

```bash
pipeq-get-devices # get the device id
vi config.txt # edit the config file
```

Run

```
pipeq config.txt
```

Config.txt

```toml
[global]
buffer_bytes = 1024  # 512 to 1024 for Raspi 3 B+
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
right.path = "right.txt"  # EQ config file for the right channel
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
sudo apt install git python3-venv python3-dev
sudo apt install sox gnuplot
sudo apt install portaudio19-dev
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

## Changelog

### 0.1.0 / 2018-11-06

Initial release.
