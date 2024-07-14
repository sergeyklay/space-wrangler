# Contributing

If you would like to contribute to Confluence Space Management Toolkit, please 
take a look at the 
[current issues](https://github.com/airslateinc/confluence-maintenance-tools/issues). 
If there is a bug or feature that you want, but it isn't listed, make an issue 
and work on it.

## Bug reports

*Before raising an issue, please ensure that you are using the latest version 
of Confluence Space Management Toolkit.*

Please provide the following information with your issue to enable me to 
respond as quickly as possible.

* The relevant versions of the packages you are using.
* The steps to recreate your issue.
* The full stacktrace if there is an exception.
* An executable code example where possible

Guidelines for bug reports:

* **Use the GitHub issue search** — check if the issue has already been 
  reported.
* **Check if the issue has been fixed** — try to reproduce it using the latest 
  `main` branch in the repository.
* **Isolate the problem** — create a reduced test case and a live example.

A good bug report shouldn't leave others needing to chase you up for more 
information. Please try to be as detailed as possible in your report. What is 
your environment? What steps will reproduce the issue? What OS experience the 
problem? What would you expect to be the outcome? All these details will help 
people to fix any potential bugs.

### Feature requests

Feature requests are welcome. But take a moment to find out whether your idea 
fits with the scope and aims of the project. It's up to *you* to make a strong 
case to convince the project's developers of the merits of this feature. Please 
provide as much detail and context as possible.

### Pull requests

Good pull requests - patches, improvements, new features - are a fantastic 
help. They should remain focused in scope and avoid containing unrelated 
commits.

Follow this process if you'd like your work considered for inclusion in the 
project:

1. Check for open issues or open a fresh issue to start a discussion around a 
   feature idea or a bug.
2. Clone the repository on GitHub to start making your changes to the `main` 
   branch (or branch off of it).
3. Write a test which shows that the bug was fixed or that the feature works as 
   expected.
4. Send a pull request and bug the maintainer until it gets merged and published.

If you are intending to implement a fairly large feature I'd appreciate if you 
open an issue with GitHub detailing your use case and intended solution to 
discuss how it might impact other work that is in flight.

I also appreciate it if you take the time to update and write tests for any 
changes you submit.

**By submitting a patch, you agree to allow the project owner to license your 
work under the same license as that used by the project.**

## Docstring Style Guide

All docstrings in this project should follow the Google style guide. Here are 
some examples:

### Function Example

```python
def example_function(param1, param2):
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

    def __init__(self, attr1, attr2):
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
