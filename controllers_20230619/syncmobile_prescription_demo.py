from random import randint
import urllib2
import calendar
import urllib

def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month / 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year, month)[1])
    return datetime.date(year, month, day)
def deduct_months(sourcedate, months):
    month = sourcedate.month - 1 - months
    year = sourcedate.year + month / 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year, month)[1])
    return datetime.date(year, month, day)


# http://127.0.0.1:8000/mrepacme/syncmobile_prescription/check_user?cid=BIOPHARMA&rep_id=DKC-156&rep_pass=1234&synccode=


def check_user():
    randNumber = randint(1001, 9999)

    retStatus = ''
    
    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.rep_pass).strip()
    synccode = str(request.vars.synccode).strip()
    
    campaign_doc_str = str(request.vars.campaign_doc_str).strip()
#    return campaign_doc_str

    compRow = db((db.sm_company_settings.cid == cid) & (db.sm_company_settings.status == 'ACTIVE')).select(db.sm_company_settings.cid, limitby=(0, 1))
    if not compRow:
        return 'FAILED<SYNCDATA>Invalid Company'
    else:
        repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.id, db.sm_rep.name, db.sm_rep.sync_count, db.sm_rep.first_sync_date, db.sm_rep.user_type, db.sm_rep.depot_id, db.sm_rep.level_id, db.sm_rep.field2, limitby=(0, 1))
#        return db._lastsql
        if not repRow:
           retStatus = 'FAILED<SYNCDATA>Invalid Authorization'
           return retStatus
        else:
            rep_name = repRow[0].name
            depot_id = repRow[0].depot_id


            sync_code = str(randNumber)
            sync_count = int(repRow[0].sync_count) + 1
            first_sync_date = repRow[0].first_sync_date
            user_type = repRow[0].user_type

            level_id = repRow[0].level_id
            depth = repRow[0].field2
            level = 'level' + str(depth)

            last_sync_date = date_fixed
            if first_sync_date == None:
                first_sync_date = date_fixed
            
            rep_update = repRow[0].update_record(sync_code_servey=sync_code, first_sync_date=first_sync_date, last_sync_date=last_sync_date, sync_count=sync_count)

            
            # set type(Rep)
#             return user_type

            if (user_type == 'survey'):

                #------ market list
                marketStr = ''

                marketRows = db((db.sm_level.cid == cid) & (db.sm_level.depth == '0')).select(db.sm_level.level_id, db.sm_level.level_name, orderby=db.sm_level.level_name, groupby=db.sm_level.level_id)
#                 return marketRows
                for marketRow in marketRows:
                    area_id = marketRow.level_id
                    area_name = marketRow.level_name

                    if marketStr == '':
                        marketStr = str(area_id) + '<fd>' + str(area_name)
                    else:
                        marketStr += '<rd>' + str(area_id) + '<fd>' + str(area_name)

                #-------------- Product list
#                 return marketStr
                productStr = ''
                productStr = ''
                productRows = db(db.sm_company_settings.cid == cid).select(db.sm_company_settings.item_list_mobile, limitby=(0,1))
                for productRow in productRows:
                    productStr = productRow.item_list_mobile
                    
                #-------------- Merchandizing list
                merchandizingStr = ''


                #-------------- Dealer list
                depotName = ''
                dealertRows = db((db.sm_depot.cid == cid) & (db.sm_depot.depot_id == depot_id)).select(db.sm_depot.name, limitby=(0, 1))
#                return db._lastsql
                if dealertRows:
                    depotName = dealertRows[0].name
                dealerStr = str(depot_id) + '<fd>' + str(depotName)

                #------------ Brand List
                brandStr = ''


                #------------ Complain Type List
                complainTypeStr = ''


                #------------ Complain From List
                compFromStr = ''


                #------------ TASK_TYPE List
                taskTypeStr = ''


                #------------ Region List
                regionStr = ''
