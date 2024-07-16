#device
#password
#============================= 
import urllib2, random, string

import datetime
import time

# http://127.0.0.1:8000/novivo/change_pw/password?cid=novivo&rep_id=NHL-0179&rep_pass=1234
def password():
    # return 'hjkhjk'
    btn_change_password=request.vars.btn_change_password
    cid = 'HAMDARD'#str(request.vars.cid).strip().upper()
    rep_id=str(request.vars.rep_id).strip().upper()
    rep_idc=str(request.vars.rep_id).strip().upper()
    password=str(request.vars.old_pass).strip()
    # return password
    checkRep=  db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id)  & (db.sm_rep.password == password) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.rep_id,db.sm_rep.password,limitby=(0, 1))
    # return rep_id
    if checkRep:  
        # return btn_change_password
        if btn_change_password:
            old_password=str(request.vars.old_pass).strip()   

            new_password=str(request.vars.new_pass).strip() 
            confirm_password = str(request.vars.confirm_pass).strip()
            


            if not(cid==''or rep_idc==''or old_password==''or new_password==''or confirm_password==''):
                     
                user_password = checkRep[0].password
                if user_password != old_password:
                    # return 'hjk'
                    response.flash ='Old password is not accurate'
                # return 'dict()'
                else:
                    if (new_password!=confirm_password):
                        response.flash='New & confirm password is not accurate'
                    else:
                        try:               
                            db((db.sm_rep.cid == cid)& (db.sm_rep.rep_id == rep_idc)  & (db.sm_rep.password == old_password) & (db.sm_rep.status == 'ACTIVE')).update(password=confirm_password)  
                            # success_msg='<table><tr><td></td></tr><tr><td style="color:#FBFBFB;text-align:center;padding:2px">Please Login Again</td></tr>'
                            # return 'jkj'
                            response.flash='Password Changed Successfully.'
                        except:
                            response.flash='Process Error'

            else:
                response.flash = 'All fields must be required !'

        return dict()
    else:
        return dict()



    