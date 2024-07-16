#http://localhost/mreport_002/sync_doctor/syncRep/FAST<url>airnetMreport2009<url>1406244051<url>101
#http://localhost/mreport_002/sync_doctor/syncRep/6143543044844939345044744139543043844744343444941044743444544443452343447449383381381390393450447441395384390381386389382387390384393450447441395382381382

def en_dec():
    mystr1='DEMO<url>airnetMreport2009<url>1234<url>20111221330003'
    mystr1=get_encript(mystr1)
#    9040140241041239345044744139543043844744343444941044743444544444744938338138139039345044744134523434395382383384385393450447441395383381382382382383383382384384381381381384
    return mystr1

def syncRep():
    START='START'
    END='END'
    
    my_str = request.args(0)
    my_str=get_decript(my_str)
    
    if my_str == '':
        msgFail='Failed'
        msgFail = get_encript(msgFail)
        return START+msgFail+END
    else:
        separator_url='<url>'
        url_list_url=my_str.split(separator_url)
        if len(url_list_url)!=4:
            msgFail='Failed'
            msgFail = get_encript(msgFail)
            return START+msgFail+END
        else:
            cid=str(url_list_url[0]).strip().upper()
            http_pass=url_list_url[1]
            sync_code=url_list_url[2]
            rep_id=str(url_list_url[3]).strip().upper()
                        
            compRow=db((db.sm_company_settings.cid==cid)& (db.sm_company_settings.http_pass==http_pass) & (db.sm_company_settings.status=='ACTIVE')).select(db.sm_company_settings.subscription_model,limitby=(0,1))
            if not compRow:
                msgFail='Failed'
                msgFail = get_encript(msgFail)
                return START+msgFail+END
            else:
                repRow=db((db.sm_rep.cid==cid)& (db.sm_rep.rep_id==rep_id)& (db.sm_rep.sync_code==sync_code) & (db.sm_rep.status=='ACTIVE')).select(db.sm_rep.id,db.sm_rep.name,limitby=(0,1))
                if not repRow:
                    msgFail='Failed'
                    msgFail = get_encript(msgFail)
                    return START+msgFail+END
                else:
                    
                    doctorRows=db((db.sm_rep_area.cid==cid)&(db.sm_rep_area.rep_id==rep_id)&(db.sm_doctor_area.cid==cid)&(db.sm_rep_area.area_id==db.sm_doctor_area.area_id)).select(db.sm_doctor_area.doc_id,db.sm_doctor_area.doc_name,orderby=db.sm_doctor_area.doc_id,groupby=db.sm_doctor_area.doc_id)
                    sync_result = '<DOCTOR>'
                    for doctorRow in doctorRows:                           
                        sync_result = sync_result+str(doctorRow.doc_id)+'<fd>'+str(doctorRow.doc_name)+'<fd><rd>'
                    sync_result = sync_result+'</DOCTOR>'
                    
                    if sync_result=='<DOCTOR></DOCTOR>':
                        nodata='No data available'
                        nodata = get_encript(nodata)
                        return START+nodata+END
                    else:
                        sync_result=get_encript(sync_result)
                        return sync_result
                        
