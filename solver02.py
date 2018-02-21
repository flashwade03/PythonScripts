from progressbar import ProgressBar
import json, os, sys, copy, time, math

tile_map = []
map_height = 0
map_width = 0
min_move = 0
paths = []
start_package_number = 1
start_level_number = 1
end_package_number = 1
end_level_number = 1
PB = None
progress = 0
UNIT = 1
current_UNIT = 1
move_limit = 1

class progress_bar:
    def __init__(self, end):
        self.pb = ProgressBar(end)

    def set_end(self, end):
        if self.pb != NONE:
            del self.pb
        self.pb = ProgressBar(end)

    def set_progress(self, progress):
        self.pb.setProgress(progress)

class DIRECTION :
    NONE = 0
    UP = 1
    DOWN = 2
    RIGHT = 3
    LEFT = 4

class TILETYPE : 
    NORMAL = 0
    FLIP = 1
    BLOCK = 2
    HORIZONTAL = 3
    VERTICAL = 4
    RIGHT = 5
    LEFT = 6
    UP = 7
    DOWN = 8
    WARP = 9
    MAGNETIC = 10

def calc_unit():
    global UNIT
    global move_limit
    total_count = pow(4, move_limit)
    if total_count <= 100:
        UNIT = 100 / total_count
    else:
        UNIT = total_count / 100

def mode_select():
    while True:
        mode = int(input("Select Mode. (single level : 1, multi level : 2, quit : 0)"))
        if mode == 0 or mode == 1 or mode == 2:
            return mode

def key_input(mode):
    global start_package_number
    global start_level_number
    global end_package_number
    global end_level_number
    global move_limit
    while True:
        start_package_number = int(input("Input start package number (-1 : reset input, -2 : go mode select): "))
        if start_package_number == -2:
            return
        elif start_package_number == -1:
            continue
        start_level_number = int(input("Input start level number (-1 : reset input, -2 : go mode select): "))
        if start_level_number == -2:
            return
        elif start_level_number == -1:
            continue
        if mode == 2:
            end_package_number = int(input("Input last package number (-1 : reset input, -2 : go mode select): "))
            if end_package_number == -2:
                return
            elif end_package_number == -1:
                continue
            end_level_number = int(input("Input last level number (-1 : reset input, -2 : go mode select)"))
            if end_level_number == -2:
                return
            elif end_level_number == -1:
                continue
        move_limit = int(input("Input maximun length of paths (default : 100) (-1 : reset input, -2 : go mode select) : "))
        if move_limit == -2:
            return
        elif move_limit == -1:
            continue
        break

def find_path(mode) :
    file_dir = os.environ['Level_Data_Path']
    global tile_map
    data = None
    json_data = None
    global map_height
    global map_width
    global paths
    global move_limit
    global min_move
    global PB

    if mode == 1:
        target_level = str(start_package_number) + "_" + str(start_level_number)
        file_path = file_dir + "/" + target_level + ".txt"
        print 'Target Level : ' + target_level
        print '\n'
        min_move = move_limit
        paths = []
        json_data = open(file_path).read()
        data = json.loads(json_data)
        map_height = data['cellSizey']
        map_width = data['cellSizex']
        tile_map = [[0 for col in range(map_width)] for row in range(map_height)]
        visited_map = [[0 for col in range(map_width)] for row in range(map_height)]
        map_data = data['pieces']
        ball_data = copy.deepcopy(data['balls'])

        for tile in map_data :
            tile_map[tile['y']][tile['x']] = tile['type']
            if tile['type'] == 2 : 
                visited_map[tile['y']][tile['x']] = 1

        for ball in ball_data :
            tile_map[ball['y']][ball['x']] = ball['type']
            visited_map[ball['y']][ball['x']] = 1
            ball['direction'] = DIRECTION.NONE
            ball['ignore_magnetic'] = False
            ball['is_moved'] = False
         
        PB = progress_bar(100)
        calc_unit()
        current_UNIT = 0
        path = []
        DFS(ball_data, visited_map, path)

        PB.set_progress(100)
        if len(paths) > 0 :
            print '\n'
            print 'Minimum Length : ' + str(len(paths[0]))
            print 'Answer Path'
            i = 1
            for p in paths : 
                print 'Path ' + str(i) + ' : '
                print p
                i += 1
        else :
            print "This stage doesn't have any answer!"
            print '\n\n'

    else :
        for package in range(start_package_number, end_package_number + 1) :
            for level in range(start_level_number, 21) :
                current_level = star(package) + "_" + str(level)
                filePath = fileDir + "/" + current_level + ".txt"
                paths = []