#                 levelRows = db((db.sm_level.cid == cid) & (db.sm_level.depot_id == depot_id)).select(db.sm_level.level0, groupby=db.sm_level.level0, limitby=(0, 1))
#                 for levelRow in levelRows:
#                     level0_id = levelRow.level0
# 
#                     level0Rows = db((db.sm_level.cid == cid) & (db.sm_level.level_id == level0_id)).select(db.sm_level.level_id, db.sm_level.level_name, limitby=(0, 1))
#                     for level0Row in level0Rows:
#                         level_id = level0Row.level_id
#                         level_name = level0Row.level_name
# 
#                         if regionStr == '':
#                             regionStr = str(level_id) + '<fd>' + str(level_name)
#                         else:
#                             regionStr += '<rd>' + str(level_id) + '<fd>' + str(level_name)


                #------------Gift list

                giftStr = ''
                      
                        
                        
                
                #------------ppm list

                ppmStr = ''

                #------------Client Category list

                clienttCatStr = ''


#                 ------------------------------Market Client List Start-----------------------------------------
                clientStr = ''



#                 ------------------------------Menu List Start-----------------------------------------
                menuStr = ''


#                ----------------------------Doctor list start-----------------------
                doctorStr = ''
#                 doctorRows = db((db.sm_doctor.cid == cid) & (db.sm_doctor.status == 'ACTIVE') & (db.sm_doctor_area.cid == cid) & (db.sm_doctor_area.doc_id == db.sm_doctor.doc_id) & (db.sm_doctor_area.area_id == area_id) ).select(db.sm_doctor.doc_id, db.sm_doctor.doc_name, db.sm_doctor_area.area_id, orderby=db.sm_doctor_area.area_id|db.sm_doctor.doc_name)
# #                return db._lastsql
#                 if not doctorRows:
#                     pass
# #                    retStatus = 'FAILED<SYNCDATA>Doctor not available'
# #                    return retStatus
#                 else:
#                    
#                     doctor_area_past=''
#                     srart_a_flag=0
#                     doctorStr_flag=0
#                     for doctorRow in doctorRows:
#                         doctor_id = doctorRow.sm_doctor.doc_id
#                         doctor_name = doctorRow.sm_doctor.doc_name
#                         doctor_area = doctorRow.sm_doctor_area.area_id
#                         if (doctor_area_past!=doctor_area):
#                             
#                             if (srart_a_flag==0):
#                                 doctorStr="<"+doctor_area+">"
#                                 
#                             else:
#                                 doctorStr=doctorStr+"</"+doctor_area_past+">"+"<"+doctor_area+">"
#                                 doctorStr_flag=0
#                         if doctorStr_flag == 0:
#                             doctorStr = doctorStr+str(doctor_id) + '<fd>' + str(doctor_name)
#                             doctorStr_flag=1
#                         else:
#                             doctorStr = doctorStr+'<rd>' + str(doctor_id) + '<fd>' + str(doctor_name)
#                         doctor_area_past=doctor_area
#                         srart_a_flag=1
#                     if (doctorStr!=''):
#                         doctorStr=doctorStr+ "</"+doctor_area+">"
#             ----------------------------Doctor list end----------------------------------




#                return doctorStr 

                regionStr=''
#                return user_type
#                return 'SUCCESS<SYNCDATA>' + str(sync_code) 
                return 'SUCCESS<SYNCDATA>' + str(sync_code) + '<SYNCDATA>' + str(marketStr) + '<SYNCDATA>' + str(productStr) + '<SYNCDATA>' + str(merchandizingStr) + '<SYNCDATA>' + str(dealerStr) + '<SYNCDATA>' + str(brandStr) + '<SYNCDATA>' + str(complainTypeStr) + '<SYNCDATA>' + str(compFromStr) + '<SYNCDATA>' + str(taskTypeStr) + '<SYNCDATA>' + str(regionStr) + '<SYNCDATA>' + str(giftStr) + '<SYNCDATA>' + str(clienttCatStr) + '<SYNCDATA>' + str(clientStr) + '<SYNCDATA>' + str(menuStr)+ '<SYNCDATA>' +str(ppmStr) + '<SYNCDATA>' + str(user_type)+ '<SYNCDATA>' +str(doctorStr)


           
