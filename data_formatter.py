#!/usr/bin/env python


""" Class that reads in raw data from a specified file, formats it as
specified and writes it to a new file. """


import numpy as np


class DataFormatter(object):

    def __init__(self, input_filename, output_filename, amplitude,
            pulse, T, start_sequence=[], stop_sequence=[],
            filler_sequence=[]):
        """ Initialize the data formatter. """

        self.input_filename = input_filename
        self.output_filename = output_filename
        self.amplitude = amplitude
        self.pulse = pulse
        self.T = T
        self.start_sequence = start_sequence
        self.stop_sequence = stop_sequence
        self.filler_sequence = filler_sequence
        self.data = None


    def read_data(self):
        """ Reads data from specified input_filename. """

        # Create readable file descriptor from specified input filename
        input_file = open(self.input_filename, 'r')

        # Store input file contents as string
        input_string = input_file.read()

        # Split input_string into a list of ints
        self.data = map(int, list(input_string)[:-1])


    def generate_data(self, data_length=1000):
        """ Generates random binary data with a specified length. """
        
        # Generate array of random binary
        data = np.random.randint(2, size=data_length)
        
        # Store data as member variable 
        self.data = data
        

    def format_data(self):
        """ Reformat data to output_filename. """

        # Initialize the formatted data
        formatted_data = np.array([], dtype=np.complex64)

        # Concatenate the start and stop sequences to self.data
        self.data = np.concatenate( (self.start_sequence, self.data, self.stop_sequence) ) * self.amplitude

        # Widen by T
        self.widen = np.zeros(len(self.data) * self.T)
        for index, value in enumerate(self.widen):
            if index % self.T == 0:
                self.widen[index] = self.data[ index/self.T ]

        # Convert self.data to a numpy array
        self.data = np.array(self.widen, dtype=np.complex64)

        # Final data
        formatted_data = np.convolve(self.data, self.pulse)
        formatted_data = np.array(formatted_data, dtype=np.complex64)

        # Print final formatted_data
        print( formatted_data )
        print( len(formatted_data) )

        # Write formatted_data to output_file
        output_file = open(self.output_filename, 'wb')
        output_file.write(formatted_data.tobytes())
            

if __name__ == '__main__':

    # Define parameters for data formatting
    input_filename = 'raw_data.bin'
    output_filename = 'formatted_data.bin'
    amplitude = 5.0 # Voltage scaling
    #pulse = np.array([0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0]) # Shape, currently a box
    pulse = np.ones(100)
    T = 200
    start_sequence = [1, 1, 1, 1, 1, 1, 1, 1] # Goes at beginning of data
    stop_sequence = [-1, -1, -1, -1, -1, -1, -1, -1] # Goes at end of data
    filler_sequence = [0] # Goes between each pulse of data

    # Make DataFormatter object
    data_formatter = DataFormatter(input_filename, output_filename, amplitude,
                pulse_width, start_sequence, stop_sequence, filler_sequence)
    data_formatter.generate_data()
    data_formatter.format_data()