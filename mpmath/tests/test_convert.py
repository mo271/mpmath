import random
from mpmath import *
from mpmath.lib import *


def test_basic_string():
    """
    Test basic string conversion
    """
    mpf.dps = 15
    assert mpf('3') == mpf('3.0') == mpf('0003.') == mpf('0.03e2') == mpf(3.0)
    assert mpf('30') == mpf('30.0') == mpf('00030.') == mpf(30.0)
    for i in range(10):
        for j in range(10):
            assert mpf('%ie%i' % (i,j)) == i * 10**j
    assert str(mpf('25000.0')) == '25000.0'
    assert str(mpf('2500.0')) == '2500.0'
    assert str(mpf('250.0')) == '250.0'
    assert str(mpf('25.0')) == '25.0'
    assert str(mpf('2.5')) == '2.5'
    assert str(mpf('0.25')) == '0.25'
    assert str(mpf('0.025')) == '0.025'
    assert str(mpf('0.0025')) == '0.0025'
    assert str(mpf('0.00025')) == '0.00025'
    assert str(mpf('0.000025')) == '2.5e-5'
    assert str(mpf(0)) == '0.0'
    assert str(mpf('2.5e1000000000000000000000')) == '2.5e+1000000000000000000000'
    assert str(mpf('2.6e-1000000000000000000000')) == '2.6e-1000000000000000000000'
    assert str(mpf(1.23402834e-15)) == '1.23402834e-15'
    assert str(mpf(-1.23402834e-15)) == '-1.23402834e-15'
    assert str(mpf(-1.2344e-15)) == '-1.2344e-15'
    assert repr(mpf(-1.2344e-15)) == "mpf('-1.2343999999999999e-15')"

def test_unicode():
    mpf.dps = 15
    assert mpf(u'2.76') == 2.76
    assert mpf(u'inf') == inf

def test_tight_string_conversion():
    mpf.dps = 15
    # In an old version, '0.5' wasn't recognized as representing
    # an exact binary number and was erroneously rounded up or down
    assert from_str('0.5', 10, round_floor) == fhalf
    assert from_str('0.5', 10, round_ceiling) == fhalf


def test_eval_repr_invariant():
    """Test that eval(repr(x)) == x"""
    random.seed(123)
    for dps in [10, 15, 20, 50, 100]:
        mpf.dps = dps
        for i in xrange(1000):
            a = mpf(random.random())**0.5 * 10**random.randint(-100, 100)
            if dps == 15:
                assert eval(repr(a)) == a
            else:
                assert eval(repr(a)).ae(a)
    mpf.dps = 15

def test_str_bugs():
    mpf.dps = 15
    # Decimal rounding used to give the wrong exponent in some cases
    assert str(mpf('1e600')) == '1.0e+600'
    assert str(mpf('1e10000')) == '1.0e+10000'


def test_convert_rational():
    mpf.dps = 15
    assert from_rational(30, 5, 53, round_half_even) == (3, 1, 2)
    assert from_rational(-7, 4, 53, round_half_even) == (-7, -2, 3)
    assert to_rational((1, -1, 1)) == (1, 2)

def test_custom_class():
    class mympf:
        def __mpfval__(self):
            return mpf(3.5).val
    class mympc:
        def __mpcval__(self):
            return mpf(3.5), mpf(2.5)
    assert mpf(2) + mympf() == 5.5
    assert mympf() + mpf(2) == 5.5
    assert mpf(mympf()) == 3.5
    assert mympc() + mpc(2) == mpc(5.5, 2.5)
    assert mpc(2) + mympc() == mpc(5.5, 2.5)
    assert mpc(mympc()) == (3.5+2.5j)