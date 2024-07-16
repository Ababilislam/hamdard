from random import randint
import urllib2
import calendar

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


# http://127.0.0.1:8000/mrepnovelta/syncmobile_ofline_ppm_report/check_user?cid=NOVELTA&rep_id=1001&rep_pass=123&synccode=2150
def check_user():
    randNumber = randint(1001, 9999)

    retStatus = ''

    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.rep_pass).strip()
    synccode = str(request.vars.synccode).strip()

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

            rep_update = repRow[0].update_record(sync_code=sync_code, first_sync_date=first_sync_date, last_sync_date=last_sync_date, sync_count=sync_count)

            
            # set type(Rep)
#            return user_type
            if (user_type == 'rep'):

                #------ market list
                marketStr = ''

                marketRows = db((db.sm_rep_area.cid == cid) & (db.sm_rep_area.rep_id == rep_id)).select(db.sm_rep_area.area_id, db.sm_rep_area.area_name, orderby=db.sm_rep_area.area_name, groupby=db.sm_rep_area.area_id)
                for marketRow in marketRows:
                    area_id = marketRow.area_id
                    area_name = marketRow.area_name

                    if marketStr == '':
                        marketStr = str(area_id) + '<fd>' + str(area_name)
                    else:
                        marketStr += '<rd>' + str(area_id) + '<fd>' + str(area_name)

                #-------------- Product list
                productStr = ''
                productRows = db(db.sm_item.cid == cid).select(db.sm_item.item_id, db.sm_item.name, db.sm_item.price, orderby=db.sm_item.name)
                for productRow in productRows:
                    item_id = productRow.item_id
                    name = productRow.name
                    price = productRow.price

                    if productStr == '':
                        productStr = str(item_id).upper() + '<fd>' + str(name).upper() + '<fd>' + str(price)
                    else:
                        productStr += '<rd>' + str(item_id).upper() + '<fd>' + str(name).upper() + '<fd>' + str(price)

                #-------------- Merchandizing list
                merchandizingStr = ''
                mproductRows = db(db.sm_merchandizing_item.cid == cid).select(db.sm_merchandizing_item.item_id, db.sm_merchandizing_item.name, orderby=db.sm_merchandizing_item.name)
                for mproductRow in mproductRows:
                    item_id = mproductRow.item_id
                    name = mproductRow.name

                    if merchandizingStr == '':
                        merchandizingStr = str(item_id) + '<fd>' + str(name)
                    else:
                        merchandizingStr += '<rd>' + str(item_id) + '<fd>' + str(name)

                #-------------- Dealer list
                depotName = ''
                dealertRows = db((db.sm_depot.cid == cid) & (db.sm_depot.depot_id == depot_id)).select(db.sm_depot.name, limitby=(0, 1))
#                return db._lastsql
                if dealertRows:
                    depotName = dealertRows[0].name
                dealerStr = str(depot_id) + '<fd>' + str(depotName)

                #------------ Brand List
                brandStr = ''
                brandRows = db((db.sm_category_type.cid == cid) & (db.sm_category_type.type_name == 'BRAND_NAME')).select(db.sm_category_type.cat_type_id, orderby=db.sm_category_type.id)
                for brandRow in brandRows:
                    brandName = brandRow.cat_type_id

                    if brandStr == '':
                        brandStr = str(brandName)
                    else:
                        brandStr += '<rd>' + str(brandName)

                #------------ Complain Type List
                complainTypeStr = ''
                complainTypeRows = db((db.sm_category_type.cid == cid) & (db.sm_category_type.type_name == 'COMPLAIN_TYPE')).select(db.sm_category_type.cat_type_id, orderby=db.sm_category_type.id)
                for complainTypeRow in complainTypeRows:
                    campType_id = complainTypeRow.cat_type_id

                    if complainTypeStr == '':
                        complainTypeStr = str(campType_id)
                    else:
                        complainTypeStr += '<rd>' + str(campType_id)

                #------------ Complain From List
                compFromStr = ''
                compFromRows = db((db.sm_category_type.cid == cid) & (db.sm_category_type.type_name == 'COMPLAIN_FROM')).select(db.sm_category_type.cat_type_id, orderby=db.sm_category_type.id)
                for compFromRow in compFromRows:
                    compFrom_id = compFromRow.cat_type_id

                    if compFromStr == '':
                        compFromStr = str(compFrom_id)
                    else:
                        compFromStr += '<rd>' + str(compFrom_id)

                #------------ TASK_TYPE List
                taskTypeStr = ''
                taskTypeRows = db((db.sm_category_type.cid == cid) & (db.sm_category_type.type_name == 'TASK_TYPE')).select(db.sm_category_type.cat_type_id, orderby=db.sm_category_type.id)
                for taskTypeRow in taskTypeRows:
                    taskType_id = taskTypeRow.cat_type_id

                    if taskTypeStr == '':
                        taskTypeStr = str(taskType_id)
                    else:
                        taskTypeStr += '<rd>' + str(taskType_id)


                #------------ Region List
                regionStr = ''
                levelRows = db((db.sm_level.cid == cid) & (db.sm_level.depot_id == depot_id)).select(db.sm_level.level0, groupby=db.sm_level.level0, limitby=(0, 1))
                for levelRow in levelRows:
                    level0_id = levelRow.level0

                    level0Rows = db((db.sm_level.cid == cid) & (db.sm_level.level_id == level0_id)).select(db.sm_level.level_id, db.sm_level.level_name, limitby=(0, 1))
                    for level0Row in level0Rows:
                        level_id = level0Row.level_id
                        level_name = level0Row.level_name

                        if regionStr == '':
                            regionStr = str(level_id) + '<fd>' + str(level_name)
                        else:
                            regionStr += '<rd>' + str(level_id) + '<fd>' + str(level_name)


                #------------Gift list

                giftStr = ''
                giftRows = db((db.sm_doctor_gift.cid == cid) & (db.sm_doctor_gift.status == 'ACTIVE')).select(db.sm_doctor_gift.gift_id, db.sm_doctor_gift.gift_name, orderby=db.sm_doctor_gift.gift_name)
                for giftRows in giftRows:
                    gift_id = giftRows.gift_id
                    gift_name = giftRows.gift_name

                    if giftStr == '':
                        giftStr = str(gift_id) + '<fd>' + str(gift_name)
                    else:
                        giftStr += '<rd>' + str(gift_id) + '<fd>' + str(gift_name)
                        
                        
                        
                
                #------------ppm list

                ppmStr = ''
                ppmRows = db((db.sm_doctor_ppm.cid == cid) & (db.sm_doctor_ppm.status == 'ACTIVE')).select(db.sm_doctor_ppm.gift_id, db.sm_doctor_ppm.gift_name, orderby=db.sm_doctor_ppm.gift_name)
#                return ppmRows
                for ppmRow in ppmRows:
                    ppm_id = ppmRow.gift_id
                    ppm_name = ppmRow.gift_name
#                    return ppm_id
                    if ppmStr == '':
                        ppmStr = str(ppm_id) + '<fd>' + str(ppm_name)
                    else:
                        ppmStr =ppmStr+ '<rd>' + str(ppm_id) + '<fd>' + str(ppm_name)
#                    return ppmStr
#                return ppmStr
                #------------Client Category list

                clienttCatStr = ''
                clienttCatRows = db((db.sm_category_type.cid == cid) & (db.sm_category_type.type_name == 'CLIENT_CATEGORY')).select(db.sm_category_type.cat_type_id, orderby=db.sm_category_type.cat_type_id)
#                return db._lastsql
                c = 0
                for clienttCatRows in clienttCatRows:
                    cat_type_id = clienttCatRows.cat_type_id


                    if clienttCatStr == '':
                        clienttCatStr = str(cat_type_id).strip().upper()
                    else:
                        clienttCatStr += '<rd>' + str(cat_type_id).strip().upper()
                    c = c + 1
                if (c == 1):
                    clienttCatStr = clienttCatStr + '<rd>'

#                 ---------------------------------------------------------------------------------------
#                 ------------------------------Market Client List Start-----------------------------------------
                clientStr = ''
                start_flag = 0
                
                for marketRow_1 in marketRows:
                    area_id = marketRow_1.area_id


                    clientStr = clientStr + '<' + area_id + '>'
#                     return clientStr
                    clientRows = db((db.sm_client.cid == cid) & (db.sm_client.area_id == area_id) & (db.sm_client.status == 'ACTIVE')).select(db.sm_client.client_id, db.sm_client.name, db.sm_client.category_id, orderby=db.sm_client.name)

        #            return db._lastsql
                    if not clientRows:
                        clientStr = clientStr + 'Retailer not available' + '</' + area_id + '>'
#                         return retStatus
                    else:
                        for clientRow in clientRows:
                            client_id = clientRow.client_id
                            name = clientRow.name
                            category_id = clientRow.category_id

                            if start_flag == 0:
                                clientStr = clientStr + str(client_id) + '<fd>' + str(name) + '<fd>' + str(category_id).strip().upper()
                                start_flag = 1
                            else:
                                clientStr = clientStr + '<rd>' + str(client_id) + '<fd>' + str(name) + '<fd>' + str(category_id).strip().upper()

                    clientStr = clientStr + '</' + area_id + '>'
#                 return clientStr


#                 --------------------------------Market Client List End--------------------------------------
#                 ------------------------------Menu List Start-----------------------------------------
                menuStr = ''
                start_flag = 0
                menuRow = db((db.sm_mobile_settings.cid == cid) & (db.sm_mobile_settings.type == 'REP')).select(db.sm_mobile_settings.sl, db.sm_mobile_settings.s_key, db.sm_mobile_settings.s_value, orderby=db.sm_mobile_settings.sl)
#                return db._lastsql
                for menuRow in menuRow:
                    s_key = menuRow.s_key
                    s_value = menuRow.s_value

                    if start_flag == 0:
                        menuStr = menuStr + str(s_key) + '<fd>' + str(s_value) 
                        start_flag = 1
                    else:
                        menuStr = menuStr + '<rd>' + str(s_key) + '<fd>' + str(s_value) 

                    
#                return menuStr


#                 --------------------------------Menu List End--------------------------------------
                
#                ----------------------------Doctor list start-----------------------
                doctorStr = ''
                doctorRows = db((db.sm_doctor.cid == cid) & (db.sm_doctor.status == 'ACTIVE') & (db.sm_doctor_area.cid == cid) & (db.sm_doctor_area.doc_id == db.sm_doctor.doc_id) ).select(db.sm_doctor.doc_id, db.sm_doctor.doc_name, db.sm_doctor_area.area_id, orderby=db.sm_doctor_area.area_id|db.sm_doctor.doc_name)
#                return db._lastsql
                if not doctorRows:
                    retStatus = 'FAILED<SYNCDATA>Doctor not available'
                    return retStatus
                else:
                   
                    doctor_area_past=''
                    srart_a_flag=0
                    doctorStr_flag=0
                    for doctorRow in doctorRows:
                        doctor_id = doctorRow.sm_doctor.doc_id
                        doctor_name = doctorRow.sm_doctor.doc_name
                        doctor_area = doctorRow.sm_doctor_area.area_id
                        if (doctor_area_past!=doctor_area):
                            
                            if (srart_a_flag==0):
                                doctorStr="<"+doctor_area+">"
                                
                            else:
                                doctorStr=doctorStr+"</"+doctor_area_past+">"+"<"+doctor_area+">"
                                doctorStr_flag=0
                        if doctorStr_flag == 0:
                            doctorStr = doctorStr+str(doctor_id) + '<fd>' + str(doctor_name)
                            doctorStr_flag=1
                        else:
                            doctorStr = doctorStr+'<rd>' + str(doctor_id) + '<fd>' + str(doctor_name)
                        doctor_area_past=doctor_area
                        srart_a_flag=1
                    if (doctorStr!=''):
                        doctorStr=doctorStr+ "</"+doctor_area+">"
#             ----------------------------Doctor list end----------------------------------




#                return doctorStr 

                regionStr=''
#                return user_type
                return 'SUCCESS<SYNCDATA>' + str(sync_code) + '<SYNCDATA>' + marketStr + '<SYNCDATA>' + productStr + '<SYNCDATA>' + merchandizingStr + '<SYNCDATA>' + dealerStr + '<SYNCDATA>' + brandStr + '<SYNCDATA>' + complainTypeStr + '<SYNCDATA>' + compFromStr + '<SYNCDATA>' + taskTypeStr + '<SYNCDATA>' + regionStr + '<SYNCDATA>' + giftStr + '<SYNCDATA>' + clienttCatStr + '<SYNCDATA>' + clientStr + '<SYNCDATA>' + menuStr+ '<SYNCDATA>' +ppmStr + '<SYNCDATA>' + user_type+ '<SYNCDATA>' +str(doctorStr)


            elif (user_type == 'sup'):
#                return level_id
                depotList = []
                marketList=[]
                marketStr = ''
                levelRows = db((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '1') & (db.sm_level[level] == level_id)).select(db.sm_level.level_id, db.sm_level.level_name, db.sm_level.depot_id)
#                return db._lastsql
                for levelRow in levelRows:
                    level_id = levelRow.level_id
                    level_name = levelRow.level_name
                    depotid = str(levelRow.depot_id).strip()

                    if depotid not in depotList:
                        depotList.append(depotid)
                        
                    if level_id not in marketList:   
                        marketList.append(level_id)
                        
                    if marketStr == '':
                        marketStr = str(level_id) + '<fd>' + str(level_name)
                    else:
                        marketStr += '<rd>' + str(level_id) + '<fd>' + str(level_name)
                    
#                    return marketStr

                #-------------- Product list
                productStr = ''
                productRows = db(db.sm_item.cid == cid).select(db.sm_item.item_id, db.sm_item.name, db.sm_item.price, orderby=db.sm_item.name)
                for productRow in productRows:
                    item_id = productRow.item_id
                    name = productRow.name
                    price = productRow.price

                    if productStr == '':
                        productStr = str(item_id) + '<fd>' + str(name) + '<fd>' + str(price)
                    else:
                        productStr += '<rd>' + str(item_id) + '<fd>' + str(name) + '<fd>' + str(price)

                #-------------- Merchandizing list
                merchandizingStr = ''
                mproductRows = db(db.sm_merchandizing_item.cid == cid).select(db.sm_merchandizing_item.item_id, db.sm_merchandizing_item.name, orderby=db.sm_merchandizing_item.name)
                for mproductRow in mproductRows:
                    item_id = mproductRow.item_id
                    name = mproductRow.name

                    if merchandizingStr == '':
                        merchandizingStr = str(item_id) + '<fd>' + str(name)
                    else:
                        merchandizingStr += '<rd>' + str(item_id) + '<fd>' + str(name)


                #-------------- Dealer list
                dealerStr = ''
                dealertRows = db((db.sm_depot.cid == cid) & (db.sm_depot.depot_id.belongs(depotList))).select(db.sm_depot.depot_id, db.sm_depot.name, orderby=db.sm_depot.name)
                for dealertRow in dealertRows:
                    depot_id = dealertRow.depot_id
                    depotName = dealertRow.name

                    if dealerStr == '':
                        dealerStr = str(depot_id) + '<fd>' + str(depotName)
                    else:
                        dealerStr += '<rd>' + str(depot_id) + '<fd>' + str(depotName)


                #------------ Brand List
                brandStr = ''
                brandRows = db((db.sm_category_type.cid == cid) & (db.sm_category_type.type_name == 'BRAND_NAME')).select(db.sm_category_type.cat_type_id, orderby=db.sm_category_type.id)
                for brandRow in brandRows:
                    cat_type_id = brandRow.cat_type_id

                    if brandStr == '':
                        brandStr = str(cat_type_id)
                    else:
                        brandStr += '<rd>' + str(cat_type_id)



                #------------ Complain Type List
                complainTypeStr = ''

                complainTypeRows = db((db.sm_category_type.cid == cid) & (db.sm_category_type.type_name == 'COMPLAIN_TYPE')).select(db.sm_category_type.cat_type_id, orderby=db.sm_category_type.id)
                for complainTypeRow in complainTypeRows:

                    campType_id = complainTypeRow.cat_type_id

                    if complainTypeStr == '':
                        complainTypeStr = str(campType_id)
                    else:
                        complainTypeStr += '<rd>' + str(campType_id)




                #------------ Complain From List
                compFromStr = ''
                compFromRows = db((db.sm_category_type.cid == cid) & (db.sm_category_type.type_name == 'COMPLAIN_FROM')).select(db.sm_category_type.cat_type_id, orderby=db.sm_category_type.id)
                for compFromRow in compFromRows:
                    compFrom_id = compFromRow.cat_type_id

                    if compFromStr == '':
                        compFromStr = str(compFrom_id)
                    else:
                        compFromStr += '<rd>' + str(compFrom_id)


                #------------ TASK_TYPE List
                taskTypeStr = ''
                taskTypeRows = db((db.sm_category_type.cid == cid) & (db.sm_category_type.type_name == 'TASK_TYPE')).select(db.sm_category_type.cat_type_id, orderby=db.sm_category_type.id)
                for taskTypeRow in taskTypeRows:
                    taskType_id = taskTypeRow.cat_type_id

                    if taskTypeStr == '':
                        taskTypeStr = str(taskType_id)
                    else:
                        taskTypeStr += '<rd>' + str(taskType_id)


                #------------ Region List
                regionStr = ''
                levelRows = db((db.sm_level.cid == cid) & (db.sm_level.depth == 0)).select(db.sm_level.level_id, db.sm_level.level_name, orderby=db.sm_level.level_name)
                for levelRow in levelRows:
                    level_id = levelRow.level_id
                    level_name = levelRow.level_name

                    if regionStr == '':
                        regionStr = str(level_id) + '<fd>' + str(level_name)
                    else:
                        regionStr += '<rd>' + str(level_id) + '<fd>' + str(level_name)

               #------------Client Category list

                clienttCatStr = ''
                clienttCatRows = db((db.sm_category_type.cid == cid) & (db.sm_category_type.type_name == 'CLIENT_CATEGORY')).select(db.sm_category_type.cat_type_id, orderby=db.sm_category_type.cat_type_id)
#                return db._lastsql
                c = 0
                for clienttCatRows in clienttCatRows:
                    cat_type_id = clienttCatRows.cat_type_id


                    if clienttCatStr == '':
                        clienttCatStr = str(cat_type_id).strip().upper()
                    else:
                        clienttCatStr += '<rd>' + str(cat_type_id).strip().upper()
                    c = c + 1

                if (c == 1):
                    clienttCatStr = clienttCatStr + '<rd>'

              #------------Gift list

                giftStr = ''
                giftRows = db((db.sm_doctor_gift.cid == cid) & (db.sm_doctor_gift.status == 'ACTIVE')).select(db.sm_doctor_gift.gift_id, db.sm_doctor_gift.gift_name, orderby=db.sm_doctor_gift.gift_name)

                for giftRows in giftRows:
                    gift_id = giftRows.gift_id
                    gift_name = giftRows.gift_name

                    if giftStr == '':
                        giftStr = str(gift_id) + '<fd>' + str(gift_name)
                    else:
                        giftStr += '<rd>' + str(gift_id) + '<fd>' + str(gift_name)
                #------------ppm list

                ppmStr = ''
                ppmRows = db((db.sm_doctor_ppm.cid == cid) & (db.sm_doctor_ppm.status == 'ACTIVE')).select(db.sm_doctor_ppm.gift_id, db.sm_doctor_ppm.gift_name, orderby=db.sm_doctor_ppm.gift_name)
#                return ppmRows
                for ppmRow in ppmRows:
                    ppm_id = ppmRow.gift_id
                    ppm_name = ppmRow.gift_name
#                    return ppm_id
                    if ppmStr == '':
                        ppmStr = str(ppm_id) + '<fd>' + str(ppm_name)
                    else:
                        ppmStr =ppmStr+ '<rd>' + str(ppm_id) + '<fd>' + str(ppm_name)
#                 ---------------------------------------------------------------------------------------



#                marketStr==============
                clientStr = ''
                start_flag = 0
                for i in range(len(marketList)):
                    area_id = marketList[i]


                    clientStr = clientStr + '<' + area_id + '>'
#                     return clientStr
                    clientRows = db((db.sm_client.cid == cid) & (db.sm_client.area_id == marketList[i]) & (db.sm_client.status == 'ACTIVE')).select(db.sm_client.client_id, db.sm_client.name, db.sm_client.category_id, orderby=db.sm_client.name)

        #            return db._lastsql
                    if not clientRows:
                        clientStr = clientStr + 'Retailer not available' + '</' + area_id + '>'
#                         return retStatus
                    else:
                        for clientRow in clientRows:
                            client_id = clientRow.client_id
                            name = clientRow.name
                            category_id = clientRow.category_id

                            if start_flag == 0:
                                clientStr = clientStr + str(client_id) + '<fd>' + str(name) + '<fd>' + str(category_id).strip().upper()
                                start_flag = 1
                            else:
                                clientStr = clientStr + '<rd>' + str(client_id) + '<fd>' + str(name) + '<fd>' + str(category_id).strip().upper()

                    clientStr = clientStr + '</' + area_id + '>'
#                 return clientStr


#                 --------------------------------Market Client List End--------------------------------------


                #                 ------------------------------Menu List Start-----------------------------------------
                menuStr = ''
                start_flag = 0
                menuRow = db((db.sm_mobile_settings.cid == cid) & (db.sm_mobile_settings.type == 'REP')).select(db.sm_mobile_settings.sl, db.sm_mobile_settings.s_key, db.sm_mobile_settings.s_value, orderby=db.sm_mobile_settings.sl)
                for menuRow in menuRow:
                    s_key = menuRow.s_key
                    s_value = menuRow.s_value

                    if start_flag == 0:
                        menuStr = menuStr + str(s_key) + '<fd>' + str(s_value) 
                        start_flag = 1
                    else:
                        menuStr = menuStr + '<rd>' + str(s_key) + '<fd>' + str(s_value) 

                    
#                return menuStr
#                 --------------------------------Menu List End--------------------------------------

#                ----------------------------Doctor list start-----------------------
                doctorStr = ''
                doctorRows = db((db.sm_doctor.cid == cid) & (db.sm_doctor.status == 'ACTIVE') & (db.sm_doctor_area.cid == cid) & (db.sm_doctor_area.doc_id == db.sm_doctor.doc_id) ).select(db.sm_doctor.doc_id, db.sm_doctor.doc_name, db.sm_doctor_area.area_id, orderby=db.sm_doctor_area.area_id|db.sm_doctor.doc_name)
#                return db._lastsql
                if not doctorRows:
                    retStatus = 'FAILED<SYNCDATA>Doctor not available'
                    return retStatus
                else:
                   
                    doctor_area_past=''
                    srart_a_flag=0
                    doctorStr_flag=0
                    for doctorRow in doctorRows:
                        doctor_id = doctorRow.sm_doctor.doc_id
                        doctor_name = doctorRow.sm_doctor.doc_name
                        doctor_area = doctorRow.sm_doctor_area.area_id
                        if (doctor_area_past!=doctor_area):
                            
                            if (srart_a_flag==0):
                                doctorStr="<"+doctor_area+">"
                                
                            else:
                                doctorStr=doctorStr+"</"+doctor_area_past+">"+"<"+doctor_area+">"
                                doctorStr_flag=0
                        if doctorStr_flag == 0:
                            doctorStr = doctorStr+str(doctor_id) + '<fd>' + str(doctor_name)
                            doctorStr_flag=1
                        else:
                            doctorStr = doctorStr+'<rd>' + str(doctor_id) + '<fd>' + str(doctor_name)
                        doctor_area_past=doctor_area
                        srart_a_flag=1
                    if (doctorStr!=''):
                        doctorStr=doctorStr+ "</"+doctor_area+">"
