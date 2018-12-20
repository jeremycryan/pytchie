#!/usr/bin/env python

import time
import random as rd
from sound_generation import *
from constants import *
from helpers import *

major_scale = [0, 2, 4, 5, 7, 9, 11]

MAJOR_CHORDS = {
    0: [0, 2, 4, 7],
    1: [0, 2, 4, 5, 9],
    2: [2, 4, 7, 9, 11],
    3: [0, 5, 7, 9],
    4: [2, 7, 9, 11],
    5: [0, 4, 7, 9, 11],
    6: [2, 7, 9, 11]
}

MAJOR_TRIADS = {
    0: [0, 4, 7],
    1: [2, 5, 9],
    2: [4, 9, 11],
    3: [0, 5, 9],
    4: [2, 7, 11],
    5: [0, 4, 9],
    6: [2, 7, 11]
}

BASS_CHORDS = {
    0: [0, 7],
    1: [2, 9],
    2: [4, 11],
    3: [0, 5],
    4: [2, 7],
    5: [4, 9],
    6: [2, 7]

}

n_minor_scale = [0, 2, 3, 5, 7, 8, 10]
h_minor_scale = [0, 2, 3, 5, 7, 8, 11]
p_minor_scale = [0, 3, 5, 7, 10]
blues_scale = [0, 3, 5, 6, 7, 10]
chromatic_scale = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
fifths_scale = [0, 7]

class Rhythm(object):

    def __init__(self, length, fullness = 0.6, intricacy = 0.7, beat_depth = 2, ppb = 2):

        self.length = length # length in beats
        self.fullness = fullness
        self.intricacy = intricacy
        self.beat_depth = beat_depth
        self.ppb = 2
        self.beats = ""

        self.generate()

    def refactor(self, intricacy, fullness, beat_depth):
        self.intricacy = intricacy
        self.fullness = fullness
        self.beat_depth = beat_depth
        self.generate()

    def generate(self):

        beats = ""
        for i in range(self.length):
            beats += self.generate_beat()

        self.beats = beats

    def generate_beat(self):

        res = ""
        if rd.random() < self.intricacy:
            for i in range(self.ppb):
                res += self.generate_subbeat(depth = self.beat_depth - 1)
        else:
            if rd.random() < self.fullness:
                res += ("n%s" % (2**self.beat_depth))
            else:
                res += ("r%s" % (2**self.beat_depth))
        return res

    def generate_subbeat(self, depth = 1):

        num = rd.random()
        if num < self.intricacy and depth >= 1:
            return self.generate_subbeat(depth-1) + self.generate_subbeat(depth-1)
        else:
            if rd.random() < self.fullness:
                return "n%s" % (2**depth)
            else:
                return "r%s" % (2**depth)
        raise
    #
    # def generate_delays(self, mdv_length):
    #
    #     delays = []
    #     beats = self.beats
    #
    #     cur_delay = 0
    #     while len(beats) > 0:
    #         if beats[0] == "r":
    #             cur_delay += float(beats[1])*mdv_length
    #             if len(beats) <= 2:
    #                 break
    #             beats = beats[2:]
    #         elif beats[0] == "n":
    #             delays.append(cur_delay)
    #             cur_delay = 0
    #             cur_delay += float(beats[1])*mdv_length
    #             if len(beats) <= 2:
    #                 break
    #             beats = beats[2:]
    #
    #     return delays






