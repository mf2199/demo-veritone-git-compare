#!/usr/bin/env python3

import argparse
import json
import logging
import os
import sys
from pathlib import Path

import colorama
import requests

file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))

from src.custom_formatters import CustomFormatter, TxtColors  # noqa: E402

colorama.init()

CREDENTIALS_FILE = os.path.join(
    os.path.abspath(os.getcwd()), "src", "credentials.json"
)

# Setting up the logger
sh = logging.StreamHandler(sys.stdout)
sh.setFormatter(CustomFormatter())
logging.getLogger().addHandler(sh)
logging.getLogger().setLevel(logging.INFO)
logger = logging.getLogger()


def _get_owner():
    owner = os.environ.get("GH_ACCOUNT")
    if not owner:
        file_name = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            os.environ.get("CREDENTIALS_FILE") or CREDENTIALS_FILE,
        )
        f = open(file_name, "r")
        owner = json.load(f)["gh_account"]
    return owner


def _get_token():
    token = os.environ.get("GH_TOKEN")
    if not token:
        file_name = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            os.environ.get("CREDENTIALS_FILE") or CREDENTIALS_FILE,
        )
        f = open(file_name, "r")
        token = json.load(f)["gh_pat"]
    return token


def compare(repo_name, base, head, owner=None, debugging=False):
    """Compares two commits using GitHub API.

    :type repo_name: str
    :param repo_name: The name of the repository.

    :type base: str
    :param base: SHA code of the commit to compare the head to.

    :type head: str
    :param head: SHA code of the commit in question.

    :type owner: str
    :param owner: [Optional] The repository owner.

    :type debugging: bool
    :param debugging: [Optional] Enables additional logging.

    :rtype Any
    :return: The result of the `git diff` command.
    """
    owner = owner or _get_owner()
    base_url = "https://api.github.com/repos"
    url = f"{base_url}/{owner}/{repo_name}/compare/{base}...{head}"
    headers = {
        "Authorization": "Bearer " + _get_token(),
        "Accept": "application/vnd.github+json",
    }
    response = requests.get(url=url, headers=headers)

    color = TxtColors.http_response_color(response.status_code)
    print(color, f"Response status: {response.status_code}", TxtColors.NORMAL)
    logger.info(f"Response status: {response.status_code}")

    if debugging:
        msg = response.json()
        print(msg)
        logger.info(msg)

    if 200 > response.status_code >= 600:
        msg = response.json()
        print(msg)
        logger.critical(msg)
    elif 500 <= response.status_code < 600:
        msg = response.json()
        print(msg)
        logger.error(msg)
    elif 400 <= response.status_code < 500:
        msg = response.json()
        print(msg)
        logger.error(msg)
    elif 300 <= response.status_code < 400:
        msg = response.json()
        print(msg)
        logger.warning(msg)

    return response


def save_to_file(content, file_path=None, base=None, head=None, indent=4):
    # Setting the file extension: either `json` if the `content` is
    # JSON-serializable, otherwise - `txt`
    try:
        content = json.dumps(content, indent=indent)
        ext = "json"
    except TypeError:
        ext = "txt"

    suffix = f"_{base[:6]}...{head[:6]}" if base and head else ""

    file_path = file_path or os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        os.pardir,
        "data",
        f"diff{suffix}.{ext}",
    )

    # Checking whether the target folder exists and creating one if necessary
    if not os.path.exists(os.path.dirname(file_path)):
        os.mkdir(os.path.dirname(file_path))

    # Writing the contents to file
    with open(file_path, "w") as f:
        f.write(content)
        f.close()


if __name__ == "__main__":  # pragma: no cover (covered by the system tests)
    # region Command Line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--repo",
        dest="repo_name",
        type=str,
        help="The name of the repository",
    )
    parser.add_argument(
        "--base",
        dest="sha_base",
        type=str,
        help="SHA of the base commit",
    )
    parser.add_argument(
        "--head",
        dest="sha_head",
        type=str,
        help="SHA of the head commit",
    )
    parser.add_argument(
        "--file",
        dest="file",
        type=str,
        help="The name of the file to export the results into.",
        default=None,
    )
    parser.add_argument(
        "--account",
        dest="account",
        type=str,
        help="The owner's account user ID (i.e. GitHub alias).",
        default=None,
    )
    parser.add_argument(
        "--debug",
        dest="debug",
        type=bool,
        help="Enables additional logging",
        default=False,
    )
    args, _ = parser.parse_known_args()
    repo = args.repo_name
    sha_base = args.sha_base
    sha_head = args.sha_head
    account = args.account
    debug = args.debug
    # endregion

    result = compare(repo, sha_base, sha_head, account, debug)

    if debug:
        print(json.dumps(result, indent=4))

    save_to_file(result.json(), None, sha_base, sha_head)
