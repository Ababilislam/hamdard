from random import randint
import urllib2
import calendar
import urllib
import time


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



def prescription_submit():
    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = urllib.unquote(str(request.vars.rep_pass).strip().decode('utf8'))
    synccode = str(request.vars.synccode).strip()
    op_pro_str = str(request.vars.opProdID_Str).strip()
    areaId = str(request.vars.areaId).strip()
    ff_present = request.vars.ff_present
    associated_call = request.vars.associated_call
    associated_call_others = request.vars.associated_call_others
    rx_type = request.vars.rx_type
        
    doctor_id = str(request.vars.doctor_id).strip()
    doctor_name =urllib.unquote(str(request.vars.doctor_name).strip().upper().decode('utf8'))
    doctor_category = str(request.vars.category).strip()
    
    
#    medicine_1 = urllib.unquote(str(request.vars.medicine_1).strip().decode('utf8'))
#    medicine_2 = urllib.unquote(str(request.vars.medicine_2).strip().decode('utf8'))
#    medicine_3 = urllib.unquote(str(request.vars.medicine_3).strip().decode('utf8'))
#    medicine_4 = urllib.unquote(str(request.vars.medicine_4).strip().decode('utf8'))
    
    
    latitude = request.vars.latitude
    longitude = request.vars.longitude
    image_name = request.vars.pres_photo
    cap_time=request.vars.cap_time
    image_path=''
    
    try:
        cap_time=cap_time
    except:
        cap_time=''
    
    if ff_present == '' or ff_present == None:
        ff_present = 0
    
    if associated_call == '' or associated_call == None:
        associated_call = 0
    
    if associated_call_others == '' or associated_call_others == None:
        associated_call_others = 0

    if rx_type == None:
        rx_type = ''
    
       
    
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
        tl_id= areaRow[0].level2
        tl_name= areaRow[0].level2_name
        reg_id= areaRow[0].level1
        reg_name= areaRow[0].level1_name
        zone_id = areaRow[0].level0
        zone_name = areaRow[0].level0_name
            
            
    compRow = db((db.sm_company_settings.cid == cid) & (db.sm_company_settings.status == 'ACTIVE')).select(db.sm_company_settings.cid, limitby=(0, 1))
    if not compRow:
        return 'FAILED<SYNCDATA>Invalid Company'
    else:
        repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.sync_code_seen_rx == synccode) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.rep_id, db.sm_rep.name, db.sm_rep.mobile_no, db.sm_rep.user_type, db.sm_rep.level_id, limitby=(0, 1))

        if not repRow:
           return 'FAILED<SYNCDATA>Invalid Authorization'
        else:
            rep_name = repRow[0].name
            mobile_no = repRow[0].mobile_no
            user_type = repRow[0].user_type


            #-------------------
            # sl=1
            # headRow=db(db.sm_prescription_seen_head.cid == cid).select(db.sm_prescription_seen_head.sl,orderby=~db.sm_prescription_seen_head.sl,limitby=(0,1))
            # if headRow:
            #     sl=headRow[0].sl+1

            sl=get_sl()

            #----------------
            prHeadInsert=db.sm_prescription_seen_head.insert(cid=cid, sl=sl, submit_date=submit_date, first_date=firstDate, submit_by_id=rep_id, submit_by_name=rep_name, user_type=user_type, doctor_id=doctor_id ,doctor_name=doctor_name,doctor_category=doctor_category, image_name=image_name, image_path=image_path,cap_time=cap_time,lat_long=lat_long,area_id = areaId,area_name = area_name, tl_id= tl_id, tl_name= tl_name,reg_id= reg_id,reg_name=reg_name,zone_id=zone_id,zone_name=zone_name,ff_present=ff_present,associated_call=associated_call,associated_call_others=associated_call_others,rx_type=rx_type)

            if prHeadInsert:
                if op_pro_str!='':           
                    op_pro_strList=op_pro_str.split('||')            
                    opArrayList = []
                    for i in range(len(op_pro_strList)):  
                        op_item_id = op_pro_strList[i].split('|')
                        
                        if op_item_id[0]==0:
                            med_type='OTHERS'
                        else:
                            med_type='OPPERTUNETY'
                        
                        opArrayList.append({'cid':cid, 'sl':sl,'submit_date':str(submit_date),'first_date':str(firstDate),'submit_by_id':rep_id,'submit_by_name':rep_name,'user_type':user_type,'doctor_id':doctor_id ,'doctor_name':doctor_name,'doctor_category':doctor_category,'area_id': areaId, 'medicine_id':str(op_item_id[0]),'medicine_name':str(op_item_id[1]).strip()})
                    
                    if len(opArrayList) > 0:
                            db.sm_prescription_seen_details.bulk_insert(opArrayList)
    