#             ----------------------------Doctor list end----------------------------------
                    

#                return 'SUCCESS<SYNCDATA>' + str(sync_code) + '<SYNCDATA>' + marketStr + '<SYNCDATA>' + productStr + '<SYNCDATA>' + merchandizingStr + '<SYNCDATA>' + dealerStr + '<SYNCDATA>' + brandStr + '<SYNCDATA>' + complainTypeStr + '<SYNCDATA>' + compFromStr + '<SYNCDATA>' + taskTypeStr + '<SYNCDATA>' + regionStr + '<SYNCDATA>' + giftStr + '<SYNCDATA>' + clienttCatStr + '<SYNCDATA>' + menuStr
                return 'SUCCESS<SYNCDATA>' + str(sync_code) + '<SYNCDATA>' + marketStr + '<SYNCDATA>' + productStr + '<SYNCDATA>' + merchandizingStr + '<SYNCDATA>' + dealerStr + '<SYNCDATA>' + brandStr + '<SYNCDATA>' + complainTypeStr + '<SYNCDATA>' + compFromStr + '<SYNCDATA>' + taskTypeStr + '<SYNCDATA>' + regionStr + '<SYNCDATA>' + giftStr + '<SYNCDATA>' + clienttCatStr + '<SYNCDATA>' + clientStr + '<SYNCDATA>' + menuStr+ '<SYNCDATA>' +ppmStr + '<SYNCDATA>' + user_type+ '<SYNCDATA>' +doctorStr
                
            else:
                return 'FAILED<SYNCDATA>Invalid Authorization'


#

# http://127.0.0.1:8000/lscmreporting/syncmobile/getScheduleClientList?cid=LSCRM&rep_id=1001&rep_pass=123&synccode=2568&sch_date=2014-9-14
def getScheduleClientList():
    retStatus = ''

    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.rep_pass).strip()
    synccode = str(request.vars.synccode).strip()

    sch_date = request.vars.sch_date

    try:
        schedule_date = datetime.datetime.strptime(sch_date, '%Y-%m-%d')
    except:
        try:
            schedule_date = datetime.datetime.strptime(sch_date, '%d-%m-%Y')
        except:
            return 'FAILED<SYNCDATA>Invalid Date'

    compRow = db((db.sm_company_settings.cid == cid) & (db.sm_company_settings.status == 'ACTIVE')).select(db.sm_company_settings.cid, limitby=(0, 1))
    if not compRow:
        return 'FAILED<SYNCDATA>Invalid Company'
    else:
        repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.sync_code == synccode) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.user_type, limitby=(0, 1))
        if not repRow:
           retStatus = 'FAILED<SYNCDATA>Invalid Authorization'
           return retStatus
        else:
            user_type = repRow[0].user_type

            #------ market list
            clientStr = ''
            clientRows = db((db.sm_visit_plan.cid == cid) & (db.sm_visit_plan.rep_id == rep_id) & (db.sm_visit_plan.schedule_date == schedule_date) & (db.sm_visit_plan.visited_flag == 0) & (db.sm_visit_plan.status == 'Approved')).select(db.sm_visit_plan.client_id, db.sm_visit_plan.client_name, orderby=db.sm_visit_plan.client_name)
            if not clientRows:
                retStatus = 'FAILED<SYNCDATA>Scheduled not available'
                return retStatus
            else:
                for clientRow in clientRows:
                    client_id = clientRow.client_id
                    client_name = clientRow.client_name

                    if clientStr == '':
                        clientStr = str(client_id) + '<fd>' + str(client_name)
                    else:
                        clientStr += '<rd>' + str(client_id) + '<fd>' + str(client_name)

                return 'SUCCESS<SYNCDATA>' + clientStr

# Unscheduled
# http://127.0.0.1:8000/lscmreporting/syncmobile/?cid=LSCRM&rep_id=1001&rep_pass=123&synccode=7048&market_id=M000003
def getMarketClientList():
    retStatus = ''

    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.rep_pass).strip()
    synccode = str(request.vars.synccode).strip()
    market_id = str(request.vars.market_id).strip()

    client_cat = str(request.vars.client_cat).strip()

#    return client_cat


    compRow = db((db.sm_company_settings.cid == cid) & (db.sm_company_settings.status == 'ACTIVE')).select(db.sm_company_settings.cid, limitby=(0, 1))
    if not compRow:
        return 'FAILED<SYNCDATA>Invalid Company'
    else:
        repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.sync_code == synccode) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.user_type, limitby=(0, 1))
        if not repRow:
           retStatus = 'FAILED<SYNCDATA>Invalid Authorization'
           return retStatus
        else:
            user_type = repRow[0].user_type

            #------ market list
            clientStr = ''
            if (client_cat == 'None'):
                clientRows = db((db.sm_client.cid == cid) & (db.sm_client.area_id == market_id) & (db.sm_client.status == 'ACTIVE')).select(db.sm_client.client_id, db.sm_client.name, db.sm_client.category_id, orderby=db.sm_client.name)
            else:
                clientRows = db((db.sm_client.cid == cid) & (db.sm_client.area_id == market_id) & (db.sm_client.status == 'ACTIVE') & (db.sm_client.category_id == client_cat)).select(db.sm_client.client_id, db.sm_client.name, db.sm_client.category_id, orderby=db.sm_client.name)
#            return db._lastsql
            if not clientRows:
                retStatus = 'FAILED<SYNCDATA>Retailer not available'
                return retStatus
            else:
                for clientRow in clientRows:
                    client_id = clientRow.client_id
                    name = clientRow.name
                    category_id = clientRow.category_id

                    if clientStr == '':
                        clientStr = str(client_id) + '<fd>' + str(name) + '<fd>' + str(category_id)
                    else:
                        clientStr += '<rd>' + str(client_id) + '<fd>' + str(name) + '<fd>' + str(category_id)

                return 'SUCCESS<SYNCDATA>' + clientStr

# delivery
# http://127.0.0.1:8000/lscmreporting/syncmobile/getDistributorClientList?cid=LSCRM&rep_id=1001&rep_pass=123&synccode=7048&dealer_id=812013
def getDistributorClientList():
    retStatus = ''
    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.rep_pass).strip()
    synccode = str(request.vars.synccode).strip()
    dealer_id = str(request.vars.dealer_id).strip()

    compRow = db((db.sm_company_settings.cid == cid) & (db.sm_company_settings.status == 'ACTIVE')).select(db.sm_company_settings.cid, limitby=(0, 1))
    if not compRow:
        return 'FAILED<SYNCDATA>Invalid Company'
    else:
        repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.sync_code == synccode) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.user_type, limitby=(0, 1))
        if not repRow:
           retStatus = 'FAILED<SYNCDATA>Invalid Authorization'
           return retStatus
        else:
            user_type = repRow[0].user_type

            #------ market list
            clientStr = ''

            clientRows = db((db.sm_client.cid == cid) & (db.sm_client.depot_id == dealer_id) & (db.sm_client.status == 'ACTIVE')).select(db.sm_client.client_id, db.sm_client.name, orderby=db.sm_client.name)
            if not clientRows:
                retStatus = 'FAILED<SYNCDATA>Retailer not available'
                return retStatus
            else:
                for clientRow in clientRows:
                    client_id = clientRow.client_id
                    name = clientRow.name

                    if clientStr == '':
                        clientStr = str(client_id) + '<fd>' + str(name)
                    else:
                        clientStr += '<rd>' + str(client_id) + '<fd>' + str(name)

                return 'SUCCESS<SYNCDATA>' + clientStr

# http://127.0.0.1:8000/lscmreporting/syncmobile/getClientInfo?cid=LSCRM&rep_id=101&rep_pass=123&synccode=5771&client_id=1
# getting route,merchandizing,client information
def getClientInfo():
    retStatus = ''

    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.rep_pass).strip()
    synccode = str(request.vars.synccode).strip()
    client_id = str(request.vars.client_id).strip()

    compRow = db((db.sm_company_settings.cid == cid) & (db.sm_company_settings.status == 'ACTIVE')).select(db.sm_company_settings.cid, limitby=(0, 1))
    if not compRow:
        return 'FAILED<SYNCDATA>Invalid Company'
    else:
        repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.sync_code == synccode) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.user_type, limitby=(0, 1))
        if not repRow:
           retStatus = 'FAILED<SYNCDATA>Invalid Authorization'
           return retStatus
        else:
            user_type = repRow[0].user_type

            clientRecords = db((db.sm_client.cid == cid) & (db.sm_client.client_id == client_id) & (db.sm_client.status == 'ACTIVE')).select(db.sm_client.area_id, db.sm_client.depot_id, limitby=(0, 1))
            if not clientRecords:
                return 'FAILED<SYNCDATA>Invalid Client'
            else:
                route_id = str(clientRecords[0].area)
                depot_id = str(clientRecords[0].depot_id)
                route_name = ''

                levelRecords = db((db.sm_level.cid == cid) & (db.sm_level.level_id == route_id)).select(db.sm_level.level_name, limitby=(0, 1))
                if levelRecords:
                    route_name = str(levelRecords[0].level_name)

                market = route_name + '-' + route_id

                # -- Distributor
                depot_name = ''
                depotRecords = db((db.sm_depot.cid == cid) & (db.sm_depot.depot_id == depot_id)).select(db.sm_depot.name, limitby=(0, 1))
                if depotRecords:
                    depot_name = str(depotRecords[0].name)

                distributorNameID = depot_name + '-' + depot_id
                #---


                #-----
                merItemStr = ''
                lastMarchRows = db((db.visit_merchandising.cid == cid) & (db.visit_merchandising.client_id == client_id)).select(db.visit_merchandising.SL, orderby= ~db.visit_merchandising.SL, limitby=(0, 1))
                if lastMarchRows:
                    lastvsl = lastMarchRows[0].SL

                    merItemRows = db((db.visit_merchandising.cid == cid) & (db.visit_merchandising.SL == lastvsl) & (db.visit_merchandising.dismantled != 'YES')).select(db.visit_merchandising.ALL, orderby=db.visit_merchandising.name)
                    for merItemRow in merItemRows:
                        m_item_id = merItemRow.m_item_id
                        name = merItemRow.name
                        qty = merItemRow.qty
                        installation_date = merItemRow.installation_date
                        visible = merItemRow.visible  # Yes,No
                        condition_value = merItemRow.condition_value  # Good,Bad
                        dismantled = merItemRow.dismantled  # YES,NO
                        new_flag = '0'

                        if merItemStr == '':
                            merItemStr = str(m_item_id) + '<fd>' + str(name) + '<fd>' + str(qty) + '<fd>' + str(installation_date) + '<fd>' + str(visible) + '<fd>' + str(condition_value) + '<fd>' + str(dismantled) + '<fd>' + new_flag
                        else:
                            merItemStr += '<rd>' + str(m_item_id) + '<fd>' + str(name) + '<fd>' + str(qty) + '<fd>' + str(installation_date) + '<fd>' + str(visible) + '<fd>' + str(condition_value) + '<fd>' + str(dismantled) + '<fd>' + new_flag

                #--------- Last Market Info
                lastMarketInforStr = ''
                marketLastVSl = ''
                marketInfoLastRows = db((db.visit_market_info.cid == cid) & (db.visit_market_info.client_id == client_id)).select(db.visit_market_info.SL, orderby= ~db.visit_market_info.SL, limitby=(0, 1))
                if marketInfoLastRows:
                    marketLastVSl = int(marketInfoLastRows[0].SL)

                    marketInfoStockRows = db((db.visit_market_info.cid == cid) & (db.visit_market_info.SL == marketLastVSl)).select(db.visit_market_info.ALL, orderby=db.visit_market_info.brand_name)
                    for marketStockRow in marketInfoStockRows:
                        m_brand_name = str(marketStockRow.brand_name)
                        m_sales = str(marketStockRow.monthly_sales)
                        m_stock = str(marketStockRow.stock)
                        m_credit = str(marketStockRow.credit_amt)
                        m_price = str(marketStockRow.price)
                        m_free_bag = str(marketStockRow.free_bag)
                        m_ret_com = str(marketStockRow.retailer_commission)
                        m_trade_pro = str(marketStockRow.trade_promotion)
                        m_remarks = str(marketStockRow.remarks)

                        marketInfoBrandStr = m_brand_name + '<fd>' + m_sales + '<fd>' + m_stock + '<fd>' + m_credit + '<fd>' + m_price + '<fd>' + m_free_bag + '<fd>' + m_ret_com + '<fd>' + m_trade_pro + '<fd>' + m_remarks;

                        if lastMarketInforStr == '':
                            lastMarketInforStr = marketInfoBrandStr
                        else:
                            lastMarketInforStr += '<rd>' + marketInfoBrandStr

                #-------------- Campaign list
                campaignStr = ''
                campaignRows = db((db.trade_promotional_offer.cid == cid) & ((db.trade_promotional_offer.from_date <= current_date) & (db.trade_promotional_offer.to_date >= current_date)) & (db.trade_promotional_offer.status == 'ACTIVE')).select(db.trade_promotional_offer.ALL, orderby=db.trade_promotional_offer.offer_name)
                for campaignRow in campaignRows:
                    offerId = campaignRow.id
                    offerName = campaignRow.offer_name
                    offer_from_date = campaignRow.from_date
                    offer_to_date = campaignRow.to_date

                    offerDes = str(offer_from_date.strftime('%d-%m-%Y')) + ', ' + str(offer_to_date.strftime('%d-%m-%Y'))
                    if campaignStr == '':
                        campaignStr = str(offerId) + '<fd>' + str(offerName) + '<fd>' + offerDes
                    else:
                        campaignStr += '<rd>' + str(offerId) + '<fd>' + str(offerName) + '<fd>' + offerDes

                #--------- Last client campaign
                lastClientCampaignStr = ''
                clientOfferRows = db((db.visit_client_offer.cid == cid) & (db.visit_client_offer.client_id == client_id) & (db.visit_client_offer.last_flag == 1)).select(db.visit_client_offer.offer_id, db.visit_client_offer.offer_name, db.visit_client_offer.offer_from_date, db.visit_client_offer.offer_to_date, orderby=db.visit_client_offer.offer_id)
                for clientOfferRow in clientOfferRows:
                    offer_id = str(clientOfferRow.offer_id)
                    offer_name = str(clientOfferRow.offer_name)
                    offer_fromDate = clientOfferRow.offer_from_date
                    offer_toDate = clientOfferRow.offer_to_date

                    offer_Des = str(offer_fromDate.strftime('%d-%m-%Y')) + ', ' + str(offer_toDate.strftime('%d-%m-%Y'))
                    if lastClientCampaignStr == '':
                        lastClientCampaignStr = str(offer_id) + '<fd>' + str(offer_name) + '<fd>' + offer_Des
                    else:
                        lastClientCampaignStr += '<rd>' + str(offer_id) + '<fd>' + str(offer_name) + '<fd>' + offer_Des

                return 'SUCCESS<SYNCDATA>' + market + '<SYNCDATA>' + merItemStr + '<SYNCDATA>' + lastMarketInforStr + '<SYNCDATA>' + campaignStr + '<SYNCDATA>' + lastClientCampaignStr + '<SYNCDATA>' + distributorNameID

# http://127.0.0.1:8000/lscmreporting/syncmobile/getClientProfile?cid=LSCRM&rep_id=101&rep_pass=123&synccode=5771&client_id=1
# getting route,merchandizing,client information
def getClientProfile():
    retStatus = ''

    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.rep_pass).strip()
    synccode = str(request.vars.synccode).strip()
    client_id = str(request.vars.client_id).strip()

    compRow = db((db.sm_company_settings.cid == cid) & (db.sm_company_settings.status == 'ACTIVE')).select(db.sm_company_settings.cid, limitby=(0, 1))
    if not compRow:
        return 'FAILED<SYNCDATA>Invalid Company'
    else:
        repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.sync_code == synccode) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.user_type, limitby=(0, 1))
        if not repRow:
           retStatus = 'FAILED<SYNCDATA>Invalid Authorization'
           return retStatus
        else:
            user_type = repRow[0].user_type

            clientRecords = db((db.sm_client.cid == cid) & (db.sm_client.client_id == client_id)).select(db.sm_client.ALL, limitby=(0, 1))
            if not clientRecords:
                return 'FAILED<SYNCDATA>Invalid Retailer'
            else:
                route_id = str(clientRecords[0].area_id)
                route_name = ''

                levelRecords = db((db.sm_level.cid == cid) & (db.sm_level.level_id == route_id)).select(db.sm_level.level_name, limitby=(0, 1))
                if levelRecords:
                    route_name = str(levelRecords[0].level_name)

                market = route_name + '-' + route_id

                #---------
                clientId = str(clientRecords[0].client_id)
                client_name = str(clientRecords[0].name)
                client_address = str(clientRecords[0].address)
                client_area_id = str(clientRecords[0].area_id)
                client_contact_no1 = str(clientRecords[0].contact_no1)
                client_contact_no2 = str(clientRecords[0].contact_no2)

                owner_name = str(clientRecords[0].owner_name)
                nid = str(clientRecords[0].nid)
                passport = str(clientRecords[0].passport)
                dob = str(clientRecords[0].dob)
                dom = str(clientRecords[0].dom)
                kids_info = str(clientRecords[0].kids_info)
                hobby = str(clientRecords[0].hobby)
                trade_license = str(clientRecords[0].trade_license)
                trade_license_no = str(clientRecords[0].trade_license_no)
                vat_registration = str(clientRecords[0].vat_registration)
                vat_registration_no = str(clientRecords[0].vat_registration_no)

                manager_name = str(clientRecords[0].manager_name)
                manager_contact_no = str(clientRecords[0].manager_contact_no)
                starting_year = str(clientRecords[0].starting_year)
                category_id = str(clientRecords[0].category_id)
                lsc_covered = str(clientRecords[0].lsc_covered)
                monthly_sales_capacity = str(clientRecords[0].monthly_sales_capacity)
                monthly_sales = str(clientRecords[0].monthly_sales)
                shop_owner_status = str(clientRecords[0].shop_owner_status)
                warehouse_capacity = str(clientRecords[0].warehouse_capacity)
                shop_size = str(clientRecords[0].shop_size)
                shop_front_size = str(clientRecords[0].shop_front_size)
                truck_number = str(clientRecords[0].truck_number)
                barge_number = str(clientRecords[0].barge_number)
                status = str(clientRecords[0].status)
                photo_name = str(clientRecords[0].photo)

                # -- Distributor
                depot_id = str(clientRecords[0].depot_id)
                depot_name = ''
                depotRecords = db((db.sm_depot.cid == cid) & (db.sm_depot.depot_id == depot_id)).select(db.sm_depot.name, limitby=(0, 1))
                if depotRecords:
                    depot_name = str(depotRecords[0].name)

                distributorNameID = depot_name + '-' + depot_id
                #---

                if client_contact_no2 == 'None':
                    client_contact_no2 = ''
                if manager_contact_no == 'None':
                    manager_contact_no = ''
                if dob == 'None':
                    dob = ''
                if dom == 'None':
                    dom = ''

                clientProfileStr = clientId + '<fd>' + client_name + '<fd>' + client_address + '<fd>' + client_area_id + '<fd>' + client_contact_no1 + '<fd>' + client_contact_no2 + '<fd>' + \
                owner_name + '<fd>' + nid + '<fd>' + passport + '<fd>' + dob + '<fd>' + dom + '<fd>' + kids_info + '<fd>' + hobby + '<fd>' + trade_license + '<fd>' + trade_license_no + '<fd>' + vat_registration + '<fd>' + vat_registration_no + \
                '<fd>' + manager_name + '<fd>' + manager_contact_no + '<fd>' + starting_year + '<fd>' + category_id + '<fd>' + lsc_covered + '<fd>' + monthly_sales_capacity + '<fd>' + monthly_sales + '<fd>' + shop_owner_status + '<fd>' + warehouse_capacity + '<fd>' + shop_size + '<fd>' + shop_front_size + '<fd>' + truck_number + '<fd>' + barge_number + '<fd>' + status + '<fd>' + photo_name

                #------------
                clientCatStr = ''
                clientCatRows = db((db.sm_category_type.cid == cid) & (db.sm_category_type.type_name == 'CLIENT_CATEGORY')).select(db.sm_category_type.cat_type_id, orderby=db.sm_category_type.cat_type_id)
                for clientCat in clientCatRows:
                    cat_type_id = clientCat.cat_type_id
                    if clientCatStr == '':
                        clientCatStr = cat_type_id
                    else:
                        clientCatStr += '<fd>' + cat_type_id

                return 'SUCCESS<SYNCDATA>' + market + '<SYNCDATA>' + clientCatStr + '<SYNCDATA>' + clientProfileStr + '<SYNCDATA>' + distributorNameID

# http://127.0.0.1:8000/lscmreporting/syncmobile/visitSubmit?cid=LSCRM&rep_id=101&rep_pass=123&synccode=5771&client_id=1&visit_type=&schedule_date=&market_info=1&order_info=1&merchandizing=1&lat=0&long=0
# http://127.0.0.1:8000/lscmreporting/syncmobile/visitSubmit?cid=LSCRM&rep_id= 1004&rep_pass=6085&synccode=&client_id=R100585&visit_type=Scheduled&market_info= Akiz <fd> 500 <fd> 2000 <fd> 12000 <fd> 320 <fd> 2 <fd> 1.0 <fd> Good <rd>Seven Ring <fd> 200 <fd> 800 <fd> 3000 <fd> 400 <fd> 0  <fd> 5 <fd> So Good &order_info=1800106001 <fd> 5 <rd>1800201001<fd> 100&merchandizing=1 <fd> Calender <fd> 2 <fd> 2014-09-08 <fd> YES <fd> GOOD<fd> NO <fd> 0 <rd>2 <fd> Wall Paint <fd> 1 <fd> 2014-09-01 <fd> NO <fd> BAD <fd> NO<fd> 1 &lat=0&long=0
def visitSubmit():
    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.rep_pass).strip()
    synccode = str(request.vars.synccode).strip()
    client_id = str(request.vars.client_id).strip().upper()
