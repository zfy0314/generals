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
        
        Attrs:
            generals: (dict: {name: (x, y)}) coordinates for different general
            cities: (list: [(x, y)]) all the city coordinates
            mountains: (list: [(x, y)]) all the mountains
            status: (dict: {name: {'army': NUM_ARMY, 'land': NUM_LAND}})
            vis: (dict: {name: [(x, y)]}) visable coordinates for different players
        '''
        self.name = name
        self.players = players
        self.width = width
        self.height = height
        self.mountain_ratio = mountain_ratio
        self.city_ratio = city_ratio
        self.round = 0
        self.generals = {name: () for name in self.players.keys()}
        self.cities = {} # a list to hold all the cities (x, y, init_strength)
        self.mountains = {} # a list to hold all the mountains (x, y)
        self.status = {name: {'army':1, 'land':1} for name in self.players.keys()}
        self.vis = {name: [self.general[name]] for name in self.players.keys()}

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
            for (x, y, s) in self.cities:
                B[x][y].is_mountain = 0.5
                B[x][y].is_city = 0.5
            for (x, y) in self.mountains:
                B[x][y].is_mountain = 0.5
                B[x][y].is_city = 0.5
            return B
        else:
            # PTAL
            blanks = {(randint(0, self.width - 1), randint(0, self.height - 1))}
            candidates = {x for x in get_valids(blanks[0], [])}
            while len(blanks) < self.width * self.height * (1 - self.mountain_ratio - self.city_ratio):
                parameters = candidates.pop()
                blanks.add(parameters)
                for parameter in get_valids(parameters):
                    candidates.add(parameter) 
            B = []                             
            for x in range(self.width):
                B.append([])
                for y in range(self.height):
                    B[x].append([])
                    if (x, y) not in blanks:
                        if random() < self.mountain_ratio / (self.mountain_ratio + self.city_ratio):
                            self.mountains.add((x, y))
                            B[x][y] = Tile(is_mountain=1)
                        else:
                            self.cities.add((x, y))
                            B[x][y] = Tile(is_city=1, init_strength=randint(40, 50))
                    else:
                        Tile()
            
            for name in self.players.keys():
                (x, y) = blanks.pop
                self.generals[name] = (x, y)
                self.board[x][y].is_general = 1
                self.owner = name
            
            return B

    def update(self): # update status (e.g. )

        if 0 == self.round:
            self.generate_board(False)
        else:
            for name: player in self.players.items():
                self.moves[name] = self.get_next_move(name)
            if self.round % 25 == 0:
                self.add_army()
            else:
                self.add_city()
            # TODO
            # update self.board according to self.moves, have to solve conflicts
            # update self.status according to self.board

        self.round += 1
        self.moves = {}

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

        if move == None: return True
        # TODO
        # check if valid

    def get_board(self, player_name):

        # PTAL
        B = self.generate_board()
        for vis in self.vis[player_name]:
            B[vis[0]][vis[1]] = self.__getitem__(vis)
        return B

    def merge_players(self, player_name_winner, player_name_loser):

        # TODO
        # update board, call by self.update

    def add_army(self):

        # need speed up
        for x in range(self.width):
            for y in range(self.height):
                if self.board[x][y].owner != None:
                    self.board[x][y].army += 1
    
    def add_city(self):
        
        for (x, y) in self.cities:
            if B.board[x][y].owner != None:
                self.board[x][y].army += 1

    def save(self, output_file):

        with open(output_file, 'a+') as fout:

            # TODO
            # save self.board for later review
    
        return os.path.getsize(output_file)

def Tile():

    def __init__(self, owner=None, is_general=0, is_mountain=0, is_city=0, init_army=0):
        
        self.is_general = is_general
        self.is_mountain = is_mountain
        self.is_city = is_city
        self.army = init_army
        self.owner = owner

    def mask(self):
        
        if (self.is_mountain or self.is_city):
            self.is_mountain = self.is_city = 0.5
        self.is_general = 0
        self.army = 0
        self.owner = None
    
    def output(self):
        
        if self.army < 2: return False
        else:
            army = self.army - 1
            self.army = 1
            return army

    def input(self, army, player_name):

        if player_name == self.owner: 
            self.army += army
        else:
            if self.army < army:
                self.owner = player_name
                self.army = army - self.army
            else:
                self.army -= army        
