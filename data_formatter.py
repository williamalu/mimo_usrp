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
        self.start_sequence = start_sequence
        self.stop_sequence = stop_sequence
        self.data = None


    def generate_data(self, data_length=1000):
        """ Generates random binary data with a specified length. """
        
        # Generate array of random binary
        np.random.seed(10)
        data = np.random.choice([1, -1], size=data_length)
        
        # Store data as member variable 
        self.data = data
        

    def format_data(self):
        """ Reformat data to output_filename. """

        # Initialize the formatted data
        formatted_data = np.array([], dtype=np.complex64)

        # Concatenate the start and stop sequences to self.data
        self.data = self.amplitude * np.concatenate( (self.start_sequence,
                                                      self.data, 
                                                      self.stop_sequence) )

        # Widen by T
        self.widen = np.zeros(len(self.data) * self.T)
        for index, value in enumerate(self.widen):
            if index % self.T == 0:
                self.widen[index] = self.data[ index//self.T ]

        # Convolve impulses with pulse shape
        formatted_data = np.convolve(self.widen, self.pulse)
        formatted_data = np.array(formatted_data, dtype=np.complex64)

        # Write formatted_data to output_file
        output_file = open(self.output_filename, 'wb')
        output_file.write(formatted_data.tobytes())
            

if __name__ == '__main__':

    # Define parameters for data formatting
    output_filename = 'formatted_data.bin'
    amplitude = 5.0 # Voltage scaling
    pulse = np.ones(100)
    T = 200
    start_sequence = [1, 1, 1, 1, 1, 1, 1, 1] # Goes at beginning of data
    stop_sequence = [-1, -1, -1, -1, -1, -1, -1, -1] # Goes at end of data

    # Make DataFormatter object
    data_formatter = DataFormatter(output_filename, amplitude,
                pulse, T, start_sequence, stop_sequence)
    data_formatter.generate_data()
    data_formatter.format_data()
    
