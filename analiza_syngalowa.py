import numpy as np
import matplotlib.pyplot as plt

# ----------------------------------------------------------
# 1. Definicje sygnałów (z zadania 2.2)
# ----------------------------------------------------------
def x(t):                                    # prostokąt 0.5 na |t|<1
    return np.where(np.abs(t) < 1, 0.5, 0.0)

def h(t):                                    # trójkąt t+1 na |t|<1
    return np.where(np.abs(t) < 1, t + 1, 0.0)

def y_dokladne(t):                           # wartość prawdziwa z zadania
    return np.where((-2 < t) & (t <= 0), 0.25*(t + 2)**2,
           np.where((0 < t) & (t < 2),   1 - 0.25*t**2, 0.0))

# ----------------------------------------------------------
# 2. Splot: SUMA RIEMANNA po τ (zmienna), t = parametr
#    y(t) = Σ_n x(τ_n)·h(t − τ_n)·dt,   τ_n = n·dt
# ----------------------------------------------------------
dt  = 0.001                    # krok siatki
T  = 5.0                       # granice całkowania (podpory leżą w [-1,1])
tau = np.arange(-T, T, dt)     # stała siatka po τ — NIE zmienia się w pętli

def y_num(t):                  # t = parametr, stały wewnątrz wywołania
    return np.sum(x(tau) * h(t - tau)) * dt

# ----------------------------------------------------------
# 3. Obliczenie y(t) dla siatki parametrów t
# ----------------------------------------------------------
t_grid = np.arange(-3.0, 3.0, 0.02)
y_wart = np.array([y_num(t) for t in t_grid])   # pętla po parametrze t

blad = np.abs(y_wart - y_dokladne(t_grid))
print(f"dt = {dt}")
print(f"maks. błąd |y_num - y_dokł| w podporze: "
      f"{blad[(t_grid > -1.9) & (t_grid < 1.9)].max():.2e}")
print(f"y(0) numerycznie = {y_num(0.0):.4f}  (dokładnie 1.0)")

# ----------------------------------------------------------
# 4. Wykresy
# ----------------------------------------------------------
fig, ax = plt.subplots(2, 2, figsize=(11, 7))

# (a) x(t) i (b) h(t)
tt = np.arange(-2.5, 2.5, dt)
ax[0, 0].plot(tt, x(tt)); ax[0, 0].set_title('x(t)')
ax[0, 0].set_xlabel('t (s)'); ax[0, 0].set_ylabel('x(t)')
ax[0, 0].set_ylim(-0.2, 2.2); ax[0, 0].grid(True)

ax[0, 1].plot(tt, h(tt)); ax[0, 1].set_title('h(t)')
ax[0, 1].set_xlabel('t (s)'); ax[0, 1].set_ylabel('h(t)')
ax[0, 1].set_ylim(-0.2, 2.2); ax[0, 1].grid(True)

# (c) wnętrze całki dla wybranego PARAMETRU t: wszystko jako funkcje τ
t0 = 0.0                                       # parametr — można zmienić
ax[1, 0].plot(tau, h(t0 - tau), 'r', label='h(t−τ)')     # odbite i przesunięte
ax[1, 0].plot(tau, x(tau),      'b', label='x(τ)')
ax[1, 0].plot(tau, x(tau)*h(t0 - tau), 'k', label='x(τ)·h(t−τ)')
ax[1, 0].fill_between(tau, 0, x(tau)*h(t0 - tau),
                       color='k', alpha=0.15)           # pole = y(t0)
ax[1, 0].set_xlim(-2.5, 2.5); ax[1, 0].set_xlabel('τ (s)')
ax[1, 0].set_title(f'całka w t = {t0}:  y({t0}) = {y_num(t0):.3f}')
ax[1, 0].legend(); ax[1, 0].grid(True)

# (d) wynik splotu numerycznie vs dokładnie
ax[1, 1].plot(t_grid, y_wart,               label='y(t) numerycznie')
ax[1, 1].plot(t_grid, y_dokladne(t_grid), '--', label='y(t) dokładnie')
ax[1, 1].set_xlabel('t (s)'); ax[1, 1].set_ylabel('y(t)')
ax[1, 1].set_title('splot y(t) = x ∗ h')
ax[1, 1].legend(); ax[1, 1].grid(True)

plt.tight_layout(); plt.show()