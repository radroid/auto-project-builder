"""The goal of this module is to automate the process of creating directories
and files for a new project.

Update: The refactored code makes use of a class to modularise project
        building.
"""


import pathlib
from pathlib import Path
import re
from jinja2 import Template


class ProjectBuilder:
    """The class manages the newly created project folder.

    Attributes:
        proj_name (str): name of project entered by the user.
        author_name (str): name of the author entered by the user.
        path (pathlib.PosixPath): path to the directory where the project
                                  directory is to be created.
        proj_dir (pathlib.PosixPath): path to the project directory.
    """

    def __init__(self, path: str or pathlib.PosixPath = None):
        """Instantiate an object.

        Args:
            path (str or pathlib.PosixPath, optional): for class attribute
                                                       'path'. Defaults to
                                                       None.

        Raises:
            FileNotFoundError: if the path provided does not exist.
            TypeError: if the path provided is not a directory.
        """
        if path is None:
            path = Path.cwd().parent
        else:
            if type(path) == str:
                path = Path(path)

            if not path.exists():
                raise FileNotFoundError('The path provided, does not exist.')
            if not path.is_dir():
                raise TypeError('Please input a path to a directory.')

        self.path = path
        self.proj_dir = None
        self.proj_name, self.author = self.get_names()

    def get_names(self):
        """Take input from user for the project name and author name. Print out
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
            path (strorpathlib.PosixPath): path where the file/directory is to
                                           be created.
            filename (str): name of the file/directory to be created.

        Raises:
            FileNotFoundError: if no project directory exists.
            FileNotFoundError: if the path input does not exist.
            FileExistsError: if the file to be created exists at the path
                             provided.

        Returns:
            pathlib.PosixPath: path with the filename (without if if None).
        """
        if self.proj_dir is None or not self.proj_dir.exists():
            raise FileNotFoundError(f'Please create a project directory before'
                                    f'creating a {filename} file.')

        if path is None:
            path = self.proj_dir
        elif type(path) == str:
            path = Path(path)

        if not path.is_dir():
            raise FileNotFoundError(f'No directory exists at {path}')

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
        proj_dir.mkdir(exist_ok=True)
        self.proj_dir = proj_dir
        print(f'Created directory: {proj_dir}')
        return proj_dir

    def create_dir(self, dir_name: str, path: str or pathlib.PosixPath = None):
        """The function creates a directory at the path specified and with the
        name input.

        Args:
            dir_name (str): name of the directory to be created.
            path (pathlib.PosixPath or str, optional): path or directory name
                                                       inside the project
                                                       directory where the
                                                       file needs to be
                                                       created.
                                                       Defaults to None.

        Returns:
            pathlib.Posix object: This is the path to the directory created.
        """
        new_dir = self.valid_path(path, dir_name)
        new_dir.mkdir(exist_ok=True)
        print(f'Created directory: {new_dir}')
        return new_dir

    def create_file(self, filename: str, template: bool = False,
                    temp_dict: dict = {}, temp_name: str = None,
                    path: str or pathlib.PosixPath = None):
        """Creates a file at a given path and a given name.

        Args:
            filename (str): name of the file to be created.
            template (bool, optional): True if there if the file needs to
                                       contain data contained in its template.
                                       Defaults to False.
            temp_dict (dict, optional): used to customise parts of the template
                                        The variable names matching a key in
                                        the dict will be replaced with the
                                        respective value. Defaults to {}.
            temp_name (str, optional): name of the template file in the
                                       templates directory. Defaults to None.
            path (pathlib.PosixPath or str, optional): path or directory name
                                                       inside the project
                                                       directory where the
                                                       file needs to be
                                                       created.
                                                       Defaults to None.

        Returns:
            pathlib.PosixPath: path to the file created.
        """
        file_path = self.valid_path(path, filename)
        file_path.touch()
        print(f'Created {filename}: {file_path}')

        if len(temp_dict) == 0:
            temp_dict = {'project_name': self.proj_name,
                         'author_name': self.author}

        if template:
            self.__add_to_file(path=file_path, template_dict=temp_dict,
                               template_name=temp_name)
            print(f'Text added to {filename}')
        print('')

        return file_path

    def __add_to_file(self, path: pathlib.PosixPath, template_dict: dict,
                      template_name: str):
        """Add to a file from a template stored in the templates directory.

        Args:
            path (pathlib.PosixPath): path to the file that needs to be
                                      updated.
            template_dict (dict): used to customise parts of the template.
                                  The variable names matching a key in the
                                  dict will be replaced with the respective
                                  value.
            template_name (str): template_name of the template file in the
                                 templates directory. Defaults to None.

        Raises:
            TypeError: if the path input is not to a file.
            FileNotFoundError: if the path input does not exist.
            FileNotFoundError: if the project directory does not exist.
            FileNotFoundError: if the template file does not exist.
        """
        if not path.is_file():
            raise TypeError('Please input path to a file.')
        elif not path.exists():
            raise FileNotFoundError(f'{path} does not exist.')
        elif self.proj_dir is None or not self.proj_dir.exists():
            raise FileNotFoundError('You need to create a project directory.')

        if template_name is None:
            template_name = path.name + '.template'

        path_temp = Path.cwd() / 'templates' / template_name

        if not path_temp.exists():
            raise FileNotFoundError('No main.py file template was'
                                    ' found in the current directory.')

        template_str = path_temp.open('r').read()
        template = Template(template_str)

        write_to_file = template.render(template_dict)

        with path.open('w') as main:
            main.write(write_to_file)


def create_simple_project(path: str or pathlib.PosixPath = None):
    """Creates a simple project using the ProjectBuilder class.

    Notes:
        Creates the following files:
        - {{ project_name }}.py: main python script
        - README.md
        - TODO.md
        - LICENSE: MIT License.
        - test_project.py: pytest python script
        - setup.py
        - .gitignore: basic python gitignore.

    Args:
        path (str or pathlib.PosixPath, optional): for class attribute 'path'.
                                                   Defaults to None.

    Returns:
        ProjectBuilder object: an instantiated ProjectBuilder class object
                               whose attributes can be used to locate the
                               project directory.
    """
    pb = ProjectBuilder()
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

    return pb


if __name__ == '__main__':
    create_simple_project()
