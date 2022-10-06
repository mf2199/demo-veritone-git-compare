# -*- coding: utf-8 -*-

from __future__ import absolute_import
import os
import pathlib

import nox

BLACK_VERSION = "black==22.3.0"
ISORT_VERSION = "isort==5.10.1"
LINT_PATHS = ["docs", "tests", "noxfile.py"]

DEFAULT_PYTHON_VERSION = "3.8"

UNIT_TEST_PYTHON_VERSIONS = ["3.7", "3.8", "3.9", "3.10"]
UNIT_TEST_DEPENDENCIES = [
    "colorama",
    "mock",
    "pytest",
    "pytest-cov",
    "requests",
]

SYSTEM_TEST_PYTHON_VERSIONS = ["3.8"]
SYSTEM_TEST_DEPENDENCIES = [
    "mock",
    "pytest",
]

CURRENT_DIRECTORY = pathlib.Path(__file__).parent.absolute()

BLACK_MAX_LINE_LENGTH = "79"

nox.options.sessions = [
    "unit",
    "system",
    "mypy",
    "cover",
    "lint",
    "blacken",
]

# Error if a Python version is missing
nox.options.error_on_missing_interpreters = False

nox.options.reuse_existing_virtualenvs = True


@nox.session(python=DEFAULT_PYTHON_VERSION)
def lint(session):
    """Run linters.

    Returns a failure if the linters find linting errors or sufficiently
    serious code quality issues.
    """
    session.install("flake8", BLACK_VERSION)
    session.run("black", "--check", "-l", BLACK_MAX_LINE_LENGTH, *LINT_PATHS)
    session.run("flake8", "src", "tests")


@nox.session(python=DEFAULT_PYTHON_VERSION)
def blacken(session):
    """Run black. Format code to uniform standard."""
    session.install(BLACK_VERSION)
    session.run("black", "-l", BLACK_MAX_LINE_LENGTH, *LINT_PATHS)


@nox.session(python=DEFAULT_PYTHON_VERSION)
def autoformat(session):
    """
    Run isort to sort imports. Then run black
    to format code to uniform standard.
    """
    session.install(BLACK_VERSION, ISORT_VERSION)
    # Use the --fss option to sort imports using strict alphabetical order.
    # See https://pycqa.github.io/isort/docs/configuration/options.html#force-sort-within-sections  # noqa: E501
    session.run("isort", "--fss", *LINT_PATHS)
    session.run("black", "-l", BLACK_MAX_LINE_LENGTH, *LINT_PATHS)


@nox.session(python=DEFAULT_PYTHON_VERSION)
def mypy(session):
    """Verify type hints are mypy compatible."""
    session.install("mypy", "types-setuptools", "types-mock", "colorama")
    session.run("mypy", "tests/")


def default(session):
    # Install all test dependencies.
    session.install(*UNIT_TEST_DEPENDENCIES)

    # Run py.test against the unit tests.
    session.run(
        "py.test",
        # "--quiet",
        "-vv",
        f"--junitxml=unit_{session.python}_sponge_log.xml",
        "--cov=src",
        "--cov=tests/unit",
        "--cov-append",
        "--cov-config=.coveragerc",
        "--cov-report=",
        "--cov-fail-under=0",
        os.path.join("tests", "unit"),
        *session.posargs,
    )


@nox.session(python=UNIT_TEST_PYTHON_VERSIONS)
def unit(session):
    """Run the unit test suite."""
    default(session)


@nox.session(python=SYSTEM_TEST_PYTHON_VERSIONS)
def system(session):
    """Run the system test suite."""
    system_test_folder_path = os.path.join("tests", "system")

    # Check the value of `RUN_SYSTEM_TESTS` env var. It defaults to true.
    if os.environ.get("RUN_SYSTEM_TESTS", "true") == "false":
        session.skip("RUN_SYSTEM_TESTS is set to false, skipping")

    system_test_folder_exists = os.path.exists(system_test_folder_path)

    # Sanity check: only run tests if found.
    if not system_test_folder_exists:
        session.skip("System tests were not found")

    session.install(*SYSTEM_TEST_DEPENDENCIES)

    # Run py.test against the system tests.
    if system_test_folder_exists:
        session.run(
            "py.test",
            "--quiet",
            f"--junitxml=system_{session.python}_sponge_log.xml",
            system_test_folder_path,
            *session.posargs,
        )


@nox.session(python=DEFAULT_PYTHON_VERSION)
def cover(session):
    """Run the final coverage report.

    This outputs the coverage report aggregating coverage from the unit
    test runs (not system test runs), and then erases coverage data.
    """
    session.install("coverage", "pytest-cov")
    session.run("coverage", "report", "--show-missing", "--fail-under=100")

    session.run("coverage", "erase")
