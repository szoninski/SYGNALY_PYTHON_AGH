# Wykres 2: prostokąty po binaryzacji dwustronnej
bar_width = x[1] - x[0]
for xi, bi in zip(x, binary):
    if bi > 0:
        color = 'mediumseagreen' if bi == 1.0 else 'lightgreen'
    else:
        color = 'indianred' if bi == -1.0 else 'mistyrose'
    # słupek od zera do wartości binarnej (obsługa wartości ujemnych)
    ax2.bar(xi, abs(bi), bottom=min(0, bi),
            width=bar_width * 0.9,
            color=color, edgecolor='black', linewidth=0.3)

ax2.axhline(0, color='black', linewidth=0.8)
ax2.set_title('Binarizacja dwustronna (silne + → 1, słabe + → 0.1, słabe − → -0.1, silne − → -1)')
ax2.set_xlabel('x')
ax2.set_ylabel('wartość binarna')
ax2.set_ylim(-1.15, 1.15)
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()