import pyaudio


def write_input_to_stdout(input_device_index, sample_rate, sample_bit, buffer_size):
    pa = pyaudio.PyAudio()
    bit_fmt = pyaudio.paInt16
    if sample_bit == 24:
        bit_fmt = pyaudio.paInt24
    if sample_bit == 32:
        bit_fmt = pyaudio.paInt32
    stream = pa.open(format=bit_fmt,
                     channels=2,
                     rate=sample_rate,
                     frames_per_buffer=buffer_size,
                     input=True,
                     input_device_index=input_device_index,
                     output=False,
                     )
    stream.start_stream()
    while stream.is_active():
        buffer = stream.read(buffer_size)
        if len(buffer) == 0:
            break
        sys.stdout.buffer.write(buffer)
    stream.stop_stream()
    stream.close()
    pa.terminate()


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 5:
        print('Usage: recorder DEVICE_INDEX SAMPLE_RATE SAMPLE_BIT BUFFER_SIZE')
        sys.exit()
    dev = None if sys.argv[1] == '-1' else int(sys.argv[1])
    r = int(sys.argv[2])
    b = int(sys.argv[3])
    bs = int(sys.argv[4])
    write_input_to_stdout(dev, r, b, bs)
