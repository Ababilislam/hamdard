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
                productRows = db(db.sm_company_settings.cid == cid).select(db.sm_company_settings.field1, limitby=(0,1))
                for productRow in productRows:
                    productStr = productRow.field1
                    
                    
#                productRows = db(db.sm_item.cid == cid).select(db.sm_item.item_id, db.sm_item.name, db.sm_item.price, orderby=db.sm_item.name)
#                for productRow in productRows:
#                    item_id = productRow.item_id
#                    name = productRow.name
#                    price = productRow.price
#
#                    if productStr == '':
#                        productStr = str(item_id).upper() + '<fd>' + str(name).upper() + '<fd>' + str(price)
#                    else:
#                        productStr += '<rd>' + str(item_id).upper() + '<fd>' + str(name).upper() + '<fd>' + str(price)
                
                
#                return productStr
                #-------------- Merchandizing list
                merchandizingStr = ''
                #-------------- Dealer list
                dealerStr = ''
#                dealertRows = db((db.sm_depot.cid == cid) & (db.sm_depot.depot_id == depot_id)).select(db.sm_depot.name, limitby=(0, 1))
##                return db._lastsql
#                if dealertRows:
#                    depotName = dealertRows[0].name
#                dealerStr = str(depot_id) + '<fd>' + str(depotName)

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
#                levelRows = db((db.sm_level.cid == cid) & (db.sm_level.depot_id == depot_id)).select(db.sm_level.level0, groupby=db.sm_level.level0, limitby=(0, 1))
#                for levelRow in levelRows:
#                    level0_id = levelRow.level0
#
#                    level0Rows = db((db.sm_level.cid == cid) & (db.sm_level.level_id == level0_id)).select(db.sm_level.level_id, db.sm_level.level_name, limitby=(0, 1))
#                    for level0Row in level0Rows:
#                        level_id = level0Row.level_id
#                        level_name = level0Row.level_name
#
#                        if regionStr == '':
#                            regionStr = str(level_id) + '<fd>' + str(level_name)
#                        else:
#                            regionStr += '<rd>' + str(level_id) + '<fd>' + str(level_name)


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
#                clienttCatRows = db((db.sm_category_type.cid == cid) & (db.sm_category_type.type_name == 'CLIENT_CATEGORY')).select(db.sm_category_type.cat_type_id, orderby=db.sm_category_type.cat_type_id)
##                return db._lastsql
#                c = 0
#                for clienttCatRows in clienttCatRows:
#                    cat_type_id = clienttCatRows.cat_type_id
#
#
#                    if clienttCatStr == '':
#                        clienttCatStr = str(cat_type_id).strip().upper()
#                    else:
#                        clienttCatStr += '<rd>' + str(cat_type_id).strip().upper()
#                    c = c + 1
#                if (c == 1):
#                    clienttCatStr = clienttCatStr + '<rd>'

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
#                return clientStr


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
                doctorRows = db((db.sm_doctor.cid == cid) & (db.sm_doctor.status == 'ACTIVE') & (db.sm_doctor_area.cid == cid) & (db.sm_doctor_area.doc_id == db.sm_doctor.doc_id) & (db.sm_doctor_area.area_id == area_id) ).select(db.sm_doctor.doc_id, db.sm_doctor.doc_name, db.sm_doctor_area.area_id, orderby=db.sm_doctor_area.area_id|db.sm_doctor.doc_name)
#                return db._lastsql
                if not doctorRows:
                    pass
#                    retStatus = 'FAILED<SYNCDATA>Doctor not available'
#                    return retStatus
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
                productRows = db(db.sm_company_settings.cid == cid).select(db.sm_company_settings.field1, limitby=(0,1))
                for productRow in productRows:
                    productStr = productRow.field1
#                productRows = db(db.sm_item.cid == cid).select(db.sm_item.item_id, db.sm_item.name, db.sm_item.price, orderby=db.sm_item.name)
#                for productRow in productRows:
#                    item_id = productRow.item_id
#                    name = productRow.name
#                    price = productRow.price
#
#                    if productStr == '':
#                        productStr = str(item_id) + '<fd>' + str(name) + '<fd>' + str(price)
#                    else:
#                        productStr += '<rd>' + str(item_id) + '<fd>' + str(name) + '<fd>' + str(price)

                #-------------- Merchandizing list
                merchandizingStr = ''
                #-------------- Dealer list
                dealerStr = ''
#                dealertRows = db((db.sm_depot.cid == cid) & (db.sm_depot.depot_id.belongs(depotList))).select(db.sm_depot.depot_id, db.sm_depot.name, orderby=db.sm_depot.name)
#                for dealertRow in dealertRows:
#                    depot_id = dealertRow.depot_id
#                    depotName = dealertRow.name
#
#                    if dealerStr == '':
#                        dealerStr = str(depot_id) + '<fd>' + str(depotName)
#                    else:
#                        dealerStr += '<rd>' + str(depot_id) + '<fd>' + str(depotName)


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
#                levelRows = db((db.sm_level.cid == cid) & (db.sm_level.depth == 0)).select(db.sm_level.level_id, db.sm_level.level_name, orderby=db.sm_level.level_name)
#                for levelRow in levelRows:
#                    level_id = levelRow.level_id
#                    level_name = levelRow.level_name
#
#                    if regionStr == '':
#                        regionStr = str(level_id) + '<fd>' + str(level_name)
#                    else:
#                        regionStr += '<rd>' + str(level_id) + '<fd>' + str(level_name)

               #------------Client Category list

                clienttCatStr = ''
#                clienttCatRows = db((db.sm_category_type.cid == cid) & (db.sm_category_type.type_name == 'CLIENT_CATEGORY')).select(db.sm_category_type.cat_type_id, orderby=db.sm_category_type.cat_type_id)
##                return db._lastsql
#                c = 0
#                for clienttCatRows in clienttCatRows:
#                    cat_type_id = clienttCatRows.cat_type_id
#
#
#                    if clienttCatStr == '':
#                        clienttCatStr = str(cat_type_id).strip().upper()
#                    else:
#                        clienttCatStr += '<rd>' + str(cat_type_id).strip().upper()
#                    c = c + 1
#
#                if (c == 1):
#                    clienttCatStr = clienttCatStr + '<rd>'

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
                doctor_area_past=''
                srart_a_flag=0
                doctorStr_flag=0
                
                for i in range(len(marketList)):
                    area_id = marketList[i]

                    doctorRows = db((db.sm_doctor.cid == cid) & (db.sm_doctor.status == 'ACTIVE') & (db.sm_doctor_area.cid == cid) & (db.sm_doctor_area.doc_id == db.sm_doctor.doc_id) & (db.sm_doctor_area.area_id == marketList[i])).select(db.sm_doctor.doc_id, db.sm_doctor.doc_name, db.sm_doctor_area.area_id, orderby=db.sm_doctor_area.area_id|db.sm_doctor.doc_name)
                    return db._lastsql
                    if not doctorRows:
                        pass
    #                    retStatus = 'FAILED<SYNCDATA>Doctor not available'
    #                    return retStatus
                    else:
                       
                        
                        for doctorRow in doctorRows:
                            doctor_id = doctorRow.sm_doctor.doc_id
                            doctor_name = doctorRow.sm_doctor.doc_name
                            doctor_area = doctorRow.sm_doctor_area.area_id
                            if (doctor_area_past!=doctor_area):
                                
                                if (srart_a_flag==0):
                                    doctorStr=doctorStr+"<"+doctor_area+">"
                                    
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
                clientRows = db((db.sm_client.cid == cid) & (db.sm_client.area_id == market_id) & (db.sm_client.status == 'ACTIVE')).select(db.sm_client.client_id, db.sm_client.name,db.sm_client.market_name,db.sm_client.address ,db.sm_client.category_id, orderby=db.sm_client.name)
            else:
                clientRows = db((db.sm_client.cid == cid) & (db.sm_client.area_id == market_id) & (db.sm_client.status == 'ACTIVE') & (db.sm_client.category_id == client_cat)).select(db.sm_client.client_id, db.sm_client.name,db.sm_client.name,db.sm_client.market_name,db.sm_client.address, db.sm_client.category_id, orderby=db.sm_client.name)
#            return db._lastsql
            if not clientRows:
                retStatus = 'FAILED<SYNCDATA>Retailer not available'
                return retStatus
            else:
                for clientRow in clientRows:
                    client_id = clientRow.client_id
                    name = clientRow.name
                    category_id = clientRow.category_id
                    address=clientRow.address
                    if len(address)>30:
                        address= str(clientRow.address)[30]
                    market_name=address+'-'+str(clientRow.market_name)

                    if clientStr == '':
                        clientStr = str(client_id) + '<fd>' + str(name)+'-' +str(market_name) + '<fd>' + str(category_id)
                    else:
                        clientStr += '<rd>' + str(client_id) + '<fd>' + str(name) +'-' +str(market_name)+ '<fd>' + str(category_id)

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
    
    note = str(request.vars.chemist_feedback).strip() 
    

#    return note
    visit_type = str(request.vars.visit_type).strip()  # scheduled,unscheduled
    sch_date = str(request.vars.schedule_date).strip()


    payment_mode = str(request.vars.payment_mode).strip().upper()
    
    
    delivery_date = str(request.vars.delivery_date).strip()
    collection_date = str(request.vars.collection_date).strip()
    version = str(request.vars.version).strip()
    
    if (version=='p1'):
        try:
            delivery_date = datetime.datetime.strptime(delivery_date, '%Y-%m-%d')
        except:
            try:
                delivery_date = datetime.datetime.strptime(delivery_date, '%d-%m-%Y')
            except:
                return 'FAILED<SYNCDATA>Invalid Delivery Date'
        
        try:
            collection_date = datetime.datetime.strptime(collection_date, '%Y-%m-%d')
    #        return abs((collection_date - current_date).days)
        except:
            try:
                collection_date = datetime.datetime.strptime(collection_date, '%d-%m-%Y')
            except:
                return 'FAILED<SYNCDATA>Invalid Collection Date'
    else:
        collection_date=current_date
        delivery_date=current_date
        
        
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
                levelRecords = db((db.sm_level.cid == cid) & (db.sm_level.level_id == route_id)).select(db.sm_level.level_id, db.sm_level.level_name, db.sm_level.depth, db.sm_level.level0, db.sm_level.level1, db.sm_level.level2, db.sm_level.level3,db.sm_level.level0_name, db.sm_level.level1_name, db.sm_level.level2_name, db.sm_level.level3_name, limitby=(0, 1))
                if levelRecords:
                    route_name = levelRecords[0].level_name
                    regionid = levelRecords[0].level0
                    areaid = levelRecords[0].level1
                    terriroryid = levelRecords[0].level2

                    level0_id = levelRecords[0].level0
                    level0_name = levelRecords[0].level0_name
                    level1 = levelRecords[0].level1
                    level1_name = levelRecords[0].level1_name
                    level2 = levelRecords[0].level2
                    level2_name = levelRecords[0].level2_name
                    level3 = levelRecords[0].level3
                    level3_name = levelRecords[0].level3_name
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
#                return note
                insertRes = db.sm_order_head.insert(cid=cid, depot_id=depot_id, depot_name=depot_name, sl=ordSl, rep_id=rep_id, rep_name=rep_name, mobile_no=mobile_no, user_type=user_type, client_id=client_id, client_name=client_name, client_cat=client_cat, order_date=visit_date, order_datetime=visit_datetime,delivery_date=delivery_date,collection_date=collection_date, ym_date=firstDate, area_id=route_id, area_name=route_name, visit_type=visit_type, lat_long=lat_long, status='Submitted', visit_image=visit_photo, payment_mode=payment_mode, field1=field1,note=str(note), level0_id = level0_id,  level0_name = level0_name,level1_id = level1_id,level1_name = level1_name,level2_id = level2_id,level2_name = level2_name,level3_id = level3_id,level3_name = level3_name )
#                return db._lastsql
                vsl = db.sm_order_head(insertRes).id
                
                

                
                #                Client lat_long update
#                return client_lat
                if ((client_lat=='') | (client_lat=='0')| (client_long=='')| (client_long=='0')):
                    db((db.sm_client.cid == cid) & (db.sm_client.client_id == client_id)).update(latitude=latitude,longitude=longitude)

#                Insert in tracking table====================
                insertTracking = db.sm_tracking_table.insert(cid=cid, depot_id=depot_id, depot_name=depot_name, sl=ordSl, rep_id=rep_id, rep_name=rep_name,call_type='SELL',  visited_id=client_id, visited_name=client_name, visit_date=visit_date, visit_time=visit_datetime,  area_id=route_id, area_name=route_name, visit_type=visit_type, visited_latlong=lat_long,actual_latlong=tracking_table_latlong)  
                    
                    

                #--------- Market Info

#                marketInfoArrayList = []
#                market_infoList = market_info.split('<rd>')
#                for i in range(len(market_infoList)):                                                                                                                                                                             
#                    brandList = market_infoList[i].split('<fd>')
#                    if len(brandList) == 9:
#                        brand_name = brandList[0]
#                        monthly_sales = brandList[1]
#                        stock = brandList[2]
#                        credit_amt = brandList[3]
#                        price = brandList[4]
#                        free_bag = brandList[5]
#                        retailer_commission = brandList[6]
#                        trade_promotion = brandList[7]
#                        remarks = brandList[8]
#
#                        if monthly_sales == '':
#                            monthly_sales = 0
#                        if stock == '':
#                            stock = 0
#                        if credit_amt == '':
#                            credit_amt = 0
#                        if price == '':
#                            price = 0
#
#                        if free_bag == '':
#                            free_bag = 0
#                        if retailer_commission == '':
#                            retailer_commission = 0
#
#
#                        marketInfoArrayList.append({'cid':cid, 'SL':vsl, 'brand_name':brand_name, 'monthly_sales':monthly_sales, 'stock':stock, 'credit_amt':credit_amt, 'price':price, 'free_bag':free_bag, 'retailer_commission':retailer_commission, 'trade_promotion':trade_promotion, 'remarks':remarks, 'client_id':client_id, 'region_id':regionid, 'area_id':areaid, 'territory_id':terriroryid, 'market_id':route_id, 'monthly_last_flag':1})
#                if len(marketInfoArrayList) > 0:
#                    db.visit_market_info.bulk_insert(marketInfoArrayList)
#                    db((db.visit_market_info.cid == cid) & (db.visit_market_info.first_date == first_currentDate) & (db.visit_market_info.client_id == client_id) & (db.visit_market_info.SL != vsl)).update(monthly_last_flag=0)

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

                        ins_dict = {'cid':cid, 'vsl':vsl, 'depot_id':depot_id, 'depot_name':depot_name, 'sl':ordSl, 'client_id':client_id, 'client_name':client_name, 'rep_id':rep_id, 'rep_name':rep_name, 'order_date':visit_date, 'order_datetime':visit_datetime, 'ym_date':firstDate,'delivery_date':delivery_date,'collection_date':collection_date,
                                                                           'area_id':route_id, 'area_name':route_name, 'item_id':itemId, 'item_name':itemName, 'category_id':itemCat, 'quantity':itemQty, 'price':itemPrice, 'order_media':'APP', 'status':'Submitted', 'level0_id' : level0_id,  'level0_name' : level0_name,'level1_id' : level1_id,'level1_name' : level1_name,'level2_id' : level2_id,'level2_name' : level2_name,'level3_id' : level3_id,'level3_name' : level3_name}

                        orderArrayList.append(ins_dict)
                if len(orderArrayList) > 0:
                    db.sm_order.bulk_insert(orderArrayList)

                #--------- Merchandizing
#                merchandArrayList = []
#                merchandizingList = merchandizing.split('<rd>')
#                for i in range(len(merchandizingList)):
#                    merchandizingDataList = merchandizingList[i].split('<fd>')
#                    if len(merchandizingDataList) == 8:
#                        m_item_id = merchandizingDataList[0]
#                        m_item_name = merchandizingDataList[1]
#                        m_qty = merchandizingDataList[2]
#                        m_date = merchandizingDataList[3]
#                        m_visitble = merchandizingDataList[4]
#                        m_status = merchandizingDataList[5]
#                        m_dismantled = merchandizingDataList[6]
#                        new_flag = merchandizingDataList[7]
#
#                        merchandArrayList.append({'cid':cid, 'SL':vsl, 'client_id':client_id, 'client_name':client_name, 'm_item_id':m_item_id, 'name':m_item_name, 'qty':m_qty, 'installation_date':m_date, 'new_flag':new_flag, 'visible':m_visitble, 'condition_value':m_status, 'dismantled':m_dismantled, 'new_flag':new_flag, 'last_flag':1})
#                if len(merchandArrayList) > 0:
#                    db.visit_merchandising.bulk_insert(merchandArrayList)
#                    db((db.visit_merchandising.cid == cid) & (db.visit_merchandising.client_id == client_id) & (db.visit_merchandising.SL != vsl) & (db.visit_merchandising.last_flag == 1)).update(last_flag=0)
#
#                #--------- Campaign
#                campaignArrayList = []
#                campaignList = campaign.split('<fd>')
#                for i in range(len(campaignList)):
#                    offerId = campaignList[i]
#                    if offerId != '':
#                        offerId = int(campaignList[i])
#                        offer_name = ''
#                        offerRow = db((db.trade_promotional_offer.cid == cid) & (db.trade_promotional_offer.id == offerId) & (db.trade_promotional_offer.status == 'ACTIVE')).select(db.trade_promotional_offer.ALL, limitby=(0, 1))
#                        if offerRow:
#                           offer_name = offerRow[0].offer_name
#                           offer_from_date = offerRow[0].from_date
#                           offer_to_date = offerRow[0].to_date
#
#                           campaignArrayList.append({'cid':cid, 'vsl':vsl, 'first_date':firstDate, 'visit_date':visit_date, 'client_id':client_id, 'client_name':client_name, 'offer_id':offerId, 'offer_name':offer_name, 'offer_from_date':offer_from_date, 'offer_to_date':offer_to_date, 'last_flag':1})
#
#                if len(campaignArrayList) > 0:
#                    db.visit_client_offer.bulk_insert(campaignArrayList)
#                    db((db.visit_client_offer.cid == cid) & (db.visit_client_offer.client_id == client_id) & (db.visit_client_offer.vsl != vsl) & (db.visit_client_offer.last_flag == 1)).update(last_flag=0)
#
#                #---------------- NB. Required update first date if visit date not same month
#                if visit_type == 'Scheduled':
#                    db((db.sm_visit_plan.cid == cid) & (db.sm_visit_plan.schedule_date == schedule_date) & (db.sm_visit_plan.client_id == client_id)).update(visited_flag=1, visit_sl=vsl, visit_date=visit_date, status='Visited')

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
                docLRows = db((db.sm_doctor_area.cid == cid) & (db.sm_doctor_area.doc_id == doctorID) & (db.sm_doctor_area.area_id == routeID)).select(db.sm_doctor_area.area_id, db.sm_doctor_area.area_name, db.sm_doctor_area.depot_id, db.sm_doctor_area.field1, limitby=(0, 1))
                docRouteRows = db((db.sm_client.cid == cid) & (db.sm_client.area_id == routeID)).select(db.sm_client.depot_id, limitby=(0, 1))
                docARows = db((db.sm_level.cid == cid) & (db.sm_level.level_id == routeID)).select(db.sm_level.ALL, limitby=(0, 1))
#                 return docARows
                if not (docRouteRows or docLRows or docARows):
                    errorFlag = 1
                    errorMsg = 'Invalid route for the doctor'
                else:
                    routeID = docLRows[0].area_id
                    depotID = docRouteRows[0].depot_id
                    areaID = docLRows[0].area_id
                    areaName = docLRows[0].area_name
                    tracking_table_latlong = docLRows[0].field1
                    
                    level0_id = docARows[0].level0
                    level0_name = docARows[0].level0_name
                    level1_id = docARows[0].level1
                    level1_name = docARows[0].level1_name
                    level2_id = docARows[0].level2
                    level2_name = docARows[0].level2_name
                    level3_id = docARows[0].level3
                    level3_name = docARows[0].level3_name
            
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
                            gftQty=int(gftQty)
#                            pass
                        else:
                            giftRows = ''
                            errorFlag = 1
                            errorMsg = 'Invalid quantity for gift ID %s' % (gftID)
                            break

                        if (int(gftQty) > 0):
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
                        if ppmQty.isdigit() :
                            ppmQty=int(ppmQty)
#                            pass      
                        else:
                            ppmRows = ''
                            errorFlag = 1
                            errorMsg = 'Invalid quantity for ppm ID %s' % (ppmID)
                            break

                        if (int(ppmQty) > 0):
                            if ppmStr == '':
                                ppmStr = ppmID + ',' + str(ppmName).replace(',', ' ') + ',' + str(ppmQty)
                            else:
                                ppmStr += 'fdsep' + ppmID + ',' + str(ppmName).replace(',', ' ') + ',' + str(ppmQty)
#                     return giftStr
            ppmRows = ''
    
#    -------------Sample part end
    
    #----- sample part
    
    
    
#    return errorFlag
    
    samplePart=str(samplePart).replace(',.', ' ').replace('.,', ' ').replace('UNDEFINED', ' ')
#    return samplePart
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
#                    return errorFlag
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
#                        return errorFlag
                        break
                    else:
                        smpQty = smpIdList[1]
                        if smpQty.isdigit() :
                            smpQty=int(smpQty)
#                            pass

                        else:
                            sampleRows = ''
                            errorFlag = 1
                            errorMsg = 'Invalid quantity for sample ID %s' % (smpID)
                            break

                        if (int(smpQty) > 0):
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
        insRes = db.sm_doctor_visit.insert(cid=cid, doc_id=doctorID, doc_name=docName, rep_id=rep_id, rep_name=rep_name, feedback=notesPart, ho_status='0', route_id=routeID,route_name=areaName, depot_id=depotID, visit_dtime=datetime_fixed, visit_date=current_date, giftnsample=itemngiftnsample,latitude = latitude, longitude = longitude, note=v_with,level0_id = level0_id,level0_name = level0_name,level1_id = level1_id,level1_name = level1_name,level2_id = level2_id,level2_name = level2_name,level3_id = level3_id,level3_name =level3_name)
        
        
        
        lat_long=str(latitude)+','+str(longitude)
        if (tracking_table_latlong=="0,0"):
            insRes =db((db.sm_doctor_area.cid == cid) & (db.sm_doctor_area.doc_id == doctorID) & (db.sm_doctor_area.area_id == areaID)).update(field1=lat_long)
        
