import numpy as np
import matplotlib.pyplot as plt

import pll as PLL

j = (0 + 1j)

def apply_U(stream1, stream2, U, PLOT=True, title="Apply U.H"):
    fixed1 = np.zeros(len(stream1), dtype=np.complex64)
    fixed2 = np.zeros(len(stream2), dtype=np.complex64)

    for idx, val1 in enumerate(stream1):
        val2 = stream2[idx]
        vec = np.matrix( [ [val1], [val2] ]) # 2x1 Data Vector
        out = U.H * vec # Correct with U_Hermitian
        
        fixed1[idx] = out[0]
        fixed2[idx] = out[1]

    if PLOT:
        plt.subplot(2, 1, 1)
        plt.plot(fixed1.real)
        plt.plot(fixed1.imag)

        plt.subplot(2, 1, 2)
        plt.plot(fixed2.real)
        plt.plot(fixed2.imag)

        plt.title(title)

        plt.show()

    return fixed1, fixed2


def find_offsets_bpsk(data, PLOT=True, title="Offset BPSK"):
    
    # Prep data
    normalized = data/np.linalg.norm(data)
    squared = np.square(normalized)

    # Take FFT and find max
    fft_data = np.fft.fft( squared )
    fft_shape = np.fft.fftfreq( squared.shape[-1] )
    max_idx = np.absolute(fft_data).argmax()

    # Plot ? 
    if PLOT:
        plt.plot(fft_shape, fft_data)
        plt.title(title)
        plt.show()

    # Extract
    frequency_offset = ( fft_shape[max_idx]/2 ) * (2 * np.pi)
    phase_offset = np.sqrt( fft_data[max_idx] )

    return frequency_offset, phase_offset


def apply_offsets(data, freq_offset, phase_offset, PLOT=True, title="Applied Offsets"):
    fixed = np.zeros(len(data), dtype=np.complex64)

    for idx, val in enumerate(data):
        fixed[idx] = val * np.exp( -j * freq_offset * idx ) / phase_offset

    if PLOT:
        plt.plot(fixed.real)
        plt.plot(fixed.imag)
        plt.title(title)
        plt.show()

    return fixed

def index_of_first_data(data, PLOT=True, title="Find First Data"):
    max_compare = np.max(data)
    beginning = 0

    for idx, val in enumerate(np.absolute(data)):
        if np.absolute(val) >= max_compare/4:
            beginning = idx
            break

    if PLOT:
        plt.plot(data.real[beginning:])
        plt.plot(data.imag[beginning:])
        plt.show()

    return beginning


def extract_binary(data, start, end, T, PLOT=True, title="Sample"):
    binary = []
    raw = []
    offset = T//8
    for val in data[(start+offset):(end+offset):T]:
        if val > 0:
            binary.append( 1 ) 
        else:
            binary.append( 0 )

        raw.append(val)

    indicies = range(start+offset, end+offset, T)
    if PLOT:
        plt.plot(data.real)
        plt.plot(data.imag)
        plt.plot(indicies, raw, '.', ms=10)
        plt.show()

    return np.array(binary)


def flip_data_if_needed( data ):

    flip = sum(data[:8]) < 4
    if flip:
        data = 1 - data

    return data


def compare_to_sent(received, sent):
    print( len(received) )
    print( len(sent) )
    print(received)
    print(sent)

    num_errors = np.count_nonzero( received - sent )
    print("Number of Errors: %d" % num_errors)
    print("Percent Error: %.2f%%" % (num_errors/len(sent) * 100) )


if __name__ == "__main__":
    # Load data
    raw_data_1 = np.fromfile("../data/received_1_trimmed.bin", dtype=np.complex64)
    raw_data_2 = np.fromfile("../data/received_2_trimmed.bin", dtype=np.complex64)

    true_data_1 = np.load("../data/data_1.npy")
    true_data_2 = np.load("../data/data_2.npy")

    U = np.matrix(np.load("../data/U_approx.npy"))
    E = np.load("../data/E_approx.npy")

    # Apply U (technically U.H)
    data_1, data_2 = apply_U(raw_data_1, raw_data_2, U, PLOT=False)

    # Correct for frequency & phase offset
    freq_off_1, phase_off_1 = find_offsets_bpsk(data_1, PLOT=True)
    freq_off_2, phase_off_2 = find_offsets_bpsk(data_2, PLOT=True)

    # Apply offsets
    data_1 = apply_offsets(data_1, freq_off_1, phase_off_1, PLOT=False)
    data_2 = apply_offsets(data_2, freq_off_2, phase_off_2, PLOT=False)

    # Apply PLL
    data_1 = data_1 / np.std(data_1)
    data_2 = data_2 / np.std(data_2)

    kp = 0.3
    ki = 0.05
    kd = 0.0

    pll = PLL.PLL(data_1, kp, ki, kd)
    pll.correct_phase_offset()
    data_1 *= np.exp( -pll.phase_list * j ) * j

    pll = PLL.PLL(data_2, kp, ki, kd)
    pll.correct_phase_offset()
    data_2 *= np.exp( -pll.phase_list * j ) * j

    ## Compare to actual values we sent
    start1 = index_of_first_data(data_1, PLOT=False)
    start2 = index_of_first_data(data_2, PLOT=False)

    end1 = len(data_1) - index_of_first_data(data_1[::-1], PLOT=False)
    end2 = len(data_2) - index_of_first_data(data_2[::-1], PLOT=False)

    bin1 = extract_binary(data_1, start1, end1, 400, PLOT=True)
    bin2 = extract_binary(data_2, start2, end2, 400, PLOT=True)

    bin1 = flip_data_if_needed(bin1)
    bin2 = flip_data_if_needed(bin2)

    compare_to_sent(bin1, true_data_1)
    compare_to_sent(bin2, true_data_2)
    
