
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
M = 51

h1 = signal.firwin(M, fc, window='boxcar', fs=Fs)
h2 = signal.firwin(M, fc, window='hamming', fs=Fs)

f, H1 = signal.freqz(h1, worN=8192, fs=Fs)
f, H2 = signal.freqz(h2, worN=8192, fs=Fs)

plt.figure()
plt.plot(f, 20*np.log10(np.abs(H1) + 1e-12),
         label='Prostokatne')
plt.plot(f, 20*np.log10(np.abs(H2) + 1e-12),
         label='Hamming')

plt.title('Porownanie okien M = 51')
plt.xlabel('Czestotliwosc [Hz]')
plt.ylabel('Amplituda [dB]')
plt.grid()
plt.legend()
plt.show()



plt.title('Okno prostokatne - rozne dlugosci')
plt.xlabel('Czestotliwosc [Hz]')
plt.ylabel('Amplituda [dB]')
plt.grid()
plt.legend()
plt.show()# New Python file