def getrigion():
    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = urllib.unquote(str(request.vars.rep_pass).strip().decode('utf8'))
    synccode = str(request.vars.synccode).strip()
    zoneID = str(request.vars.zoneId).strip()
    marketStr = ''

    marketRows = db((db.sm_level.cid == cid) & (db.sm_level.depth == '1') & (db.sm_level.level0 == zoneID)).select(db.sm_level.level_id, db.sm_level.level_name, orderby=db.sm_level.level_name, groupby=db.sm_level.level_id)
#                 return marketRows
    for marketRow in marketRows:
        area_id = marketRow.level_id
        area_name = marketRow.level_name

        if marketStr == '':
            marketStr = str(area_id) + '<fd>' + str(area_name)
        else:
            marketStr += '<rd>' + str(area_id) + '<fd>' + str(area_name)
    return 'SUCCESS'+'<SYNCDATA>'+str(marketStr)   

def getrsm():
    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = urllib.unquote(str(request.vars.rep_pass).strip().decode('utf8'))
    synccode = str(request.vars.synccode).strip()
    rsmID = str(request.vars.rsmID).strip()
    marketStr = ''

    marketRows = db((db.sm_level.cid == cid) & (db.sm_level.depth == '2') & (db.sm_level.level1 == rsmID)).select(db.sm_level.level_id, db.sm_level.level_name, orderby=db.sm_level.level_name, groupby=db.sm_level.level_id)
#     return db._lastsql
    for marketRow in marketRows:
        area_id = marketRow.level_id
        area_name = marketRow.level_name

        if marketStr == '':
            marketStr = str(area_id) + '<fd>' + str(area_name)
        else:
            marketStr += '<rd>' + str(area_id) + '<fd>' + str(area_name)
    return 'SUCCESS'+'<SYNCDATA>'+str(marketStr) 

def getfm():
    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = urllib.unquote(str(request.vars.rep_pass).strip().decode('utf8'))
    synccode = str(request.vars.synccode).strip()
    fmID = str(request.vars.fmID).strip()
    marketStr = ''

    marketRows = db((db.sm_level.cid == cid) & (db.sm_level.depth == '3') & (db.sm_level.level2 == fmID)).select(db.sm_level.level_id, db.sm_level.level_name, orderby=db.sm_level.level_name, groupby=db.sm_level.level_id)
#                 return marketRows
    for marketRow in marketRows:
        area_id = marketRow.level_id
        area_name = marketRow.level_name

        if marketStr == '':
            marketStr = str(area_id) + '<fd>' + str(area_name)
        else:
            marketStr += '<rd>' + str(area_id) + '<fd>' + str(area_name)
    return 'SUCCESS'+'<SYNCDATA>'+str(marketStr)       



def getDoctor():
    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = urllib.unquote(str(request.vars.rep_pass).strip().decode('utf8'))
    synccode = str(request.vars.synccode).strip()
    marketId = str(request.vars.marketId).strip()
#     return marketId
    doctorStr = ''

    doctorRows = db((db.sm_doctor_area.cid == cid) & (db.sm_doctor_area.area_id == marketId)).select(db.sm_doctor_area.doc_id, db.sm_doctor_area.doc_name, orderby=db.sm_doctor_area.doc_name, groupby=db.sm_doctor_area.doc_id)
    for doctorRows in doctorRows:
        doc_id = doctorRows.doc_id
        doc_name = doctorRows.doc_name

        if doctorStr == '':
            doctorStr = str(doc_id) + '<fd>' + str(doc_name)
        else:
            doctorStr += '<rd>' + str(doc_id) + '<fd>' + str(doc_name)
    return 'SUCCESS'+'<SYNCDATA>'+str(doctorStr)   






