def read_public_notice(rawtext):
    "Get everything from the notice."

def _read_coords(rawtext):
    "Get coordinates from the notice."

def _convert_coords(degrees, minutes, seconds):
    [degrees, minutes, seconds] = map(float, [degrees, minutes, seconds])
    return degrees + minutes/60 + seconds/3600
