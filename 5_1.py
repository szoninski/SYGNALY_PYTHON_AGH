# New Python file

import matplotlib.pyplot as plt
import numpy as np

# Parametry sygnałów
A = 1               # Amplituda
phi = 0             # Faza początkowa
omega0 = 0.2 * np.pi
omega1 = omega0
omega2 = omega0 + 2 * np.pi

# Zakres próbek
n = np.arange(0, 50, 1)

# Obliczenie sygnałów
x1 = A * np.cos(omega1 * n + phi)
x2 = A * np.cos(omega2 * n + phi)

# Rysowanie wykresów
plt.figure(figsize=(10, 5))

plt.stem(n, x1, linefmt='b-', markerfmt='bo',
         basefmt='k-', label='omega0')
plt.stem(n, x2, linefmt='r--', markerfmt='rx',
         basefmt='k-', label='omega0 + 2pi')

plt.title('Porównanie dwóch sygnałów sinusoidalnych')
plt.xlabel('Numer próbki n')
plt.ylabel('Amplituda')
plt.legend()
plt.grid(True)
plt.show()