#                if medicine_1!='':
#                    db.sm_prescription_details.insert(cid=cid, sl=sl,submit_by_id=rep_id,medicine_id=0, medicine_name=medicine_1, med_type='OTHER')
#                if medicine_2!='':
#                    db.sm_prescription_details.insert(cid=cid, sl=sl,submit_by_id=rep_id,medicine_id=0, medicine_name=medicine_2, med_type='OTHER')
#                if medicine_3!='':
#                    db.sm_prescription_details.insert(cid=cid, sl=sl,submit_by_id=rep_id,medicine_id=0, medicine_name=medicine_3, med_type='OTHER')
#                if medicine_4!='':
#                    db.sm_prescription_details.insert(cid=cid, sl=sl,submit_by_id=rep_id,medicine_id=0, medicine_name=medicine_4, med_type='OTHER')
            
            
            
            return 'SUCCESS<SYNCDATA>'





#=============New Check User==============================

def check_user_pharma():
    randNumber = randint(1001, 9999)
    retStatus = ''
    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.rep_pass).strip()
    synccode = str(request.vars.synccode).strip()
    vNo = request.vars.vNo

    try:
        vNo=int(vNo)
    except:
        vNo=0

    compRow = db((db.sm_company_settings.cid == cid) & (db.sm_company_settings.status == 'ACTIVE')).select(db.sm_company_settings.cid, limitby=(0, 1))
    if not compRow:
        return 'FAILED<SYNCDATA>Invalid Company'
    else:               
        repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.id, db.sm_rep.name,db.sm_rep.sync_code_seen_rx, db.sm_rep.sync_count_seen_rx, db.sm_rep.first_sync_date_seen_rx, db.sm_rep.last_sync_date_seen_rx, db.sm_rep.user_type, db.sm_rep.depot_id, db.sm_rep.level_id, db.sm_rep.field2, limitby=(0, 1))

        if not repRow:
           retStatus = 'FAILED<SYNCDATA>Invalid Authorization 2'
           return retStatus
        else:

            rep_name = repRow[0].name
            depot_id = repRow[0].depot_id
            lastSyncTIme=str(repRow[0].last_sync_date_seen_rx)
            #sync_code = repRow[0].sync_code
            #sync_count = repRow[0].sync_count_seen_rx
            sync_count=vNo

            # vRows = db((db.sm_mobile_settings.cid == cid) & (db.sm_mobile_settings.s_key == 'SEEN_RX_V_NO') & (
            #             db.sm_mobile_settings.s_value == vNo)).select(db.sm_mobile_settings.id, limitby=(0, 1))
            #
            # if not vRows:
            #     retStatus = 'FAILED<SYNCDATA>Please update your application.'
            #     return retStatus




            sync_code = str(randNumber)
            #sync_count = int(repRow[0].sync_count_seen_rx) + 1
            first_sync_date = repRow[0].first_sync_date_seen_rx
            user_type = repRow[0].user_type

            level_id = repRow[0].level_id
            depth = repRow[0].field2
            level = 'level' + str(depth)
            
            last_sync_date = str(repRow[0].last_sync_date_seen_rx)