#    return client_id
    market_info = str(request.vars.market_info).strip()
    order_info = str(request.vars.order_info).strip()
    merchandizing = str(request.vars.merchandizing).strip()
    campaign = str(request.vars.campaign).strip()


    visit_type = str(request.vars.visit_type).strip()  # scheduled,unscheduled
    sch_date = str(request.vars.schedule_date).strip()


    payment_mode = str(request.vars.payment_mode).strip()

    schedule_date = ''
    if visit_type == 'Scheduled':
        try:
            schedule_date = datetime.datetime.strptime(sch_date, '%Y-%m-%d')
        except:
            try:
                schedule_date = datetime.datetime.strptime(sch_date, '%d-%m-%Y')
            except:
                return 'FAILED<SYNCDATA>Invalid Date'


    latitude = request.vars.lat
    longitude = request.vars.long
    visit_photo = request.vars.visit_photo

    if latitude == '' or latitude == None:
        latitude = 0
    if longitude == '' or longitude == None:
        longitude = 0

    lat_long = str(latitude) + ',' + str(longitude)


    visit_date = current_date
    visit_datetime = date_fixed
    firstDate = first_currentDate
    depot_name = ''
    client_name = ''
    route_id = ''
    route_name = ''

#    return market_info
#    return merchandizing


    compRow = db((db.sm_company_settings.cid == cid) & (db.sm_company_settings.status == 'ACTIVE')).select(db.sm_company_settings.cid, limitby=(0, 1))
    if not compRow:
        return 'FAILED<SYNCDATA>Invalid Company'
    else:
        repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.sync_code == synccode) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.rep_id, db.sm_rep.name, db.sm_rep.mobile_no, db.sm_rep.user_type, db.sm_rep.level_id, limitby=(0, 1))
        if not repRow:
           return 'FAILED<SYNCDATA>Invalid Authorization'
        else:
            rep_name = repRow[0].name
            mobile_no = repRow[0].mobile_no
            user_type = repRow[0].user_type

            #----
#            clientRecords = db((db.sm_client.cid == cid) & (db.sm_client.client_id == client_id) & (db.sm_client.status == 'ACTIVE')).select(db.sm_client.name, db.sm_client.category_id, db.sm_client.area_id, db.sm_client.depot_id, limitby=(0, 1))
#            return db._lastsql
            clientRecords = db((db.sm_client.cid == cid) & (db.sm_client.client_id == client_id) & (db.sm_client.status == 'ACTIVE')).select(db.sm_client.name, db.sm_client.category_id, db.sm_client.area_id, db.sm_client.depot_id,db.sm_client.latitude,db.sm_client.longitude, limitby=(0, 1))
#            return db._lastsql
            client_lat=''
            client_long=''
            tracking_table_latlong="0,0"
            if not clientRecords:
                return 'FAILED<SYNCDATA>Invalid Retailer'
            else:
                client_name = clientRecords[0].name
                client_cat = clientRecords[0].category_id
                route_id = clientRecords[0].area_id
                depot_id = str(clientRecords[0].depot_id).strip().upper()
                client_lat = str(clientRecords[0].latitude).strip()
                client_long = str(clientRecords[0].longitude).strip()
                
                tracking_table_latlong= str(client_lat)+","+str(client_long)

                regionid = ''
                areaid = ''
                terriroryid = ''
                marketid = ''
                #-----
                levelRecords = db((db.sm_level.cid == cid) & (db.sm_level.level_id == route_id)).select(db.sm_level.level_id, db.sm_level.level_name, db.sm_level.depth, db.sm_level.level0, db.sm_level.level1, db.sm_level.level2, limitby=(0, 1))
                if levelRecords:
                    route_name = levelRecords[0].level_name
                    regionid = levelRecords[0].level0
                    areaid = levelRecords[0].level1
                    terriroryid = levelRecords[0].level2


                #----
                ordSl = 0
                depotRow = db((db.sm_depot.cid == cid) & (db.sm_depot.depot_id == depot_id)).select(db.sm_depot.id, db.sm_depot.name, db.sm_depot.order_sl, limitby=(0, 1))
                if depotRow:
                    depot_name = depotRow[0].name
                    order_sl = int(depotRow[0].order_sl)
                    ordSl = order_sl + 1
                depotRow[0].update_record(order_sl=ordSl)

                #----
                field1 = ''
                if (order_info != ''):
                    field1 = 'ORDER'
                insertRes = db.sm_order_head.insert(cid=cid, depot_id=depot_id, depot_name=depot_name, sl=ordSl, rep_id=rep_id, rep_name=rep_name, mobile_no=mobile_no, user_type=user_type, client_id=client_id, client_name=client_name, client_cat=client_cat, order_date=visit_date, order_datetime=visit_datetime, ym_date=firstDate, area_id=route_id, area_name=route_name, visit_type=visit_type, lat_long=lat_long, status='Submitted', visit_image=visit_photo, payment_mode=payment_mode, field1=field1)
                vsl = db.sm_order_head(insertRes).id
                
                

                
                #                Client lat_long update
#                return client_lat
                if ((client_lat=='') | (client_lat=='0')| (client_long=='')| (client_long=='0')):
                    db((db.sm_client.cid == cid) & (db.sm_client.client_id == client_id)).update(latitude=latitude,longitude=longitude)

#                Insert in tracking table====================
                insertTracking = db.sm_tracking_table.insert(cid=cid, depot_id=depot_id, depot_name=depot_name, sl=ordSl, rep_id=rep_id, rep_name=rep_name,call_type='SELL',  visited_id=client_id, visited_name=client_name, visit_date=visit_date, visit_time=visit_datetime,  area_id=route_id, area_name=route_name, visit_type=visit_type, visited_latlong=lat_long,actual_latlong=tracking_table_latlong)  
                    
                    

                #--------- Market Info

                marketInfoArrayList = []
                market_infoList = market_info.split('<rd>')
                for i in range(len(market_infoList)):                                                                                                                                                                             
                    brandList = market_infoList[i].split('<fd>')
                    if len(brandList) == 9:
                        brand_name = brandList[0]
                        monthly_sales = brandList[1]
                        stock = brandList[2]
                        credit_amt = brandList[3]
                        price = brandList[4]
                        free_bag = brandList[5]
                        retailer_commission = brandList[6]
                        trade_promotion = brandList[7]
                        remarks = brandList[8]

                        if monthly_sales == '':
                            monthly_sales = 0
                        if stock == '':
                            stock = 0
                        if credit_amt == '':
                            credit_amt = 0
                        if price == '':
                            price = 0

                        if free_bag == '':
                            free_bag = 0
                        if retailer_commission == '':
                            retailer_commission = 0


                        marketInfoArrayList.append({'cid':cid, 'SL':vsl, 'brand_name':brand_name, 'monthly_sales':monthly_sales, 'stock':stock, 'credit_amt':credit_amt, 'price':price, 'free_bag':free_bag, 'retailer_commission':retailer_commission, 'trade_promotion':trade_promotion, 'remarks':remarks, 'client_id':client_id, 'region_id':regionid, 'area_id':areaid, 'territory_id':terriroryid, 'market_id':route_id, 'monthly_last_flag':1})
                if len(marketInfoArrayList) > 0:
                    db.visit_market_info.bulk_insert(marketInfoArrayList)
                    db((db.visit_market_info.cid == cid) & (db.visit_market_info.first_date == first_currentDate) & (db.visit_market_info.client_id == client_id) & (db.visit_market_info.SL != vsl)).update(monthly_last_flag=0)

                #--------- Order Info
                orderArrayList = []
                order_infoList = order_info.split('<rd>')
                for i in range(len(order_infoList)):
                    orderDataList = order_infoList[i].split('<fd>')
                    if len(orderDataList) == 2:
                        itemId = orderDataList[0]
                        itemQty = orderDataList[1]

                        itemName = ''
                        itemCat = ''
                        itemPrice = 0

                        itemRow = db((db.sm_item.cid == cid) & (db.sm_item.item_id == itemId)).select(db.sm_item.name, db.sm_item.category_id, db.sm_item.price, limitby=(0, 1))
                        if itemRow:
                            itemName = itemRow[0].name
                            itemCat = itemRow[0].category_id
                            itemPrice = itemRow[0].price

                        ins_dict = {'cid':cid, 'vsl':vsl, 'depot_id':depot_id, 'depot_name':depot_name, 'sl':ordSl, 'client_id':client_id, 'client_name':client_name, 'rep_id':rep_id, 'rep_name':rep_name, 'order_date':visit_date, 'order_datetime':visit_datetime, 'ym_date':firstDate,
                                                                           'area_id':route_id, 'area_name':route_name, 'item_id':itemId, 'item_name':itemName, 'category_id':itemCat, 'quantity':itemQty, 'price':itemPrice, 'order_media':'APP', 'status':'Submitted'}

                        orderArrayList.append(ins_dict)
                if len(orderArrayList) > 0:
                    db.sm_order.bulk_insert(orderArrayList)

                #--------- Merchandizing
                merchandArrayList = []
                merchandizingList = merchandizing.split('<rd>')
                for i in range(len(merchandizingList)):
                    merchandizingDataList = merchandizingList[i].split('<fd>')
                    if len(merchandizingDataList) == 8:
                        m_item_id = merchandizingDataList[0]
                        m_item_name = merchandizingDataList[1]
                        m_qty = merchandizingDataList[2]
                        m_date = merchandizingDataList[3]
                        m_visitble = merchandizingDataList[4]
                        m_status = merchandizingDataList[5]
                        m_dismantled = merchandizingDataList[6]
                        new_flag = merchandizingDataList[7]

                        merchandArrayList.append({'cid':cid, 'SL':vsl, 'client_id':client_id, 'client_name':client_name, 'm_item_id':m_item_id, 'name':m_item_name, 'qty':m_qty, 'installation_date':m_date, 'new_flag':new_flag, 'visible':m_visitble, 'condition_value':m_status, 'dismantled':m_dismantled, 'new_flag':new_flag, 'last_flag':1})
                if len(merchandArrayList) > 0:
                    db.visit_merchandising.bulk_insert(merchandArrayList)
                    db((db.visit_merchandising.cid == cid) & (db.visit_merchandising.client_id == client_id) & (db.visit_merchandising.SL != vsl) & (db.visit_merchandising.last_flag == 1)).update(last_flag=0)

                #--------- Campaign
                campaignArrayList = []
                campaignList = campaign.split('<fd>')
                for i in range(len(campaignList)):
                    offerId = campaignList[i]
                    if offerId != '':
                        offerId = int(campaignList[i])
                        offer_name = ''
                        offerRow = db((db.trade_promotional_offer.cid == cid) & (db.trade_promotional_offer.id == offerId) & (db.trade_promotional_offer.status == 'ACTIVE')).select(db.trade_promotional_offer.ALL, limitby=(0, 1))
                        if offerRow:
                           offer_name = offerRow[0].offer_name
                           offer_from_date = offerRow[0].from_date
                           offer_to_date = offerRow[0].to_date

                           campaignArrayList.append({'cid':cid, 'vsl':vsl, 'first_date':firstDate, 'visit_date':visit_date, 'client_id':client_id, 'client_name':client_name, 'offer_id':offerId, 'offer_name':offer_name, 'offer_from_date':offer_from_date, 'offer_to_date':offer_to_date, 'last_flag':1})

                if len(campaignArrayList) > 0:
                    db.visit_client_offer.bulk_insert(campaignArrayList)
                    db((db.visit_client_offer.cid == cid) & (db.visit_client_offer.client_id == client_id) & (db.visit_client_offer.vsl != vsl) & (db.visit_client_offer.last_flag == 1)).update(last_flag=0)

                #---------------- NB. Required update first date if visit date not same month
                if visit_type == 'Scheduled':
                    db((db.sm_visit_plan.cid == cid) & (db.sm_visit_plan.schedule_date == schedule_date) & (db.sm_visit_plan.client_id == client_id)).update(visited_flag=1, visit_sl=vsl, visit_date=visit_date, status='Visited')

    return 'SUCCESS<SYNCDATA>' + str(vsl)

# http://127.0.0.1:8000/lscmreporting/syncmobile/deliverySubmit?cid=LSCRM&rep_id=101&rep_pass=123&synccode=5771&depot_id=1&delivery_data=&lat=0&long=0
# http://127.0.0.1:8000/lscmreporting/syncmobile/deliverySubmit?cid=LSCRM&rep_id= 1004&rep_pass=6085&synccode=&depot_id=812010&delivery_data=R100585 <rd> 1800106001 <fd> 4 <fdfd> 1800201001 <fd> 10 <fdfd> 1800201006 <fd> 2&lat=0&long=0
# delivery_data=client_id1 <rd> item_id1 <fd> qty <fdfd> item_id2 <fd> qty <fdfd> item_id3 <fd> qty <rdrd>
# R100585 <rd> 1800106001 <fd> 4 <fdfd> 1800201001 <fd> 10 <fdfd> 1800201006 <fd> 2 <rdrd>

def deliverySubmit():
    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.rep_pass).strip()
    synccode = str(request.vars.synccode).strip()
    depot_id = str(request.vars.depot_id).strip().upper()
    delivery_data = str(request.vars.delivery_data).strip()
    deliveryDate = str(request.vars.delivery_date).strip()

    latitude = request.vars.lat
    longitude = request.vars.long

    if latitude == '' or latitude == None:
        latitude = 0
    if longitude == '' or longitude == None:
        longitude = 0

    lat_long = str(latitude) + ',' + str(longitude)


    delivery_date = ''
    try:
        delivery_date = datetime.datetime.strptime(deliveryDate, '%Y-%m-%d')
    except:
        try:
            delivery_date = datetime.datetime.strptime(deliveryDate, '%d-%m-%Y')
        except:
            return 'FAILED<SYNCDATA>Invalid Date'


    # visit_date=current_date
    order_datetime = delivery_date  # date_fixed
    firstDate = str(delivery_date)[0:7] + '-01'  # 2014-09-16
    depot_name = ''
    client_id = ''
    client_name = ''
    route_id = ''
    route_name = ''


    compRow = db((db.sm_company_settings.cid == cid) & (db.sm_company_settings.status == 'ACTIVE')).select(db.sm_company_settings.cid, limitby=(0, 1))
    if not compRow:
        return 'FAILED<SYNCDATA>Invalid Company'
    else:
        repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.sync_code == synccode) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.rep_id, db.sm_rep.name, db.sm_rep.mobile_no, db.sm_rep.user_type, db.sm_rep.level_id, limitby=(0, 1))
        if not repRow:
           return 'FAILED<SYNCDATA>Invalid Authorization'
        else:
            rep_name = repRow[0].name
            mobile_no = repRow[0].mobile_no
            user_type = repRow[0].user_type

            if delivery_data == '':
                return 'FAILED<SYNCDATA>Data not available'
            else:
                #---------
                delivery_dataList = delivery_data.split('<rdrd>')
                for i in range(len(delivery_dataList)):
                    deliveryDataList = delivery_dataList[i].split('<rd>')
                    if len(deliveryDataList) == 2:
                        client_id = str(deliveryDataList[0]).strip().upper()
                        clientData = deliveryDataList[1]

                        #----------------------
                        clientRecords = db((db.sm_client.cid == cid) & (db.sm_client.client_id == client_id) & (db.sm_client.depot_id == depot_id) & (db.sm_client.status == 'ACTIVE')).select(db.sm_client.name, db.sm_client.category_id, db.sm_client.area_id, limitby=(0, 1))
                        if not clientRecords:
                            return 'FAILED<SYNCDATA>Invalid Retailer'
                        else:
                            client_name = clientRecords[0].name
                            client_cat = clientRecords[0].category_id
                            route_id = clientRecords[0].area_id

                            levelRecords = db((db.sm_level.cid == cid) & (db.sm_level.level_id == route_id)).select(db.sm_level.level_id, db.sm_level.level_name, db.sm_level.depth, db.sm_level.level0, limitby=(0, 1))
                            if levelRecords:
                                route_name = levelRecords[0].level_name

                            #----
                            vsl = 0
                            depotRow = db((db.sm_depot.cid == cid) & (db.sm_depot.depot_id == depot_id)).select(db.sm_depot.id, db.sm_depot.name, db.sm_depot.del_sl, limitby=(0, 1))
                            if depotRow:
                                depot_name = depotRow[0].name
                                del_sl = int(depotRow[0].del_sl)
                                vsl = del_sl + 1
                            depotRow[0].update_record(del_sl=vsl)

                            #---------------------------
                            headFlag = False
                            totalAmount = 0
                            insert_list = []
                            clientDataList = str(clientData).split('<fdfd>')
                            for j in range(len(clientDataList)):
                                itemDataList = str(clientDataList[j]).split('<fd>')
                                if len(itemDataList) == 2:
                                    itemId = str(itemDataList[0]).strip().upper()
                                    itemIQty = itemDataList[1]

                                    if (itemIQty == ''):
                                            itemIQty = 0

                                    itemName = ''
                                    itemCat = ''
                                    itemPrice = 0

                                    itemRow = db((db.sm_item.cid == cid) & (db.sm_item.item_id == itemId)).select(db.sm_item.name, db.sm_item.category_id, db.sm_item.price, limitby=(0, 1))
                                    if itemRow:
                                        itemName = itemRow[0].name
                                        itemCat = itemRow[0].category_id
                                        itemPrice = itemRow[0].price

                                    #--------
                                    if int(itemIQty) > 0:
                                        temp_amount = float(itemPrice) * float(itemIQty)
                                        totalAmount = float(totalAmount) + float(temp_amount)

                                        ins_dict = {'cid':cid, 'depot_id':depot_id, 'depot_name':depot_name, 'sl':vsl, 'client_id':client_id, 'client_name':client_name, 'rep_id':rep_id, 'rep_name':rep_name, 'order_datetime':order_datetime, 'delivery_date':delivery_date, 'area_id':route_id, 'area_name':route_name, 'item_id':itemId, 'item_name':itemName, 'category_id':itemCat, 'quantity':itemIQty, 'price':itemPrice, 'invoice_media':'APP', 'status':'Invoiced', 'ym_date':firstDate}
                                        insert_list.append(ins_dict)

                                        #---------------- Update target AchievementQty
                                        achievement_qty = 0
                                        targetRow = db((db.target_vs_achievement.cid == cid) & (db.target_vs_achievement.first_date == firstDate) & (db.target_vs_achievement.client_id == client_id) & (db.target_vs_achievement.item_id == itemId)).select(db.target_vs_achievement.id, db.target_vs_achievement.achievement_qty, limitby=(0, 1))
                                        if targetRow:
                                            achievement_qty = int(targetRow[0].achievement_qty)
                                            newAchQty = achievement_qty + int(itemIQty)
                                            targetRow[0].update_record(achievement_qty=newAchQty)

                                        #---------------
                                        if headFlag == False:
                                            db.sm_invoice_head.insert(cid=cid, depot_id=depot_id, depot_name=depot_name, sl=vsl, client_id=client_id, client_name=client_name, rep_id=rep_id, rep_name=rep_name, delivery_date=delivery_date, area_id=route_id, area_name=route_name, invoice_media='APP', ym_date=firstDate)
                                            headFlag = True

                            if len(insert_list) > 0:
                                #------
                                data_for_balance_update = str(cid) + '<fdfd>DELIVERY<fdfd>' + str(vsl) + '<fdfd>' + str(datetime_fixed) + '<fdfd>' + str(depot_id) + '-' + str(vsl) + '<fdfd>DPT-' + str(depot_id) + '<fdfd>CLT-' + str(client_id) + '<fdfd>' + str(totalAmount)
                                result_string = set_balance_transaction(data_for_balance_update)

                                db((db.sm_invoice_head.cid == cid) & (db.sm_invoice_head.depot_id == depot_id) & (db.sm_invoice_head.sl == vsl)).update(status='Invoiced')
                                db.sm_invoice.bulk_insert(insert_list)

    #----

    return 'SUCCESS'

# http://127.0.0.1:8000/lscmreporting/syncmobile/updateClientProfile?cid=LSCRM&rep_id=101&rep_pass=123&synccode=5771&client_id=1&client_profile=
def updateClientProfile():
    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.rep_pass).strip()
    synccode = str(request.vars.synccode).strip()

    # client_data = str(request.vars.client_data).strip()
    client_data = urllib2.unquote(request.vars.client_data)

    latitude = request.vars.lat
    longitude = request.vars.long

    if latitude == '' or latitude == None:
        latitude = 0
    if longitude == '' or longitude == None:
        longitude = 0

    profile_photo = str(request.vars.profile_photo).strip()
    if profile_photo == 'None' or profile_photo == 'undefined':
        profile_photo = ''

    profile_photo_str = str(request.vars.profile_photo_str).strip()
    if profile_photo_str == 'None' or profile_photo_str == 'undefined':
        profile_photo_str = ''

    visit_date = current_date
    visit_datetime = date_fixed

    compRow = db((db.sm_company_settings.cid == cid) & (db.sm_company_settings.status == 'ACTIVE')).select(db.sm_company_settings.cid, limitby=(0, 1))
    if not compRow:
        return 'FAILED<SYNCDATA>Invalid Company'
    else:
        repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.sync_code == synccode) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.rep_id, db.sm_rep.name, db.sm_rep.mobile_no, db.sm_rep.user_type, db.sm_rep.level_id, limitby=(0, 1))
        if not repRow:
           return 'FAILED<SYNCDATA>Invalid Authorization'
        else:
            rep_name = repRow[0].name
            mobile_no = repRow[0].mobile_no
            user_type = repRow[0].user_type

            client_dataList = client_data.split('<fd>')
            if len(client_dataList) != 31:
                return 'FAILED<SYNCDATA>Invalid Data'
            else:
                client_id = client_dataList[0]
                cp_name = client_dataList[1]
                cp_address = client_dataList[2]
                cp_marketid = client_dataList[3]
                cp_contact1 = client_dataList[4]
                cp_contact2 = client_dataList[5]

                cp_owner_name = client_dataList[6]
                cp_nid = client_dataList[7]
                cp_Passport = client_dataList[8]
                cp_dob = client_dataList[9]
                cp_dom = client_dataList[10]
                cp_kidsinfo = client_dataList[11]
                cp_hobby = client_dataList[12]
                cp_trade_license = client_dataList[13]
                cp_trade_licence_no = client_dataList[14]
                cp_vat_registration = client_dataList[15]
                cp_vat_reg_no = client_dataList[16]

                cp_manager_name = client_dataList[17]
                cp_manager_cont_no = client_dataList[18]
                cp_starting_year = client_dataList[19]
                cp_Category = client_dataList[20]
                cp_lsc_covered = client_dataList[21]
                cp_monthly_sales_capacity = client_dataList[22]
                cp_monthly_sales = client_dataList[23]
                cp_shop_rent_own = client_dataList[24]
                cp_warehouse_capacity = client_dataList[25]
                cp_shop_size = client_dataList[26]
                cp_shop_front_size = client_dataList[27]
                cp_truck_number = client_dataList[28]
                cp_barge_number = client_dataList[29]
                cp_status = client_dataList[30]


