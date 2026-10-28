import numpy as np

# These three arrays do not quite match the descriptions in the exercise.
# Change the arguments so that every array becomes correct.
even_numbers = np.arange(0, 10, 2)
many_values = np.linspace(0, 10, 100)
descending_integers = np.arange(100, 1, -1)

print("Even numbers:", even_numbers)
print("Number of evenly spaced values:", len(many_values))
print("Last descending integer:", descending_integers[-1])
