"""Minimal smoke test: confirm the alaf package can be imported."""

import alaf


def test_import() -> None:
    assert alaf.__version__ == "0.1.0"