#            cp_id+'<fd>'+cp_name+'<fd>'+cp_address+'<fd>'+cp_marketid+'<fd>'+cp_contact1+'<fd>'+cp_contact2+'<fd>'+
#            cp_owner_name+'<fd>'+cp_nid+'<fd>'+cp_Passport+'<fd>'+cp_dob+'<fd>'+cp_dom+'<fd>'+cp_kidsinfo+'<fd>'+cp_hobby+'<fd>'+cp_trade_license+'<fd>'+cp_trade_licence_no+'<fd>'+cp_vat_registration+'<fd>'+cp_vat_reg_no+'<fd>'+
#            cp_manager_name+'<fd>'+cp_manager_cont_no+'<fd>'+cp_starting_year+'<fd>'+cp_Category+'<fd>'+cp_lsc_covered+'<fd>'+
#            cp_monthly_sales_capacity+'<fd>'+cp_monthly_sales+'<fd>'+cp_shop_rent_own+'<fd>'+cp_warehouse_capacity+'<fd>'+cp_shop_size+'<fd>'+
#            cp_shop_front_size+'<fd>'+cp_truck_number+'<fd>'+cp_barge_number+'<fd>'+cp_status

            #----
            clientRecords = db((db.sm_client.cid == cid) & (db.sm_client.client_id == client_id) & (db.sm_client.status == 'ACTIVE')).select(db.sm_client.id, limitby=(0, 1))
            if not clientRecords:
                return 'FAILED<SYNCDATA>Invalid Retailer'
            else:
                try:
                    cp_monthly_sales = 0
                    cp_warehouse_capacity = 0
                    cp_shop_size = 0
                    cp_shop_front_size = 0
                    cp_truck_number = 0
                    cp_barge_number = 0
                    cp_monthly_sales_capacity = 0
#                 return 'cp_name:' + str(cp_name) + '   ' + 'cp_address:' + str(cp_address) + '   ' + 'cp_contact1:' + str(cp_contact1) + '   ' + 'cp_contact2:' + str(cp_contact2) + '   ' + 'cp_owner_name:' + str(cp_owner_name) + '   ' + 'cp_nid: ' + str(cp_nid) + '   ' + 'cp_Passport: ' + str(cp_Passport) + '   ' + 'cp_dob: ' + str(cp_dob) + '   ' + 'cp_dom: ' + str(cp_dom) + '   ' + 'cp_kidsinfo: ' + str(cp_kidsinfo) + '   ' + 'cp_hobby: ' + str(cp_hobby) + '   ' + 'cp_trade_license: ' + str(cp_trade_license) + '   ' + 'cp_trade_licence_no: ' + str(cp_trade_licence_no) + '   ' + str(cp_vat_registration) + '   ' + 'cp_vat_reg_no: ' + str(cp_vat_reg_no) + '   ' + 'cp_manager_name: ' + str(cp_manager_name) + '   ' + 'cp_manager_cont_no: ' + str(cp_manager_cont_no) + '   ' + 'cp_starting_year: ' + str(cp_starting_year) + '   ' + 'cp_Category: ' + str(cp_Category) + '   ' + 'cp_lsc_covered: ' + str(cp_lsc_covered) + '   ' + 'cp_monthly_sales_capacity: ' + str(cp_monthly_sales_capacity) + '   ' + 'cp_monthly_sales: ' + str(cp_monthly_sales) + '   ' + 'cp_shop_rent_own: ' + str(cp_shop_rent_own) + '   ' + 'cp_warehouse_capacity; ' + str(cp_warehouse_capacity) + '   ' + 'cp_shop_size: ' + str(cp_shop_size) + '   ' + 'cp_shop_front_size: ' + str(cp_shop_front_size) + '   ' + 'cp_truck_number: ' + str(cp_truck_number) + '   ' + 'cp_barge_number: ' + str(cp_barge_number) + '   ' + 'cp_status: ' + str(cp_status) + '   ' + 'latitude: ' + str(latitude) + '   ' + 'longitude: ' + str(longitude) + '   ' + 'profile_photo: ' + str(profile_photo) + '   ' + 'profile_photo_str:' + str(profile_photo_str) + '   ' + 'visit_datetime:' + str(visit_datetime) + '   ' + 'rep_id:' + str(rep_id)


                    if (cp_nid == 'None'):
                        cp_nid = '0'

                    clientRecords[0].update_record(name=cp_name, address=cp_address, contact_no1=cp_contact1, contact_no2=cp_contact2,
                        owner_name=cp_owner_name, nid=cp_nid, passport=cp_Passport, dob=cp_dob, dom=cp_dom, kids_info=cp_kidsinfo, hobby=cp_hobby, trade_license=cp_trade_license, trade_license_no=cp_trade_licence_no, vat_registration=cp_vat_registration, vat_registration_no=cp_vat_reg_no,
                        manager_name=cp_manager_name, manager_contact_no=cp_manager_cont_no, starting_year=cp_starting_year, category_id=cp_Category,
                        lsc_covered=cp_lsc_covered, monthly_sales_capacity=cp_monthly_sales_capacity, monthly_sales=cp_monthly_sales,
                        shop_owner_status=cp_shop_rent_own, warehouse_capacity=cp_warehouse_capacity, shop_size=cp_shop_size, shop_front_size=cp_shop_front_size, truck_number=cp_truck_number, barge_number=cp_barge_number, status=cp_status, latitude=latitude, longitude=longitude, photo=profile_photo, photo_str=profile_photo_str, updated_on=visit_datetime, updated_by=rep_id)
#                 return db._lastsql
                except:
                    return 'FAILED<SYNCDATA>Error to Update data'

                return 'SUCCESS'




# =====================MapClientProfile
def Map():
    retStatus = ''

    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.rep_pass).strip()
    synccode = str(request.vars.synccode).strip()
    market_id = str(request.vars.market_id).strip()

    compRow = db((db.sm_company_settings.cid == cid) & (db.sm_company_settings.status == 'ACTIVE')).select(db.sm_company_settings.cid, limitby=(0, 1))
    if not compRow:
        return 'FAILED<SYNCDATA>Invalid Company'
    else:
        repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.sync_code == synccode) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.user_type, limitby=(0, 1))
        if not repRow:
           retStatus = 'FAILED<SYNCDATA>Invalid Authorization'
           return retStatus
        else:
            user_type = repRow[0].user_type

            #------ market list
            clientStr = ''
#            clientRows = db((db.sm_client.cid == cid) & (db.sm_client.area_id == market_id) & (db.sm_client.status == 'ACTIVE') & (db.sm_client.latitude != '0') & (db.sm_client.longitude != '0')).select(db.sm_client.client_id, db.sm_client.name, db.sm_client.latitude, db.sm_client.longitude, orderby=db.sm_client.name)


            if (client_cat == ''):
                clientRows = db((db.sm_client.cid == cid) & (db.sm_client.area_id == market_id) & (db.sm_client.status == 'ACTIVE') & (db.sm_client.category_id == client_cat)).select(db.sm_client.client_id, db.sm_client.name, orderby=db.sm_client.name)
            else:
                clientRows = db((db.sm_client.cid == cid) & (db.sm_client.area_id == market_id) & (db.sm_client.status == 'ACTIVE') & (db.sm_client.category_id == client_cat)).select(db.sm_client.client_id, db.sm_client.name, orderby=db.sm_client.name)

            return db._lastsql
            if not clientRows:
                retStatus = 'FAILED<SYNCDATA>Retailer not available or Location not confirmed'
                return retStatus
            else:
                start_flag = 0
                map_string_name = ''
                map_string_name_in = ''
                center_point = ''
                c = 0
                x = 0

                for row in clientRows:
                    c = c + 1
                    clientStr = str(row.name) + '( ' + str(row.client_id) + ' )'
                    point_view = str(row.latitude) + ',' + str(row.longitude)


                    clientStr = """<li class="ui-btn ui-shadow ui-corner-all ui-btn-icon-left ui-icon-location" style="border-bottom-style:solid; border-color:#CBE4E4;border-bottom-width:thin"><a onClick="marketRetailerNextCProfileLV(' """ + str(row.name) + """-""" + str(row.client_id) + """ ')">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;""" + str(row.name) + """-""" + str(row.client_id) + """</a></li>"""



                    #             point_view = str(row.sm_client.field1)
#                     pSName = str(row.name)
#                     if (c == 1):
#                         center_point = point_view
                    if (start_flag == 0):
                        center_point = point_view
                        map_string_name = map_string_name + clientStr + "," + str(point_view) + ',' + str(x) + 'rdrd'
                        start_flag = 1
                    else:
                        map_string_name = map_string_name + clientStr + "," + str(point_view) + ',' + str(x) + 'rdrd'
                    x = x + 1

                if (map_string_name == ''):
                    map_string_name = 'No Outlet Available' + "," + '23.811991,90.422952' + ',' + '0' + 'rdrd'
                    center_point = '23.811991, 90.422952'

                clientStr = str(map_string_name) + '<fdfd>' + str(center_point)

            return 'SUCCESS<SYNCDATA>' + clientStr


#============================= Image Upload
def fileUploaderVisit():
    import shutil
    filename = request.vars.upload.filename
    file = request.vars.upload.file
#    shutil.copyfileobj(file,open('C:/workspace/Dropbox/sabbir_acer/web2py/applications/welcome/uploads/'+filename,'wb'))
    shutil.copyfileobj(file, open('/home/www-data/web2py/applications/lscmreporting/static/visit_pic/' + filename, 'wb'))
    return 'success'

# def fileUploaderProfile():
#    import shutil
#    filename = request.vars.upload.filename
#    file = request.vars.upload.file
# #    shutil.copyfileobj(file,open('C:/workspace/Dropbox/sabbir_acer/web2py/applications/welcome/uploads/'+filename,'wb'))
#    shutil.copyfileobj(file, open('/home/www-data/web2py/applications/lscmreporting/static/client_pic/' + filename, 'wb'))
#    return 'success'


def fileUploaderProfile():
    import shutil
    filename = request.vars.upload.filename
    file = request.vars.upload.file

    #    Remove file start============
    import os
    myfile = "/home/www-data/web2py/applications/lscrmap/static/client_pic/" + filename

    # # if file exists, delete it ##
    if os.path.isfile(myfile):
        os.remove(myfile)

#    Remove file end============

#    shutil.copyfileobj(file,open('C:/workspace/Dropbox/sabbir_acer/web2py/applications/welcome/uploads/'+filename,'wb'))
    shutil.copyfileobj(file, open('/home/www-data/web2py/applications/lscrmap/static/client_pic/' + filename, 'wb'))
    return 'success'




#============================= Report
def getVisitReport():
    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.rep_pass).strip()
    synccode = str(request.vars.synccode).strip()
    client_id = str(request.vars.client_id).strip()

    compRow = db((db.sm_company_settings.cid == cid) & (db.sm_company_settings.status == 'ACTIVE')).select(db.sm_company_settings.cid, limitby=(0, 1))
    if not compRow:
        return 'FAILED<SYNCDATA>Invalid Company'
    else:
        repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.sync_code == synccode) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.user_type, limitby=(0, 1))
        if not repRow:
           retStatus = 'FAILED<SYNCDATA>Invalid Authorization'
           return retStatus
        else:
            user_type = repRow[0].user_type

            clientRecords = db((db.sm_client.cid == cid) & (db.sm_client.client_id == client_id) & (db.sm_client.status == 'ACTIVE')).select(db.sm_client.ALL, limitby=(0, 1))
            if not clientRecords:
                return 'FAILED<SYNCDATA>Invalid Client'
            else:
                route_id = str(clientRecords[0].area_id)
                route_name = ''

                levelRecords = db((db.sm_level.cid == cid) & (db.sm_level.level_id == route_id)).select(db.sm_level.level_name, limitby=(0, 1))
                if levelRecords:
                    route_name = str(levelRecords[0].level_name)

                market = route_name + '-' + route_id

                #--------- client campaign
                lastClientCampaignStr = '<tr ><td colspan="3" ><b>Campaign:</b></td></tr>'
                lastClientCampaignStr += '<tr style="font-weight:bold; text-shadow:none; color:#408080;" ><td >Visit Date</td><td >Offer</td><td>Period</td></tr>'

                clientOfferRows = db((db.visit_client_offer.cid == cid) & (db.visit_client_offer.client_id == client_id) & (db.visit_client_offer.last_flag == 1)).select(db.visit_client_offer.ALL, orderby=db.visit_client_offer.vsl | db.visit_client_offer.offer_id)
                for clientOfferRow in clientOfferRows:
                    visit_date = str(clientOfferRow.visit_date.strftime('%d-%m-%Y'))
                    offer_id = str(clientOfferRow.offer_id)
                    offer_name = str(clientOfferRow.offer_name)
                    offer_from_date = str(clientOfferRow.offer_from_date.strftime('%d-%m-%Y'))
                    offer_to_date = str(clientOfferRow.offer_to_date.strftime('%d-%m-%Y'))

                    offerDes = offer_from_date + ', ' + offer_to_date

                    lastClientCampaignStr += '<tr style="font-size:11px;"><td>' + visit_date + '</td><td >' + offer_name + ' (' + offer_id + ')</td><td>' + offerDes + '</td></tr>'

                #-------------------- Retailer Stock

                marketLastVSl = ''
                visit_date = ''
                marketInfoLastRows = db((db.visit_market_info.cid == cid) & (db.visit_market_info.client_id == client_id)).select(db.visit_market_info.SL, orderby= ~db.visit_market_info.SL, limitby=(0, 1))
                if marketInfoLastRows:
                    marketLastVSl = int(marketInfoLastRows[0].SL)

                    visitRows = db((db.sm_order_head.cid == cid) & (db.sm_order_head.id == marketLastVSl)).select(db.sm_order_head.sl, db.sm_order_head.rep_id, db.sm_order_head.rep_name, db.sm_order_head.order_date, db.sm_order_head.visit_type, db.sm_order_head.mobile_no, orderby= ~db.sm_order_head.sl, limitby=(0, 1))
                    if visitRows:
                        visit_date = visitRows[0].order_date.strftime('%d-%m-%Y')


                lastStockStr = '<tr ><td colspan="2" ><b>Retailer Sotck: (' + str(visit_date) + ')</b></td></tr>'
                lastStockStr += '<tr style="font-weight:bold; text-shadow:none; color:#408080;" ><td >Brand</td><td >Stock</td></tr>'

                marketInfoStockList = []
                marketInfoStockRows = db((db.visit_market_info.cid == cid) & (db.visit_market_info.SL == marketLastVSl)).select(db.visit_market_info.brand_name, db.visit_market_info.stock, orderby=db.visit_market_info.brand_name)
                for marketStockRow in marketInfoStockRows:
                    brand_name = str(marketStockRow.brand_name)
                    stock = int(marketStockRow.stock)
                    marketInfoStockList.append({'Brand':brand_name, 'Qty':stock})

                    lastStockStr += '<tr style="font-size:11px;"><td>' + brand_name + '</td><td >' + str(stock) + '</td></tr>'

                #----------- Sales Delivery
                previousTwoMonth = deduct_months(first_currentDate, 2)

                salesList = []

                monthStart = previousTwoMonth
                salesDeliveryRows1 = db((db.sm_invoice.cid == cid) & (db.sm_invoice.client_id == client_id) & (db.sm_invoice.ym_date == monthStart) & (db.sm_invoice.note != 'Returned')).select(db.sm_invoice.ym_date, db.sm_invoice.quantity.sum(), orderby=db.sm_invoice.ym_date, groupby=db.sm_invoice.ym_date)
                if not salesDeliveryRows1:
                    salesMonth = monthStart.strftime('%b-%Y')
                    salesList.append({'Month':salesMonth, 'Qty':0})
                else:
                    for salesDel in salesDeliveryRows1:
                        salesMonth = salesDel.sm_invoice.ym_date.strftime('%b-%Y')
                        salesQty = salesDel[db.sm_invoice.quantity.sum()]
                        salesList.append({'Month':salesMonth, 'Qty':salesQty})

                monthStart = add_months(monthStart, 1)
                salesDeliveryRows2 = db((db.sm_invoice.cid == cid) & (db.sm_invoice.client_id == client_id) & (db.sm_invoice.ym_date == monthStart) & (db.sm_invoice.note != 'Returned')).select(db.sm_invoice.ym_date, db.sm_invoice.quantity.sum(), orderby=db.sm_invoice.ym_date, groupby=db.sm_invoice.ym_date)
                if not salesDeliveryRows2:
                    salesMonth = monthStart.strftime('%b-%Y')
                    salesList.append({'Month':salesMonth, 'Qty':0})
                else:
                    for salesDel in salesDeliveryRows2:
                        salesMonth = salesDel.sm_invoice.ym_date.strftime('%b-%Y')
                        salesQty = salesDel[db.sm_invoice.quantity.sum()]
                        salesList.append({'Month':salesMonth, 'Qty':salesQty})

                monthStart = add_months(monthStart, 1)
                salesDeliveryRows3 = db((db.sm_invoice.cid == cid) & (db.sm_invoice.client_id == client_id) & (db.sm_invoice.ym_date == monthStart) & (db.sm_invoice.note != 'Returned')).select(db.sm_invoice.ym_date, db.sm_invoice.quantity.sum(), orderby=db.sm_invoice.ym_date, groupby=db.sm_invoice.ym_date)
                if not salesDeliveryRows3:
                    salesMonth = monthStart.strftime('%b-%Y')
                    salesList.append({'Month':salesMonth, 'Qty':0})
                else:
                    for salesDel in salesDeliveryRows3:
                        salesMonth = salesDel.sm_invoice.ym_date.strftime('%b-%Y')
                        salesQty = salesDel[db.sm_invoice.quantity.sum()]
                        salesList.append({'Month':salesMonth, 'Qty':salesQty})

                return 'SUCCESS<SYNCDATA>' + lastClientCampaignStr + '<SYNCDATA>' + lastStockStr + '<SYNCDATA>' + str(marketInfoStockList) + '<SYNCDATA>' + str(salesList)


#=====
def complainSubmit():
    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.rep_pass).strip()
    synccode = str(request.vars.synccode).strip()

    complain_from = str(request.vars.complain_from).strip()
    complain_ref = str(request.vars.complain_ref).strip()
    complain_type = str(request.vars.complain_type).strip()
    complain_details = str(request.vars.complain_details).strip()

    submit_date = current_date
    visit_datetime = date_fixed
    firstDate = first_currentDate


    compRow = db((db.sm_company_settings.cid == cid) & (db.sm_company_settings.status == 'ACTIVE')).select(db.sm_company_settings.cid, limitby=(0, 1))
    if not compRow:
        return 'FAILED<SYNCDATA>Invalid Company'
    else:
        repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.sync_code == synccode) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.rep_id, db.sm_rep.name, db.sm_rep.mobile_no, db.sm_rep.user_type, db.sm_rep.level_id, limitby=(0, 1))
        if not repRow:
           return 'FAILED<SYNCDATA>Invalid Authorization'
        else:
            rep_name = repRow[0].name
            mobile_no = repRow[0].mobile_no
            user_type = repRow[0].user_type

            #----
#             complainFromRows = db((db.sm_category_type.cid == cid) & (db.sm_category_type.type_name == 'COMPLAIN_FROM') & (db.sm_category_type.cat_type_id == complain_from)).select(db.sm_category_type.cat_type_id, limitby=(0, 1))
#             if not complainFromRows:
#                 return 'FAILED<SYNCDATA>Invalid COMPLAIN FROM Sync Again for Update'
#             else:
                #----
            complainTypeRows = db((db.sm_category_type.cid == cid) & (db.sm_category_type.type_name == 'COMPLAIN_TYPE') & (db.sm_category_type.cat_type_id == complain_type)).select(db.sm_category_type.cat_type_id, limitby=(0, 1))
            if not complainTypeRows:
                return 'FAILED<SYNCDATA>Invalid Feedback TYPE Sync Again for Update'
            else:

                #----
                insertRes = db.complain.insert(cid=cid, submit_firstdt=firstDate, submit_date=submit_date, submitted_by_id=rep_id, submitted_by_name=rep_name, complain_from=complain_from, ref=complain_ref, complain_type=complain_type, des=complain_details, status='Submitted')
#                sl = db.sm_order_head(insertRes).id

                return 'SUCCESS<SYNCDATA>' #+ str(sl)

#=====
def showComplain():
    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.rep_pass).strip()
    synccode = str(request.vars.synccode).strip()


    compRow = db((db.sm_company_settings.cid == cid) & (db.sm_company_settings.status == 'ACTIVE')).select(db.sm_company_settings.cid, limitby=(0, 1))
    if not compRow:
        return 'FAILED<SYNCDATA>Invalid Company'
    else:
        repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.sync_code == synccode) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.rep_id, db.sm_rep.name, db.sm_rep.mobile_no, db.sm_rep.user_type, db.sm_rep.level_id, limitby=(0, 1))
        if not repRow:
           return 'FAILED<SYNCDATA>Invalid Authorization'
        else:
            rep_name = repRow[0].name
            mobile_no = repRow[0].mobile_no
            user_type = repRow[0].user_type


            #--------- Complain
#             reportStr = '<tr style="font-weight:bold; text-shadow:none; color:#408080;" ><td >Submit</td><td >Type</td><td>From, Ref</td><td>Action</td></tr>'
            reportStr = '<tr style="font-weight:bold; text-shadow:none; color:#408080;" ><td >Submit</td><td >Type</td><td>Feedback</td></tr>'

            records = db((db.complain.cid == cid) & (db.complain.submitted_by_id == rep_id)).select(db.complain.ALL, orderby= ~db.complain.id, limitby=(0, 10))

            for record in records:
                submit_date = str(record.submit_date.strftime('%d-%m-%Y'))
                complain_type = str(record.complain_type)
                complain_from = str(record.complain_from)
                ref = str(record.ref)
                complain_details = str(record.des)

                reply_msg = str(record.reply_msg)
                action = str(record.action)

#                 reportStr += '<tr style="font-size:11px;"><td>' + submit_date + '</td><td >' + complain_type + '</td><td>' + complain_from + ', ' + ref + '</td><td>' + action + '</td></tr>'
                reportStr += '<tr style="font-size:11px;"><td>' + submit_date + '</td><td >' + complain_type + '</td><td>' + ref + '</td></tr>'

            return 'SUCCESS<SYNCDATA>' + reportStr


#=====
def showTask():
    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.rep_pass).strip()
    synccode = str(request.vars.synccode).strip()

    action = str(request.vars.action).strip()
    rowid = request.vars.rowid


    compRow = db((db.sm_company_settings.cid == cid) & (db.sm_company_settings.status == 'ACTIVE')).select(db.sm_company_settings.cid, limitby=(0, 1))
    if not compRow:
        return 'FAILED<SYNCDATA>Invalid Company'
    else:
        repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.sync_code == synccode) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.rep_id, db.sm_rep.name, db.sm_rep.mobile_no, db.sm_rep.user_type, db.sm_rep.level_id, limitby=(0, 1))
        if not repRow:
           return 'FAILED<SYNCDATA>Invalid Authorization'
        else:
            rep_name = repRow[0].name
            mobile_no = repRow[0].mobile_no
            user_type = repRow[0].user_type


            if action == 'Update':
                try:
                    if int(rowid) > 0:
                        db((db.task.cid == cid) & (db.task.spo_id == rep_id) & (db.task.id == rowid)).update(complete_datetime=date_fixed, complete_date=current_date, status='Done')
                except:
                    pass

            #--------- Task

            reportStr = '<tr style="font-weight:bold; text-shadow:none; color:#408080;" ><td>Task Date</td><td >Type</td><td >Task</td><td>Status</td></tr>'

            records = db((db.task.cid == cid) & (db.task.spo_id == rep_id)).select(db.task.ALL, orderby= ~db.task.id, limitby=(0, 10))
            for record in records:
                id = str(record.id)
                task_type = str(record.task_type)
                task = str(record.task)
                task_datetime = str(record.task_datetime.strftime('%d-%m-%Y %I:%M %p'))
                status = str(record.status)
                complete_datetime = record.complete_datetime

                if complete_datetime != None:
                    complete_datetime = str(complete_datetime.strftime('%d-%m-%Y %I:%M %p'))


                if status == 'Due':
                    reportStr += '<tr style="font-size:11px;"><td>' + task_datetime + '</td><td >' + task + '</td><td>' + task_type + '</td><td><button id="btn_task_update' + id + '" onClick="updateTask(\'' + id + '\')" >' + status + '</button></td></tr>'
                else:
                    reportStr += '<tr style="font-size:11px;"><td>' + task_datetime + '</td><td >' + task + '</td><td>' + task_type + '</td><td>' + status + ', ' + complete_datetime + '</td></tr>'

            return 'SUCCESS<SYNCDATA>' + reportStr


