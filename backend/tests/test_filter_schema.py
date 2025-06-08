"""
these tests are intended to verify that the changes made to filter yamls will yield the
desired results. Note that these tests DO NOT make any checks against functions in
filter_utils. If you make changes there, the correct tests are found in test_filter_utils.

tests for override filters have not yet been implemented
"""

import pytest
from pathlib import Path
import yaml
from typing import List, Dict, Union
import re
from constants import APPLIED_FILTER_PATH  # , APPLIED_FILTER_OVERRIDES_PATH
from tests.test_constants import (
    DESIRED_FAIL_APPLIED_EMAIL_FILTER_SUBJECT,
    DESIRED_PASS_APPLIED_EMAIL_FILTER_FROM,
    SAMPLE_FILTER_PATH,
)

FilterConfigType = List[Dict[str, Union[str, int, bool, list, dict]]]

FILTER_CONFIG_DIR = Path(__file__).parent.parent / "email_query_filters"


def get_base_filter_config_paths() -> List[Path]:
    return [SAMPLE_FILTER_PATH] + [
        x for x in FILTER_CONFIG_DIR.iterdir() if "override" not in str(x)
    ]


def get_override_filter_config_paths() -> List[Path]:
    return [x for x in FILTER_CONFIG_DIR.iterdir() if "override" in str(x)]


def load_filter_config(filter_path: str) -> FilterConfigType:
    with open(filter_path, "r") as fid:
        filter_config = yaml.safe_load(fid)
        return filter_config


def validate_schema_block_order(filter_config: FilterConfigType) -> bool:
    """
    Validates that 'exclude' blocks appear after 'include' blocks in the schema.
    """

    include_seen = False
    for block in filter_config:
        how = block.get("how")
        if how == "include":
            include_seen = True
        elif how == "exclude" and not include_seen:
            return False  # Exclude block before any include block

    return True


@pytest.mark.parametrize(
    "filter_config", [load_filter_config(x) for x in get_base_filter_config_paths()]
)
def test_base_filter_yaml_schema(filter_config):
    logic_list = [block["logic"] for block in filter_config if block["logic"]]
    how_list = [block["how"] for block in filter_config]
    exclude_terms = sum(
        [block["terms"] for block in filter_config if block["how"] == "exclude"], []
    )

    assert all(
        [
            (x == "any" and y == "include") or (x == "all" and y == "exclude")
            for x, y in zip(logic_list, how_list)
        ]
    ), "logic=any is not allowed for how=exclude"
    assert all(["*" not in x for x in exclude_terms]), (
        "wildcard is not allowed in exclude blocks"
    )
    assert validate_schema_block_order(filter_config), (
        "Exclude block found before an include block"
    )


def apply_base_filter(field_text, field_name, filter_config) -> bool:
    """Applies the YAML filter to the given text."""

    ret_val = False  # Default to failing if no filter logic is defined.

    for block in filter_config:
        if block["field"] == field_name:
            # check if the text is in the any, include block for that field
            if block["logic"] == "any" and block["how"] == "include":
                # simple compare
                if not ret_val:
                    ret_val = any(
                        [
                            x.lower() in field_text.lower()
                            for x in block["terms"]
                            if "*" not in x
                        ]
                    )

                # use regex for wildcard compare
                if not ret_val:
                    ret_val = any(
                        [
                            re.findall(
                                x.replace(" * ", ".*").lower(), field_text.lower()
                            )
                            for x in block["terms"]
                            if "*" in x
                        ]
                    )

            # check if the text is in the all, exclude block for that field.
            # all, exclude logic will override any matching includes
            if ret_val:
                if block["logic"] == "all" and block["how"] == "exclude":
                    ret_val = all(
                        [x.lower() not in field_text.lower() for x in block["terms"]]
                    )

    return ret_val


@pytest.mark.parametrize(
    "test_constant,filter_config",
    [(DESIRED_FAIL_APPLIED_EMAIL_FILTER_SUBJECT, APPLIED_FILTER_PATH)],
)
def test_apply_email_filter_subject_fail(test_constant, filter_config):
    """
    Tests if the desired subject pairs in test_constants will fail the filter
    """
    filter_config = load_filter_config(APPLIED_FILTER_PATH)

    result_list = []
    for subject_text in test_constant:
        result = apply_base_filter(subject_text, "subject", filter_config)
        result_list.append(result)

    assert not any(result_list), (
        f"These subject pairs failed to fail: {[x for x, y in list(zip(test_constant, result_list)) if y]}"
    )


@pytest.mark.parametrize(
    "test_constant,filter_config",
    [(DESIRED_PASS_APPLIED_EMAIL_FILTER_FROM, APPLIED_FILTER_PATH)],
)
def test_apply_email_filter_from_pass(test_constant, filter_config):
    """
    Tests if the desired from pairs in test_constants will pass the filter
    """
    filter_config = load_filter_config(APPLIED_FILTER_PATH)

    result_list = []
    for from_text in test_constant:
        result = apply_base_filter(from_text, "from", filter_config)
        result_list.append(result)

    assert all(result_list), (
        f"These from pairs failed to pass: {[x for x, y in list(zip(test_constant, result_list)) if not y]}"
    )


@pytest.mark.parametrize(
    "test_constant,filter_config",
    [(DESIRED_FAIL_APPLIED_EMAIL_FILTER_SUBJECT, APPLIED_FILTER_PATH)],
)
def test_apply_email_filter_from_fail(test_constant, filter_config):
    """
    Tests if the desired from pairs in test_constants will fail the filter
    """
    filter_config = load_filter_config(APPLIED_FILTER_PATH)

    result_list = []
    for from_text in test_constant:
        result = apply_base_filter(from_text, "from", filter_config)
        result_list.append(result)

    assert not any(result_list), (
        f"These from pairs failed to fail: {[x for x, y in list(zip(test_constant, result_list)) if y]}"
    )
