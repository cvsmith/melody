import miditoaudio
from mingus.containers import *
from mingus.containers.instrument import MidiInstrument
from mingus.midi.midi_file_out import write_Composition
from music_config import * 
import random

TEST_DATA = [
    (0.0, 
        {
            'r': [0.4, 0.1],
            'g': [0.02],
            'b': [0.88],
        }
    ),
    (0.5,
        {
            'r': [0.7],
            'g': [],
            'b': [0.28, 0.5, 0.9]
        }
    ),
    (0.9,
        {
            'r': [0.5],
            'g': [0.9],
            'b': [0.85]
        }
    )
]

# Write MIDI file corresponding to music data, return path to 
def write_midi_file(data, filename):
    comp = make_composition(data)

# Return mingus composition object from data
def make_composition(data):
    comp = Composition()
    for moment in data:
        (time, tones) = moment


comp = Composition()
t1 = Track(Instrument())
t1.instrument.instrument_nr = COLOR_INSTR_NRS['r']
t2 = Track(Instrument())
t2.instrument.instrument_nr = COLOR_INSTR_NRS['g']
t3 = Track(Instrument())
t3.instrument.instrument_nr = COLOR_INSTR_NRS['b']

for track in [t1, t2, t3]:
    bar = Bar(key='C', meter=METER)
    for i in xrange(int(bar.length) * 4):
        note = random.choice(ALL_NOTES+[None])
        bar.place_notes(note, METER[1])
    track.add_bar(bar)
    comp.add_track(track)

print comp

write_Composition('test_composition.mid', comp, 180)
    