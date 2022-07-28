import pytest
from game.app import Component, Ship
from game.settings import FPS, screen_height, screen_width
from game.main import run, key_checking, clock, BG, WINDOW


def test_component_exists():
    assert Component


def test_component_move_exists():
    component = Component(1, 2, 'player_back.png')
    assert component.move("left") is None


def test_component_update_exists():
    component = Component(1, 2, 'player_back.png')
    assert component.update() is None


def test_ship_exists():
    assert Ship


def test_ship_move_exists():
    ship = Component(1, 2, 'player_back.png')
    assert ship.move("left") is None


def test_ship_update_exists():
    ship = Ship(1, 2, 'player_back.png')
    assert ship.update() is None


def test_ship_render_exists():
    ship = Ship(1, 2, 'player_back.png')
    assert ship.render() is None


def test_setting_fps():
    assert FPS == 60


def test_setting_screen_height():
    assert screen_height == 640


def test_setting_screen_width():
    assert screen_width == 960


def test_main_run():
    assert run is not None


def test_main_keyboard_checking():
    ship = Component(1, 2, 'player_back.png')
    assert key_checking(ship) is None


def test_main_window():
    assert WINDOW is not None


def test_main_clock():
    assert clock is not None


def test_main_bg():
    assert BG is not None
