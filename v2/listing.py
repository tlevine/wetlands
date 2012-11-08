import pymongo
import datetime
import lxml.html, lxml.etree
import re
from unidecode import unidecode
from urllib2 import urlopen

DATETIME = datetime.datetime.now()
connection = pymongo.Connection('localhost')
db = connection.wetlands

def main():
    html = listing_retrieve()
    data = listing_parse(html)
    listing_save(data, db)

def listing_retrieve(
        url = 'http://www.mvn.usace.army.mil/ops/regulatory/publicnotices.asp?ShowLocationOrder=False',
        stamp = datetime.datetime.now().isoformat()
    ):
    rawtext = urlopen(url).read()
    open('listings/%s.html' % stamp, 'w').write(rawtext)
    return rawtext

def listing_parse(rawtext):
    # There are more data in the comments!
    text_with_locations = rawtext.replace('<!--', '').replace('-->', '').replace('&nbsp;', ' ')
    unicodetext = unidecode(text_with_locations)
    html = lxml.html.fromstring(unicodetext)
    table = _onenode(html, '//table[@width="570" and @border="1" and @cellpadding="0" and @cellspacing="0" and @bordercolor="#ffffff" and @bgcolor="#efefef"]')
    trs = table.xpath('tr')

    # Getting the cells
    thead = [td.text_content().strip() for td in trs.pop(0)]
    if len(thead) != _NCOL:
        _log(thead)
        _RRRaise(AssertionError('The table header does not have exactly %d cells.' % _NCOL))

    if thead != _COLNAMES:
        pairs = zip(thead, _COLNAMES)
        for a, b in pairs:
            _log(a, b), 'Match' if a == b else 'Differ'
        _RRRaise(AssertionError('The table header does not have the right names.'))

    # List of dictionaries of data
    data = []
    publicnotices = []
    drawings = []
    for tr in trs:
        if len(tr.xpath('td')) != _NCOL:
            _RRRaise(AssertionError('The table row does not have exactly %d cells.' % _NCOL))

        # As a dict
        row = dict(zip(thead, [td.text_content().strip() for td in tr.xpath('td')]))

        # Clean up the permit application number
        row['PermitApplication No.'] = _clean_permit_application_number(row['PermitApplication No.'])

        # Dates
        row['Public Notice Date'] = _parsedate(row['Public Notice Date'])
        row['Expiration Date'] = _parsedate(row['Expiration Date'])

        # PDF download links
        del(row['View or Download'])
        pdfkeys = set(tr.xpath('td[position()=6]/descendant::a/text()'))
        if not pdfkeys.issubset({'Public Notice', 'Drawings'}):
            _log(pdfkeys)
            _RRRaise(AssertionError('The table row has unexpected hyperlinks.'))
        if len(pdfkeys) == 0:
            print(row)
            _RRRaise(AssertionError('No pdf hyperlinks found for permit %s.' % row['PermitApplication No.']))
        for key in ['Public Notice', 'Drawings']:
            try:
                row[key] = _onenode(tr, 'td/descendant::a[text()="%s"]/@href' % key)
            except AssertionError:
                if key == 'Public Notice':
                    raise
                else:
                    continue

            if row[key][:4] != 'pdf/':
                _RRRaise(AssertionError('The %s pdf link doesn\'t have the expected path.' % key))

        # Project manager contact information
        del(row['Project Manager'])
        pm = _onenode(tr, 'td[position()=8]')

        # Email address
        try:
            row['Project Manager Email'] = _onenode(pm, 'descendant::a/@href')
        except AssertionError:
            _log(row)
            raise

        if row['Project Manager Email'][:7] == 'mailto:':
            row['Project Manager Email'] = unicode(row['Project Manager Email'][7:])
        else:
            msg = 'This is a strange email link: <%s>' % row['Project Manager Email']
            _RRRaise(AssertionError(msg))

        # Name
        row['Project Manager Name'] = _onenode(pm, 'descendant::a').text_content().strip()

        # Phone number
        phone_match = re.match(_PHONE_NUMBER, pm.text_content())
        if phone_match:
            row['Project Manager Phone'] = phone_match.group(1)
        else:
            _log(row)
            msg = 'This is a strange phone number: %s' % pm.text_content()
            _RRRaise(AssertionError(msg))

        # Append to our big lists
        data.append(row)

    data2 = []
    for row in data:
        row2 = {new: row.get(old, None) for old, new in _KEYMAP}
        for k, v in row2.items():
            if type(v) in {lxml.etree._ElementStringResult, str}:
                row2[k] = unicode(v)
        data2.append(row2)

    return data2

