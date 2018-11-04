import pyaudio
from player import play_stdin
from filter_loader import build_eq, parse_roomeq


def show_devices():
    def _show_device_info(device):
        print(' '*2 + device['name'])
        print(' '*4 + 'device_index:', device['index'])
        in_ch = device['maxInputChannels']
        None if in_ch == 0 else print(' '*4 + 'input_channels:', in_ch)
        out_ch = device['maxOutputChannels']
        None if out_ch == 0 else print(' '*4 + 'output_channels:', out_ch)
        sr = device['defaultSampleRate']
        print(' '*4 + 'default_sample_rate:', sr)

    def _show_devices_by_host_api_type(pa_type):
        info = pa.get_host_api_info_by_type(pa_type)
        device_count = info.get('deviceCount')
        if device_count > 0:
            print(info['name'], 'devices')
            for i in range(0, device_count):
                _show_device_info(pa.get_device_info_by_host_api_device_index(info.get('index'), i))

    pa = pyaudio.PyAudio()
    for i in range(0, pa.get_host_api_count()):
        _show_devices_by_host_api_type(pa.get_host_api_info_by_index(i)['type'])


def _select_device():
    input_device = input('input device:')
    if not input_device.isdecimal():
        input_device = '-1'
    output_device = input('output device:')
    if not output_device.isdecimal():
        output_device = '-1'
    return input_device, output_device


def build_command(input_device, rates, bits, buffers, sox_effects):
    """
    :param input_device: device index e.g. 2
    :param rates: [input, internal, output] e.g. [48000, 96000, 48000]
    :param bits: [input, internal, output] e.g. [16, 32, 16]
    :param buffers: [input, eq, mix] e.g. [512, 512, 2048]
    :param sox_effects: [left, right] e.g. [['equalizer', '80', '5q', '-6'], ['equalizer', '10000', '2q', '3']]
    :return str: command
    """

    rec = ['pipeq-recorder', str(input_device), str(rates[0]), str(bits[0]), str(buffers[0])]
    # rec = ['cat', 'test.pcm']

    tmp = "L1=$(mktemp -u);R1=$(mktemp -u);L2=$(mktemp -u);R2=$(mktemp -u);" \
          "mkfifo $L1 $L2 $R1 $R2;" \
          "trap 'rm -f $L1 $L2 $R1 $R2' EXIT;"
    s2l = "sh -c " \
          "'sox --buffer "+str(buffers[1])+"" \
          " -t raw -b "+str(bits[0])+" -e signed -c 2 -r "+str(rates[0])+" $0" \
          " -t raw -b "+str(bits[1])+" -e signed -c 1 -r "+str(rates[1])+" $1" \
          " remix 1 "+' '.join(sox_effects[0])+"'" \
          " $L1 $L2"
    s2r = "sh -c " \
          "'sox --buffer "+str(buffers[1])+"" \
          " -t raw -b "+str(bits[0])+" -e signed -c 2 -r "+str(rates[0])+" $0" \
          " -t raw -b "+str(bits[1])+" -e signed -c 1 -r "+str(rates[1])+" $1" \
          " remix 2 "+' '.join(sox_effects[1])+"'" \
          " $R1 $R2"
    rec = "sh -c '"+' '.join(rec)+" | tee $0 > $1' $L1 $R1"
    mix = "sox --buffer "+str(buffers[2])+" -M" \
          " -t raw -b "+str(bits[1])+" -e signed -c 1 -r "+str(rates[1])+" $L2" \
          " -t raw -b "+str(bits[1])+" -e signed -c 1 -r "+str(rates[1])+" $R2" \
          " -t raw -b "+str(bits[2])+" -e signed -c 2 -r "+str(rates[2])+" -"

    return tmp + s2l + ' & ' + s2r + ' & ' + rec + ' & ' + mix


if __name__ == '__main__':
    import sys
    show_devices()
    dev_in, dev_out = _select_device()
    sr_in = 48000
    sr_proc = 192000
    sr_out = 48000
    bit_in = 16
    bit_proc = 32
    bit_out = 16
    buf_in = 256
    buf_eq = 256
    buf_mix = 2048
    buf_out = 256
    eq_l = ['gain', '-3']
    eq_r = ['gain', '-3']
    if len(sys.argv) == 3:
        eq_l += build_eq(parse_roomeq(sys.argv[1]))
        eq_r += build_eq(parse_roomeq(sys.argv[2]))
    cmd = build_command(dev_in, [sr_in, sr_proc, sr_out], [bit_in, bit_proc, bit_out], [buf_in, buf_eq, buf_mix], [eq_l, eq_r])
    print(cmd)
    play_stdin(cmd, sr_out, bit_out, buf_out, dev_out)
