#!/usr/bin/env python2
# -*- encoding: utf-8 -*-
"""
Test that the right information is extracted from each pdf

Handling null values:
  * No value means that the information has not been processed.
  * None or the empty list indicates that the information is missing from the translated document.
  * The empty string indicates that the value is "".
"""

import os
import unittest
from read import read_public_notice, \
    _read_coords, _convert_coords, \
    _read_wqc_number, \
    _read_cup_number, \
    _read_acres

class TestAcres(unittest.TestCase):
    def setUp(self):
        self.rawtext = '''
3): Lat 29° 12' 09.91"N / Long -89° 38' 36.53"W; Borrow Area 9 (Pt. 9):
Lat 29° 12' 52.5"N / Long -89° 36' 49.7"W; Section 39-41, T20S-R28E; Section 16-21 ,26-28,34,35,1 3, 24, T218-
R28E; West of Empire Waten/vay within Bastian Bay area.
DESCRIPTION: Shell Island East Restoration Berm Enhancement Project and Shell Island West NRDA Restoration Project (BA-
110/11 1) forthe proposed creation of +/- 615 acres of beach/dune habitat and +/-343 acres of brackish marsh
habitat along the Barataria Basin Barrier Shoreline. Project includes the dredging of +/-12.9 M c.y. of sediment from
potential borrow areas MR-A, MR-B, MR-E, 35E, and 9 (MR-B and MR-E previously permitted under P20101416 -
Scofield Island Restoration Project/ BA-40). Conveyance of sediment within a submerged/buried 30" pipeline
proposed from borrow sources MR-A, MR-B, and MR-E along an existing dredge pipeline corridor follows the
Empire Waterway (previously permitted under P20101416) and from Areas 35E and 9 with estimated losses in
sediment due to transfer anticipated. Proposed till required for the creation of dune habitat is +/- 6.4M c.y. and +/-
1.8M c.y. for the creation of marsh habitat. Project also includes the excavation of +/- 467,900 c.y. for access
channels and subsequent placement on both sides to a height conducive to marsh establishment, excavation of +/-
865,000 c.y. for the construction of the primary dikes for containment of marsh creation areas, the placement 250
c.y. of gravel for dredge pipeline levee crossings, and the excavation of +/- 21,400 c.y. for navigational crossings,
booster pump locations, Empire Harbor Canal crossing, Highway 11 and 23 crossings, and the Empire Marsh
crossing. "Approximately 2,291 ac. of non-vegetated waterbottom, 1.2 ac. of non-wet, and 132 ac. of vegetated
wetland habitat may be impacted as a result of proposed activity.**
Approximately 1,832 acres of Essential Fish Habitat (EFH) utilized by various life stages of red drum and panaeid
shrimp would be altered or destroyed by this project. This information is provided to initiate federal consultation
requirements pertaining to EF H under the Magnuson-Stevens Fishery Conservation and Management Act.*
NOTICE the Louisiana Department of Natural Resources, Office of Coastal Management (OCM) has
received the above application for a Coastal Use Permit (CUP) in accordance with the State and Local
Coastal Resources Management Act of 1978, as amended, (Louisiana R.S. 49:2'''
    def test_go(self):
        self.assertListEqual(_read_acres(self.rawtext), [615., 343., 1832.])


