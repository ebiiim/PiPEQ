import sys
import subprocess
import time
import toml
from player import play_stdin
from filter_loader import build_eq_by_type, format_eq_plot
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


def show_eq(eq_list, is_debug):
    eq_dummy = '"equalizer 24000 1q 0.1"'
    eq_l = format_eq_plot(eq_list[0]) if eq_list[0] != [] else eq_dummy
    eq_r = format_eq_plot(eq_list[0]) if eq_list[1] != [] else eq_dummy
    # BSD compatibility (BSD mktemp do not have `--suffix`)
    cmd = "UUID_L=$(uuidgen);UUID_R=$(uuidgen);" \
          "PLOT_L=/tmp/$UUID_L.png;PLOT_R=/tmp/$UUID_R.png;touch $PLOT_L $PLOT_R;" \
          "trap 'rm -f $PLOT_L $PLOT_R' EXIT;" \
          "pipeq-plot-eq 48000 " + eq_l + " | gnuplot > $PLOT_L;" \
          "pipeq-plot-eq 48000 " + eq_r + " | gnuplot > $PLOT_R;" \
          "pipeq-show-eq $PLOT_L $PLOT_R"
    if is_debug:
        print(cmd)
    subprocess.Popen(cmd, shell=True)


def run():
    # default
    default_filter = ['gain', '-3']
    buf_in = 512
    buf_out = 512
    eq_l = []
    eq_r = []
    conf = {'global': {'buffer_bytes': 1024, 'debug': False, 'wait_for_plot': 5},
            'input': {'device_id': -1, 'rate': 48000, 'bit': 16},
            'output': {'device_id': -1, 'rate': 48000, 'bit': 16},
            'eq': {'left': {'type': '', 'path': ''},
                   'right': {'type': '', 'path': ''}}
            }

    if len(sys.argv) == 1:  # no config
        get_devices()
        conf['input']['device_id'], conf['output']['device_id'] = _select_device()

    if len(sys.argv) == 2:  # load config
        conf = toml.load(sys.argv[1])
        buf_in = int(conf['global']['buffer_bytes']/(conf['input']['bit']/8))  # frames_per_buffer
        buf_out = int(conf['global']['buffer_bytes']/(conf['output']['bit']/8))  # frames_per_buffer
        eq_l = build_eq_by_type(conf['eq']['left']['type'], conf['eq']['left']['path'])
        eq_r = build_eq_by_type(conf['eq']['right']['type'], conf['eq']['right']['path'])

    cmd = build_command(conf['input']['device_id'],
                        [conf['input']['rate'], conf['output']['rate']],
                        [conf['input']['bit'], conf['output']['bit']],
                        [buf_in, conf['global']['buffer_bytes']], [default_filter+eq_l, default_filter+eq_r])

    if conf['global']['debug']:
        print(conf)
        print('buf_in, bun_out: ', buf_in, ', ', buf_out)
        print(cmd)

    show_eq([eq_l, eq_r], conf['global']['debug'])
    time.sleep(conf['global']['wait_for_plot'])

    start = time.time()
    play_stdin(cmd, conf['output']['rate'], conf['output']['bit'], buf_out, conf['output']['device_id'])
    stop = time.time() - start
    print("{:.2f}s".format(stop))


if __name__ == '__main__':
    run()
