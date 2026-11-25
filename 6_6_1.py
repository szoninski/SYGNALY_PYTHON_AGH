import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

Fs = 4000
fc = 1000

plt.figure()

for M in [11, 51, 101]:
    h = signal.firwin(M, fc, window='boxcar', fs=Fs)
    f, H = signal.freqz(h, worN=8192, fs=Fs)

    plt.plot(f, 20*np.log10(np.abs(H) + 1e-12),
             label=f'M = {M}')

plt.title('Okno prostokatne - rozne dlugosci')
plt.xlabel('Czestotliwosc [Hz]')
plt.ylabel('Amplituda [dB]')
plt.grid()
plt.legend()
plt.show()