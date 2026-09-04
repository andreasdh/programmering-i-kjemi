import numpy as np
from scipy import stats

method_A_mg_L = np.array([5.10, 10.20, 7.50, 12.30, 3.90, 8.80, 15.10, 6.40])
method_B_mg_L = np.array([5.22, 10.28, 7.65, 12.40, 3.99, 8.93, 15.21, 6.47])

differences = method_B_mg_L - method_A_mg_L
n_pairs = len(differences)
mean_difference = np.mean(differences)
sd_difference = np.std(differences, ddof=1)
standard_error = sd_difference / np.sqrt(n_pairs)
df = n_pairs - 1
alpha = 0.05

paired_test = stats.ttest_rel(method_B_mg_L, method_A_mg_L)
t_critical = stats.t.ppf(1 - alpha / 2, df=df)
ci_lower = mean_difference - t_critical * standard_error
ci_upper = mean_difference + t_critical * standard_error

print("Forskjell for hvert prøvepar:")
print(differences)
print(f"Gjennomsnittlig B − A:   {mean_difference:.3f} mg/L")
print(f"95 % KI for forskjellen: [{ci_lower:.3f}, {ci_upper:.3f}] mg/L")
print(f"t-statistikk:            {paired_test.statistic:.3f}")
print(f"Frihetsgrader:           {df}")
print(f"p-verdi (tosidig):       {paired_test.pvalue:.5f}")
