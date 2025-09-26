#!/usr/bin/env python3

from guitarstring import GuitarString
from stdaudio import play_sample
import stdkeys

if __name__ == '__main__':
    # initialize window
    stdkeys.create_window()

    # Define frequencies for the notes
    CONCERT_A = 220
    CONCERT_A_SHARP = CONCERT_A * (1.059463**1)
    CONCERT_B = CONCERT_A * (1.059463**2)
    CONCERT_C = CONCERT_A * (1.059463**3)
    CONCERT_C_SHARP = CONCERT_A * (1.059463**4)
    CONCERT_D = CONCERT_A * (1.059463**5)
    CONCERT_D_SHARP = CONCERT_A * (1.059463**6)
    CONCERT_E = CONCERT_A * (1.059463**7)
    CONCERT_F = CONCERT_A * (1.059463**8)
    CONCERT_F_SHARP = CONCERT_A * (1.059463**9)
    CONCERT_G = CONCERT_A * (1.059463**10)
    CONCERT_G_SHARP = CONCERT_A * (1.059463**11)
    CONCERT_A2 = CONCERT_A * (1.059463**12)
    CONCERT_A2_SHARP = CONCERT_A * (1.059463**13)
    CONCERT_B2 = CONCERT_A * (1.059463**14)
    CONCERT_C2 = CONCERT_A * (1.059463**15)
    CONCERT_C2_SHARP = CONCERT_A * (1.059463**16)
    CONCERT_D2 = CONCERT_A * (1.059463**17)
    CONCERT_D2_SHARP = CONCERT_A * (1.059463**18)
    CONCERT_E2 = CONCERT_A * (1.059463**19)

    # Create GuitarString objects for each note
    GuitarStrings = [GuitarString(CONCERT_A), GuitarString(CONCERT_A_SHARP), GuitarString(CONCERT_B),
                     GuitarString(CONCERT_C), GuitarString(CONCERT_C_SHARP), GuitarString(CONCERT_D),
                     GuitarString(CONCERT_D_SHARP), GuitarString(CONCERT_E), GuitarString(CONCERT_F),
                     GuitarString(CONCERT_F_SHARP), GuitarString(CONCERT_G), GuitarString(CONCERT_G_SHARP),
                     GuitarString(CONCERT_A2), GuitarString(CONCERT_A2_SHARP), GuitarString(CONCERT_B2),
                     GuitarString(CONCERT_C2), GuitarString(CONCERT_C2_SHARP), GuitarString(CONCERT_D2),
                     GuitarString(CONCERT_D2_SHARP), GuitarString(CONCERT_E2)]  

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
            if key == 'q':
                GuitarStrings[0].pluck()
            elif key == '2':
                GuitarStrings[1].pluck()
            elif key == 'w':
                GuitarStrings[2].pluck()
            elif key == 'e':
                GuitarStrings[3].pluck()
            elif key == '4':
                GuitarStrings[4].pluck()
            elif key == 'r':
                GuitarStrings[5].pluck()
            elif key == '5':
                GuitarStrings[6].pluck()
            elif key == 't':
                GuitarStrings[7].pluck()
            elif key == 'y':
                GuitarStrings[8].pluck()
            elif key == '7':
                GuitarStrings[9].pluck()
            elif key == 'u':
                GuitarStrings[10].pluck()
            elif key == '8':
                GuitarStrings[11].pluck()
            elif key == 'i':
                GuitarStrings[12].pluck()
            elif key == '9':
                GuitarStrings[13].pluck()
            elif key == 'o':
                GuitarStrings[14].pluck()
            elif key == 'p':
                GuitarStrings[15].pluck()
            elif key == '-':
                GuitarStrings[16].pluck()
            elif key == '[':
                GuitarStrings[17].pluck()
            elif key == '=':
                GuitarStrings[18].pluck()
            elif key == ']':
                GuitarStrings[19].pluck()

        # compute the superposition of samples, only for audible strings
        threshold = 1e-4
        sample = sum(
            string.sample() for string in GuitarStrings
            if abs(string.sample()) > threshold
        )
        
        # Prevent overflow by clipping the sample to valid audio range
        sample = max(-1.0, min(1.0, sample))

        # play the sample on standard audio
        play_sample(sample)

        # advance the simulation of each guitar string by one step
        for string in GuitarStrings:
            string.tick()
