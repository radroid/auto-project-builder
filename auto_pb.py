"""The goal of this module is to automate the process of creating directories
and files for a new project.

Update: The refactored code makes use of a class to modularise project
        building.
"""


import pathlib
from pathlib import Path
import re
from shutil import rmtree
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

    def create_dir(self):
        """The function creates a directory at the path specified and with the
        name input.

        Returns:
            pathlib.Posix object: This is the path to the directory created.
        """
        new_dir = self.path / self.proj_name
        new_dir.mkdir(exist_ok=True)
        self.proj_dir = new_dir
        print(f'Created directory: {new_dir}')
        return new_dir

    def create_readme(self):
        """The function creates a README.md file at the path specified.

        Returns:
            pathlib.Posix object: This is the path to the README.md file
                                  created.

        Raises:
            FileNotFoundError: if the no project directory is exists.
        """
        if self.proj_dir is None or not self.proj_dir.exists():
            raise FileNotFoundError('Please create a project directory before'
                                    'creating a README.md file.')

        readme = self.proj_dir / 'README.md'
        readme.touch()

        with readme.open('w') as write:
            write.write('Hello World!\n')

        print(f'Created README.md: {readme}')
        return readme

    def add_to_readme(self):
        """The function adds text to a README.md file.

        Notes:
            proj_name (str): name of the project, will be used as the main
                             heading in the README file
            author (str): name of the author, will be added at the bottom of
                          the README file.

        Raises:
            FileNotFoundError: if the path provided does not exists.
        """
        if not self.path.exists():
            raise FileNotFoundError('You need to create a project '
                                    'directory and README.md file.')
        elif self.proj_dir is None or not self.proj_dir.exists():
            raise FileNotFoundError('You need to create a README.md file.')

        path_temp = Path.cwd() / 'README.md.template'

        if not path_temp.exists():
            raise FileNotFoundError('No README.md file template was found in '
                                    'the current directory.')

        readme_temp_str = path_temp.open('r').read()
        readme_template = Template(readme_temp_str)

        template_dict = {'project_name': self.proj_name,
                         'author_name': self.author}
        text_to_write = readme_template.render(template_dict)

        path = self.proj_dir / 'README.md'
        with path.open('w') as readme:
            readme.write(text_to_write)

    def __delete_all__(self):
        rmtree(self.path)


if __name__ == '__main__':
    pb = ProjectBuilder()
    pb.create_dir()
    pb.create_readme()
    pb.add_to_readme()
