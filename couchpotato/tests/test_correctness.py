import math

from couchpotato import lazify
from hypothesis import given
from hypothesis.strategies import text, integers, booleans, floats, complex_numbers, tuples, characters, binary, fractions, decimals
from nose.tools import assert_equal

def pass_through(value):
    return value

lazy_pass = lazify(pass_through)

@given(text())
def test_equal_output_text(s):
    assert_equal(pass_through(s), lazy_pass(s))

@given(integers())
def test_equal_output_integers(arg):
    assert_equal(pass_through(arg), lazy_pass(arg))

@given(booleans())
def test_equal_output_booleans(arg):
    assert_equal(pass_through(arg), lazy_pass(arg))

@given(floats().filter(lambda x: not math.isnan(x)))
def test_equal_output_floats(arg):
    assert_equal(pass_through(arg), lazy_pass(arg))

@given(complex_numbers().filter(lambda x: not math.isnan(x.real) and not math.isnan(x.imag)))
def test_equal_output_complex(arg):
    assert_equal(pass_through(arg), lazy_pass(arg))

@given(tuples(integers(), integers(),))
def test_equal_output_tuple(arg):
    assert_equal(pass_through(arg), lazy_pass(arg))

@given(characters())
def test_equal_output_char(arg):
    assert_equal(pass_through(arg), lazy_pass(arg))

@given(binary())
def test_equal_output_binary(arg):
    assert_equal(pass_through(arg), lazy_pass(arg))

@given(fractions())
def test_equal_output_fraction(arg):
    assert_equal(pass_through(arg), lazy_pass(arg))

@given(decimals().filter(lambda x: not math.isnan(x)))
def test_equal_output_decimal(arg):
    assert_equal(pass_through(arg), lazy_pass(arg))