#        return depotName
#         insertTracking = db.sm_tracking_table.insert(cid=cid, depot_id=depotID, depot_name=depotName, sl="0", rep_id=rep_id, rep_name=rep_name,call_type='DCR',  visited_id=doctorID, visited_name=docName, visit_date=current_date, visit_time=datetime_fixed,  area_id=routeID, area_name=routeName, visit_type=visit_type, visited_latlong=lat_long, actual_latlong=tracking_table_latlong) 
        
        return 'SUCCESS<SYNCDATA>'
# ========================Doctor End================

#==================Report Start================
#http://127.0.0.1:8000/mrepnovelta/syncmobile_ofline_ppm_02012015/s_call_order_summary?
#cid=NOVELTA&rep_id=1001&rep_pass=123&synccode=8201&rep_id_report=1001&se_item_report=All&se_market_report=DG022&date_from=2015-02-09&date_to=2015-02-09
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
#    return user_type
    if (date_from==''):
        date_from=current_date
    if (date_to==''):
        now = datetime.datetime.strptime(current_date, "%Y-%m-%d")
        date_to=now + datetime.timedelta(days = 1)
    else :   
        date_to_get = datetime.datetime.strptime(date_to, "%Y-%m-%d")
        date_to=date_to_get + datetime.timedelta(days = 1) 
#    return date_to
        
#    if (date_from==date_from):
#        now = datetime.datetime.strptime(date_from, "%Y-%m-%d")
#        date_to=now + datetime.timedelta(days = 1)
        
        
    
    repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.sync_code == synccode) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.ALL, limitby=(0, 1))

#     return db._lastsql
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
    
    
    
#     return user_type
    if (user_type=='REP'):
        #    Sales Call====================
        qset=db()
        qset=qset((db.sm_order_head.cid == cid) & (db.sm_order_head.rep_id == rep_id))
        qset=qset((db.sm_order_head.delivery_date >= date_from) & (db.sm_order_head.delivery_date  < date_to))
        
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
        qset_oc=qset_oc((db.sm_order_head.delivery_date >= date_from) & (db.sm_order_head.delivery_date  < date_to))
        
        if (se_market_report!="ALL"):        
           qset_oc=qset_oc(db.sm_order_head.area_id==se_market_report)
        records_oc=qset_oc.select(db.sm_order_head.sl.count())
#        return db._lastsql
        if records_oc:
            order_count=records_oc[0][db.sm_order_head.sl.count()]
        
        

        
        
        
    
    
    #  Order Value  
        condition=""
        if (se_market_report!="ALL"):        
           condition="and sm_order.area_id='"+ str(se_market_report) +"' "


        records_ov=[]
        sql_str="SELECT SUM((sm_order.price) * (sm_order.quantity)) as totalprice, sm_order.area_id as area_id, sm_order.area_name as area_name FROM sm_order WHERE sm_order.cid = '"+ str(cid) +"' AND sm_order.rep_id = '"+ str(rep_id) +"' AND sm_order.delivery_date >= '"+ str(date_from) +"' AND sm_order.delivery_date < '"+ str(date_to) +"' "+ condition + " GROUP BY sm_order.area_id;"
#         return sql_str
        records_ov=db.executesql(sql_str,as_dict = True)

        order_value='0.0'
        areawise_flag=0
        areawise_str=""
        total_value=0
        for i in range(len(records_ov)): 
            records_ov_dict=records_ov[i]        
            if (areawise_flag==0):
                    repwise_str='Area wise: '
                    areawise_flag=1
            
#            areawise_str=areawise_str+'Route: '+str(records_ov[db.sm_order.area_name])+'('+str(records_ov[db.sm_order.area_id])+') --'+str(records_ov[db.sm_order.price.sum()])+'</br>'
            areawise_str=areawise_str+str(records_ov_dict["area_name"])+'('+str(records_ov_dict["area_id"])+'): '+str(records_ov_dict["totalprice"])+'</br>'
            
            total_value=total_value+float(records_ov_dict["totalprice"])
            
#        return total_value 
        
        if (sales_call==None):
            sales_call='0'
        if (order_count==None):
            order_count='0'
        if (order_value==None):
            order_value='0.0'
        
        
    #    return db._lastsql
        report_value_str= '  '+str(total_value) +'</br><font style=" font-size:11px">'+str(areawise_str)+'</font>'
        
        report_string='  '+str(sales_call)+'</br><rd>'+'  '+str(order_count) +'</br><rd>'+report_value_str
#        report_string=str(sales_call)+ '<rd>' +str(order_count)+ '<rd><font style=" font-size:11px"></br>' +str(report_value_str)+'</font>'
#        return report_string
    
    if (user_type=='SUP'):
        levelList=[]
        marketList=[]
        spicial_codeList=[]
        marketStr=''
        SuplevelRows = db((db.sm_supervisor_level.cid == cid) & (db.sm_supervisor_level.sup_id == rep_id) ).select(db.sm_supervisor_level.level_id,db.sm_supervisor_level.level_depth_no, orderby=~db.sm_supervisor_level.level_id)
        for SuplevelRows in SuplevelRows:
            Suplevel_id = SuplevelRows.level_id
            depth = SuplevelRows.level_depth_no
            level = 'level' + str(depth)
            if Suplevel_id not in levelList:
                levelList.append(Suplevel_id)
                
        
        
        cTeam=0
        for i in range(len(levelList)):
            levelRows = db((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '1') & (db.sm_level[level] == levelList[i]) ).select(db.sm_level.level_id, db.sm_level.level_name, db.sm_level.depot_id,db.sm_level.special_territory_code)
#             return levelRows
            for levelRow in levelRows:
                level_id = levelRow.level_id
                special_territory_code = levelRow.special_territory_code
                if level_id==special_territory_code:
                    cTeam=1

                if marketStr=='':
                    marketStr="'"+str(level_id)+"'"
                else:
                    marketStr=marketStr+",'"+str(level_id)+"'" 
            if cTeam==1:    
                if depth < 2:
                    return 'SUCCESS<SYNCDATA>'+'Data Not Available.'
                if special_territory_code not in spicial_codeList:
                    if (special_territory_code !='' and level_id==special_territory_code):
                        spicial_codeList.append(special_territory_code)    
            
                    levelSpecialRows = db((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '1') & (db.sm_level.special_territory_code.belongs(spicial_codeList)) ).select(db.sm_level.level_id, db.sm_level.level_name, db.sm_level.depot_id)        

                    for levelSpecialRow in levelSpecialRows:
                        level_id = levelSpecialRow.level_id
#                         if level_id not in marketList:   
#                             marketList.append(level_id)   
                        if marketStr=='':
                            marketStr="'"+str(Suplevel_id)+"'"
                        else:
                            marketStr=marketStr+",'"+str(level_id)+"'" 
                                
#         return marketStr
        condition=''
        if (se_market_report!="ALL"):
            condition=condition+"AND route_id = '"+str(se_market_report)+"'"
        if (rep_id!=rep_id_report):
            condition=condition+"AND rep_id = '"+str(rep_id_report)+"'"
        condition=condition+" AND area_id IN ("+str(marketStr)+")"  
        
        qset_vc_str="SELECT count(sl) as Vcount FROM sm_order_head WHERE cid =  '"+ str(cid) +"' AND delivery_date >=  '"+ str(date_from) +"' AND delivery_date <  '"+ str(date_to) +"' "+ condition + " "
#         return qset_vc_str
        reportRows_count=db.executesql(qset_vc_str,as_dict = True)

        visit_count=0
        for reportRows_count in reportRows_count:
            visit_count=reportRows_count['Vcount']

#        ==== Order Count====================
        qset_oc_str="SELECT count(sl) as Ocount FROM sm_order_head WHERE cid =  '"+ str(cid) +"' AND field1 = 'ORDER' AND delivery_date >=  '"+ str(date_from) +"' AND delivery_date <  '"+ str(date_to) +"' "+ condition + " "
        reportRows_order_count=db.executesql(qset_oc_str,as_dict = True)

        order_count=0
        for reportRows_order_count in reportRows_order_count:
            order_count=reportRows_order_count['Ocount']

# #            =============area wise Value

 

        records_ov=[]
        sql_str="SELECT SUM( (sm_order.price) * ( sm_order.quantity ) ) AS totalprice, sm_order.area_id AS area_id, sm_order.area_name AS area_name FROM sm_order WHERE sm_order.cid =  '"+ str(cid) +"' AND sm_order.delivery_date >=  '"+ str(date_from) +"' AND sm_order.delivery_date <  '"+ str(date_to) +"' "+ condition + " GROUP BY sm_order.area_name"
#        return sql_str
        records_ov=db.executesql(sql_str,as_dict = True)

        order_value='0.0'
        areawise_flag=0
        areawise_str=""
        total_value=0
        for i in range(len(records_ov)): 
            records_ov_dict=records_ov[i]        
            if (areawise_flag==0):
                    repwise_str='Area wise: </br>'
                    areawise_flag=1
            
            total_value=total_value+int(records_ov_dict["totalprice"])
            areawise_str=areawise_str+str(records_ov_dict["area_name"])+'('+str(records_ov_dict["area_id"])+'): '+str(records_ov_dict["totalprice"])+'</br>'


        report_value_str= '  '+str(total_value) +'</br><font style=" font-size:11px"></br>'+str(areawise_str)+'</font>'

       
        
    
        report_string='  '+str(visit_count)+'</br><rd>'+'  '+str(order_count) +'</br><rd>'+report_value_str
        
    
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
    
#     date_to=""
    
    if (date_from==''):
        date_from=current_date
    if (date_to==''):
        date_from_check = datetime.datetime.strptime(date_from, "%Y-%m-%d")
        date_to=date_from_check + datetime.timedelta(days = 1)
    else :   
        date_to_get = datetime.datetime.strptime(date_to, "%Y-%m-%d")
        date_to=date_to_get + datetime.timedelta(days = 1)     
    
    
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
        qset=qset((db.sm_order_head.delivery_date >= date_from) & (db.sm_order_head.delivery_date  < date_to))
        
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
        qset_oc=qset_oc((db.sm_order_head.delivery_date >= date_from) & (db.sm_order_head.delivery_date  < date_to))
        
        if (se_market_report!="ALL"):        
           qset_oc=qset_oc(db.sm_order_head.area_id==se_market_report)
        
        records_oc=qset_oc.select(db.sm_order_head.sl.count())
#        return db._lastsql
        if records_oc:
            order_count=records_oc[0][db.sm_order_head.sl.count()]
        
        

        
        
        
    
    
    #  Order Value  
        condition=""
        if (se_market_report!="ALL"):        
           condition="and sm_order.area_id='"+ str(se_market_report) +"' "

#        records_ov=qset_ov.select(db.sm_order.price.sum(),db.sm_order.area_id,db.sm_order.area_name, groupby=db.sm_order.area_id)
        records_ov=[]
        sql_str="SELECT SUM((sm_order.price) * (sm_order.quantity)) as totalprice, sm_order.area_id as area_id, sm_order.area_name as area_name FROM sm_order WHERE sm_order.cid = '"+ str(cid) +"' AND sm_order.rep_id = '"+ str(rep_id) +"' AND sm_order.delivery_date >= '"+ str(date_from) +"' AND sm_order.delivery_date < '"+ str(date_to) +"' "+ condition + " GROUP BY sm_order.area_id;"
        records_ov=db.executesql(sql_str,as_dict = True)
#        return db._lastsql
        order_value='0.0'
        areawise_flag=0
        areawise_str=""
        total_value=0
        for i in range(len(records_ov)): 
            records_ov_dict=records_ov[i]        
            if (areawise_flag==0):
                    repwise_str='Area wise: '
                    areawise_flag=1
            
#            areawise_str=areawise_str+'Route: '+str(records_ov[db.sm_order.area_name])+'('+str(records_ov[db.sm_order.area_id])+') --'+str(records_ov[db.sm_order.price.sum()])+'</br>'
            areawise_str=areawise_str+'Route: '+str(records_ov_dict["area_name"])+'('+str(records_ov_dict["area_id"])+'): '+str(records_ov_dict["totalprice"])+'</br>'
            total_value=total_value+float(records_ov_dict["totalprice"])
        
        if (sales_call==None):
            sales_call='0'
        if (order_count==None):
            order_count='0'
        if (order_value==None):
            order_value='0.0'
        
        report_value_str= '  '+str(total_value) +'</br><font style=" font-size:12px"></br>'+str(areawise_str)+'</font>'
#        return report_value_str
       
        
    
        report_string='  '+str(sales_call)+'</br><rd>'+'  '+str(order_count) +'</br><rd>'+report_value_str
        
#        report_string=str(sales_call)+ '<rd>' +str(order_count)+ '<rd> <font style=" font-size:11px"></br>' +str(areawise_str)+'</font>'
        
        
        
        
#        ========================================
    
    
    
    
#    Last three order
    
        qset_ol=db()
        qset_ol=qset_ol((db.sm_order_head.cid == cid) & (db.sm_order_head.rep_id == rep_id) & (db.sm_order_head.field1 == 'ORDER')) 
        qset_ol=qset_ol((db.sm_order_head.delivery_date >= date_from) & (db.sm_order_head.delivery_date  < date_to))
    #    return se_market_report
        if (se_market_report!="ALL"):        
           qset_ol=qset_ol(db.sm_order_head.area_id==se_market_report) 
        records_ol=qset_ol.select(db.sm_order_head.ALL, orderby=~db.sm_order_head.id, limitby=(0,20))
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
            qset_o=qset_o((db.sm_order.delivery_date >= date_from) & (db.sm_order.delivery_date  < date_to))
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
                payment_mode=record_o.payment_mode
                
                    
    #         ===========  amount
#                qset_amount=db()
#                qset_amount=qset_amount((db.sm_order.cid == cid) & (db.sm_order.rep_id == rep_id)) 
#                qset_amount=qset_amount((db.sm_order.order_date >= date_from) & (db.sm_order.order_date  < date_to))
#                records_amount=qset_amount.select(db.sm_order.price.sum())
                records_amount=[]
                amount_str="SELECT SUM((sm_order.price) * (sm_order.quantity)) as totalprice FROM sm_order WHERE (((sm_order.cid = '"+ str(cid) +"') AND (sm_order.rep_id = '"+ str(rep_id) +"')) AND ((sm_order.delivery_date >= '"+ str(date_from) +"') AND (sm_order.delivery_date < '"+ str(date_to) +"') and  (sm_order.vsl = '"+ str(vsl) + "') "+ "))"                
                
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
                    order_string=order_string+ "Visit SL:"+str(vsl)+ " Time:"+str(order_datetime)+"</br>Rep: "+str(rep_name)+" ("+str(rep_id)+")</br>"+str(c_name)+" ("+str(c_id)+" )"+"</br>PaymentMode "+str(payment_mode)+"</br>Order ="+str(order_amount)+"</br>"+"</br>"
#                    else:
#                        order_string=order_string+"</br>"+"Visit SL:"+str(vsl)+ " Time:"+str(order_datetime)
                order_vsl_past=vsl
                
#        return order_string
        report_string=str(report_string)+'<rd>'+'<font style=" font-size:11px"></br>'+str(order_string)+'</font>'
#        return report_string
    
    
    
    if (user_type=='SUP'):
        levelList=[]
        marketList=[]
        spicial_codeList=[]
        marketStr=''
        SuplevelRows = db((db.sm_supervisor_level.cid == cid) & (db.sm_supervisor_level.sup_id == rep_id) ).select(db.sm_supervisor_level.level_id,db.sm_supervisor_level.level_depth_no, orderby=~db.sm_supervisor_level.level_id)
        for SuplevelRows in SuplevelRows:
            Suplevel_id = SuplevelRows.level_id
            depth = SuplevelRows.level_depth_no
            level = 'level' + str(depth)
            if Suplevel_id not in levelList:
                levelList.append(Suplevel_id)
        
        
        
        
        cTeam=0
        for i in range(len(levelList)):
            levelRows = db((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '1') & (db.sm_level[level] == levelList[i]) ).select(db.sm_level.level_id, db.sm_level.level_name, db.sm_level.depot_id,db.sm_level.special_territory_code)
#             return levelRows
            for levelRow in levelRows:
                level_id = levelRow.level_id
                special_territory_code = levelRow.special_territory_code
                if level_id==special_territory_code:
                    cTeam=1

                if marketStr=='':
                    marketStr="'"+str(level_id)+"'"
                else:
                    marketStr=marketStr+",'"+str(level_id)+"'" 
            if cTeam==1:    
                if depth < 2:
                    return 'SUCCESS<SYNCDATA>'+'Data Not Available.'
                if special_territory_code not in spicial_codeList:
                    if (special_territory_code !='' and level_id==special_territory_code):
                        spicial_codeList.append(special_territory_code)    
            
                    levelSpecialRows = db((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '1') & (db.sm_level.special_territory_code.belongs(spicial_codeList)) ).select(db.sm_level.level_id, db.sm_level.level_name, db.sm_level.depot_id)        

                    for levelSpecialRow in levelSpecialRows:
                        level_id = levelSpecialRow.level_id
#                         if level_id not in marketList:   
#                             marketList.append(level_id)   
                        if marketStr=='':
                            marketStr="'"+str(Suplevel_id)+"'"
                        else:
                            marketStr=marketStr+",'"+str(level_id)+"'" 
                                
#         return marketStr
        condition=''
        if (se_market_report!="ALL"):
            condition=condition+"AND route_id = '"+str(se_market_report)+"'"
        if (rep_id!=rep_id_report):
            condition=condition+"AND rep_id = '"+str(rep_id_report)+"'"
        condition=condition+" AND area_id IN ("+str(marketStr)+")"  
        
        qset_vc_str="SELECT count(sl) as Vcount FROM sm_order_head WHERE cid =  '"+ str(cid) +"' AND delivery_date >=  '"+ str(date_from) +"' AND delivery_date <  '"+ str(date_to) +"' "+ condition + " "
#         return qset_vc_str
        reportRows_count=db.executesql(qset_vc_str,as_dict = True)

        visit_count=0
        for reportRows_count in reportRows_count:
            visit_count=reportRows_count['Vcount']

#        ==== Order Count====================
        qset_oc_str="SELECT count(sl) as Ocount FROM sm_order_head WHERE cid =  '"+ str(cid) +"' AND field1 = 'ORDER' AND delivery_date >=  '"+ str(date_from) +"' AND delivery_date <  '"+ str(date_to) +"' "+ condition + " "
        reportRows_order_count=db.executesql(qset_oc_str,as_dict = True)

        order_count=0
        for reportRows_order_count in reportRows_order_count:
            order_count=reportRows_order_count['Ocount']

# #            =============area wise Value

 

        records_ov=[]
        sql_str="SELECT SUM( (sm_order.price) * ( sm_order.quantity ) ) AS totalprice, sm_order.area_id AS area_id, sm_order.area_name AS area_name FROM sm_order WHERE sm_order.cid =  '"+ str(cid) +"' AND sm_order.delivery_date >=  '"+ str(date_from) +"' AND sm_order.delivery_date <  '"+ str(date_to) +"' "+ condition + " GROUP BY sm_order.area_name"
#        return sql_str
        records_ov=db.executesql(sql_str,as_dict = True)

        order_value='0.0'
        areawise_flag=0
        areawise_str=""
        total_value=0
        for i in range(len(records_ov)): 
            records_ov_dict=records_ov[i]        
            if (areawise_flag==0):
                    repwise_str='Area wise: </br>'
                    areawise_flag=1
            
            total_value=total_value+int(records_ov_dict["totalprice"])
            areawise_str=areawise_str+str(records_ov_dict["area_name"])+'('+str(records_ov_dict["area_id"])+'): '+str(records_ov_dict["totalprice"])+'</br>'


        report_value_str= '  '+str(total_value) +'</br><font style=" font-size:11px"></br>'+str(areawise_str)+'</font>'

       
        
    
#         report_string='  '+str(visit_count)+'</br><rd>'+'  '+str(order_count) +'</br><rd>'+report_value_str


#        return report_value_str

        order_string=''
       
            

    
    
        report_string='  '+str(visit_count)+'</br><rd>'+'  '+str(order_count) +'</br><rd>'+report_value_str
        report_string=str(report_string)+ '<rd>'+str(order_string)
       
#    Last 7 order
        
#         qset_ol=db()
#         qset_ol=qset_ol((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '1') & (db.sm_level[level] == level_rep) &     (db.sm_order_head.cid == cid) & (db.sm_order_head.area_id == db.sm_level.level_id ) & (db.sm_order_head.order_datetime >= date_from) & (db.sm_order_head.order_datetime  < date_to) & (db.sm_order_head.field1 == 'ORDER')  )          
#         if (se_market_report!="ALL"):
#             qset_rc=qset_ol(db.sm_order_head.area_id == se_market_report)        
#         if (rep_id!=rep_id_report):
#             qset_ol=qset_ol(db.sm_order_head.rep_id == rep_id_report)
#             
#         records_ol=qset_ol.select(db.sm_order_head.ALL, orderby=~db.sm_order_head.id, limitby=(0,20))
# #        return records_ol
#      
# 
#         order_sl=[]
#         
#         for record_ol in records_ol:
#             order_sl.append(record_ol.sl)
#     
#          
# #        return len(order_sl)
#         order_string=''
#         start_flag_amount=0
#         ordeer_vsl_past='0'
#         i=0
#         while i < len(order_sl):
#                 i=i+1
# ##            return len(order_sl)
#                 qset_o=db()
#                 qset_o=qset_o((db.sm_order.cid == cid) & (db.sm_order.rep_id == rep_id) ) 
#                 qset_o=qset_o((db.sm_order.order_date >= date_from) & (db.sm_order.order_date  < date_to))
#                 qset_o=qset_o((db.sm_order.sl.belongs(order_sl)))
#             
# #           
#                 records_o=qset_ol.select(db.sm_order.ALL, orderby=~db.sm_order.vsl)
# #            return db._lastsql
# #           
#                 for record_o in records_o:
#                     vsl=record_o.vsl
#                     c_id=record_o.client_id
#                     c_name=record_o.client_name
#                     order_datetime=record_o.order_datetime
#                     rep_name=record_o.rep_name
#                 
#   
#     #         ===========  amount
# #                 return 'sdasd'
#                 qset_amount=db()
#                 qset_amount=qset_amount((db.sm_order.cid == cid) & (db.sm_order.vsl == vsl)) 
#                 qset_amount=qset_amount((db.sm_order.order_date >= date_from) & (db.sm_order.order_date  < date_to))
#                 records_amount=qset_amount.select(db.sm_order.price.sum())
# #                return db._lastsql
# #                return records_amount
#                 order_amount='0.0'
#                 start_flag_amount=0
#                 if records_amount:
#                     order_amount=records_amount[0][db.sm_order.price.sum()]     
# #                     return order_amount
#                 if (ordeer_vsl_past!=vsl):
#                     if (start_flag_amount==0):
#                         start_flag_amount=1
#                         order_string=order_string+"</br>Visit SL:"+str(vsl)+ " Time:"+str(order_datetime)+"</br>Rep: "+str(rep_name)+" ("+str(rep_id)+")</br>"+str(c_name)+" ("+str(c_id)+" )</br>Order ="+str(order_amount)
#                     else:
#                         order_string=order_string+"</br>"+"Visit SL:"+str(vsl)+ " Time:"+str(order_datetime)
#                 ordeer_vsl_past=vsl
# #                return ordeer_vsl_past
#         report_string=str(report_string)+ '<rd>'+str(order_string)
#         report_string=str(report_string)+'<font style=" font-size:11px"></br>'+str(order_string)+'</font>'
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
    