class TestCUP(unittest.TestCase):
    def setUp(self):
        self.rawtext = '''
OFFICE OF COASTAL MANAGEMENT
P.O. BOX 44487
BATON ROUGE, LA 70804-4487
Phone (225)342-6140
Fax (225) 342-9439
Email sharon.mccarthy@la.gov
OCM REVIEWER:
Sharon Mccarthy
CUP NUMBER:
P20120216
Plaquemines Parish, LA; Shell Island East (Pt. 250): Lat 29° 16' 38.24"N / Long -89° 37' 43.91"W; Shell Island
West (Pt. 240): Lat 29° 17' 49.45"N / Long -89° 39' 51 .73"W; Borrow Areas/MR-A (Pt. 3): Lat 29° 26' 57.94"N/
Long -89° 36' 11.43"W; MR-B (Pt. 13): Lat 29° 22' 52.80"N / Long -89° 34' 36.95"W; MR-E (Pt. 6): Lat 29° 21'
04.95"N / Long -89° 30' 07.18"W; 35E (Pt. 3): Lat 29° 12' 09.91"N / Long -89° 38' 36.53"W; Borrow Area 9 (Pt. 9):
Lat 29° 12' 52.5"N / Long -89° 36' 49.7"W; Section 39-41, T20S-R28E; Section 16-21 ,26-28,34,35,1 3, 24, T218-
R28E; West of Empire Waten/vay within Bastian Bay area.
DESCRIPTION: Shell Island East Restoration Berm Enhancement Project and Shell Island West NRDA Restoration Project (BA-
110/11 1) forthe proposed creation of +/- 615 acres of beach/dune habitat and +/-343 acres of brackish marsh
habitat along the Barataria Basin Barrier Shoreline. Project includes the dredging of +/-12.9 M c.y. of sediment from
potential borrow areas MR-A, MR-B, MR-E, 35E, and 9 (MR-B and MR-E previously permitted under P20101416 -
Scofield Island Restoration Project/ BA-40). Conveyance of sediment within a submerged/buried 30" pipeline
proposed from borrow sources MR-A, MR-B, and MR-E along an existing dredge pipeline corridor follows the
Empire Waterway (previously permitted under P20101416) and from Areas 35E and 9 with estimated losses in
sediment due to transfer anticipated. Proposed till required for the creation of dune habitat is +/- 6.4M c.y. and +/-
1.8M c.y. for the creation of marsh habitat. Project also includes the excavation of +/- 467,900 c.y. for access
channels and subsequent placement on both sides to a height conducive to marsh establishment, excavation of +/-
865,000 c.y. for the construction of the primary dikes for containment of marsh creation areas, the placement 250
c.y. of gravel for dredge pipeline levee crossings, and the excavation of +/- 21,400 c.y. for navigational crossings,
booster pump locations, Empire Harbor Canal crossing, Highway 11 and 23 crossings, and the Empire Marsh
crossing. "Approximately 2,291 ac. of non-vegetated waterbottom, 1.2 ac. of non-wet, and 132 ac. of vegetated
wetland habitat may be impacted as a result of proposed activity.**
'''
    def test_go(self):
        observed = _read_cup_number(self.rawtext)
        expected = {'P20120216','P20101416'}
        self.assertEqual(observed, expected)

class TestWQC(unittest.TestCase):
    def setUp(self):
        self.rawtext = '''
ttn: Water Quality Certifications
Post Office Box 4313
Baton Rouge, LA 70821-4313

(504) 862-2675 FAX (504) 862-2574
Project Manager
Jamie Crowe
Permit Application Number
MVN 1999-3891 CO

(225) 219-3225 FAX (225) 325-8250
Project Manager
Jamie Phillippe
WQC Application Number
990825-04

Interested parties are hereby notified that a permit application has been received by the New
Orleans District of the U.S. Army Corps of Engineers pursuant to: [X] Section 10 of the Rivers and
Harbors Act of March 3, 1899 (30 Stat. 1151; 33 USC 403); and/or [X] Section 404 of the Clean Water
Act (86 Stat. 816; 33 USC 1344).
Application has also been made to the Louisiana Department of Environmental Quality,
Office of Environmental Services, for a Water Quality Certification (WQC) in accordance with statutory
authority contained in LRS 30:2074 A(3) and provisions of Section 401 of the Clean Water Act.
MODIFICATION OF SHIP MOORING FACILITY IN
'''
    def test_go(self):
       self.assertEqual(_read_wqc_number(self.rawtext), '990825-04')

