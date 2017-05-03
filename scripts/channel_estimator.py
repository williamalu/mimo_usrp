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
    xcorr = np.correlate(noise_h11, noise1, mode='full')
    h11 = xcorr[np.argmax(np.absolute(xcorr))]
    xcorr = np.correlate(noise_h12, noise2, mode='full')
    h12 = xcorr[np.argmax(np.absolute(xcorr))]
    xcorr = np.correlate(noise_h21, noise1, mode='full')
    h21 = xcorr[np.argmax(np.absolute(xcorr))]
    xcorr = np.correlate(noise_h22, noise2, mode='full')
    h22 = xcorr[np.argmax(np.absolute(xcorr))]

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