#    return date_to
    repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.sync_code == synccode) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.id,db.sm_rep.user_type,db.sm_rep.level_id,db.sm_rep.field2, limitby=(0, 1))

#    return db._lastsql
   
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
        levelList=[]
        SuplevelRows = db((db.sm_supervisor_level.cid == cid) & (db.sm_supervisor_level.sup_id == rep_id) ).select(db.sm_supervisor_level.level_id,db.sm_supervisor_level.level_depth_no, orderby=~db.sm_supervisor_level.level_id)
#         return db._lastsql
#         return SuplevelRows
        
        levelStr=''
        for SuplevelRows in SuplevelRows:
            Suplevel_id = SuplevelRows.level_id
            depth = SuplevelRows.level_depth_no
            level = 'level' + str(depth)+'_id'
#             return level
            if Suplevel_id not in levelList:
                levelList.append(Suplevel_id)
                if levelStr=='':
                    levelStr="'"+str(Suplevel_id)+"'"
                else:
                    levelStr=levelStr+",'"+str(Suplevel_id)+"'"        
        condition=''
        if (se_market_report!="ALL"):
            condition=condition+"AND route_id = '"+str(se_market_report)+"'"
        if (rep_id!=rep_id_report):
            condition=condition+"AND rep_id = '"+str(rep_id_report)+"'"
        condition=condition+" AND "+str(level)+" IN ("+str(levelStr)+")"    
        qset_vcS="SELECT  count(id) as visitCount FROM sm_doctor_visit WHERE cid = '"+ cid +"' AND  visit_dtime >= '"+str(date_from)+"' AND     visit_dtime < '"+str(date_to)+"'"+condition+"  limit  1;"       
        reportRows_count=db.executesql(qset_vcS,as_dict = True) 
        visit_count=''
        for reportRows_count in reportRows_count:
            visit_count=reportRows_count['visitCount']
            
#         return visit_count
        
#        =============area wise
  
        qset_acS="SELECT  count(id) as vCount,route_id,route_name FROM sm_doctor_visit WHERE cid = '"+ cid +"' AND  visit_dtime >= '"+str(date_from)+"' AND     visit_dtime < '"+str(date_to)+"'"+condition+"  group by route_id;"
        reportRows=db.executesql(qset_acS,as_dict = True) 
 
        areawise_str=''
        areawise_flag=0
        
        
        for reportRow in reportRows:
            if (areawise_flag==0):
                areawise_str='Area wise: </br>'
                areawise_flag=1
            areawise_str=areawise_str+str(reportRow['route_name'])+'('+str(reportRow['route_id'])+') --'+str(reportRow['vCount'])+'</br>'

            
#        RepWise=========================

        qset_rcS="SELECT  count(id) as vCount,rep_id,rep_name FROM sm_doctor_visit WHERE cid = '"+ cid +"' AND  visit_dtime >= '"+str(date_from)+"' AND     visit_dtime < '"+str(date_to)+"'"+condition+"  group by rep_id;"
        repRows=db.executesql(qset_rcS,as_dict = True) 
        
        repwise_str=''
        repwise_flag=0
        for repRow in repRows:
            if (repwise_flag==0):
                repwise_str='Rep wise: </br>'
                repwise_flag=1
            
            repwise_str=repwise_str+str(repRow['rep_name'])+'('+str(repRow['rep_id'])+') --'+str(repRow['vCount'])+'</br>'
                     
#    return repwise_str
    
        report_string=str(visit_count)+'</br></br><rd>'+areawise_str+'</br></br><rd>'+repwise_str



    
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
        records_detail=qset_detail.select(db.sm_doctor_visit.ALL, orderby=~db.sm_doctor_visit.id, limitby=(0,20))
        
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
           
            if (att_string !=''):
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
            
                        
                    
                    
                    
                    
                campaign_string=''
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
        levelList=[]
        SuplevelRows = db((db.sm_supervisor_level.cid == cid) & (db.sm_supervisor_level.sup_id == rep_id) ).select(db.sm_supervisor_level.level_id,db.sm_supervisor_level.level_depth_no, orderby=~db.sm_supervisor_level.level_id)
#         return db._lastsql
#         return SuplevelRows
        
        levelStr=''
        for SuplevelRows in SuplevelRows:
            Suplevel_id = SuplevelRows.level_id
            depth = SuplevelRows.level_depth_no
            level = 'level' + str(depth)+'_id'
#             return level
            if Suplevel_id not in levelList:
                levelList.append(Suplevel_id)
                if levelStr=='':
                    levelStr="'"+str(Suplevel_id)+"'"
                else:
                    levelStr=levelStr+",'"+str(Suplevel_id)+"'"        
        condition=''
        if (se_market_report!="ALL"):
            condition=condition+"AND route_id = '"+str(se_market_report)+"'"
        if (rep_id!=rep_id_report):
            condition=condition+"AND rep_id = '"+str(rep_id_report)+"'"
        condition=condition+" AND "+str(level)+" IN ("+str(levelStr)+")"    
        qset_vcS="SELECT  count(id) as visitCount FROM sm_doctor_visit WHERE cid = '"+ cid +"' AND  visit_dtime >= '"+str(date_from)+"' AND     visit_dtime < '"+str(date_to)+"'"+condition+"  limit  1;"       
        reportRows_count=db.executesql(qset_vcS,as_dict = True) 
        visit_count=''
        for reportRows_count in reportRows_count:
            visit_count=reportRows_count['visitCount']
            
#         return visit_count
        
#        =============area wise
  
        qset_acS="SELECT  count(id) as vCount,route_id,route_name FROM sm_doctor_visit WHERE cid = '"+ cid +"' AND  visit_dtime >= '"+str(date_from)+"' AND     visit_dtime < '"+str(date_to)+"'"+condition+"  group by route_id;"
        reportRows=db.executesql(qset_acS,as_dict = True) 
 
        areawise_str=''
        areawise_flag=0
        
        
        for reportRow in reportRows:
            if (areawise_flag==0):
                areawise_str='Area wise: </br>'
                areawise_flag=1
            areawise_str=areawise_str+str(reportRow['route_name'])+'('+str(reportRow['route_id'])+') --'+str(reportRow['vCount'])+'</br>'

            
#        RepWise=========================

        qset_rcS="SELECT  count(id) as vCount,rep_id,rep_name FROM sm_doctor_visit WHERE cid = '"+ cid +"' AND  visit_dtime >= '"+str(date_from)+"' AND     visit_dtime < '"+str(date_to)+"'"+condition+"  group by rep_id;"
        repRows=db.executesql(qset_rcS,as_dict = True) 
        
        repwise_str=''
        repwise_flag=0
        for repRow in repRows:
            if (repwise_flag==0):
                repwise_str='Rep wise: </br>'
                repwise_flag=1
            
            repwise_str=repwise_str+str(repRow['rep_name'])+'('+str(repRow['rep_id'])+') --'+str(repRow['vCount'])+'</br>'
                     
#    return repwise_str
    
        report_string=str(visit_count)+'</br></br><rd>'+areawise_str+'</br></br><rd>'+repwise_str
        
        
#    Detail===========
        qset_detailS="SELECT  * FROM sm_doctor_visit WHERE cid = '"+ cid +"' AND  visit_dtime >= '"+str(date_from)+"' AND     visit_dtime < '"+str(date_to)+"'"+condition+"  order by id limit  20;"
        records_detail=db.executesql(qset_detailS,as_dict = True) 
        start_flag=0
        visit_string=''
        for records_detail in records_detail:
    #        return records_detail
            v_id = records_detail['id']
            rep_id = records_detail['rep_id'] 
            rep_name = records_detail['rep_name'] 
            doc_id = records_detail['doc_id'] 
            doc_name  =  records_detail['doc_name'] 
            feedback =  records_detail['feedback'] 
            visit_dtime = records_detail['visit_dtime'] 
            att_string   =  records_detail['giftnsample'] 
    #        return att_string
           
            if (att_string !=''):
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
                campaign_string=''
                if (campaign!=''):
                    campaignList = campaign.split('fdsep')
                    start_c_flag=0
                    
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
    repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.sync_code == synccode) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.id,db.sm_rep.user_type,db.sm_rep.level_id,db.sm_rep.field2, limitby=(0, 1))

#    return db._lastsql
   
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
            
    if (user_type=='SUP'):
        levelList=[]
        SuplevelRows = db((db.sm_supervisor_level.cid == cid) & (db.sm_supervisor_level.sup_id == rep_id) ).select(db.sm_supervisor_level.level_id,db.sm_supervisor_level.level_depth_no, orderby=~db.sm_supervisor_level.level_id)
        for SuplevelRows in SuplevelRows:
            Suplevel_id = SuplevelRows.level_id
            depth = SuplevelRows.level_depth_no
            level = 'level' + str(depth)
            if Suplevel_id not in levelList:
                levelList.append(Suplevel_id)
        
        qset_vc=db()
        qset_vc=qset_vc((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '1') & (db.sm_level[level] in (levelList)) &     (db.sm_prescription_head.cid == cid) & (db.sm_prescription_head.area_id == db.sm_level.level_id ) & (db.sm_prescription_head.created_on >= date_from) & (db.sm_prescription_head.created_on  < date_to))          
        if (se_market_report!="ALL"):
            qset_vc=qset_vc((db.sm_prescription_head.area_id == se_market_report))        
        if (rep_id!=rep_id_report):
            qset_vc=qset_vc((db.sm_prescription_head.submit_by_id == rep_id_report))
        reportRows_count=qset_vc.select(db.sm_prescription_head.id.count())    
#         return db._lastsql
        visit_count=''
        if reportRows_count:
            visit_count=reportRows_count[0][db.sm_prescription_head.id.count()]
            
#        return db._lastsql
        
#        =============area wise
        qset_ac=db()
        qset_ac=qset_ac((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '1') & (db.sm_level[level] in (levelList)) &     (db.sm_prescription_head.cid == cid) & (db.sm_prescription_head.area_id == db.sm_level.level_id ) & (db.sm_prescription_head.created_on >= date_from) & (db.sm_prescription_head.created_on  < date_to))          
        if (se_market_report!="ALL"):
            qset_ac=qset_ac((db.sm_prescription_head.area_id == se_market_report))        
        if (rep_id!=rep_id_report):
            qset_ac=qset_ac((db.sm_prescription_head.submit_by_id == rep_id_report))
        reportRows=qset_ac.select(db.sm_prescription_head.id.count(),db.sm_prescription_head.area_id,db.sm_level.level_name, groupby = db.sm_prescription_head.area_id)  
        
        
#        reportRows = db((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '1') & (db.sm_level[level] == level_rep) &     (db.sm_doctor_visit.cid == cid) & (db.sm_doctor_visit.route_id == db.sm_level.level_id ) & (db.sm_doctor_visit.visit_dtime >= date_from) & (db.sm_doctor_visit.visit_dtime  < date_to)).select(db.sm_doctor_visit.id.count(),db.sm_doctor_visit.route_id,db.sm_level.level_name, groupby = db.sm_doctor_visit.route_id)
#        levelRows = db((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '1') & (db.sm_level[level] == level_rep) ).select(db.sm_level.is_leaf)
        areawise_str=''
        areawise_flag=0
        
        
        for reportRow in reportRows:
            if (areawise_flag==0):
                areawise_str='Area wise: </br>'
                areawise_flag=1
            areawise_str=areawise_str+str(reportRow[db.sm_level.level_name])+'('+str(reportRow[db.sm_prescription_head.area_id])+') --'+str(reportRow[db.sm_prescription_head.id.count()])+'</br>'
           
 
#        RepWise=========================
        qset_rc=db()
        qset_rc=qset_rc((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '1') & (db.sm_level[level] in (levelList)) &     (db.sm_prescription_head.cid == cid) & (db.sm_prescription_head.area_id == db.sm_level.level_id ) & (db.sm_prescription_head.created_on >= date_from) & (db.sm_prescription_head.created_on  < date_to))          
        if (se_market_report!="ALL"):
            qset_rc=qset_rc((db.sm_prescription_head.area_id == se_market_report))        
        if (rep_id!=rep_id_report):
            qset_rc=qset_rc((db.sm_prescription_head.submit_by_id == rep_id_report))
            
        repRows=qset_rc.select(db.sm_prescription_head.id.count(),db.sm_prescription_head.submit_by_id,db.sm_prescription_head.submit_by_name, groupby = db.sm_prescription_head.submit_by_id)    
            
#        repRows = db((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '1') & (db.sm_level[level] == level_rep) &     (db.sm_doctor_visit.cid == cid) & (db.sm_doctor_visit.route_id == db.sm_level.level_id ) & (db.sm_doctor_visit.visit_dtime >= date_from) & (db.sm_doctor_visit.visit_dtime  < date_to)).select(db.sm_doctor_visit.id.count(),db.sm_doctor_visit.rep_id,db.sm_doctor_visit.rep_name, groupby = db.sm_doctor_visit.rep_id)
        repwise_str=''
        repwise_flag=0
        for repRow in repRows:
            if (repwise_flag==0):
                repwise_str='Rep wise: </br>'
                repwise_flag=1
            
            repwise_str=repwise_str+str(repRow[db.sm_prescription_head.submit_by_name])+'('+str(repRow[db.sm_prescription_head.submit_by_id])+') --'+str(repRow[db.sm_prescription_head.id.count()])+'</br>'
                     
#    return repwise_str
    
        report_string=str(visit_count)+'</br></br><rd>'+areawise_str+'</br></br><rd>'+repwise_str


#
#    return db._lastsql
#    report_string=str(visit_count)+','+areawise_str+','+repwise_str
    
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
        
        

    if (user_type=='SUP'): 
        levelList=[]
        SuplevelRows = db((db.sm_supervisor_level.cid == cid) & (db.sm_supervisor_level.sup_id == rep_id) ).select(db.sm_supervisor_level.level_id,db.sm_supervisor_level.level_depth_no, orderby=~db.sm_supervisor_level.level_id)
        for SuplevelRows in SuplevelRows:
            Suplevel_id = SuplevelRows.level_id
            depth = SuplevelRows.level_depth_no
            level = 'level' + str(depth)
            if Suplevel_id not in levelList:
                levelList.append(Suplevel_id)
                
        qset_vc=db()
        qset_vc=qset_vc((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '1') & (db.sm_level[level] in (levelList))  & (db.sm_prescription_head.cid == cid) & (db.sm_prescription_head.area_id == db.sm_level.level_id ) & (db.sm_prescription_head.created_on >= date_from) & (db.sm_prescription_head.created_on < date_to))          
        if (se_market_report!="ALL"):
            qset_vc=qset_vc((db.sm_prescription_head.area_id == se_market_report))        
        if (rep_id!=rep_id_report):
            qset_vc=qset_vc((db.sm_prescription_head.submit_by_id == rep_id_report))
        reportRows_count=qset_vc.select(db.sm_prescription_head.id.count())    
        
        visit_count=''
        if reportRows_count:
            visit_count=reportRows_count[0][db.sm_prescription_head.id.count()]
            
        
        
#        =============area wise
        qset_ac=db()
        qset_ac=qset_ac((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '1') & (db.sm_level[level] in (levelList))  &     (db.sm_prescription_head.cid == cid) & (db.sm_prescription_head.area_id == db.sm_level.level_id ) & (db.sm_prescription_head.created_on >= date_from) & (db.sm_prescription_head.created_on < date_to))          
        if (se_market_report!="ALL"):
            qset_ac=qset_ac((db.sm_prescription_head.area_id == se_market_report))        
        if (rep_id!=rep_id_report):
            qset_ac=qset_ac((db.sm_prescription_head.submit_by_id == rep_id_report))
        reportRows=qset_ac.select(db.sm_prescription_head.id.count(),db.sm_prescription_head.area_id,db.sm_level.level_name, groupby = db.sm_prescription_head.area_id)  
        
        

        areawise_str=''
        areawise_flag=0
        for reportRow in reportRows:
            if (areawise_flag==0):
                areawise_str='Area wise: </br>'
                areawise_flag=1
            areawise_str=areawise_str+str(reportRow[db.sm_level.level_name])+'('+str(reportRow[db.sm_prescription_head.area_id])+'): '+str(reportRow[db.sm_prescription_head.id.count()])+'</br>'
           
 
#        RepWise=========================
        qset_rc=db()
        qset_rc=qset_rc((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '1') & (db.sm_level[level] in (levelList))  &     (db.sm_prescription_head.cid == cid) & (db.sm_prescription_head.area_id == db.sm_level.level_id ) & (db.sm_prescription_head.created_on >= date_from) & (db.sm_prescription_head.created_on  < date_to))          
        if (se_market_report!="ALL"):
            qset_rc=qset_rc((db.sm_prescription_head.area_id == se_market_report))        
        if (rep_id!=rep_id_report):
            qset_rc=qset_rc((db.sm_prescription_head.submit_by_id == rep_id_report))
            
        repRows=qset_rc.select(db.sm_prescription_head.id.count(),db.sm_prescription_head.submit_by_id,db.sm_prescription_head.submit_by_name, groupby = db.sm_prescription_head.submit_by_id)    
            

        repwise_str=''
        repwise_flag=0
        for repRow in repRows:
            if (repwise_flag==0):
                repwise_str='Rep wise: </br>'
                repwise_flag=1
            
            repwise_str=repwise_str+str(repRow[db.sm_prescription_head.submit_by_name])+'('+str(repRow[db.sm_prescription_head.submit_by_id])+'): '+str(repRow[db.sm_prescription_head.id.count()])+'</br>'
                     
#    return repwise_str
    
        report_string=str(visit_count)+'</br></br><rd>'+areawise_str+'</br></br><rd>'+repwise_str   
        
        
#    Detail===========
        qset_detail=db()
        qset_detail=qset_detail((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '1') & (db.sm_level[level] in (levelList))  &     (db.sm_prescription_head.cid == cid) & (db.sm_prescription_head.area_id == db.sm_level.level_id ) & (db.sm_prescription_head.created_on >= date_from) & (db.sm_prescription_head.created_on  < date_to))  
       
        
        if (se_market_report!="ALL"):   
            qset_detail=qset_detail((db.sm_prescription_head.area_id == se_market_report))
        if (rep_id!=rep_id_report):
            qset_detail=qset_detail((db.sm_prescription_head.submit_by_id == rep_id_report))
        records_detail=qset_detail.select(db.sm_prescription_head.ALL, orderby=~db.sm_prescription_head.id, limitby=(0,10))
        

        
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
  
        
        report_string=str(report_string)+'<rd>'+str(visit_string)
    return 'SUCCESS<SYNCDATA>'+report_string 

#==================Report End================


#=============New Check User==============================

def check_user_pharma():
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
#         return repRow
#        return db._lastsql
        if not repRow:
           retStatus = 'FAILED<SYNCDATA>Invalid Authorization 2'
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
#             return level_id
            last_sync_date = date_fixed
            if first_sync_date == None:
                first_sync_date = date_fixed

            rep_update = repRow[0].update_record(sync_code=sync_code, first_sync_date=first_sync_date, last_sync_date=last_sync_date, sync_count=sync_count)

            
            s_key_list=[]
            s_key_list.append('VISIT_SAVE_LIMIT')
            s_key_list.append('ORDER_LOCATION')
            s_key_list.append('DELIVERY_DATE')
            s_key_list.append('PAYMENT_DATE')
            s_key_list.append('PAYMENT_MODE')
            s_key_list.append('COLLECTION_DATE')
            
            
            settingsRows = db((db.sm_settings_pharma.cid == cid) &(db.sm_settings_pharma.s_key.belongs(s_key_list)) ).select(db.sm_settings_pharma.s_key,db.sm_settings_pharma.s_value)
#            return db._lastsql
            visit_save_limit='0'
            visit_location=''
            delivery_date=''
            payment_date=''
            payment_mode=''
            for settingsRow in settingsRows:
                if (str(settingsRow.s_key)== 'VISIT_SAVE_LIMIT'):
                    visit_save_limit=str(settingsRow.s_value)
                if (str(settingsRow.s_key)== 'ORDER_LOCATION'):
                    visit_location=str(settingsRow.s_value)
                if (str(settingsRow.s_key)== 'DELIVERY_DATE'):
                    delivery_date=str(settingsRow.s_value)
                if (str(settingsRow.s_key)== 'PAYMENT_DATE'):
                    payment_date=str(settingsRow.s_value)
                if (str(settingsRow.s_key)== 'PAYMENT_MODE'):
                    payment_mode=str(settingsRow.s_value)
                if (str(settingsRow.s_key)== 'COLLECTION_DATE'):
                    collection_date=str(settingsRow.s_value)