#             return last_sync_dateTime

            if len(str(lastSyncTIme))< 10 :
                last_sync_date = date_fixed
            if first_sync_date == None:
                first_sync_date = date_fixed

            else:
                datetimeFormat = '%Y-%m-%d %H:%M:%S'
                timedelta = datetime.datetime.strptime(datetime_fixed, datetimeFormat) - datetime.datetime.strptime(last_sync_date,datetimeFormat)

                if (str(timedelta).find('day')!=-1):
                    pass
                else:
                    try:
                        timeDiff=str(timedelta).split(':')[0]
                        timeDiffMinute=str(timedelta).split(':')[1]
                        if int(timeDiff) > 0:
                            pass
                        elif ((int(timeDiff) == 0) & (int(timeDiffMinute) > 15)) :
                            pass
                        elif ((int(timeDiff) > 0) & (int(timeDiffMinute) > 15)) :
                            pass
                        else:
                            pass

                    except:
                        pass
            last_sync_date = date_fixed
            if first_sync_date == None:
                first_sync_date = date_fixed


            rep_update = repRow[0].update_record(sync_code_seen_rx=sync_code, first_sync_date_seen_rx=first_sync_date, last_sync_date_seen_rx=last_sync_date, sync_count_seen_rx=sync_count)

            if rep_update:
                area_id_list =[]
                if user_type == 'rep':
                    repAreaRows = db((db.sm_rep_area.cid == cid) & (db.sm_rep_area.rep_id == rep_id)).select(
                        db.sm_rep_area.area_id, db.sm_rep_area.area_name, orderby=db.sm_rep_area.area_id)
                    if not repAreaRows:
                        response.flash = 'Rep Territory Not Available'
                    else:
                        for row in repAreaRows:
                            area_id = row.area_id
                            area_id_list.append(area_id)

                regStr=''
                qset1 = db()
                qset1 = qset1(db.sm_level.cid == cid)
                qset1 = qset1(db.sm_level.depth == 3)
                qset1 = qset1(db.sm_level.level1 !='')
                if user_type == 'rep':
                    qset1 = qset1(db.sm_level.level_id.belongs(area_id_list))

                regRows=qset1.select(db.sm_level.level1,db.sm_level.level1_name,groupby=db.sm_level.level1,orderby=db.sm_level.level1_name)

                for regRow in regRows:
                    level_id=regRow.level1
                    level_name=regRow.level1_name

                    if regStr=='':
                        regStr=str(level_id)+'<fd>'+str(level_name)
                    else:
                        regStr+='<rd>'+str(level_id)+'<fd>'+str(level_name)

                time.sleep(1)

                areaStr=''
                qset2 = db()
                qset2 = qset2(db.sm_level.cid == cid)
                qset2 = qset2(db.sm_level.depth == 3)
                qset2 = qset2(db.sm_level.level2 != '')
                if user_type == 'rep':
                    qset2 = qset2(db.sm_level.level_id.belongs(area_id_list))

                areaRows=qset2.select(db.sm_level.level2,db.sm_level.level2_name,db.sm_level.level1,groupby=db.sm_level.level2,orderby=db.sm_level.level_name)

                for areaRow in areaRows:
                    level1=areaRow.level1
                    level_id=areaRow.level2
                    level_name=areaRow.level2_name

                    if areaStr=='':
                        areaStr=str(level1)+'<fd>'+str(level_id)+'<fd>'+str(level_name)
                    else:
                        areaStr+='<rd>'+str(level1)+'<fd>'+str(level_id)+'<fd>'+str(level_name)

                time.sleep(1)
                trStr=''
                qset3=db()
                qset3=qset3(db.sm_level.cid == cid)
                qset3 = qset3(db.sm_level.depth == 3)
                if user_type == 'rep':
                    qset3 = qset3(db.sm_level.level_id.belongs(area_id_list))

                trRows=qset3.select(db.sm_level.level_id,db.sm_level.level_name,db.sm_level.level1,db.sm_level.level2,orderby=db.sm_level.level_name)

                for trRow in trRows:
                    level1=trRow.level1
                    level2=trRow.level2
                    level_id=trRow.level_id
                    level_name=trRow.level_name

                    if trStr=='':
                        trStr=str(level1)+'<fd>'+str(level2)+'<fd>'+str(level_id)+'<fd>'+str(level_name)
                    else:
                        trStr+='<rd>'+str(level1)+'<fd>'+str(level2)+'<fd>'+str(level_id)+'<fd>'+str(level_name)


                docCategoryStr=''
                rxdocCatRows=db((db.sm_mobile_settings.cid==cid) & (db.sm_mobile_settings.s_key == 'RX_DOC_CAT')).select(db.sm_mobile_settings.s_value,limitby=(0,1))
                if rxdocCatRows:
                    docCategoryStr=rxdocCatRows[0].s_value

                rxGpsStr=''
                rxGpsRows=db((db.sm_mobile_settings.cid==cid) & (db.sm_mobile_settings.s_key == 'RX_GPS')).select(db.sm_mobile_settings.s_value,limitby=(0,1))
                if rxGpsRows:
                    rxGpsStr=rxGpsRows[0].s_value

                time.sleep(1)
    #                 medRows=db().select(db.medicine_list.id,db.medicine_list.name,db.medicine_list.brand, orderby=db.medicine_list.brand,limitby=(0,10))
    #                 medStr=''
    #                 for mRow in medRows:
    #                     id =   str(mRow.id)
    #                     name =   str(mRow.name)
    #                     brandName =  str(mRow.brand)
    # #                    genericName = str(mRow.generic)
    # #                    strength = str(mRow.strength)
    # #                    formation = str(mRow.formation)
    # #                    company = str(mRow.company)
    #
    #                     if medStr == '':
    #                         medStr = id+' | '+name+' | '+brandName
    #                     else:
    #                         medStr += '||' +id+' | '+name+' | '+brandName

                medStr = ''
                brandRows = db().select(db.seen_rx_brand.id, db.seen_rx_brand.brand_name,orderby=db.seen_rx_brand.brand_name)
                #brandRows = db((db.sm_item.cid==cid)&(db.sm_item.manufacturer!='-')).select(db.sm_item.manufacturer,orderby=db.sm_item.manufacturer,distinct=True)
                brandStr = ''
                for bRow in brandRows:
                    id = check_special_char_id(bRow.brand_name) #bRow.manufacturer
                    brand_name = str(bRow.brand_name)

                    if brandStr == '':
                        brandStr = id + ' | ' + brand_name
                    else:
                        brandStr += '||' + id + ' | ' + brand_name

                medStr = brandStr

                rxTypeRows = db().select(db.seen_rx_type.id, db.seen_rx_type.name,
                                        orderby=db.seen_rx_type.name, limitby=(0, 100))
                rxTypeStr = ''
                for rRow in rxTypeRows:
                    id = str(rRow.id)
                    typeName = str(rRow.name)

                    if rxTypeStr == '':
                        rxTypeStr = id + ' | ' + typeName
                    else:
                        rxTypeStr += '||' + id + ' | ' + typeName


                return 'SUCCESS<SYNCDATA>' + str(sync_code)+'<SYNCDATA>'+regStr+'<SYNCDATA>'+areaStr+'<SYNCDATA>'+trStr+'<SYNCDATA>'+docCategoryStr+'<SYNCDATA>'+rxGpsStr+'<SYNCDATA>'+medStr+'<SYNCDATA>'+rxTypeStr

           
