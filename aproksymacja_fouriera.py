import numpy as np
import matplotlib.pyplot as plt


def fourier_coeff(k, T0, T1):
    """Wspolczynniki szereju Fouriera a_k = (1/T0) * integral x(t) e^{-jkW0 t} dt.
    Dla symetrycznego impulsu: a_k = sin(k*W0*T1) / (k*pi), a_0 = 2*T1/T0."""
    if k == 0:
        return 2.0 * T1 / T0
    Omega0 = 2.0 * np.pi / T0
    return np.sin(k * Omega0 * T1) / (k * np.pi)


def x_original(t, T0, T1):
    """Oryginalny sygnal prostokatny (okresowy, symetryczny wzgledem t=0)."""
    t_mod = np.mod(t + T0 / 2.0, T0) - T0 / 2.0   # t w (-T0/2, T0/2]
    return np.where(np.abs(t_mod) < T1, 1.0, 0.0)


def x_approx(t, N, T0, T1):
    """Aproksymacja x_N(t) = sum_{k=-N}^{N} a_k e^{jk Omega0 t} (rzeczywista)."""
    Omega0 = 2.0 * np.pi / T0
    xN = np.zeros_like(t, dtype=complex)   # zespolona, bo wykladniki sa zespolone
    for k in range(-N, N + 1):
        xN = xN + fourier_coeff(k, T0, T1) * np.exp(1j * k * Omega0 * t)
    return np.real(xN)


def error_EN(N, T0, T1, num_samples=200001):
    """E_N = calka po okresie T0 z |x(t) - x_N(t)|^2 dt (numerycznie, trapezy)."""
    t = np.linspace(-T0 / 2.0, T0 / 2.0, num_samples)
    diff = x_original(t, T0, T1) - x_approx(t, N, T0, T1)
    # trapez: np.trapz usuniete w NumPy 2.x, zamiast niej np.trapezoid
    trapz = getattr(np, "trapezoid", None) or getattr(np, "trapz")
    return trapz(diff ** 2, t)


# ------------------- Parametry przypadkow a) i b) -------------------
cases = [
    ("a) T0 = 1, T1 = 0.25", 1.0, 0.25),
    ("b) T0 = 1, T1 = 0.1",  1.0, 0.10),
]

# ----------------------- Analiza dla obu przypadkow ------------------
t = np.linspace(-1.0, 1.0, 4000)      # dwa okresy do wizualizacji
Ns = [1, 3, 5, 10, 20, 50]            # liczba harmonicznych
tag = {"a) T0 = 1, T1 = 0.25": "a", "b) T0 = 1, T1 = 0.1": "b"}  # czyste nazwy plikow

for title, T0, T1 in cases:
    x = x_original(t, T0, T1)

    # wykres aproksymacji dla roznych N
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(t, x, "k", lw=1.5, label="x(t)")
    for N in Ns:
        ax.plot(t, x_approx(t, N, T0, T1), lw=1.0, label=f"x_{N}(t)")
    ax.set_title(f"Aproksymacja szeregiem Fouriera – {title}")
    ax.set_xlabel("t"); ax.set_ylabel("x(t)"); ax.legend(); ax.grid(True)
    plt.tight_layout()
    plt.savefig(f"aprox_{tag[title]}.png", dpi=150)
    plt.show()

    # bledy E_N oraz wykres zbieznosci
    EN = [error_EN(N, T0, T1) for N in Ns]
    print(f"\n=== {title} ===")
    print("  N     E_N")
    for N, e in zip(Ns, EN):
        print(f"{N:4d}   {e:.6e}")

    plt.figure(figsize=(7, 4.5))
    plt.semilogy(Ns, EN, "o-")
    plt.title(f"Błąd aproksymacji E_N – {title}")
    plt.xlabel("N"); plt.ylabel("E_N (skala log)"); plt.grid(True, which="both")
    plt.tight_layout()
    plt.savefig(f"blad_{tag[title]}.png", dpi=150)
    plt.show()

print("\nE_N maleje ~ jak 1/(2N+1) (tw. Parsevala), co potwierdza zbieznosc szeregu.")