#========================PromoCombo================
            promoRows = db((db.sm_promo_product_bonus.cid == cid) &(db.sm_promo_product_bonus.status=='ACTIVE') ).select(db.sm_promo_product_bonus.id,db.sm_promo_product_bonus.circular_number,db.sm_promo_product_bonus.note)
#             return promoRows
            promo_str=''
            for promoRows in promoRows:
                row_id = promoRows.id
                circular_number = promoRows.circular_number
                note = promoRows.note
                   
                if promo_str == '':
                    promo_str = str(row_id) + '<fd>' + str(circular_number)+ '<fd>' + str(note)
                else:
                    promo_str =promo_str+ '<rd>' + str(row_id) + '<fd>' + str(circular_number)+ '<fd>' + str(note)  
#                 return promo_str
#             return promo_str
# ========================DocCategory & Speciality
            cat_row=db(db.doc_catagory.cid == cid).select(db.doc_catagory.category, orderby=db.doc_catagory.category)
            catStr=''
            for cat_row in cat_row:
                catStr=catStr+str(cat_row.category)+','
            
            spc_row=db(db.doc_speciality.cid == cid).select(db.doc_speciality.specialty, orderby=db.doc_speciality.specialty    )
            spcStr=''
            for spc_row in spc_row:
                spcStr=spcStr+str(spc_row.specialty)+','

# ==================================

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
                productRows = db(db.sm_company_settings.cid == cid).select(db.sm_company_settings.field1, limitby=(0,1))
                for productRow in productRows:
                    productStr = productRow.field1
                    
                    

                
                
#                return productStr
                #-------------- Merchandizing list
                merchandizingStr = ''
                #-------------- Dealer list
                dealerStr = ''

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
                cliendepot_name=''


#                 ---------------------------------------------------------------------------------------
#                 ------------------------------Market Client List Start-----------------------------------------
                clientStr = ''
                start_flag = 0
                client_depot=''
                for marketRow_1 in marketRows:
                    area_id = marketRow_1.area_id


                    clientStr = clientStr + '<' + area_id + '>'
#                     return clientStr
                    clientRows = db((db.sm_client.cid == cid) & (db.sm_client.area_id == area_id) & (db.sm_client.status == 'ACTIVE')).select(db.sm_client.client_id, db.sm_client.name, db.sm_client.category_id,db.sm_client.depot_id,db.sm_client.depot_name,db.sm_client.market_name,db.sm_client.address, orderby=db.sm_client.name)

        #            return db._lastsql
                    if not clientRows:
                        clientStr = clientStr + 'Retailer not available' + '</' + area_id + '>'
#                         return retStatus
                    else:
                        client_depot=''
                        cliendepot_name=''
                        for clientRow in clientRows:
                            client_id = clientRow.client_id
                            name = clientRow.name
                            category_id = clientRow.category_id
                            address=clientRow.address
                            if len(address)>30:
                                address= str(clientRow.address)[30]
                            market_name=address+'-'+str(clientRow.market_name)
                            client_depot=clientRow.depot_id
                            cliendepot_name=clientRow.depot_name
                            if start_flag == 0:
                                
                                clientStr = clientStr + str(client_id) + '<fd>' + str(name)+' - '+str(market_name) + ' <fd>' + str(category_id).strip().upper()
                                start_flag = 1
                            else:
                                clientStr = clientStr + '<rd>' + str(client_id) + '<fd>' + str(name) +' - '+str(market_name)  + ' <fd>' + str(category_id).strip().upper()

                    clientStr = clientStr + '</' + area_id + '>'
                    clientStr=clientStr.replace("'","")
#                return clientStr





              


                    
#                 --------------------------------Market Client List End--------------------------------------
#                 ------------------------------Menu List Start-----------------------------------------
                menuStr = ''
                start_flag = 0
                menuRow = db((db.sm_mobile_settings_pharma.cid == cid) & (db.sm_mobile_settings_pharma.type == 'REP')).select(db.sm_mobile_settings_pharma.sl, db.sm_mobile_settings_pharma.s_key, db.sm_mobile_settings_pharma.s_value, orderby=db.sm_mobile_settings_pharma.sl)
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
#                 doctorRows = db((db.sm_doctor.cid == cid) & (db.sm_doctor.status == 'ACTIVE') & (db.sm_doctor_area.cid == cid) & (db.sm_doctor_area.doc_id == db.sm_doctor.doc_id) & (db.sm_doctor_area.area_id == area_id) ).select(db.sm_doctor.doc_id, db.sm_doctor.doc_name, db.sm_doctor_area.area_id, orderby=db.sm_doctor_area.area_id|db.sm_doctor.doc_name)
#                return db._lastsql
#                 doctorRows = db((db.sm_doctor.cid == cid) & (db.sm_doctor.status == 'ACTIVE') & (db.sm_doctor_area.cid == cid) & (db.sm_doctor_area.doc_id == db.sm_doctor.doc_id) & (db.sm_doctor_area.area_id.belongs(marketList))).select(db.sm_doctor.doc_id, db.sm_doctor.doc_name, db.sm_doctor_area.area_id, orderby=db.sm_doctor_area.area_id|db.sm_doctor.doc_name)
                doctor_area_past=''
                srart_a_flag=0
                doctorStr_flag=0
                for marketRow_1 in marketRows:
                    area_id = marketRow_1.area_id
                    doctorRows = db((db.sm_doctor.cid == cid) & (db.sm_doctor.status == 'ACTIVE') & (db.sm_doctor_area.cid == cid) & (db.sm_doctor_area.doc_id == db.sm_doctor.doc_id)  & (db.sm_doctor_area.area_id == area_id) ).select(db.sm_doctor.doc_id, db.sm_doctor.doc_name, db.sm_doctor_area.area_id, orderby=db.sm_doctor_area.area_id|db.sm_doctor.doc_name)
                    if not doctorRows:
                        pass
    #                    retStatus = 'FAILED<SYNCDATA>Doctor not available'
    #                    return retStatus
                    else:
                       
                        
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
                marketStr=marketStr.replace("'","")
                productStr=productStr.replace("'","")
                merchandizingStr =merchandizingStr.replace("'","")
                dealerStr=dealerStr.replace("'","")
                brandStr =brandStr.replace("'","")
                complainTypeStr=complainTypeStr.replace("'","")
                compFromStr =compFromStr.replace("'","")
                taskTypeStr =taskTypeStr.replace("'","")
                regionStr =regionStr.replace("'","")
                giftStr =giftStr.replace("'","")
                clienttCatStr =clienttCatStr.replace("'","")
                clientStr =clientStr.replace("'","")
                menuStr=menuStr.replace("'","")
                ppmStr =ppmStr.replace("'","")
                doctorStr =doctorStr.replace("'","")
                promo_str =promo_str.replace("'","")
#                 return str(cliendepot_name)
                marketStrCteam=marketStr
                cTeam=0
                return 'SUCCESS<SYNCDATA>' + str(sync_code) + '<SYNCDATA>' + marketStr + '<SYNCDATA>' + productStr + '<SYNCDATA>' + merchandizingStr + '<SYNCDATA>' + dealerStr + '<SYNCDATA>' + brandStr + '<SYNCDATA>' + complainTypeStr + '<SYNCDATA>' + compFromStr + '<SYNCDATA>' + taskTypeStr + '<SYNCDATA>' + regionStr + '<SYNCDATA>' + giftStr + '<SYNCDATA>' + clienttCatStr + '<SYNCDATA>' + clientStr + '<SYNCDATA>' + menuStr+ '<SYNCDATA>' +ppmStr + '<SYNCDATA>' + user_type+ '<SYNCDATA>' +str(doctorStr)+ '<SYNCDATA>' +str(visit_save_limit)+'<SYNCDATA>'+str(visit_location)+'<SYNCDATA>'+str(delivery_date)+'<SYNCDATA>'+str(payment_date)+'<SYNCDATA>'+str(payment_mode)+'<SYNCDATA>'+str(collection_date)+'<SYNCDATA>'+str(promo_str)+'<SYNCDATA>'+str(client_depot)+'<SYNCDATA>'+str(cliendepot_name)+'<SYNCDATA>'+str(catStr)+'<SYNCDATA>'+str(spcStr)+'<SYNCDATA>'+str(marketStrCteam)+'<SYNCDATA>'+str(cTeam)#+'<SYNCDATA>'+str(stockBalance_str)


            elif (user_type == 'sup'):
                depotList = []
                marketList=[]
                spicial_codeList=[]
                marketStr = ''
                spCodeStr=''
                levelList=[]
                SuplevelRows = db((db.sm_supervisor_level.cid == cid) & (db.sm_supervisor_level.sup_id == rep_id) ).select(db.sm_supervisor_level.level_id,db.sm_supervisor_level.level_depth_no, orderby=~db.sm_supervisor_level.level_id)
#                 return db._lastsql
                for SuplevelRows in SuplevelRows:
                    Suplevel_id = SuplevelRows.level_id
                    depth = SuplevelRows.level_depth_no
                    level = 'level' + str(depth)
                    if Suplevel_id not in levelList:
                        levelList.append(Suplevel_id)
                cTeam=0
                for i in range(len(levelList)):
#                     levelRows = db((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '1') & (db.sm_level[level] == levelList[i]) & (db.sm_level.special_territory_code<>levelList[i])).select(db.sm_level.level_id, db.sm_level.level_name, db.sm_level.depot_id,db.sm_level.special_territory_code)
                    levelRows = db((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '1') & (db.sm_level[level] == levelList[i]) ).select(db.sm_level.level_id, db.sm_level.level_name, db.sm_level.depot_id,db.sm_level.special_territory_code)
#                     return levelRows
                    for levelRow in levelRows:
                        level_id = levelRow.level_id
                        level_name = levelRow.level_name
                        depotid = str(levelRow.depot_id).strip()
                        special_territory_code = levelRow.special_territory_code
                        if level_id==special_territory_code:
#                             return level_id
                            cTeam=1
                        
                        if depotid not in depotList:
                            depotList.append(depotid)
                            
                        if level_id not in marketList:   
                            marketList.append(level_id)
                            
                        if cTeam==1:    
                            if special_territory_code not in spicial_codeList:
                                if (special_territory_code !='' and level_id==special_territory_code):
                                    spicial_codeList.append(special_territory_code)    
    #                             spCodeStr=spCodeStr+','+str(special_territory_code)
                        
                        if marketStr == '':
                            marketStr = str(level_id) + '<fd>' + str(level_name)
                        else:
                            marketStr += '<rd>' + str(level_id) + '<fd>' + str(level_name)
                levelSpecialRows = db((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '1') & (db.sm_level.special_territory_code.belongs(spicial_codeList)) ).select(db.sm_level.level_id, db.sm_level.level_name, db.sm_level.depot_id)        
#                 return db._lastsql
                for levelSpecialRow in levelSpecialRows:
                    level_id = levelSpecialRow.level_id
                    level_name = levelSpecialRow.level_name
                    depotid = str(levelSpecialRow.depot_id).strip()
 
                    if depotid not in depotList:
                        depotList.append(depotid)
                         
                    if level_id not in marketList:   
                        marketList.append(level_id)    
                        if marketStr == '':
                            marketStr = str(level_id) + '<fd>' + str(level_name)
                        else:
                            marketStr += '<rd>' + str(level_id) + '<fd>' + str(level_name) 
                         
                                  
#                 return len(spicial_codeList)
#                 return  cTeam   
                marketListCteam=[]
                marketStrCteam=''
                if cTeam==1: 
#                     levelSpecialRows = db((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '1') & (db.sm_level.special_territory_code.belongs(spicial_codeList))).select(db.sm_level.level_id, db.sm_level.level_name, db.sm_level.depot_id)        
# #                     return db._lastsql
#                     for levelSpecialRow in levelSpecialRows:
#                         level_id = levelSpecialRow.level_id
#                         level_name = levelSpecialRow.level_name
#                         depotid = str(levelSpecialRow.depot_id).strip()
#       
#                         if depotid not in depotList:
#                             depotList.append(depotid)
#                               
#                         if level_id not in marketList: 
#                             marketList.append(level_id)  
#                               
#                            
# #                         return len(marketList)       
#                         if marketStr == '':
#                             marketStr = str(level_id) + '<fd>' + str(level_name)
#                         else:
#                             marketStr += '<rd>' + str(level_id) + '<fd>' + str(level_name) 
                    levelSpecialRowsCteam = db((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '1') & (db.sm_level.level_id.belongs(spicial_codeList))).select(db.sm_level.level_id, db.sm_level.level_name, db.sm_level.depot_id)
                    for levelSpecialRowsCteam in levelSpecialRowsCteam:
                        level_id = levelSpecialRowsCteam.level_id
                        level_name = levelSpecialRowsCteam.level_name
                        depotid = str(levelSpecialRowsCteam.depot_id).strip() 
                        marketListCteam.append(level_id)     
                        if marketStrCteam == '':
                            marketStrCteam = str(level_id) + '<fd>' + str(level_name)
                        else:
                            marketStrCteam += '<rd>' + str(level_id) + '<fd>' + str(level_name)   
#                     return marketStrCteam        
                            

                                 
#                     return len(marketList)
#                     return marketStr

#                 return len(marketList)
                #-------------- Product list
                productStr = ''
                productRows = db(db.sm_company_settings.cid == cid).select(db.sm_company_settings.field1, limitby=(0,1))
                for productRow in productRows:
                    productStr = productRow.field1


                #-------------- Merchandizing list
                merchandizingStr = ''
                #-------------- Dealer list
                dealerStr = ''



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


               #------------Client Category list

                clienttCatStr = ''


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
                client_depot=''
                cliendepot_name=''
                
                for i in range(len(marketList)):
                    area_id = marketList[i]


                    clientStr = clientStr + '<' + area_id + '>'
#                     return clientStr
                    clientRows = db((db.sm_client.cid == cid) & (db.sm_client.area_id == marketList[i]) & (db.sm_client.status == 'ACTIVE')).select(db.sm_client.client_id, db.sm_client.name, db.sm_client.category_id,db.sm_client.depot_id,db.sm_client.depot_name,db.sm_client.market_name,db.sm_client.address, orderby=db.sm_client.name)

#                     return db._lastsql
                    if not clientRows:
                        clientStr = clientStr + 'Retailer not available' + '</' + area_id + '>'
#                         return retStatus
                    else:
                        
                        for clientRow in clientRows:
                            client_id = clientRow.client_id
                            name = clientRow.name
                            category_id = clientRow.category_id
                            address=clientRow.address
                            if len(address)>30:
                                address= str(clientRow.address)[30]
                            market_name=address+'-'+str(clientRow.market_name)
                            market_name = clientRow.market_name
                            if start_flag == 0:
                                client_depot=clientRow.depot_id
                                cliendepot_name=clientRow.depot_name
                                clientStr = clientStr + str(client_id) + '<fd>' + str(name)+' - '+str(market_name)  + ' <fd>' + str(category_id).strip().upper()
                                start_flag = 1
                            else:
                                clientStr = clientStr + '<rd>' + str(client_id) + '<fd>' + str(name) +' - '+str(market_name) + ' <fd>' + str(category_id).strip().upper()

                    clientStr = clientStr + '</' + area_id + '>'
                    clientStr=clientStr.replace("'","")
#                     return clientStr
 
#                 --------------------------------Market Client List End--------------------------------------


                #                 ------------------------------Menu List Start-----------------------------------------
#                 return len(marketList)
                menuStr = ''
                start_flag = 0
                menuRow = db((db.sm_mobile_settings_pharma.cid == cid) & (db.sm_mobile_settings_pharma.type == 'REP')).select(db.sm_mobile_settings_pharma.sl, db.sm_mobile_settings_pharma.s_key, db.sm_mobile_settings_pharma.s_value, orderby=db.sm_mobile_settings_pharma.sl)
                
                for menuRow in menuRow:
                    s_key = menuRow.s_key
                    s_value = menuRow.s_value

                    if start_flag == 0:
                        menuStr = menuStr + str(s_key) + '<fd>' + str(s_value) 
                        start_flag = 1
                    else:
                        menuStr = menuStr + '<rd>' + str(s_key) + '<fd>' + str(s_value) 

                
#                 return menuStr
#                 --------------------------------Menu List End--------------------------------------

#                ----------------------------Doctor list start-----------------------
                
                doctorStr = ''
                doctor_area_past=''
                srart_a_flag=0
                doctorStr_flag=0
                
                if cTeam==1: 
                    for i in range(len(marketListCteam)):
                        area_id = marketListCteam[i]
    #                 return len(marketList)
                        doctorRows = db((db.sm_doctor.cid == cid) & (db.sm_doctor.status == 'ACTIVE') & (db.sm_doctor_area.cid == cid) & (db.sm_doctor_area.doc_id == db.sm_doctor.doc_id) & (db.sm_doctor_area.area_id==area_id)).select(db.sm_doctor.doc_id, db.sm_doctor.doc_name, db.sm_doctor_area.area_id, orderby=db.sm_doctor_area.area_id|db.sm_doctor.doc_name)
        #                 return db._lastsql
                        if not doctorRows:
                            pass
        #                    retStatus = 'FAILED<SYNCDATA>Doctor not available'
        #                    return retStatus
                        else:
                             
                              
                            for doctorRow in doctorRows:
                                doctor_id = doctorRow.sm_doctor.doc_id
                                doctor_name = doctorRow.sm_doctor.doc_name
                                doctor_area = doctorRow.sm_doctor_area.area_id
                                if (doctor_area_past!=doctor_area):
                                      
                                    if (srart_a_flag==0):
                                        doctorStr=doctorStr+"<"+doctor_area+">"
                                          
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
                else:
                    for i in range(len(marketList)):
                        area_id = marketList[i]
#                         return area_id
                        doctorRows = db((db.sm_doctor.cid == cid) & (db.sm_doctor.status == 'ACTIVE') & (db.sm_doctor_area.cid == cid) & (db.sm_doctor_area.doc_id == db.sm_doctor.doc_id) & (db.sm_doctor_area.area_id==area_id)).select(db.sm_doctor.doc_id, db.sm_doctor.doc_name, db.sm_doctor_area.area_id, orderby=db.sm_doctor_area.area_id|db.sm_doctor.doc_name)
#                         return db._lastsql
                        if not doctorRows:
#                             return 'fgfgh'
                            pass
                        else:
#                             return doctorRow
                            for doctorRow in doctorRows:
                                doctor_id = doctorRow.sm_doctor.doc_id
                                doctor_name = doctorRow.sm_doctor.doc_name
                                doctor_area = doctorRow.sm_doctor_area.area_id
                                if (doctor_area_past!=doctor_area):
                                    if (srart_a_flag==0):
                                        doctorStr=doctorStr+"<"+doctor_area+">"
                                          
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
#                     return doctorStr
#             ----------------------------Doctor list end----------------------------------
                    
#                 return  doctorStr           
#                return 'SUCCESS<SYNCDATA>' + str(sync_code) + '<SYNCDATA>' + marketStr + '<SYNCDATA>' + productStr + '<SYNCDATA>' + merchandizingStr + '<SYNCDATA>' + dealerStr + '<SYNCDATA>' + brandStr + '<SYNCDATA>' + complainTypeStr + '<SYNCDATA>' + compFromStr + '<SYNCDATA>' + taskTypeStr + '<SYNCDATA>' + regionStr + '<SYNCDATA>' + giftStr + '<SYNCDATA>' + clienttCatStr + '<SYNCDATA>' + menuStr
                marketStr=marketStr.replace("'","")
                productStr=productStr.replace("'","")
                merchandizingStr =merchandizingStr.replace("'","")
                dealerStr=dealerStr.replace("'","")
                brandStr =brandStr.replace("'","")
                complainTypeStr=complainTypeStr.replace("'","")
                compFromStr =compFromStr.replace("'","")
                taskTypeStr =taskTypeStr.replace("'","")
                regionStr =regionStr.replace("'","")
                giftStr =giftStr.replace("'","")
                clienttCatStr =clienttCatStr.replace("'","")
                clientStr =clientStr.replace("'","")
                menuStr=menuStr.replace("'","")
                ppmStr =ppmStr.replace("'","")
                doctorStr =doctorStr.replace("'","")
                promo_str =promo_str.replace("'","")
                return 'SUCCESS<SYNCDATA>' + str(sync_code) + '<SYNCDATA>' + marketStr + '<SYNCDATA>' + productStr + '<SYNCDATA>' + merchandizingStr + '<SYNCDATA>' + dealerStr + '<SYNCDATA>' + brandStr + '<SYNCDATA>' + complainTypeStr + '<SYNCDATA>' + compFromStr + '<SYNCDATA>' + taskTypeStr + '<SYNCDATA>' + regionStr + '<SYNCDATA>' + giftStr + '<SYNCDATA>' + clienttCatStr + '<SYNCDATA>' + clientStr + '<SYNCDATA>' + menuStr+ '<SYNCDATA>' +ppmStr + '<SYNCDATA>' + user_type+ '<SYNCDATA>' +doctorStr + '<SYNCDATA>' +str(visit_save_limit)+'<SYNCDATA>'+str(visit_location)+'<SYNCDATA>'+str(delivery_date)+'<SYNCDATA>'+str(payment_date)+'<SYNCDATA>'+str(payment_mode)+'<SYNCDATA>'+str(collection_date)+'<SYNCDATA>'+str(promo_str)+'<SYNCDATA>'+str(client_depot)+'<SYNCDATA>'+str(cliendepot_name)+'<SYNCDATA>'+str(catStr)+'<SYNCDATA>'+str(spcStr)+'<SYNCDATA>'+str(marketStrCteam)+'<SYNCDATA>'+str(cTeam)
                
            else:
                return 'FAILED<SYNCDATA>Invalid Authorization'



#===================Check User End==========================

def visitSubmit_pharma():
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
    promo_ref = str(request.vars.bonus_combo)
    
#     if (promo_ref!='0'):
#         promo_ref=promo_ref.strip().replace(')','').split('(')[1]
        
    
    note = str(request.vars.chemist_feedback).strip() 
    location_detail = str(request.vars.location_detail).strip() 
#     return location_detail.find("LastLocation-")
    last_location=0
    if (location_detail.find("LastLocation-") > -1):
        last_location=1
        location_detail=location_detail.replace("LastLocation-","")
    else:
        pass
        
        
