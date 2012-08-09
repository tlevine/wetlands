import pymongo
connection = pymongo.Connection('localhost')
db = connection.wetlands

WEB_DIR=u'www.mvn.usace.army.mil/ops/regulatory/'
PUBLIC_NOTICE=u'http://wetlands.thomaslevine.com/pdfs/%s/public_notice.pdf'

for permit in db.permit.find():
    public_notice = db.public_notice.find_one(_id=permit['_id'])
    row = {
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
        "Total Acres": sum(permit.get('Acres', [])),
        "CUP": ','.join(permit.get('CUP', [])),
        "WQC": permit.get('WQC', ''),
#       "Coordinates": 

        # Whether particular terms are in the public notice
        "Says 'Section 10'": permit.get('Section 10', False),
        "Says 'Section 404'": permit.get('Section 404', False),
        "Says 'Drill'": permit.get('Drill', False),
        "Says 'Road'": permit.get('Road', False),
        "Says 'Mitigation Bank'": permit.get('Mitigation Bank', False),
    }
    print row
