
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal

# Parametry sygnałów
A = 1
phi = 0
omega0 = 0.2 * np.pi

# Dwie różne długości sygnałów
N1 = 30
N2 = 50

# Przedziały próbek
n1 = np.arange(N1)
n2 = np.arange(N2)

# Generowanie dwóch sygnałów
x1 = A * np.cos(omega0 * n1 + phi)
x2 = A * np.cos((omega0 + 2*np.pi) * n2 + phi)

# Splot sygnałów
y = signal.convolve(x1, x2, mode='full')

# Oś próbek dla wyniku splotu
n3 = np.arange(len(y))

# Wykresy
plt.figure(figsize=(12, 8))

plt.subplot(3, 1, 1)
plt.stem(n1, x1)
plt.title('Pierwszy sygnał sinusoidalny (N = 30)')
plt.xlabel('Próbka n')
plt.ylabel('Amplituda')
plt.grid()

plt.subplot(3, 1, 2)
plt.stem(n2, x2)
plt.title('Drugi sygnał sinusoidalny (N = 50)')
plt.xlabel('Próbka n')
plt.ylabel('Amplituda')
plt.grid()

plt.subplot(3, 1, 3)
plt.stem(n3, y)
plt.title('Splot dwóch sygnałów')
plt.xlabel('Próbka n')
plt.ylabel('Amplituda')
plt.grid()

plt.tight_layout()
plt.show()
