import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.6), dpi=150)

fy = ["FY21", "FY22", "FY23", "FY24", "FY25", "FY26"]
upi_volume_cr = [2233, 4597, 8376, 13113, 18587, 24162]
bars = ax1.bar(fy, upi_volume_cr, color="#1f77b4", width=0.62)
for b, v in zip(bars, upi_volume_cr):
    ax1.text(b.get_x() + b.get_width() / 2, b.get_height() * 1.03,
             f"{v:,}", ha="center", va="bottom", fontsize=8.5)
ax1.set_yscale("log")
ax1.set_title("UPI: Annual transaction volume (crore, log scale)", fontsize=10.5)
ax1.set_ylabel("Transactions per year (crore)")
ax1.set_ylim(top=60000)
ax1.grid(axis="y", linestyle=":", alpha=0.5)
ax1.text(0.02, 0.94,
         "e\u20b9 (cumulative, Jul 2026): 17.5 crore\n(~1,400\u00d7 smaller than UPI FY26)",
         transform=ax1.transAxes, fontsize=8, va="top",
         bbox=dict(boxstyle="round", fc="#fff4d6", ec="#d9a400"))

labels = ["Users\n(million)", "Cumulative\ntransactions\n(million)"]
dec_2025 = [8, 120]
jul_2026 = [12, 175]
x = [0, 1]
width = 0.35
b1 = ax2.bar([i - width / 2 for i in x], dec_2025, width, label="Dec 2025", color="#2ca02c")
b2 = ax2.bar([i + width / 2 for i in x], jul_2026, width, label="Jul 2026", color="#ff7f0e")
for bars in (b1, b2):
    for b in bars:
        ax2.text(b.get_x() + b.get_width() / 2, b.get_height() * 1.02,
                 f"{int(b.get_height()):,}", ha="center", va="bottom", fontsize=8.5)
ax2.set_xticks(x)
ax2.set_xticklabels(labels, fontsize=9)
ax2.set_title("Digital Rupee (e\u20b9): Adoption milestones", fontsize=10.5)
ax2.set_ylabel("Count (million)")
ax2.set_ylim(top=220)
ax2.legend(fontsize=8.5, loc="upper left")
ax2.grid(axis="y", linestyle=":", alpha=0.5)

fig.suptitle("Scale comparison: UPI vs India's Digital Rupee (e\u20b9)",
             fontsize=12, y=1.02)
fig.tight_layout()
fig.savefig("erupee_chart.png", bbox_inches="tight")
print("saved erupee_chart.png")