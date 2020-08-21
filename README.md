# Auto Project Builder
The aim is to automate the repetitive task of creating directories and files for a new project. Refer to the [Milestones](https://github.com/radroid/auto-project-builder/milestones) section to better understand the features and scope of the project.

[![You didn't ask](https://forthebadge.com/images/badges/you-didnt-ask-for-this.svg)](https://forthebadge.com) 
[![Powered by](https://forthebadge.com/images/badges/powered-by-responsibility.svg)](https://forthebadge.com) 
[![for real](https://forthebadge.com/images/badges/fo-real.svg)](https://forthebadge.com)

Function:
```python 
create_simple_project()
```
Project created by the above function:
``` 
projectname/
│
├── project_name.py
├── LICENSE
├── TODO.md
└── README.md
```

## Usage for Mac/Linux Users

**Prerequisites:**
- You know the basics of using terminal on Mac/Linux.
  * How to use `cd` to change the current directory
  * Use `ls` to list directories in the current directory.
- You have the latest version of python installed.

1. Clone this repository into your projects folder, i.e. the folder you would like to create projects in.

> *Note: use `cd` command to navigate to your projects directory.*

```bash
git clone www.github.com/radoid/auto-project-builder.git
```

2. Create a virtual environment in the auto-project-builder directory.
```bash
cd auto-project-builder
python3 -m venv pb_venv
```

3. Activate environment and install the required modules.

> *Note: check your python version by using `python --version`.*

```bash
source pb_venv/bin/activate
pip install -r requirements.txt
```

4. Activate python in the terminal window.
```bash
python
```

5. Use the `auto_pb` module to create a simple project.
> *Note: the following was written after completion of the first iteration of this project. 
> More functions may be added since then.

```python
from auto_pb import create_simple_project

# pb is an instance (object) of the ProjectBuilder class.
pb = create_simple_project()

# print the paths.
print(f'Path to the folder containing the project folder: {pb.path}')
print(f'Path to the project folder: {pb.proj_path}')
```
> You can 
- modify the templates to suit your style.
- go through the ProjectBuilder class to add your own functionality.
- collaborate with me to improve the project. :smiley:

## Contributing
There are **Two ways** to do this:
1. Collaborate
2. Code Review

### Code Review
> I will be mentioning your name in the `Contribution` section* for helpful and constructive feedback.

I would really appreciate any kind of feedback on the way I have chosen to tackle this problem. Keep in mind, I am a beginner and even a small piece of advice can go a long way. **Be as critical as you can!** Thank you for spending time to look at my code.

The best way to start is by going through the example codes in `hangman/examples`.
I would appreciate comments on anything and everything, but here are some to get you started:
- Architecture or **Design** of the code.
- Style and **Documentation**.
- **Testing**: this one can be get time consuming compared to the others.

You can refer to [this guide](https://www.kevinlondon.com/2015/05/05/code-review-best-practices.html) for advice on Code Reviews.
* I will be creating a `Contributions through Code Reviews` section.

## Support
I am looking for a job ooportunity in Canada. It would mean a lot if we could connect and discuss what we can do for each other.
Follow and Reach out to me one of the following places!

![Github Follow](https://img.shields.io/github/followers/radroid?label=Follow&style=social) ![Twitter Follow](https://img.shields.io/twitter/follow/Raj_Dholakia001?label=Follow&style=social)


## License

[![License](https://img.shields.io/github/license/radroid/Hangman?style=for-the-badge)](https://github.com/radroid/Hangman/blob/master/LICENSE)

**[MIT license](https://opensource.org/licenses/MIT)**
