

    
import numpy as np
import pyaudio

volume = 0.5
fs = 48000
duration = 5.0
f = 440.0

data = (np.sin(2* np.pi * np.arange(fs*duration)*f/fs)).astype(np.float32)

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paFloat32, channels=1, rate=fs, output=True)
stream.write(volume * data)

stream.stop_stream()
stream.close()
p.terminate()

class Tone:
    def __init__(self, volume=0.5, rate=48000, channels=1):
        self.volume = volume
        self.rate = rate
        self.channels = channels
        self.p = pyaudio.PyAudio()
        self.stream = p.open(format=pyaudio.paFloat32, channels=self.channels, rate=self.rate, output=True)
        
    def play(self, octave=3, note=1, duration=2):
        f = 2**(octave) * 55 * 2**(((note)-10)/12)
        sample = (np.sin(2* np.pi * np.arange(fs*duration)*f/self.rate)).astype(np.float32)
        self.stream.write(self.volume * sample)
        
    def stop(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        
        
import numpy as np
import pyaudio
import wave
       
Time = 5
data = []
CHUNK = 1024
RATE = 48000

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True, frames_per_buffer=CHUNK)
w = wave.open("./out.wav", "wb")
w.setnchannels(1)
w.setsampwidth(p.get_sample_size(pyaudio.paInt16))
w.setframerate(RATE)
try:
    while True:
        w.writeframes(stream.read(CHUNK))
except KeyboardInterrupt:
    pass