def DFS(ball_data, visited_map, path):
    #print 'path : '
    #print path
    #print 'map'
    #for row in tile_map:
    #    print row
    #print 'visited'
    #for row in visited_map:
    #    print row
    #print 'ball'
    #print ball_data
    global paths
    global min_move
    global current_UNIT
    global progress 
    temp_visited_map = copy.deepcopy(visited_map)
    temp_ball_data = copy.deepcopy(ball_data)

    if len(path) > min_move :
        #print 'len(path)'
        #print len(path)
        #print 'min_move'
        #print min_move
        current_UNIT += 1
        if current_UNIT == UNIT:
            progress += 1
            current_UNIT = 0
            PB.set_progress(progress)
        return 

    while True:
        #print 1
        is_move = 0
        for ball in temp_ball_data:
            if is_possible_move(ball, temp_ball_data, temp_visited_map):
        #        print 'is possible move'
                ball = move_ball(ball)
                temp_visited_map[ball['y']][ball['x']] = 1
                if tile_map[ball['y']][ball['x']] != TILETYPE.MAGNETIC:
                    if ball['ignore_magnetic'] == False:
                        if ball['direction'] == DIRECTION.UP:
                            if ball['x'] -1 >= 0 and tile_map[ball['y']][ball['x']-1] == TILETYPE.MAGNETIC:
                                ball['x'] = ball['x']-1
                                ball['direction'] = DIRECTION.NONE
                                ball['ignore_magnetic'] = True
                            elif ball['x'] +1 <= map_width-1 and tile_map[ball['y']][ball['x']+1] == TILETYPE.MAGNETIC:
                                ball['x'] = ball['x']+1
                                ball['direction'] = DIRECTION.NONE
                                ball['ignore_magnetic'] = True
                        elif ball['direction'] == DIRECTION.DOWN:
                            if ball['x']-1>=0 and tile_map[ball['y']][ball['x']-1] == TILETYPE.MAGNETIC:
                                ball['x'] = ball['x']-1
                                ball['direction'] = DIRECTION.NONE
                                ball['ignore_magnetic'] = True
                            elif ball['x']+1 <= map_width -1 and tile_map[ball['y']][ball['x']+1] == TILETYPE.MAGNETIC:
                                ball['x'] = ball['x']+1
                                ball['direction'] = DIRECTION.NONE
                                ball['ignore_magnetic'] = True
                        elif ball['direction'] == DIRECTION.RIGHT:
                            if ball['y']-1 >=0 and tile_map[ball['y']-1][ball['x']] == TILETYPE.MAGNETIC:
                                ball['y'] = ball['y'] -1
                                ball['direction'] = DIRECTION.NONE
                                ball['ignore_magnetic'] = True
                            elif ball['y']+1 <= map_height-1 and tile_map[ball['y']+1][ball['x']] == TILETYPE.MAGNETIC:
                                ball['y'] = ball['y']+1
                                ball['direction'] = DIRECTION.NONE
                                ball['ignore_magnetic'] = True
                        elif ball['direction'] == DIRECTION.LEFT:
                            if ball['y']-1 >=0 and tile_map[ball['y']-1][ball['x']] == TILETYPE.MAGNETIC:
                                ball['y'] = ball['y']-1
                                ball['direction'] = DIRECTION.NONE
                                ball['ignore_magnetic'] = True
                            elif ball['y']+1 <= map_height-1 and tile_map[ball['y']+1][ball['x']] == TILETYPE.MAGNETIC:
                                ball['y'] = ball['y']+1
                                ball['direction'] = DIRECTION.NONE
                                ball['ignore_magnetic'] = True
            else:
                is_move += 1
                ball['direction'] = DIRECTION.NONE
                ball['is_moved'] = True
        
        if is_move == len(temp_ball_data):
            break

    for ball in temp_ball_data:
        if tile_map[ball['y']][ball['x']] != TILETYPE.MAGNETIC:
            if ball['y']-1 >= 0 and tile_map[ball['y']-1][ball['x']] == TILETYPE.MAGNETIC:
                ball['y'] = ball['y'] -1
                ball['direction'] = DIRECTION.NONE
            elif ball['y']+1 <= map_height - 1 and tile_map[ball['y']+1][ball['x']] == TILETYPE.MAGNETIC:
                ball['y'] = ball['y']+1
                ball['direction'] = DIRECTION.NONE
            elif ball['x'] -1 >=0 and tile_map[ball['y']][ball['x']-1] == TILETYPE.MAGNETIC:
                ball['x'] = ball['x']-1
                ball['direction'] = DIRECTION.NONE
            elif ball['x'] + 1 <= map_width -1 and tile_map[ball['y']][ball['x']+1] == TILETYPE.MAGNETIC:
                ball['x'] = ball['x']+1
                ball['direction'] = DIRECTION.NONE

    #for row in temp_visited_map:
    #    print row

    ret = True
    for h in range(0, map_height):
        for l in range(0, map_width):
            if tile_map[h][l] == 0:
                if temp_visited_map[h][l] == 0:
                    ret = False
            elif tile_map[h][l] == TILETYPE.VERTICAL:
                if temp_visited_map[h][l] == 0:
                    ret = False
            elif tile_map[h][l] == TILETYPE.HORIZONTAL:
                if temp_visited_map[h][l] == 0:
                    ret = False

    if ret == True:
        if len(path) > min_move:
            current_UNIT += 1
            if current_UNIT == UNIT:
                progress += 1
                current_UNIT = 0
            PB.set_progress(progress)
            return
        elif len(path) == min_move:
            paths.append(path)
            current_UNIT += 1
            if current_UNIT == UNIT:
                progress += 1
                current_UNIT = 0
            PB.set_progress(progress)
            return
        elif len(path) < min_move:
            min_move = len(path)
            paths = []
            paths.append(path)
            current_UNIT += 1
            if current_UNIT == UNIT:
                progress += 1
                current_UNIT = 0
            PB.set_progress(progress)
            return

    #for ball in temp_ball_data:
    #    print "result ball"
    #    print ball
    temp_path = copy.deepcopy(path)
    b1 = copy.deepcopy(temp_ball_data)
    v1 = copy.deepcopy(temp_visited_map)
    ret = False
    for ball in b1 :
        if is_possible_move_to_direction(ball, b1, v1, DIRECTION.UP):
            ret = True
            break

    if ret:
        for ball in b1 :
            ball['direction'] = DIRECTION.UP
            ball['is_moved'] = False
    #        print "temp ball"
    #        print ball
        temp_path.append("Up")
        DFS(b1, v1, temp_path)

    temp_path = copy.deepcopy(path)
    b2 = copy.deepcopy(temp_ball_data)
    v2 = copy.deepcopy(temp_visited_map)
    ret = False
    for ball in b2:
        if is_possible_move_to_direction(ball, b2, v2, DIRECTION.DOWN):
            ret = True
            break

    if ret:
        for ball in b2 :
            ball['direction'] = DIRECTION.DOWN
            ball['is_moved'] = False
    #        print "tempball"
    #        print ball
        temp_path.append("Down")
        DFS(b2, v2, temp_path)

    temp_path = copy.deepcopy(path)
    b3 = copy.deepcopy(temp_ball_data)
    v3 = copy.deepcopy(temp_visited_map)
    ret = False
    for ball in b3:
        if is_possible_move_to_direction(ball, b3, v3, DIRECTION.RIGHT):
            ret = True
            break
    
    if ret:
        for ball in b3:
            ball['direction'] = DIRECTION.RIGHT
            ball['is_moved'] = False
    #        print "tempball"
    #        print ball
        temp_path.append("Right")
        DFS(b3, v3, temp_path)

    temp_path = copy.deepcopy(path)
    b4 = copy.deepcopy(temp_ball_data)
    v4 = copy.deepcopy(temp_visited_map)
    ret = False
    for ball in b4:
        if is_possible_move_to_direction(ball, b4, v4, DIRECTION.LEFT):
            ret = True
            break

    if ret:
        for ball in b4:
            ball['direction'] = DIRECTION.LEFT
            ball['is_moved'] = False
    #        print "tempball"
    #        print ball
        temp_path.append("Left")
        DFS(b4, v4, temp_path)

    current_UNIT += 1
    if current_UNIT == UNIT:
        progress += 1
        current_UNIT = 0
    PB.set_progress(progress)

