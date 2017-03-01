#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile as wav
# import additional packages as needed

def load_wave(filename):
    """Load a wave signal from a specified file.

        This function should return a pair as (rate, x),
        where:

        - rate: the sampling rate
        - x:    a vector that represents a sample sequence.
    """
    return wav.read(filename)
    pass


def find_note_begins(x):
    """Find the beginning index of each chunk.

        This function should return a vector of indices,
        where each index corresponds to the begining of a chunk.
    """
    y=x[:,0].tolist()
    yl=len(y)
    chunk=16384
    i=0
    count=0
    c=[]
    while (count < yl):
        z=y[count:count+chunk]
        m=max(z)
        if m>2000:
            i=z.index(m)
            j=i+count
            c.append(j)
            count=j+chunk
        else:
            count=count+chunk
    return c
    pass

def compute_principal_freq(x, rate, b):
    """Compute the principal frequency of a chunk.

        Arguments:
        - x:        The vector of samples
        - rate:     The sampling rate
        - b:        The begining of a chunk.

        This function returns the principal frequency of a chunk,
        in terms of Hertz.

        Note:
        - You can fix the chunk length to be 16384.
    """

    chunk=16384
    y=x[b:b+chunk,0]
    z=np.fft.fft(y)
    fr=np.fft.fftfreq(len(z),1./rate)
    i=np.argmax(np.abs(z))
    f=abs(fr[i])
    return f

    pass

def analyze_wave(filename):
    """Complete the whole analysis procedure.

        This function returns a tuple comprised of
        three parts:
        - x:            The loaded sequence of samples
        - note_begins:  The beginning index of each chunk
        - note_freqs:   The principal frequency of each chunk
    """

    # Step 1: Load wave from file
    (rate, x) = load_wave(filename)

    # Step 2: find the begining position of each note
    note_begins = find_note_begins(x)

    # Step 3: compute the principal frequency of each note
    note_freqs = [compute_principal_freq(x, rate, b) for b in note_begins]

    # return results
    return x, note_begins, note_freqs


if __name__ == '__main__':
    # main script

    x, note_begins, note_freqs = analyze_wave("cnotes.wav")

    n = len(note_begins)
    assert len(note_freqs) == n

    # display the results
    for i in range(n):
        b = note_begins[i]
        f = note_freqs[i]
        print "Note %2d:  begins at %6d,  freq = %.1f" % (i, b, f)

    # plotting the note beginning positions
    # (please comment out this part if you don't want to see the plots)
    #
    plt.plot(
        range(len(x)), x, 'b-',
        note_begins, x[note_begins], 'r+', markersize=16)
    plt.show()
