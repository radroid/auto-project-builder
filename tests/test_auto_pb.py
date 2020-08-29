"""Tests functions in auto-pb.py using PyTests."""

# import pytest
from tests.tud_test_base import set_keyboard_input
from auto_pb import ProjectBuilder
from auto_pb import create_simple_project, create_ml_project
from pathlib import Path
from shutil import rmtree
import subprocess
import pytest


# Part of code Refactoring
@pytest.fixture()
def pb():
    set_keyboard_input(['test', 'RaDroid'])
    pb = ProjectBuilder()
    yield pb
    if pb.proj_dir is not None and pb.proj_dir.exists():
        rmtree(pb.proj_dir)


@pytest.fixture(scope="module")
def sim_proj():
    """Uses the create_simple_project() method from the auto_pb module and
    returns a ProjectBuilder instance."""
    set_keyboard_input(['simple-project', 'RaDroid'])
    sim_proj = create_simple_project()
    yield sim_proj
    rmtree(sim_proj.proj_dir)


@pytest.fixture(scope="module")
def ml_proj():
    """Uses the create_ml_project() method from the auto_pb module and returns a
    ProjectBuilder instance."""
    set_keyboard_input(['machine-learning-project', 'RaDroid'])
    ml_proj = create_ml_project()
    yield ml_proj
    rmtree(ml_proj.proj_dir)


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
    assert names_tup == ('test', 'RaDroid')


# Test Milestone 2. Create Directory
def test_create_proj_dir_creation_1(pb):
    new_dir = pb.create_proj_dir()
    assert new_dir.exists()


def test_create_proj_dir_creation_2(pb):
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
    path = sim_proj.proj_dir / 'simple_project.py'
    assert path.exists()


# Test Milstone 9. Create more files.
def test_sim_proj_license_exists(sim_proj):
    path = sim_proj.proj_dir / 'LICENSE'
    assert path.exists()


def test_sim_proj_test_exists(sim_proj):
    path = sim_proj.proj_dir / 'test_simple_project.py'
    assert path.exists()


def test_sim_proj_setup_exists(sim_proj):
    path = sim_proj.proj_dir / 'setup.py'
    assert path.exists()


def test_sim_proj_gitignore_exists(sim_proj):
    path = sim_proj.proj_dir / '.gitignore'
    assert path.exists()


# Test Milestone 15. Create Pipenv virtual environment.
def test_sim_proj_venv_exists(sim_proj):
    path = sim_proj.proj_dir / 'venv'
    assert path.exists()


# Test Milestone 10. Simplify directory creation and Refactor
def test_valid_path_error_1(pb):
    with pytest.raises(FileNotFoundError):
        pb.valid_path(Path.cwd())


def test_valid_path_error_2(pb):
    pb.create_proj_dir()
    path = Path.cwd() / 'does-not-exist'
    with pytest.raises(FileNotFoundError):
        pb.valid_path(path)


def test_valid_path_error_3(pb):
    pb.create_proj_dir()
    path = pb.proj_dir / 'present.txt'
    path.touch()
    with pytest.raises(FileExistsError):
        pb.valid_path(filename='present.txt')


def test_create_dir_1(pb):
    pb.create_proj_dir()
    pb.create_dir('hello_dir')
    path = pb.proj_dir / 'hello_dir'
    assert path.exists()


def test_create_dir_2(pb):
    pb.create_proj_dir()
    path = pb.proj_dir / 'hello_dir' / 'sub_dir'
    with pytest.raises(FileNotFoundError):
        pb.create_dir(path)


# Test Milestone 12. Function for ML project
def test_ml_proj_dir_exists(ml_proj):
    assert ml_proj.proj_dir.exists()


def test_ml_proj_dir_data(ml_proj):
    data_dir = ml_proj.proj_dir / 'data'
    assert data_dir.is_dir()


def test_ml_proj_dir_tests(ml_proj):
    tests_dir = ml_proj.proj_dir / 'tests'
    assert tests_dir.is_dir()


def test_ml_proj_dir_tests_file(ml_proj):
    tests_file = ml_proj.proj_dir / 'tests' / \
        'test_machine_learning_project.py'
    assert tests_file.is_file()


def test_ml_proj_dir_notebooks(ml_proj):
    notebooks_dir = ml_proj.proj_dir / 'notebooks'
    assert notebooks_dir.is_dir()


def test_ml_proj_dir_notebooks_file(ml_proj):
    notebooks_file = ml_proj.proj_dir / 'notebooks' / \
        'machine-learning-project.ipynb'
    assert notebooks_file.is_file()


def test_ml_proj_readme_exists(ml_proj):
    path = ml_proj.proj_dir / 'README.md'
    assert path.exists()


def test_ml_proj_todo_exists(ml_proj):
    path = ml_proj.proj_dir / 'TODO.md'
    assert path.exists()


def test_ml_proj_license_exists(ml_proj):
    path = ml_proj.proj_dir / 'LICENSE'
    assert path.exists()


def test_ml_proj_gitignore_exists(ml_proj):
    path = ml_proj.proj_dir / '.gitignore'
    assert path.exists()


def ml_proj_conda_env():
    set_keyboard_input(['machine-learning-project-2', 'RaDroid'])
    ml_proj = create_ml_project(create_conda_env=True)

    try:
        # Get conda environments
        envs = subprocess.check_output(['conda', 'env', 'list'])
        envs_list = [env.strip() for env in str(envs).split('\\n')]

        proj_env = ml_proj.proj_dir / 'env'
        assert str(proj_env) in envs_list
    finally:
        if ml_proj.proj_dir.exists():
            rmtree(ml_proj.proj_dir)
