import datetime
import fire
import importlib
import json
import os
from pprint import pprint
import time

from base.game import Board

def main(config_file='configs/test101.json'):
    
    with open(config_file, 'r') as fin:
        config = json.load(fin)

    if 'view' not in config.keys():
        view = False
    else:
        view = True
        viewer = importlib.import_module(config['view'])
    if 'save' in config.keys():
        with open(config['save'], 'w') as fin:
            pass
    players = {name: importlib.import_module(config['players'][name].Player) 
                   for name in config['players'].keys()}
    B = Board(config_file,
              player,
              config['width'],
              config['height'],
              config['mountain_ratio'],
              config['city_ratio'])

    while B.update():
        if view:
            viewer(B)
        else:
            pprint(B.status)
        if 'save' in config.keys():
            B.save(config['save'])
    print(B.winner)

if __name__ == '__main__':
    fire.Fire(main)