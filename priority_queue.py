from heapq import *

# https://docs.python.org/2/library/heapq.html#priority-queue-implementation-notes

class PriorityQueue:	
	def __init__(self):
		self.heap = []                         # list of entries arranged in a heap
		self.entry_finder = {}               # mapping of tasks to entries

	def add_update(self, task, priority):
	    if task in self.entry_finder:
	        self.remove(task)

	    entry = [priority, task]
	    self.entry_finder[task] = entry
	    heappush(self.heap, entry)

	def remove(self, task):
	    entry = self.entry_finder.pop(task)
	    entry[-1] = None

	def pop(self):
	    while self.heap:
	        priority, task = heappop(self.heap)
	        if task is not None:
	            del self.entry_finder[task]
	            return task
	    raise KeyError('pop from an empty priority queue')

	def __contains__(self, item):
		return item in self.entry_finder

	def empty(self):
		return len(self.heap) == 0

