# New Python file
import numpy as np
import matplotlib.pyplot as plt

# ================== FUNKCJA ZDEFINIOWANA PRZEZ UŻYTKOWNIKA ==================
def f(x):
    return np.abs(x)          # wpisz tutaj swoją funkcję

# ================== PARAMETRY ==================
L = np.pi           # połowa okresu (analiza na [-L, L])
N = 500             # liczba próbek
n_terms = 15        # liczba wyrazów szeregu Fouriera

x = np.linspace(-L, L, N)
y = f(x)

# ================== WSPÓŁCZYNNIKI FOURIERA ==================
a0 = (1 / L) * np.trapz(y, x)
a = np.zeros(n_terms)
b = np.zeros(n_terms)

for n in range(1, n_terms + 1):
    a[n-1] = (1 / L) * np.trapz(y * np.cos(n * np.pi * x / L), x)
    b[n-1] = (1 / L) * np.trapz(y * np.sin(n * np.pi * x / L), x)

# ================== APROKSYMACJA ==================
approx = np.full_like(x, a0 / 2)
for n in range(1, n_terms + 1):
    approx += a[n-1] * np.cos(n * np.pi * x / L) + b[n-1] * np.sin(n * np.pi * x / L)

# ================== BINARYZACJA: próg 50% maksimum ==================
threshold = 0.5 * approx.max()   # próg
binary = np.where(approx >= threshold, 1.0, 0.1)   # 1 jeśli >= próg, inaczej 0.1

# ================== WYKRESY ==================
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

# Wykres 1: oryginał i aproksymacja
ax1.plot(x, y, 'b-', label='f(x) — oryginał', linewidth=2)
ax1.plot(x, approx, 'r--', label=f'Aproksymacja Fouriera (n = {n_terms})', linewidth=2)
ax1.axhline(threshold, color='gray', linestyle=':', label='Próg = 50% max')
ax1.set_title('Analiza Fouriera funkcji f(x)')
ax1.set_xlabel('x')
ax1.set_ylabel('f(x)')
ax1.legend()
ax1.grid(True, alpha=0.3)

# Wykres 2: prostokąty po binaryzacji (1 lub 0.1)
bar_width = x[1] - x[0]
colors = np.where(approx >= threshold, 'mediumseagreen', 'lightcoral')
for xi, yi, c in zip(x, binary, colors):
    ax2.bar(xi, yi, width=bar_width * 0.9, color=c, edgecolor='black', linewidth=0.3)

ax2.set_title('Prostokąty po binaryzacji (≥ 50% max → 1, poniżej → 0.1)')
ax2.set_xlabel('x')
ax2.set_ylabel('wartość binarna')
ax2.set_ylim(0, 1.15)
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()