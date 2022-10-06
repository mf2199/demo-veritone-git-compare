import json
import os

import mock
import uuid

from requests import Response

TEST_ACCOUNT = "veritone"
TEST_REPO = "veritone-sdk"
TEST_SHA_BASE = "5a971a2e09c250b20e7ad98685ce2bd945fdbe33"
TEST_SHA_HEAD = "61a8c32c8d8987fac5d98fb0d19729f8ee724868"
# TEST_REPO = "google-cloud-python"
# TEST_SHA_BASE = "f923873817a6beaf90dae0954a79cff8f6f6c4d7"
# TEST_SHA_HEAD = "7b5ff28f9c74e5d2771f52663945e055b99a5470"

TEST_OWNER = str(uuid.uuid4())
TEST_TOKEN = str(uuid.uuid4())


def test_http_response_color():
    from src import compare

    for i in range(200, 300):
        expected = compare.TxtColors.OKGREEN
        assert compare.TxtColors.http_response_color(i) == expected
    for i in range(300, 400):
        expected = compare.TxtColors.WARNING
        assert compare.TxtColors.http_response_color(i) == expected
    for i in range(400, 500):
        expected = compare.TxtColors.FAIL
        assert compare.TxtColors.http_response_color(i) == expected

    expected = compare.TxtColors.HEADER
    assert compare.TxtColors.http_response_color(0) == expected
    assert compare.TxtColors.http_response_color(1000) == expected


@mock.patch.dict("os.environ", {"GH_ACCOUNT": TEST_OWNER})
def test__get_owner_from_env():
    from src import compare

    assert compare._get_owner() == TEST_OWNER


@mock.patch.dict(
    "os.environ",
    {
        "GH_ACCOUNT": "",
        "CREDENTIALS_FILE": os.path.join(
            os.pardir,
            "tests",
            "fixtures",
            "test_credentials.json",
        ),
    },
)
def test__get_owner_from_file():
    from src import compare

    file_name = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        os.pardir,
        "fixtures",
        "test_credentials.json",
    )
    f = open(file_name, "r")
    expected = json.load(f)["gh_account"]

    assert compare._get_owner() == expected


@mock.patch.dict("os.environ", {"GH_TOKEN": TEST_TOKEN})
def test__get_token_from_env():
    from src import compare

    assert compare._get_token() == TEST_TOKEN


@mock.patch.dict(
    "os.environ",
    {
        "GH_TOKEN": "",
        "CREDENTIALS_FILE": os.path.join(
            os.pardir,
            "tests",
            "fixtures",
            "test_credentials.json",
        ),
    },
)
def test__get_token_from_file():
    from src import compare

    file_name = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        os.pardir,
        "fixtures",
        "test_credentials.json",
    )
    f = open(file_name, "r")
    expected = json.load(f)["gh_pat"]

    assert compare._get_token() == expected


@mock.patch("src.compare.requests")
def test_compare(mock_requests, caplog):
    from src import compare

    mock_response = Response()
    mock_response.status_code = 200
    mock_response.json = mock.MagicMock(return_value={})
    mock_requests.get.return_value = mock_response
    result = compare.compare(
        TEST_REPO, TEST_SHA_BASE, TEST_SHA_HEAD, TEST_ACCOUNT, True
    )
    assert result.status_code == 200
    mock_requests.get.assert_called_once_with(url=mock.ANY, headers=mock.ANY)
    assert str(mock_response.status_code) in caplog.text
