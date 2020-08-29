"""The goal of this module is to automate the process of creating directories
and files for a new project.

Update: The refactored code makes use of a class to modularise project \
    building.
"""


import os
import pathlib
from pathlib import Path
import re
from jinja2 import Template


class ProjectBuilder:
    """The class manages the newly created project folder.

    Attributes:
        proj_name (str): name of project entered by the user.

        author_name (str): name of the author entered by the user.

        path (pathlib.PosixPath):\
            path to a directory where the project directory is to be created.\
            Defaults to None. If None, path to the parent directory of this\
                 project directory will be used.

        proj_dir (pathlib.PosixPath): path to the project directory.
    """

    def __init__(self, path: str or pathlib.PosixPath = None):
        """Instantiate an object.

        Args:
            path (str or pathlib.PosixPath, optional):\
                For class attribute 'path'.

        Raises:
            TypeError: if the path provided is not an absolute path.
            FileNotFoundError: if the path provided does not exist.
            TypeError: if the path input is not to a directory.
        """
        if path is None:
            path = Path.cwd().parent
        else:
            if type(path) == str:
                path = Path(path)

            if not path.is_absolute():
                raise TypeError(f'Path entered is not an absolute path.\n'
                                f'path: {path}')
            if not path.exists():
                raise FileNotFoundError(f'The path provided, does not exist.\n'
                                        f'path: {path}')
            if not path.is_dir():
                raise TypeError(f'No directory present at {path}')

        self.path = path
        self.proj_dir = None
        self.proj_name, self.author = self.get_names()

    def get_names(self):
        """Take input from user for the project name and author name. Print out \
        the information provided.

        Returns (Tuple):
            proj_name (str): name of project entered by the user.
            author_name (str): name of the author entered by the user.
        """
        print('\n> What would you like to name your project?')
        for attempt in range(3):
            proj_name = input().strip()
            is_valid = self.valid_project_name(proj_name)
            if is_valid:
                break
            else:
                print('> Please enter a valid project name.')
        else:
            print('\n')
            raise UserWarning('You ran out of attempts to enter a valid '
                              'project name.')

        print('\n> Who is the author of the project? '
              '(Enter full name of the author)')
        author_name = input()

        print('\n### Project Details ###')
        print(f'Project name: {proj_name}')
        print(f'Author:       {author_name}\n')
        return proj_name, author_name

    @staticmethod
    def valid_project_name(name: str):
        """Checks if the 'name' provided is a valid name for the project.

        Args:
            name (str): name of the project or directory to be created.

        Raises:
            TypeError: if the provided argument is not a string.

        Returns:
            bool: if the name provided is valid or no.
        """
        if type(name) != str:
            raise TypeError('Argument is not a string.')

        # Setup Regex expressions
        bad_start = re.match(r'^([-_]).+$', name)
        bad_end = re.match(r'^.+([-_])$', name)
        bad_chars = re.findall(r'(\W)', name)
        bad_chars = set(bad_chars)
        if '-' in bad_chars:
            bad_chars.remove('-')

        # Create space.
        print('')

        if name[0].isdigit():
            print('> PROBLEM: The first character cannot be a number (digit).')
            return False
        elif name.find(' ') > -1:
            print('> PROBLEM: No spaces allowed in the project name. '
                  'Tip: Replace " " with "-", spaces with dashes.')
            return False
        elif bad_chars:
            print(f'> PROBLEM: These special charaters cannot be used in the '
                  f'project name: {tuple(bad_chars)}')
            return False
        elif bad_start:
            print(f'PROBLEM: The project name cannot start with \''
                  f'{bad_start.group(1)}\'.')
            return False
        elif bad_end:
            print(f'PROBLEM: The project name cannot end with \''
                  f'{bad_end.group(1)}\'.')
            return False

        return True

    def valid_path(self, path: str or pathlib.PosixPath = None,
                   filename: str = None):
        """The method does all the error checks to ensure file creation is
           possible.

        Args:
            path (str or pathlib.PosixPath):\
                Path where the file/directory is to be created.

            filename (str): name of the file/directory to be created.

        Raises:
            FileNotFoundError: if no project directory exists.
            FileNotFoundError: if the path input does not exist.
            TypeError: if the path input is not a directory.
            FileExistsError: if the file to be created exists at the path
                             provided.

        Returns:
            pathlib.PosixPath: path with the filename (without if if None).
        """
        if self.proj_dir is None or not self.proj_dir.exists():
            raise FileNotFoundError(f'Please create a project directory before'
                                    f' creating a {filename} file.')

        if path is None:
            path = self.proj_dir
        elif type(path) == str:
            path = Path(path)

        if not path.exists():
            raise FileNotFoundError(f'The path provided, does not exist.\n \
                                    path: {path}')
        if not path.is_dir():
            raise TypeError(f'No directory present at {path}')

        if filename is None:
            return path

        file_path = path / filename

        if file_path.exists():
            raise FileExistsError(f'File {filename} already exists at {path}.')

        return file_path

    def create_proj_dir(self):
        """The function creates a directory at the path specified and with the
        name input.

        Returns:
            pathlib.Posix object: This is the path to the directory created.
        """
        proj_dir = self.path / self.proj_name

        if proj_dir.exists():
            self.proj_dir = proj_dir
            print(f'Directory exists: {proj_dir}\n\n')
            return proj_dir

        proj_dir.mkdir(exist_ok=True)
        self.proj_dir = proj_dir
        print(f'Created directory: {proj_dir}\n\n')
        return proj_dir

    def create_dir(self, dir_name: str, path: str or pathlib.PosixPath = None):
        """The function creates a directory at the path specified and with the
        name input.

        Args:
            dir_name (str): name of the directory to be created.
            path (pathlib.PosixPath or str, optional):\
                path or directory name inside the project directory where the \
                file needs to be created. Defaults to None.

        Returns:
            pathlib.Posix object: This is the path to the directory created.
        """
        new_dir = self.valid_path(path, dir_name)
        new_dir.mkdir(exist_ok=True)
        print(f'Created directory \'{dir_name}\': {new_dir}\n')
        return new_dir

    def create_file(self, filename: str, template: bool = False,
                    temp_dict: dict = None, temp_name: str = None,
                    path: str or pathlib.PosixPath = None):
        """Creates a file at a given path and a given name.

        Args:
            filename (str): name of the file to be created.

            template (bool, optional):\
                True if there if the file needs to contain data contained in \
                its template. Defaults to False.

            temp_dict (dict, optional):\
                used to customise parts of the template. The variable names \
                matching a key in the dict will be replaced with the \
                respective value. Defaults to None. If None, the project and \
                author names are added to the dictionary.

            temp_name (str, optional):\
                name of the template file in the templates directory.\
                Defaults to None. Uses the filename argument followed \
                by '.template' to create a name. A file of this name \
                is looked for in the templates directory.

            path (pathlib.PosixPath or str, optional):\
                path or directory name inside the project directory where the \
                file needs to be created. Defaults to None. If None, the \
                project directory is used as path.

        Returns:
            pathlib.PosixPath: path to the file created.
        """
        file_path = self.valid_path(path, filename)
        file_path.touch()
        print(f'Created {filename}: {file_path}')

        if temp_dict is None:
            temp_dict = {'project_name': self.proj_name,
                         'author_name': self.author,
                         'git_username': 'radroid'}

        if template:
            self.__add_to_file(path_to_file=file_path, template_dict=temp_dict,
                               template_name=temp_name)
            print(f'Text added to {filename}')
        print('')

        return file_path

    def __add_to_file(self, path_to_file: pathlib.PosixPath,
                      template_dict: dict, template_name: str):
        """Add to a file from a template stored in the templates directory.

        Args:
            path_to_file (pathlib.PosixPath):\
                path to the file that needs to be updated.
            template_dict (dict):\
                used to customise parts of the template. The variable names \
                matching a key in the dict will be replaced with the \
                respective value.
            template_name (str):\
                template_name of the template file in the templates directory.

        Raises:
            TypeError: if the path input is not to a file.
            FileNotFoundError: if the path input does not exist.
            FileNotFoundError: if the project directory does not exist.
            FileNotFoundError: if the template file does not exist.
        """
        if not path_to_file.is_file():
            raise TypeError('Please input path to a file.')
        elif not path_to_file.exists():
            raise FileNotFoundError(f'{path_to_file} does not exist.')
        elif self.proj_dir is None or not self.proj_dir.exists():
            raise FileNotFoundError('You need to create a project directory.')

        if template_name is None:
            template_name = path_to_file.name + '.template'

        path_temp = Path.cwd() / 'templates' / template_name

        if not path_temp.exists():
            raise FileNotFoundError(f'No {template_name} file template was'
                                    ' found in the current directory.')

        template_str = path_temp.open('r').read()
        template = Template(template_str)

        write_to_file = template.render(template_dict)

        with path_to_file.open('w') as main:
            main.write(write_to_file)

    def create_conda_env(self, yml_file_path: str or pathlib.PosixPath = None):
        """Creates a conda environment from a .yml file for a project.

        Args:
            yml_file_path (strorpathlib.PosixPath, optional):\
                [description]. Defaults to None. If None a new .yml file is \
                created using a environment.yml.template file from the \
                templates directory.

        Raises:
            TypeError: if the path provided is not an absolute path.
            TypeError: the path input is not to a .yml file.
            FileNotFoundError: if the path provided does not exist.
        """
        command = 'conda env create -f {} --prefix {}'
        create_loc = self.proj_dir / 'env'
        template_path = Path.cwd() / 'other-files'

        if yml_file_path is None:
            yml_file_path = template_path / 'environment.yml'

            if yml_file_path.exists():
                yml_file_path.unlink()

            self.create_file('environment.yml', template=True,
                             temp_dict={'env_name': str(create_loc)},
                             path=template_path)
        else:
            if not yml_file_path.is_absolute():
                raise TypeError(f'Path entered is not an absolute path.\n'
                                f'path: {yml_file_path}')
            if not yml_file_path.suffix == '.yml':
                raise TypeError(f'Path input is not to a .yml file.\n'
                                f'{yml_file_path}')

        if not yml_file_path.exists():
            raise FileNotFoundError(f'No .yml file found at {yml_file_path}')

        print(f'Creating conda environment at {create_loc}\n\n')
        os.system(command.format(yml_file_path, create_loc))

    def create_pipenv(self):
        command = 'python3 -m venv {}'
        create_loc = self.proj_dir / 'venv'

        print(f'Creating Pipenv environment at {create_loc}\n\n')
        os.system(command.format(create_loc))


