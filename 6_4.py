# New Python file

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# Wlasna funkcja obliczajaca charakterystyke czestotliwosciowa
def freqz_lab(B, A, w):
    H = np.zeros(len(w), dtype=complex)

    for i in range(len(w)):
        z = np.exp(1j * w[i])

        licznik = 0
        mianownik = 0

        for k in range(len(B)):
            licznik += B[k] * z**(-k)

        for k in range(len(A)):
            mianownik += A[k] * z**(-k)

        H[i] = licznik / mianownik

    return H


# Parametry filtru z zadania 6.3
Fs = 200
f0 = 50

r1 = 1.0
r2 = 0.95
omega = 2 * np.pi * f0 / Fs

# Wspolczynniki transmitancji
B = [1, -2*r1*np.cos(omega), r1**2]
A = [1, -2*r2*np.cos(omega), r2**2]

# Wektor czestotliwosci
w = np.linspace(0, np.pi, 1000)

# Obliczenie charakterystyki wlasna funkcja
H_lab = freqz_lab(B, A, w)

# Obliczenie charakterystyki funkcja scipy.signal.freqz
w_scipy, H_scipy = signal.freqz(B, A, worN=w)

# Charakterystyki amplitudowe w dB
mag_lab = 20 * np.log10(np.maximum(np.abs(H_lab), 1e-12))
mag_scipy = 20 * np.log10(np.maximum(np.abs(H_scipy), 1e-12))

# Charakterystyki fazowe
phase_lab = np.unwrap(np.angle(H_lab))
phase_scipy = np.unwrap(np.angle(H_scipy))

# Porownanie wynikow
error = np.max(np.abs(H_lab - H_scipy))
print("Maksymalna roznica:", error)

# Wykresy
plt.figure(figsize=(12, 10))

# Charakterystyka amplitudowa
plt.subplot(3, 1, 1)
plt.plot(w, mag_lab, label="freqz_lab", linewidth=2)
plt.plot(w_scipy, mag_scipy, "--", label="scipy.signal.freqz")
plt.title("Charakterystyka amplitudowa")
plt.xlabel("Czestotliwosc [rad/probke]")
plt.ylabel("Amplituda [dB]")
plt.ylim(-100, 5)
plt.grid(True)
plt.legend()

# Charakterystyka fazowa
plt.subplot(3, 1, 2)
plt.plot(w, phase_lab, label="freqz_lab")
plt.plot(w_scipy, phase_scipy, "--", label="scipy.signal.freqz")
plt.title("Charakterystyka fazowa")
plt.xlabel("Czestotliwosc [rad/probke]")
plt.ylabel("Faza [rad]")
plt.grid(True)
plt.legend()

# Roznica pomiedzy wynikami
plt.subplot(3, 1, 3)
plt.plot(w, np.abs(H_lab - H_scipy))
plt.title("Roznica pomiedzy funkcjami")
plt.xlabel("Czestotliwosc [rad/probke]")
plt.ylabel("Blad bezwzgledny")
plt.grid(True)

plt.tight_layout()
plt.show()
