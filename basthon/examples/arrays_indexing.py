import numpy as np

absorbance = np.array([0.12, 0.25, 0.37, 0.49, 0.61])

print("Element with index 2:", absorbance[2])
print("Elements with indices 1 and 2:", absorbance[1:3])
print("From index 2 to the end:", absorbance[2:])
print("The first two elements:", absorbance[:2])
print("The last element:", absorbance[-1])
