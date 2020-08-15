"""Tests functions in auto-pb.py using PyTests."""

# import pytest
from tests.tud_test_base import set_keyboard_input
from auto_pb import ProjectBuilder
from pathlib import Path
import pytest

auto_pb = ProjectBuilder()


# Test Milestone 1. First User Input
def test_get_names():
    set_keyboard_input(["test_1", "Raj Dholakia"])
    names_tup = auto_pb.get_names()

    assert names_tup == ("test_1", "Raj Dholakia")


# Test Milestone 2. Create Directory
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


# Test Milestone 3a. Create Readme.md
def test_create_readme_creation_1():
    path = Path.cwd() / 'tests'
    readme = auto_pb.create_readme(path)
    assert readme.exists()
    readme.unlink()


def test_create_readme_creation_2():
    path = Path.cwd() / 'tests'
    readme = auto_pb.create_readme(str(path))
    assert readme.exists()
    readme.unlink()


def test_create_readme_error_1():
    path = Path.cwd() / 'non_existant'
    with pytest.raises(FileNotFoundError):
        auto_pb.create_readme(path)


def test_create_readme_error_2():
    path = Path.cwd() / 'test.txt'
    path.touch()
    with pytest.raises(TypeError):
        auto_pb.create_readme(path)
    path.unlink()


def test_create_readme_text():
    path = Path.cwd() / 'tests'
    readme = auto_pb.create_readme(path)
    with readme.open('r') as read:
        text = read.read()
    readme.unlink()
    assert text == 'Hello World!\n'


# Test Milestone 3b. Add text to Readme.md
def test_add_to_readme_1():
    proj_name = 'test-1'
    author = 'Raj Dholakia'
    path = Path.cwd() / 'tests'
    new_dir = auto_pb.create_dir(path, proj_name)
    readme = auto_pb.create_readme(new_dir)
    auto_pb.add_to_readme(readme, proj_name, author)

    text_to_write = f'# {proj_name}\nWelcome to {proj_name}!\n\n\n' \
                    f'\nCreated by {author}.'

    with readme.open('r') as read:
        text_written = read.read()

    readme.unlink()
    new_dir.rmdir()
    assert text_to_write == text_written
