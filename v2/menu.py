import pymongo
import datetime

DAY = datetime.date.today()
connection = pymongo.Connection('desk')
db = connection.wetlands

def menu_retrieve():
    return html

def menu_parse(html):
    return data

def menu_save(data, db):
    data['_id'] = data['permitId']
    db.permits.save(data)
