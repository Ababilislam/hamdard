#http://127.0.0.1:8000/mreporting/sync_doctor/syncRep/FAST<url>airnetMreport2009<url>1406244051<url>101
#http://127.0.0.1:8000/mreporting/sync_doctor/syncRep/6143543044844939345044744139543043844744343444941044743444544443452343447449383381381390393450447441395384390381386389382387390384393450447441395382381382

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
                    giftRows=db((db.sm_doctor_gift.cid==cid)&(db.sm_doctor_gift.status=='ACTIVE')).select(db.sm_doctor_gift.gift_id,db.sm_doctor_gift.gift_name,orderby=db.sm_doctor_gift.gift_id)
                    sync_result = '<GIFT>'
                    for giftRow in giftRows:                           
                        sync_result = sync_result+str(giftRow.gift_name)+'<fd>'+str(giftRow.gift_id)+'<fd><rd>'
                    sync_result = sync_result+'</GIFT>'
                    
                    if sync_result=='<GIFT></GIFT>':
                        nodata='No data available'
                        nodata = get_encript(nodata)
                        return START+nodata+END
                    else:
                        sync_result=get_encript(sync_result)
                        return sync_result


#http://127.0.0.1:8000/mreporting/sync_gift/giftSubmit/DEMO<url>airnetMreport2009<url>1234<url>20111221330003<url>D00001<url>G0001fd-fd3rd-rdG0002fd-fd5rd-rd
#http://127.0.0.1:8000/mreporting/sync_gift/giftSubmit/0840140241345234340412393450447441395430438447443434449410447434445444447449383381381390393450447441395382383384385393450447441395383381382382382383383382384384381381381384393450447441395401381381381381382393450447441395404381381381382435433378435433384447433378447433404381381381383435433378435433386447433378447433

def giftSubmit():
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
                    giftRows=db((db.sm_doctor_gift.cid==cid)).select(db.sm_doctor_gift.gift_id,db.sm_doctor_gift.gift_name)
                                            
                    giftList=item_qty_all.split('rd-rd')                        
                    for i in range(len(giftList)):
                        gftIdQty=str(giftList[i]).strip()
                        if gftIdQty=='':
                            break
                        
                        gftIdList=gftIdQty.split('fd-fd')
                        if len(gftIdList)!=2:
                            giftRows=''
                            msgFail='Failed'
                            msgFail = get_encript(msgFail)
                            return START+msgFail+END
                        else:
                            gftID=str(gftIdList[0]).strip().upper()
                            
                            validGift=False
                            for gftRow in giftRows:
                                giftId=str(gftRow.gift_id).strip()
                                giftName=gftRow.gift_name
                                if giftId==gftID:
                                    validGift=True
                                    break
                            
                            if validGift==False:
                                giftRows=''
                                msgFail='Failed'
                                msgFail = get_encript(msgFail)
                                return START+msgFail+END
                            else:                                    
                                gftQty=gftIdList[1]
                                if gftQty.isdigit():
                                    pass
                                else:
                                    giftRows=''
                                    msgFail='Failed'
                                    msgFail = get_encript(msgFail)
                                    return START+msgFail+END
                                
                                if giftStr=='':
                                    giftStr=gftID+','+str(giftName).replace(',', ' ')+','+str(gftQty)
                                else:
                                    giftStr+='fdsep'+gftID+','+str(giftName).replace(',', ' ')+','+str(gftQty)
                    giftRows=''   
                    
                    #----- sample part    
                    sampleStr=''
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