def listing_save(data, db):
    data_new = [{
        '_id': doc['permitApplicationNumber'],
        'scriptRuns': [],

        'location': doc['location'],
        'projectDescription': doc['projectDescription'],
        'applicant': doc['applicant'],
        'publicNoticeDate': doc['publicNoticeDate'],
        'expirationDate': doc['expirationDate'],
        'permitApplicationNumber': doc['permitApplicationNumber'],

        'publicNotice': {
            'url': doc['publicNoticeUrl'],
            'data': {},
        },
        'drawings': {
            'url': doc['drawingsUrl'],
            'data': {},
        },

        'projectManager': {
            'email': doc['projectManagerEmail'],
            'name': doc['projectManagerName'],
            'phone': doc['projectManagerPhone'],
        },
    } for doc in data]
    del(data)
    del(doc)

    for doc_new in data_new:
        # If the permitApplicationNumber doesn't exist
        db.permit.update({"_id": doc_new['_id']}, doc_new, upsert = True)

        # Even if it was already there, set it as unprocessed so we know to
        # process it.
        db.permit.update(
            {"_id": doc_new['_id']},
            {"$push": {"scriptRuns": DATETIME}}
        )
        db.permit.update(
            {"_id": doc_new['_id']},
            {"$set": {"publicNotice.processed": False }}
        )
        db.permit.update(
            {"_id": doc_new['_id']},
            {"$set": {"drawings.processed": False }}
        )

_KEYMAP = [
    ('Project Description','projectDescription'),
    ('Applicant','applicant'),
    ('PermitApplication No.','permitApplicationNumber'),
    ('Public Notice Date','publicNoticeDate'),
    ('Public Notice','publicNoticeUrl'),
    ('Location','location'),
    ('Drawings','drawingsUrl'),
    ('Expiration Date','expirationDate'),
    ('Project Manager Email', 'projectManagerEmail'),
    ('Project Manager Name','projectManagerName'),
    ('Project Manager Phone','projectManagerPhone'),
]
_PHONE_NUMBER = re.compile(r'[^0-9]*(\d{3}-\d{3}-\d{4})[^0-9]*')
_NCOL = 8
_COLNAMES = [
    'Project Description',
    'Applicant',
    'Public Notice Date',
    'Expiration Date',
    'PermitApplication No.',
    'View or Download',
    'Location',
    'Project Manager'
]

def _parsedate(rawdate):
    return datetime.datetime.strptime(rawdate, '%m/%d/%Y')

QUIET = False

def _log(foo):
    if QUIET == False:
        print(foo)

def _RRRaise(exception):
    raise exception
    if QUIET:
        print({
            'exception': str(type(exception)),
            'message': str(exception),
            'datetime': datetime.datetime.now(),
            'scraper_run': scraper_run
        })
    else:
        raise exception

PERMIT_APPLICATION_NUMBER_REGEX = re.compile(r'^MVN-[0-9]+-[0-9]+(?:-[A-Z]+)?$')
PERMIT_YEAR = re.compile(r'[12][901][789012][0-9]')

MANUAL_REPLACEMENTS = {
    'MVN 2009-3063 CO (ERRATUM)': 'MVN-2009-3063-CO-(ERRATUM)',
    'MVN 2010-1080 WLL/ MVN 2010 1032 WLL B': 'MVN-2010-1080-WLL_MVN-2010-1032-WLLB',
    'MVN-2010-1080-WLL/ MVN-2010-1032-WLL-A': 'MVN-2010-1080-WLL_MVN-2010-1032-WLL-A',
}
def _clean_permit_application_number(n):
    'Clean up the permit application number.'
    if n[:3] == 'MVN':
        return _clean_mvn_permit_application_number(n)
    elif n[:3] == 'CEM':
        return _clean_cem_permit_application_number(n)
    else:
        raise AssertionError('Unexpected first block in %s' % n)

def _clean_cem_permit_application_number(n):
    'Clean up the permit application number for CEM permits.'
    for c in '/ \\':
        assert c not in n, n
    assert n.upper() == n
    return n

def _clean_mvn_permit_application_number(n):
    'Clean up the permit application number for MVN permits.'

    # If this is a manual one, replace it that way.
    if n in MANUAL_REPLACEMENTS:
        return MANUAL_REPLACEMENTS[n]

    # Remove delimiters
    n = filter(lambda char: char not in '- ', n)

    # Add hyphen delimeters
    n = n[:3] + '-' + n[3:7] + '-' + n[7:]

    # If there's a fourth group
    if re.match(r'.+[0-9][A-Z]+$', n):
        # Add the delimiter
        n = re.sub(r'(.+[0-9])([A-Z]+)$', r'\1-\2', n)
    else:
        if not re.match(r'.+-[0-9]+$', n):
            raise AssertionError('The third group of %s is not all numbers.' % n)

    # Check year
    if 'MVN' != n[:3]:
        raise AssertionError('The first three letters of %s are not "MVN"' % n)

    # Check year
    if not re.match(PERMIT_YEAR, n[4:8]):
        raise AssertionError('The second group of %s doesn\'t seem like a year.' % n)

    # Final check
    if not re.match(PERMIT_APPLICATION_NUMBER_REGEX, n):
        raise AssertionError(
            'Permit application number %s could not be cleaned up.' % n
        )

    return n

def _onenode(html, xpath):
    nodes = html.xpath(xpath)
    if len(nodes) != 1:
        _log(map(lxml.html.tostring, nodes))
        _RRRaise(AssertionError('Not exactly one node'))
    else:
        return nodes[0]

if __name__ == '__main__':
    main()
