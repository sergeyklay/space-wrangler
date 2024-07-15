# Contributing

If you would like to contribute to Confluence Space Management Toolkit, please 
take a look at the 
[current issues](https://github.com/airslateinc/confluence-maintenance-tools/issues). 
If there is a bug or feature that you want, but it isn't listed, make an issue 
and work on it.

## Bug reports

*Before raising an issue, please ensure that you are using the latest version 
of Confluence Space Management Toolkit.*

Please provide the following information with your issue to enable a quick
response:

* The relevant versions of the packages you are using.
* The steps to recreate your issue.
* The full stacktrace if there is an exception.
* An executable code example where possible.

### Feature requests

Feature requests are welcome. Ensure your idea fits within the scope and aims of
the project. Provide as much detail and context as possible.

### Pull requests

To have your work considered for inclusion in the project:

1. Check for open issues or open a new issue to start a discussion around a
   feature idea or a bug.
2. Clone the repository on GitHub to start making your changes to the `main`
   branch (or branch off of it).
3. Write a test to show that the bug was fixed or that the feature works as
   expected.
4. Ensure that all new code is properly type-annotated.
5. Send a pull request.

**By submitting a patch, you agree to allow the project owner to license your 
work under the same license as that used by the project.**

## Coding Standards

### Supported Systems and Python Versions

All contributions must ensure compatibility with Linux and macOS. The code should
support all currently supported Python versions as listed in the project's GitHub
workflow.

### Line Length

In both code and documentation, we avoid using lines longer than 79 characters
unless there is a clear, obvious, and justified reason to do otherwise. For
documentation, the line length can be 80 characters or slightly varied, but
it's best to aim for 79 characters. This helps maintain readability and
consistency throughout the project.

### Language

All comments in the code, any user-facing text such as log output, and all
docstrings must be written in English. This ensures consistency and
accessibility for all contributors and users of the project.

### Documentation and Testing Requirements

No code can be without documentation. Please provide documentation for any new
functionality you propose. Additionally, no functionality can be left untested.
Ensure that you write tests covering both negative and positive cases.

### Typing Requirements

All new code must be properly type-annotated. This includes:

- Function signatures (both parameters and return types)
- Class attributes
- Any complex data structures used within functions or methods

Using type annotations helps improve code readability, maintainability, and
correctness by:

- **Improving code clarity:** Type annotations make it immediately clear what
  type of data is expected, reducing misunderstandings and errors.
- **Enhancing IDE support:** Many modern IDEs use type annotations to provide
  better code completion, error checking, and refactoring tools.
- **Facilitating static analysis:** Tools like `mypy` can use type annotations
  to detect potential bugs before runtime, ensuring more robust and error-free code.
- **Promoting better documentation:** Type annotations serve as an inline form
  of documentation, providing valuable information to other developers working
  on the project.

### Docstring Style Guide

All docstrings in this project should follow the Google style guide. Here are 
some examples:

### Function Example

```python
def example_function(param1: int, param2: str) -> bool:
    """Function description.

    Args:
        param1 (int): Description of param1.
        param2 (str): Description of param2.

    Returns:
        bool: Description of the return value.
    """
    return True
```

### Class Example

```python
class ExampleClass:
    """Class description.

    Attributes:
        attr1 (int): Description of attr1.
        attr2 (str): Description of attr2.
    """

    def __init__(self, attr1: int, attr2: str) -> None:
        """Initialize ExampleClass.

        Args:
            attr1 (int): Description of attr1.
            attr2 (str): Description of attr2.
        """
        self.attr1 = attr1
        self.attr2 = attr2
```

Make sure to include all relevant details in your docstrings, such as parameter
descriptions and return values. This helps maintain consistency and readability
throughout the codebase.

## Resources

* [How to Contribute to Open Source](https://opensource.guide/how-to-contribute/)
* [Using Pull Requests](https://help.github.com/articles/about-pull-requests/)
* [Writing good commit messages](http://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html)
* [Google Python Style Guide: 3.8 Comments and Docstrings](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings)
* [PEP 484: Type Hints](https://www.python.org/dev/peps/pep-0484/)
* [Mypy: Optional Types](https://mypy.readthedocs.io/en/stable/kinds_of_types.html#optional-types)
