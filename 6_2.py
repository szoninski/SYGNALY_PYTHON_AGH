import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# ------------------------------------------------------------
# System coefficients:  a0*y[n] + a1*y[n-1] + ... = b0*x[n] + b1*x[n-1] + ...
# Solved recursively as:
#   y[n] = sum_{m=0..M} (b[m]/a0)*x[n-m] - sum_{k=1..N} (a[k]/a0)*y[n-k]
# ------------------------------------------------------------
a = np.array([1.0, -0.9])              # denominator (a[0] must be nonzero)
b = np.array([0.5, 0.2, 0.1])          # numerator
# Example: a = [1, -0.9], b = [0.5, 0.2, 0.1] -> IIR low-pass-ish filter

# Input signal: unit impulse (change freely, e.g. np.ones, sine, step...)
N = 40
x = np.zeros(N)
x[0] = 1.0                             # delta[n] -> y = impulse response h[n]

# ------------------------------------------------------------
# 1) Manual implementation of the difference equation (6.2)
# ------------------------------------------------------------
def lccde(b, a, x):
    """Solve y[n] = sum_m (b[m]/a0) x[n-m] - sum_k (a[k]/a0) y[n-k] (zero ICs)."""
    a0 = a[0]
    b_n = b / a0                        # normalized numerator
    a_n = a[1:] / a0                    # normalized feedback coefficients (a1..aN)
    M, Nfb = len(b_n), len(a_n)

    y = np.zeros(len(x))
    for n in range(len(x)):
        # feed-forward part: sum over m = 0..M of b[m]*x[n-m]
        s = 0.0
        for m in range(M):
            if 0 <= n - m < len(x):
                s += b_n[m] * x[n - m]
        # feedback part: subtract sum over k = 1..N of a[k]*y[n-k]
        for k in range(Nfb):
            if 0 <= n - (k + 1):
                s -= a_n[k] * y[n - (k + 1)]
        y[n] = s
    return y

y_own = lccde(b, a, x)

# ------------------------------------------------------------
# 2) Reference: scipy.signal.lfilter (equivalent of Matlab filter())
# ------------------------------------------------------------
y_sp = signal.lfilter(b, a, x)

# ------------------------------------------------------------
# 3) Compare
# ------------------------------------------------------------
err = np.abs(y_own - y_sp)
print(f"max |y_own - lfilter| = {err.max():.3e}")

# ------------------------------------------------------------
# 4) Plot
# ------------------------------------------------------------
n = np.arange(N)
fig, axes = plt.subplots(2, 1, figsize=(10, 7))

axes[0].stem(n, y_own, linefmt="C0-", markerfmt="C0o", basefmt="k-",
             label="manual difference equation")
axes[0].plot(n, y_sp, "C3--", lw=1.5, label="scipy.signal.lfilter")
axes[0].set_xlabel("n")
axes[0].set_ylabel("y[n]")
axes[0].set_title("Response of the system described by the difference equation")
axes[0].legend()
axes[0].grid(True, alpha=0.3)

axes[1].stem(n, err, linefmt="C1-", markerfmt="C1o", basefmt="k-")
axes[1].set_xlabel("n")
axes[1].set_ylabel("|error|")
axes[1].set_title("Absolute difference between manual implementation and lfilter")
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()