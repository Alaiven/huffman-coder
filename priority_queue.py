""" Priority queue module"""

import heapq

class PriorityQueue(object):
    """ Heap based priority queue """

    def __init__(self):
        self.items = []

    def push(self, priority, elem):
        """ pushes element """
        heapq.heappush(self.items, (priority, elem))

    def pop(self):
        """ pops element """
        _, elem = heapq.heappop(self.items)
        return elem

    def empty(self):
        """ checks if queue is empty"""
        return not self.items
