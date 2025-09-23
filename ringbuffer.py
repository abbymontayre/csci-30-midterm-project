class RingBuffer:
    def __init__(self, capacity: int):
        # create an empty ring buffer, with given max capacity
        self._capacity = capacity
        self._buffer = [None] * capacity
        self._size = 0
        self._front = 0
        self._rear = 0
    def size(self) -> int:
        # return number of items currently in the buffer
        return self._size
    def is_empty(self) -> bool:
        # is the buffer empty (size equals zero)?
        return self._size == 0
    def is_full(self) -> bool:
        # is the buffer full (size equals capacity)?
        return self._size == self._capacity
    def enqueue(self, x: float):
        # add item x to the end
        self._buffer[self._rear] = x
        self._rear = (self._rear + 1) % self._capacity # divide by capacity to wrap around
        self._size += 1
    def dequeue(self) -> float:
        # return and remove item from the front
        item = self._buffer[self._front]
        self._front = (self._front + 1)% self._capacity
        self._size -= 1
        return item
    def peek(self) -> float:
        # return (but do not delete) item from the front
        return self._buffer[self._front]