def check_duplicate_ball(y, x, ball, visited_map):
    if ball['y'] == y and ball['x'] == x:
        if ball['is_moved'] == True:
            return False
        else :
            if ball['direction'] == DIRECTION.UP:
                if ball['type'] == 0:
                    if ball['y'] - 1 >= 0:
                        current_type = tile_map[ball['y']][ball['x']]
                        next_type = tile_map[ball['y']-1][ball['x']]
                        if current_type == TILETYPE.HORIZONTAL:
                            return False
                        elif next_type == TILETYPE.BLOCK or next_type == TILETYPE.HORIZONTAL or next_type == TILETYPE.FLIP :
                            return False
                        elif (next_type == TILETYPE.NORMAL or next_type == TILETYPE.VERTICAL) and visited_map[ball['y']-1][ball['x'] ] == 0:
                            return True
                        elif next_type == TILETYPE.RIGHT or next_type == TILETYPE.LEFT or next_type == TILETYPE.UP or next_type == TILETYPE.DOWN:
                            for b in ball_data:
                                if ball['x'] != b['x'] or ball['y'] != b['y']:
                                
                                    return True
                        elif next_type == TILETYPE.WARP or next_type == TILETYPE.MAGNETIC:
                            return True

                elif ball['type'] == 1:
                    if ball['y'] + 1 <= map_height-1 : 
                        current_type = tile_map[ball['y']][ball['x']]
                        next_type = tile_map[ball['y']+1][ball['x']]
                        if current_type == TILETYPE.HORIZONTAL:
                            return False
                        elif next_type == TILETYPE.BLOCK or next_type == TILETYPE.HORIZONTAL or next_type == TILETYPE.FLIP :
                            return False
                        elif (next_type == TILETYPE.NORMAL or next_type == TILETYPE.VERTICAL) and visited_map[ball['y']+1][ball['x'] ] == 0:
                            return True
                        elif next_type == TILETYPE.RIGHT or next_type == TILETYPE.LEFT or next_type == TILETYPE.UP or next_type == TILETYPE.DOWN:
                            return True
                        elif next_type == TILETYPE.WARP or next_type == TILETYPE.MAGNETIC:
                            return True

            elif ball['direction'] == DIRECTION.DOWN:
                if ball['type'] == 0:
                    if ball['y'] + 1 <= map_height-1 : 
                        current_type = tile_map[ball['y']][ball['x']]
                        next_type = tile_map[ball['y']+1][ball['x']]
                        if current_type == TILETYPE.HORIZONTAL:
                            return False
                        elif next_type == TILETYPE.BLOCK or next_type == TILETYPE.HORIZONTAL or next_type == TILETYPE.FLIP :
                            return False
                        elif (next_type == TILETYPE.NORMAL or next_type == TILETYPE.VERTICAL) and visited_map[ball['y']+1][ball['x'] ] == 0:
                            return True
                        elif next_type == TILETYPE.RIGHT or next_type == TILETYPE.LEFT or next_type == TILETYPE.UP or next_type == TILETYPE.DOWN:
                            return True
                        elif next_type == TILETYPE.WARP or next_type == TILETYPE.MAGNETIC:
                            return True

                elif ball['type'] == 1:
                    if ball['y'] - 1 >= 0:
                        current_type = tile_map[ball['y']][ball['x']]
                        next_type = tile_map[ball['y']-1][ball['x']]
                        if current_type == TILETYPE.HORIZONTAL:
                            return False
                        elif next_type == TILETYPE.BLOCK or next_type == TILETYPE.HORIZONTAL or next_type == TILETYPE.FLIP :
                            return False
                        elif (next_type == TILETYPE.NORMAL or next_type == TILETYPE.VERTICAL) and visited_map[ball['y']-1][ball['x'] ] == 0:
                            return True
                        elif next_type == TILETYPE.RIGHT or next_type == TILETYPE.LEFT or next_type == TILETYPE.UP or next_type == TILETYPE.DOWN:
                            return True
                        elif next_type == TILETYPE.WARP or next_type == TILETYPE.MAGNETIC:
                            return True


            elif ball['direction'] == DIRECTION.RIGHT:
                if ball['type'] == 0:
                    if ball['x'] + 1 <= map_width - 1:
                        current_type = tile_map[ball['y']][ball['x']]
                        next_type = tile_map[ball['y']][ball['x'] + 1]
                        if current_type == TILETYPE.VERTICAL:
                            return False
                        elif next_type == TILETYPE.BLOCK or next_type == TILETYPE.VERTICAL or next_type == TILETYPE.FLIP:
                            return False
                        elif (next_type == TILETYPE.NORMAL or next_type == TILETYPE.HORIZONTAL) and visited_map[ball['y']][ball['x'] + 1] == 0:
                            return True
                        elif next_type == TILETYPE.RIGHT or next_type == TILETYPE.LEFT or next_type == TILETYPE.UP or next_type == TILETYPE.DOWN:
                            return True
                        elif next_type == TILETYPE.WARP or next_type == TILETYPE.MAGNETIC:
                            return True

                elif ball['type'] == 1:
                    if ball['x'] - 1 >= 0:
                        current_type = tile_map[ball['y']][ball['x']]
                        next_type = tile_map[ball['y']][ball['x'] - 1]
                        if current_type == TILETYPE.VERTICAL:
                            return False
                        elif next_type == TILETYPE.BLOCK or next_type == TILETYPE.VERTICAL or next_type == TILETYPE.FLIP:
                            return False
                        elif (next_type == TILETYPE.NORMAL or next_type == TILETYPE.HORIZONTAL) and visited_map[ball['y']][ball['x'] - 1] == 0:
                            return True
                        elif next_type == TILETYPE.RIGHT or next_type == TILETYPE.LEFT or next_type == TILETYPE.UP or next_type == TILETYPE.DOWN:
                            return True
                        elif next_type == TILETYPE.WARP or next_type == TILETYPE.MAGNETIC:
                            return True


            elif ball['direction'] == DIRECTION.LEFT:
                if ball['type'] == 0:
                    if ball['x'] - 1 >= 0:
                        current_type = tile_map[ball['y']][ball['x']]
                        next_type = tile_map[ball['y']][ball['x'] - 1]
                        if current_type == TILETYPE.VERTICAL:
                            return False
                        elif next_type == TILETYPE.BLOCK or next_type == TILETYPE.VERTICAL or next_type == TILETYPE.FLIP:
                            return False
                        elif (next_type == TILETYPE.NORMAL or next_type == TILETYPE.HORIZONTAL) and visited_map[ball['y']][ball['x'] - 1] == 0:
                            return True
                        elif next_type == TILETYPE.RIGHT or next_type == TILETYPE.LEFT or next_type == TILETYPE.UP or next_type == TILETYPE.DOWN:
                            return True
                        elif next_type == TILETYPE.WARP or next_type == TILETYPE.MAGNETIC:
                            return True

                elif ball['type'] == 1:
                    if ball['x'] + 1 <= map_width - 1:
                        current_type = tile_map[ball['y']][ball['x']]
                        next_type = tile_map[ball['y']][ball['x'] + 1]
                        if current_type == TILETYPE.VERTICAL:
                            return False
                        elif next_type == TILETYPE.BLOCK or next_type == TILETYPE.VERTICAL or next_type == TILETYPE.FLIP:
                            return False
                        elif (next_type == TILETYPE.NORMAL or next_type == TILETYPE.HORIZONTAL) and visited_map[ball['y']][ball['x'] + 1] == 0:
                            return True
                        elif next_type == TILETYPE.RIGHT or next_type == TILETYPE.LEFT or next_type == TILETYPE.UP or next_type == TILETYPE.DOWN:
                            return True
                        elif next_type == TILETYPE.WARP or next_type == TILETYPE.MAGNETIC:
                            return True


            elif ball['direction'] == DIRECTION.NONE:
                return False
    else:
        return True

    return False