class Riff(object):

    def __init__(self, key = 69,
        scale = major_scale, temerity = 0.8,
        rhythm = None, max_run = 5, max_jump = 5,
        bump_up = None):

        self.key = key
        self.scale = scale
        self.temerity = temerity # Higher makes it stray farther from center note, range 0-1
        self.last_note = key

        self.max_run = max_run
        self.max_jump = max_jump

        self.cur_octave = 0
        self.cur_idx = 0

        self.notes = []

        if rhythm == None:
            self.rhythm = Rhythm(2)
        else:
            self.rhythm = rhythm

        self.bump_up = bump_up
        self.generate()

    def add_note(self, note):
        self.notes.append(note)

    def return_to_origin(self):

        distance_to_root = abs(self.last_note - self.key)
        chance_to_return = 1 - (self.temerity ** distance_to_root)

        if rd.random() < chance_to_return:
            return True
        else:
            return False

    def jump(self):
        """ Jumps a random interval up or down """

        max_interval = self.max_jump
        interval = rd.choice(range(0, max_interval + 1))
        direction = rd.choice([-1, 1])

        if self.return_to_origin():
            if self.cur_octave == 0:
                direction = -1
            else:
                direction = -(self.cur_octave / abs(self.cur_octave))

        for i in range(interval):

            self.cur_idx += direction

            if self.cur_idx < 0:
                self.cur_idx = len(self.scale) - 1
                self.cur_octave -= 1

            if self.cur_idx == len(self.scale):
                self.cur_idx = 0
                self.cur_octave += 1

        new_note = self.key + 12*self.cur_octave + self.scale[int(self.cur_idx)]
        self.last_note = new_note
        self.add_note(new_note)

    def run(self, max_distance = 5):
        """ Runs within a scale for a random distance"""

        max_distance = self.max_run
        distance = rd.choice(range(1, max_distance+1))
        direction = rd.choice([-1, 1])

        if self.return_to_origin():
            if self.cur_octave == 0:
                direction = -1
            else:
                direction = -(self.cur_octave / abs(self.cur_octave))

        for i in range(distance):

            self.cur_idx += direction

            if self.cur_idx < 0:
                self.cur_idx = len(self.scale) - 1
                self.cur_octave -= 1

            if self.cur_idx == len(self.scale):
                self.cur_idx = 0
                self.cur_octave += 1

            new_note = self.key + 12*self.cur_octave + self.scale[int(self.cur_idx)]
            self.last_note = new_note
            self.add_note(new_note)


    def generate(self):

        if self.bump_up:
            for note in self.bump_up.notes:
                key = self.key
                chord = self.scale
                chord_width = len(chord)
                overwide = 0
                if note in chord:
                    new_idx = (chord.index(note) + 2) % chord_width
                    if chord.index(note) >= chord_width:
                        overwide = 1
                    self.cur_octave += 1
                else:
                    new_idx = rd.choice(range(chord_width))
                new_note = chord[new_idx]
                self.last_note = new_note
                self.add_note(new_note+self.key + 12*self.cur_octave)
                if overwide:
                    self.cur_octave -= 1
            return


        while len(self.notes) < 15:
            if rd.random() < 0.2:
                self.run()
            else:
                self.jump()


    def add_to_sample(self, sample, voice, time_offset, mdv_length = 0.1):

        t = time_offset
        #delays = self.rhythm.generate_delays(0.1) * 5
        beats = self.rhythm.beats
        r_idx = 0

        for i, tone in enumerate(self.notes):
            if len(beats) <= 1:
                break
            while beats[0] == "r":
                t += int(beats[1]) * mdv_length
                beats = beats[2:]
                if len(beats) <= 1:
                    break
            if len(beats) <= 1:
                break
            if beats[0] == "n":
                freq = midi_to_freq(tone)
                sound = voice.generate_tone(freq)
                sample.add_tone(sound, t)
                beats = beats[2:]
                if len(beats) <= 1:
                    break
                t += int(beats[1]) * mdv_length


