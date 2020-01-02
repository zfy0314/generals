from pprint import pprint
import signal
import os

from base.game import Board
from base.utils import clear, cprint, error_filter

class Human_Player():
    # deprecated

    def __init__(self, name):

        self.name = name

    def get_next_move(self, board):

        self.view(board)
        return error_filter(self.parse)

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

    def parse(self):

        tmp = input("{}'s turn: ".format(self.name))
        if tmp == '': return None
        n = [int(x) for x in tmp.replace('(', ' ').replace(')', ' ').replace(',', ' ').split(' ') if not x == '']
        if len(n) != 5: raise ValueError
        return ((n[0], n[1]), (n[2], n[3]), n[4] > 0)

class Human_Player2():

    def __init__(self, name):

        self.name = name
        self.queue = [None]
        self.move = {
            'w': (lambda p: (p[0] - 1, p[1])),
            'a': (lambda p: (p[0], p[1] - 1)),
            's': (lambda p: (p[0] + 1, p[1])),
            'd': (lambda p: (p[0], p[1] + 1))
        }

    def get_next_move(self, board):

        self.view(board)
        return error_filter(self.parse)

    def view(self, board):

        queue_step = 0
        for x in range(len(board)):
            cnt = 0
            cprint(str(x).zfill(3), 'system', end=' ')
            for t in board[x]:
                cprint(t, end=' ')
                cnt += 1
            if x == 0: 
                print('    Queued moves:', end='')
            else:
                if queue_step < len(self.queue):
                    print('    {}'.format(self.queue[queue_step]), end='')
                    queue_step += 1
            if queue_step < len(self.queue):
                print('\n' + ' ' * ((cnt + 2) * 4) + str(self.queue[queue_step]))
                queue_step += 1
            else:
                print('\n')
        print('    ', end='')
        for i in range(cnt):
            cprint(str(i).zfill(3), 'system', end=' ')
        print('')

    def parse(self):

        '''
        Usage:
            input: 
                Q {MOVES}: quit all queued moves and save new moves
                {MOVES}: use queued move and add new moves to the end of the queue

                {MOVES}: (x, y) w/a/s/d/w1/a1/s1/d1
        '''

        if len(self.queue) == 0:
            self.queue = [None]
        tmp = input("{}'s turn: (queued: {})\n".format(self.name, self.queue[0]))
        if 'q' in tmp or 'Q' in tmp: 
            self.queue = []
            tmp = tmp.replace('q', '').replace('Q', '')
        tmp =  [x for x in tmp.split(' ') if not x == '']
        if tmp != []:
            x, y = int(tmp[0]), int(tmp[1])
            for m in tmp[2:]:
                if m in {'w', 'a', 's', 'd', 'w1', 'a1', 's1', 'd1'}:
                    (x1, y1) = self.move[m[0]]((x, y))
                    self.queue.append(((x, y), (x1, y1), '1' in m))
                    x, y = x1, y1
                else:
                    for i in range(len(m)):
                        if not m[i] in {'w', 'a', 's', 'd', '1'}:
                            raise ValueError
                        if m[i] == '1': continue
                        (x1, y1) = self.move[m[i]]((x, y))
                        if i != len(m) - 1:
                            self.queue.append(((x, y), (x1, y1), '1' == m[i+1]))
                        else:
                            self.queue.append(((x, y), (x1, y1), False))
                        x, y = x1, y1

        if len(self.queue) > 0:
            while self.queue != [] and self.queue[0] == None:
                del self.queue[0]
        if self.queue == []:
            self.queue = [None]
        move = self.queue[0]
        del self.queue[0]
        return move

class Resume_Player():

    def __init__(self, name, moves):

        self.name = name
        self.moves = moves[::1]

    def get_next_move(self, board):

        return self.moves.pop()

def cli_init():
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
        players[name] = Human_Player2(name)
    pprint(players)
    config = input('use default settings? ')
    if config == '':
        B = Board('offline', players, width=15, height=15, mountain_ratio=0.3, city_ratio=0.1, human=True)
    else:
        height = int(input('height: '))
        width = int(input('width: '))
        mountain_ratio = eval(input('mountain ratio: '))
        city_ratio = eval(input('city ratio: '))
        B = Board('offline', players, width=width, height=height, mountain_ratio=mountain_ratio, city_ratio=city_ratio, human=True)
    return B

def resume_from_file():
    # TODO
    # resume saved
    B = None
    return B

def cli(resume=''):

    if resume == '':
        B = cli_init()
    elif os.path.isfile(resume):
        B = resume_from_file(resume)
    else:
        raise FileNotFoundError 
    
    while True:
        try:
            status = B.update()
            if status == False:
                break
        except KeyboardInterrupt:
            pprint(B.info())
            exit(1)
            
    print(B.winner)


if __name__ == '__main__':
    cli()