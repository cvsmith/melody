import miditoaudio
from mingus.containers import *
from mingus.containers.instrument import MidiInstrument
from mingus.midi.midi_file_out import write_Composition, write_Track
from music_config import * 
import random
import wave

TEST_DATA = [ [0, {"r": [], "b": [], "g": []}] , [1, {"r": [8], "b": [], "g": []}] , [2, {"r": [8], "b": [], "g": []}] , [3, {"r": [8], "b": [], "g": []}] , [4, {"r": [8], "b": [], "g": [16]}] , [5, {"r": [8], "b": [], "g": [16]}] , [6, {"r": [8], "b": [12], "g": [16, 18]}] , [7, {"r": [8], "b": [13], "g": [16, 18]}] , [8, {"r": [8], "b": [], "g": [17]}] , [9, {"r": [8], "b": [], "g": [17]}] , [10, {"r": [8], "b": [], "g": []}] , [11, {"r": [8], "b": [10], "g": [15]}] , [12, {"r": [], "b": [10], "g": [15]}] , [13, {"r": [3], "b": [10], "g": [16, 7, 14]}] , [14, {"r": [3], "b": [11], "g": [16, 17, 8, 14]}] , [15, {"r": [3], "b": [12], "g": [8, 17]}] , [16, {"r": [3], "b": [13], "g": [8]}] , [17, {"r": [3], "b": [14], "g": [8]}] , [18, {"r": [3], "b": [14], "g": []}] , [19, {"r": [3], "b": [14], "g": []}] , [20, {"r": [3], "b": [10], "g": []}] , [21, {"r": [3], "b": [10], "g": [16]}] , [22, {"r": [7], "b": [10], "g": [16]}] , [23, {"r": [7], "b": [11], "g": [16, 17]}] , [24, {"r": [7], "b": [11, 12], "g": [15]}] , [25, {"r": [8], "b": [13], "g": [16]}] , [26, {"r": [8], "b": [13], "g": [16]}] , [27, {"r": [7], "b": [14], "g": []}] , [28, {"r": [5], "b": [14], "g": []}] , [29, {"r": [4], "b": [11], "g": [9]}] , [30, {"r": [4], "b": [11], "g": [9, 7]}] , [31, {"r": [4], "b": [12], "g": [16, 8]}] , [32, {"r": [4], "b": [], "g": [16]}] , [33, {"r": [10], "b": [], "g": [16]}] , [34, {"r": [10], "b": [13], "g": [16]}] , [35, {"r": [5], "b": [14], "g": [17]}] , [36, {"r": [4], "b": [15], "g": [8]}] , [37, {"r": [4], "b": [15], "g": [9]}] , [38, {"r": [4], "b": [12], "g": [9]}] , [39, {"r": [], "b": [12], "g": []}] , [40, {"r": [5], "b": [12], "g": []}] , [41, {"r": [9, 5], "b": [12], "g": []}] , [42, {"r": [], "b": [13], "g": []}] , [43, {"r": [], "b": [13], "g": [3]}] , [44, {"r": [], "b": [14], "g": [3, 5]}] , [45, {"r": [7], "b": [], "g": [3, 5]}] , [46, {"r": [8], "b": [], "g": []}] , [47, {"r": [], "b": [], "g": []}] ]

# Write MIDI file corresponding to music data, return path to 
def write_midi_file(data):
    tracks = make_tracks(data)
    for i in xrange(len(tracks)):
        write_Track('track%s.mid' % i, tracks[i], 180)
    

# Return mingus composition object from data
def make_tracks(data):
    r_track = Track(Instrument())
    r_track.instrument.instrument_nr = COLOR_INSTR_NRS['r']
    r_bar = Bar(key='C', meter=METER)
    r_bar.is_empty = True
    g_track = Track(Instrument())
    g_track.instrument.instrument_nr = COLOR_INSTR_NRS['g']
    g_bar = Bar(key='C', meter=METER)
    g_bar.is_empty = True
    b_track = Track(Instrument())
    b_track.instrument.instrument_nr = COLOR_INSTR_NRS['b']
    b_bar = Bar(key='C', meter=METER)
    b_bar.is_empty = True
    track_colors = {'r': r_track, 'g': g_track, 'b': b_track}
    bar_colors = {'r': r_bar, 'g': g_bar, 'b': b_bar}

    for moment in data:
        (time, colors) = moment
        for color, tones in colors.iteritems():
            if tones == []:
                bar = bar_colors[color]
                if bar.is_empty:
                    bar.place_rest(FIRST_REST_LENGTH)
                else:
                    bar.place_rest(REST_LENGTH)
            else:
                notes = note_container.NoteContainer()
                for tone in tones:
                    notes += ALL_NOTES[tone]
                bar.place_notes(notes, BEAT_LENGTH)
                bar.is_empty = False
            # TODO: If last note == current note, increase duration of 1st note
    for color in ('r', 'g', 'b'):
        track_colors[color].add_bar(bar_colors[color])

    return (r_track, b_track, g_track)

# Merge wave files
def merge_wave_files(infiles, outfile):
    data= []
    for infile in infiles:
        w = wave.open(infile, 'rb')
        data.append( [w.getparams(), w.readframes(w.getnframes())] )
        w.close()

    output = wave.open(outfile, 'wb')
    output.setparams(data[0][0])
    output.writeframes(data[0][1])
    output.writeframes(data[1][1])
    output.close()
    
write_midi_file(TEST_DATA)
merge_wave_files(['track0.mid', 'track1.mid', 'track2.mid'])