import sys, os, random 
from bfs import BFS

class MAP:

    dx = [-1, 0, 1, -1, 0, 1, -1, 0, 1]
    dy = [-1, -1, -1, 0, 0, 0, 1, 1, 1]

    mine_position = None
    display_map_data = None
    internal_map_data = None

    width = 0
    height = 0
    total_mine_count = 0
    remain_tiles = 0

    bfs = None

    def __init__(self):
        print 'Initialize MAP object'
        self.bfs = BFS()

    def create_map(self, w, h, mc = 0):
        
        self.mine_position = []
        self.width = w
        self.height = h
        
        if mc == 0:
            if self.width == 9:
                self.total_mine_count = 10
            elif self.width == 16:
                self.total_mine_count = 40
            elif self.width == 30:
                self.total_mine_count = 99
        else:
            self.mine_count = mc

        self.remain_tiles = (self.height * self.width) - self.total_mine_count
        self.display_map_data = [['*']*self.width for i in range(self.height)]
        self.internal_map_data = [[0]*self.width for i in range(self.height)]
        
        finish = False
        made_mine_count = 0

        while not finish:

            x = random.randrange(0, self.width)
            y = random.randrange(0, self.height)

            #check duplication mine position
            if self.internal_map_data[y][x] == -1:
                continue                
            
            self.mine_position.append([y, x])
            self.internal_map_data[y][x] = -1
            made_mine_count += 1

            if made_mine_count == self.total_mine_count:
                finish = True
        
        for mine in self.mine_position:
            for index in range(0, 8):
                nextY = mine[0] + self.dy[index]
                nextX = mine[1] + self.dx[index]
                if nextY >= 0 and nextY < self.height and nextX >=0 and nextX < self.width and self.internal_map_data[nextY][nextX] != -1:
                    self.internal_map_data[nextY][nextX] += 1

    def check_mine(self, input_y, input_x):
        if self.internal_map_data[input_y][input_x] == -1:
            return True
        else:
            return False

    def is_possible_choose(self, input_y, input_x):
        if input_y < 0 or input_x >= self.height or input_x < 0 or input_x >= self.height:
            return False

        if self.display_map_data[input_y][input_x] == '*':
            return True
        else:
            return False

    def choose_tile(self, input_y, input_x):
        if input_y >= 0 and input_y < self.height and input_x >=0 and input_x < self.width and self.check_mine(input_y, input_x) == False and self.is_possible_choose(input_y, input_x) == True:
            if self.internal_map_data[input_y][input_x] == 0:
                zeros = self.bfs.find_positions_with_condition(0, self.internal_map_data, input_y, input_x)
                for z in zeros:
                    self.display_map_data[z[0]][z[1]] = str(0)
                    for index in range(0, 8):
                        nx = z[1] + self.dx[index]
                        ny = z[0] + self.dy[index]
                        if nx >= 0 and nx < self.width and ny >=0 and ny < self.height and self.display_map_data[ny][nx] == '*' and self.internal_map_data[ny][nx] != -1 :
                            self.display_map_data[ny][nx] = str(self.internal_map_data[ny][nx])
                            self.remain_tiles -= 1
                self.remain_tiles -= len(zeros)
            else:
                self.display_map_data[input_y][input_x] = str(self.internal_map_data[input_y][input_x])
                self.remain_tiles -= 1
            
    
    def print_internal_map(self):
        for height in range(0, self.height):
            print self.internal_map_data[height]
    
    def did_find_all_mines(self):
        if self.remain_tiles == 0:
            return True
        else:
            return False

    def print_display_map(self):
        for height in range(0, self.height):
            print self.display_map_data[height]
                

