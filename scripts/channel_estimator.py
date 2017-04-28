import numpy as np

if __name__ == "__main__":
    noise1 = np.random.randn(50000);
    noise2 = np.random.randn(50000);

    zeros_gap = np.zeros(10000);

    zeros = np.zeros(50000);

    channel1 = np.concatenate( [noise1, zeros_gap, zeros] )
    channel2 = np.concatenate( [zeros, zeros_gap, noise2] )

    channel1 = np.array( channel1, dtype=np.complex64 )
    channel2 = np.array( channel2, dtype=np.complex64 )

    data_path = '../data/'
    channel1.tofile(data_path + "channel1_H_estimator.bin")
    channel2.tofile(data_path + "channel2_H_estimator.bin")

    
