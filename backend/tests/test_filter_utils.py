"""
test that the strings produced by filter utils match expectations

tests for override filters have not yet been implemented.
"""

from typing import List, Dict, Union

from utils.filter_utils import (
    parse_base_filter_config,
)  # , parse_override_filter_config
from tests.test_constants import SAMPLE_FILTER_PATH, EXPECTED_SAMPLE_QUERY_STRING

FilterConfigType = List[Dict[str, Union[str, int, bool, list, dict]]]


def test_parse_filter_config_against_sample_filter(
    filter_path=SAMPLE_FILTER_PATH, expected_query_string=EXPECTED_SAMPLE_QUERY_STRING
):
    result_str = parse_base_filter_config(filter_path)

    # remove white space from expected string for the purpose of comparing
    expected_query_string = (
        expected_query_string.replace("\n", "").replace("\t", "").replace("    ", "")
    )

    assert result_str == expected_query_string, (
        "result query string doesn't match expected query string"
    )