#     return location_detail
    visit_type = str(request.vars.visit_type).strip()  # scheduled,unscheduled
    sch_date = str(request.vars.schedule_date).strip()


    payment_mode = str(request.vars.payment_mode).strip().upper()
    
     
    delivery_date = str(request.vars.delivery_date).strip()
    collection_date = str(request.vars.collection_date).strip()
    version = str(request.vars.version).strip()
    
    if (version=='p1'):
        try:
            delivery_date = datetime.datetime.strptime(delivery_date, '%Y-%m-%d')
        except:
            try:
                delivery_date = datetime.datetime.strptime(delivery_date, '%d-%m-%Y')
            except:
                return 'FAILED<SYNCDATA>Invalid Delivery Date'
        
        try:
            collection_date = datetime.datetime.strptime(collection_date, '%Y-%m-%d')
    #        return abs((collection_date - current_date).days)
        except:
            try:
                collection_date = datetime.datetime.strptime(collection_date, '%d-%m-%Y')
            except:
                return 'FAILED<SYNCDATA>Invalid Collection Date'
    else:
        collection_date=current_date
        delivery_date=current_date
        
        
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
            clientRecords = db((db.sm_client.cid == cid) & (db.sm_client.client_id == client_id) & (db.sm_client.status == 'ACTIVE')).select(db.sm_client.name, db.sm_client.category_id, db.sm_client.area_id, db.sm_client.depot_id,db.sm_client.latitude,db.sm_client.longitude,db.sm_client.store_id,db.sm_client.store_name,db.sm_client.market_id,db.sm_client.market_name, limitby=(0, 1))
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
                store_id = str(clientRecords[0].store_id).strip()
                store_name = str(clientRecords[0].store_name).strip()
                market_id = str(clientRecords[0].market_id).strip()
                market_name = str(clientRecords[0].market_name).strip()
                
                tracking_table_latlong= str(client_lat)+","+str(client_long)
                
                regionid = ''
                areaid = ''
                terriroryid = ''
                                
                level0_id = ''
                level0_name = ''
                level1_id  = ''
                level1_name = ''
                level2_id  = ''
                level2_name = ''
                level3_id  = ''
                level3_name =''
                #-----
                levelRecords = db((db.sm_level.cid == cid)& (db.sm_level.is_leaf == '1') & (db.sm_level.level_id == route_id)).select(db.sm_level.level_id, db.sm_level.level_name, db.sm_level.depth, db.sm_level.level0, db.sm_level.level1, db.sm_level.level2, db.sm_level.level3,db.sm_level.level0_name, db.sm_level.level1_name, db.sm_level.level2_name, db.sm_level.level3_name, limitby=(0, 1))
                if not levelRecords:
                    return 'FAILED<SYNCDATA>Invalid Route'
                else:
                    route_name = levelRecords[0].level_name
                    regionid = levelRecords[0].level0
                    areaid = levelRecords[0].level1
                    terriroryid = levelRecords[0].level2
                    
                    level0_id = levelRecords[0].level0
                    level0_name = levelRecords[0].level0_name
                    level1_id  = levelRecords[0].level1
                    level1_name = levelRecords[0].level1_name
                    level2_id  = levelRecords[0].level2
                    level2_name = levelRecords[0].level2_name
                    level3_id  = levelRecords[0].level3
                    level3_name = levelRecords[0].level3_name


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

                try:
                    depotSlRow = db((db.sm_order_head.cid == cid) & (db.sm_order_head.depot_id == depot_id)&(db.sm_order_head.sl == ordSl)).select(db.sm_order_head.sl, limitby=(0, 1))
                    if depotSlRow:
                        depotRow = db((db.sm_depot.cid == cid) & (db.sm_depot.depot_id == depot_id)).select(db.sm_depot.id, db.sm_depot.name, db.sm_depot.order_sl, limitby=(0, 1))
                        if depotRow:
                            depot_name = depotRow[0].name
                            order_sl = int(depotRow[0].order_sl)
                            ordSl = order_sl + 1
                        depotRow[0].update_record(order_sl=ordSl)
                    insertRes = db.sm_order_head.insert(cid=cid, depot_id=depot_id, depot_name=depot_name, sl=ordSl,store_id=store_id,store_name=store_name, rep_id=rep_id, rep_name=rep_name,market_id=market_id,market_name=market_name, mobile_no=mobile_no, user_type=user_type, client_id=client_id, client_name=client_name, client_cat=client_cat, order_date=visit_date, order_datetime=visit_datetime,delivery_date=delivery_date,collection_date=collection_date, ym_date=firstDate, area_id=route_id, area_name=route_name, visit_type=visit_type, lat_long=lat_long,order_media='APP', status='Submitted', visit_image=visit_photo, payment_mode=payment_mode, field1=field1,note=str(note),location_detail=str(location_detail),last_location=str(last_location), level0_id = level0_id,  level0_name = level0_name,level1_id = level1_id,level1_name = level1_name,level2_id = level2_id,level2_name = level2_name,level3_id = level3_id,level3_name = level3_name,promo_ref=promo_ref )
                    vsl = db.sm_order_head(insertRes).id
                except:
                    try:
                        time.sleep(1)
                        ordSl = 0
                        depotRow = db((db.sm_depot.cid == cid) & (db.sm_depot.depot_id == depot_id)).select(db.sm_depot.id, db.sm_depot.name, db.sm_depot.order_sl, limitby=(0, 1))
                        if depotRow:
                            depot_name = depotRow[0].name
                            order_sl = int(depotRow[0].order_sl)
                            ordSl = order_sl + 1
                        depotRow[0].update_record(order_sl=ordSl)
                        insertRes = db.sm_order_head.insert(cid=cid, depot_id=depot_id, depot_name=depot_name, sl=ordSl,store_id=store_id,store_name=store_name, rep_id=rep_id, rep_name=rep_name,market_id=market_id,market_name=market_name, mobile_no=mobile_no, user_type=user_type, client_id=client_id, client_name=client_name, client_cat=client_cat, order_date=visit_date, order_datetime=visit_datetime,delivery_date=delivery_date,collection_date=collection_date, ym_date=firstDate, area_id=route_id, area_name=route_name, visit_type=visit_type, lat_long=lat_long,order_media='APP', status='Submitted', visit_image=visit_photo, payment_mode=payment_mode, field1=field1,note=str(note),location_detail=str(location_detail),last_location=str(last_location), level0_id = level0_id,  level0_name = level0_name,level1_id = level1_id,level1_name = level1_name,level2_id = level2_id,level2_name = level2_name,level3_id = level3_id,level3_name = level3_name,promo_ref=promo_ref )
                        vsl = db.sm_order_head(insertRes).id
                    except:
                        return 'FAILED<SYNCDATA>Please Try again'

                
                #                Client lat_long update
#                return client_lat
                if ((client_lat=='') | (client_lat=='0')| (client_long=='')| (client_long=='0')):
                    db((db.sm_client.cid == cid) & (db.sm_client.client_id == client_id)).update(latitude=latitude,longitude=longitude)

#                Insert in tracking table====================
                insertTracking = db.sm_tracking_table.insert(cid=cid, depot_id=depot_id, depot_name=depot_name, sl=ordSl, rep_id=rep_id, rep_name=rep_name,call_type='SELL',  visited_id=client_id, visited_name=client_name, visit_date=visit_date, visit_time=visit_datetime,  area_id=route_id, area_name=route_name, visit_type=visit_type, visited_latlong=lat_long,actual_latlong=tracking_table_latlong,location_detail=str(location_detail))  
                
                #--------- Order Info
                orderArrayList = []
                order_infoList = order_info.split('<rd>')
                for i in range(len(order_infoList)):
                    orderDataList = order_infoList[i].split('<fd>')
                    if len(orderDataList) == 2:
                        itemId = orderDataList[0]
                        itemQty = orderDataList[1]                       
                        ins_dict = {'cid':cid, 'vsl':vsl, 'depot_id':depot_id, 'depot_name':depot_name, 'sl':ordSl, 'store_id':store_id,'store_name':store_name,'client_id':client_id, 'client_name':client_name, 'rep_id':rep_id, 'rep_name':rep_name,'market_id':market_id,'market_name':market_name, 'order_date':visit_date, 'order_datetime':visit_datetime, 'ym_date':firstDate,'delivery_date':delivery_date,'payment_mode':payment_mode,'collection_date':collection_date,
                                                                           'area_id':route_id, 'area_name':route_name, 'item_id':itemId,'quantity':itemQty,'order_media':'APP', 'status':'Submitted', 'level0_id' : level0_id,  'level0_name' : level0_name,'level1_id' : level1_id,'level1_name' : level1_name,'level2_id' : level2_id,'level2_name' : level2_name,'level3_id' : level3_id,'level3_name' : level3_name}

                        orderArrayList.append(ins_dict)
                if len(orderArrayList) > 0:
                    db.sm_order.bulk_insert(orderArrayList)
#                     return "Update sm_order o , sm_item i  set o.item_name=i.name,o.category_id_sp=i.category_id_sp,o.price=i.price,o.item_vat=i.vat_amt, o.item_unit=i.unit_type,o.item_carton=i.item_carton where o.cid=i.cid AND o.item_id=i.item_id and o.cid='"+str(cid)+"' and o.vsl="+str(vsl)+" and o.depot_id="+str(depot_id)+" and o.sl="+str(ordSl)
                    updateRecords="Update sm_order o , sm_item i  set o.item_name=i.name,o.category_id=i.category_id,o.category_id_sp=i.category_id_sp,o.price=i.price,o.item_vat=i.vat_amt, o.item_unit=i.unit_type,o.item_carton=i.item_carton where o.cid=i.cid AND o.item_id=i.item_id and o.cid='"+str(cid)+"' and o.vsl="+str(vsl)+" and o.depot_id='"+str(depot_id)+"' and o.sl="+str(ordSl)
                    
                    
                    records=db.executesql(updateRecords) 


    return 'SUCCESS<SYNCDATA>' + str(vsl)





def doctor_visit_submit_pharma():
    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.rep_pass).strip()
    synccode = str(request.vars.synccode).strip()
    client_id = str(request.vars.client_id).strip().upper()
    routeID = str(request.vars.route).strip().upper()
    location_detail = str(request.vars.location_detail).strip()
    doc_others = str(request.vars.doc_others).strip()
#     return doc_others
    last_location=0
    if (location_detail.find("LastLocation-") != -1):
        last_location=1
        location_detail=location_detail.replace("LastLocation-","")
    else:
        pass
     
    visit_type = str(request.vars.visit_type).strip()  # scheduled,unscheduled
    sch_date = str(request.vars.schedule_date).strip()
 
    msg = str(request.vars.msg).strip().decode("ascii", "ignore")
#     return msg
 
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
            if len(myStrList)>3:
                ppmPart = str(myStrList[4]).strip().upper()
            else:
                ppmPart=''
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
                docLRows = db((db.sm_doctor_area.cid == cid) & (db.sm_doctor_area.doc_id == doctorID) & (db.sm_doctor_area.area_id == routeID)).select(db.sm_doctor_area.area_id, db.sm_doctor_area.area_name, db.sm_doctor_area.depot_id, db.sm_doctor_area.field1, limitby=(0, 1))
                docRouteRows = db((db.sm_client.cid == cid) & (db.sm_client.area_id == routeID)).select(db.sm_client.depot_id, limitby=(0, 1))
#                 return docRouteRows
                docARows = db((db.sm_level.cid == cid) & (db.sm_level.level_id == routeID)).select(db.sm_level.ALL, limitby=(0, 1))
#                 return docARows
                if not (docRouteRows or docLRows or docARows):
                    errorFlag = 1
                    errorMsg = 'Invalid route for the doctor'
                else:
                    if docRouteRows:
                        depotID = docRouteRows[0].depot_id
                    else:
                        depotID=''
                    routeID = docLRows[0].area_id
                     
                    areaID = docLRows[0].area_id
                    areaName = docLRows[0].area_name
                    tracking_table_latlong = docLRows[0].field1
                     
                    level0_id = docARows[0].level0
                    level0_name = docARows[0].level0_name
                    level1_id = docARows[0].level1
                    level1_name = docARows[0].level1_name
                    level2_id = docARows[0].level2
                    level2_name = docARows[0].level2_name
                    level3_id = docARows[0].level3
                    level3_name = docARows[0].level3_name
             
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
#     return proposedPart
    proposedStr = ''
    if errorFlag == 0:
        if proposedPart != '':
            propItemList = proposedPart.split(',')
            for i in range(len(propItemList)):
                proposedStr_single=str(propItemList[i]).strip().split('|')
                if len(proposedStr_single)>0:
                    itemID = proposedStr_single[0]
                    itemName=proposedStr_single[1]
                    if proposedStr == '':
                        proposedStr = itemID + ',' + str(itemName).replace(',', ' ')
                    else:
                        proposedStr += 'fdsep' + itemID + ',' + str(itemName).replace(',', ' ')
 
 
    #------------- gift part
     
#    return errorFlag
    giftStr = ''
    if errorFlag == 0:
#         return giftPart
        if len(giftPart) > 5:
            giftList = giftPart.split('.')
            for i in range(len(giftList)):
                gftIdQty = str(giftList[i]).strip()
                gftIdList = gftIdQty.split(',')
                giftLCheck=gftIdList[1].split('|')
                if len(giftLCheck)>0:
                    gftID = gftIdList[1].split('|')[0]
                    giftName=gftIdList[1].split('|')[1]
                    gftQty = int(gftIdList[0])
                    if (int(gftQty) > 0):
                        if giftStr == '':
                            giftStr = gftID + ',' + str(giftName).replace(',', ' ') + ',' + str(gftQty)
                        else:
                            giftStr += 'fdsep' + gftID + ',' + str(giftName).replace(',', ' ') + ',' + str(gftQty)
    #                        return giftStr
 
     
     
    #----- ppm part start
#    return errorFlag
    ppmStr = ''
    if errorFlag == 0:
#                 return giftPart
        if ppmPart != '':
            ppmList = ppmPart.split('.')
            for i in range(len(ppmList)):
                ppmIdQty = str(ppmList[i]).strip()
                ppmIdList = ppmIdQty.split(',')
                ppmLCheck=ppmIdList[1].split('|')
                if len(ppmLCheck)>0:
                    ppmID = ppmIdList[1].split('|')[0]
                    ppmName=ppmIdList[1].split('|')[1]
                    ppmQty = int(ppmIdList[0])
                    if (int(ppmQty) > 0):
                        if ppmStr == '':
                            ppmStr = ppmID + ',' + str(ppmName).replace(',', ' ') + ',' + str(ppmQty)
                        else:
                            ppmStr += 'fdsep' + ppmID + ',' + str(ppmName).replace(',', ' ') + ',' + str(ppmQty)
#                     return giftStr
 
     
#    -------------Sample part end
     
    #----- sample part
     
 
    samplePart=str(samplePart).replace(',.', ' ').replace('.,', ' ').replace('UNDEFINED', ' ')
     
    sampleStr = ''
    if errorFlag == 0:
        if samplePart != '':
             
            sampleList = samplePart.split('.')
            for i in range(len(sampleList)):
                smpIdQty = str(sampleList[i]).strip()
                smpIdList = smpIdQty.split(',')
                smpLCheck=smpIdList[1].split('|')
                if len(smpLCheck)>0:
                    smpID = smpIdList[1].split('|')[0]
                    smpName=smpIdList[1].split('|')[1]
                    smpQty = int(smpIdList[0])
                    if (int(smpQty) > 0):
                        if sampleStr == '':
                            sampleStr = smpID + ',' + str(smpName).replace(',', ' ') + ',' + str(smpQty)
                        else:
                            sampleStr += 'fdsep' + smpID + ',' + str(smpName).replace(',', ' ') + ',' + str(smpQty)
 
 
 
 
 
 
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
 
         
        insRes = db.sm_doctor_visit.insert(cid=cid, doc_id=doctorID, doc_name=docName, rep_id=rep_id, rep_name=rep_name, feedback=notesPart, ho_status='0', route_id=routeID,route_name=areaName, depot_id=depotID, visit_dtime=datetime_fixed, visit_date=current_date, giftnsample=itemngiftnsample,latitude = latitude, longitude = longitude, note=v_with,field1=doc_others,level0_id = level0_id,level0_name = level0_name,level1_id = level1_id,level1_name = level1_name,level2_id = level2_id,level2_name = level2_name,level3_id = level3_id,level3_name =level3_name)
#         return db._lastsql
         
         
        lat_long=str(latitude)+','+str(longitude)
        if (tracking_table_latlong=="0,0"):
            insRes =db((db.sm_doctor_area.cid == cid) & (db.sm_doctor_area.doc_id == doctorID) & (db.sm_doctor_area.area_id == areaID)).update(field1=lat_long)
         
#        return depotName
#         insertTracking = db.sm_tracking_table.insert(cid=cid, depot_id=depotID, depot_name=depotName, sl="0", rep_id=rep_id, rep_name=rep_name,call_type='DCR',  visited_id=doctorID, visited_name=docName, visit_date=current_date, visit_time=datetime_fixed,  area_id=routeID, area_name=routeName, visit_type=visit_type, visited_latlong=lat_long, actual_latlong=tracking_table_latlong, location_detail=str(location_detail),last_location=str(last_location)) 
         
        return 'SUCCESS<SYNCDATA>'






def infoPromo():
    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.rep_pass).strip()
    synccode = str(request.vars.synccode).strip()
    compRow = db((db.sm_company_settings.cid == cid) & (db.sm_company_settings.status == 'ACTIVE')).select(db.sm_company_settings.cid, limitby=(0, 1))
    if not compRow:
        return 'FAILED<SYNCDATA>Invalid Company'
    else:
        repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.sync_code == synccode) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.rep_id, db.sm_rep.name, db.sm_rep.mobile_no, db.sm_rep.user_type, db.sm_rep.level_id, db.sm_rep.depot_id, limitby=(0, 1))

       
        if not repRow:
           return 'FAILED<SYNCDATA>Invalid Authorization'

        else:
            #                  Bonus rate==================
#             bonusString='<font style="font-size:18px" >Bonus:<br></font><table width="100%" border="1" cellpadding="0" cellspacing="0" style="border:solid; border-style:solid"><tr style="font-size:16px; font-weight:bold"><td width="80%">Product</td><td width="20%">Bonus</td></tr>'     
            bonusString='<font style="font-size:18px; color:#306161" >Bonus:<br></font><table width="100%" border="1" cellpadding="0" cellspacing="0" style="border:solid; border-style:solid; border-color:#0CF; color:#306161"><tr style="font-size:16px; font-weight:bold"><td width="80%">Offer<td width="10%" align="center">MinQty</td></tr>'
#             itemBonusRows = db((db.sm_promo_product_bonus_products.cid == cid) & (db.sm_promo_product_bonus_products.from_date <= current_date)  & (db.sm_promo_product_bonus_products.to_date >= current_date) ).select(db.sm_promo_product_bonus_products.product_id,db.sm_promo_product_bonus_products.product_name, db.sm_promo_product_bonus_products.note, orderby=db.sm_promo_product_bonus_products.product_name)
            itemBonusRows = db((db.sm_promo_product_bonus.cid == cid) & (db.sm_promo_product_bonus.status == 'ACTIVE') & (db.sm_promo_product_bonus.from_date <= current_date)  & (db.sm_promo_product_bonus.to_date >= current_date) ).select(db.sm_promo_product_bonus.note,db.sm_promo_product_bonus.circular_number, db.sm_promo_product_bonus.min_qty, orderby=db.sm_promo_product_bonus.note)
            for itemBonusRows in itemBonusRows:
#                 product_id = itemBonusRows.product_id      
#                 product_name = itemBonusRows.product_name       
#                 note = itemBonusRows.note
                min_qty = itemBonusRows.min_qty      
                circular_number = itemBonusRows.circular_number       
                note = itemBonusRows.note
                
                bonusString=bonusString+'<tr style="font-size:14px"><td >'+str(note)+'</td><td align="center">'+str(min_qty)+'</td></tr>'

                 
#                 bonusString=bonusString+'<tr style="font-size:14px"><td >'+str(product_name)+' ('+str(product_id)+')'+'</td><td >'+str(note)+'</td></tr>'

            bonusString=bonusString+'</table>'
            
#                  Special rate==================
            specialRate='<font style="font-size:18px;color:#306161" >Special Rate:<br></font><table width="100%" border="1" cellpadding="0" cellspacing="0" style="border:solid; border-style:solid; border-color:#0CF; color:#306161"><tr style="font-size:16px; font-weight:bold"><td width="80%">Product</td><td align="center">MinQty</td><td align="right">Rate</td></tr>'     
            itemSpecial_str=''
            itemSpecialRows = db((db.sm_promo_special_rate.cid == cid) & (db.sm_promo_special_rate.status == 'ACTIVE')  & (db.sm_promo_special_rate.from_date <= current_date)  & (db.sm_promo_special_rate.to_date >= current_date) ).select(db.sm_promo_special_rate.product_id,db.sm_promo_special_rate.product_name, db.sm_promo_special_rate.special_rate_tp, db.sm_promo_special_rate.special_rate_vat,db.sm_promo_special_rate.min_qty, orderby=db.sm_promo_special_rate.product_name)
            for itemSpecialRows in itemSpecialRows:
                product_id = itemSpecialRows.product_id      
                product_name = itemSpecialRows.product_name       
                special_rate_tp = itemSpecialRows.special_rate_tp
                special_rate_vat = itemSpecialRows.special_rate_vat
                min_qty=itemSpecialRows.min_qty
                
                                
