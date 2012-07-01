# -*- encoding: utf-8 -*-
import re

def read_public_notice(rawtext):
    "Get everything from the notice."

_COORDS = re.compile(r'(-?\d+)°(\d+)\'([0-9.]+)"([NW])')
def _read_coords(rawtext, decimal = True, verbose = False):
    "Get coordinates from the notice."
    rawcoords = re.findall(_COORDS, ''.join(rawtext.split()))
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