# http://127.0.0.1:8000/lscmreporting/syncmobile/visitSubmit?cid=LSCRM&rep_id=101&rep_pass=123&synccode=5771&client_id=1&visit_type=&schedule_date=&market_info=1&order_info=1&merchandizing=1&lat=0&long=0
# http://127.0.0.1:8000/lscmreporting/syncmobile/visitSubmit?cid=LSCRM&rep_id= 1004&rep_pass=6085&synccode=&client_id=R100585&visit_type=Scheduled&market_info= Akiz <fd> 500 <fd> 2000 <fd> 12000 <fd> 320 <fd> 2 <fd> 1.0 <fd> Good <rd>Seven Ring <fd> 200 <fd> 800 <fd> 3000 <fd> 400 <fd> 0  <fd> 5 <fd> So Good &order_info=1800106001 <fd> 5 <rd>1800201001<fd> 100&merchandizing=1 <fd> Calender <fd> 2 <fd> 2014-09-08 <fd> YES <fd> GOOD<fd> NO <fd> 0 <rd>2 <fd> Wall Paint <fd> 1 <fd> 2014-09-01 <fd> NO <fd> BAD <fd> NO<fd> 1 &lat=0&long=0
def prescription_submit():
    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = urllib.unquote(str(request.vars.rep_pass).strip().decode('utf8'))
    synccode = str(request.vars.synccode).strip()
    campaign_doc_str = str(request.vars.campaign_doc_str).strip()
#    return campaign_doc_str
    areaId = str(request.vars.areaId).strip()
    
    
    
    
    doctor_id = str(request.vars.doctor_id).strip()
    doctor_name = urllib.unquote(str(request.vars.doctor_name).strip().upper().decode('utf8'))
    
    
    medicine_1 = urllib.unquote(str(request.vars.medicine_1).strip().decode('utf8'))
    medicine_2 = urllib.unquote(str(request.vars.medicine_2).strip().decode('utf8'))
    medicine_3 = urllib.unquote(str(request.vars.medicine_3).strip().decode('utf8'))
    medicine_4 = urllib.unquote(str(request.vars.medicine_4).strip().decode('utf8'))
    medicine_5 = urllib.unquote(str(request.vars.medicine_5).strip().decode('utf8'))
    
    
    
    latitude = request.vars.latitude
    longitude = request.vars.longitude
    image_name = request.vars.pres_photo
    image_path=''
    
    
    if latitude == '' or latitude == None:
        latitude = 0
    if longitude == '' or longitude == None:
        longitude = 0
    
    lat_long = str(latitude) + ',' + str(longitude)
    
    submit_date = current_date
    firstDate = first_currentDate
    
    areaRow = db((db.sm_level.cid == cid) & (db.sm_level.level_id == areaId) ).select(db.sm_level.ALL, limitby=(0, 1))        
    if not areaRow:
       return 'FAILED<SYNCDATA>Invalid Route'
    else:
        area_name = areaRow[0].level_name
        tl_id= areaRow[0].level1
        tl_name= areaRow[0].level1_name
        reg_id= areaRow[0].level0
        reg_name= areaRow[0].level0_name
            
            
    compRow = db((db.sm_company_settings.cid == cid) & (db.sm_company_settings.status == 'ACTIVE')).select(db.sm_company_settings.cid, limitby=(0, 1))
    if not compRow:
        return 'FAILED<SYNCDATA>Invalid Company'
    else:
        repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.sync_code_servey == synccode) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.rep_id, db.sm_rep.name, db.sm_rep.mobile_no, db.sm_rep.user_type, db.sm_rep.level_id, limitby=(0, 1))
        
        if not repRow:
           return 'FAILED<SYNCDATA>Invalid Authorization'
        else:
            rep_name = repRow[0].name
            mobile_no = repRow[0].mobile_no
            user_type = repRow[0].user_type
            
            #-------------------            
            sl=1
            headRow=db(db.sm_prescription_head.cid == cid).select(db.sm_prescription_head.sl,orderby=~db.sm_prescription_head.sl,limitby=(0,1))
            if headRow:
                sl=headRow[0].sl+1
            
            #----------------
            db.sm_prescription_head.insert(cid=cid, sl=sl, submit_date=submit_date, first_date=firstDate, submit_by_id=rep_id, submit_by_name=rep_name, user_type=user_type, doctor_id=doctor_id ,doctor_name=doctor_name, image_name=image_name, image_path=image_path, lat_long=lat_long, area_id = areaId,area_name = area_name, tl_id= tl_id, tl_name= tl_name,reg_id= reg_id,reg_name=reg_name)
            
            
            
            campaign_doc_strList=campaign_doc_str.split('<rd>')
            campaignArrayList = []
            for i in range(len(campaign_doc_strList)):  
                item_id = campaign_doc_strList[i]
                campaignArrayList.append({'cid':cid, 'sl':sl, 'medicine_id':item_id})
            if len(campaignArrayList) > 0:
                    db.sm_prescription_details.bulk_insert(campaignArrayList)    
                    dateRecords="update sm_item_prescription,sm_prescription_details set  sm_prescription_details.medicine_name=sm_item_prescription.name, sm_prescription_details.med_type=sm_item_prescription.item_identity WHERE sm_prescription_details.cid = '"+ cid +"' AND  sm_prescription_details.cid = '"+ cid + "' AND sm_prescription_details.medicine_id=sm_item_prescription.item_id AND sm_prescription_details.medicine_name='' AND sm_prescription_details.med_type='' ;"
                    records=db.executesql(dateRecords) 
            
            
            if len(campaign_doc_str)== 0:
                updateOthersS="update sm_prescription_head set  field1=1 WHERE cid = '"+ cid + "' AND sl='"+ str(sl) + "' ;"
                updateOthers=db.executesql(updateOthersS)        
            #----------------
            #----------------