#                 itemSpecialList_str=itemSpecialList_str+'Special:Min '+str(min_qty)+' TP ' +str(special_rate_tp)+' Vat'+str(special_rate_vat)+'='+str(total)+'<fdfd>'
                
                specialRate=specialRate+'<tr style="font-size:14px"><td >'+str(product_name)+' ('+str(product_id)+')'+'</td><td align="center">'+str(min_qty)+'</td><td align="right">'+str(special_rate_tp)+'</td></tr>'
                
                itemSpecial_str=itemSpecial_str+str(product_id)+'<fd>'+'product: '+str(product_name)+' ('+str(product_id)+')'+'Special Rate:'+str(special_rate_tp)+'  Special Vat:'+str(special_rate_vat)+"<br>"
            specialRate=specialRate+'</table>'
        
        #     Flat rate==================

            itemFlatRows = db((db.sm_promo_flat_rate.cid == cid)  & (db.sm_promo_flat_rate.status == 'ACTIVE') & (db.sm_promo_flat_rate.from_date <= current_date)  & (db.sm_promo_flat_rate.to_date >= current_date) ).select(db.sm_promo_flat_rate.product_id,db.sm_promo_flat_rate.product_name, db.sm_promo_flat_rate.min_qty, db.sm_promo_flat_rate.flat_rate, orderby=db.sm_promo_flat_rate.product_name)
            
            flarRate='<font style="font-size:18px;color:#306161" >Flat Rate:<br></font><table width="100%" border="1" cellpadding="0" cellspacing="0" style="border:solid; border-style:solid; border-color:#0CF; color:#306161"><tr style="font-size:16px; font-weight:bold"><td width="80%">Product</td><td align="center">MinQty</td><td align="right">FlatRate</td></tr>'
            itemFlat_str=''
            for itemFlatRows in itemFlatRows:
                product_id = itemFlatRows.product_id
                product_name = itemFlatRows.product_name
                flat_rate = itemFlatRows.flat_rate
                min_qty = itemFlatRows.min_qty      
                flarRate=flarRate+'<tr style="font-size:14px"><td >'+str(product_name)+' ('+str(product_id)+')'+'</td><td align="center">'+str(min_qty)+'</td><td align="right">'+str(flat_rate)+'</td></tr>'
#                 flarRate=flarRate+'product: '+str(product_name)+' | '+str(product_id)+'Minimum Qty:'+str(min_qty)+'  Flat Rate:'+str(flat_rate)+'<br>'
                itemFlat_str=itemFlat_str+'Flat:Min '+str(min_qty)+' Rate '+str(flat_rate)+'fdfd'
                
                
            flarRate=flarRate+'</table>'
            
            
            #     sm_promo_declared_item rate==================

            itemDeclearedRows = db((db.sm_promo_declared_item.cid == cid)  & (db.sm_promo_declared_item.status == 'ACTIVE')  ).select(db.sm_promo_declared_item.product_id,db.sm_promo_declared_item.product_name, db.sm_promo_declared_item.approved_date, orderby=db.sm_promo_declared_item.product_name)
            
            declearedRate='<font style="font-size:18px;color:#306161" >Declared Item:<br></font><table width="100%" border="1" cellpadding="0" cellspacing="0" style="border:solid; border-style:solid; border-color:#0CF; color:#306161"><tr style="font-size:16px; font-weight:bold"><td width="80%">Product</td><td >ApprovedDate</td></tr>'
            for itemDeclearedRows in itemDeclearedRows:
                product_id = itemDeclearedRows.product_id
                product_name = itemDeclearedRows.product_name
                approved_date = itemDeclearedRows.approved_date
#                 return approved_date
                declearedRate=declearedRate+'<tr style="font-size:14px"><td >'+str(product_name)+' ('+str(product_id)+')'+'</td><td >'+str(approved_date)+'</td></tr>'

            
            declearedRate=declearedRate+'</table>'
    
            retStatus = 'SUCCESS<SYNCDATA>'+bonusString+'<br><br>'+specialRate+'<br><br>'+flarRate+'<br><br>'+declearedRate
            return retStatus
# ======================Inbox
def infoInbox():
    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.rep_pass).strip()
    synccode = str(request.vars.synccode).strip()
    compRow = db((db.sm_company_settings.cid == cid) & (db.sm_company_settings.status == 'ACTIVE')).select(db.sm_company_settings.cid, limitby=(0, 1))
    if not compRow:
        return 'FAILED<SYNCDATA>Invalid Company'
    else:
        repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.sync_code == synccode) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.rep_id, db.sm_rep.name, db.sm_rep.mobile_no, db.sm_rep.user_type, db.sm_rep.level_id, db.sm_rep.depot_id, limitby=(0, 1))

        
        if not repRow:
           return 'FAILED<SYNCDATA>Invalid Authorization'

        else:
#                  Special rate==================
            inbox_str='<font style="font-size:18px" >Inbox:<br></font><table width="100%" border="0"><tr style="font-size:16px"><td width="20%">From</td><td >MSG</td></tr>'     
            inboxRows = db((db.sm_inbox.cid == cid) & (db.sm_inbox.sms_date <= current_date) & (db.sm_inbox.to_sms == rep_id) ).select(db.sm_inbox.ALL, orderby=~db.sm_inbox.id , limitby=(0,10))

            for inboxRows in inboxRows:
                sl = inboxRows.sl    
                from_sms = inboxRows.from_sms 
                to_sms = inboxRows.to_sms 
                mobile_no = inboxRows.mobile_no 
                sms= inboxRows.sms 

                inbox_str=inbox_str+'<tr><td>'+str(from_sms)+'</td><td>'+str(sms)+'</td></tr>'
            inbox_str=inbox_str+'</table>'
        
       
            retStatus = 'SUCCESS<SYNCDATA>'+inbox_str
            return retStatus

# ============================Kpi
def infoKpi():
    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.rep_pass).strip()
    synccode = str(request.vars.synccode).strip()
    compRow = db((db.sm_company_settings.cid == cid) & (db.sm_company_settings.status == 'ACTIVE')).select(db.sm_company_settings.cid, limitby=(0, 1))
    if not compRow:
        return 'FAILED<SYNCDATA>Invalid Company'
    else:
        repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.sync_code == synccode) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.rep_id, db.sm_rep.name, db.sm_rep.mobile_no, db.sm_rep.user_type, db.sm_rep.level_id, db.sm_rep.depot_id, limitby=(0, 1))

        
        if not repRow:
           return 'FAILED<SYNCDATA>Invalid Authorization'

        else:
            kpi_str=''
            kpi_str='KPI'
#                  Special rate==================
#             inbox_str='<font style="font-size:18px" >Inbox:<br></font><table width="100%" border="0"><tr style="font-size:16px"><td width="20%">From</td><td >MSG</td></tr>'     
#             inboxRows = db((db.sm_inbox.cid == cid) & (db.sm_inbox.sms_date <= current_date) & (db.sm_inbox.to_sms == rep_id) ).select(db.sm_inbox.ALL, orderby=~db.sm_inbox.id , limitby=(0,10))
# 
#             for inboxRows in inboxRows:
#                 sl = inboxRows.sl    
#                 from_sms = inboxRows.from_sms 
#                 to_sms = inboxRows.to_sms 
#                 mobile_no = inboxRows.mobile_no 
#                 sms= inboxRows.sms 
# 
#                 inbox_str=inbox_str+'<tr><td>'+str(from_sms)+'</td><td>'+str(sms)+'</td></tr>'
#             inbox_str=inbox_str+'</table>'
        
       
            retStatus = 'SUCCESS<SYNCDATA>'+kpi_str
            return retStatus


# =================Promo=======================

# ===============================Help
def infoHelp():
    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.rep_pass).strip()
    synccode = str(request.vars.synccode).strip()
    compRow = db((db.sm_company_settings.cid == cid) & (db.sm_company_settings.status == 'ACTIVE')).select(db.sm_company_settings.cid, limitby=(0, 1))
    if not compRow:
        return 'FAILED<SYNCDATA>Invalid Company'
    else:
        repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.sync_code == synccode) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.rep_id, db.sm_rep.name, db.sm_rep.mobile_no, db.sm_rep.user_type, db.sm_rep.level_id, db.sm_rep.depot_id, limitby=(0, 1))

        
        if not repRow:
           return 'FAILED<SYNCDATA>Invalid Authorization'

        else:
            help_str=''
            help_str='Help'
#                  Special rate==================
#             inbox_str='<font style="font-size:18px" >Inbox:<br></font><table width="100%" border="0"><tr style="font-size:16px"><td width="20%">From</td><td >MSG</td></tr>'     
#             inboxRows = db((db.sm_inbox.cid == cid) & (db.sm_inbox.sms_date <= current_date) & (db.sm_inbox.to_sms == rep_id) ).select(db.sm_inbox.ALL, orderby=~db.sm_inbox.id , limitby=(0,10))
# 
#             for inboxRows in inboxRows:
#                 sl = inboxRows.sl    
#                 from_sms = inboxRows.from_sms 
#                 to_sms = inboxRows.to_sms 
#                 mobile_no = inboxRows.mobile_no 
#                 sms= inboxRows.sms 
# 
#                 inbox_str=inbox_str+'<tr><td>'+str(from_sms)+'</td><td>'+str(sms)+'</td></tr>'
#             inbox_str=inbox_str+'</table>'
        
       
            retStatus = 'SUCCESS<SYNCDATA>'+help_str
            return retStatus



def depot_wise_stock_report():
    
    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.rep_pass).strip()
    synccode = str(request.vars.synccode).strip()
    client_depot = str(request.vars.client_depot).strip()
    client_depot_name=str(request.vars.client_depot_name).strip().upper()
    today=datetime.datetime.strptime(current_date,'%Y-%m-%d')
    compRow = db((db.sm_company_settings.cid == cid) & (db.sm_company_settings.status == 'ACTIVE')).select(db.sm_company_settings.cid, limitby=(0, 1))
    if not compRow:
        return 'FAILED<SYNCDATA>Invalid Company'
    else:
        repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.sync_code == synccode) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.rep_id, db.sm_rep.name, db.sm_rep.mobile_no, db.sm_rep.user_type, db.sm_rep.level_id, db.sm_rep.depot_id, limitby=(0, 1))

        
        if not repRow:
           return 'FAILED<SYNCDATA>Invalid Authorization'

        else:
            
                depot_id=client_depot
                depot_name=client_depot_name
                

                stockBalanceRecords=db((db.sm_depot_stock_balance.cid==cid)&(db.sm_depot_stock_balance.depot_id==depot_id) & (db.sm_item.cid==cid) & (db.sm_depot_stock_balance.item_id==db.sm_item.item_id)).select(db.sm_depot_stock_balance.ALL,(db.sm_depot_stock_balance.quantity-db.sm_depot_stock_balance.block_qty).sum(),db.sm_item.name,db.sm_item.unit_type,groupby=db.sm_depot_stock_balance.item_id,orderby=db.sm_item.name)
                
#                 stockBalance_str='<table width="500" border="1" cellpadding="0" cellspacing="0" style="border:solid; border-style:solid">'
#                 stockBalance_str=stockBalance_str+'<tr ><td width="100" style="padding-left:0px;"><b>Depot ID</b></td><td width="5"><b>:</b></td><td width="300" align="left">'+str(depot_id) +'</td></tr>'
#                 stockBalance_str=stockBalance_str+'<tr ><td width="100" style="padding-left:0px;"><b>Depot Name<</b></td><td width="5"><b>:</b></td><td width="300" align="left">'+str(depot_name) +'</td></tr>'
#                 stockBalance_str=stockBalance_str+'</table>'



                stockBalance_str='<font style="color:#306161">'+'Depot ID :'+str(depot_id) +'</br>'
                stockBalance_str=stockBalance_str+'Depot Name :'+str(depot_name) +'</br></br></font>'
                

              


                
                stockBalance_str=stockBalance_str+'<table width="600" border="1" cellpadding="0" cellspacing="0" style="border:solid; border-style:solid; border-color:#0CF; color:#306161"> <tr style="font-size:16px; font-weight:bold">'

#                 stockBalance_str=stockBalance_str+'<td  width="50">Item ID </td> '
                stockBalance_str=stockBalance_str+'<td width="20" align="right">Stock</td>'
                stockBalance_str=stockBalance_str+'<td >&nbsp;&nbsp;Product</td></tr>'
                

                stockBalance_str_show=''
                start_flag=0
                for record in stockBalanceRecords:                   
                    item_id=record.sm_depot_stock_balance.item_id
                    quantity=record[(db.sm_depot_stock_balance.quantity-db.sm_depot_stock_balance.block_qty).sum() ]                 
                    itemName=record.sm_item.name
                   
                    if start_flag==0:
                        stockBalance_str_show= str(item_id)+'<fd>'+str(quantity)
                        start_flag=1
                    else:
                        stockBalance_str_show= stockBalance_str_show+'<rd>'+str(item_id)+'<fd>'+str(quantity)
                        

                    stockBalance_str=stockBalance_str+'<tr>'
#                     stockBalance_str=stockBalance_str+' <td >'+str(item_id)+'</td>'
                    stockBalance_str=stockBalance_str+'<td  align="right">'+str(quantity)+'</td>'
                    stockBalance_str=stockBalance_str+' <td >&nbsp;&nbsp;'+str(itemName)+'( '+str(item_id)+' )'+'</td>'
                    stockBalance_str=stockBalance_str+' </tr> '

          

                stockBalance_str=stockBalance_str+'</table>'
#                 return stockBalance_str_show
                return 'SUCCESS<SYNCDATA>'+stockBalance_str+'<SYNCDATA>'+stockBalance_str_show

# ============================================
def client_outstanding_report():
    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.rep_pass).strip()
    synccode = str(request.vars.synccode).strip()
    client = str(request.vars.client).strip()
#     return client
    
    compRow = db((db.sm_company_settings.cid == cid) & (db.sm_company_settings.status == 'ACTIVE')).select(db.sm_company_settings.cid, limitby=(0, 1))
    if not compRow:
        return 'FAILED<SYNCDATA>Invalid Company'
    else:
        repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.sync_code == synccode) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.rep_id, db.sm_rep.name, db.sm_rep.mobile_no, db.sm_rep.user_type, db.sm_rep.level_id, db.sm_rep.depot_id, limitby=(0, 1))

        
        if not repRow:
           return 'FAILED<SYNCDATA>Invalid Authorization'

        else:
            qset=db()
            qset=qset(db.sm_invoice_head.cid==cid)
            qset=qset(db.sm_invoice_head.status=='Invoiced')
            qset=qset(db.sm_invoice_head.client_id==client)
            
                    
               
            records=qset.select(db.sm_invoice_head.sl,db.sm_invoice_head.invoice_date,db.sm_invoice_head.client_id,db.sm_invoice_head.client_name,db.sm_invoice_head.payment_mode,db.sm_invoice_head.area_id,db.sm_invoice_head.total_amount,db.sm_invoice_head.vat_total_amount,db.sm_invoice_head.discount,db.sm_invoice_head.return_tp,db.sm_invoice_head.return_vat,db.sm_invoice_head.return_discount,db.sm_invoice_head.collection_amount,orderby=~db.sm_invoice_head.invoice_date)
            if records:  
                for record_name in records:  
                    client_name =record_name.client_name 
                    break  
                
                outstanding_str='<table width="500" border="0" cellspacing="0" cellpadding="0" style="color:#306161">'
                outstanding_str=outstanding_str+'<tr ><td width="100" style="padding-left:0px;"><b>Customer ID</b></td><td width="5"><b>:</b></td><td width="300" align="left">'+str(client) +'</td></tr>'
                outstanding_str=outstanding_str+'<tr ><td width="100" style="padding-left:0px;"><b>Customer Name</b></td><td width="5"><b>:</b></td><td width="300" align="left">'+str(client_name) +'</td></tr>'
                records_credit=db((db.sm_cp_approved.cid==cid) & (db.sm_cp_approved.client_id==client) & (db.sm_cp_approved.status=='ACTIVE')).select(db.sm_cp_approved.approved_date,db.sm_cp_approved.credit_amount,orderby=~db.sm_cp_approved.approved_date, limitby=(0,1))
                approved_date=''
                credit_amount=''
                for records_credit in records_credit:
                    approved_date =records_credit.approved_date   
                    credit_amount =records_credit.credit_amount 
#                     return approved_date
                    outstanding_str=outstanding_str+'<tr ><td width="100" style="padding-left:0px;"><b>Credit</b></td><td width="5"><b>:</b></td><td width="300" align="left">'+str(credit_amount) +'  <font style="font-size:12px; color:#006A6A"> Approved '+str(approved_date)+'</font></td></tr>'
                    
                    
                
                
                outstanding_str=outstanding_str+'</table><br>'
                
                 
    
    
                  
    
    
                    
                outstanding_str=outstanding_str+'<table width="600" border="1" cellpadding="0" cellspacing="0" style="border:solid; border-style:solid; border-color:#0CF; color:#306161"> <tr class="table_title">'
    
                outstanding_str=outstanding_str+'<td  width="100">Date </td> '
                outstanding_str=outstanding_str+'<td  width="50">InvNo</td>'
                outstanding_str=outstanding_str+'<td width="50"> Terms</td>'
                outstanding_str=outstanding_str+'<td width="50" align="right">TP</td>'
                outstanding_str=outstanding_str+'<td width="50" align="right">VAT</td>'
                outstanding_str=outstanding_str+'<td width="50" align="right">Disc</td>'
                outstanding_str=outstanding_str+'<td width="50" align="right">InvAmt</td>'
                outstanding_str=outstanding_str+'<td width="50" align="right">RetAmt</td>'
                outstanding_str=outstanding_str+'<td width="50" align="right">OutStanding</td>'
                outstanding_str=outstanding_str+'<td width="50" align="right">%</td></tr>'

              
               
                for record in records:                   
                    invoice_date=record.invoice_date
    #                 quantity=record[db.sm_depot_stock_balance.quantity.sum() ]                 
                    sl=record.sl
                    client_id=record.client_id
                    client_name =record.client_name   
                    payment_mode=record.payment_mode
                    area_id=record.area_id
                    total_amount=record.total_amount
                    vat_total_amount=record.vat_total_amount
                    discount=record.discount
                    return_tp=record.return_tp
                    return_vat=record.return_vat
                    return_discount=record.return_discount
                    collection_amount=record.collection_amount
                    
                    return_amt=float(record.return_tp)+float(record.return_vat)-float(record.return_discount)
                    outstanding=float(record.total_amount)-float(record.collection_amount)-float(return_amt)
                    
                    outstanding_str+'<tr>'
                    outstanding_str=outstanding_str+' <td >'+str(invoice_date)+'</td>'
                    outstanding_str=outstanding_str+' <td >'+str(sl)+'</td>'
                    
                    outstanding_str=outstanding_str+' <td >'+str(payment_mode)+'</td>'
                    outstanding_str=outstanding_str+' <td align="right">'+str(float(total_amount)-float(vat_total_amount)+float(discount))+'</td>'
                    outstanding_str=outstanding_str+' <td align="right">'+str(vat_total_amount)+'</td>'
                    
                    
                    outstanding_str=outstanding_str+' <td align="right">'+str(discount)+'</td>'
                    outstanding_str=outstanding_str+' <td align="right">'+str(total_amount)+'</td>'
                    outstanding_str=outstanding_str+' <td align="right">'+str(return_amt)+'</td>'
                    outstanding_str=outstanding_str+'<td  align="right">'+str(outstanding)+'</td>'
                    
                    if record.total_amount!=0:
                        show_out=round((outstanding/record.total_amount*100),2)
                    else:
                        show_out=0
                    outstanding_str=outstanding_str+'<td  align="right">'+str(show_out)+'</td>'
                    outstanding_str=outstanding_str+' </tr> '
    
                
                
                outstanding_str=outstanding_str+'</table>'+'<br><br><br><br><br>' 
            else:
                outstanding_str= 'No Outstanding'+'<br><br><br><br><br>' 
            
    return 'SUCCESS<SYNCDATA>'+outstanding_str
            

#     Last order
# ============================================
def client_invoice_report():
    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.rep_pass).strip()
    synccode = str(request.vars.synccode).strip()
    client = str(request.vars.client).strip()
#     return client
     
    compRow = db((db.sm_company_settings.cid == cid) & (db.sm_company_settings.status == 'ACTIVE')).select(db.sm_company_settings.cid, limitby=(0, 1))
    if not compRow:
        return 'FAILED<SYNCDATA>Invalid Company'
    else:
        repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.sync_code == synccode) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.rep_id, db.sm_rep.name, db.sm_rep.mobile_no, db.sm_rep.user_type, db.sm_rep.level_id, db.sm_rep.depot_id, limitby=(0, 1))
 
         
        if not repRow:
           return 'FAILED<SYNCDATA>Invalid Authorization'
 
        else:
            qset=db()
            qset=qset(db.sm_invoice_head.cid==cid)
#             qset=qset(db.sm_invoice_head.status=='Invoiced')
            qset=qset(db.sm_invoice_head.client_id==client)
             
                     
                
            records=qset.select(db.sm_invoice_head.ALL,orderby=~db.sm_invoice_head.sl, limitby=(0,1))
          
            if records:  
                client_name =''
                depot_id=''
                depot_name=''
                store_id=''
                store_name=''
                sl =''
                rep_id=''
                rep_name=''
                d_man_id=''
                d_man_name=''
                order_sl=''              
                delivery_dt=''                   
                payment_mode=''                
                discount=''
                status=''
                note=''
                for record in records:  
                    client_name =record.client_name 
                    depot_id=record.depot_id 
                    depot_name=record.depot_name
                    store_id=record.store_id 
                    store_name=record.store_name 
                    sl =record.sl 
                    rep_id=record.rep_id 
                    rep_name=record.rep_name 
                    d_man_id=record.d_man_id 
                    d_man_name=record.d_man_name 
                    order_sl=record.order_sl                     
                    delivery_dt=record.delivery_date                    
                    payment_mode=record.payment_mode                     
                    discount=record.discount 
                    status=record.status 
                    note=record.note 
        


                    invoice_str='<table width="500" border="0" cellspacing="0" cellpadding="0" style="color:#306161">'
                    invoice_str=invoice_str+'<tr ><td width="100" style="padding-left:0px;"><b>Branch</b></td><td width="5"><b>:</b></td><td width="300" align="left">'+str(depot_name) + '('+str(depot_id) +')'+'</td></tr>'
                    invoice_str=invoice_str+'<tr ><td width="100" style="padding-left:0px;"><b>Store</b></td><td width="5"><b>:</b></td><td width="300" align="left">'+str(store_name) + '('+str(store_id) +')'+'</td></tr>'
                    invoice_str=invoice_str+'<tr ><td width="100" style="padding-left:0px;"><b>Customer</b></td><td width="5"><b>:</b></td><td width="300" align="left">'+str(client_name) + '('+str(client) +')'+'</td></tr>'
