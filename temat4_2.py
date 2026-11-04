# New Python file
# New Python file
import numpy as np
import matplotlib.pyplot as plt

# ----------------------------------------------------------------
# Zadanie 4.2 (wersja Python zamiast Matlaba)
#
# Odpowiednik funkcji Matlaba:
#     function H = freqs_lab(B, A, Om)
# która wyznacza charakterystykę częstotliwościową układu
# ciągłego o transmitancji H(s) = B(s)/A(s)
# dla częstotliwości Om (wektor pulsacji w rad/s).
#
# B, A  - współczynniki wielomianów licznika i mianownika
#         w kolejności malejących potęg s,
#         np. B = [b2, b1, b0]  ->  b2*s^2 + b1*s + b0
# H     - zespolona wartość H(j*Om) dla każdego Om.
# ----------------------------------------------------------------

def freqs_lab(B, A, Om):
    """Wylicza H(j*Om) = B(j*Om)/A(j*Om) wektoryzowane (bez scipy.signal)."""
    B = np.atleast_1d(np.asarray(B, dtype=float))
    A = np.atleast_1d(np.asarray(A, dtype=float))
    Om = np.atleast_1d(np.asarray(Om, dtype=float))

    s = 1j * Om                                    # s = j*omega
    # Horner: wartość wielomianu w punktach s (wektorowo, po kolumnach)
    num = np.full_like(s, 0.0)
    for bcoef in B:
        num = num * s + bcoef
    den = np.full_like(s, 0.0)
    for acoef in A:
        den = den * s + acoef

    H = num / den
    return H if np.ndim(Om) > 0 else H.item()


# ----------------------------------------------------------------
# Przykład użycia: filtr notch z zadania 4.1
#   H(s) = [(s + a + jb)(s + a - jb)] / [(s + c + jb)(s + c - jb)]
# ----------------------------------------------------------------
f0 = 50.0          # częstotliwość wycięcia [Hz]
Bw = 2.0           # szerokość -3 dB [Hz]
depth_dB = 40.0    # głębokość wycięcia [dB]

b = 2 * np.pi * f0
c = np.pi * Bw
a = c * 10 ** (-depth_dB / 20.0)

# B(s) i A(s) w kolejności malejących potęg s
B = [1.0, 2 * a, a**2 + b**2]      # s^2 + 2a s + (a^2 + b^2)
A = [1.0, 2 * c, c**2 + b**2]      # s^2 + 2c s + (c^2 + b^2)

# Siatka pulsacji: od 1 rad/s do ~30000 rad/s
Om = np.logspace(0, 5, 2000)

H = freqs_lab(B, A, Om)            # <- nasza funkcja

# Kontrolne wartości (zgadzają się z 4.1)
print("H(j0)     = |H| = %.5f" % abs(freqs_lab(B, A, 0.0)))
print("H(jw0)    = |H| = %.6f  (%.2f dB)" % (abs(freqs_lab(B, A, b)),
                                             20 * np.log10(abs(freqs_lab(B, A, b)))))
print("H(j2pi60) = |H| = %.5f" % abs(freqs_lab(B, A, 2 * np.pi * 60)))

# ---- Charakterystyki ----
f = Om / (2 * np.pi)
mag_dB = 20 * np.log10(np.abs(H))
phase_deg = np.unwrap(np.angle(H)) * 180 / np.pi

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

ax1.semilogx(f, mag_dB, 'b')
ax1.axvline(f0, color='r', ls='--', alpha=0.5, label=f'$f_0$ = {f0:.0f} Hz')
ax1.axhline(-3, color='gray', ls=':', alpha=0.7, label='-3 dB')
ax1.set_ylabel('|H(j$\\omega$)| [dB]')
ax1.set_title('Charakterystyka amplitudowa (freqs_lab)')
ax1.grid(True, which='both', alpha=0.3)
ax1.legend()
ax1.set_ylim(-60, 5)

ax2.semilogx(f, phase_deg, 'b')
ax2.axvline(f0, color='r', ls='--', alpha=0.5)
ax2.set_xlabel('f [Hz]')
ax2.set_ylabel('arg H(j$\\omega$) [°]')
ax2.set_title('Charakterystyka fazowa')
ax2.grid(True, which='both', alpha=0.3)

plt.tight_layout()
plt.savefig('freqs_lab_charakterystyki.png', dpi=150)
plt.show()