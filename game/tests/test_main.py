from game.main import *
from game.tiles import *
import pytest
import sys
import typing
sys.path.append("../..")


def test_game_exists() -> None:
    assert Game


def test_player_exists() -> None:
    assert Game


def test_tile_exists() -> None:
    assert Tile


def test_rock_exists() -> None:
    assert Rock


def test_asteroid_exists() -> None:
    assert Asteroid


def test_park_ship_exists() -> None:
    assert ParkSpaceShip


def test_tile_map_exists() -> None:
    assert TileMap


def test_game_health() -> None:
    game_one = Game()
    assert game_one.health == 10


def test_game_seconds() -> None:
    game_one = Game()
    assert game_one.seconds == 60


def test_game_minutes() -> None:
    game_one = Game()
    assert game_one.minutes == 2


def test_game_level() -> None:
    game_one = Game()
    assert game_one.level == 1


def test_game_score() -> None:
    game_one = Game()
    assert game_one.score == 0


def test_game_milliseconds() -> None:
    game_one = Game()
    assert game_one.milliseconds == 0


def test_game_current_frames() -> None:
    game_one = Game()
    assert game_one.current_frames == 0


def test_game_running() -> None:
    game_one = Game()
    assert game_one.running is True


def test_game_playing() -> None:
    game_one = Game()
    assert game_one.playing is False


def test_game_game_over() -> None:
    game_one = Game()
    assert game_one.gameover is False


def test_game_player() -> None:
    game_one = Game()
    assert game_one.player is None


def test_game_current_map() -> None:
    game_one = Game()
    assert game_one.current_map is None


def test_game_current_space_mao() -> None:
    game_one = Game()
    assert game_one.current_space_map is None


def test_game_start() -> None:
    game_one = Game()
    assert game_one.start is False


def test_settings_width() -> None:
    assert WIN_WIDTH == 960


def test_settings_height() -> None:
    assert WIN_HEIGHT == 640


def test_settings_tile_size() -> None:
    assert TILESIZE == 32


def test_settings_fps() -> None:
    assert FPS == 60


def test_print_fps() -> None:
    assert PRINT_FPS is True


def test_timer() -> None:
    assert ACTION_TIMER == 8


def test_asteroid_count() -> None:
    assert ASTEROID_COUNT == 3


def test_rock_spawn_percent() -> None:
    assert ROCK_SPAWN_PERCENT == 2


def test_player_layer() -> None:
    assert GROUND_LAYER == 1
