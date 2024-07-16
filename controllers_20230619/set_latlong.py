from random import randint
import urllib2
import calendar


# http://127.0.0.1:8000/mrepnovelta/syncmobile_ofline_ppm_report/check_user?cid=NOVELTA&rep_id=1001&rep_pass=123&synccode=2150
def set_latlong():
    lat = ''
    long = ''
    visited_id = ''
    visit_time=''
    visited_latlong=''
    trackingRows = db((db.sm_tracking_table.cid == "BIOPHARMA") & (db.sm_tracking_table.call_type == "DCR") &  (db.sm_tracking_table.id < 793)).select(db.sm_tracking_table.ALL, orderby=db.sm_tracking_table.visit_time ,limitby=(0, 20))
#               
    for trackingRows in trackingRows:
        visited_id = trackingRows.visited_id
        visit_time=trackingRows.visit_time
        visited_latlong=trackingRows.visited_latlong
        
        lat=visited_latlong.split(',')[0]
        long=visited_latlong.split(',')[1]
        
        db((db.sm_doctor_visit.cid == "BIOPHARMA") & (db.sm_doctor_visit.doc_id == visited_id) & (db.sm_doctor_visit.visit_dtime == visit_time)).update(latitude=lat,longitude=long)

                    
    return "DONE"




