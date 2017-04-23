import numpy as np
import matplotlib.pyplot as plt

def takeFFT(data):
    data = data / np.linalg.norm(data)
    data_squared = np.square(data)
    fft_out = np.fft.fft(data_squared)
    fft_shape = np.fft.fftfreq(data_squared.shape[-1])

    plt.stem(fft_shape, fft_out)
    #plt.stem(fft_shape, np.fft.fftshift(fft_out))

def showData(data):
    plt.plot(data.real)
    plt.plot(data.imag)


def showStar(data):
    plt.figure()
    plt.plot(data.real, data.imag, '.')


def fixFreq(data, freq, hbar):
    for i, val in enumerate(data):
        data[i] = val*np.exp( (0 - 1j)*freq*i ) / hbar
    return data


if __name__ == "__main__":

    data = np.fromfile('new_received_trimmed.bin', dtype=np.complex64)
    
    takeFFT(data)
    #data = fixFreq(data, 0.007333 * np.pi, np.sqrt(0.68188))
    #showData(data)
    showStar(data)

    plt.show()
