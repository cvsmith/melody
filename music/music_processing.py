import miditoaudio
from mingus.containers import *
from mingus.containers.instrument import MidiInstrument
from mingus.midi.midi_file_out import write_Composition, write_Track
from music_config import * 
from pydub import AudioSegment
import random
import sys
import wave

TEST_DATA = [
[0, {"r": [], "b": [], "g": []}] ,
[1, {"r": [], "b": [], "g": []}] ,
[2, {"r": [], "b": [18, 13], "g": [4]}] ,
[3, {"r": [], "b": [18, 13], "g": [4]}] ,
[4, {"r": [], "b": [18, 13], "g": [4]}] ,
[5, {"r": [], "b": [13], "g": [4]}] ,
[6, {"r": [8, 11], "b": [16, 13], "g": [4, 5]}] ,
[7, {"r": [8, 11], "b": [16, 13], "g": []}] ,
[8, {"r": [], "b": [13], "g": []}] ,
[9, {"r": [], "b": [], "g": [6]}] ,
[10, {"r": [], "b": [11, 14], "g": [6]}] ,
[11, {"r": [], "b": [11, 14], "g": [6]}] ,
[12, {"r": [], "b": [11], "g": []}] ,
[13, {"r": [9], "b": [11], "g": [5]}] ,
[14, {"r": [9, 12], "b": [18, 11], "g": [5]}] ,
[15, {"r": [9, 12], "b": [18, 11], "g": [5]}] ,
[16, {"r": [], "b": [11], "g": [5]}] ,
[17, {"r": [], "b": [], "g": [5]}] ,
[18, {"r": [], "b": [], "g": []}] ,
[19, {"r": [], "b": [16, 12], "g": []}] ,
[20, {"r": [], "b": [16, 12], "g": [6]}] ,
[21, {"r": [], "b": [12], "g": []}] ,
[22, {"r": [], "b": [12], "g": []}] ,
[23, {"r": [], "b": [12], "g": [5]}] ,
[24, {"r": [10, 7], "b": [16, 12], "g": [5]}] ,
[25, {"r": [10, 7], "b": [16, 12], "g": [5]}] ,
[26, {"r": [], "b": [13], "g": [5]}] ,
[27, {"r": [], "b": [13], "g": [5]}] ,
[28, {"r": [], "b": [], "g": [5]}] ,
[29, {"r": [], "b": [9, 13], "g": [7]}] ,
[30, {"r": [], "b": [9, 13], "g": [7]}] ,
[31, {"r": [], "b": [9], "g": [7]}] ,
[32, {"r": [], "b": [9, 11], "g": []}] ,
[33, {"r": [], "b": [9, 11], "g": [5]}] ,
[34, {"r": [], "b": [9], "g": [5]}] ,
[35, {"r": [10, 14], "b": [16, 9], "g": [5]}] ,
[36, {"r": [14], "b": [16, 9], "g": [5]}] ,
[37, {"r": [], "b": [9, 11], "g": [5]}] ,
[38, {"r": [], "b": [9, 11], "g": [5]}] ,
[39, {"r": [], "b": [], "g": [7]}] ,
[40, {"r": [], "b": [17, 12], "g": [7]}] ,
[41, {"r": [], "b": [17, 12], "g": []}] ,
[42, {"r": [], "b": [12], "g": [5]}] ,
[43, {"r": [], "b": [12], "g": [5]}] ,
[44, {"r": [9, 13], "b": [17, 12], "g": [5]}] ,
[45, {"r": [9, 13], "b": [17, 12], "g": [5]}] ,
[46, {"r": [], "b": [12], "g": [5]}] ,
[47, {"r": [], "b": [], "g": [5]}]
]

# Write MIDI file corresponding to music data, return path to 
def write_midi_files(data):
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
    
write_midi_files(TEST_DATA)
sys.argv = ['', '--sf2-dir', './', '--midi-dir', './']
miditoaudio.main()
merge_wave_files(['track0.wav', 'track1.wav', 'track2.wav'], 'output.wav')