#             return medicine_1
            if medicine_1!='':
                db.sm_prescription_details.insert(cid=cid, sl=sl, medicine_name=medicine_1, med_type='OTHER')
            if medicine_2!='':
                db.sm_prescription_details.insert(cid=cid, sl=sl, medicine_name=medicine_2, med_type='OTHER')
            if medicine_3!='':
                db.sm_prescription_details.insert(cid=cid, sl=sl, medicine_name=medicine_3, med_type='OTHER')
            if medicine_4!='':
                db.sm_prescription_details.insert(cid=cid, sl=sl, medicine_name=medicine_4, med_type='OTHER')
            if medicine_5!='':
                db.sm_prescription_details.insert(cid=cid, sl=sl, medicine_name=medicine_5, med_type='OTHER')
            
            
            return 'SUCCESS<SYNCDATA>'

# Prescription report======================
def report_summary_prescription():
    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.rep_pass).strip()
    synccode = str(request.vars.synccode).strip()
    
    rep_id_report = str(request.vars.rep_id_report).strip().upper()
    se_item_report = str(request.vars.se_item_report).strip().upper()
    se_market_report = str(request.vars.se_market_report).strip().upper()
    user_type = str(request.vars.user_type).strip().upper()
    
    date_from = str(request.vars.date_from).strip().upper()
    date_to = str(request.vars.date_to).strip().upper()
    
    
#    return date_to
    if (date_from==''):
        date_from=current_date
    if (date_to==''):
        date_from_check = datetime.datetime.strptime(date_from, "%Y-%m-%d")
        date_to=date_from_check + datetime.timedelta(days = 1)
    elif (date_from==date_from):
        now = datetime.datetime.strptime(date_from, "%Y-%m-%d")
        date_to=now + datetime.timedelta(days = 1)
    else:
        date_to_check = datetime.datetime.strptime(date_to, "%Y-%m-%d")
        date_to=date_to_check + datetime.timedelta(days = 1)
        
    
#    if (date_from==date_from):
#        now = datetime.datetime.strptime(date_from, "%Y-%m-%d")
#        date_to=now + datetime.timedelta(days = 1)
    
