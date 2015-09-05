from mingus.containers import *
from mingus.containers.instrument import MidiInstrument
from mingus.midi.midi_file_out import write_Composition


comp = Composition()
t1 = Track(Instrument())
t1.instrument = MidiInstrument(name='Acoustic Grand Piano')
t1.instrument.instrument_nr = 0
t2 = Track(Instrument())
t2.instrument = MidiInstrument(name='Violin')
t2.instrument.instrument_nr = 40
t3 = Track(Instrument())
t3.instrument = MidiInstrument(name='Clarinet')
t3.instrument.instrument_nr = 71


tracks = [t1, t2, t3]

notes = NoteContainer(['C-4', 'E-4', 'G-4', 'C-5'])

bar1 = Bar(key='C', meter=(4, 4))
bar1.length = 4
bar1.current_beat = 0
bar1.place_notes(notes[0], 1)
bar1.current_beat = 3
bar1.place_notes(notes[3], 1)
t1.add_bar(bar1)
bar2 = Bar(key='C', meter=(4, 4))
bar2.length = 4
bar2.current_beat = 0
bar2.place_notes(notes[1], 1)
bar2.current_beat = 3
bar2.place_notes(notes[3], 1)
t2.add_bar(bar2)
bar3 = Bar(key='C', meter=(4, 4))
bar3.length = 4
bar3.current_beat = 2
bar3.place_notes(notes[2], 1)
bar3.current_beat = 3
bar3.place_notes(notes[3], 1)
t3.add_bar(bar3)

for t in tracks:
    comp.add_track(t)

print comp

write_Composition('test_composition.midi', comp, 240)



    