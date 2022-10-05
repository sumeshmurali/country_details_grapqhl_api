"""
This file is to test if the tests are working properly
"""

import pytest


def test_success_test():
    assert True


def test_fail_test():
    with pytest.raises(AssertionError):
        assert False
