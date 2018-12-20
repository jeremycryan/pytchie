#!/usr/bin/env python

from math import sin, pi
import random as rd
import scipy.io.wavfile as wv
import numpy as np
import os
from constants import *
from helpers import *

################################################################################
# ------------------------ ENVELOPE OBJECT ----------------------------------- #
################################################################################

class Envelope(object):

    def __init__(self, attack, decay, sustain, release, sustain_vol):
        #   The value of each phase is equal to the time, in seconds,
        #   spent in that phase.

        self.attack = attack
        self.decay = decay
        self.sustain = sustain
        self.release = release
        self.sustain_vol = sustain_vol

        self.length = attack + decay + sustain + release

    def copy(self):
        return Envelope(self.attack, self.decay, self.sustain,
            self.release, self.sustain_vol)

    def get_level(self, time):
        #   Returns a level, with maximum volume 1.0, based on adsr envelope.

        time = float(time)
        level = 0
        if time <= self.attack:
            thru = time/self.attack
            level = thru
        elif time <= self.attack + self.decay:
            thru = (time - self.attack)/(self.decay)
            level = 1 - thru*(1 - self.sustain_vol)
        elif time <= self.attack + self.decay + self.sustain:
            level = self.sustain_vol
        elif time <= self.attack + self.decay + self.sustain + self.release:
            thru = (time - self.sustain - self.decay - self.attack)/self.release
            level = (1 - thru)*self.sustain_vol

        return level

################################################################################
# ---------------------------- WAVE OBJECT ----------------------------------- #
################################################################################

class Wave(object):

    def __init__(self):
        self.modulation_amp = 0
        self.modulation_period = 1
        self.through_period = 0
        self.frequency = 0

    def get_level(self, dt):
        #   Returns sample of wave, based on time passed and frequency attribute
        #   Returns a value between -1 and 1

        self.through_period += dt*self.frequency
        level = self.wave_func(self.through_period)
        return level

    def wave_func(self, through_period):

        return 1

class SquareWave(Wave):

    def __init__(self, duty_cycle = 0.5):
        Wave.__init__(self)
        self.duty_cycle = duty_cycle

    def wave_func(self, through_period):
        if through_period%1 < self.duty_cycle:
            return 1
        else:
            return -1

class SawWave(Wave):

    def __init__(self):
        Wave.__init__(self)

    def wave_func(self, through_period):
        thru = through_period % 1
        amp = 1.0 - thru*2
        return amp

class SineWave(Wave):

    def __init__(self):
        Wave.__init__(self)

    def wave_func(self, through_period):
        amp = sin(through_period * 2 * pi)
        return amp

class Noise(Wave):

    def __init__(self):
        Wave.__init__(self)

    def wave_func(self, through_period):
        amp = rd.random() - 0.5
        return amp * 0.3

class Trumpet(Wave):

    def __init__(self):
        Wave.__init__(self)
        self.modulation_amp = 4
        self.modulation_period = 0.12

    def wave_func(self, through_period):
        amt = through_period * 2 * pi

        ot0 = sin(amt)
        ot1 = sin((amt*2)%(2*pi))
        ot2 = sin((amt*3)%(2*pi))
        ot3 = sin((amt*4)%(2*pi))
        ot4 = sin((amt*5)%(2*pi))
        ot5 = sin((amt*6)%(2*pi))
        ot6 = sin((amt*7)%(2*pi))
        ot7 = sin((amt*8)%(2*pi))
        ot8 = sin((amt*9)%(2*pi))

        return (0.65*ot0 + 0.4*ot1 + 0.45*ot2 + ot3 + 0.35*ot4 + 0.65*ot5 + 0.25*ot6 + 0.1*ot7 + 0.05*ot8)*0.5

