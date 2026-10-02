import numpy as np

vector_v = np.array([1.0, 4.0, 5.0])
vector_w = np.array([2.0, -1.0, 3.0])

print("Addition:", vector_v + vector_w)
print("Subtraction:", vector_v - vector_w)
print("Element-wise multiplication:", vector_v * vector_w)
print("Scalar multiplication:", 3 * vector_v)
print("Dot product:", np.dot(vector_v, vector_w))
