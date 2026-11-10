# New Python file
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# ------------------------------------------------------------
# Input signals x[n] and impulse response h[n]
# ------------------------------------------------------------
x = np.array([1.0, 2.0, 3.0, 4.0])          # x[n], starts at n = 0
h = np.array([0.5, 1.0, 0.5])              # h[n], starts at n = 0

x_start = 0   # index of the first sample of x
h_start = 0   # index of the first sample of h

# ------------------------------------------------------------
# 1) Manual implementation of the convolution sum:
#    y[n] = sum_k x[k] * h[n-k]
# ------------------------------------------------------------
def conv_sum(x, h, x_start=0, h_start=0):
    """Compute y = x*h with explicit summation; returns (y, y_start)."""
    N, M = len(x), len(h)
    L = N + M - 1                       # length of the result
    y = np.zeros(L)
    for n in range(L):                  # for every output sample
        # k must satisfy: 0 <= k <= N-1  and  0 <= n-k <= M-1
        k_min = max(0, n - (M - 1))
        k_max = min(N - 1, n)
        for k in range(k_min, k_max + 1):
            y[n] += x[k] * h[n - k]
    return y, x_start + h_start         # index of y[0]

y_own, y_start = conv_sum(x, h, x_start, h_start)

# Equivalent "flipped h" view, for demonstration:
# y[n] = sum_k x[k] * h[n-k]  ->  flip h and slide it over x
y_flip = np.zeros(len(x) + len(h) - 1)
for n in range(len(y_flip)):
    acc = 0.0
    for k in range(len(x)):
        idx = n - k                     # index into h
        if 0 <= idx < len(h):
            acc += x[k] * h[idx]
        # outside the range h[n-k] = 0, so nothing is added
    y_flip[n] = acc

# ------------------------------------------------------------
# 2) Reference implementations (equivalent of Matlab conv)
# ------------------------------------------------------------
y_np = np.convolve(x, h, mode="full")
y_sp = signal.convolve(x, h, mode="full")

# ------------------------------------------------------------
# 3) Compare
# ------------------------------------------------------------
print("manual convolution :", y_own)
print("flipped-h version  :", y_flip)
print("np.convolve        :", y_np)
print("scipy convolution  :", y_sp)
print(f"max |y_own - y_np| = {np.max(np.abs(y_own - y_np)):.3e}")
print(f"max |y_own - y_sp| = {np.max(np.abs(y_own - y_sp)):.3e}")

# ------------------------------------------------------------
# 4) Plot
# ------------------------------------------------------------
n_y = np.arange(y_start, y_start + len(y_own))   # absolute indices of y

fig, axes = plt.subplots(3, 1, figsize=(10, 8))

axes[0].stem(np.arange(x_start, x_start + len(x)), x, basefmt="k-")
axes[0].set_title("x[n]")
axes[0].set_ylabel("x")
axes[0].grid(True, alpha=0.3)

axes[1].stem(np.arange(h_start, h_start + len(h)), h, basefmt="k-")
axes[1].set_title("h[n]")
axes[1].set_ylabel("h")
axes[1].grid(True, alpha=0.3)

axes[2].stem(n_y, y_own, linefmt="C0-", markerfmt="C0o", basefmt="k-",
             label="manual conv sum")
axes[2].plot(n_y, y_np, "C3--", lw=1.5, label="np.convolve")
axes[2].set_title("y[n] = x[n] * h[n]")
axes[2].set_xlabel("n")
axes[2].set_ylabel("y")
axes[2].legend()
axes[2].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()