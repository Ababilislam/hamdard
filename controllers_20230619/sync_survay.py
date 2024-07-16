
def en_dec():
#    mystr1='DEMO<url>airnetMreport2009<url>1234<url>20111221330003<url>D00001<url>aFfd-fd3rd-rdbsfd-fd5rd-rdBFfd-fd3rd-rd'
    mystr1='DEMO<url>airnetMreport2009<url>1234<url>20111221330003<url>D00001<url>test feedback'
    
    mystr1=get_encript(mystr1)
#    0640140234523434410412393450447441395430438447443434449410447434445444447449383381381390393450447441395382383384385393450447441395383381382382382383383382384384381381381384393450447441395401381381381381382393450447441395430403435433378435433384447433378447433431448435433378435433386447433378447433399403435433378435433384447433378447433
    return mystr1

#http://127.0.0.1:8000/mreporting/sync_survay/survaySubmit/DEMO<url>airnetMreport2009<url>1234<url>20111221330003<url>D00001<url>AFfd-fd3rd-rdBSfd-fd5rd-rdBFfd-fd3rd-rd
#http://127.0.0.1:8000/mreporting/sync_survay/survaySubmit/0640140234523434410412393450447441395430438447443434449410447434445444447449383381381390393450447441395382383384385393450447441395383381382382382383383382384384381381381384393450447441395401381381381381382393450447441395430403435433378435433384447433378447433431448435433378435433386447433378447433399403435433378435433384447433378447433

def survaySubmit():
    START='START'
    END='END'
    my_str = request.args(0)
    my_str=get_decript(my_str)
    
    if my_str=='':
        msgFail='Failed'
        msgFail = get_encript(msgFail)
        return START+msgFail+END
    else:
        separator_url='<url>'
        
        url_list_url=my_str.split(separator_url)
        if len(url_list_url)!=6:
            msgFail='Failed'
            msgFail = get_encript(msgFail)
            return START+msgFail+END
        else:
            cid=str(url_list_url[0]).strip().upper()
            http_pass=url_list_url[1]
            sync_code=url_list_url[2]
            rep_id=str(url_list_url[3]).strip().upper()
            doctor_id=str(url_list_url[4]).strip().upper()
            item_qty_all=url_list_url[5]
            
            compRow=db((db.sm_company_settings.cid==cid)& (db.sm_company_settings.http_pass==http_pass) & (db.sm_company_settings.status=='ACTIVE')).select(db.sm_company_settings.subscription_model,limitby=(0,1))
            if not compRow:
                msgFail='Failed'
                msgFail = get_encript(msgFail)
                return START+msgFail+END
            else:
                repRow=db((db.sm_rep.cid==cid)& (db.sm_rep.rep_id==rep_id)& (db.sm_rep.sync_code==sync_code) & (db.sm_rep.status=='ACTIVE')).select(db.sm_rep.name,db.sm_rep.depot_id,limitby=(0,1))
                if not repRow:
                    msgFail='Failed'
                    msgFail = get_encript(msgFail)
                    return START+msgFail+END
                else:
                    rep_name=repRow[0].name
                    depot_id=repRow[0].depot_id
                    
                    #----------------------
                    doctor_name=''
                    depot_Row=db((db.sm_doctor.cid==cid) & (db.sm_doctor.doc_id==doctor_id)).select(db.sm_doctor.doc_name,limitby=(0,1))                        
                    if not depot_Row:
                        msgFail='Failed'
                        msgFail = get_encript(msgFail)
                        return START+msgFail+END
                    else:
                        doctor_name=depot_Row[0].doc_name
                    
                    routeId=''
                    docRoute_Row=db((db.sm_doctor_area.cid==cid) & (db.sm_doctor_area.doc_id==doctor_id)).select(db.sm_doctor_area.area_id,limitby=(0,1))                        
                    if docRoute_Row:
                        routeId=docRoute_Row[0].area_id
                    
                    #------------- gift part
                    giftStr=''
                    
                    #----- sample part    
                    sampleStr=''
                    sampleRows=db(db.sm_item.cid==cid).select(db.sm_item.item_id,db.sm_item.name,db.sm_item.category_id,orderby=db.sm_item.item_id)
                    
                    sampleList=item_qty_all.split('rd-rd')                        
                    for i in range(len(sampleList)):
                        smpIdQty=str(sampleList[i]).strip()
                        if smpIdQty=='':
                            break
                        
                        smpIdList=smpIdQty.split('fd-fd')
                        if len(smpIdList)!=2:
                            sampleRows=''
                            msgFail='Failed'
                            msgFail = get_encript(msgFail)
                            return START+msgFail+END
                        else:
                            smpID=str(smpIdList[0]).strip().upper()
                            
                            validSample=False
                            for smpRow in sampleRows:
                                smpId=str(smpRow.item_id).strip()
                                smpName=smpRow.name                                  
                                if smpId==smpID:
                                    validSample=True
                                    break
                            
                            if validSample==False:
                                sampleRows=''
                                msgFail='Failed'
                                msgFail = get_encript(msgFail)
                                return START+msgFail+END
                            else:
                                smpQty=smpIdList[1]
                                if smpQty.isdigit():
                                    pass
                                else:
                                    sampleRows=''
                                    msgFail='Failed'
                                    msgFail = get_encript(msgFail)
                                    return START+msgFail+END
                                
                                if sampleStr=='':
                                    sampleStr=smpID+','+str(smpName).replace(',', ' ')+','+str(smpQty)
                                else:
                                    sampleStr+='fdsep'+smpID+','+str(smpName).replace(',', ' ')+','+str(smpQty)
                    sampleRows=''
                    #-------------------
                    if (giftStr=='' and sampleStr==''):
                        msgFail='Failed'
                        msgFail = get_encript(msgFail)
                        return START+msgFail+END
                    else:
                        giftnsample=giftStr+'rdsep'+sampleStr
                    
                    feedback=''
                    #-----------------
                    insRes=db.sm_doctor_visit.insert(cid=cid,doc_id=doctor_id,doc_name=doctor_name,rep_id=rep_id,rep_name=rep_name,feedback=feedback,ho_status='0',route_id=routeId,depot_id=depot_id,visit_dtime=datetime_fixed,visit_date=current_date,giftnsample=giftnsample)
                    if insRes:
                        returnStr='success'
                        returnStr = get_encript(returnStr)
                        return START+returnStr+END
                    else:
                        msgFail='Failed'
                        msgFail = get_encript(msgFail)
                        return START+msgFail+END
    
    return dict()


