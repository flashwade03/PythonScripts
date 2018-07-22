import sys, os, queue

class BFS:

    dx = [0, 1, 0, -1]
    dy = [-1, 0, 1, 0]

    q = None
    visited = None

    def __init__(self):
        self.q = queue.Queue()
        visited = []

    def find_positions_with_condition(self, condition, target_m, start_y, start_x):
        ret = []
        target_width = len(target_m[0])
        target_height = len(target_m)
        self.visited = [[0]*target_width for i in range(target_height)]

        self.visited[start_y][start_x] = 1
        self.q.put([start_y, start_x])
        ret.append([start_y, start_x])
        
        while True:
            if self.q.qsize() == 0:
                break
            
            element = self.q.get()
            cur_y = element[0]
            cur_x = element[1]

            for index in range(0, 4):
                next_y = cur_y + self.dy[index]
                next_x = cur_x + self.dx[index]
                
                if next_y >= 0 and next_y < target_height and next_x >= 0 and next_x < target_width and self.visited[next_y][next_x] == 0 and target_m[next_y][next_x] == condition:
                    self.q.put([next_y, next_x])
                    self.visited[next_y][next_x] = 1
                    ret.append([next_y, next_x])

        return ret
            

