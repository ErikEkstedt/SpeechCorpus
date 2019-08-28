import buckeye

from os.path import join
import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import read, write

from speechcorpus.utils import read_wav
import sounddevice as sd

sd.default.samplerate = 16000

ROOT = "data/Buckeye"
speaker = buckeye.Speaker.from_zip(join(ROOT, "s01.zip"), load_wavs=True)

audio = []
for track in speaker:
    print(track.name)
    track = speaker[0]
    frames = track.wav.getnframes()
    y = np.frombuffer(track.wav.readframes(frames), dtype=np.int16)
    audio.append((y, track.name))
plt.plot(audio[0][0][:256000])
plt.show()


y, sr = read_wav("data/Buckeye/s01/s0101a.wav")

start = 10
end = 70
plt.plot(y[start * sr : end * sr])
plt.show()

sd.play(y)