#                     invoice_str=invoice_str+'<tr ><td width="100" style="padding-left:0px;"><b>SL </b>'+str(sl)+'</td><td width="5"></td><td width="300" align="left"><b>Order SL </b>'+str(order_sl) +'</td></tr>'
                    invoice_str=invoice_str+'<tr ><td width="100" style="padding-left:0px;"><b>Invoice SL</b></td><td width="5"><b>:</b></td><td width="300" align="left">'+str(sl) +'</td></tr>'
                    invoice_str=invoice_str+'<tr ><td width="100" style="padding-left:0px;"><b>Order SL</b></td><td width="5"><b>:</b></td><td width="300" align="left">'+str(order_sl) +'</td></tr>'
                    invoice_str=invoice_str+'<tr ><td width="100" style="padding-left:0px;"><b>Rep</b></td><td width="5"><b>:</b></td><td width="300" align="left">'+str(rep_name) + '('+str(rep_id) +')'+'</td></tr>'
                    invoice_str=invoice_str+'<tr ><td width="100" style="padding-left:0px;"><b>D.Man</b></td><td width="5"><b>:</b></td><td width="300" align="left">'+str(d_man_name) + '('+str(d_man_id) +')'+'</td></tr>'
                    invoice_str=invoice_str+'<tr ><td width="100" style="padding-left:0px;"><b>DeliveryDate</b></td><td width="5"><b>:</b></td><td width="300" align="left">'+str(delivery_dt) +'</td></tr>'
                    invoice_str=invoice_str+'<tr ><td width="100" style="padding-left:0px;"><b>Payment Mode</b></td><td width="5"><b>:</b></td><td width="300" align="left">'+str(payment_mode) +'</td></tr>'
                    invoice_str=invoice_str+'<tr ><td width="100" style="padding-left:0px;"><b>Discount</b></td><td width="5"><b>:</b></td><td width="300" align="left">'+str(discount) +'</td></tr>'
                    invoice_str=invoice_str+'<tr ><td width="100" style="padding-left:0px;"><b>Status Mode</b></td><td width="5"><b>:</b></td><td width="300" align="left">'+str(status) +'</td></tr>'
                    invoice_str=invoice_str+'<tr ><td width="100" style="padding-left:0px;"><b>Notes</b></td><td width="5"><b>:</b></td><td width="300" align="left">'+str(note) +'</td></tr>'
                    invoice_str=invoice_str+'</table>'                    

 
                qset_detail=db()
                qset_detail=qset_detail(db.sm_invoice.cid==cid)
                qset_detail=qset_detail(db.sm_invoice.depot_id==depot_id)
                qset_detail=qset_detail(db.sm_invoice.sl==sl)
                qset_detail=qset_detail(db.sm_invoice.client_id==client)
                 
                         
                    
                records_detail=qset_detail.select(db.sm_invoice.ALL,orderby=~db.sm_invoice.item_name)
#                 return records_detail
                if records_detail:  
                    item_id =''
                    item_name =''
                    batch_id=''
                    category_id =''
                    quantity=''
                    bonus_qty =''
                    price=''
                    gross_total=0
                    invoice_str=invoice_str+"""<table width="700" border="1" cellpadding="0" cellspacing="0" style="border:solid; border-style:solid; border-color:#0CF; color:#306161"> 
                        <tr align="left" class="blackCatHead"  >
                        <td width="50">ID</td>
                        <td width="150" >Name</td>
                        <td width="50" align="center" >Category</td>
                        <td width="50"   >BatchID</td>
                        <td width="50" align="center"  >Qty</td>
                        <td width="50" align="center"  >BonusQty </td>
                        <td width="50" align="right"  >TP</td>
                        <td width="50" align="right"  >Vat</td>
                        <td width="50" align="right"  >Amount </td>
                        <td align="center"  >Short Note </td></tr>"""
                    for records_detail in records_detail:  
                        item_id     =records_detail.item_id 
                        item_name   =records_detail.item_name 
                        batch_id    =records_detail.batch_id
                        category_id =records_detail.category_id 
                        quantity    =records_detail.quantity 
                        bonus_qty   =records_detail.bonus_qty 
                        price       =records_detail.price
                        item_vat =records_detail.item_vat
                        short_note=records_detail.short_note
                        
                        amt=quantity*(price+item_vat)
                        gross_total =float(gross_total)+ float(amt)
                                                  
                                                  
                        invoice_str=invoice_str+'<tr ><td style="padding-left:0px;">'+str(item_id)+'</td>'
                        invoice_str=invoice_str+'<td >'+str(item_name)+'</td>'
                       
                        invoice_str=invoice_str+'<td align="center" >'+str(category_id)+'</td>'
                        invoice_str=invoice_str+'<td >'+str(batch_id)+'</td>'
                        invoice_str=invoice_str+'<td align="center">'+str(quantity)+'</td>'
                        invoice_str=invoice_str+'<td align="center">'+str(bonus_qty)+'</td>'
                        invoice_str=invoice_str+'<td align="right">'+str(price)+'</td>'
                        invoice_str=invoice_str+'<td align="right">'+str(item_vat)+'</td>'
                        invoice_str=invoice_str+'<td align="right">'+str(amt)+'</td>'
                        
                        invoice_str=invoice_str+'<td >'+str(short_note)+'</td>'
                        invoice_str=invoice_str+'</tr>'#</table>'                    
                    
                    


                
                                                       
                    netTotal=float(gross_total)-float(discount)                              
                    invoice_str=invoice_str+'<tr ><td ></td>'
                    invoice_str=invoice_str+'<td ></td>'
                    invoice_str=invoice_str+'<td ></td>'
                    invoice_str=invoice_str+'<td ></td>'
                    invoice_str=invoice_str+'<td ></td>'
                    invoice_str=invoice_str+'<td ></td>'
                    invoice_str=invoice_str+'<td ></td>'
                    invoice_str=invoice_str+'<td >Total</td>'
                    invoice_str=invoice_str+'<td >'+str(gross_total)+'</td>'
                    invoice_str=invoice_str+'<td ></td></tr>'
                    
                    invoice_str=invoice_str+'<tr ><td ></td>'
                    invoice_str=invoice_str+'<td ></td>'
                    invoice_str=invoice_str+'<td ></td>'
                    invoice_str=invoice_str+'<td ></td>'
                    invoice_str=invoice_str+'<td ></td>'
                    invoice_str=invoice_str+'<td ></td>'
                    invoice_str=invoice_str+'<td ></td>'
                    invoice_str=invoice_str+'<td >Discount</td>'
                    invoice_str=invoice_str+'<td >'+str(discount)+'</td>'
                    invoice_str=invoice_str+'<td ></td></tr>'
                    
                    invoice_str=invoice_str+'<tr ><td ></td>'
                    invoice_str=invoice_str+'<td ></td>'
                    invoice_str=invoice_str+'<td ></td>'
                    invoice_str=invoice_str+'<td ></td>'
                    invoice_str=invoice_str+'<td ></td>'
                    invoice_str=invoice_str+'<td ></td>'
                    invoice_str=invoice_str+'<td ></td>'
                    invoice_str=invoice_str+'<td >NetTotal</td>'
                    invoice_str=invoice_str+'<td >'+str(netTotal)+'</td>'
                    invoice_str=invoice_str+'<td ></td></tr>'
                    invoice_str=invoice_str+'</tr></table>'                    
                    return 'SUCCESS<SYNCDATA>'+invoice_str
                else:
                    return 'SUCCESS<SYNCDATA>'+invoice_str
             
            else:
                return 'SUCCESS<SYNCDATA>'+'No Invoice' 
                    
                 
                 
                 
                 
# ===================================ClientOrder=========
def client_order_report():
    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.rep_pass).strip()
    synccode = str(request.vars.synccode).strip()
    client = str(request.vars.client).strip()
#     return client
     
    compRow = db((db.sm_company_settings.cid == cid) & (db.sm_company_settings.status == 'ACTIVE')).select(db.sm_company_settings.cid, limitby=(0, 1))
    if not compRow:
        return 'FAILED<SYNCDATA>Invalid Company'+'<br><br><br>'
    else:
        repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.sync_code == synccode) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.rep_id, db.sm_rep.name, db.sm_rep.mobile_no, db.sm_rep.user_type, db.sm_rep.level_id, db.sm_rep.depot_id, limitby=(0, 1))
 
         
        if not repRow:
           return 'FAILED<SYNCDATA>Invalid Authorization'+'<br><br><br>'
 
        else:
            qset=db()
            qset=qset(db.sm_order.cid==cid)
            qset=qset(db.sm_order.client_id==client)
             
                     
                
            records=qset.select(db.sm_order.ALL,orderby=~db.sm_order.sl, limitby=(0,1))
            
#             return db._lastsql
            if records:  
                depot_id=''
                depot_name=''
                sl=''
                store_id=''
                store_name=''
                client_id=''
                client_name=''
                rep_id=''
                rep_name  =''      
                order_date=''
                order_datetime=''
                
                payment_mode=''
                status=''
                invoice_ref    =''

                location_detail =''
                last_location=''
                promo_ref=''
                i=0
                for record in records:  
                    if i==0:
                        i=i+1
                        client_name =record.client_name 
                        depot_id=record.depot_id 
                        depot_name=record.depot_name
                        store_id=record.store_id 
                        store_name=record.store_name 
                        sl =record.sl 
                        rep_id=record.rep_id 
                        
                        rep_name=record.rep_name                 
                        order_datetime=record.order_datetime                    
                        payment_mode=record.payment_mode     
                        
                        status=record.status 
                        
                         
                        
                        
    
                        invoice_str='<table width="500" border="0" cellspacing="0" cellpadding="0" style="color:#306161">'
                        invoice_str=invoice_str+'<tr ><td width="100" style="padding-left:0px;"><b>Branch</b></td><td width="5"><b>:</b></td><td width="300" align="left">'+str(depot_name) + '('+str(depot_id) +')'+'</td></tr>'
                        invoice_str=invoice_str+'<tr ><td width="100" style="padding-left:0px;"><b>Store</b></td><td width="5"><b>:</b></td><td width="300" align="left">'+str(store_name) + '('+str(store_id) +')'+'</td></tr>'
                        invoice_str=invoice_str+'<tr ><td width="100" style="padding-left:0px;"><b>Customer</b></td><td width="5"><b>:</b></td><td width="300" align="left">'+str(client_name) + '('+str(client) +')'+'</td></tr>'
                
                        invoice_str=invoice_str+'<tr ><td width="100" style="padding-left:0px;"><b>OrderSL</b></td><td width="5"><b>:</b></td><td width="300" align="left">'+str(sl) +'</td></tr>'
                        invoice_str=invoice_str+'<tr ><td width="100" style="padding-left:0px;"><b>Rep</b></td><td width="5"><b>:</b></td><td width="300" align="left">'+str(rep_name) + '('+str(rep_id) +')'+'</td></tr>'
                        invoice_str=invoice_str+'<tr ><td width="100" style="padding-left:0px;"><b>OrderDate</b></td><td width="5"><b>:</b></td><td width="300" align="left">'+str(order_datetime)+'</td></tr>'
                        invoice_str=invoice_str+'</table>'  
                    else:
                        pass                  


                    
               
                    item_id =''
                    item_name =''
                   
                    category_id =''
                    quantity=''
                    
                    price=''
                    gross_total=0
                    invoice_str=invoice_str+"""<table width="500" border="1" cellpadding="0" cellspacing="0" style="border:solid; border-style:solid; border-color:#0CF; color:#306161"> 
                        <tr align="left" class="blackCatHead"  >
                        <td width="50" >ID</td>
                        <td >Name</td>
                        <td width="50" align="center"  >Category</td>
                        
                        <td width="50" align="center"  >Qty</td>
                        <td width="50" align="right"  >TP</td>
                        <td width="50" align="right"  >Vat</td>
                        <td width="50" align="right"  >Amount </td>
                        </tr>"""
                    qset_detail=db()
                    qset_detail=qset_detail(db.sm_order.cid==cid)
                    qset_detail=qset_detail(db.sm_order.client_id==client)
                    qset_detail=qset_detail(db.sm_order.sl==sl)
                     
                             
                        
                    records_detail=qset_detail.select(db.sm_order.ALL,orderby=db.sm_order.item_name)    
#                     return db._lastsql
                    for records_detail in records_detail:  
                        item_id     =records_detail.item_id 
                        item_name   =records_detail.item_name 
                       
                        category_id =records_detail.category_id 
                        quantity    =records_detail.quantity 
                        
                        price       =records_detail.price
                        item_vat =records_detail.item_vat
                        
                         
                        amt=quantity*(price+item_vat)
                        gross_total =float(gross_total)+ float(amt)
                                                   
                                                
                       
                        invoice_str=invoice_str+'<tr ><td >'+str(item_id)+'</td>'
                        invoice_str=invoice_str+'<td style="padding-left:0px;">'+str(item_name)+'</td>'
                 
                        invoice_str=invoice_str+'<td align="center">'+str(category_id)+'</td>'
                        invoice_str=invoice_str+'<td align="center">'+str(quantity)+'</td>'
                        
                        invoice_str=invoice_str+'<td align="right">'+str(price)+'</td>'
                        invoice_str=invoice_str+'<td align="right">'+str(item_vat)+'</td>'
                        invoice_str=invoice_str+'<td align="right">'+str(amt)+'</td>'
                        
                        invoice_str=invoice_str+'</tr>'#</table>'                    
                     
                     
                    invoice_str=invoice_str+'<tr ><td ></td>'
                    
                    
                    invoice_str=invoice_str+'<td ></td>'
                    invoice_str=invoice_str+'<td ></td>'
                    invoice_str=invoice_str+'<td ></td>'
                    invoice_str=invoice_str+'<td ></td>'
                    invoice_str=invoice_str+'<td align="right">Total</td>'
                    
                    invoice_str=invoice_str+'<td align="right">'+str(gross_total)+'</td>'
                    
                    invoice_str=invoice_str+'</tr></table>'       
                    
                                   
                    return 'SUCCESS<SYNCDATA>'+invoice_str+'<br><br><br>'
             
            else:
                return 'SUCCESS<SYNCDATA>'+'No Order' +'<br><br><br>'       
                    
                                  
                 
# ===================================TodayOrder=========
def today_order_report():
    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.rep_pass).strip()
    synccode = str(request.vars.synccode).strip()
    date_from=current_date
    now = datetime.datetime.strptime(current_date, "%Y-%m-%d")
    date_to=now + datetime.timedelta(days = 1)
     
    compRow = db((db.sm_company_settings.cid == cid) & (db.sm_company_settings.status == 'ACTIVE')).select(db.sm_company_settings.cid, limitby=(0, 1))
    if not compRow:
        return 'FAILED<SYNCDATA>Invalid Company'+'<br><br><br>'
    else:
        repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.sync_code == synccode) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.rep_id, db.sm_rep.name, db.sm_rep.mobile_no, db.sm_rep.user_type, db.sm_rep.level_id, db.sm_rep.depot_id, limitby=(0, 1))
 
         
        if not repRow:
           return 'FAILED<SYNCDATA>Invalid Authorization'+'<br><br><br>'
 
        else:
            qset=db()
            qset=qset(db.sm_order.cid==cid)
            qset=qset(db.sm_order.order_date>=date_from)
            qset=qset(db.sm_order.order_date<=date_to)
             
                     
                
            records=qset.select(db.sm_order.ALL,orderby=~db.sm_order.sl)
            
#             return db._lastsql
            if records:  
                depot_id=''
                depot_name=''
                sl=''
                store_id=''
                store_name=''
                client_id=''
                client_name=''
                rep_id=''
                rep_name  =''      
                order_date=''
                order_datetime=''
                
                payment_mode=''
                status=''
                invoice_ref    =''

                location_detail =''
                last_location=''
                promo_ref=''
                i=0
                for record in records:  
                    if i==0:
                        i=i+1
                        client_name =record.client_name 
                        depot_id=record.depot_id 
                        depot_name=record.depot_name
                        store_id=record.store_id 
                        store_name=record.store_name 
                        sl =record.sl 
                        rep_id=record.rep_id 
                        
                        rep_name=record.rep_name                 
                        order_datetime=record.order_datetime                    
                        payment_mode=record.payment_mode     
                        
                        status=record.status 
                        
                         
                        
                        
    
                        invoice_str='<table width="500" border="0" cellspacing="0" cellpadding="0" style="color:#306161">'
                        invoice_str=invoice_str+'<tr ><td width="100" style="padding-left:0px;"><b>Branch</b></td><td width="5"><b>:</b></td><td width="300" align="left">'+str(depot_name) + '('+str(depot_id) +')'+'</td></tr>'
                        invoice_str=invoice_str+'<tr ><td width="100" style="padding-left:0px;"><b>Store</b></td><td width="5"><b>:</b></td><td width="300" align="left">'+str(store_name) + '('+str(store_id) +')'+'</td></tr>'
#                         invoice_str=invoice_str+'<tr ><td width="100" style="padding-left:0px;"><b>Customer</b></td><td width="5"><b>:</b></td><td width="300" align="left">'+str(client_name) + '('+str(client) +')'+'</td></tr>'
                
                        invoice_str=invoice_str+'<tr ><td width="100" style="padding-left:0px;"><b>OrderSL</b></td><td width="5"><b>:</b></td><td width="300" align="left">'+str(sl) +'</td></tr>'
                        invoice_str=invoice_str+'<tr ><td width="100" style="padding-left:0px;"><b>Rep</b></td><td width="5"><b>:</b></td><td width="300" align="left">'+str(rep_name) + '('+str(rep_id) +')'+'</td></tr>'
                        invoice_str=invoice_str+'<tr ><td width="100" style="padding-left:0px;"><b>OrderDate</b></td><td width="5"><b>:</b></td><td width="300" align="left">'+str(order_datetime)+'</td></tr>'
                        invoice_str=invoice_str+'</table>'  
                    else:
                        pass                  


                    
               
                    item_id =''
                    item_name =''
                   
                    category_id =''
                    quantity=''
                    
                    price=''
                    gross_total=0
                    invoice_str=invoice_str+"""<table width="500" border="1" cellpadding="0" cellspacing="0" style="border:solid; border-style:solid; border-color:#0CF; color:#306161"> 
                        <tr align="left" class="blackCatHead"  >
                        <td width="50" >ID</td>
                        <td >Name</td>
                        <td width="50" align="center"  >Category</td>
                        
                        <td width="50" align="center"  >Qty</td>
                        <td width="50" align="right"  >TP</td>
                        <td width="50" align="right"  >Vat</td>
                        <td width="50" align="right"  >Amount </td>
                        </tr>"""
                    qset_detail=db()
                    qset_detail=qset_detail(db.sm_order.cid==cid)
                    qset_detail=qset_detail(db.sm_order.order_date>=date_from)
                    qset_detail=qset_detail(db.sm_order.order_date<=date_to)
                    qset_detail=qset_detail(db.sm_order.sl==sl)
                     
                             
                        
                    records_detail=qset_detail.select(db.sm_order.ALL,orderby=db.sm_order.item_name)    
#                     return db._lastsql
                    for records_detail in records_detail:  
                        item_id     =records_detail.item_id 
                        item_name   =records_detail.item_name 
                       
                        category_id =records_detail.category_id 
                        quantity    =records_detail.quantity 
                        
                        price       =records_detail.price
                        item_vat =records_detail.item_vat
                        
                         
                        amt=quantity*(price+item_vat)
                        gross_total =float(gross_total)+ float(amt)
                                                   
                                                
                       
                        invoice_str=invoice_str+'<tr ><td >'+str(item_id)+'</td>'
                        invoice_str=invoice_str+'<td style="padding-left:0px;">'+str(item_name)+'</td>'
                 
                        invoice_str=invoice_str+'<td align="center">'+str(category_id)+'</td>'
                        invoice_str=invoice_str+'<td align="center">'+str(quantity)+'</td>'
                        
                        invoice_str=invoice_str+'<td align="right">'+str(price)+'</td>'
                        invoice_str=invoice_str+'<td align="right">'+str(item_vat)+'</td>'
                        invoice_str=invoice_str+'<td align="right">'+str(amt)+'</td>'
                        
                        invoice_str=invoice_str+'</tr>'#</table>'                    
                     
                     
                    invoice_str=invoice_str+'<tr ><td ></td>'
                    
                    
                    invoice_str=invoice_str+'<td ></td>'
                    invoice_str=invoice_str+'<td ></td>'
                    invoice_str=invoice_str+'<td ></td>'
                    invoice_str=invoice_str+'<td ></td>'
                    invoice_str=invoice_str+'<td align="right">Total</td>'
                    
                    invoice_str=invoice_str+'<td align="right">'+str(gross_total)+'</td>'
                    
                    invoice_str=invoice_str+'</tr></table>'       
                    
                                   
                    return 'SUCCESS<SYNCDATA>'+invoice_str+'<br><br><br>'
             
            else:
                return 'SUCCESS<SYNCDATA>'+'No Order' +'<br><br><br>'       
                    
                                  
                                  
#  =======================Notice                
                 
               # ===================================ClientOrder=========
def notice_report():
    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.rep_pass).strip()
    synccode = str(request.vars.synccode).strip()
    
     
    compRow = db((db.sm_company_settings.cid == cid) & (db.sm_company_settings.status == 'ACTIVE')).select(db.sm_company_settings.cid, limitby=(0, 1))
    if not compRow:
        return 'FAILED<SYNCDATA>Invalid Company'+'<br><br><br>'
    else:
        repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.sync_code == synccode) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.rep_id, db.sm_rep.name, db.sm_rep.mobile_no, db.sm_rep.user_type, db.sm_rep.level_id, db.sm_rep.depot_id, limitby=(0, 1))
 
         
        if not repRow:
           return 'FAILED<SYNCDATA>Invalid Authorization'+'<br><br><br>'
 
        else:
            noticeRow = db((db.sm_notice.cid == cid) & (db.sm_notice.notice_date <= current_date)).select(db.sm_notice.ALL,orderby=~db.sm_notice.id,limitby=(0, 30))
