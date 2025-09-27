#!/usr/bin/env python3

from guitarstring import GuitarString
from stdaudio import play_sample
import stdkeys

if __name__ == '__main__':
    # initialize window
    stdkeys.create_window()

    keyboard = "q2we4r5ty7u8i9op-[=]"
    GuitarStrings = {keyboard[i]: GuitarString(220 * (1.059463**i)) for i in range(len(keyboard))}
    
    # Set to track only the strings that have been plucked
    active_strings = set()

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
            if key in GuitarStrings:
                string = GuitarStrings[key]
                string.pluck()
                # Add to active strings
                active_strings.add(string)

        # compute the superposition of samples from active strings only
        sample = sum(string.sample() for string in active_strings)
        
        # prevents overflow and chooses between prioritizing volume or preventing overflow
        if len(active_strings) > 0:
            dynamic_scale = 1.0 / len(active_strings)
            fixed_scale = 0.3
            sample = sample * max(dynamic_scale, fixed_scale)
       
        # play the sample on standard audio
        play_sample(sample)
        
        #takes care of removing strings that are quiet
        for string in list(active_strings):
            string.tick()
            if abs(string.sample()) < 1e-10:
                active_strings.discard(string)