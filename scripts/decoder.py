#!/usr/bin/env python


""" Class that reads in received data from a specified file, and plots
and decodes the data. """


import numpy as np
import matplotlib.pyplot as plt


j = (0 + 1j)


class Decoder(object):

    def __init__(self, data_path, received_data_filename_1,
            received_data_filename_2, U_matrix, E_vector):

        self.data_path = data_path
        self.received_data_filename_1 = received_data_filename_1
        self.received_data_filename_2 = received_data_filename_2
        self.data_raw_1 = None
        self.data_raw_2 = None
        self.frequency_offset_1 = None
        self.phase_offset_1 = None
        self.data_fixed_1 = None
        self.data_fixed_2 = None

        self.U_matrix = U_matrix
        self.E_vector = E_vector


    def read_file(self):

        file_path_1 = self.data_path + self.received_data_filename_1
        self.data_raw_1 = np.fromfile(file_path_1, dtype=np.complex64)
        self.data_fixed_1 = self.data_raw_1

        file_path_2 = self.data_path + self.received_data_filename_2
        self.data_raw_2 = np.fromfile(file_path_2, dtype=np.complex64)
        self.data_fixed_2 = self.data_raw_2


    def find_offsets_bpsk(self):

        # Take the normalized data
        normalized_data_1 = self.data_raw_1 / np.linalg.norm(self.data_raw_1)
        squared_data_1 = np.square( normalized_data_1 )
        # Take FFT of the square of the normalized data
        fft_data_1 = np.fft.fft( squared_data_1 )
        fft_shape_1 = np.fft.fftfreq( squared_data_1.shape[-1] )
        # Find the index of the maximum amplitude peak
        max_index_1 = np.absolute(fft_data_1).argmax()
        # Extract frequency and phase offsets from the peak
        self.frequency_offset_1 = ( fft_shape_1[max_index_1]/2 ) * (2 * np.pi)
        self.phase_offset_1 = np.sqrt(fft_data_1[max_index_1])
        print(self.frequency_offset_1, self.phase_offset_1)

        # Take the normalized data
        normalized_data_2 = self.data_raw_2 / np.linalg.norm(self.data_raw_2)
        squared_data_2 = np.square( normalized_data_2 )
        # Take FFT of the square of the normalized data
        fft_data_2 = np.fft.fft( squared_data_2 )
        fft_shape_2 = np.fft.fftfreq( squared_data_2.shape[-1] )
        # Find the index of the maximum amplitude peak
        max_index_2 = np.absolute(fft_data_2).argmax()
        # Extract frequency and phase offsets from the peak
        self.frequency_offset_2 = ( fft_shape_2[max_index_2]/2 ) * (2 * np.pi)
        self.phase_offset_2 = np.sqrt(fft_data_2[max_index_2])
        print(self.frequency_offset_2, self.phase_offset_2)


    def fix_offsets(self):

        data_fixed_1 = np.zeros(len(self.data_raw_1), dtype=np.complex64)
        for i, val in enumerate(self.data_raw_1):
            data_fixed_1[i] = val * np.exp(-j * self.frequency_offset_1 * i) / \
                    self.phase_offset_1
        self.data_fixed_1 = np.array(data_fixed_1, dtype=np.complex64)

        data_fixed_2 = np.zeros(len(self.data_raw_2), dtype=np.complex64)
        for i, val in enumerate(self.data_raw_2):
            data_fixed_2[i] = val * np.exp(-j * self.frequency_offset_2 * i) / \
                    self.phase_offset_2
        self.data_fixed_2 = np.array(data_fixed_2, dtype=np.complex64)


    def plot_data(self):

        plt.figure()
        plt.subplot(2, 1, 1)
        plt.plot(self.data_raw_1.real, label='real')
        plt.plot(self.data_raw_1.imag, label='imag')
        plt.title('Received Raw 2')
        plt.legend()
        plt.subplot(2, 1, 2)
        plt.plot(self.data_fixed_1.real, label='real')
        plt.plot(self.data_fixed_1.imag, label='imag')
        plt.title('Received Fixed 2')
        plt.legend()

        plt.figure()
        plt.subplot(2, 1, 1)
        plt.plot(self.data_raw_2.real, label='real')
        plt.plot(self.data_raw_2.imag, label='imag')
        plt.title('Received Raw 1')
        plt.legend()
        plt.subplot(2, 1, 2)
        plt.plot(self.data_fixed_2.real, label='real')
        plt.plot(self.data_fixed_2.imag, label='imag')
        plt.title('Received Fixed 1')
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
        
        # Multiply by respective U-matrix value for MIMO
        for i in range(len(self.data_fixed_1)):
            data_vector = np.matrix([[self.data_fixed_1[i]],
                    [self.data_fixed_2[i]]])
            result = self.U_matrix * data_vector
            result 

            self.data_fixed_1[i] = result[0] / self.E_vector[0]
            self.data_fixed_2[i] = result[1] / self.E_vector[1]


    def apply_E(self):
        
        # Multiply by respective U-matrix value for MIMO
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
    E_vector = np.load(data_path + 'E_approx.npy')
    print E_vector

    decoder = Decoder(data_path, received_data_filename_1,
            received_data_filename_2, U_matrix, E_vector)
    decoder.read_file()
    decoder.find_offsets_bpsk()
    decoder.fix_offsets()
    decoder.apply_U()
    # decoder.apply_E()
    decoder.plot_data()

    # samples = decoder.sample_data(200)
    # decoder.is_data_correct()
