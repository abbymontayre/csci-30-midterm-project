#!/usr/bin/env python3

from guitarstring import GuitarString
from stdaudio import play_sample
import stdkeys

if __name__ == '__main__':
    # initialize window
    stdkeys.create_window()

    # Define frequencies for the notes using chromatic scale
    # 1.059463 is the 12th root of 2 (equal temperament tuning)
    CONCERT_A = 220
    frequencies = [CONCERT_A * (1.059463**i) for i in range(20)]

    # Create GuitarString objects for each note
    GuitarStrings = [GuitarString(freq) for freq in frequencies]  

    # dictionary mapping keys to guitar string indices
    key_to_string = {
        'q': 0,   # A
        '2': 1,   # A#
        'w': 2,   # B
        'e': 3,   # C
        '4': 4,   # C#
        'r': 5,   # D
        '5': 6,   # D#
        't': 7,   # E
        'y': 8,   # F
        '7': 9,   # F#
        'u': 10,  # G
        '8': 11,  # G#
        'i': 12,  # A2
        '9': 13,  # A2#
        'o': 14,  # B2
        'p': 15,  # C2
        '-': 16,  # C2#
        '[': 17,  # D2
        '=': 18,  # D2#
        ']': 19   # E2
    }

    n_iters = 0
    while True:
        # it turns out that the bottleneck is in polling for key events
        # for every iteration, so we'll do it less often, say every 
        # 1000 or so iterations
        if n_iters == 1000:
            stdkeys.poll()
            n_iters = 0
        n_iters += 1

        # check if the user has typed a key; if so, process it
        if stdkeys.has_next_key_typed():
            key = stdkeys.next_key_typed()
            if key in key_to_string:
                GuitarStrings[key_to_string[key]].pluck()

        # compute the superposition of samples, only for audible strings
        threshold = 1e-4
        sample = sum(
            string.sample() for string in GuitarStrings
            if abs(string.sample()) > threshold
        )
        
        # Simple scaling to prevent overflow
        sample = sample * 0.5

        # play the sample on standard audio
        play_sample(sample)

        # advance the simulation of each guitar string by one step
        for string in GuitarStrings:
            string.tick()
