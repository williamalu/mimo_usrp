import numpy as np
import matplotlib.pyplot as plt


def make_pulses(data, T, pulse):
    widen = np.zeros(len(data) * T, dtype=np.complex64)
    for idx, val in enumerate(widen):
        if idx % T == 0:
            widen[idx] = data[ idx//T ]

    return np.convolve(widen, pulse, 'full')

def raised_cosine(size, T):
    W = 1/T
    pulse = np.zeros(size, dtype=np.complex64)
    alpha = 0.5
    
    for idx, t in enumerate(range(-size//T, size//T)):
        val = np.sinc(2*W*t) * ( np.cos( 2*np.pi*alpha*W*t )/( 1 - 16 * (alpha**2) * (W**2) * (t**2)) )
        pulse[idx] = t

    plt.plot(pulse)
    plt.show()
    exit()
    
    return pulse


if __name__ == "__main__":
    data_path = '../data/'

    # Gen noise
    np.random.seed(45)
    noise_size = 10000
    noise1 = np.array(np.random.choice([0.5, -0.5], size=noise_size))
    noise2 = np.array(np.random.choice([0.5, -0.5], size=noise_size))

    # Make noise into pulses
    T = 50
    pulse = np.ones(50)
    noise1 = make_pulses(noise1, T, pulse)
    noise2 = make_pulses(noise2, T, pulse)

    # Save noise for cross correlation later
    noise1.tofile(data_path + "noise_1.bin")
    noise2.tofile(data_path + "noise_2.bin")

    # Make filler so we can send everything at once
    zeros_gap = np.zeros(60000)
    zeros = np.zeros(len(noise1))

    # Data for channel 1
    channel1 = np.concatenate( [noise1, zeros_gap, zeros] )
    channel2 = np.concatenate( [zeros, zeros_gap, noise2] )

    channel1 = np.array( channel1, dtype=np.complex64 )
    channel2 = np.array( channel2, dtype=np.complex64 )

    # Save out data
    channel1.tofile(data_path + "noise_1_transmit.bin")
    channel2.tofile(data_path + "noise_2_transmit.bin")

    # Plot for verification
    plt.plot(channel1)
    plt.plot(channel2)
    plt.show()