def is_possible_move(ball, ball_data, visited_map):
    if ball['direction'] == DIRECTION.UP :
        if ball['type'] == 0:
            if ball['y'] - 1 >= 0:
                current_type = tile_map[ball['y']][ball['x']]
                next_type = tile_map[ball['y']-1][ball['x']]
                if current_type == TILETYPE.HORIZONTAL:
                    return False
                elif next_type == TILETYPE.BLOCK or next_type == TILETYPE.HORIZONTAL or next_type == TILETYPE.FLIP :
                    return False
                elif (next_type == TILETYPE.NORMAL or next_type == TILETYPE.VERTICAL) and visited_map[ball['y']-1][ball['x'] ] == 0:
                    return True
                elif next_type == TILETYPE.RIGHT or next_type == TILETYPE.LEFT or next_type == TILETYPE.UP or next_type == TILETYPE.DOWN:
                    for b in ball_data:
                        if b['x'] == ball['x'] and b['y'] == ball['y']-1:
                            if b['is_moved'] == True:
                                return False
                            else:
                                return is_possible_move_to_direction(b, ball_data, visited_map, b['direction'])
                    return True
                elif next_type == TILETYPE.WARP or next_type == TILETYPE.MAGNETIC:
                    for b in ball_data:
                        if b['x'] == ball['x'] and b['y'] == ball['y']-1:
                            return is_possible_move_to_direction(b, ball_data, visited_map, b['direction'])
                    return True

        elif ball['type'] == 1:
            if ball['y'] + 1 <= map_height-1 : 
                current_type = tile_map[ball['y']][ball['x']]
                next_type = tile_map[ball['y']+1][ball['x']]
                if current_type == TILETYPE.HORIZONTAL:
                    return False
                elif next_type == TILETYPE.BLOCK or next_type == TILETYPE.HORIZONTAL or next_type == TILETYPE.FLIP :
                    return False
                elif (next_type == TILETYPE.NORMAL or next_type == TILETYPE.VERTICAL) and visited_map[ball['y']+1][ball['x'] ] == 0:
                    return True
                elif next_type == TILETYPE.RIGHT or next_type == TILETYPE.LEFT or next_type == TILETYPE.UP or next_type == TILETYPE.DOWN:
                    for b in ball_data:
                        if b['x'] == ball['x'] and b['y'] == ball['y']+1:
                            if b['is_moved'] == True:
                                return False
                            else:
                                return is_possible_move_to_direction(b, ball_data, visited_map, b['direction'])
                    return True
                elif next_type == TILETYPE.WARP or next_type == TILETYPE.MAGNETIC:
                    for b in ball_data:
                        if b['x'] == ball['x'] and b['y'] == ball['y']+1:
                            return is_possible_move_to_direction(b, ball_data, visited_map, b['direction'])
                    return True

    elif ball['direction'] == DIRECTION.DOWN:
        if ball['type'] == 0:
            if ball['y'] + 1 <= map_height-1 : 
                current_type = tile_map[ball['y']][ball['x']]
                next_type = tile_map[ball['y']+1][ball['x']]
                if current_type == TILETYPE.HORIZONTAL:
                    return False
                elif next_type == TILETYPE.BLOCK or next_type == TILETYPE.HORIZONTAL or next_type == TILETYPE.FLIP :
                    return False
                elif (next_type == TILETYPE.NORMAL or next_type == TILETYPE.VERTICAL) and visited_map[ball['y']+1][ball['x'] ] == 0:
                    return True
                elif next_type == TILETYPE.RIGHT or next_type == TILETYPE.LEFT or next_type == TILETYPE.UP or next_type == TILETYPE.DOWN:
                    for b in ball_data:
                        if b['x'] == ball['x'] and b['y'] == ball['y']+1:
                            if b['is_moved'] == True:
                                return False
                            else:
                                return is_possible_move_to_direction(b, ball_data, visited_map, b['direction'])
                    return True
                elif next_type == TILETYPE.WARP or next_type == TILETYPE.MAGNETIC:
                    for b in ball_data:
                        if b['x'] == ball['x'] and b['y'] == ball['y']+1:
                            return is_possible_move_to_direction(b, ball_data, visited_map, b['direction'])
                    return True

        elif ball['type'] == 1:
            if ball['y'] - 1 >= 0:
                current_type = tile_map[ball['y']][ball['x']]
                next_type = tile_map[ball['y']-1][ball['x']]
                if current_type == TILETYPE.HORIZONTAL:
                    return False
                elif next_type == TILETYPE.BLOCK or next_type == TILETYPE.HORIZONTAL or next_type == TILETYPE.FLIP :
                    return False
                elif (next_type == TILETYPE.NORMAL or next_type == TILETYPE.VERTICAL) and visited_map[ball['y']-1][ball['x'] ] == 0:
                    return True
                elif next_type == TILETYPE.RIGHT or next_type == TILETYPE.LEFT or next_type == TILETYPE.UP or next_type == TILETYPE.DOWN:
                    for b in ball_data:
                        if b['x'] == ball['x'] and b['y'] == ball['y']-1:
                            if b['is_moved'] == True:
                                return False
                            else:
                                return is_possible_move_to_direction(b, ball_data, visited_map, b['direction'])
                    return True
                elif next_type == TILETYPE.WARP or next_type == TILETYPE.MAGNETIC:
                    for b in ball_data:
                        if b['x'] == ball['x'] and b['y'] == ball['y']-1:
                            return is_possible_move_to_direction(b, ball_data, visited_map, b['direction'])
                    return True

    elif ball['direction'] == DIRECTION.RIGHT:
        if ball['type'] == 0:
            if ball['x'] + 1 <= map_width - 1:
                current_type = tile_map[ball['y']][ball['x']]
                next_type = tile_map[ball['y']][ball['x'] + 1]
                if current_type == TILETYPE.VERTICAL:
                    return False
                elif next_type == TILETYPE.BLOCK or next_type == TILETYPE.VERTICAL or next_type == TILETYPE.FLIP:
                    return False
                elif (next_type == TILETYPE.NORMAL or next_type == TILETYPE.HORIZONTAL) and visited_map[ball['y']][ball['x'] + 1] == 0:
                    return True
                elif next_type == TILETYPE.RIGHT or next_type == TILETYPE.LEFT or next_type == TILETYPE.UP or next_type == TILETYPE.DOWN:
                    for b in ball_data:
                        if b['x'] == ball['x']+1 and b['y'] == ball['y']:
                            if b['is_moved'] == True:
                                return False
                            else:
                                return is_possible_move_to_direction(b, ball_data, visited_map, b['direction'])
                    return True
                elif next_type == TILETYPE.WARP or next_type == TILETYPE.MAGNETIC:
                    for b in ball_data:
                        if b['x'] == ball['x']+1 and b['y'] == ball['y']:
                            return is_possible_move_to_direction(b, ball_data, visited_map, b['direction'])
                    return True

        elif ball['type'] == 1:
            if ball['x'] - 1 >= 0:
                current_type = tile_map[ball['y']][ball['x']]
                next_type = tile_map[ball['y']][ball['x'] - 1]
                if current_type == TILETYPE.VERTICAL:
                    return False
                elif next_type == TILETYPE.BLOCK or next_type == TILETYPE.VERTICAL or next_type == TILETYPE.FLIP:
                    return False
                elif (next_type == TILETYPE.NORMAL or next_type == TILETYPE.HORIZONTAL) and visited_map[ball['y']][ball['x'] - 1] == 0:
                    return True
                elif next_type == TILETYPE.RIGHT or next_type == TILETYPE.LEFT or next_type == TILETYPE.UP or next_type == TILETYPE.DOWN:
                    for b in ball_data:
                        if b['x'] == ball['x']-1 and b['y'] == ball['y']:
                            if b['is_moved'] == True:
                                return False
                            else:
                                return is_possible_move_to_direction(b, ball_data, visited_map, b['direction'])
                    return True
                elif next_type == TILETYPE.WARP or next_type == TILETYPE.MAGNETIC:
                    for b in ball_data:
                        if b['x'] == ball['x'] -1 and b['y'] == ball['y']:
                            return is_possible_move_to_direction(b, ball_data, visited_map, b['direction'])
                    return True

    elif ball['direction'] == DIRECTION.LEFT:
        if ball['type'] == 0:
            if ball['x'] - 1 >= 0:
                current_type = tile_map[ball['y']][ball['x']]
                next_type = tile_map[ball['y']][ball['x'] - 1]
                if current_type == TILETYPE.VERTICAL:
                    return False
                elif next_type == TILETYPE.BLOCK or next_type == TILETYPE.VERTICAL or next_type == TILETYPE.FLIP:
                    return False
                elif (next_type == TILETYPE.NORMAL or next_type == TILETYPE.HORIZONTAL) and visited_map[ball['y']][ball['x'] - 1] == 0:
                    return True
                elif next_type == TILETYPE.RIGHT or next_type == TILETYPE.LEFT or next_type == TILETYPE.UP or next_type == TILETYPE.DOWN:
                    for b in ball_data:
                        if b['x'] == ball['x']-1 and b['y'] == ball['y']:
                            if b['is_moved'] == True:
                                return False
                            else:
                                return is_possible_move_to_direction(b, ball_data, visited_map, b['direction'])
                    return True
                elif next_type == TILETYPE.WARP or next_type == TILETYPE.MAGNETIC:
                    for b in ball_data:
                        if b['x'] == ball['x'] -1 and b['y'] == ball['y']:
                            return is_possible_move_to_direction(b, ball_data, visited_map, b['direction'])
                    return True

        elif ball['type'] == 1:
            if ball['x'] + 1 <= map_width - 1:
                current_type = tile_map[ball['y']][ball['x']]
                next_type = tile_map[ball['y']][ball['x'] + 1]
                if current_type == TILETYPE.VERTICAL:
                    return False
                elif next_type == TILETYPE.BLOCK or next_type == TILETYPE.VERTICAL or next_type == TILETYPE.FLIP:
                    return False
                elif (next_type == TILETYPE.NORMAL or next_type == TILETYPE.HORIZONTAL) and visited_map[ball['y']][ball['x'] + 1] == 0:
                    return True
                elif next_type == TILETYPE.RIGHT or next_type == TILETYPE.LEFT or next_type == TILETYPE.UP or next_type == TILETYPE.DOWN:
                    for b in ball_data:
                        if b['x'] == ball['x']+1 and b['y'] == ball['y']:
                            if b['is_moved'] == True:
                                return False
                            else:
                                return is_possible_move_to_direction(b, ball_data, visited_map, b['direction'])
                    return True
                elif next_type == TILETYPE.WARP or next_type == TILETYPE.MAGNETIC:
                    for b in ball_data:
                        if b['x'] == ball['x']+1 and b['y'] == ball['y']:
                            return is_possible_move_to_direction(b, ball_data, visited_map, b['direction'])
                    return True

    return False    

