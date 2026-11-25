import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
# CZESC 3
Fs = 5000
Fpass = 1000
Fstop = 1500
Rp = 1
Rs = 30

# Przeliczenie tolerancji z dB na skale liniowa
delta_p = (10**(Rp / 20) - 1) / (10**(Rp / 20) + 1)
delta_s = 10**(-Rs / 20)

# Szerokosc pasma przejsciowego
width = (Fstop - Fpass) / (Fs / 2)

# Czestotliwosc odciecia
fc = (Fpass + Fstop) / 2

# Funkcja sprawdzajaca parametry filtra
def verify(h):
    f, H = signal.freqz(h, worN=65536, fs=Fs)
    A = np.abs(H)

    passband = A[f <= Fpass]
    stopband = A[f >= Fstop]

    rp = 20 * np.log10(np.max(passband) / np.min(passband))
    rs = -20 * np.log10(np.max(stopband))

    correct = (
        np.min(passband) >= 1 - delta_p
        and np.max(passband) <= 1 + delta_p
        and rs >= Rs
    )

    return rp, rs, correct


# METODA KAISERA
A = -20 * np.log10(min(delta_p, delta_s))

M_kaiser, beta = signal.kaiserord(A, width)

# Zwiekszanie dlugosci az filtr spelni wymagania
while True:
    h_kaiser = signal.firwin(
        M_kaiser,
        fc,
        window=('kaiser', beta),
        fs=Fs
    )

    rp_k, rs_k, correct_k = verify(h_kaiser)

    if correct_k:
        break

    M_kaiser += 1


# ALGORYTM PARKSA-MCCLELLANA
M_pm = 3

while True:
    h_pm = signal.remez(
        M_pm,
        [0, Fpass, Fstop, Fs / 2],
        [1, 0],
        weight=[1 / delta_p, 1 / delta_s],
        fs=Fs
    )

    rp_pm, rs_pm, correct_pm = verify(h_pm)

    if correct_pm:
        break

    M_pm += 1


# Wyswietlenie wynikow
print('--- Filtr Kaisera ---')
print('Dlugosc M:', M_kaiser)
print('Rzad N:', M_kaiser - 1)
print(f'Rp = {rp_k:.3f} dB')
print(f'Rs = {rs_k:.3f} dB')
print('Spelnia wymagania:', correct_k)

print('\n--- Filtr Parksa-McClellana ---')
print('Dlugosc M:', M_pm)
print('Rzad N:', M_pm - 1)
print(f'Rp = {rp_pm:.3f} dB')
print(f'Rs = {rs_pm:.3f} dB')
print('Spelnia wymagania:', correct_pm)


# Charakterystyki amplitudowe
f, H_kaiser = signal.freqz(h_kaiser, worN=8192, fs=Fs)
f, H_pm = signal.freqz(h_pm, worN=8192, fs=Fs)

plt.figure(figsize=(10, 5))

plt.plot(
    f,
    20 * np.log10(np.maximum(np.abs(H_kaiser), 1e-12)),
    label=f'Kaiser, M = {M_kaiser}'
)

plt.plot(
    f,
    20 * np.log10(np.maximum(np.abs(H_pm), 1e-12)),
    label=f'Parks-McClellan, M = {M_pm}'
)

# Granice pasm i wymagane tlumienie
plt.axvline(Fpass, color='green', linestyle='--',
            label='Fpass = 1000 Hz')

plt.axvline(Fstop, color='red', linestyle='--',
            label='Fstop = 1500 Hz')

plt.axhline(-Rs, color='black', linestyle=':',
            label='Rs = 30 dB')

plt.title('Porownanie filtrow FIR')
plt.xlabel('Czestotliwosc [Hz]')
plt.ylabel('Amplituda [dB]')
plt.ylim(-80, 5)
plt.grid()
plt.legend()
plt.tight_layout()
plt.show()