#=====
def regionOrderReport():
    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.rep_pass).strip()
    synccode = str(request.vars.synccode).strip()

    regionId = str(request.vars.regionId).strip()
    month = request.vars.month

    firstDate = str(current_date)[0:5] + str(month) + '-01'
    # return regionId

    compRow = db((db.sm_company_settings.cid == cid) & (db.sm_company_settings.status == 'ACTIVE')).select(db.sm_company_settings.cid, limitby=(0, 1))
    if not compRow:
        return 'FAILED<SYNCDATA>Invalid Company'
    else:
        repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.sync_code == synccode) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.rep_id, db.sm_rep.name, db.sm_rep.mobile_no, db.sm_rep.user_type, db.sm_rep.level_id, limitby=(0, 1))
        if not repRow:
           return 'FAILED<SYNCDATA>Invalid Authorization'
        else:
            rep_name = repRow[0].name
            mobile_no = repRow[0].mobile_no
            user_type = repRow[0].user_type


            areaList = []
            levelRows = db((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '1') & (db.sm_level.level0 == regionId)).select(db.sm_level.level_id, orderby=db.sm_level.level_id)
            for levelRow in levelRows:
                level_id = str(levelRow.level_id).strip()
                areaList.append(level_id)

            records = db((db.sm_order.cid == cid) & (db.sm_order.ym_date == firstDate) & (db.sm_order.area_id.belongs(areaList))).select(db.sm_order.item_id, db.sm_order.item_name, db.sm_order.quantity.sum(), orderby=db.sm_order.item_name, groupby=db.sm_order.item_id)

            #--------- Task
            reportStr = '<tr style="font-weight:bold;" ><td colspan="2">Monthly Order</td></tr>'
            reportStr += '<tr style="font-weight:bold; text-shadow:none; color:#408080;" ><td>Item</td><td >Qty</td></tr>'
            for record in records:
                item_id = str(record.sm_order.item_id)
                item_name = str(record.sm_order.item_name)
                quantity = str(record[db.sm_order.quantity.sum()])

                reportStr += '<tr style="font-size:11px;"><td>' + item_name + '</td><td >' + quantity + '</td></tr>'

            return 'SUCCESS<SYNCDATA>' + reportStr


#=====
def regionSalesConfReport():
    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.rep_pass).strip()
    synccode = str(request.vars.synccode).strip()

    regionId = str(request.vars.regionId).strip()
    month = request.vars.month

    firstDate = str(current_date)[0:5] + str(month) + '-01'
    # return regionId

    compRow = db((db.sm_company_settings.cid == cid) & (db.sm_company_settings.status == 'ACTIVE')).select(db.sm_company_settings.cid, limitby=(0, 1))
    if not compRow:
        return 'FAILED<SYNCDATA>Invalid Company'
    else:
        repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.sync_code == synccode) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.rep_id, db.sm_rep.name, db.sm_rep.mobile_no, db.sm_rep.user_type, db.sm_rep.level_id, limitby=(0, 1))
        if not repRow:
           return 'FAILED<SYNCDATA>Invalid Authorization'
        else:
            rep_name = repRow[0].name
            mobile_no = repRow[0].mobile_no
            user_type = repRow[0].user_type


            areaList = []
            levelRows = db((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '1') & (db.sm_level.level0 == regionId)).select(db.sm_level.level_id, orderby=db.sm_level.level_id)
            for levelRow in levelRows:
                level_id = str(levelRow.level_id).strip()
                areaList.append(level_id)

            #--------- Sales
            records = db((db.sm_invoice.cid == cid) & (db.sm_invoice.ym_date == firstDate) & (db.sm_invoice.area_id.belongs(areaList))).select(db.sm_invoice.item_id, db.sm_invoice.item_name, db.sm_invoice.quantity.sum(), orderby=db.sm_invoice.item_name, groupby=db.sm_invoice.item_id)

            reportStr = '<tr style="font-weight:bold;" ><td colspan="2">Monthly Sales Confirmed</td></tr>'
            reportStr += '<tr style="font-weight:bold; text-shadow:none; color:#408080;" ><td>Item</td><td >Qty</td></tr>'
            for record in records:
                item_id = str(record.sm_invoice.item_id)
                item_name = str(record.sm_invoice.item_name)
                quantity = str(record[db.sm_invoice.quantity.sum()])

                reportStr += '<tr style="font-size:11px;"><td>' + item_name + '</td><td >' + quantity + '</td></tr>'

            return 'SUCCESS<SYNCDATA>' + reportStr

#=====
def regionVisitSummaryReport():
    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.rep_pass).strip()
    synccode = str(request.vars.synccode).strip()

    regionId = str(request.vars.regionId).strip()
    month = request.vars.month

    firstDate = str(current_date)[0:5] + str(month) + '-01'
    # return regionId

    compRow = db((db.sm_company_settings.cid == cid) & (db.sm_company_settings.status == 'ACTIVE')).select(db.sm_company_settings.cid, limitby=(0, 1))
    if not compRow:
        return 'FAILED<SYNCDATA>Invalid Company'
    else:
        repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.sync_code == synccode) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.rep_id, db.sm_rep.name, db.sm_rep.mobile_no, db.sm_rep.user_type, db.sm_rep.level_id, limitby=(0, 1))
        if not repRow:
           return 'FAILED<SYNCDATA>Invalid Authorization'
        else:
            rep_name = repRow[0].name
            mobile_no = repRow[0].mobile_no
            user_type = repRow[0].user_type


            areaList = []
            levelRows = db((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '1') & (db.sm_level.level0 == regionId)).select(db.sm_level.level_id, orderby=db.sm_level.level_id)
            for levelRow in levelRows:
                level_id = str(levelRow.level_id).strip()
                areaList.append(level_id)


            #---------
            scheduleCount = db((db.sm_order_head.cid == cid) & (db.sm_order_head.ym_date == firstDate) & (db.sm_order_head.visit_type == 'Scheduled') & (db.sm_order_head.area_id.belongs(areaList))).count()
            unscheduleCount = db((db.sm_order_head.cid == cid) & (db.sm_order_head.ym_date == firstDate) & (db.sm_order_head.visit_type == 'Unscheduled') & (db.sm_order_head.area_id.belongs(areaList))).count()

            # scheduledVisitedCount=db((db.sm_visit_plan.cid==cid)&(db.sm_visit_plan.first_date==firstDate)&(db.sm_visit_plan.status=='Visited')&(db.sm_visit_plan.level0_id==regionId)).count()
            scheduledVisitPendingCount = db((db.sm_visit_plan.cid == cid) & (db.sm_visit_plan.first_date == firstDate) & (db.sm_visit_plan.status == 'Approved') & (db.sm_visit_plan.level0_id == regionId)).count()

            reportStr = '<tr style="font-weight:bold;" ><td colspan="2">Monthly Visit Summary</td></tr>'
            # reportStr+='<tr style="font-weight:bold; text-shadow:none; color:#408080;" ><td>Item</td><td >Qty</td></tr>'

            reportStr += '<tr style="font-size:11px;"><td>' + 'Scheduled Visit' + '</td><td >' + str(scheduleCount) + '</td></tr>'
            reportStr += '<tr style="font-size:11px;"><td>' + 'Unscheduled Visit' + '</td><td >' + str(unscheduleCount) + '</td></tr>'
            # reportStr+='<tr style="font-size:11px;"><td>'+'Scheduled Visit Done'+'</td><td >'+str(scheduledVisitedCount)+'</td></tr>'
            reportStr += '<tr style="font-size:11px;"><td>' + 'Scheduled Visit Due' + '</td><td >' + str(scheduledVisitPendingCount) + '</td></tr>'

            return 'SUCCESS<SYNCDATA>' + reportStr


#=====
def regionTarVsAchReport():
    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.rep_pass).strip()
    synccode = str(request.vars.synccode).strip()

    regionId = str(request.vars.regionId).strip()
    month = request.vars.month

    firstDate = str(current_date)[0:5] + str(month) + '-01'
    # return regionId

    compRow = db((db.sm_company_settings.cid == cid) & (db.sm_company_settings.status == 'ACTIVE')).select(db.sm_company_settings.cid, limitby=(0, 1))
    if not compRow:
        return 'FAILED<SYNCDATA>Invalid Company'
    else:
        repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.sync_code == synccode) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.rep_id, db.sm_rep.name, db.sm_rep.mobile_no, db.sm_rep.user_type, db.sm_rep.level_id, limitby=(0, 1))
        if not repRow:
           return 'FAILED<SYNCDATA>Invalid Authorization'
        else:
            rep_name = repRow[0].name
            mobile_no = repRow[0].mobile_no
            user_type = repRow[0].user_type


            #-------------- Target Vs Achievement
            reportStr = '<tr style="font-weight:bold;" ><td colspan="2">Monthly Target Vs Achievement</td></tr>'
            reportStr += '<tr style="font-weight:bold; text-shadow:none; color:#408080;" ><td>Brand</td><td >Target / Achievement(Qty)</td></tr>'

            brandWiseTARows = db((db.target_vs_achievement.cid == cid) & (db.target_vs_achievement.first_date == firstDate) & (db.target_vs_achievement.region_id == regionId)).select(db.target_vs_achievement.item_id, db.target_vs_achievement.item_name, db.target_vs_achievement.target_qty.sum(), db.target_vs_achievement.achievement_qty.sum(), orderby=db.target_vs_achievement.item_id, groupby=db.target_vs_achievement.item_id)
            for row in brandWiseTARows:
                item_id = row.target_vs_achievement.item_id
                item_name = row.target_vs_achievement.item_name
                target_qty = row[db.target_vs_achievement.target_qty.sum()]
                achievement_qty = row[db.target_vs_achievement.achievement_qty.sum()]

                reportStr += '<tr style="font-size:11px;"><td>' + item_name + '</td><td >' + str(target_qty) + ' / ' + str(achievement_qty) + '</td></tr>'


            return 'SUCCESS<SYNCDATA>' + reportStr

#=====
def regionTodaySummary():
    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.rep_pass).strip()
    synccode = str(request.vars.synccode).strip()

    regionId = str(request.vars.regionId).strip()
    month = request.vars.month

    toDay = current_date
    # return regionId


    compRow = db((db.sm_company_settings.cid == cid) & (db.sm_company_settings.status == 'ACTIVE')).select(db.sm_company_settings.cid, limitby=(0, 1))
    if not compRow:
        return 'FAILED<SYNCDATA>Invalid Company'
    else:
        repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.sync_code == synccode) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.rep_id, db.sm_rep.name, db.sm_rep.mobile_no, db.sm_rep.user_type, db.sm_rep.level_id, limitby=(0, 1))
        if not repRow:
           return 'FAILED<SYNCDATA>Invalid Authorization'
        else:
            rep_name = repRow[0].name
            mobile_no = repRow[0].mobile_no
            user_type = repRow[0].user_type


            areaList = []
            levelRows = db((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '1') & (db.sm_level.level0 == regionId)).select(db.sm_level.level_id, orderby=db.sm_level.level_id)
            for levelRow in levelRows:
                level_id = str(levelRow.level_id).strip()
                areaList.append(level_id)

            #--------- Order
            records = db((db.sm_order.cid == cid) & (db.sm_order.order_date == toDay) & (db.sm_order.area_id.belongs(areaList))).select(db.sm_order.item_id, db.sm_order.item_name, db.sm_order.quantity.sum(), orderby=db.sm_order.item_name, groupby=db.sm_order.item_id)

            reportStr = '<tr style="font-weight:bold;" ><td colspan="2">Today Order</td></tr>'
            reportStr += '<tr style="font-weight:bold; text-shadow:none; color:#408080;" ><td>Item</td><td >Qty</td></tr>'
            for record in records:
                item_id = str(record.sm_order.item_id)
                item_name = str(record.sm_order.item_name)
                quantity = str(record[db.sm_order.quantity.sum()])

                reportStr += '<tr style="font-size:11px;"><td>' + item_name + '</td><td >' + quantity + '</td></tr>'


            #--------- Sales
            records2 = db((db.sm_invoice.cid == cid) & (db.sm_invoice.delivery_date == toDay) & (db.sm_invoice.area_id.belongs(areaList))).select(db.sm_invoice.item_id, db.sm_invoice.item_name, db.sm_invoice.quantity.sum(), orderby=db.sm_invoice.item_name, groupby=db.sm_invoice.item_id)

            reportStr += '<tr style="font-weight:bold;" ><td colspan="2">Today Sales</td></tr>'
            reportStr += '<tr style="font-weight:bold; text-shadow:none; color:#408080;" ><td>Item</td><td >Qty</td></tr>'
            for record in records2:
                item_id = str(record.sm_invoice.item_id)
                item_name = str(record.sm_invoice.item_name)
                quantity = str(record[db.sm_invoice.quantity.sum()])

                reportStr += '<tr style="font-size:11px;"><td>' + item_name + '</td><td >' + quantity + '</td></tr>'


            #-------- Visit
            scheduleCount = db((db.sm_order_head.cid == cid) & (db.sm_order_head.order_date == toDay) & (db.sm_order_head.visit_type == 'Scheduled') & (db.sm_order_head.area_id.belongs(areaList))).count()
            unscheduleCount = db((db.sm_order_head.cid == cid) & (db.sm_order_head.order_date == toDay) & (db.sm_order_head.visit_type == 'Unscheduled') & (db.sm_order_head.area_id.belongs(areaList))).count()

            # scheduledVisitedCount=db((db.sm_visit_plan.cid==cid)&(db.sm_visit_plan.first_date==firstDate)&(db.sm_visit_plan.status=='Visited')&(db.sm_visit_plan.level0_id==regionId)).count()
            scheduledVisitPendingCount = db((db.sm_visit_plan.cid == cid) & (db.sm_visit_plan.schedule_date == toDay) & (db.sm_visit_plan.status == 'Approved') & (db.sm_visit_plan.level0_id == regionId)).count()

            reportStr += '<tr style="font-weight:bold;" ><td colspan="2">Today Visit</td></tr>'
            # reportStr+='<tr style="font-weight:bold; text-shadow:none; color:#408080;" ><td>Item</td><td >Qty</td></tr>'

            reportStr += '<tr style="font-size:11px;"><td>' + 'Scheduled Visit' + '</td><td >' + str(scheduleCount) + '</td></tr>'
            reportStr += '<tr style="font-size:11px;"><td>' + 'Unscheduled Visit' + '</td><td >' + str(unscheduleCount) + '</td></tr>'
            # reportStr+='<tr style="font-size:11px;"><td>'+'Scheduled Visit Done'+'</td><td >'+str(scheduledVisitedCount)+'</td></tr>'
            reportStr += '<tr style="font-size:11px;"><td>' + 'Scheduled Visit Due' + '</td><td >' + str(scheduledVisitPendingCount) + '</td></tr>'


            return 'SUCCESS<SYNCDATA>' + reportStr





# ========================Doctor Start================

def getMarketClientList_doc():
    retStatus = ''

    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.rep_pass).strip()
    synccode = str(request.vars.synccode).strip()
    market_id = str(request.vars.market_id).strip()

    compRow = db((db.sm_company_settings.cid == cid) & (db.sm_company_settings.status == 'ACTIVE')).select(db.sm_company_settings.cid, limitby=(0, 1))
    if not compRow:
        return 'FAILED<SYNCDATA>Invalid Company'
    else:
        repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.sync_code == synccode) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.user_type, limitby=(0, 1))
        if not repRow:
           retStatus = 'FAILED<SYNCDATA>Invalid Authorization'
           return retStatus
        else:
            user_type = repRow[0].user_type

            #------ market list
            clientStr = ''
            clientRows = db((db.sm_doctor.cid == cid) & (db.sm_doctor.status == 'ACTIVE') & (db.sm_doctor_area.cid == cid) & (db.sm_doctor_area.doc_id == db.sm_doctor.doc_id) & (db.sm_doctor_area.area_id == market_id)).select(db.sm_doctor.doc_id, db.sm_doctor.doc_name, orderby=db.sm_doctor.doc_name)
#            return db._lastsql
            if not clientRows:
                retStatus = 'FAILED<SYNCDATA>Doctor not available'
                return retStatus
            else:
                for clientRow in clientRows:
                    client_id = clientRow.doc_id
                    name = clientRow.doc_name

                    if clientStr == '':
                        clientStr = str(client_id) + '<fd>' + str(name)
                    else:
                        clientStr += '<rd>' + str(client_id) + '<fd>' + str(name)

                return 'SUCCESS<SYNCDATA>' + clientStr



def getClientInfo_doc():
    retStatus = ''

    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.rep_pass).strip()
    synccode = str(request.vars.synccode).strip()
    client_id = str(request.vars.client_id).strip()

    compRow = db((db.sm_company_settings.cid == cid) & (db.sm_company_settings.status == 'ACTIVE')).select(db.sm_company_settings.cid, limitby=(0, 1))
    if not compRow:
        return 'FAILED<SYNCDATA>Invalid Company'
    else:
        repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.sync_code == synccode) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.user_type, limitby=(0, 1))
        if not repRow:
           retStatus = 'FAILED<SYNCDATA>Invalid Authorization'
           return retStatus
        else:
            user_type = repRow[0].user_type

            clientRecords = db((db.sm_client.cid == cid) & (db.sm_client.client_id == client_id) & (db.sm_client.status == 'ACTIVE')).select(db.sm_client.area_id, db.sm_client.depot_id, limitby=(0, 1))
            if not clientRecords:
                return 'FAILED<SYNCDATA>Invalid Client'
            else:
                route_id = str(clientRecords[0].area_id)
                depot_id = str(clientRecords[0].depot_id)
                route_name = ''

                levelRecords = db((db.sm_level.cid == cid) & (db.sm_level.level_id == route_id)).select(db.sm_level.level_name, limitby=(0, 1))
                if levelRecords:
                    route_name = str(levelRecords[0].level_name)

                market = route_name + '-' + route_id

                # -- Distributor
                depot_name = ''
                depotRecords = db((db.sm_depot.cid == cid) & (db.sm_depot.depot_id == depot_id)).select(db.sm_depot.name, limitby=(0, 1))
                if depotRecords:
                    depot_name = str(depotRecords[0].name)

                distributorNameID = depot_name + '-' + depot_id
                #---


                #-----
                merItemStr = ''
                lastMarchRows = db((db.visit_merchandising.cid == cid) & (db.visit_merchandising.client_id == client_id)).select(db.visit_merchandising.SL, orderby= ~db.visit_merchandising.SL, limitby=(0, 1))

                #--------- Last client campaign
                lastClientCampaignStr = ''
                clientOfferRows = db((db.visit_client_offer.cid == cid) & (db.visit_client_offer.client_id == client_id) & (db.visit_client_offer.last_flag == 1)).select(db.visit_client_offer.offer_id, db.visit_client_offer.offer_name, db.visit_client_offer.offer_from_date, db.visit_client_offer.offer_to_date, orderby=db.visit_client_offer.offer_id)
                for clientOfferRow in clientOfferRows:
                    offer_id = str(clientOfferRow.offer_id)
                    offer_name = str(clientOfferRow.offer_name)
                    offer_fromDate = clientOfferRow.offer_from_date
                    offer_toDate = clientOfferRow.offer_to_date

                    offer_Des = str(offer_fromDate.strftime('%d-%m-%Y')) + ', ' + str(offer_toDate.strftime('%d-%m-%Y'))
                    if lastClientCampaignStr == '':
                        lastClientCampaignStr = str(offer_id) + '<fd>' + str(offer_name) + '<fd>' + offer_Des
                    else:
                        lastClientCampaignStr += '<rd>' + str(offer_id) + '<fd>' + str(offer_name) + '<fd>' + offer_Des

                return 'SUCCESS<SYNCDATA>' + market + '<SYNCDATA>' + merItemStr + '<SYNCDATA>' + lastMarketInforStr + '<SYNCDATA>' + campaignStr + '<SYNCDATA>' + lastClientCampaignStr + '<SYNCDATA>' + distributorNameID



# cid.v.doctorid..itemid1,itemid2,itemid3..giftid,qty.giftid,qty..sampleID,sampleQty..notes
# http://127.0.0.1:8000/mreporting/doctor_visit/sms_doctor_visit_submit?password=Compaq510DuoDuo&mob=8801719078552&cid=CONCORD&msg=CON.V.D00001..ACET,ACUP,ACUT..G0001,1.G0002,2..ACUP,4.ACUT,2..Item ACUT work properly
# http://127.0.0.1:8000/mrepbiopharma/syncmobile/doctor_visit_submit?cid=BIOPHARMA&rep_id=NDHK-111&rep_pass=123&synccode=6629&client_id=10001&visit_type=Unscheduled&schedule_date=&msg=BIOPHARMA.v.10001..SAC01,PAC01..,undefined.10002,2.10001,1..SAC01,2.PAC01,3..&lat=&long=
def doctor_visit_submit():
    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.rep_pass).strip()
    synccode = str(request.vars.synccode).strip()
    client_id = str(request.vars.client_id).strip().upper()
    routeID = str(request.vars.route).strip().upper()



    visit_type = str(request.vars.visit_type).strip()  # scheduled,unscheduled
    sch_date = str(request.vars.schedule_date).strip()

    msg = str(request.vars.msg).strip()
#    return msg

    schedule_date = ''
    if visit_type == 'Scheduled':
        try:
            schedule_date = datetime.datetime.strptime(sch_date, '%Y-%m-%d')
        except:
            try:
                schedule_date = datetime.datetime.strptime(sch_date, '%d-%m-%Y')
            except:
                return 'FAILED<SYNCDATA>Invalid Date'


    latitude = request.vars.lat
    longitude = request.vars.long
    v_with = request.vars.v_with
    
    visit_photo = request.vars.visit_photo

    if latitude == '' or latitude == None:
        latitude = 0
    if longitude == '' or longitude == None:
        longitude = 0

    lat_long = str(latitude) + ',' + str(longitude)


    visit_date = current_date
    visit_datetime = date_fixed
    firstDate = first_currentDate
    depot_name = ''
    client_name = ''
    
    route_name = ''

