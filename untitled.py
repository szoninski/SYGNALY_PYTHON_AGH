# New Python fileimport matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import numpy as np
a = int(input("podaj poczatek przedzialu"))
b = int(input("podaj koniec przedzialu"))

def f(x):
    return -x**2+0.5*x+2
  

# Przedział [a, b]


# Gęsto próbkujemy funkcję — im więcej punktów, tym dokładniej
x = np.linspace(a, b, 1000)
y = f(x)

# Pole pod wykresem = całka oznaczona
pole = np.trapezoid(y, x)        # w starszych wersjach NumPy
# pole = np.trapezoid(y, x)  # NumPy >= 2.0 (np.trapz usunięte)

print(f"Pole pod wykresem: {pole:.6f}")

# Wizualizacja: wykres + zaznaczone pole
fig, ax = plt.subplots()
ax.plot(x, y, 'b', linewidth=2, label='f(x) = do zdefiniowania')
ax.fill_between(x, y, alpha=0.3, color='green', label='pole pod wykresem')
ax.legend()
plt.show()
