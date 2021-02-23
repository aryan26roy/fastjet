from __future__ import absolute_import
import sys

from . import _core
import awkward as ak


class pathfinder:       # wrapper class on python side
    def map(self, obs, dims, start, stop):
        for elem in obs:
            if elem[0] > dims[0] or elem[1] > dims[1]:
                raise ValueError("Obstacle Outside Map")
        if start[0] > dims[0] or start[1] > dims[1] or stop[0] > dims[0] or stop[1] > dims[1]:
            raise ValueError("Start/Stop Outside Map")
        if start in obs or stop in obs:
            raise ValueError("Can't mark obstacles")
        grid = []
        for i in range(dims[0]):
            aee = []
            for j in range(dims[1]):
                if [i, j] in obs:
                    aee.append(0)
                    continue
                if [i, j] == start:
                    aee.append(2)
                    continue
                if [i, j] == stop:
                    aee.append(1)
                    continue
                else:
                    aee.append(4)
            grid.append(aee)
        for elem in grid:
            print(elem)
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0])

    def mapras(self, grid):
        lg = len(grid[0])
        for elem in grid:
            if len(elem) != lg:
                raise ValueError("Dimension Mismatch")
        self.grid = grid        # the map
        self.rows = len(grid)       # metadata of the map
        self.cols = len(grid[0])

    def mark(self, start, stop):        # function to mark the start and stop point on the map
        if start[0] > self.rows or start[1] > self.cols or start[0] > self.rows or start[1] > self.cols:
            raise ValueError("Start/Stop outside the map")
        count = 0
        for elem in self.grid:      # raise exception if there is no start/stop
            if 1 in elem:
                count += 1
            if 2 in elem:
                count += 1
        if count == 2:
            	raise ValueError("Start/Stop already exists")
        if self.grid[start[0]][start[1]] == 0 or self.grid[stop[0]][stop[1]] == 0:
            raise ValueError("Error: Cannot Mark Obstacles")
        for i in range(self.rows):
    	    for j in range(self.cols):
    	        if i == start[0] and j == start[1]:
    		        self.grid[i][j] = 2
    	        if i == stop[0] and j == stop[1]:
    		        self.grid[i][j] = 1
        for elem in self.grid:
            print(elem)

    def delete(self):       # function to delete the start and stop points
        for i in range(self.rows):
            for j in range(self.cols):
                if self.grid[i][j] == 2 or self.grid[i][j] == 1:
                    self.grid[i][j] =4
        print(self.grid)

    def findpath(self, algo):
        count = 0
        for elem in self.grid:      # raise exception if there is no start/stop
            if 1 in elem:
            	count += 1
            if 2 in elem:
            	count += 1
        if count < 2 or count > 2:
            raise ValueError("No Start/Stop")
        if algo == "BFS":
            f = _core.BFS_FIND(self.grid)       # call the BFS algorithm
        if algo == "DFS":
            f = _core.DFS_FIND(self.grid)       # call the DFS algorithm
        if algo == "DJK":
            f = _core.interface(self.grid)     # call the Dijkstra Algorithm
        form1 = list(f.keys())[-1]
        f.pop(form1)
        length1 = f['Length'][0]
        f.pop('Length')
        for key in f:
            f[key] = f[key].astype('int64')
        aa = ak.from_buffers(form1, length1, f)
        return aa