class Song(object):

    def __init__(self, length, bpm, lead_intricacy = 0.7, lead_temerity = 0.7,
        bass_intricacy = 0.3, bass_temerity = 0.3, chords = ["RAND"]*4,
        snare_intricacy = 0.5):

        self.sinewave = SineWave()
        self.sawtooth = SawWave()
        self.flute = Flute()
        self.trumpet = Trumpet()
        self.violin = Violin()
        self.noise = Noise()
        self.square = SquareWave()
        self.instruments = [self.flute, self.trumpet, self.violin, self.noise]

        self.label_to_instrument = {"FLUTE": self.flute,
            "TRUMPET": self.trumpet,
            "VIOLIN": self.violin,
            "SNARE": self.noise,
            "RANDOM": rd.choice(self.instruments)}

        self.chord_to_idx = {"I": 0, "ii": 1, "iii": 2,
            "IV": 3, "V": 4, "vi": 5, "vii": 6,
            "RAND": rd.choice(range(7))}

        self.set_tempo(bpm)
        mrt = self.mdv_length/0.15

        self.instrument_envelopes = {self.violin: Envelope(0.1, 0.15*mrt, 0.1*mrt, 0.1*mrt, 0.5),
            self.flute: Envelope(0.07, 0.15*mrt, 0.15*mrt, 0.1*mrt, 0.4),
            self.trumpet: Envelope(0.05, 0.15*mrt, 0.1*mrt, 0.1*mrt, 0.5),
            self.noise: Envelope(0.05, 0.07, 0.06, 0.1*mrt, 0.2)}

        self.length = length

        self.key = rd.choice(range(12)) + 60
        self.changes = [self.chord_to_idx[chord] for chord in chords]
        #self.changes[0] = rd.choice([0, 3, 5])
        self.bars_per_chord = 2
        self.double_time = self.mdv_length*4*4*self.bars_per_chord * len(self.changes)
        self.sample = Sample(self.length*self.double_time+0.5)

        self.lead_intricacy = lead_intricacy
        self.lead_temerity = lead_temerity

        self.bass_intricacy = bass_intricacy
        self.bass_temerity = bass_temerity

        self.snare_intricacy = snare_intricacy


    def bassline(self, t_init = 0):
        bass_envelope = Envelope(0.05, 0.15, 0.2, 0.15, 0.2)
        voice = rd.choice([self.sawtooth, self.square])
        bass = Voice(bass_envelope, voice, volume = 0.2)
        bass_rhythms = [Rhythm(self.bars_per_chord*2, intricacy = self.bass_intricacy, fullness = 1)]
        bass_riffs = [Riff(scale = BASS_CHORDS[chord],
            rhythm=rd.choice(bass_rhythms), key=self.key-12*3,
            temerity = self.bass_temerity, max_run = 1) for chord in self.changes]

        for chord in bass_riffs*2:
            chord.add_to_sample(self.sample, bass, t_init, mdv_length = self.mdv_length)
            t_init += self.mdv_length * 4 * len(self.changes)

    def snare_line(self, t_init = 0):
        snare_envelope = Envelope(0.02, 0.05, 0.1, 0.05, 0.1)
        snare = Voice(snare_envelope, self.noise, volume = 2.0)

        snare_rhythm = Rhythm(self.bars_per_chord*2, intricacy = self.snare_intricacy)
        snare_riff = Riff(rhythm=snare_rhythm)

        t = t_init
        for chord in self.changes*2:
            snare_riff.add_to_sample(self.sample, snare, t, mdv_length = self.mdv_length)
            t += self.mdv_length * 4 * len(self.changes)

    def lead_line(self, t_init=0, seed=[None]*4):

        #   Choose a random voice; if seeded, instead choose seed
        if seed[0]:
            lead_instrument = seed[0]
        else:
            lead_instrument = rd.choice(self.instruments)


        #   Choose envelope based on synthesized instrument, and generate voice
        lead_envelope = self.instrument_envelopes[lead_instrument]
        lead = Voice(lead_envelope, lead_instrument, volume = 0.5)

        #   Generate possible measure-long rhythms for lead line.
        #   TODO randomize number of rhythms in lead_rhythms
        rhythm_0 = Rhythm(self.bars_per_chord*2, intricacy = self.lead_intricacy)
        rhythm_1 = Rhythm(self.bars_per_chord*2, intricacy = self.lead_intricacy)

        if seed[1]:
            lead_rhythms = seed[1]
        else:
            lead_rhythms = [rhythm_0, rhythm_1]

        if seed[1]:
            played_rhythms = seed[1]
        else:
            lead_rhythms = [rhythm_0, rhythm_1]
            played_rhythms = [rd.choice(lead_rhythms) for i in range(len(self.changes))]

        #   Generate an array of riffs for the chord cahnges with given rhythms.
        if seed[2]:
            lead_riffs = seed[2]
        elif seed[3]:
            lead_riffs = [Riff(scale = MAJOR_CHORDS[self.changes[i]],
                rhythm=played_rhythms[i],
                bump_up=seed[3][i],
                temerity = self.lead_temerity, key=self.key, max_run=3, max_jump=3) for i in range(len(self.changes))]
        else:
            lead_riffs = [Riff(scale = MAJOR_CHORDS[self.changes[i]],
                rhythm=played_rhythms[i],
                temerity = self.lead_temerity, key=self.key, max_run=3, max_jump=3) for i in range(len(self.changes))]

        t = t_init
        for riff in lead_riffs*2:
            riff.add_to_sample(self.sample, lead, t, mdv_length = self.mdv_length)
            t += self.mdv_length * 4 * len(self.changes)

        seed = [lead_instrument, played_rhythms, lead_riffs, None]
        return seed



    def comping(self, t_init=0, seed = [None,]*5):

        if seed[4]:
            brass_rhythm = seed[4]
        else:
            brass_rhythm = Rhythm(self.bars_per_chord*2, intricacy = 0)

        #   Instantiate
        brass_envelope = Envelope(0.15, 0.2, self.bars_per_chord*6*self.mdv_length, 0.1, 0.3)
        short_brass_envelope = Envelope(0.05, 0.1, 0.1, 0.05, 0.3)
        long_brass = Voice(brass_envelope, self.trumpet, volume = 0.3)
        short_brass = Voice(short_brass_envelope, self.trumpet, volume = 0.5)
        long_strings = Voice(brass_envelope, self.violin, volume = 0.3)

        mode = rd.choice(["LONG", "SHORT", "STRINGS"])
        if seed[0]:
            mode = seed[0]
        if mode == "LONG":
            chord_voice = long_brass
        elif mode == "SHORT":
            chord_voice = short_brass
        elif mode == "STRINGS":
            chord_voice = long_strings

        if seed[2]:
            brass_notes = seed[2]
        else:
            brass_notes = [[chord_voice.generate_tone(midi_to_freq(self.key-12+i)) for i in MAJOR_TRIADS[chord]] for chord in self.changes]

        if mode == "SHORT":
            brass_beats = [0.5, 1, 2, 4]
        else:
            brass_beats = [4]

        t = 0
        i = 0
        lengths = []
        while i < len(self.changes)*2:
            if t >= (i+1)*self.mdv_length*4*len(self.changes):
                t = (i+1)*self.mdv_length*4*len(self.changes)
                i += 1
                continue
            for note in brass_notes[i%len(self.changes)]:
                self.sample.add_tone(note, t+t_init)
            if seed[3]:
                length = seed[3][0]
                seed[3] = seed[3][1:]
            else:
                length = rd.choice(brass_beats)
            lengths += [length]
            t += self.mdv_length * length * len(self.changes)

        seed = [mode, chord_voice, brass_notes, lengths, brass_rhythm]
        return seed

    def set_tempo(self, bpm):

        mpb = 1.0/bpm   #   minutes per beat
        spb = mpb*60    #   seconds per beat
        spqb = spb/4    #   seconds per quarter beat

        self.mdv_length = spqb

    def draw_loading_bar(self, surf):
        pass

    def generate_preset_0(self, lead_instrument=None, played_rhythms=None, lead_riffs=None, surf = None, enables=[1, 1, 1, 1], comp_instrument = None):

        now = time.time()

        if enables[0]:
            ls = self.lead_line(t_init=0, seed = [lead_instrument, played_rhythms, lead_riffs, None])
        if enables[1]:
            ss = self.snare_line(t_init=0)
        if enables[2]:
            bs = self.bassline(t_init=0)
        if enables[3]:
            cs = self.comping(t_init=0, seed = [None, comp_instrument, None, None, None])

        for i in range(self.length-1):

            if enables[0]:
                reseed = False
                if rd.random() <= 0.4:
                    reseed = True
                    ls = [lead_instrument, None, None, None]
                ls = self.lead_line(t_init=self.double_time*(i+1), seed = ls)

                while ls[0] == self.noise:
                    ls[0] = rd.choice(self.instruments)

                if rd.random() < 0.6 and not reseed:
                    self.lead_line(t_init=self.double_time*(i+1), seed = ls[:-2] + [None] + [ls[2]])

            if enables[1]:
                self.snare_line(t_init=self.double_time*(i+1))
            if enables[2]:
                self.bassline(t_init=self.double_time*(i+1))
            if enables[3]:
                self.comping(t_init=self.double_time*(i+1), seed=[None, comp_instrument, None, None, None])


        self.sample.write_to_file("test.wav")

        #print('Sample "test.wav" had been generated.')
        #print("Time to generate: %s" % (time.time() - now))




if __name__ == '__main__':
    a = Song(2)
    a.generate_preset_0()
    os.system("aplay test.wav")
