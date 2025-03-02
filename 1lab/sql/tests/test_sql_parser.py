"""Tests for sql parser."""
from sql.sql_parser import SQLParser
import pytest


@pytest.mark.parametrize(
        "query, result",
        [
            (["SELECT", "FROM"], True),
            (["SELECT", "*", "FROM", "table1"], True),
            (["SelEct", "FROM"], False),
            (["SELECT", "froM"], False),
            (["SELECT", "SELECT", "FROM"], False),
            (["SELECT", "FROM", "FROM"], False),
            (["FROM", "SELECT"], False),
            (["SELECT", "FROM", "WHERE"], True),
            (["SELECT", "FROM", "WHERE", "WHERE"], False),
            (["SELECT", "WHERE", "FROM"], False),
            (["FROM", "WHERE", "SELECT"], False)
        ]
)
def test_select_from(query, result):
    """Test for select and from validation."""
    parser = SQLParser()
    assert parser.validate_struct(query) == result


@pytest.mark.parametrize(
        "query, result",
        [
            (["SELECT", "FROM"], False),
            (["SELECT", "FROM", "table1"], False),
            (["sef", "SELECT", "table1", "FROM"], False),
            (["SELECT", "col1,", "col2,", "FROM", "table1"], False),
            (["SELECT", "col1", "col2,", "FROM", "table1"], False),
            (["SELECT", "col1,", "col2", "FROM", "table1"], True),
            (["SELECT", "col1,", "col2", "FROM"], False),
        ]
)
def test_columns_and_tables(query, result):
    """Test for columns and table names validation."""
    parser = SQLParser()
    assert parser.validate_columns_and_table(query) == result
