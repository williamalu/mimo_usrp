import numpy as np

if __name__ == "__main__":
    data_path = '../data/'

    np.random.seed(45)
    noise1 = np.random.randn(50000);
    noise2 = np.random.randn(50000);

    noise1.tofile(data_path + "noise_1.bin")
    noise2.tofile(data_path + "noise_2.bin")

    zeros_gap = np.zeros(10000);

    zeros = np.zeros(50000);

    channel1 = np.concatenate( [noise1, zeros_gap, zeros] )
    channel2 = np.concatenate( [zeros, zeros_gap, noise2] )

    channel1 = np.array( channel1, dtype=np.complex64 )
    channel2 = np.array( channel2, dtype=np.complex64 )

    channel1.tofile(data_path + "noise_1_transmit.bin")
    channel2.tofile(data_path + "noise_2_transmit.bin")

    