#    return market_info
#    return merchandizing


    compRow = db((db.sm_company_settings.cid == cid) & (db.sm_company_settings.status == 'ACTIVE')).select(db.sm_company_settings.cid, limitby=(0, 1))
    if not compRow:
        return 'FAILED<SYNCDATA>Invalid Company'
    else:
        repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.sync_code == synccode) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.rep_id, db.sm_rep.name, db.sm_rep.mobile_no, db.sm_rep.user_type, db.sm_rep.level_id, db.sm_rep.depot_id, limitby=(0, 1))
#         return db._lastsql
        depotID = ''
        if not repRow:
           return 'FAILED<SYNCDATA>Invalid Authorization'
        else:
            rep_name = repRow[0].name
            mobile_no = repRow[0].mobile_no
            user_type = repRow[0].user_type
            
#            depotID = repRow[0].depot_id


            errorFlag = 0
            dblSep = '..'
            myStrList = msg.split(dblSep, msg.count(dblSep))
            proposedPart = str(myStrList[0]).strip().upper()
            giftPart = str(myStrList[1]).strip().upper()
            samplePart = str(myStrList[2]).strip().upper()
            notesPart = str(myStrList[3]).strip().upper()
            ppmPart = str(myStrList[4]).strip().upper()
#            return ppmPart

            doctorID = ''
            docName = ''
            areaID=''
            
            typeValue = visit_type
            doctorID = client_id






            doctorRows = db((db.sm_doctor.cid == cid) & (db.sm_doctor.doc_id == doctorID) & (db.sm_doctor.status == 'ACTIVE')).select(db.sm_doctor.doc_name, limitby=(0, 1))
            if not doctorRows:
                errorFlag = 1
                errorMsg = 'Invalid doctor'
            else:
                docName = doctorRows[0].doc_name


            settRows = db((db.sm_settings.cid == cid) & (db.sm_settings.s_key == 'DOCTOR_ROUTE_CHECK') & (db.sm_settings.s_value == 'YES')).select(db.sm_settings.s_value, limitby=(0, 1))
            tracking_table_latlong=""
            if settRows:
                docRouteRows = db((db.sm_doctor_area.cid == cid) & (db.sm_doctor_area.doc_id == doctorID) & (db.sm_doctor_area.area_id == routeID)).select(db.sm_doctor_area.area_id, db.sm_doctor_area.depot_id, db.sm_doctor_area.area_name, db.sm_doctor_area.field1, limitby=(0, 1))
                if not docRouteRows:
                    errorFlag = 1
                    errorMsg = 'Invalid route for the doctor'
                else:
                    routeID = docRouteRows[0].area_id
                    depotID = docRouteRows[0].depot_id
                    areaID = docRouteRows[0].area_id
                    tracking_table_latlong = docRouteRows[0].field1
            
            if (tracking_table_latlong==""):
                tracking_table_latlong='0,0'
            
            depotName=''
            if (depotID!=''):
                depotRows = db((db.sm_depot.cid == cid) & (db.sm_depot.depot_id == depotID) ).select(db.sm_depot.name, limitby=(0, 1))
                if depotRows:
                    depotName = depotRows[0].name
            
            routeName=''
            if (routeID!=''):
                routeRows = db((db.sm_level.cid == cid) & (db.sm_level.level_id == areaID) ).select(db.sm_level.level_name, limitby=(0, 1))
                if routeRows:
                    routeName = routeRows[0].level_name
#            return routeName






#    return errorFlag  
     #----- proposed part
#    return proposedPart
    proposedStr = ''
    if errorFlag == 0:
        if proposedPart != '':
            itemRows = db(db.sm_item.cid == cid).select(db.sm_item.item_id, db.sm_item.name, db.sm_item.category_id, orderby=db.sm_item.item_id)
            propItemList = proposedPart.split(',')
            for i in range(len(propItemList)):
                itemID = str(propItemList[i]).strip()
                validItemId = False
                if (itemID !=''):
                    for itemRow in itemRows:
                        itemId = str(itemRow.item_id).strip()
                        itemName = itemRow.name
                        if itemId == itemID:
                            validItemId = True
                            break
                    if validItemId == False:
    #                    return itemID
                        itemRows = ''
                        errorFlag = 1
                        errorMsg = 'Invalid Item ID %s' % (itemID)
                        break
                    else:
                        if proposedStr == '':
                            proposedStr = itemID + ',' + str(itemName).replace(',', ' ')
                        else:
                            proposedStr += 'fdsep' + itemID + ',' + str(itemName).replace(',', ' ')
            itemRows = ''
    #------------- gift part
    
#    return errorFlag
    giftStr = ''
    if errorFlag == 0:
#        return giftPart
        if giftPart != '':
            giftRows = db((db.sm_doctor_gift.cid == cid)).select(db.sm_doctor_gift.gift_id, db.sm_doctor_gift.gift_name)
#            return db._lastsql
            giftList = giftPart.split('.')
            
            for i in range(len(giftList)):
                gftIdQty = str(giftList[i]).strip()
                gftIdList = gftIdQty.split(',')
                if len(gftIdList) != 2:
                    giftRows = ''
                    errorFlag = 1
                    errorMsg = 'Invalid gift,quantity '
                    break
                else:
                    gftID = str(gftIdList[0]).strip()
                    validGift = False
                    for gftRow in giftRows:
                        giftId = str(gftRow.gift_id).strip()
                        giftName = gftRow.gift_name
                        if giftId == gftID:
                            validGift = True
                            break
#                    return validGift
                    if validGift == False:
                        giftRows = ''
                        errorFlag = 1
                        errorMsg = 'Invalid gift ID %s' % (gftID)
                        break
                    else:
                        gftQty = gftIdList[1]
                        if gftQty.isdigit():
                            pass
                        else:
                            giftRows = ''
                            errorFlag = 1
                            errorMsg = 'Invalid quantity for gift ID %s' % (gftID)
                            break

                        if giftStr == '':
                            giftStr = gftID + ',' + str(giftName).replace(',', ' ') + ',' + str(gftQty)
                        else:
                            giftStr += 'fdsep' + gftID + ',' + str(giftName).replace(',', ' ') + ',' + str(gftQty)
#                        return giftStr
            giftRows = ''
    
    
    #----- ppm part start
#    return errorFlag
    ppmStr = ''
    if errorFlag == 0:
#                 return giftPart
        if ppmPart != '':
            ppmRows = db((db.sm_doctor_ppm.cid == cid)).select(db.sm_doctor_ppm.gift_id, db.sm_doctor_ppm.gift_name)
            ppmList = ppmPart.split('.')
            for i in range(len(ppmList)):
                ppmIdQty = str(ppmList[i]).strip()
                ppmIdList = ppmIdQty.split(',')
                if len(ppmIdList) != 2:
                    ppmRows = ''
                    errorFlag = 1
                    errorMsg = 'Invalid ppm,quantity format in SMS'
                    break
                else:
                    ppmID = str(ppmIdList[0]).strip()
                    validppm = False
                    for ppmRow in ppmRows:
                        ppmId = str(ppmRow.gift_id).strip()
                        ppmName = ppmRow.gift_name
                        if ppmId == ppmID:
                            validppm = True
                            break
                    if validppm == False:
                        ppmRows = ''
                        errorFlag = 1
                        errorMsg = 'Invalid ppm ID %s' % (ppmID)
                        break
                    else:
                        ppmQty = ppmIdList[1]
                        if ppmQty.isdigit():
                            pass
                        else:
                            ppmRows = ''
                            errorFlag = 1
                            errorMsg = 'Invalid quantity for ppm ID %s' % (ppmID)
                            break

                        if ppmStr == '':
                            ppmStr = ppmID + ',' + str(ppmName).replace(',', ' ') + ',' + str(ppmQty)
                        else:
                            ppmStr += 'fdsep' + ppmID + ',' + str(ppmName).replace(',', ' ') + ',' + str(ppmQty)
#                     return giftStr
            ppmRows = ''
    
#    -------------Sample part end
    
    
    #----- sample part
    
    
    
#    return errorFlag
    sampleStr = ''
    if errorFlag == 0:
        if samplePart != '':
            sampleRows = db(db.sm_item.cid == cid).select(db.sm_item.item_id, db.sm_item.name, db.sm_item.category_id, orderby=db.sm_item.item_id)
            sampleList = samplePart.split('.')
            for i in range(len(sampleList)):
                smpIdQty = str(sampleList[i]).strip()
                smpIdList = smpIdQty.split(',')
                if len(smpIdList) != 2:
                    sampleRows = ''
                    errorFlag = 1
                    errorMsg = 'Invalid sample,quantity format in SMS'
                    break
                else:
                    smpID = str(smpIdList[0]).strip()
                    validSample = False
                    for smpRow in sampleRows:
                        smpId = str(smpRow.item_id).strip()
                        smpName = smpRow.name
                        if smpId == smpID:
                            validSample = True
                            break

                    if validSample == False:
                        sampleRows = ''
                        errorFlag = 1
                        errorMsg = 'Invalid sample ID %s' % (smpID)
                        break
                    else:
                        smpQty = smpIdList[1]
                        if smpQty.isdigit():
                            pass
                        else:
                            sampleRows = ''
                            errorFlag = 1
                            errorMsg = 'Invalid quantity for sample ID %s' % (smpID)
                            break

                        if sampleStr == '':
                            sampleStr = smpID + ',' + str(smpName).replace(',', ' ') + ',' + str(smpQty)
                        else:
                            sampleStr += 'fdsep' + smpID + ',' + str(smpName).replace(',', ' ') + ',' + str(smpQty)
            sampleRows = ''





                   #=================Get sl for inbox
#    return errorFlag
    if errorFlag == 0:
        sl_inbox = 0
        rows_check = db(db.sm_doctor_inbox.cid == cid).select(db.sm_doctor_inbox.sl, orderby= ~db.sm_doctor_inbox.sl, limitby=(0, 1))
        if rows_check:
            last_sl = int(rows_check[0].sl)
            sl_inbox = last_sl + 1
        else:
            sl_inbox = 1

        if (proposedStr == '' and giftStr == '' and sampleStr == ''):
            itemngiftnsample = ''
        else:
            itemngiftnsample = proposedStr + 'rdsep' + giftStr + 'rdsep' + sampleStr+ 'rdsep' + ppmStr

    #             return giftStr
        insRes = db.sm_doctor_visit.insert(cid=cid, doc_id=doctorID, doc_name=docName, rep_id=rep_id, rep_name=rep_name, feedback=notesPart, ho_status='0', route_id=routeID, depot_id=depotID, visit_dtime=datetime_fixed, visit_date=current_date, giftnsample=itemngiftnsample,latitude = latitude, longitude = longitude, note=v_with)
        
        
        
        lat_long=str(latitude)+','+str(longitude)
        if (tracking_table_latlong=="0,0"):
            insRes =db((db.sm_doctor_area.cid == cid) & (db.sm_doctor_area.doc_id == doctorID) & (db.sm_doctor_area.area_id == areaID)).update(field1=lat_long)
        
#        return depotName
        insertTracking = db.sm_tracking_table.insert(cid=cid, depot_id=depotID, depot_name=depotName, sl="0", rep_id=rep_id, rep_name=rep_name,call_type='DCR',  visited_id=doctorID, visited_name=docName, visit_date=current_date, visit_time=datetime_fixed,  area_id=routeID, area_name=routeName, visit_type=visit_type, visited_latlong=lat_long, actual_latlong=tracking_table_latlong) 
        
        return 'SUCCESS<SYNCDATA>'
# ========================Doctor End================

#==================Report Start================
#http://127.0.0.1:8000/mrepnovelta/syncmobile_ofline_ppm_02012015/s_call_order_summary?
#cid=NOVELTA&rep_id=1001&rep_pass=123&synccode=8201&rep_id_report=1001&se_item_report=XCS2&se_market_report=DG022&date_from=2015-02-09&date_to=2015-02-09
def s_call_order_summary():
    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.rep_pass).strip()
    synccode = str(request.vars.synccode).strip()
    
    rep_id_report = str(request.vars.rep_id_report).strip().upper()
    se_item_report = str(request.vars.se_item_report).strip().upper()
    se_market_report = str(request.vars.se_market_report).strip().upper()
    
    
    date_from = str(request.vars.date_from).strip().upper()
    date_to = str(request.vars.date_to).strip().upper()
    
    user_type = str(request.vars.user_type).strip().upper()
    
    if (date_from==''):
        date_from=current_date
    if (date_to==''):
        now = datetime.datetime.strptime(current_date, "%Y-%m-%d")
        date_to=now + datetime.timedelta(days = 1)
        
    if (date_from==date_from):
        now = datetime.datetime.strptime(date_from, "%Y-%m-%d")
        date_to=now + datetime.timedelta(days = 1)
        
        
    
    repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.sync_code == synccode) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.ALL, limitby=(0, 1))

#   return db._lastsql
    if not repRow:
       retStatus = 'FAILED<SYNCDATA>Invalid Authorization'
       return retStatus
    else:
       pass
    if (user_type == 'SUP'):
        level_rep = repRow[0].level_id
#        level_id = repRow[0].level_id
        depth = repRow[0].field2
        level = 'level' + str(depth)
    
    report_string=""
    
    
    
    
    if (user_type=='REP'):
        #    Sales Call====================
        qset=db()
        qset=qset((db.sm_order_head.cid == cid) & (db.sm_order_head.rep_id == rep_id))
        qset=qset((db.sm_order_head.order_date >= date_from) & (db.sm_order_head.order_date  < date_to))
        
        if (se_market_report!="ALL"):        
           qset=qset(db.sm_order_head.area_id==se_market_report)
        records=qset.select(db.sm_order_head.sl.count())
    #    report_string=str(records)
        if records:
            sales_call=records[0][db.sm_order_head.sl.count()]
        
        report_string=str(sales_call)
        
        
         
        #  Order Count  
        qset_oc=db()
        qset_oc=qset_oc((db.sm_order_head.cid == cid) & (db.sm_order_head.rep_id == rep_id) & (db.sm_order_head.field1 == 'ORDER')) 
        qset_oc=qset_oc((db.sm_order_head.order_date >= date_from) & (db.sm_order_head.order_date  < date_to))
        
        if (se_market_report!="ALL"):        
           qset_oc=qset_oc(db.sm_order_head.area_id==se_market_report)
        records_oc=qset_oc.select(db.sm_order_head.sl.count())
#        return db._lastsql
        if records_oc:
            order_count=records_oc[0][db.sm_order_head.sl.count()]
        
        

        
        
        
    
    
    #  Order Value  
        condition=""
        if (se_market_report!="ALL"):        
           condition="and (db.sm_order.area_id=="+ str(se_market_report) +") "

#        records_ov=qset_ov.select(db.sm_order.price.sum(),db.sm_order.area_id,db.sm_order.area_name, groupby=db.sm_order.area_id)
        records_ov=[]
        sql_str="SELECT SUM((sm_order.price) * (sm_order.quantity)) as totalprice, sm_order.area_id as area_id, sm_order.area_name as area_name FROM sm_order WHERE (((sm_order.cid = '"+ str(cid) +"') AND (sm_order.rep_id = '"+ str(rep_id) +"')) AND ((sm_order.order_date >= '"+ str(date_from) +"') AND (sm_order.order_date < '"+ str(date_to) +"') "+ condition + ")) GROUP BY sm_order.area_id;"
        records_ov=db.executesql(sql_str,as_dict = True)
#        return db._lastsql
        order_value='0.0'
        areawise_flag=0
        areawise_str=""
#        for records_ov in records_ov:  
        for i in range(len(records_ov)): 
            records_ov_dict=records_ov[i]        
            if (areawise_flag==0):
                    repwise_str='Area wise: </br>'
                    areawise_flag=1
            
#            areawise_str=areawise_str+'Route: '+str(records_ov[db.sm_order.area_name])+'('+str(records_ov[db.sm_order.area_id])+') --'+str(records_ov[db.sm_order.price.sum()])+'</br>'
            areawise_str=areawise_str+'Route: '+str(records_ov_dict["area_name"])+'('+str(records_ov_dict["area_id"])+') --'+str(records_ov_dict["totalprice"])+'</br>'
#        return order_value 
        
        if (sales_call==None):
            sales_call='0'
        if (order_count==None):
            order_count='0'
        if (order_value==None):
            order_value='0.0'
        
        
    #    return db._lastsql
        report_string=str(sales_call)+ '<rd>' +str(order_count)+ '<rd><font style=" font-size:11px"></br>' +str(areawise_str)+'</font>'
    
    
    if (user_type=='SUP'):
        qset_vc=db()
        qset_vc=qset_vc((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '1') & (db.sm_level[level] == level_rep) &     (db.sm_order_head.cid == cid) & (db.sm_order_head.area_id == db.sm_level.level_id ) & (db.sm_order_head.order_datetime >= date_from) & (db.sm_order_head.order_datetime  < date_to)   )          
        
#        return user_type
        
        if (se_market_report!="ALL"):
            qset_vc=qset_vc(db.sm_order_head.area_id == se_market_report)        
        if (rep_id!=rep_id_report):
            qset_vc=qset_vc(db.sm_order_head.rep_id == rep_id_report)

        reportRows_count=qset_vc.select(db.sm_order_head.sl.count())    
        

    
        visit_count='0'
        if reportRows_count:
            visit_count=reportRows_count[0][db.sm_order_head.sl.count()]

        
        
#        =============area wise
        qset_ac=db()
        qset_ac=qset_ac((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '1') & (db.sm_level[level] == level_rep) &     (db.sm_order_head.cid == cid) & (db.sm_order_head.area_id == db.sm_level.level_id ) & (db.sm_order_head.order_datetime >= date_from) & (db.sm_order_head.order_datetime  < date_to)   )
          
        if (se_market_report!="ALL"):
            qset_ac=qset_ac(db.sm_order_head.area_id == se_market_report)        
        if (rep_id!=rep_id_report):
            qset_ac=qset_ac(db.sm_order_head.rep_id == rep_id_report)
  
        reportRows=qset_ac.select(db.sm_order_head.sl.count(),db.sm_order_head.area_id,db.sm_order_head.area_name, groupby = db.sm_order_head.area_id  , orderby=db.sm_order_head.area_id)  
        

        areawise_str=''
        areawise_flag=0
        past_area=''
#        return reportRows
    
        for reportRow in reportRows:
            if (areawise_flag==0):
                areawise_str='</br> Area wise: </br>'
                areawise_flag=1
           
            
            areawise_str=areawise_str+str(reportRow[db.sm_order_head.area_name])+'('+str(reportRow[db.sm_order_head.area_id])+') --'+str(reportRow[db.sm_order_head.sl.count()])+'</br>'
           
#            =============area wise Value
        qset_ac_value=db()
        qset_ac_value=qset_ac_value((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '1') & (db.sm_level[level] == level_rep) &     (db.sm_order.cid == cid) & (db.sm_order.area_id == db.sm_level.level_id ) & (db.sm_order.order_datetime >= date_from) & (db.sm_order.order_datetime  < date_to)   )
          
        if (se_market_report!="ALL"):
            qset_ac_value=qset_ac_value(db.sm_order.area_id == se_market_report)        
        if (rep_id!=rep_id_report):
            qset_ac_value=qset_ac_value(db.sm_order.rep_id == rep_id_report)
  
        reportRows_value=qset_ac.select(db.sm_order.price.sum(),db.sm_order.area_id,db.sm_order.area_name, groupby = db.sm_order.area_id  , orderby=db.sm_order.area_id)  
        

        areawise_v_str=''
        areawise_flag=0
        
    
        for reportRows_value in reportRows_value:
            if (areawise_flag==0):
                areawise_v_str='</br> Area wise: </br>'
                areawise_flag=1
           
            
            areawise_v_str=areawise_v_str+str(reportRows_value[db.sm_order.area_name])+'('+str(reportRows_value[db.sm_order.area_id])+') --'+str(reportRows_value[db.sm_order.price.sum()])+'</br>'
           
#        areawise_str=areawise_str+"</br>"  +areawise_v_str  
            
            
            
#        return areawise_str
#        RepWise=========================
        qset_rc=db()
        qset_rc=qset_rc((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '1') & (db.sm_level[level] == level_rep) &     (db.sm_order_head.cid == cid) & (db.sm_order_head.area_id == db.sm_level.level_id ) & (db.sm_order_head.order_datetime >= date_from) & (db.sm_order_head.order_datetime  < date_to)   )          
        if (se_market_report!="ALL"):
            qset_rc=qset_rc(db.sm_order_head.area_id == se_market_report)        
        if (rep_id!=rep_id_report):
            qset_rc=qset_rc(db.sm_order_head.rep_id == rep_id_report)
#        if (se_item_report!="ALL"):        
#            qset_rc=qset_rc(db.sm_order.item_id==se_item_report)  
            
        repRows=qset_rc.select(db.sm_order_head.sl.count(),db.sm_order_head.rep_id,db.sm_order_head.rep_name, groupby = db.sm_order_head.rep_id  , orderby=db.sm_order_head.rep_id)    
            

        repwise_str=''
        repwise_flag=0
        for repRow in repRows:
            if (repwise_flag==0):
                repwise_str='Rep wise: </br>'
                repwise_flag=1
            
            repwise_str=repwise_str+str(repRow[db.sm_order_head.rep_name])+'('+str(repRow[db.sm_order_head.rep_id])+') --'+str(repRow[db.sm_order_head.sl.count()])+'</br>'
                     

    
#        report_string=str(visit_count)+'</br></br><rd>'+areawise_str+'</br></br><rd>'+repwise_str
        
        
        #        RepWise Value=========================
        qset_rc_value=db()
        qset_rc_value=qset_rc_value((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '1') & (db.sm_level[level] == level_rep) &     (db.sm_order.cid == cid) & (db.sm_order.area_id == db.sm_level.level_id ) & (db.sm_order.order_datetime >= date_from) & (db.sm_order.order_datetime  < date_to)   )          
        if (se_market_report!="ALL"):
            qset_rc_value=qset_rc_value(db.sm_order.area_id == se_market_report)        
        if (rep_id!=rep_id_report):
            qset_rc_value=qset_rc_value(db.sm_order.rep_id == rep_id_report)
#        if (se_item_report!="ALL"):        
#            qset_rc=qset_rc(db.sm_order.item_id==se_item_report)  
            
        repRows_value=qset_rc_value.select(db.sm_order.price.sum(),db.sm_order.rep_id,db.sm_order.rep_name, groupby = db.sm_order.rep_id  , orderby=db.sm_order.rep_id)    
            

        repwise_str_value=''
        repwise_flag=0
        for repRows_value in repRows_value:
            if (repwise_flag==0):
                repwise_str_value='Rep wise: </br>'
                repwise_flag=1
            
            repwise_str_value=repwise_str_value+str(repRows_value[db.sm_order.rep_name])+'('+str(repRows_value[db.sm_order.rep_id])+') --'+str(repRows_value[db.sm_order.price.sum()])+'</br>'
                     
        
        
