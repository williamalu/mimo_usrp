# script for trimming received noise files to estimate H

import numpy as np
import matplotlib.pyplot as plt
import matplotlib

matplotlib.rcParams['agg.path.chunksize'] = 10000

data_path = '../data/'

data1 = np.fromfile(data_path + 'received1.bin', dtype=np.complex64)
data2 = np.fromfile(data_path + 'received2.bin', dtype=np.complex64)

data1 = data1[int(2.974e6):int(3.086e6)]
data2 = data2[int(2.974e6):int(3.086e6)]

# plt.plot(data2[int(2.974e6):int(3.086e6)].real,label="real")
# plt.plot(data2[int(2.974e6):int(3.086e6)].imag,label="imag")
# plt.show()

output_file = open(data_path + 'received1_trimmed.bin', 'wb')
output_file.write(data1.tobytes())
output_file.close()

output_file = open(data_path + 'received2_trimmed.bin', 'wb')
output_file.write(data2.tobytes())
output_file.close()