class Flute(Wave):

    def __init__(self):
        Wave.__init__(self)
        self.modulation_amp = 10
        self.modulation_period = 0.12

    def wave_func(self, through_period):
        amt = through_period * 2 * pi

        ot0 = sin(amt)
        ot1 = sin((amt*2)%(2*pi))
        ot2 = sin((amt*3)%(2*pi))
        ot3 = sin((amt*4)%(2*pi))
        ot4 = sin((amt*5)%(2*pi))
        ot5 = sin((amt*6)%(2*pi))
        ot6 = sin((amt*7)%(2*pi))
        ot7 = sin((amt*8)%(2*pi))

        return (1.0*ot0 + 1.0*ot1 + 0.15*ot2 + 0.25*ot3 + 0.2*ot4 + 0.04*ot5 + 0.03*ot6 + 0.02*ot7)

class Violin(Wave):

    def __init__(self):
        Wave.__init__(self)
        self.modulation_amp = 7
        self.modulation_period = 0.15

    def wave_func(self, through_period):
        amt = through_period * 2 * pi

        ot0 = sin(amt)
        ot1 = sin((amt*2)%(2*pi))
        ot2 = sin((amt*3)%(2*pi))
        ot3 = sin((amt*4)%(2*pi))
        ot4 = sin((amt*5)%(2*pi))
        ot5 = sin((amt*6)%(2*pi))
        ot6 = sin((amt*7)%(2*pi))
        ot7 = sin((amt*8)%(2*pi))

        return (1.0*ot0 + 0.6*ot1 + 0.6*ot2 + 0.7*ot3 + 0.5*ot4 + 0.25*ot5 + 0.5*ot6 + 0.2*ot7)


################################################################################
# --------------------------- VOICE OBJECT ----------------------------------- #
################################################################################

class Voice(object):

    def __init__(self, envelope, wave, volume = 1.0):
        self.envelope = envelope
        self.wave = wave
        self.freq_to_tone = {}
        self.volume = volume

    def generate_tone(self, frequency):

        vibrato_amp = self.wave.modulation_amp
        vibrato_per = self.wave.modulation_period

        #   Don't generate if you already have in this voice
        if frequency in self.freq_to_tone:
            return self.freq_to_tone[frequency]

        self.wave.frequency = frequency
        samples = []
        length = self.envelope.length
        num_samples = int(length * SAMPLE_RATE)
        sample_time = 1.0/SAMPLE_RATE


        for i in range(num_samples):
            t = i * sample_time
            self.wave.frequency = frequency + vibrato_amp * sin(2*pi/vibrato_per*t)
            wave_amp = self.wave.get_level(sample_time)
            env_amp = self.envelope.get_level(t)
            samples.append(wave_amp*env_amp*self.volume)

        #samples = np.asarray(samples).astype(np.float32)

        self.freq_to_tone[frequency] = samples

        return samples

################################################################################
# ---------------------------- SAMPLE OBJECT --------------------------------- #
################################################################################

class Sample(object):
    # This class pretty much just adds up a bunch of tones into one big playable
    # list

    def __init__(self, length):
        self.length = length

        self.data = [0] * int(1.0 * length * SAMPLE_RATE + 1)

    def add_tone(self, tone, time):

        start_idx = int(1.0*time*SAMPLE_RATE)
        cur_idx = 0

        for sample in tone:

            if cur_idx + start_idx >= len(self.data):
                break

            self.data[cur_idx + start_idx] += sample

            cur_idx += 1

    def get_data_as_array(self):
        maximum = max([abs(i) for i in self.data])
        self.data = [i*1.0/maximum for i in self.data]

        return np.asarray(self.data).astype(np.float32)

    def write_to_file(self, filename):
        data = self.get_data_as_array()
        wv.write(fp(os.path.join("output", filename)), SAMPLE_RATE, data)


if __name__ == '__main__':
    env_0 = Envelope(0.05, 0.1, 0.10, 0.2, 0.1)
    sinewave = SineWave()
    a = Voice(env_0, sinewave)
    b = Sample(2)
    sound = a.generate_tone(220)
    b.add_tone(sound, 1)
    sound2 = a.generate_tone(440)
    b.add_tone(sound2, 1.2)
    sound3 = a.generate_tone(880)
    b.add_tone(sound3, 1.4)
    b.write_to_file("test.wav")
    os.system("aplay test.wav")
