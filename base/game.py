from copy import deepcopy
import json
from random import randint, random
import os

class Board():

    def __init__(self, name, players={}, width=20, height=20, 
                 mountain_ratio=0.5, city_ratio=0.5):

        '''
        Args:
            name: (string) identifier of the board
            players: (dict: {name: player_class}) different players, 
                every player must have "get_next_move" callable
            mountain_ratio: (double) NUM_MOUNTAIN / NUM_TILES
            city_ratio: (double) NUM_CITY / NUM_TILES
        
        Attrs:
            generals: (dict: {name: (x, y)}) coordinates for different general
            cities: (set: {(x, y)}) all the city coordinates
            mountains: (set: {(x, y)}) all the mountains
            lands: (dict: {name: {(x, y)}}) coordinates for lands owned by different player
            status: (dict: {name: {'army': NUM_ARMY, 'land': NUM_LAND}})
            vis: (dict: {name: {(x, y)}}) visable coordinates for different players
        '''
        self.name = name
        self.players = players
        self.width = width
        self.height = height
        self.mountain_ratio = mountain_ratio
        self.city_ratio = city_ratio
        self.round = 0
        self.generals = {name: () for name in self.players.keys()}
        self.cities = {}
        self.mountains = {}
        self.lands = {name: {} for name in self.players.keys()}
        self.status = {name: {'army':1, 'land':1} for name in self.players.keys()}
        self.vis = {name: {} for name in self.players.keys()}

    def __getitem__(self, index):
        
        '''
        Args:
            index: (tuple) x, y index of self.board
        '''
        return deepcopy(self.board[index[0]][index[1]])

    def generate_board(self, blank=True):

        def is_valid(parameters, checked):
            (x, y) = parameters
            return (parameters not in checked) and (x in range(self.width)) and (y in range(self.height))

        def get_valids(parameters, checked):
            (x, y) = parameters
            return [parameter for parameter in (x+1, y), (x-1, y), (x, y+1), (x, y-1) \
                        if is_valid(parameter, checked)]

        if blank == True:
            B = [[Tile() for i in range(self.height)] for j in range(self.width)]
            for (x, y) in self.cities.union(self.mountains):
                B[x][y].is_mountain = 0.5
                B[x][y].is_city = 0.5
            return B

        else:
            # PTAL
            # generate blank tiles, connection guaranteed
            blanks = {(randint(0, self.width - 1), randint(0, self.height - 1))}
            candidates = {x for x in get_valids(blanks[0], [])}
            while len(blanks) < self.width * self.height * (1 - self.mountain_ratio - self.city_ratio):
                parameters = candidates.pop()
                blanks.add(parameters)
                for parameter in get_valids(parameters):
                    candidates.add(parameter)

            # draw the board
            B = []                             
            for x in range(self.width):
                B.append([])
                for y in range(self.height):
                    B[x].append([])
                    if (x, y) not in blanks:
                        # add mountain
                        if random() < self.mountain_ratio / (self.mountain_ratio + self.city_ratio):
                            self.mountains.add((x, y))
                            B[x][y] = Tile(is_mountain=1)
                        # add city
                        else:
                            self.cities.add((x, y))
                            B[x][y] = Tile(is_city=1, init_strength=randint(40, 50))
                    else:
                        B[x][y] = Tile()
            
            # add generals
            for name in self.players.keys():
                (x, y) = blanks.pop
                self.generals[name] = (x, y)
                self.board[x][y].is_general = 1
                self.owner = name
                self.lands[name].add((x, y))
            
            self.board = B

    def update(self): 

        def get_surrounded(x0, y0):
            potentials = []
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if (x0 + dx in range(self.width)) and (y0 + dy in range(self.height)):
                        potentials.append((x0 + dx, y0 + dy))
            return potentials

        if 0 == self.round:
            # initialization
            self.generate_board(False)
            self.moves = {}
        else:
            for name in self.players.keys():
                move = self.get_next_move(name)
                self.moves[name] = move
                if move == None: continue

                # update army
                ((x0, y0), (x1, y1), is_half) = move
                old_owner = self.board[x1][y1].input(
                    self.board[x0][y0].output(is_half),
                    name)
                
                # if owner changed
                if old_owner != name:
                    self.lands[name].add((x1, y1))
                    self.lands[name].discard((x1, y1))
                    for (x2, y2) in get_surrounded(x1, y1):
                        self.vis[name].add((x2, y2))
                        if not True in [p in self.lands[old_owner] for p in get_surrounded(x2, y2)]:
                            self.vis[old_owner].discard((x2, y2))
                    
            if self.round % 25 == 0:
                self.add_army()
            else:
                self.add_city()
            
        self.round += 1

        # liveness inspection
        for name, (x, y) in self.generals.items():
            if self.board[x][y].owner != name:
                self.merge_players(self.board[x][y].owner, name)

        # alternative implementation available
        # update status
        for name in self.players.keys():
            self.status[name]['army'] = 0
            for (x, y) in self.lands[name]:
                self.status[name]['army'] += self.board[x][y].army
            self.status[name]['land'] = len(self.lands[name])

        if len(self.players) == 1:
            self.winner = self.players.keys() 
            return False # game terminated
        else:
            return True

    def get_next_move(self, player_name):

        board = self.get_board(name)
        move = self.players[player_name].get_next_move(board)
        while not is_valid(move, player_name):
            move = self.players[player_name].get_next_move(board)
        return move

    def is_valid(self, move, player_name):

        '''
        Args:
            move: (tuple or None) ((x0, y0), (x1, y1), is_half)
                  move from (x0, y0) to (x1, y1), is_half in [True, False]
        '''

        if move == None: return True
        if not ((x0 in range(self.width)) and (x1 in range(self.width)) and 
                (y0 in range(self.height)) and (y1 in range(self.height))): return False
        if not self.board[x0][y0].owner == player_name: return False
        if not self.board[x0][y0].army > 1: return False
        return True

    def get_board(self, player_name):

        # PTAL
        B = self.generate_board()
        for vis in self.vis[player_name]:
            B[vis[0]][vis[1]] = self.__getitem__(vis)
        return B

    def merge_players(self, player_name_winner, player_name_loser):

        for (x, y) in self.lands[player_name_loser]:
            self.board[x][y].owner = player_name_winner
        (x0, y0) = self.generals[player_name_loser].pop()
        self.cities.add((x0, y0))
        self.board[x0][y0].is_general = 0
        self.board[x0][y0].is_city = 0
        self.vis[player_name_winner] = \
            self.vis[player_name_winner].union(self.vis[player_name_loser])
        self.lands[player_name_winner] = \
            self.lands[player_name_winner].union(self.lands[player_name_loser])

    def add_army(self):

        for name in self.players.keys():
            for (x, y) in self.lands[name]:
                self.board[x][y].army += 1
    
    def add_city(self):
        
        for (x, y) in self.cities:
            if B.board[x][y].owner != None:
                self.board[x][y].army += 1
        for name, (x, y) in self.generals.items():
            self.board[x][y].armg += 1

    def save(self, output_file):

        with open(output_file, 'a+') as fout:

            # TODO
            # save self.board for later review @ljt
    
        return os.path.getsize(output_file)

def Tile():

    def __init__(self, owner=None, is_general=0, is_mountain=0, is_city=0, init_army=0):
        
        self.is_general = is_general
        self.is_mountain = is_mountain
        self.is_city = is_city
        self.army = init_army
        self.owner = owner

    def mask(self):

        # deprecated        
        if (self.is_mountain or self.is_city):
            self.is_mountain = self.is_city = 0.5
        self.is_general = 0
        self.army = 0
        self.owner = None
    
    def output(self, is_half=False):
        
        if self.army < 2: return False # should not be reached
        if is_half:
            army = self.army // 2
            self.army -= army
            return army
        else:
            army = self.army - 1
            self.army = 1
            return army

    def input(self, army, player_name):

        old_owner = self.owner
        if player_name == self.owner: 
            self.army += army
        else:
            if self.army < army:
                self.owner = player_name
                self.army = army - self.army
            else:
                self.army -= army
        return old_owner # for better maintainance        

def test_board():

    # TODO
    # check all the methods within Board

    return None

