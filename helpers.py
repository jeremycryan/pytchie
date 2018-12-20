#!/usr/bin/env python

def midi_to_freq(num):
    """ Takes a MIDI number and returns a frequency in Hz for corresponding note. """
    num_a = num - 69
    freq = 440 * 2**(num_a / 12.0)
    return freq

if __name__ == '__main__':
    print(midi_to_freq(69))
    print(midi_to_freq(60))
    print(midi_to_freq(105))
