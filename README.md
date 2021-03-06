# A platform to test/build [generals](generals.io) playing algorithm

V0.0.0 release:
-----
![demo](screenshot.png)
* **Main Feature**: offline cli generals for up to 8 players

How to play:
-----
1. set map as prompted (default set to 2 players; 15*15; mountain ratio 0.3; city ratio 0.1)
2. type x y w/a/s/d/w1/a1/s1/d1 to control the army
    * x, y: initial coordinates
    * *1: move half of the army
    * add 'Q' to the front to quit all queued moves

------------
for developers:

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
| |--utils.py # some helper class/func
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
|--offline.py # v0.0.0 offline cli generals
|
|--play.py # main entrance, flag pointed to config file
|
|--requirements.txt # tracks python packages
|
|--README.md
|
|--test.py # a wrapper to test each module
```

Dos and Don'ts
-----
***DOs***
1. checkout new branches to implement new players
2. merge to {DATE}_dev
3. stash useless code before merging
4. try to be in line with requirements.txt e.g. package versions
5. try to keep player.py simple, place complex logic in other files
6. update README

***DO NOTs***
1. merge to master branch
2. edit other players

Target
-----
* v0.0.0: offline cli generals for up to 8 players
* v0.1.0: visualization and interation
* ...
* v1.0.0: player implementation
