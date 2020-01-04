import datetime
import fire
import importlib
import os
from pprint import pprint
import time
import yaml

from base.game import Board

def main(config_file='configs/humans_2.yaml'):
    
    with open(config_file, 'r') as fin:
        config = yaml.load(fin.read(), Loader=yaml.SafeLoader)

    if 'view' not in config.keys():
        view = False
    else:
        view = True
        viewer = importlib.import_module(config['view'])

        # TODO
        # add viewer implementation

    if 'resume' in config.keys():
        B = yaml.load(open(config['resume'], 'r'), Loader=yaml.SafeLoader)
        B.get_players()
    else: 
        B = Board(config_file,
                config['players'], 
                config['width'],
                config['height'],
                config['mountain_ratio'],
                config['city_ratio'])
        if 'human' in config.keys():
            B.human = True

    while True:
        try:
            status = B.update()
            if status == False:
                break
        except KeyboardInterrupt:
            pprint(B.info())
            if 'save' in config.keys():
                B.save(config['save'])
            exit(1)
    print('Winner:', B.winner)
    if 'save' in config.keys():
        B.save(config['save'])

if __name__ == '__main__':
    fire.Fire(main)