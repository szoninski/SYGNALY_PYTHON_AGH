import matplotlib.pyplot as plt
import numpy as np

wybor = int(input("wybierz wykres"))

if wybor == 1:

  # 1. Definicja parametrów
  omega = 2 * np.pi * 1  
  t = np.linspace(0, 2, 500)  
 
  
  y1 = np.exp(1j * omega * t)


  fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6), sharex=True)


  ax1.plot(t, y1.real, color="crimson", linewidth=2, label=r"$\text{Re}\{e^{j\omega t}\} = \cos(\omega t)$")
  ax1.grid(True, linestyle="--", alpha=0.6)
  ax1.set_ylabel("Amplituda")
  ax1.legend(loc="upper right")
  ax1.set_title(r"Wykres funkcji $e^{j\omega t}$ w dziedzinie czasu", fontsize=14)


  ax2.plot(t, y1.imag, color="dodgerblue", linewidth=2, label=r"$\text{Im}\{e^{j\omega t}\} = \sin(\omega t)$")
  ax2.grid(True, linestyle="--", alpha=0.6)
  ax2.set_xlabel("Czas t [s]")
  ax2.set_ylabel("Amplituda")
  ax2.legend(loc="upper right")

  plt.tight_layout()
  plt.show()
  print(ax1)

if wybor == 2:

  import matplotlib.pyplot as plt
  import numpy as np

# 1. Definicja parametrów funkcji
  c = 4.0          
  a = -0.5         
  omega = 3.0      
  
 
  t = np.linspace(0, 10, 500)
  # Jedno główne równanie w Pythonie:
  y2 = 4 * np.exp(-0.5 * t) * np.cos(3 * t)
  
  # Opcjonalnie: obwiednia wykresu (pokazuje jak zanika amplituda)
  obwiednia_gorna = c * np.exp(a * t)
  obwiednia_dolna = -c * np.exp(a * t)
  
  # 3. Tworzenie wykresu i określenie rozmiaru okna
  fig, ax = plt.subplots(figsize=(8, 6))
  
  # 4. Rysowanie funkcji oraz obwiedni (przerywaną linią)
  ax.plot(t, y2, color="blue", linewidth=2, label=r"$f(t) = c \cdot e^{at} \cdot \cos(\omega t)$")
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
  plt.tight_layout()
  plt.show()



#if y1 - y2 == 0:
  print(ax1)
  
  