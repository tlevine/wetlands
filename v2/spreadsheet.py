import datetime
import csv
import pymongo
connection = pymongo.Connection('localhost')
db = connection.wetlands

WEB_DIR=u'www.mvn.usace.army.mil/ops/regulatory/'
# PUBLIC_NOTICE=u'http://wetlands.thomaslevine.com/pdfs/%s/public_notice.pdf'
PUBLIC_NOTICE=u'http://chainsaw.chickenkiller.com:1419/pdfs/%s/public_notice.pdf'

spreadsheetname = datetime.date.today().isoformat() + '.csv'
f = open(spreadsheetname, 'w')
fieldnames = [
    "Permit Application No.",

    # Information from the listings page
    "Applicant",
#   "Drawings URL",
    "Expiration Date",
    "Location",
    "Project Description",
    "Project Manager Phone",
    "Project Manager Email",
    "Project Manager Name",
    "Public Notice Date",
#   "Public Notice URL",
    "Public Notice URL",

    # Information from the public notice
    "Total Acres",
    "CUP",
    "WQC",
#   "Coordinates",

    # Whether particular terms are in the public notice
    "Says 'Section 10'",
    "Says 'Section 404'",
    "Says 'Drill'",
    "Says 'Road'",
    "Says 'Mitigation Bank'",
]
c = csv.DictWriter(f, fieldnames)
c.writeheader()

for permit in db.permit.find():
    public_notice = db.public_notice.find_one({'_id': permit['_id']})
    # assert permit['_id'] == public_notice['_id']
    c.writerow({
        "Permit Application No.": permit['_id'],

        # Information from the listings page
        "Applicant": permit['applicant'],
#       "Drawings URL": WEB_DIR + permit['drawings']['url'] if 'drawings' in permit else '',
        "Expiration Date": permit['expirationDate'],
        "Location": permit["location"], 
        "Project Description": permit["projectDescription"],
        "Project Manager Phone": permit["projectManager"]["phone"],
        "Project Manager Email": permit["projectManager"]["email"],
        "Project Manager Name": permit["projectManager"]["name"],
        "Public Notice Date": permit["publicNoticeDate"],
#       "Public Notice URL": permit["publicNotice"]["url"],
        "Public Notice URL": PUBLIC_NOTICE % permit['_id'],

        # Information from the public notice
        "Total Acres": sum(public_notice['Acres']),
        "CUP": ','.join(public_notice['CUP']),
        "WQC": public_notice['WQC'],
#       "Coordinates": 

        # Whether particular terms are in the public notice
        "Says 'Section 10'": public_notice['Section 10'],
        "Says 'Section 404'": public_notice['Section 404'],
        "Says 'Drill'": public_notice['Drill'],
        "Says 'Road'": public_notice['Road'],
        "Says 'Mitigation Bank'": public_notice['Mitigation Bank'],
    })
    del(permit)
    del(public_notice)


i = open('index.html', 'w')
i.write('<h1>Army Corps 404 Website Scraper Output</h1>')
i.write(
    '<p>The most recent spreadsheet is <a href="%s">here</a>, '
    'and the pdf files are <a href="pdfs">here</a>.</p>' % spreadsheetname
)
i.write('<p>Read more <a href="https://github.com/tlevine/wetlands">here</a>.</p>')
