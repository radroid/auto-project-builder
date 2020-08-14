"""The goal of this module is to automate the process of creating directories
and files for a new project."""


def get_names():
    """Take input from user for the project name and author name. Print out
    the information provided.

    Returns (Tuple):
        proj_name (str): name of project entered by the user.
        author_name (str): name of the author entered by the user.
    """
    print('\n> What would you like to name your project?')
    proj_name = input()
    print('\n> Who is the author of the project? '
          '(Enter full name of the author)')
    author_name = input()

    print('\n### Project Details ###')
    print(f'Project name: {proj_name}')
    print(f'Author\'s name: {author_name}\n')
    return proj_name, author_name
