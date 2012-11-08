'''
The parish name should be extracted from a location field.
'''
from nose.tools import assert_equal
from listing import _extract_parish

def _(location, parish):
    'The location should become the parish.'
    observed_parish = _extract_parish(location)
    assert_string_equal(observed_parish, parish)

def test_MVN_1998_04602_CQ():
    _('St. Helena Parish', 'St. Helena')

def test_MVN_2012_1266_CU():
    _('Ascension Parish', 'Ascension')

def test_MVN_2011_00428_WLL():
    _('Terrebonne Parish', 'Terrebonne')

def test_MVN_2012_01939_WLL():
    _('St. Martin Parish', 'St. Martin')

def test_MVN_2012_00926():
    _('Lafourche Parish', 'Lafourche')

def test_MVN_2012_1896_EPP():
    _('St. Tammany Parish', 'St. Tammany')

def test_MVN_2009_0862_EBB():
    _('Jefferson Parish', 'Jefferson')

def test_MVN_2011_1918_CU():
    _('East Baton Rouge Parish', 'East Baton Rouge')

def test_MVN_2011_30781_WII():
    _('Multiple Parishes', None)

def test_MVN_2012_1996_CU():
    _('St. John the Baptist Parish', 'St. John the Baptist')

def test_CEMVN_NWP_2012():
    _('(NO PROJECT AREA)', None)
