from pprint import pprint
import signal
import sys

from base.game import Board
from base.utils import clear, cprint

class Human_Player():

    def __init__(self, name):

        self.name = name

    def get_next_move(self, board):

        self.view(board)
        tmp = input("{}'s turn: ".format(self.name))
        clear()
        if tmp == '': return None
        else: return self.parse(tmp)

    def view(self, board):

        for x in range(len(board)):
            cnt = 0
            cprint(str(x).zfill(3), 'system', end=' ')
            for t in board[x]:
                cprint(t, end=' ')
                cnt += 1
            print('\n')
        print('    ', end='')
        for i in range(cnt):
            cprint(str(i).zfill(3), 'system', end=' ')
        print('')

    def parse(self, tmp):

        n = [int(x) for x in tmp.replace('(', ' ').replace(')', ' ').replace(',', ' ').split(' ') if not x == '']
        return ((n[0], n[1]), (n[2], n[3]), n[4] > 0)

def cli():

    # initialize
    num_players = input('number of players: ')
    if num_players == '':
        num_players = 2
    else:
        num_players = int(num_players)
    assert num_players in range(1, 9)
    players = {}
    for i in range(num_players):
        name = input("player {}'s name: ".format(i))
        if name == '':
            name = 'player-{}'.format(i)
        players[name] = Human_Player(name)
    pprint(players)
    config = input('ues default setting? ')
    if config == '':
        B = Board('offline', players, width=15, height=15, mountain_ratio=0.3, city_ratio=0.1, human=True)
    else:
        height = int(input('height: '))
        width = int(input('width: '))
        mountain_ratio = eval(input('mountain ratio: '))
        city_ratio = eval(input('city ratio: '))
        B = Board('offline', players, width=width, height=height, mountain_ratio=mountain_ratio, city_ratio=city_ratio, human=True)
    
    while True:
        try:
            B.update()
        except KeyboardInterrupt:
            pprint(B.info())
            exit(1)
            
    print(B.winner)


if __name__ == '__main__':
    cli()