from player import play_stdin
from filter_loader import build_eq_by_type
from get_devices import get_devices


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
    :param rates: [input, output] e.g. [48000, 48000]
    :param bits: [input, output] e.g. [16, 16]
    :param buffers: [input, sox] e.g. [512, 1024]
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
          " -t raw -b "+str(bits[0])+" -e signed -c 1 -r "+str(rates[0])+" $1" \
          " remix 1 "+' '.join(sox_effects[0])+"'" \
          " $L1 $L2"
    s2r = "sh -c " \
          "'sox --buffer "+str(buffers[1])+"" \
          " -t raw -b "+str(bits[0])+" -e signed -c 2 -r "+str(rates[0])+" $0" \
          " -t raw -b "+str(bits[0])+" -e signed -c 1 -r "+str(rates[0])+" $1" \
          " remix 2 "+' '.join(sox_effects[1])+"'" \
          " $R1 $R2"
    rec = "sh -c '"+' '.join(rec)+" | tee $0 > $1' $L1 $R1"
    mix = "sox --buffer "+str(buffers[1])+" -M" \
          " -t raw -b "+str(bits[0])+" -e signed -c 1 -r "+str(rates[0])+" $L2" \
          " -t raw -b "+str(bits[0])+" -e signed -c 1 -r "+str(rates[0])+" $R2" \
          " -t raw -b "+str(bits[1])+" -e signed -c 2 -r "+str(rates[1])+" -"

    return tmp + s2l + ' & ' + s2r + ' & ' + rec + ' & ' + mix


if __name__ == '__main__':
    import sys
    import toml

    buf_in = 512
    buf_out = 512
    eq_l = ['gain', '-3']
    eq_r = ['gain', '-3']

    conf = {'global': {'buffer_bytes': 1024, 'debug': False},
            'input': {'device_id': -1, 'rate': 48000, 'bit': 16},
            'output': {'device_id': -1, 'rate': 48000, 'bit': 16},
            'eq': {'left': {'type': '', 'path': ''},
                   'right': {'type': '', 'path': ''}}
            }

    if len(sys.argv) == 1:  # no config
        get_devices()
        conf['input']['device_id'], conf['output']['device_id'] = _select_device()

    if len(sys.argv) == 2:
        conf = toml.load(sys.argv[1])
        eq_l += build_eq_by_type(conf['eq']['left']['type'], conf['eq']['left']['path'])
        eq_r += build_eq_by_type(conf['eq']['right']['type'], conf['eq']['right']['path'])

    cmd = build_command(conf['input']['device_id'],
                        [conf['input']['rate'], conf['output']['rate']],
                        [conf['input']['bit'], conf['output']['bit']],
                        [buf_in, conf['global']['buffer_bytes']], [eq_l, eq_r])

    if conf['global']['debug']:
        print(conf)
        print(cmd)

    play_stdin(cmd, conf['output']['rate'], conf['output']['bit'], buf_out, conf['output']['device_id'])
