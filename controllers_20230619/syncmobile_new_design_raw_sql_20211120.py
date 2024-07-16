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




# Unscheduled
# http://127.0.0.1:8000/lscmreporting/syncmobile/?clircid=LSCRM&rep_id=1001&rep_pass=123&synccode=7048&market_id=M000003
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
def fileUploaderPrescription():
    import shutil
    filename = request.vars.upload.filename
    file = request.vars.upload.file
#    shutil.copyfileobj(file,open('C:/workspace/Dropbox/sabbir_acer/web2py/applications/welcome/uploads/'+filename,'wb'))
#     shutil.copyfileobj(file, open('/home/www-data/web2py/applications/mrepacme/static/prescription_pic/' + filename, 'wb'))
    shutil.copyfileobj(file, open('/home/www-data/web2py/applications/demo/static/prescription_pic/' + filename, 'wb'))
    return 'success'

def fileUploader_docVisit():
    import shutil
    filename = request.vars.upload.filename
    file = request.vars.upload.file
#    shutil.copyfileobj(file,open('C:/workspace/Dropbox/sabbir_acer/web2py/applications/welcome/uploads/'+filename,'wb'))
    shutil.copyfileobj(file, open('/home/www-data/web2py/applications/demo/static/docVisit_pic/' + filename, 'wb'))
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




# ========================Doctor End================

#==================Report Start================
#http://127.0.0.1:8000/mrepnovelta/syncmobile_ofline_ppm_02012015/s_call_order_summary?
#cid=NOVELTA&rep_id=1001&rep_pass=123&synccode=8201&rep_id_report=1001&se_item_report=XCS2&se_market_report=DG022&date_from=2015-02-09&date_to=2015-02-09
def s_call_order_summary():
#     return 'SUCCESS<SYNCDATA>'+'Please try later'
    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.rep_pass).strip()
    synccode = str(request.vars.synccode).strip()
    
    rep_id_report = str(request.vars.rep_id_report).strip().upper()
    se_item_report = str(request.vars.se_item_report).strip().upper()
    se_market_report = str(request.vars.se_market_report).strip().upper()
    if se_market_report=='':
       se_market_report= 'ALL'
    
    
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
           condition="and sm_order.area_id='"+ str(se_market_report) +"' "


        records_ov=[]
        sql_str="SELECT SUM((sm_order.price) * (sm_order.quantity)) as totalprice, sm_order.area_id as area_id, sm_order.area_name as area_name FROM sm_order WHERE sm_order.cid = '"+ str(cid) +"' AND sm_order.rep_id = '"+ str(rep_id) +"' AND sm_order.order_date >= '"+ str(date_from) +"' AND sm_order.order_date < '"+ str(date_to) +"' "+ condition + " GROUP BY sm_order.area_id;"
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
            condition=condition+"AND area_id = '"+str(se_market_report)+"'"
        if (rep_id!=rep_id_report):
            condition=condition+"AND rep_id = '"+str(rep_id_report)+"'"
        condition=condition+" AND area_id IN ("+str(marketStr)+")"  
        
        qset_vc_str="SELECT count(sl) as Vcount FROM sm_order_head WHERE cid =  '"+ str(cid) +"' AND order_date >=  '"+ str(date_from) +"' AND order_date <  '"+ str(date_to) +"' "+ condition + " "
#         return qset_vc_str
        reportRows_count=db.executesql(qset_vc_str,as_dict = True)

        visit_count=0
        for reportRows_count in reportRows_count:
            visit_count=reportRows_count['Vcount']

#        ==== Order Count====================
        qset_oc_str="SELECT count(sl) as Ocount FROM sm_order_head WHERE cid =  '"+ str(cid) +"' AND field1 = 'ORDER' AND order_date >=  '"+ str(date_from) +"' AND order_date <  '"+ str(date_to) +"' "+ condition + " "
        reportRows_order_count=db.executesql(qset_oc_str,as_dict = True)

        order_count=0
        for reportRows_order_count in reportRows_order_count:
            order_count=reportRows_order_count['Ocount']

# #            =============area wise Value

 

        records_ov=[]
        sql_str="SELECT SUM( (sm_order.price) * ( sm_order.quantity ) ) AS totalprice, sm_order.area_id AS area_id, sm_order.area_name AS area_name FROM sm_order WHERE sm_order.cid =  '"+ str(cid) +"' AND sm_order.order_date >=  '"+ str(date_from) +"' AND sm_order.order_date <  '"+ str(date_to) +"' "+ condition + " GROUP BY sm_order.area_name"
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




# ====================20210517======
# sals_rprt_more_path='http://127.0.0.1:8000/navana/sales_report/'
# sals_rprt_more_path='http://w05.yeapps.com/navana/sales_report/'



# ===================== 20210830 sales order report  START=================

def salsCall_order_smry():
    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.rep_pass).strip()
    synccode = str(request.vars.synccode).strip()
    
    rep_id_report = str(request.vars.rep_id_report).strip().upper()
    se_item_report = 'ALL'
    se_market_report = 'ALL'
    
    
    date_from = current_date


    user_type = str(request.vars.user_type).strip().upper()

    now = datetime.datetime.strptime(current_date, "%Y-%m-%d")
    date_ton=now + datetime.timedelta(days = 1)
    date_to=str(date_ton).split(' ')[0]

    sals_rprt_more_path=''
    report_url = db((db.sm_settings.cid == cid) & (db.sm_settings.s_key == 'web_report_url') ).select(db.sm_settings.s_value, limitby=(0, 1))
   
    if not report_url:
       retStatus = 'FAILED<SYNCDATA>Invalid Settings'
       return retStatus
    else:
       sals_rprt_more_path=report_url[0].s_value

    
    repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.sync_code == synccode) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.ALL, limitby=(0, 1))

    if not repRow:
       retStatus = 'FAILED<SYNCDATA>Invalid Authorization'
       return retStatus
    else:
       pass
    
    if (user_type == 'SUP'):
        level_rep = repRow[0].level_id
        depth = repRow[0].field2
        level = 'level' + str(depth)
        # return  level
    
    report_string=""
    
    report_str=""
    
    if (user_type=='REP'):
        repAreaRow = db((db.sm_rep_area.cid == cid) & (db.sm_rep_area.rep_id == rep_id)).select(db.sm_rep_area.area_id,orderby=db.sm_rep_area.area_id,groupby=db.sm_rep_area.area_id)
        sales_call='0'
        rp_areaList=[]

        repAreaStr=''
        for repAreaRow in repAreaRow:
            repArea_id=repAreaRow.area_id
            rp_areaList.append(repArea_id)
            if repAreaStr=='':
                repAreaStr="'"+str(repArea_id)+"'"
            else:
                repAreaStr=repAreaStr+",'"+str(repArea_id)+"'" 
       
        qset=db()
        qset=qset((db.sm_order_head.cid == cid) )#& (db.sm_order_head.rep_id == rep_id)
        qset=qset((db.sm_order_head.order_date == date_from))
        if (se_market_report!="ALL"):        
           qset=qset(db.sm_order_head.area_id==se_market_report)
        else:
           qset=qset(db.sm_order_head.area_id.belongs(rp_areaList))

        records=qset.select(db.sm_order_head.sl.count())
        # if records:
        #     sales_call=records[0][db.sm_order_head.sl.count()]
        
        report_string=str(sales_call)
        
        
        
        condition=""
        condition=condition+"AND area_id IN ("+str(repAreaStr)+") "

        records_ov=[]
        sql_str="SELECT SUM((sm_order.price) * (sm_order.quantity)) as totalprice, sm_order.area_id as area_id, sm_order.area_name as area_name FROM sm_order WHERE sm_order.cid = '"+ str(cid) +"' AND sm_order.order_date = '"+ str(date_from) +"' "+ condition + " GROUP BY sm_order.area_id order by order_date desc, area_name asc;"
        # return sql_str
        records_ov=db.executesql(sql_str,as_dict = True)
        order_count='0'
        
        order_value='0.0'
        areawise_flag=0
        areawise_str=""
        total_value=0
        if (sales_call==None):
            sales_call='0'
        if (order_count==None):
            order_count='0'
        if (order_value==None):
            order_value='0.0'


        report_str=report_str+"""<table width="100%" border="1" cellpadding="0" cellspacing="0" style="border:solid; border-style:solid; border-color:transparent; color:#fff;background:#7a828e;padding:5px"><tr align="left" class="blackCatHead"  ><td width="100%">Sales Report &nbsp;:&nbsp;&nbsp;Today</td></tr></table><br>"""
        report_str=report_str+"""<table width="100%" border="1" cellpadding="0" cellspacing="0" style="border:solid; border-style:solid; border-color:#0CF; color:#fff"> 
                                <tr  class="blackCatHead"  >
                                <td >Territory</td>
                                <td width="10%" align="center"  >Visit Count</td>
                                <td width="10%" align="center"  >Order Count</td>
                                <td width="10%" align="right"  >Amount</td>
                                </tr>"""
        gtotalprice=0.0
        for i in range(len(records_ov)): 
            records_ov_dict=records_ov[i]        
            area_name=str(records_ov_dict["area_name"])      
            area_id=str(records_ov_dict["area_id"])      
            totalprice=records_ov_dict["totalprice"]

            qset_oc=db()
            qset_oc=qset_oc((db.sm_order_head.cid == cid)  & (db.sm_order_head.field1 == 'ORDER')) 
            qset_oc=qset_oc((db.sm_order_head.order_date == date_from))
            
            
            qset_oc=qset_oc((db.sm_order_head.area_id==area_id))
            records_oc=qset_oc.select(db.sm_order_head.sl.count())

            # return records_oc
            if records_oc:
                order_count=records_oc[0][db.sm_order_head.sl.count()]

            # ----------------------
            qset_s=db()
            qset_s=qset_s((db.sm_order_head.cid == cid)  ) 
            qset_s=qset_s((db.sm_order_head.order_date == date_from))
            
            
            qset_s=qset_s((db.sm_order_head.area_id==area_id))
            records_s=qset_s.select(db.sm_order_head.sl.count())

            # return records_oc
            if records_s:
                sales_call=records_s[0][db.sm_order_head.sl.count()]






             
                                 

            report_str=report_str+'<td style="padding-left:0px;">'+str(area_name)+'|'+str(area_id)+'</td>'

            report_str=report_str+'<td align="center">'+str(sales_call)+'</td>'
            report_str=report_str+'<td align="center">'+str(order_count)+'</td>'
            report_str=report_str+'<td align="right">'+str(totalprice)+'</td>'
             
            report_str=report_str+'</tr>'
            # gtotalprice+=int((totalprice).split('.')[0])
            gtotalprice+=totalprice
        report_str=report_str+'<tr><td colspan="3" align="right">Total Amount</td><td colspan="1" align="right">'+str(gtotalprice).split('.')[0]+'</td></tr>'

        
        linkPath="window.open('"+sals_rprt_more_path+"sales_report_detail_url?"+"cid="+cid+"&rep_id="+rep_id+"&password="+password+"&synccode="+synccode+"&se_item_report="+se_item_report+"&se_market_report="+se_market_report+" ', '_system');"

        report_str=report_str+'<tr> <td colspan="4" align="right" style="padding:5px 0"><a onClick="'+linkPath+'" target="_blank" style="width: 50px;height: auto;padding: 5px 14px;background: #7a828e;">More</a></td></tr></table>'  
       
        
    if (user_type=='SUP'):
        levelList=[]
        marketList=[]
        spicial_codeList=[]
        marketStr=''
        SuplevelRows = db((db.sm_supervisor_level.cid == cid) & (db.sm_supervisor_level.sup_id == rep_id) ).select(db.sm_supervisor_level.level_id,db.sm_supervisor_level.level_depth_no, orderby=~db.sm_supervisor_level.level_id)
        # return db._lastsql
        for SuplevelRows in SuplevelRows:
            Suplevel_id = SuplevelRows.level_id
            depth = SuplevelRows.level_depth_no
            level = 'level' + str(depth)

            if Suplevel_id not in levelList:
                levelList.append(Suplevel_id)
        # return len(levelList)
        cTeam=0
        for i in range(len(levelList)):

            if (level=='level0'):
                levelRows = db((db.sm_level.cid == cid) &(db.sm_level.depth == '1') & (db.sm_level[level] == levelList[i]) ).select(db.sm_level.level_id, db.sm_level.level_name, db.sm_level.depot_id,db.sm_level.special_territory_code)
                # return levelRows
            if (level=='level1'):
                levelRows = db((db.sm_level.cid == cid) &(db.sm_level.depth == '2') &(db.sm_level[level] == levelList[i]) ).select(db.sm_level.level_id, db.sm_level.level_name, db.sm_level.depot_id,db.sm_level.special_territory_code)
                        
            if (level=='level2'):
                levelRows = db((db.sm_level.cid == cid)  &(db.sm_level.depth == '3') & (db.sm_level[level] == levelList[i]) ).select(db.sm_level.level_id, db.sm_level.level_name, db.sm_level.depot_id,db.sm_level.special_territory_code)
           
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
                if special_territory_code not in spicial_codeList:
                    if (special_territory_code !='' and level_id==special_territory_code):
                        spicial_codeList.append(special_territory_code)    
            
                    levelSpecialRows = db((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '1') & (db.sm_level.special_territory_code.belongs(spicial_codeList)) ).select(db.sm_level.level_id, db.sm_level.level_name, db.sm_level.depot_id)        

                    for levelSpecialRow in levelSpecialRows:
                        level_id = levelSpecialRow.level_id
                        if marketStr=='':
                            marketStr="'"+str(Suplevel_id)+"'"
                        else:
                            marketStr=marketStr+",'"+str(level_id)+"'" 

        condition=''
        if (se_market_report!="ALL"):
            condition=condition+"AND area_id = '"+str(se_market_report)+"'"

        records_ov=[]
        if (level=='level0'):
            level_name='Region'

            condition=condition+" AND level1_id IN ("+str(marketStr)+")"  
            sql_str="SELECT SUM( (sm_order.price) * ( sm_order.quantity ) ) AS totalprice, sm_order.level1_id AS level1_id, sm_order.level1_name AS level1_name,sm_order.area_id AS area_id, sm_order.area_name AS area_name,sm_order.rep_id as rep_id FROM sm_order WHERE sm_order.cid =  '"+ str(cid) +"' AND sm_order.order_date >=  '"+ str(date_from) +"' AND sm_order.order_date <  '"+ str(date_to) +"' "+ condition + " GROUP BY sm_order.level1_id  order by order_date desc, level1_name asc"
            # return sql_str
        if (level=='level1'):
            level_name='Area'

            condition=condition+" AND level2_id IN ("+str(marketStr)+")"  
            sql_str="SELECT SUM( (sm_order.price) * ( sm_order.quantity ) ) AS totalprice,sm_order.level2_id AS level2_id, sm_order.level2_name AS level2_name, sm_order.area_id AS area_id, sm_order.area_name AS area_name,sm_order.rep_id as rep_id FROM sm_order WHERE sm_order.cid =  '"+ str(cid) +"' AND sm_order.order_date >=  '"+ str(date_from) +"' AND sm_order.order_date <  '"+ str(date_to) +"' "+ condition + " GROUP BY sm_order.level2_id  order by order_date desc, level2_name asc"
        if (level=='level2'):
            level_name='Territory'
            if marketStr!='':
                condition=condition+" AND area_id IN ("+str(marketStr)+")"  
            else:
                return 'FAILED<SYNCDATA>Data not available'
            sql_str="SELECT SUM( (sm_order.price) * ( sm_order.quantity ) ) AS totalprice, sm_order.area_id AS area_id, sm_order.area_name AS area_name,sm_order.rep_id as rep_id FROM sm_order WHERE sm_order.cid =  '"+ str(cid) +"' AND sm_order.order_date >=  '"+ str(date_from) +"' AND sm_order.order_date <  '"+ str(date_to) +"' "+ condition + " GROUP BY sm_order.area_id  order by order_date desc, area_name asc"
            # return sql_str
        records_ov=db.executesql(sql_str,as_dict = True)

        order_value='0.0'
        areawise_flag=0
        areawise_str=""
        total_value=0

# =================================
        if (level=='level0'):
            condition_1=" AND level1_id IN ("+str(marketStr)+")"  
            sql_str_total="SELECT SUM( (sm_order.price) * ( sm_order.quantity ) ) AS totalprice, sm_order.level0_id AS level0_id, sm_order.level1_name AS level0_name,sm_order.area_id AS area_id, sm_order.area_name AS area_name,sm_order.rep_id as rep_id FROM sm_order WHERE sm_order.cid =  '"+ str(cid) +"' AND sm_order.order_date >=  '"+ str(date_from) +"' AND sm_order.order_date <  '"+ str(date_to) +"' "+ condition + " GROUP BY sm_order.level0_id  order by order_date desc, level0_name asc"
            # return sql_str_total
            records_ov_total=db.executesql(sql_str_total,as_dict = True)
            report_str_total="""<table width="100%" border="1" cellpadding="0" cellspacing="0" style="border:solid; border-style:solid; border-color:#0CF; color:#fff"> 
                                <tr  class="blackCatHead"  >
                                <td >Zone</td>
                                <td width="10%" align="center"  >Visit Count</td>
                                <td width="10%" align="center"  >Order Count</td>
                                <td width="10%" align="right"  >Amount</td>
                                </tr>"""
            for i in range(len(records_ov_total)): 
                records_ov_dict_total=records_ov_total[i] 

                leve0_id=str(records_ov_dict_total["level0_id"])   
                leve0_idName=str(records_ov_dict_total["level0_id"])+'|'+  str(records_ov_dict_total["level0_name"])    

                totalprice_total=int(round(records_ov_dict_total["totalprice"]))   

                qset_vc_str_total="SELECT count(sl) as Vcount_total FROM sm_order_head WHERE cid =  '"+ str(cid) +"' AND order_date >=  '"+ str(date_from) +"' AND order_date <  '"+ str(date_to) +"' AND level0_id = '"+str(leve0_id)+"'" 
                reportRows_count_total=db.executesql(qset_vc_str_total,as_dict = True)

                visit_count_total=0
                for reportRows_count_total in reportRows_count_total:
                    visit_count_total=reportRows_count_total['Vcount_total']

                qset_oc_str_total="SELECT count(sl) as Ocount_total FROM sm_order_head WHERE cid =  '"+ str(cid) +"' AND field1 = 'ORDER' AND order_date >=  '"+ str(date_from) +"' AND order_date <  '"+ str(date_to) +"' AND level0_id = '"+str(leve0_id)+"'" 
                
                reportRows_order_count_total=db.executesql(qset_oc_str_total,as_dict = True)

                order_count_total=0
                for reportRows_order_count_total in reportRows_order_count_total:
                    order_count_total=reportRows_order_count_total['Ocount_total']
                
                report_str_total=report_str_total+'<tr><td style="padding-left:0px;">'+str(leve0_idName)+'</td><td align="center">'+str(visit_count_total)+'</td>'
                report_str_total=report_str_total+'<td align="center">'+str(order_count_total)+'</td>'
                report_str_total=report_str_total+'<td align="right">'+str(totalprice_total)+'</td>'
                 
                report_str_total=report_str_total+'</tr>'
            report_str_total=report_str_total+'</table><br>'

# ========================





        report_str=report_str+"""<table width="100%" border="1" cellpadding="0" cellspacing="0" style="border:solid; border-style:solid; border-color:transparent; color:#fff;background:#7a828e;padding:5px"><tr align="left" class="blackCatHead"  ><td width="100%">Sales Report &nbsp;:&nbsp;&nbsp;Today</td></tr></table><br>"""

        if (level=='level0'):
            report_str=report_str+report_str_total

        report_str=report_str+"""<table width="100%" border="1" cellpadding="0" cellspacing="0" style="border:solid; border-style:solid; border-color:#0CF; color:#fff"> 
                                <tr  class="blackCatHead"  >
                                <td >"""+level_name+"""</td>
                                <td width="10%" align="center"  >Visit Count</td>
                                <td width="10%" align="center"  >Order Count</td>
                                <td width="10%" align="right"  >Amount</td>
                                </tr>"""
        level_idName=''
        area_id=''
        area_name=''
        gtotalprice=0.0

        for i in range(len(records_ov)): 
            records_ov_dict=records_ov[i] 
            if (areawise_flag==0):
                repwise_str='Area wise: </br>'
                areawise_flag=1 

            if (level=='level0'):
                level_id=str(records_ov_dict["level1_id"])   
                level_idName=str(records_ov_dict["level1_id"])+'|'+  str(records_ov_dict["level1_name"])    

                totalprice=int(round(records_ov_dict["totalprice"]))   

                qset_vc_str="SELECT count(sl) as Vcount FROM sm_order_head WHERE cid =  '"+ str(cid) +"' AND order_date >=  '"+ str(date_from) +"' AND order_date <  '"+ str(date_to) +"' AND level1_id = '"+str(level_id)+"'" 
                reportRows_count=db.executesql(qset_vc_str,as_dict = True)

                visit_count=0
                for reportRows_count in reportRows_count:
                    visit_count=reportRows_count['Vcount']

                qset_oc_str="SELECT count(sl) as Ocount FROM sm_order_head WHERE cid =  '"+ str(cid) +"' AND field1 = 'ORDER' AND order_date >=  '"+ str(date_from) +"' AND order_date <  '"+ str(date_to) +"' AND level1_id = '"+str(level_id)+"'" 
                
                reportRows_order_count=db.executesql(qset_oc_str,as_dict = True)

                order_count=0
                for reportRows_order_count in reportRows_order_count:
                    order_count=reportRows_order_count['Ocount']



            if (level=='level1'):
                level_id=str(records_ov_dict["level2_id"])   
                level_idName=str(records_ov_dict["level2_id"])+'|'+  str(records_ov_dict["level2_name"])    
                 
                condition=condition+" AND level2_id IN ("+str(marketStr)+")"  
                totalprice=int(round(records_ov_dict["totalprice"]))   

                qset_vc_str="SELECT count(sl) as Vcount FROM sm_order_head WHERE cid =  '"+ str(cid) +"' AND order_date >=  '"+ str(date_from) +"' AND order_date <  '"+ str(date_to) +"' AND level2_id = '"+str(level_id)+"' " 
                reportRows_count=db.executesql(qset_vc_str,as_dict = True)
                visit_count=0
                for reportRows_count in reportRows_count:
                    visit_count=reportRows_count['Vcount']

                qset_oc_str="SELECT count(sl) as Ocount FROM sm_order_head WHERE cid =  '"+ str(cid) +"' AND field1 = 'ORDER' AND order_date >=  '"+ str(date_from) +"' AND order_date <  '"+ str(date_to) +"' AND level2_id = '"+str(level_id)+"'" 
                reportRows_order_count=db.executesql(qset_oc_str,as_dict = True)

                order_count=0
                for reportRows_order_count in reportRows_order_count:
                    order_count=reportRows_order_count['Ocount']


            if (level=='level2'):
                level_id=str(records_ov_dict["area_id"])   
      
                area_id=str(records_ov_dict["area_id"])      
                area_name=str(records_ov_dict["area_name"])      
                rep_id_detail=str(records_ov_dict["rep_id"])      
                totalprice=int(round(records_ov_dict["totalprice"]))   

                qset_vc_str="SELECT count(sl) as Vcount FROM sm_order_head WHERE cid =  '"+ str(cid) +"' AND order_date >=  '"+ str(date_from) +"' AND order_date <  '"+ str(date_to) +"' AND area_id = '"+str(area_id)+"'" 
                reportRows_count=db.executesql(qset_vc_str,as_dict = True)
                visit_count=0
                for reportRows_count in reportRows_count:
                    visit_count=reportRows_count['Vcount']

                qset_oc_str="SELECT count(sl) as Ocount FROM sm_order_head WHERE cid =  '"+ str(cid) +"' AND field1 = 'ORDER' AND order_date >=  '"+ str(date_from) +"' AND order_date <  '"+ str(date_to) +"' AND area_id = '"+str(area_id)+"'" 
                reportRows_order_count=db.executesql(qset_oc_str,as_dict = True)

                order_count=0
                for reportRows_order_count in reportRows_order_count:
                    order_count=reportRows_order_count['Ocount']


                                 
            if (level=='level0'):
                report_str=report_str+'<td style="padding-left:0px;">'+str(level_idName)+'</td>'
            pass
                                 
            if (level=='level1'):
                report_str=report_str+'<td style="padding-left:0px;">'+str(level_idName)+'</td>'
            pass              
            if (level=='level2'):
                report_str=report_str+'<td style="padding-left:0px;">'+str(area_name)+'|'+str(area_id)+'</td>'

            pass


            report_str=report_str+'<td align="center">'+str(visit_count)+'</td>'
            report_str=report_str+'<td align="center">'+str(order_count)+'</td>'
            report_str=report_str+'<td align="right">'+str(totalprice)+'</td>'
             
            report_str=report_str+'</tr>'
            # gtotalprice+=int(round(totalprice))
            gtotalprice+=totalprice
        report_str=report_str+'<tr><td colspan="3" align="right">Total Amount</td><td colspan="1" align="right">'+str(gtotalprice).split('.')[0]+'</td></tr>'

        if (level=='level0'):
            linkPath="window.open('"+sals_rprt_more_path+"sales_report_zm_url?"+"cid="+cid+"&rep_id="+rep_id+"&password="+password+"&synccode="+synccode+"&se_item_report="+se_item_report+"&se_market_report="+se_market_report+"&level_id="+level_id+"&date_from="+date_from+" ', '_system');"
            pass
        if (level=='level1'):
            linkPath="window.open('"+sals_rprt_more_path+"sales_report_rsm_url?"+"cid="+cid+"&rep_id="+rep_id+"&password="+password+"&synccode="+synccode+"&se_item_report="+se_item_report+"&se_market_report="+se_market_report+"&level_id="+level_id+"&date_from="+date_from+" ', '_system');"
            pass
        if (level=='level2'):
            linkPath="window.open('"+sals_rprt_more_path+"sales_report_detail_url?"+"cid="+cid+"&rep_id="+rep_id+"&password="+password+"&synccode="+synccode+"&se_item_report="+se_item_report+"&se_market_report="+se_market_report+" ', '_system');"
            pass
            


        report_str=report_str+'<tr> <td colspan="4" align="right" style="padding:5px 0px"><a onClick="'+linkPath+'" target="_blank" style="width: 50px;height: auto;padding: 5px 14px;background: #7a828e;">More</a></td></tr></table>'  
      
    return 'SUCCESS<SYNCDATA>'+report_str



# ===================== 20210830 sales order report  END=================


    # ========================= SALES REPORT DCR ================

def salesRprt_doctor():
    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.rep_pass).strip()
    synccode = str(request.vars.synccode).strip()
    
    rep_id_report = str(request.vars.rep_id).strip().upper()    
    se_item_report ='ALL'
    se_market_report = 'ALL'
    user_type = str(request.vars.user_type).strip().upper()
    
    
    date_from = current_date
    now = datetime.datetime.strptime(current_date, "%Y-%m-%d")
    date_ton=now + datetime.timedelta(days = 1)
    date_to=str(date_ton).split(' ')[0]
    
    # sals_rprt_dcr_more_path='http://127.0.0.1:8000/navana/sales_report/'

    sals_rprt_dcr_more_path=''
#    return date_to
    report_url = db((db.sm_settings.cid == cid) & (db.sm_settings.s_key == 'web_report_url') ).select(db.sm_settings.s_value, limitby=(0, 1))
    
    if not report_url:
       retStatus = 'FAILED<SYNCDATA>Invalid Settings'
       return retStatus
    else:
       sals_rprt_dcr_more_path=report_url[0].s_value



    
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
        repAreaRow = db((db.sm_rep_area.cid == cid) & (db.sm_rep_area.rep_id == rep_id)).select(db.sm_rep_area.area_id,orderby=db.sm_rep_area.area_id,groupby=db.sm_rep_area.area_id)


        rp_areaList=[]
        repAreaStr=''
        for repAreaRow in repAreaRow:
            repArea_id=repAreaRow.area_id
            rp_areaList.append(repArea_id)
            if repAreaStr=='':
                repAreaStr="'"+str(repArea_id)+"'"
            else:
                repAreaStr=repAreaStr+",'"+str(repArea_id)+"'" 
        #    Sales Call====================
        

        condition=""

        condition="AND route_id IN ("+str(repAreaStr)+") "
        

        qOc_success_dcr="SELECT  COUNT(sm_doctor_visit.doc_id)as doc_count FROM sm_doctor_visit WHERE sm_doctor_visit.cid = '"+ str(cid) +"' AND sm_doctor_visit.rep_id = '"+ str(rep_id) +"' AND sm_doctor_visit.giftnsample!='' AND sm_doctor_visit.visit_date >= '"+ str(date_from) +"' AND sm_doctor_visit.visit_date < '"+ str(date_to) +"' "+ condition + " GROUP BY sm_doctor_visit.route_id;"
        rptsdcr=db.executesql(qOc_success_dcr,as_dict = True)

        success_dcrC=0
        for rptsdcr in rptsdcr:
            success_dcrC=rptsdcr['doc_count']
            
        records_ov=[]
        sql_str="SELECT  COUNT(sm_doctor_visit.doc_id)as doc_count,sm_doctor_visit.route_id as route_id, sm_doctor_visit.route_name as route_name FROM sm_doctor_visit WHERE sm_doctor_visit.cid = '"+ str(cid) +"' AND sm_doctor_visit.rep_id = '"+ str(rep_id) +"' AND sm_doctor_visit.visit_date >= '"+ str(date_from) +"' AND sm_doctor_visit.visit_date < '"+ str(date_to) +"' "+ condition + " GROUP BY sm_doctor_visit.route_id;"
        records_ov=db.executesql(sql_str,as_dict = True)
        # return sql_str
        report_string=report_string+"""<table width="100%" border="1" cellpadding="0" cellspacing="0" style="border:solid; border-style:solid; border-color:transparent; color:#fff;background:#7a828e;padding:5px "><tr align="left" class="blackCatHead"  ><td width="100%">Sales Report &nbsp;:&nbsp;&nbsp;Today</td></tr></table><br>"""
        report_string=report_string+"""<table width="100%" border="1" cellpadding="0" cellspacing="0" style="border:solid; border-style:solid; border-color:#0CF; color:#fff"> 
                                <tr  class="blackCatHead"  >
                                <td >Territory</td>
                                <td width="10%" align="center"  >Visit Count</td>
                                <td width="10%" align="center"  >Succesful DCR</td>
                                </tr>"""
        for i in range(len(records_ov)): 
            records_ov_dict=records_ov[i]        
            doc_visit_count=str(records_ov_dict["doc_count"])      
            route_name=str(records_ov_dict["route_name"])      
            route_id=str(records_ov_dict["route_id"])      
                                 

            report_string=report_string+'<td style="padding-left:0px;">'+str(route_name)+'|'+str(route_id)+'</td>'

            report_string=report_string+'<td align="center">'+str(doc_visit_count)+'</td>'
            report_string=report_string+'<td align="center">'+str(success_dcrC)+'</td>'
             
            report_string=report_string+'</tr>'

        
        linkPath="window.open('"+sals_rprt_dcr_more_path+"salesDcr_report_detail?"+"cid="+cid+"&rep_id="+rep_id+"&password="+password+"&synccode="+synccode+" ', '_system');"
        # report_string=report_string+'<tr> <td colspan="4" align="right"><a onClick="'+linkPath+'" target="_blank">More</a></td></tr></table>'  
        
        report_string=report_string+'<tr> <td colspan="4" align="right" style="padding:5px 0px"><a onClick="'+linkPath+'"  style="width: 50px;height: auto;padding: 5px 14px;background: #7a828e;">More</a></td></tr></table>'  
       
            
            
    if (user_type=='SUP'):   

        levelList=[]
        SuplevelRows = db((db.sm_supervisor_level.cid == cid) & (db.sm_supervisor_level.sup_id == rep_id) ).select(db.sm_supervisor_level.level_id,db.sm_supervisor_level.level_depth_no, orderby=~db.sm_supervisor_level.level_id)
        
        levelStr=''
        for SuplevelRows in SuplevelRows:
            Suplevel_id = SuplevelRows.level_id
            depth = SuplevelRows.level_depth_no
            level = 'level' + str(depth)#+'_id'
            if Suplevel_id not in levelList:
                levelList.append(Suplevel_id)
                if levelStr=='':
                    levelStr="'"+str(Suplevel_id)+"'"
                else:
                    levelStr=levelStr+",'"+str(Suplevel_id)+"'" 


        marketStr=''
        marketStrList=[]
        for i in range(len(levelList)):
            
            levelRows = db((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '1') & (db.sm_level[level] == levelList[i]) ).select(db.sm_level.level_id, db.sm_level.level_name, db.sm_level.depot_id,db.sm_level.special_territory_code)
            for levelRow in levelRows:
                level_id = levelRow.level_id
                marketStrList.append(level_id)
                special_territory_code = levelRow.special_territory_code
                if level_id==special_territory_code:
                    cTeam=1

                if marketStr=='':
                    marketStr="'"+str(level_id)+"'"
                else:
                    marketStr=marketStr+",'"+str(level_id)+"'" 

        # return  marketStr           
        condition=''

        condition=condition+"AND route_id IN ("+str(marketStr)+")"

        qset=db()
        qset = qset(db.sm_doctor_visit.cid == cid)
        qset = qset(db.sm_doctor_visit.route_id.belongs(marketStrList))
        qset = qset((db.sm_doctor_visit.visit_date == date_from))

        records = qset.select(db.sm_doctor_visit.doc_id.count(),db.sm_doctor_visit.doc_id,db.sm_doctor_visit.rep_id,db.sm_doctor_visit.route_id,db.sm_doctor_visit.route_name,db.sm_doctor_visit.visit_date, orderby=~db.sm_doctor_visit.visit_date, groupby=db.sm_doctor_visit.route_id)
        # return db._lastsql

        if records:
            for i in range(len(records)):
                recordListStr = records[i]
                doc_id = recordListStr[db.sm_doctor_visit.doc_id]
                visit_date = recordListStr[db.sm_doctor_visit.visit_date]
               
                

        qsetCount=db()
        qsetCount = qsetCount(db.sm_doctor_visit.cid == cid)
        qsetCount = qsetCount(db.sm_doctor_visit.giftnsample!='')
        qsetCount = qsetCount(db.sm_doctor_visit.route_id.belongs(marketStrList))
        qsetCount = qsetCount((db.sm_doctor_visit.visit_date == date_from))

        recordsCount = qsetCount.select(db.sm_doctor_visit.doc_id.count(),db.sm_doctor_visit.doc_id,db.sm_doctor_visit.rep_id,db.sm_doctor_visit.route_id,db.sm_doctor_visit.route_name,db.sm_doctor_visit.visit_date, orderby=~db.sm_doctor_visit.visit_date, groupby=db.sm_doctor_visit.route_id)
        vChecklist=[]
        vCountList=[]
        for recordsCount in recordsCount:
            vCount=recordsCount[db.sm_doctor_visit.doc_id.count()]
            vCheck=str(recordsCount[db.sm_doctor_visit.rep_id])+'|'+str(recordsCount[db.sm_doctor_visit.visit_date])
            vChecklist.append(vCheck)
            vCountList.append(vCount)


        report_string=report_string+"""<table width="100%" border="1" cellpadding="0" cellspacing="0" style="border:solid; border-style:solid; border-color:transparent; color:#fff;background:#7a828e;padding:5px"><tr align="left" class="blackCatHead"  ><td width="100%">Sales Report &nbsp;:&nbsp;&nbsp;Today</td></tr></table><br>"""



        report_string=report_string+"""<table width="100%" border="1" cellpadding="0" cellspacing="0" style="border:solid; border-style:solid; border-color:#0CF; color:#fff"> 
                                <tr  class="blackCatHead"  >
                                <td >Territory</td>
                                <td width="10%" align="center"  >Visit Count</td>
                                <td width="10%" align="center"  >Succesful DCR</td>
                                </tr>"""
        for i,record in enumerate(records):
            doc_id_c=record[(db.sm_doctor_visit.doc_id.count())]
            docId_check=record[(db.sm_doctor_visit.rep_id)]+'|'+str(record[(db.sm_doctor_visit.visit_date)])
            visit_date=record[(db.sm_doctor_visit.visit_date)]
            route_id=record[(db.sm_doctor_visit.route_id)]
            route_name=record[(db.sm_doctor_visit.route_name)]
            doc_count=0
            if [s for s in vChecklist if docId_check in s]:
                index_element = vChecklist.index(docId_check)           
                doc_count=vCountList[index_element]
            pass

            report_string=report_string+'<td style="padding-left:0px;">'+str(route_name)+'|'+str(route_id)+'</td>'

            report_string=report_string+'<td align="center">'+str(doc_id_c)+'</td>'
            report_string=report_string+'<td align="center">'+str(doc_count)+'</td>'
             
            report_string=report_string+'</tr>'

        # return rep_id
        linkPath="window.open('"+sals_rprt_dcr_more_path+"salesDcr_report_detail?"+"cid="+cid+"&rep_id="+rep_id+"&password="+password+"&synccode="+synccode+"&se_item_report="+se_item_report+"&se_market_report="+se_market_report+" ', '_system');"

        
        report_string=report_string+'<tr> <td colspan="4" align="right" style="padding:5px 0px"><a onClick="'+linkPath+'"  style="width: 50px;height: auto;padding: 5px 14px;background: #7a828e;">More</a></td></tr></table>'  
        
    

    
    return 'SUCCESS<SYNCDATA>'+report_string











def s_call_order_detail():
#     return 'SUCCESS<SYNCDATA>'+'Please try later'
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
           condition="and sm_order.area_id='"+ str(se_market_report) +"' "

#        records_ov=qset_ov.select(db.sm_order.price.sum(),db.sm_order.area_id,db.sm_order.area_name, groupby=db.sm_order.area_id)
        records_ov=[]
        sql_str="SELECT SUM((sm_order.price) * (sm_order.quantity)) as totalprice, sm_order.area_id as area_id, sm_order.area_name as area_name FROM sm_order WHERE sm_order.cid = '"+ str(cid) +"' AND sm_order.rep_id = '"+ str(rep_id) +"' AND sm_order.order_date >= '"+ str(date_from) +"' AND sm_order.order_date < '"+ str(date_to) +"' "+ condition + " GROUP BY sm_order.area_id;"
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
        qset_ol=qset_ol((db.sm_order_head.order_date >= date_from) & (db.sm_order_head.order_date  < date_to))
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
                payment_mode=record_o.payment_mode
                
                    
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
            condition=condition+"AND area_id = '"+str(se_market_report)+"'"
        if (rep_id!=rep_id_report):
            condition=condition+"AND rep_id = '"+str(rep_id_report)+"'"
        condition=condition+" AND area_id IN ("+str(marketStr)+")"  
        
        qset_vc_str="SELECT count(sl) as Vcount FROM sm_order_head WHERE cid =  '"+ str(cid) +"' AND order_date >=  '"+ str(date_from) +"' AND order_date <  '"+ str(date_to) +"' "+ condition + " "
#         return qset_vc_str
        reportRows_count=db.executesql(qset_vc_str,as_dict = True)

        visit_count=0
        for reportRows_count in reportRows_count:
            visit_count=reportRows_count['Vcount']

#        ==== Order Count====================
        qset_oc_str="SELECT count(sl) as Ocount FROM sm_order_head WHERE cid =  '"+ str(cid) +"' AND field1 = 'ORDER' AND order_date >=  '"+ str(date_from) +"' AND order_date <  '"+ str(date_to) +"' "+ condition + " "
        reportRows_order_count=db.executesql(qset_oc_str,as_dict = True)

        order_count=0
        for reportRows_order_count in reportRows_order_count:
            order_count=reportRows_order_count['Ocount']

# #            =============area wise Value

 

        records_ov=[]
        sql_str="SELECT SUM( (sm_order.price) * ( sm_order.quantity ) ) AS totalprice, sm_order.area_id AS area_id, sm_order.area_name AS area_name FROM sm_order WHERE sm_order.cid =  '"+ str(cid) +"' AND sm_order.order_date >=  '"+ str(date_from) +"' AND sm_order.order_date <  '"+ str(date_to) +"' "+ condition + " GROUP BY sm_order.area_name"
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
#     return 'SUCCESS<SYNCDATA>'+'Please try later'
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
        # ============ 20210609 START==============
        for SuplevelRows in SuplevelRows:
            Suplevel_id = SuplevelRows.level_id
            depth = SuplevelRows.level_depth_no
            level = 'level' + str(depth)#+'_id'
            if Suplevel_id not in levelList:
                levelList.append(Suplevel_id)
                if levelStr=='':
                    levelStr="'"+str(Suplevel_id)+"'"
                else:
                    levelStr=levelStr+",'"+str(Suplevel_id)+"'"  
        marketStr=''
        marketStrList=[]
        for i in range(len(levelList)):
            
            levelRows = db((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '1') & (db.sm_level[level] == levelList[i]) ).select(db.sm_level.level_id, db.sm_level.level_name, db.sm_level.depot_id,db.sm_level.special_territory_code)
            for levelRow in levelRows:
                level_id = levelRow.level_id
                marketStrList.append(level_id)
                special_territory_code = levelRow.special_territory_code
                if level_id==special_territory_code:
                    cTeam=1

                if marketStr=='':
                    marketStr="'"+str(level_id)+"'"
                else:
                    marketStr=marketStr+",'"+str(level_id)+"'"   

        condition=''
        if (se_market_report!="ALL"):
            condition=condition+"AND route_id = '"+str(se_market_report)+"'"
        if (rep_id!=rep_id_report):
            condition=condition+"AND rep_id = '"+str(rep_id_report)+"'"
        condition=condition+"AND route_id IN ("+str(marketStr)+")" 

    # ============ 20210609 ==============

        qset_vcS="SELECT  count(id) as visitCount FROM sm_doctor_visit WHERE cid = '"+ cid +"' AND  visit_date >= '"+str(date_from).split(' ')[0]+"' AND visit_date < '"+str(date_to).split(' ')[0]+"'"+condition+"  limit  1;"       
        reportRows_count=db.executesql(qset_vcS,as_dict = True) 
        visit_count=''
        for reportRows_count in reportRows_count:
            visit_count=reportRows_count['visitCount']
            

#        =============area wise
  
        qset_acS="SELECT  count(id) as vCount,route_id,route_name FROM sm_doctor_visit WHERE cid = '"+ cid +"' AND  visit_date >= '"+str(date_from).split(' ')[0]+"' AND     visit_date < '"+str(date_to).split(' ')[0]+"'"+condition+"  group by route_id;"
        reportRows=db.executesql(qset_acS,as_dict = True) 
        # return qset_acS
        areawise_str=''
        areawise_flag=0
        
        
        for reportRow in reportRows:
            if (areawise_flag==0):
                areawise_str='Area wise: </br>'
                areawise_flag=1
            areawise_str=areawise_str+str(reportRow['route_name'])+'('+str(reportRow['route_id'])+') --'+str(reportRow['vCount'])+'</br>'
       

#        RepWise=========================

        qset_rcS="SELECT  count(id) as vCount,rep_id,rep_name FROM sm_doctor_visit WHERE cid = '"+ cid +"' AND  visit_date >= '"+str(date_from).split(' ')[0]+"' AND     visit_date < '"+str(date_to).split(' ')[0]+"'"+condition+"  group by rep_id;"
        repRows=db.executesql(qset_rcS,as_dict = True) 
        
    # ============ 20210609  END==============
        
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
#     return 'SUCCESS<SYNCDATA>'+'Please try later'
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
        records_detail=qset_detail.select(db.sm_doctor_visit.ALL, orderby=~db.sm_doctor_visit.id, limitby=(0,50))
        
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
        
        # ============ 20210609 Start ===============
        levelStr=''
        for SuplevelRows in SuplevelRows:
            Suplevel_id = SuplevelRows.level_id
            depth = SuplevelRows.level_depth_no
            level = 'level' + str(depth)#+'_id'
#             return level
            if Suplevel_id not in levelList:
                levelList.append(Suplevel_id)
                if levelStr=='':
                    levelStr="'"+str(Suplevel_id)+"'"
                else:
                    levelStr=levelStr+",'"+str(Suplevel_id)+"'"      
        marketStr=''
        marketStrList=[]
        for i in range(len(levelList)):
            
            levelRows = db((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '1') & (db.sm_level[level] == levelList[i]) ).select(db.sm_level.level_id, db.sm_level.level_name, db.sm_level.depot_id,db.sm_level.special_territory_code)
            for levelRow in levelRows:
                level_id = levelRow.level_id
                marketStrList.append(level_id)
                special_territory_code = levelRow.special_territory_code
                if level_id==special_territory_code:
                    cTeam=1

                if marketStr=='':
                    marketStr="'"+str(level_id)+"'"
                else:
                    marketStr=marketStr+",'"+str(level_id)+"'" 

        condition=''
        if (se_market_report!="ALL"):
            condition=condition+"AND route_id = '"+str(se_market_report)+"'"
        if (rep_id!=rep_id_report):
            condition=condition+"AND rep_id = '"+str(rep_id_report)+"'"

        condition=condition+"AND route_id IN ("+str(marketStr)+")"

        # ============ 20210609 End ===============  
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
        qset_detailS="SELECT  * FROM sm_doctor_visit WHERE cid = '"+ cid +"' AND  visit_dtime >= '"+str(date_from)+"' AND     visit_dtime < '"+str(date_to)+"'"+condition+"  order by id limit  50;"
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
#     return 'SUCCESS<SYNCDATA>'+'Please try later'
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
        return db._lastsql
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
#     return 'SUCCESS<SYNCDATA>'+'Please try later'
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
#     return 'FAILED<SYNCDATA>Please Try Later.'
    randNumber = randint(1001, 9999)

    retStatus = ''

    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.rep_pass).strip()
    synccode = str(request.vars.synccode).strip()
#     return cid




    compRow_str = "SELECT cid,temp_item_list FROM sm_company_settings WHERE cid='"+cid+"' AND status='ACTIVE' LIMIT 1 "
    compRow=db.executesql(compRow_str,as_dict=True)
    # return compRowb
    # compRow = db((db.sm_company_settings.cid == cid) & (db.sm_company_settings.status == 'ACTIVE')).select(db.sm_company_settings.cid, limitby=(0, 1))
    if not compRow:
        return 'FAILED<SYNCDATA>Invalid Company'
    else:
#         'Order|DistributionInvoicing|DCR|Tour|PrescriptionMPO|Attendance|QuickCheckin|PrescriptionTeam|SampleGiftPPMAllocation|Live-checkinFARM'
        
        # module_Str='Order|DistributionInvoicing|DCR|Tour|PrescriptionMPO|Attendance|QuickCheckin|PrescriptionTeam|SampleGiftPPMAllocation|Live-checkin|FARM'
        # module_Str=compRow[0].temp_item_list
        for compRow in compRow:
            module_Str = str(compRow['temp_item_list'])


        repRown = "SELECT id,name,sync_count,first_sync_date,last_sync_date,user_type,depot_id,level_id,field2,note FROM sm_rep WHERE cid='"+cid+"' AND rep_id='"+rep_id+"' AND password='"+password+"' AND status='ACTIVE' LIMIT 1 "
        repRow=db.executesql(repRown,as_dict=True)



        # repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.id, db.sm_rep.name, db.sm_rep.sync_count, db.sm_rep.first_sync_date, db.sm_rep.last_sync_date, db.sm_rep.user_type, db.sm_rep.depot_id, db.sm_rep.level_id, db.sm_rep.field2,db.sm_rep.note, limitby=(0, 1))


#         return repRow
        # return repRow
        if not repRow:
           retStatus = 'FAILED<SYNCDATA>Invalid Authorization 2'
           return retStatus
        else:
            marketStrn=''
            sync_code = str(randNumber)
            for repRow in repRow:

                rep_name = str(repRow['name'])
                depot_id = str(repRow['depot_id'])
                lastSyncTIme=str(repRow['last_sync_date'])


                sync_count = int(repRow['sync_count']) + 1
                first_sync_date = repRow['first_sync_date']
                user_type = repRow['user_type']

                level_id = repRow['level_id']
                depth = repRow['field2']
                level = 'level' + str(depth)
    #             return level_id
                last_sync_date = str(repRow['last_sync_date'])
                repType=repRow['note']
            
            if len(str(lastSyncTIme))< 10 :
                last_sync_date = date_fixed
            if first_sync_date == None:
                first_sync_date = date_fixed
                
            else:
                datetimeFormat = '%Y-%m-%d %H:%M:%S' 
#                 return last_sync_date
                timedelta = datetime.datetime.strptime(datetime_fixed, datetimeFormat) - datetime.datetime.strptime(last_sync_date,datetimeFormat)
#                 return str(timedelta)
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
#                             return 'FAILED<SYNCDATA>You have already synced. Please retry after 30 minutes.'
                    except:
                        pass
            last_sync_date = date_fixed
            if first_sync_date == None:
                first_sync_date = date_fixed


            # rep_updaten = "UPDATE sm_rep SET sync_code='"+str(sync_code)+"' AND first_sync_date='"+str(first_sync_date)+"' AND last_sync_date='"+str(last_sync_date)+"' AND sync_count='"+str(sync_count)+"' WHERE cid='"+cid+"' AND password='"+password+"' AND status='ACTIVE' "
            # rep_update=db.executesql(rep_updaten,as_dict=True)

            rep_update = "UPDATE sm_rep SET sync_code='"+str(sync_code)+"',first_sync_date='"+str(first_sync_date)+"',last_sync_date='"+str(last_sync_date)+"',sync_count='"+str(sync_count)+"'  WHERE cid='"+cid+"' AND rep_id='"+rep_id+"' AND password='"+password+"' AND status='ACTIVE' "
            rep_update=db.executesql(rep_update)

            # rep_update = repRow[0].update_record(sync_code=sync_code, first_sync_date=first_sync_date, last_sync_date=last_sync_date, sync_count=sync_count)

            
            s_key_list=[]
            s_key_list.append('VISIT_SAVE_LIMIT')
            s_key_list.append('ORDER_LOCATION')
            s_key_list.append('DELIVERY_DATE')
            s_key_list.append('PAYMENT_DATE')
            s_key_list.append('PAYMENT_MODE')
            s_key_list.append('COLLECTION_DATE')
            
            if marketStrn=='':
                # marketStrn="'"+str(s_key_list)+"'"
                marketStrn="'"+str(s_key_list).replace("['",""''"")+"'"
                marketStrn=str(marketStrn).replace("']'","'")

            else:
                marketStrn=marketStrn+"'"+str(s_key_list)+"'"
            # return marketStrnn
            # settingsRowls = db((db.sm_settings_pharma.cid == cid) &(db.sm_settings_pharma.s_key.belongs(s_key_list)) ).select(db.sm_settings_pharma.s_key,db.sm_settings_pharma.s_value)

            settingsRowss = "SELECT s_key,s_value FROM sm_settings_pharma WHERE cid='"+cid+"' AND s_key IN("+marketStrn+")"

            settingsRows=db.executesql(settingsRowss,as_dict=True)
 
            # return settingsRows
            # return marketStrn
            visit_save_limit='0'
            visit_location=''
            delivery_date=''
            payment_date=''
            payment_mode=''
            
            # for repRow in repRow:

            #     rep_name = str(repRow['name'])
            for settingsRow in settingsRows:

                rs_key= str(settingsRow['s_key'])
                if (str(settingsRow['s_key'])== 'VISIT_SAVE_LIMIT'):
                    visit_save_limit=str(settingsRow['s_value'])
                if (str(settingsRow['s_key'])== 'ORDER_LOCATION'):
                    visit_location=str(settingsRow['s_value'])
                if (str(settingsRow['s_key'])== 'DELIVERY_DATE'):
                    delivery_date=str(settingsRow['s_value'])
                if (str(settingsRow['s_key'])== 'PAYMENT_DATE'):
                    payment_date=str(settingsRow['s_value'])
                if (str(settingsRow['s_key'])== 'PAYMENT_MODE'):
                    payment_mode=str(settingsRow['s_value'])
                if (str(settingsRow['s_key'])== 'COLLECTION_DATE'):
                    collection_date=str(settingsRow['s_value'])
#========================PromoCombo================

            # promoRows = db((db.sm_promo_product_bonus.cid == cid) &(db.sm_promo_product_bonus.status=='ACTIVE') ).select(db.sm_promo_product_bonus.id,db.sm_promo_product_bonus.circular_number,db.sm_promo_product_bonus.note)

            promoRows = "SELECT id,circular_number,note FROM sm_promo_product_bonus WHERE cid='"+cid+"' AND status='ACTIVE' "
            prmRow=db.executesql(promoRows,as_dict=True)

            promo_str=''

            for prm in prmRow:

                row_id = str(prm['id'])
                circular_number=str(prm['circular_number'])
                note=str(prm['note'])

                   
                if promo_str == '':
                    promo_str = str(row_id) + '<fd>' + str(circular_number)+ '<fd>' + str(note)
                else:
                    promo_str =promo_str+ '<rd>' + str(row_id) + '<fd>' + str(circular_number)+ '<fd>' + str(note)  


# ========================DocCategory & Speciality

            cat_rows = "SELECT category FROM doc_catagory WHERE cid='"+cid+"' ORDER BY id "
            cat_row=db.executesql(cat_rows,as_dict=True)
            
            # cat_row=db(db.doc_catagory.cid == cid).select(db.doc_catagory.category, orderby=db.doc_catagory.category)
            catStr=''
            for cat_row in cat_row:
                catStr=catStr+str(cat_row['category'])+','


            spc_rows = "SELECT specialty FROM doc_speciality WHERE cid='"+cid+"' ORDER BY sl "
            spc_row=db.executesql(spc_rows,as_dict=True)

            # spc_row=db(db.doc_speciality.cid == cid).select(db.doc_speciality.specialty, orderby=db.doc_speciality.specialty    )
            spcStr=''
            for spc_row in spc_row:
                spcStr=spcStr+str(spc_row['specialty'])+','
                
                
#  ==============================   
            
            today_1= time.strftime("%Y-%m-%d")  
            today= datetime.datetime.strptime(today_1, "%Y-%m-%d")
#             tomorrow =today + datetime.timedelta(days = 1)
            tomorrow =today + datetime.timedelta(days = 2)

#    ====================================Prescriptio
             
            # prProductRows = db(db.sm_company_settings.cid == cid).select(db.sm_company_settings.item_list_mobile,db.sm_company_settings.note, limitby=(0,1))
            
            prProductRows = "SELECT item_list_mobile,note FROM sm_company_settings WHERE cid='"+cid+"' LIMIT 1"
            prProductRow=db.executesql(prProductRows,as_dict=True)
            prProductStr = ''
            for prProductRow in prProductRow:
                prProductStr = str(prProductRow['item_list_mobile'])
                prSampleStr =  str(prProductRow['note'])
            

            # cRow_check_rx= db((db.sm_settings.cid == cid) & (db.sm_settings.s_key == 'RX')).select(db.sm_settings.s_value, limitby=(0, 1))
           
            cRow_check_rxs = "SELECT s_value FROM sm_settings WHERE cid='"+cid+"' AND s_key='RX' LIMIT 1"
            cRow_check_rx=db.executesql(cRow_check_rxs,as_dict=True)
            rx_show='NO'
            with_whom=''
            for cRow_check_rx in cRow_check_rx:
                rx_show=str(cRow_check_rx['s_value'])
                
            cRow_check_Wwhoms = "SELECT s_value FROM sm_settings WHERE cid='"+cid+"' AND s_key='WITHWHOM' LIMIT 1"
            cRow_check_Wwhom=db.executesql(cRow_check_Wwhoms,as_dict=True)

            # cRow_check_Wwhom= db((db.sm_settings.cid == cid) & (db.sm_settings.s_key == 'WITHWHOM')).select(db.sm_settings.s_value, limitby=(0, 1))
            for cRow_check_Wwhom in cRow_check_Wwhom:
                with_whom=str(cRow_check_Wwhom['s_value'])   
                
# ============================================   

            cl_cat_rows = "SELECT cat_type_id,cat_type_name FROM sm_category_type WHERE cid='"+cid+"' AND type_name='CLIENT_CATEGORY' ORDER BY cat_type_name"
            cl_cat_row=db.executesql(cl_cat_rows,as_dict=True)

            # cl_cat_row=db((db.sm_category_type.cid == cid) & (db.sm_category_type.type_name=='CLIENT_CATEGORY')).select(db.sm_category_type.cat_type_id,db.sm_category_type.cat_type_name, orderby=db.sm_category_type.cat_type_name)
            cl_catStr=''
            for cl_cat_row in cl_cat_row:
                cl_catStr=cl_catStr+str(cl_cat_row['cat_type_name'])+'|'+str(cl_cat_row['cat_type_id'])+','
            

            cl_subcat_rows = "SELECT cat_type_id,cat_type_name FROM sm_category_type WHERE cid='"+cid+"' AND type_name='CLIENT_SUB_CATEGORY' ORDER BY cat_type_name"
            cl_subcat_row=db.executesql(cl_subcat_rows,as_dict=True)

            # cl_subcat_row=db((db.sm_category_type.cid == cid) & (db.sm_category_type.type_name=='CLIENT_SUB_CATEGORY')).select(db.sm_category_type.cat_type_id,db.sm_category_type.cat_type_name, orderby=db.sm_category_type.cat_type_name)
            
            cl_subcatStr=''
            for cl_subcat_row in cl_subcat_row:
                cl_subcatStr=cl_subcatStr+str(cl_subcat_row['cat_type_name'])+'|'+str(cl_subcat_row['cat_type_id'])+','    
            

            productcomRows = "SELECT item_id,name FROM sm_item WHERE cid='"+cid+"' ORDER BY item_id"
            productcomRow=db.executesql(productcomRows,as_dict=True)

            # productcomRow=db(db.sm_item.cid == cid).select(db.sm_item.item_id, db.sm_item.name)    

            productcomStr='' 
            for productcomRow in productcomRow:
                item_id = str(productcomRow['item_id'])
                name = str(productcomRow['name'])
              
                if productcomStr == '':
                    productcomStr = str(item_id) + '<fd>' + str(name)
                else:
                    productcomStr += '<rd>' + str(item_id) + '<fd>' + str(name) 
                    
            cRow_check_Ddegree = "SELECT s_value FROM sm_settings WHERE cid='"+cid+"' AND s_key='Doc_degree' LIMIT 1"
            cRow_check_Ddegree=db.executesql(cRow_check_Ddegree,as_dict=True)

            # cRow_check_Wwhom= db((db.sm_settings.cid == cid) & (db.sm_settings.s_key == 'WITHWHOM')).select(db.sm_settings.s_value, limitby=(0, 1))
            for cRow_check_Ddegree in cRow_check_Ddegree:
                doc_degree_str=str(cRow_check_Ddegree['s_value'])  
            # doc_degree_str='MBBS,DMF,BDS,DMA,DDT,DMS,BPT,RMP,LMAF,BSC,DMT,BUMS,DMTD,BDA,DHMS,LMF,DMDT,BSPT,VD,BAMS,BDHT,PC,BSS,DID,DPT,LMAFP,CDT,D PHARM,DM,DUMS,BRMP,BSMF,DAMS,DIPLOMA,DMCH,DMP,BDT,DT,FWV,FCPS,PGT,CCD,MD,MCPS,MPH,MS,CMU,FCGP,FRCP,FCCP,FRCS,DCH,D-CARD,DDV,DMU,DGO,DTCD,MPHIL,D-ORTHO,BHS,FT,DO,DLO,DU,FMD,MRCP,MCH,DMC,FRSH,DPH,PHD,MSC,DCM,CPR,DA,DEM,FP,MACP,CULTRA,MRCS,EOC,EDC,CCU,DOC,IMCI,RMP,MAMS,FICS,PGPN,FWHO,C-CARD,CCCD,DD,DMUD,FACP,DCO,CDD,FACC,FELLOW,ACLS,CC,DLP,FAMS,FTC,VD,WHO,DDS,DMCH,DTM,ICO,MRSH,MSS,AO,DFM,DTMH,PGD,BHE,BPT,DDT,MACE,MRCOG,ADMS,CMH,DGHS,DMF,DPM,EOCT,FACS,FICO,LMAFP,MRCPS,PDT,AMC,CMT,CMUD,DAMS,DDM,DVD,FCPC,FCPGS,FMAS,FESC,FRSPH,MMED,CCE,DDC,FACE,CDV,DM,FAAP,FAPSIC,FELLO,FOS,FRCH,FRSM,IHT,MACG,MPT,CCC,CRP,DMAS,FRSTMH,FSCAI,MCGP,'
# ==================================
            doctor_area_past=''
            srart_a_flag=0
            doctorStr_flag=0
            if (user_type == 'rep'):

                linkpathRows = "SELECT link_name,link_path,field1 FROM sm_linkpath WHERE cid='"+cid+"' AND user_type='rep' ORDER BY link_name"
                linkpathRows=db.executesql(linkpathRows,as_dict=True)

                # linkpathRows = db((db.sm_linkpath.cid == cid) & (db.sm_linkpath.user_type == 'rep')).select(db.sm_linkpath.link_name, db.sm_linkpath.link_path, db.sm_linkpath.field1, orderby=db.sm_linkpath.link_name)
#                 return db._lastsql
                linkStr=''
                for linkpathRows in linkpathRows:
                    link_name = str(linkpathRows['link_name'])
                    link_path = str(linkpathRows['link_path'])
                    checkType=  str(linkpathRows['field1'])
                    
                    if linkStr == '':
                        linkStr = str(link_name) + '<fd>' + str(link_path)+ '<fd>' + str(checkType)
                    else:
                        linkStr += '<rd>' + str(link_name) + '<fd>' + str(link_path)+ '<fd>' + str(checkType)
                        
                        
                        
                #------ market list
                
                marketStr = ''
                repareaListn = ''
                repareaList=[]
                marketRow = "SELECT area_id,area_name FROM sm_rep_area WHERE cid='"+cid+"' AND rep_id='"+rep_id+"' GROUP BY area_id ORDER BY area_name "
                marketRows=db.executesql(marketRow,as_dict=True)

                # marketRows = db((db.sm_rep_area.cid == cid) & (db.sm_rep_area.rep_id == rep_id)).select(db.sm_rep_area.area_id, db.sm_rep_area.area_name, orderby=db.sm_rep_area.area_name, groupby=db.sm_rep_area.area_id)
               
                # return db._lastsql
                repareaListn=''
                for marketRow in marketRows:
                    area_id = str(marketRow['area_id'])
                    area_name = str(marketRow['area_name'])
                    repareaList.append(area_id)


                    if repareaListn=='':
                        # repareaListn="'"+str(s_key_list)+"'"
                        repareaListn="'"+str(area_id)+"'"
                        # repareaListn=str(area_id).replace("']'","'")
                        


                    else:
                        repareaListn=repareaListn+"'"+str(area_id)+"'"
                        # repareaListn=repareaListn+"'"+str(repareaList)+"'"
                    # return repareaListn 


                    if marketStr == '':
                        marketStr = str(area_id) + '<fd>' + str(area_name)
                    else:
                        marketStr += '<rd>' + str(area_id) + '<fd>' + str(area_name)

                #-------------- Product list
                productStr = ''
                productRowsn = "SELECT field1 FROM sm_company_settings WHERE cid='"+cid+"'LIMIT 1 "
                productRows=db.executesql(productRowsn,as_dict=True)

                # productRows = db(db.sm_company_settings.cid == cid).select(db.sm_company_settings.field1, limitby=(0,1))

                for productRow in productRows:
                    productStr = str(productRow['field1'])
                    
                    

                
                
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

                giftRowsn = "SELECT gift_id,gift_name FROM sm_doctor_gift WHERE cid='"+cid+"' AND status='ACTIVE' ORDER BY gift_name "
                giftRows=db.executesql(giftRowsn,as_dict=True)

                # giftRows = db((db.sm_doctor_gift.cid == cid) & (db.sm_doctor_gift.status == 'ACTIVE')).select(db.sm_doctor_gift.gift_id, db.sm_doctor_gift.gift_name, orderby=db.sm_doctor_gift.gift_name)
                for giftRows in giftRows:
                    gift_id = str(giftRows['gift_id'])
                    gift_name = str(giftRows['gift_name'])

                    if giftStr == '':
                        giftStr = str(gift_id) + '<fd>' + str(gift_name)
                    else:
                        giftStr += '<rd>' + str(gift_id) + '<fd>' + str(gift_name)
                        
                        
                        
                
                #------------ppm list

                ppmStr = ''

                ppmRowsn = "SELECT gift_id,gift_name FROM sm_doctor_ppm WHERE cid='"+cid+"' AND status='ACTIVE' ORDER BY gift_name "
                ppmRows=db.executesql(ppmRowsn,as_dict=True)

                # ppmRows = db((db.sm_doctor_ppm.cid == cid) & (db.sm_doctor_ppm.status == 'ACTIVE')).select(db.sm_doctor_ppm.gift_id, db.sm_doctor_ppm.gift_name, orderby=db.sm_doctor_ppm.gift_name)
#                return ppmRows
                for ppmRow in ppmRows:
                    ppm_id = str(ppmRow['gift_id'])
                    ppm_name = str(ppmRow['gift_name'])
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
                    area_id = str(marketRow_1['area_id'])


                    clientStr = clientStr + '<' + area_id + '>'
#                     return clientStr

                    clientRowsn = "SELECT client_id,name,category_id,depot_id,depot_name,market_name,address FROM sm_client WHERE cid='"+cid+"' AND area_id='"+area_id+"' AND status='ACTIVE' ORDER BY name "
                    clientRows=db.executesql(clientRowsn,as_dict=True)

                    # clientRows = db((db.sm_client.cid == cid) & (db.sm_client.area_id == area_id) & (db.sm_client.status == 'ACTIVE')).select(db.sm_client.client_id, db.sm_client.name, db.sm_client.category_id,db.sm_client.depot_id,db.sm_client.depot_name,db.sm_client.market_name,db.sm_client.address, orderby=db.sm_client.name)

        #            return db._lastsql
                    if not clientRows:
                        clientStr = clientStr + 'Retailer not available' + '</' + area_id + '>'
#                         return retStatus
                    else:
                        client_depot=''
                        cliendepot_name=''
                        for clientRow in clientRows:
                            client_id = str(clientRow['client_id'])
                            name = str(clientRow['name'])
                            category_id = str(clientRow['category_id'])
                            address=str(clientRow['address'])
                            if len(address)>30:
                                address= str(clientRow['address'])[30]
                            market_name=address+'-'+str(clientRow['market_name'])
                            client_depot=str(clientRow['depot_id'])
                            cliendepot_name=str(clientRow['depot_name'])
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

                menuRown = "SELECT sl,s_key,s_value FROM sm_mobile_settings_pharma WHERE cid='"+cid+"' AND type='REP' ORDER BY sl "
                menuRow=db.executesql(menuRown,as_dict=True)

                # menuRow = db((db.sm_mobile_settings_pharma.cid == cid) & (db.sm_mobile_settings_pharma.type == 'REP')).select(db.sm_mobile_settings_pharma.sl, db.sm_mobile_settings_pharma.s_key, db.sm_mobile_settings_pharma.s_value, orderby=db.sm_mobile_settings_pharma.sl)
#                 return menuRow
                for menuRow in menuRow:
                    s_key = str(menuRow['s_key'])
                    s_value = str(menuRow['s_value'])

                    if start_flag == 0:
                        menuStr = menuStr + str(s_key) + '<fd>' + str(s_value) 
                        start_flag = 1
                    else:
                        menuStr = menuStr + '<rd>' + str(s_key) + '<fd>' + str(s_value) 

                    
#                 return menuStr


#                 --------------------------------Menu List End--------------------------------------
                
#                ----------------------------Doctor list start-----------------------
#                 ----------Tourplan Market-------------------------------------------              
                marketTourStr=''
                
                marketTourRowsn = "SELECT microunion_id,microunion_name,area_id FROM sm_microunion WHERE cid='"+cid+"' AND  area_id IN("+repareaListn+") GROUP BY microunion_id,microunion_name ORDER BY microunion_name "
                marketTourRows=db.executesql(marketTourRowsn,as_dict=True)
                # marketTourRows = db((db.sm_microunion.cid==cid)  &(db.sm_microunion.area_id.belongs(repareaList))).select(db.sm_microunion.microunion_id,db.sm_microunion.microunion_name,db.sm_microunion.area_id, orderby=db.sm_microunion.microunion_name, groupby=db.sm_microunion.microunion_id|db.sm_microunion.microunion_name)
                # return marketTourRowsn
                
                for marketTourRow in marketTourRows:
                    market_id =  str(marketTourRow['microunion_id'])
                    market_name =  str(marketTourRow['microunion_name'])
                    if market_id!= None:
                        if marketTourStr == '':
                            marketTourStr = str(market_id) + '<fd>' + str(market_name)
                        else:
                            marketTourStr += '<rd>' + str(market_id) + '<fd>' + str(market_name)
                marketTourStr =marketTourStr+'<rd>' +  'LeaveMorning' + '<fd>' + 'LeaveMorning'
                marketTourStr =marketTourStr+'<rd>' +  'LeaveEvening' + '<fd>' + 'LeaveEvening'


               #                ----------------------------Doctor list start-----------------------
                doctorStr = ''

                doctor_area_past=''
                srart_a_flag=0
                doctorStr_flag=0
                for marketRow_1 in marketRows:
                    area_id = str(marketRow_1['area_id'])


                    doctorRowsn = "SELECT doc_id,doc_name,area_id FROM sm_doctor_area  WHERE   cid='"+cid+"'  AND area_id='"+area_id+"' ORDER BY area_id,doc_name "
                    doctorRows=db.executesql(doctorRowsn,as_dict=True)


                    # doctorRows = db((db.sm_doctor.cid == cid) & (db.sm_doctor.status == 'ACTIVE') & (db.sm_doctor_area.cid == cid) & (db.sm_doctor_area.doc_id == db.sm_doctor.doc_id)  & (db.sm_doctor_area.area_id == area_id) ).select(db.sm_doctor.doc_id, db.sm_doctor.doc_name, db.sm_doctor_area.area_id, orderby=db.sm_doctor_area.area_id|db.sm_doctor.doc_name)
                    # return doctorRowsn
                    if not doctorRows:
                        pass
    #                    retStatus = 'FAILED<SYNCDATA>Doctor not available'
    #                    return retStatus
                    else:
                       
                        
                        for doctorRow in doctorRows:
                            doctor_id = str(doctorRow['doc_id'])
                            doctor_name = str(doctorRow['doc_name'])
                            doctor_area = str(doctorRow['area_id'])
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

#               
                
                
#                 ====================================================================
                
                # first_currentDate= datetime.datetime.strptime(str(current_date)[0:7] + '-01', '%Y-%m-%d')

                firstDate = str(first_currentDate).split(' ')[0]
                # return first_currentDate



                docTThisMonthRown = "SELECT route_id,route_name,schedule_date,status FROM sm_doctor_visit_plan WHERE cid='"+cid+"'  AND  rep_id='"+rep_id+"' AND  first_date='"+firstDate+"' AND (status='CReq' OR status='Confirmed')  GROUP BY schedule_date,route_id ORDER BY schedule_date,route_name"
                docTThisMonthRow=db.executesql(docTThisMonthRown,as_dict=True)

                # docTThisMonthRow=db((db.sm_doctor_visit_plan.cid == cid) & (db.sm_doctor_visit_plan.rep_id == rep_id)  & (db.sm_doctor_visit_plan.first_date == first_currentDate) & ((db.sm_doctor_visit_plan.status == 'CReq') | (db.sm_doctor_visit_plan.status == 'Confirmed'))).select(db.sm_doctor_visit_plan.route_id,db.sm_doctor_visit_plan.route_name,db.sm_doctor_visit_plan.schedule_date,db.sm_doctor_visit_plan.status, groupby=db.sm_doctor_visit_plan.schedule_date|db.sm_doctor_visit_plan.route_id, orderby=db.sm_doctor_visit_plan.schedule_date|db.sm_doctor_visit_plan.route_name)


                # return docTThisMonthRown
                marketStrDocThisMonth=''
                # srart_d_flag=0
                # docTThisMonthRowFlag=0
                # pastSchDate=''
                # for docTThisMonthRow in docTThisMonthRow:
                #     route_id = docTThisMonthRow.route_id
                #     route_name = docTThisMonthRow.route_name
                #     schedule_date = docTThisMonthRow.schedule_date
                #     status=docTThisMonthRow.status
                    
                #     if (str(pastSchDate)!=str(schedule_date)):
                #         if (srart_d_flag==0):
                #             marketStrDocThisMonth="<"+str(schedule_date)+">"
                #         else:
                #             marketStrDocThisMonth=marketStrDocThisMonth+"</"+str(pastSchDate)+">"+"<"+str(schedule_date)+">"
                #             srart_d_flag=0
                #     if srart_d_flag == 0:
                #         marketStrDocThisMonth = marketStrDocThisMonth+str(route_id) + '<fd>' + str(route_name)+ '<fd>' + str(status)
                #         srart_d_flag=1
                #     else:
                #         marketStrDocThisMonth = marketStrDocThisMonth+'<rd>' + str(route_id) + '<fd>' + str(route_name)+ '<fd>' + str(status)
                #     pastSchDate=schedule_date
                #     srart_d_flag=1
#                 return marketStrDocThisMonth
                    
#                 ------------------------------------------------------------------

    #             return docTourRow
    
                today = str(today).split(' ')[0]
                tomorrow = str(tomorrow).split(' ')[0]

                docTourRown = "SELECT route_id,route_name,schedule_date FROM sm_doctor_visit_plan WHERE cid='"+cid+"'  AND  rep_id='"+rep_id+"' AND status='Confirmed' AND  schedule_date>='"+today+"' AND  schedule_date<'"+tomorrow+"' GROUP BY schedule_date,route_id,route_name ORDER BY schedule_date,route_id,route_name"
                docTourRow=db.executesql(docTourRown,as_dict=True)
                # docTourRow=db((db.sm_doctor_visit_plan.cid==cid) & (db.sm_doctor_visit_plan.rep_id == rep_id)  & (db.sm_doctor_visit_plan.status == 'Confirmed')  & (db.sm_doctor_visit_plan.schedule_date >= today)  & (db.sm_doctor_visit_plan.schedule_date < tomorrow)).select(db.sm_doctor_visit_plan.route_id,db.sm_doctor_visit_plan.route_name, db.sm_doctor_visit_plan.schedule_date, groupby=db.sm_doctor_visit_plan.schedule_date|db.sm_doctor_visit_plan.route_id|db.sm_doctor_visit_plan.route_name, orderby=db.sm_doctor_visit_plan.schedule_date|db.sm_doctor_visit_plan.route_id|db.sm_doctor_visit_plan.route_name)
#                 return db._lastsql
#                 return docTourRow
                marketStrDoc=''
                for docTourRow in docTourRow:
                    route_id = str(docTourRow['route_id'])
                    route_name = str(docTourRow['route_name'])
                    schedule_date = str(docTourRow['schedule_date'])
#                     market=docTourRow.sm_doctor_area.field1
    
                    if marketStrDoc == '':
                        marketStrDoc = str(route_id) + '<fd>' + str(route_name)+'<fd>' +str(schedule_date)
                    else:
                        marketStrDoc += '<rd>' + str(route_id) + '<fd>' + str(route_name)+ '<fd>' +str(schedule_date)
#                 ===================================================================
                regionStr=''
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
                cTeam='0'
#                 return prSampleStr
#                 return menuStr
                return 'SUCCESS<SYNCDATA>' + str(sync_code) + '<SYNCDATA>' + marketStr + '<SYNCDATA>' + productStr + '<SYNCDATA>' + merchandizingStr + '<SYNCDATA>' + dealerStr + '<SYNCDATA>' + brandStr + '<SYNCDATA>' + complainTypeStr + '<SYNCDATA>' + compFromStr + '<SYNCDATA>' + taskTypeStr + '<SYNCDATA>' + regionStr + '<SYNCDATA>' + giftStr + '<SYNCDATA>' + clienttCatStr + '<SYNCDATA>' + clientStr + '<SYNCDATA>' + menuStr+ '<SYNCDATA>' +ppmStr + '<SYNCDATA>' + user_type+ '<SYNCDATA>' +str(doctorStr)+ '<SYNCDATA>' +str(visit_save_limit)+'<SYNCDATA>'+str(visit_location)+'<SYNCDATA>'+str(delivery_date)+'<SYNCDATA>'+str(payment_date)+'<SYNCDATA>'+str(payment_mode)+'<SYNCDATA>'+str(collection_date)+'<SYNCDATA>'+str(promo_str)+'<SYNCDATA>'+str(client_depot)+'<SYNCDATA>'+str(cliendepot_name)+'<SYNCDATA>'+str(catStr)+'<SYNCDATA>'+str(spcStr)+'<SYNCDATA>'+str(marketStrCteam)+'<SYNCDATA>'+str(cTeam)+'<SYNCDATA>'+str(marketStrDoc)+'<SYNCDATA>'+str(marketTourStr)+'<SYNCDATA>'+str(marketStrDocThisMonth)+'<SYNCDATA>'+str(prProductStr)+'<SYNCDATA>'+str(with_whom)+'<SYNCDATA>'+str(rx_show)+'<SYNCDATA>'+str(linkStr)  +'<SYNCDATA>'+str(cl_catStr) +'<SYNCDATA>'+str(cl_subcatStr)+'<SYNCDATA>'+str(repType)+'<SYNCDATA>'   +str(prSampleStr)+'<SYNCDATA>'+str(module_Str)+'<SYNCDATA>'+str(productcomStr)+'<SYNCDATA>'+str(doc_degree_str)


            elif (user_type == 'sup'):
                linkpathRows = db((db.sm_linkpath.cid == cid) & (db.sm_linkpath.user_type == 'sup')).select(db.sm_linkpath.link_name, db.sm_linkpath.link_path, db.sm_linkpath.field1,orderby=db.sm_linkpath.link_name)
#                 return db._lastsql
                linkStr=''
                for linkpathRows in linkpathRows:
                    link_name = linkpathRows.link_name
                    link_path = linkpathRows.link_path
                    checkType=  linkpathRows.field1
                    
                    if linkStr == '':
                        linkStr = str(link_name) + '<fd>' + str(link_path)+ '<fd>' + str(checkType)
                    else:
                        linkStr += '<rd>' + str(link_name) + '<fd>' + str(link_path)+ '<fd>' + str(checkType)
                        
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
#                 if int(depth) > 1: 
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
                if cTeam==1 and int(depth) > 1: 

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
                if int(depth) > 1:
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
               #                ----------------------------Doctor list start-----------------------
                
                doctorStr = ''
                doctor_area_past=''
                srart_a_flag=0
                doctorStr_flag=0
                
                if cTeam==1   and int(depth) > 1:  
                    for i in range(len(marketListCteam)):
                        area_id = marketListCteam[i]
    #                 return len(marketList)
                        doctorRows = db((db.sm_doctor_area.cid == cid)  & (db.sm_doctor_area.area_id==area_id)).select(db.sm_doctor_area.doc_id, db.sm_doctor_area.doc_name, db.sm_doctor_area.area_id, orderby=db.sm_doctor_area.area_id|db.sm_doctor_area.doc_name)
        #                 return db._lastsql
                        if not doctorRows:
                            pass
        #                    retStatus = 'FAILED<SYNCDATA>Doctor not available'
        #                    return retStatus
                        else:
                             
                              
                            for doctorRow in doctorRows:
                                doctor_id = doctorRow.doc_id
                                doctor_name = doctorRow.doc_name
                                doctor_area = doctorRow.area_id
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
#                     if int(depth) > 1:
                    d_check=0
                    for i in range(len(marketList)):
                        area_id = marketList[i]
                        d_check=d_check+1
                        if int(depth) == 0 and d_check >10:
                            break
#                         return area_id
                        # doctorRows = db((db.sm_doctor.cid == cid) & (db.sm_doctor.status == 'ACTIVE') & (db.sm_doctor_area.cid == cid) & (db.sm_doctor_area.doc_id == db.sm_doctor.doc_id) & (db.sm_doctor_area.area_id==area_id)).select(db.sm_doctor.doc_id, db.sm_doctor.doc_name, db.sm_doctor_area.area_id, orderby=db.sm_doctor_area.area_id|db.sm_doctor.doc_name)
#                         return db._lastsql
                        doctorRows = db((db.sm_doctor_area.cid == cid)  & (db.sm_doctor_area.area_id==area_id)).select(db.sm_doctor_area.doc_id, db.sm_doctor_area.doc_name, db.sm_doctor_area.area_id, orderby=db.sm_doctor_area.area_id|db.sm_doctor_area.doc_name)
                        
                        if not doctorRows:
#                             return 'fgfgh'
                            pass
                        else:
#                             return doctorRow
                            for doctorRow in doctorRows:
                                doctor_id = doctorRow.doc_id
                                doctor_name = doctorRow.doc_name
                                doctor_area = doctorRow.area_id
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
                    
#                 return  doctorStr           
#                return 'SUCCESS<SYNCDATA>' + str(sync_code) + '<SYNCDATA>' + marketStr + '<SYNCDATA>' + productStr + '<SYNCDATA>' + merchandizingStr + '<SYNCDATA>' + dealerStr + '<SYNCDATA>' + brandStr + '<SYNCDATA>' + complainTypeStr + '<SYNCDATA>' + compFromStr + '<SYNCDATA>' + taskTypeStr + '<SYNCDATA>' + regionStr + '<SYNCDATA>' + giftStr + '<SYNCDATA>' + clienttCatStr + '<SYNCDATA>' + menuStr
                
                
                #                 ====================================================================
                
#                 return first_currentDate
                #               ----------Tourplan Market-------------------------------------------              
                marketTourStr=''
#                 marketTourRows = db((db.sm_rep_area.cid == db.sm_depot_market.cid) &(db.sm_doctor_area.cid == db.sm_depot_market.cid)&(db.sm_doctor_area.area_id == db.sm_rep_area.area_id) & (db.sm_rep_area.rep_id == rep_id) & (db.sm_doctor_area.field1 == db.sm_depot_market.market_id)).select(db.sm_depot_market.market_id, db.sm_depot_market.market_name, orderby=db.sm_depot_market.market_name, groupby=db.sm_depot_market.market_id)
#                 marketTourRows = db((db.sm_doctor_area.cid==cid) & (db.sm_doctor_area.field1!='') & (db.sm_doctor_area.note!='') &(db.sm_doctor_area.area_id.belongs(marketList))).select(db.sm_doctor_area.field1,db.sm_doctor_area.note, orderby=db.sm_doctor_area.note, groupby=db.sm_doctor_area.field1|db.sm_doctor_area.note)
                
                marketTourRows = db((db.sm_microunion.cid==cid)  &(db.sm_microunion.area_id.belongs(marketList))).select(db.sm_microunion.microunion_id,db.sm_microunion.microunion_name, orderby=db.sm_microunion.microunion_name, groupby=db.sm_microunion.microunion_id|db.sm_microunion.microunion_name)


#                 return db._lastsql
                for marketTourRow in marketTourRows:
                    market_id =  marketTourRow.microunion_id
                    market_name =  marketTourRow.microunion_name
                    if market_id!= None:
                        if marketTourStr == '':
                            marketTourStr = str(market_id) + '<fd>' + str(market_name)
                        else:
                            marketTourStr += '<rd>' + str(market_id) + '<fd>' + str(market_name)
                marketTourStr =marketTourStr+'<rd>' +  'LeaveMorning' + '<fd>' + 'LeaveMorning'
                marketTourStr =marketTourStr+'<rd>' +  'LeaveEvening' + '<fd>' + 'LeaveEvening'
#                 marketTourStr += '<rd>' + 'HOLIDAY' + '<fd>' + ''
#                 marketTourStr += '<rd>' + 'MEETING' + '<fd>' + ''
#                 marketTourStr += '<rd>' + 'LEAVE' + '<fd>' + ''
#                 marketTourStr += '<rd>' + 'OTHERS' + '<fd>' + ''
#                 return marketTourStr


                docTThisMonthRow=db((db.sm_doctor_visit_plan.cid == cid) & (db.sm_doctor_visit_plan.rep_id == rep_id)  & (db.sm_doctor_visit_plan.first_date == first_currentDate) & ((db.sm_doctor_visit_plan.status == 'CReq') | (db.sm_doctor_visit_plan.status == 'Confirmed'))).select(db.sm_doctor_visit_plan.route_id,db.sm_doctor_visit_plan.route_name,db.sm_doctor_visit_plan.schedule_date,db.sm_doctor_visit_plan.status, groupby=db.sm_doctor_visit_plan.schedule_date|db.sm_doctor_visit_plan.route_id, orderby=db.sm_doctor_visit_plan.schedule_date|db.sm_doctor_visit_plan.route_name)
#                 return docTThisMonthRow
                marketStrDocThisMonth=''
                srart_d_flag=0
                docTThisMonthRowFlag=0
                pastSchDate=''
                for docTThisMonthRow in docTThisMonthRow:
                    route_id = docTThisMonthRow.route_id
                    route_name = docTThisMonthRow.route_name
                    schedule_date = docTThisMonthRow.schedule_date
                    status=docTThisMonthRow.status
                    
                    if (str(pastSchDate)!=str(schedule_date)):
                        if (srart_d_flag==0):
                            marketStrDocThisMonth="<"+str(schedule_date)+">"
                        else:
                            marketStrDocThisMonth=marketStrDocThisMonth+"</"+str(pastSchDate)+">"+"<"+str(schedule_date)+">"
                            srart_d_flag=0
                    if srart_d_flag == 0:
                        marketStrDocThisMonth = marketStrDocThisMonth+str(route_id) + '<fd>' + str(route_name)+ '<fd>' + str(status)
                        srart_d_flag=1
                    else:
                        marketStrDocThisMonth = marketStrDocThisMonth+'<rd>' + str(route_id) + '<fd>' + str(route_name)+ '<fd>' + str(status)
                    pastSchDate=schedule_date
                    srart_d_flag=1
#                 return marketStrDocThisMonth
                    
#                 ------------------------------------------------------------------
                docTourRow=db((db.sm_doctor_visit_plan.cid==cid) & (db.sm_doctor_visit_plan.rep_id == rep_id)  & (db.sm_doctor_visit_plan.status == 'Confirmed')  & (db.sm_doctor_visit_plan.schedule_date >= today)  & (db.sm_doctor_visit_plan.schedule_date < tomorrow)).select(db.sm_doctor_visit_plan.route_id,db.sm_doctor_visit_plan.route_name, db.sm_doctor_visit_plan.schedule_date, groupby=db.sm_doctor_visit_plan.schedule_date|db.sm_doctor_visit_plan.route_id|db.sm_doctor_visit_plan.route_name, orderby=db.sm_doctor_visit_plan.schedule_date|db.sm_doctor_visit_plan.route_id|db.sm_doctor_visit_plan.route_name)
#                 return docTourRow
                marketStrDoc=''
                for docTourRow in docTourRow:
                    route_id = docTourRow.route_id
                    route_name = docTourRow.route_name
                    schedule_date = docTourRow.schedule_date
#                     market=docTourRow.sm_doctor_area.field1
    
                    if marketStrDoc == '':
                        marketStrDoc = str(route_id) + '<fd>' + str(route_name)+'<fd>' +str(schedule_date)
                    else:
                        marketStrDoc += '<rd>' + str(route_id) + '<fd>' + str(route_name)+ '<fd>' +str(schedule_date)
#                 docTourRow=db((db.sm_doctor_visit_plan.cid == db.sm_doctor_area.cid) & (db.sm_doctor_visit_plan.route_id == db.sm_doctor_area.field1)  & (db.sm_doctor_visit_plan.rep_id == rep_id)  & (db.sm_doctor_visit_plan.status == 'Confirmed')  & (db.sm_doctor_visit_plan.schedule_date >= today)  & (db.sm_doctor_visit_plan.schedule_date < tomorrow)).select(db.sm_doctor_area.area_id,db.sm_doctor_area.area_name,db.sm_doctor_area.field1,db.sm_doctor_visit_plan.schedule_date, groupby=db.sm_doctor_area.area_id|db.sm_doctor_area.area_name, orderby=db.sm_doctor_area.area_id|db.sm_doctor_area.area_name)
# #                 return db._lastsql
#                 marketStrDoc=''
#                 for docTourRow in docTourRow:
#                     route_id = docTourRow.sm_doctor_area.area_id
#                     route_name = docTourRow.sm_doctor_area.area_name
#                     schedule_date = docTourRow.sm_doctor_visit_plan.schedule_date
#                     market=docTourRow.sm_doctor_area.field1
#      
#                     if marketStrDoc == '':
#                         marketStrDoc = str(route_id) + '<fd>' + str(route_name)+'[ '+str(market)+ ' ]<fd>' +str(schedule_date)
#                     else:
#                         marketStrDoc += '<rd>' + str(route_id) + '<fd>' + str(route_name)+'[ '+str(market)+ ' ]<fd>' +str(schedule_date)
                
#                 ===================================================================
                
                
                
                
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
#                 marketTourStr=''
#                 marketStrDocThisMonth=''
#                 marketStrDoc=''
                return 'SUCCESS<SYNCDATA>' + str(sync_code) + '<SYNCDATA>' + marketStr + '<SYNCDATA>' + productStr + '<SYNCDATA>' + merchandizingStr + '<SYNCDATA>' + dealerStr + '<SYNCDATA>' + brandStr + '<SYNCDATA>' + complainTypeStr + '<SYNCDATA>' + compFromStr + '<SYNCDATA>' + taskTypeStr + '<SYNCDATA>' + regionStr + '<SYNCDATA>' + giftStr + '<SYNCDATA>' + clienttCatStr + '<SYNCDATA>' + clientStr + '<SYNCDATA>' + menuStr+ '<SYNCDATA>' +ppmStr + '<SYNCDATA>' + user_type+ '<SYNCDATA>' +doctorStr + '<SYNCDATA>' +str(visit_save_limit)+'<SYNCDATA>'+str(visit_location)+'<SYNCDATA>'+str(delivery_date)+'<SYNCDATA>'+str(payment_date)+'<SYNCDATA>'+str(payment_mode)+'<SYNCDATA>'+str(collection_date)+'<SYNCDATA>'+str(promo_str)+'<SYNCDATA>'+str(client_depot)+'<SYNCDATA>'+str(cliendepot_name)+'<SYNCDATA>'+str(catStr)+'<SYNCDATA>'+str(spcStr)+'<SYNCDATA>'+str(marketStrCteam)+'<SYNCDATA>'+str(cTeam)+'<SYNCDATA>'+str(marketStrDoc)+'<SYNCDATA>'+str(marketTourStr)+'<SYNCDATA>'+str(marketStrDocThisMonth)+'<SYNCDATA>'+str(prProductStr)+'<SYNCDATA>'+str(with_whom)+'<SYNCDATA>'+str(rx_show)+'<SYNCDATA>'+str(linkStr) +'<SYNCDATA>'+str(cl_catStr) +'<SYNCDATA>'+str(cl_subcatStr) +'<SYNCDATA>'+str(repType)+'<SYNCDATA>'   +str(prSampleStr)+'<SYNCDATA>'+str(module_Str)+'<SYNCDATA>'+str(productcomStr)+'<SYNCDATA>'+str(doc_degree_str)
                
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
    # return order_info
    merchandizing = str(request.vars.merchandizing).strip()
    campaign = str(request.vars.campaign).strip()
    promo_ref = str(request.vars.bonus_combo)
    OShift = str(request.vars.OShift)
    
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
    
    try:
        orderCheck_date=''
        order_checkRow = db((db.sm_order_head.cid == cid) & (db.sm_order_head.rep_id == rep_id) & (db.sm_order_head.client_id == client_id)).select(db.sm_order_head.order_datetime, orderby=~db.sm_order_head.id, limitby=(0, 1))
        if order_checkRow:
            orderCheck_date = order_checkRow[0].order_datetime
        if orderCheck_date!='':
            datetimeFormat = '%Y-%m-%d %H:%M:%S' 
            timedeltaO = datetime.datetime.strptime(datetime_fixed, datetimeFormat) - datetime.datetime.strptime(str(orderCheck_date),datetimeFormat)
    #         timedelta = datetime.datetime.strptime(datetime_fixed, datetimeFormat) - datetime.datetime.strptime(orderCheck_date,datetimeFormat)
            timeDiffMinuteO=str(timedeltaO).split(':')[1]
            
#             if (int(timeDiffMinuteO) > 10) :
#                 pass
#             else:
#                 return 'FAILED<SYNCDATA>Order Already Submitted. No need to submit again. Please check last order if needed'
    
    except:
        pass 
    
    
    
    
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
    firstDaten = str(firstDate).split(' ')[0]
    depot_name = ''
    client_name = ''
    route_id = ''
    route_name = ''

#    return market_info
#    return merchandizing


    # compRow = db((db.sm_company_settings.cid == cid) & (db.sm_company_settings.status == 'ACTIVE')).select(db.sm_company_settings.cid, limitby=(0, 1))

    compRown = "SELECT cid FROM sm_company_settings WHERE cid='"+cid+"' AND status='ACTIVE' LIMIT 1"
    compRow=db.executesql(compRown,as_dict=True)

    if not compRow:
        return 'FAILED<SYNCDATA>Invalid Company'
    else:
        # repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.sync_code == synccode) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.rep_id, db.sm_rep.name, db.sm_rep.mobile_no, db.sm_rep.user_type, db.sm_rep.level_id, limitby=(0, 1))
       


        repRown = "SELECT rep_id,name,mobile_no,user_type,level_id FROM sm_rep WHERE cid='"+cid+"' AND rep_id='"+rep_id+"' AND password='"+password+"' AND sync_code='"+synccode+"' AND status='ACTIVE'  ORDER BY rep_id LIMIT 1"
        repRow=db.executesql(repRown,as_dict=True)
        if not repRow:
           return 'FAILED<SYNCDATA>Invalid Authorization'
        else:
            for repRow in repRow:
                rep_name = str(repRow['name'])
                mobile_no = str(repRow['mobile_no'])
                user_type = str(repRow['user_type'])


#            return db._lastsql
            # clientRecords = db((db.sm_client.cid == cid) & (db.sm_client.client_id == client_id) & (db.sm_client.status == 'ACTIVE')).select(db.sm_client.name, db.sm_client.category_id, db.sm_client.area_id, db.sm_client.depot_id,db.sm_client.latitude,db.sm_client.longitude,db.sm_client.store_id,db.sm_client.store_name,db.sm_client.market_id,db.sm_client.market_name, limitby=(0, 1))


            clientRecordn = "SELECT name,category_id,area_id,depot_id,latitude,longitude,store_id,store_name,market_id,market_name FROM sm_client WHERE cid='"+cid+"' AND client_id='"+client_id+"' AND status='ACTIVE' LIMIT 1"
            clientRecords=db.executesql(clientRecordn,as_dict=True)
            client_lat=''
            client_long=''
            tracking_table_latlong="0,0"
            if not clientRecords:
                return 'FAILED<SYNCDATA>Invalid Retailer'
            else:
                for cr in clientRecords:
                    
                    client_name = str(cr['name'])
                    client_cat = str(cr['category_id'])
                    route_id = str(cr['area_id'])
                    depot_id = str(cr['depot_id']).strip().upper()
                    client_lat = str(cr['latitude']).strip()
                    client_long = str(cr['longitude']).strip()
                    store_id = str(cr['store_id']).strip()
                    store_name = str(cr['store_name']).strip()
                    market_id = str(cr['market_id']).strip()
                    market_name = str(cr['market_name']).strip()
                    
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
                # levelRecords = db((db.sm_level.cid == cid)& (db.sm_level.is_leaf == '1') & (db.sm_level.level_id == route_id)).select(db.sm_level.level_id, db.sm_level.level_name, db.sm_level.depth, db.sm_level.level0, db.sm_level.level1, db.sm_level.level2, db.sm_level.level3,db.sm_level.level0_name, db.sm_level.level1_name, db.sm_level.level2_name, db.sm_level.level3_name, limitby=(0, 1))

                levelRecordn = "SELECT level_id,level_name,depth,level0,level1,level2,level3,level0_name,level1_name,level2_name,level3_name FROM sm_level WHERE cid='"+cid+"' AND is_leaf=1 AND level_id='"+route_id+"'  LIMIT 1"
                levelRecords=db.executesql(levelRecordn,as_dict=True)

                
                if not levelRecords:
                    return 'FAILED<SYNCDATA>Invalid Route'
                else:
                    for lr in levelRecords:
                        
                        route_name = str(lr['level_name'])
                        regionid = str(lr['level0'])
                        areaid = str(lr['level1'])
                        terriroryid = str(lr['level2'])
                        
                        level0_id = str(lr['level0'])
                        level0_name = str(lr['level0_name'])
                        level1_id  = str(lr['level1'])
                        level1_name = str(lr['level1_name'])
                        level2_id  = str(lr['level2'])
                        level2_name = str(lr['level2_name'])
                        level3_id  = str(lr['level3'])
                        level3_name = str(lr['level3_name'])


                #----
                ordSl = 0

                # depotRow = db((db.sm_depot.cid == cid) & (db.sm_depot.depot_id == depot_id)).select(db.sm_depot.id, db.sm_depot.name, db.sm_depot.order_sl, limitby=(0, 1))


                depotRown = "SELECT id,name,order_sl FROM sm_depot WHERE cid='"+cid+"' AND depot_id='"+depot_id+"'  LIMIT 1"
                depotRow=db.executesql(depotRown,as_dict=True)
                # return depotRown
                for dptr in depotRow:
                    row_id=str(dptr['id'])
                    depot_name = str(dptr['name'])
                    order_sl = int(dptr['order_sl'])
                    # return order_sl
                    ordSl =  order_sl + 1
                    # return ordSl


                depotRowupdtn = "UPDATE sm_depot SET order_sl='"+str(ordSl)+"' WHERE cid='"+cid+"' AND  id='"+row_id+"' "
                depotRowupdt=db.executesql(depotRowupdtn)

                # depotRow[0].update_record(order_sl=ordSl)
                #----

                field1 = ''
                if (order_info != ''):
                    field1 = 'ORDER'

                
                try:
                    # depotSlRow = db((db.sm_order_head.cid == cid) & (db.sm_order_head.depot_id == depot_id)&(db.sm_order_head.sl == ordSl)).select(db.sm_order_head.sl, limitby=(0, 1))


                    depotSlRown="SELECT id FROM sm_order_head WHERE cid='"+cid+"' AND depot_id='"+depot_id+"' AND sl='"+str(ordSl)+"' LIMIT 1 "
                    depotSlRow=db.executesql(depotSlRown,as_dict=True)
                    if depotSlRow:
                        # depotRow = db((db.sm_depot.cid == cid) & (db.sm_depot.depot_id == depot_id)).select(db.sm_depot.id, db.sm_depot.name, db.sm_depot.order_sl, limitby=(0, 1))

                        dptRowslctn="SELECT id,name,order_sl FROM sm_depot  WHERE cid='"+cid+"' AND depot_id='"+str(depot_id)+"' LIMIT 1"
                        dptRowslct=db.executesql(dptRowslctn,as_dict=True)
                        for dptRowslct in dptRowslct:
                            dpt_row_id = str(dptRowslct['id'])
                            depot_name = str(dptRowslct['name'])
                            order_sl = int(dptRowslct['order_sl'])
                            ordSl = order_sl + 1


                        dptRwudtn = "UPDATE sm_depot SET order_sl='"+str(ordSl)+"' WHERE cid='"+cid+"' AND  id='"+dpt_row_id+"' "
                        dptRwudt=db.executesql(dptRwudtn)
                        # depotRow[0].update_record(order_sl=ordSl)
                    insertResn= "INSERT INTO sm_order_head (cid,depot_id,depot_name,sl,store_id,store_name,rep_id,rep_name,market_id,market_name,mobile_no,user_type,client_id,client_name,client_cat,order_date,order_datetime,delivery_date,collection_date,ym_date,area_id,area_name,visit_type,lat_long,order_media,status,visit_image,payment_mode,field1,note,location_detail,last_location,level0_id,level0_name,level1_id,level1_name,level2_id,level2_name,level3_id,level3_name,promo_ref,created_by) VALUES ('"+cid+"','"+depot_id+"','"+depot_name+"','"+str(ordSl)+"','"+store_id+"','"+store_name+"','"+rep_id+"','"+rep_name+"','"+market_id+"','"+market_name+"','"+mobile_no+"','"+user_type+"','"+client_id+"','"+client_name+"','"+client_cat+"','"+visit_date+"','"+str(visit_datetime)+"','"+str(delivery_date)+"','"+str(collection_date)+"','"+firstDaten+"','"+route_id+"','"+route_name+"','"+visit_type+"','"+lat_long+"','APP','Submitted','"+visit_photo+"','"+payment_mode+"','"+field1+"','"+str(note)+"','"+str(location_detail)+"','"+str(last_location)+"','"+level0_id+"','"+level0_name+"','"+level1_id+"','"+level1_name+"','"+level2_id+"','"+level2_name+"','"+level3_id+"','"+level3_name+"','"+promo_ref+"','"+str(OShift)+"')"
                    insertRes=db.executesql(insertResn)
                    
                    # insertRes = db.sm_order_head.insert(cid=cid, depot_id=depot_id, depot_name=depot_name, sl=ordSl,store_id=store_id,store_name=store_name, rep_id=rep_id, rep_name=rep_name,market_id=market_id,market_name=market_name, mobile_no=mobile_no, user_type=user_type, client_id=client_id, client_name=client_name, client_cat=client_cat, order_date=visit_date, order_datetime=visit_datetime,delivery_date=delivery_date,collection_date=collection_date, ym_date=firstDate, area_id=route_id, area_name=route_name, visit_type=visit_type, lat_long=lat_long,order_media='APP', status='Submitted', visit_image=visit_photo, payment_mode=payment_mode, field1=field1,note=str(note),location_detail=str(location_detail),last_location=str(last_location), level0_id = level0_id,  level0_name = level0_name,level1_id = level1_id,level1_name = level1_name,level2_id = level2_id,level2_name = level2_name,level3_id = level3_id,level3_name = level3_name,promo_ref=promo_ref,created_by=OShift )

                    lastvsln="SELECT id,sl FROM sm_order_head  WHERE cid='"+cid+"' AND rep_id='"+str(rep_id)+"' AND sl='"+str(ordSl)+"' AND depot_id='"+str(depot_id)+"' LIMIT 1"
                    lastvsl=db.executesql(lastvsln,as_dict=True)
                    # return lastvsln
                    for lvsl in lastvsl:
                        vsl=str(lvsl['id'])
                    # vsl = db.sm_order_head(insertRes).id
                    # return vsl

                except:
                    try:
                        time.sleep(1)
                        ordSl = 0



                        depotRownn = "SELECT id,name,order_sl FROM sm_depot WHERE cid='"+cid+"' AND depot_id='"+depot_id+"'  LIMIT 1"
                        deptRow=db.executesql(depotRownn,as_dict=True)
                        # return depotRown
                        for dptr in deptRow:
                            row_id=str(dptr['id'])
                            depot_name = str(dptr['name'])
                            order_sl = int(dptr['order_sl'])
                            # return order_sl
                            ordSl =  order_sl + 1


                        dptRowupdtn = "UPDATE sm_depot SET order_sl='"+str(ordSl)+"' WHERE cid='"+cid+"' AND  id='"+row_id+"' "
                        dptRowupdt=db.executesql(dptRowupdtn)
                        # depotRow = db((db.sm_depot.cid == cid) & (db.sm_depot.depot_id == depot_id)).select(db.sm_depot.id, db.sm_depot.name, db.sm_depot.order_sl, limitby=(0, 1))
                        # if depotRow:
                        #     depot_name = depotRow[0].name
                        #     order_sl = int(depotRow[0].order_sl)
                        #     ordSl = order_sl + 1
                        # depotRow[0].update_record(order_sl=ordSl)
                        insertResn= "INSERT INTO sm_order_head (cid,depot_id,depot_name,sl,store_id,store_name,rep_id,rep_name,market_id,market_name,mobile_no,user_type,client_id,client_name,client_cat,order_date,order_datetime,delivery_date,collection_date,ym_date,area_id,area_name,visit_type,lat_long,order_media,status,visit_image,payment_mode,field1,note,location_detail,last_location,level0_id,level0_name,level1_id,level1_name,level2_id,level2_name,level3_id,level3_name,promo_ref,created_by) VALUES ('"+cid+"','"+depot_id+"','"+depot_name+"','"+str(ordSl)+"','"+store_id+"','"+store_name+"','"+rep_id+"','"+rep_name+"','"+market_id+"','"+market_name+"','"+mobile_no+"','"+user_type+"','"+client_id+"','"+client_name+"','"+client_cat+"','"+visit_date+"','"+str(visit_datetime)+"','"+str(delivery_date)+"','"+str(collection_date)+"','"+firstDaten+"','"+route_id+"','"+route_name+"','"+visit_type+"','"+lat_long+"','APP','Submitted','"+visit_photo+"','"+payment_mode+"','"+field1+"','"+str(note)+"','"+str(location_detail)+"','"+str(last_location)+"','"+level0_id+"','"+level0_name+"','"+level1_id+"','"+level1_name+"','"+level2_id+"','"+level2_name+"','"+level3_id+"','"+level3_name+"','"+promo_ref+"','"+str(OShift)+"')"
                        insertRes=db.executesql(insertResn)

                        lastvsln="SELECT id,sl FROM sm_order_head  WHERE cid='"+cid+"' AND rep_id='"+str(rep_id)+"' AND sl='"+str(ordSl)+"' AND depot_id='"+str(depot_id)+"' LIMIT 1"
                        lastvsl=db.executesql(lastvsln,as_dict=True)
                        # return lastvsln
                        for lvsl in lastvsl:
                            vsl=str(lvsl['id'])
                        # insertRes = db.sm_order_head.insert(cid=cid, depot_id=depot_id, depot_name=depot_name, sl=ordSl,store_id=store_id,store_name=store_name, rep_id=rep_id, rep_name=rep_name,market_id=market_id,market_name=market_name, mobile_no=mobile_no, user_type=user_type, client_id=client_id, client_name=client_name, client_cat=client_cat, order_date=visit_date, order_datetime=visit_datetime,delivery_date=delivery_date,collection_date=collection_date, ym_date=firstDate, area_id=route_id, area_name=route_name, visit_type=visit_type, lat_long=lat_long,order_media='APP', status='Submitted', visit_image=visit_photo, payment_mode=payment_mode, field1=field1,note=str(note),location_detail=str(location_detail),last_location=str(last_location), level0_id = level0_id,  level0_name = level0_name,level1_id = level1_id,level1_name = level1_name,level2_id = level2_id,level2_name = level2_name,level3_id = level3_id,level3_name = level3_name,promo_ref=promo_ref,created_by=OShift )
                        # vsl = db.sm_order_head(insertRes).id


                    except:
                        return 'FAILED<SYNCDATA>Please Try again'

                
                #                Client lat_long update
#                return client_lat

                if ((client_lat=='') | (client_lat=='0')| (client_long=='')| (client_long=='0')):

                    depotRowclnt = "UPDATE sm_client SET latitude='"+str(latitude)+"',longitude='"+str(longitude)+"' WHERE cid='"+cid+"' AND  client_id='"+client_id+"'"
                    depotRowclnt=db.executesql(depotRowclnt)
                    # db((db.sm_client.cid == cid) & (db.sm_client.client_id == client_id)).update(latitude=latitude,longitude=longitude)

#                Insert in tracking table====================
                insertTrackingn="INSERT INTO sm_tracking_table (cid,depot_id,depot_name,sl,rep_id,rep_name,call_type,visited_id,visited_name,visit_date,visit_time,area_id,area_name,visit_type,visited_latlong,actual_latlong,location_detail) VALUES ('"+cid+"','"+depot_id+"','"+depot_name+"','"+str(ordSl)+"','"+rep_id+"','"+rep_name+"','SELL','"+client_id+"','"+client_name+"','"+str(visit_date)+"','"+str(visit_datetime)+"','"+route_id+"','"+route_name+"','"+visit_type+"','"+lat_long+"','"+tracking_table_latlong+"','"+str(location_detail)+"')"
                # return 'fdg'
                insertTracking=db.executesql(insertTrackingn)


                # insertTracking = db.sm_tracking_table.insert(cid=cid, depot_id=depot_id, depot_name=depot_name, sl=ordSl, rep_id=rep_id, rep_name=rep_name,call_type='SELL',  visited_id=client_id, visited_name=client_name, visit_date=visit_date, visit_time=visit_datetime,  area_id=route_id, area_name=route_name, visit_type=visit_type, visited_latlong=lat_long,actual_latlong=tracking_table_latlong,location_detail=str(location_detail))  
                
                #--------- Order Info
                orderArrayList = []
                order_infoList = order_info.split('<rd>')
                for i in range(len(order_infoList)):
                    orderDataList = order_infoList[i].split('<fd>')
                    if len(orderDataList) == 2:
                        itemId = orderDataList[0]
                        itemQty = orderDataList[1]                       
                        ins_dict = {'cid':cid, 'vsl':vsl, 'depot_id':depot_id, 'depot_name':depot_name, 'sl':ordSl, 'store_id':store_id,'store_name':store_name,'client_id':client_id, 'client_name':client_name, 'rep_id':rep_id, 'rep_name':rep_name,'market_id':market_id,'market_name':market_name, 'order_date':visit_date, 'order_datetime':visit_datetime, 'ym_date':firstDate,'delivery_date':delivery_date,'payment_mode':payment_mode,'collection_date':collection_date,'area_id':route_id, 'area_name':route_name, 'item_id':itemId,'quantity':itemQty,'order_media':'APP', 'status':'Submitted', 'level0_id' : level0_id,  'level0_name' : level0_name,'level1_id' : level1_id,'level1_name' : level1_name,'level2_id' : level2_id,'level2_name' : level2_name,'level3_id' : level3_id,'level3_name' : level3_name}

                        orderArrayList.append(ins_dict)
                if len(orderArrayList) > 0:
                    db.sm_order.bulk_insert(orderArrayList)

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
    location_detail = str(request.vars.location_detail).strip()
    imageName = str(request.vars.imageName).strip()
    
    
    productl_combo=str(request.vars.productl_combo).strip()
    product2_combo=str(request.vars.product2_combo).strip()
    product3_combo=str(request.vars.product3_combo).strip()
    
    
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
    v_shift = request.vars.v_shift
     
    visit_photo = request.vars.visit_photo
 
    if latitude == '' or latitude == None:
        latitude = '0'
    if longitude == '' or longitude == None:
        longitude = '0'
 
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
 
 
 
#             return errorFlag
 
 
            doctorRows = db((db.sm_doctor.cid == cid) & (db.sm_doctor.doc_id == doctorID) & (db.sm_doctor.status == 'ACTIVE')).select(db.sm_doctor.doc_name, limitby=(0, 1))
            if not doctorRows:
                errorFlag = 1
                errorMsg = 'Invalid doctor'
            else:
                docName = doctorRows[0].doc_name
#             return errorFlag
            settRows = db((db.sm_settings.cid == cid) & (db.sm_settings.s_key == 'DOCTOR_ROUTE_CHECK') & (db.sm_settings.s_value == 'YES')).select(db.sm_settings.s_value, limitby=(0, 1))
            tracking_table_latlong=""
             
            if settRows:
                if visit_type=="Schedule":
                    docLRows = db((db.sm_doctor_area.cid == cid) & (db.sm_doctor_area.doc_id == doctorID) & (db.sm_doctor_area.area_id == routeID)).select(db.sm_doctor_area.area_id, db.sm_doctor_area.area_name, db.sm_doctor_area.depot_id, db.sm_doctor_area.area_id, limitby=(0, 1))
                else:
                    docLRows = db((db.sm_doctor_area.cid == cid) & (db.sm_doctor_area.doc_id == doctorID) & (db.sm_doctor_area.area_id == routeID)).select(db.sm_doctor_area.area_id, db.sm_doctor_area.area_name, db.sm_doctor_area.depot_id, db.sm_doctor_area.area_id, limitby=(0, 1))
#                 docRouteRows = db((db.sm_client.cid == cid) & (db.sm_client.area_id == routeID)).select(db.sm_client.depot_id, limitby=(0, 1))
#                 return db._lastsql
                
#                 return docLRows
                if not (docLRows):
                    errorFlag = 1
                    errorMsg = 'Invalid route for the doctor'
                else:
                    routeID = docLRows[0].area_id
                     
                    areaID = docLRows[0].area_id
                    areaName = docLRows[0].area_name
                    tracking_table_latlong = ''#docLRows[0].field1
                     
                    docARows = db((db.sm_level.cid == cid) & (db.sm_level.level_id == areaID)).select(db.sm_level.ALL, limitby=(0, 1))
                    if docARows:
                        level0_id = docARows[0].level0
                        level0_name = docARows[0].level0_name
                        level1_id = docARows[0].level1
                        level1_name = docARows[0].level1_name
                        level2_id = docARows[0].level2
                        level2_name = docARows[0].level2_name
                        level3_id = docARows[0].level3
                        level3_name = docARows[0].level3_name
                    else:
                        level0_id = ""
                        level0_name = ""
                        level1_id = ""
                        level1_name = ""
                        level2_id = ""
                        level2_name = ""
                        level3_id = ""
                        level3_name = ""
                    docRouteRows = db((db.sm_client.cid == cid) & (db.sm_client.area_id == areaID)).select(db.sm_client.depot_id, limitby=(0, 1))
                    if docRouteRows:
                        depotID = docRouteRows[0].depot_id
                    else:
                        depotID=''
#             return errorFlag 
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
 
 
 
 
 
 
#     return errorFlag  
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
     
#     return errorFlag
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
 
     
    # return giftPart
     
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
 
     
#    -------------Sample part end
     
    #----- sample part
     
    
    # samplePart=str(samplePart).replace(',.', ' ').replace('.,', ' ').replace('UNDEFINED', ' ')
     
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
 
 
 
 
 
                    # return giftStr
 
                   #=================Get sl for inbox

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
        # return itemngiftnsample
 
        import time
        today= time.strftime("%Y-%m-%d")  
#         insRes = db.sm_doctor_visit.insert(cid=cid, doc_id=doctorID, doc_name=docName, rep_id=rep_id, rep_name=rep_name, feedback=notesPart, ho_status='0', route_id=routeID,route_name=areaName, depot_id=depotID, visit_dtime=datetime_fixed, visit_date=current_date, giftnsample=itemngiftnsample, note=v_with,field1=doc_others,level0_id = level0_id,level0_name = level0_name,level1_id = level1_id,level1_name = level1_name,level2_id = level2_id,level2_name = level2_name,level3_id = level3_id,level3_name =level3_name,location_detail=location_detail)
        insRes = db.sm_doctor_visit.insert(cid=cid, doc_id=doctorID, doc_name=docName, rep_id=rep_id, rep_name=rep_name, feedback=notesPart, ho_status='0', route_id=routeID,route_name=areaName, depot_id=depotID, visit_dtime=datetime_fixed, visit_date=current_date, giftnsample=itemngiftnsample,latitude = latitude, longitude = longitude, note=v_with,field1=doc_others,level0_id = level0_id,level0_name = level0_name,level1_id = level1_id,level1_name = level1_name,level2_id = level2_id,level2_name = level2_name,level3_id = level3_id,level3_name =level3_name,location_detail=location_detail,imageName=imageName ,updated_by=v_shift)
        
        rows_check1 = db((db.sm_doctor_visit.cid == cid) & (db.sm_doctor_visit.rep_id == rep_id)).select(db.sm_doctor_visit.id, orderby= ~db.sm_doctor_visit.id, limitby=(0, 1))
        
        if rows_check1:
            last_id = int(rows_check1[0].id)

            insnewRes = db.sm_dcr_reminder_product.insert(cid=cid,visit_sl=last_id,product_1=productl_combo,product_2=product2_combo,product_3=product3_combo)   
 
        
#         return db._lastsql
        planUpdate=db((db.sm_doctor_visit_plan.cid == cid) & (db.sm_doctor_visit_plan.rep_id == rep_id) & (db.sm_doctor_visit_plan.route_id == routeID) & (db.sm_doctor_visit_plan.schedule_date == today)).update(visited_flag=1)
#         return db._lastsql
         
         
        lat_long=str(latitude)+','+str(longitude)
        if (tracking_table_latlong=="0,0"):
            insRes =db((db.sm_doctor_area.cid == cid) & (db.sm_doctor_area.doc_id == doctorID) & (db.sm_doctor_area.area_id == areaID)).update(latitude=str(latitude),longitude=str(longitude))
         
#        return depotName
        insertTracking = db.sm_tracking_table.insert(cid=cid, depot_id=depotID, depot_name=depotName, sl="0", rep_id=rep_id, rep_name=rep_name,call_type='DCR',  visited_id=doctorID, visited_name=docName, visit_date=current_date, visit_time=datetime_fixed,  area_id=routeID, area_name=routeName, visit_type=visit_type, visited_latlong=lat_long, actual_latlong=tracking_table_latlong, location_detail=str(location_detail),last_location=str(last_location)) 
         
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
            bonusString='<font style="font-size:18px; color:#fff" >Bonus:<br></font><table width="100%" border="1" cellpadding="0" cellspacing="0" style="border:solid; border-style:solid; border-color:#0CF; color:#fff"><tr style="font-size:16px; font-weight:bold"><td width="80%">Offer<td width="10%" align="center">MinQty</td></tr>'
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
            specialRate='<font style="font-size:18px;color:#fff" >Special Rate:<br></font><table width="100%" border="1" cellpadding="0" cellspacing="0" style="border:solid; border-style:solid; border-color:#0CF; color:#fff"><tr style="font-size:16px; font-weight:bold"><td width="80%">Product</td><td align="center">MinQty</td><td align="right">Rate</td></tr>'     
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
            
            flarRate='<font style="font-size:18px;color:#fff" >Flat Rate:<br></font><table width="100%" border="1" cellpadding="0" cellspacing="0" style="border:solid; border-style:solid; border-color:#0CF; color:#fff"><tr style="font-size:16px; font-weight:bold"><td width="80%">Product</td><td align="center">MinQty</td><td align="right">FlatRate</td></tr>'
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
            
            declearedRate='<font style="font-size:18px;color:#fff" >Declared Item:<br></font><table width="100%" border="1" cellpadding="0" cellspacing="0" style="border:solid; border-style:solid; border-color:#0CF; color:#fff"><tr style="font-size:16px; font-weight:bold"><td width="80%">Product</td><td >ApprovedDate</td></tr>'
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
            recRow = db((db.sm_msg_box.cid == cid) & (db.sm_msg_box.msg_to == rep_id) & (db.sm_msg_box.status == 'Active')).select(db.sm_msg_box.ALL ,orderby=~db.sm_msg_box.id,limitby=(0,20))
#             return db._lastsql
            inbox_str='<table style="border-style:solid; border-width:thin; border-color:#096;background-color:#EDFEED" width="100%" border="1" cellspacing="0">'
            for recRow in recRow:
                msg=recRow.msg
                msgTime_1=recRow.created_on
#                 msgTime=msgTime_1.strftime('%d, %b %H:%M'  )
                msgTime=msgTime_1.strftime('%d, %b %I:%M:%S %p'  )
                msgFrom=recRow.msg_from
                msgFromName=recRow.msgFromName
                if msgFromName=='':
                    msgFromInfo=msgFrom
                else:
                    msgFromInfo=str(msgFromName)+' ['+str(msgFrom)+']'
#                 inbox_str=inbox_str+'<tr height="30px"><td >'+str(msgTime)+'</br>'+str(msgFromName)+' | '+str(msgFrom)+'</br>'+str(msg)+'</td></tr>'
                inbox_str=inbox_str+'<tr height="30px"><td ><font style="font-size:14px;color:#339">'+str(msgTime)+'</font></br><font style="font-size:12px;color:#633">From: '+str(msgFromInfo)+'</font></br><font style="font-size:16px;color:#366;font-style:italic">'+str(msg)+'</font></td></tr>'
            inbox_str=inbox_str+'</table>'
    #         return repStr
            
       
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



                stockBalance_str='<font style="color:#fff">'+'Depot ID :'+str(depot_id) +'</br>'
                stockBalance_str=stockBalance_str+'Depot Name :'+str(depot_name) +'</br></br></font>'
                

              


                
                stockBalance_str=stockBalance_str+'<table width="600" border="1" cellpadding="0" cellspacing="0" style="border:solid; border-style:solid; border-color:#0CF; color:#fff"> <tr style="font-size:16px; font-weight:bold">'

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
                
                outstanding_str='<table width="500" border="0" cellspacing="0" cellpadding="0" style="color:#fff">'
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
                
                 
    
    
                  
    
    
                    
                outstanding_str=outstanding_str+'<table width="600" border="1" cellpadding="0" cellspacing="0" style="border:solid; border-style:solid; border-color:#0CF; color:#fff"> <tr class="table_title">'
    
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

            # Nazma Azam 2020-05-03 start
            qset = qset(db.sm_invoice_head.rep_id == rep_id)
            # Nazma Azam 2020-05-03 end

            qset=qset(db.sm_invoice_head.client_id==client)
             
                     
               # Nazma Azam 2020-05-03 start
            records=qset.select(db.sm_invoice_head.ALL,orderby=~db.sm_invoice_head.sl, limitby=(0,5))
            # return records
            # return db._lastsql
            # Nazma Azam 2020-05-03 end

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

                # Nazma Azam 2020-03-05 start

                start_flag=0
                invoice_str =''

                
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

                    # Nazma Azam 2020-03-05 start

                    # if start_flag == 0:
                    #     invoice_str = invoice_str+str(depot_name) + '<fd>'+str(depot_id) +'<fd>'+str(store_name) + '<fd>'+str(store_id) +'<fd>'+str(client_name) + '<fd>'+str(client) +'<fd>'+str(sl) +'<fd>'+str(order_sl) +'<fd>'+str(rep_name) + '<fd>'+str(rep_id) +'<fd>'+str(d_man_name) + '<fd>'+str(d_man_id) +'<fd>'+str(delivery_dt)+'<fd>'+str(payment_mode)+'<fd>'+str(discount) +'<fd>'+str(status) +'<fd>'+str(note)
                    #     start_flag = 1
                    # else:
                    #     invoice_str = invoice_str+'<rd>' + str(depot_name) + '<fd>'+str(depot_id) +'<fd>'+str(store_name) + '<fd>'+str(store_id) +'<fd>'+str(client_name) + '<fd>'+str(client) +'<fd>'+str(sl) +'<fd>'+str(order_sl) +'<fd>'+str(rep_name) + '<fd>'+str(rep_id) +'<fd>'+str(d_man_name) + '<fd>'+str(d_man_id) +'<fd>'+str(delivery_dt)+'<fd>'+str(payment_mode)+'<fd>'+str(discount) +'<fd>'+str(status) +'<fd>'+str(note)


                    invoice_str=invoice_str+'<table width="500" border="0" cellspacing="0" cellpadding="0" style="color:#fff">'
                    invoice_str=invoice_str+'<tr ><td width="100" style="padding-left:0px;"><b>Branch</b></td><td width="5"><b>:</b></td><td width="300" align="left">'+str(depot_name) + '('+str(depot_id) +')'+'</td></tr>'
                    invoice_str=invoice_str+'<tr ><td width="100" style="padding-left:0px;"><b>Store</b></td><td width="5"><b>:</b></td><td width="300" align="left">'+str(store_name) + '('+str(store_id) +')'+'</td></tr>'
                    invoice_str=invoice_str+'<tr ><td width="100" style="padding-left:0px;"><b>Customer</b></td><td width="5"><b>:</b></td><td width="300" align="left">'+str(client_name) + '('+str(client) +')'+'</td></tr>'
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



                # Nazma Azam 2020-03-05 end

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
                        invoice_str=invoice_str+"""<table width="700" border="1" cellpadding="0" cellspacing="0" style="border:solid; border-style:solid; border-color:#0CF; color:#fff"> 
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
                            # return
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
                        # return 'SUCCESS<SYNCDATA>'+invoice_str
                    # else:
                    #     return 'SUCCESS<SYNCDATA>'+invoice_str
                return 'SUCCESS<SYNCDATA>' + invoice_str
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
                        
                         
                        
                        
    
                        invoice_str='<table width="500" border="0" cellspacing="0" cellpadding="0" style="color:#fff">'
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
                    invoice_str=invoice_str+"""<table width="500" border="1" cellpadding="0" cellspacing="0" style="border:solid; border-style:solid; border-color:#0CF; color:#fff"> 
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
                        
                         
                        
                        
    
                        invoice_str='<table width="500" border="0" cellspacing="0" cellpadding="0" style="color:#fff">'
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
                    invoice_str=invoice_str+"""<table width="500" border="1" cellpadding="0" cellspacing="0" style="border:solid; border-style:solid; border-color:#0CF; color:#fff"> 
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
            now = datetime.datetime.strptime(current_date, "%Y-%m-%d")
            date_to=now + datetime.timedelta(days = 1)
            noticeRow = db((db.sm_notice.cid == cid) & (db.sm_notice.notice_date <= date_to)).select(db.sm_notice.ALL,orderby=~db.sm_notice.id,limitby=(0, 30))
            if noticeRow:
                notice_str="""<table style="border-style:solid; border-width:thin; border-color:#096;background-color:#EDFEED" width="100%" border="1" cellspacing="0"> 
                        """
                
                for noticeRow in noticeRow:  
                    notice_date_str  = noticeRow.notice_date 

                    notice_date=notice_date_str.strftime('%d, %b %I:%M:%S %p'  )
                    notice   = noticeRow.notice 
                                                             
                    notice_str=notice_str+'<tr height="30px"><td style="padding:5px"><font style="font-size:12px;color:#633">'+str(notice_date)+'</font></br><font style="font-size:15px;color:#366;font-style:italic">'+str(notice)+'</font></td>'
                   

                                                
                return 'SUCCESS<SYNCDATA>'+notice_str+'<br><br><br>'
            
            else:
                return 'SUCCESS<SYNCDATA>'+'No Notice'   
                 
                 
                
     
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
                
                approvrd_str='<table width="500" border="0" cellspacing="0" cellpadding="0" style="color:#fff">'
                approvrd_str=approvrd_str+'<tr ><td width="100" style="padding-left:0px;"><b>Customer ID</b></td><td width="5"><b>:</b></td><td width="300" align="left">'+str(client) +'</td></tr>'
                approvrd_str=approvrd_str+'<tr ><td width="100" style="padding-left:0px;"><b>Customer Name</b></td><td width="5"><b>:</b></td><td width="300" align="left">'+str(client_name) +'</td></tr>'

                approvrd_str=approvrd_str+'</table><br>'
                
                 
    
#                 return approvrd_str
                  
    
    
                    
                approvrd_str=approvrd_str+'<table width="600" border="1" cellpadding="0" cellspacing="0" style="border:1px solid #94E2F6; color:#fff"> <tr class="table_title">'
    
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
            
            doc_degree_str='DVM,RVP,RMP,AH,AV,DVM Veterinary Surgeon,ULO,Consultant,VFA,UIO,VFI,AI,Compunder,VS Consultant,'
            
            docRow = db((db.sm_doctor.cid == cid) & (db.sm_doctor.doc_id == doc) & (db.sm_doctor_area.cid == cid) & (db.sm_doctor_area.area_id == route) & (db.sm_doctor_area.doc_id == doc)).select(db.sm_doctor.ALL,db.sm_doctor_area.address,db.sm_doctor_area.district,db.sm_doctor_area.thana,db.sm_doctor_area.field1,db.sm_doctor_area.note, limitby=(0, 1))
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
            OtherChamber=''
            dPharmaRoute=''
            dNMDRoute=''
            rtn_str=''
            if docRow:  
                dName=docRow[0][db.sm_doctor.doc_name]
                dSpaciality=docRow[0][db.sm_doctor.specialty]+','+spcStr
                dDegree=docRow[0][db.sm_doctor.degree]+','+doc_degree_str
                dCaegory=docRow[0][db.sm_doctor.doctors_category]+','+catStr
                dDOB=docRow[0][db.sm_doctor.dob]
                dMDay=docRow[0][db.sm_doctor.mar_day]
                dMobile=docRow[0][db.sm_doctor.mobile]
                dCAddress=docRow[0][db.sm_doctor.des]
                dDist=docRow[0][db.sm_doctor_area.note]
                dThana=docRow[0][db.sm_doctor_area.field1]
                OtherChamber=docRow[0][db.sm_doctor.chamber_1]
                dPharmaRoute=docRow[0][db.sm_doctor.pharma_route]
                dNMDRoute=docRow[0][db.sm_doctor.nmd_route]
                
                third_party_id=docRow[0][db.sm_doctor.third_party_id]
                service_id=docRow[0][db.sm_doctor.service_id]
                service_kol_dsc=docRow[0][db.sm_doctor.service_kol_dsc]
                at_ins=docRow[0][db.sm_doctor.attached_institution]
                dMicrounion=docRow[0][db.sm_doctor.field1]

                rtn_str=str(dName)+'<fdfd>'+str(dSpaciality)+'<fdfd>'+str(dDegree)+'<fdfd>'+str(dCaegory)+'<fdfd>'+str(dDOB)+'<fdfd>'+str(dMDay)+'<fdfd>'+str(dMobile)+'<fdfd>'+str(dCAddress)+'<fdfd>'+str(dDist)+'<fdfd>'+str(dThana)+'<fdfd>'+str(OtherChamber)+'<fdfd>'+str(dPharmaRoute)+'<fdfd>'+str(dNMDRoute)+'<fdfd>'+str(third_party_id)+'<fdfd>'+str(service_id)+'<fdfd>'+str(service_kol_dsc)+'<fdfd>'+str(at_ins)+'<fdfd>'+str(dMicrounion)
             
    return 'SUCCESS<SYNCDATA>'+rtn_str  

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
    dDist=str(request.vars.dDist).strip()
    dAttachedInstitute=str(request.vars.dAttachedInstitute).strip()
    dS_K_D=str(request.vars.dS_K_D).strip()
    dService=str(request.vars.dService).strip()
    dParty=str(request.vars.dParty).strip()
    
    dDOB=str(request.vars.dDOB).strip()
    dMDay=str(request.vars.dMDay).strip()
    dMobile=str(request.vars.dMobile).strip()
    dCAddress=str(request.vars.dCAddress).strip()
    dOtherChamber=str(request.vars.dOtherChamber).strip()
    dPharmaRoute=str(request.vars.dPharmaRoute).strip()
    dNMDRoute=str(request.vars.dNMDRoute).strip()
    
    route = urllib.unquote(route.decode('utf8'))
    doc= urllib.unquote(doc.decode('utf8'))
    dName= urllib.unquote(dName.decode('utf8'))
    dSpaciality=  urllib.unquote(dSpaciality.decode('utf8'))
    dDegree= urllib.unquote(dDegree.decode('utf8'))
    dCategory= urllib.unquote(dCategory.decode('utf8'))
    dDist=str(request.vars.dDist).strip()
    dAttachedInstitute=urllib.unquote(dAttachedInstitute.decode('utf8'))
    dS_K_D=urllib.unquote(dS_K_D.decode('utf8'))
    dService=urllib.unquote(dService.decode('utf8'))
    dParty=urllib.unquote(dParty.decode('utf8'))
    
    dDOB=urllib.unquote(dDOB.decode('utf8'))
    dMDay=urllib.unquote(dMDay.decode('utf8'))
    dMobile=urllib.unquote(dMobile.decode('utf8'))
    dCAddress=urllib.unquote(dCAddress.decode('utf8'))
    dOtherChamber=urllib.unquote(dOtherChamber.decode('utf8'))
    dPharmaRoute=urllib.unquote(dPharmaRoute.decode('utf8'))
    dNMDRoute=urllib.unquote(dNMDRoute.decode('utf8'))
    
#     mName=dDist.split('|')[0]
#     mID=dDist.split('|')[1]
    mName=''
    mID=''
    
    
    compRow = db((db.sm_company_settings.cid == cid) & (db.sm_company_settings.status == 'ACTIVE')).select(db.sm_company_settings.cid, limitby=(0, 1))
    if not compRow:
        return 'FAILED<SYNCDATA>Invalid Company'
    else:
        repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.sync_code == synccode) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.rep_id, db.sm_rep.name, db.sm_rep.mobile_no, db.sm_rep.user_type, db.sm_rep.level_id, db.sm_rep.depot_id, limitby=(0, 1))

        
        if not repRow:
           return 'FAILED<SYNCDATA>Invalid Authorization'

        else:
            docRow = db((db.sm_doctor_temp.cid == cid) & (db.sm_doctor_temp.doc_id == doc) & (db.sm_doctor_temp.pharma_route_id == dPharmaRoute)).select(db.sm_doctor_temp.id, limitby=(0, 1))
            if docRow:  
                 db((db.sm_doctor_temp.cid == cid) & (db.sm_doctor_temp.doc_id == doc) & (db.sm_doctor_temp.pharma_route_id == dPharmaRoute) ).update(doc_name=dName,specialty=dSpaciality,degree=dDegree,mobile=dMobile,des=dDist,status='ACTIVE',attached_institution=dAttachedInstitute,dob=dDOB,mar_day=dMDay,doctors_category=dCategory,service_kol_dsc=dS_K_D,service_id=dService,third_party_id=dParty,note=dCAddress,otherChamber=dOtherChamber,pharma_route_id=dPharmaRoute, nmd_route_id=dNMDRoute,new_doc=0)
            else:
                db.sm_doctor_temp.insert(cid =cid,doc_id = doc,doc_name=dName,specialty=dSpaciality,degree=dDegree,mobile=dMobile,des=dDist,status='ACTIVE',attached_institution=dAttachedInstitute,dob=dDOB,mar_day=dMDay,doctors_category=dCategory,service_kol_dsc=dS_K_D,service_id=dService,third_party_id=dParty,note=dCAddress,otherChamber=dOtherChamber,pharma_route_id=dPharmaRoute, nmd_route_id=dNMDRoute,new_doc=0)

    
    
    
    
                
                
#                  db((db.sm_doctor_area.cid == cid) & (db.sm_doctor_area.doc_id == doc) & (db.sm_doctor_area.area_id == route) ).update(address=dCAddress,field1=mID,note=mName)
    return 'SUCCESS<SYNCDATA>'+'Updated Successfully  '


# ============Chemist_info==============
def chemist_info():
    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.rep_pass).strip()
    synccode = str(request.vars.synccode).strip()
    route = str(request.vars.route).strip()
    chemist = str(request.vars.docId).strip()
#     return chemist
    compRow = db((db.sm_company_settings.cid == cid) & (db.sm_company_settings.status == 'ACTIVE')).select(db.sm_company_settings.cid, limitby=(0, 1))
    if not compRow:
        return 'FAILED<SYNCDATA>Invalid Company'
    else:
        repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.sync_code == synccode) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.rep_id, db.sm_rep.name, db.sm_rep.mobile_no, db.sm_rep.user_type, db.sm_rep.level_id, db.sm_rep.depot_id, limitby=(0, 1))

        if not repRow:
           return 'FAILED<SYNCDATA>Invalid Authorization'

        else:
            cat_row=db((db.sm_category_type.cid == cid) & (db.sm_category_type.type_name=='CLIENT_CATEGORY')).select(db.sm_category_type.cat_type_id,db.sm_category_type.cat_type_name, orderby=db.sm_category_type.cat_type_name)
            catStr=''
            for cat_row in cat_row:
                catStr=catStr+str(cat_row.cat_type_name)+'|'+str(cat_row.cat_type_id)+','
            
            subcat_row=db((db.sm_category_type.cid == cid) & (db.sm_category_type.type_name=='CLIENT_SUB_CATEGORY')).select(db.sm_category_type.cat_type_id,db.sm_category_type.cat_type_name, orderby=db.sm_category_type.cat_type_name)
            subcatStr=''
            for subcat_row in subcat_row:
                subcatStr=subcatStr+str(subcat_row.cat_type_name)+'|'+str(subcat_row.cat_type_id)+','
                
#             dist_row=db((db.district.cid == cid) ).select(db.district.district_id,db.district.name, orderby=db.district.name)
#             distStr=''
#             for dist_row in dist_row:
#                 distStr=distStr+str(dist_row.name)+'|'+str(dist_row.district_id)+','
#                 
#             thana_row=db((db.district.cid == cid) ).select(db.district.district_id,db.district.name, orderby=db.district.name)
#             distStr=''
#             for dist_row in dist_row:
#                 distStr=distStr+str(dist_row.name)+'|'+str(dist_row.district_id)+','


            docRow = db((db.sm_client.cid == cid) & (db.sm_client.client_id == chemist) ).select(db.sm_client.ALL,limitby=(0, 1))

            ChemistName =''
            Address_Line_1 =''
            district=''
            thana=''
            RegistrationNo =''
            NID =''
            Contact_Name =''
            Contact_phone =''
            Category =''
            SubCategory =''
            DOB =''
            Cash_Credit =''#* default= NeedToSet
            Credit_Limit ='0'
            Status=''
            if docRow:  
                ChemistID =docRow[0].client_id
                ChemistName =docRow[0].name
                Address_Line_1 =docRow[0].address
                RegistrationNo =docRow[0].vat_registration_no
                district=docRow[0].district
                thana=docRow[0].thana
                NID =docRow[0].nid
                Contact_Name =docRow[0].owner_name
                Contact_phone =docRow[0].contact_no1
                Category =docRow[0].category_id          
                SubCategory =docRow[0].sub_category_id
                DOB =docRow[0].dob
                Cash_Credit =docRow[0].field1
                Credit_Limit =docRow[0].credit_limit
                Status=docRow[0].status
                
# 
                rtn_str=str(ChemistName)+'<fdfd>'+str(Address_Line_1)+'<fdfd>'+str(district)+'<fdfd>'+str(thana)+'<fdfd>'+str(RegistrationNo)+'<fdfd>'+str(NID)+'<fdfd>'+str(Contact_Name)+'<fdfd>'+str(Contact_phone)+'<fdfd>'+str(Category)+'<fdfd>'+str(SubCategory)+'<fdfd>'+str(DOB)+'<fdfd>'+str(Cash_Credit)+'<fdfd>'+str(Credit_Limit)+'<fdfd>'+str(Status)+'<fdfd>'+str(catStr)+'<fdfd>'+str(subcatStr)+'<fdfd>'+str(ChemistID)
             
    return 'SUCCESS<SYNCDATA>'+rtn_str  

def chemist_info_submit():
    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.rep_pass).strip()
    synccode = str(request.vars.synccode).strip()
    route = str(request.vars.route).strip()
    client_id = str(request.vars.client_id).strip()
    ChemistName=str(request.vars.ChemistName).strip()
    Address_Line_1=str(request.vars.Address_Line_1).strip()
    district=str(request.vars.district).strip()
    thana=str(request.vars.thana).strip()
    RegistrationNo=str(request.vars.RegistrationNo).strip()
    NID=str(request.vars.NID).strip()
    Contact_Name=str(request.vars.Contact_Name).strip()
    Contact_phone=str(request.vars.Contact_phone).strip()
    Category=str(request.vars.Category).strip()
    SubCategory=str(request.vars.SubCategory).strip()
    DOB=str(request.vars.DOB).strip()
    Cash_Credit=str(request.vars.Cash_Credit).strip()
    Credit_Limit=str(request.vars.Credit_Limit).strip()
    Status=str(request.vars.Status).strip()
    
    
    route = urllib.unquote(route.decode('utf8'))
    client_id = urllib.unquote(client_id.decode('utf8'))
    ChemistName=urllib.unquote(ChemistName.decode('utf8'))
    Address_Line_1=urllib.unquote(Address_Line_1.decode('utf8'))
    district=urllib.unquote(district.decode('utf8'))
    RegistrationNo=urllib.unquote(RegistrationNo.decode('utf8'))
#     NID=urllib.unquote(NID.decode('utf8'))
    Contact_Name=urllib.unquote(Contact_Name.decode('utf8'))
    Contact_phone=urllib.unquote(Contact_phone.decode('utf8'))
    Category=urllib.unquote(Category.decode('utf8'))
    SubCategory=urllib.unquote(SubCategory.decode('utf8'))
    DOB=urllib.unquote(DOB.decode('utf8'))
    Cash_Credit=urllib.unquote(Cash_Credit.decode('utf8'))
#     Credit_Limit=urllib.unquote(Credit_Limit.decode('utf8'))
    Status=urllib.unquote(Status.decode('utf8'))
    thana=urllib.unquote(thana.decode('utf8'))
    catID=''
    catName=''
    subcatID=''
    subcatName=''

    if Category!='' and Category!=None and Category!='None':
        catID=Category.split('|')[1]
        catName=Category.split('|')[0]

    if SubCategory!='' and Category!=None and Category!='None':
        subcatID=SubCategory.split('|')[1]
        subcatName=SubCategory.split('|')[0]
    if DOB=='' or DOB==None or DOB=='None':
        DOB='000-00-00'
    if NID=='' or NID!=None or NID!='None':
        NID=0
    if Contact_phone=='' or Contact_phone!=None or Contact_phone!='None':
        Contact_phone=0
    if Credit_Limit=='' or Credit_Limit!=None or Credit_Limit!='None':
        Credit_Limit=0
    
#    return  subcatID
#     mName=dDist.split('|')[0]
#     mID=dDist.split('|')[1]
    
    
    ChemistName=urllib.unquote(ChemistName.decode('utf8'))
    Address_Line_1=urllib.unquote(Address_Line_1.decode('utf8'))
    district=urllib.unquote(district.decode('utf8'))
    RegistrationNo=urllib.unquote(RegistrationNo.decode('utf8'))
#     NID=urllib.unquote(NID.decode('utf8'))
    Contact_Name=urllib.unquote(Contact_Name.decode('utf8'))
#     Contact_phone=urllib.unquote(Contact_phone.decode('utf8'))
    Category=urllib.unquote(Category.decode('utf8'))
    SubCategory=urllib.unquote(SubCategory.decode('utf8'))
    DOB=urllib.unquote(DOB.decode('utf8'))
    Cash_Credit=urllib.unquote(Cash_Credit.decode('utf8'))
#     Credit_Limit=urllib.unquote(Credit_Limit.decode('utf8'))
    Status=urllib.unquote(Status.decode('utf8'))
    thana=urllib.unquote(thana.decode('utf8'))
    catID=''
    catName=''
    subcatID=''
    subcatName
    if (DOB==''): 
        DOB='1900-01-01'
    compRow = db((db.sm_company_settings.cid == cid) & (db.sm_company_settings.status == 'ACTIVE')).select(db.sm_company_settings.cid, limitby=(0, 1))
    if not compRow:
        return 'FAILED<SYNCDATA>Invalid Company'
    else:
        repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.sync_code == synccode) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.rep_id, db.sm_rep.name, db.sm_rep.mobile_no, db.sm_rep.user_type, db.sm_rep.level_id, db.sm_rep.depot_id, limitby=(0, 1))

        
        if not repRow:
           return 'FAILED<SYNCDATA>Invalid Authorization'

        else:
            chemistRow = db((db.sm_client_temp.cid == cid) & (db.sm_client_temp.client_id == client_id) ).select(db.sm_client_temp.client_id, limitby=(0, 1))
            
            

            if chemistRow:  
                 db((db.sm_client_temp.cid == cid) & (db.sm_client_temp.client_id == client_id) ).update( address=Address_Line_1,area_id =route,vat_registration_no=RegistrationNo ,district=district,thana=thana,nid=int(NID) , owner_name=Contact_Name ,contact_no1=Contact_phone ,category_id=catID , category_name=catName,sub_category_id=subcatID ,sub_category_name=subcatName, dob=DOB ,field1=Cash_Credit ,credit_limit=int(Credit_Limit) ,status=Status,newChemist=0)
                 # db((db.sm_client_temp.cid == cid) & (db.sm_client_temp.client_id == client_id) ).update( address=Address_Line_1,area_id =route,name=ChemistName ,vat_registration_no=RegistrationNo ,district=district,thana=thana,nid=int(NID) , owner_name=Contact_Name ,contact_no1=Contact_phone ,category_id=catID , category_name=catName,sub_category_id=subcatID ,sub_category_name=subcatName, dob=DOB ,field1=Cash_Credit ,credit_limit=int(Credit_Limit) ,status=Status,newChemist=0)
            else:
                db.sm_client_temp.insert(cid =cid,client_id=client_id ,address=Address_Line_1,area_id =route,vat_registration_no=RegistrationNo ,district=district,thana=thana,nid=int(NID) , owner_name=Contact_Name ,contact_no1=Contact_phone ,category_id=catID , category_name=catName,sub_category_id=subcatID ,sub_category_name=subcatName, field1=Cash_Credit ,credit_limit=int(Credit_Limit) ,status=Status,newChemist=0)
                 # db.sm_client_temp.insert(cid =cid,client_id=client_id ,address=Address_Line_1,area_id =route,name=ChemistName ,vat_registration_no=RegistrationNo ,district=district,thana=thana,nid=int(NID) , owner_name=Contact_Name ,contact_no1=Contact_phone ,category_id=catID , category_name=catName,sub_category_id=subcatID ,sub_category_name=subcatName, field1=Cash_Credit ,credit_limit=int(Credit_Limit) ,status=Status,newChemist=0)
                     
    return 'SUCCESS<SYNCDATA>'+'Updated Successfully ! '

# ================================Add Doctor
# def doc_catSp():
#     cid = str(request.vars.cid).strip().upper()
#     rep_id = str(request.vars.rep_id).strip().upper()
#     password = str(request.vars.rep_pass).strip()
#     synccode = str(request.vars.synccode).strip()
#     route = str(request.vars.route).strip()
#    
# #     return client
#     compRow = db((db.sm_company_settings.cid == cid) & (db.sm_company_settings.status == 'ACTIVE')).select(db.sm_company_settings.cid, limitby=(0, 1))
#     if not compRow:
#         return 'FAILED<SYNCDATA>Invalid Company'
#     else:
#         repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.sync_code == synccode) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.rep_id, db.sm_rep.name, db.sm_rep.mobile_no, db.sm_rep.user_type, db.sm_rep.level_id, db.sm_rep.depot_id, limitby=(0, 1))
# 
#         if not repRow:
#            return 'FAILED<SYNCDATA>Invalid Authorization'
# 
#         else:
#             cat_row=db(db.doc_catagory.cid == cid).select(db.doc_catagory.category, orderby=db.doc_catagory.category)
#             catStr=''
#             for cat_row in cat_row:
#                 catStr=catStr+str(cat_row.category)+','
#             
#             spc_row=db(db.doc_speciality.cid == cid).select(db.doc_speciality.specialty, orderby=db.doc_speciality.specialty    )
#             spcStr=''
#             for spc_row in spc_row:
#                 spcStr=spcStr+str(spc_row.specialty)+','
# 
#             
#             rtn_str=str(catStr)+'<fdfd>'+str(spcStr)
# #             return rtn_str
#     return 'SUCCESS<SYNCDATA>'+rtn_str  


def microunion_add_submit():
    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.rep_pass).strip()
    synccode = str(request.vars.synccode).strip()
    
    route = str(request.vars.route).strip()
    routeName= str(request.vars.routeName).strip()
    mIdAdd=str(request.vars.mIdAdd).strip()
    mNameAdd=str(request.vars.mNameAdd).strip()
        
    route = urllib.unquote(route.decode('utf8'))
    routeName= urllib.unquote(routeName.decode('utf8'))
    mIdAdd= urllib.unquote(mIdAdd.decode('utf8'))
    mNameAdd=  urllib.unquote(mNameAdd.decode('utf8'))
    
    
    
    compRow = db((db.sm_company_settings.cid == cid) & (db.sm_company_settings.status == 'ACTIVE')).select(db.sm_company_settings.cid, limitby=(0, 1))
    if not compRow:
        return 'FAILED<SYNCDATA>Invalid Company'
    else:
        repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.sync_code == synccode) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.rep_id, db.sm_rep.name, db.sm_rep.mobile_no, db.sm_rep.user_type, db.sm_rep.level_id, db.sm_rep.depot_id, limitby=(0, 1))
        
        
        if not repRow:
           return 'FAILED<SYNCDATA>Invalid Authorization'

        else:
            micRow = db((db.sm_microunion.cid == cid) & (db.sm_microunion.area_id == route) & (db.sm_microunion.microunion_id == mIdAdd) ).select(db.sm_microunion.microunion_id, limitby=(0, 1))
            if micRow:
                return 'SUCCESS<SYNCDATA>'+'Already Exist '
            else:
                areaRow = db((db.sm_level.cid == cid) & (db.sm_level.level_id == route) ).select(db.sm_level.level0,db.sm_level.level0_name,db.sm_level.level1,db.sm_level.level1_name,db.sm_level.level2,db.sm_level.level2_name,db.sm_level.level_id,db.sm_level.level_name, limitby=(0, 1))
                level0=''
                level0_name=''
                level1=''
                level1_name=''
                level2=''
                level2_name=''
                level_id=''
                level_name=''
                if areaRow:
                    level0=areaRow[0].level0
                    level0_name=areaRow[0].level0_name
                    level1=areaRow[0].level1
                    level1_name=areaRow[0].level1_name
                    level2=areaRow[0].level2
                    level2_name=areaRow[0].level2_name
                    level_id=areaRow[0].level_id
                    level_name=areaRow[0].level_name

            insertMicrounion = db.sm_microunion.insert(cid=cid,microunion_id=mIdAdd, microunion_name=mNameAdd, level0=level0,level0_name=level0_name,level1=level1,level1_name=level1_name,level2=level2,level2_name=level2_name,level3=level_id,level3_name=level_name,area_id=level_id,area_name=level_name,note='Submitted')
            
    return 'SUCCESS<SYNCDATA>'+'Added Successfully  '









def doc_add_submit():
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
    dDist=str(request.vars.dDist).strip()
    dAttachedInstitute=str(request.vars.dAttachedInstitute).strip()
    dS_K_D=str(request.vars.dS_K_D).strip()
    dService=str(request.vars.dService).strip()
    dParty=str(request.vars.dParty).strip()
    
    dDOB=str(request.vars.dDOB).strip()
    dMDay=str(request.vars.dMDay).strip()
    dMobile=str(request.vars.dMobile).strip()
    dCAddress=str(request.vars.dCAddress).strip()
    dOtherChamber=str(request.vars.dOtherChamber).strip()
    dPharmaRoute=str(request.vars.dPharmaRoute).strip().upper()
    dNMDRoute=str(request.vars.dNMDRoute).strip().upper()
    user_type=str(request.vars.user_type).strip()
    repType=    str(request.vars.repType).strip()
    
    route = urllib.unquote(route.decode('utf8'))
    doc= urllib.unquote(doc.decode('utf8'))
    dName= urllib.unquote(dName.decode('utf8'))
    dSpaciality=  urllib.unquote(dSpaciality.decode('utf8'))
    dDegree= urllib.unquote(dDegree.decode('utf8'))
    dCategory= urllib.unquote(dCategory.decode('utf8'))
    dMicroUnion=str(request.vars.dMicroUnion).strip()
    dAttachedInstitute=urllib.unquote(dAttachedInstitute.decode('utf8'))
    dS_K_D=urllib.unquote(dS_K_D.decode('utf8'))
    dService=urllib.unquote(dService.decode('utf8'))
    dParty=urllib.unquote(dParty.decode('utf8'))
    
    dDOB=urllib.unquote(dDOB.decode('utf8'))
    dMDay=urllib.unquote(dMDay.decode('utf8'))
    dMobile=urllib.unquote(dMobile.decode('utf8'))
    dCAddress=urllib.unquote(dCAddress.decode('utf8'))
    dOtherChamber=urllib.unquote(dOtherChamber.decode('utf8'))
    dPharmaRoute=urllib.unquote(dPharmaRoute.decode('utf8'))
    dNMDRoute=urllib.unquote(dNMDRoute.decode('utf8'))
    
    
    
#     if dCategory=='':
#         dCategory='A'
#     if dDist=='':
#         dDist='-'
#     if dThana=='':
#         dThana='-'
    
    
    compRow = db((db.sm_company_settings.cid == cid) & (db.sm_company_settings.status == 'ACTIVE')).select(db.sm_company_settings.cid, limitby=(0, 1))
    if not compRow:
        return 'FAILED<SYNCDATA>Invalid Company'
    else:
        repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.sync_code == synccode) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.rep_id, db.sm_rep.name, db.sm_rep.mobile_no, db.sm_rep.user_type, db.sm_rep.level_id, db.sm_rep.depot_id, db.sm_rep.note, limitby=(0, 1))

        
        if not repRow:
           return 'FAILED<SYNCDATA>Invalid Authorization'

        else:
            #             =============  Nazma 12/05/18
            note=repRow[0][db.sm_rep.note]
                        
            docSlRow = db((db.sm_settings_pharma.cid == cid) & (db.sm_settings_pharma.s_key == 'DOCSL') ).select(db.sm_settings_pharma.s_value, limitby=(0, 1))
            docSL=0
            if docSlRow:
                docSL=docSlRow[0][db.sm_settings_pharma.s_value]
#             Insert Doctor
            docSL=int(docSL)+1
            
            
            
#             ============Nazma========
#             return user_type
            if user_type=='rep' and repType=='SIN':
                nmdChkRow = db((db.sm_rep_area.cid == cid) & (db.sm_rep_area.area_id == dNMDRoute) & (db.sm_rep_area.rep_id == rep_id) ).select(db.sm_rep_area.cid)
            elif user_type=='rep' and repType!='SIN':
                nmdChkRow = db((db.sm_rep_area.cid == cid) & (db.sm_rep_area.area_id == dPharmaRoute) & (db.sm_rep_area.rep_id == rep_id) ).select(db.sm_rep_area.cid)
                
            elif user_type!='rep' and repType!='SIN':
                nmdChkRow = db((db.sm_level.cid == cid) & (db.sm_level.level_id == dPharmaRoute) & (db.sm_level.is_leaf == '1') ).select(db.sm_level.cid) 
#                 nmdChkRow = db((db.sm_rep_area.cid == cid) & (db.sm_rep_area.area_id == dPharmaRoute) & (db.sm_rep_area.rep_id == rep_id) ).select(db.sm_rep_area.cid)
                
            else:
                nmdChkRow = db((db.sm_level.cid == cid) & (db.sm_level.level_id == dNMDRoute) & (db.sm_level.is_leaf == '1') ).select(db.sm_level.cid)
            
            if not nmdChkRow and repType=='SIN':
                return 'FAILED<SYNCDATA>Invalid SNV Route'
            elif not nmdChkRow and repType!='SIN':
                return 'FAILED<SYNCDATA>Invalid Route'
            else:
                if note== 'SIN':
                    insertDoctor = db.sm_doctor_temp.insert(cid =cid,doc_id = docSL,doc_name=dName,specialty=dSpaciality,degree=dDegree,mobile=dMobile,status='ACTIVESIN',attached_institution=dAttachedInstitute,dob=dDOB,mar_day=dMDay,doctors_category=dCategory,service_kol_dsc=dS_K_D,service_id=dService,third_party_id=dParty,note=dCAddress,otherChamber=dOtherChamber,pharma_route_id=dPharmaRoute, sin_route_id=dNMDRoute,microunion=dMicroUnion,new_doc=1)
                    if insertDoctor:  
                         db((db.sm_settings_pharma.cid == cid) & (db.sm_settings_pharma.s_key == 'DOCSL') ).update(s_value=docSL)
                
                else:
                    insertDoctor = db.sm_doctor_temp.insert(cid =cid,doc_id = docSL,doc_name=dName,specialty=dSpaciality,degree=dDegree,mobile=dMobile,status='ACTIVE',attached_institution=dAttachedInstitute,dob=dDOB,mar_day=dMDay,doctors_category=dCategory,service_kol_dsc=dS_K_D,service_id=dService,third_party_id=dParty,note=dCAddress,otherChamber=dOtherChamber,pharma_route_id=dPharmaRoute, nmd_route_id=dNMDRoute,microunion=dMicroUnion,new_doc=1)
                    if insertDoctor:  
                         db((db.sm_settings_pharma.cid == cid) & (db.sm_settings_pharma.s_key == 'DOCSL') ).update(s_value=docSL)
                     
    #                  db.sm_doctor_area.insert(cid=cid, doc_id=docSL, doc_name=dName,area_id=route,area_name=routeName,address=dCAddress,district=dDist,thana=dThana,field1=dMicroUnion)
                 
    return 'SUCCESS<SYNCDATA>'+'Added Successfully  '

# ================================ Doctor List
def doc_list():
    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.rep_pass).strip()
    synccode = str(request.vars.synccode).strip()
    route = str(request.vars.route).strip()
    repType = str(request.vars.repType).strip()
    
    
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
              
                if cid=='IPINMD':
                    doctorRows = db((db.sm_doctor_temp.cid == cid) & (db.sm_doctor_temp.status != 'REJECTED') & (db.sm_doctor_temp.status != 'ACTIVESIN')  & (db.sm_doctor_temp.nmd_route_id.belongs(areaList))   ).select(db.sm_doctor_temp.doc_id, db.sm_doctor_temp.doc_name, db.sm_doctor_temp.nmd_route_id, db.sm_doctor_temp.pharma_route_id,db.sm_doctor_temp.sin_route_id, orderby=db.sm_doctor_temp.doc_id)
                else:
                    if repType=='SIN':
#                         return repType
                        doctorRows = db((db.sm_doctor_temp.cid == cid)   & (db.sm_doctor_temp.status == 'ACTIVESIN') & (db.sm_doctor_temp.sin_route_id.belongs(areaList))   ).select(db.sm_doctor_temp.doc_id, db.sm_doctor_temp.doc_name, db.sm_doctor_temp.nmd_route_id, db.sm_doctor_temp.pharma_route_id,db.sm_doctor_temp.sin_route_id, orderby=db.sm_doctor_temp.doc_id)
                    else:    
                        doctorRows = db((db.sm_doctor_temp.cid == cid) & (db.sm_doctor_temp.status != 'REJECTED')  & (db.sm_doctor_temp.status != 'ACTIVESIN') & (db.sm_doctor_temp.pharma_route_id.belongs(areaList))   ).select(db.sm_doctor_temp.doc_id, db.sm_doctor_temp.doc_name, db.sm_doctor_temp.nmd_route_id, db.sm_doctor_temp.pharma_route_id,db.sm_doctor_temp.sin_route_id, orderby=db.sm_doctor_temp.doc_id)
                    
#                 doctorRows = db((db.sm_doctor.cid == cid) & (db.sm_doctor.status == 'SUBMITTED') & (db.sm_doctor_area.cid == cid) & (db.sm_doctor_area.doc_id == db.sm_doctor.doc_id) & (db.sm_doctor_area.area_id.belongs(areaList))   ).select(db.sm_doctor.doc_id, db.sm_doctor.doc_name, db.sm_doctor_area.area_id, orderby=db.sm_doctor.doc_id)
#                 return doctorRows
                if not doctorRows:
                    rtn_str='Nothing pending for approval.'
    
                else:
                    rtn_str=' <table width="100%" border="0" cellspacing="0" cellpadding="0">'
                    for doctorRow in doctorRows:
                        doctor_id = doctorRow.doc_id
                        doctor_name = doctorRow.doc_name
                        doctor_area_pharma = doctorRow.pharma_route_id
                        doctor_area_nmd = doctorRow.nmd_route_id
                        
                        if doctor_area_nmd=='':
                            doctor_area_nmd = doctorRow.sin_route_id
                            
                        rtn_str=rtn_str+' <tr  height="30px"> <td >'+str(doctor_name)+'|'+str(doctor_id)+'|'+str(doctor_area_pharma)+'|'+str(doctor_area_nmd)+' </td><td></td></tr>'
                    rtn_str=rtn_str+'</table>'
#                 return rtn_str
#                 =======Microunion
                microunionRows = db((db.sm_microunion.cid == cid) & (db.sm_microunion.area_id.belongs(areaList)) & (db.sm_microunion.note == 'Submitted')  ).select(db.sm_microunion.area_id, db.sm_microunion.area_name,db.sm_microunion.microunion_id, db.sm_microunion.microunion_name, orderby=db.sm_microunion.area_id| db.sm_microunion.area_name|db.sm_microunion.microunion_id| db.sm_microunion.microunion_name)

                if not microunionRows:
                    micro_str='Nothing pending for approval.'
    
                else:
                    micro_str=' <table width="100%" border="0" cellspacing="0" cellpadding="0">'
                    for microunionRows in microunionRows:
                        area_id = microunionRows.area_id
                        area_name = microunionRows.area_name
                        microunion_id = microunionRows.microunion_id
                        microunion_name = microunionRows.microunion_name
                        micro_str=micro_str+' <tr  height="30px"> <td >'+str(area_name)+'|'+str(area_id)+'--'+str(microunion_name)+'|'+str(microunion_id)+' </td><td></td></tr>'
                    micro_str=micro_str+'</table>'                
#                 return micro_str
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
                        
                if cid=='IPINMD':
                    doctorRows = db((db.sm_doctor_temp.cid == cid) & (db.sm_doctor_temp.status != 'REJECTED')  & (db.sm_doctor_temp.nmd_route_id.belongs(areaList))   ).select(db.sm_doctor_temp.doc_id, db.sm_doctor_temp.doc_name, db.sm_doctor_temp.nmd_route_id, db.sm_doctor_temp.pharma_route_id,db.sm_doctor_temp.sin_route_id, orderby=db.sm_doctor_temp.doc_id)
                else:
                    
                    if repType=='SIN':
                        
                        doctorRows = db((db.sm_doctor_temp.cid == cid)  & (db.sm_doctor_temp.status == 'ACTIVESIN') & (db.sm_doctor_temp.sin_route_id.belongs(areaList))   ).select(db.sm_doctor_temp.doc_id, db.sm_doctor_temp.doc_name, db.sm_doctor_temp.nmd_route_id, db.sm_doctor_temp.pharma_route_id,db.sm_doctor_temp.sin_route_id, orderby=db.sm_doctor_temp.doc_id)
                    else:    
                        doctorRows = db((db.sm_doctor_temp.cid == cid) & (db.sm_doctor_temp.status != 'REJECTED')  & (db.sm_doctor_temp.status != 'ACTIVESIN') & (db.sm_doctor_temp.pharma_route_id.belongs(areaList))   ).select(db.sm_doctor_temp.doc_id, db.sm_doctor_temp.doc_name, db.sm_doctor_temp.nmd_route_id, db.sm_doctor_temp.pharma_route_id,db.sm_doctor_temp.sin_route_id, orderby=db.sm_doctor_temp.doc_id)
                    
#                     doctorRows = db((db.sm_doctor_temp.cid == cid) & (db.sm_doctor_temp.status != 'REJECTED')  & (db.sm_doctor_temp.pharma_route_id.belongs(areaList))   ).select(db.sm_doctor_temp.doc_id, db.sm_doctor_temp.doc_name, db.sm_doctor_temp.nmd_route_id, db.sm_doctor_temp.pharma_route_id,db.sm_doctor_temp.sin_route_id, orderby=db.sm_doctor_temp.doc_id)
                 
                if not doctorRows:
                    rtn_str='Nothing pending for approval.'
    
                else:

                    rtn_str=' <table width="100%" border="0" cellspacing="0" cellpadding="0">'
                  
                    for doctorRow in doctorRows:
                        doctor_id = doctorRow.doc_id
                        doctor_name = doctorRow.doc_name
                        doctor_area_pharma = doctorRow.pharma_route_id
                        doctor_area_nmd = doctorRow.nmd_route_id
                        if doctor_area_nmd=='':
                            doctor_area_nmd = doctorRow.sin_route_id
                            
                        rtn_str=rtn_str+' <tr  height="30px"> <td style="color:#fff">'+str(doctor_name)+'|'+str(doctor_id)+'|'+str(doctor_area_pharma)+'|'+str(doctor_area_nmd)+' </td><td><img  width="50px;" height="50px" src="confirm.png"  onClick="confirmDoc('+str(doctor_id)+')"  alt=""></td></tr>'
                    rtn_str=rtn_str+'</table>'
                    
#                 return rtn_str
                #                 =======Microunion
                microunionRows = db((db.sm_microunion.cid == cid) & (db.sm_microunion.area_id.belongs(areaList)) & (db.sm_microunion.note == 'Submitted')  ).select(db.sm_microunion.area_id, db.sm_microunion.area_name,db.sm_microunion.microunion_id, db.sm_microunion.microunion_name, orderby=db.sm_microunion.area_id| db.sm_microunion.area_name|db.sm_microunion.microunion_id| db.sm_microunion.microunion_name)

                if not microunionRows:
                    micro_str='Nothing pending for approval.'
    
                else:
                    micro_str=' <table width="100%" border="0" cellspacing="0" cellpadding="0">'
                    for microunionRows in microunionRows:
                        area_id = microunionRows.area_id
                        area_name = microunionRows.area_name
                        microunion_id = microunionRows.microunion_id
                        microunion_name = microunionRows.microunion_name
                        microPass=area_id+'|'+microunion_id
                        micro_str=micro_str+' <tr  height="30px"> <td >'+str(area_name)+'|'+str(area_id)+'--'+str(microunion_name)+'|'+str(microunion_id)+' </td><td><img  width="50px;" height="50px" src="confirm.png"  onClick="confirmMicro(\''+microPass+'\')"  alt=""> </td></tr>'
                    micro_str=micro_str+'</table>'     
                
#             return rtn_str
    return 'SUCCESS<SYNCDATA>'+rtn_str +'<SYNCDATA>'+micro_str 

def microConfirm():
    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.rep_pass).strip()
    synccode = str(request.vars.synccode).strip()
    area_Id = str(request.vars.area_Id).strip()
    micro_Id = str(request.vars.micro_Id).strip()
    
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
                
                if cid=='IPINMD':
                    doctorRows = db((db.sm_doctor_temp.cid == cid) & (db.sm_doctor_temp.status != 'REJECTED')  & (db.sm_doctor_temp.nmd_route_id.belongs(areaList))   ).select(db.sm_doctor_temp.doc_id, db.sm_doctor_temp.doc_name, db.sm_doctor_temp.nmd_route_id, db.sm_doctor_temp.pharma_route_id,db.sm_doctor_temp.sin_route_id, orderby=db.sm_doctor_temp.doc_id)
                else:
                    doctorRows = db((db.sm_doctor_temp.cid == cid) & (db.sm_doctor_temp.status != 'REJECTED')  & (db.sm_doctor_temp.pharma_route_id.belongs(areaList))   ).select(db.sm_doctor_temp.doc_id, db.sm_doctor_temp.doc_name, db.sm_doctor_temp.nmd_route_id, db.sm_doctor_temp.pharma_route_id,db.sm_doctor_temp.sin_route_id, orderby=db.sm_doctor_temp.doc_id)
                 
                if not doctorRows:
                    rtn_str='Nothing pending for approval.'
    
                else:

                    rtn_str=' <table width="100%" border="0" cellspacing="0" cellpadding="0">'
                  
                    for doctorRow in doctorRows:
                        doctor_id = doctorRow.doc_id
                        doctor_name = doctorRow.doc_name
                        doctor_area_pharma = doctorRow.pharma_route_id
                        doctor_area_nmd = doctorRow.nmd_route_id
                        
                        if doctor_area_nmd=='':
                            doctor_area_nmd = doctorRow.sin_route_id
                        
                        rtn_str=rtn_str+' <tr  height="30px"> <td >'+str(doctor_name)+'|'+str(doctor_id)+'|'+str(doctor_area_pharma)+'|'+str(doctor_area_nmd)+' </td></tr>'
                    rtn_str=rtn_str+'</table>'
                
#                 =======Microunion
                microunionRows = db((db.sm_microunion.cid == cid) & (db.sm_microunion.area_id.belongs(areaList)) & (db.sm_microunion.note == 'Submitted')  ).select(db.sm_microunion.area_id, db.sm_microunion.area_name,db.sm_microunion.microunion_id, db.sm_microunion.microunion_name, orderby=db.sm_microunion.area_id| db.sm_microunion.area_name|db.sm_microunion.microunion_id| db.sm_microunion.microunion_name)

                if not microunionRows:
                    micro_str='Nothing pending for approval.'
    
                else:
                    micro_str=' <table width="100%" border="0" cellspacing="0" cellpadding="0">'
                    for doctorRow in doctorRows:
                        area_id = microunionRows.area_id
                        area_name = microunionRows.area_name
                        microunion_id = microunionRows.microunion_id
                        microunion_name = microunionRows.microunion_name
                        micro_str=rtn_str+' <tr  height="30px"> <td >'+str(area_name)+'|'+str(area_id)+'--'+str(microunion_name)+'|'+str(microunion_id)+' </td><td></td></tr>'
                    micro_str=micro_str+'</table>'                

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
                        
                if cid=='IPINMD':
                    doctorRows = db((db.sm_doctor_temp.cid == cid) & (db.sm_doctor_temp.status != 'REJECTED')  & (db.sm_doctor_temp.nmd_route_id.belongs(areaList))   ).select(db.sm_doctor_temp.doc_id, db.sm_doctor_temp.doc_name, db.sm_doctor_temp.nmd_route_id, db.sm_doctor_temp.pharma_route_id,db.sm_doctor_temp.sin_route_id, orderby=db.sm_doctor_temp.doc_id)
                else:
                    doctorRows = db((db.sm_doctor_temp.cid == cid) & (db.sm_doctor_temp.status != 'REJECTED')  & (db.sm_doctor_temp.pharma_route_id.belongs(areaList))   ).select(db.sm_doctor_temp.doc_id, db.sm_doctor_temp.doc_name, db.sm_doctor_temp.nmd_route_id, db.sm_doctor_temp.pharma_route_id,db.sm_doctor_temp.sin_route_id, orderby=db.sm_doctor_temp.doc_id)
                 
                if not doctorRows:
                    rtn_str='Nothing pending for approval.'
    
                else:

                    rtn_str=' <table width="100%" border="0" cellspacing="0" cellpadding="0">'
                  
                    for doctorRow in doctorRows:
                        doctor_id = doctorRow.doc_id
                        doctor_name = doctorRow.doc_name
                        doctor_area_pharma = doctorRow.pharma_route_id
                        doctor_area_nmd = doctorRow.nmd_route_id
                        
                        if doctor_area_nmd=='':
                            doctor_area_nmd = doctorRow.sin_route_id
                            
                        rtn_str=rtn_str+' <tr  height="30px"> <td style="color:#fff">'+str(doctor_name)+'|'+str(doctor_id)+'|'+str(doctor_area_pharma)+'|'+str(doctor_area_nmd)+' </td><td><img  width="50px;" height="50px" src="confirm.png"  onClick="confirmDoc('+str(doctor_id)+')"  alt=""></td></tr>'
                    rtn_str=rtn_str+'</table>'
                    
                
                #                 =======Microunion
                
                microunionRowsCheck = db((db.sm_microunion.cid == cid) & (db.sm_microunion.area_id==area_Id) & (db.sm_microunion.microunion_id == micro_Id) & (db.sm_microunion.note != 'Submitted')  ).select(db.sm_microunion.area_id, limitby=(0,1))
                if microunionRowsCheck:
                    pass
                else:
                    microunionRowsConfirm = db((db.sm_microunion.cid == cid) & (db.sm_microunion.area_id==area_Id) & (db.sm_microunion.microunion_id == micro_Id)   ).update(note='Active')
                    
                    
                
                
                microunionRows = db((db.sm_microunion.cid == cid) & (db.sm_microunion.area_id.belongs(areaList)) & (db.sm_microunion.note == 'Submitted')  ).select(db.sm_microunion.area_id, db.sm_microunion.area_name,db.sm_microunion.microunion_id, db.sm_microunion.microunion_name, orderby=db.sm_microunion.area_id| db.sm_microunion.area_name|db.sm_microunion.microunion_id| db.sm_microunion.microunion_name)

                if not microunionRows:
                    micro_str='Nothing pending for approval.'
    
                else:
                    micro_str=' <table width="100%" border="0" cellspacing="0" cellpadding="0">'
                    for microunionRows in microunionRows:
                        area_id = microunionRows.area_id
                        area_name = microunionRows.area_name
                        microunion_id = microunionRows.microunion_id
                        microunion_name = microunionRows.microunion_name
                        microPass=area_id+'|'+microunion_id
                        micro_str=micro_str+' <tr  height="30px"> <td >'+str(area_name)+'|'+str(area_id)+'--'+str(microunion_name)+'|'+str(microunion_id)+' </td><td><img  width="50px;" height="50px" src="confirm.png"  onClick="confirmMicro(\''+microPass+'\')"  alt=""> </td></tr>'
                    micro_str=micro_str+'</table>'     
                
#             return rtn_str
    return 'SUCCESS<SYNCDATA>'+rtn_str +'<SYNCDATA>'+micro_str 

def confirmDoc():
    #     Nazma
    url_part_1 = 'http://w02.yeapps.com/vitalac/syncmobile_417_new_ibn_newtest/'
    
    
    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.rep_pass).strip()
    synccode = str(request.vars.synccode).strip()
    route = str(request.vars.route).strip()
    docID = str(request.vars.docID).strip()
    pharma_route= str(request.vars.pharma_route).strip().upper()
    nmd_route= str(request.vars.nmd_route).strip().upper()
    repType= str(request.vars.repType).strip().upper()
    
    rtn_str=''
#     return docID
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
                pass


            else:
                
                
                
                
                
                docRowsGet = db((db.sm_doctor_temp.cid == cid) & (db.sm_doctor_temp.doc_id == docID) ).select(db.sm_doctor_temp.ALL, limitby=(0,1))
                if docRowsGet:
                    cid                     =docRowsGet[0][db.sm_rep.cid]
                    doc_id                  =docRowsGet[0][db.sm_doctor_temp.doc_id]
                    doc_name                =docRowsGet[0][db.sm_doctor_temp.doc_name]
                    specialty               =docRowsGet[0][db.sm_doctor_temp.specialty]
                    degree                  =docRowsGet[0][db.sm_doctor_temp.degree]                   
                    mobile                  =docRowsGet[0][db.sm_doctor_temp.mobile]                    
                    des                     =docRowsGet[0][db.sm_doctor_temp.note]
                    status                  =docRowsGet[0][db.sm_doctor_temp.status]
                    attached_institution    =docRowsGet[0][db.sm_doctor_temp.attached_institution]
                    designation             =docRowsGet[0][db.sm_doctor_temp.designation]
                    dob                     =docRowsGet[0][db.sm_doctor_temp.dob]
                    mar_day                 =docRowsGet[0][db.sm_doctor_temp.mar_day]
                    doctors_category        =docRowsGet[0][db.sm_doctor_temp.doctors_category]
                    service_kol_dsc         =docRowsGet[0][db.sm_doctor_temp.service_kol_dsc]
                    service_id              =docRowsGet[0][db.sm_doctor_temp.service_id]
                    third_party_id          =docRowsGet[0][db.sm_doctor_temp.third_party_id]
                    otherChamber            =docRowsGet[0][db.sm_doctor_temp.otherChamber]               
                    pharma_route_id         =docRowsGet[0][db.sm_doctor_temp.pharma_route_id]
                    pharma_route_name       =docRowsGet[0][db.sm_doctor_temp.pharma_route_name]
                    nmd_route_id            =docRowsGet[0][db.sm_doctor_temp.nmd_route_id]
                    nmd_route_name          =docRowsGet[0][db.sm_doctor_temp.nmd_route_name]
                    new_doc                 =docRowsGet[0][db.sm_doctor_temp.new_doc]
                    
                    field1                  =docRowsGet[0][db.sm_doctor_temp.field1]
                    note                    =docRowsGet[0][db.sm_doctor_temp.note]
                    microunion              =docRowsGet[0][db.sm_doctor_temp.microunion]
                    
                    # =============Nazma 12/05/2018 start
                    sin_route_id            =docRowsGet[0][db.sm_doctor_temp.sin_route_id]
                    sin_route_name          =docRowsGet[0][db.sm_doctor_temp.sin_route_name]
                    #=======================================
                    
                    # ==========Nazma start
                    if status=='Rreq':
#                         if cid=='IBNSINA':
        #                 if cid=='ACME':
                        delete_doc_area=db((db.sm_doctor_area.cid == cid) & (db.sm_doctor_area.doc_id == docID) & (db.sm_doctor_area.area_id == pharma_route)).delete()
                        delete_temp=db((db.sm_doctor_temp.cid == cid) & (db.sm_doctor_temp.doc_id == docID) & (db.sm_doctor_temp.status == 'Rreq') & (db.sm_doctor_temp.pharma_route_id == pharma_route) & (db.sm_doctor_temp.new_doc == 0)).delete() 
            
                        if cid=='IPINMD':
                            delete_doc_area=db((db.sm_doctor_area.cid == cid) & (db.sm_doctor_area.doc_id == docID) & (db.sm_doctor_area.area_id == nmd_route)).delete()
                            delete_temp=db((db.sm_doctor_temp.cid == cid) & (db.sm_doctor_temp.doc_id == docID) & (db.sm_doctor_temp.status == 'Rreq') & (db.sm_doctor_temp.nmd_route_id == nmd_route) & (db.sm_doctor_temp.new_doc == 0) ).delete() 
                    
    # ==========Nazma end
                    
                    
                    # ================    Nazma
                    
                    phrmaChkRow = db((db.sm_level.cid == cid) & (db.sm_level.level_id == pharma_route_id) & (db.sm_level.is_leaf == '1') ).select(db.sm_level.cid)
#                     return phrmaChkRow           
                    if not phrmaChkRow:
                        return 'FAILED<SYNCDATA>Invalid Route'
                    
                    else:
                        docSlRow = db((db.sm_settings_pharma.cid == cid) & (db.sm_settings_pharma.s_key == 'DOCSL') ).select(db.sm_settings_pharma.s_value, limitby=(0, 1))
                        docSL=0
                        if docSlRow:
                            docSL=docSlRow[0][db.sm_settings_pharma.s_value]
                        docSL=int(docSL)+1
                        db((db.sm_settings_pharma.cid == cid) & (db.sm_settings_pharma.s_key == 'DOCSL') ).update(s_value=docSL)
                        
#                         if repType=='SIN' or repType=='':
#                             
#                             phrmaChkRow = db((db.sm_level.cid == cid) & (db.sm_level.level_id == pharma_route_id) & (db.sm_level.is_leaf == '1') ).select(db.sm_level.cid)
#                             
#                             if not phrmaChkRow:
#                                 return 'FAILED<SYNCDATA>Invalid Route'
#                             
#                             else:
#                                 delete_temp=db((db.sm_doctor_temp.cid == cid) & (db.sm_doctor_temp.doc_id == docID)).update(status = 'ACTIVE')
#                         
#                         
#                         else:
                        if new_doc==1 and pharma_route_id!='':
                            phrmaChkRow = db((db.sm_level.cid == cid) & (db.sm_level.level_id == pharma_route_id) & (db.sm_level.is_leaf == '1') ).select(db.sm_level.cid)
                            if not phrmaChkRow:
                                return 'FAILED<SYNCDATA>Invalid Route'
                            
                            else:
                                doc_id=docSL
                                doc_insert=db.sm_doctor.insert(cid=cid, doc_id=doc_id, doc_name=doc_name, specialty=specialty,degree=degree,mobile=mobile,des=des,status='ACTIVE',attached_institution=attached_institution,designation=designation,dob=dob,mar_day=mar_day,doctors_category=doctors_category,service_kol_dsc=service_kol_dsc,service_id=service_id,third_party_id=third_party_id,pharma_route=pharma_route,sin_route=sin_route_id,field1=microunion,chamber_1=otherChamber)
                                docRowCheckP=db((db.sm_doctor_area.cid == cid) & (db.sm_doctor_area.doc_id == docID) & (db.sm_doctor_area.area_id == pharma_route_id) ).select(db.sm_doctor_area.area_id, limitby=(0,1))
                                
                                if docRowCheckP:
                                    pass
                                else:
                                    docarea_insert=db.sm_doctor_area.insert(cid=cid,doc_id=doc_id,doc_name=doc_name,area_id=pharma_route)    
        
                                docRowCheckS=db((db.sm_doctor_area.cid == cid) & (db.sm_doctor_area.doc_id == docID) & (db.sm_doctor_area.area_id == sin_route_id) ).select(db.sm_doctor_area.area_id, limitby=(0,1))
                                
                                if docRowCheckS:
                                    pass
                                else:
                                    docarea_insert=db.sm_doctor_area.insert(cid=cid,doc_id=doc_id,doc_name=doc_name,area_id=sin_route_id)    
    
                            delete_temp=db((db.sm_doctor_temp.cid == cid) & (db.sm_doctor_temp.doc_id == docID)).delete()
        
        
                            
                            
#                             elif new_doc==1  and status !='ACTIVESIN':
#                                 doc_id=docSL
#                                 doc_insert=db.sm_doctor.insert(cid=cid, doc_id=doc_id, doc_name=doc_name, specialty=specialty,degree=degree,mobile=mobile,des=des,status='ACTIVE',attached_institution=attached_institution,designation=designation,dob=dob,mar_day=mar_day,doctors_category=doctors_category,service_kol_dsc=service_kol_dsc,service_id=service_id,third_party_id=third_party_id,pharma_route=pharma_route,nmd_route=nmd_route)
#                                 docarea_insert=db.sm_doctor_area.insert(cid=cid,doc_id=doc_id,doc_name=doc_name,area_id=pharma_route_id)   
                                #         Nazma
#                                 userText = str(cid).strip() + '<url>' + str(doc_id).strip() + '<url>' + str(doc_name).strip() + '<url>' + str(specialty) + '<url>' + str(degree).strip() + '<url>' + str(mobile).strip() + '<url>' +str(des).strip() + '<url>'+str(status).strip() + '<url>'+str(attached_institution).strip() + '<url>'+str(designation).strip() + '<url>'+str(dob).strip() + '<url>'+ str(mar_day).strip() + '<url>'+str(doctors_category).strip() + '<url>'+str(service_kol_dsc).strip() + '<url>'+str(service_id).strip() + '<url>'+ str(third_party_id ).strip() + '<url>'+str(pharma_route ).strip() + '<url>' +str(nmd_route ).strip() + '<url>' +str(new_doc ).strip()                                                 
#                                 request_text = urllib2.quote(userText)
#                                 url = url_part_1+'addDocIPInmd?add_data=' + request_text     
#                                 result = fetch(url)
                                
                                
                                
                                
        #                         return db._lastsql
#                                 if cid=='IPINMD':
#                                     doc_id=docSL
#                                     docRowCheck=db((db.sm_doctor_area.cid == cid) & (db.sm_doctor_area.doc_id == doc_id) & (db.sm_doctor_area.area_id == nmd_route_id) ).select(db.sm_doctor_area.area_id, limitby=(0,1))
#                                     if docRowCheck:
#                                         pass
#                                     else:
#                                         docarea_insert=db.sm_doctor_area.insert(cid=cid,doc_id=doc_id,doc_name=doc_name,area_id=nmd_route)   
                                        #     Nazma
                
#                                         userText = str(cid).strip() + '<url>' + str(doc_id).strip() + '<url>' + str(doc_name).strip() +  '<url>' +str(nmd_route ).strip()  + '<url>' +str(new_doc ).strip() 
#                                         request_text = urllib2.quote(userText)
#                                         url = url_part_1+'addDocAreaIPInmd?add_data=' + request_text     
#                                         result = fetch(url)
                                        
                                        
                                        
#                                 else:
#                                     
#                                     docRowCheck=db((db.sm_doctor_area.cid == cid) & (db.sm_doctor_area.doc_id == doc_id) & (db.sm_doctor_area.area_id == pharma_route_id) ).select(db.sm_doctor_area.area_id, limitby=(0,1))
#                                     if docRowCheck:
#                                         pass
#                                     else:
#                                         docarea_insert=db.sm_doctor_area.insert(cid=cid,doc_id=doc_id,doc_name=doc_name,area_id=pharma_route)  
#                                     #     Nazma
#         
# #                                         userText = str(cid).strip() + '<url>' + str(doc_id).strip() + '<url>' + str(doc_name).strip() +  '<url>' +str(nmd_route ).strip()  + '<url>' +str(new_doc ).strip() 
# #                                         request_text = urllib2.quote(userText)
# #                                         url = url_part_1+'addDocAreaPharmaNmdIpi?add_data=' + request_text     
# #                                         result = fetch(url)
#                                         
#                                                                                          
#                                 delete_temp=db((db.sm_doctor_temp.cid == cid) & (db.sm_doctor_temp.doc_id == docID)).delete()
                        else:
                            
                            doc_update=db((db.sm_doctor.cid == cid) & (db.sm_doctor.doc_id == doc_id) ).update(doc_name=doc_name, specialty=specialty,degree=degree,mobile=mobile,des=des,status='ACTIVE',attached_institution=attached_institution,designation=designation,dob=dob,mar_day=mar_day,doctors_category=doctors_category,service_kol_dsc=service_kol_dsc,service_id=service_id,third_party_id=third_party_id)#,pharma_route=pharma_route_id,nmd_route=nmd_route_id)
                            docRowCheck=db((db.sm_doctor_area.cid == cid) & (db.sm_doctor_area.doc_id == doc_id) & (db.sm_doctor_area.area_id == pharma_route_id) ).select(db.sm_doctor_area.area_id, limitby=(0,1))
                            if docRowCheck:
                                pass
                            else:
                                docarea_insert=db.sm_doctor_area.insert(cid=cid,doc_id=doc_id,doc_name=doc_name,area_id=pharma_route_id)
                                #     Nazma Update
                                
#                                 userText = str(cid).strip() + '<url>' + str(docID).strip() + '<url>' + str(doc_name).strip() +  '<url>' +str(specialty ).strip() + '<url>' + str(degree).strip() + '<url>' + str(mobile).strip() +  '<url>' +str(des ).strip() + '<url>' + str(attached_institution).strip() + '<url>' + str(designation).strip() +  '<url>' +str(dob ).strip() + '<url>' + str(mar_day).strip() + '<url>' + str(doctors_category).strip() +  '<url>' +str(service_kol_dsc ).strip() + '<url>' + str(service_id).strip() + '<url>' + str(third_party_id).strip() +  '<url>' +str(pharma_route_id ).strip()  +  '<url>' +str(nmd_route_id ).strip()  + '<url>' +str(new_doc ).strip() 
#                                 request_text = urllib2.quote(userText)
#                                 url = url_part_1+'updateDocIpiNmd?add_data=' + request_text     
#                                 result = fetch(url)
    #                             -------------
    #                             if cid=='IPINMD':
    #                                 docRowCheck=db((db.sm_doctor_area.cid == cid) & (db.sm_doctor_area.doc_id == doc_id) & (db.sm_doctor_area.area_id == nmd_route_id) ).select(db.sm_doctor_area.area_id, limitby=(0,1))
    #                                 if docRowCheck:
    #                                     pass
    #                                 else:
    #                                     docarea_insert=db.sm_doctor_area.insert(cid=cid,doc_id=doc_id,doc_name=doc_name,area_id=nmd_route)
    #                             #     Nazma
    #     
    #                                     userText = str(cid).strip() + '<url>' + str(doc_id).strip() + '<url>' + str(doc_name).strip() +  '<url>' +str(nmd_route_id ).strip()  + '<url>' +str(new_doc ).strip()
    #                                     request_text = urllib2.quote(userText)
    #                                     url = url_part_1+'addDocAreaIpinmdNm?add_data=' + request_text             
    #                                     result = fetch(url)
    #                                        
    #                             else:
    #                                 docRowCheck=db((db.sm_doctor_area.cid == cid) & (db.sm_doctor_area.doc_id == doc_id) & (db.sm_doctor_area.area_id == pharma_route_id) ).select(db.sm_doctor_area.area_id, limitby=(0,1))
    #                                 if docRowCheck:
    #                                     pass
    #                                 else:
    #                                     docarea_insert=db.sm_doctor_area.insert(cid=cid,doc_id=doc_id,doc_name=doc_name,area_id=pharma_route)  
    #                                     #     Nazma
    #                                     userText = str(cid).strip() + '<url>' + str(doc_id).strip() + '<url>' + str(doc_name).strip() +  '<url>' +str(nmd_route_id ).strip()  + '<url>' +str(new_doc ).strip()
    #                                     request_text = urllib2.quote(userText)
    #                                     url = url_part_1+'addDocAreaRtNmdIpi?add_data=' + request_text     
    #                                     result = fetch(url)
    #     #                                 -----------------
                            
                            delete_temp=db((db.sm_doctor_temp.cid == cid) & (db.sm_doctor_temp.doc_id == doc_id)).delete()
                    
                    
                    
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
                
                levelSpecialRows = db((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '1') & (db.sm_level.special_territory_code.belongs(spicial_codeList))).select(db.sm_level.level_id, db.sm_level.level_name, db.sm_level.depot_id)    
                for levelSpecialRow in levelSpecialRows:
                    level_id = levelSpecialRow.level_id
                    level_name = levelSpecialRow.level_name
                    if level_id not in areaList:
                            areaList.append(level_id)
                        
                if cid=='IPINMD':
                    doctorRows = db((db.sm_doctor_temp.cid == cid) & (db.sm_doctor_temp.status != 'REJECTED')  & (db.sm_doctor_temp.nmd_route_id.belongs(areaList))   ).select(db.sm_doctor_temp.doc_id, db.sm_doctor_temp.doc_name, db.sm_doctor_temp.nmd_route_id, db.sm_doctor_temp.pharma_route_id,db.sm_doctor_temp.sin_route_id, orderby=db.sm_doctor_temp.doc_id)
                else:
                    doctorRows = db((db.sm_doctor_temp.cid == cid) & (db.sm_doctor_temp.status != 'REJECTED')  & (db.sm_doctor_temp.pharma_route_id.belongs(areaList))   ).select(db.sm_doctor_temp.doc_id, db.sm_doctor_temp.doc_name, db.sm_doctor_temp.nmd_route_id, db.sm_doctor_temp.pharma_route_id,db.sm_doctor_temp.sin_route_id, orderby=db.sm_doctor_temp.doc_id)
                 
                if not doctorRows:
                    rtn_str='Nothing pending for approval.'
    
                else:

                    rtn_str=' <table width="100%" border="0" cellspacing="0" cellpadding="0">'
                  
                    for doctorRow in doctorRows:
                        doctor_id = doctorRow.doc_id
                        doctor_name = doctorRow.doc_name
                        doctor_area_pharma = doctorRow.pharma_route_id
                        doctor_area_nmd = doctorRow.nmd_route_id
                        
                        if doctor_area_nmd=='':
                            doctor_area_nmd = doctorRow.sin_route_id
                        
                        rtn_str=rtn_str+' <tr  height="30px"> <td style="color:#fff">'+str(doctor_name)+'|'+str(doctor_id)+'|'+str(doctor_area_pharma)+'|'+str(doctor_area_nmd)+' </td><td><img  width="50px;" height="50px" src="confirm.png"  onClick="confirmDoc('+str(doctor_id)+')"  alt=""></td></tr>'
                    rtn_str=rtn_str+'</table>'
#             return rtn_str
    return 'SUCCESS<SYNCDATA>'+rtn_str 

def cancelDoc():
    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.rep_pass).strip()
    synccode = str(request.vars.synccode).strip()
    route = str(request.vars.route).strip()
    docID = str(request.vars.docID).strip()
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
                pass
#                 areaList=[]
#                 levelRows = db((db.sm_rep_area.cid == cid) & (db.sm_rep_area.rep_id == rep_id)).select(db.sm_rep_area.area_id)
#                     
#                 for levelRow in levelRows:
#                     level_id = levelRow.area_id
#                     
#                     if level_id not in areaList:
#                         areaList.append(level_id)
#                 
#                 doctorRows = db((db.sm_doctor.cid == cid) & (db.sm_doctor.status == 'SUBMITTED') & (db.sm_doctor_area.cid == cid) & (db.sm_doctor_area.doc_id == db.sm_doctor.doc_id) & (db.sm_doctor_area.area_id.belongs(areaList))   ).select(db.sm_doctor.doc_id, db.sm_doctor.doc_name, db.sm_doctor_area.area_id, orderby=db.sm_doctor.doc_id)
#                 if not doctorRows:
#                     rtn_str='Nothing pending for approval.'
#     
#                 else:
#                     rtn_str=' <table width="100%" border="0" cellspacing="0" cellpadding="0">'
#                     for doctorRow in doctorRows:
#                         doctor_id = doctorRow.sm_doctor.doc_id
#                         doctor_name = doctorRow.sm_doctor.doc_name
#                         doctor_area = doctorRow.sm_doctor_area.area_id
#                         rtn_str=rtn_str+' <tr  height="30px"> <td >'+str(doctor_name)+'|'+str(doctor_id)+'|'+str(doctor_area)+' </td><td></td></tr>'
#                     rtn_str=rtn_str+'</table>'
                                

            else:
                doctorRows = db((db.sm_doctor_temp.cid == cid) & (db.sm_doctor_temp.doc_id == docID) ).update(status = 'REJECTED')
#                 docareRows= db((db.sm_doctor_area.cid == cid) & (db.sm_doctor_area.doc_id == docID) ).delete()
                
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
                
                levelSpecialRows = db((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '1') & (db.sm_level.special_territory_code.belongs(spicial_codeList))).select(db.sm_level.level_id, db.sm_level.level_name, db.sm_level.depot_id)    
                for levelSpecialRow in levelSpecialRows:
                    level_id = levelSpecialRow.level_id
                    level_name = levelSpecialRow.level_name
                    if level_id not in areaList:
                            areaList.append(level_id)
                        
                if cid=='IPINMD':
                    doctorRows = db((db.sm_doctor_temp.cid == cid) & (db.sm_doctor_temp.status != 'REJECTED')  & (db.sm_doctor_temp.nmd_route_id.belongs(areaList))   ).select(db.sm_doctor_temp.doc_id, db.sm_doctor_temp.doc_name, db.sm_doctor_temp.nmd_route_id, db.sm_doctor_temp.pharma_route_id,db.sm_doctor_temp.sin_route_id, orderby=db.sm_doctor_temp.doc_id)
                else:
                    doctorRows = db((db.sm_doctor_temp.cid == cid) & (db.sm_doctor_temp.status != 'REJECTED')  & (db.sm_doctor_temp.pharma_route_id.belongs(areaList))   ).select(db.sm_doctor_temp.doc_id, db.sm_doctor_temp.doc_name, db.sm_doctor_temp.nmd_route_id, db.sm_doctor_temp.pharma_route_id,db.sm_doctor_temp.sin_route_id, orderby=db.sm_doctor_temp.doc_id)
                 
                if not doctorRows:
                    rtn_str='Nothing pending for approval.'
    
                else:

                    rtn_str=' <table width="100%" border="0" cellspacing="0" cellpadding="0">'
                  
                    for doctorRow in doctorRows:
                        doctor_id = doctorRow.doc_id
                        doctor_name = doctorRow.doc_name
                        doctor_area_pharma = doctorRow.pharma_route_id
                        doctor_area_nmd = doctorRow.nmd_route_id
                        
                        if doctor_area_nmd=='':
                            doctor_area_nmd = doctorRow.sin_route_id
                        
                        rtn_str=rtn_str+' <tr  height="30px"> <td >'+str(doctor_name)+'|'+str(doctor_id)+'|'+str(doctor_area_pharma)+'|'+str(doctor_area_nmd)+' </td><td><img  width="50px;" height="50px" src="confirm.png"  onClick="confirmDoc('+str(doctor_id)+')"  alt=""></td></tr>'
                    rtn_str=rtn_str+'</table>'
#             return rtn_str
    return 'SUCCESS<SYNCDATA>'+rtn_str 

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
            docRow = db((db.sm_doctor_temp.cid == cid) & (db.sm_doctor_temp.doc_id == doc) ).select(db.sm_doctor_temp.ALL, limitby=(0, 1))
#             return db._lastsql
            dCaegory                =''
            dName                   =''
            dSpaciality             =''
            dMicrounion             =''
            dDegree                 =''
            attached_institution    =''
            service_kol_dsc         =''
            service_id              =''
            third_party_id          =''
            
            dDOB                    =''
            dMDay                   =''
            dMobile                 =''
            
            dCAddress               =''
            otherChamber            =''
            pharma_route            =''
            nmd_route               =''
            snv_route               =''
                       
            new_doc=''
            
            status               =''
            note               =''
            field1               =''
            
            rtn_str=''
            if docRow:  
                dCaegory                =docRow[0][db.sm_doctor_temp.doctors_category]
                dName                   =docRow[0][db.sm_doctor_temp.doc_name]
                dSpaciality             =docRow[0][db.sm_doctor_temp.specialty]
                dMicrounion             =docRow[0][db.sm_doctor_temp.microunion]
                dDegree                 =docRow[0][db.sm_doctor_temp.degree]
                attached_institution    =docRow[0][db.sm_doctor_temp.attached_institution]
                service_kol_dsc         =docRow[0][db.sm_doctor_temp.service_kol_dsc]
                service_id              =docRow[0][db.sm_doctor_temp.service_id]
                third_party_id          =docRow[0][db.sm_doctor_temp.third_party_id]
                
                dDOB                    =docRow[0][db.sm_doctor_temp.dob]
                dMDay                   =docRow[0][db.sm_doctor_temp.mar_day]
                dMobile                 =docRow[0][db.sm_doctor_temp.mobile]
                
                dCAddress               =docRow[0][db.sm_doctor_temp.note]
                otherChamber            =docRow[0][db.sm_doctor_temp.otherChamber]
                pharma_route            =docRow[0][db.sm_doctor_temp.pharma_route_id]
                nmd_route               =docRow[0][db.sm_doctor_temp.nmd_route_id]
                
                new_doc                 =docRow[0][db.sm_doctor_temp.new_doc]
                status                  =docRow[0][db.sm_doctor_temp.status]
                note                    =docRow[0][db.sm_doctor_temp.note]
                field1                  =docRow[0][db.sm_doctor_temp.field1]
                
                snv_route               =docRow[0][db.sm_doctor_temp.sin_route_id]
                
                
                
#                 dDist=docRow[0][db.sm_doctor_temp.district]
#                 dThana=docRow[0][db.sm_doctor_temp.thana]
                if dCaegory==None:
                    dCaegory=''
                if dName==None:
                    dName=''
                if dSpaciality==None:
                    dSpaciality=''
                if dMicrounion==None:
                    dMicrounion=''
                if dDegree==None:
                    dDegree=''
                if attached_institution==None:
                    attached_institution=''
                if service_kol_dsc==None:
                    service_kol_dsc=''
                if service_id==None:
                    service_id=''
                if third_party_id==None:
                    third_party_id=''
                if dDOB==None:
                    dDOB=''
                if dMDay==None:
                    dMDay=''
                if dMobile==None:
                    dMobile=''
                if dCAddress==None:
                    dCAddress=''
                if otherChamber==None:
                    otherChamber=''
                if pharma_route==None:
                    pharma_route=''
                if nmd_route==None:
                    nmd_route=''
                if new_doc==None:
                    new_doc=''
                if status==None:
                    status=''
                if note==None:
                    note=''
                
                rtn_str=str(dCaegory)+'<fdfd>'+str(dName)+'<fdfd>'+str(dSpaciality)+'<fdfd>'+str(dMicrounion)+'<fdfd>'+str(dDegree)+'<fdfd>'+str(attached_institution)+'<fdfd>'+str(service_kol_dsc)+'<fdfd>'+str(service_id)+'<fdfd>'+str(third_party_id)+'<fdfd>'+str(dDOB)+'<fdfd>'+str(dMDay)+'<fdfd>'+str(dMobile)+'<fdfd>'+str(dCAddress)+'<fdfd>'+str(otherChamber)+'<fdfd>'+str(pharma_route)+'<fdfd>'+str(nmd_route)+'<fdfd>'+str(new_doc)+'<fdfd>'+str(status)+'<fdfd>'+str(note)+'<fdfd>'+str(field1)+'<fdfd>'+str(snv_route)
#                 rtn_str=str(dName)+'<fdfd>'+str(dSpaciality)+'<fdfd>'+str(dDegree)+'<fdfd>'+str(dCaegory)+'<fdfd>'+str(dDOB)+'<fdfd>'+str(dMDay)+'<fdfd>'+str(dMobile)+'<fdfd>'+str(dCAddress)+'<fdfd>'+str(dDist)+'<fdfd>'+str(dThana)+'<fdfd>'+str(pharma_route)+'<fdfd>'+str(nmd_route)
             
    return 'SUCCESS<SYNCDATA>'+rtn_str 


def tourDocEntry():
    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.rep_pass).strip()
    synccode = str(request.vars.synccode).strip()
    
    tour_date = str(request.vars.tour_date).strip()
    tour_doc_str= str(request.vars.tour_doc_str).strip()
    submitStr=str(request.vars.submitStr).strip().decode("ascii", "ignore")
#     return submitStr
    repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.sync_code == synccode) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.rep_id, db.sm_rep.name, db.sm_rep.mobile_no, db.sm_rep.user_type, db.sm_rep.level_id, db.sm_rep.depot_id, limitby=(0, 1))
    if not repRow:
         return 'Invalid Authorization'
    
    else:
         userType=repRow[0].user_type
         rep_name=repRow[0].name
         compLevel = db((db.level_name_settings.cid == cid)).select(db.level_name_settings.depth ,orderby=~db.level_name_settings.depth, limitby=(0,1))
         for compLevel in compLevel:
           levelDepth=compLevel.depth
         

         if userType=="rep":
           userdepth=levelDepth
         elif userType=="sup":
           supDepthRow = db((db.sm_supervisor_level.cid == cid) & (db.sm_supervisor_level.sup_id == rep_id) ).select(db.sm_supervisor_level.level_id,db.sm_supervisor_level.level_depth_no ,orderby=db.sm_supervisor_level.level_id)
           if supDepthRow:
               userdepth=supDepthRow[0].level_depth_no
#            return leveldepth
#          return userdepth
         tour_docList = submitStr.split('<rd>')
         marketList=[]
         marketDict={}
         for i in range(len(tour_docList)):                                                                                                                                                                             
             marketId = tour_docList[i].split('<fd>')[1]
             marketName = tour_docList[i].split('<fd>')[2]
             tour_date = tour_docList[i].split('<fd>')[0]
             if len(marketId) > 0:
                 marketRows=db((db.sm_doctor_visit_plan.cid==cid) & (db.sm_doctor_visit_plan.rep_id==rep_id)&(db.sm_doctor_visit_plan.schedule_date==tour_date)&(db.sm_doctor_visit_plan.route_id==marketId)&(db.sm_doctor_visit_plan.status!='Cancelled')).select(db.sm_doctor_visit_plan.route_id,limitby=(0,1))
                 
                 if not marketRows:
#                      firstDate=str(tour_date)[0:8] + '01'
                     month=str(tour_date).split('-')[1]
                     if len(str(tour_date).split('-')[1])==1:
                         month='0'+str(tour_date).split('-')[1]
                     firstDate=str(tour_date).split('-')[0]+'-'+month+'-' + '01'
#                      return firstDate
                     marketDict={'cid':cid,'rep_id':rep_id,'rep_name':rep_name, 'first_date':firstDate,'schedule_date':tour_date,'route_id':marketId,'route_name':marketName,'status':'Submitted','field2':userdepth}
                     marketList.append(marketDict)
                 else:
                     return 'Alredy Exist'
#          return len(marketList)        
         if len(marketList)>0:
                db.sm_doctor_visit_plan.bulk_insert(marketList)
                cancellDelete=db((db.sm_doctor_visit_plan.cid==cid) & (db.sm_doctor_visit_plan.rep_id==rep_id)&(db.sm_doctor_visit_plan.status=='Cancelled')).delete()
#                 recordsRep_S="update sm_rep r, sm_doctor_visit_plan d  set  d.rep_name=r.name  WHERE d.cid=r.cid and d.rep_id=r.rep_id and d.rep_name='';"
#                 recordsRep=db.executesql(recordsRep_S)
                recordsLevel_S="update sm_doctor_visit_plan d, sm_level l  set  d.level2_id=l.level2,d.level2_name=l.level2_name,d.level1_id=l.level1,d.level1_name=l.level1_name,d.level0_id=l.level0,d.level0_name=l.level0_name,d.route_name=l.level_name WHERE d.cid=l.cid and d.route_id=l.level_id and d.route_name='';"
                recordsLevel=db.executesql(recordsLevel_S)
                return 'SUCCESS'
         else:
             return 'Alredy Exist'     

    
def tourPending():
    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.rep_pass).strip()
    synccode = str(request.vars.synccode).strip()
    
    
    repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.sync_code == synccode) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.rep_id, db.sm_rep.name, db.sm_rep.mobile_no, db.sm_rep.user_type, db.sm_rep.level_id, db.sm_rep.depot_id, limitby=(0, 1))
    
    if not repRow:
       return 'Invalid Authorization'

    else:
        userType=repRow[0][db.sm_rep.user_type]
        repStr=''
        if  userType=='rep':    
            supRepLevelRow=''
            import time
            today= time.strftime("%Y-%m-%d")            
            supRepRow = db((db.sm_doctor_visit_plan.cid == cid) & (db.sm_doctor_visit_plan.rep_id == rep_id) &  (db.sm_doctor_visit_plan.status != 'Cancelled') & (db.sm_doctor_visit_plan.schedule_date >= today)).select(db.sm_doctor_visit_plan.rep_id,db.sm_doctor_visit_plan.rep_name, groupby=db.sm_doctor_visit_plan.rep_id|db.sm_doctor_visit_plan.rep_name ,orderby=db.sm_doctor_visit_plan.rep_id|db.sm_doctor_visit_plan.rep_name)
    #         return supRepRow
            repStr=repStr+'<table style="border-color:#B1EBDF; border-style:solid" width="100%" border="1" cellspacing="0">'
                
            for supRepRow in supRepRow:
                rep_id=supRepRow.rep_id
                rep_name=supRepRow.rep_name
                rep_id_name=str(rep_name)+'|'+str(rep_id)
#                 repStr+='<li  style="border-bottom-style:solid; border-color:#CBE4E4;border-bottom-width:thin" ><input  type="submit" onClick="tourRepInfo(\''+rep_id+'\');"   style=" background-color:#09C; color:#FFF; font-size:12px; width:40px; height:30px;" value=" Info "    />&nbsp;&nbsp; <font id="'+ rep_id +'"  class="name" >'+ rep_id_name+'</font></li>'
                repStr=repStr+'<tr  height="30px"><td style="border-color:#B1EBDF; border-style:solid" onClick="tourRepInfo(\''+rep_id+'\')" >'
                repStr+='<font  id="'+ rep_id +'" class="name" >'+ rep_id_name+' | '+rep_id+'   </font>   </td></tr>'
                                     
            repStr=repStr+'</table>'
        
        if  userType=='sup':   
            compLevel = db((db.level_name_settings.cid == cid)).select(db.level_name_settings.depth ,orderby=~db.level_name_settings.depth, limitby=(0,1))
            for compLevel in compLevel:
                levelDepth=compLevel.depth
#             return levelDepth
            areaList=[]
            import time
            today = datetime.datetime.today()
            nextMonthDatetime = today + datetime.timedelta(days=(today.max.day - today.day)+1)
#             nextMonth=str(nextMonthDatetime).split(' ')[0][0:7]+'-01'
            month=str(nextMonthDatetime).split('-')[1]
            if len(str(nextMonthDatetime).split('-')[1])==1:
                 month='0'+str(nextMonthDatetime).split('-')[1]
                 
            nextMonth=str(nextMonthDatetime).split('-')[0]+'-'+month+'-' + '01'
            
#             return nextMonth
            supDepthRow = db((db.sm_supervisor_level.cid == cid) & (db.sm_supervisor_level.sup_id == rep_id) ).select(db.sm_supervisor_level.level_id,db.sm_supervisor_level.level_depth_no ,orderby=db.sm_supervisor_level.level_id)
#             return db._lastsql
            for supDepthRow in supDepthRow:
                areaList.append(supDepthRow.level_id)
            
            if len(areaList)>0:
                depth=supDepthRow.level_depth_no
                level='level'+str(depth)+'_id'
#                 return level
                marketList=[]
                supLevel='level'+str(depth)
                supARec=db((db.sm_level.cid == cid)& (db.sm_level.is_leaf == '1') & (db.sm_level[supLevel].belongs(areaList)) ).select(db.sm_level.level_id,orderby=db.sm_level.level_id)
#                 return supAList
                supAList=[]
                for supARec in supARec:
                    supAList.append(supARec.level_id)
                    marketList.append(supARec.level_id)
#              ====================Market   
#             marketList=[]
#             marketTourRows = db((db.sm_microunion.cid==cid) &(db.sm_microunion.area_id.belongs(supAList))).select(db.sm_microunion.microunion_id,db.sm_microunion.microunion_name, orderby=db.sm_microunion.microunion_name, groupby=db.sm_microunion.microunion_id|db.sm_microunion.microunion_name)
#             
#             for marketTourRow in marketTourRows:
#                 market_id =  marketTourRow.microunion_id
#                 marketList.append(market_id)
                
            if int(depth)==int(levelDepth)-1:
                supRepRow = db((db.sm_doctor_visit_plan.cid == cid) & (db.sm_doctor_visit_plan.route_id.belongs(marketList)) & (db.sm_doctor_visit_plan.status == 'Submitted') & ((db.sm_doctor_visit_plan.first_date == nextMonth) | (db.sm_doctor_visit_plan.first_date == first_currentDate)) & (db.sm_doctor_visit_plan.field2 > int(depth))).select(db.sm_doctor_visit_plan.rep_id,db.sm_doctor_visit_plan.rep_name,db.sm_doctor_visit_plan.status, groupby=db.sm_doctor_visit_plan.rep_id|db.sm_doctor_visit_plan.rep_name ,orderby=~db.sm_doctor_visit_plan.status|db.sm_doctor_visit_plan.rep_id|db.sm_doctor_visit_plan.rep_name)
            else:
                supRepRow = db((db.sm_doctor_visit_plan.cid == cid) & (db.sm_doctor_visit_plan.route_id.belongs(marketList)) & (db.sm_doctor_visit_plan.status == 'Submitted') & ((db.sm_doctor_visit_plan.first_date == nextMonth) | (db.sm_doctor_visit_plan.first_date == first_currentDate))  & (db.sm_doctor_visit_plan.field2 > int(depth))).select(db.sm_doctor_visit_plan.rep_id,db.sm_doctor_visit_plan.rep_name,db.sm_doctor_visit_plan.status, groupby=db.sm_doctor_visit_plan.rep_id|db.sm_doctor_visit_plan.rep_name ,orderby=~db.sm_doctor_visit_plan.status|db.sm_doctor_visit_plan.rep_id|db.sm_doctor_visit_plan.rep_name)
#                 supRepRow = db((db.sm_doctor_visit_plan.cid == cid) & (db.sm_doctor_visit_plan.route_id.belongs(marketList)) & (db.sm_doctor_visit_plan.status == 'ConfirmedASM') & (db.sm_doctor_visit_plan.first_date == nextMonth)).select(db.sm_doctor_visit_plan.rep_id,db.sm_doctor_visit_plan.rep_name,db.sm_doctor_visit_plan.status, groupby=db.sm_doctor_visit_plan.rep_id|db.sm_doctor_visit_plan.rep_name ,orderby=~db.sm_doctor_visit_plan.status|db.sm_doctor_visit_plan.rep_id|db.sm_doctor_visit_plan.rep_name)
#             return db._lastsql
            repStr=repStr+'<table style="border-color:#B1EBDF; border-style:solid" width="100%" border="1" cellspacing="0">'
#             return     supRepRow
            
            for supRepRow in supRepRow:
                
                rep_id_plan=supRepRow.rep_id
                rep_name_plan=supRepRow.rep_name
                status_plan=supRepRow.status
                rep_id_name=str(rep_name_plan)+'|'+str(rep_id_plan)
                
                
                
                if status_plan!='Submitted':
#                     path_value_tour='http://127.0.0.1:8000/kpl/tour_web/'
                    path_value_tour='http://w05.yeapps.com/kpl/tour_web/'
                    linkPath="window.open('"+path_value_tour+"tourShowSup_web?"+"cid="+cid+"&rep_id="+rep_id_plan+"', '_system');"
                    
                    
#                     repStr=repStr+'<tr  height="30px"><td style="border-color:#B1EBDF; border-style:solid" onClick="repPendingDoc(\''+rep_id_plan+'\')" >'
                    repStr=repStr+'<tr  height="30px"><td style="border-color:#B1EBDF; border-style:solid" >'
                    repStr+='<font onclick="'+linkPath+'" style="color:#900" id="'+ rep_id_plan +'" class="name" >'+ rep_name_plan+' | '+rep_id_plan+'   *</font>   </td></tr>'
                                 
            repStr=repStr+'</table>'
#             return repStr
            repStr=repStr+'<br><table style="border-color:#B1EBDF; border-style:solid"  width="100%" border="1" cellspacing="0">'
            supRepLevelRow = db((db.sm_rep_area.cid == cid) & (db.sm_rep_area.area_id.belongs(supAList)) ).select(db.sm_rep_area.rep_id,db.sm_rep_area.rep_name, groupby=db.sm_rep_area.rep_id|db.sm_rep_area.rep_name ,orderby=db.sm_rep_area.rep_id|db.sm_rep_area.rep_name)
#                 return supRepLevelRow
            for supRepLevelRow in supRepLevelRow:
                rep_id_RepArea=supRepLevelRow.rep_id
                rep_name_RepArea=supRepLevelRow.rep_name
                repStr=repStr+'<tr  height="30px" ><td style="border-color:#B1EBDF; border-style:solid" onClick="tourRepInfo(\''+rep_id_RepArea+'\')">'
                repStr+='<font id="'+ rep_id_RepArea +'"   class="name" >'+ rep_name_RepArea+' | '+ rep_id_RepArea+'</font> </td></tr>'
                
            repStr=repStr+'</table>'    
        if supRepLevelRow or supRepRow:
            return '</START>'+'SUCCESS<SYNCDATA>'+str(repStr)+'</END>'
        else:
            return '</START>'+'FAILED<SYNCDATA>Pending not availabe</END>'
            

def repPendingDoc():
    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.rep_pass).strip()
    synccode = str(request.vars.synccode).strip()
    rep_id_pending=str(request.vars.rep_id_pending).strip()
    
    repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.sync_code == synccode) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.rep_id, db.sm_rep.name, db.sm_rep.mobile_no, db.sm_rep.user_type, db.sm_rep.level_id, db.sm_rep.depot_id, limitby=(0, 1))
    import time
    if not repRow:
       return 'Invalid Authorization'

    else:
        userType=repRow[0][db.sm_rep.user_type]

    import datetime
    today = datetime.datetime.today()
    nextMonthDatetime = today + datetime.timedelta(days=(today.max.day - today.day)+1)
#     nextMonth=str(nextMonthDatetime).split(' ')[0][0:7]+'-01'
    month=str(nextMonthDatetime).split('-')[1]
    if len(str(nextMonthDatetime).split('-')[1])==1:
         month='0'+str(nextMonthDatetime).split('-')[1]
    nextMonth=str(nextMonthDatetime).split('-')[0]+'-'+month+'-' + '01'
    
    
    
    
#     return nextMonth
    docTThisMonthRow=db((db.sm_doctor_visit_plan.cid == cid) & (db.sm_doctor_visit_plan.rep_id == rep_id_pending)  & (db.sm_doctor_visit_plan.first_date == nextMonth)).select(db.sm_doctor_visit_plan.route_id,db.sm_doctor_visit_plan.route_name,db.sm_doctor_visit_plan.schedule_date,db.sm_doctor_visit_plan.status, groupby=db.sm_doctor_visit_plan.schedule_date|db.sm_doctor_visit_plan.route_id, orderby=db.sm_doctor_visit_plan.schedule_date|db.sm_doctor_visit_plan.route_name)
#     return db._lastsql
#     return docTThisMonthRow
    marketStrDocThisMonth=''
    srart_d_flag=0
    docTThisMonthRowFlag=0
    pastSchDate=''
    for docTThisMonthRow in docTThisMonthRow:
        route_id = docTThisMonthRow.route_id
        route_name = docTThisMonthRow.route_name
        schedule_date = docTThisMonthRow.schedule_date
        status=docTThisMonthRow.status
        
        if (str(pastSchDate)!=str(schedule_date)):
            if (srart_d_flag==0):
                marketStrDocThisMonth="<"+str(schedule_date)+">"
            else:
                marketStrDocThisMonth=marketStrDocThisMonth+"</"+str(pastSchDate)+">"+"<"+str(schedule_date)+">"
                srart_d_flag=0
        if srart_d_flag == 0:
            marketStrDocThisMonth = marketStrDocThisMonth+str(route_id) + '<fd>' + str(route_name)+ '<fd>' + str(status)
            srart_d_flag=1
        else:
            marketStrDocThisMonth = marketStrDocThisMonth+'<rd>' + str(route_id) + '<fd>' + str(route_name)+ '<fd>' + str(status)
        pastSchDate=schedule_date
        srart_d_flag=1


    if marketStrDocThisMonth!='':
        return '</START>'+'SUCCESS<SYNCDATA>'+str(marketStrDocThisMonth)+'</END>'
    else:
        return '</START>'+'FAILED<SYNCDATA>Pending not availabe</END>'
        
def tourConfirm_doc():
    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.rep_pass).strip()
    synccode = str(request.vars.synccode).strip()

    pendingRep= str(request.vars.pendingRep).strip()

    repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.sync_code == synccode) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.rep_id, db.sm_rep.name, db.sm_rep.mobile_no, db.sm_rep.user_type, db.sm_rep.level_id, db.sm_rep.depot_id, limitby=(0, 1))
#     return repRow
    if not repRow:
         return 'Invalid Authorization'
    
    else:
        compLevel = db((db.level_name_settings.cid == cid)).select(db.level_name_settings.depth ,orderby=~db.level_name_settings.depth, limitby=(0,1))
        for compLevel in compLevel:
            levelDepth=compLevel.depth
        supDepthRow = db((db.sm_supervisor_level.cid == cid) & (db.sm_supervisor_level.sup_id == rep_id) ).select(db.sm_supervisor_level.level_id,db.sm_supervisor_level.level_depth_no ,orderby=db.sm_supervisor_level.level_id)
        areaList=[]
        for supDepthRow in supDepthRow:
            areaList.append(supDepthRow.level_id)
        if len(areaList)>0:
            depth=supDepthRow.level_depth_no    
            
        import datetime
        today = datetime.datetime.today()
        nextMonthDatetime = today + datetime.timedelta(days=(today.max.day - today.day)+1)
#         nextMonth=str(nextMonthDatetime).split(' ')[0][0:7]+'-01'
        month=str(nextMonthDatetime).split('-')[1]
        if len(str(nextMonthDatetime).split('-')[1])==1:
             month='0'+str(nextMonthDatetime).split('-')[1]
        nextMonth=str(nextMonthDatetime).split('-')[0]+'-'+month+'-' + '01'
        
        
        if int(depth)==int(levelDepth)-1:
#             docTThisMonthRow=db((db.sm_doctor_visit_plan.cid == cid) & (db.sm_doctor_visit_plan.rep_id == pendingRep)  & (db.sm_doctor_visit_plan.first_date == nextMonth)).update(status='ConfirmedASM')
            docTThisMonthRow=db((db.sm_doctor_visit_plan.cid == cid) & (db.sm_doctor_visit_plan.rep_id == pendingRep)  & (db.sm_doctor_visit_plan.first_date == nextMonth)).update(status='Confirmed')
        else:
            docTThisMonthRow=db((db.sm_doctor_visit_plan.cid == cid) & (db.sm_doctor_visit_plan.rep_id == pendingRep)  & (db.sm_doctor_visit_plan.first_date == nextMonth)).update(status='Confirmed')
        #     return db._lastsql
                
        if docTThisMonthRow:
        #              db((db.sm_doctor_visit_plan.cid == cid) & (db.sm_doctor_visit_plan.id.belongs(marketList))).update(status='Confirmed')  
            return 'SUCCESS'
        else:
            return 'FAILED' 
         
         
def tourCancel_doc():
    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.rep_pass).strip()
    synccode = str(request.vars.synccode).strip()

    pendingRep= str(request.vars.pendingRep).strip()
#     return tour_route_str
    repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.sync_code == synccode) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.rep_id, db.sm_rep.name, db.sm_rep.mobile_no, db.sm_rep.user_type, db.sm_rep.level_id, db.sm_rep.depot_id, limitby=(0, 1))
    if not repRow:
        return 'Invalid Authorization'
    
    else:
        compLevel = db((db.level_name_settings.cid == cid)).select(db.level_name_settings.depth ,orderby=~db.level_name_settings.depth, limitby=(0,1))
        for compLevel in compLevel:
            levelDepth=compLevel.depth
        supDepthRow = db((db.sm_supervisor_level.cid == cid) & (db.sm_supervisor_level.sup_id == rep_id) ).select(db.sm_supervisor_level.level_id,db.sm_supervisor_level.level_depth_no ,orderby=db.sm_supervisor_level.level_id)
        areaList=[]
        for supDepthRow in supDepthRow:
            areaList.append(supDepthRow.level_id)
        if len(areaList)>0:
            depth=supDepthRow.level_depth_no
            
        rep_name=str(repRow[0].name)
        import datetime
        today = datetime.datetime.today()
        nextMonthDatetime = today + datetime.timedelta(days=(today.max.day - today.day)+1)
#         nextMonth=str(nextMonthDatetime).split(' ')[0][0:7]+'-01'
        month=str(nextMonthDatetime).split('-')[1]
        if len(str(nextMonthDatetime).split('-')[1])==1:
             month='0'+str(nextMonthDatetime).split('-')[1]
        nextMonth=str(nextMonthDatetime).split('-')[0]+'-'+month+'-' + '01'
        
        if int(depth)==int(levelDepth)-1:
            docTThisMonthRow=db((db.sm_doctor_visit_plan.cid == cid) & (db.sm_doctor_visit_plan.rep_id == pendingRep)  & (db.sm_doctor_visit_plan.first_date == nextMonth)).update(status='Cancelled')
        else:
            docTThisMonthRow=db((db.sm_doctor_visit_plan.cid == cid) & (db.sm_doctor_visit_plan.rep_id == pendingRep)  & (db.sm_doctor_visit_plan.first_date == nextMonth)).update(status='Cancelled')
            
                
        if docTThisMonthRow:
            msg ='Request Cancelled Please check'
            msg_insert=db.sm_msg_box.insert(cid=cid,msg_date=current_date,msg_from=rep_id,msgFromName=rep_name,msg_to=pendingRep,msg=msg,    status='Active')  
            return 'SUCCESS'
        else:
            return 'FAILED'
         
         
# ==============================================        
def repPendingDocShow():
    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.rep_pass).strip()
    synccode = str(request.vars.synccode).strip()
    rep_id_pending=rep_id
    
    repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.sync_code == synccode) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.rep_id, db.sm_rep.name, db.sm_rep.mobile_no, db.sm_rep.user_type, db.sm_rep.level_id, db.sm_rep.depot_id, limitby=(0, 1))
    visitPlanMarketComb=''
    if not repRow:
        return 'Invalid Authorization'

    else:             
        today= time.strftime("%Y-%m-%d")      
        recRow = db((db.sm_doctor_visit_plan.cid == cid) & (db.sm_doctor_visit_plan.rep_id == rep_id_pending) & (db.sm_doctor_visit_plan.schedule_date >= today)  ).select(db.sm_doctor_visit_plan.id,db.sm_doctor_visit_plan.route_id,db.sm_doctor_visit_plan.route_name,db.sm_doctor_visit_plan.schedule_date,db.sm_doctor_visit_plan.status,db.sm_doctor_visit_plan.field1, groupby=db.sm_doctor_visit_plan.route_id|db.sm_doctor_visit_plan.route_name|db.sm_doctor_visit_plan.schedule_date ,orderby=db.sm_doctor_visit_plan.schedule_date|db.sm_doctor_visit_plan.route_id|db.sm_doctor_visit_plan.route_name)
#         return db._lastsql
        visitPlanMarketComb='<br><table style="border-style:solid; border-width:thin; border-color:#096" width="100%" border="1" cellspacing="0">'
        for recRow in recRow:
            id=str(recRow.id)
            route_id=recRow.route_id
            route_name=recRow.route_name
            schedule_date_1=recRow.schedule_date
            schedule_date=schedule_date_1.strftime('%d, %b')
            status=recRow.status
            mainStr=str(schedule_date)+' | '+str(route_name)+' | '+str(route_id)
            submitStr=str(route_id)+ ' | '+str(schedule_date)
            if (status=='Submitted'):
                visitPlanMarketComb=visitPlanMarketComb+'<tr height="30px"><td width="60px">'+str(schedule_date)+'<td>'+str(route_name)+' | '+str(route_id)+'</td><td width="40px"><input  type="submit" onClick="tourDelete_doc(\''+id+'\');"   style=" background-color:#09C; color:#FFF; font-size:12px; width:40px; height:30px;" value=" X "    /></td></tr>'
            if (status=='Confirmed'):
                visitPlanMarketComb=visitPlanMarketComb+'<tr height="30px" style="background-color:#E6FFF2"><td width="60px">'+str(schedule_date)+'<td colspan="2">'+str(route_name)+' | '+str(route_id)+'</td></tr>'
            if (status=='Cancelled'):
                visitPlanMarketComb=visitPlanMarketComb+'<tr height="30px" style="background-color:#FAEFED"><td width="60px">'+str(schedule_date)+'<td colspan="2">'+str(route_name)+' | '+str(route_id)+'</td></tr>'
            
#             '<li  style="border-bottom-style:solid; border-color:#CBE4E4;border-bottom-width:thin" > '+'<table width="100%" border="0" cellpadding="0" cellspacing="0" style="border-radius:5px;">'+'<tr style="border-bottom:1px solid #D2EEE9;"><td width="60px" style="text-align:center; padding-left:5px;"><input  type="submit" onClick="tourDelete_doc(\''+id+'\');"   style=" background-color:#09C; color:#FFF; font-size:20px" value=" X "   /></td><td  style="text-align:left;" </br><font id="'+ id +'"  class="name" >'+ mainStr+'</font></td></tr>'+'</table>'+'</li>'
            
        visitPlanMarketComb=visitPlanMarketComb+'</table>'
        if visitPlanMarketComb!='':
            return '</START>'+'SUCCESS<SYNCDATA>'+str(visitPlanMarketComb)+'</END>'
        else:
            return '</START>'+'FAILED<SYNCDATA>Pending not availabe</END>'     
        

  
def tourCReq_doc():
    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.rep_pass).strip()
    synccode = str(request.vars.synccode).strip()
    
    submitStrGet=str(request.vars.submitStr).strip().decode("ascii", "ignore")
#     checkLeave=str(request.vars.checkLeave).strip()
#     checkOthers=str(request.vars.checkOthers).strip()
#     return submitStrGet
   
    repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.sync_code == synccode) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.rep_id, db.sm_rep.name, db.sm_rep.mobile_no, db.sm_rep.user_type, db.sm_rep.level_id, db.sm_rep.depot_id, limitby=(0, 1))
    visitPlanMarketComb=''
    if not repRow:
        return '</START>'+'SUCCESS<SYNCDATA>'+'Invalid Authorization'+'</END>'

    else:  
        userType=repRow[0].user_type
        rep_name=repRow[0].name
        compLevel = db((db.level_name_settings.cid == cid)).select(db.level_name_settings.depth ,orderby=~db.level_name_settings.depth, limitby=(0,1))
        for compLevel in compLevel:
           levelDepth=compLevel.depth
         

        if userType=="rep":
           userdepth=levelDepth
        elif userType=="sup":
            supDepthRow = db((db.sm_supervisor_level.cid == cid) & (db.sm_supervisor_level.sup_id == rep_id) ).select(db.sm_supervisor_level.level_id,db.sm_supervisor_level.level_depth_no ,orderby=db.sm_supervisor_level.level_id)
            if supDepthRow:
                userdepth=supDepthRow[0].level_depth_no
               
        if submitStrGet!='':
            reqDate=submitStrGet.split('<date>')[0]
            submitStr=submitStrGet.split('<date>')[1]
            
            chechRow=db((db.sm_doctor_visit_plan.cid == cid) & (db.sm_doctor_visit_plan.rep_id == rep_id)& (db.sm_doctor_visit_plan.schedule_date == reqDate) & (db.sm_doctor_visit_plan.status == 'Submitted')).select(db.sm_doctor_visit_plan.schedule_date)     
#             return chechRow
            if chechRow:    
                return '</START>'+'SUCCESS<SYNCDATA>'+'Allready Submitted'+'</END>'
#             return 'Test'
            marketList=[]
            marketDict={}
#             return submitStr
            if (submitStr!=''):
                tour_docList = submitStr.split('<rd>')
                
                for i in range(len(tour_docList)):                                                                                                                                                                             
                    marketId = tour_docList[i].split('<fd>')[0]
                    marketName = tour_docList[i].split('<fd>')[1]
                    tour_date = reqDate
                    if len(marketId) > 0:
#                             firstDate=str(tour_date)[0:8] + '01'
                            month=str(tour_date).split('-')[1]
                            if len(str(tour_date).split('-')[1])==1:
                                 month='0'+str(tour_date).split('-')[1]
                            firstDate=str(tour_date).split('-')[0]+'-'+month+'-' + '01'
                            marketDict={'cid':cid,'rep_id':rep_id,'rep_name':rep_name, 'first_date':firstDate,'schedule_date':tour_date,'route_id':marketId,'route_name':marketName,'status':'CReq','field2':userdepth}
                            marketList.append(marketDict)
                    
            if len(marketList)>0:
                   db.sm_doctor_visit_plan.bulk_insert(marketList)
                   recordsRep_S="update sm_rep r, sm_doctor_visit_plan d  set  d.rep_name=r.name  WHERE d.cid=r.cid and d.rep_id=r.rep_id and d.rep_name='';"
                   recordsRep=db.executesql(recordsRep_S)
                   
            return '</START>'+'SUCCESS<SYNCDATA>'+'Submitted Successfully'+'</END>'
            
        
def tourDelete_doc():
    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.rep_pass).strip()
    synccode = str(request.vars.synccode).strip()

    tour_id= str(request.vars.tour_id).strip()
#     return tour_id
    repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.sync_code == synccode) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.rep_id, db.sm_rep.name, db.sm_rep.mobile_no, db.sm_rep.user_type, db.sm_rep.level_id, db.sm_rep.depot_id, limitby=(0, 1))
    
    if not repRow:
         return 'Invalid Authorization'
    
    else:
        db((db.sm_doctor_visit_plan.cid == cid) & (db.sm_doctor_visit_plan.id == tour_id) ).delete()
#         return db._lastsql
        return 'SUCCESS'

 


def repPendingCancel():
    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.rep_pass).strip()
    synccode = str(request.vars.synccode).strip()
    rep_id_pending=str(request.vars.rep_id_pending).strip()
    
    repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.sync_code == synccode) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.rep_id, db.sm_rep.name, db.sm_rep.mobile_no, db.sm_rep.user_type, db.sm_rep.level_id, db.sm_rep.depot_id, limitby=(0, 1))
    import time
    if not repRow:
       return 'Invalid Authorization'

    else:
        userType=repRow[0][db.sm_rep.user_type]
        repStr=''
#         if  userType=='rep':   
#             
#             today= time.strftime("%Y-%m-%d")          
#             recRow = db((db.sm_doctor_visit_plan.cid == cid) & (db.sm_doctor_visit_plan.rep_id == rep_id) & (db.sm_doctor_visit_plan.status == 'Submitted') & (db.sm_doctor_visit_plan.schedule_date >= today)).select(db.sm_doctor_visit_plan.id,db.sm_doctor_visit_plan.route_id,db.sm_doctor_visit_plan.route_name,db.sm_doctor_visit_plan.schedule_date, groupby=db.sm_doctor_visit_plan.route_id|db.sm_doctor_visit_plan.route_name|db.sm_doctor_visit_plan.schedule_date ,orderby=db.sm_doctor_visit_plan.schedule_date|db.sm_doctor_visit_plan.route_id|db.sm_doctor_visit_plan.route_name)
#             #         return supRepRow
#             for recRow in recRow:
#                 id=recRow.id
#                 route_id=recRow.route_id
#                 route_name=recRow.route_name
#                 schedule_date=recRow.schedule_date
#                 mainStr=str(route_name)+'|'+str(route_id)+ ' | '+str(schedule_date)
#                 submitStr=str(route_id)+ ' | '+str(schedule_date)
#                 visitPlanMarketComb+='<li  style="border-bottom-style:solid; border-color:#CBE4E4;border-bottom-width:thin" onClick="check_boxTourTrue(\''+submitStr+'\')"> '+'<table width="100%" border="0" id="order_tbl" cellpadding="0" cellspacing="0" style="border-radius:5px;">'+'<tr style="border-bottom:1px solid #D2EEE9;"><td  style="text-align:left;">'+'</br><font id="'+ submitStr +'" onClick="check_boxTourTrue(\''+submitStr+'\')" class="name" >'+ mainStr+'</font></td></tr>'+'</table>'+'</li>'
            
        if  userType=='sup':    
            areaList=[]
            import time
            today= time.strftime("%Y-%m-%d")
            supDepthRow = db((db.sm_supervisor_level.cid == cid) & (db.sm_supervisor_level.sup_id == rep_id) ).select(db.sm_supervisor_level.level_id,db.sm_supervisor_level.level_depth_no ,orderby=db.sm_supervisor_level.level_id)
#             return db._lastsql
            for supDepthRow in supDepthRow:
                areaList.append(supDepthRow.level_id)
            
            if len(areaList)>0:
                depth=supDepthRow.level_depth_no
                level='level'+str(depth)+'_id'
#                 return level
                today= time.strftime("%Y-%m-%d")  
                
                supLevel='level'+str(depth)
                supARec=db((db.sm_level.cid == cid)& (db.sm_level.is_leaf == '1') & (db.sm_level[supLevel].belongs(areaList)) ).select(db.sm_level.level_id,orderby=db.sm_level.level_id)
#                 return supAList
                supAList=[]
                for supARec in supARec:
                    supAList.append(supARec.level_id)
#              ====================Market   
            marketList=[]
            marketTourRows = db((db.sm_microunion.cid==cid) &(db.sm_microunion.area_id.belongs(supAList))).select(db.sm_microunion.microunion_id,db.sm_microunion.microunion_name, orderby=db.sm_microunion.microunion_name, groupby=db.sm_microunion.microunion_id)
#                 return db._lastsql
            for marketTourRow in marketTourRows:
                market_id =  marketTourRow.microunion_id
                marketList.append(market_id)
                
                
#                 supRepRow = db((db.sm_doctor_visit_plan.cid == cid) & (db.sm_doctor_visit_plan.route_id.belongs(marketList)) & (db.sm_doctor_visit_plan.status == 'CReq') & (db.sm_doctor_visit_plan.schedule_date >= today)).select(db.sm_doctor_visit_plan.rep_id,db.sm_doctor_visit_plan.rep_name,db.sm_doctor_visit_plan.status, groupby=db.sm_doctor_visit_plan.rep_id|db.sm_doctor_visit_plan.rep_name ,orderby=~db.sm_doctor_visit_plan.status|db.sm_doctor_visit_plan.rep_id|db.sm_doctor_visit_plan.rep_name)
#                 return db._lastsql
                
                
                supRepRow = db((db.sm_doctor_visit_plan.cid == cid) & (db.sm_doctor_visit_plan.route_id.belongs(marketList)) & (db.sm_doctor_visit_plan.status == 'CReq') & (db.sm_doctor_visit_plan.schedule_date >= today)).select(db.sm_doctor_visit_plan.rep_id,db.sm_doctor_visit_plan.rep_name,db.sm_doctor_visit_plan.status, groupby=db.sm_doctor_visit_plan.rep_id|db.sm_doctor_visit_plan.rep_name ,orderby=~db.sm_doctor_visit_plan.status|db.sm_doctor_visit_plan.rep_id|db.sm_doctor_visit_plan.rep_name)
#                 return db._lastsql
                
                for supRepRow in supRepRow:
                    rep_id=supRepRow.rep_id
                    rep_name=supRepRow.rep_name
                    status=supRepRow.status
                    rep_id_name=str(rep_name)+'|'+str(rep_id)

                    repStr+='<li  style="border-bottom-style:solid; border-color:#CBE4E4;border-bottom-width:thin" > <font id="sup_'+ rep_id +'" onClick="repCancelReq_sup(\''+rep_id+'\')" class="name" >'+ rep_name+' | '+rep_id+'   </font>   </li>'

         
        if repStr!='':
            return '</START>'+'SUCCESS<SYNCDATA>'+str(repStr)+'</END>'
        else:
            return '</START>'+'FAILED<SYNCDATA>Pending not availabe</END>'



def repCancelReq_sup():
    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.rep_pass).strip()
    synccode = str(request.vars.synccode).strip()
    rep_id_pending=str(request.vars.rep_id_pending).strip()
    
    repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.sync_code == synccode) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.rep_id, db.sm_rep.name, db.sm_rep.mobile_no, db.sm_rep.user_type, db.sm_rep.level_id, db.sm_rep.depot_id, limitby=(0, 1))
    import time
    if not repRow:
       return 'Invalid Authorization'

    else:
        userType=repRow[0][db.sm_rep.user_type]
        repStr=''

        if  userType=='sup': 
            compLevel = db((db.level_name_settings.cid == cid)).select(db.level_name_settings.depth ,orderby=~db.level_name_settings.depth, limitby=(0,1))
            for compLevel in compLevel:
                levelDepth=compLevel.depth

            supDepthRow = db((db.sm_supervisor_level.cid == cid) & (db.sm_supervisor_level.sup_id == rep_id) ).select(db.sm_supervisor_level.level_id,db.sm_supervisor_level.level_depth_no ,orderby=db.sm_supervisor_level.level_id)
            areaList=[]
            for supDepthRow in supDepthRow:
                areaList.append(supDepthRow.level_id)            
            if len(areaList)>0:
                depth=supDepthRow.level_depth_no

            import time
            today= time.strftime("%Y-%m-%d")
            if int(depth)==int(levelDepth)-1:
                supRepRow = db((db.sm_doctor_visit_plan.cid == cid) & (db.sm_doctor_visit_plan.rep_id==rep_id_pending) & (db.sm_doctor_visit_plan.status == 'CReq') & (db.sm_doctor_visit_plan.schedule_date >= today)).select(db.sm_doctor_visit_plan.id,db.sm_doctor_visit_plan.schedule_date,db.sm_doctor_visit_plan.route_id,db.sm_doctor_visit_plan.route_name,db.sm_doctor_visit_plan.field1, groupby=db.sm_doctor_visit_plan.rep_id|db.sm_doctor_visit_plan.rep_name|db.sm_doctor_visit_plan.schedule_date ,orderby=~db.sm_doctor_visit_plan.status|db.sm_doctor_visit_plan.rep_id|db.sm_doctor_visit_plan.rep_name)
            else:
#                 supRepRow = db((db.sm_doctor_visit_plan.cid == cid) & (db.sm_doctor_visit_plan.rep_id==rep_id_pending) & (db.sm_doctor_visit_plan.status == 'CReqASM') & (db.sm_doctor_visit_plan.schedule_date >= today)).select(db.sm_doctor_visit_plan.id,db.sm_doctor_visit_plan.schedule_date,db.sm_doctor_visit_plan.route_id,db.sm_doctor_visit_plan.route_name,db.sm_doctor_visit_plan.field1, groupby=db.sm_doctor_visit_plan.rep_id|db.sm_doctor_visit_plan.rep_name|db.sm_doctor_visit_plan.schedule_date ,orderby=~db.sm_doctor_visit_plan.status|db.sm_doctor_visit_plan.rep_id|db.sm_doctor_visit_plan.rep_name)
                supRepRow = db((db.sm_doctor_visit_plan.cid == cid) & (db.sm_doctor_visit_plan.rep_id==rep_id_pending) & (db.sm_doctor_visit_plan.status == 'CReq') & (db.sm_doctor_visit_plan.schedule_date >= today)).select(db.sm_doctor_visit_plan.id,db.sm_doctor_visit_plan.schedule_date,db.sm_doctor_visit_plan.route_id,db.sm_doctor_visit_plan.route_name,db.sm_doctor_visit_plan.field1, groupby=db.sm_doctor_visit_plan.rep_id|db.sm_doctor_visit_plan.rep_name|db.sm_doctor_visit_plan.schedule_date ,orderby=~db.sm_doctor_visit_plan.status|db.sm_doctor_visit_plan.rep_id|db.sm_doctor_visit_plan.rep_name)
                
#             return supRepRow    
            repStr='<table style="border-style:solid; border-width:thin; border-color:#096" width="100%" border="1" cellspacing="0">'
            amndPlan=''
            schedule_date_past=''
            for supRepRow in supRepRow:
                id=str(supRepRow.id)
                route_id=supRepRow.route_id
                route_name=supRepRow.route_name
                schedule_date_1=supRepRow.schedule_date
                reson=supRepRow.field1
                schedule_date=schedule_date_1.strftime('%d, %b')
                amndPlan=amndPlan+'<br>'+str(route_name)+' | '+str(route_id)
                appRow = db((db.sm_doctor_visit_plan.cid == cid) & (db.sm_doctor_visit_plan.rep_id==rep_id_pending) & (db.sm_doctor_visit_plan.status == 'Confirmed') & (db.sm_doctor_visit_plan.schedule_date == schedule_date_1)).select(db.sm_doctor_visit_plan.id,db.sm_doctor_visit_plan.schedule_date,db.sm_doctor_visit_plan.route_id,db.sm_doctor_visit_plan.route_name,db.sm_doctor_visit_plan.field1, orderby=~db.sm_doctor_visit_plan.status|db.sm_doctor_visit_plan.rep_id|db.sm_doctor_visit_plan.rep_name)
#                 return db._lastsql
                appPlan=''
                for appRow in appRow:
                    route_idApp=appRow.route_id
                    route_nameApp=appRow.route_name
                    appPlan=appPlan+'<br>'+str(route_nameApp)+' | '+str(route_idApp)
                if appPlan=='':
                    appPlan='-'
                if ((schedule_date_1!=schedule_date_past) ):    
                    repStr+='<tr height="30px"><td width="60px"><font style="font-size:18px; color:#00ABFD"> '+str(schedule_date)+'</font><br>'
                
                
                schedule_date_past=schedule_date_1
                
                repStr+='<font style="font-size:16px; color:#900"> ApprovedPlan:</font>'+str(appPlan)+'<br><font style="font-size:16px; color:#900">AmendmentRequest:</font>'+str(amndPlan)+'<br><br><input  type="submit" onClick="tourCReq_done(\''+id+'\');"   style=" background-color:#09C; color:#FFF; font-size:12px;  height:30px;" value=" Approve "    />&nbsp;&nbsp;<input  type="submit" onClick="tourCReq_reject(\''+id+'\');"   style=" background-color:#09C; color:#FFF; font-size:12px;  height:30px;" value="   Reject   "    /><br><br></td></tr>'
            repStr=repStr+'</table>'
         
        if repStr!='':
            return '</START>'+'SUCCESS<SYNCDATA>'+str(repStr)+'</END>'
        else:
            return '</START>'+'FAILED<SYNCDATA>Pending not availabe</END>' 


def tourCReq_done():
    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.rep_pass).strip()
    synccode = str(request.vars.synccode).strip()
    rep_id_pending=str(request.vars.rep_id_pending).strip()
    rowId=str(request.vars.rowId).strip()
    
    repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.sync_code == synccode) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.rep_id, db.sm_rep.name, db.sm_rep.mobile_no, db.sm_rep.user_type, db.sm_rep.level_id, db.sm_rep.depot_id, limitby=(0, 1))
    import time
    if not repRow:
       return 'Invalid Authorization'

    else:
        
        
        userType=repRow[0][db.sm_rep.user_type]
        repStr=''   
        if  userType=='sup': 
#             deleteRows = db((db.sm_doctor_visit_plan.cid == cid) & (db.sm_doctor_visit_plan.id == rowId)).delete()   
           
            compLevel = db((db.level_name_settings.cid == cid)).select(db.level_name_settings.depth ,orderby=~db.level_name_settings.depth, limitby=(0,1))
            for compLevel in compLevel:
                levelDepth=compLevel.depth

            supDepthRow = db((db.sm_supervisor_level.cid == cid) & (db.sm_supervisor_level.sup_id == rep_id) ).select(db.sm_supervisor_level.level_id,db.sm_supervisor_level.level_depth_no ,orderby=db.sm_supervisor_level.level_id)
            areaList=[]
            for supDepthRow in supDepthRow:
                areaList.append(supDepthRow.level_id)            
            if len(areaList)>0:
                depth=supDepthRow.level_depth_no

            import time
            today= time.strftime("%Y-%m-%d")
            
            
            checkRow = db((db.sm_doctor_visit_plan.cid == cid) & (db.sm_doctor_visit_plan.id == rowId)).select(db.sm_doctor_visit_plan.id,db.sm_doctor_visit_plan.schedule_date,db.sm_doctor_visit_plan.rep_id,limitby=(0,1))
#             return checkRow
            amndDate=''
            if checkRow:
                amndDate=checkRow[0].schedule_date
#             return amndDate
            if int(depth)==int(levelDepth)-1:
                supRepRow = db((db.sm_doctor_visit_plan.cid == cid) & (db.sm_doctor_visit_plan.rep_id==rep_id_pending) & (db.sm_doctor_visit_plan.status == 'Confirmed') & (db.sm_doctor_visit_plan.schedule_date == amndDate)).delete()
                supRepRow = db((db.sm_doctor_visit_plan.cid == cid) & (db.sm_doctor_visit_plan.rep_id==rep_id_pending) & (db.sm_doctor_visit_plan.status == 'CReq') & (db.sm_doctor_visit_plan.schedule_date == amndDate)).update(status='Confirmed')
#                 supRepRow = db((db.sm_doctor_visit_plan.cid == cid) & (db.sm_doctor_visit_plan.rep_id==rep_id_pending) & (db.sm_doctor_visit_plan.status == 'CReq') & (db.sm_doctor_visit_plan.schedule_date == amndDate)).update(status='CReqASM')
            else:
                supRepRow = db((db.sm_doctor_visit_plan.cid == cid) & (db.sm_doctor_visit_plan.rep_id==rep_id_pending) & (db.sm_doctor_visit_plan.status == 'Confirmed') & (db.sm_doctor_visit_plan.schedule_date == amndDate)).delete()
                supRepRow = db((db.sm_doctor_visit_plan.cid == cid) & (db.sm_doctor_visit_plan.rep_id==rep_id_pending) & (db.sm_doctor_visit_plan.status == 'CReq') & (db.sm_doctor_visit_plan.schedule_date == amndDate)).update(status='Confirmed')
#                 supRepRow = db((db.sm_doctor_visit_plan.cid == cid) & (db.sm_doctor_visit_plan.rep_id==rep_id_pending) & (db.sm_doctor_visit_plan.status == 'CReqASM') & (db.sm_doctor_visit_plan.schedule_date == amndDate)).update(status='Confirmed')
            
            
            if int(depth)==int(levelDepth)-1:
                supRepRow = db((db.sm_doctor_visit_plan.cid == cid) & (db.sm_doctor_visit_plan.rep_id==rep_id_pending) & (db.sm_doctor_visit_plan.status == 'CReq') & (db.sm_doctor_visit_plan.schedule_date >= today)).select(db.sm_doctor_visit_plan.id,db.sm_doctor_visit_plan.schedule_date,db.sm_doctor_visit_plan.route_id,db.sm_doctor_visit_plan.route_name,db.sm_doctor_visit_plan.field1, groupby=db.sm_doctor_visit_plan.rep_id|db.sm_doctor_visit_plan.rep_name|db.sm_doctor_visit_plan.schedule_date ,orderby=~db.sm_doctor_visit_plan.status|db.sm_doctor_visit_plan.rep_id|db.sm_doctor_visit_plan.rep_name)
            else:
                supRepRow = db((db.sm_doctor_visit_plan.cid == cid) & (db.sm_doctor_visit_plan.rep_id==rep_id_pending) & (db.sm_doctor_visit_plan.status == 'CReq') & (db.sm_doctor_visit_plan.schedule_date >= today)).select(db.sm_doctor_visit_plan.id,db.sm_doctor_visit_plan.schedule_date,db.sm_doctor_visit_plan.route_id,db.sm_doctor_visit_plan.route_name,db.sm_doctor_visit_plan.field1, groupby=db.sm_doctor_visit_plan.rep_id|db.sm_doctor_visit_plan.rep_name|db.sm_doctor_visit_plan.schedule_date ,orderby=~db.sm_doctor_visit_plan.status|db.sm_doctor_visit_plan.rep_id|db.sm_doctor_visit_plan.rep_name)
#                 supRepRow = db((db.sm_doctor_visit_plan.cid == cid) & (db.sm_doctor_visit_plan.rep_id==rep_id_pending) & (db.sm_doctor_visit_plan.status == 'CReqASM') & (db.sm_doctor_visit_plan.schedule_date >= today)).select(db.sm_doctor_visit_plan.id,db.sm_doctor_visit_plan.schedule_date,db.sm_doctor_visit_plan.route_id,db.sm_doctor_visit_plan.route_name,db.sm_doctor_visit_plan.field1, groupby=db.sm_doctor_visit_plan.rep_id|db.sm_doctor_visit_plan.rep_name|db.sm_doctor_visit_plan.schedule_date ,orderby=~db.sm_doctor_visit_plan.status|db.sm_doctor_visit_plan.rep_id|db.sm_doctor_visit_plan.rep_name)
                
#             return supRepRow    
            repStr='<table style="border-style:solid; border-width:thin; border-color:#096" width="100%" border="1" cellspacing="0">'
            
            amndPlan=''
            for supRepRow in supRepRow:
                id=str(supRepRow.id)
                route_id=supRepRow.route_id
                route_name=supRepRow.route_name
                schedule_date_1=supRepRow.schedule_date
                reson=supRepRow.field1
                schedule_date=schedule_date_1.strftime('%d, %b')
                amndPlan=amndPlan+'<br>'+str(route_name)+' | '+str(route_id)
                appRow = db((db.sm_doctor_visit_plan.cid == cid) & (db.sm_doctor_visit_plan.rep_id==rep_id_pending) & (db.sm_doctor_visit_plan.status == 'Confirmed') & (db.sm_doctor_visit_plan.schedule_date == schedule_date_1)).select(db.sm_doctor_visit_plan.id,db.sm_doctor_visit_plan.schedule_date,db.sm_doctor_visit_plan.route_id,db.sm_doctor_visit_plan.route_name,db.sm_doctor_visit_plan.field1, groupby=db.sm_doctor_visit_plan.rep_id|db.sm_doctor_visit_plan.rep_name|db.sm_doctor_visit_plan.schedule_date ,orderby=~db.sm_doctor_visit_plan.status|db.sm_doctor_visit_plan.rep_id|db.sm_doctor_visit_plan.rep_name)
#                 return db._lastsql
                appPlan=''
                for appRow in appRow:
                    route_idApp=appRow.route_id
                    route_nameApp=appRow.route_name
                    appPlan=appPlan+'<br>'+str(route_nameApp)+' | '+str(route_idApp)
                if appPlan=='':
                    appPlan='-'
                repStr+='<tr height="30px"><td width="60px"><font style="font-size:18px; color:#00ABFD"> '+str(schedule_date)+'</font><br><font style="font-size:16px; color:#900"> ApprovedPlan:</font><br>'+str(appPlan)+'<br><font style="font-size:16px; color:#900">AmendmentRequest:</font><br>'+str(amndPlan)+'<br><input  type="submit" onClick="tourCReq_done(\''+id+'\');"   style=" background-color:#09C; color:#FFF; font-size:12px;  height:30px;" value=" Approve "    /><input  type="submit" onClick="tourCReq_reject(\''+id+'\');"   style=" background-color:#09C; color:#FFF; font-size:12px;  height:30px;" value=" Reject "    /><br><br></td></tr>'
            repStr=repStr+'</table>'
         
        if repStr!='':
            return '</START>'+'SUCCESS<SYNCDATA>'+str(repStr)+'</END>'
        else:
            return '</START>'+'FAILED<SYNCDATA>Pending not availabe</END>' 

def tourCReq_reject():
    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.rep_pass).strip()
    synccode = str(request.vars.synccode).strip()
    rep_id_pending=str(request.vars.rep_id_pending).strip()
    rowId=str(request.vars.rowId).strip()
    
    repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.sync_code == synccode) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.rep_id, db.sm_rep.name, db.sm_rep.mobile_no, db.sm_rep.user_type, db.sm_rep.level_id, db.sm_rep.depot_id, limitby=(0, 1))
    import time
    if not repRow:
       return 'Invalid Authorization'

    else:
        
        
        userType=repRow[0][db.sm_rep.user_type]
        repStr=''   
        if  userType=='sup': 
#             deleteRows = db((db.sm_doctor_visit_plan.cid == cid) & (db.sm_doctor_visit_plan.id == rowId)).delete()   
           
            compLevel = db((db.level_name_settings.cid == cid)).select(db.level_name_settings.depth ,orderby=~db.level_name_settings.depth, limitby=(0,1))
            for compLevel in compLevel:
                levelDepth=compLevel.depth

            supDepthRow = db((db.sm_supervisor_level.cid == cid) & (db.sm_supervisor_level.sup_id == rep_id) ).select(db.sm_supervisor_level.level_id,db.sm_supervisor_level.level_depth_no ,orderby=db.sm_supervisor_level.level_id)
            areaList=[]
            for supDepthRow in supDepthRow:
                areaList.append(supDepthRow.level_id)            
            if len(areaList)>0:
                depth=supDepthRow.level_depth_no

            import time
            today= time.strftime("%Y-%m-%d")
            
            
            checkRow = db((db.sm_doctor_visit_plan.cid == cid) & (db.sm_doctor_visit_plan.id == rowId)).select(db.sm_doctor_visit_plan.id,db.sm_doctor_visit_plan.schedule_date,db.sm_doctor_visit_plan.rep_id,limitby=(0,1))
#             return checkRow
            amndDate=''
            if checkRow:
                amndDate=checkRow[0].schedule_date
#             return amndDate
            if int(depth)==int(levelDepth)-1:
                supRepRow = db((db.sm_doctor_visit_plan.cid == cid) & (db.sm_doctor_visit_plan.rep_id==rep_id_pending) & (db.sm_doctor_visit_plan.status == 'CReq') & (db.sm_doctor_visit_plan.schedule_date == amndDate)).delete()
            else:
                supRepRow = db((db.sm_doctor_visit_plan.cid == cid) & (db.sm_doctor_visit_plan.rep_id==rep_id_pending) & (db.sm_doctor_visit_plan.status == 'CReq') & (db.sm_doctor_visit_plan.schedule_date == amndDate)).delete()
#                 supRepRow = db((db.sm_doctor_visit_plan.cid == cid) & (db.sm_doctor_visit_plan.rep_id==rep_id_pending) & (db.sm_doctor_visit_plan.status == 'CReqASM') & (db.sm_doctor_visit_plan.schedule_date == amndDate)).delete()
                
            
            
            if int(depth)==int(levelDepth)-1:
                supRepRow = db((db.sm_doctor_visit_plan.cid == cid) & (db.sm_doctor_visit_plan.rep_id==rep_id_pending) & (db.sm_doctor_visit_plan.status == 'CReq') & (db.sm_doctor_visit_plan.schedule_date >= today)).select(db.sm_doctor_visit_plan.id,db.sm_doctor_visit_plan.schedule_date,db.sm_doctor_visit_plan.route_id,db.sm_doctor_visit_plan.route_name,db.sm_doctor_visit_plan.field1, groupby=db.sm_doctor_visit_plan.rep_id|db.sm_doctor_visit_plan.rep_name|db.sm_doctor_visit_plan.schedule_date ,orderby=~db.sm_doctor_visit_plan.status|db.sm_doctor_visit_plan.rep_id|db.sm_doctor_visit_plan.rep_name)
            else:
                supRepRow = db((db.sm_doctor_visit_plan.cid == cid) & (db.sm_doctor_visit_plan.rep_id==rep_id_pending) & (db.sm_doctor_visit_plan.status == 'CReq') & (db.sm_doctor_visit_plan.schedule_date >= today)).select(db.sm_doctor_visit_plan.id,db.sm_doctor_visit_plan.schedule_date,db.sm_doctor_visit_plan.route_id,db.sm_doctor_visit_plan.route_name,db.sm_doctor_visit_plan.field1, groupby=db.sm_doctor_visit_plan.rep_id|db.sm_doctor_visit_plan.rep_name|db.sm_doctor_visit_plan.schedule_date ,orderby=~db.sm_doctor_visit_plan.status|db.sm_doctor_visit_plan.rep_id|db.sm_doctor_visit_plan.rep_name)
#                 supRepRow = db((db.sm_doctor_visit_plan.cid == cid) & (db.sm_doctor_visit_plan.rep_id==rep_id_pending) & (db.sm_doctor_visit_plan.status == 'CReqASM') & (db.sm_doctor_visit_plan.schedule_date >= today)).select(db.sm_doctor_visit_plan.id,db.sm_doctor_visit_plan.schedule_date,db.sm_doctor_visit_plan.route_id,db.sm_doctor_visit_plan.route_name,db.sm_doctor_visit_plan.field1, groupby=db.sm_doctor_visit_plan.rep_id|db.sm_doctor_visit_plan.rep_name|db.sm_doctor_visit_plan.schedule_date ,orderby=~db.sm_doctor_visit_plan.status|db.sm_doctor_visit_plan.rep_id|db.sm_doctor_visit_plan.rep_name)
                
#             return supRepRow    
            repStr='<table style="border-style:solid; border-width:thin; border-color:#096" width="100%" border="1" cellspacing="0">'
            amndPlan=''
            for supRepRow in supRepRow:
                id=str(supRepRow.id)
                route_id=supRepRow.route_id
                route_name=supRepRow.route_name
                schedule_date_1=supRepRow.schedule_date
                reson=supRepRow.field1
                schedule_date=schedule_date_1.strftime('%d, %b')
                amndPlan=amndPlan+'<br>'+str(route_name)+' | '+str(route_id)
                appRow = db((db.sm_doctor_visit_plan.cid == cid) & (db.sm_doctor_visit_plan.rep_id==rep_id_pending) & (db.sm_doctor_visit_plan.status == 'Confirmed') & (db.sm_doctor_visit_plan.schedule_date == schedule_date_1)).select(db.sm_doctor_visit_plan.id,db.sm_doctor_visit_plan.schedule_date,db.sm_doctor_visit_plan.route_id,db.sm_doctor_visit_plan.route_name,db.sm_doctor_visit_plan.field1, groupby=db.sm_doctor_visit_plan.rep_id|db.sm_doctor_visit_plan.rep_name|db.sm_doctor_visit_plan.schedule_date ,orderby=~db.sm_doctor_visit_plan.status|db.sm_doctor_visit_plan.rep_id|db.sm_doctor_visit_plan.rep_name)
#                 return db._lastsql
                appPlan=''
                for appRow in appRow:
                    route_idApp=appRow.route_id
                    route_nameApp=appRow.route_name
                    appPlan=appPlan+'<br>'+str(route_nameApp)+' | '+str(route_idApp)
                if appPlan=='':
                    appPlan='-'
                repStr+='<tr height="30px"><td width="60px"><font style="font-size:18px; color:#00ABFD"> '+str(schedule_date)+'</font><br><font style="font-size:16px; color:#900"> ApprovedPlan:</font><br>'+str(appPlan)+'<br><font style="font-size:16px; color:#900">AmendmentRequest:</font><br>'+str(amndPlan)+'<br><input  type="submit" onClick="tourCReq_done(\''+id+'\');"   style=" background-color:#09C; color:#FFF; font-size:12px;  height:30px;" value=" Approve "    /><input  type="submit" onClick="tourCReq_reject(\''+id+'\');"   style=" background-color:#09C; color:#FFF; font-size:12px;  height:30px;" value=" Reject "    /><br><br></td></tr>'
            repStr=repStr+'</table>'
         
        if repStr!='':
            return '</START>'+'SUCCESS<SYNCDATA>'+str(repStr)+'</END>'
        else:
            return '</START>'+'FAILED<SYNCDATA>Pending not availabe</END>' 


def tourCReq_delete():
    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.rep_pass).strip()
    synccode = str(request.vars.synccode).strip()
    rep_id_pending=str(request.vars.rep_id_pending).strip()
    rowId=str(request.vars.rowId).strip()
    
    repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.sync_code == synccode) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.rep_id, db.sm_rep.name, db.sm_rep.mobile_no, db.sm_rep.user_type, db.sm_rep.level_id, db.sm_rep.depot_id, limitby=(0, 1))
    import time
    if not repRow:
       return 'Invalid Authorization'

    else:
        
        
        userType=repRow[0][db.sm_rep.user_type]
        repStr=''   
        if  userType=='sup': 
            deleteRows = db((db.sm_doctor_visit_plan.cid == cid) & (db.sm_doctor_visit_plan.id == rowId)).delete()   
           
            import time
            today= time.strftime("%Y-%m-%d")
            
                
            supRepRow = db((db.sm_doctor_visit_plan.cid == cid) & (db.sm_doctor_visit_plan.rep_id==rep_id_pending) & (db.sm_doctor_visit_plan.status == 'CReq') & (db.sm_doctor_visit_plan.schedule_date >= today)).select(db.sm_doctor_visit_plan.id,db.sm_doctor_visit_plan.schedule_date,db.sm_doctor_visit_plan.route_id,db.sm_doctor_visit_plan.route_name,db.sm_doctor_visit_plan.field1, groupby=db.sm_doctor_visit_plan.rep_id|db.sm_doctor_visit_plan.rep_name ,orderby=~db.sm_doctor_visit_plan.status|db.sm_doctor_visit_plan.rep_id|db.sm_doctor_visit_plan.rep_name)
#                 return db._lastsql
            repStr='<table style="border-style:solid; border-width:thin; border-color:#096" width="100%" border="1" cellspacing="0">'
            for supRepRow in supRepRow:
                id=str(supRepRow.id)
                route_id=supRepRow.route_id
                route_name=supRepRow.route_name
                schedule_date_1=supRepRow.schedule_date
                reson=supRepRow.field1
                schedule_date=schedule_date_1.strftime('%d, %b')
                
                repStr+='<tr height="30px"><td width="60px">'+str(schedule_date)+'<td>'+str(route_name)+' | '+str(route_id)+'</td><td width="45px" align="right"><input  type="submit" onClick="tourCReq_delete(\''+id+'\');"   style=" background-color:#09C; color:#FFF; font-size:12px;  height:30px;" value=" Done "    /></td>'

         
        if repStr!='':
            return '</START>'+'SUCCESS<SYNCDATA>'+str(repStr)+'</END>'
        else:
            return '</START>'+'FAILED<SYNCDATA>Pending not availabe</END>' 

def lastThreeVisit():
    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.rep_pass).strip()
    synccode = str(request.vars.synccode).strip()
    rep_id_pending=str(request.vars.rep_id_pending).strip()
    
    repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.sync_code == synccode) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.rep_id, db.sm_rep.name, db.sm_rep.mobile_no, db.sm_rep.user_type, db.sm_rep.level_id, db.sm_rep.depot_id, limitby=(0, 1))
    import time
    if not repRow:
       return 'Invalid Authorization'

    else:
        userType=repRow[0][db.sm_rep.user_type]
        visitPlanMarketComb=''
      
        recRow = db((db.sm_doctor_visit.cid == cid) & (db.sm_doctor_visit.rep_id == rep_id_pending)).select(db.sm_doctor_visit.ALL ,orderby=~db.sm_doctor_visit.id,limitby=(0,3))
#         return recRow
        repStr='<table style="border-style:solid; border-width:thin; border-color:#096" width="100%" border="1" cellspacing="0">'
        for recRow in recRow:
            id=recRow.id
            doc_id=recRow.doc_id
            doc_name=recRow.doc_name
            rep_id=recRow.rep_id
            rep_name=recRow.rep_name
            route_id=recRow.route_id
            route_name=recRow.route_name
            rep_id=recRow.rep_id
            visit_dtime_1=recRow.visit_dtime
            visit_dtime=visit_dtime_1.strftime('%d, %b %H:%M'  )
            repIdName=str(rep_name)+' | '+str(rep_id)
            repStr=repStr+'<tr height="30px"><td >'+str(visit_dtime)+'</br>'+str(route_name)+' | '+str(route_id)+'</br>'+str(doc_name)+' | '+str(doc_id)+'</td></tr>'
        repStr=repStr+'</table>'
#         return repStr
        import datetime
        today_1= time.strftime("%Y-%m-%d")  
        today= datetime.datetime.strptime(today_1, "%Y-%m-%d")
        tomorrow =today + datetime.timedelta(days = 8)
        recTour = db((db.sm_doctor_visit_plan.cid == cid) & (db.sm_doctor_visit_plan.rep_id == rep_id_pending) & (db.sm_doctor_visit_plan.status == 'Confirmed') & (db.sm_doctor_visit_plan.schedule_date >= today) & (db.sm_doctor_visit_plan.schedule_date < tomorrow)).select(db.sm_doctor_visit_plan.ALL ,orderby=db.sm_doctor_visit_plan.schedule_date)
#         return recTour
        if recTour:
            repStr=repStr+'<br><font style="font-size:16px">'+'Tour Plan'+'</font>'+'<table style="border-style:solid; border-width:thin; border-color:#096" width="100%" border="1" cellspacing="0">'

        for recTour in recTour:
            route_id=str(recTour.route_id)
            route_name=str(recTour.route_name)
            
            visit_dtime_1=recTour.schedule_date
            visit_dtime=visit_dtime_1.strftime('%d, %b'  )
           
            repStr=repStr+'<tr height="30px"><td >'+str(visit_dtime)+'</br>'+str(route_name)+' | '+str(route_name)+'</td></tr>'
        repStr=repStr+'</table>'
        if recRow:
            return '</START>'+'SUCCESS<SYNCDATA>'+str(repStr)+'<SYNCDATA>'+str(repIdName)+'</END>'
        else:
            return '</START>'+'FAILED<SYNCDATA>Data not availabe</END>'    
              

def checkRequest():
    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.rep_pass).strip()
    synccode = str(request.vars.synccode).strip()
    
    checkReq=0
    repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.sync_code == synccode) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.rep_id, db.sm_rep.name, db.sm_rep.mobile_no, db.sm_rep.user_type, db.sm_rep.level_id, db.sm_rep.depot_id, limitby=(0, 1))
    
    if not repRow:
       return 'Invalid Authorization'

    else:
        userType=repRow[0][db.sm_rep.user_type]
        repStr=''
        if  userType=='rep':    
            import time
            today= time.strftime("%Y-%m-%d")            
            supRepRow = db((db.sm_doctor_visit_plan.cid == cid) & (db.sm_doctor_visit_plan.rep_id == rep_id) &  (db.sm_doctor_visit_plan.status != 'Cancelled') & (db.sm_doctor_visit_plan.schedule_date >= today)).select(db.sm_doctor_visit_plan.rep_id,db.sm_doctor_visit_plan.rep_name, groupby=db.sm_doctor_visit_plan.rep_id|db.sm_doctor_visit_plan.rep_name ,orderby=db.sm_doctor_visit_plan.rep_id|db.sm_doctor_visit_plan.rep_name)
    #         return supRepRow
            for supRepRow in supRepRow:
                rep_id=supRepRow.rep_id
                rep_name=supRepRow.rep_name
                rep_id_name=str(rep_name)+'|'+str(rep_id)
                repStr+='<li  style="border-bottom-style:solid; border-color:#CBE4E4;border-bottom-width:thin" ><input  type="submit" onClick="tourRepInfo(\''+rep_id+'\');"   style=" background-color:#09C; color:#FFF; font-size:12px; width:40px; height:30px;" value=" Info "    />&nbsp;&nbsp; <font id="'+ rep_id +'"  class="name" >'+ rep_id_name+'</font></li>'
            checkReq=1    
        if  userType=='sup':    
            areaList=[]
            import time
            today= time.strftime("%Y-%m-%d")
            supDepthRow = db((db.sm_supervisor_level.cid == cid) & (db.sm_supervisor_level.sup_id == rep_id) ).select(db.sm_supervisor_level.level_id,db.sm_supervisor_level.level_depth_no ,orderby=db.sm_supervisor_level.level_id)
#             return db._lastsql
            for supDepthRow in supDepthRow:
                areaList.append(supDepthRow.level_id)
            
            if len(areaList)>0:
                depth=supDepthRow.level_depth_no
                level='level'+str(depth)+'_id'
#                 return level
                today= time.strftime("%Y-%m-%d")  
                
                supLevel='level'+str(depth)
                supARec=db((db.sm_level.cid == cid)& (db.sm_level.is_leaf == '1') & (db.sm_level[supLevel].belongs(areaList)) ).select(db.sm_level.level_id,orderby=db.sm_level.level_id)
#                 return supAList
                supAList=[]
                for supARec in supARec:
                    supAList.append(supARec.level_id)
#              ====================Market   
            marketList=[]
            marketTourRows = db((db.sm_doctor_area.cid==cid) &(db.sm_doctor_area.area_id.belongs(supAList))).select(db.sm_doctor_area.field1,db.sm_doctor_area.note, orderby=db.sm_doctor_area.note, groupby=db.sm_doctor_area.field1|db.sm_doctor_area.note)
#                 return db._lastsql
            for marketTourRow in marketTourRows:
                market_id =  marketTourRow.field1
                marketList.append(market_id)
    
                
                
                
                
                
                
            supRepRow = db((db.sm_doctor_visit_plan.cid == cid) & (db.sm_doctor_visit_plan.route_id.belongs(marketList)) & (db.sm_doctor_visit_plan.status == 'Submitted') & (db.sm_doctor_visit_plan.schedule_date >= today)).select(db.sm_doctor_visit_plan.rep_id,db.sm_doctor_visit_plan.rep_name,db.sm_doctor_visit_plan.status, groupby=db.sm_doctor_visit_plan.rep_id|db.sm_doctor_visit_plan.rep_name ,orderby=~db.sm_doctor_visit_plan.status|db.sm_doctor_visit_plan.rep_id|db.sm_doctor_visit_plan.rep_name)
#                 return db._lastsql
             
            for supRepRow in supRepRow:
                checkReq=1
 
        return checkReq
        
         
def inbox():
    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.rep_pass).strip()
    synccode = str(request.vars.synccode).strip()
    rep_id_pending=str(request.vars.rep_id_pending).strip()
    
    repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.sync_code == synccode) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.rep_id, db.sm_rep.name, db.sm_rep.mobile_no, db.sm_rep.user_type, db.sm_rep.level_id, db.sm_rep.depot_id, limitby=(0, 1))
    import time
    if not repRow:
       return 'Invalid Authorization'

    else:
        userType=repRow[0][db.sm_rep.user_type]
        visitPlanMarketComb=''
      
        recRow = db((db.sm_msg_box.cid == cid) & (db.sm_msg_box.msg_to == rep_id) & (db.sm_msg_box.status == 'Active')).select(db.sm_msg_box.ALL ,orderby=~db.sm_msg_box.id,limitby=(0,20))
#         return recRow
        repStr='<table style="border-style:solid; border-width:thin; border-color:#096" width="100%" border="1" cellspacing="0">'
        for recRow in recRow:
            msg=recRow.msg
            msgTime_1=recRow.created_on
            msgTime=msgTime_1.strftime('%d, %b %H:%M'  )
            msgFrom=recRow.msg_from
            msgFromName=recRow.msgFromName
#             repStr=repStr+'<tr height="30px"><td >'+str(msgTime)+'</br>'+str(msgFromName)+' | '+str(msgFrom)+'</br>'+str(msg)+'</td></tr>'
            repStr=repStr+'<tr height="30px"><td >'+str(msgTime)+'</br>'+str(msgFrom)+'</br>'+str(msg)+'</td></tr>'
        repStr=repStr+'</table>'
#         return repStr
        if repStr!='':
            return '</START>'+'SUCCESS<SYNCDATA>'+str(repStr)+'<SYNCDATA>'+str(repIdName)+'</END>'
        else:
            return '</START>'+'FAILED<SYNCDATA>Msg not availabe</END>'      


def holidayInfo():
    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.rep_pass).strip()
    synccode = str(request.vars.synccode).strip()
    
    compRow = db((db.sm_company_settings.cid == cid) & (db.sm_company_settings.status == 'ACTIVE')).select(db.sm_company_settings.cid, limitby=(0, 1))
    if not compRow:
        return 'FAILED<SYNCDATA>Invalid Company'
    else:
        repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.id, db.sm_rep.name, db.sm_rep.sync_count, db.sm_rep.first_sync_date, db.sm_rep.user_type, db.sm_rep.depot_id, db.sm_rep.level_id, db.sm_rep.field2, limitby=(0, 1))
#         return db._lastsql
        if not repRow:
           retStatus = 'FAILED<SYNCDATA>Invalid Authorization'
           return retStatus
        else:
            holiday_str=''
            holydayReason="""<select id="holidayReason" style=" width:100%;background-color:#CFC" data-native-menu="false" >
                        <option value="Personal" >Personal</option>
                        <option value="Medical" >Medical</option>
                        <option value="Others" >Others</option>
                        </select>"""
            
            holidayRow= db((db.sm_holiday.cid == cid) & (db.sm_holiday.rep_id == rep_id)).select(db.sm_holiday.ALL,orderby=~db.sm_holiday.id, limitby=(0, 10))

            
            
            holiday_str=''
            if holidayRow:
                holiday_str=holiday_str+'<table width="100%" border="1" cellpadding="0" cellspacing="0" style="border:solid; border-style:solid; border-color:#008080"><tr style="font-size:16px; font-weight:bold"><td width="20%">Date</td><td >Reason</td><td width="20%">Status</td></tr>'
                for holidayRow in holidayRow:
                    holiday_1 = holidayRow.holiday
                    reason = holidayRow.field1
                    holiday = holiday_1.strftime('%d, %b'  )
                    status = str(holidayRow.status)
                    holiday_str=holiday_str+'<tr style="font-size:14px"><td >'+str(holiday)+'</td><td >'+str(reason)+'</td><td >'+str(status)+'</td></tr>'
                holiday_str=holiday_str+'</table>'
            retStatus= 'SUCCESS<SYNCDATA>'+holiday_str+'<SYNCDATA>'+str(holydayReason)
            return retStatus
def holidayAdd():
    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.rep_pass).strip()
    synccode = str(request.vars.synccode).strip()
    holiday = str(request.vars.holiday).strip()
    holidayReason = str(request.vars.holidayReason).strip()
#     return holidayReason
    
    import time
    compRow = db((db.sm_company_settings.cid == cid) & (db.sm_company_settings.status == 'ACTIVE')).select(db.sm_company_settings.cid, limitby=(0, 1))
    if not compRow:
        return 'FAILED<SYNCDATA>Invalid Company'
    else:
        repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.ALL, limitby=(0, 1))
#         return db._lastsql
        if not repRow:
           retStatus = 'FAILED<SYNCDATA>Invalid Authorization'
           return retStatus
        else:
            rep_id = str(repRow[0].rep_id)
            rep_name = str(repRow[0].name)
            user_type = str(repRow[0].user_type)
#             return user_type
            slRow= db(db.sm_holiday.cid == cid).select(db.sm_holiday.sl,orderby=~db.sm_holiday.sl, limitby=(0, 1))
            sl=0
            if slRow:
                sl= int(slRow[0].sl)
            max_sl=sl+1
            
            holidayRow_check= db((db.sm_holiday.cid == cid) & (db.sm_holiday.rep_id == rep_id) & (db.sm_holiday.holiday == holiday)).select(db.sm_holiday.ALL,orderby=~db.sm_holiday.id, limitby=(0, 1))
            if holidayRow_check:
                return 'SUCCESS<SYNCDATA>Already Exist'
                
            else:
                holyday_insert=db.sm_holiday.insert(cid=cid,sl=max_sl,rep_id=rep_id,rep_name=rep_name,user_type=user_type,holiday=holiday,status='Submitted',    field1=holidayReason)            
                retStatus = 'SUCCESS<SYNCDATA>Submitted Successfully'
#                 if (holyday_insert):
#                     retStatus = 'SUCCESS<SYNCDATA>Submitted Successfully'
#                 else:     
#                     retStatus = 'SUCCESS<SYNCDATA>Error Please Try Again'
            holiday_str=''
            holydayReason="""<select id="holidayReason" style=" width:100%;background-color:#CFC" data-native-menu="false" >
                        <option value="Personal" >Personal</option>
                        <option value="Medical" >Medical</option>
                        <option value="Others" >Others</option>
                        </select>"""
            holidayRow= db((db.sm_holiday.cid == cid) & (db.sm_holiday.rep_id == rep_id)).select(db.sm_holiday.ALL,orderby=~db.sm_holiday.id, limitby=(0, 10))
#             return db._lastsql
            
            if holidayRow:
                holiday_str=holiday_str+'<table width="100%" border="1" cellpadding="0" cellspacing="0" style="border:solid; border-style:solid; border-color:#008080"><tr style="font-size:16px; font-weight:bold"><td width="20%">Date</td><td >Reason</td><td width="20%">Status</td></tr>'
                for holidayRow in holidayRow:
                    holiday_1 = holidayRow.holiday
                    reason = holidayRow.field1
                    holiday = holiday_1.strftime('%d, %b'  )
                    status = str(holidayRow.status)
                    holiday_str=holiday_str+'<tr style="font-size:14px"><td  >'+str(holiday)+'</td><td >'+str(reason)+'</td><td >'+str(status)+'</td></tr>'
                holiday_str=holiday_str+'</table>'
            return retStatus+'<SYNCDATA>'+holiday_str+'<SYNCDATA>'+holydayReason


def checkInbox():
    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.rep_pass).strip()
    synccode = str(request.vars.synccode).strip()
    
    checkReq=0
#     repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.sync_code == synccode) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.rep_id, db.sm_rep.name, db.sm_rep.mobile_no, db.sm_rep.user_type, db.sm_rep.level_id, db.sm_rep.depot_id, limitby=(0, 1))
#     
#     if not repRow:
#        return 'Invalid Authorization'

#     else:
#     userType=repRow[0][db.sm_rep.user_type]
    holidayCheck=0
#     holidayRow_check= db((db.sm_msg_box.cid == cid) & (db.sm_msg_box.msg_to == rep_id)).select(db.sm_msg_box.ALL,orderby=~db.sm_msg_box.id, limitby=(0, 10))
#     if holidayRow_check:
#         holidayCheck=1
        
    try:
       version = str(request.vars.version).strip()   
    except:
       version = '0'
      
    cRow_check= db((db.sm_settings.cid == cid) & (db.sm_settings.s_key == 'COMMON')& (db.sm_settings.s_value == version)).select(db.sm_settings.ALL, limitby=(0, 1))
    cStr=''
    if cRow_check:
        cStr1=cRow_check[0].field1
        cStr2=cRow_check[0].note
        cStr='<span style="color:#063">'+str(cStr1)+'</span>' 
    else:
        cStr2='http://im-gp.com/d/hamdard/'

        linkPath="window.open('"+cStr2+"', '_system');"
        
        
        repStr='<font style="color:#656DC0" onclick="'+linkPath+'" style="color:#900" >'+ cStr2 +'</font> '
        cStr= 'Please Update App '+'</br>'+repStr

        # cStr='Please Update App '+'</br>'+ '<a href="'+str(cStr2)+'" target="_blank"><span style="color:#67C065">'+str(cStr2)+'</span></a>' 

    return str(holidayCheck)+'<SYNCDATA>'+str(cStr)

#     return holidayCheck   



# =====================================

def chemist_submit():
    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.rep_pass).strip()
    synccode = str(request.vars.synccode).strip()
    route = str(request.vars.route).strip()
#     client_id = str(request.vars.client_id).strip()
    ChemistName=str(request.vars.ChemistName).strip()
    Address_Line_1=str(request.vars.Address_Line_1).strip()
    district=str(request.vars.district).strip()
    thana=str(request.vars.thana).strip()
    RegistrationNo=str(request.vars.RegistrationNo).strip()
    NID=str(request.vars.NID).strip()
    Contact_Name=str(request.vars.Contact_Name).strip()
    Contact_phone=str(request.vars.Contact_phone).strip()
    Category=str(request.vars.Category).strip()
    SubCategory=str(request.vars.SubCategory).strip()
    DOB=str(request.vars.DOB).strip()
    Cash_Credit=str(request.vars.Cash_Credit).strip()
    Credit_Limit=str(request.vars.Credit_Limit).strip()
    Status=str(request.vars.Status).strip()
    imageName=str(request.vars.imageName).strip()
    NumberofDoc=str(request.vars.NumberofDoc).strip()
    AvgPatientPerDay=str(request.vars.AvgPatientPerDay).strip()
    
    
    route = urllib.unquote(route.decode('utf8'))
#     client_id = urllib.unquote(client_id.decode('utf8'))
    ChemistName=urllib.unquote(ChemistName.decode('utf8'))
    Address_Line_1=urllib.unquote(Address_Line_1.decode('utf8'))
    district=urllib.unquote(district.decode('utf8'))
    RegistrationNo=urllib.unquote(RegistrationNo.decode('utf8'))
    NID=urllib.unquote(NID.decode('utf8'))
    Contact_Name=urllib.unquote(Contact_Name.decode('utf8'))
#     Contact_phone=urllib.unquote(Contact_phone.decode('utf8'))
    Category=urllib.unquote(Category.decode('utf8'))
    SubCategory=urllib.unquote(SubCategory.decode('utf8'))
    DOB=urllib.unquote(DOB.decode('utf8'))
    Cash_Credit=urllib.unquote(Cash_Credit.decode('utf8'))
#     Credit_Limit=urllib.unquote(Credit_Limit.decode('utf8'))
    Status=urllib.unquote(Status.decode('utf8'))
    thana=urllib.unquote(thana.decode('utf8'))
    imageName=urllib.unquote(imageName.decode('utf8'))
    NumberofDoc=urllib.unquote(NumberofDoc.decode('utf8'))
    AvgPatientPerDay=urllib.unquote(AvgPatientPerDay.decode('utf8'))
    catID=''
    catName=''
    subcatID=''
    subcatName=''
    
    if Category!='' and Category!=None and Category!='None':
        catID=Category.split('|')[1]
        catName=Category.split('|')[0]

    if SubCategory!='' and Category!=None and Category!='None':
        subcatID=SubCategory.split('|')[1]
        subcatName=SubCategory.split('|')[0]
    if DOB=='' or DOB==None or DOB=='None':
        DOB='000-00-00'
    if NID=='' or NID!=None or NID!='None':
        NID=0
    if Contact_phone=='' or Contact_phone!=None or Contact_phone!='None':
        Contact_phone=0
    if Credit_Limit=='' or Credit_Limit!=None or Credit_Limit!='None':
        Credit_Limit=0
    
#    return  subcatID
#     mName=dDist.split('|')[0]
#     mID=dDist.split('|')[1]
    
    
    ChemistName=urllib.unquote(ChemistName.decode('utf8'))
    Address_Line_1=urllib.unquote(Address_Line_1.decode('utf8'))
    district=urllib.unquote(district.decode('utf8'))
    RegistrationNo=urllib.unquote(RegistrationNo.decode('utf8'))
#     NID=urllib.unquote(NID.decode('utf8'))
    Contact_Name=urllib.unquote(Contact_Name.decode('utf8'))
#     Contact_phone=urllib.unquote(Contact_phone.decode('utf8'))
    Category=urllib.unquote(Category.decode('utf8'))
    SubCategory=urllib.unquote(SubCategory.decode('utf8'))
    DOB=urllib.unquote(DOB.decode('utf8'))
    Cash_Credit=urllib.unquote(Cash_Credit.decode('utf8'))
#     Credit_Limit=urllib.unquote(Credit_Limit.decode('utf8'))
    Status=urllib.unquote(Status.decode('utf8'))
    thana=urllib.unquote(thana.decode('utf8'))
    catID=''
    catName=''
    subcatID=''
    subcatName=''
    if (DOB==''): 
        DOB='1900-01-01'
    compRow = db((db.sm_company_settings.cid == cid) & (db.sm_company_settings.status == 'ACTIVE')).select(db.sm_company_settings.cid, limitby=(0, 1))
    if not compRow:
        return 'FAILED<SYNCDATA>Invalid Company'
    else:
        repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.sync_code == synccode) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.rep_id, db.sm_rep.name, db.sm_rep.mobile_no, db.sm_rep.user_type, db.sm_rep.level_id, db.sm_rep.depot_id, limitby=(0, 1))

        
        if not repRow:
           return 'FAILED<SYNCDATA>Invalid Authorization'

        else:
            
            
            slRow= db((db.sm_settings_pharma.cid == cid) & (db.sm_settings_pharma.s_key == 'CHEMSL')).select(db.sm_settings_pharma.s_value,orderby=~db.sm_settings_pharma.s_value, limitby=(0, 1))
            #             return slRow
            clientId=0
            if slRow:
                clientId= int(slRow[0].s_value)
            maxClient_id=clientId+1
#             return maxClient_id
#             chemistRow = db((db.sm_client_temp.cid == cid) ).select(db.sm_client_temp.client_id, orderby=~db.sm_client_temp.id,limitby=(0, 1))
#             getID=0
#             if chemistRow:
#                 getID=int(str(chemistRow[0].client_id).replace('D',''))
#             client_id='D0'+str(getID+1)
#             return client_id
#             if chemistRow:  
#                  db((db.sm_client_temp.cid == cid) & (db.sm_client_temp.client_id == client_id) ).update( area_id =route,name=ChemistName ,vat_registration_no=RegistrationNo ,district=district,thana=thana,nid=int(NID) , owner_name=Contact_Name ,contact_no1=Contact_phone ,category_id=catID , category_name=catName,sub_category_id=subcatID ,sub_category_name=subcatName, dob=DOB ,field1=Cash_Credit ,credit_limit=int(Credit_Limit) ,status=Status)
#             else:
#                 pass
            db.sm_client_temp.insert(cid =cid,client_id=maxClient_id ,address=Address_Line_1,area_id =route,name=ChemistName ,vat_registration_no=RegistrationNo ,district=district,thana=thana,nid=int(NID) , owner_name=Contact_Name ,contact_no1=Contact_phone ,category_id=catID , category_name=catName,sub_category_id=subcatID ,sub_category_name=subcatName, field1=Cash_Credit ,credit_limit=int(Credit_Limit) ,status=Status,photo=imageName, field2=NumberofDoc,note=AvgPatientPerDay,newChemist=1)
            settings_update=db((db.sm_settings_pharma.cid == cid) & (db.sm_settings_pharma.s_key == 'CHEMSL')).update(s_value=str(maxClient_id))
                  
    return 'SUCCESS<SYNCDATA>'+'Submitted Successfully  '
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
#     return holidayReason
    
    import time
    compRow = db((db.sm_company_settings.cid == cid) & (db.sm_company_settings.status == 'ACTIVE')).select(db.sm_company_settings.cid, limitby=(0, 1))
    if not compRow:
        return 'FAILED<SYNCDATA>Invalid Company'
    else:
        repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.ALL, limitby=(0, 1))
#         return repRow
#         return db._lastsql
        if not repRow:
           retStatus = 'FAILED<SYNCDATA>Invalid Authorization'
           return retStatus
        else:
            slRow= db((db.sm_settings_pharma.cid == cid) & (db.sm_settings_pharma.s_key == 'CHEMSL')).select(db.sm_settings_pharma.s_value,orderby=~db.sm_settings_pharma.s_value, limitby=(0, 1))
            #             return slRow
            clientId=0
            if slRow:
                clientId= int(slRow[0].s_value)
            maxClient_id=clientId+1
            #             return maxClient_id
            
            client_insert=db.sm_client.insert(cid=cid,client_id=maxClient_id,name=chemist_name,area_id=market_id,market_id=str(market_id),contact_no1= chemist_ph , trade_license_no=trade_license_no,vat_registration_no=vat_registration_no , created_by= rep_id,  dob= chemist_dob,status='SUBMITTED',photo=imageName,address=chemist_add)            
#             client_update=db((db.sm_client.cid == cid) & (db.sm_client.client_id == maxClient_id)).update(market_id=str(market_id),contact_no1= chemist_ph , trade_license_no=trade_license_no,vat_registration_no=vat_registration_no )
            settings_update=db((db.sm_settings_pharma.cid == cid) & (db.sm_settings_pharma.s_key == 'CHEMSL')).update(s_value=str(maxClient_id))
#             slRow[0].update_record(s_value=maxClient_id)
            retStatus = 'SUCCESS<SYNCDATA>Submitted Successfully'
            
            
            return retStatus

def chemist_cancelSubmit():
    return 'FAILED<SYNCDATA>Restricted'
    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.rep_pass).strip()
    synccode = str(request.vars.synccode).strip()
    market_id = str(request.vars.market_id).strip()
    visit_client = str(request.vars.visit_client).strip()
    visit_clientName = str(request.vars.visit_clientName).strip()
    inactive_reason = str(request.vars.inactive_reason).strip()
    market_id = str(request.vars.market_id).strip()
    
    
#     return holidayReason
    
    import time
    compRow = db((db.sm_company_settings.cid == cid) & (db.sm_company_settings.status == 'ACTIVE')).select(db.sm_company_settings.cid, limitby=(0, 1))
    if not compRow:
        return 'FAILED<SYNCDATA>Invalid Company'
    else:
        repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.ALL, limitby=(0, 1))
#         return repRow
#         return db._lastsql
        if not repRow:
           retStatus = 'FAILED<SYNCDATA>Invalid Authorization'
           return retStatus
        else:
            clientRow= db((db.sm_client.cid == cid) & (db.sm_client.client_id == visit_client)).select(db.sm_client.client_id, limitby=(0, 1))
#             return clientRow
            if clientRow:
                client_update=db((db.sm_client.cid == cid) & (db.sm_client.client_id == visit_client)).update(status='ACTIVE',field1=inactive_reason) 
            clientRowTemp= db((db.sm_client_temp.cid == cid) & (db.sm_client_temp.client_id == visit_client)).select(db.sm_client_temp.client_id, limitby=(0, 1))
            if clientRowTemp:

                clientUpdate=db((db.sm_client_temp.cid == cid) & (db.sm_client_temp.client_id == visit_client)).update(status='Rreq',note=inactive_reason)
            else:

                clientInsert=db.sm_client_temp.insert(cid =cid,client_id=visit_client ,name=visit_clientName,area_id=market_id,status='Rreq',note=inactive_reason,newChemist=0)
#                 client_update=db((db.sm_client.cid == cid) & (db.sm_client.client_id == visit_client)).update(status='INACTIVE',field1=inactive_reason)            
#                 return db._lastsql
            retStatus = 'SUCCESS<SYNCDATA>Submitted Successfully'


            return retStatus  
        
def check_this_n_next_month():
    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.rep_pass).strip()
    synccode = str(request.vars.synccode).strip()

    compRow = db((db.sm_company_settings.cid == cid) & (db.sm_company_settings.status == 'ACTIVE')).select(db.sm_company_settings.cid, limitby=(0, 1))
    if not compRow:
        return 'FAILED<SYNCDATA>Invalid Company'
    else:
        repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.ALL, limitby=(0, 1))
#         return repRow
#         return db._lastsql
        if not repRow:
           retStatus = 'FAILED<SYNCDATA>Invalid Authorization'
           return retStatus
        else:
            rep_name = repRow[0].name
            depot_id = repRow[0].depot_id
            user_type = repRow[0].user_type
            level_id = repRow[0].level_id
            depth = repRow[0].field2
            level = 'level' + str(depth)


#  ==============================   
            import datetime
            today_1= time.strftime("%Y-%m-%d")  
            today= datetime.datetime.strptime(today_1, "%Y-%m-%d")
            tomorrow =today + datetime.timedelta(days = 1)
            
            
            today = datetime.datetime.today()
            nextMonthDatetime = today + datetime.timedelta(days=(today.max.day - today.day)+1)
            nextMonth=str(nextMonthDatetime).split('-')[0]+'-'+str(nextMonthDatetime).split('-')[1]+'-01'
#             nextMonth=str(nextMonthDatetime).split(' ')[0]
#             return nextMonth

# ==================================

            if (user_type == 'rep'):
                
                #------ market list
                marketStr = ''
                repareaList=[]
                marketRows = db((db.sm_rep_area.cid == cid) & (db.sm_rep_area.rep_id == rep_id)).select(db.sm_rep_area.area_id, db.sm_rep_area.area_name, orderby=db.sm_rep_area.area_name, groupby=db.sm_rep_area.area_id)
                for marketRow in marketRows:
                    area_id = marketRow.area_id
                    area_name = marketRow.area_name
                    repareaList.append(area_id)
                    if marketStr == '':
                        marketStr = str(area_id) + '<fd>' + str(area_name)
                    else:
                        marketStr += '<rd>' + str(area_id) + '<fd>' + str(area_name)

               
               

#               ----------Tourplan Market-------------------------------------------    
     
                docNextMonthRow=db((db.sm_doctor_visit_plan.cid == cid) & (db.sm_doctor_visit_plan.rep_id == rep_id)  & (db.sm_doctor_visit_plan.first_date == nextMonth) ).select(db.sm_doctor_visit_plan.route_id,db.sm_doctor_visit_plan.route_name,db.sm_doctor_visit_plan.schedule_date,db.sm_doctor_visit_plan.status, groupby=db.sm_doctor_visit_plan.schedule_date|db.sm_doctor_visit_plan.route_id, orderby=db.sm_doctor_visit_plan.schedule_date|db.sm_doctor_visit_plan.route_name)
#                 return docNextMonthRow
                marketStrDocNextMonth=''
                srart_d_flag=0
                docNextMonthRowFlag=0
                pastSchDate=''
                for docNextMonthRow in docNextMonthRow:
                    route_id = docNextMonthRow.route_id
                    route_name = docNextMonthRow.route_name
                    schedule_date = docNextMonthRow.schedule_date
                    status=docNextMonthRow.status
                    
                    if (str(pastSchDate)!=str(schedule_date)):
                        if (srart_d_flag==0):
                            marketStrDocNextMonth="<"+str(schedule_date)+">"
                        else:
                            marketStrDocNextMonth=marketStrDocNextMonth+"</"+str(pastSchDate)+">"+"<"+str(schedule_date)+">"
                            srart_d_flag=0
                    if srart_d_flag == 0:
                        marketStrDocNextMonth = marketStrDocNextMonth+str(route_id) + '<fd>' + str(route_name)+ '<fd>' + str(status)
                        srart_d_flag=1
                    else:
                        marketStrDocNextMonth = marketStrDocNextMonth+'<rd>' + str(route_id) + '<fd>' + str(route_name)+ '<fd>' + str(status)
                    pastSchDate=schedule_date
                    srart_d_flag=1
#                 return marketStrDocNextMonth
#                    ======================CheckNext Approve Flag=============       
                approvedFlag=2
                NextMonthFRow=db((db.sm_doctor_visit_plan.cid == cid) & (db.sm_doctor_visit_plan.rep_id == rep_id)  & (db.sm_doctor_visit_plan.first_date == nextMonth)& (db.sm_doctor_visit_plan.status == 'Confirmed') ).select(db.sm_doctor_visit_plan.route_id,db.sm_doctor_visit_plan.route_name,db.sm_doctor_visit_plan.schedule_date,db.sm_doctor_visit_plan.status, groupby=db.sm_doctor_visit_plan.schedule_date|db.sm_doctor_visit_plan.route_id, orderby=db.sm_doctor_visit_plan.schedule_date|db.sm_doctor_visit_plan.route_name)
                if NextMonthFRow:
                    approvedFlag=1
#                  ==============================         
                          
                          
                marketTourStr=''
                marketTourRows = db((db.sm_microunion.cid==cid) &(db.sm_microunion.area_id.belongs(repareaList))).select(db.sm_microunion.microunion_id,db.sm_microunion.microunion_name, orderby=db.sm_microunion.microunion_name, groupby=db.sm_microunion.microunion_id)
#                 return db._lastsql
                for marketTourRow in marketTourRows:
                    market_id =  marketTourRow.microunion_id
                    market_name =  marketTourRow.microunion_name
                    if market_id!= None:
                        if marketTourStr == '':
                            marketTourStr = str(market_id) + '<fd>' + str(market_name)
                        else:
                            marketTourStr += '<rd>' + str(market_id) + '<fd>' + str(market_name)
                
#                 marketTourStr += '<rd>' + 'HOLIDAY' + '<fd>' + ''
#                 marketTourStr += '<rd>' + 'MEETING' + '<fd>' + ''
#                 marketTourStr += '<rd>' + 'LEAVE' + '<fd>' + ''
#                 marketTourStr += '<rd>' + 'OTHERS' + '<fd>' + ''
                
#                 ====================================================================
                

                docTThisMonthRow=db((db.sm_doctor_visit_plan.cid == cid) & (db.sm_doctor_visit_plan.rep_id == rep_id)  & (db.sm_doctor_visit_plan.first_date == first_currentDate) ).select(db.sm_doctor_visit_plan.route_id,db.sm_doctor_visit_plan.route_name,db.sm_doctor_visit_plan.schedule_date,db.sm_doctor_visit_plan.status, groupby=db.sm_doctor_visit_plan.schedule_date|db.sm_doctor_visit_plan.route_id, orderby=db.sm_doctor_visit_plan.schedule_date|db.sm_doctor_visit_plan.route_name)
                marketStrDocThisMonth=''
                srart_d_flag=0
                docTThisMonthRowFlag=0
                pastSchDate=''
                for docTThisMonthRow in docTThisMonthRow:
                    route_id = docTThisMonthRow.route_id
                    route_name = docTThisMonthRow.route_name
                    schedule_date = docTThisMonthRow.schedule_date
                    status=docTThisMonthRow.status
                    
                    if (str(pastSchDate)!=str(schedule_date)):
                        if (srart_d_flag==0):
                            marketStrDocThisMonth="<"+str(schedule_date)+">"
                        else:
                            marketStrDocThisMonth=marketStrDocThisMonth+"</"+str(pastSchDate)+">"+"<"+str(schedule_date)+">"
                            srart_d_flag=0
                    if srart_d_flag == 0:
                        marketStrDocThisMonth = marketStrDocThisMonth+str(route_id) + '<fd>' + str(route_name)+ '<fd>' + str(status)
                        srart_d_flag=1
                    else:
                        marketStrDocThisMonth = marketStrDocThisMonth+'<rd>' + str(route_id) + '<fd>' + str(route_name)+ '<fd>' + str(status)
                    pastSchDate=schedule_date
                    srart_d_flag=1
#                 return marketStrDocThisMonth
                    
#                 ------------------------------------------------------------------
#                 docTourRow=db((db.sm_doctor_visit_plan.cid == db.sm_doctor_area.cid) & (db.sm_doctor_visit_plan.route_id == db.sm_doctor_area.field1)  & (db.sm_doctor_visit_plan.rep_id == rep_id)  & (db.sm_doctor_visit_plan.status == 'Confirmed')  & (db.sm_doctor_visit_plan.schedule_date >= today)  & (db.sm_doctor_visit_plan.schedule_date < tomorrow)).select(db.sm_doctor_area.area_id,db.sm_doctor_area.area_name,db.sm_doctor_area.field1,db.sm_doctor_visit_plan.schedule_date, groupby=db.sm_doctor_area.area_id|db.sm_doctor_area.area_name, orderby=db.sm_doctor_area.area_id|db.sm_doctor_area.area_name)
                docTourRow=db((db.sm_doctor_visit_plan.cid == db.sm_microunion.cid) & (db.sm_doctor_visit_plan.route_id == db.sm_microunion.microunion_id)  & (db.sm_doctor_visit_plan.rep_id == rep_id)  & (db.sm_doctor_visit_plan.status == 'Confirmed')  & (db.sm_doctor_visit_plan.schedule_date >= today)  & (db.sm_doctor_visit_plan.schedule_date < tomorrow)).select(db.sm_microunion.area_id,db.sm_microunion.area_name,db.sm_microunion.microunion_id,db.sm_doctor_visit_plan.schedule_date, groupby=db.sm_microunion.area_id|db.sm_microunion.area_name, orderby=db.sm_microunion.area_id|db.sm_microunion.area_name)
#                 return docTourRow
                marketStrDoc=''
                for docTourRow in docTourRow:
                    route_id = docTourRow.sm_microunion.area_id
                    route_name = docTourRow.sm_microunion.area_name
                    schedule_date = docTourRow.sm_doctor_visit_plan.schedule_date
                    market=docTourRow.sm_microunion.microunion_id
    
                    if marketStrDoc == '':
                        marketStrDoc = str(route_id) + '<fd>' + str(route_name)+'[ '+str(market)+ ' ]<fd>' +str(schedule_date)
                    else:
                        marketStrDoc += '<rd>' + str(route_id) + '<fd>' + str(route_name)+'[ '+str(market)+ ' ]<fd>' +str(schedule_date)
                
#                 ===================================================================
#                 return str(approvedFlag)
                return 'SUCCESS'+'<SYNCDATA>'+str(marketStrDoc)+'<SYNCDATA>'+str(marketTourStr)+'<SYNCDATA>'+str(marketStrDocThisMonth)+'<SYNCDATA>'+str(marketStrDocNextMonth)+'<SYNCDATA>'+str(approvedFlag)

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
                    for levelRow in levelRows:
                        level_id = levelRow.level_id
                        level_name = levelRow.level_name
                        depotid = str(levelRow.depot_id).strip()
                        special_territory_code = levelRow.special_territory_code
                        if level_id==special_territory_code:
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

                
                
#                 ------------------------------------------
                
                docNextMonthRow=db((db.sm_doctor_visit_plan.cid == cid) & (db.sm_doctor_visit_plan.rep_id == rep_id)  & (db.sm_doctor_visit_plan.first_date == nextMonth) ).select(db.sm_doctor_visit_plan.route_id,db.sm_doctor_visit_plan.route_name,db.sm_doctor_visit_plan.schedule_date,db.sm_doctor_visit_plan.status, groupby=db.sm_doctor_visit_plan.schedule_date|db.sm_doctor_visit_plan.route_id, orderby=db.sm_doctor_visit_plan.schedule_date|db.sm_doctor_visit_plan.route_name)
                marketStrDocNextMonth=''
                srart_d_flag=0
                docNextMonthRowFlag=0
                pastSchDate=''
                for docNextMonthRow in docNextMonthRow:
                    route_id = docNextMonthRow.route_id
                    route_name = docNextMonthRow.route_name
                    schedule_date = docNextMonthRow.schedule_date
                    status=docNextMonthRow.status
                    
                    if (str(pastSchDate)!=str(schedule_date)):
                        if (srart_d_flag==0):
                            marketStrDocNextMonth="<"+str(schedule_date)+">"
                        else:
                            marketStrDocNextMonth=marketStrDocNextMonth+"</"+str(pastSchDate)+">"+"<"+str(schedule_date)+">"
                            srart_d_flag=0
                    if srart_d_flag == 0:
                        marketStrDocNextMonth = marketStrDocNextMonth+str(route_id) + '<fd>' + str(route_name)+ '<fd>' + str(status)
                        srart_d_flag=1
                    else:
                        marketStrDocNextMonth = marketStrDocNextMonth+'<rd>' + str(route_id) + '<fd>' + str(route_name)+ '<fd>' + str(status)
                    pastSchDate=schedule_date
                    srart_d_flag=1
                
                
                approvedFlag=2
                NextMonthFRow=db((db.sm_doctor_visit_plan.cid == cid) & (db.sm_doctor_visit_plan.rep_id == rep_id)  & (db.sm_doctor_visit_plan.first_date == nextMonth)& (db.sm_doctor_visit_plan.status == 'Confirmed') ).select(db.sm_doctor_visit_plan.route_id,db.sm_doctor_visit_plan.route_name,db.sm_doctor_visit_plan.schedule_date,db.sm_doctor_visit_plan.status, groupby=db.sm_doctor_visit_plan.schedule_date|db.sm_doctor_visit_plan.route_id, orderby=db.sm_doctor_visit_plan.schedule_date|db.sm_doctor_visit_plan.route_name)
                if NextMonthFRow:
                    approvedFlag=1
#                  ==============================      
                
                
                marketTourStr=''
#                 marketTourRows = db((db.sm_rep_area.cid == db.sm_depot_market.cid) &(db.sm_doctor_area.cid == db.sm_depot_market.cid)&(db.sm_doctor_area.area_id == db.sm_rep_area.area_id) & (db.sm_rep_area.rep_id == rep_id) & (db.sm_doctor_area.field1 == db.sm_depot_market.market_id)).select(db.sm_depot_market.market_id, db.sm_depot_market.market_name, orderby=db.sm_depot_market.market_name, groupby=db.sm_depot_market.market_id)
#                 marketTourRows = db((db.sm_doctor_area.cid==cid) &(db.sm_doctor_area.area_id.belongs(marketList))).select(db.sm_doctor_area.field1,db.sm_doctor_area.note, orderby=db.sm_doctor_area.note, groupby=db.sm_doctor_area.field1)

                marketTourRows = db((db.sm_microunion.cid==cid) &(db.sm_microunion.area_id.belongs(marketList))).select(db.sm_microunion.microunion_id,db.sm_microunion.microunion_name, orderby=db.sm_microunion.microunion_name, groupby=db.sm_microunion.microunion_id)
                
                
                
                
                for marketTourRow in marketTourRows:
                    market_id =  marketTourRow.microunion_id
                    market_name =  marketTourRow.microunion_name
                    if market_id!= None:
                        if marketTourStr == '':
                            marketTourStr = str(market_id) + '<fd>' + str(market_name)
                        else:
                            marketTourStr += '<rd>' + str(market_id) + '<fd>' + str(market_name)
#                 marketTourStr += '<rd>' + 'HOLIDAY' + '<fd>' + ''
#                 marketTourStr += '<rd>' + 'MEETING' + '<fd>' + ''
#                 marketTourStr += '<rd>' + 'LEAVE' + '<fd>' + ''
#                 marketTourStr += '<rd>' + 'OTHERS' + '<fd>' + ''            
                 
#                 return marketTourStr


                docTThisMonthRow=db((db.sm_doctor_visit_plan.cid == cid) & (db.sm_doctor_visit_plan.rep_id == rep_id)  & (db.sm_doctor_visit_plan.first_date == first_currentDate) & ((db.sm_doctor_visit_plan.status == 'CReq') | (db.sm_doctor_visit_plan.status == 'Confirmed'))).select(db.sm_doctor_visit_plan.route_id,db.sm_doctor_visit_plan.route_name,db.sm_doctor_visit_plan.schedule_date,db.sm_doctor_visit_plan.status, groupby=db.sm_doctor_visit_plan.schedule_date|db.sm_doctor_visit_plan.route_id, orderby=db.sm_doctor_visit_plan.schedule_date|db.sm_doctor_visit_plan.route_name)
#                 return docTThisMonthRow
                marketStrDocThisMonth=''
                srart_d_flag=0
                docTThisMonthRowFlag=0
                pastSchDate=''
                for docTThisMonthRow in docTThisMonthRow:
                    route_id = docTThisMonthRow.route_id
                    route_name = docTThisMonthRow.route_name
                    schedule_date = docTThisMonthRow.schedule_date
                    status=docTThisMonthRow.status
                    
                    if (str(pastSchDate)!=str(schedule_date)):
                        if (srart_d_flag==0):
                            marketStrDocThisMonth="<"+str(schedule_date)+">"
                        else:
                            marketStrDocThisMonth=marketStrDocThisMonth+"</"+str(pastSchDate)+">"+"<"+str(schedule_date)+">"
                            srart_d_flag=0
                    if srart_d_flag == 0:
                        marketStrDocThisMonth = marketStrDocThisMonth+str(route_id) + '<fd>' + str(route_name)+ '<fd>' + str(status)
                        srart_d_flag=1
                    else:
                        marketStrDocThisMonth = marketStrDocThisMonth+'<rd>' + str(route_id) + '<fd>' + str(route_name)+ '<fd>' + str(status)
                    pastSchDate=schedule_date
                    srart_d_flag=1
#                 return marketStrDocThisMonth
                    
#                 ------------------------------------------------------------------
                
                docTourRow=db((db.sm_doctor_visit_plan.cid == db.sm_microunion.cid) & (db.sm_doctor_visit_plan.route_id == db.sm_microunion.microunion_id)  & (db.sm_doctor_visit_plan.rep_id == rep_id)  & (db.sm_doctor_visit_plan.status == 'Confirmed')  & (db.sm_doctor_visit_plan.schedule_date >= today)  & (db.sm_doctor_visit_plan.schedule_date < tomorrow)).select(db.sm_microunion.area_id,db.sm_microunion.area_name,db.sm_microunion.microunion_id,db.sm_doctor_visit_plan.schedule_date, groupby=db.sm_microunion.area_id|db.sm_microunion.area_name, orderby=db.sm_microunion.area_id|db.sm_microunion.area_name)
#                 return db._lastsql
                marketStrDoc=''
                for docTourRow in docTourRow:
                    route_id = docTourRow.sm_microunion.area_id
                    route_name = docTourRow.sm_microunion.area_name
                    schedule_date = docTourRow.sm_doctor_visit_plan.schedule_date
                    market=docTourRow.sm_microunion.microunion_id
     
                    if marketStrDoc == '':
                        marketStrDoc = str(route_id) + '<fd>' + str(route_name)+'[ '+str(market)+ ' ]<fd>' +str(schedule_date)
                    else:
                        marketStrDoc += '<rd>' + str(route_id) + '<fd>' + str(route_name)+'[ '+str(market)+ ' ]<fd>' +str(schedule_date)
                
#                 ===================================================================
  
                return 'SUCCESS'+'<SYNCDATA>'+str(marketStrDoc)+'<SYNCDATA>'+str(marketTourStr)+'<SYNCDATA>'+str(marketStrDocThisMonth)+'<SYNCDATA>'+str(marketStrDocNextMonth)+'<SYNCDATA>'+str(approvedFlag)
                
            else:
                return 'FAILED<SYNCDATA>Invalid Authorization'     

def prescription_submit():
    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = urllib.unquote(str(request.vars.rep_pass).strip().decode('utf8'))
    synccode = str(request.vars.synccode).strip()
    campaign_doc_str = str(request.vars.campaign_doc_str).strip()
    op_doc_str = str(request.vars.opProdID_Str).strip()
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
        tl_id= areaRow[0].level2
        tl_name= areaRow[0].level2_name
        reg_id= areaRow[0].level1
        reg_name= areaRow[0].level1_name
            
            
    compRow = db((db.sm_company_settings.cid == cid) & (db.sm_company_settings.status == 'ACTIVE')).select(db.sm_company_settings.cid, limitby=(0, 1))
    if not compRow:
        return 'FAILED<SYNCDATA>Invalid Company'
    else:
        repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.sync_code == synccode) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.rep_id, db.sm_rep.name, db.sm_rep.mobile_no, db.sm_rep.user_type, db.sm_rep.level_id, limitby=(0, 1))
#         return db._lastsql
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
                item_id = campaign_doc_strList[i].split('<||>')[0]
                item_name = campaign_doc_strList[i].split('<||>')[1]
                campaignArrayList.append({'cid':cid, 'sl':sl, 'medicine_id':item_id, 'medicine_name':item_name,'submit_date':submit_date,'first_date':firstDate,'submit_by_id':rep_id, 'submit_by_name':rep_name, 'user_type':user_type, 'doctor_id':doctor_id ,'doctor_name':doctor_name})
            if len(campaignArrayList) > 0:
                    db.sm_prescription_details.bulk_insert(campaignArrayList)    
                    dateRecords="update sm_item_prescription,sm_prescription_details set  sm_prescription_details.medicine_name=sm_item_prescription.name, sm_prescription_details.med_type=sm_item_prescription.item_identity WHERE sm_prescription_details.cid = '"+ cid +"' AND  sm_prescription_details.cid = '"+ cid + "' AND sm_prescription_details.medicine_id=sm_item_prescription.item_id AND sm_prescription_details.medicine_name='' AND sm_prescription_details.med_type='' ;"
                    records=db.executesql(dateRecords) 
                    
                    
            
            op_doc_strList=op_doc_str.split('<rd>')
            opArrayList = []
            for i in range(len(op_doc_strList)):  
                op_item_id = op_doc_strList[i]
                opArrayList.append({'cid':cid, 'sl':sl, 'medicine_id':op_item_id,'med_type':'OPPERTUNETY'})
            if len(opArrayList) > 0:
                    db.sm_prescription_details.bulk_insert(opArrayList)    
                    opRecords="update sm_item_prescription,sm_prescription_details set  sm_prescription_details.medicine_name=sm_item_prescription.name WHERE sm_prescription_details.cid = '"+ cid +"' AND  sm_prescription_details.cid = '"+ cid + "' AND sm_prescription_details.medicine_id=sm_item_prescription.item_id AND sm_prescription_details.medicine_name='' AND sm_prescription_details.med_type='OPPERTUNETY' ;"
                    records=db.executesql(opRecords)         
            #----------------
            #----------------
#             return medicine_1
            if medicine_1!='':
                db.sm_prescription_details.insert(cid=cid, sl=sl, medicine_name=medicine_1, med_type='OTHER')
            if medicine_2!='':
                db.sm_prescription_details.insert(cid=cid, sl=sl, medicine_name=medicine_2, med_type='OTHER')
            if medicine_3!='':
                db.sm_prescription_details.insert(cid=cid, sl=sl, medicine_name=medicine_3, med_type='OTHER')
                db((db.sm_prescription_head.cid == cid) & (db.sm_prescription_head.sl == sl) & (db.sm_prescription_head.submit_date == submit_date)).update(field1=medicine_3)
            if medicine_4!='':
                db.sm_prescription_details.insert(cid=cid, sl=sl, medicine_name=medicine_4, med_type='OTHER')
            if medicine_5!='':
                db.sm_prescription_details.insert(cid=cid, sl=sl, medicine_name=medicine_5, med_type='OTHER')
            
            
            return 'SUCCESS<SYNCDATA>'  
        
# =================Doctor Sync=======================        
def doctor_sync():
    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.rep_pass).strip()
    synccode = str(request.vars.synccode).strip()
    sync_code=synccode
    productStr=''
    merchandizingStr=''
    dealerStr=''
    brandStr=''
    marketStr =''
    complainTypeStr =''
    compFromStr =''
    taskTypeStr =''
    regionStr =''
    giftStr =''
    clienttCatStr =''
    clientStr =''
    menuStr =''
    ppmStr ='' 
    user_type=''
    doctorStr =''
    visit_save_limit=''
    visit_location=''
    delivery_date=''
    payment_date=''
    payment_mode=''
    collection_date=''
    promo_str=''
    client_depot=''
    cliendepot_name=''
    catStr=''
    spcStr=''
    marketStrCteam=''

    cTeam=''
    marketStrDoc=''
    marketTourStr=''
    marketStrDocThisMonth=''
    prProductStr=''
    compRow = db((db.sm_company_settings.cid == cid) & (db.sm_company_settings.status == 'ACTIVE')).select(db.sm_company_settings.cid, limitby=(0, 1))
    if not compRow:
        return 'FAILED<SYNCDATA>Invalid Company'
    else:
        repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.sync_code == synccode) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.rep_id, db.sm_rep.name, db.sm_rep.mobile_no, db.sm_rep.user_type, db.sm_rep.level_id, limitby=(0, 1))
#         return db._lastsql
        if not repRow:
           return 'FAILED<SYNCDATA>Invalid Authorization'
        else:
            user_type = repRow[0].user_type
            
        doctor_area_past=''
        srart_a_flag=0
        doctorStr_flag=0
        if (user_type == 'rep'):
            repareaList=[]

            marketTourRows = db((db.sm_rep_area.cid == cid) & (db.sm_rep_area.rep_id == rep_id) ).select(db.sm_rep_area.area_id, orderby=db.sm_rep_area.area_id, groupby=db.sm_rep_area.area_id)
#             return marketTourRows
#             return db._lastsql
            doctorStr = ''
            
            srart_a_flag=0
            doctorStr_flag=0
            
            for marketRow_1 in marketTourRows:
                area_id = marketRow_1.area_id
                repareaList.append(area_id)
                
#             doctorRows = db((db.sm_doctor.cid == cid) & (db.sm_doctor.status == 'ACTIVE') & (db.sm_doctor_area.cid == cid) & (db.sm_doctor_area.doc_id == db.sm_doctor.doc_id)  & (db.sm_doctor_area.field1.belongs(repareaList)) ).select(db.sm_doctor.doc_id, db.sm_doctor.doc_name, db.sm_doctor_area.field1, orderby=db.sm_doctor_area.field1|db.sm_doctor.doc_name)
            doctorRows = db((db.sm_doctor_area.cid == cid)   & (db.sm_doctor_area.area_id.belongs(repareaList))  ).select(db.sm_doctor_area.doc_id, db.sm_doctor_area.doc_name, db.sm_doctor_area.area_id, orderby=db.sm_doctor_area.area_id|db.sm_doctor_area.doc_name)
#             return db._lastsql
#                 return doctorRows
            if not doctorRows:
                pass
            else:
                for doctorRow in doctorRows:
                    doctor_id = doctorRow.doc_id
                    doctor_name = doctorRow.doc_name
                    doctor_area = doctorRow.area_id
#                     doctor_id = doctorRow.sm_doctor_area.doc_id
#                     doctor_name = doctorRow.sm_doctor_area.doc_name
#                     doctor_area = doctorRow.sm_doctor_area.field1
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
#                       return doctorStr
            if (doctorStr!=''):
                doctorStr=doctorStr+ "</"+doctor_area+">"
#                 return doctorStr
#             ----------------------------Doctor list end----------------------------------


            return 'SUCCESS<SYNCDATA>' + str(doctorStr)


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
#                 --------------------------------Menu List End--------------------------------------

#                ----------------------------Doctor list start-----------------------
            
            doctorStr = ''
            srart_a_flag=0
#                 doctor_area_past=''
#                 srart_a_flag=0
#                 doctorStr_flag=0

            for i in range(len(marketList)):
                area_id = marketList[i]
#                         return area_id
                doctorRows = db((db.sm_doctor_area.cid == cid) & (db.sm_doctor_area.doc_id == db.sm_doctor.doc_id) & (db.sm_doctor_area.area_id==area_id)).select(db.sm_doctor.doc_id, db.sm_doctor.doc_name, db.sm_doctor_area.area_id, orderby=db.sm_doctor_area.area_id|db.sm_doctor.doc_name)
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
    
#                return 'SUCCESS<SYNCDATA>' + str(sync_code) + '<SYNCDATA>' + marketStr + '<SYNCDATA>' + productStr + '<SYNCDATA>' + merchandizingStr + '<SYNCDATA>' + dealerStr + '<SYNCDATA>' + brandStr + '<SYNCDATA>' + complainTypeStr + '<SYNCDATA>' + compFromStr + '<SYNCDATA>' + taskTypeStr + '<SYNCDATA>' + regionStr + '<SYNCDATA>' + giftStr + '<SYNCDATA>' + clienttCatStr + '<SYNCDATA>' + menuStr
            
            
            #                 ====================================================================
            
#                 return first_currentDate
            #               ----------Tourplan Market-------------------------------------------              
            marketTourStr=''
#                 marketTourRows = db((db.sm_rep_area.cid == db.sm_depot_market.cid) &(db.sm_doctor_area.cid == db.sm_depot_market.cid)&(db.sm_doctor_area.area_id == db.sm_rep_area.area_id) & (db.sm_rep_area.rep_id == rep_id) & (db.sm_doctor_area.field1 == db.sm_depot_market.market_id)).select(db.sm_depot_market.market_id, db.sm_depot_market.market_name, orderby=db.sm_depot_market.market_name, groupby=db.sm_depot_market.market_id)
            marketTourRows = db((db.sm_doctor_area.cid==cid) &(db.sm_doctor_area.area_id.belongs(marketList))).select(db.sm_doctor_area.field1,db.sm_doctor_area.note, orderby=db.sm_doctor_area.note, groupby=db.sm_doctor_area.field1)


            

            return 'SUCCESS<SYNCDATA>' + str(doctorStr)#+ str(sync_code) + '<SYNCDATA>' + marketStr + '<SYNCDATA>' + productStr + '<SYNCDATA>' + merchandizingStr + '<SYNCDATA>' + dealerStr + '<SYNCDATA>' + brandStr + '<SYNCDATA>' + complainTypeStr + '<SYNCDATA>' + compFromStr + '<SYNCDATA>' + taskTypeStr + '<SYNCDATA>' + regionStr + '<SYNCDATA>' + giftStr + '<SYNCDATA>' + clienttCatStr + '<SYNCDATA>' + clientStr + '<SYNCDATA>' + menuStr+ '<SYNCDATA>' +ppmStr + '<SYNCDATA>' + user_type+ '<SYNCDATA>' +doctorStr + '<SYNCDATA>' +str(visit_save_limit)+'<SYNCDATA>'+str(visit_location)+'<SYNCDATA>'+str(delivery_date)+'<SYNCDATA>'+str(payment_date)+'<SYNCDATA>'+str(payment_mode)+'<SYNCDATA>'+str(collection_date)+'<SYNCDATA>'+str(promo_str)+'<SYNCDATA>'+str(client_depot)+'<SYNCDATA>'+str(cliendepot_name)+'<SYNCDATA>'+str(catStr)+'<SYNCDATA>'+str(spcStr)+'<SYNCDATA>'+str(marketStrCteam)+'<SYNCDATA>'+str(cTeam)+'<SYNCDATA>'+str(marketStrDoc)+'<SYNCDATA>'+str(marketTourStr)+'<SYNCDATA>'+str(marketStrDocThisMonth)+'<SYNCDATA>'+str(prProductStr)
            
        else:
            return 'FAILED<SYNCDATA>Invalid Authorization'
# ===============================        
def report_summary_doctor_tr():
    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.rep_pass).strip()
    synccode = str(request.vars.synccode).strip()
    
    rep_id_report = str(request.vars.rep_id_report).strip().upper()
    
    se_market_report = str(request.vars.se_market_report).strip().upper()
    user_type = str(request.vars.user_type).strip().upper()
    
    date_year = str(request.vars.date_year).strip().upper()
    date_month = str(request.vars.date_month).strip().upper()
    year_month=str(date_year)+'-'+str(date_month)

    repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.sync_code == synccode) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.id,db.sm_rep.user_type,db.sm_rep.level_id,db.sm_rep.field2, limitby=(0, 1))

#    return db._lastsql
   
    level_rep=''
    
    if not repRow:
       retStatus = 'FAILED<SYNCDATA>Invalid Authorization'
       return retStatus
    else:
       pass

    recRep=db((db.sm_doc_visit_report.cid == cid) & (db.sm_doc_visit_report.y_month == year_month)  & (db.sm_doc_visit_report.tr==se_market_report)).select(db.sm_doc_visit_report.ALL, orderby=db.sm_doc_visit_report.tr)
    
    
    recordDoc=db((db.sm_doctor_area.cid == cid) & (db.sm_doc_visit_report.cid == cid)  & (db.sm_doctor_area.doc_id!=db.sm_doc_visit_report.doc)  & (db.sm_doctor_area.area_id==se_market_report)).select(db.sm_doctor_area.doc_id,db.sm_doctor_area.doc_name, orderby=db.sm_doctor_area.doc_name , groupby=db.sm_doctor_area.doc_id)

    
    recRepDoc=db((db.sm_doctor_area.cid == cid) & (db.sm_doctor_area.area_id == se_market_report)).select(db.sm_doctor_area.id.count(), limitby=(0,1))
    docTr=0
    if recRepDoc:
        docTr=recRepDoc[0][db.sm_doctor_area.id.count()]
#     return recRep

#         return db._lastsql
    
    flagRep=0
    reportShow=''
    reportShowHead=''
    docCunt=0
    totalVisit=0
    for recRep in recRep:
        docCunt=docCunt+1
        total=0
#         total=int(recRep.d_1)+int(recRep.d_2)+int(recRep.d_3)+int(recRep.d_4)+int(recRep.d_5)+int(recRep.d_6)+int(recRep.d_7)+int(recRep.d_8)+int(recRep.d_9)+int(recRep.d_10)+int(recRep.d_11)+int(recRep.d_12)+int(recRep.d_13)+int(recRep.d_14)+int(recRep.d_15)+int(recRep.d_16)+int(recRep.d_17)+int(recRep.d_18)+int(recRep.d_19)+int(recRep.d_20)+int(recRep.d_21)+int(recRep.d_22)+int(recRep.d_23)+int(recRep.d_24)+int(recRep.d_25)+int(recRep.d_26)+int(recRep.d_27)+int(recRep.d_28)+int(recRep.d_29)+int(recRep.d_30)+int(recRep.d_31)
        
        d_1=' '
        d_2=' '
        d_3=' '
        d_4=' '
        d_5=' '
        d_6=' '
        d_7=' '
        d_8=' '
        d_9=' '
        d_10=' '
        d_11=' '
        d_12=' '
        d_13=' '
        d_14=' '
        d_15=' '
        d_16=' '
        d_17=' '
        d_18=' '
        d_19=' '
        d_20=' '
        d_21=' '
        d_22=' '
        d_23=' '
        d_24=' '
        d_25=' '
        d_26=' '
        d_27=' '
        d_28=' '
        d_29=' '
        d_30=' '
        d_31=' '
        if int(recRep.d_1)>0: d_1='Y';total=total+1;totalVisit=totalVisit+1;
        if int(recRep.d_2)>0: d_2='Y';total=total+1;totalVisit=totalVisit+1;
        if int(recRep.d_3)>0: d_3='Y';total=total+1;totalVisit=totalVisit+1;
        if int(recRep.d_4)>0: d_4='Y';total=total+1;totalVisit=totalVisit+1;
        if int(recRep.d_5)>0: d_5='Y';total=total+1;totalVisit=totalVisit+1;
        if int(recRep.d_6)>0: d_6='Y';total=total+1;totalVisit=totalVisit+1;
        if int(recRep.d_7)>0: d_7='Y';total=total+1;totalVisit=totalVisit+1;
        if int(recRep.d_8)>0: d_8='Y';total=total+1;totalVisit=totalVisit+1;
        if int(recRep.d_9)>0: d_9='Y';total=total+1;totalVisit=totalVisit+1;
        if int(recRep.d_10)>0: d_10='Y';total=total+1;totalVisit=totalVisit+1;
        if int(recRep.d_11)>0: d_11='Y';total=total+1;totalVisit=totalVisit+1;
        if int(recRep.d_12)>0: d_12='Y';total=total+1;totalVisit=totalVisit+1;
        if int(recRep.d_13)>0: d_13='Y';total=total+1;totalVisit=totalVisit+1;
        if int(recRep.d_14)>0: d_14='Y';total=total+1;totalVisit=totalVisit+1;
        if int(recRep.d_15)>0: d_15='Y';total=total+1;totalVisit=totalVisit+1;
        if int(recRep.d_16)>0: d_16='Y';total=total+1;totalVisit=totalVisit+1;
        if int(recRep.d_17)>0: d_17='Y';total=total+1;totalVisit=totalVisit+1;
        if int(recRep.d_18)>0: d_18='Y';total=total+1;totalVisit=totalVisit+1;
        if int(recRep.d_19)>0: d_19='Y';total=total+1;totalVisit=totalVisit+1;
        if int(recRep.d_20)>0: d_20='Y';total=total+1;totalVisit=totalVisit+1;
        if int(recRep.d_21)>0: d_21='Y';total=total+1;totalVisit=totalVisit+1;
        if int(recRep.d_22)>0: d_22='Y';total=total+1;totalVisit=totalVisit+1;
        if int(recRep.d_23)>0: d_23='Y';total=total+1;totalVisit=totalVisit+1;
        if int(recRep.d_24)>0: d_24='Y';total=total+1;totalVisit=totalVisit+1;
        if int(recRep.d_25)>0: d_25='Y';total=total+1;totalVisit=totalVisit+1;
        if int(recRep.d_26)>0: d_26='Y';total=total+1;totalVisit=totalVisit+1;
        if int(recRep.d_27)>0: d_27='Y';total=total+1;totalVisit=totalVisit+1;
        if int(recRep.d_28)>0: d_28='Y';total=total+1;totalVisit=totalVisit+1;
        if int(recRep.d_29)>0: d_29='Y';total=total+1;totalVisit=totalVisit+1;
        if int(recRep.d_30)>0: d_30='Y';total=total+1;totalVisit=totalVisit+1;
        if int(recRep.d_31)>0: d_31='Y';total=total+1;totalVisit=totalVisit+1;
        
        
           
        if flagRep==0:
            rsm='<font style="font-size:16px">RSM: </font>'+str(recRep.rsm_name)+' | '+str(recRep.rsm_id)
            fm='<font style="font-size:16px">FM: </font>'+str(recRep.fm_name)+' | '+str(recRep.fm_id)
            tr='<font style="font-size:16px">TR: </font>'+str(recRep.tr_name)+' | '+str(recRep.tr)
            reportShowHead=rsm+'<br>'+fm+'<br>'+tr+'<br><br>'
            
            
            reportShow=reportShow+'<table width="100%" border="1" cellpadding="0" cellspacing="0">'
            reportShow=reportShow+'<tr>'+'<td style="background-color:transparent">Doctor</td>'+'<td style="background-color:transparent">DoctorName</td>'+'<td>01</td>'+'<td>02</td>'+'<td>03</td>'+'<td>04</td>'+'<td>05</td>'+'<td>06</td>'+'<td>07</td>'+'<td>08</td>'+'<td>09</td>'+'<td>10</td>'+'<td>11</td>'+'<td>12</td>'+'<td>13</td>'+'<td>14</td>'+'<td>15</td>'+'<td>16</td>'+'<td>17</td>'+'<td>18</td>'+'<td>19</td>'+'<td>20</td>'+'<td>21</td>'+'<td>22</td>'+'<td>23</td>'+'<td>24</td>'+'<td>25</td>'+'<td>26</td>'+'<td>27</td>'+'<td>28</td>'+'<td>29</td>'+'<td>30</td>'+'<td>31</td>'+'<td style="background-color:transparent">Total</td>'+'</tr>'
            flagRep=1
        
        
        
        reportShow=reportShow+'<tr>'
        reportShow=reportShow+'<td style="background-color:transparent">'+str(recRep.doc)+'</td>'+'<td style="background-color:transparent">'+str(recRep.doc_name)+'</td>'+'<td>'+str(d_1)+'</td>'+'<td>'+str(d_2)+'</td>'+'<td>'+str(d_3)+'</td>'+'<td>'+str(d_4)+'</td>'+'<td>'+str(d_5)+'</td>'+'<td>'+str(d_6)+'</td>'+'<td>'+str(d_7)+'</td>'+'<td>'+str(d_8)+'</td>'+'<td>'+str(d_9)+'</td>'+'<td>'+str(d_10)+'</td>'+'<td>'+str(d_11)+'</td>'+'<td>'+str(d_12)+'</td>'+'<td>'+str(d_13)+'</td>'+'<td>'+str(d_14)+'</td>'+'<td>'+str(d_15)+'</td>'+'<td>'+str(d_16)+'</td>'+'<td>'+str(d_17)+'</td>'+'<td>'+str(d_18)+'</td>'+'<td>'+str(d_19)+'</td>'+'<td>'+str(d_20)+'</td>'+'<td>'+str(d_21)+'</td>'+'<td>'+str(d_22)+'</td>'+'<td>'+str(d_23)+'</td>'+'<td>'+str(d_24)+'</td>'+'<td>'+str(d_25)+'</td>'+'<td>'+str(d_26)+'</td>'+'<td>'+str(d_27)+'</td>'+'<td>'+str(d_28)+'</td>'+'<td>'+str(d_29)+'</td>'+'<td>'+str(d_30)+'</td>'+'<td>'+str(d_31)+'</td>'+'<td style="background-color:transparent">'+str(total)+'</td>'
        reportShow=reportShow+'</tr>'
#             return total
#         reportShow=reportShow+'<tr>'
#         reportShow=reportShow+'<td>'+str(recRep.rsm_id)+'<td>'+str(recRep.rsm_name)+'</td>'+'<td>'+str(recRep.fm_id)+'<td>'+str(recRep.fm_name)+'</td>'+'<td>'+str(recRep.tr)+'<td>'+str(recRep.tr_name)+'</td>'+'<td>'+str(recRep.doc)+'<td>'+str(recRep.doc_name)+'</td>'+'<td>'+str(recRep.d_1)+'</td>'+'<td>'+str(recRep.d_2)+'</td>'+'<td>'+str(recRep.d_3)+'</td>'+'<td>'+str(recRep.d_4)+'</td>'+'<td>'+str(recRep.d_5)+'</td>'+'<td>'+str(recRep.d_6)+'</td>'+'<td>'+str(recRep.d_7)+'</td>'+'<td>'+str(recRep.d_8)+'</td>'+'<td>'+str(recRep.d_9)+'</td>'+'<td>'+str(recRep.d_10)+'</td>'+'<td>'+str(recRep.d_11)+'</td>'+'<td>'+str(recRep.d_12)+'</td>'+'<td>'+str(recRep.d_13)+'</td>'+'<td>'+str(recRep.d_14)+'</td>'+'<td>'+str(recRep.d_15)+'</td>'+'<td>'+str(recRep.d_16)+'</td>'+'<td>'+str(recRep.d_17)+'</td>'+'<td>'+str(recRep.d_18)+'</td>'+'<td>'+str(recRep.d_19)+'</td>'+'<td>'+str(recRep.d_20)+'</td>'+'<td>'+str(recRep.d_21)+'</td>'+'<td>'+str(recRep.d_22)+'</td>'+'<td>'+str(recRep.d_23)+'</td>'+'<td>'+str(recRep.d_24)+'</td>'+'<td>'+str(recRep.d_25)+'</td>'+'<td>'+str(recRep.d_26)+'</td>'+'<td>'+str(recRep.d_27)+'</td>'+'<td>'+str(recRep.d_28)+'</td>'+'<td>'+str(recRep.d_29)+'</td>'+'<td>'+str(recRep.d_30)+'</td>'+'<td>'+str(recRep.d_31)+'</td>'+'<td>'+str(total)+'</td>'
#         reportShow=reportShow+'</tr>'
    
    
    
    for x in range(len(recordDoc)): 
        recordD=recordDoc[x]  
        reportShow=reportShow+'<tr>'
        reportShow=reportShow+'<td style="background-color:transparent">'+str(recordD["doc_id"])+'</td>'+'<td style="background-color:transparent">'+str(recordD["doc_name"])+'</td>'+'<td></td>'+'<td></td>'+'<td></td>'+'<td></td>'+'<td></td>'+'<td></td>'+'<td></td>'+'<td></td>'+'<td></td>'+'<td></td>'+'<td></td>'+'<td></td>'+'<td></td>'+'<td></td>'+'<td></td>'+'<td></td>'+'<td></td>'+'<td></td>'+'<td></td>'+'<td></td>'+'<td></td>'+'<td></td>'+'<td></td>'+'<td></td>'+'<td></td>'+'<td></td>'+'<td></td>'+'<td></td>'+'<td></td>'+'<td></td>'+'<td></td>'+'<td style="background-color:transparent">0</td>'
        reportShow=reportShow+'</tr>'
        
    
    
    reportShow=reportShow+'</table>'
    
    reportShowfinal=reportShowHead+'<font style="font-size:14px; color:#fff">Number of Doctors in this territory: </font><font style="font-size:14px; color:#cceaab">'+str(docTr)+'</font><br><font style="font-size:14px; color:#fff">Number of Doctors visited in this territory: </font><font style="font-size:14px; color:#cceaab">'+str(docCunt)+'</font><br><font style="font-size:14px; color:#fff">Total number of Doctor Visit: </font><font style="font-size:14px; color:#cceaab">'+str(totalVisit)+'</font>'+reportShow
    
    
    return 'SUCCESS<SYNCDATA>'+reportShowfinal



def report_summary_ord_tr():
    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.rep_pass).strip()
    synccode = str(request.vars.synccode).strip()
    
    rep_id_report = str(request.vars.rep_id_report).strip().upper()
    
    se_market_report = str(request.vars.se_market_report).strip().upper()
    user_type = str(request.vars.user_type).strip().upper()
    
    date_year = str(request.vars.date_year).strip().upper()
    date_month = str(request.vars.date_month).strip().upper()
    year_month=str(date_year)+'-'+str(date_month)

    repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.sync_code == synccode) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.id,db.sm_rep.user_type,db.sm_rep.level_id,db.sm_rep.field2, limitby=(0, 1))

#    return db._lastsql
   
    level_rep=''
    
    if not repRow:
       retStatus = 'FAILED<SYNCDATA>Invalid Authorization'
       return retStatus
    else:
       pass
   
    
#     =========================================
    recRep=db((db.sm_client_visit_report.cid == cid) & (db.sm_client_visit_report.y_month == year_month)  & (db.sm_client_visit_report.tr==se_market_report)).select(db.sm_client_visit_report.ALL, orderby=db.sm_client_visit_report.tr)
    
    

    
    recordDocStr="Select client_id, name FROM sm_client where client_id NOT IN ( Select client_id from sm_client_visit_report where tr ='"+str(se_market_report)+"' and y_month='"+str(year_month)+"') and area_id='"+str(se_market_report)+"'"
    recordDoc=db.executesql(recordDocStr,as_dict = True)
    
    recRepDoc=db((db.sm_client.cid == cid) & (db.sm_client.area_id == se_market_report)).select(db.sm_client.id.count(), limitby=(0,1))
    docTr=0
    if recRepDoc:
        docTr=recRepDoc[0][db.sm_client.id.count()]
    flagRep=0
    reportShow=''
    reportShowHead=''
    reportShowfinal=''
    docCunt=0
    totalVisit=0
    reportShow=reportShow+'<table width="100%" border="1" cellpadding="0" cellspacing="0">'
    reportShow=reportShow+'<tr>'+'<td style="background-color:transparent">Client</td>'+'<td style="background-color:transparent">ClientName</td>'+'<td>01</td>'+'<td>02</td>'+'<td>03</td>'+'<td>04</td>'+'<td>05</td>'+'<td>06</td>'+'<td>07</td>'+'<td>08</td>'+'<td>09</td>'+'<td>10</td>'+'<td>11</td>'+'<td>12</td>'+'<td>13</td>'+'<td>14</td>'+'<td>15</td>'+'<td>16</td>'+'<td>17</td>'+'<td>18</td>'+'<td>19</td>'+'<td>20</td>'+'<td>21</td>'+'<td>22</td>'+'<td>23</td>'+'<td>24</td>'+'<td>25</td>'+'<td>26</td>'+'<td>27</td>'+'<td>28</td>'+'<td>29</td>'+'<td>30</td>'+'<td>31</td>'+'<td style="background-color:transparent">Total</td>'+'</tr>'
    for recRep in recRep:
        docCunt=docCunt+1
        total=0
#         total=int(recRep.d_1)+int(recRep.d_2)+int(recRep.d_3)+int(recRep.d_4)+int(recRep.d_5)+int(recRep.d_6)+int(recRep.d_7)+int(recRep.d_8)+int(recRep.d_9)+int(recRep.d_10)+int(recRep.d_11)+int(recRep.d_12)+int(recRep.d_13)+int(recRep.d_14)+int(recRep.d_15)+int(recRep.d_16)+int(recRep.d_17)+int(recRep.d_18)+int(recRep.d_19)+int(recRep.d_20)+int(recRep.d_21)+int(recRep.d_22)+int(recRep.d_23)+int(recRep.d_24)+int(recRep.d_25)+int(recRep.d_26)+int(recRep.d_27)+int(recRep.d_28)+int(recRep.d_29)+int(recRep.d_30)+int(recRep.d_31)
        
        d_1=' '
        d_2=' '
        d_3=' '
        d_4=' '
        d_5=' '
        d_6=' '
        d_7=' '
        d_8=' '
        d_9=' '
        d_10=' '
        d_11=' '
        d_12=' '
        d_13=' '
        d_14=' '
        d_15=' '
        d_16=' '
        d_17=' '
        d_18=' '
        d_19=' '
        d_20=' '
        d_21=' '
        d_22=' '
        d_23=' '
        d_24=' '
        d_25=' '
        d_26=' '
        d_27=' '
        d_28=' '
        d_29=' '
        d_30=' '
        d_31=' '
        a_1=recRep.a_1; a_2=recRep.a_2; a_4=recRep.a_4; a_3=recRep.a_3; a_5=recRep.a_5; a_6=recRep.a_6;
        a_7=recRep.a_7; a_8=recRep.a_8; a_9=recRep.a_9; a_10=recRep.a_10;  a_11=recRep.a_11; a_12=recRep.a_12;
        a_13=recRep.a_13; a_14=recRep.a_14; a_15=recRep.a_15; a_16=recRep.a_16;  a_17=recRep.a_17; a_18=recRep.a_18;
        a_19=recRep.a_19; a_20=recRep.a_20; a_21=recRep.a_21;  a_22=recRep.a_22; a_23=recRep.a_23;  a_24=recRep.a_24;
        a_25=recRep.a_25; a_26=recRep.a_26; a_27=recRep.a_27; a_28=recRep.a_28;  a_29=recRep.a_29; 
        a_30=recRep.a_30; a_31=recRep.a_31;
        
        
        if recRep.a_1==None: a_1=0;  
        if recRep.a_2==None: a_2=0; 
        if recRep.a_3==None: a_3=0;
        if recRep.a_4==None: a_4=0; 
        if recRep.a_5==None: a_5=0;
        if recRep.a_6==None: a_6=0; 
        if recRep.a_7==None: a_7=0; 
        if recRep.a_8==None: a_8=0;
        if recRep.a_9==None: a_9=0; 
        if recRep.a_10==None: a_10=0;
        if recRep.a_11==None: a_11=0; 
        if recRep.a_12==None: a_12=0; 
        if recRep.a_13==None: a_13=0; 
        if recRep.a_14==None: a_14=0; 
        if recRep.a_15==None: a_15=0;
        if recRep.a_16==None: a_16=0; 
        if recRep.a_17==None: a_17=0; 
        if recRep.a_18==None: a_18=0;
        if recRep.a_19==None: a_19=0; 
        if recRep.a_20==None: a_20=0; 
        if recRep.a_21==None: a_21=0; 
        if recRep.a_22==None: a_22=0; 
        if recRep.a_23==None: a_23=0; 
        if recRep.a_24==None: a_24=0; 
        if recRep.a_25==None: a_25=0; 
        if recRep.a_26==None: a_26=0;
        if recRep.a_27==None: a_27=0; 
        if recRep.a_28==None: a_28=0;
        if recRep.a_29==None: a_29=0; 
        if recRep.a_30==None: a_30=0; 
        if recRep.a_31==None: a_31=0; 
         
        if int(recRep.d_1)>0: d_1='Y';
        if int(recRep.d_2)>0: d_2='Y';
        if int(recRep.d_3)>0: d_3='Y';
        if int(recRep.d_4)>0: d_4='Y';
        if int(recRep.d_5)>0: d_5='Y';
        if int(recRep.d_6)>0: d_6='Y';
        if int(recRep.d_7)>0: d_7='Y';
        if int(recRep.d_8)>0: d_8='Y';
        if int(recRep.d_9)>0: d_9='Y';
        if int(recRep.d_10)>0: d_10='Y';
        if int(recRep.d_11)>0: d_11='Y';
        if int(recRep.d_12)>0: d_12='Y';
        if int(recRep.d_13)>0: d_13='Y';
        if int(recRep.d_14)>0: d_14='Y';
        if int(recRep.d_15)>0: d_15='Y';
        if int(recRep.d_16)>0: d_16='Y';
        if int(recRep.d_17)>0: d_17='Y';
        if int(recRep.d_18)>0: d_18='Y';
        if int(recRep.d_19)>0: d_19='Y';
        if int(recRep.d_20)>0: d_20='Y';
        if int(recRep.d_21)>0: d_21='Y';
        if int(recRep.d_22)>0: d_22='Y';
        if int(recRep.d_23)>0: d_23='Y';
        if int(recRep.d_24)>0: d_24='Y';
        if int(recRep.d_25)>0: d_25='Y';
        if int(recRep.d_26)>0: d_26='Y';
        if int(recRep.d_27)>0: d_27='Y';
        if int(recRep.d_28)>0: d_28='Y';
        if int(recRep.d_29)>0: d_29='Y';
        if int(recRep.d_30)>0: d_30='Y';
        if int(recRep.d_31)>0: d_31='Y';
        
        
        
        if int(a_1)>0: d_1=str(a_1);total=total+int(a_1);totalVisit=totalVisit+int(a_1);
        if int(a_2)>0: d_2=str(a_2);total=total+int(a_2);totalVisit=totalVisit+int(a_2);
        if int(a_3)>0: d_3=str(a_3);total=total+int(a_3);totalVisit=totalVisit+int(a_3);
        if int(a_4)>0: d_4=str(a_4);total=total+int(a_4);totalVisit=totalVisit+int(a_4);
        if int(a_5)>0: d_5=str(a_5);total=total+int(a_5);totalVisit=totalVisit+int(a_5);
        if int(a_6)>0: d_6=str(a_6);total=total+int(a_6);totalVisit=totalVisit+int(a_6);
        if int(a_7)>0: d_7=str(a_7);total=total+int(a_7);totalVisit=totalVisit+int(a_7);
        if int(a_8)>0: d_8=str(a_8);total=total+int(a_8);totalVisit=totalVisit+int(a_8);
        if int(a_9)>0: d_9=str(a_9);total=total+int(a_9);totalVisit=totalVisit+int(a_9);
        if int(a_10)>0: d_10=str(a_10);total=total+int(a_10);totalVisit=totalVisit+int(a_10);
        if int(a_11)>0: d_11=str(a_11);total=total+int(a_11);totalVisit=totalVisit+int(a_11);
        if int(a_12)>0: d_12=str(a_12);total=total+int(a_12);totalVisit=totalVisit+int(a_12);
        if int(a_13)>0: d_13=str(a_13);total=total+int(a_13);totalVisit=totalVisit+int(a_13);
        if int(a_14)>0: d_14=str(a_14);total=total+int(a_14);totalVisit=totalVisit+int(a_14);
        if int(a_15)>0: d_15=str(a_15);total=total+int(a_15);totalVisit=totalVisit+int(a_15);
        if int(a_16)>0: d_16=str(a_16);total=total+int(a_16);totalVisit=totalVisit+int(a_16);
        if int(a_17)>0: d_17=str(a_17);total=total+int(a_17);totalVisit=totalVisit+int(a_17);
        if int(a_18)>0: d_18=str(a_18);total=total+int(a_18);totalVisit=totalVisit+int(a_18);
        if int(a_19)>0: d_19=str(a_19);total=total+int(a_19);totalVisit=totalVisit+int(a_19);
        if int(a_20)>0: d_20=str(a_20);total=total+int(a_20);totalVisit=totalVisit+int(a_20);
        if int(a_21)>0: d_21=str(a_21);total=total+int(a_21);totalVisit=totalVisit+int(a_21);
        if int(a_22)>0: d_22=str(a_22);total=total+int(a_22);totalVisit=totalVisit+int(a_22);
        if int(a_23)>0: d_23=str(a_23);total=total+int(a_23);totalVisit=totalVisit+int(a_23);
        if int(a_24)>0: d_24=str(a_24);total=total+int(a_24);totalVisit=totalVisit+int(a_24);
        if int(a_25)>0: d_25=str(a_25);total=total+int(a_25);totalVisit=totalVisit+int(a_25);
        if int(a_26)>0: d_26=str(a_26);total=total+int(a_26);totalVisit=totalVisit+int(a_26);
        if int(a_27)>0: d_27=str(a_27);total=total+int(a_27);totalVisit=totalVisit+int(a_27);
        if int(a_28)>0: d_28=str(a_28);total=total+int(a_28);totalVisit=totalVisit+int(a_28);
        if int(a_29)>0: d_29=str(a_29);total=total+int(a_29);totalVisit=totalVisit+int(a_29);
        if int(a_30)>0: d_30=str(a_30);total=total+int(a_30);totalVisit=totalVisit+int(a_30);
        if int(a_31)>0: d_31=str(a_31);total=total+int(a_31);totalVisit=totalVisit+int(a_31);
        
        
           
        if flagRep==0:
            rsm='<font style="font-size:16px">RSM: </font>'+str(recRep.rsm_name)+' | '+str(recRep.rsm_id)
            fm='<font style="font-size:16px">FM: </font>'+str(recRep.fm_name)+' | '+str(recRep.fm_id)
            tr='<font style="font-size:16px">TR: </font>'+str(recRep.tr_name)+' | '+str(recRep.tr)
            reportShowHead=rsm+'<br>'+fm+'<br>'+tr+'<br><br>'
            
            
            
            flagRep=1
        
        
        
        reportShow=reportShow+'<tr>'
        reportShow=reportShow+'<td style="background-color:transparent">'+str(recRep.client_id)+'</td>'+'<td style="background-color:transparent">'+str(recRep.client_name)+'</td>'+'<td>'+str(d_1)+'</td>'+'<td>'+str(d_2)+'</td>'+'<td>'+str(d_3)+'</td>'+'<td>'+str(d_4)+'</td>'+'<td>'+str(d_5)+'</td>'+'<td>'+str(d_6)+'</td>'+'<td>'+str(d_7)+'</td>'+'<td>'+str(d_8)+'</td>'+'<td>'+str(d_9)+'</td>'+'<td>'+str(d_10)+'</td>'+'<td>'+str(d_11)+'</td>'+'<td>'+str(d_12)+'</td>'+'<td>'+str(d_13)+'</td>'+'<td>'+str(d_14)+'</td>'+'<td>'+str(d_15)+'</td>'+'<td>'+str(d_16)+'</td>'+'<td>'+str(d_17)+'</td>'+'<td>'+str(d_18)+'</td>'+'<td>'+str(d_19)+'</td>'+'<td>'+str(d_20)+'</td>'+'<td>'+str(d_21)+'</td>'+'<td>'+str(d_22)+'</td>'+'<td>'+str(d_23)+'</td>'+'<td>'+str(d_24)+'</td>'+'<td>'+str(d_25)+'</td>'+'<td>'+str(d_26)+'</td>'+'<td>'+str(d_27)+'</td>'+'<td>'+str(d_28)+'</td>'+'<td>'+str(d_29)+'</td>'+'<td>'+str(d_30)+'</td>'+'<td>'+str(d_31)+'</td>'+'<td style="background-color:transparent">'+str(total)+'</td>'
        reportShow=reportShow+'</tr>'
    
        
    for x in range(len(recordDoc)): 
        recordD=recordDoc[x] 
        reportShow=reportShow+'<tr>'
        reportShow=reportShow+'<td style="background-color:transparent">'+str(recordD["client_id"])+'</td>'+'<td style="background-color:transparent">'+str(recordD["name"])+'</td>'+'<td></td>'+'<td></td>'+'<td></td>'+'<td></td>'+'<td></td>'+'<td></td>'+'<td></td>'+'<td></td>'+'<td></td>'+'<td></td>'+'<td></td>'+'<td></td>'+'<td></td>'+'<td></td>'+'<td></td>'+'<td></td>'+'<td></td>'+'<td></td>'+'<td></td>'+'<td></td>'+'<td></td>'+'<td></td>'+'<td></td>'+'<td></td>'+'<td></td>'+'<td></td>'+'<td></td>'+'<td></td>'+'<td></td>'+'<td></td>'+'<td></td>'+'<td style="background-color:transparent">0</td>'
        reportShow=reportShow+'</tr>'
        
#     reportShowfinal=reportShowHead+'<font style="font-size:14px; color:#fff">Number of Doctors in this territory: </font><font style="font-size:14px; color:#cceaab">'+str(docTr)+'</font><br><font style="font-size:14px; color:#fff">Number of Doctors visited in this territory: </font><font style="font-size:14px; color:#cceaab">'+str(docCunt)+'</font><br><font style="font-size:14px; color:#fff">Total number of Doctor Visit: </font><font style="font-size:14px; color:#cceaab">'+str(totalVisit)+'</font>'+reportShow
#     ========================

    reportShow=reportShow+'</table>'
    reportShowfinal=reportShowHead+'<font style="font-size:14px; color:#fff">Number of Clients in this territory: </font><font style="font-size:14px; color:#cceaab">'+str(docTr)+'</font><br><font style="font-size:14px; color:#fff">Number Clients visited in this territory: </font><font style="font-size:14px; color:#cceaab">'+str(docCunt)+'</font><br><font style="font-size:14px; color:#fff">Total amount of Client Visit: </font><font style="font-size:14px; color:#cceaab">'+str(totalVisit)+'</font>'+reportShow
#     reportShowfinal=reportShow
    
    return 'SUCCESS<SYNCDATA>'+reportShowfinal

# =======================================================
def report_summary_PaySlip_tr():
    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.rep_pass).strip()
    synccode = str(request.vars.synccode).strip()
    
    rep_id_report = str(request.vars.rep_id_report).strip().upper()
    
    se_market_report = str(request.vars.se_market_report).strip().upper()
    user_type = str(request.vars.user_type).strip().upper()
    
    date_year = str(request.vars.date_year).strip().upper()
    date_month = str(request.vars.date_month).strip().upper()
    year_month=str(date_year)+'-'+str(date_month)

    repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.sync_code == synccode) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.id,db.sm_rep.user_type,db.sm_rep.level_id,db.sm_rep.field2, limitby=(0, 1))

#    return db._lastsql
   
    level_rep=''
    
    if not repRow:
       retStatus = 'FAILED<SYNCDATA>Invalid Authorization'
       return retStatus
    else:
       pass
   
    
#     =========================================
    
#     reportShowfinal=reportShowHead+'<font style="font-size:14px; color:#fff">Number of Clients in this territory: </font><font style="font-size:14px; color:#cceaab">'+str(docTr)+'</font><br><font style="font-size:14px; color:#fff">Number Clients visited in this territory: </font><font style="font-size:14px; color:#cceaab">'+str(docCunt)+'</font><br><font style="font-size:14px; color:#fff">Total amount of Client Visit: </font><font style="font-size:14px; color:#cceaab">'+str(totalVisit)+'</font>'+reportShow
    reportShowfinal='PaySlip'
    
    return 'SUCCESS<SYNCDATA>'+reportShowfinal
def report_summary_PaySlip_tr():
    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.rep_pass).strip()
    synccode = str(request.vars.synccode).strip()
    
    rep_id_report = str(request.vars.rep_id_report).strip().upper()
    
    se_market_report = str(request.vars.se_market_report).strip().upper()
    user_type = str(request.vars.user_type).strip().upper()
    
    date_year = str(request.vars.date_year).strip().upper()
    date_month = str(request.vars.date_month).strip().upper()
    year_month=str(date_year)+'-'+str(date_month)

    repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.sync_code == synccode) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.id,db.sm_rep.user_type,db.sm_rep.level_id,db.sm_rep.field2, limitby=(0, 1))

#    return db._lastsql
   
    level_rep=''
    
    if not repRow:
       retStatus = 'FAILED<SYNCDATA>Invalid Authorization'
       return retStatus
    else:
       pass
   
    
#     =========================================
    
#     reportShowfinal=reportShowHead+'<font style="font-size:14px; color:#fff">Number of Clients in this territory: </font><font style="font-size:14px; color:#cceaab">'+str(docTr)+'</font><br><font style="font-size:14px; color:#fff">Number Clients visited in this territory: </font><font style="font-size:14px; color:#cceaab">'+str(docCunt)+'</font><br><font style="font-size:14px; color:#fff">Total amount of Client Visit: </font><font style="font-size:14px; color:#cceaab">'+str(totalVisit)+'</font>'+reportShow
    reportShowfinal='PaySlip'
    
    return 'SUCCESS<SYNCDATA>'+reportShowfinal


def report_summary_ExpenseSlip_tr():
    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.rep_pass).strip()
    synccode = str(request.vars.synccode).strip()
    
    rep_id_report = str(request.vars.rep_id_report).strip().upper()
    
    se_market_report = str(request.vars.se_market_report).strip().upper()
    user_type = str(request.vars.user_type).strip().upper()
    
    date_year = str(request.vars.date_year).strip().upper()
    date_month = str(request.vars.date_month).strip().upper()
    year_month=str(date_year)+'-'+str(date_month)

    repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.sync_code == synccode) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.id,db.sm_rep.user_type,db.sm_rep.level_id,db.sm_rep.field2, limitby=(0, 1))

#    return db._lastsql
   
    level_rep=''
    
    if not repRow:
       retStatus = 'FAILED<SYNCDATA>Invalid Authorization'
       return retStatus
    else:
       pass
   
    
#     =========================================
    
#     reportShowfinal=reportShowHead+'<font style="font-size:14px; color:#fff">Number of Clients in this territory: </font><font style="font-size:14px; color:#cceaab">'+str(docTr)+'</font><br><font style="font-size:14px; color:#fff">Number Clients visited in this territory: </font><font style="font-size:14px; color:#cceaab">'+str(docCunt)+'</font><br><font style="font-size:14px; color:#fff">Total amount of Client Visit: </font><font style="font-size:14px; color:#cceaab">'+str(totalVisit)+'</font>'+reportShow
    reportShowfinal='ExpenseSlip'
    
    return 'SUCCESS<SYNCDATA>'+reportShowfinal



def microUnionReady():
    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.rep_pass).strip()
    synccode = str(request.vars.synccode).strip()
    route = str(request.vars.route).strip()
    compRow = db((db.sm_company_settings.cid == cid) & (db.sm_company_settings.status == 'ACTIVE')).select(db.sm_company_settings.cid, limitby=(0, 1))
    if not compRow:
        return 'FAILED<SYNCDATA>Invalid Company'
    else:
        repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.sync_code == synccode) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.rep_id, db.sm_rep.name, db.sm_rep.mobile_no, db.sm_rep.user_type, db.sm_rep.level_id, limitby=(0, 1))
#         return db._lastsql
        if not repRow:
           return 'FAILED<SYNCDATA>Invalid Authorization'
        else:
            user_type = repRow[0].user_type
        
            
#         microunionRow=db((db. sm_doctor_area.cid==cid) & (db. sm_doctor_area.area_id == route)  & (db.sm_doctor_area.field1 != '')  & (db.sm_doctor_area.note != '')).select(db.sm_doctor_area.field1,db.sm_doctor_area.note, groupby=db.sm_doctor_area.field1|db.sm_doctor_area.note, orderby=db.sm_doctor_area.note)
        microunionRow=db((db.sm_microunion.cid==cid) & (db.sm_microunion.area_id == route)  & (db.sm_microunion.note != 'Submitted')).select(db.sm_microunion.microunion_id,db.sm_microunion.microunion_name, groupby=db.sm_microunion.microunion_id|db.sm_microunion.microunion_name, orderby=db.sm_microunion.microunion_name|db.sm_microunion.microunion_id)
#         return db._lastsql
        microunionStr=''
        for microunionRow in microunionRow:
            route_id = microunionRow.microunion_id
            route_name = microunionRow.microunion_name
           
            if microunionStr == '':
                microunionStr = str(route_name)+ '|' +str(route_id)  
            else:
                microunionStr += '<rd>' + str(route_name)+ '|' +str(route_id)  
        
            
        return 'SUCCESS<SYNCDATA>' + str(microunionStr)   
    

# ================================ Chemist pending List
def chP_list():
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
 
                chemistRows = db((db.sm_client_temp.cid == cid) & (db.sm_client_temp.status != 'REJECTED') & (db.sm_client_temp.newChemist == 0) ).select(db.sm_client_temp.id,db.sm_client_temp.client_id,db.sm_client_temp.name, db.sm_client_temp.address, db.sm_client_temp.contact_no1,db.sm_client_temp.trade_license_no,db.sm_client_temp.vat_registration_no,db.sm_client_temp.photo,db.sm_client_temp.note,db.sm_client_temp.status, orderby=db.sm_client_temp.client_id)
                # return doctorRows
                if not chemistRows:
                    pass
     
                else:
                    rtn_str=rtn_str+"""<table width="100%" border="0" cellspacing="0" cellpadding="0">
                            <tr style="font-size:16px; background-color:#CCC"><td >Update Chemist</td></tr>
                            </table>
                            </br>"""
                    for chemistRows in chemistRows:
                        row_id = chemistRows.id
                        chemist_id = chemistRows.client_id
                        chemist_name = chemistRows.name
                        chemist_address = chemistRows.address
                        chemist_contact = chemistRows.contact_no1
                        chemist_trade = chemistRows.trade_license_no
                        chemist_vat = chemistRows.vat_registration_no
#                         chemist_dob = chemistRows.dob
                        chemist_dob='-'
                        photo = chemistRows.photo
                        note = chemistRows.note
                        status=chemistRows.status
                        if status=='Rreq':
                            noteStr="""<tr>
                            <td >Reason </td>
                            <td >"""+str(note)+"""</td></tr>"""
                        
                        imgSrc='http://i001.yeapps.com/image_hub/static/kpl_image/'+str(photo)
 
                        rtn_str=rtn_str+"""<table width="100%" border="0" cellspacing="0" cellpadding="0">
                            <tr><td ><img src='"""+imgSrc+""" ' width="100" height="100" alt="Image" ></td></tr>
                            </table>
                            </br>"""
                        rtn_str=rtn_str+"""<table width="100%" border="0">
                            <tr>
                            <td width="30%">ID <font style="color:#903; font-size:16px"> * </font></td>
                            <td >"""+str(chemist_id)+"""</td>
                            </tr>
                            <tr>
                            <td >Name <font style="color:#903; font-size:16px"> * </font></td>
                            <td >"""+str(chemist_name)+"""</td>
                            </tr>
                            <tr>
                            <td >Address</td>
                            <td >"""+str(chemist_address)+"""</td>
                            </tr>
                            <tr>
                            <td >Phone <font style="color:#903; font-size:16px"> * </font></td>
                             <td >"""+str(chemist_contact)+"""</td>
                            </tr>
                            <tr>
                            <td >Trade License</td>
                            <td >"""+str(chemist_trade)+"""</td>
                            </tr>
                            <tr>
                            <td >Vat Registration</td>
                            <td >"""+str(chemist_vat)+"""</td>
                            </tr>
                            <tr>
                            <td >Date of birth</td>
                            <td >"""+str(chemist_dob)+"""</td></tr>"""
                            
                        if status=='Rreq':    
                            rtn_str=rtn_str+ noteStr
                        rtn_str=rtn_str+ """ </table>"""
#                     New===========

                chemistRows = db((db.sm_client_temp.cid == cid) & (db.sm_client_temp.status != 'REJECTED')  & (db.sm_client_temp.newChemist == 1) ).select(db.sm_client_temp.id,db.sm_client_temp.client_id,db.sm_client_temp.name, db.sm_client_temp.address, db.sm_client_temp.contact_no1,db.sm_client_temp.trade_license_no,db.sm_client_temp.vat_registration_no,db.sm_client_temp.photo, orderby=db.sm_client_temp.client_id)
#                 return doctorRows
                if not chemistRows:
                    pass
     
                else:
                    rtn_str=rtn_str+"""<table width="100%" border="0" cellspacing="0" cellpadding="0">
                        <tr style="font-size:16px; background-color:#CCC"><td >Add Chemist</td></tr>
                        </table>
                        </br>"""
                    for chemistRows in chemistRows:
                        row_id = chemistRows.id
                        chemist_id = chemistRows.client_id
                        chemist_name = chemistRows.name
                        chemist_address = chemistRows.address
                        chemist_contact = chemistRows.contact_no1
                        chemist_trade = chemistRows.trade_license_no
                        chemist_vat = chemistRows.vat_registration_no
#                         chemist_dob = chemistRows.dob
                        chemist_dob='-'
                        photo = chemistRows.photo
                        imgSrc='http://i001.yeapps.com/image_hub/static/kpl_image/'+str(photo)
 
                        rtn_str=rtn_str+"""<table width="100%" border="0" cellspacing="0" cellpadding="0">
                            <tr><td ><img src='"""+imgSrc+""" ' width="100" height="100" alt="Image" ></td></tr>
                            </table>
                            </br>"""
                        rtn_str=rtn_str+"""<table width="100%" border="0">
                            <tr>
                            <td width="30%">ID <font style="color:#903; font-size:16px"> * </font></td>
                            <td >"""+str(chemist_id)+"""</td>
                            </tr>
                            <tr>
                            <td >Name <font style="color:#903; font-size:16px"> * </font></td>
                            <td >"""+str(chemist_name)+"""</td>
                            </tr>
                            <tr>
                            <td >Address</td>
                            <td >"""+str(chemist_address)+"""</td>
                            </tr>
                            <tr>
                            <td >Phone <font style="color:#903; font-size:16px"> * </font></td>
                             <td >"""+str(chemist_contact)+"""</td>
                            </tr>
                            <tr>
                            <td >Trade License</td>
                            <td >"""+str(chemist_trade)+"""</td>
                            </tr>
                            <tr>
                            <td >Vat Registration</td>
                            <td >"""+str(chemist_vat)+"""</td>
                            </tr>
                            <tr>
                            <td >Date of birth</td>
                            <td >"""+str(chemist_dob)+"""</td>
                            </tr>
                            
                            
                        
                        
                    </table>""" 
            if userType=='sup':
                levelList=[]
                marketList=[]
                spicial_codeList=[]
                marketStr=''
                SuplevelRows = db((db.sm_supervisor_level.cid == cid) & (db.sm_supervisor_level.sup_id == rep_id) ).select(db.sm_supervisor_level.level_id,db.sm_supervisor_level.level_depth_no, orderby=~db.sm_supervisor_level.level_id)
                # return SuplevelRows
                for SuplevelRows in SuplevelRows:
                    Suplevel_id = SuplevelRows.level_id
                    depth = SuplevelRows.level_depth_no
                    level = 'level' + str(depth)
                    if Suplevel_id not in levelList:
                        levelList.append(Suplevel_id)
                
                cTeam=0
                for i in range(len(levelList)):
                    levelRows = db((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '1') & (db.sm_level[level] == levelList[i]) ).select(db.sm_level.level_id, db.sm_level.level_name, db.sm_level.depot_id,db.sm_level.special_territory_code)
                    # return db._lastsql
                    for levelRow in levelRows:
                        level_id = levelRow.level_id
                        special_territory_code = levelRow.special_territory_code
                        if level_id==special_territory_code:
                            cTeam=1

                        if marketStr=='':
                            marketStr="'"+str(level_id)+"'"
                        else:
                            marketStr=marketStr+",'"+str(level_id)+"'" 
                        marketList.append(level_id)



                # return marketStr
                chemistRows = db((db.sm_client_temp.cid == cid) & (db.sm_client_temp.status != 'REJECTED')  & (db.sm_client_temp.newChemist == 0) & (db.sm_client_temp.area_id.belongs(marketList))).select(db.sm_client_temp.id,db.sm_client_temp.client_id,db.sm_client_temp.name, db.sm_client_temp.address, db.sm_client_temp.contact_no1,db.sm_client_temp.trade_license_no,db.sm_client_temp.vat_registration_no,db.sm_client_temp.photo,db.sm_client_temp.note,db.sm_client_temp.status, orderby=db.sm_client_temp.client_id)
                # return chemistRows
                # return db._lastsql
                
                if not chemistRows:
                    pass
     
                else:
                    rtn_str=rtn_str+"""<table width="100%" border="0" cellspacing="0" cellpadding="0">
                            <tr style="font-size:16px; background-color:#000"><td >Update Chemist</td></tr>
                            </table>
                            </br>"""
                    for chemistRows in chemistRows:
                        row_id = chemistRows.id
                        chemist_id = chemistRows.client_id
                        chemist_name = chemistRows.name
                        chemist_address = chemistRows.address
                        chemist_contact = chemistRows.contact_no1
                        chemist_trade = chemistRows.trade_license_no
                        chemist_vat = chemistRows.vat_registration_no
#                         chemist_dob = chemistRows.dob
                        chemist_dob='-'
                        photo = chemistRows.photo
                        note = chemistRows.note
                        status=chemistRows.status
                        
                        if status=='Rreq':
                            noteStr="""<tr>
                            <td >Reason </td>
                            <td >"""+str(note)+"""</td></tr>"""
                        rtn_str=rtn_str+ """ </table>"""
                        imgSrc='http://i001.yeapps.com/image_hub/static/kpl_image/'+str(photo)
 
                        rtn_str=rtn_str+"""<table width="100%" border="0" cellspacing="0" cellpadding="0">
                            <tr><td ><img src='"""+imgSrc+""" ' width="100" height="100" alt="Image" ></td></tr>
                            </table>
                            </br>"""
                        rtn_str=rtn_str+"""<table width="100%" border="0">
                            <tr>
                            <td width="30%">ID <font style="color:#903; font-size:16px"> * </font></td>
                            <td >"""+str(chemist_id)+"""</td>
                            </tr>
                            <tr>
                            <td >Name <font style="color:#903; font-size:16px"> * </font></td>
                            <td >"""+str(chemist_name)+"""</td>
                            </tr>
                            <tr>
                            <td >Address</td>
                            <td >"""+str(chemist_address)+"""</td>
                            </tr>
                            <tr>
                            <td >Phone <font style="color:#903; font-size:16px"> * </font></td>
                             <td >"""+str(chemist_contact)+"""</td>
                            </tr>
                            <tr>
                            <td >Trade License</td>
                            <td >"""+str(chemist_trade)+"""</td>
                            </tr>
                            <tr>
                            <td >Vat Registration</td>
                            <td >"""+str(chemist_vat)+"""</td>
                            </tr>
                            <tr>
                            <td >Date of birth</td>
                            <td >"""+str(chemist_dob)+"""</td>
                            </tr>"""
                        if status=='Rreq':    
                            rtn_str=rtn_str+ noteStr
                        rtn_str=rtn_str+"""    </table><table width="100%" border="0">
                            <tr>
                            <td width="50%" ><input type="submit"  onClick="chemist_approve("""+str(row_id)+""");"   style="width:100%; height:50px; background-color:#09C; color:#FFF; font-size:20px" value="Approve"   /></td>
                            <td width="50%" ><input type="submit"  onClick="chemist_reject("""+str(row_id)+""");"   style="width:100%; height:50px; background-color:#09C; color:#FFF; font-size:20px" value="Reject"   /></td>
                            </tr></table>"""
                        
                      
                        
                    
                    
                chemistRows = db((db.sm_client_temp.cid == cid) & (db.sm_client_temp.status != 'REJECTED')  & (db.sm_client_temp.newChemist == 1) & (db.sm_client_temp.area_id.belongs(marketList))).select(db.sm_client_temp.id,db.sm_client_temp.client_id,db.sm_client_temp.name, db.sm_client_temp.address, db.sm_client_temp.contact_no1,db.sm_client_temp.trade_license_no,db.sm_client_temp.vat_registration_no,db.sm_client_temp.photo, orderby=db.sm_client_temp.client_id)
                # return db._lastsql
                if not chemistRows:
                    pass
     
                else:
                    rtn_str=rtn_str+"""<table width="100%" border="0" cellspacing="0" cellpadding="0">
                        <tr style="font-size:16px; background-color:#CCC"><td >Add Chemist</td></tr>
                        </table>
                        </br>"""
                    for chemistRows in chemistRows:
                        row_id = chemistRows.id
                        chemist_id = chemistRows.client_id
                        chemist_name = chemistRows.name
                        chemist_address = chemistRows.address
                        chemist_contact = chemistRows.contact_no1
                        chemist_trade = chemistRows.trade_license_no
                        chemist_vat = chemistRows.vat_registration_no
#                         chemist_dob = chemistRows.dob
                        chemist_dob='-'
                        photo = chemistRows.photo
                        imgSrc='http://i001.yeapps.com/image_hub/static/kpl_image/'+str(photo)
 
                        rtn_str=rtn_str+"""<table width="100%" border="0" cellspacing="0" cellpadding="0">
                            <tr><td ><img src='"""+imgSrc+""" ' width="100" height="100" alt="Image" ></td></tr>
                            </table>
                            </br>"""
                        rtn_str=rtn_str+"""<table width="100%" border="0">
                            <tr>
                            <td width="30%">ID <font style="color:#903; font-size:16px"> * </font></td>
                            <td >"""+str(chemist_id)+"""</td>
                            </tr>
                            <tr>
                            <td >Name <font style="color:#903; font-size:16px"> * </font></td>
                            <td >"""+str(chemist_name)+"""</td>
                            </tr>
                            <tr>
                            <td >Address</td>
                            <td >"""+str(chemist_address)+"""</td>
                            </tr>
                            <tr>
                            <td >Phone <font style="color:#903; font-size:16px"> * </font></td>
                             <td >"""+str(chemist_contact)+"""</td>
                            </tr>
                            <tr>
                            <td >Trade License</td>
                            <td >"""+str(chemist_trade)+"""</td>
                            </tr>
                            <tr>
                            <td >Vat Registration</td>
                            <td >"""+str(chemist_vat)+"""</td>
                            </tr>
                            <tr>
                            <td >Date of birth</td>
                            <td >"""+str(chemist_dob)+"""</td>
                            </tr>
                            </table><table width="100%" border="0">
                            <tr>
                            <td width="50%" ><input type="submit"  onClick="chemist_approve("""+str(row_id)+""");"   style="width:100%; height:50px; background-color:#09C; color:#FFF; font-size:20px" value="Approve"   /></td>
                            <td width="50%" ><input type="submit"  onClick="chemist_reject("""+str(row_id)+""");"   style="width:100%; height:50px; background-color:#09C; color:#FFF; font-size:20px" value="Reject"   /></td>
                            </tr>
                        
                        
                    </table>"""         
                     
                    

                 
                    

    return 'SUCCESS<SYNCDATA>'+rtn_str     
    
def chemist_approve():
    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.rep_pass).strip()
    synccode = str(request.vars.synccode).strip()
    row_id = str(request.vars.row_id).strip()
     
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
            if userType=='sup':
                chemistRows = db((db.sm_client_temp.cid == cid) & ((db.sm_client_temp.status == 'SUBMITTED') | (db.sm_client_temp.status == 'ACTIVE') | (db.sm_client_temp.status == 'Rreq'))& (db.sm_client_temp.id == row_id) ).select(db.sm_client_temp.ALL, limitby=(0,1))
#                 return chemistRows
                if not chemistRows:
                    rtn_str='Nothing pending for approval.'
     
                else:
                    route           =chemistRows[0].area_id
                    client_id       =chemistRows[0].client_id
                    ChemistName     =chemistRows[0].name
                    address         =chemistRows[0].address
                    RegistrationNo  =chemistRows[0].vat_registration_no                             
                    district        =chemistRows[0].district
                    thana           =chemistRows[0].thana
                    NID             =chemistRows[0].nid
                    Contact_Name    =chemistRows[0].owner_name
                    Contact_phone   =chemistRows[0].contact_no1
                    catID           =chemistRows[0].category_id
                    catName         =chemistRows[0].category_name
                    subcatID        =chemistRows[0].sub_category_id
                    subcatName      =chemistRows[0].sub_category_name
#                     DOB             =chemistRows[0].dob
                    DOB='1900-01-01'
                    Cash_Credit     =chemistRows[0].field1
                    Credit_Limit    =chemistRows[0].credit_limit

                    imageName       =chemistRows[0].photo
                    NumberofDoc     =chemistRows[0].field2
                    AvgPatientPerDay=chemistRows[0].note
                    status          =chemistRows[0].status
                    
                    
                    
#                     return route_id
                    depoRow = db((db.sm_client.cid == cid) & (db.sm_client.area_id == route) ).select(db.sm_client.depot_id,db.sm_client.depot_name,db.sm_client.store_id,db.sm_client.store_name,orderby=~db.sm_client.depot_id, limitby=(0, 1))
#                     depoRow = db((db.sm_level.cid == cid) & (db.sm_level.level_id == route_id) & (db.sm_level.is_leaf == '1')).select(db.sm_level.depot_id, db.sm_level.level7_name, db.sm_level.level8, db.sm_level.level8_name, limitby=(0, 1))
#                     return depoRow
                    depot_id=''
                    depot_name=''
                    store_id=''
                    store_name=''
                    if repRow:
                        depot_id=depoRow[0].depot_id
                        depot_name=depoRow[0].depot_name
                        store_id=depoRow[0].store_id
                        store_name=depoRow[0].store_name


                    chemistCheckRows = db((db.sm_client.cid == cid) & (db.sm_client.client_id == client_id)).select(db.sm_client.id, limitby=(0,1))
#                     return chemistCheckRows
                    if chemistCheckRows:
                        if status=='Rreq':
                            db((db.sm_client.cid == cid) & (db.sm_client.client_id == client_id) ).update( status='INACTIVE')
                        else:
#                             db((db.sm_client.cid == cid) & (db.sm_client.client_id == client_id) ).update( area_id =route,name=ChemistName,address=address ,vat_registration_no=RegistrationNo ,district=district,thana=thana,nid=int(NID) , owner_name=Contact_Name ,contact_no1=Contact_phone ,category_id=catID , category_name=catName,sub_category_id=subcatID ,sub_category_name=subcatName, dob=DOB ,field1=Cash_Credit ,credit_limit=int(Credit_Limit) ,status='ACTIVE',photo=imageName,field2=NumberofDoc,note=AvgPatientPerDay,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name)
                            db((db.sm_client.cid == cid) & (db.sm_client.client_id == client_id) ).update( area_id =route,name=ChemistName,address=address ,vat_registration_no=RegistrationNo ,district=district,thana=thana,nid=int(NID) , owner_name=Contact_Name ,contact_no1=Contact_phone ,category_id=catID , category_name=catName,sub_category_id=subcatID ,sub_category_name=subcatName ,field1=Cash_Credit ,credit_limit=int(Credit_Limit) ,status='ACTIVE',photo=imageName,field2=NumberofDoc,note=AvgPatientPerDay,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name)
                        db((db.sm_client_temp.cid == cid) & (db.sm_client_temp.client_id == client_id) ).delete()
                    else:
                        db.sm_client.insert(cid =cid,client_id=client_id ,address=address,area_id =route,name=ChemistName ,vat_registration_no=RegistrationNo ,district=district,thana=thana,nid=int(NID) , owner_name=Contact_Name ,contact_no1=Contact_phone ,category_id=catID , category_name=catName,sub_category_id=subcatID ,sub_category_name=subcatName ,field1=Cash_Credit ,credit_limit=int(Credit_Limit) ,status='ACTIVE',photo=imageName, field2=NumberofDoc,note=AvgPatientPerDay,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name)
#                         db.sm_client.insert(cid =cid,client_id=client_id ,address=address,area_id =route,name=ChemistName ,vat_registration_no=RegistrationNo ,district=district,thana=thana,nid=int(NID) , owner_name=Contact_Name ,contact_no1=Contact_phone ,category_id=catID , category_name=catName,sub_category_id=subcatID ,sub_category_name=subcatName, dob=DOB ,field1=Cash_Credit ,credit_limit=int(Credit_Limit) ,status='ACTIVE',photo=imageName, field2=NumberofDoc,note=AvgPatientPerDay,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name)

                        db((db.sm_client_temp.cid == cid) & (db.sm_client_temp.client_id == client_id) ).delete()

    return 'SUCCESS<SYNCDATA>'+'Approved'  
def chemist_reject():
    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.rep_pass).strip()
    synccode = str(request.vars.synccode).strip()
    row_id = str(request.vars.row_id).strip()
     
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
            if userType=='sup':
                chemistRows = db((db.sm_client_temp.cid == cid) & ((db.sm_client_temp.status == 'SUBMITTED') | (db.sm_client_temp.status == 'ACTIVE'))& (db.sm_client_temp.id == row_id) ).select(db.sm_client_temp.ALL, limitby=(0,1))
#                 return chemistRows
                if not chemistRows:
                    rtn_str='Nothing pending for approval.'
     
                else:
#                     Change status in client_temp table
                    chemistRows = db((db.sm_client_temp.cid == cid) & (db.sm_client_temp.id == row_id) ).update(status='REJECTED')

    return 'SUCCESS<SYNCDATA>'+'Rejected'     
    
def addDodNmd():  
    add_data = str(request.vars.add_data)
    add_data=urllib2.unquote(add_data)
    separator='<url>'    
    urlList=add_data.split(separator,add_data.count(separator))
    cid                     =(urlList[0]).upper()
    doc_id                  =(urlList[1]).upper()
    doc_name                =(urlList[2]).upper()
    specialty               =(urlList[3]).upper()
    degree                  =(urlList[4]).upper()
    mobile                  =(urlList[5]).upper()
    des                     =(urlList[6]).upper()
    attached_institution    =(urlList[8]).upper()
    designation             =(urlList[9]).upper()
    dob                     =(urlList[10]).upper()
    mar_day                 =(urlList[11]).upper()
    doctors_category        =(urlList[12]).upper()
    service_kol_dsc         =(urlList[13]).upper()
    service_id              =(urlList[14]).upper()
    third_party_id          =(urlList[15]).upper()
    otherChamber            =(urlList[16]).upper()
    pharma_route_id         =(urlList[17]).upper()
    pharma_route_name       =(urlList[18]).upper()
    nmd_route_id            =(urlList[19]).upper()
    nmd_route_name          =(urlList[20]).upper()
    new_doc                 =(urlList[21]).upper()
    pharma_route            =(urlList[22]).upper()
    nmd_route               =(urlList[23]).upper()
    
    field1                  =(urlList[24]).upper()
    note                    =(urlList[25])
    
    db.sm_doctor_temp.insert(cid ='IBNSINA',doc_id = doc_id,doc_name=doc_name,specialty=specialty,degree=degree,mobile=mobile,des=des,status='ACTIVE',attached_institution=attached_institution,dob=dob,mar_day=mar_day,doctors_category=doctors_category,service_kol_dsc=service_kol_dsc,service_id=service_id,third_party_id=third_party_id,otherChamber=otherChamber,pharma_route_id=pharma_route, nmd_route_id=nmd_route,new_doc=new_doc,field1=field1,note=note)
    return 'SUCCESS'



# =======Approve canell doc req=========================

#=========================    Nazma
def cancellDoc():
    return 'FAILED<SYNCDATA>Restricted'
#    cid = 'IBNSINA'
    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.rep_pass).strip()
    synccode = str(request.vars.synccode).strip()

    route = str(request.vars.route).strip()
#     route_name  = str(request.vars.route_name).strip()
    route_name=''
    
    docId = str(request.vars.docId).strip()
#     docName = str(request.vars.docName).strip()
    docName=''

    reason = str(request.vars.reason).strip()
#     pharmaRoute = str(request.vars.pharmaRoute).strip()
#     nmdRoute = str(request.vars.nmdRoute).strip()
    
    
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
            docInfo = db((db.sm_doctor.cid == cid) & (db.sm_doctor.doc_id == docId) ).select(db.sm_doctor.ALL, limitby=(0,1))
            
            if docInfo:
                cid                     =docInfo[0][db.sm_doctor.cid]
                doc_id                  =docInfo[0][db.sm_doctor.doc_id]
                docName                 =docInfo[0][db.sm_doctor.doc_name]
                specialty               =docInfo[0][db.sm_doctor.specialty]
                degree                  =docInfo[0][db.sm_doctor.degree]                   
                mobile                  =docInfo[0][db.sm_doctor.mobile]                    
                des                     =docInfo[0][db.sm_doctor.des]
                status                  =docInfo[0][db.sm_doctor.status]
                attached_institution    =docInfo[0][db.sm_doctor.attached_institution]
                designation             =docInfo[0][db.sm_doctor.designation]
                dob                     =docInfo[0][db.sm_doctor.dob]
                mar_day                 =docInfo[0][db.sm_doctor.mar_day]
                doctors_category        =docInfo[0][db.sm_doctor.doctors_category]
                service_kol_dsc         =docInfo[0][db.sm_doctor.service_kol_dsc]
                service_id              =docInfo[0][db.sm_doctor.service_id]
                third_party_id          =docInfo[0][db.sm_doctor.third_party_id]
                
            routeInfo = db((db.sm_doctor_area.cid == cid) & (db.sm_doctor_area.area_id == route)).select(db.sm_doctor_area.area_name, limitby=(0,1))      
            
            if routeInfo:    
                route_name=routeInfo[0][db.sm_doctor_area.area_name]   
            
            
            
            
#             if cid=='IBNSINA':

#             if cid=='ACME':
                
            doctorRows = db((db.sm_doctor_temp.cid == cid) & (db.sm_doctor_temp.doc_id == docId) ).select(db.sm_doctor_temp.ALL)
            if doctorRows:
                doctorUpdateRows = db((db.sm_doctor_temp.cid == cid) & (db.sm_doctor_temp.doc_id == docId) ).update(pharma_route_id=route,new_doc=0,status='Rreq',note=reason)
            else:
                
                doc_ibn_insert=db.sm_doctor_temp.insert(cid=cid,doc_id=docId,doc_name=docName,specialty=specialty,degree=degree,mobile=mobile,des=des,attached_institution=attached_institution,dob=dob,mar_day=mar_day,doctors_category=doctors_category,service_kol_dsc=service_kol_dsc,service_id=service_id,third_party_id=third_party_id,pharma_route_id=route,pharma_route_name=route_name,new_doc=0,status='Rreq',note=reason) 
                                                            
#             if cid=='IPINMD':
#                 doctorRows = db((db.sm_doctor_temp.cid == cid) & (db.sm_doctor_temp.doc_id == docId) ).select(db.sm_doctor_temp.ALL)
#                 if doctorRows:
#                     doctorUpdateRows = db((db.sm_doctor_temp.cid == cid) & (db.sm_doctor_temp.doc_id == docId) ).update(nmd_route_id=route,new_doc=0,status='Rreq',note=reason)
# 
#                 else:
#                     doc_ibn_insert=db.sm_doctor_temp.insert(cid=cid,doc_id=docId,doc_name=docName,specialty=specialty,degree=degree,mobile=mobile,des=des,attached_institution=attached_institution,dob=dob,mar_day=mar_day,doctors_category=doctors_category,service_kol_dsc=service_kol_dsc,service_id=service_id,third_party_id=third_party_id,nmd_route_id=route,nmd_route_name=route_name,new_doc=0,status='Rreq',note=reason) 
# 
#             else:
#                 pass

            return 'SUCCESS<SYNCDATA>'+'Updated Successfully  '




def schedule_sync():
    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.rep_pass).strip()
    synccode = str(request.vars.synccode).strip()
#     opStr='<ASTART>G0001<fd>Aceclofenac<rd>F0002<fd>Albendazole<rd>G0003<fd>Alfuzosin Hydrochloride<rd>F0004<fd>Ambroxol Hydrochloride<rd>F0005<fd>Amino Acid<rd>F0006<fd>Amlexanox<rd>F0007<fd>Amlodipine<rd>F0008<fd>Amoxicillin<rd>F0009<fd>Ascorbic Acid<rd>F0010<fd>Atorvastatin<rd>F0011<fd>Azithromycin<rd><AEND><BSTART>F0012<fd>Baclofen<rd>F0013<fd>Bambuterol Hydrochloride<rd>F0014<fd>Betamethasone Valerate <rd>F0015<fd>BIMATOPROST<rd>F0016<fd>Bisoprolol Fumarate<rd>F0017<fd>BRIMONIDINE<rd>F0018<fd>BRIMONIDINE TIMOLOL<rd>F0019<fd>Brinzolamide<rd>F0020<fd>Brinzolamide   Timolol<rd>F0021<fd>Bromazepam<rd>F0022<fd>Bromfenac<rd>F0023<fd>Bromhexine<rd>F0024<fd>Butamirate Citrate INN<rd><BEND><CSTART>F0025<fd>Calcium Carbonate<rd>F0026<fd>Calcium Carbonate  <rd>F0027<fd>Calcium Orotate<rd>F0028<fd>Carbamazepine<rd>F0029<fd>Carbocisteine<rd>F0030<fd>Carbonyl Iron Folic Acid Vit C Vit B Comp <rd>F0031<fd>Carbonyl Iron Folic Acid Zinc<rd> F0032<fd>Carbonyl Iron Folic Acid Zinc Vit B  Ascorbic Acid<rd>F0033<fd>Carbonyl Iron with Folic Acid<rd> F0034<fd>CARBOXYMETHYLCELLULOSE<rd>F0035<fd>Cefadroxil Monohydrate<rd>F0036<fd>Cefalexin<rd>F0037<fd>Cefepime<rd>F0038<fd>Cefixime<rd>F0039<fd>Cefpodoxime Clavulanic Acid<rd>F0040<fd>Cefpodoxime Proxetil<rd>F0041<fd>Ceftazidime<rd>F0042<fd>Ceftibuten Dihydrate<rd>F0043<fd>Ceftriaxone<rd>F0044<fd>Cefuroxime axetil<rd>F0045<fd>Cefuroxime Clavulanic Acid<rd>F0046<fd>Celiprolol Hydrochloride<rd>F0047<fd>Cephradine Monohydrate<rd>F0048<fd>Cetirizine HCl<rd>F0049<fd>CHLORBUTANOL POLYVINYL ALCOHOL NACL<rd>F0050<fd>Chlorhexidine Gluconate and Isopropyl Alcohol<rd>F0051<fd>Ciprofloxacin<rd>F0052<fd>Clindamycin Hydrochloride<rd>F0053<fd>Clobetasol 0 05p Salicylic Acid <rd>F0054<fd>Clomiphene Citrate<rd>F0055<fd>Clonazepam<rd>F0056<fd>Clopidogrel Bisulfate<rd><CEND><DSTART>F0057<fd>Danazol<rd>F0058<fd>Dapoxetine<rd>F0059<fd>Desloratadine<rd>F0060<fd>Dexamethasone<rd>F0061<fd>Dextromethorphan HBr<rd>F0062<fd>Diacerein<rd>F0063<fd>Diclofenac Sodium<rd>F0064<fd>Diphenhydramine Hydrochloride<rd>F0065<fd>Domperidone<rd>F0066<fd>Doripenem<rd><DEND><ESTART>F0067<fd>Ebastine<rd>F0068<fd>Enalapril<rd>F0069<fd>Entecavir<rd>F0070<fd>Epalrestat<rd>F0071<fd>EPINASTINE<rd>F0072<fd>Escitalopram Oxalate<rd>F0073<fd>Esomeprazole<rd>F0074<fd>Etoricoxib<rd><EEND><FSTART>F0075<fd>Febuxostat<rd>F0076<fd>Fexofenadine Hydrochloride<rd>F0077<fd>Flucloxacillin<rd>F0078<fd>Fluconazole<rd>F0079<fd>Flunarizine Hydrochloride<rd>F0080<fd>Fluorometholone<rd>F0081<fd>Flupentixol Hydrochloride<rd>F0082<fd>Flupentixol Hydrochloride <rd>F0083<fd>Furosemide Spironolactone<rd>F0084<fd>Fusidic Acid Betamethasone<rd><FEND><GSTART>F0085<fd>Gabapentin<rd>F0086<fd>GATIFLOXACIN<rd>F0087<fd>Gemifloxacin Mesylate<rd>F0088<fd>Gliclazide<rd>F0089<fd>Glimepiride USP<rd>F0090<fd>Glucosamine<rd>F0091<fd>Glucose<rd>F0092<fd>Guaiphenesin<rd><GEND><HSTART>F0093<fd>Hydrocortisone Acetate<rd><HEND><ISTART>F0094<fd>Irbesartan<rd>F0095<fd>Iron Sucrose<rd><IEND><JSTART><JEND><KSTART>F0096<fd>Ketoprofen<rd>F0097<fd>Ketorolac Tromethamine<rd>F0098<fd>Ketotifen Fumarate<rd><KEND><LSTART>F0099<fd>Lactitol Monohydrate<rd>F0100<fd>Lactulose<rd>F0101<fd>Lamivudine<rd>F0102<fd>Letrozole<rd>F0103<fd>LEVOBUNOLOL<rd>F0104<fd>Levofloxacin<rd>F0105<fd>Levosalbutamol Sulfate<rd>F0106<fd>Levothyroxine Sodium<rd>F0107<fd>Linagliptin<rd>F0108<fd>Liquid Sucrose   Glycerol<rd>F0109<fd>Loratadine<rd>F0110<fd>Losartan Potassium<rd><LEND><MSTART>F0111<fd>Magaldrate   Simethicone<rd>F0112<fd>Mebeverine HCl<rd>F0113<fd>Mebhydroline<rd>F0114<fd>Meclizine Monohydrate<rd>F0115<fd>Mecobalamine<rd>F0116<fd>Medroxy Progesterone<rd>F0117<fd>Meropenem<rd>F0118<fd>Metformin HCl<rd>F0119<fd>Methyl Salicylate Menthol<rd>F0120<fd>Metoprolol Tartrate<rd>F0121<fd>Metronidazole<rd>F0122<fd>Miconazole<rd>F0123<fd>Midazolam Maleate<rd>F0124<fd>Montelukast Sodium<rd>F0125<fd>Moxifloxacin<rd>F0126<fd>Multivitamin   Multiminerals<rd>F0127<fd>Mupirocin<rd><MEND><NSTART>F0128<fd>Naproxen<rd>F0129<fd>Nitazoxanide<rd>F0130<fd>Nitroglycerin<rd>F0131<fd>Norethisterone<rd><NEND><OSTART>F0132<fd>Olopatadine<rd>F0133<fd>Omeprazole<rd>F0134<fd>Ondansetron<rd>F0135<fd>Orlistat<rd><OEND><PSTART>F0136<fd>Pantoprazole<rd>F0137<fd>Paracetamol<rd>F0138<fd>Permethrin<rd>F0139<fd>Pitavastatin<rd>F0140<fd>Pizotifen<rd>F0141<fd>Polyethylene Glycol<rd>F0142<fd>Polyethylene Glycol   Propylene Glycol<rd>F0143<fd>Potassium Citrate<rd>F0144<fd>Povidone Iodine<rd>F0145<fd>Prednisolone<rd>F0146<fd>PREDNISOLONE NEOMYCIN POLYMYXIN B<rd>F0147<fd>Pregabalin<rd><PEND><QSTART><QEND><RSTART><REND><SSTART>F0148<fd>Salmeterol Fluticasone Propionate<rd>F0149<fd>Simethicone<rd>F0150<fd>Sodium Alginate  Potassium Bicarbonate<rd>F0151<fd>Sodium Chloride<rd>F0152<fd>Sofosbuvir<rd>F0153<fd>Sucralose<rd>F0154<fd>Sulbutamol<rd>F0155<fd>Sulindac<rd>F0156<fd>Sulphamethoxazole rimethoprim<rd><SEND><TSTART>F0157<fd>Tadalafil<rd>F0158<fd>Tamsulosin Hydrochloride<rd>F0159<fd>Tapentadol<rd>F0160<fd>Terbinafin HCl<rd>F0161<fd>Thiazide Triamterene<rd>F0162<fd>Tibolone<rd>F0163<fd>Tiemonium MethylSulfate<rd>F0164<fd>Tolfenamic Acid<rd>F0165<fd>Tolperisone Hydrochloride<rd>F0166<fd>Tranexamic Acid<rd>F0167<fd>Trifluoperazine<rd>F0168<fd>Trimetazidine<rd><TEND><USTART><UEND><VSTART>F0169<fd>Vardenafil<rd>F0170<fd>Vildagliptin<rd>F0171<fd>Vildagliptin   Metformin<rd>F0172<fd>Vinpocetine<rd>F0173<fd>Vitamin B Complex<rd>F0174<fd>Vitamin E<rd><VEND><WSTART><WEND><XSTART><XEND><YSTART><YEND><ZSTART>F0175<fd>Zinc Folic Acid<rd>F0176<fd>Zinc Oxide Virgin Castor Oil<rd>F0177<fd>Zinc Vitamin B Complex<rd><ZEND>'
    opStr='<ASTART><AEND><BSTART><BEND><CSTART><CEND><DSTART><DEND><ESTART><EEND><FSTART><FEND><GSTART><GEND><HSTART><HEND><ISTART><IEND><JSTART><JEND><KSTART><KEND><LSTART><LEND><MSTART><MEND><NSTART><NEND><OSTART><OEND><PSTART><PEND><QSTART><QEND><RSTART><REND><SSTART><SEND><TSTART><TEND><USTART><UEND><VSTART><VEND><WSTART><WEND><XSTART><XEND><YSTART><YEND><ZSTART><ZEND>'
    compRow = db((db.sm_company_settings.cid == cid) & (db.sm_company_settings.status == 'ACTIVE')).select(db.sm_company_settings.cid, limitby=(0, 1))
    if not compRow:
        return 'FAILED<SYNCDATA>Invalid Company'
    else:
        repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.sync_code == synccode) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.rep_id, db.sm_rep.name, db.sm_rep.mobile_no, db.sm_rep.user_type, db.sm_rep.level_id, limitby=(0, 1))
#         return db._lastsql
        if not repRow:
           return 'FAILED<SYNCDATA>Invalid Authorization'
        else:
            user_type = repRow[0].user_type
        
        today_1= time.strftime("%Y-%m-%d")  
        today= datetime.datetime.strptime(today_1, "%Y-%m-%d")
        tomorrow =today + datetime.timedelta(days = 2)    
        docTourRow=db((db.sm_doctor_visit_plan.cid==cid) & (db.sm_doctor_visit_plan.rep_id == rep_id)  & (db.sm_doctor_visit_plan.status == 'Confirmed')  & (db.sm_doctor_visit_plan.schedule_date >= today)  & (db.sm_doctor_visit_plan.schedule_date < tomorrow)).select(db.sm_doctor_visit_plan.route_id,db.sm_doctor_visit_plan.route_name, db.sm_doctor_visit_plan.schedule_date, groupby=db.sm_doctor_visit_plan.schedule_date|db.sm_doctor_visit_plan.route_id|db.sm_doctor_visit_plan.route_name, orderby=db.sm_doctor_visit_plan.schedule_date|db.sm_doctor_visit_plan.route_id|db.sm_doctor_visit_plan.route_name)
        marketStrDoc=''
        for docTourRow in docTourRow:
            route_id = docTourRow.route_id
            route_name = docTourRow.route_name
            schedule_date = docTourRow.schedule_date
#                     market=docTourRow.sm_doctor_area.field1

            if marketStrDoc == '':
                marketStrDoc = str(route_id) + '<fd>' + str(route_name)+'<fd>' +str(schedule_date)
            else:
                marketStrDoc += '<rd>' + str(route_id) + '<fd>' + str(route_name)+ '<fd>' +str(schedule_date)
        
            
        return 'SUCCESS<SYNCDATA>' + str(marketStrDoc)


# ========Get Doc Online

def marketNext_Doc_online():
    retStatus = ''

    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.rep_pass).strip()
    synccode = str(request.vars.synccode).strip()
    market_id = str(request.vars.market_id).strip()

    client_cat = str(request.vars.client_cat).strip()
    
    scheduled_date = str(request.vars.scheduled_date).strip()
#     return rep_id
#     return market_id
#     return scheduled_date


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

            clientRows = db((db.sm_doctor_day_plan.cid == cid) & (db.sm_doctor_day_plan.area_id == market_id) & (db.sm_doctor_day_plan.rep_id == rep_id) &  (db.sm_doctor_day_plan.plan_date == scheduled_date)).select(db.sm_doctor_day_plan.doc_id, db.sm_doctor_day_plan.doc_name,db.sm_doctor_day_plan.area_name,db.sm_doctor_day_plan.area_id,db.sm_doctor_day_plan.visit_time,  orderby=db.sm_doctor_day_plan.doc_name)
#             return clientRows
            if not clientRows:
                retStatus = 'FAILED<SYNCDATA>Retailer not available'
                return retStatus
            else:
                for clientRow in clientRows:
                    client_id = clientRow.doc_id
                    name = clientRow.doc_name
                    category_id = clientRow.visit_time
#                     address=clientRow.address
                    
                    market_name=str(clientRow.area_name)

                    if clientStr == '':
                        clientStr = str(client_id) + '<fd>' + str(name)+'-' +str(market_name) + '<fd>' + str(category_id)
                    else:
                        clientStr += '<rd>' + str(client_id) + '<fd>' + str(name) +'-' +str(market_name)+ '<fd>' + str(category_id)

                return 'SUCCESS<SYNCDATA>' + clientStr
            



# ===========================Check in====================            

               # Nazma Azam 2019-02-06 start

def morningCheckInSubmit():
    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.rep_pass).strip()
    synccode = str(request.vars.synccode).strip()

    user_type = str(request.vars.user_type).strip()

    latitude = request.vars.latitude
    longitude = request.vars.longitude
    lat_long = latitude + ',' + longitude
    submit_date = str(current_date)
    submit_date_time = str(datetime_fixed)

    #                 Nazma Akhter 2019-01-19 start

    #     submit_time = str(datetime_fixed)[11:16]
    submit_time = str(datetime_fixed).split(' ')[1].split(':')[0]
    m_submit_time_s_value = ''
    m_o_submit_time_s_value = ''

    #     return submit_date_time
    #     return submit_time
    compRow = db((db.sm_company_settings.cid == cid) & (db.sm_company_settings.status == 'ACTIVE')).select(
        db.sm_company_settings.cid, limitby=(0, 1))
    if not compRow:
        return 'FAILED<SYNCDATA>Invalid Company'
    else:
        repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & ( db.sm_rep.sync_code == synccode) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.rep_id, db.sm_rep.name,db.sm_rep.mobile_no, db.sm_rep.user_type, db.sm_rep.level_id,db.sm_rep.depot_id,limitby=(0, 1))
        if not repRow:
            return 'FAILED<SYNCDATA>Invalid Authorization'

        else:
            sm_rep_name = repRow[0].name
#             #                 Nazma Akhter 2019-01-19 start
#             m_check_in_Info_select = db((db.sm_attendance.cid == cid) & (db.sm_attendance.rep_id == rep_id) & (db.sm_attendance.check_in_date == submit_date) & (db.sm_attendance.m_check_in != 'None') & (db.sm_attendance.m_check_in_latlong != '0,0')).select(db.sm_attendance.ALL, limitby=(0, 1))
# #             return m_check_in_Info_select
#             check_rep=''
#             if m_check_in_Info_select:
#                 check_rep=m_check_in_Info_select[0].rep_id
# #             return check_rep
# #             if check_rep!='':
#                 return 'FAILED<SYNCDATA>Morning checkin/checkout - Restricted.'
# 
#             else:

            m_settings_rows = db((db.sm_settings.cid == cid) & (db.sm_settings.s_key == 'm_check_in')).select(db.sm_settings.ALL, limitby=(0, 1))
            if m_settings_rows:
                m_submit_time_s_value = m_settings_rows[0].s_value

            m_o_settings_rows = db((db.sm_settings.cid == cid) & (db.sm_settings.s_key == 'm_check_out')).select( db.sm_settings.ALL, limitby=(0, 1))
            if m_o_settings_rows:
                m_o_submit_time_s_value = m_o_settings_rows[0].s_value

                #                 return submit_time
                if ((float(submit_time) >= float(m_submit_time_s_value)) and (float(submit_time) <= float(m_o_submit_time_s_value))):

                    insert_m_check_in = db.sm_attendance.insert(cid=cid, rep_id=rep_id, user_type=user_type,rep_name=sm_rep_name, check_in_date=submit_date,m_check_in=submit_date_time,m_check_in_latlong=lat_long)
                    # Nazma Azam 2019-12-21 start
                    insert_track_check_in = db.sm_tracking_table.insert(cid=cid, rep_id=rep_id, rep_name=sm_rep_name,call_type='CHECKIN',visit_date=current_date,visit_time=submit_date_time,visited_latlong=lat_long)

                    
                    if insert_m_check_in:
                        return 'SUCCESS<SYNCDATA>Morning Checkin Successfully !'
                else:
                    return 'FAILED<SYNCDATA>Morning checkin/checkout - Restricted.'


def morningCheckOutSubmit():
    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.rep_pass).strip()
    synccode = str(request.vars.synccode).strip()

    user_type = str(request.vars.user_type).strip()

    latitude = request.vars.latitude
    longitude = request.vars.longitude
    lat_long = latitude + ',' + longitude
    submit_date = str(current_date)
    submit_date_time = str(datetime_fixed)

    #                 Nazma Akhter 2019-01-19 start

    #     submit_time = str(datetime_fixed)[11:16]
    submit_time = str(datetime_fixed).split(' ')[1].split(':')[0]
    m_submit_time_s_value = ''
    m_o_submit_time_s_value = ''

    #     return submit_date_time
    #     return submit_time
    compRow = db((db.sm_company_settings.cid == cid) & (db.sm_company_settings.status == 'ACTIVE')).select(db.sm_company_settings.cid, limitby=(0, 1))
    if not compRow:
        return 'FAILED<SYNCDATA>Invalid Company'
    else:
        repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.sync_code == synccode) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.rep_id,db.sm_rep.name,db.sm_rep.mobile_no,db.sm_rep.user_type, db.sm_rep.level_id,db.sm_rep.depot_id, limitby=(0, 1))
        if not repRow:
            return 'FAILED<SYNCDATA>Invalid Authorization'

        else:
            sm_rep_name = repRow[0].name
            m_settings_rows = db((db.sm_settings.cid == cid) & (db.sm_settings.s_key == 'm_check_in')).select(db.sm_settings.ALL, limitby=(0, 1))
            if m_settings_rows:
                m_submit_time_s_value = m_settings_rows[0].s_value

            m_o_settings_rows = db((db.sm_settings.cid == cid) & (db.sm_settings.s_key == 'm_check_out')).select(db.sm_settings.ALL, limitby=(0, 1))
            if m_o_settings_rows:
                m_o_submit_time_s_value = m_o_settings_rows[0].s_value

                #                 return submit_time
                if ((float(submit_time) >= float(m_submit_time_s_value)) and ( float(submit_time) <= float(m_o_submit_time_s_value))):

                    m_check_in_Info_select = db((db.sm_attendance.cid == cid) & (db.sm_attendance.rep_id == rep_id) & ( db.sm_attendance.check_in_date == submit_date)  & (db.sm_attendance.m_check_in_latlong != '0,0')).select(db.sm_attendance.ALL, limitby=(0, 1))
                    #                     return db._lastsql
                    if m_check_in_Info_select:
                        m_check_out_Info = db((db.sm_attendance.cid == cid) & (db.sm_attendance.rep_id == rep_id) & (db.sm_attendance.check_in_date == submit_date)).update(m_check_out=submit_date_time,m_check_out_latlong=lat_long)
                       
                        # Nazma Azam 2019-12-21 start
                        insert_track_check_out = db.sm_tracking_table.insert(cid=cid, rep_id=rep_id, rep_name=sm_rep_name,call_type='CHECKIN',visit_date=current_date,visit_time=submit_date_time,visited_latlong=lat_long)


                        if m_check_out_Info:
                            return 'SUCCESS<SYNCDATA>Morning Checkout Successfully !'
                    else:
                        return 'FAILED<SYNCDATA>Morning checkin/checkout - Restricted.'

                else:
                    return 'FAILED<SYNCDATA>Morning checkin/checkout - Restricted.'


def eveningCheckInSubmit():
    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.rep_pass).strip()
    synccode = str(request.vars.synccode).strip()

    user_type = str(request.vars.user_type).strip()

    latitude = request.vars.latitude
    longitude = request.vars.longitude
    lat_long = latitude + ',' + longitude
    submit_date = str(current_date)
    submit_date_time = str(datetime_fixed)

    #     submit_time = str(datetime_fixed)[11:16]
    submit_time = str(datetime_fixed).split(' ')[1].split(':')[0]
    #     return submit_time
    e_o_submit_time_s_value = ''
    e_submit_time_s_value = ''

    #     return submit_date
    #     return submit_time
    #     return submit_date_time

    compRow = db((db.sm_company_settings.cid == cid) & (db.sm_company_settings.status == 'ACTIVE')).select(db.sm_company_settings.cid, limitby=(0, 1))
    if not compRow:
        return 'FAILED<SYNCDATA>Invalid Company'
    else:
        repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.sync_code == synccode) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.rep_id,db.sm_rep.name,db.sm_rep.mobile_no,db.sm_rep.user_type, db.sm_rep.level_id,db.sm_rep.depot_id,limitby=(0, 1))
        if not repRow:
            return 'FAILED<SYNCDATA>Invalid Authorization'

        else:
            sm_rep_name = repRow[0].name
            e_settings_rows = db((db.sm_settings.cid == cid) & (db.sm_settings.s_key == 'e_check_in')).select( db.sm_settings.ALL, limitby=(0, 1))
            if e_settings_rows:
                e_submit_time_s_value = e_settings_rows[0].s_value

            e_o_settings_rows = db((db.sm_settings.cid == cid) & (db.sm_settings.s_key == 'e_check_out')).select(db.sm_settings.ALL, limitby=(0, 1))
            #             return db._lastsql
            if e_o_settings_rows:
                e_o_submit_time_s_value = e_o_settings_rows[0].s_value

            if ((float(submit_time) >= float(e_submit_time_s_value)) and (float(submit_time) <= float(e_o_submit_time_s_value))):

#                 m_check_in_Info_select = db((db.sm_attendance.cid == cid) & (db.sm_attendance.rep_id == rep_id) & (db.sm_attendance.check_in_date == submit_date) & (db.sm_attendance.m_check_in_latlong != '0,0') & ( db.sm_attendance.m_check_out_latlong != '0,0') & (db.sm_attendance.e_check_in_latlong == '0,0')).update(e_check_in=submit_date_time, e_check_in_latlong=lat_long)
                m_check_in_Info_select = db((db.sm_attendance.cid == cid) & (db.sm_attendance.rep_id == rep_id) & (db.sm_attendance.check_in_date == submit_date) & (db.sm_attendance.m_check_in_latlong != '0,0') & (db.sm_attendance.e_check_in_latlong == '0,0')).update(e_check_in=submit_date_time, e_check_in_latlong=lat_long)

                if m_check_in_Info_select:
                    return 'SUCCESS<SYNCDATA>Evening Checkin Successfully !'

                else:
                    m_check_in_Info_select_in = db((db.sm_attendance.cid == cid) & (db.sm_attendance.rep_id == rep_id) & (db.sm_attendance.check_in_date == submit_date)).select(db.sm_attendance.ALL,limitby=(0, 1))

                    if not m_check_in_Info_select_in:
                        insert_e_check_in = db.sm_attendance.insert(cid=cid, rep_id=rep_id,rep_name=sm_rep_name, user_type=user_type,check_in_date=submit_date, e_check_in=submit_date_time,e_check_in_latlong=lat_long)
                        
                         # Nazma Azam 2019-12-21 start
                        insert_track_check_in = db.sm_tracking_table.insert(cid=cid, rep_id=rep_id, rep_name=sm_rep_name, call_type='CHECKIN',visit_date=current_date,visit_time=submit_date_time,visited_latlong=lat_long)

                        if insert_e_check_in:
                            return 'SUCCESS<SYNCDATA>Evening Checkin Successfully !'

                    else:
                        return 'FAILED<SYNCDATA>Evening checkin/checkout - Restricted.'



            else:
                return 'FAILED<SYNCDATA>Evening checkin/checkout - Restricted.'


def eveningCheckOutSubmit():
    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.rep_pass).strip()
    synccode = str(request.vars.synccode).strip()

    user_type = str(request.vars.user_type).strip()

    latitude = request.vars.latitude
    longitude = request.vars.longitude
    lat_long = latitude + ',' + longitude
    submit_date = str(current_date)
    submit_date_time = str(datetime_fixed)

    #     submit_time = str(datetime_fixed)[11:16]
    #     submit_time = str(datetime_fixed).split(' ')[1].split(':')[0]
    submit_time = str(datetime_fixed).split(' ')[1].split(':')[0] + '.' + str(datetime_fixed).split(' ')[1].split(':')[1]
    #     return submit_time
    e_submit_time_s_value = ''
    e_o_submit_time_s_value = ''

    #     return submit_date_time
    #     return submit_time
    compRow = db((db.sm_company_settings.cid == cid) & (db.sm_company_settings.status == 'ACTIVE')).select(db.sm_company_settings.cid, limitby=(0, 1))
    if not compRow:
        return 'FAILED<SYNCDATA>Invalid Company'
    else:
        repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.sync_code == synccode) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.rep_id,db.sm_rep.name,db.sm_rep.mobile_no,db.sm_rep.user_type,db.sm_rep.level_id,db.sm_rep.depot_id,limitby=(0, 1))
        if not repRow:
            return 'FAILED<SYNCDATA>Invalid Authorization'

        else:
            sm_rep_name=repRow[0].name
            e_settings_rows = db((db.sm_settings.cid == cid) & (db.sm_settings.s_key == 'e_check_in')).select(db.sm_settings.ALL, limitby=(0, 1))
            if e_settings_rows:
                e_submit_time_s_value = e_settings_rows[0].s_value

            e_o_settings_rows = db((db.sm_settings.cid == cid) & (db.sm_settings.s_key == 'e_check_out')).select( db.sm_settings.ALL, limitby=(0, 1))
            #             return db._lastsql
            if e_o_settings_rows:
                e_o_submit_time_s_value = e_o_settings_rows[0].s_value

            #             return submit_time
            if ((float(submit_time) >= float(e_submit_time_s_value)) and (float(submit_time) <= float(e_o_submit_time_s_value))):

                m_check_in_Info_select = db((db.sm_attendance.cid == cid) & (db.sm_attendance.rep_id == rep_id) & ( db.sm_attendance.check_in_date == submit_date) & (db.sm_attendance.e_check_in_latlong != '0,0') & ( db.sm_attendance.e_check_out_latlong == '0,0')).select(db.sm_attendance.ALL, limitby=(0, 1))
                #                 return db._lastsql
                if m_check_in_Info_select:

                    e_check_out_Info = db((db.sm_attendance.cid == cid) & (db.sm_attendance.rep_id == rep_id) & ( db.sm_attendance.check_in_date == submit_date) & (db.sm_attendance.e_check_in_latlong != '0,0') & (db.sm_attendance.e_check_out_latlong == '0,0')).update( e_check_out=submit_date_time, e_check_out_latlong=lat_long)
                    
                    # Nazma Azam 2019-12-21 start
                    insert_track_check_out = db.sm_tracking_table.insert(cid=cid, rep_id=rep_id, rep_name=sm_rep_name,call_type='CHECKIN',visit_date=current_date,visit_time=submit_date_time,visited_latlong=lat_long)

                    if e_check_out_Info:
                        return 'SUCCESS<SYNCDATA>Evening Checkout Successfully !'

                else:
                    return 'FAILED<SYNCDATA>Evening checkin/checkout - Restricted.'

            else:
                #                 return 'aa'
                return 'FAILED<SYNCDATA>Evening checkin/checkout - Restricted.'

                # Nazma Azam 2019-02-06 end

        


 #                 Nazma Akhter 2019-01-19 end

#            Nazma Azam 2019-01-13 end



#                 Nazma Azam 2019-01-29 start
#                 Nazma Azam 2019-01-29 start

def poultry_info_submit():

    cid = str(request.vars.cid).strip().upper()
    cm_id = str(request.vars.rep_id).strip().upper()
    cm_pass = str(request.vars.rep_pass).strip().upper()
    synccode = str(request.vars.synccode).strip().upper()
    addPName = str(request.vars.addPName).strip().upper()
    addPOName = str(request.vars.addPOName).strip()

    # Nazma Azam 2020-03-07 start
    imageName = str(request.vars.imageName).strip()
    # Nazma Azam 2020-03-07 end

     #             ===============2019-02-01 novivo2019 start ================

    tr_poultry=str(request.vars.tr_poultry).strip()
    try:
        MobileP = str(request.vars.MobileP).strip()
    except:
        MobileP='0'

    #             ===============2019-02-01 novivo2019 end ================

     # Nazma Azam 2019-02-01 start


    farm_area_id_val = tr_poultry.split('|')[1]
    farm_area_name_val = tr_poultry.split('|')[0]
     # Nazma Azam 2019-02-01 end



    AddressP = str(request.vars.AddressP).strip()
    addCDOBp = str(request.vars.addCDOBp).strip()
    anniversaryP = str(request.vars.anniversaryP).strip()
    chemist_medicine_p = str(request.vars.chemist_medicine_p).strip()
    
    managerP = str(request.vars.managerP).strip()
    consultantP = str(request.vars.consultantP).strip()
    addCCategoryP = str(request.vars.addCCategoryP).strip()
    birds_animal_p = str(request.vars.birds_animal_p).strip()

#     return scheduleDate
#     return endTime
    rearingP = str(request.vars.rearingP).strip()
    feedingP = str(request.vars.feedingP).strip()
    wateringP = str(request.vars.wateringP).strip()
#     return endTime
    broodingP = str(request.vars.broodingP).strip()
    addPondsP = str(request.vars.addPondsP).strip()
    latitude = str(request.vars.latitude).strip()

#    giftImage = str(request.vars.giftImage).strip()

    longitude = str(request.vars.longitude).strip()
#     return fdisplay_data
     # Nazma Azam 2019-02-01 start

    poultry_farm_id_text=str(request.vars.poultry_farm_id_text).strip()
    # return poultry_farm_id_text
    # Nazma Azam 2019-02-01 end

    status = ''
    if (cid == '' or cm_id == '' or cm_pass == '' or synccode == ''):
        return "Unauthorized User"
    else:
        checkRepRows = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == cm_id) & (db.sm_rep.password == cm_pass) & (db.sm_rep.status == 'ACTIVE') & (db.sm_rep.sync_code == synccode)).select(db.sm_rep.status, db.sm_rep.name, limitby=(0, 1))
        
        if checkRepRows:
            status = checkRepRows[0][db.sm_rep.status]
            rep_name = checkRepRows[0][db.sm_rep.name]
            
    if (status != 'ACTIVE'):
        return "Unauthorized User"

    if (status == 'ACTIVE'):
        
#         ================SL ready============
        checkSl = db((db.sm_settings.cid == cid) & (db.sm_settings.s_key == 'farm_sl')).select(db.sm_settings.s_value,  limitby=(0, 1))
        # return checkSl
        if checkSl:
            farm_id = int(checkSl[0][db.sm_settings.s_value]) + 1
        else:
            farm_id = 1 
      
        checkSl_update = db((db.sm_settings.cid == cid) & (db.sm_settings.s_key == 'farm_sl')).update(s_value=farm_id)

     # Nazma Azam 2019-02-01 start
        check_firm = db((db.sm_farm.cid == cid) & (db.sm_farm.farm_id == poultry_farm_id_text)).select(db.sm_farm.farm_id, orderby=~db.sm_farm.farm_id, limitby=(0, 1))
        if not check_firm:
#         if poultry_farm_id_text=='0':
     # Nazma Azam 2019-02-01 end

        #             ===============2019-02-01 novivo2019 start ================


            # Nazma Azam 2020-03-07 start
            farmInsert = db.sm_farm.insert(cid=cid, farm_id=farm_id, farm_name=addPName,farm_type='POULTRY' ,latitude=latitude, longitude=longitude, owner_name=addPOName ,route=farm_area_id_val, address=AddressP, mobile_no=MobileP, medicine=chemist_medicine_p, manger_name=managerP,consultant_name=consultantP, category=addCCategoryP, birds_animal=birds_animal_p, rearing_housing=rearingP, feeding=feedingP, watering=wateringP ,brooding=broodingP , poandsSize=addPondsP, anniversary=anniversaryP, dob=addCDOBp,image=imageName)
     # Nazma Azam 2020-03-07 end

     #             ===============2019-02-01 novivo2019 end ================
            if farmInsert:
                return 'SUCCESS<SYNCDATA>Submitted successfully!'
            else:
        #             =============== novivo2019 start ================
                return 'FAILED<SYNCDATA>Sorry ! PLease try again !'

        #             =============== novivo2019 end ================

                 # Nazma Azam 2019-02-01 start

        else:

            farm_update_select_Row = db((db.sm_farm.cid == cid) & (db.sm_farm.farm_id == poultry_farm_id_text) ).select(db.sm_farm.ALL, limitby=(0, 1))
            if farm_update_select_Row:
                #         Nazma Azam 2020-03-07 start

                poultry_update=farm_update_select_Row[0].update_record(cid=cid, farm_name=addPName,farm_type='POULTRY' ,latitude=latitude, longitude=longitude, owner_name=addPOName ,route=farm_area_id_val, address=AddressP, mobile_no=MobileP, medicine=chemist_medicine_p, manger_name=managerP,consultant_name=consultantP, category=addCCategoryP, birds_animal=birds_animal_p, rearing_housing=rearingP, feeding=feedingP, watering=wateringP ,brooding=broodingP , poandsSize=addPondsP, anniversary=anniversaryP, dob=addCDOBp,image=imageName)
                #         Nazma Azam 2020-03-07 end

                if poultry_update:
                    return 'SUCCESS<SYNCDATA>Updated successfully!'
                else:
                    return 'FAILED<SYNCDATA>Sorry ! PLease try again !'

             # Nazma Azam 2019-02-01 end

        
        

def cattleSubmit():
    
    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password=  str(request.vars.rep_pass).strip()
    synccode = str(request.vars.synccode).strip()
    farm_name=str(request.vars.farm_name)
    # imageName = str(request.vars.imageName).strip()
    owner_name=str(request.vars.owner_name).strip()
    #             ===============2019-02-01 novivo2019 start ================

    tr_cattle=str(request.vars.tr_cattle).strip()
    try:
        mobileC=str(request.vars.mobileC).strip()
    except:
        mobileC='0'

    #             ===============2019-02-01 novivo2019 end ================

     # Nazma Azam 2019-02-01 start

    # return tr_cattle
    farm_area_id_val = tr_cattle.split('|')[1]
    farm_area_name_val = tr_cattle.split('|')[0]
     # Nazma Azam 2019-02-01 end

    address=str(request.vars.address).strip().upper()
    dob=str(request.vars.add_dob).strip().decode("ascii", "ignore")
    anniversary=str(request.vars.anniversary).strip().decode("ascii", "ignore")
#     return anniversary
    medicine=str(request.vars.chemist_medicine).strip()
    
    manger_name=str(request.vars.farm_manager).strip()
    consultant_name=str(request.vars.farm_consultant).strip()
    category=str(request.vars.addCCategory).strip()
    birds_animal=str(request.vars.birds_animal).strip()
    rearing_housing=str(request.vars.rearing).strip()
    feeding=str(request.vars.feeding).strip()
    watering=str(request.vars.watering).strip()
    brooding=str(request.vars.brooding).strip()
    poandsSize=str(request.vars.ponds_bigha).strip()
    
    imageName = str(request.vars.imageName).strip()#.decode("ascii", "ignore")
    
    # Nazma Azam 2019-02-01 start

    cattle_farm_id_text=str(request.vars.cattle_farm_id_text).strip()
    # Nazma Azam 2019-02-01 end

    # return tr_cattle
    # return cattle_farm_id_text
    latitude = str(request.vars.latitude).strip()
    longitude = str(request.vars.longitude).strip()
    status = ''
    if (cid == '' or rep_id == '' or password == '' or synccode == ''):
        return "Unauthorized User"
    else:
        checkRepRows = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.status == 'ACTIVE') & (db.sm_rep.sync_code == synccode)).select(db.sm_rep.status, db.sm_rep.name, limitby=(0, 1))
#         return db._lastsql
#         return checkRepRows
        if checkRepRows:
            status = checkRepRows[0][db.sm_rep.status]
            rep_name = checkRepRows[0][db.sm_rep.name]
           
    if (status != 'ACTIVE'):
        return "Unauthorized User"

    if (status == 'ACTIVE'):
#         ================SL ready============
        checkSl = db((db.sm_settings.cid == cid) & (db.sm_settings.s_key == 'farm_sl')).select(db.sm_settings.s_value,  limitby=(0, 1))
        # return checkSl
        if checkSl:
            farm_id = int(checkSl[0][db.sm_settings.s_value]) + 1
        else:
            farm_id = 1 
      
        checkSl_update = db((db.sm_settings.cid == cid) & (db.sm_settings.s_key == 'farm_sl')).update(s_value=farm_id)
      
        
        check_firm = db((db.sm_farm.cid == cid) & (db.sm_farm.farm_id == cattle_farm_id_text)).select(db.sm_farm.farm_id, orderby=~db.sm_farm.farm_id, limitby=(0, 1))
        if not check_firm:
#         if cattle_farm_id_text=='0':

#             ===============2019-02-01 novivo2019 start ================
#             Nazma Azam 2020-03-07 start
            cattle_insert=db.sm_farm.insert(cid=cid,farm_id=farm_id,farm_name=farm_name,farm_type='CATTLE',owner_name=owner_name,route=farm_area_id_val,address=address,mobile_no=mobileC,dob=dob,anniversary=anniversary,medicine=medicine,manger_name=manger_name,consultant_name=consultant_name,category=category,birds_animal=birds_animal,rearing_housing=rearing_housing,feeding=feeding,watering=watering,brooding=brooding,poandsSize=poandsSize,image=imageName,latitude=latitude,longitude=longitude)
            # Nazma Azam 2020-03-07 end

#             ===============2019-02-01 novivo2019 end ================

    #             return client_insert
           # return farm_id
            if cattle_insert:
                return 'SUCCESS<SYNCDATA>Submitted successfully!'
            else:
             #             ===============2019-02-01 novivo2019 start ================

                return 'FAILED<SYNCDATA>Sorry ! PLease try again !'
#             ===============2019-02-01 novivo2019 end ================
     # Nazma Azam 2019-02-01 start


        else:
            farm_update_select_Row = db((db.sm_farm.cid == cid) & (db.sm_farm.farm_id == cattle_farm_id_text) ).select(db.sm_farm.ALL, limitby=(0, 1))
            if farm_update_select_Row:
                # Nazma Azam 2020-03-07 start
                cattle_update=farm_update_select_Row[0].update_record(cid=cid,farm_name=farm_name,farm_type='CATTLE',owner_name=owner_name,route=farm_area_id_val,address=address,mobile_no=mobileC,dob=dob,anniversary=anniversary,medicine=medicine,manger_name=manger_name,consultant_name=consultant_name,category=category,birds_animal=birds_animal,rearing_housing=rearing_housing,feeding=feeding,watering=watering,brooding=brooding,poandsSize=poandsSize,image=imageName,latitude=latitude,longitude=longitude)
                # Nazma Azam 2020-03-07 end

                if cattle_update:
                    return 'SUCCESS<SYNCDATA>Updated successfully!'
                else:
                    return 'FAILED<SYNCDATA>Sorry ! PLease try again !'

     # Nazma Azam 2019-02-01 end

            #
def aqua_info_submit():

    cid = str(request.vars.cid).strip().upper()
    cm_id = str(request.vars.rep_id).strip().upper()
    cm_pass = str(request.vars.rep_pass).strip().upper()
    synccode = str(request.vars.synccode).strip().upper()
    addAName = str(request.vars.addCNameA).strip().upper()
    addAOName = str(request.vars.addAOName).strip()
     #             ===============2019-02-01 novivo2019 start ================

    tr_aqua=str(request.vars.tr_aqua).strip()
    try:
        mobileA=str(request.vars.mobileA).strip()
    except:
        mobileA='0'

    #             ===============2019-02-01 novivo2019 end ================
     # Nazma Azam 2019-02-01 start


    farm_area_id_val = tr_aqua.split('|')[1]
    farm_area_name_val = tr_aqua.split('|')[0]
     # Nazma Azam 2019-02-01 end
    AddressA = str(request.vars.addressAq).strip()
    addCDOBa = str(request.vars.addCDOBa).strip()
    anniversaryA = str(request.vars.anniversaryA).strip()
    chemist_medicine_a = str(request.vars.chemist_medicine_a).strip()
    
    managerA = str(request.vars.managerA).strip()
    consultantA = str(request.vars.consultantA).strip()
    addCCategoryA= str(request.vars.addCCategoryA).strip()
    birds_animal_a = str(request.vars.birds_animal_a)
#     return birds_animal_a
#     return endTime
    rearingA = str(request.vars.rearingA).strip()
    feedingA = str(request.vars.feedingA).strip()
    wateringA = str(request.vars.wateringA).strip()
#     return endTime
    broodingA = str(request.vars.broodingA).strip()
    addPondsA = str(request.vars.addCPhoneA).strip()
    latitude = str(request.vars.latitude).strip()
#    giftImage = str(request.vars.giftImage).strip()

    longitude = str(request.vars.longitude).strip()
#     return fdisplay_data
      # Nazma Azam 2019-02-01 start
    # Nazma Azam 2020-03-07 start
    imageName = str(request.vars.imageName).strip()
    # Nazma Azam 2020-03-07 start

    aqua_farm_id_text=str(request.vars.aqua_farm_id_text).strip()
    # Nazma Azam 2019-02-01 end
    status = ''
    if (cid == '' or cm_id == '' or cm_pass == '' or synccode == ''):
        return "FAILED<SYNCDATA>Unauthorized User"
    else:
        checkRepRows = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == cm_id) & (db.sm_rep.password == cm_pass) & (db.sm_rep.status == 'ACTIVE') & (db.sm_rep.sync_code == synccode)).select(db.sm_rep.status, db.sm_rep.name, limitby=(0, 1))
          
        if checkRepRows:
            status = checkRepRows[0][db.sm_rep.status]
            rep_name = checkRepRows[0][db.sm_rep.name]
              
    if (status != 'ACTIVE'):
        return "Unauthorized User"
  
    if (status == 'ACTIVE'):
#          
# #         ================SL ready============
        checkSl = db((db.sm_settings.cid == cid) & (db.sm_settings.s_key == 'farm_sl')).select(db.sm_settings.s_value,  limitby=(0, 1))
        # return checkSl
        if checkSl:
            farm_id = int(checkSl[0][db.sm_settings.s_value]) + 1
        else:
            farm_id = 1 
      
        checkSl_update = db((db.sm_settings.cid == cid) & (db.sm_settings.s_key == 'farm_sl')).update(s_value=farm_id)

        
        
        check_firm = db((db.sm_farm.cid == cid) & (db.sm_farm.farm_id == aqua_farm_id_text)).select(db.sm_farm.farm_id, orderby=~db.sm_farm.farm_id, limitby=(0, 1))        
        if not check_firm:
      # Nazma Azam 2019-02-01 start

#         if aqua_farm_id_text=='0':
       
#             ===============2019-02-01 novivo2019 start ================

            # Nazma Azam 2020-03-07 start
            farmInsert = db.sm_farm.insert(cid=cid,farm_name=addAName, farm_id=farm_id,farm_type='AQUA',latitude=latitude, longitude=longitude, owner_name=addAOName ,route=farm_area_id_val, address=AddressA, mobile_no=mobileA, medicine=chemist_medicine_a, manger_name=managerA,consultant_name=consultantA, category=addCCategoryA, birds_animal=birds_animal_a, rearing_housing=rearingA, feeding=feedingA, watering=wateringA ,brooding=broodingA , poandsSize=addPondsA, anniversary=anniversaryA, dob=addCDOBa,image=imageName)
                # Nazma Azam 2020-03-07 end
    #             ===============2019-02-01 novivo2019 end ================
            if farmInsert:
                return 'SUCCESS<SYNCDATA>Submitted successfully!'
            else:
    #             ===============2019-02-01 novivo2019 start ================
                return 'FAILED<SYNCDATA>Sorry ! PLease try again !'

#             ===============2019-02-01 novivo2019 end ================

     # Nazma Azam 2019-02-01 start


        else:
            farm_update_select_Row = db((db.sm_farm.cid == cid) & (db.sm_farm.farm_id == aqua_farm_id_text) ).select(db.sm_farm.ALL, limitby=(0, 1))
            if farm_update_select_Row:
                # Nazma Azam   2020-03-07 start
                cattle_update=farm_update_select_Row[0].update_record(cid=cid,farm_name=addAName, farm_type='AQUA',latitude=latitude, longitude=longitude, owner_name=addAOName ,route=farm_area_id_val, address=AddressA, mobile_no=mobileA, medicine=chemist_medicine_a, manger_name=managerA,consultant_name=consultantA, category=addCCategoryA, birds_animal=birds_animal_a, rearing_housing=rearingA, feeding=feedingA, watering=wateringA ,brooding=broodingA , poandsSize=addPondsA, anniversary=anniversaryA, dob=addCDOBa,image=imageName)
                # Nazma Azam   2020-03-07 end

                if cattle_update:
                    return 'SUCCESS<SYNCDATA>Updated successfully!'
                else:
                    return 'FAILED<SYNCDATA>Sorry ! PLease try again !'

     # Nazma Azam 2019-02-01 end

def farmListData():
    cid = str(request.vars.cid).strip().upper()
    cm_id = str(request.vars.rep_id).strip().upper()
    cm_pass = str(request.vars.rep_pass).strip().upper()
    synccode = str(request.vars.synccode).strip().upper()
    farm_combo_val = str(request.vars.farm_combo_val).strip()
    farm_area_id_val = farm_combo_val.split('|')[1]
    farm_area_name_val = farm_combo_val.split('|')[0]

    # return farm_id_val


    status = ''
    if (cid == '' or cm_id == '' or cm_pass == '' or synccode == ''):
        return "FAILED<SYNCDATA>Unauthorized User"
    else:
        checkRepRows = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == cm_id) & (db.sm_rep.password == cm_pass) & (db.sm_rep.status == 'ACTIVE') & (db.sm_rep.sync_code == synccode)).select(db.sm_rep.status, db.sm_rep.name, limitby=(0, 1))
          
        if checkRepRows:
            status = checkRepRows[0][db.sm_rep.status]
            rep_name = checkRepRows[0][db.sm_rep.name]
              
    if (status != 'ACTIVE'):
        return "FAILED<SYNCDATA>Unauthorized User"
  
    if (status == 'ACTIVE'):
            farmRows = db((db.sm_farm.cid == cid) & (db.sm_farm.route == farm_area_id_val) & (db.sm_farm.status == 'ACTIVE')).select(db.sm_farm.ALL, orderby=db.sm_farm.farm_name)
            # return farmRows
            if farmRows:
                farmStr=''
                for farmRows in farmRows:
                    farm_id=str(farmRows.farm_id)
                    farm_name=str(farmRows.farm_name)
                    farm_type=str(farmRows.farm_type)
                    owner_name=str(farmRows.owner_name)
                    address=str(farmRows.address)
                    
                    dob=str(farmRows.dob)
                    anniversary=str(farmRows.anniversary)
                    medicine=str(farmRows.medicine)
                    manger_name=str(farmRows.manger_name)
                    consultant_name=str(farmRows.consultant_name)
                    category=str(farmRows.category)
                    birds_animal=str(farmRows.birds_animal)
                    rearing_housing=str(farmRows.rearing_housing)
                    feeding=str(farmRows.feeding)
                    watering=str(farmRows.watering)
                    brooding=str(farmRows.brooding)
                    poandsSize=str(farmRows.poandsSize)

                    farmStr=farmStr+str(farmRows.farm_id)+'<fd>'+str(farmRows.farm_name)+'<fd>'+str(farmRows.farm_type)+'<fd>'+str(farmRows.owner_name)+'<fd>'+str(farmRows.address)+'<fd>'+str(farmRows.dob)+'<fd>'+str(farmRows.anniversary)+'<fd>'+str(farmRows.medicine)+'<fd>'+str(farmRows.manger_name)+'<fd>'+str(farmRows.consultant_name)+'<fd>'+str(farmRows.category)+'<fd>'+str(farmRows.birds_animal)+'<fd>'+str(farmRows.rearing_housing)+'<fd>'+str(farmRows.feeding)+'<fd>'+str(farmRows.watering)+'<fd>'+str(farmRows.brooding)+'<fd>'+str(farmRows.poandsSize)+'<rd>'
                return "SUCCESS<SYNCDATA>"+farmStr
            else:
                return "FAILED<SYNCDATA>No Farm Available !"



# ============farm_info Nazma Azam 2019-02-01 start==============
def farm_info():
    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.rep_pass).strip()
    synccode = str(request.vars.synccode).strip()
    farm_Id = str(request.vars.farm_Id).strip()
    farm_combo_val_tr = str(request.vars.farm_combo_val_tr).strip()
    farm_area_id_val = farm_combo_val_tr.split('|')[1]
    farm_area_name_val = farm_combo_val_tr.split('|')[0]

    # return farm_combo_val_tr
    compRow = db((db.sm_company_settings.cid == cid) & (db.sm_company_settings.status == 'ACTIVE')).select(db.sm_company_settings.cid, limitby=(0, 1))
    if not compRow:
        return 'FAILED<SYNCDATA>Invalid Company'
    else:
        repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.sync_code == synccode) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.rep_id, db.sm_rep.name, db.sm_rep.mobile_no, db.sm_rep.user_type, db.sm_rep.level_id, db.sm_rep.depot_id, limitby=(0, 1))

        if not repRow:
           return 'FAILED<SYNCDATA>Invalid Authorization'

        else:



            farmRow = db((db.sm_farm.cid == cid) & (db.sm_farm.farm_id == farm_Id) & (db.sm_farm.route == farm_area_id_val) ).select(db.sm_farm.ALL,limitby=(0, 1))
            # return  farmRow
            farm_id =''
            farm_name =''
            route=''
            latitude=''
            longitude =''
            image =''
            farm_type =''
            owner_name =''
            address =''
            medicine =''
            manger_name =''
            consultant_name =''
            category= ''
            birds_animal =''
            rearing_housing=''
            feeding=''
            watering=''
            brooding=''
            poandsSize=''
            status=''
            anniversary=''
            dob=''
            mobile_no=''
            if farmRow:
                farm_id =farmRow[0].farm_id
                farm_name =farmRow[0].farm_name
                route =farmRow[0].route
                latitude =farmRow[0].latitude
                longitude=farmRow[0].longitude
                image=farmRow[0].image
                farm_type =farmRow[0].farm_type
                owner_name =farmRow[0].owner_name
                address =farmRow[0].address
                mobile_no=farmRow[0].mobile_no
                medicine =farmRow[0].medicine
                manger_name =farmRow[0].manger_name
                consultant_name =farmRow[0].consultant_name
                category =farmRow[0].category
                birds_animal =farmRow[0].birds_animal
                rearing_housing=farmRow[0].rearing_housing


                feeding =farmRow[0].feeding
                watering =farmRow[0].watering
                brooding =farmRow[0].brooding
                poandsSize =farmRow[0].poandsSize
                status =farmRow[0].status
                anniversary =farmRow[0].anniversary
                dob=farmRow[0].dob

#
                rtn_str=str(farm_id)+'<fdfd>'+str(farm_name)+'<fdfd>'+str(route)+'<fdfd>'+str(latitude)+'<fdfd>'+str(longitude)+'<fdfd>'+str(image)+'<fdfd>'+str(farm_type)+'<fdfd>'+str(owner_name)+'<fdfd>'+str(address)+'<fdfd>'+str(medicine)+'<fdfd>'+str(manger_name)+'<fdfd>'+str(consultant_name)+'<fdfd>'+str(category)+'<fdfd>'+str(birds_animal)+'<fdfd>'+str(rearing_housing)+'<fdfd>'+str(feeding)+'<fdfd>'+str(watering)+'<fdfd>'+str(brooding)+'<fdfd>'+str(poandsSize)+'<fdfd>'+str(status)+'<fdfd>'+str(anniversary)+'<fdfd>'+str(dob)+'<fdfd>'+str(mobile_no)

    return 'SUCCESS<SYNCDATA>'+rtn_str


def fv_submit():
    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.rep_pass).strip()
    synccode = str(request.vars.synccode).strip()
    farm_Id = str(request.vars.farm_Id).strip()
    tr_owner = str(request.vars.tr_owner).strip()
    tr_visitType = str(request.vars.tr_visitType).strip()
    tr_doctor = str(request.vars.tr_doctor).strip()
    tr_rx = str(request.vars.tr_rx).strip()
    tr_note = str(request.vars.tr_note).strip()

    # return farm_combo_val_tr
    compRow = db((db.sm_company_settings.cid == cid) & (db.sm_company_settings.status == 'ACTIVE')).select(db.sm_company_settings.cid, limitby=(0, 1))
    if not compRow:
        return 'FAILED<SYNCDATA>Invalid Company'
    else:
        repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.sync_code == synccode) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.rep_id, db.sm_rep.name, db.sm_rep.mobile_no, db.sm_rep.user_type, db.sm_rep.level_id, db.sm_rep.depot_id, limitby=(0, 1))

        if not repRow:
            return 'FAILED<SYNCDATA>Invalid Authorization'

        else:
            rep_name=repRow[0].name
            farmRow = db((db.sm_farm.cid == cid) & (db.sm_farm.farm_id == farm_Id)).select(db.sm_farm.ALL,limitby=(0, 1))
            route=''
            latitude=''
            longitude =''
            if farmRow:
                farm_name =farmRow[0].farm_name
                route =farmRow[0].route
                latitude =farmRow[0].latitude
                longitude=farmRow[0].longitude
                farm_type =farmRow[0].farm_type
            track_latlong= str(latitude)+','+str(longitude)  
            insertFarm = db.sm_farm_visit.insert(cid=cid,rep_id=rep_id,rep_name=rep_name,farm_id=farm_Id, farm_name=farm_name, route=route, latitude=latitude,longitude=longitude, farm_type=farm_type, meet_with=tr_owner, visit_type=tr_visitType, doc_support=tr_doctor, rx_value=tr_rx, note=tr_note)
            insert_track_check_in = db.sm_tracking_table.insert(cid=cid, rep_id=rep_id, rep_name=rep_name,call_type='FARM', visit_date=current_date,visit_time=datetime_fixed,visited_latlong=track_latlong,visited_id=farm_Id,visited_name=farm_name,visit_type=farm_type,area_id=route)
            
            return 'SUCCESS<SYNCDATA>'+'Sbmitted Successfully'
            
        
def checkInSubmit():
    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.rep_pass).strip()
    synccode = str(request.vars.synccode).strip()

    user_type = str(request.vars.user_type).strip()

    latitude = request.vars.latitude
    longitude = request.vars.longitude
    lat_long = latitude + ',' + longitude
    submit_date = str(current_date)
    submit_date_time = str(datetime_fixed)


    submit_time = str(datetime_fixed).split(' ')[1].split(':')[0]



    compRow = db((db.sm_company_settings.cid == cid) & (db.sm_company_settings.status == 'ACTIVE')).select(db.sm_company_settings.cid, limitby=(0, 1))
    if not compRow:
        return 'FAILED<SYNCDATA>Invalid Company'
    else:
        repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.sync_code == synccode) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.rep_id,db.sm_rep.name,limitby=(0, 1))
        if not repRow:
            return 'FAILED<SYNCDATA>Invalid Authorization'

        else:
            rep_name = repRow[0].name

            insert_check_in = db.sm_attendance.insert(cid=cid, rep_id=rep_id, user_type=user_type,rep_name=rep_name, check_in_date=submit_date,m_check_in=submit_date_time,m_check_in_latlong=lat_long,m_check_out=submit_date_time,m_check_out_latlong=lat_long,e_check_in=submit_date_time,e_check_in_latlong=lat_long,e_check_out=submit_date_time,e_check_out_latlong=lat_long)
            insert_track_check_in = db.sm_tracking_table.insert(cid=cid, rep_id=rep_id, rep_name=rep_name,call_type='CHECKIN', visit_date=current_date,visit_time=submit_date_time,visited_latlong=lat_long)

            if insert_check_in:
                return 'SUCCESS<SYNCDATA>Submitted Successfully !'

            else:
                return 'FAILED<SYNCDATA>Sorry !'

            # Nazma Azam 2020-01-16 end
            
def change_password():
     
    cid = str(request.vars.cid).strip().upper()
    rep_id=str(request.vars.rep_id).strip().upper()
    password=str(request.vars.rep_pass).strip()

    old_password=str(request.vars.old_password).strip()    
    new_password=str(request.vars.new_password).strip() 
    confirm_password = str(request.vars.confirm_password).strip()
    

    checkRep=  db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id)  & (db.sm_rep.password == password) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.rep_id,db.sm_rep.password,limitby=(0, 1))
    
    if checkRep:       

        user_password = checkRep[0].password
    
        if user_password != old_password:
            return 'FAILED<chngPass>Old password is not accurate'
        
        if (new_password!=confirm_password):
             return 'FAILED<chngPass>New & confirm password is not accurate'
        else:
            try:               
                db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id)  & (db.sm_rep.password == password) & (db.sm_rep.status == 'ACTIVE')).update(password=new_password)  
                success_msg='<table><tr><td>Password Changed Successfully.</td></tr><tr><td style="color:#FBFBFB;text-align:center;padding:2px">Please Login Again</td></tr>'
                return 'SUCCESS<chngPass>'+str(success_msg)
            except:
                return 'FAILED<chngPass>Process Error'
    else:
        return 'FAILED<chngPass>Process Error'   

#============================= Test dynamic path
def dmpath():
    # return '<start>http://127.0.0.1:8000/navana/syncmobile_new_design_raw_sql/<fd>http://i001.yeapps.com/image_hub/static/mundi_image/<fd>http://i001.yeapps.com/image_hub/mundi_image/<fd>http://127.0.0.1:8000/navana/syncmobile_new_design_raw_sql/<fd>http://127.0.0.1:8000/navana/syncmobile_new_design_raw_sql/<fd>http://127.0.0.1:8000/navana/tour_web/<fd>http://127.0.0.1:8000/navana/tour_web_members/<end>'
    
   # ====apu
    return '<start>http://127.0.0.1:8000/hamdard/syncmobile_new_design_raw_sql/<fd>http://i001.yeapps.com/image_hub/static/mundi_image/<fd>http://i001.yeapps.com/image_hub/mundi_image/<fd>http://127.0.0.1:8000/hamdard/syncmobile_new_design_raw_sql/<fd>http://127.0.0.1:8000/hamdard/syncmobile_new_design_raw_sql/<fd>http://127.0.0.1:8000/hamdard/tour_web/<fd>http://127.0.0.1:8000/hamdard/tour_web_members/<end>'
    # =====apu end
    # return '<start>http://w05.yeapps.com/novivo/syncmobile_new_design_raw/<fd>http://i001.yeapps.com/image_hub/static/mundi_image/<fd>http://i001.yeapps.com/image_hub/mundi_image/<fd>http://w05.yeapps.com/novivo/syncmobile_new_design/<fd>http://w05.yeapps.com/novivo/syncmobile_new_design_raw/<fd>http://w05.yeapps.com/novivo/tour_web/<fd>http://w05.yeapps.com/novivo/tour_web_members/<end>'
    
    # return '<start>http://127.0.0.1:8000/novivo/syncmobile_new_design/<fd>http://i001.yeapps.com/image_hub/static/mundi_image/<fd>http://i001.yeapps.com/image_hub/mundi_image/<fd>http://w05.yeapps.com/novivo/syncmobile_new_design/<fd>http://w05.yeapps.com/novivo/syncmobile_new_design/<fd>http://w05.yeapps.com/novivo/tour_web/<fd>http://w05.yeapps.com/novivo/tour_web_members/<end>'


    # return '<start>http://w05.yeapps.com/novivo/syncmobile_new_design/<fd>http://i001.yeapps.com/image_hub/static/mundi_image/<fd>http://i001.yeapps.com/image_hub/mundi_image/<fd>http://w05.yeapps.com/novivo/syncmobile_new_design/<fd>http://w05.yeapps.com/novivo/syncmobile_new_design/<fd>http://w05.yeapps.com/novivo/tour_web/<fd>http://w05.yeapps.com/novivo/tour_web_members/<end>'
   
    # return '<start>http://w05.yeapps.com/mundi/syncmobile_417_new_ibn_newtest_web/<fd>http://i001.yeapps.com/image_hub/skfahd_image/skfahd_image/<fd>http://i001.yeapps.com/image_hub/skfahd_image/skfahd_image/<fd>http://w05.yeapps.com/mundi/syncmobile_417_new_ibn_newtest_web/<fd>http://w05.yeapps.com/mundi/syncmobile_417_new_ibn_newtest_web/<fd>http://a007.yeapps.com/mundi/tour_web/<fd>http://w05.yeapps.com/mundi/tour_web_members/<end>'

