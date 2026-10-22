number_of_terms = 100
series_sum = 0

for n in range(number_of_terms):
    term = (2 / 3)**n
    series_sum = series_sum + term

print(series_sum)
