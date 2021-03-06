"""
When run from the command line, this returns a documents to be processed.
Output includes the parameters needed for paper in a tab-delimeted format.
These parameters are

* permit
* url
* papertype

Output might look like this.

permit	url	papertype
MVN-2010-0024-EII	http://www.mvn.usace.army.mil/ops/regulatory/pdf/MVN-2010-0024-EIIJPN.pdf	publicNotice

It returns publicNotices until all of those are processed, then it returns
drawings.
"""
import sys
import pymongo

def main(outputformat):
    'outputformat must be "sh", "tsv" or "permitonly"'
    connection = pymongo.Connection('localhost')
    db = connection.wetlands
    for papertype in ['publicNotice', 'drawings']:
        doc = db.permit.find_one({papertype + '.processed': False})
        if doc == None:
            print 'No more documents to process'
            exit(1)

        elif doc[papertype]['url'] == None:
            continue

        if papertype == 'drawings':
            shpapertype = 'drawing'
        elif papertype == 'publicNotice':
            shpapertype = 'public_notice'

        if outputformat == 'tsv':
            print_tsv(doc, papertype, shpapertype)
        elif outputformat == 'sh':
            print_sh(doc, papertype, shpapertype)

        # Only print one
        break

def print_sh(doc, papertype, shpapertype):
    "Print a paper command the documents queried from the database."
    print('paper '
        "--permit '%s' "
        "--url '%s' "
        "--papertype '%s' "
        % (doc['permitApplicationNumber'], doc[papertype]['url'], shpapertype)
    ) 

def print_tsv(doc, papertype, shpapertype):
    "Print a tsv for the documents queried from the database."
    print('permit\turl\tpapertype')
    print('\t'.join([
      doc['permitApplicationNumber'],
      doc[papertype]['url'],
      shpapertype
    ]))

if __name__ == '__main__':
    main(sys.argv[1])
