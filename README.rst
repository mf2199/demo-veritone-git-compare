Commit Comparing Tool
=====================

Helllo and thank you for taking time to review this demo. The code addresses
the challenge sent as a part of the recruiting process and was written
primarily for demonstration purposes.

An Overview
-----------

The core functionality is contained within the `compare.py`_ script located in
the `src`_ folder, that can be executed from either command line interface or
via programmatic access to the public `compare` method. The script utilizes
GitHub API to perform `git diff` operation and saves the result into a local
folder.

.. _`compare.py`: https://github.com/mf2199/demo-veritone-git-compare/blob/dev/src/compare.py
.. _`src`: https://github.com/mf2199/demo-veritone-git-compare/tree/dev/src

Basic Usage - Command Line
--------------------------

The script requires a minimum of three CLI arguments:

 - `--repo` - The name of the source repository;
 - `--base` - The SHA code of the base branch;
 - `--head` - The SHA code of the head branch;

In addition to that the script will need the GitHub organization (account) name
and a Personal Access Token which can be obtained by following these
`instructions`_. Both values need to be stored locally in a JSON format in a
secrets file `credentials.json` which has the following structure:

.. code-block::

    {
      "gh_account": <the-github-account-name>,
      "gh_pat": <access-token>
    }

.. _`instructions`: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token

An example usage:

.. code-block:: console

    python src/compare.py --repo <repo-name> --base <base-SHA> --head <head-SHA>

Additional Options
------------------

For better flexibility, two more command line options were added:

 - `--file` - Will override the outputs path and allow storing the results in a
   custom location;
 - `--debug` - This option provides additional logging output and can be used
   for debugging purposes.

API Access
----------

The results can also be obtained by invoking the `compare` method directly using
the same arguments as with the command line usage. The function will then return
a `Response` object containing the `diff` information along with the
concomitant metadata.

The Pipeline
------------

This repository unitilzes GitHub Actions for error-checking the code before
accepting submissions. The pipeline runs a series of unit and system tests along
with code format and style checks according to the published `PEP8 guidelines`_.

.. _`PEP8 guidelines`: https://peps.python.org/pep-0008/