class TestConvertCoords(unittest.TestCase):
    def setUp(self):
        self.rawtext = '''
Plaquemines Parish, LA; Shell Island East (Pt. 250): Lat 29° 16' 38.24"N / Long -89° 37' 43.91"W; Shell Island
West (Pt. 240): Lat 29° 17' 49.45"N / Long -89° 39' 51 .73"W; Borrow Areas/MR-A (Pt. 3): Lat 29° 26' 57.94"N/
Long -89° 36' 11.43"W; MR-B (Pt. 13): Lat 29° 22' 52.80"N / Long -89° 34' 36.95"W; MR-E (Pt. 6): Lat 29° 21'
04.95"N / Long -89° 30' 07.18"W; 35E (Pt. 3): Lat 29° 12' 09.91"N / Long -89° 38' 36.53"W; Borrow Area 9 (Pt. 9):
Lat 29° 12' 52.5"N / Long -89° 36' 49.7"W; Section 39-41, T20S-R28E; Section 16-21 ,26-28,34,35,1 3, 24, T218-
R28E; West of Empire Waten/vay within Bastian Bay area.
'''
    def test_minutes_seconds(self):
        self.maxDiff = None
        observed = _read_coords(self.rawtext, decimal = False)
        expected = [
            # Latitude, longitude
            ( ( 29.0, 16.0, 38.24 ) , ( -89.0, -37.0, -43.91 ) ),
            ( ( 29.0, 17.0, 49.45 ) , ( -89.0, -39.0, -51.73 ) ),
            ( ( 29.0, 26.0, 57.94 ) , ( -89.0, -36.0, -11.43 ) ),
            ( ( 29.0, 22.0, 52.80 ) , ( -89.0, -34.0, -36.95 ) ),
            ( ( 29.0, 21.0, 04.95 ) , ( -89.0, -30.0, -07.18 ) ),
            ( ( 29.0, 12.0, 09.91 ) , ( -89.0, -38.0, -36.53 ) ),
            ( ( 29.0, 12.0, 52.5  ) , ( -89.0, -36.0, -49.7  ) ),
        ]
        self.assertListEqual(observed, expected)

    def test_defaults(self):
        _read_coords(self.rawtext, decimal = True) == _read_coords(self.rawtext)
        _read_coords(self.rawtext, decimal = False) != _read_coords(self.rawtext)

    def test_decimal(self):
        observed = _read_coords(self.rawtext, decimal = True)
        expected = [
            # Latitude, longitude
            (29.277288888888886, -89.62886388888889),
            (29.297069444444446, -89.66436944444445),
            (29.449427777777778, -89.603175), 
            (29.381333333333334, -89.57693055555555),
            (29.351375, -89.50199444444445),
            (29.20275277777778, -89.64348055555556),
            (29.214583333333334, -89.61380555555554)
            # &c.
        ]
        self.assertListEqual(observed, expected)

    def test_positive(self):
        observed = _convert_coords(29, 16, 38.24 )
        self.assertAlmostEqual(observed, 29.27728888, delta = 10**10)

    def test_negative(self):
        observed = _convert_coords(-89, -37, -43.91 )
        self.assertAlmostEquals(observed, 89.62886388888889, delta = 10**10)

    def test_different_signs(self):
        "Sending parameters of different signs raises a ValueError."
        with self.assertRaises(ValueError):
            _convert_coords(-89, 37, 43.91 )
        with self.assertRaises(ValueError):
            _convert_coords(0, -37, 43.91 )
        _convert_coords(0, 37, 43.91 )
        _convert_coords(0, 0, 43.91 )
        _convert_coords(0, 0, -43.91 )

class TestReadPublicNotice(unittest.TestCase):
    def setUp(self):
        rawtext = open('fixtures/Kilbride PN.pdf.txt').read()
        self.data = read_public_notice(rawtext)
    def test_keys(self):
        observed = set(self.data.keys())
        expected = {
            'WQC',
            'CUP',
            'Mitigation Bank',
            'Acres',
            'Parish',
            'Coords',
            'Basin',
            'HUC',
            '10 acre',
            'Section 10',
            'Section 404',
        }
        self.assertSetEqual(observed, expected)
    def test_types(self):
        observed = {} # Make this
        expected = {
            'WQC': unicode,
            'CUP': set,
            'Mitigation Bank': bool,
            'Acres': list,
            'Parish': unicode,
            'Coords': list,
            'Basin': unicode,
#           'HUC',
            '10 acre': bool,
            'Section 10': bool,
            'Section 404': bool,
        }

        set(observed['Acres']).issubset({float})
        set(observed['Coords']).issubset({tuple})
        for c in observed['Coords']:
            # Latitude, longitude
            len(c) == 2
            type(c[0]) == type(c[1]) == float

            # Within a reasonable boundary
            29 < c[0] < 31
            88 < c[1] < 94

if __name__ == "__main__":
    unittest.main()