def create_simple_project(path: str or pathlib.PosixPath = None):
    """Creates a simple project using the ProjectBuilder class.

    Notes:
        Creates the following files in the project directory:
        - {{ project_name }}.py : main python script
        - README.md
        - TODO.md
        - LICENSE : MIT License.
        - test_project.py : pytest python script
        - setup.py
        - .gitignore : basic python gitignore.
        - venv : python 3 virtual environment directory.

    Args:
        path (str or pathlib.PosixPath, optional): for class attribute 'path'.
                                                   Defaults to None.

    Returns:
        ProjectBuilder object: an instantiated ProjectBuilder class object
                               whose attributes can be used to locate the
                               project directory.
    """
    pb = ProjectBuilder(path=path)
    pb.create_proj_dir()

    files = ['README.md',
             'TODO.md',
             'LICENSE',
             'setup.py',
             '.gitignore']

    for filename in files:
        pb.create_file(filename=filename, template=True)

    # Create main python file
    filename = f'{pb.proj_name.replace("-","_").lower()}.py'
    pb.create_file(filename=filename, template=True,
                   temp_name='main.py.template')

    # Create test python file
    test_filename = 'test_' + filename
    pb.create_file(filename=test_filename, template=True,
                   temp_name='test_project.py.template')

    pb.create_pipenv()

    return pb


