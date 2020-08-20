"""Tests functions in auto-pb.py using PyTests."""

# import pytest
from tests.tud_test_base import set_keyboard_input
from auto_pb import ProjectBuilder
from pathlib import Path
import pytest


# Part of code Refactoring
@pytest.fixture()
def pb():
    set_keyboard_input(['test', 'Raj Dholakia'])
    pb = ProjectBuilder()
    yield pb
    if pb.proj_dir is not None and pb.proj_dir.exists():
        pb.__delete_all__


# Test Milestone 1. First User Input
def test_instantiating_path_error_1():
    path = Path.cwd() / 'non_existant'
    with pytest.raises(FileNotFoundError):
        ProjectBuilder(path)


def test_instantiating_path_error_2():
    path = Path.cwd() / 'test.txt'
    path.touch()
    with pytest.raises(TypeError):
        ProjectBuilder(path)
    path.unlink()


def test_instantiating_error_1():
    set_keyboard_input(['-test_1',  # Start with '-'
                        '$Te*st=2',  # Contains illegal special charaters.
                        'next&warning'])  # Contains one illegal character.
    with pytest.raises(UserWarning):
        ProjectBuilder()


def test_instantiating_error_2():
    set_keyboard_input(['endswith-',  # Ends with '-'
                        'One space',  # Contains white space.
                        '_incorrect'])  # Start with '_'
    with pytest.raises(UserWarning):
        ProjectBuilder()


def test_instantiating_right_1():
    set_keyboard_input(['test_2', 'Raj Dholakia'])
    path = Path.cwd() / 'tests'
    pb = ProjectBuilder(path=path)
    assert pb.path == path


def test_instantiating_right_2():
    set_keyboard_input(['test_2', 'Raj Dholakia'])
    path = Path.cwd() / 'tests'
    pb = ProjectBuilder(path=str(path))
    assert pb.path == path


def test_instantiating_right_3(pb):
    assert pb.path == Path.cwd().parent


def test_instantiating_right_4(pb):
    names_tup = pb.proj_name, pb.author
    assert names_tup == ('test', 'Raj Dholakia')


# Test Milestone 2. Create Directory
def test_create_dir_creation_1(pb):
    new_dir = pb.create_dir()
    assert new_dir.exists()


def test_create_dir_creation_2(pb):
    new_dir = pb.create_dir()
    assert new_dir == Path.cwd().parent / 'test'


# Test Milestone 3a. Create Readme.md
def test_create_readme_creation(pb):
    pb.create_dir()
    readme = pb.create_readme()
    assert readme.exists()


def test_create_readme_creation_error(pb):
    with pytest.raises(FileNotFoundError):
        pb.create_readme()


# Test Milestone 3b. Add text to Readme.md
def test_add_to_readme(pb):
    proj_name = 'test'
    author = 'Raj Dholakia'
    pb.create_dir()
    readme = pb.create_readme()

    text_to_write = f'# {proj_name}\nWelcome to {proj_name}!\n\n\n' \
                    f'Created by {author}.'

    with readme.open('r') as read:
        text_written = read.read()

    assert text_to_write == text_written
