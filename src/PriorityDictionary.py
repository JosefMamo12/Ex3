class PriorityDictionary(dict):
    def __init__(self):
        self._heap = []
        dict.__init__(self)

    def smallest(self):
        if len(self) == 0:
            raise IndexError("This Priority Queue is empty")
        heap = self._heap
        while heap[0][1] not in self or self[heap[0][1]] != heap[0][0]:
            last_item = heap.pop()
            insertion_point = 0
            while True:
                small_child = insertion_point*2 + 1
                if small_child + 1 < len(heap) and heap[small_child] > heap[small_child + 1]:
                    small_child += 1
                if small_child >= len(heap) or last_item <= heap[small_child]:
                    heap[insertion_point] = last_item
                    break
                heap[insertion_point] = heap[small_child]
                insertion_point = small_child
        return heap[0][1]