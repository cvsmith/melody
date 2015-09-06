import miditoaudio
from mingus.containers import *
from mingus.containers.instrument import MidiInstrument
from mingus.midi.midi_file_out import write_Composition, write_Track
from music_config import * 
from pydub import AudioSegment
import random
import sys
import wave

# Write MIDI file corresponding to music data, return path to 
def write_midi_files(data):
    tracks = make_tracks(data)
    for i in xrange(len(tracks)):
        write_Track('track%s.mid' % i, tracks[i], 180, repeat=1)
    

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

    for point in data:
        colors = point[1]
        for color, tones in colors.iteritems():
            bar = bar_colors[color]
            if tones == []:
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
    sound1 = AudioSegment.from_file(infiles[0])
    sound2 = AudioSegment.from_file(infiles[1])
    sound3 = AudioSegment.from_file(infiles[2])

    temp = sound1.overlay(sound2)
    final = sound3.overlay(temp)

    final.export(outfile, format='wav')

def main(testData,outfile='output.wav'):
    write_midi_files(testData)
    sys.argv = ['', '--sf2-dir', './', '--midi-dir', './']
    miditoaudio.main()
    merge_wave_files(['track0.wav', 'track1.wav', 'track2.wav'],
                     outfile)

if __name__ == '__main__':
    main([
    [0, {"r": [], "b": [8], "g": []}] ,
    [1, {"r": [], "b": [8], "g": []}] ,
    [2, {"r": [], "b": [8], "g": []}] ,
    [3, {"r": [], "b": [8], "g": []}] ,
    [4, {"r": [], "b": [8], "g": [16]}] ,
    [5, {"r": [], "b": [8], "g": [16]}] ,
    [6, {"r": [12], "b": [8], "g": [16, 18]}] ,
    [7, {"r": [13, 14], "b": [8], "g": [16, 17, 18]}] ,
    [8, {"r": [], "b": [8], "g": [17]}] ,
    [9, {"r": [], "b": [8], "g": [17]}] ,
    [10, {"r": [], "b": [8], "g": []}] ,
    [11, {"r": [10], "b": [8], "g": [15]}] ,
    [12, {"r": [10], "b": [], "g": [15]}] ,
    [13, {"r": [10], "b": [3], "g": [7, 14, 16]}] ,
    [14, {"r": [11], "b": [3], "g": [8, 14, 16, 17]}] ,
    [15, {"r": [12], "b": [3, 4], "g": [8, 7, 17]}] ,
    [16, {"r": [13], "b": [3], "g": [8]}] ,
    [17, {"r": [14], "b": [3], "g": [7]}] ,
    [18, {"r": [14], "b": [3], "g": []}] ,
    [19, {"r": [14], "b": [3], "g": []}] ,
    [20, {"r": [10], "b": [2, 3], "g": []}] ,
    [21, {"r": [10], "b": [3], "g": [16, 15]}] ,
    [22, {"r": [10], "b": [7], "g": [16]}] ,
    [23, {"r": [11], "b": [7], "g": [16]}] ,
    [24, {"r": [12], "b": [7], "g": [15]}] ,
    [25, {"r": [12, 13], "b": [8], "g": [16]}] ,
    [26, {"r": [13, 14], "b": [8, 7], "g": [16]}] ,
    [27, {"r": [14], "b": [5, 7], "g": []}] ,
    [28, {"r": [14], "b": [4, 5], "g": []}] ,
    [29, {"r": [11], "b": [4, 5], "g": [9]}] ,
    [30, {"r": [11], "b": [4], "g": [7, 8, 9]}] ,
    [31, {"r": [12], "b": [4], "g": [8, 16]}] ,
    [32, {"r": [], "b": [4], "g": [16]}] ,
    [33, {"r": [], "b": [10], "g": [16]}] ,
    [34, {"r": [13, 14], "b": [10, 5], "g": [16, 17]}] ,
    [35, {"r": [14, 15], "b": [4, 5], "g": [17]}] ,
    [36, {"r": [15], "b": [4], "g": [8, 9]}] ,
    [37, {"r": [15], "b": [4], "g": [9]}] ,
    [38, {"r": [12], "b": [4], "g": [9]}] ,
    [39, {"r": [12], "b": [5], "g": []}] ,
    [40, {"r": [12], "b": [9, 5], "g": []}] ,
    [41, {"r": [12], "b": [9, 5], "g": []}] ,
    [42, {"r": [13], "b": [6], "g": []}] ,
    [43, {"r": [13], "b": [], "g": [3, 5]}] ,
    [44, {"r": [14], "b": [], "g": [3, 5]}] ,
    [45, {"r": [], "b": [7], "g": [3, 5]}] ,
    [46, {"r": [], "b": [8], "g": []}] ,
    [47, {"r": [], "b": [], "g": []}]
    ])

