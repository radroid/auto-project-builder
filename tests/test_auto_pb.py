"""Tests functions in auto-pb.py using PyTests."""

# import pytest
from tests.tud_test_base import set_keyboard_input
from auto_pb import ProjectBuilder
from auto_pb import create_simple_project
from pathlib import Path
from shutil import rmtree
import pytest


# Part of code Refactoring
@pytest.fixture()
def pb():
    set_keyboard_input(['test', 'Raj Dholakia'])
    pb = ProjectBuilder()
    yield pb
    if pb.proj_dir is not None and pb.proj_dir.exists():
        rmtree(pb.proj_dir)


@pytest.fixture(scope="module")
def sim_proj():
    """Uses the simple_project() method from the auto_pb module. and returns a
    ProjectBuilder instance."""
    set_keyboard_input(['test', 'Raj Dholakia'])
    sim_proj = create_simple_project()
    yield sim_proj
    rmtree(sim_proj.proj_dir)


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
    new_dir = pb.create_proj_dir()
    assert new_dir.exists()


def test_create_dir_creation_2(pb):
    new_dir = pb.create_proj_dir()
    assert new_dir == Path.cwd().parent / 'test'


# Test Milestone 3a. Create Readme.md
def test_create_readme_creation(pb):
    pb.create_proj_dir()
    readme = pb.create_file('README.md')
    assert readme.exists()


def test_create_readme_creation_error(pb):
    with pytest.raises(FileNotFoundError):
        pb.create_file('README.md')


# Test Milestone 3b. Add text to Readme.md
def test_add_to_readme(pb):
    proj_name = 'test'
    author = 'Raj Dholakia'
    pb.create_proj_dir()
    readme = pb.create_file('README.md', template=True)

    text_to_write = f'# {proj_name}\nWelcome to {proj_name}!\n\n\n' \
                    f'Created by {author}.'

    with readme.open('r') as read:
        text_written = read.read()

    assert text_to_write == text_written


# Test Milestone 5. Create other files using Templates.
def test_create_todo_creation(pb):
    pb.create_proj_dir()
    todo = pb.create_file('TODO.md')
    assert todo.exists()


def test_create_todo_creation_error(pb):
    with pytest.raises(FileNotFoundError):
        pb.create_file('TODO.md')


def test_create_main_creation_1(pb):
    pb.create_proj_dir()
    filename = f'{pb.proj_name.replace("-","_")}.py'
    main = pb.create_file(f'{filename}')
    assert main.exists()


def test_create_main_creation_2(pb):
    pb.create_proj_dir()
    filename = f'{pb.proj_name.replace("-","_")}.py'
    main = pb.create_file(f'{filename}', template=True,
                          temp_name='main.py.template')
    assert main.exists()


def test_create_main_creation_error_1(pb):
    with pytest.raises(FileNotFoundError):
        pb.create_file('main.py')


def test_create_main_creation_error_2(pb):
    pb.create_proj_dir()
    filename = f'{pb.proj_name.replace("-","_")}.py'
    with pytest.raises(FileNotFoundError):
        pb.create_file(f'{filename}', template=True)


# Test Milestone 6. Create a function to make code resuable.
def test_sim_proj_dir_exists(sim_proj):
    assert sim_proj.proj_dir.exists()


def test_sim_proj_readme_exists(sim_proj):
    path = sim_proj.proj_dir / 'README.md'
    assert path.exists()


def test_sim_proj_todo_exists(sim_proj):
    path = sim_proj.proj_dir / 'TODO.md'
    assert path.exists()


def test_sim_proj_main_exists(sim_proj):
    path = sim_proj.proj_dir / 'test.py'
    assert path.exists()


# Test Milstone 9. Create more files.
def test_sim_proj_license_exists(sim_proj):
    path = sim_proj.proj_dir / 'LICENSE'
    assert path.exists()


def test_sim_proj_test_exists(sim_proj):
    path = sim_proj.proj_dir / 'test.py'
    assert path.exists()


def test_sim_proj_setup_exists(sim_proj):
    path = sim_proj.proj_dir / 'setup.py'
    assert path.exists()


def test_sim_proj_gitignore_exists(sim_proj):
    path = sim_proj.proj_dir / '.gitignore'
    assert path.exists()
