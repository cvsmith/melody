from mingus.containers import Bar, Composition, Note, NoteContainer, Track
from mingus.containers.instrument import MidiInstrument
from mingus.midi.midi_file_out import write_Composition
import copy

comp = Composition()
t1 = Track(instrument=MidiInstrument(name='Acoustic Grand Piano'))
t2 = Track(instrument=MidiInstrument(name='Violin'))
t3 = Track(instrument=MidiInstrument(name='Clarinet'))

tracks = [t1, t2, t3]

beat = 0
notes = NoteContainer(['C-4', 'E-4', 'G-4', 'C-5'])

for track in tracks:
    bar = Bar(key='C', meter=(4, 4))
    bar.length = 16
    bar.current_beat = beat
    print bar.current_beat
    print track
    bar.place_notes(notes[beat], 1)
    track.add_bar(bar)
    print track
    beat += 1

for t in tracks:
    comp.add_track(t)

print comp
write_Composition('test_composition.midi', comp, 480)



    