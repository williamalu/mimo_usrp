import numpy as np

V = 100

x = np.array([V, -V, V, V, V, -V, -V, V, V, -V, -V, -V, -V], dtype=complex)

with open("data.bin", "wb") as f:
    f.write(x.tobytes())