from base.utils import cprint, error_filter

class Player():

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
        cprint('{}'.format(self.name), id=self.name, end='')
        tmp = input("'s turn: (queued: {})\n".format(self.queue[0]))
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