import pyaudio


def get_devices():
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