#        report_string=str(visit_count)+'</br><rd>'+areawise_str+'</br></br><rd>'+repwise_str
        
        report_count_str=areawise_str+"</br>"+repwise_str
        report_value_str=areawise_v_str+"</br>"+repwise_str_value
        
        
    
        report_string=str(visit_count)+'</br></br><rd>'+report_count_str+'</br></br><rd>'+report_value_str
        
    
    return 'SUCCESS<SYNCDATA>'+report_string

def s_call_order_detail():
    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.rep_pass).strip()
    synccode = str(request.vars.synccode).strip()
    
    rep_id_report = str(request.vars.rep_id_report).strip().upper()
    se_item_report = str(request.vars.se_item_report).strip().upper()
    se_market_report = str(request.vars.se_market_report).strip().upper()
    
    
    date_from = str(request.vars.date_from).strip().upper()
    date_to = str(request.vars.date_to).strip().upper()
    
    user_type = str(request.vars.user_type).strip().upper()
    
    date_to=""
    
    if (date_from==''):
        date_from=current_date
    if (date_to==''):
        date_from_check = datetime.datetime.strptime(date_from, "%Y-%m-%d")
        date_to=date_from_check + datetime.timedelta(days = 1)
        
    
    
    repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.sync_code == synccode) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.ALL, limitby=(0, 1))

#   return db._lastsql
    if not repRow:
       retStatus = 'FAILED<SYNCDATA>Invalid Authorization'
       return retStatus
    else:
       pass
    if (user_type == 'SUP'):
        level_rep = repRow[0].level_id
#        level_id = repRow[0].level_id
        depth = repRow[0].field2
        level = 'level' + str(depth)
    
    report_string=""
    
    order_string=""
    visit_count="0"
    report_count_str="0"
    report_value_str="0"
    
    
    if (user_type=='REP'):
        #    Sales Call====================
        qset=db()
        qset=qset((db.sm_order_head.cid == cid) & (db.sm_order_head.rep_id == rep_id))
        qset=qset((db.sm_order_head.order_date >= date_from) & (db.sm_order_head.order_date  < date_to))
        
        if (se_market_report!="ALL"):        
           qset=qset(db.sm_order_head.area_id==se_market_report)
        records=qset.select(db.sm_order_head.sl.count())
    #    report_string=str(records)
        if records:
            sales_call=records[0][db.sm_order_head.sl.count()]
        
        report_string=str(sales_call)
        
        
         
        #  Order Count  
        qset_oc=db()
        qset_oc=qset_oc((db.sm_order_head.cid == cid) & (db.sm_order_head.rep_id == rep_id) & (db.sm_order_head.field1 == 'ORDER')) 
        qset_oc=qset_oc((db.sm_order_head.order_date >= date_from) & (db.sm_order_head.order_date  < date_to))
        
        if (se_market_report!="ALL"):        
           qset_oc=qset_oc(db.sm_order_head.area_id==se_market_report)
        
        records_oc=qset_oc.select(db.sm_order_head.sl.count())
#        return db._lastsql
        if records_oc:
            order_count=records_oc[0][db.sm_order_head.sl.count()]
        
        

        
        
        
    
    
    #  Order Value  
        condition=""
        if (se_market_report!="ALL"):        
           condition="and (db.sm_order.area_id=="+ str(se_market_report) +") "

#        records_ov=qset_ov.select(db.sm_order.price.sum(),db.sm_order.area_id,db.sm_order.area_name, groupby=db.sm_order.area_id)
        records_ov=[]
        sql_str="SELECT SUM((sm_order.price) * (sm_order.quantity)) as totalprice, sm_order.area_id as area_id, sm_order.area_name as area_name FROM sm_order WHERE (((sm_order.cid = '"+ str(cid) +"') AND (sm_order.rep_id = '"+ str(rep_id) +"')) AND ((sm_order.order_date >= '"+ str(date_from) +"') AND (sm_order.order_date < '"+ str(date_to) +"') "+ condition + ")) GROUP BY sm_order.area_id;"
        records_ov=db.executesql(sql_str,as_dict = True)
#        return db._lastsql
        order_value='0.0'
        areawise_flag=0
        areawise_str=""
#        for records_ov in records_ov:  
        for i in range(len(records_ov)): 
            records_ov_dict=records_ov[i]        
            if (areawise_flag==0):
                    repwise_str='Area wise: </br>'
                    areawise_flag=1
            
#            areawise_str=areawise_str+'Route: '+str(records_ov[db.sm_order.area_name])+'('+str(records_ov[db.sm_order.area_id])+') --'+str(records_ov[db.sm_order.price.sum()])+'</br>'
            areawise_str=areawise_str+'Route: '+str(records_ov_dict["area_name"])+'('+str(records_ov_dict["area_id"])+') --'+str(records_ov_dict["totalprice"])+'</br>'

        
        if (sales_call==None):
            sales_call='0'
        if (order_count==None):
            order_count='0'
        if (order_value==None):
            order_value='0.0'
        
        
    #    return db._lastsql
        report_string=str(sales_call)+ '<rd>' +str(order_count)+ '<rd> <font style=" font-size:11px"></br>' +str(areawise_str)+'</font>'
        
        
        
        
#        ========================================
    
    
    
    
#    Last three order
    
        qset_ol=db()
        qset_ol=qset_ol((db.sm_order_head.cid == cid) & (db.sm_order_head.rep_id == rep_id) & (db.sm_order_head.field1 == 'ORDER')) 
        qset_ol=qset_ol((db.sm_order_head.order_date >= date_from) & (db.sm_order_head.order_date  < date_to))
    #    return se_market_report
        if (se_market_report!="ALL"):        
           qset_ol=qset_ol(db.sm_order_head.area_id==se_market_report) 
        records_ol=qset_ol.select(db.sm_order_head.ALL, orderby=~db.sm_order_head.id, limitby=(0,7))
#        return records_ol
     
       
       
#    records_ol=qset_ol.select(db.sm_order_head.ALL, orderby=~db.sm_order_head.id, limitby=(0,3))
#    return records_ol
        order_sl=[]
        
        for record_ol in records_ol:
            order_sl.append(record_ol.sl)
    
         
#        return len(order_sl)
        order_string=''
        start_flag_amount=0
        order_vsl_past='0'
        if (len(order_sl)>0): 
#            return len(order_sl)
            qset_o=db()
            qset_o=qset_o((db.sm_order.cid == cid) & (db.sm_order.rep_id == rep_id) ) 
            qset_o=qset_o((db.sm_order.order_date >= date_from) & (db.sm_order.order_date  < date_to))
            qset_o=qset_o((db.sm_order.sl.belongs(order_sl)))
            
            if (se_market_report!="ALL"):        
                qset_o=qset_o(db.sm_order.area_id==se_market_report) 
            
            records_o=qset_o.select(db.sm_order.ALL, orderby=~db.sm_order.vsl)
#            return db._lastsql
            c=0
            for record_o in records_o:
                c=c+1
                vsl=record_o.vsl
                c_id=record_o.client_id
                c_name=record_o.client_name
                rep_id=record_o.rep_id
                rep_name=record_o.rep_name
                order_datetime=record_o.order_datetime
                
                    
    #         ===========  amount
#                qset_amount=db()
#                qset_amount=qset_amount((db.sm_order.cid == cid) & (db.sm_order.rep_id == rep_id)) 
#                qset_amount=qset_amount((db.sm_order.order_date >= date_from) & (db.sm_order.order_date  < date_to))
#                records_amount=qset_amount.select(db.sm_order.price.sum())
                records_amount=[]
                amount_str="SELECT SUM((sm_order.price) * (sm_order.quantity)) as totalprice FROM sm_order WHERE (((sm_order.cid = '"+ str(cid) +"') AND (sm_order.rep_id = '"+ str(rep_id) +"')) AND ((sm_order.order_date >= '"+ str(date_from) +"') AND (sm_order.order_date < '"+ str(date_to) +"') and  (sm_order.vsl = '"+ str(vsl) + "') "+ "))"                
                records_amount=db.executesql(amount_str,as_dict = True)
                order_amount='0.0'
                for x in range(len(records_amount)): 
                    records_amount_dict=records_amount[x] 
                    order_amount=  str(records_amount_dict["totalprice"])







                
                
#                return db._lastsql
                
#                if records_amount:
#                    order_amount=records_amount[0][db.sm_order.price.sum()]     
                
                if (str(order_vsl_past) != str(vsl)):
#                    start_flag_amount=0
#                    if (start_flag_amount==0):
                    order_string=order_string+ "Visit SL:"+str(vsl)+ " Time:"+str(order_datetime)+"</br>Rep: "+str(rep_name)+" ("+str(rep_id)+")</br>"+str(c_name)+" ("+str(c_id)+" )</br>Order ="+str(order_amount)+"</br>"+"</br>"
#                    else:
#                        order_string=order_string+"</br>"+"Visit SL:"+str(vsl)+ " Time:"+str(order_datetime)
                order_vsl_past=vsl
                
#        return c
        report_string=str(sales_call)+ '<rd>' +str(order_count)+ '<rd><font style=" font-size:11px"></br>' +str(areawise_str)+'</font>'+'<rd>'+str(order_string)
#        return report_string
    
    
    
    if (user_type=='SUP'):
        order_string=""
        report_count_str="0"
        report_value_str="0"
        qset_vc=db()
        qset_vc=qset_vc((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '1') & (db.sm_level[level] == level_rep) &     (db.sm_order_head.cid == cid) & (db.sm_order_head.area_id == db.sm_level.level_id ) & (db.sm_order_head.order_datetime >= date_from) & (db.sm_order_head.order_datetime  < date_to)   )          
        
#        return user_type
        
        if (se_market_report!="ALL"):
            qset_vc=qset_vc(db.sm_order_head.area_id == se_market_report)        
        if (rep_id!=rep_id_report):
            qset_vc=qset_vc(db.sm_order_head.rep_id == rep_id_report)

        reportRows_count=qset_vc.select(db.sm_order_head.sl.count())    
        

    
        visit_count='0'
        if reportRows_count:
            visit_count=reportRows_count[0][db.sm_order_head.sl.count()]

        
        
#        =============area wise
        qset_ac=db()
        qset_ac=qset_ac((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '1') & (db.sm_level[level] == level_rep) &     (db.sm_order_head.cid == cid) & (db.sm_order_head.area_id == db.sm_level.level_id ) & (db.sm_order_head.order_datetime >= date_from) & (db.sm_order_head.order_datetime  < date_to)   )
          
        if (se_market_report!="ALL"):
            qset_ac=qset_ac(db.sm_order_head.area_id == se_market_report)        
        if (rep_id!=rep_id_report):
            qset_ac=qset_ac(db.sm_order_head.rep_id == rep_id_report)
  
        reportRows=qset_ac.select(db.sm_order_head.sl.count(),db.sm_order_head.area_id,db.sm_order_head.area_name, groupby = db.sm_order_head.area_id  , orderby=db.sm_order_head.area_id)  
        

        areawise_str=''
        areawise_flag=0
        past_area=''
#        return reportRows
    
        for reportRow in reportRows:
            if (areawise_flag==0):
                areawise_str='</br> Area wise: </br>'
                areawise_flag=1
           
            
            areawise_str=areawise_str+str(reportRow[db.sm_order_head.area_name])+'('+str(reportRow[db.sm_order_head.area_id])+') --'+str(reportRow[db.sm_order_head.sl.count()])+'</br>'
           
#            =============area wise Value
        qset_ac_value=db()
        qset_ac_value=qset_ac_value((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '1') & (db.sm_level[level] == level_rep) &     (db.sm_order.cid == cid) & (db.sm_order.area_id == db.sm_level.level_id ) & (db.sm_order.order_datetime >= date_from) & (db.sm_order.order_datetime  < date_to)   )
          
        if (se_market_report!="ALL"):
            qset_ac_value=qset_ac_value(db.sm_order.area_id == se_market_report)        
        if (rep_id!=rep_id_report):
            qset_ac_value=qset_ac_value(db.sm_order.rep_id == rep_id_report)
  
        reportRows_value=qset_ac.select(db.sm_order.price.sum(),db.sm_order.area_id,db.sm_order.area_name, groupby = db.sm_order.area_id  , orderby=db.sm_order.area_id)  
        

        areawise_v_str=''
        areawise_flag=0
        
    
        for reportRows_value in reportRows_value:
            if (areawise_flag==0):
                areawise_v_str='</br> Area wise: </br>'
                areawise_flag=1
           
            
            areawise_v_str=areawise_v_str+str(reportRows_value[db.sm_order.area_name])+'('+str(reportRows_value[db.sm_order.area_id])+') --'+str(reportRows_value[db.sm_order.price.sum()])+'</br>'
           
#        areawise_str=areawise_str+"</br>"  +areawise_v_str  
            
            
            
#        return areawise_str
#        RepWise=========================
        qset_rc=db()
        qset_rc=qset_rc((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '1') & (db.sm_level[level] == level_rep) &     (db.sm_order_head.cid == cid) & (db.sm_order_head.area_id == db.sm_level.level_id ) & (db.sm_order_head.order_datetime >= date_from) & (db.sm_order_head.order_datetime  < date_to)   )          
        if (se_market_report!="ALL"):
            qset_rc=qset_rc(db.sm_order_head.area_id == se_market_report)        
        if (rep_id!=rep_id_report):
            qset_rc=qset_rc(db.sm_order_head.rep_id == rep_id_report)
#        if (se_item_report!="ALL"):        
#            qset_rc=qset_rc(db.sm_order.item_id==se_item_report)  
            
        repRows=qset_rc.select(db.sm_order_head.sl.count(),db.sm_order_head.rep_id,db.sm_order_head.rep_name, groupby = db.sm_order_head.rep_id  , orderby=db.sm_order_head.rep_id)    
            

        repwise_str=''
        repwise_flag=0
        for repRow in repRows:
            if (repwise_flag==0):
                repwise_str='Rep wise: </br>'
                repwise_flag=1
            
            repwise_str=repwise_str+str(repRow[db.sm_order_head.rep_name])+'('+str(repRow[db.sm_order_head.rep_id])+') --'+str(repRow[db.sm_order_head.sl.count()])+'</br>'
                     

    
#        report_string=str(visit_count)+'</br></br><rd>'+areawise_str+'</br></br><rd>'+repwise_str
        
        
        #        RepWise Value=========================
        qset_rc_value=db()
        qset_rc_value=qset_rc_value((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '1') & (db.sm_level[level] == level_rep) &     (db.sm_order.cid == cid) & (db.sm_order.area_id == db.sm_level.level_id ) & (db.sm_order.order_datetime >= date_from) & (db.sm_order.order_datetime  < date_to)   )          
        if (se_market_report!="ALL"):
            qset_rc_value=qset_rc_value(db.sm_order.area_id == se_market_report)        
        if (rep_id!=rep_id_report):
            qset_rc_value=qset_rc_value(db.sm_order.rep_id == rep_id_report)
#        if (se_item_report!="ALL"):        
#            qset_rc=qset_rc(db.sm_order.item_id==se_item_report)  
            
        repRows_value=qset_rc_value.select(db.sm_order.price.sum(),db.sm_order.rep_id,db.sm_order.rep_name, groupby = db.sm_order.rep_id  , orderby=db.sm_order.rep_id)    
            

        repwise_str_value=''
        repwise_flag=0
        for repRows_value in repRows_value:
            if (repwise_flag==0):
                repwise_str_value='Rep wise: </br>'
                repwise_flag=1
            
            repwise_str_value=repwise_str_value+str(repRows_value[db.sm_order.rep_name])+'('+str(repRows_value[db.sm_order.rep_id])+') --'+str(repRows_value[db.sm_order.price.sum()])+'</br>'
                     
        
        
#        report_string=str(visit_count)+'</br><rd>'+areawise_str+'</br></br><rd>'+repwise_str
        
        report_count_str=areawise_str+"</br>"+repwise_str
        report_value_str=areawise_v_str+"</br>"+repwise_str_value
        
        
    
        report_string=str(visit_count)+'</br></br><rd>'+report_count_str+'</br></br><rd>'+report_value_str
    
#        return report_string
        #        ========================================
    
    
    
    
#    Last three order
    
        qset_ol=db()
        qset_ol=qset_ol((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '1') & (db.sm_level[level] == level_rep) &     (db.sm_order_head.cid == cid) & (db.sm_order_head.area_id == db.sm_level.level_id ) & (db.sm_order_head.order_datetime >= date_from) & (db.sm_order_head.order_datetime  < date_to) & (db.sm_order_head.field1 == 'ORDER')  )          
        if (se_market_report!="ALL"):
            qset_rc=qset_ol(db.sm_order_head.area_id == se_market_report)        
        if (rep_id!=rep_id_report):
            qset_ol=qset_ol(db.sm_order_head.rep_id == rep_id_report)
            
        records_ol=qset_ol.select(db.sm_order_head.ALL, orderby=~db.sm_order_head.id, limitby=(0,7))
#        return records_ol
     
       
       
#    records_ol=qset_ol.select(db.sm_order_head.ALL, orderby=~db.sm_order_head.id, limitby=(0,3))
#        return records_ol
        order_sl=[]
        
        for record_ol in records_ol:
            order_sl.append(record_ol.sl)
    
         
#        return len(order_sl)
        order_string=''
        start_flag_amount=0
        ordeer_vsl_past='0'
        if (len(order_sl)>0): 
#            return len(order_sl)
            qset_o=db()
            qset_o=qset_o((db.sm_order.cid == cid) & (db.sm_order.rep_id == rep_id) ) 
            qset_o=qset_o((db.sm_order.order_date >= date_from) & (db.sm_order.order_date  < date_to))
            qset_o=qset_o((db.sm_order.sl.belongs(order_sl)))
            
            if (se_market_report!="ALL"):        
                qset_o=qset_o(db.sm_order.area_id==se_market_report) 
#            return rep_id
            if (rep_id!=rep_id_report):
                qset_o=qset_o(db.sm_order.rep_id == rep_id_report)
            
            records_o=qset_ol.select(db.sm_order.ALL, orderby=~db.sm_order.vsl)
#            return db._lastsql
           
            for record_o in records_o:
                vsl=record_o.vsl
                c_id=record_o.client_id
                c_name=record_o.client_name
                order_datetime=record_o.order_datetime
                
                    
    #         ===========  amount
                qset_amount=db()
                qset_amount=qset_amount((db.sm_order.cid == cid) & (db.sm_order.vsl == vsl)) 
                qset_amount=qset_amount((db.sm_order.order_date >= date_from) & (db.sm_order.order_date  < date_to))
                records_amount=qset_amount.select(db.sm_order.price.sum())
#                return db._lastsql
#                return records_amount
                order_amount='0.0'
                start_flag_amount=0
                if records_amount:
                    order_amount=records_amount[0][db.sm_order.price.sum()]     
#                    return order_amount
                if (ordeer_vsl_past!=vsl):
                    if (start_flag_amount==0):
                        start_flag_amount=1
                        order_string=order_string+"</br>Visit SL:"+str(vsl)+ " Time:"+str(order_datetime)+"</br>Rep: "+str(rep_name)+" ("+str(rep_id)+")</br>"+str(c_name)+" ("+str(c_id)+" )</br>Order ="+str(order_amount)
                    else:
                        order_string=order_string+"</br>"+"Visit SL:"+str(vsl)+ " Time:"+str(order_datetime)
                ordeer_vsl_past=vsl
#                return ordeer_vsl_past
            report_string=str(report_string)+ '<rd>'+str(order_string)
    return 'SUCCESS<SYNCDATA>'+report_string   


#http://127.0.0.1:8000/mrepnovelta/syncmobile_ofline_ppm_report/report_summary_doctor?cid=NOVELTA&rep_id=test1002&rep_pass=123&synccode=1042&rep_id_report=test1001&se_item_report=&se_market_report=All&date_from=&date_to=
def report_summary_doctor():
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
    
    
    
    if (date_from==''):
        date_from=current_date
    if (date_to==''):
        now = datetime.datetime.strptime(current_date, "%Y-%m-%d")
        date_to=now + datetime.timedelta(days = 1)
        
    
    if (date_from==date_from):
        now = datetime.datetime.strptime(date_from, "%Y-%m-%d")
        date_to=now + datetime.timedelta(days = 1)
    
    
    repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.sync_code == synccode) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.id,db.sm_rep.user_type,db.sm_rep.level_id,db.sm_rep.field2, limitby=(0, 1))

#   return db._lastsql
   
    level_rep=''
    
    if not repRow:
       retStatus = 'FAILED<SYNCDATA>Invalid Authorization'
       return retStatus
    else:
       pass
   
    if (user_type == 'SUP'):
        level_rep = repRow[0].level_id
#        level_id = repRow[0].level_id
        depth = repRow[0].field2
        level = 'level' + str(depth)
       

        
        


    report_string=""
    
        
#  visit Count  
    if (user_type=='REP'):
        qset_vc=db()
        qset_vc=qset_vc((db.sm_doctor_visit.cid == cid) & (db.sm_doctor_visit.rep_id == rep_id) )  
        qset_vc=qset_vc((db.sm_doctor_visit.visit_dtime >= date_from) & (db.sm_doctor_visit.visit_dtime  < date_to))
        
        if (se_market_report!="ALL"):   
            qset_vc=qset_vc((db.sm_doctor_visit.route_id == se_market_report))
        
           
        records_vc=qset_vc.select(db.sm_doctor_visit.doc_id.count())
        visit_count=''
        if records_vc:
            visit_count=records_vc[0][db.sm_doctor_visit.doc_id.count()]
        
        report_string=str(visit_count)+'<rd>'+'<rd>'
            
    if (user_type=='SUP'):
        
        
        qset_vc=db()
        qset_vc=qset_vc((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '1') & (db.sm_level[level] == level_rep) &     (db.sm_doctor_visit.cid == cid) & (db.sm_doctor_visit.route_id == db.sm_level.level_id ) & (db.sm_doctor_visit.visit_dtime >= date_from) & (db.sm_doctor_visit.visit_dtime  < date_to))          
        if (se_market_report!="ALL"):
            qset_vc=qset_vc((db.sm_doctor_visit.route_id == se_market_report))        
        if (rep_id!=rep_id_report):
            qset_vc=qset_vc((db.sm_doctor_visit.rep_id == rep_id_report))
        reportRows_count=qset_vc.select(db.sm_doctor_visit.id.count())    
        
        visit_count=''
        if reportRows_count:
            visit_count=reportRows_count[0][db.sm_doctor_visit.id.count()]
            
        
        
#        =============area wise
        qset_ac=db()
        qset_ac=qset_ac((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '1') & (db.sm_level[level] == level_rep) &     (db.sm_doctor_visit.cid == cid) & (db.sm_doctor_visit.route_id == db.sm_level.level_id ) & (db.sm_doctor_visit.visit_dtime >= date_from) & (db.sm_doctor_visit.visit_dtime  < date_to))          
        if (se_market_report!="ALL"):
            qset_ac=qset_ac((db.sm_doctor_visit.route_id == se_market_report))        
        if (rep_id!=rep_id_report):
            qset_ac=qset_ac((db.sm_doctor_visit.rep_id == rep_id_report))
        reportRows=qset_ac.select(db.sm_doctor_visit.id.count(),db.sm_doctor_visit.route_id,db.sm_level.level_name, groupby = db.sm_doctor_visit.route_id)  
        
        