#             return db._lastsql
            if noticeRow:
                notice_str="""<table width="500" border="1" cellpadding="0" cellspacing="0" style="border:solid; border-style:solid; border-color:#0CF; color:#306161"> 
                        <tr align="left" class="blackCatHead"  >
                        <td width="120px" >Date</td>
                        <td >Notice</td>
                        </tr>"""
                
                for noticeRow in noticeRow:  
                    notice_date  = noticeRow.notice_date 
                    notice   = noticeRow.notice 
                                                             
                    notice_str=notice_str+'<tr ><td >'+str(notice_date)+'</td>'
                    notice_str=notice_str+'<td style="padding-left:0px;">'+str(notice)+'</td>'
                    notice_str=notice_str+'</tr>'#</table>'                    
                                                
                return 'SUCCESS<SYNCDATA>'+notice_str+'<br><br><br>'
            
            else:
                return 'SUCCESS<SYNCDATA>'+'No Notice' +'<br><br><br>'                 
                 
                
     
 # ====================Client approved========================
def client_approved_report():
    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.rep_pass).strip()
    synccode = str(request.vars.synccode).strip()
    client = str(request.vars.client).strip()
#     return client
    
    compRow = db((db.sm_company_settings.cid == cid) & (db.sm_company_settings.status == 'ACTIVE')).select(db.sm_company_settings.cid, limitby=(0, 1))
    if not compRow:
        return 'FAILED<SYNCDATA>Invalid Company'
    else:
        repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.sync_code == synccode) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.rep_id, db.sm_rep.name, db.sm_rep.mobile_no, db.sm_rep.user_type, db.sm_rep.level_id, db.sm_rep.depot_id, limitby=(0, 1))

        
        if not repRow:
           return 'FAILED<SYNCDATA>Invalid Authorization'

        else:
            qset=db()
            qset=qset(db.sm_promo_approved_rate.cid==cid)
            qset=qset(db.sm_promo_approved_rate.status=='ACTIVE')
            qset=qset(db.sm_promo_approved_rate.client_id==client)
            
            
            qset=qset(db.sm_promo_approved_rate.from_date <= current_date)
            qset=qset(db.sm_promo_approved_rate.to_date >= current_date)
            
            
            
                    
               
            records=qset.select(db.sm_promo_approved_rate.ALL,orderby=~db.sm_promo_approved_rate.id)
#             return records
            if records:  
                for record_name in records:  
                    client_name =record_name.client_name 
                    break  
                
                approvrd_str='<table width="500" border="0" cellspacing="0" cellpadding="0" style="color:#306161">'
                approvrd_str=approvrd_str+'<tr ><td width="100" style="padding-left:0px;"><b>Customer ID</b></td><td width="5"><b>:</b></td><td width="300" align="left">'+str(client) +'</td></tr>'
                approvrd_str=approvrd_str+'<tr ><td width="100" style="padding-left:0px;"><b>Customer Name</b></td><td width="5"><b>:</b></td><td width="300" align="left">'+str(client_name) +'</td></tr>'

                approvrd_str=approvrd_str+'</table><br>'
                
                 
    
#                 return approvrd_str
                  
    
    
                    
                approvrd_str=approvrd_str+'<table width="600" border="1" cellpadding="0" cellspacing="0" style="border:solid; border-style:solid; border-color:#0CF; color:#306161"> <tr class="table_title">'
    
                approvrd_str=approvrd_str+'<td  width="100">From </td> '
                approvrd_str=approvrd_str+'<td  width="100">To</td>'
                approvrd_str=approvrd_str+'<td width="50"> ProductID</td>'
                approvrd_str=approvrd_str+'<td  >Name</td>'
                approvrd_str=approvrd_str+'<td width="50" >BonusType</td>'
                approvrd_str=approvrd_str+'<td width="50" align="right" >FixedPercent</td></tr>'

              
               
                for record in records:                                  
                    from_date=record.from_date
                    to_date=record.to_date
                    product_id =record.product_id   
                    product_name=record.product_name
                    bonus_type=record.bonus_type
                    fixed_percent_rate=record.fixed_percent_rate
                    
                    approvrd_str+'<tr>'
                    approvrd_str=approvrd_str+' <td >'+str(from_date)+'</td>'
                    approvrd_str=approvrd_str+' <td >'+str(to_date)+'</td>'                    
                    approvrd_str=approvrd_str+' <td >'+str(product_id)+'</td>'
                    approvrd_str=approvrd_str+' <td >'+str(product_name)+'</td>'
                    approvrd_str=approvrd_str+' <td >'+str(bonus_type)+'</td>'
                    approvrd_str=approvrd_str+' <td align="right">'+str(fixed_percent_rate)+'</td>'
                    approvrd_str=approvrd_str+' </tr> '

                approvrd_str=approvrd_str+'</table>'+'<br><br><br><br><br>' 
            else:
                approvrd_str= 'No Approved Rate'+'<br><br><br><br><br>' 
            
    return 'SUCCESS<SYNCDATA>'+approvrd_str    
     
# ====================Doc Info=============

def doc_info():
    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.rep_pass).strip()
    synccode = str(request.vars.synccode).strip()
    route = str(request.vars.route).strip()
    doc = str(request.vars.docId).strip()
#     return client
    compRow = db((db.sm_company_settings.cid == cid) & (db.sm_company_settings.status == 'ACTIVE')).select(db.sm_company_settings.cid, limitby=(0, 1))
    if not compRow:
        return 'FAILED<SYNCDATA>Invalid Company'
    else:
        repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.sync_code == synccode) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.rep_id, db.sm_rep.name, db.sm_rep.mobile_no, db.sm_rep.user_type, db.sm_rep.level_id, db.sm_rep.depot_id, limitby=(0, 1))

        if not repRow:
           return 'FAILED<SYNCDATA>Invalid Authorization'

        else:
            cat_row=db(db.doc_catagory.cid == cid).select(db.doc_catagory.category, orderby=db.doc_catagory.category)
            catStr=''
            for cat_row in cat_row:
                catStr=catStr+str(cat_row.category)+','
            
            spc_row=db(db.doc_speciality.cid == cid).select(db.doc_speciality.specialty, orderby=db.doc_speciality.specialty    )
            spcStr=''
            for spc_row in spc_row:
                spcStr=spcStr+str(spc_row.specialty)+','
#             cat_row=db(db.doc_catagory.cid == cid).select(db.doc_catagory.category, orderby=db.doc_catagory.category)
#             catStr=''
#             for cat_row in cat_row:
#                 catStr=catStr+str(cat_row.category)+','
            docRow = db((db.sm_doctor.cid == cid) & (db.sm_doctor.doc_id == doc) & (db.sm_doctor_area.cid == cid) & (db.sm_doctor_area.area_id == route) & (db.sm_doctor_area.doc_id == doc)).select(db.sm_doctor.ALL,db.sm_doctor_area.address,db.sm_doctor_area.district,db.sm_doctor_area.thana, limitby=(0, 1))
#             return docRow
            dName=''
            dSpaciality=''
            dDegree=''
            dCaegory=''
            dDOB=''
            dMDay=''
            dMobile=''
            dStatus=''
            dCAddress=''
            dThana=''
            dDist=''
            rtn_str=''
            if docRow:  
                dName=docRow[0][db.sm_doctor.doc_name]
                dSpaciality=docRow[0][db.sm_doctor.specialty]+','+spcStr
                dDegree=docRow[0][db.sm_doctor.degree]
                dCaegory=docRow[0][db.sm_doctor.doctors_category]+','+catStr
                dDOB==docRow[0][db.sm_doctor.dob]
                dMDay=docRow[0][db.sm_doctor.mar_day]
                dMobile=docRow[0][db.sm_doctor.mobile]
                dCAddress=docRow[0][db.sm_doctor_area.address]
                dDist=docRow[0][db.sm_doctor_area.district]
                dThana=docRow[0][db.sm_doctor_area.thana]
                rtn_str=str(dName)+'<fdfd>'+str(dSpaciality)+'<fdfd>'+str(dDegree)+'<fdfd>'+str(dCaegory)+'<fdfd>'+str(dDOB)+'<fdfd>'+str(dMDay)+'<fdfd>'+str(dMobile)+'<fdfd>'+str(dCAddress)+'<fdfd>'+str(dDist)+'<fdfd>'+str(dThana)
             
    return 'SUCCESS<SYNCDATA>'+rtn_str  


def getBaseUrl(cid):
    baseUrl = ''
    baseUrl = 'http://a002.businesssolutionapps.com/skf/syncmobile_ofline_ppm_report_test_live_20150502/';

    return baseUrl

def doc_info_submit():
    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.rep_pass).strip()
    synccode = str(request.vars.synccode).strip()
    route = str(request.vars.route).strip()
    doc = str(request.vars.docId).strip()
    
    dName=str(request.vars.dName).strip()
    dSpaciality=str(request.vars.dSpaciality).strip()
    dDegree=str(request.vars.dDegree).strip()
    dCategory=str(request.vars.dCategory).strip()
    dDOB=str(request.vars.dDOB).strip()
    dMDay=str(request.vars.dMDay).strip()
    dMobile=str(request.vars.dMobile).strip()
    dCAddress=str(request.vars.dCAddress).strip()
    dDist=str(request.vars.dDist).strip()
    dThana=str(request.vars.dThana).strip()
#     return dCategory

    urlPath = getBaseUrl(cid)+'doc_info_submit?cid='+cid+'&rep_id='+rep_id+'&rep_pass='+password+'&synccode='+synccode+'&route='+urllib.quote(route)+'&docId='+urllib.quote(doc)+'&dName='+urllib.quote(dName)+'&dSpaciality='+urllib.quote(dSpaciality)+'&dDegree='+urllib.quote(dDegree)+'&dDOB='+urllib.quote(dDOB)+'&dMDay='+urllib.quote(dMDay)+'&dMobile='+urllib.quote(dMobile)+'&dCAddress='+urllib.quote(dCAddress)+'&dCategory='+urllib.quote(dCategory)+'&dDist='+urllib.quote(dDist)+'&dThana='+urllib.quote(dThana)
    
    
    #     return urlPath
    #-----
    try:
        result = fetch(urlPath)
    except:
        result = ''
    
    return result 


# ================================Add Doctor


def doc_add_submit():
    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.rep_pass).strip()
    synccode = str(request.vars.synccode).strip()
    route = str(request.vars.route).strip()
    routeName= str(request.vars.routeName).strip()
    
    
    dName=str(request.vars.dName).strip()
    dSpaciality=str(request.vars.dSpaciality).strip()
    dDegree=str(request.vars.dDegree).strip()
    dCategory=str(request.vars.dCategory).strip()
    dDOB=str(request.vars.dDOB).strip()
    dMDay=str(request.vars.dMDay).strip()
    dMobile=str(request.vars.dMobile).strip()
    dCAddress=str(request.vars.dCAddress).strip()
    dDist=str(request.vars.dDist).strip()
    dThana=str(request.vars.dThana).strip()
    
    urlPath = getBaseUrl(cid)+'doc_add_submit?cid='+cid+'&rep_id='+rep_id+'&rep_pass='+password+'&synccode='+synccode+'&route='+urllib.quote(route)+'&routeName='+urllib.quote(routeName)+'&dName='+urllib.quote(dName)+'&dSpaciality='+urllib.quote(dSpaciality)+'&dDegree='+urllib.quote(dDegree)+'&dDOB='+urllib.quote(dDOB)+'&dMDay='+urllib.quote(dMDay)+'&dMobile='+urllib.quote(dMobile)+'&dCAddress='+urllib.quote(dCAddress)+'&dCategory='+urllib.quote(dCategory)+'&dDist='+urllib.quote(dDist)+'&dThana='+urllib.quote(dThana)
    return urlPath
                                                                                                                    
    #     return urlPath
    #-----
    try:
        result = fetch(urlPath)
    except:
        result = ''
    
    return result 
# ================================ Doctor List
def doc_list():
    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.rep_pass).strip()
    synccode = str(request.vars.synccode).strip()
    route = str(request.vars.route).strip()
    
    rtn_str=''
#     return client
    compRow = db((db.sm_company_settings.cid == cid) & (db.sm_company_settings.status == 'ACTIVE')).select(db.sm_company_settings.cid, limitby=(0, 1))
    if not compRow:
        return 'FAILED<SYNCDATA>Invalid Company'
    else:
        repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.sync_code == synccode) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.rep_id, db.sm_rep.name, db.sm_rep.mobile_no, db.sm_rep.user_type, db.sm_rep.level_id, db.sm_rep.depot_id, limitby=(0, 1))
        if not repRow:
           return 'FAILED<SYNCDATA>Invalid Authorization'

        else:
            userType=repRow[0][db.sm_rep.user_type]
            if userType=='rep':
                
                areaList=[]
                levelRows = db((db.sm_rep_area.cid == cid) & (db.sm_rep_area.rep_id == rep_id)).select(db.sm_rep_area.area_id)
                    
                for levelRow in levelRows:
                    level_id = levelRow.area_id
                    
                    if level_id not in areaList:
                        areaList.append(level_id)
                
                doctorRows = db((db.sm_doctor.cid == cid) & (db.sm_doctor.status == 'SUBMITTED') & (db.sm_doctor_area.cid == cid) & (db.sm_doctor_area.doc_id == db.sm_doctor.doc_id) & (db.sm_doctor_area.area_id.belongs(areaList))   ).select(db.sm_doctor.doc_id, db.sm_doctor.doc_name, db.sm_doctor_area.area_id, orderby=db.sm_doctor.doc_id)
#                 return doctorRows
                if not doctorRows:
                    rtn_str='Nothing pending for approval.'
    
                else:
                    rtn_str=' <table width="100%" border="0" cellspacing="0" cellpadding="0">'
                    for doctorRow in doctorRows:
                        doctor_id = doctorRow.sm_doctor.doc_id
                        doctor_name = doctorRow.sm_doctor.doc_name
                        doctor_area = doctorRow.sm_doctor_area.area_id
                        rtn_str=rtn_str+' <tr  height="30px"> <td >'+str(doctor_name)+'|'+str(doctor_id)+'|'+str(doctor_area)+' </td><td></td></tr>'
                    rtn_str=rtn_str+'</table>'
                                

            else:
                
                levelList=[]
                areaList=[]
                spicial_codeList=[]
                SuplevelRows = db((db.sm_supervisor_level.cid == cid) & (db.sm_supervisor_level.sup_id == rep_id) ).select(db.sm_supervisor_level.level_id,db.sm_supervisor_level.level_depth_no, orderby=~db.sm_supervisor_level.level_id)
                for SuplevelRows in SuplevelRows:
                    Suplevel_id = SuplevelRows.level_id
                    depth = SuplevelRows.level_depth_no
                    level = 'level' + str(depth)
                    if Suplevel_id not in levelList:
                        levelList.append(Suplevel_id)
                
                for i in range(len(levelList)):
                    levelRows = db((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '1') & (db.sm_level[level] == levelList[i])).select(db.sm_level.level_id, db.sm_level.level_name, db.sm_level.depot_id, db.sm_level.special_territory_code)
                    
                    for levelRow in levelRows:
                        level_id = levelRow.level_id
                        level_name = levelRow.level_name
                        special_territory_code = levelRow.special_territory_code
                        if level_id not in areaList:
                            areaList.append(level_id)
                        if special_territory_code not in spicial_codeList:
                            if (special_territory_code!=''):
                                spicial_codeList.append(special_territory_code)
                                   
                
#                 levelSpecialRows = db((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '1') & (db.sm_level.special_territory_code.belongs(spicial_codeList))).select(db.sm_level.level_id, db.sm_level.level_name, db.sm_level.depot_id)    
#                 
#                 
#                 for levelSpecialRow in levelSpecialRows:
#                     level_id = levelSpecialRow.level_id
#                     level_name = levelSpecialRow.level_name
#                     if level_id not in areaList:
#                             areaList.append(level_id)
                        
                doctorRows = db((db.sm_doctor.cid == cid) & (db.sm_doctor.status == 'SUBMITTED') & (db.sm_doctor_area.cid == cid) & (db.sm_doctor_area.doc_id == db.sm_doctor.doc_id) & (db.sm_doctor_area.area_id.belongs(areaList)) ).select(db.sm_doctor.doc_id, db.sm_doctor.doc_name, db.sm_doctor_area.area_id, orderby=db.sm_doctor.doc_id)
                
                if not doctorRows:
                    rtn_str='Nothing pending for approval.'
    
                else:

                    rtn_str=' <table width="100%" border="0" cellspacing="0" cellpadding="0">'
                  
                    for doctorRow in doctorRows:
                        doctor_id = doctorRow.sm_doctor.doc_id
                        doctor_name = doctorRow.sm_doctor.doc_name
                        doctor_area = doctorRow.sm_doctor_area.area_id
                        rtn_str=rtn_str+' <tr  height="30px"> <td >'+str(doctor_name)+'|'+str(doctor_id)+'|'+str(doctor_area)+' </td><td><img  width="50px;" height="50px" src="confirm.png"  onClick="confirmDoc('+str(doctor_id)+')"  alt="">'#<input type="submit" onClick="confirmDoc('+str(doctor_id)+')"   value="     Confirm     "   /> </td></tr>'
                    rtn_str=rtn_str+'</table>'
#             return rtn_str
    return 'SUCCESS<SYNCDATA>'+rtn_str 

def confirmDoc():
    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.rep_pass).strip()
    synccode = str(request.vars.synccode).strip()
    route = ''#str(request.vars.route).strip()
    docID = str(request.vars.docID).strip()
    
    urlPath = getBaseUrl(cid)+'confirmDoc?cid='+cid+'&rep_id='+rep_id+'&rep_pass='+password+'&synccode='+synccode+'&route='+route+'&docID='+docID
    
                                                                                                                   
    #     return urlPath
    #-----
    try:
       result = fetch(urlPath)
    except:
       result = ''
    
    return result 

def cancelDoc():
    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.rep_pass).strip()
    synccode = str(request.vars.synccode).strip()
    route = '' #str(request.vars.route).strip()
    docID = str(request.vars.docID).strip()
    
    urlPath = getBaseUrl(cid)+'cancelDoc?cid='+cid+'&rep_id='+rep_id+'&rep_pass='+password+'&synccode='+synccode+'&route='+route+'&docID='+docID
    
                                                                                                                    
    #     return urlPath
    #-----
    try:
        result = fetch(urlPath)
    except:
        result = ''
    
    return result 

def doc_info_confirm():
    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.rep_pass).strip()
    synccode = str(request.vars.synccode).strip()
    doc = str(request.vars.docID).strip()

    compRow = db((db.sm_company_settings.cid == cid) & (db.sm_company_settings.status == 'ACTIVE')).select(db.sm_company_settings.cid, limitby=(0, 1))
    if not compRow:
        return 'FAILED<SYNCDATA>Invalid Company'
    else:
        repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.sync_code == synccode) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.rep_id, db.sm_rep.name, db.sm_rep.mobile_no, db.sm_rep.user_type, db.sm_rep.level_id, db.sm_rep.depot_id, limitby=(0, 1))

        if not repRow:
           return 'FAILED<SYNCDATA>Invalid Authorization'

        else:
            docRow = db((db.sm_doctor.cid == cid) & (db.sm_doctor.doc_id == doc) & (db.sm_doctor_area.cid == cid)  & (db.sm_doctor_area.doc_id == doc)).select(db.sm_doctor.ALL,db.sm_doctor_area.address,db.sm_doctor_area.district,db.sm_doctor_area.thana, limitby=(0, 1))
#             return db._lastsql
            dName=''
            dSpaciality=''
            dDegree=''
            dCaegory=''
            dDOB=''
            dMDay=''
            dMobile=''
            dStatus=''
            dCAddress=''
            dThana=''
            dDist=''
            rtn_str=''
            if docRow:  
                dName=docRow[0][db.sm_doctor.doc_name]
                dSpaciality=docRow[0][db.sm_doctor.specialty]
                dDegree=docRow[0][db.sm_doctor.degree]
                dCaegory=docRow[0][db.sm_doctor.doctors_category]
                dDOB==docRow[0][db.sm_doctor.dob]
                dMDay=docRow[0][db.sm_doctor.mar_day]
                dMobile=docRow[0][db.sm_doctor.mobile]
                dCAddress=docRow[0][db.sm_doctor_area.address]
                dDist=docRow[0][db.sm_doctor_area.district]
                dThana=docRow[0][db.sm_doctor_area.thana]
                if dName==None:
                    dName=''
                if dSpaciality==None:
                    dSpaciality=''
                if dDegree==None:
                    dDegree=''
                if dCaegory==None:
                    dCaegory=''
                if dDOB==None:
                    dDOB=''
                if dMDay==None:
                    dMDay=''
                if dMobile==None:
                    dMobile=''
                if dCAddress==None:
                    dCAddress=''
                if dDist==None:
                    dDist=''
                if dThana==None:
                    dThana=''
                rtn_str=str(dName)+'<fdfd>'+str(dSpaciality)+'<fdfd>'+str(dDegree)+'<fdfd>'+str(dCaegory)+'<fdfd>'+str(dDOB)+'<fdfd>'+str(dMDay)+'<fdfd>'+str(dMobile)+'<fdfd>'+str(dCAddress)+'<fdfd>'+str(dDist)+'<fdfd>'+str(dThana)
             
    return 'SUCCESS<SYNCDATA>'+rtn_str  

#============================= Test dynamic path
def dmpath():
    return '<start>http://127.0.0.1:8000/skf/syncmobile_ofline_ppm_report_test_live_20150502/<fd>http://e2.businesssolutionapps.com/mrepbiopharma/static/<fd>http://e2.businesssolutionapps.com/mrepbiopharma/syncmobile_ofline_ppm_report_test/<fd>http://127.0.0.1:8000/skf/syncmobile_ofline_ppm_report_test_live_20150502/<end>'
#     return '<start>http://a002.businesssolutionapps.com/skf/syncmobile_ofline_ppm_report_test_live_20150502_test/<fd>http://e2.businesssolutionapps.com/mrepbiopharma/static/<fd>http://e2.businesssolutionapps.com/mrepbiopharma/syncmobile_ofline_ppm_report_test/<fd>http://a002.businesssolutionapps.com/skf/syncmobile_ofline_ppm_report_test_live_20150502_test/<end>'
#     return '<start>http://c003.cloudapp.net/skf/syncmobile_ofline_ppm_report_test_live_20150502/<fd>http://e2.businesssolutionapps.com/mrepbiopharma/static/<fd>http://e2.businesssolutionapps.com/mrepbiopharma/syncmobile_ofline_ppm_report_test/<fd>http://c003.cloudapp.net/skf/syncmobile_ofline_ppm_report_test_live_20150502/<end>'


