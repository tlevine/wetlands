"""
When run from the command line, this returns a list of documents to be
processed. Output includes the parameters needed for paper in a tab-delimeted
format. These parameters are

* permit
* url
* papertype
* date

Output might look like this.

permit	url	papertype	date
MVN-2010-0024-EII	http://www.mvn.usace.army.mil/ops/regulatory/pdf/MVN-2010-0024-EIIJPN.pdf	public_notice	2012-08-05
MVN-2010-0024-EII	http://www.mvn.usace.army.mil/ops/regulatory/pdf/MVN-2010-0024DWG.pdf	drawings	2012-08-05

They are sorted by papertype and date in order of priority. First, they are
sorted by paper type, with public notices first. Within paper type, they are
sorted by date, with old dates first.
"""
import pymongo

connection = pymongo.Connection('localhost')
db = connection.wetlands

