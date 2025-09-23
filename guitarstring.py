from ringbuffer import RingBuffer
from math import ceil
import random

SAMP_RATE = 44100
DECAY = 0.996

class GuitarString:
    def __init__(self, frequency: float):
        # create a guitar string of the given frequency, using a sampling rate of 44100 Hz
        self.capacity = ceil(SAMP_RATE / frequency)
        self.buffer = RingBuffer(self.capacity)
        self._ticks = 0  

    @classmethod
    def make_from_array(cls, init: list[int]):
        # create a guitar string whose size and initial values are given by the array `init`
        
        # create GuitarString object with placeholder freq
        stg = cls(1000)  

        stg.capacity = len(init)
        stg.buffer = RingBuffer(stg.capacity)
        for x in init:
            stg.buffer.enqueue(x)
        return stg

    def pluck(self):
        # set the buffer to white noise
        for x in range(self.capacity):
            self.buffer.dequeue()
            self.buffer.enqueue(random.uniform(-0.5, 0.5))

    def tick(self):
        # advance the simulation one time step by applying the Karplus--Strong update
        first = self.buffer.dequeue()
        second = self.buffer.peek()
        new_value = DECAY * 0.5 * (first + second)
        self.buffer.enqueue(new_value)
        self._ticks += 1

    def sample(self) -> float:
        # return the current sample
        return self.buffer.peek()

    def time(self) -> int:
        # return the number of ticks so far
        return self._ticks
