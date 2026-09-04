import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

measurements_mg_L = np.array([
    10.02, 10.05, 9.98, 10.01, 10.03, 9.99,
    10.04, 10.00, 10.06, 9.97, 10.02, 10.42,
])
alpha = 0.05

n = len(measurements_mg_L)
mean = np.mean(measurements_mg_L)
sample_sd = np.std(measurements_mg_L, ddof=1)
deviations = np.abs(measurements_mg_L - mean)

suspect_index = np.argmax(deviations)
suspect_value = measurements_mg_L[suspect_index]
G_calculated = deviations[suspect_index] / sample_sd

# Tosidig kritisk verdi for én mulig utligger.
t_critical = stats.t.ppf(1 - alpha / (2 * n), df=n - 2)
G_critical = (n - 1) / np.sqrt(n) * np.sqrt(
    t_critical**2 / (n - 2 + t_critical**2)
)

flagged = G_calculated > G_critical

print(f"Antall målinger: {n}")
print(f"Kandidat:        {suspect_value:.2f} mg/L")
print(f"Beregnet G:      {G_calculated:.3f}")
print(f"Kritisk G:       {G_critical:.3f}")
print(f"Statistisk flagg: {flagged}")

measurement_number = np.arange(1, n + 1)
plt.scatter(measurement_number, measurements_mg_L, label="Målinger")
plt.scatter(
    measurement_number[suspect_index],
    suspect_value,
    color="#b23a48",
    label="Kandidat",
    zorder=3,
)
plt.axhline(mean, color="black", linestyle="--", label="Gjennomsnitt")
plt.xlabel("Måling nummer")
plt.ylabel("Konsentrasjon (mg/L)")
plt.xticks(measurement_number)
plt.legend()
plt.tight_layout()
plt.show()
