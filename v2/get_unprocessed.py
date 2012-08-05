"""
When run from the command line, this returns a list of documents to be
processed. Output includes the parameters needed for paper in a tab-delimeted
format. These parameters are

* permit
* url
* papertype

Output might look like this.

permit	url	papertype	date
MVN-2010-0024-EII	http://www.mvn.usace.army.mil/ops/regulatory/pdf/MVN-2010-0024-EIIJPN.pdf	publicNotice
MVN-2010-0024-EII	http://www.mvn.usace.army.mil/ops/regulatory/pdf/MVN-2010-0024DWG.pdf	drawing

They are sorted by papertype in order of priority; public notices are first.
"""
import pymongo

def main(outputformat):
    connection = pymongo.Connection('localhost')
    db = connection.wetlands
    print('permit\turl\tpapertype')
    for papertype in {'publicNotice', 'drawing'}:
        if outputformat == 'tsv':
            print_tsv(db, papertype)
        elif outputformat == 'sh':
            print_sh(db, papertype)

def print_sh(db, papertype):
    "Print a paper command the documents queried from the database."
    query = db.permit.find({papertype + '.processed': False})
    for doc in query:
        print('paper '
            "--permit '%s'"
            "--url '%s'"
            "--papertype '%s'"
            % (doc['permitApplicationNumber'], doc[papertype]['url'], papertype)
        ) 

def print_tsv(db, papertype):
    "Print a tsv for the documents queried from the database."
    query = db.permit.find({papertype + '.processed': False})
    for doc in query:
        print('\t'.join([
          doc['permitApplicationNumber'],
          doc[papertype]['url'],
          papertype
       ]))

if __name__ == '__main__':
    main('sh')
