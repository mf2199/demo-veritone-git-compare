from urllib import request

import mock

TEST_ACCOUNT = "veritone"
TEST_REPO = "veritone-sdk"
TEST_SHA_BASE = "5a971a2e09c250b20e7ad98685ce2bd945fdbe33"
TEST_SHA_HEAD = "61a8c32c8d8987fac5d98fb0d19729f8ee724868"


@mock.patch.dict("os.environ", {"GH_ACCOUNT": TEST_ACCOUNT})
def test_compare():
    from src import compare

    base_url = "https://github.com"
    expected_diff_url = "/".join(
        [
            base_url,
            TEST_ACCOUNT,
            TEST_REPO,
            "compare",
            f"{TEST_SHA_BASE}...{TEST_SHA_HEAD}.diff",
        ]
    )
    expected = request.urlopen(expected_diff_url).read().decode("ascii")

    result = compare.compare(
        repo_name=TEST_REPO,
        base=TEST_SHA_BASE,
        head=TEST_SHA_HEAD,
        owner=TEST_ACCOUNT,
    )

    for f in result.json()["files"]:
        assert f["patch"] in expected
