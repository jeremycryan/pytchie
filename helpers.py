#!/usr/bin/env python
import os
import sys

def midi_to_freq(num):
    """ Takes a MIDI number and returns a frequency in Hz for corresponding note. """
    num_a = num - 69
    freq = 440 * 2**(num_a / 12.0)
    return freq

def fp(relative):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(relative)

if __name__ == '__main__':
    print(midi_to_freq(69))
    print(midi_to_freq(60))
    print(midi_to_freq(105))