#http://127.0.0.1:8000/mreporting/sync_survay/feed_backSubmit/DEMO<url>airnetMreport2009<url>1234<url>20111221330003<url>D00001<url>nothing
#http://127.0.0.1:8000/mreporting/sync_survay/feed_backSubmit/6840140241041239345044744139543043844744343444941044743444544444744938345234343381381390393450447441395382383384385393450447441395383381382382382383383382384384381381381384393450447441395401381381381381382393450447441395443444449437438443436
def feed_backSubmit():
    START='START'
    END='END'
    my_str = request.args(0)
    my_str=get_decript(my_str)
    
    if my_str=='':
        msgFail='Failed'
        msgFail = get_encript(msgFail)
        return START+msgFail+END
    else:
        separator_url='<url>'
        
        url_list_url=my_str.split(separator_url)
        if len(url_list_url)!=6:
            msgFail='Failed'
            msgFail = get_encript(msgFail)
            return START+msgFail+END
        else:
            cid=str(url_list_url[0]).strip().upper()
            http_pass=url_list_url[1]
            sync_code=url_list_url[2]
            rep_id=str(url_list_url[3]).strip().upper()
            doctor_id=str(url_list_url[4]).strip().upper()
            feed_back=url_list_url[5]
            
            compRow=db((db.sm_company_settings.cid==cid)& (db.sm_company_settings.http_pass==http_pass) & (db.sm_company_settings.status=='ACTIVE')).select(db.sm_company_settings.subscription_model,limitby=(0,1))
            if not compRow:
                msgFail='Failed'
                msgFail = get_encript(msgFail)
                return START+msgFail+END
            else:
                repRow=db((db.sm_rep.cid==cid)& (db.sm_rep.rep_id==rep_id)& (db.sm_rep.sync_code==sync_code) & (db.sm_rep.status=='ACTIVE')).select(db.sm_rep.name,db.sm_rep.depot_id,limitby=(0,1))
                if not repRow:
                    msgFail='Failed'
                    msgFail = get_encript(msgFail)
                    return START+msgFail+END
                else:
                    rep_name=repRow[0].name
                    depot_id=repRow[0].depot_id
                    
                    #----------------------
                    doctor_name=''
                    depot_Row=db((db.sm_doctor.cid==cid) & (db.sm_doctor.doc_id==doctor_id)).select(db.sm_doctor.doc_name,limitby=(0,1))                        
                    if not depot_Row:
                        msgFail='Failed'
                        msgFail = get_encript(msgFail)
                        return START+msgFail+END
                    else:
                        doctor_name=depot_Row[0].doc_name
                    
                    routeId=''
                    docRoute_Row=db((db.sm_doctor_area.cid==cid) & (db.sm_doctor_area.doc_id==doctor_id)).select(db.sm_doctor_area.area_id,limitby=(0,1))                        
                    if docRoute_Row:
                        routeId=docRoute_Row[0].area_id
                    
                    #----------------- gift part
                    giftStr=''
                    #----- sample part    
                    sampleStr=''
                    #-----------------
                    giftnsample=''
                    #-----------------
                    feedback=feed_back
                    #-----------------
                    insRes=db.sm_doctor_visit.insert(cid=cid,doc_id=doctor_id,doc_name=doctor_name,rep_id=rep_id,rep_name=rep_name,feedback=feedback,ho_status='0',route_id=routeId,depot_id=depot_id,visit_dtime=datetime_fixed,visit_date=current_date,giftnsample=giftnsample)
                    if insRes:
                        returnStr='success'
                        returnStr = get_encript(returnStr)
                        return START+returnStr+END
                    else:
                        msgFail='Failed'
                        msgFail = get_encript(msgFail)
                        return START+msgFail+END
    
    return dict()


