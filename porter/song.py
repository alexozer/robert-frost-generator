#!/usr/bin/env python3

from collections import namedtuple
import random
import mido

Note = namedtuple('Note', ['pitch', 'duration'])
CHORD_CHAIN = [{2, 4, 6}, {0, 2, 4}, {0, 2, 5}, {0, 3, 5}, {1, 3, 5}, {1, 3, 6}, {4, 6, 1}]
EPSILON = 0.001

def note_at(notes, beat_time):
    """ Returns whether a note resides at the given time """
    t = 0
    for n in notes:
        if abs(beat_time - t) < EPSILON:
            return True
        t += n.duration

def gen_notes(chord, max_beats, underlying_notes=None):
    SAME_DURATION_PROB = 0.8
    SAME_DIRECTION_PROB = 0.8

    beats = 0
    notes = []

    while beats < max_beats:
        duration = 2 ** random.randint(-1, 2)
        if len(notes) > 0 and random.random() < SAME_DURATION_PROB:
            duration = notes[-1].duration

        if len(notes) == 0:
            pitch = random.choice(list(chord))
        elif len(notes) > 1 and random.random() < SAME_DIRECTION_PROB:
            pitch = 2 * notes[-1].pitch - notes[-2].pitch
        else:
            pitch = random.randint(0, 7)

        if (underlying_notes is not None and
            random.random() < 0.85 and
            note_at(underlying_notes, beats) and
            len(notes) > 0):

            notes[-1] = Note(notes[-1].pitch, notes[-1].duration + duration)
        else:
            notes.append(Note(pitch, duration))

        beats += duration

    remaining_duration = max_beats - (beats - notes[-1].duration)
    notes = notes[:-1]
    notes.append(Note(0, remaining_duration))

    return notes

def gen_chord_walk(max_beats):
    DIRECTED_PROB = 0.9

    num_choords = len(CHORD_CHAIN)
    chord_idxs = [random.choice(range(num_choords))]
    target_idx = (chord_idxs[0] + (num_choords // 2)) % num_choords
    for i in range(int(max_beats / 4) - 1):
        last_idx = chord_idxs[-1]
        if (target_idx - last_idx) % num_choords < num_choords // 2 and \
                random.random() < DIRECTED_PROB:
            direction = 1
        else:
            direction = -1

        chord_idxs.append((last_idx + direction) % num_choords)

    chord_idxs.extend(list(reversed(chord_idxs)))
    return [CHORD_CHAIN[i] for i in chord_idxs]

def track_of_notes(notes, ticks_per_beat, scale_offset=0, time_offset=0, velocity=64):
    scale_semitones = [0, 2, 4, 5, 7, 9, 11]

    track = mido.MidiTrack()
    for i, note in enumerate(notes):
        midi_pitch = (60 + scale_offset +
                      scale_semitones[note.pitch % len(scale_semitones)] +
                      note.pitch // len(scale_semitones) * 11
                      )
        track.append(mido.Message(
            'note_on',
            note=midi_pitch,
            time=time_offset * ticks_per_beat if i == 0 else 0,
        ))

        midi_duration = int(note.duration * ticks_per_beat)
        track.append(mido.Message('note_off', note=midi_pitch, time=midi_duration))

    return track

def write_song():
    mid = mido.MidiFile(type=1)
    def add_track(notes, time_offset=0, velocity=64):
        mid.tracks.append(track_of_notes(notes, mid.ticks_per_beat, scale_offset, time_offset, velocity))

    def flatten(chunks):
        return [n for chunk in chunks for n in chunk]

    STRIDE = 16

    notes1 = []
    walk = gen_chord_walk(STRIDE)
    for chord in walk:
        notes1.append(gen_notes(chord, 2))

    shift = -5
    shifted_chunks = [[Note((n.pitch + shift) % 8, n.duration) for n in chunk] for chunk in notes1]
    shifted_chords = [{(n + shift) % 8 for n in chord} for chord in walk]

    notes2_flat = []
    for note_chunk, chord in zip(shifted_chunks, shifted_chords):
        notes2_flat.extend(gen_notes(chord, 2, underlying_notes=note_chunk))

    scale_offset = random.randint(0, 11)
    add_track(flatten(notes1) + notes2_flat)
    add_track(flatten(shifted_chunks), time_offset=STRIDE)
    mid.save('song.mid')

if __name__ == '__main__':
    write_song()
