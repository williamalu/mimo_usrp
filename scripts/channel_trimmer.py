#!/usr/bin/env python

""" Class for creating trimmed received noise files to estimate H
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib

class Trimmer(object):
    data_path = "../data/"

    @staticmethod
    def trim_both(fname, output_name, noise_length=100000, gap=10000, offset=10):
        """ Writes two files that each contain one of the two trimmed blocks
            of received noise

            Parameters
            ----------
            fname : str
                name of the binary file to be trimmed, without file extension
            noise_length : int
                length of the noise block, in number of samples
            gap : int
                length of the gap between noise blocks, in number of samples
            offset : int
                number of samples used to accurately tune finding the blocks
        """

        received = np.fromfile(Trimmer.data_path+fname+".bin",
            dtype=np.complex64)
        rec_length = range(len(received))
        rec_ampl = np.absolute(received)
        noise_ampl = np.amax(rec_ampl[:200000])

        beg1 = np.argmax(rec_ampl>3*noise_ampl)+offset
        end1 = beg1 + noise_length
        beg2 = end1 + gap
        end2 = beg2 + noise_length

        plt.subplot(2,1,1)
        plt.plot(rec_length[beg1-gap:end1+gap], rec_ampl[beg1-gap:end1+gap],
            '.', ms=2, label="received")
        plt.plot(rec_length[beg1:end1], rec_ampl[beg1:end1],
            '.', ms=2, label="first")
        plt.title("FIRST")
        plt.subplot(2,1,2)
        plt.plot(rec_length[beg2-gap:end2+gap], rec_ampl[beg2-gap:end2+gap],
            '.', ms=2, label="received")
        plt.plot(rec_length[beg2:end2], rec_ampl[beg2:end2],
            '.', ms=2, label="second")
        plt.title("SECOND")
        plt.show()

        Trimmer.write_trimmed(output_name, received[beg1:end1], received[beg2:end2])


    @staticmethod
    def write_trimmed(output_name, first, second):
        """ Writes two binary complex64 files

            Parametersc
            ----------
            fname : str
                base name of the file to write
            first : ndarray
                the first complex array to write to a file
            second : ndarray
                the second complex array to write to a file
        """
        output_file = open(Trimmer.data_path+output_name+"1.bin", 'wb')
        output_file.write(first.tobytes())
        output_file.close()
        output_file = open(Trimmer.data_path+output_name+"2.bin", 'wb')
        output_file.write(second.tobytes())
        output_file.close()


if __name__ == "__main__":
    Trimmer.trim_both("recnoise1", output_name="noise_h1", offset=19)
    Trimmer.trim_both("recnoise2", output_name="noise_h2", offset=19)
