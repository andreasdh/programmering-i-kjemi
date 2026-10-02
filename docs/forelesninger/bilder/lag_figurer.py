import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from mendeleev import element

MARINE, AKSENT, ORANSJE = "#1b3a5c", "#2a7f8f", "#d9822b"
UT = "/home/claude/bilder/"
plt.rcParams.update({"font.size": 14})

# 1) Periodesystem fargekodet etter elektronegativitet
fig, ax = plt.subplots(figsize=(13, 6.2))
cmap = plt.get_cmap("viridis")
norm = matplotlib.colors.Normalize(0.7, 4.0)
for z in range(1, 119):
    e = element(z)
    g, p = e.group_id, e.period
    if g is None:
        continue
    en = e.electronegativity("pauling")
    farge = cmap(norm(en)) if en is not None else (0.88, 0.88, 0.88, 1)
    ax.add_patch(plt.Rectangle((g - 0.5, -p - 0.5), 0.94, 0.94, color=farge))
    tekstfarge = "white" if (en is not None and norm(en) < 0.55) else "black"
    ax.text(g - 0.03, -p + 0.08, e.symbol, ha="center", va="center", fontsize=12, color=tekstfarge, weight="bold")
    if en is not None:
        ax.text(g - 0.03, -p - 0.22, f"{en:.1f}".replace(".", ","), ha="center", va="center", fontsize=8, color=tekstfarge)
ax.set_xlim(0.4, 18.6); ax.set_ylim(-7.6, -0.4); ax.set_aspect("equal"); ax.axis("off")
sm = matplotlib.cm.ScalarMappable(norm=norm, cmap=cmap)
cb = fig.colorbar(sm, ax=ax, shrink=0.7, pad=0.01, format=matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:.1f}".replace(".", ","))); cb.set_label("Elektronegativitet (Pauling)")
ax.set_title("Elektronegativitet i periodesystemet (grå: ingen verdi)", color=MARINE, weight="bold")
fig.tight_layout(); fig.savefig(UT + "elektronegativitet_periodesystem.png", dpi=150); plt.close(fig)

# 2) Annotert boksplott
nitrate = np.array([0.42, 0.47, 0.50, 0.55, 0.58, 0.61, 0.65, 0.72, 0.85, 1.10, 1.35, 2.80])
q1, med, q3 = np.percentile(nitrate, [25, 50, 75]); iqr = q3 - q1
lo = nitrate[nitrate >= q1 - 1.5 * iqr].min(); hi = nitrate[nitrate <= q3 + 1.5 * iqr].max()
fig, ax = plt.subplots(figsize=(12, 4.6))
bp = ax.boxplot(nitrate, orientation="horizontal", widths=0.25, patch_artist=True,
                boxprops=dict(facecolor="#e9f5ee", edgecolor=MARINE, linewidth=2),
                medianprops=dict(color=ORANSJE, linewidth=3),
                whiskerprops=dict(color=MARINE, linewidth=2), capprops=dict(color=MARINE, linewidth=2),
                flierprops=dict(marker="o", markerfacecolor="#b23a48", markeredgecolor="#b23a48", markersize=9))
ax.plot(nitrate, np.full_like(nitrate, 0.66), "|", color="gray", markersize=14)
ax.text(0.40, 0.66, "målingene", va="center", ha="right", color="gray", fontsize=12)
def pil(x, xt, yt, tekst, farge=MARINE):
    ax.annotate(tekst, xy=(x, 1.0), xytext=(xt, yt), ha="center", va="bottom",
                color=farge, fontsize=12, arrowprops=dict(arrowstyle="->", color=farge))
k = lambda v: f"{v:.2f}".replace(".", ",")
pil(q1, 0.42, 1.38, f"Q1 = {k(q1)}\n(25-persentil)")
pil(med, 0.72, 1.68, f"median = {k(med)}", ORANSJE)
pil(q3, 1.02, 1.38, f"Q3 = {k(q3)}\n(75-persentil)")
pil(hi, 1.62, 1.62, "værhåret slutter ved største\nmåling innenfor Q3 + 1,5 · IQR")
pil(2.80, 2.62, 1.38, "mulig utligger:\nundersøk, ikke slett!", "#b23a48")
ax.annotate("", xy=(q1, 0.8), xytext=(q3, 0.8), arrowprops=dict(arrowstyle="<->", color=AKSENT))
ax.text(q3 + 0.03, 0.8, f"IQR = Q3 − Q1 = {k(iqr)}", ha="left", va="center", fontsize=11, color=AKSENT)
ax.set_ylim(0.55, 2.0); ax.set_yticks([]); ax.set_xlim(0.3, 3.0)
ax.set_xlabel("Nitratkonsentrasjon (mg/L)")
ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:.1f}".replace(".", ",")))
for s in ["top", "right", "left"]: ax.spines[s].set_visible(False)
ax.set_title("Hvordan leser vi et boksplott?", color=MARINE, weight="bold")
fig.tight_layout(); fig.savefig(UT + "boksplott_forklart.png", dpi=150); plt.close(fig)