def is_possible_move_to_direction(ball, ball_data, visited_map, direction) :
    if direction == DIRECTION.UP :
        if ball['type'] == 0:
            if ball['y'] - 1 >= 0:
                current_type = tile_map[ball['y']][ball['x']]
                next_type = tile_map[ball['y']-1][ball['x']]
                if current_type == TILETYPE.HORIZONTAL:
                    return False
                elif next_type == TILETYPE.BLOCK or next_type == TILETYPE.HORIZONTAL or next_type == TILETYPE.FLIP :
                    return False
                elif (next_type == TILETYPE.NORMAL or next_type == TILETYPE.VERTICAL) and visited_map[ball['y']-1][ball['x'] ] == 0:
                    return True
                elif next_type == TILETYPE.RIGHT or next_type == TILETYPE.LEFT or next_type == TILETYPE.UP or next_type == TILETYPE.DOWN or next_type == TILETYPE.WARP or next_type == TILETYPE.MAGNETIC:
                    for b in ball_data:
                        if b['x'] == ball['x'] and b['y'] == ball['y'] -1 :
                            return False
                    return True
                
        elif ball['type'] == 1:
            if ball['y'] + 1 <= map_height-1 : 
                current_type = tile_map[ball['y']][ball['x']]
                next_type = tile_map[ball['y']+1][ball['x']]
                if current_type == TILETYPE.HORIZONTAL:
                    return False
                elif next_type == TILETYPE.BLOCK or next_type == TILETYPE.HORIZONTAL or next_type == TILETYPE.FLIP :
                    return False
                elif (next_type == TILETYPE.NORMAL or next_type == TILETYPE.VERTICAL) and visited_map[ball['y']+1][ball['x'] ] == 0:
                    return True
                elif next_type == TILETYPE.RIGHT or next_type == TILETYPE.LEFT or next_type == TILETYPE.UP or next_type == TILETYPE.DOWN or next_type == TILETYPE.WARP or next_type == TILETYPE.MAGNETIC:
                    for b in ball_data:
                        if b['x'] == ball['x'] and b['y'] == ball['y']+1:
                            return False
                    return True

    elif direction == DIRECTION.DOWN:
        if ball['type'] == 0:
            if ball['y'] + 1 <= map_height-1 : 
                current_type = tile_map[ball['y']][ball['x']]
                next_type = tile_map[ball['y']+1][ball['x']]
                if current_type == TILETYPE.HORIZONTAL:
                    return False
                elif next_type == TILETYPE.BLOCK or next_type == TILETYPE.HORIZONTAL or next_type == TILETYPE.FLIP :
                    return False
                elif (next_type == TILETYPE.NORMAL or next_type == TILETYPE.VERTICAL) and visited_map[ball['y']+1][ball['x'] ] == 0:
                    return True
                elif next_type == TILETYPE.RIGHT or next_type == TILETYPE.LEFT or next_type == TILETYPE.UP or next_type == TILETYPE.DOWN or next_type == TILETYPE.WARP or next_type == TILETYPE.MAGNETIC:
                    for b in ball_data:
                        if b['x'] == ball['x'] and b['y'] == ball['y']+1:
                            return False
                    return True
        
        elif ball['type'] == 1:
            if ball['y'] - 1 >= 0:
                current_type = tile_map[ball['y']][ball['x']]
                next_type = tile_map[ball['y']-1][ball['x']]
                if current_type == TILETYPE.HORIZONTAL:
                    return False
                elif next_type == TILETYPE.BLOCK or next_type == TILETYPE.HORIZONTAL or next_type == TILETYPE.FLIP :
                    return False
                elif (next_type == TILETYPE.NORMAL or next_type == TILETYPE.VERTICAL) and visited_map[ball['y']-1][ball['x'] ] == 0:
                    return True
                elif next_type == TILETYPE.RIGHT or next_type == TILETYPE.LEFT or next_type == TILETYPE.UP or next_type == TILETYPE.DOWN or next_type == TILETYPE.WARP or next_type == TILETYPE.MAGNETIC:
                    for b in ball_data:
                        if b['x'] == ball['x'] and b['y'] == b['y']-1:
                            return False
                    return True
 
    elif direction == DIRECTION.RIGHT:
        if ball['type'] == 0:
            if ball['x'] + 1 <= map_width - 1:
                current_type = tile_map[ball['y']][ball['x']]
                next_type = tile_map[ball['y']][ball['x'] + 1]
                if current_type == TILETYPE.VERTICAL:
                    return False
                elif next_type == TILETYPE.BLOCK or next_type == TILETYPE.VERTICAL or next_type == TILETYPE.FLIP:
                    return False
                elif (next_type == TILETYPE.NORMAL or next_type == TILETYPE.HORIZONTAL) and visited_map[ball['y']][ball['x'] + 1] == 0:
                    return True
                elif next_type == TILETYPE.RIGHT or next_type == TILETYPE.LEFT or next_type == TILETYPE.UP or next_type == TILETYPE.DOWN or next_type == TILETYPE.WARP or next_type == TILETYPE.MAGNETIC:
                    for b in ball_data:
                        if b['x'] == ball['x']+1 and b['y'] == ball['y']:
                            return False
                    return True
        elif ball['type'] == 1:
            if ball['x'] - 1 >= 0:
                current_type = tile_map[ball['y']][ball['x']]
                next_type = tile_map[ball['y']][ball['x'] - 1]
                if current_type == TILETYPE.VERTICAL:
                    return False
                elif next_type == TILETYPE.BLOCK or next_type == TILETYPE.VERTICAL or next_type == TILETYPE.FLIP:
                    return False
                elif (next_type == TILETYPE.NORMAL or next_type == TILETYPE.HORIZONTAL) and visited_map[ball['y']][ball['x'] - 1] == 0:
                    return True
                elif next_type == TILETYPE.RIGHT or next_type == TILETYPE.LEFT or next_type == TILETYPE.UP or next_type == TILETYPE.DOWN or next_type == TILETYPE.WARP or next_type == TILETYPE.MAGNETIC:
                    for b in ball_data:
                        if b['x'] == ball['x']-1 and b['y'] == ball['y']:
                            return False
                    return True
    elif direction == DIRECTION.LEFT:
        if ball['type'] == 0:
            if ball['x'] - 1 >= 0:
                current_type = tile_map[ball['y']][ball['x']]
                next_type = tile_map[ball['y']][ball['x'] - 1]
                if current_type == TILETYPE.VERTICAL:
                    return False
                elif next_type == TILETYPE.BLOCK or next_type == TILETYPE.VERTICAL or next_type == TILETYPE.FLIP:
                    return False
                elif (next_type == TILETYPE.NORMAL or next_type == TILETYPE.HORIZONTAL) and visited_map[ball['y']][ball['x'] - 1] == 0:
                    return True
                elif next_type == TILETYPE.RIGHT or next_type == TILETYPE.LEFT or next_type == TILETYPE.UP or next_type == TILETYPE.DOWN or next_type == TILETYPE.WARP or next_type == TILETYPE.MAGNETIC:
                    for b in ball_data:
                        if b['x'] == ball['x']-1 and b['y'] == ball['y']:
                            return False
                    return True
        elif ball['type'] == 1:
            if ball['x'] + 1 <= map_width - 1:
                current_type = tile_map[ball['y']][ball['x']]
                next_type = tile_map[ball['y']][ball['x'] + 1]
                if current_type == TILETYPE.VERTICAL:
                    return False
                elif next_type == TILETYPE.BLOCK or next_type == TILETYPE.VERTICAL or next_type == TILETYPE.FLIP:
                    return False
                elif (next_type == TILETYPE.NORMAL or next_type == TILETYPE.HORIZONTAL) and visited_map[ball['y']][ball['x'] + 1] == 0:
                    return True
                elif next_type == TILETYPE.RIGHT or next_type == TILETYPE.LEFT or next_type == TILETYPE.UP or next_type == TILETYPE.DOWN or next_type == TILETYPE.WARP or next_type == TILETYPE.MAGNETIC:
                    for b in ball_data:
                        if b['x'] == ball['x']+1 and b['y'] == ball['y']:
                            return False
                    return True

    return False

