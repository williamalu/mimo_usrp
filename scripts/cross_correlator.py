import numpy as np
import numpy as np
import matplotlib.pyplot as plt

j = (0 + 1j)

if __name__ == "__main__":
    noise1 = np.fromfile('data/channel1_H_estimator.bin', dtype=np.complex64)[:50000]
    noise2 = np.fromfile('data/channel2_H_estimator.bin', dtype=np.complex64)[60000:]
    
    received1 = np.fromfile('data/received1_trimmed.bin', dtype=np.complex64)
    received2 = np.fromfile('data/received2_trimmed.bin', dtype=np.complex64)

    h_11_noisy = received1[725:50725]
    h_21_noisy = received1[60725:110725]

    (lags, c, line, b) = plt.xcorr(h_21_noisy, noise2, maxlags=40000)

    #h_11 = np.correlate(h_11_noisy, noise1)
    #print(h_11)


    #plt.plot(received1)
    #plt.plot(h_21_noisy)
    plt.show()

