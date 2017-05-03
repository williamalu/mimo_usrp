import numpy as np
import numpy as np
import matplotlib.pyplot as plt

j = (0 + 1j)

if __name__ == "__main__":
    # Load data files
    noise1 = np.fromfile('../data/noise_1.bin')
    noise2 = np.fromfile('../data/noise_2.bin') 
    noise_h11 = np.fromfile('../data/noise_h11.bin', dtype=np.complex64)
    noise_h12 = np.fromfile('../data/noise_h12.bin', dtype=np.complex64)
    noise_h21 = np.fromfile('../data/noise_h21.bin', dtype=np.complex64)
    noise_h22 = np.fromfile('../data/noise_h22.bin', dtype=np.complex64)

    # Estimate channels
    xcorr11 = np.correlate(noise_h11, noise1, mode='full')
    h11 = xcorr11[np.argmax(np.absolute(xcorr11))]

    xcorr12 = np.correlate(noise_h12, noise2, mode='full')
    h12 = xcorr12[np.argmax(np.absolute(xcorr12))]

    xcorr21 = np.correlate(noise_h21, noise1, mode='full')
    h21 = xcorr21[np.argmax(np.absolute(xcorr21))]

    xcorr22 = np.correlate(noise_h22, noise2, mode='full')
    h22 = xcorr22[np.argmax(np.absolute(xcorr22))]

    # Plot estimator
    plt.subplot(2, 2, 1)
    plt.plot(xcorr11)
    plt.subplot(2, 2, 2)
    plt.plot(xcorr12)
    plt.subplot(2, 2, 3)
    plt.plot(xcorr21)
    plt.subplot(2, 2, 4)
    plt.plot(xcorr22)
    plt.show()

    # Print the channel estimate
    print(h11)
    print(h12)
    print(h21)
    print(h22)
    #print('h11: {}').format(h11)
    #print('h12: {}').format(h12)
    #print('h21: {}').format(h21)
    #print('h22: {}').format(h22)
    print('')

    # SVD
    H_approx = np.matrix([[h11, h12],[h21, h22]])
    np.save("../data/H_approx", H_approx)

    U, E, V_ = np.linalg.svd(H_approx)
    np.save("../data/U_approx", U)
    np.save("../data/E_approx", E)
    np.save("../data/V*_approx", V_)
    print("U: ", U)
    print("E: ", E)
    print("V_: ", V_)
    #print('U:\n{}\n').format(U)
    #print('E:\n{}\n').format(E)
    #print('V_:\n{}\n').format(V_)
