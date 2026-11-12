import numpy as np

array_from_list = np.array([1, 2, 3, 4])
values_with_step = np.arange(0, 10, 2)
evenly_spaced_values = np.linspace(0, 10, 6)
zero_array = np.zeros(5)
one_array = np.ones(5)

print("From a list:", array_from_list)
print("Using arange:", values_with_step)
print("Using linspace:", evenly_spaced_values)
print("Zeros:", zero_array)
print("Ones:", one_array)
