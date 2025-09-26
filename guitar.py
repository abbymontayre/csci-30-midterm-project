#!/usr/bin/env python3

from guitarstring import GuitarString
from stdaudio import play_sample
import stdkeys

if __name__ == '__main__':
    # initialize window
    stdkeys.create_window()

    # Create GuitarString objects and key mapping in one integrated structure
    # 1.059463 is the 12th root of 2 (equal temperament tuning)
    keys = ['q', '2', 'w', 'e', '4', 'r', '5', 't', 'y', '7', 'u', '8', 'i', '9', 'o', 'p', '-', '[', '=', ']']
    notes = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A2', 'A2#', 'B2', 'C2', 'C2#', 'D2', 'D2#', 'E2']
    
    # Create GuitarString objects and key mapping
    GuitarStrings = [GuitarString(220 * (1.059463**i)) for i in range(20)]
    key_to_string = dict(zip(keys, range(20)))
    
    # List to track only the strings that have been plucked
    active_strings = []

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
                string = GuitarStrings[key_to_string[key]]
                string.pluck()
                # Add to active strings if not already there
                if string not in active_strings:
                    active_strings.append(string)

        # compute the superposition of samples from active strings only
        sample = sum(string.sample() for string in active_strings)
        
        # prevents overflow and chooses between prioritizing volumee or preventing overflow
        if len(active_strings) > 0:
            # Use the larger of: division by active strings, or fixed 0.3 scaling
            dynamic_scale = 1.0 / len(active_strings)
            fixed_scale = 0.3
            sample = sample * max(dynamic_scale, fixed_scale)
       
        # play the sample on standard audio
        play_sample(sample)

        #takes care of removing strings that are quiet
        i = 0
        while i < len(active_strings):
            string = active_strings[i]
            string.tick()
            # Remove string from active list if it's quiet enough
            if abs(string.sample()) < 1e-10:
                active_strings.pop(i)
            else:
                i += 1
