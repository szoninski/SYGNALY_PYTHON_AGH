import numpy as np

def calka_prostokaty(x, dt=1.0, N=100):
    """I ≈ Σ_{n=-N}^{N-1} x(n·dt)·dt  (z wzoru — suma prostokątów)"""
    n = np.arange(-N, N)              # od -N do N-1
    return np.sum(x(n * dt)) * dt

def calka_trapezy(x, dt=1.0, N=100):
    """I ≈ Σ_{n=-N}^{N-1} [x(n·dt) + x((n+1)·dt)]/2 · dt"""
    n = np.arange(-N, N)
    return np.sum((x(n * dt) + x((n + 1) * dt)) / 2) * dt

# przykład: całka z exp(-t²) na przedziale [-N·dt, N·dt]
x = lambda t: np.exp(-t**2)

print(calka_prostokaty(x, dt=0.001, N=5000))   # ≈ 1.7724 (√π)
print(calka_trapezy(x,     dt=0.001, N=5000))
