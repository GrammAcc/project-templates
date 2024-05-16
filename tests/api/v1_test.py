from packagename import utils


def _url_from_endpoint(endpoint: str) -> str:
    """Convert a named endpoint into the corresponding URL on the api."""

    return f"{utils.get_domain()}/api/v1/{endpoint}"


def test_replace_me_query_param(fixt_client):
    """The replace-me endpoint should return the list of Example resources filtered
    by name when the `q` parameter is provided."""

    expected = [
        {
            "mtmexamples": [],
            "name": "Some Example",
            "otmexamples": [
                {
                    "example_id": 1,
                    "name": "Some One-to-Many Example",
                    "uri": "http://api.packagename.local/api/v1/otmexample/1",
                }
            ],
            "uri": "http://api.packagename.local/api/v1/example/1",
        }
    ]
    res = fixt_client.get(f"{_url_from_endpoint('replace-me')}?q=Some Example")
    assert res.status_code == 200
    records = res.json
    assert records == expected


def test_cofeemaker(fixt_client):
    """Ensure the coffee endpoint gives an appropriate response according to
    the HTCPCP standard."""

    res = fixt_client.get(f"{_url_from_endpoint('coffee')}")
    assert res.status_code == 418
    assert res.status == "418 I'M A TEAPOT"