def create_ml_project(path: str or pathlib.PosixPath = None,
                      create_conda_env: bool = False):
    """Creates a basic layout for a machine learning project using
     ProjectBuilder class.

    Notes:
        Creates the following file structure:

        project_directory/
        |
        ├── data/
        |
        ├── tests/
        |   └── test_project.py: pytest python script
        |
        ├── notebooks/
        |   └── {{ project_name }}.ipynb: main jupyter notebook
        |
        ├── env/ : conda environment for the project
        |
        ├── README.md
        ├── TODO.md
        ├── LICENSE: MIT License.
        └── .gitignore: basic python gitignore.

    Args:
        path (str or pathlib.PosixPath, optional):\
            for class attribute 'path'. Defaults to None.

        create_conda_env (bool):\
            if True the function creates a conda environment in the project \
            folder. Default to False.

    Returns:
        ProjectBuilder object:
            an instantiated ProjectBuilder class object whose attributes can
             be used to locate the project directory.
    """
    ml_pb = ProjectBuilder(path=path)
    ml_pb.create_proj_dir()

    files = ['README.md',
             'TODO.md',
             'LICENSE',
             '.gitignore']

    for filename in files:
        ml_pb.create_file(filename=filename, template=True)

    dirs = ['data',
            'tests',
            'notebooks']

    for dir_name in dirs:
        ml_pb.create_dir(dir_name=dir_name)

    # Create main jupyter notebook.
    notebook = f'{ml_pb.proj_name.lower()}.ipynb'
    path = ml_pb.proj_dir / 'notebooks'
    ml_pb.create_file(filename=notebook, template=True,
                      temp_name='jupyter.ipynb.template',
                      path=path)

    # Create test python file
    name = ml_pb.proj_name.replace('-', '_').lower()
    test_filename = f'test_{name}.py'
    path = ml_pb.proj_dir / 'tests'

    ml_pb.create_file(filename=test_filename, template=True,
                      temp_name='test_project.py.template',
                      path=path)

    if create_conda_env:
        ml_pb.create_conda_env()

    return ml_pb


if __name__ == '__main__':
    # ml_pb = create_ml_project()
    pb = ProjectBuilder()
    pb.create_proj_dir()
    pb.create_pipvenv()
