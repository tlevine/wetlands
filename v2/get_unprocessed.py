"""
When run from the command line, this returns a list of documents to be
processed. Output includes the parameters needed for paper in a tab-delimeted
format. These parameters are

* permit
* url
* papertype

Output might look like this.

permit	url	papertype	date
MVN-2010-0024-EII	http://www.mvn.usace.army.mil/ops/regulatory/pdf/MVN-2010-0024-EIIJPN.pdf	public_notice
MVN-2010-0024-EII	http://www.mvn.usace.army.mil/ops/regulatory/pdf/MVN-2010-0024DWG.pdf	drawings

They are sorted by papertype in order of priority; public notices are first.
"""
import pymongo

connection = pymongo.Connection('localhost')
db = connection.wetlands
# db.permits.find_one
