#!/usr/bin/env python


""" Class that reads in received data from a specified file, and plots
and decodes the data. """


import numpy as np
import matplotlib.pyplot as plt


j = (0 + 1j)


class Decoder(object):

    def __init__(self, data_path, received_data_filename_1,
            received_data_filename_2, U_matrix):

        self.data_path = data_path
        self.received_data_filename_1 = received_data_filename_1
        self.received_data_filename_2 = received_data_filename_2
        self.data_raw_1 = None
        self.data_raw_2 = None
        self.frequency_offset = None
        self.phase_offset = None
        self.data_fixed_1 = None
        self.data_fixed_2 = None

        self.samples = None

        self.U_matrix = U_matrix


    def read_file(self):

        file_path_1 = self.data_path + self.received_data_filename_1
        file_path_2 = self.data_path + self.received_data_filename_2
        self.data_raw_1 = np.fromfile(file_path_1, dtype=np.complex64)
        self.data_raw_2 = np.fromfile(file_path_2, dtype=np.complex64)
        self.data_fixed_1 = self.data_raw_1
        self.data_fixed_2 = self.data_raw_2


    def find_offsets_bpsk(self):

        # Take the normalized data
        normalized_data = self.data_raw / np.linalg.norm(self.data_raw)
        squared_data = np.square( normalized_data )

        # Take FFT of the square of the normalized data
        fft_data = np.fft.fft( squared_data )
        fft_shape = np.fft.fftfreq( squared_data.shape[-1] )

        # Find the index of the maximum amplitude peak
        max_index = np.absolute(fft_data).argmax()

        # Extract frequency and phase offsets from the peak
        self.frequency_offset = ( fft_shape[max_index]/2 ) * (2 * np.pi)
        self.phase_offset = np.sqrt(fft_data[max_index])

        print(self.frequency_offset, self.phase_offset)


    def fix_offsets(self):

        data_fixed = np.zeros(len(self.data_raw), dtype=np.complex64)
        for i, val in enumerate(self.data_raw):
            data_fixed[i] = val * np.exp(-j * self.frequency_offset * i) / \
                    self.phase_offset

        self.data_fixed = np.array(data_fixed, dtype=np.complex64)


    def plot_data(self):

        plt.figure()
        plt.subplot(2, 1, 1)
        plt.plot(self.data_raw_1.real, label='real')
        plt.plot(self.data_raw_1.imag, label='imag')
        plt.title('Received Raw 1')
        plt.legend()
        plt.subplot(2, 1, 2)
        plt.plot(self.data_fixed_1.real, label='real')
        plt.plot(self.data_fixed_1.imag, label='imag')
        plt.title('Received Fixed 1')
        plt.legend()

        plt.figure()
        plt.subplot(2, 1, 1)
        plt.plot(self.data_raw_2.real, label='real')
        plt.plot(self.data_raw_2.imag, label='imag')
        plt.title('Received Raw 2')
        plt.legend()
        plt.subplot(2, 1, 2)
        plt.plot(self.data_fixed_2.real, label='real')
        plt.plot(self.data_fixed_2.imag, label='imag')
        plt.title('Received Fixed 2')
        plt.legend()
        plt.show()

    
    def sample_data(self, T):

        oldval = None
        start_index = None
        for i, val in enumerate(self.data_fixed):
            if i == 0:
                oldval = val
                continue

            if (val - oldval) > 0.0025:
                start_index = i
                break

        samples = []
        for i in range(i, len(self.data_fixed), T):
            data = self.data_fixed[i].real

            if data > 0:
                samples.append(1)
            else:
                samples.append(0)

        self.samples = np.array(samples[:36])

    
    def is_data_correct(self):

        true_data = np.loadtxt('data_in_binary.txt')

        errors = true_data - self.samples
        print( np.count_nonzero(errors) )


    def apply_U(self):
        
        # Multiply by respective V-vector value for MIMO
        for i in range(len(self.data_fixed_1)):
            data_vector = np.matrix([[self.data_fixed_1[i]],
                    [self.data_fixed_2[i]]])
            result = self.U_matrix * data_vector

            self.data_fixed_1[i] = result[0]
            self.data_fixed_2[i] = result[1]


if __name__ == "__main__":

    data_path = '../data/'
    received_data_filename_1 = 'received_1_trimmed.bin'
    received_data_filename_2 = 'received_2_trimmed.bin'
    U_matrix = np.matrix.getH(np.matrix(np.load(data_path + 'U_approx.npy')))

    decoder = Decoder(data_path, received_data_filename_1,
            received_data_filename_2, U_matrix)
    decoder.read_file()
    # decoder.find_offsets_bpsk()
    # decoder.fix_offsets()
    decoder.apply_U()
    decoder.plot_data()

    # samples = decoder.sample_data(200)
    # decoder.is_data_correct()
