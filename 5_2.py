# New Python file

import matplotlib.pyplot as plt
import numpy as np
from scipy import signal

# Parametry
omega0 = 0.2 * np.pi

# Długości sygnałów
N1 = 30
N2 = 50

# Funkcja generująca sygnał z równania różnicowego
def sinusoidal_signal(N, omega0):
    x = np.zeros(N)

    # Warunki początkowe
    x[0] = 1
    x[1] = np.cos(omega0)

    # Równanie różnicowe
    for n in range(2, N):
        x[n] = 2 * np.cos(omega0) * x[n-1] - x[n-2]

    return x

# Generowanie sygnałów
x1 = sinusoidal_signal(N1, omega0)
x2 = sinusoidal_signal(N2, omega0)

# Splot sygnałów
y = signal.convolve(x1, x2, mode='full')

# Osie czasu
n1 = np.arange(N1)
n2 = np.arange(N2)
n3 = np.arange(len(y))

# Wykresy
plt.figure(figsize=(12, 9))

plt.subplot(3, 1, 1)
plt.stem(n1, x1)
plt.title('Sygnał 1 - długość 30 próbek')
plt.xlabel('n')
plt.ylabel('x1[n]')
plt.grid()

plt.subplot(3, 1, 2)
plt.stem(n2, x2)
plt.title('Sygnał 2 - długość 50 próbek')
plt.xlabel('n')
plt.ylabel('x2[n]')
plt.grid()

plt.subplot(3, 1, 3)
plt.stem(n3, y)
plt.title('Splot dwóch sygnałów')
plt.xlabel('n')
plt.ylabel('y[n]')
plt.grid()

plt.tight_layout()
plt.show()
