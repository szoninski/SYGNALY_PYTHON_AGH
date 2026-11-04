# New Python file
# New Python file
import numpy as np
import matplotlib.pyplot as plt


# --- Parametry specyfikacji (można zmieniać) ---
f0 = 50.0        # częstotliwość wycięcia [Hz]
B = 2.0          # szerokość pasma wycięcia (-3 dB) [Hz]
depth_dB = 40.0  # głębokość wycięcia [dB]

# --- Obliczenie a, b, c ---
b = 2 * np.pi * f0                       # omega
c = np.pi * B                            # [rad/
a = c * 10 ** (-depth_dB / 20.0)         # [rad/s]

print(f"b = {b:.4f} rad/s  (f0 = {f0} Hz)")
print(f"c = {c:.4f} rad/s  (B = {B} Hz)")
print(f"a = {a:.6f} rad/s  (głębokość = {depth_dB} dB)")

# --- Transmitancja H(s) w postaci wymiernej (num/den wg numpy.poly1d) ---
num = [1.0, 2 * a, a**2 + b**2]   # s^2 + 2a s + (a^2+b^2)
den = [1.0, 2 * c, c**2 + b**2]   # s^2 + 2c s + (c^2+b^2)

def H(s):
    """H(s) dla zespolonego s (zgodnie z powyższym num/den)."""
    s = np.asarray(s, dtype=complex)
    num_s = (s + a + 1j * b) * (s + a - 1j * b)
    den_s = (s + c + 1j * b) * (s + c - 1j * b)
    return num_s / den_s

# --- Siatka częstotliwości ---
f = np.logspace(np.log10(1.0), np.log10(5000.0), 2000)  # 1 Hz ... 5 kHz
w = 2 * np.pi * f
Hjw = H(1j * w)

mag_dB = 20 * np.log10(np.abs(Hjw))
phase_deg = np.unwrap(np.angle(Hjw)) * 180 / np.pi

# --- Wartości kontrolne ---
print(f"\n|H(j0)|      = {np.abs(H(0j)):.5f}  ({20*np.log10(np.abs(H(0j))):+.4f} dB)")
print(f"|H(jw0)|     = {np.abs(H(1j*b)):.6f} ({20*np.log10(np.abs(H(1j*b))):+.2f} dB)")
print(f"|H(j*2pi*40)| = {np.abs(H(1j*2*np.pi*40)):.5f}  ({20*np.log10(np.abs(H(1j*2*np.pi*40))):+.4f} dB)")
print(f"|H(j*2pi*60)| = {np.abs(H(1j*2*np.pi*60)):.5f}  ({20*np.log10(np.abs(H(1j*2*np.pi*60))):+.4f} dB)")

# --- Rysowanie charakterystyk ---
fig, axes = plt.subplots(2, 2, figsize=(13, 9))
fig.suptitle(f"Filtr notch:  f0 = {f0} Hz,  B = {B} Hz,  głębokość = {depth_dB} dB\n"
             f"a = {a:.4f},  b = {b:.2f},  c = {c:.4f} rad/s", fontsize=12)

# (1) Charakterystyka amplitudowa [dB] – skala log
ax = axes[0, 0]
ax.semilogx(f, mag_dB, 'b')
ax.axvline(f0, color='r', ls='--', alpha=0.5, label=f'$f_0$ = {f0:.0f} Hz')
ax.axhline(-3, color='gray', ls=':', alpha=0.7, label='-3 dB')
ax.set_xlabel('f [Hz]')
ax.set_ylabel('|H(jω)| [dB]')
ax.set_title('Charakterystyka amplitudowa')
ax.grid(True, which='both', alpha=0.3)
ax.legend()
ax.set_ylim(-60, 5)

# (2) Zoom na wycięcie
ax = axes[0, 1]
f_zoom = np.linspace(f0 - 5, f0 + 5, 1000)
Hjw_zoom = H(1j * 2 * np.pi * f_zoom)
ax.plot(f_zoom, 20 * np.log10(np.abs(Hjw_zoom)), 'b')
ax.axvline(f0, color='r', ls='--', alpha=0.5)
ax.axhline(-3, color='gray', ls=':', alpha=0.7)
for s in (-1, 1):
    ax.axvline(f0 + s * B / 2, color='g', ls='--', alpha=0.6, label='$f_0 ± B/2$' if s == -1 else None)
ax.set_xlabel('f [Hz]')
ax.set_ylabel('|H(jω)| [dB]')
ax.set_title(f'Zoom: wycięcie wokół {f0:.0f} Hz')
ax.grid(True, alpha=0.3)

# (3) Charakterystyka fazowa
ax = axes[1, 0]
ax.semilogx(f, phase_deg, 'b')
ax.axvline(f0, color='r', ls='--', alpha=0.5)
ax.set_xlabel('f [Hz]')
ax.set_ylabel('arg H(jω) [°]')
ax.set_title('Charakterystyka fazowa')
ax.grid(True, which='both', alpha=0.3)

# (4) Bieguny i zera w płaszczyźnie s
ax = axes[1, 1]
zeros = [-a + 1j * b, -a - 1j * b]
poles = [-c + 1j * b, -c - 1j * b]
ax.scatter(np.real(zeros), np.imag(zeros), marker='o', s=80, facecolors='none', edgecolors='b', label='zera')
ax.scatter(np.real(poles), np.imag(poles), marker='x', s=80, c='r', label='bieguny')
ax.axhline(0, color='k', lw=0.5)
ax.axvline(0, color='k', lw=0.5)
ax.set_xlabel('Re(s)')
ax.set_ylabel('Im(s)')
ax.set_title('Bieguny i zera')
ax.grid(True, alpha=0.3)
ax.legend()
#zoom na okolice wycięcia
ax.set_xlim(-10 * max(c, a), 10 * max(c, a))
ax.set_ylim(0, 2 * b)

plt.tight_layout()
plt.savefig('notch_charakterystyki.png', dpi=150)
plt.show()