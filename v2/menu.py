import pymongo
import datetime
import lxml.html
import re
from unidecode import unidecode

DAY = datetime.date.today()
#connection = pymongo.Connection('desk')
#db = connection.wetlands

_PHONE_NUMBER = re.compile(r'[^0-9]*(\d{3}-\d{3}-\d{4})[^0-9]*')
_NCOL = 8
_COLNAMES = [
    'Project Description',
    'Applicant',
    'Public Notice Date',
    'Expiration Date',
#    'Permit Application No.',
    'PermitApplication No.',
    'View or Download',
    'Location',
    'Project Manager'
]

def _parsedate(rawdate):
    return datetime.datetime.strptime(rawdate, '%m/%d/%Y').date()

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


def menu_retrieve():
    return rawtext

def menu_parse(rawtext):
    # There are more data in the comments!
    text_with_locations = rawtext.replace('<!--', '').replace('-->', '').replace('&nbsp;', ' ')
    unicodetext = unidecode(text_with_locations)
    html = lxml.html.fromstring(unicodetext)
    table = _onenode(html, '//table[@width="570" and @border="1" and @cellpadding="0" and @cellspacing="0" and @bordercolor="#ffffff" and @bgcolor="#efefef"]')
    trs = table.xpath('tr')

    # Getting the cells 
    thead = [td.text_content().strip() for td in trs.pop(0)]
    if len(thead) != self.NCOL:
        print(thead)
        RRRaise(AssertionError('The table header does not have exactly %d cells.' % self.NCOL))

    if thead != self.COLNAMES:
        pairs = zip(thead, self.COLNAMES)
        for a, b in pairs:
            print(a, b), 'Match' if a == b else 'Differ'
        RRRaise(AssertionError('The table header does not have the right names.'))

    # List of dictionaries of data
    data = []
    publicnotices = []
    drawings = []
    for tr in trs:
        if len(tr.xpath('td')) != self.NCOL:
            RRRaise(AssertionError('The table row does not have exactly %d cells.' % self.NCOL))

        # As a dict
        row = dict(zip(thead, [td.text_content().strip() for td in tr.xpath('td')]))

        # Dates
        row['Public Notice Date'] = self.parsedate(row['Public Notice Date'])
        row['Expiration Date'] = self.parsedate(row['Expiration Date'])

        # PDF download links
        del(row['View or Download'])
        pdfkeys = set(tr.xpath('td[position()=6]/descendant::a/text()'))
        if not pdfkeys.issubset({'Public Notice', 'Drawings'}):
            print(pdfkeys)
            RRRaise(AssertionError('The table row has unexpected hyperlinks.'))
        if len(pdfkeys) == 0:
            print row
            RRRaise(AssertionError('No pdf hyperlinks found for permit %s.' % row['PermitApplication No.']))
        for key in ['Public Notice', 'Drawings']:
            try:
                row[key] = unicode(_onenode(tr, 'td/descendant::a[text()="%s"]/@href' % key))
            except AssertionError:
                if key == 'Public Notice':
                    raise
                else:
                    continue

            if row[key][:4] != 'pdf/':
                RRRaise(AssertionError('The %s pdf link doesn\'t have the expected path.' % key))

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
            RRRaise(AssertionError(msg))

        # Name 
        row['Project Manager Name'] = _onenode(pm, 'descendant::a').text_content().strip()

        # Phone number
        phone_match = re.match(self.PHONE_NUMBER, pm.text_content())
        if phone_match:
            row['Project Manager Phone'] = phone_match.group(1)
        else:
            print(row)
            msg = 'This is a strange phone number: %s' % pm.text_content()
            RRRaise(AssertionError(msg))

        # References
        row.update(self.reference())

        # Append to our big lists
        data.append(row)
        cwd = 'http://www.mvn.usace.army.mil/ops/regulatory/'
        publicnotices.append(PublicNotice(
            url = cwd + row['Public Notice'],
            permit = row['PermitApplication No.']
        ))
        if row.has_key('Drawings'):
            drawings.append(Drawings(
                url = cwd + row['Drawings'],
                permit = row['PermitApplication No.']
            ))

    dt.insert(data, 'ListingData')
    return publicnotices + drawings

def menu_save(data, db):
    data['_id'] = data['permitId']
    db.permits.save(data)


def _onenode(html, xpath):
    nodes = html.xpath(xpath)
    if len(nodes) != 1:
        print(map(lxml.html.tostring, nodes))
        RRRaise(AssertionError('Not exactly one node'))
    else:
        return nodes[0]
