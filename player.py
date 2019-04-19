import subprocess
import pyaudio


def _fetch_stdin(command, buffer_size):
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while True:
        buffer = p.stdout.read(buffer_size)
        if buffer:
            yield buffer
        if not buffer and p.poll() is not None:
            break


def play_stdin(command, sample_rate, sample_bit, buffer_size, output_device):
    dev = None if output_device == '-1' else int(output_device)
    bit_fmt = pyaudio.paInt16
    if sample_bit == 24:
        bit_fmt = pyaudio.paInt24
    if sample_bit == 32:
        bit_fmt = pyaudio.paInt32

    pa = pyaudio.PyAudio()
    stream = pa.open(format=bit_fmt,
                     channels=2,
                     rate=sample_rate,
                     frames_per_buffer=buffer_size,
                     input=False,
                     output=True,
                     output_device_index=dev,
                     )
    stream.start_stream()
    c = 0
    c_max = int(0.1 * (sample_rate/buffer_size))
    for buffer in _fetch_stdin(command, buffer_size):
        if c > c_max:  # wait 0.1s to avoid noise in Raspi
            stream.write(buffer)
        else:
            c += 1
    stream.stop_stream()
    stream.close()
    pa.terminate()
