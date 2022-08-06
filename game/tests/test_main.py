import pytest
import sys
sys.path.append("../..")
from game.main import *
from game.tiles import *


def test_game_exists():
    assert Game

def test_player_exists():
    assert Game

def test_tile_exists():
    assert Tile

def test_rock_exists():
    assert Rock

def test_asteroid_exists():
    assert Asteroid


def test_park_ship_exists():
    assert ParkSpaceShip

def test_tile_map_exists():
    assert TileMap

def test_game_health():
    game_one = Game()
    assert game_one.health == 10

def test_game_seconds():
    game_one = Game()
    assert game_one.seconds == 60

def test_game_minutes():
    game_one = Game()
    assert game_one.minutes == 2

def test_game_level():
    game_one = Game()
    assert game_one.level == 1

def test_game_score():
    game_one = Game()
    assert game_one.score == 0

def test_game_milliseconds():
    game_one = Game()
    assert game_one.milliseconds == 0

def test_game_current_frames():
    game_one = Game()
    assert game_one.current_frames == 0

def test_game_running():
    game_one = Game()
    assert game_one.running == True

def test_game_playing():
    game_one = Game()
    assert game_one.playing == False

def test_game_gameover():
    game_one = Game()
    assert game_one.gameover == False

def test_game_player():
    game_one = Game()
    assert game_one.player == None

def test_game_current_map():
    game_one = Game()
    assert game_one.current_map == None

def test_game_current_space_mao():
    game_one = Game()
    assert game_one.current_space_map == None

def test_game_start():
    game_one = Game()
    assert game_one.start == False

def test_settings_width():
    assert WIN_WIDTH == 960

def test_settings_height():
    assert WIN_HEIGHT == 640

def test_settings_tilesize():
    assert TILESIZE == 32

def test_settings_FPS():
    assert FPS == 60

def test_print_fps():
    assert PRINT_FPS == True

def test_timer():
    assert ACTION_TIMER == 8

def test_asteroid_count():
    assert ASTEROID_COUNT == 3

def test_rock_spawn_percent():
    assert ROCK_SPAWN_PERCENT == 1

def test_PLAYER_LAYER():
    assert GROUND_LAYER == 1