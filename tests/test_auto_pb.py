"""Tests functions in auto-pb.py using PyTests."""

# import pytest
from tests.tud_test_base import set_keyboard_input
import auto_pb
from pathlib import Path
import pytest


def test_get_names():
    set_keyboard_input(["test_1", "Raj Dholakia"])
    names_tup = auto_pb.get_names()

    assert names_tup == ("test_1", "Raj Dholakia")


def test_create_dir_creation_1():
    path = Path.cwd()
    new_dir = auto_pb.create_dir(path, 'test_1')
    assert new_dir.exists()
    new_dir.rmdir()


def test_create_dir_creation_2():
    path = Path.cwd()
    new_dir = auto_pb.create_dir(str(path), 'test_1')
    assert new_dir.exists()
    new_dir.rmdir()


def test_create_dir_error_1():
    path = Path.cwd() / 'non_existant'
    with pytest.raises(FileNotFoundError):
        auto_pb.create_dir(path, 'test_1')


def test_create_dir_error_2():
    path = Path.cwd() / 'test.txt'
    path.touch()
    with pytest.raises(TypeError):
        auto_pb.create_dir(path, 'test_1')
    path.unlink()
