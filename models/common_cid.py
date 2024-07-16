import datetime

db = DAL('mysql://root:@localhost/hamdard')
# db = DAL('mysql://w-001-replica%visitors:visitors123456@w-001-replica.mysql.database.azure.com/visitors', decode_credentials=True)

mreporting_http_pass = 'abC321'
date_fixed = datetime.datetime.now() + datetime.timedelta(hours=6)
# date_fixed_get