def move_ball(ball):
    tempball = ball
    next_type = 0
    next_x = 0
    next_y = 0
    if tempball['direction'] == DIRECTION.UP:
        next_x = tempball['x']
        next_y = tempball['y']-1
        next_type = tile_map[next_y][next_x]
    elif tempball['direction'] == DIRECTION.DOWN:
        next_x = tempball['x']
        next_y = tempball['y']+1
        next_type = tile_map[next_y][next_x]
    elif tempball['direction'] == DIRECTION.RIGHT:
        next_x = tempball['x']+1
        next_y = tempball['y']
        next_type = tile_map[next_y][next_x]
    elif tempball['direction'] == DIRECTION.LEFT:
        next_x = tempball['x']-1
        next_y = tempball['y']
        next_type = tile_map[next_y][next_x]

    if next_type == TILETYPE.NORMAL:
        tempball['x'] = next_x
        tempball['y'] = next_y
        tempball['ignore_magnetic'] = False
    elif next_type == TILETYPE.FLIP or next_type == TILETYPE.BLOCK:
        tempball['ignore_magnetic'] = False
    elif next_type == TILETYPE.VERTICAL:
        tempball['y'] = next_y
        tempball['x'] = next_x
        tempball['ignore_magnetic'] = False
    elif next_type == TILETYPE.HORIZONTAL:
        tempball['y'] = next_y
        tempball['x'] = next_x
        tempball['ignore_magnetic'] = False
    elif next_type == TILETYPE.RIGHT:
        tempball['y'] = next_y
        tempball['x'] = next_x
        tempball['direction'] = DIRECTION.RIGHT
        tempball['ignore_magnetic'] = True
    elif next_type == TILETYPE.LEFT:
        tempball['y'] = next_y
        tempball['x'] = next_x
        tempball['direction'] = DIRECTION.LEFT
        tempball['ignore_magnetic'] = True
    elif next_type == TILETYPE.UP:
        tempball['x'] = next_x
        tempball['y'] = next_y
        tempball['direction'] = DIRECTION.UP
        tempball['ignore_magnetic'] = True
    elif next_type == TILETYPE.DOWN:
        tempball['y'] = next_y
        tempball['x'] = next_x
        tempball['direction'] = DIRECTION.DOWN
        tempball['ignore_magnetic'] = True
    elif next_type == TILETYPE.WARP:
        for h in range(0, map_height):
            for l in range(0, map_width):
                if tile_map[h][l] == TILETYPE.WARP and (h != next_y or l != next_x):
                    tempball['y'] = h
                    tempball['x'] = l
                    tempball['ignore_magnetic'] = False
                    return tempball
    elif next_type == TILETYPE.MAGNETIC:
        tempball['y'] = next_y
        tempball['x'] = next_x
        tempball['direction'] = DIRECTION.NONE
        tempball['ignore_magnetic'] = True

    return tempball

def main():
    global mim_move
    global start_package_number
    global start_level_number
    global end_package_number
    global end_level_number
    global move_limit
    while True:
        move_limit = 100
        mode = mode_select()
        if mode == 0 :
            break
        else:
            key_input(mode)
            if start_package_number == -2 or start_level_number == -2 or end_package_number == -2 or end_level_number == -2 or move_limit == -2:
                continue
            find_path(mode)


    print 'Terminate solver\n'

if __name__ == "__main__" : 
    sys.exit(main())
