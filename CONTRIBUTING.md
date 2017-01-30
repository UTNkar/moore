# Contributing to Project Moore

:+1::tada: First off, thanks for considering to contribute! :tada::+1:

The following is a set of guidelines for contributing to Project Moore. These
are just guidelines, not rules. Use your best judgment, and feel free to propose
changes to this document in a pull request.

#### Table Of Contents

[What should I know before I get
started?](#what-should-i-know-before-i-get-started)

[How Can I Contribute?](#how-can-i-contribute)
  * [Reporting Bugs](#reporting-bugs)
  * [Suggesting Enhancements](#suggesting-enhancements)
  * [Your First Code Contribution](#your-first-code-contribution)
  * [Pull Requests](#pull-requests)

[Styleguides](#styleguides)
  * [Git Commit Messages](#git-commit-messages)
  * [Python Styleguide](#python-styleguide)
  * [Documentation Styleguide](#documentation-styleguide)

[Additional Notes](#additional-notes)
  * [Issue and Pull Request Labels](#issue-and-pull-request-labels)

## What should I know before I get started?

Project Moore is a project started by [UTN](https://utn.se/). You free to use,
improve and distribute our code. We do ask that you publish your respective
code. Furthermore, UTN board and management team decides the direction of the
project. These decisions are upheld by the UTN system administrator. In any
dispute their decision is final, but you're free to debate your case.

## How Can I Contribute?

### Reporting Bugs

This section guides you through submitting a bug report for Project Moore.
Following these guidelines helps maintainers and the community understand your
report :pencil:, reproduce the behavior :computer:, and find related reports
:mag_right:.

Before creating bug reports, please check [this
list](#before-submitting-a-bug-report) as you might find out that you don't need
to create one. When you are creating a bug report, please [include as many
details as possible](#how-do-i-submit-a-good-bug-report). Fill out [the required
template](.github/ISSUE_TEMPLATE.md), the information it asks for helps us
resolve issues faster.

#### Before Submitting A Bug Report

* **Clear your cache** to ensure the problem isn't caused by old files in your
browser.
* **Perform a [cursory search](https://github.com/UTNkar/moore/issues)** to see
if the problem has already been reported. If it has, add a comment to the
existing issue instead of opening a new one.

#### How Do I Submit A (Good) Bug Report?

Bugs are tracked as [GitHub issues](https://guides.github.com/features/issues/).
After you've found a new bug, create an
[issue](https://github.com/UTNkar/moore/issues) following information by filling
in [the template](ISSUE_TEMPLATE.md).

Explain the problem and include additional details to help maintainers reproduce
the problem:

* **Use a clear and descriptive title** for the issue to identify the problem.
* **Describe the exact steps which reproduce the problem** in as many details as
possible. For example, start by explaining how opened the page, e.g. which
program/browser you used.
* **Describe the behavior you observed after following the steps** and point out
what exactly is the problem with that behavior.
* **Explain which behavior you expected to see instead and why.**
* **Include screenshots and animated GIFs** which show you following the
described steps and clearly demonstrate the problem if possible. You can use
[this tool](http://www.cockos.com/licecap/) to record GIFs on macOS and
Windows, and [this tool](https://github.com/colinkeenan/silentcast) or [this
tool](https://github.com/GNOME/byzanz) on Linux.
* **If the problem is related to performance**, include a performance profile,
available in all major browsers.
* **If the problem wasn't triggered by a specific action**, describe what you
were doing before the problem happened and share more information using the
guidelines below.

Provide more context by answering these questions:

* **Did the problem start happening recently** or was this always a problem?
* **Can you reliably reproduce the issue?** If not, provide details about how
often the problem happens and under which conditions it normally happens.
* **What's the name and version of the OS you're using**?


### Suggesting Enhancements

This section guides you through submitting an enhancement suggestion for Project
Moore, including completely new features and minor improvements to existing
functionality. Following these guidelines helps us to understand your suggestion
:pencil: and find related suggestions :mag_right:.

Before creating enhancement suggestions, please check [this
list](#before-submitting-an-enhancement-suggestion) as you might find out that
you don't need to create one. When you are creating an enhancement suggestion,
please [include as many details as
possible](#how-do-i-submit-a-good-enhancement-suggestion). Fill in [the
template](ISSUE_TEMPLATE.md), including the steps that you imagine you would
take if the feature you're requesting existed.

#### Before Submitting An Enhancement Suggestion

* **Perform a [cursory search](https://github.com/UTNkar/moore/issues)** to see
if the enhancement has already been suggested. If it has, add a comment to the
existing issue instead of opening a new one.

#### How Do I Submit A (Good) Enhancement Suggestion?

Enhancement suggestions are tracked as [GitHub
issues](https://guides.github.com/features/issues/). Create an
[issue](https://github.com/UTNkar/moore/issues) and provide the following
information:

* **Use a clear and descriptive title** for the issue to identify the
suggestion.
* **Provide a step-by-step description of the suggested enhancement** in as many
details as possible.
* **Provide specific examples to demonstrate the steps**.
* **Describe the current behavior** and **explain which behavior you expected to
see instead** and why.
* **Include screenshots and animated GIFs** which help you demonstrate the steps
or point out the part of Project Moore which the suggestion is related to. You
can use [this tool](http://www.cockos.com/licecap/) to record GIFs on macOS
and Windows, and [this tool](https://github.com/colinkeenan/silentcast) or
[this tool](https://github.com/GNOME/byzanz) on Linux.
* **Explain why this enhancement would be useful**.
* **List some other websites or applications where this enhancement exists.**

### Your First Code Contribution

Unsure where to begin contributing to Project Moore? You can start by looking
through the `help-wanted` issues. [Help wanted issues][help-wanted] are issues
that don't require a full understanding of Project Moore or the Django
framework, but can guide you in to the development process.

If you want to get more involved in the development, but still don't know where
to start, then please contact the [UTN
system administrator](mailto:admin@utn.se). He will help you get started.

### Pull Requests

* Fill in [the required template](PULL_REQUEST_TEMPLATE.md)
* Include screenshots and animated GIFs in your pull request whenever possible.
* Follow the repository [styleguides](#styleguides).
* End files with a newline.

## Styleguides

### Git Commit Messages

* Use the present tense ("Add feature" not "Added feature")
* Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
* Limit the first line to 72 characters or less
* Reference issues and pull requests liberally
* When only changing documentation, include `[ci skip]` in the commit description
* Consider starting the commit message with an applicable emoji:
    * :triangular_ruler: `:triangular_ruler:` when improving the format/structure of the code
    * :art: `:art:` when improving templates
    * :racehorse: `:racehorse:` when improving performance
    * :memo: `:memo:` when writing docs
    * :bug: `:bug:` when fixing a bug
    * :fire: `:fire:` when removing code or files
    * :green_heart: `:green_heart:` when fixing the CI build
    * :white_check_mark: `:white_check_mark:` when adding tests
    * :lock: `:lock:` when dealing with security
    * :arrow_up: `:arrow_up:` when upgrading dependencies
    * :arrow_down: `:arrow_down:` when downgrading dependencies
    * :shirt: `:shirt:` when removing linter warnings

### Python Styleguide

* Always adhere to the [PEP8
styleguide](https://www.python.org/dev/peps/pep-0008/).
* The closing of a multi-line constructs should match the first character of the
first line of this construct.
* Separate import statements.
    * Not: `import sys, os`
* When using multi-line equations, break before the binary operator.

### Documentation Styleguide

* Use [Documentation
String](https://docs.python.org/3/tutorial/controlflow.html#tut-docstrings).
* Use [Type
Annotations](https://docs.python.org/3/tutorial/controlflow.html#function-annotations)
whenever possible.
* All functions/methods, classes, and modules should be documented in a clear
way with references to other relevant code.

#### Example

```python
def function_with_pep484_type_annotations(param1: int, param2: str) -> bool:
    """Example function with PEP 484 type annotations.

    Args:
        param1: The first parameter.
        param2: The second parameter.

    Returns:
        The return value. True for success, False otherwise.

    """
    return param1 == param2
```

## Additional Notes

### Issue and Pull Request Labels

This section lists the labels we use to help us track and manage issues and pull
requests.

[GitHub search](https://help.github.com/articles/searching-issues/) makes it
easy to use labels for finding groups of issues or pull requests you're
interested in. To help you find issues and pull requests, each label is listed
with search links for finding open items with that label. We  encourage you to
read about [other search
filters](https://help.github.com/articles/searching-issues/) which will help you
write more focused queries.

The labels are loosely grouped by their purpose, but it's not required that
every issue have a label from every group or that an issue can't have more than
one label from the same group.

Please open an issue if you have suggestions for new labels, and if you notice
some labels are missing on some repositories, then please open an issue on that
repository.

#### Type of Issue and Issue State

| Label name | Description |
| --- | --- |
| `enhancement` | Feature requests. |
| `bug` | Confirmed bugs or reports that are very likely to be bugs. |
| `question` | Questions more than bug reports or feature requests (e.g. how do I do X). |
| `feedback` | General feedback more than bug reports or feature requests. |
| `help-wanted` | The UTN system administrator would appreciate help others in resolving these issues. |
| `more-information-needed` | More information needs to be collected about these problems or feature requests (e.g. steps to reproduce). |
| `needs-reproduction` | Likely bugs, but haven't been reliably reproduced. |
| `duplicate` | Issues which are duplicates of other issues, i.e. they have been reported before. |
| `wontfix` | The UTN system administrator has decided not to fix these issues for now, either because they're working as intended or for some other reason. |
| `invalid` | Issues which aren't valid (e.g. user errors). |

#### Topic Categories

| Label name | Description |
| --- | --- |
| `documentation` | Related to any type of documentation. |
| `performance` | Related to performance. |
| `security` | Related to security. |
| `ui` | Related to visual design. |

#### Pull Request Labels

| Label name | Description
| --- | --- |
| `work-in-progress` | Pull requests which are still being worked on, more changes will follow. |
| `needs-review` | Pull requests which need code review, and approval. |
| `requires-changes` | Pull requests which need to be updated based on review comments and then reviewed again. |
| `needs-testing` | Pull requests which need manual testing. |

[help-wanted]:https://github.com/UTNkar/moore/labels/help-wanted
