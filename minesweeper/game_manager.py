from map import *

class GameManager:
    map_instance = None
    running = False
    status = None
    is_first_run = False
    difficulty = None
    mine_count = None
    max_mine_count = None
    map_width = None
    map_height = None

    class Status:
        INIT = 0
        INPUT = 1
        PLAY = 2
        RESUlT = 3

    def __init__(self):
        self.map_instance = MAP()
        self.running = False
        self.status = GameManager.Status.INIT
        self.if_first_run = True
        self.difficulty = 0
        self.mine_count = 0
        self.max_mine_count = 0
        self.map_width = 0
        self.map_height = 0
        print 'Initialized GameManager'

    def run_game(self):
        self.running = True
        self.status = GameManager.Status.INPUT
        self.select_game_mode()

    def select_game_mode(self):
        if self.is_first_run:
            print 'Welcome the minesweeper game!'

        self.is_first_run = False
        choose_diff = False
        while not choose_diff:
            print 'Please select difficulty'
            i = input("0(EASY), 1(NORMAL), 2(HARD)")
            if type(i) != int:
                print 'Please input the number!!!'
                continue
            self.difficulty = int(i)
            if self.difficulty != 0 and self.difficulty != 1 and self.difficulty != 2:
                print 'Please input the Right number!!!'
                continue

            choose_diff = True

        self.max_mine_count = 0
        self.map_width = 0
        self.map_height = 0
        if self.difficulty == 0:
            self.max_mine_count = 78
            self.map_width = 9
            self.map_height = 9
        elif self.difficulty == 1:
            self.max_mine_count = 253
            self.map_width = 16
            self.map_height = 16
        else:
            self.max_mine_count = 477
            self.map_width = 30
            self.map_height = 16

        choose_mine_count = False
        while not choose_mine_count:
            print 'Please input mine count'
            i = input("0(default) and you can set range (1 ~ size of map - 3)")
            if type(i) != int:
                print 'Please input the number!!!'
                continue
            self.mine_count = int(i)
            if self.mine_count > (self.map_width * self.map_height) - 3:
                print 'Invalid mine count : ' + str(self.mine_count)
                continue
                
            choose_mine_count = True

        self.map_instance.create_map(self.map_width, self.map_height, self.mine_count)
        self.play_game()

    def play_game(self):
        self.status = GameManager.Status.PLAY
        finish = False
        is_winner = False

        while not finish:
            self.map_instance.print_display_map()
            if self.map_instance.did_find_all_mines():
                is_winner = True
                finish = False

            else:
                print '\n'
                y, x = input('Input the y, x position (with a comma in between): ')
                if self.map_instance.is_possible_choose(y, x):
                    if self.map_instance.check_mine(y, x):
                        is_winner = False
                        finish = True 
                    else:
                        self.map_instance.choose_tile(y, x)
                else:
                    print 'You can choose that position'
                    continue

        self.go_result(is_winner)

    def go_result(self, result):
        if result:
            print 'You are Winner !!!'
        else:
            print 'Oops! That is mine...'

        print 'Choose your next!'
        choose_action = False
        next_action = 0
        while not choose_action:
            i = input('0(go to main), 1(quit game) : ')
            if type(i) != int:
                print 'Please input the number'
                continue
            next_action = int(i)
            if next_action != 0 and next_action != 1:
                continue

            choose_action = True

        if next_action == 0:
            self.run_game()


