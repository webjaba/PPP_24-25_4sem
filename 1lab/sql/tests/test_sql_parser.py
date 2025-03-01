"""Tests for sql parser."""
from sql.sql_parser_oop import SQLParser
import pytest


@pytest.mark.parametrize(
        "query, result",
        [
            (["SELECT", "FROM"], True),
            (["SELECT", "*", "FROM", "table1"], True),
            (["SelEct", "FROM"], False),
            (["SELECT", "froM"], False),
        ]
)
def test_select_from(query, result):
    """Test for select and from validation."""
    parser = SQLParser()
    assert parser.validate_select_from(query) == result
