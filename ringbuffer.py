class RingBuffer:
    def __init__(self, capacity: int):
        self._capacity = capacity
        self._buffer = [None] * capacity
        self._size = 0
        self._front = 0
        self._rear = 0
    # def size(self) -> int:
    #     # return number of items currently in the buffer
    # def is_empty(self) -> bool:
    #     # is the buffer empty (size equals zero)?
    # def is_full(self) -> bool:
    #     # is the buffer full (size equals capacity)?
    # def enqueue(self, x: float):
    #     # insert
    # def dequeue(self) -> float:
    #     # return and remove item from the front
    # def peek(self) -> float:
    #     # return (but do not delete) item from the front