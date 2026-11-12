from time import perf_counter
import numpy as np

number_of_values = 100_000
values_list = list(range(number_of_values))
values_array = np.arange(number_of_values)

start = perf_counter()
squared_with_loop = []
for value in values_list:
    squared_with_loop.append(value**2)
loop_time = perf_counter() - start

start = perf_counter()
squared_with_array = values_array**2
vectorized_time = perf_counter() - start

print(f"Loop time: {loop_time:.6f} s")
print(f"Vectorized time: {vectorized_time:.6f} s")
print("The results agree:", squared_with_loop[-1] == squared_with_array[-1])
