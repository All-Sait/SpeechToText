import numpy as np
from flask import Flask, request
from scipy.io.wavfile import write
from scipy.fft import ifft
import whisper

import requests

app = Flask(__name__)

@app.route('/receive_data', methods=['POST'])
def receive_data():
    data = request.json  # Assuming you are sending JSON data
    process_data(data)
    return 'Data received successfully!'
 # API endpoint configuration

def process_data(data):
    data = np.array(data)
    rate = 44100
    max_frequency = 3600
    between = 1/60
    full_waveform = np.array([])
    for freq_vols in data:
        t = np.linspace(0,between,int(rate*between),endpoint=False)
        segment_waveform = np.zeros_like(t)
        for i,volume in enumerate(freq_vols):
            frequency = (i/len(freq_vols)) * max_frequency
            segment_waveform += volume * np.sin(np.pi * frequency * t)
           # segment_waveform = segment_waveform / np.max(np.abs(segment_waveform))
        #segment_waveform = segment_waveform / np.max(np.abs(segment_waveform))
        full_waveform = np.concatenate((full_waveform,segment_waveform))

    full_waveform = full_waveform/np.max(np.abs(full_waveform))
    audio_signal = np.int16(full_waveform*32767)
    write('output.wav',rate,audio_signal)

if __name__ == '__main__':
    app.run(port=5000)