# 3) CSV som råtekst og som tabell
linjer = ["sample_id,sample_type,concentration_uM,replicate,absorbance",
          "blank_1,blank,0,1,0.010", "std_2_1,standard,2,1,0.171",
          "std_2_2,standard,2,2,0.169", "std_6_3,standard,6,3,", "unknown_1,unknown,,1,0.603"]
fig, (a1, a2) = plt.subplots(1, 2, figsize=(14, 3.6), gridspec_kw={"width_ratios": [1.05, 1]})
a1.axis("off"); a1.set_title("Råtekst i fila uvvis_raw.csv", color=MARINE, weight="bold")
a1.add_patch(FancyBboxPatch((0, 0), 1, 1, boxstyle="round,pad=0.02", fc="#f5f7fa", ec="#dde3ea", transform=a1.transAxes))
for i, l in enumerate(linjer):
    a1.text(0.03, 0.88 - i * 0.15, l, family="monospace", fontsize=10.5, transform=a1.transAxes,
            color=MARINE if i == 0 else "black", weight="bold" if i == 0 else "normal")
a2.axis("off"); a2.set_title("Samme data som dataramme i Pandas", color=MARINE, weight="bold")
rader = [l.split(",") for l in linjer]
celler = [[c if c != "" else "NaN" for c in r] for r in rader[1:]]
tab = a2.table(cellText=celler, colLabels=[r[0] for r in [[c] for c in rader[0]]],
               loc="center", cellLoc="center", colWidths=[0.17, 0.2, 0.28, 0.15, 0.2])
tab.auto_set_font_size(False); tab.set_fontsize(9.5); tab.scale(1, 1.55)
for (r, c), cell in tab.get_celld().items():
    cell.set_edgecolor("#dde3ea")
    if r == 0:
        cell.set_facecolor(MARINE); cell.get_text().set_color("white"); cell.get_text().set_weight("bold")
    elif cell.get_text().get_text() == "NaN":
        cell.set_facecolor("#fdf3e7"); cell.get_text().set_color("#b23a48")
fig.text(0.5, 0.02, "Én rad = én observasjon     Én kolonne = én variabel     Tom celle = manglende verdi (NaN)",
         ha="center", color=AKSENT, fontsize=12, weight="bold")
fig.tight_layout(rect=(0, 0.06, 1, 1)); fig.savefig(UT + "csv_og_dataramme.png", dpi=150); plt.close(fig)

# 4) Plassholdere for egne foto
plassholdere = {
    "molekylmodeller.jpg": "Molekylbyggesett: pinnemodell\nog kalottmodell av samme molekyl",
    "panda.jpg": "Panda",
    "spektrofotometer.jpg": "UV-Vis-spektrofotometer\nmed kyvette",
    "flammeprover.jpg": "Flammeprøver:\nNa (gul), Li (rød), K (fiolett)",
    "pipette.jpg": "Pipettering",
    "bekk_provetaking.jpg": "Vannprøvetaking i bekk",
    "kyvetter.jpg": "Ti uavhengig preparerte løsninger\nmot én kyvette målt ti ganger",
}
for navn, tekst in plassholdere.items():
    fig = plt.figure(figsize=(6, 4))
    fig.patch.set_facecolor("#eef1f4")
    fig.text(0.5, 0.58, tekst, ha="center", va="center", fontsize=17, color=MARINE, weight="bold")
    fig.text(0.5, 0.2, f"Plassholder: bytt ut fila\nbilder/{navn}", ha="center", va="center", fontsize=12, color="gray")
    fig.savefig(UT + navn, dpi=100, facecolor=fig.get_facecolor()); plt.close(fig)
print("ok")
