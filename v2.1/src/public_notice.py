# -*- encoding: utf-8 -*-
import re
import json
import dumptruck

def main():
    import sys
    # Read input
    permit = sys.argv[1]
    text = sys.stdin.read()

    # Parse
    doc = read_public_notice(text)
    doc['permitApplicationNumber'] = permit
    doc['pdfParsed'] = 1

    # Clean up
    doc['CUP'] = list(doc['CUP'])[0] if len(doc['CUP']) > 0 else ''
    doc['Coords'] = json.dumps(doc['Coords'])
    doc['Acres'] = json.dumps(doc['Acres'])

    # Connect to database
    db = dumptruck.DumpTruck(dbname = '/tmp/wetlands.db')

    # Update the document; upsert updates the specified columns
    db.upsert(doc, 'application')

    # print doc

def read_public_notice(rawtext):
    "Get everything from the notice."
    data = {}

    try:
        data['Acres'] = _read_acres(rawtext)
    except Exception, e:
        data['AcresException'] = unicode(type(e)) + ': ' + unicode(e)
        data['Acres'] = []
    else:
        data['AcresException'] = None

    try:
        data.update(_read_terms(rawtext))
    except Exception, e:
        data['TermsException'] = unicode(type(e)) + ': ' + unicode(e)
    else:
        data['TermsException'] = None

    try:
        data['CUP'] = _read_cup_number(rawtext)
    except Exception, e:
        data['CUPException'] = unicode(type(e)) + ': ' + unicode(e)
        data['CUP'] = u''
    else:
        data['CUPException'] = None

    try:
        data['WQC'] = _read_wqc_number(rawtext)
    except Exception, e:
        data['WQCException'] = unicode(type(e)) + ': ' + unicode(e)
        data['WQC'] = u''
    else:
        data['WQCException'] = None

    try:
        data['Coords'] = _read_coords(rawtext)
    except Exception, e:
        data['CoordsException'] = unicode(type(e)) + ': ' + unicode(e)
        data['Coords'] = []
    else:
        data['CoordsException'] = None

    return data

def strip_ws(rawtext):
    return ''.join(rawtext.split())

ACRES = re.compile(r'([0-9,.]+)acre')
def _read_acres(rawtext):
    raw = re.findall(ACRES, strip_ws(rawtext))
    return [float(a.replace(',', '')) for a in raw]

TERMS = [
    "Mitigation Bank",
    "Drill",
    "Road",
    "Section 10",
    "Section 404"
]
CLEANTERMS = [t.lower().replace(' ', '') for t in TERMS]
def _read_terms(rawtext):
    rawtext = strip_ws(rawtext).lower()
    return {term: (cleanterm in rawtext) for cleanterm, term in zip(CLEANTERMS, TERMS) }

#           --> optionally, list numbers for "cubic yards"  or "material".  this is more difficult.  These will be numbers estimating the volumes of material dredged or filled.

CUP_NUMBER = re.compile(r'\s(P\d{8})[^0-9]')
def _read_cup_number(rawtext):
    return set(re.findall(CUP_NUMBER, rawtext))

WQC_NUMBER = re.compile(r'WQCApplicationNumber[^0-9]*([0-9-]+)')
def _read_wqc_number(rawtext):
    rawtext = strip_ws(rawtext)
    wqc_numbers = re.findall(WQC_NUMBER, rawtext)

    if len(wqc_numbers) > 1:
        raise AssertionError('Multiple WQC numbers found')
    elif len(wqc_numbers) == 0:
        raise AssertionError('No WQC numbers found')

    no_hyphen = wqc_numbers[0].replace('-', '')
    if len(no_hyphen) != 8:
        raise AssertionError('WQC number has the wrong length.')

    return no_hyphen[:6] + '-' + no_hyphen[-2:]


MINUTE_COORDS = re.compile(r'(-?\d+)°(\d+)\'([0-9.]+)"([NW])')
DECIMAL_COORDS = re.compile(r'(lat|latitude|long|longitude)[0-9.]+',
    flags = re.IGNORECASE)

def _read_coords(rawtext, **kwargs):
    "Get coordinates from the notice."
    rawtext = strip_ws(rawtext)

    rawcoords = re.findall(MINUTE_COORDS, rawtext)
    if len(rawcoords) > 0:
        return _clean_minute_coords(rawcoords, **kwargs)

    rawcoordsd = re.findall(DECIMAL_COORDS, rawtext)
    return _clean_minute_coords(rawcoordsd)

def _clean_minute_coords(rawcoords, decimal = True, verbose = False):
    cleancoords = []
    while len(rawcoords) > 0:
        first = rawcoords.pop(0)
        second = rawcoords.pop(0)

        f = first[-1]
        s = second[-1]
        if f != 'N':
            raise ValueError('Wrong direction: %s' % f)
        if s != 'W':
            raise ValueError('Wrong direction: %s' % s)

        # Handle sign
        s = int(second[0])
        if s < 0:
            second = [-s] + list(second[1:3])

        f = int(first[0])
        s = int(second[0])
        if not 28 < f < 32:
            raise ValueError('Strange latitude: %d' % f)
        if not 88 < s < 94:
            raise ValueError('Strange longitude: %d' % s)


        lat = tuple([float(f) for f in first[:3]])
        lng = tuple([-float(s) for s in second[:3]])

        if decimal:
            latlng = tuple([_convert_coords(*foo) for foo in [lat, lng]])
            cleancoords.append(latlng)
        else:
            cleancoords.append((lat, lng))

        if verbose:
            print lat, lng

    return cleancoords

def _convert_coords(degrees, minutes, seconds):
    [degrees, minutes, seconds] = map(float, [degrees, minutes, seconds])

    # Check signs
    for arg in [degrees, minutes, seconds]:
        if arg == 0:
            continue
        elif arg > 0:
            positive = True
            break
        elif arg < 0:
            positive = False
            break
        else:
            raise ValueError('wtf?')
    for arg in [degrees, minutes, seconds]:
        if positive and arg < 0:
            raise ValueError('All arguments must have the same sign.')
        elif not positive and arg > 0:
            raise ValueError('All arguments must have the same sign.')

    return degrees + minutes/60 + seconds/3600

if __name__ == '__main__':
    main()
