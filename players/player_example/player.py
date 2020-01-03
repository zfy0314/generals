

class Player():

    def __init__(self, **kwargs):

        '''
        Args:
            name: (string) player identifier
        '''
        
        self.name = kwargs['name'] # needed for all players
    
    def get_next_move(self, board): # needed for all players

        next_move = None
        
        # Some algorithm

        return next_move