#    return date_to
    repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.sync_code_servey == synccode) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.id,db.sm_rep.user_type,db.sm_rep.level_id,db.sm_rep.field2, limitby=(0, 1))

#     return db._lastsql
   
    level_rep=''
    
    if not repRow:
       retStatus = 'FAILED<SYNCDATA>Invalid Authorization'
       return retStatus
    else:
       pass
   
   
        


    report_string=""
    
        
#  visit Count  
    if (user_type=='SURVEY'):
        qset_vc=db()
        qset_vc=qset_vc((db.sm_prescription_head.cid == cid) & (db.sm_prescription_head.submit_by_id == rep_id) )  
        qset_vc=qset_vc((db.sm_prescription_head.created_on >= date_from) & (db.sm_prescription_head.created_on  < date_to))
        
        if (se_market_report!="ALL"):   
            qset_vc=qset_vc((db.sm_prescription_head.area_id == se_market_report))
        
           
        records_vc=qset_vc.select(db.sm_prescription_head.id.count())
#         return db._lastsql
        visit_count=''
        if records_vc:
            visit_count=records_vc[0][db.sm_prescription_head.id.count()]
        
        report_string=str(visit_count)+'<rd>'+'<rd>'
            
    
    
    return 'SUCCESS<SYNCDATA>'+report_string
def report_detail_prescription():
    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.rep_pass).strip()
    synccode = str(request.vars.synccode).strip()
    
    rep_id_report = str(request.vars.rep_id_report).strip().upper()
    se_item_report = str(request.vars.se_item_report).strip().upper()
    se_market_report = str(request.vars.se_market_report).strip().upper()
    
    user_type = str(request.vars.user_type).strip().upper()
    
#    return user_type
    date_from = str(request.vars.date_from).strip().upper()
    date_to = str(request.vars.date_to).strip().upper()
    
#     date_to=""
    
    if (date_from==''):
        date_from=current_date
    if (date_to==''):
        date_from_check = datetime.datetime.strptime(date_from, "%Y-%m-%d")
        date_to=date_from_check + datetime.timedelta(days = 1)
    elif (date_from==date_from):
        now = datetime.datetime.strptime(date_from, "%Y-%m-%d")
        date_to=now + datetime.timedelta(days = 1)
    else:
        date_to_check = datetime.datetime.strptime(date_to, "%Y-%m-%d")
        date_to=date_to_check + datetime.timedelta(days = 1)
        
#    return date_to
    
    repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.sync_code_servey == synccode) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.id,db.sm_rep.level_id,db.sm_rep.field2, limitby=(0, 1))

#   return db._lastsql
    if not repRow:
       retStatus = 'FAILED<SYNCDATA>Invalid Authorization'
       return retStatus
    else:
       pass
    
    report_string=""
    
        
#  visit Count  
    if (user_type=='SURVEY'):
        qset_vc=db()
        qset_vc=qset_vc((db.sm_prescription_head.cid == cid) & (db.sm_prescription_head.submit_by_id == rep_id) )  
        qset_vc=qset_vc((db.sm_prescription_head.created_on >= date_from) & (db.sm_prescription_head.created_on  < date_to))
        
        if (se_market_report!="ALL"):   
            qset_vc=qset_vc((db.sm_prescription_head.area_id == se_market_report))
        
           
        records_vc=qset_vc.select(db.sm_prescription_head.id.count())
        visit_count=''
        if records_vc:
            visit_count=records_vc[0][db.sm_prescription_head.id.count()]
    
    

        report_string=str(visit_count)#+ '<rd>' + '<rd>' 
    
    #    Detail===========
        qset_detail=db()
        qset_detail=qset_detail((db.sm_prescription_head.cid == cid) & (db.sm_prescription_head.submit_by_id == rep_id))  
        qset_detail=qset_detail((db.sm_prescription_head.created_on >= date_from) & (db.sm_prescription_head.created_on  < date_to))
        
        if (se_market_report!="ALL"):   
            qset_detail=qset_detail((db.sm_prescription_head.area_id == se_market_report))
            
        records_detail=qset_detail.select(db.sm_prescription_head.ALL, orderby=~db.sm_prescription_head.id, limitby=(0,10))
        
    #    return records_detail
    #    return db._lastsql
        
        start_flag=0
        visit_string=''
        for records_detail in records_detail:
            v_id = records_detail.sl 
            doc_id = records_detail.doctor_id 
            doc_name  =  records_detail.doctor_name 
            visit_dtime = records_detail.created_on

           
            visit_string=visit_string+'</br>'+'VisitSL: '+str(v_id)+'</br>'+str(doc_name)+"-"+str(doc_id)+'</br>'+"VisitTime: "+str(visit_dtime)
            detail_info = db((db.sm_prescription_details.cid == cid) & (db.sm_prescription_details.sl == v_id) ).select(db.sm_prescription_details.ALL)
