
import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# 1. DEFINICJA SYGNAŁÓW
# ==========================================

dt = 0.01
t = np.arange(-5, 5 + dt, dt)

# Sygnał x(t) - impuls trójkątny
def x(t):
    return np.maximum(1 - np.abs(t), 0)

# Sygnał h(t) - odpowiedź wykładnicza
def h(t):
    return np.where(t >= 0, np.exp(-t), 0)

xt = x(t)
ht = h(t)

# ==========================================
# 2. OBLICZANIE SPLOTU
# ==========================================

# Przybliżenie całki przez sumę
y = np.convolve(xt, ht, mode="full") * dt

# Oś czasu wyniku splotu
ty = np.arange(2 * len(t) - 1) * dt + 2 * t[0]

# ==========================================
# 3. WYBÓR CHWILI DO POKAZANIA SPLOTU
# ==========================================

t0 = 0.5

# h(t0 - tau): odwrócenie i przesunięcie h
h_shift = h(t0 - t)

# Iloczyn sygnałów pod całką
product = xt * h_shift

# Przybliżona wartość całki dla wybranej chwili
y_t0 = np.sum(product) * dt

# ==========================================
# 4. RYSOWANIE WYKRESÓW
# ==========================================

fig, ax = plt.subplots(3, 2, figsize=(13, 10))

# Sygnał x(t)
ax[0, 0].plot(t, xt, color="blue")
ax[0, 0].set_title("Sygnał x(t)")
ax[0, 0].set_xlabel("t")
ax[0, 0].grid(True)

# Sygnał h(t)
ax[0, 1].plot(t, ht, color="green")
ax[0, 1].set_title("Sygnał h(t)")
ax[0, 1].set_xlabel("t")
ax[0, 1].grid(True)

# Odbicie h względem osi pionowej i przesunięcie
ax[1, 0].plot(t, h(-t), "--", label="h(-τ)")
ax[1, 0].plot(t, h_shift, label=f"h({t0} - τ)")
ax[1, 0].set_title("Odwracanie i przesuwanie sygnału h")
ax[1, 0].set_xlabel("τ")
ax[1, 0].legend()
ax[1, 0].grid(True)

# Iloczyn x(τ) * h(t0 - τ)
ax[1, 1].plot(t, xt, label="x(τ)")
ax[1, 1].plot(t, h_shift, label="h(t₀ - τ)")
ax[1, 1].fill_between(
    t, product, 0, alpha=0.3, label="Iloczyn"
)
ax[1, 1].set_title("Iloczyn pod całką")
ax[1, 1].set_xlabel("τ")
ax[1, 1].legend()
ax[1, 1].grid(True)

# Splot y(t)
ax[2, 0].plot(ty, y, color="red", label="y(t) = x(t) * h(t)")
ax[2, 0].axvline(t0, color="black", linestyle="--")
ax[2, 0].scatter([t0], [y_t0], color="black",
                 label=f"y({t0}) ≈ {y_t0:.4f}")
ax[2, 0].set_title("Wynik konwolucji")
ax[2, 0].set_xlabel("t")
ax[2, 0].legend()
ax[2, 0].grid(True)

# Wartość splotu w wybranej chwili
ax[2, 1].axis("off")
ax[2, 1].text(
    0.05, 0.7,
    f"Chwila t₀ = {t0}\n\n"
    f"y(t₀) ≈ {y_t0:.6f}\n\n"
    "y(t₀) = ∫ x(τ) h(t₀ - τ) dτ",
    fontsize=14,
    transform=ax[2, 1].transAxes
)

plt.tight_layout()
plt.show()

print(f"Przybliżona wartość y({t0}) = {y_t0:.6f}")
