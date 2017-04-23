#!/usr/bin/env python


""" Class that reads in received data from a specified file, and plots
and decodes the data. """


import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


data = np.fromfile('received_trimmed.bin', dtype=np.complex64)

# with open("received_trimmed.bin", "wb") as f:
#     f.write(data[1171000:1179000].tobytes())

mag = np.absolute(data)
plt.scatter(data.real, data.imag, s=2)
plt.figure()
plt.plot(data.real,'-')
plt.plot(data.imag,'-')

plt.show()