#             return detail_info
            
            for detail_info in detail_info:
                v_id = detail_info.sl 
                medicine_id=detail_info.medicine_id
                medicine_name=detail_info.medicine_name
                med_type=detail_info.med_type
                        
                visit_string=visit_string+'</br>'+medicine_name+'-'+medicine_id+"----"+med_type     
                    
                    
                    
          
        report_string=str(report_string)+'<rd>'+str(visit_string)
        
        

    
    return 'SUCCESS<SYNCDATA>'+report_string 

#==================Report End================
#============================= Image Upload
def fileUploaderPrescription():
    import shutil
    filename = request.vars.upload.filename
    file = request.vars.upload.file
#    shutil.copyfileobj(file,open('C:/workspace/Dropbox/sabbir_acer/web2py/applications/welcome/uploads/'+filename,'wb'))
#     shutil.copyfileobj(file, open('/home/www-data/web2py/applications/mrepacme/static/prescription_pic/' + filename, 'wb'))
    shutil.copyfileobj(file, open('/home/www-data/web2py/applications/gpl/static/prescription_pic/' + filename, 'wb'))
    return 'success'


#not used
#def fileUploaderProfile():
#    import shutil
#    filename = request.vars.upload.filename
#    file = request.vars.upload.file
#    #    Remove file start============
#    import os
#    myfile = "/home/www-data/web2py/applications/lscrmap/static/client_pic/" + filename
#    # # if file exists, delete it ##
#    if os.path.isfile(myfile):
#        os.remove(myfile)        
##    Remove file end============
##    shutil.copyfileobj(file,open('C:/workspace/Dropbox/sabbir_acer/web2py/applications/welcome/uploads/'+filename,'wb'))
#    shutil.copyfileobj(file, open('/home/www-data/web2py/applications/mrepacme/static/client_pic/' + filename, 'wb'))
#    return 'success'
#
#
##== Test dynamic path
#def dmpath():
#    import urllib2
#    cid = str(request.vars.CID).strip().upper()
#    url = 'http://im-gp.com/dmpath/index.php?CID=' + cid + '&HTTPPASS=e99business321cba'
#
#    result = ''
#    try:
#        result = urllib2.urlopen(url)
#    except:
#        result = 'Invalid Request'
#    return result


#============== dynamic path
# <start>sync<fd>imageShow<fd>imageSubmit<end>

def dm_prescription_path():
    return '<start>http://a002.businesssolutionapps.com/gpl/syncmobile_prescription/<fd>http://a002.businesssolutionapps.com/gpl/static/<fd>http://a002.businesssolutionapps.com/gpl/syncmobile_prescription/<end>'

#     return '<start>http://127.0.0.1:8000/skf/syncmobile_prescription/<fd>http://127.0.0.1:8000/mrepacme/static/<fd>http://127.0.0.1:8000/mrepacme/syncmobile_prescription/<end>'
#     return '<start>http://a002.businesssolutionapps.com/skf/syncmobile_prescription/<fd>http://127.0.0.1:8000/mrepacme/static/<fd>http://127.0.0.1:8000/mrepacme/syncmobile_prescription/<end>'
    









