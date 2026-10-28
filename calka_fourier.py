import numpy as np
import matplotlib.pyplot as plt




# 1. Okresl przedzial calkowania
a = int(input("Podaj początek przedziału: "))
b = int(input("Podaj koniec przedziału: "))
w = float(input("Podaj omega (w): "))   # czestotliwosc

# 2. Zdefiniuj sygnal x(t) — przyklad: x(t) = t^2
def x(t):
    return t**2   # <-- tu wpisz swoja funkcje

# 3. Probkowanie i calka zespolona metoda trapezow
t = np.linspace(a, b, 1000)
y = x(t) * np.exp(-1j * w * t)

calka = np.trapezoid(y, t)   # starsze NumPy: np.trapz
print(f"Wartość całki: {calka}")
print(f"Część rzeczywista: {calka.real:.6f}")
print(f"Część urojona:   {calka.imag:.6f}")

# 4. Wykres — osobno Re i Im (wynik jest zespolony)
fig, ax = plt.subplots()
ax.plot(t, y.real, 'b', label='Re{ x(t)·e^(-jwt) }')
ax.plot(t, y.imag, 'r--', label='Im{ x(t)·e^(-jwt) }')
ax.fill_between(t, y.real, alpha=0.2)   # "pole" pod czescia rzeczywista
ax.legend()
plt.show()