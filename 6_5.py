# New Python file

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal



Fs = 5000
Fpass = 1000
Fstop = 1500
Rp = 1
Rs = 30


# Butterworth
n_b, wn_b = signal.buttord(
    Fpass, Fstop, Rp, Rs, fs=Fs
)
b_b, a_b = signal.butter(n_b, wn_b, fs=Fs)

# Chebyshev Type I
n_c1, wn_c1 = signal.cheb1ord(
    Fpass, Fstop, Rp, Rs, fs=Fs
)
b_c1, a_c1 = signal.cheby1(
    n_c1, Rp, wn_c1, fs=Fs
)

# Chebyshev Type II
n_c2, wn_c2 = signal.cheb2ord(
    Fpass, Fstop, Rp, Rs, fs=Fs
)
b_c2, a_c2 = signal.cheby2(
    n_c2, Rs, wn_c2, fs=Fs
)

# Elliptic
n_e, wn_e = signal.ellipord(
    Fpass, Fstop, Rp, Rs, fs=Fs
)
b_e, a_e = signal.ellip(
    n_e, Rp, Rs, wn_e, fs=Fs
)

filters = {
    "Butterworth": (b_b, a_b),
    "Chebyshev I": (b_c1, a_c1),
    "Chebyshev II": (b_c2, a_c2),
    "Elliptic": (b_e, a_e)
}


print("RZEDY FILTROW:")
print("Butterworth:", n_b)
print("Chebyshev I:", n_c1)
print("Chebyshev II:", n_c2)
print("Elliptic:", n_e)

for name, (b, a) in filters.items():
    print("\n", name)
    print("Licznik B =", np.round(b, 6))
    print("Mianownik A =", np.round(a, 6))

# H(z) = B(z) / A(z)
# B(z) = b0 + b1*z^-1 + ...
# A(z) = a0 + a1*z^-1 + ...

# ==========================================
# 4. ZERA I BIEGUNY
# ==========================================

fig, axes = plt.subplots(2, 2, figsize=(10, 10))

theta = np.linspace(0, 2*np.pi, 500)

for ax, (name, (b, a)) in zip(axes.flat, filters.items()):

    zeros, poles, gain = signal.tf2zpk(b, a)

    ax.plot(np.cos(theta), np.sin(theta),
            'k--', label="Okrag jednostkowy")

    ax.scatter(zeros.real, zeros.imag,
               marker='o', facecolors='none',
               edgecolors='blue', s=80,
               label="Zera")

    ax.scatter(poles.real, poles.imag,
               marker='x', color='red',
               s=80, label="Bieguny")

    ax.axhline(0, color='gray', linewidth=0.5)
    ax.axvline(0, color='gray', linewidth=0.5)

    ax.set_title(name)
    ax.set_xlabel("Re")
    ax.set_ylabel("Im")
    ax.set_aspect('equal')
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.grid(True)
    ax.legend()

plt.suptitle("Zera i bieguny filtrow IIR")
plt.tight_layout()
plt.show()

# ==========================================
# 5. CHARAKTERYSTYKI AMPLITUDOWE
# ==========================================

plt.figure(figsize=(12, 6))

for name, (b, a) in filters.items():

    f, H = signal.freqz(b, a, worN=8192, fs=Fs)

    magnitude = 20 * np.log10(
        np.maximum(np.abs(H), 1e-12)
    )

    plt.plot(f, magnitude, label=name)

plt.axvline(Fpass, color='green', linestyle='--',
            label="Fpass = 1000 Hz")

plt.axvline(Fstop, color='red', linestyle='--',
            label="Fstop = 1500 Hz")

plt.axhline(-Rp, color='green', linestyle=':')
plt.axhline(-Rs, color='red', linestyle=':')

plt.title("Charakterystyki amplitudowe filtrow IIR")
plt.xlabel("Czestotliwosc [Hz]")
plt.ylabel("Amplituda [dB]")
plt.ylim(-100, 5)
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

# ==========================================
# 6. CHARAKTERYSTYKI FAZOWE
# ==========================================

plt.figure(figsize=(12, 6))

for name, (b, a) in filters.items():

    f, H = signal.freqz(b, a, worN=8192, fs=Fs)

    phase = np.unwrap(np.angle(H))

    plt.plot(f, phase, label=name)

plt.title("Charakterystyki fazowe filtrow IIR")
plt.xlabel("Czestotliwosc [Hz]")
plt.ylabel("Faza [rad]")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

# ==========================================
# 7. ODPOWIEDZI IMPULSOWE
# ==========================================

N = 100

impulse = np.zeros(N)
impulse[0] = 1

fig, axes = plt.subplots(2, 2, figsize=(12, 8))

for ax, (name, (b, a)) in zip(axes.flat, filters.items()):

    h = signal.lfilter(b, a, impulse)

    ax.stem(np.arange(N), h, basefmt=" ")

    ax.set_title(name)
    ax.set_xlabel("Numer probki")
    ax.set_ylabel("Amplituda")
    ax.grid(True)

plt.suptitle("Odpowiedzi impulsowe filtrow IIR")
plt.tight_layout()
plt.show()

# ==========================================
# 8. SPRAWDZENIE WYMAGAN
# ==========================================

print("\nSPRAWDZENIE WYMAGAN:")

for name, (b, a) in filters.items():

    f, H = signal.freqz(b, a, worN=16384, fs=Fs)

    mag = 20 * np.log10(
        np.maximum(np.abs(H), 1e-12)
    )

    passband = mag[f <= Fpass]
    stopband = mag[f >= Fstop]

    # Maksymalny spadek w pasmie przepustowym
    pass_loss = -np.min(passband)

    # Minimalne tlumienie w pasmie zaporowym
    stop_attenuation = -np.max(stopband)

    # Sprawdzenie stabilnosci
    poles = np.roots(a)
    stable = np.all(np.abs(poles) < 1)

    # Niewielka tolerancja numeryczna
    tolerance = 1e-6

    meets_requirements = (
        pass_loss <= Rp + tolerance
        and stop_attenuation >= Rs - tolerance
        and stable
    )

    print("\n", name)
    print("Tlumienie w pasmie przepustowym:",
          round(pass_loss, 3), "dB")
    print("Tlumienie w pasmie zaporowym:",
          round(stop_attenuation, 3), "dB")
    print("Stabilny:", stable)
    print("Spelnia wymagania:", meets_requirements)