#        reportRows = db((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '1') & (db.sm_level[level] == level_rep) &     (db.sm_doctor_visit.cid == cid) & (db.sm_doctor_visit.route_id == db.sm_level.level_id ) & (db.sm_doctor_visit.visit_dtime >= date_from) & (db.sm_doctor_visit.visit_dtime  < date_to)).select(db.sm_doctor_visit.id.count(),db.sm_doctor_visit.route_id,db.sm_level.level_name, groupby = db.sm_doctor_visit.route_id)
#        levelRows = db((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '1') & (db.sm_level[level] == level_rep) ).select(db.sm_level.is_leaf)
        areawise_str=''
        areawise_flag=0
        for reportRow in reportRows:
            if (areawise_flag==0):
                areawise_str='Area wise: </br>'
                areawise_flag=1
            areawise_str=areawise_str+'Route: '+str(reportRow[db.sm_level.level_name])+'('+str(reportRow[db.sm_doctor_visit.route_id])+') --'+str(reportRow[db.sm_doctor_visit.id.count()])+'</br>'
           
 
#        RepWise=========================
        qset_rc=db()
        qset_rc=qset_rc((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '1') & (db.sm_level[level] == level_rep) &     (db.sm_doctor_visit.cid == cid) & (db.sm_doctor_visit.route_id == db.sm_level.level_id ) & (db.sm_doctor_visit.visit_dtime >= date_from) & (db.sm_doctor_visit.visit_dtime  < date_to))          
        if (se_market_report!="ALL"):
            qset_rc=qset_rc((db.sm_doctor_visit.route_id == se_market_report))        
        if (rep_id!=rep_id_report):
            qset_rc=qset_rc((db.sm_doctor_visit.rep_id == rep_id_report))
            
        repRows=qset_rc.select(db.sm_doctor_visit.id.count(),db.sm_doctor_visit.rep_id,db.sm_doctor_visit.rep_name, groupby = db.sm_doctor_visit.rep_id)    
            
#        repRows = db((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '1') & (db.sm_level[level] == level_rep) &     (db.sm_doctor_visit.cid == cid) & (db.sm_doctor_visit.route_id == db.sm_level.level_id ) & (db.sm_doctor_visit.visit_dtime >= date_from) & (db.sm_doctor_visit.visit_dtime  < date_to)).select(db.sm_doctor_visit.id.count(),db.sm_doctor_visit.rep_id,db.sm_doctor_visit.rep_name, groupby = db.sm_doctor_visit.rep_id)
        repwise_str=''
        repwise_flag=0
        for repRow in repRows:
            if (repwise_flag==0):
                repwise_str='Rep wise: </br>'
                repwise_flag=1
            
            repwise_str=repwise_str+'Rep: '+str(repRow[db.sm_doctor_visit.rep_name])+'('+str(repRow[db.sm_doctor_visit.rep_id])+') --'+str(repRow[db.sm_doctor_visit.id.count()])+'</br>'
                     
#    return repwise_str
    
        report_string=str(visit_count)+'</br></br><rd>'+areawise_str+'</br></br><rd>'+repwise_str


#
#    return db._lastsql
#    report_string=str(visit_count)+','+areawise_str+','+repwise_str
    
    return 'SUCCESS<SYNCDATA>'+report_string

def report_detail_doctor():
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
    
    date_to=""
    
    if (date_from==''):
        date_from=current_date
    if (date_to==''):
        date_from_check = datetime.datetime.strptime(date_from, "%Y-%m-%d")
        date_to=date_from_check + datetime.timedelta(days = 1)
        
#    return date_to
    
    repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.sync_code == synccode) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.id,db.sm_rep.level_id,db.sm_rep.field2, limitby=(0, 1))

#   return db._lastsql
    if not repRow:
       retStatus = 'FAILED<SYNCDATA>Invalid Authorization'
       return retStatus
    else:
       pass
    if (user_type == 'SUP'):
        level_rep = repRow[0].level_id
#        level_id = repRow[0].level_id
        depth = repRow[0].field2
        level = 'level' + str(depth)
    
    report_string=""
    
        
#  visit Count  
    if (user_type=='REP'):
        qset_vc=db()
        qset_vc=qset_vc((db.sm_doctor_visit.cid == cid) & (db.sm_doctor_visit.rep_id == rep_id) )  
        qset_vc=qset_vc((db.sm_doctor_visit.visit_dtime >= date_from) & (db.sm_doctor_visit.visit_dtime  < date_to))
        
        if (se_market_report!="ALL"):   
            qset_vc=qset_vc((db.sm_doctor_visit.route_id == se_market_report))
        
           
        records_vc=qset_vc.select(db.sm_doctor_visit.doc_id.count())
        visit_count=''
        if records_vc:
            visit_count=records_vc[0][db.sm_doctor_visit.doc_id.count()]
    
    

        report_string=str(visit_count)+ '<rd>' + '<rd>' 
    
    #    Detail===========
        qset_detail=db()
        qset_detail=qset_detail((db.sm_doctor_visit.cid == cid) & (db.sm_doctor_visit.rep_id == rep_id)& (db.sm_doctor_visit.giftnsample != '') )  
        qset_detail=qset_detail((db.sm_doctor_visit.visit_dtime >= date_from) & (db.sm_doctor_visit.visit_dtime  < date_to))
        
        if (se_market_report!="ALL"):   
            qset_detail=qset_detail((db.sm_doctor_visit.route_id == se_market_report))
        records_detail=qset_detail.select(db.sm_doctor_visit.ALL, orderby=~db.sm_doctor_visit.id, limitby=(0,10))
        
    #    return records_detail
    #    return db._lastsql
        
        start_flag=0
        visit_string=''
        for records_detail in records_detail:
    #        return records_detail
            v_id = records_detail.id 
            doc_id = records_detail.doc_id 
            doc_name  =  records_detail.doc_name 
            feedback =  records_detail.feedback
            visit_dtime = records_detail.visit_dtime
            att_string   =  records_detail.giftnsample
    #        return att_string
        
            att_list = att_string.split('rdsep')
    #        return len(att_list)
            for i in range(len(att_list)):
                if (len(att_list)==4):
                    campaign = att_list[0]
                    gift = att_list[1]
                    sample = att_list[2]
                    ppm = att_list[3]
                if (len(att_list)==3):
                    campaign = att_list[0]
                    gift = att_list[1]
                    sample = att_list[2]
        #                ppm = att_list[3]
                if (len(att_list)==2):
                    campaign = att_list[0]
                    gift = att_list[1]
                if (len(att_list)==1):
                    campaign = att_list[0]
                    gift = att_list[1]
                if (len(att_list)==0):
                    campaign = att_list[0]
        #                gift = att_list[1]
        
                    
                
                
                
                
        #            return ppm
            if (campaign!=''):
                campaignList = campaign.split('fdsep')
                start_c_flag=0
                campaign_string=''
    #                return len(campaignList)
                for x in range(len(campaignList)):
                    campaign_singleList=campaignList[x].split(',')
                    if (start_c_flag==0):
                        campaign_string=str(campaign_singleList[1])+" ("+str(campaign_singleList[0])+")"
                        start_c_flag=1
                    else:
                        campaign_string=campaign_string+', '+str(campaign_singleList[1])+" ("+str(campaign_singleList[0])+")"
    #            return campaign_string
    #        return gift
            gift_string=''
            if (gift!=''):
                giftList = gift.split('fdsep')
                start_g_flag=0
                gift_string=''
                for g in range(len(giftList)):
                    gift_singleList=giftList[g].split(',')
                    if (start_g_flag==0):
                        gift_string=str(gift_singleList[1])+" ("+str(gift_singleList[0])+") - "+str(gift_singleList[2])
                        start_g_flag=1
    #                        return gift_string
                    else:
                        gift_string=gift_string + ', '+str(gift_singleList[1])+" ("+str(gift_singleList[0])+") - "+str(gift_singleList[2])
                        
    #                return gift_string
            ppm_string=''
            if (ppm!=''):
                    ppmList = ppm.split('fdsep')
                    start_p_flag=0
                    ppm_string=''
                    
                    for p in range(len(ppmList)):
                        ppm_singleList=ppmList[p].split(',')
                        if (start_p_flag==0):
                            ppm_string=str(ppm_singleList[1])+" ("+str(ppm_singleList[0])+") - "+str(ppm_singleList[2]) 
                            start_p_flag=1
    #                        return gift_string
                        else:
                            ppm_string=ppm_string + ', '+str(ppm_singleList[1])+" ("+str(ppm_singleList[0])+") - "+str(ppm_singleList[2]) 
                            
            sample_string=''
            if (sample!=''):
                    sampleList = sample.split('fdsep')
                    start_s_flag=0
                    sample_string=''
                    for s in range(len(sampleList)):
                        sample_singleList=sampleList[s].split(',')
                        if (start_s_flag==0):
                            sample_string=str(sample_singleList[1])+" ("+str(sample_singleList[0])+") - "+str(sample_singleList[2])  
                            start_s_flag=1
    #                        return gift_string
                        else:
                            sample_string=sample_string + ', '+str(sample_singleList[1])+" ("+str(sample_singleList[0])+") - "+str(sample_singleList[2])  
                    
    #            return ppm_string
        
        
            if (start_flag==0):
                visit_string = "Visit SL:"+str(v_id)+ " Time:"+str(visit_dtime)+"</br>"+str(doc_name)+" ("+str(doc_id)+" )"
                if (campaign_string!=''):
                    visit_string=visit_string+"</br>Product: "+str(campaign_string)
                if (sample_string!=''):
                    visit_string=visit_string+"</br>Sample: "+str(sample_string)
                if (gift_string!=''):
                    visit_string=visit_string+"</br>Gift: "+str(gift_string)
                if (ppm_string!=''):
                    visit_string=visit_string+"</br>PPM: "+str(ppm_string)
                if (feedback!=''):
                    visit_string=visit_string+"</br>Feedback: "+str(feedback)
                    
                    
    
                start_flag=1
            else:
                visit_string = visit_string+"</br></br>"+"Visit SL:"+str(v_id)+ " Time:"+str(visit_dtime)+"</br>"+str(doc_name)+" ("+str(doc_id)+" )"
                if (campaign_string!=''):
                    visit_string=visit_string+"</br>Product: "+str(campaign_string)
                if (sample_string!=''):
                    visit_string=visit_string+"</br>Sample: "+str(sample_string)
                if (gift_string!=''):
                    visit_string=visit_string+"</br>Gift: "+str(gift_string)
                if (ppm_string!=''):
                    visit_string=visit_string+"</br>PPM: "+str(ppm_string)
                if (feedback!=''):
                    visit_string=visit_string+"</br>Feedback: "+str(feedback)
                     
        report_string=str(report_string)+'<rd>'+str(visit_string)
        
        

    if (user_type=='SUP'): 
        qset_vc=db()
        qset_vc=qset_vc((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '1') & (db.sm_level[level] == level_rep) &     (db.sm_doctor_visit.cid == cid) & (db.sm_doctor_visit.route_id == db.sm_level.level_id ) & (db.sm_doctor_visit.visit_dtime >= date_from) & (db.sm_doctor_visit.visit_dtime  < date_to))          
        if (se_market_report!="ALL"):
            qset_vc=qset_vc((db.sm_doctor_visit.route_id == se_market_report))        
        if (rep_id!=rep_id_report):
            qset_vc=qset_vc((db.sm_doctor_visit.rep_id == rep_id_report))
        reportRows_count=qset_vc.select(db.sm_doctor_visit.id.count())    
        
        visit_count=''
        if reportRows_count:
            visit_count=reportRows_count[0][db.sm_doctor_visit.id.count()]
            
        
        
#        =============area wise
        qset_ac=db()
        qset_ac=qset_ac((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '1') & (db.sm_level[level] == level_rep) &     (db.sm_doctor_visit.cid == cid) & (db.sm_doctor_visit.route_id == db.sm_level.level_id ) & (db.sm_doctor_visit.visit_dtime >= date_from) & (db.sm_doctor_visit.visit_dtime  < date_to))          
        if (se_market_report!="ALL"):
            qset_ac=qset_ac((db.sm_doctor_visit.route_id == se_market_report))        
        if (rep_id!=rep_id_report):
            qset_ac=qset_ac((db.sm_doctor_visit.rep_id == rep_id_report))
        reportRows=qset_ac.select(db.sm_doctor_visit.id.count(),db.sm_doctor_visit.route_id,db.sm_level.level_name, groupby = db.sm_doctor_visit.route_id)  
        
        
#        reportRows = db((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '1') & (db.sm_level[level] == level_rep) &     (db.sm_doctor_visit.cid == cid) & (db.sm_doctor_visit.route_id == db.sm_level.level_id ) & (db.sm_doctor_visit.visit_dtime >= date_from) & (db.sm_doctor_visit.visit_dtime  < date_to)).select(db.sm_doctor_visit.id.count(),db.sm_doctor_visit.route_id,db.sm_level.level_name, groupby = db.sm_doctor_visit.route_id)
#        levelRows = db((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '1') & (db.sm_level[level] == level_rep) ).select(db.sm_level.is_leaf)
        areawise_str=''
        areawise_flag=0
        for reportRow in reportRows:
            if (areawise_flag==0):
                areawise_str='Area wise: </br>'
                areawise_flag=1
            areawise_str=areawise_str+'Route: '+str(reportRow[db.sm_level.level_name])+'('+str(reportRow[db.sm_doctor_visit.route_id])+') --'+str(reportRow[db.sm_doctor_visit.id.count()])+'</br>'
           
 
#        RepWise=========================
        qset_rc=db()
        qset_rc=qset_rc((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '1') & (db.sm_level[level] == level_rep) &     (db.sm_doctor_visit.cid == cid) & (db.sm_doctor_visit.route_id == db.sm_level.level_id ) & (db.sm_doctor_visit.visit_dtime >= date_from) & (db.sm_doctor_visit.visit_dtime  < date_to))          
        if (se_market_report!="ALL"):
            qset_rc=qset_rc((db.sm_doctor_visit.route_id == se_market_report))        
        if (rep_id!=rep_id_report):
            qset_rc=qset_rc((db.sm_doctor_visit.rep_id == rep_id_report))
            
        repRows=qset_rc.select(db.sm_doctor_visit.id.count(),db.sm_doctor_visit.rep_id,db.sm_doctor_visit.rep_name, groupby = db.sm_doctor_visit.rep_id)    
            
#        repRows = db((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '1') & (db.sm_level[level] == level_rep) &     (db.sm_doctor_visit.cid == cid) & (db.sm_doctor_visit.route_id == db.sm_level.level_id ) & (db.sm_doctor_visit.visit_dtime >= date_from) & (db.sm_doctor_visit.visit_dtime  < date_to)).select(db.sm_doctor_visit.id.count(),db.sm_doctor_visit.rep_id,db.sm_doctor_visit.rep_name, groupby = db.sm_doctor_visit.rep_id)
        repwise_str=''
        repwise_flag=0
        for repRow in repRows:
            if (repwise_flag==0):
                repwise_str='Rep wise: </br>'
                repwise_flag=1
            
            repwise_str=repwise_str+'Rep: '+str(repRow[db.sm_doctor_visit.rep_name])+'('+str(repRow[db.sm_doctor_visit.rep_id])+') --'+str(repRow[db.sm_doctor_visit.id.count()])+'</br>'
                     
#    return repwise_str
    
        report_string=str(visit_count)+'</br></br><rd>'+areawise_str+'</br></br><rd>'+repwise_str   
        
        
#    Detail===========
        qset_detail=db()
        qset_detail=qset_detail((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '1') & (db.sm_level[level] == level_rep) &     (db.sm_doctor_visit.cid == cid) & (db.sm_doctor_visit.route_id == db.sm_level.level_id ) & (db.sm_doctor_visit.visit_dtime >= date_from) & (db.sm_doctor_visit.visit_dtime  < date_to))  
       
        
        if (se_market_report!="ALL"):   
            qset_detail=qset_detail((db.sm_doctor_visit.route_id == se_market_report))
        if (rep_id!=rep_id_report):
            qset_detail=qset_detail((db.sm_doctor_visit.rep_id == rep_id_report))
        records_detail=qset_detail.select(db.sm_doctor_visit.ALL, orderby=~db.sm_doctor_visit.id, limitby=(0,10))
        
#        return records_detail
#        return db._lastsql
        
        start_flag=0
        visit_string=''
        for records_detail in records_detail:
    #        return records_detail
            v_id = records_detail.id 
            rep_id = records_detail.rep_id 
            rep_name = records_detail.rep_name 
            doc_id = records_detail.doc_id 
            doc_name  =  records_detail.doc_name 
            feedback =  records_detail.feedback
            visit_dtime = records_detail.visit_dtime
            att_string   =  records_detail.giftnsample
    #        return att_string
        
            att_list = att_string.split('rdsep')
    #        return len(att_list)
            for i in range(len(att_list)):
                if (len(att_list)==4):
                    campaign = att_list[0]
                    gift = att_list[1]
                    sample = att_list[2]
                    ppm = att_list[3]
                if (len(att_list)==3):
                    campaign = att_list[0]
                    gift = att_list[1]
                    sample = att_list[2]
        #                ppm = att_list[3]
                if (len(att_list)==2):
                    campaign = att_list[0]
                    gift = att_list[1]
                if (len(att_list)==1):
                    campaign = att_list[0]
                    gift = att_list[1]
                if (len(att_list)==0):
                    campaign = att_list[0]
        #                gift = att_list[1]
        
                    
                
                
                
                
        #            return ppm
            if (campaign!=''):
                campaignList = campaign.split('fdsep')
                start_c_flag=0
                campaign_string=''
    #                return len(campaignList)
                for x in range(len(campaignList)):
                    campaign_singleList=campaignList[x].split(',')
                    if (start_c_flag==0):
                        campaign_string=str(campaign_singleList[1])+" ("+str(campaign_singleList[0])+")"
                        start_c_flag=1
                    else:
                        campaign_string=campaign_string+', '+str(campaign_singleList[1])+" ("+str(campaign_singleList[0])+")"
    #            return campaign_string
    #        return gift
            gift_string=''
            if (gift!=''):
                giftList = gift.split('fdsep')
                start_g_flag=0
                gift_string=''
                for g in range(len(giftList)):
                    gift_singleList=giftList[g].split(',')
                    if (start_g_flag==0):
                        gift_string=str(gift_singleList[1])+" ("+str(gift_singleList[0])+") - "+str(gift_singleList[2])
                        start_g_flag=1
    #                        return gift_string
                    else:
                        gift_string=gift_string + ', '+str(gift_singleList[1])+" ("+str(gift_singleList[0])+") - "+str(gift_singleList[2])
                        
    #                return gift_string
            ppm_string=''
            if (ppm!=''):
                    ppmList = ppm.split('fdsep')
                    start_p_flag=0
                    ppm_string=''
                    
                    for p in range(len(ppmList)):
                        ppm_singleList=ppmList[p].split(',')
                        if (start_p_flag==0):
                            ppm_string=str(ppm_singleList[1])+" ("+str(ppm_singleList[0])+") - "+str(ppm_singleList[2]) 
                            start_p_flag=1
    #                        return gift_string
                        else:
                            ppm_string=ppm_string + ', '+str(ppm_singleList[1])+" ("+str(ppm_singleList[0])+") - "+str(ppm_singleList[2]) 
                            
            sample_string=''
            if (sample!=''):
                    sampleList = sample.split('fdsep')
                    start_s_flag=0
                    sample_string=''
                    for s in range(len(sampleList)):
                        sample_singleList=sampleList[s].split(',')
                        if (start_s_flag==0):
                            sample_string=str(sample_singleList[1])+" ("+str(sample_singleList[0])+") - "+str(sample_singleList[2])  
                            start_s_flag=1
    #                        return gift_string
                        else:
                            sample_string=sample_string + ', '+str(sample_singleList[1])+" ("+str(sample_singleList[0])+") - "+str(sample_singleList[2])  
                    
    #            return ppm_string
        
        
            if (start_flag==0):
                visit_string = "Visit SL:"+str(v_id)+ " Time:"+str(visit_dtime)+"</br> Rep:"+str(rep_name)+" ("+str(rep_id)+" )"+"</br>Doctor:"+str(doc_name)+" ("+str(doc_id)+" )"
                if (campaign_string!=''):
                    visit_string=visit_string+"</br>Product: "+str(campaign_string)
                if (sample_string!=''):
                    visit_string=visit_string+"</br>Sample: "+str(sample_string)
                if (gift_string!=''):
                    visit_string=visit_string+"</br>Gift: "+str(gift_string)
                if (ppm_string!=''):
                    visit_string=visit_string+"</br>PPM: "+str(ppm_string)
                if (feedback!=''):
                    visit_string=visit_string+"</br>Feedback: "+str(feedback)
                    
                    
    
                start_flag=1
            else:
                visit_string = visit_string+"</br></br>"+"Visit SL:"+str(v_id)+ " Time:"+str(visit_dtime)+"</br>"+str(doc_name)+" ("+str(doc_id)+" )"
                if (campaign_string!=''):
                    visit_string=visit_string+"</br>Product: "+str(campaign_string)
                if (sample_string!=''):
                    visit_string=visit_string+"</br>Sample: "+str(sample_string)
                if (gift_string!=''):
                    visit_string=visit_string+"</br>Gift: "+str(gift_string)
                if (ppm_string!=''):
                    visit_string=visit_string+"</br>PPM: "+str(ppm_string)
                if (feedback!=''):
                    visit_string=visit_string+"</br>Feedback: "+str(feedback) 
        
        report_string=str(report_string)+'<rd>'+str(visit_string)
    return 'SUCCESS<SYNCDATA>'+report_string 




#==================Report End================


#============================= Test dynamic path
def dmpath():
#    import urllib2
#    cid = str(request.vars.CID).strip().upper()
#    url = 'http://im-gp.com/dmpath/index_bio_off.php?CID=' + cid + '&HTTPPASS=e99business321cba'
#
#    result = ''
#    try:
#        result = urllib2.urlopen(url)
#    except:
#        result = 'Invalid Request'
#    return result


#     cid = str(request.vars.CID).strip().upper()
#     if (cid='BIOPHARMA'):
#          return '<start>http://127.0.0.1:8000/mrepnovelta/syncmobile_ofline_ppm_02012015/<fd>http://127.0.0.1:8000/mrepnovelta/static/<fd>http://127.0.0.1:8000/mrepnovelta/syncmobile_ofline_ppm_02012015/<end>'
#         return '<start>http://e2.businesssolutionapps.com/mrepbiopharma/syncmobile_ofline_ppm_report_test/<fd>http://e2.businesssolutionapps.com/mrepbiopharma/static/<fd>http://e2.businesssolutionapps.com/mrepbiopharma/syncmobile_ofline_ppm_report_test/<end>'
         return '<start>http://127.0.0.1:8000/mrepbiopharma/syncmobile_ofline_ppm_report_test_20/<fd>http://e2.businesssolutionapps.com/mrepbiopharma/static/<fd>http://e2.businesssolutionapps.com/mrepbiopharma/syncmobile_ofline_ppm_report_test/<end>'












