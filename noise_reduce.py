import noisereduce as nr
import numpy as np
import scipy.io.wavfile
import wave
import matplotlib.pyplot as plt
import numpy as np

rate, data = scipy.io.wavfile.read("test.wav")
#rate, data = wavfile.read("mywav.wav")

print(min(data),max(data))
noisy_part = data[0:2000]
data=data/1.0
#data = np.float32(data)
#data = float(data[0:1000])
#print(data)
#data=wave.open('test.wav','rb') 
#data = float(data)
#print(data)
#reduced_noise = nr.reduce_noise(audio_clip=data, noise_clip=noisy_part, verbose=True)
length = data.shape[0] / rate
time = np.linspace(0., length, data.shape[0])
plt.plot(time, data[:], label="Left channel")
plt.show()
