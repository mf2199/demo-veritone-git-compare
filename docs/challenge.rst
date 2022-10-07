=============
The Challenge
=============

At Veritone, we want to help developers ensuring our build process and tools are
efficient and innovative. One common task is compiling a list of Git commit
messages between two commits or versions. The output should be helpful for our
customer success team to allow them to know the issues fixed between two
versions of our code.

Create a script or tool in Bash, Python, Golang, Node.JS that would allow you to
compare two GitHub commits. The created tool should take the GitHub
organization, repository name, head commit, and base commit as inputs. The
solution should take advantage of the GitHub API (documentation located at
https://docs.github.com/en/rest).

In addition, leverage GitHub Actions to create a build and test pipeline for the
tool you produce. The tests should ensure that your solution is working before
each pull request merge. Documentation for GitHub Actions is at
https://docs.github.com/en/actions.


Guidelines
----------

* The tool should be written in one of the following languages:

    - Bash
    - Python
    - Golang
    - Node.JS

* Utilize the GitHub API for the solution

* The tool's parameters should be the following:

    - GitHub organization
    - Repository Name
    - Head commit
    - Base commit

Deliverables
------------

Via Github, please provide the following:
* The code you wrote with the build and test pipeline

Requirements
------------

For the tool

* The code should be reusable
* We want to use GitHub Personal Access Tokens for access to the GitHub API

For tests:

* Fail the pipeline if the tests fail.
* Are you testing negative cases as well?

What we are looking for
-----------------------

1. Correctness - will your solution produce the desired results
2. Conciseness - does your solution balance clarity and brevity
3. Maintainability - does your code stand up to changing needs
4. Automation - does your pipeline ensure that the tool performs as expected
5. Anti-patterns - does your solution avoid anti-patterns

What to expect
--------------

After you submit your work, our team will review it. If the solution matches
what we are looking for, we will schedule a time to discuss the solution with
you. During this time we will ask you to share your screen and potentially do
some modifications.
