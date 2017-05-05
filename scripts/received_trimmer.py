import numpy as np
import matplotlib.pyplot as plt


if __name__ == "__main__":
    received1 = np.fromfile("../data/received_1.bin", dtype=np.complex64)
    received2 = np.fromfile("../data/received_2.bin", dtype=np.complex64)
    plt.plot(np.abs(received2))
    plt.show()

    max_compare = np.max(received1)

    beginning = 0
    for i, val in enumerate(np.absolute(received1)):
        if np.absolute(val) >= max_compare/4:
            beginning = i
            break

    end = 0
    for i, val in enumerate(np.absolute(received1[::-1])):
        if np.absolute(val) >= max_compare/4:
            end = len(received1) - i
            break

    buffer_len = 0 #(end - beginning)//2
    received1_trimmed = received1[beginning-buffer_len : end+buffer_len]
    received2_trimmed = received2[beginning-buffer_len : end+buffer_len]

    received1_trimmed.tofile("../data/received_1_trimmed.bin")
    received2_trimmed.tofile("../data/received_2_trimmed.bin")
    
    plt.subplot(2, 1, 1)
    plt.plot(received1_trimmed.real)
    plt.plot(received1_trimmed.imag)
    plt.subplot(2, 1, 2)
    plt.plot(received2_trimmed.real)
    plt.plot(received2_trimmed.imag)
    plt.show()


