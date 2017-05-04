#!/usr/bin/env python


""" Class that reads in raw data from a specified file, formats it as
specified and writes it to a new file. """


import numpy as np


class DataFormatter(object):

    def __init__(self, data_path, V_matrix, amplitude,
            pulse, T, seed, start_sequence=[], stop_sequence=[]):
        """ Initialize the data formatter. """

        self.data_path = data_path
        self.V_matrix = V_matrix
        self.amplitude = amplitude
        self.pulse = pulse
        self.T = T
        self.start_sequence = np.array(start_sequence)
        self.stop_sequence = np.array(stop_sequence)
        self.seed = seed
        self.data1 = None
        self.data2 = None
        self.transmit_data1 = None
        self.transmit_data2 = None


    def generate_data(self, data_length=100):
        """ Generates random binary data with a specified length. """
        
        # Generate array of random binary
        np.random.seed(self.seed)
        data1 = np.array(np.random.choice([1, 0], size=data_length))
        data2 = np.array(np.random.choice([1, 0], size=data_length))

        # Store data
        self.data1 = np.concatenate( [self.start_sequence, data1,
                self.stop_sequence] )

        self.data2 = np.concatenate( [self.start_sequence, data2,
                self.stop_sequence] )

        np.save("../data/data_1", self.data1)
        np.save("../data/data_2", self.data2)
        

    def format_data(self):
        """ Reformat data to output_filename. """

        # Initialize the formatted data
        self.transmit_data1 = np.array([], dtype=np.complex64)
        self.transmit_data2 = np.array([], dtype=np.complex64)
    
        # Change 0s to -1s
        self.data1[ self.data1==0 ] = -1
        self.data2[ self.data2==0 ] = -1

        # Scale
        self.data1 = self.amplitude * self.data1
        self.data2 = self.amplitude * self.data2

        # Widen by T
        self.widen1 = np.zeros(len(self.data1) * self.T, dtype=np.complex64)
        for index, value in enumerate(self.widen1):
            if index % self.T == 0:
                self.widen1[index] = self.data1[ index//self.T ]

        self.widen2 = np.zeros(len(self.data2) * self.T, dtype=np.complex64)
        for index, value in enumerate(self.widen2):
            if index % self.T == 0:
                self.widen2[index] = self.data2[ index//self.T ]

        # Convolve impulses with pulse shape
        self.transmit_data1 = np.convolve(self.widen1, self.pulse)
        self.transmit_data1 = np.array(self.transmit_data1, dtype=np.complex64)

        self.transmit_data2 = np.convolve(self.widen2, self.pulse)
        self.transmit_data2 = np.array(self.transmit_data2, dtype=np.complex64)

        # Multiply by respective V-vector value for MIMO
        for i, val in enumerate(self.transmit_data1):
            vec = np.matrix( [ [val], [self.transmit_data2[i]] ] )
            out = self.V_matrix * vec

            self.transmit_data1[i] = out[0]
            self.transmit_data2[i] = out[1]

        # Write formatted_data to output_file
        self.transmit_data1.tofile(self.data_path + 'send_1.bin')
        self.transmit_data2.tofile(self.data_path + 'send_2.bin')


    def visualize_data(self):
        import matplotlib.pyplot as plt
        plt.plot(self.transmit_data1.real, label="Real")
        plt.plot(self.transmit_data1.imag, label="Imaginary")
        plt.legend()
        plt.title("data 1")

        plt.figure()
        plt.plot(self.transmit_data2.real, label="Real")
        plt.plot(self.transmit_data2.imag, label="Imaginary")
        plt.legend()
        plt.title("data 2")

        plt.show()
            

if __name__ == '__main__':

    # Define parameters for data formatting
    data_path = '../data/'
    amplitude = 0.5 # Voltage scaling
    pulse = np.ones(100) # TODO: Change to a raised cosine
    T = 400
    start_sequence = [1, 1, 1, 1, 1, 1, 1, 1] # Goes at beginning of data
    stop_sequence =  [0, 0, 0, 0, 0, 0, 0, 0] # Goes at end of data

    #V_matrix = np.matrix( "1, 0; 0, 1")
    V_matrix = np.matrix(np.load("../data/V_H_approx.npy")) # TODO: Need to update once we have the SVD values

    # Make DataFormatter object
    data_formatter = DataFormatter(data_path, V_matrix, amplitude,
                pulse, T, 10, start_sequence, stop_sequence)
    data_formatter.generate_data()
    data_formatter.format_data()
    data_formatter.visualize_data()
    
