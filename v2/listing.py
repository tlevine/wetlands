import pymongo
import datetime
import lxml.html, lxml.etree
import re
from unidecode import unidecode
from urllib2 import urlopen

DATETIME = datetime.datetime.now()
#connection = pymongo.Connection('desk')
#db = connection.wetlands

def listing_retrieve(url = 'http://www.mvn.usace.army.mil/ops/regulatory/publicnotices.asp?ShowLocationOrder=False', stamp = datetime.datetime.now().isoformat()):
    "Change the url for testing.")
    rawtext = urlopen().read()
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
        print(thead)
        _RRRaise(AssertionError('The table header does not have exactly %d cells.' % _NCOL))

    if thead != _COLNAMES:
        pairs = zip(thead, _COLNAMES)
        for a, b in pairs:
            print(a, b), 'Match' if a == b else 'Differ'
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

        # Dates
        row['Public Notice Date'] = _parsedate(row['Public Notice Date'])
        row['Expiration Date'] = _parsedate(row['Expiration Date'])

        # PDF download links
        del(row['View or Download'])
        pdfkeys = set(tr.xpath('td[position()=6]/descendant::a/text()'))
        if not pdfkeys.issubset({'Public Notice', 'Drawings'}):
            print(pdfkeys)
            _RRRaise(AssertionError('The table row has unexpected hyperlinks.'))
        if len(pdfkeys) == 0:
            print row
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
            print(row)
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
            print(row)
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
    doc_new = {
        'scriptRuns': [DATETIME],

        'location': data['location'],
        'projectDescription': data['projectDescription'],
        'applicant': data['applicant'],
        'publicNoticeDate': data['publicNoticeDate'],
        'expirationDate': data['expirationDate'],
        'permitApplicationNumber': data['permitApplicationNumber'],

        'publicNotice': {
            'url': data['publicNoticeUrl'],
            'processed': False,
            'data': {},
        },
        'drawings': {
            'url': data['drawingsUrl'],
            'processed': False,
            'data': {},
        },

        'projectManager': {
            'email': data['projectManagerEmail'],
            'name': data['projectManagerName'],
            'phone': data['projectManagerPhone'],
        },
    }

    # If the permitApplicationNumber doesn't exist,
    # db.permits.save(doc_new)

    # If it does,
    # db.permits.
    #   append the current DATETIME to scriptRuns
    #   set drawings.processed to false 

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
    return datetime.datetime.strptime(rawdate, '%m/%d/%Y').date()

QUIET = False
def _RRRaise(exception):
    if QUIET:
        dt.insert({
            'exception': str(type(exception)),
            'message': str(exception),
            'datetime': datetime.datetime.now(),
            'scraper_run': scraper_run
        }, 'exceptions')
    else:
        raise exception


def _onenode(html, xpath):
    nodes = html.xpath(xpath)
    if len(nodes) != 1:
        print(map(lxml.html.tostring, nodes))
        _RRRaise(AssertionError('Not exactly one node'))
    else:
        return nodes[0]
