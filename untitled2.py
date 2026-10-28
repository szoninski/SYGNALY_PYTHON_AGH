# New Python file
import numpy as np
import matplotlib.pyplot as plt

# --- Parametry ---
A = 1.0        # amplituda
f0 = 5.0       # częstotliwość nośnej [Hz]
phi = 0.0      # faza
kAM = 0.7      # współczynnik modulacji AM
fm = 1.0       # częstotliwość modulująca [Hz]

fs = 1000.0                    # częstotliwość próbkowania
T = 1.0                        # sygnały zdefiniowane dla |t| < 1
t = np.arange(-2, 2, 1/fs)     # oś czasu

# --- Definicje sygnałów ---
x1 = np.where(np.abs(t) < T, 1.0, 0.0)                          # (3.6) impuls prostokątny
x2 = np.where(np.abs(t) < T, A*np.cos(2*np.pi*f0*t + phi), 0.0) # (3.7) fragment sinusoidy
x3 = np.where(np.abs(t) < T,                                   # (3.8) fragment z modulacją AM
              (1 + kAM*np.cos(2*np.pi*fm*t))*np.cos(2*np.pi*f0*t + phi),
              0.0)

# --- Widmo Fouriera (FFT + normalizacja do wartości ciągłej) ---
def spectrum(x):
    N = len(x)
    X = np.fft.fftshift(np.fft.fft(x, 8*N)) / fs   # gęste próbkowanie, dzielenie przez fs -> X(f) ciągłe
    f = np.fft.fftshift(np.fft.fftfreq(8*N, 1/fs))
    return f, X

freq1, X1 = spectrum(x1)
freq2, X2 = spectrum(x2)
freq3, X3 = spectrum(x3)

# --- Wykresy ---
signals = [(x1, freq1, X1, 'x1(t) – impuls prostokątny'),
          (x2, freq2, X2, 'x2(t) – fragment sinusoidy'),
          (x3, freq3, X3, 'x3(t) – sinusoida z modulacją AM')]

fig, axes = plt.subplots(3, 2, figsize=(12, 9))
for i, (x, f, X, title) in enumerate(signals):
    axes[i, 0].plot(t, x, 'b')
    axes[i, 0].set_title(f'{title} – przebieg czasowy')
    axes[i, 0].set_xlabel('t [s]')
    axes[i, 0].set_ylabel('x(t)')
    axes[i, 0].grid(True)

    axes[i, 1].plot(f, np.abs(X), 'r')
    axes[i, 1].set_title(f'{title} – widmo amplitudowe |X(f)|')
    axes[i, 1].set_xlabel('f [Hz]')
    axes[i, 1].set_ylabel('|X(f)|')
    axes[i, 1].set_xlim(-15, 15)
    axes[i, 1].grid(True)

plt.tight_layout()
plt.show()