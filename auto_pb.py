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
            FileNotFoundError: if no project directory exists.
        """
        if self.proj_dir is None or not self.proj_dir.exists():
            raise FileNotFoundError('Please create a project directory before'
                                    'creating a README.md file.')

        readme = self.proj_dir / 'README.md'
        readme.touch()
        print(f'Created README.md: {readme}')

        self.__add_to_readme()
        print('Text added to README.md')

        return readme

    def __add_to_readme(self):
        """The function adds text to a README.md file.

        Raises:
            FileNotFoundError: if the path provided does not exists.
        """
        if not self.path.exists():
            raise FileNotFoundError('You need to create a project '
                                    'directory and README.md file.')
        elif self.proj_dir is None or not self.proj_dir.exists():
            raise FileNotFoundError('You need to create a README.md file.')

        path_temp = Path.cwd() / 'templates' / 'README.md.template'

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

    def create_todo(self):
        """The function creates a Todo.md file at the path specified.

        Returns:
            pathlib.Posix object: This is the path to the Todo.md file
                                  created.

        Raises:
            FileNotFoundError: if no project directory exists.
        """
        if self.proj_dir is None or not self.proj_dir.exists():
            raise FileNotFoundError('Please create a project directory before'
                                    'creating a TODO.md file.')

        todo = self.create_file('TODO.md', template=True)
        return todo

    def __add_to_todo(self):
        """The function adds text to a Todo.md file.

        Raises:
            FileNotFoundError: if the path provided does not exists.
        """
        if not self.path.exists():
            raise FileNotFoundError('You need to create a project '
                                    'directory and TODO.md file.')
        elif self.proj_dir is None or not self.proj_dir.exists():
            raise FileNotFoundError('You need to create a TODO.md file.')

        path_temp = Path.cwd() / 'templates' / 'TODO.md.template'

        if not path_temp.exists():
            raise FileNotFoundError('No TODO.md file template was found in '
                                    'the current directory.')

        todo_temp_str = path_temp.open('r').read()
        todo_template = Template(todo_temp_str)

        template_dict = {'project_name': self.proj_name}
        text_to_write = todo_template.render(template_dict)

        path = self.proj_dir / 'TODO.md'
        with path.open('w') as todo:
            todo.write(text_to_write)

    def create_main(self):
        """The function creates a {{proj_name}}.py file at the path specified.

        Returns:
            pathlib.Posix object: This is the path to the {{proj_name}}.py file
                                  created.

        Raises:
            FileNotFoundError: if no project directory exists.
        """
        if self.proj_dir is None or not self.proj_dir.exists():
            raise FileNotFoundError(f'Please create a project directory before'
                                    f'creating a {self.proj_name} file.')

        main = self.proj_dir / f'{self.proj_name}.py'
        main.touch()
        print(f'Created {self.proj_name}: {main}')

        self.__add_to_todo()
        print('Text added to TODO.md')

        return main

    def __add_to_main(self):
        """The function adds text to a {{proj_name}}.py file.

        Raises:
            FileNotFoundError: if the path provided does not exists.
        """
        if not self.path.exists():
            raise FileNotFoundError(f'You need to create a project '
                                    f'directory and {self.proj_name}.py file.')
        elif self.proj_dir is None or not self.proj_dir.exists():
            raise FileNotFoundError(f'You need to create a {self.proj_name}.py'
                                    ' file.')

        path_temp = Path.cwd() / 'templates' / 'main.py.template'

        if not path_temp.exists():
            raise FileNotFoundError('No main.py file template was'
                                    ' found in the current directory.')

        main_temp_str = path_temp.open('r').read()
        main_template = Template(main_temp_str)

        template_dict = {'project_name': self.proj_name}
        text_to_write = main_template.render(template_dict)

        path = self.proj_dir / f'{self.proj_name}.py'
        with path.open('w') as main:
            main.write(text_to_write)

    def create_file(self, filename: str, template: bool = False,
                    temp_dict: dict = {}, temp_name: str = None,
                    path: str or pathlib.PosixPath = None):
        """Creates a file at a given path and a given name.

        Args:
            filename (str): name of the file to created.
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

        Raises:
            FileNotFoundError: if no project directory exists.
            FileNotFoundError: if the path input does not exist.

        Returns:
            pathlib.PosixPath: path to the file created.
        """
        if self.proj_dir is None or not self.proj_dir.exists():
            raise FileNotFoundError(f'Please create a project directory before'
                                    f'creating a {filename} file.')

        if path is None:
            path = self.proj_dir

        if type(path) == str:
            path = self.proj_dir / path

        if not path.exists() or not path.is_dir():
            raise FileNotFoundError(f'No directory exists at {path}')

        file_path = path / filename
        file_path.touch()
        print(f'Created {filename}: {file_path}')

        if len(temp_dict) == 0:
            temp_dict = {'project_name': self.proj_name,
                         'author_name': self.author}

        if template:
            self.__add_to_file(path=file_path, template_dict=temp_dict,
                               name=temp_name)
            print(f'Text added to {filename}')

        return file_path

    def __add_to_file(self, path: pathlib.PosixPath, template_dict: dict,
                      name: str):
        """Add to a file from a template stored in the templates directory.

        Args:
            path (pathlib.PosixPath): path to the file that needs to be
                                      updated.
            template_dict (dict): used to customise parts of the template.
                                  The variable names matching a key in the
                                  dict will be replaced with the respective
                                  value.
            name (str): name of the template file in the templates
                        directory. Defaults to None.

        Raises:
            FileNotFoundError: if the path input does not exist.
            FileNotFoundError: if the project directory does not exist.
            FileNotFoundError: if the template file does not exist.
        """
        if not path.exists():
            raise FileNotFoundError(f'You need to create a project '
                                    f'directory and {self.proj_name}.py file.')
        elif self.proj_dir is None or not self.proj_dir.exists():
            raise FileNotFoundError(f'You need to create a {self.proj_name}.py'
                                    ' file.')

        if name is None:
            name = path.name + '.template'

        path_temp = Path.cwd() / 'templates' / name

        if not path_temp.exists():
            raise FileNotFoundError('No main.py file template was'
                                    ' found in the current directory.')

        template_str = path_temp.open('r').read()
        template = Template(template_str)

        write_to_file = template.render(template_dict)

        with path.open('w') as main:
            main.write(write_to_file)


def create_simple_project():
    """Creates a simple project using the ProjectBuilder class.

    Returns:
        ProjectBuilder object: an instantiated ProjectBuilder class object
                               whose attributes can be used to locate the
                               project directory.
    """
    pb = ProjectBuilder()
    pb.create_dir()

    files = ['README.md',
             'TODO.md']

    for filename in files:
        pb.create_file(filename=filename, template=True)

    pb.create_file(filename=f'{pb.proj_name}.py', template=True,
                   temp_name='main.py.template')

    return pb


if __name__ == '__main__':
    pb = ProjectBuilder()
    pb.create_dir()
    pb.create_readme()
    pb.create_todo
    pb.create_main
