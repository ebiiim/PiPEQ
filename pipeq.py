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


def build_command(input_device, rates, bits, input_buffer, sox_effects):
    err2null = '2>/dev/null'
    rec = ['pipeq-recorder', str(input_device), str(rates[0]), str(bits[0]), str(input_buffer), err2null]
    sox = ['sox', '-t raw -b', str(bits[0]), '-e signed -c 2 -r', str(rates[0]), '-',
           '-t raw -b', str(bits[1]), '-e signed -c 2 -r', str(rates[1]), '-'] + sox_effects + [err2null]
    cmd = rec + ['|'] + sox
    return ' '.join(cmd)


if __name__ == '__main__':
    import sys
    show_devices()
    in_dev, out_dev = _select_device()
    in_sr = 48000
    out_sr = 48000
    in_bit = 16
    out_bit = 16
    in_bs = 512
    out_bs = 512
    ses = ['gain', '-3']
    if len(sys.argv) == 2:
        ses += build_eq(parse_roomeq(sys.argv[1]))
    command = build_command(in_dev, [in_sr, out_sr], [in_bit, out_bit], in_bs, ses)
    play_stdin(command, out_sr, out_bit, out_bs, out_dev)
