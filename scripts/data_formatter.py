#!/usr/bin/env python


""" Class that reads in raw data from a specified file, formats it as
specified and writes it to a new file. """


import numpy as np


class DataFormatter(object):

    def __init__(self, output_filename, amplitude,
            pulse, T, start_sequence=[], stop_sequence=[]):
        """ Initialize the data formatter. """

        self.output_filename = output_filename
        self.amplitude = amplitude
        self.pulse = pulse
        self.T = T
        self.start_sequence = np.array(start_sequence)
        self.stop_sequence = np.array(stop_sequence)
        self.data = None
        self.formatted_data = None


    def generate_data(self, data_length=20):
        """ Generates random binary data with a specified length. """
        
        # Generate array of random binary
        np.random.seed(10)
        data = np.array(np.random.choice([1, 0], size=data_length))

        # Store data
        self.data = np.concatenate( [self.start_sequence, data,
                self.stop_sequence] )

        np.savetxt("data_in_binary.txt", self.data)
        

    def format_data(self):
        """ Reformat data to output_filename. """

        # Initialize the formatted data
        self.formatted_data = np.array([], dtype=np.complex64)
    
        # Change 0s to -1s
        self.data[ self.data==0 ] = -1

        # Scale
        self.data = self.amplitude * self.data

        # Widen by T
        self.widen = np.zeros(len(self.data) * self.T, dtype=np.complex64)
        for index, value in enumerate(self.widen):
            if index % self.T == 0:
                self.widen[index] = self.data[ index//self.T ]

        # Convolve impulses with pulse shape
        self.formatted_data = np.convolve(self.widen, self.pulse)
        self.formatted_data = np.array(self.formatted_data, dtype=np.complex64)

        # Write formatted_data to output_file
        output_file = open(self.output_filename, 'wb')
        output_file.write(self.formatted_data.tobytes())
        output_file.close()


    def visualize_data(self):
        import matplotlib.pyplot as plt
        print(self.formatted_data)
        plt.plot(self.formatted_data.real, label="Real")
        plt.plot(self.formatted_data.imag, label="Imaginary")
        plt.legend()
        #plt.scatter(self.formatted_data.real, self.formatted_data.imag, s=2)
        plt.show()
            

if __name__ == '__main__':

    # Define parameters for data formatting
    output_filename = 'formatted_data.bin'
    amplitude = 0.5 # Voltage scaling
    pulse = np.ones(100)
    T = 400
    start_sequence = [1, 1, 1, 1, 1, 1, 1, 1] # Goes at beginning of data
    stop_sequence =  [0, 0, 0, 0, 0, 0, 0, 0] # Goes at end of data

    # Make DataFormatter object
    data_formatter = DataFormatter(output_filename, amplitude,
                pulse, T, start_sequence, stop_sequence)
    data_formatter.generate_data()
    data_formatter.format_data()
    data_formatter.visualize_data()
    
