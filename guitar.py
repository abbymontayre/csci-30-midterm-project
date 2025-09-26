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
    
    # List to track only the strings that have been plucked
    active_strings = []

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
                string_index = key_to_string[key]
                string = GuitarStrings[string_index]
                string.pluck()
                # Add to active strings if not already there
                if string not in active_strings:
                    active_strings.append(string)

        # compute the superposition of samples from active strings only
        sample = sum(string.sample() for string in active_strings)
        
        # Always apply consistent scaling to prevent overflow and maintain volume consistency
        sample = sample * 0.5
        # play the sample on standard audio
        play_sample(sample)

        # advance the simulation only for active strings and remove quiet ones
        strings_to_remove = []
        for string in active_strings:
            string.tick()
            # Remove string from active list if it's quiet enough (much lower threshold)
            if abs(string.sample()) < 1e-10:
                strings_to_remove.append(string)
        
        # Remove quiet strings from active list
        for string in strings_to_remove:
            active_strings.remove(string)
