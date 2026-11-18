
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# Parametry zadania
Fs = 200       # Czestotliwosc probkowania [Hz]
f0 = 50        # Czestotliwosc do wyciecia [Hz]

r1 = 1.0       # Promien zer
r2 = 0.95      # Promien biegunow
omega = 2 * np.pi * f0 / Fs

# Wspolczynniki transmitancji H(z)
b = [1, -2*r1*np.cos(omega), r1**2]
a = [1, -2*r2*np.cos(omega), r2**2]

print("Parametry filtru:")
print("r1 =", r1)
print("r2 =", r2)
print("omega =", omega)
print("Licznik b =", b)
print("Mianownik a =", a)

# Odpowiedz impulsowa
N = 150
impulse = np.zeros(N)
impulse[0] = 1

h = signal.lfilter(b, a, impulse)
t = np.arange(N) / Fs

# Charakterystyka czestotliwosciowa
f, H = signal.freqz(b, a, worN=8192, fs=Fs)
magnitude = 20 * np.log10(np.maximum(np.abs(H), 1e-12))

# Wykresy
plt.figure(figsize=(12, 8))

# Odpowiedz impulsowa
plt.subplot(2, 1, 1)
plt.stem(t, h, basefmt=" ")
plt.title("Odpowiedz impulsowa filtru Notch")
plt.xlabel("Czas [s]")
plt.ylabel("Amplituda")
plt.grid(True)

# Charakterystyka amplitudowa
plt.subplot(2, 1, 2)
plt.plot(f, magnitude)
plt.axvline(f0, color='red', linestyle='--',
            label='50 Hz')
plt.title("Charakterystyka amplitudowa filtru Notch")
plt.xlabel("Czestotliwosc [Hz]")
plt.ylabel("Amplituda [dB]")
plt.ylim(-100, 5)
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()
