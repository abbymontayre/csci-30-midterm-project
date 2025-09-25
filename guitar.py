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

    #Create string_status (active = true; inactive = false) to match with GuitarStrings
    string_active = [False] * len(GuitarStrings)

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
                string_active[0] = True
            elif key == '2':
                GuitarStrings[1].pluck()
                string_active[1] = True
            elif key == 'w':
                GuitarStrings[2].pluck()
                string_active[2] = True
            elif key == 'e':
                GuitarStrings[3].pluck()
                string_active[3] = True
            elif key == '4':
                GuitarStrings[4].pluck()
                string_active[4] = True
            elif key == 'r':
                GuitarStrings[5].pluck()
                string_active[5] = True
            elif key == '5':
                GuitarStrings[6].pluck()
                string_active[6] = True
            elif key == 't':
                GuitarStrings[7].pluck()
                string_active[7] = True
            elif key == 'y':
                GuitarStrings[8].pluck()
                string_active[8] = True
            elif key == '7':
                GuitarStrings[9].pluck()
                string_active[9] = True
            elif key == 'u':
                GuitarStrings[10].pluck()
                string_active[10] = True
            elif key == '8':
                GuitarStrings[11].pluck()
                string_active[11] = True
            elif key == 'i':
                GuitarStrings[12].pluck()
                string_active[12] = True
            elif key == '9':
                GuitarStrings[13].pluck()
                string_active[13] = True
            elif key == 'o':
                GuitarStrings[14].pluck()
                string_active[14] = True
            elif key == 'p':
                GuitarStrings[15].pluck()
                string_active[15] = True
            elif key == '-':
                GuitarStrings[16].pluck()
                string_active[16] = True
            elif key == '[':
                GuitarStrings[17].pluck()
                string_active[17] = True
            elif key == '=':
                GuitarStrings[18].pluck()
                string_active[18] = True
            elif key == ']':
                GuitarStrings[19].pluck()
                string_active[19] = True

        # compute the superposition of samples, only for audible strings
        threshold = 1e-4
        sample = 0.0

        for x in range(len(GuitarStrings)):
            if string_active[x]:
                sample += GuitarStrings[x].sample()

            # advance the simulation of each active guitar string by one step
            GuitarStrings[x].tick()

            if abs(GuitarStrings[x].sample()) < threshold:
                string_active[x] = False

        # play the sample on standard audio
        play_sample(sample)