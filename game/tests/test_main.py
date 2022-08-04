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

def test_game_run():
    game_one = Game()
    assert game_one.run() == None

def test_game_make_sound():
    game_one = Game()
    assert game_one.make_sound() == None

def test_game_make_labels():
    game_one = Game()
    assert game_one.make_labels() == None

def test_game_countdowm():
    game_one = Game()
    assert game_one.countdown() == None