# #            settingsRows = db((db.sm_settings_pharma.cid == cid) &(db.sm_settings_pharma.s_key.belongs(s_key_list)) ).select(db.sm_settings_pharma.s_key,db.sm_settings_pharma.s_value)
#
#
#             else:
#                 return 'FAILED<SYNCDATA>Invalid Authorization'





#============================= Test dynamic path
def dmpath():
#    return '<start>http://a007.yeapps.com/acme/syncmobile_417_new/<fd>http://a007.yeapps.com/acme/static/<fd>http://a007.yeapps.com/acme/syncmobile_417_new/<fd>http://a007.yeapps.com/acme/syncmobile_417_new/<end>'
     return '<start>http://127.0.0.1:8000/hamdard/syncmobile_rx_seen_200101/<fd>http://127.0.0.1:8000/hamdard/<fd>http://127.0.0.1:8000/hamdard/<fd>http://127.0.0.1:8000/hamdard/<end>'


############ report

def summary_daily():
    cid=str(request.vars.cid)
    rep_id=str(request.vars.rep_id)
    from_date=str(request.vars.from_date)
    
    if from_date=='':
        from_date=current_date
    
    rptPrStr=''        
    rptPrRows=db((db.sm_prescription_seen_head.cid==cid)&(db.sm_prescription_seen_head.submit_by_id==rep_id)&(db.sm_prescription_seen_head.submit_date==from_date)).select(db.sm_prescription_seen_head.area_id,db.sm_prescription_seen_head.area_name,db.sm_prescription_seen_head.doctor_id,db.sm_prescription_seen_head.doctor_name,db.sm_prescription_seen_head.id.count(),groupby=db.sm_prescription_seen_head.area_id|db.sm_prescription_seen_head.doctor_id,orderby=db.sm_prescription_seen_head.area_name|db.sm_prescription_seen_head.doctor_name)
    
    for row in rptPrRows:
        area_name =   str(row[db.sm_prescription_seen_head.area_name])
        doctor_name =   str(row[db.sm_prescription_seen_head.doctor_name]).capitalize()
        doctor_count =   str(row[db.sm_prescription_seen_head.id.count()])
        
        if rptPrStr == '':
            rptPrStr = area_name+' | '+doctor_name+' | '+doctor_count
        else:
            rptPrStr += '||' +area_name+' | '+doctor_name+' | '+doctor_count
    
    return rptPrStr

############ notice

def notice_list():
    cid=str(request.vars.cid)
    rep_id=str(request.vars.rep_id)

    noticeStr=''
    noticeRows=db(db.sm_notice.cid==cid).select(db.sm_notice.notice,db.sm_notice.notice_date,orderby=~db.sm_notice.notice_date,limitby=(0,5))

    for row in noticeRows:
        notice_date =   str(row.notice_date.strftime('%d-%m-%Y'))
        notice =   str(row.notice)

        if noticeStr == '':
            noticeStr = notice_date+' | '+notice
        else:
            noticeStr += '||' +notice_date+' | '+notice

    return noticeStr


def get_sl():
    import time
    sl = str(time.time())
    sl=sl.replace('.','')
    return sl


def check_version():
    cid=request.vars.cid
    vNo=request.vars.vNo

    retStr=''
    vRows = db((db.sm_mobile_settings.cid == cid)&(db.sm_mobile_settings.s_key == 'SEEN_RX_V_NO')&(db.sm_mobile_settings.s_value ==vNo)).select(db.sm_mobile_settings.id,limitby=(0,1))

    if not vRows:
        retStr= 'Please update your application.'

    return retStr