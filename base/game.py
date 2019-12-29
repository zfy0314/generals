import json
import os

class Board():

    def __init__(self, name, players={}, width=20, height=20, 
                 mountain_ratio=0.5, city_ratio=0.5):

        '''
        Args:
            name: (string) identifier of the board
            players: (dict: {name: player_class}) different players, 
                every player must have "get_next_move" callable
        '''
        self.name = name
        self.players = players
        self.width = width
        self.height = height
        self.mountain_ratio = mountain_ratio
        self.city_ratio = city_ratio
        self.round = 0

    def init(self):

        # TODO
        # generate self.board
        self.status = {name: {'army':1, 'land':1} for name in self.players.keys()}

    def update(self): # update status (e.g. )

        if 0 == self.round:
            self.init()
        else:
            for name: player in self.players.items():
                self.moves[name] = player.get_next_move()
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

    def get_board(self, player_name):

        # TODO
        # return self.board w.r.t player

    def merge_players(self, player_name_winner, player_name_loser):

        # TODO
        # update board, call by self.update

    def add_army(self):

        # TODO
        # add army, call by self.update

    def save(self, output_file):

        with open(output_file, 'a+') as fout:

            # TODO
            # save self.board for later review
    
        return os.path.getsize(output_file)