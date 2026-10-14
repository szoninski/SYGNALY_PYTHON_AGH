import matplotlib.pyplot as plt
import numpy as np

# 1. Definicja parametrów funkcji
c = 4.0          # Amplituda początkowa
a = -0.5         # Współczynnik tłumienia (ujemny = funkcja zanika)
omega = 3.0      # Częstość kołowa (odpowiada za gęstość fal)

# 2. Generowanie danych (czas t od 0 do 10 sekund, 500 punktów)
t = np.linspace(0, 10, 500)
# Jedno główne równanie w Pythonie:
y = c * np.exp(a * t) * np.cos(omega * t)

# Opcjonalnie: obwiednia wykresu (pokazuje jak zanika amplituda)
obwiednia_gorna = c * np.exp(a * t)
obwiednia_dolna = -c * np.exp(a * t)

# 3. Tworzenie wykresu i określenie rozmiaru okna
fig, ax = plt.subplots(figsize=(8, 6))

# 4. Rysowanie funkcji oraz obwiedni (przerywaną linią)
ax.plot(t, y, color="blue", linewidth=2, label=r"$f(t) = c \cdot e^{at} \cdot \cos(\omega t)$")
ax.plot(t, obwiednia_gorna, "r--", alpha=0.5, label="Obwiednia tłumienia")
ax.plot(t, obwiednia_dolna, "r--", alpha=0.5)

# 5. Przesunięcie osi do punktu (0,0) - klasyczny układ kartezjański
ax.spines["left"].set_position("zero")
ax.spines["bottom"].set_position("zero")

# Ukrycie górnej i prawej krawędzi obramowania
ax.spines["right"].set_color("none")
ax.spines["top"].set_color("none")

# Strzałki na końcach osi
ax.plot(1, 0, ">k", transform=ax.get_yaxis_transform(), clip_on=False)
ax.plot(0, 1, "^k", transform=ax.get_xaxis_transform(), clip_on=False)

# 6. Dodanie siatki, tytułu i legendy
ax.grid(True, linestyle="--", alpha=0.6)
ax.set_title("Wykres drgań tłumionych w układzie kartezjańskim", fontsize=14, pad=20)
ax.set_xlabel("Czas (t)", loc="right")
ax.set_ylabel("Amplituda (f(t))", loc="top")
ax.legend(loc="upper right")

# 7. Ustawienie zakresu osi (dopasowane do wartości c)
ax.set_xlim(-0.5, 10)
ax.set_ylim(-c - 1, c + 1)

# 8. Wyświetlenie wykresu
plt.show()
