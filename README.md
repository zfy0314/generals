# A platform to test/build [generals](generals.io) playing algorithm

Directory Tree
-----
```sh
--root/
|
|--base/
| |
| |--__init__.py
| |
| |--game.py # recreate generals
| |
| |--vis.py # visualize 
|
|--players/ # where different algorithms are stored
| |
| |--player_example/
| | |
| | |--__init__.py
| | |
| | |--player.py # the actual class to be called, should be inheritated from base_player
| | |
| | |--{OTHER_IMPLEMENTATION_CODES}
| |
| |--player_{OTHER}/
|
|--models/ # large models should be place here
| |
| |--model_example.{EXTENTION}
| |
| |--model_{OTHER}.{EXTENTION}
|
|--configs/ # different playing settings
| |
| |--{INDENTIFIER}.json
|
|--play.py # main entrance, flag pointed to config file
|
|--requirements.txt # tracks python packages
|
|--README.md
```

Dos and Don'ts
-----
***DOs***
1. checkout new branches to implement new players
2. merge to {DATE}_dev
3. stash useless code before merging
4. try to be in line with requirements.txt e.g. package versions
5. try to keep player.py simple, place complex logic in other files

***DO NOTs***
1. merge to master branch
2. edit other players