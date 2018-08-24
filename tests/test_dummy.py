import pytest
import dummy

def test_imports():
    import numpy

def test_dummy_True():
    assert dummy.dummy_equals(1,1)

def test_dummy_False():
    assert not dummy.dummy_equals(1,2)
