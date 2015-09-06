from mingus.containers import *

# NOT major pentatonic, F instead of E
PENT_SCALE = {
    0: "C",
    1: "D",
    2: "F",
    3: "G",
    4: "A"
}

ALL_NOTES = []
for octave in (3, 4, 5, 6):
    for degree in xrange(5):
        ALL_NOTES += [Note(PENT_SCALE[degree], octave)]

COLOR_INSTR_NRS = {
    'r': 0,     # Acoustic Grand Piano
    'g': 40,    # Violin
    'b': 71,    # Clarinet
}

METER = (48, 4) # Beats per bar, duration of beat

REST_LENGTH = 4
FIRST_REST_LENGTH = 12
BEAT_LENGTH = 4
