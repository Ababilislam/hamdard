
import urllib2, random, string

def index():
    session.clear()
    return dict()
    
def login_submit():
    cid = str(request.vars.cid).strip().upper()
    uid = str(request.vars.uid).strip().upper()
    password = str(request.vars.password).strip()
    mac_hdd = str(request.vars.uploadkey)
    
    session.cid = cid
    
    redirect(URL(c='default', f='check_user', vars=dict(cid=cid, uid=uid, password=password, uploadkey=mac_hdd)))
    
def check_user():
    cid = str(request.vars.cid).strip().upper()
    uid = str(request.vars.uid).strip().upper()
    password = str(request.vars.password).strip()
    
    loginSyncCode=str(request.vars.loginSyncCode)    
    if loginSyncCode=='None':
        loginSyncCode=''
        
    user_agent=str(request.vars.userAgentKey).strip()
    request_ip=request.client
    if (request_ip=='' or request_ip==None):
        request_ip='127.0.0.1'
    
    # if cid,userid,pass blank
    if (cid == '' or uid == '' or password == ''):
        session.flash = 'CID,User ID and Password required !'
        redirect(URL('index'))
        
    mac_hdd = str(request.vars.uploadkey)
    # Note: Supervisor device checking depend on settings, others device checking from cpanel
    
    # mac_hdd='123HDSN123'    # temporary used for java
    
    access_module = 'RetailerMapping'
    
    supervisorRows=db((db.sm_rep.cid==cid) & (db.sm_rep.rep_id==uid)  & (db.sm_rep.password==password)  & (db.sm_rep.user_type=='sup') & (db.sm_rep.status=='ACTIVE')).select(db.sm_rep.level_id,db.sm_rep.field2,limitby=(0,1))
    if supervisorRows:
        level_id=supervisorRows[0].level_id
        depthNo=supervisorRows[0].field2
        
        session.level_id=level_id
        session.depthNo=depthNo
        
        level = 'level' + str(depthNo)
        
        distributorList = []
        marketList=[]
        levelList=[]
        
        levelRows = db((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '1') & (db.sm_level[level] == level_id)).select(db.sm_level.level_id, orderby=db.sm_level.level_id)
        for levelRow in levelRows:
            levelid = levelRow.level_id            
            marketList.append(levelid)
        
        levelRows0 = db((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '0') & (db.sm_level[level] == level_id)).select(db.sm_level.level_id, orderby=db.sm_level.level_id)
        for levelRow0 in levelRows0:
            levelid0 = levelRow0.level_id            
            levelList.append(levelid0)
            
        levelRows2 = db((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '1') & (db.sm_level[level] == level_id)).select(db.sm_level.depot_id, groupby=db.sm_level.depot_id)
        for levelRow2 in levelRows2:
            depotid=levelRow2.depot_id
            distributorList.append(depotid)
            
        session.marketList=marketList
        session.levelList=levelList
        session.distributorList=distributorList
        
        moduleTaskStr='rm_item_view,rm_depot_view,rm_client_view,rm_rep_view,rm_reparea_view,rm_sup_view,rm_visit_list_view,rm_invoice_view,rm_analysis_view,rm_doctor_manage,rm_doctor_view,rm_doctor_visit_view'
        
        c_name='Transcom Distribution Company Ltd.'; phone='123';  email_add='tdclmohakhali@transcombd.com'; street='Sadar Road, Mohakhali, Dhaka. Ph: 9896479,9862763, 8855371-80 Ext:258 Fax:8860325'; city='Dhaka'; country='Bangladesh'; zip_code='1234'; logo=''
        companyStr=c_name+'<compfdsep>'+phone+'<compfdsep>'+email_add+'<compfdsep>'+street+'<compfdsep>'+city+'<compfdsep>'+country+'<compfdsep>'+zip_code+'<compfdsep>'+logo
        
        myDecReslutStr='success<fd>'+cid+'<fd>'+uid+'<fd>'+'Supervisor'+'<fd>6<fd>9<fd>5<fd>%s<fd>%s<fd>YESNO' %(moduleTaskStr,companyStr)
        
    else:
        mac_address = 'a'
        hdd_address = 'b'
        
    #    Get ip address
        ip_address = request_ip
        http_pass = mreporting_http_pass
        
        userText = str(cid).strip() + '<url>' + str(uid).strip() + '<url>' + str(password).strip() + '<url>' + str(mac_address) + '<url>' + str(hdd_address).strip() + '<url>' + str(ip_address).strip() + '<url>' + str(http_pass).strip() + '<url>' + str(access_module).strip()
        
        request_text = urllib2.quote(userText)
        
    #    create url to get login permission from cpanel
        #url = 'http://businesssolutionapps.appspot.com/cpanel/login_permission/check_login?login_data=' + request_text
        #url = 'http://127.0.0.1:8000/cpanel/login_permission/check_login?login_data=' + request_text
        url = 'http://e.businesssolutionapps.com/cpanel/login_permission/check_login?login_data=' + request_text
        
        try:
            result = fetch(url)
        except:
            session.flash = 'Connection Time out. Please try again after few minutes.'
            redirect(URL('index'))
            
        if (str(result).find('START') == (-1) or str(result).find('END') == (-1)):
            session.flash = 'Communication error'
            redirect(URL('index'))
        else:
            myDecReslutStr = str(result)[5:-3]
            separator = '<fd>'
            urlList = myDecReslutStr.split(separator, myDecReslutStr.count(separator))
            if len(urlList) == 2:  # Failed
                myDecReslutStr = urlList[0]
                
                
    if myDecReslutStr != 'failed':
        separator = '<fd>'
        sepCount = myDecReslutStr.count(separator)
        
        urlList = myDecReslutStr.split(separator, sepCount)
        
        if len(urlList) == 10:
            myRes = urlList[0]
            my_cid = urlList[1]
            my_uid = urlList[2]
            my_type = urlList[3]
            my_gmt = urlList[4]
            my_fromTime = urlList[5]
            my_toTime = urlList[6]
            my_task = urlList[7]
            my_companyStr = urlList[8]
            my_deviceCheck = urlList[9]
            
#            return my_task
            if myRes == 'success':
                session.cid = my_cid
                session.user_id = my_uid
                session.user_type = my_type
                session.gmt = int(my_gmt)
                session.from_time = my_fromTime
                session.to_time = my_toTime
                session.task_listStr = my_task
                session.module_id = access_module
                session.companyStr = my_companyStr                
                session.levleDepth='0'
                
                session.login_synCode=loginSyncCode
                
                #------------------- set Prefix
                session.prefix_invoice='SK'
                
                #--------------------                
                compSettingsRows = db((db.sm_company_settings.cid == session.cid) & (db.sm_company_settings.status == 'ACTIVE')).select(db.sm_company_settings.status, limitby=(0, 1))
                if compSettingsRows:
                    sysItemPerPageRows = db(db.sm_settings.cid == session.cid).select()
                    for records in sysItemPerPageRows:
                        s_key = records.s_key
                        value = records.s_value
                        if (s_key == 'ITEM_PER_PAGE'):
                            itemPerPage = int(value)
                            session.items_per_page = itemPerPage
                        elif (s_key == 'AUTO_RECEIVE'):
                            autoReceive = value
                            session.auto_receive = str(autoReceive).strip().upper()
                        elif (s_key == 'SHOW_LEVEL_FOR_DEPOT'):
                            showLevelForDepot = value
                            session.showLevelForDepot = str(showLevelForDepot).strip().upper()
                        elif (s_key == 'ERROR_PROCESS'):
                            session.error_process_flag = str(value).strip().upper()
                        elif (s_key == 'LEVEL_DEPTH'):
                            session.levleDepth = str(value).strip()
                        elif (s_key == 'LEDGER_CREATE'):
                            session.ledgerCreate = str(value).strip().upper()
                        elif (s_key == 'DEVICE_CHECK'):
                            session.deviceCheck = str(value).strip().upper()
                        elif (s_key == 'STOCK_CRON'):
                            session.stockCreate = str(value).strip().upper()
                        elif (s_key == 'MARKET_DAY'):
                            session.market_day_check = str(value).strip().upper()
                        
                        
                    if ((session.items_per_page != None)and(session.auto_receive != None)and(session.showLevelForDepot != None)):
                         #----------------------
                        item = 0
                        depot = 0
                        primary_sales = 0
                        working_area = 0
                        field_force = 0
                        client = 0
                        secondary_sales = 0
                        report = 0
                        utility_settings = 0
                        target = 0
                        office = 0
                        doctor = 0
                        ppm = 0
                        records_websettings = db((db.sm_web_settings.cid == session.cid) & (db.sm_web_settings.s_value == 1)).select(db.sm_web_settings.s_key, db.sm_web_settings.s_value)
                        for records in records_websettings:
                            s_key = records.s_key
                            value = records.s_value
                            if (s_key == 'item'):
                                item = int(value)
                            elif (s_key == 'depot'):
                                depot = int(value)
                            elif (s_key == 'primary_sales'):
                                primary_sales = int(value)
                            elif (s_key == 'working_area'):
                                working_area = int(value)
                            elif (s_key == 'field_force'):
                                field_force = int(value)
                            elif (s_key == 'client'):
                                client = int(value)
                            elif (s_key == 'secondary_sales'):
                                secondary_sales = int(value)
                            elif (s_key == 'report'):
                                report = int(value)
                            elif (s_key == 'utility_settings'):
                                utility_settings = int(value)
                            elif (s_key == 'target'):
                                target = int(value)
                            elif (s_key == 'office'):
                                office = int(value)
                            elif (s_key == 'doctor'):
                                doctor = int(value)
                            elif (s_key == 'visit'):
                                visit = int(value)
                            elif (s_key == 'ppm'):
                                ppm = int(value)

                        session.setting_item = item
                        session.setting_depot = depot
                        session.primary_sales = primary_sales
                        session.setting_working_area = working_area
                        session.field_force = field_force
                        session.setting_client = client
                        session.secondary_sales = secondary_sales
                        session.setting_report = report
                        session.utility_settings = utility_settings
                        session.setting_target = target
                        session.setting_office = office
                        session.setting_doctor = doctor
                        session.visit = visit
                        session.ppm = ppm
                        
                        #======= Level Name Settings
                        level0Name = ''
                        level1Name = ''
                        level2Name = ''
                        level3Name = ''
                        level4Name = ''
                        level5Name = ''
                        level6Name = ''
                        level7Name = ''
                        level8Name = ''
                        
                        records_levelsettings = db(db.level_name_settings.cid == session.cid).select(db.level_name_settings.ALL, orderby=db.level_name_settings.depth)
                        for records_level in records_levelsettings:
                            levelDepth = str(records_level.depth)
                            levelName = str(records_level.name)
                            if levelDepth == '0':
                                level0Name = levelName
                            elif levelDepth == '1':
                                level1Name = levelName
                            elif levelDepth == '2':
                                level2Name = levelName
                            elif levelDepth == '3':
                                level3Name = levelName
                            elif levelDepth == '4':
                                level4Name = levelName
                            elif levelDepth == '5':
                                level5Name = levelName
                            elif levelDepth == '6':
                                level6Name = levelName
                            elif levelDepth == '7':
                                level7Name = levelName
                            elif levelDepth == '8':
                                level8Name = levelName
                        
                        session.level0Name = level0Name
                        session.level1Name = level1Name
                        session.level2Name = level2Name
                        session.level3Name = level3Name
                        session.level4Name = level4Name
                        session.level5Name = level5Name
                        session.level6Name = level6Name
                        session.level7Name = level7Name
                        session.level8Name = level8Name
                        #=========== End Level Name Settings
                        
                        
                        
                        if (session.user_type == 'Depot'):
                            records_depot = db((db.sm_depot_user.cid == session.cid) & (db.sm_depot_user.user_id == session.user_id)).select(db.sm_depot_user.depot_id, limitby=(0, 1))
                            depot_id = ''
                            for records_depot in records_depot:
                                depot_id = records_depot.depot_id
                                break
                            
                            if (depot_id == '' or depot_id == None):
                                session.flash = 'Depot/Distributor not assigned, needed to assign !'
                                redirect(URL('index'))
                            else:
                                user_depot_name = ''
                                depot_category=''
                                user_depot_address=''
                                depot_short_name=''
                                depotRows = db((db.sm_depot.cid == session.cid) & (db.sm_depot.depot_id == depot_id)).select(db.sm_depot.name,db.sm_depot.depot_category,db.sm_depot.field1,db.sm_depot.short_name, limitby=(0, 1))
                                if depotRows:
                                    user_depot_name = depotRows[0].name
                                    depot_category = depotRows[0].depot_category
                                    user_depot_address=depotRows[0].field1
                                    depot_short_name=depotRows[0].short_name
                                    
                                session.depot_id = depot_id
                                session.user_depot_name = user_depot_name
                                session.user_depot_category = depot_category
                                session.user_depot_address = user_depot_address
                                session.depot_short_name = depot_short_name
                                
                                marketList=[]
                                clientRows=db((db.sm_client.cid==session.cid)&(db.sm_client.depot_id==depot_id)&(db.sm_client.status=='ACTIVE')).select(db.sm_client.area_id,groupby=db.sm_client.area_id)
                                for clRow in clientRows:
                                    areaId=clRow.area_id
                                    marketList.append(areaId)
                                    
                                session.marketList=marketList
                        
                        #===============Device Check
                        # for supervisor device check from settings, for admin/depotuser device check from cpanel
                        device_name=''
                        if session.user_type=='Supervisor':
                            if session.deviceCheck=='YES':  #& (db.sm_login_device.user_id==session.user_id)
                                deviceRows=db((db.sm_login_device.cid==session.cid)  & (db.sm_login_device.sync_code==session.login_synCode)& (db.sm_login_device.status=='Activated')).select(db.sm_login_device.ALL,limitby=(0,1))
                                if not deviceRows:
                                    session.flash = 'Unauthorized Device.Please contact with administrator !'
                                    redirect(URL('index'))                            
                                else:
                                    device_name=deviceRows[0].device_name
                                    
                        else:
                            if my_deviceCheck=='YES':   #& (db.sm_login_device.user_id==session.user_id)
                                deviceRows=db((db.sm_login_device.cid==session.cid)  & (db.sm_login_device.sync_code==session.login_synCode)& (db.sm_login_device.status=='Activated')).select(db.sm_login_device.ALL,limitby=(0,1))
                                if not deviceRows:
                                    session.flash = 'Unauthorized Device.Please contact with administrator !'
                                    redirect(URL('index'))                            
                                else:
                                    device_name=deviceRows[0].device_name
                        
                        #db.sm_login_log.insert(cid=session.cid,user_id=session.user_id,device_name=device_name,user_agent=user_agent,request_ip=request_ip,sync_code=session.login_synCode)
                        #==============
                        
                        appName = str(request.application)
                        session.appName=appName
                        
                        menuDivStr = ""
                        #================================================================== Used for menu
                        
#                         if session.setting_item == 1:
#                             if check_role('rm_item_manage') == True or check_role('rm_item_view') == True or check_role('rm_item_batch_manage') == True or check_role('rm_item_batch_view') == True or check_role('rm_item_cat_unit_manage') == True  or check_role('rm_item_cat_unit_view') == True or check_role('rm_depot_belt_manage') == True or check_role('rm_depot_belt_view') == True or check_role('rm_depot_market_manage') == True or check_role('rm_depot_market_view') == True:
#                                 menuDivStr += """ <div style=" background-color:#F2F2F2; border-radius:0px; margin:0px; padding:0px 0px 0px 0px; margin:0px; font-size:16px; height:25px; vertical-align:middle; background-image: linear-gradient( #F5F5F5 , #CACACA 50px);"><div id="item">&nbsp;BasicSettings</div></div>"""
#                                 menuDivStr += """ <div style="margin:0px; padding:0px; border:0px;">"""
#                                 menuDivStr += """ <ul >"""
#                                 if check_role('rm_item_cat_unit_manage') == True or check_role('rm_item_cat_unit_view') == True:
#                                     session.rm_item_cat_unit_manage="True"
#                                     session.rm_item_cat_unit_view="True"
#                                     
#                                 if check_role('rm_item_manage') == True or check_role('rm_item_view') == True:
#                                     menuDivStr += """ <li ><a href="/""" + appName + """/item/item"><div>Item</div></a></li>"""
#                                     
#                                 if check_role('rm_item_batch_manage') == True or check_role('rm_item_batch_view') == True:                                
#                                     menuDivStr += """ <li ><a href="/""" + appName + """/item/item_batch"><div>Item Batch</div></a></li>"""
#                                     
#                                 if check_role('rm_depot_manage') == True or check_role('rm_depot_view') == True:
#                                     menuDivStr += """<li ><a href="/""" + appName + """/depot/depot"><div>Depot/Branch</div></a></li>"""
#                                     menuDivStr += """<li ><a href="/""" + appName + """/depot_store/depot_store_add"><div>Branch-Store</div></a></li>"""
#                                     
#                                 if check_role('rm_depot_belt_manage') == True or check_role('rm_depot_belt_view') == True:
#                                     menuDivStr += """<li ><a href="/""" + appName + """/depot_belt/depot_belt_add"><div>Branch-Belt</div></a></li>"""
#                                     
#                                 if check_role('rm_depot_market_manage') == True or check_role('rm_depot_market_view') == True:
#                                     menuDivStr += """<li ><a href="/""" + appName + """/depot_market/depot_market_add"><div>Branch-Market</div></a></li>"""
#                                     
#                                 if check_role('rm_depot_type_manage') == True or check_role('rm_depot_type_view') == True:
#                                     session.rm_depot_type_manage="True"
#                                     session.rm_depot_type_view="True"
#                                     
#                                 if check_role('rm_depot_user_manage') == True or check_role('rm_depot_user_view') == True:
#                                     session.rm_depot_user_manage="True"
#                                     session.rm_depot_user_view="True"
#                                     
#                                 if check_role('rm_depot_setting_manage') == True or check_role('rm_depot_setting_view') == True:
#                                     session.rm_depot_setting_manage="True"
#                                     session.rm_depot_setting_view="True"
#                                     
#                             menuDivStr += """</ul>"""
#                             menuDivStr += """</div>"""
#                             
#                         if session.field_force == 1 or session.setting_working_area == 1 or session.utility_settings == 1:
#                             if check_role('rm_workingarea_manage') == True or check_role('rm_workingarea_view') == True  or check_role('rm_rep_manage') == True  or check_role('rm_rep_view') == True  or check_role('rm_reparea_manage') == True  or check_role('rm_reparea_view') == True  or check_role('rm_sup_manage') == True  or check_role('rm_sup_view') == True   or check_role('rm_delivery_man_manage') == True or check_role('rm_delivery_man_view') == True or check_role('rm_utility_manage') == True or check_role('rm_ff_target_manage') == True or check_role('rm_ff_target_view') == True:
#                                 
#                                 menuDivStr += """<div style=" background-color:#F2F2F2; border-radius:0px; padding:0px 0px 0px 0px; margin:0px; font-size:16px; height:25px; vertical-align:middle; background-image: linear-gradient( #F5F5F5 , #CACACA 50px);"><div id="fieldforce">&nbsp;FieldForce</div></div>"""
#                                 menuDivStr += """<div style="margin:0px; padding:0px; border:0px;">"""
#                                 menuDivStr += """<ul>"""
#                                 
#                                 if session.setting_working_area == 1:
#                                     if check_role('rm_workingarea_manage') == True or check_role('rm_workingarea_view') == True:
#                                         if session.user_type == 'Depot':
#                                             if session.showLevelForDepot == 'YES':
#                                                 menuDivStr += """<li ><a href="/""" + appName + """/level/level"><div>Area Structure</div></a></li>"""
#                                             elif session.showLevelForDepot == 'NO':
#                                                 menuDivStr += """<li ><a href="/""" + appName + """/level/area_list"><div>Area Structure</div></a></li>"""
#                                                 
#                                         else:
#                                             menuDivStr += """<li ><a href="/""" + appName + """/level/level"><div>Area Structure</div></a></li>"""
#                                 
#                                 if session.field_force == 1:
#                                     if check_role('rm_rep_manage') == True or check_role('rm_rep_view') == True or check_role('rm_reparea_manage') == True or check_role('rm_reparea_view') == True or check_role('rm_sup_manage') == True or check_role('rm_sup_view') == True or check_role('rm_delivery_man_manage') == True or check_role('rm_delivery_man_view') == True or check_role('rm_ff_target_manage') == True or check_role('rm_ff_target_view') == True:
#                                         
#                                         if check_role('rm_rep_manage') == True or check_role('rm_rep_view') == True:
#                                           menuDivStr += """<li ><a href="/""" + appName + """/representative/rep"><div>MSO</div></a></li>"""
#                                         
#                                         if check_role('rm_reparea_manage') == True or check_role('rm_reparea_view') == True:
#                                           menuDivStr += """<li ><a href="/""" + appName + """/representative/rep_area"><div>MSO-Teritory</div></a></li>"""
#                                           
#                                         if check_role('rm_sup_manage') == True or check_role('rm_sup_view') == True:
#                                           menuDivStr += """<li ><a href="/""" + appName + """/representative/supervisor_create"><div>Supervisor (RSM/FM)</div></a></li>"""
#                                           menuDivStr += """<li ><a href="/""" + appName + """/representative/supervisor_level"><div>Supervisor-Level</div></a></li>"""
#                                         
#                                         if check_role('rm_delivery_man_manage') == True or check_role('rm_delivery_man_view') == True:
#                                           menuDivStr+="""<li ><a href="/"""+appName+"""/delivery_man/delivery_man"><div>Delivery Man</div></a></li>"""
#                                           
#                                         if check_role('rm_ff_target_manage') == True or check_role('rm_ff_target_view') == True:
#                                           menuDivStr += """<li ><a href="/""" + appName + """/target/field_force_target_add"><div>Field Force Target</div></a></li>"""
#                                                 
#                                 if session.utility_settings == 1:
#                                     if check_role('rm_utility_manage') == True:
#                                         menuDivStr += """<li ><a href="/""" + appName + """/utility_mrep/utility"><div>Batch Process</div></a></li>"""
#                                 
#                                 menuDivStr += """</ul>"""
#                                 menuDivStr += """</div>"""
#                         
#                         if session.setting_client == 1 or session.setting_report == 1:
#                             if check_role('rm_client_manage') == True or check_role('rm_client_view') == True or check_role('rm_client_cat_manage') == True or check_role('rm_client_cat_view') == True or check_role('rm_client_payment_manage')==True or check_role('rm_client_payment_view')==True or check_role('rm_analysis_view') == True:                                   
#                                 menuDivStr += """<div style=" background-color:#F2F2F2; border-radius:0px; padding:0px 0px 0px 0px; margin:0px; font-size:16px; height:25px; vertical-align:middle; background-image: linear-gradient( #F5F5F5 , #CACACA 50px);"><div id="primarysale">&nbsp;Customer</div></div>"""
#                                 menuDivStr += """<div style="margin:0px; padding:0px; border:0px;">"""
#                                 
#                                 if check_role('rm_client_cat_manage') == True or check_role('rm_client_cat_view') == True:
#                                     session.rm_client_cat_manage="True"
#                                     session.rm_client_cat_view="True"
#                                     
#                                 if check_role('rm_client_manage') == True or check_role('rm_client_view') == True:
#                                     menuDivStr += """<li ><a href="/""" + appName + """/client/client"><div>Customer</div></a></li>"""
#                                 
#                                 if check_role('rm_analysis_view') == True:
#                                     if session.ledgerCreate=='YES':
#                                         menuDivStr+="""<li ><a href="/"""+appName+"""/utility/reports_home"><div>Ledger</div></a></li>"""
#                                         
#                                 menuDivStr += """</ul>"""
#                                 menuDivStr += """</div>"""
# 
#                         
#                         if session.primary_sales == 1:
#                             if check_role('rm_requisition_manage') == True or check_role('rm_requisition_view') == True or check_role('rm_stock_issue_manage') == True or check_role('rm_stock_issue_view') == True or check_role('rm_stock_receive_manage') == True or check_role('rm_stock_receive_view') == True or check_role('rm_stock_damage_manage') == True or check_role('rm_stock_damage_view') == True or check_role('rm_depot_payment_manage') == True or check_role('rm_depot_payment_view') == True or check_role('rm_stock_transfer_manage') == True or check_role('rm_stock_transfer_view') == True:
#                                 menuDivStr += """<div style=" background-color:#F2F2F2; border-radius:0px; padding:0px 0px 0px 0px; margin:0px; font-size:16px; height:25px; vertical-align:middle; background-image: linear-gradient( #F5F5F5 , #CACACA 50px);"><div id="primarysale">&nbsp;Inventory</div></div>"""
#                                 menuDivStr += """<div style="margin:0px; padding:0px; border:0px;">"""
#                                 
#                                 if check_role('rm_requisition_manage') == True or check_role('rm_requisition_view') == True:
#                                     menuDivStr += """<li ><a href="/""" + appName + """/depot/depot_stock_requisition_list"><div>Requisition</div></a></li>"""
#                                     
#                                 if check_role('rm_stock_issue_manage') == True or check_role('rm_stock_issue_view') == True:
#                                     menuDivStr += """<li ><a href="/""" + appName + """/depot/depot_stock_issue_list"><div>Transfer(Branch To Branch)</div></a></li>"""
#                                     
#                                 if check_role('rm_stock_receive_manage') == True or check_role('rm_stock_receive_view') == True:
#                                     menuDivStr += """<li ><a href="/""" + appName + """/depot/depot_stock_receive_list"><div>GR Note(Receive)</div></a></li>"""
#                                     
#                                 if check_role('rm_stock_trans_dispute_manage') == True or check_role('rm_stock_trans_dispute_view') == True:
#                                      menuDivStr += """<li ><a href="/""" + appName + """/depot/depot_trans_dispute_list"><div>Excess/Shortage</div></a></li>"""
#                                      
#                                 if check_role('rm_stock_transfer_manage') == True or check_role('rm_stock_transfer_view') == True:
#                                     menuDivStr += """<li ><a href="/""" + appName + """/depot/depot_stock_transfer_list"><div>Internal Transfer</div></a></li>"""
#                                     
#                                 if check_role('rm_stock_damage_manage') == True or check_role('rm_stock_damage_view') == True:
#                                     menuDivStr += """<li ><a href="/""" + appName + """/depot/depot_stock_damage_list"><div>Internal Adjustment</div></a></li>"""
#                                     
#                             menuDivStr += """</ul>"""
#                             menuDivStr += """</div>"""
#                         
#                         if session.visit == 1:
#                             if check_role('rm_print_manager_view')==True or check_role('rm_client_payment_manage')==True  or check_role('rm_client_payment_view')==True or check_role('rm_visit_plan_manage') == True or check_role('rm_visit_plan_view') == True or check_role('rm_visit_manage') == True or check_role('rm_visit_list_view') == True or check_role('rm_feedback_manage') == True or check_role('rm_feedback_view') == True or check_role('rm_feedback_manage') == True or check_role('rm_feedback_view') == True or check_role('rm_task_manage') == True or check_role('rm_task_view') == True:
#                                 menuDivStr += """<div style=" background-color:#F2F2F2; border-radius:0px; padding:0px 0px 0px 0px; margin:0px; font-size:16px; height:25px; vertical-align:middle; background-image: linear-gradient( #F5F5F5 , #CACACA 50px);"><div id="visit">&nbsp;Order & Invoice</div></div>"""
#                                 menuDivStr += """<div style="margin:0px; padding:0px; border:0px;">"""
#                                 menuDivStr += """<ul>"""
#                                 
#                                 if check_role('rm_visit_plan_manage') == True or check_role('rm_visit_plan_view') == True:
#                                     menuDivStr += """<li ><a href="/""" + appName + """/client_visit/visit_plan"><div>Visit Plan</div></a></li>"""
#                                 
#                                 if check_role('rm_visit_manage') == True or check_role('rm_visit_list_view') == True:
#                                     menuDivStr += """<li style="background-color:#D8EBEB;font-weight:bold"><a href="/""" + appName + """/order_invoice/order"><div>Order</div></a></li>""" #Order
#                                     if check_role('rm_analysis_view') == True:
#                                         menuDivStr += """<li ><a href="/""" + appName + """/showMap/index"><div>Map</div></a></li>"""
#                                         
#                                 if check_role('rm_feedback_manage') == True or check_role('rm_feedback_view') == True:
#                                     menuDivStr += """<li ><a href="/""" + appName + """/client_visit/complain"><div>Feedback</div></a></li>"""
#                                     
#                                 if check_role('rm_task_manage') == True or check_role('rm_task_view') == True:
#                                     menuDivStr += """<li ><a href="/""" + appName + """/client_visit/task"><div>Task</div></a></li>"""
#                                     
#                                 if session.secondary_sales == 1:
#                                     if check_role('rm_invoice_manage') == True or check_role('rm_invoice_view') == True or check_role('rm_inbox_manage')==True or check_role('rm_inbox_view')==True:
#                                         
#                                         if check_role('rm_invoice_manage') == True or check_role('rm_invoice_view') == True:
#                                             menuDivStr += """<li ><a href="/""" + appName + """/order_invoice/invoice_list"><div>Invoice/Delivery</div></a></li>"""
#         
#                                         if check_role('rm_invoice_manage') == True or check_role('rm_invoice_view') == True:
#                                             menuDivStr += """<li ><a href="/""" + appName + """/order_invoice/return_list"><div>Return</div></a></li>"""
#         
#                                         if check_role('rm_inbox_manage')==True or check_role('rm_inbox_view')==True:
#                                             menuDivStr+="""<li ><a href="/"""+appName+"""/inbox/inbox"><div>Inbox</div></a></li>"""
#         #                                
#                                 
#                                 if session.user_type=='Depot':                                    
#                                     if check_role('rm_print_manager_view')==True:
#                                         menuDivStr+="""<li style="background-color:#D8EBEB;font-weight:bold"><a href="/"""+appName+"""/print_manager/print_invoice"><div>Print Manager</div></a></li>"""
#                                         menuDivStr+="""<li style="background-color:#D8EBEB;font-weight:bold"><a href="/"""+appName+"""/print_manager/print_synopsis"><div>Synopsis</div></a></li>"""
#                                         
#                                     if check_role('rm_client_payment_manage')==True or check_role('rm_client_payment_view')==True:
#                                         menuDivStr+="""<li style="background-color:#D8EBEB;font-weight:bold"><a href="/"""+appName+"""/payment_collection/collection_list"><div>Payment Collection</div></a></li>"""
#                                         
#                                 
#                                 menuDivStr += """</ul>"""
#                                 menuDivStr += """</div>"""
#                         
#                         
#                         if session.setting_doctor==1:
#                             if check_role('rm_doctor_manage') == True or check_role('rm_doctor_view') == True or check_role('rm_doctor_visit_manage') == True or check_role('rm_doctor_visit_view') == True or check_role('rm_doctor_visit_plan_manage') == True or check_role('rm_doctor_visit_plan_view') == True or check_role('rm_doctor_inbox_manage') == True:
#                                              
#                                 menuDivStr+="""<div style=" background-color:#F2F2F2; border-radius:0px; padding:0px 0px 0px 0px; margin:0px; font-size:16px; height:25px; vertical-align:middle; background-image: linear-gradient( #F5F5F5 , #CACACA 50px);"><div id="doctor">&nbsp;DCR</div></div>"""
#                                 menuDivStr+="""<div style="margin:0px; padding:0px; border:0px;">"""
#                                 menuDivStr+="""<ul>"""
#                                  
#                                 menuDivStr+="""<li style="background-color:#D8EBEB;font-weight:bold"><a href="/"""+appName+"""/doctor_visit/doctor_visit_add"><div>Visit & Report</div></a></li>"""
#                                 menuDivStr += """<li ><a href="/""" + appName + """/dcr_report/index"><div>DCR Report
# </div></a></li>"""
#                                 #menuDivStr += """<li ><a href="/""" + appName + """/showMap_doctor/index"><div>Visit Tracking -Map</div></a></li>"""      
#                                 
#                                 menuDivStr+="""</ul>"""
#                                 menuDivStr+="""</div>"""
#                                 
#                                 if check_role('rm_doctor_manage') == True or check_role('rm_doctor_view') == True:
#                                     menuDivStr+="""<div style=" background-color:#F2F2F2; border-radius:0px; padding:0px 0px 0px 0px; margin:0px; font-size:16px; height:25px; vertical-align:middle; background-image: linear-gradient( #F5F5F5 , #CACACA 50px);"><div id="doctor">&nbsp;DCRSettings</div></div>"""
#                                     menuDivStr+="""<div style="margin:0px; padding:0px; border:0px;">"""
#                                     menuDivStr+="""<ul>"""
#                                     if check_role('rm_analysis_view') == True:
#                                          
#                                         menuDivStr+="""<li ><a href="/"""+appName+"""/doctor/doctor_list"><div>Doctor</div></a></li>"""
#                                         menuDivStr+="""<li ><a href="/"""+appName+"""/doctor_route/doctor_route_add"><div>Doctor Chamber</div></a></li>"""
#                                      
#                                     if session.user_type=='Admin':
#                                         menuDivStr+="""<li ><a href="/"""+appName+"""/doctor_gift/gift_add"><div>Gift</div></a></li>"""
#                                         if session.ppm == 1:
#                                             menuDivStr+="""<li ><a href="/"""+appName+"""/doctor_ppm/gift_add"><div>PPM</div></a></li>"""                                
#                                              
#                                     if check_role('rm_doctor_visit_plan_manage') == True or check_role('rm_doctor_visit_plan_view') == True:
#                                         menuDivStr += """<li ><a href="/""" + appName + """/doctor_visit/doctor_visit_plan"><div>Doctor Visit Plan</div></a></li>"""
#
#                                     if check_role('rm_doctor_visit_view') == True or check_role('rm_doctor_visit_view') == True:
#                                         menuDivStr += """<li ><a href="/""" + appName + """/doctor_visit/prescription_list"><div>Prescription</div></a></li>"""
#                                  
#                                  
#                                     if check_role('rm_doctor_inbox_manage') == True:
#                                         menuDivStr+="""<li ><a href="/"""+appName+"""/doctor_visit/doctor_inbox"><div>Inbox</div></a></li>"""
#                                      
#                                     menuDivStr+="""</ul>"""
#                                     menuDivStr+="""</div>"""
                        
                        if session.setting_report == 1:
                            if check_role('rm_analysis_view') == True:  #Reports
                                
                                menuDivStr += """<div style=" background-color:#F2F2F2; border-radius:0px; padding:0px 0px 0px 0px; margin:0px; font-size:16px; height:25px; vertical-align:middle; background-image: linear-gradient( #F5F5F5 , #CACACA 50px);"><div id="reports">&nbsp;Reports</div></div>"""
                                menuDivStr += """<div style="margin:0px; padding:0px; border:0px;">"""
                                menuDivStr += """<ul>"""
                                
#                                 if session.user_type=='Admin':
#                                     menuDivStr += """<li ><a href="/""" + appName + """/dashboard/dashboard"><div>Dashboard</div></a></li>"""
                                    
                                #menuDivStr += """<li ><a href="/""" + appName + """/analysis/analysis"><div>Analysis</div></a></li>"""
                                menuDivStr += """<li ><a href="/""" + appName + """/report/home"><div>Stock & Collection</div></a></li>"""
                                menuDivStr += """<li ><a href="/""" + appName + """/report_sales/home"><div>Sales</div></a></li>"""
                                menuDivStr += """<li ><a href="/""" + appName + """/report_sales2/home"><div>Sales-2</div></a></li>"""
                                menuDivStr += """<li ><a href="/""" + appName + """/report_others/home"><div>Others</div></a></li>"""
                                
                                if session.visit == 1:
                                    menuDivStr += """<li ><a href="/""" + appName + """/showMap/index"><div>Retailer Map</div></a></li>"""
                                
                                if session.setting_doctor==1:
                                    menuDivStr += """<li ><a href="/""" + appName + """/showMap_doctor/index"><div>Chambers Map</div></a></li>"""
                                
                                if check_role('rm_report_process_manage') == True:
                                    menuDivStr += """<li ><a href="/""" + appName + """/utility/process_report"><div>Process Report</div></a></li>"""
                                    
                                if session.user_type=='Depot':
                                    menuDivStr += """<li ><a href="/""" + appName + """/report/set_default_store"><div>Set Default Store</div></a></li>"""
                                    
                                menuDivStr += """</ul>"""
                                menuDivStr += """</div>"""
                        
#                         if session.utility_settings == 1:
#                             if check_role('rm_utility_manage') == True or check_role('rm_merchandizing_manage') == True:
#                                 menuDivStr += """<div style=" background-color:#F2F2F2; border-radius:0px; padding:0px 0px 0px 0px; margin:0px; font-size:16px; height:25px; vertical-align:middle; background-image: linear-gradient( #F5F5F5 , #CACACA 50px);"><div id="settings">&nbsp;Settings</div></div>"""
#                                 menuDivStr += """<div style="margin:0px; padding:0px; border:0px;">"""
#                                 menuDivStr += """<ul>"""
# 
#                                 if check_role('rm_merchandizing_manage') == True:
#                                     menuDivStr += """<li ><a href="/""" + appName + """/settings/merchandizing_item"><div>Merchandizing Item</div></a></li>"""
#                                     
#                                 if check_role('rm_utility_manage') == True:
#                                     menuDivStr += """<li ><a href="/""" + appName + """/utility_mrep/utility_settings"><div>Utility</div></a></li>"""
#                                     #menuDivStr += """<li ><a href="/""" + appName + """/settings/brand"><div>Brand</div></a></li>"""
#                                     
#                                     menuDivStr += """<li ><a href="/""" + appName + """/settings/district"><div>District</div></a></li>"""
#                                     menuDivStr += """<li ><a href="/""" + appName + """/settings/payment_mode"><div>Invoice Term</div></a></li>"""
#                                     menuDivStr += """<li ><a href="/""" + appName + """/settings/credit_note"><div>Credit Type</div></a></li>"""
#                                     menuDivStr += """<li ><a href="/""" + appName + """/settings/payment_type"><div>Payment Type</div></a></li>"""
#                                     menuDivStr += """<li ><a href="/""" + appName + """/settings/payment_adjustment_type"><div>Payment Adj. Cause</div></a></li>"""
#                                     menuDivStr += """<li ><a href="/""" + appName + """/settings/return_cause"><div>Return Cause</div></a></li>"""
#                                     
#                                     if check_role('rm_feedback_manage') == True:
#                                         menuDivStr += """<li ><a href="/""" + appName + """/settings/complain_type"><div>Complain Type</div></a></li>"""
#                                         menuDivStr += """<li ><a href="/""" + appName + """/settings/complain_from"><div>Complain From</div></a></li>"""
#                                         
#                                     if check_role('rm_task_manage') == True:
#                                         menuDivStr += """<li ><a href="/""" + appName + """/settings/task_type"><div>Task Type</div></a></li>"""
#                                         
#                                     if session.market_day_check == 'YES':
#                                         menuDivStr += """<li ><a href="/""" + appName + """/settings/market_day_add"><div>Market Day</div></a></li>"""
#                                         
#                                 menuDivStr += """</ul>"""
#                                 menuDivStr += """</div>"""
#                                 
#                         if session.utility_settings == 1:
#                             if check_role('rm_campaign_manage') == True or check_role('rm_campaign_view') == True:
#                                 menuDivStr += """<div style=" background-color:#F2F2F2; border-radius:0px; padding:0px 0px 0px 0px; margin:0px; font-size:16px; height:25px; vertical-align:middle; background-image: linear-gradient( #F5F5F5 , #CACACA 50px);"><div id="settings">&nbsp;Promotion</div></div>"""
#                                 menuDivStr += """<div style="margin:0px; padding:0px; border:0px;">"""
#                                 menuDivStr += """<ul>"""
#                                 
#                                 if check_role('rm_campaign_manage') == True or check_role('rm_campaign_view') == True:
#                                     menuDivStr += """<li ><a href="/""" + appName + """/promotion/approved_rate"><div>Approved Rate</div></a></li>"""                                    
#                                     menuDivStr += """<li ><a href="/""" + appName + """/promotion/product_bonus"><div>Product Bonus</div></a></li>"""                                
#                                     menuDivStr+="""<li ><a href="/"""+appName+"""/promotion/special_rate"><div>Special Rate</div></a></li>"""                                    
#                                     menuDivStr+="""<li ><a href="/"""+appName+"""/promotion/flat_rate"><div>Flat Rate</div></a></li>"""                                    
#                                     menuDivStr+="""<li ><a href="/"""+appName+"""/promotion/regular_discount"><div>Regular Discount</div></a></li>"""                                        
#                                     menuDivStr+="""<li ><a href="/"""+appName+"""/promotion/declared_item"><div>Declared Item</div></a></li>"""
#                                     
#                                 menuDivStr += """</ul>"""
#                                 menuDivStr += """</div>"""
#                         
#                         if session.utility_settings == 1:
#                             if check_role('rm_credit_policy_manage') == True or check_role('rm_credit_policy_view') == True:
#                                 menuDivStr += """<div style=" background-color:#F2F2F2; border-radius:0px; padding:0px 0px 0px 0px; margin:0px; font-size:16px; height:25px; vertical-align:middle; background-image: linear-gradient( #F5F5F5 , #CACACA 50px);"><div id="settings">&nbsp;CreditPolicy</div></div>"""
#                                 menuDivStr += """<div style="margin:0px; padding:0px; border:0px;">"""
#                                 menuDivStr += """<ul>"""
# 
#                                 if check_role('rm_credit_policy_manage') == True or check_role('rm_credit_policy_view') == True:
#                                     menuDivStr += """<li ><a href="/""" + appName + """/credit_policy/approved_credit"><div>Approved Credit</div></a></li>"""
#                                     menuDivStr += """<li ><a href="/""" + appName + """/credit_policy/rsm_credit"><div>RSM Credit</div></a></li>"""
#                                     menuDivStr+="""<li ><a href="/"""+appName+"""/credit_policy/special_credit"><div>Special Credit</div></a></li>"""
#                                                                     
#                                 menuDivStr += """</ul>"""
#                                 menuDivStr += """</div>"""
#                                 
#                         if session.user_type!='Supervisor':
#                             menuDivStr += """<div style=" background-color:#F2F2F2; border-radius:0px; padding:0px 0px 0px 0px; margin:0px; font-size:16px; height:25px; vertical-align:middle; background-image: linear-gradient( #F5F5F5 , #CACACA 50px);"><div id="tools">&nbsp;Tools</div></div>"""
#                             menuDivStr += """<div style="margin:0px; padding:0px; border:0px;">"""
#                             menuDivStr += """<ul>"""
#                             
#                             if check_role('rm_device_manage') == True or check_role('rm_device_view') == True:
#                                  menuDivStr += """<li ><a href="/""" + appName + """/utility/device_list"><div>Device</div></a></li>"""
#                                  
#                             if check_role('rm_user_log_view') == True:
#                                  menuDivStr += """<li ><a href="/""" + appName + """/utility/user_log"><div>User Log</div></a></li>"""
#                                  
#                             menuDivStr += """<li ><a href="/""" + appName + """/utility/password" target="_blank"><div>Change Password</div></a></li>"""
#                             menuDivStr += """</ul>"""
#                             menuDivStr += """</div>"""
                            
                        session.menuDivStr = menuDivStr
                        #======================
                        
                        redirect(URL(c='default', f='home'))
                        
                    else:
                        session.flash = 'Need settings data for item per page, auto receive and show level for depot'
                        redirect(URL('index'))
                else:
                    session.flash = 'Need Company Settings'
                    redirect(URL('index'))
            else:
                session.flash = 'Login failed'
                redirect(URL('index'))
        else:
            session.flash = 'Process error'
            redirect(URL('index'))
    else:
        session.flash = 'Invalid Authorization'
        redirect(URL('index'))

    return dict()


def home():
    if (session.cid == '' or session.user_id == '' or session.cid == None or session.user_id == None):
        redirect(URL('index'))
        
    #----------------
    response.title = 'MReporting Home'
    #-----------------
    
#    my_date=get_mydate(gmt_time=session.gmt)

    if ((session.cName == None) or (session.cName == '')):
        compStr = str(session.companyStr)
        separator = '<compfdsep>'
        compList = compStr.split(separator, compStr.count(separator))
        if len(compList) == 8:
            cName = compList[0]
            cPhone = compList[1]
            cEmail = compList[2]
            cStreet = compList[3]
            cCity = compList[4]
            cCountry = compList[5]
            cZip = compList[6]
            cLogo = compList[7]

            session.cName = cName
            session.cPhone = cPhone
            session.cEmail = cEmail
            session.cStreet = cStreet
            session.cCity = cCity
            session.cCountry = cCountry
            session.cZip = cZip
            session.cLogo = cLogo
            
            session.company_address=str(session.cStreet)+'. Mail: '+(session.cEmail)
            
        else:
            response.flash = 'internal process error in home page'
    
    
    #----- Admin user redirect
#    if session.user_type=='Admin':
#        redirect(URL('dashboard','dashboard'))
    
    
    return dict()


#===============================set depot user==========

def depot_user():
    c_id = session.cid
    #----------Task assaign----------
    task_id = 'rm_depot_user_manage'
    task_id_view = 'rm_depot_user_view'
    access_permission = check_role(task_id)
    access_permission_view = check_role(task_id_view)
    if (access_permission == False) and (access_permission_view == False):
        session.flash = 'Access is Denied !'
        redirect (URL('depot', 'depot'))

    response.title = 'Set Branch User'

    #--------paging
    if len(request.args):
        page = int(request.args[0])
    else:
        page = 0
    items_per_page = session.items_per_page
    limitby = (page * items_per_page, (page + 1) * items_per_page + 1)
    #--------end paging
    
    records = db(db.sm_depot_user.cid == c_id).select(db.sm_depot_user.id, db.sm_depot_user.user_id, db.sm_depot_user.depot_id, orderby=db.sm_depot_user.user_id, limitby=limitby)
    
    return dict(records=records, page=page, items_per_page=items_per_page, access_permission=access_permission, access_permission_view=access_permission_view)


def get_depot_user():
    import urllib2

    cid = session.cid
    http_pass = mreporting_http_pass

    if (cid != None and http_pass != ''):
        userText = str(cid).strip() + '<url>' + str(http_pass).strip()

        request_text = urllib2.quote(userText)
        #url = 'http://www.businesssolutionapps.appspot.com/cpanel/get_depot/get_depot?depot_data=' + request_text
        #url = 'http://127.0.0.1:8000/cpanel/get_depot/get_depot?depot_data=' + request_text
        url = 'http://e.businesssolutionapps.com/cpanel/get_depot/get_depot?depot_data=' + request_text
        
        result = fetch(url)
#        result= urllib2.urlopen(url)
#        result= result.read()

        if result != '':
            separator = '<user>'

            sepCount = result.count(separator)
            i = 0
            userList = result.split(separator, sepCount)
            while i < len(userList):
                user_id = userList[i]
                if user_id != '':
                   rows = db((db.sm_depot_user.cid == session.cid) & (db.sm_depot_user.user_id == user_id)).select(db.sm_depot_user.user_id, limitby=(0, 1))
                   if rows:
                        i = i + 1
                        pass
                   else:
                        depot_user_insert = db.sm_depot_user.insert(cid=session.cid, user_id=user_id)
                        i = i + 1

        redirect(URL('depot_user'))
    else:
        redirect(URL('index'))


#-----------------depot user edit---------------------
def depot_user_edit():
    c_id = session.cid
    #----------Task assaign----------
    task_id = 'rm_depot_user_manage'
    task_id_view = 'rm_depot_user_view'
    access_permission = check_role(task_id)
    access_permission_view = check_role(task_id_view)
    if (access_permission == False) and (access_permission_view == False):
        session.flash = 'Access is Denied !'
        redirect (URL('depot', 'depot_user'))
        
    query = (db.sm_depot.cid == c_id)
    db.sm_depot_user.depot_id.requires = IS_IN_DB(db(query), db.sm_depot.depot_id,'%(depot_id)s | %(name)s', orderby=db.sm_depot.depot_id)
#    return request.args(1)

    page = request.args(0)
    record = db.sm_depot_user(request.args(1))  # or redirect(URL('index'))

    form = SQLFORM(db.sm_depot_user,
                  record=record,
                  deletable=True,
                  fields=['depot_id'],
                  submit_button='Update'
                  )
    
    records = db((db.sm_depot_user.cid == c_id) & (db.sm_depot_user.id == request.args(1))).select(db.sm_depot_user.user_id, limitby=(0, 1))
    user_id = ''
    for records_show_id in records :
         user_id = records_show_id.user_id
         break

    if form.accepts(request.vars, session):
        response.flash = 'Data Update Successfully'

        redirect(URL('depot_user'))

    return dict(form=form, user_id=user_id, page=page)

#------------------item end----------------------


#=================== Logout
def log_out():
    #=============== Login log    
    #loginRows=db((db.sm_login_log.cid==session.cid) & (db.sm_login_log.user_id==session.user_id)).select(db.sm_login_log.id,orderby=~db.sm_login_log.id,limitby=(0,1))
    #if loginRows:
        #loginRows[0].update_record(logout_time=date_fixed)
        
    #==============
    redirect(URL('index'))
    
    return dict()

#=============================
def get_item_list():
    retStr = ''
    cid = session.cid
    rows = db(db.sm_item.cid == cid).select(db.sm_item.item_id, db.sm_item.name, orderby=db.sm_item.name)
    for row in rows:
        item_id = str(row.item_id)
        name = str(row.name).replace('|', ' ').replace(',', ' ')

        if retStr == '':
            retStr = item_id + '|' + name
        else:
            retStr += ',' + item_id + '|' + name

    return retStr

#=============================
def get_temp_item_list():
    retStr = ''
    cid = session.cid
    rows = db(db.sm_item_temp.cid == cid).select(db.sm_item_temp.item_id, db.sm_item_temp.name, orderby=db.sm_item_temp.name)
    for row in rows:
        item_id = str(row.item_id)
        name = str(row.name).replace('|', ' ').replace(',', ' ')

        if retStr == '':
            retStr = item_id + '|' + name
        else:
            retStr += ',' + item_id + '|' + name

    return retStr

def get_item_data_list():
    retStr = ''
    cid = session.cid
    rows = db(db.sm_item.cid == cid).select(db.sm_item.item_id, db.sm_item.name, db.sm_item.category_id, db.sm_item.dist_price, db.sm_item.price, orderby=db.sm_item.name)
    for row in rows:
        item_id = str(row.item_id)
        name = str(row.name).replace('|', ' ').replace(',', ' ')
        category_id = str(row.category_id).replace('|', ' ').replace(',', ' ')
        dist_price = str(row.dist_price)
        price = str(row.price)
        
        if retStr == '':
            retStr = name + '|' + item_id + '|' + category_id + '|' + dist_price + '|' + price
        else:
            retStr += ',' + name + '|' + item_id + '|' + category_id + '|' + dist_price + '|' + price

    return retStr

#=============Item batch List
def get_item_batch():
    retStr = ''
    cid = session.cid
    rows = db((db.sm_item_batch.cid == cid) & (db.sm_item_batch.expiary_date >= current_date)).select(db.sm_item_batch.item_id, db.sm_item_batch.name, db.sm_item_batch.batch_id,db.sm_item_batch.expiary_date, orderby=db.sm_item_batch.name)

    for row in rows:
        item_id = str(row.item_id)
        name = str(row.name).replace('|', ' ').replace(',', ' ')
        batch_id = str(row.batch_id).replace('|', ' ').replace(',', ' ')
        expiary_date=str(row.expiary_date).replace('|', ' ').replace(',', ' ')
        
        if retStr == '':
            retStr = batch_id + '|' + item_id + '|' + expiary_date
        else:
            retStr += ',' + batch_id + '|' + item_id + '|' + expiary_date
            
    return retStr

#=============Item batch List by item
def get_batch_by_item():
    retStr = ''
    cid = session.cid
    itemId=request.vars.itemId
    
    rows = db((db.sm_item_batch.cid == cid) & (db.sm_item_batch.item_id == itemId) & (db.sm_item_batch.expiary_date >= current_date)).select(db.sm_item_batch.item_id, db.sm_item_batch.name, db.sm_item_batch.batch_id,db.sm_item_batch.expiary_date, orderby=db.sm_item_batch.name)
    for row in rows:
        item_id = str(row.item_id)
        batch_id = str(row.batch_id).replace('|', ' ').replace(',', ' ')
        expiary_date=str(row.expiary_date).replace('|', ' ').replace(',', ' ')
        
        if retStr == '':
            retStr = batch_id + '|' + item_id + '|' + expiary_date
        else:
            retStr += ',' + batch_id + '|' + item_id + '|' + expiary_date
            
    return retStr

#=============Item batch List with available stock by item
def get_available_batch_by_item():
    retStr = ''
    cid = session.cid
    depotId=request.vars.depotId
    storeId=request.vars.storeId
    itemId=request.vars.itemId
    
    rows = db((db.sm_depot_stock_balance.cid == cid) & (db.sm_depot_stock_balance.depot_id == depotId) & (db.sm_depot_stock_balance.store_id == storeId) & (db.sm_depot_stock_balance.item_id == itemId) & (db.sm_depot_stock_balance.expiary_date >= current_date)&(db.sm_depot_stock_balance.quantity-db.sm_depot_stock_balance.block_qty>0)).select(db.sm_depot_stock_balance.item_id,db.sm_depot_stock_balance.batch_id,db.sm_depot_stock_balance.expiary_date,db.sm_depot_stock_balance.quantity,db.sm_depot_stock_balance.block_qty, orderby=db.sm_depot_stock_balance.expiary_date)
    for row in rows:
        item_id = str(row.item_id)
        batch_id = str(row.batch_id).replace('|', ' ').replace(',', ' ')
        expiary_date=str(row.expiary_date).replace('|', ' ').replace(',', ' ')
        quantity=row.quantity
        block_qty=row.block_qty
        availableQty=str(quantity-block_qty)
        
        if retStr == '':
            retStr = batch_id + '|' + item_id + '|' + expiary_date + '|' + availableQty
        else:
            retStr += ',' + batch_id + '|' + item_id + '|' + expiary_date + '|' + availableQty
            
    return retStr

#=============Item batch List with available stock by item
def get_available_batch_by_item_adjustment():
    retStr = ''
    cid = session.cid
    depotId=request.vars.depotId
    storeId=request.vars.storeId
    itemId=request.vars.itemId
    
    rows = db((db.sm_depot_stock_balance.cid == cid) & (db.sm_depot_stock_balance.depot_id == depotId) & (db.sm_depot_stock_balance.store_id == storeId) & (db.sm_depot_stock_balance.item_id == itemId) &(db.sm_depot_stock_balance.quantity-db.sm_depot_stock_balance.block_qty>0)).select(db.sm_depot_stock_balance.item_id,db.sm_depot_stock_balance.batch_id,db.sm_depot_stock_balance.expiary_date,db.sm_depot_stock_balance.quantity,db.sm_depot_stock_balance.block_qty, orderby=db.sm_depot_stock_balance.batch_id)
    for row in rows:
        item_id = str(row.item_id)
        batch_id = str(row.batch_id).replace('|', ' ').replace(',', ' ')
        expiary_date=str(row.expiary_date).replace('|', ' ').replace(',', ' ')
        quantity=row.quantity
        block_qty=row.block_qty
        availableQty=str(quantity-block_qty)
        
        if retStr == '':
            retStr = batch_id + '|' + item_id + '|' + expiary_date + '|' + availableQty
        else:
            retStr += ',' + batch_id + '|' + item_id + '|' + expiary_date + '|' + availableQty
            
    return retStr

def get_item_category():
    retStr = ''
    cid = session.cid
    rows = db((db.sm_category_type.cid == cid) & (db.sm_category_type.type_name == 'ITEM_CATEGORY')).select(db.sm_category_type.cat_type_id, orderby=db.sm_category_type.cat_type_id)
    for row in rows:
        cat_type_id = str(row.cat_type_id)

        if retStr == '':
            retStr = cat_type_id
        else:
            retStr += ',' + cat_type_id
    return retStr

def get_item_unit_type():
    retStr = ''
    cid = session.cid
    rows = db((db.sm_category_type.cid == cid) & (db.sm_category_type.type_name == 'ITEM_UNIT')).select(db.sm_category_type.cat_type_id, orderby=db.sm_category_type.cat_type_id)
    for row in rows:
        cat_type_id = str(row.cat_type_id)
        if retStr == '':
            retStr = cat_type_id
        else:
            retStr += ',' + cat_type_id
    return retStr
    
def get_depot_list():
    retStr = ''
    cid = session.cid
    
    if session.user_type=='Supervisor':
        rows = db((db.sm_depot.cid == cid)&(db.sm_depot.depot_id.belongs(session.distributorList))).select(db.sm_depot.depot_id, db.sm_depot.name, orderby=db.sm_depot.name)
    else:
        if session.user_type=='Depot':
            rows = db((db.sm_depot.cid == cid)&(db.sm_depot.depot_id==session.depot_id)).select(db.sm_depot.depot_id, db.sm_depot.name, orderby=db.sm_depot.name)
        else:
            rows = db(db.sm_depot.cid == cid).select(db.sm_depot.depot_id, db.sm_depot.name, orderby=db.sm_depot.name)
    
    for row in rows:
        depot_id = str(row.depot_id)
        name = str(row.name).replace('|', ' ').replace(',', ' ')

        if retStr == '':
            retStr = depot_id + '|' + name
        else:
            retStr += ',' + depot_id + '|' + name

    return retStr

def get_depot_list_all():
    retStr = ''
    cid = session.cid
    
    rows = db(db.sm_depot.cid == cid).select(db.sm_depot.depot_id, db.sm_depot.name, orderby=db.sm_depot.name)
    
    for row in rows:
        depot_id = str(row.depot_id)
        name = str(row.name).replace('|', ' ').replace(',', ' ')

        if retStr == '':
            retStr = depot_id + '|' + name
        else:
            retStr += ',' + depot_id + '|' + name

    return retStr

def get_depot_category():
    retStr = ''
    cid = session.cid
    rows = db((db.sm_category_type.cid == cid) & (db.sm_category_type.type_name == 'DEPOT_CATEGORY')).select(db.sm_category_type.cat_type_id, orderby=db.sm_category_type.cat_type_id)
    for row in rows:
        cat_type_id = str(row.cat_type_id)

        if retStr == '':
            retStr = cat_type_id
        else:
            retStr += ',' + cat_type_id

    return retStr

def get_receive_depot_list():
    retStr = ''
    cid = session.cid
    
#     qset = db()
#     qset = qset(db.sm_depot_settings.cid == cid)
#     qset = qset(db.sm_depot_settings.from_to_type == 'Receive')
#     qset = qset(db.sm_depot.cid == cid)
#     qset = qset(db.sm_depot.depot_id == db.sm_depot_settings.depot_id_from_to)
#     records = qset.select(db.sm_depot_settings.depot_id_from_to, db.sm_depot.name, orderby=db.sm_depot_settings.depot_id, groupby=db.sm_depot_settings.depot_id_from_to)
    
    qset = db()
    qset = qset(db.sm_depot.cid == cid)
    records = qset.select(db.sm_depot.depot_id, db.sm_depot.name, orderby=db.sm_depot.depot_id)
    
    for row in records:
        depot_id = str(row.depot_id)
        name = str(row.name).replace('|', ' ').replace(',', ' ')
        
        if retStr == '':
            retStr = depot_id + '|' + name
        else:
            retStr += ',' + depot_id + '|' + name

    return retStr

def get_level_list():
    retStr = ''
    cid = session.cid
    rows = db(db.sm_level.cid == cid).select(db.sm_level.level_id, db.sm_level.level_name, orderby=db.sm_level.level_name)
    for row in rows:
        level_id = str(row.level_id)
        name = str(row.level_name).replace('|', ' ').replace(',', ' ')

        if retStr == '':
            retStr = level_id + '|' + name
        else:
            retStr += ',' + level_id + '|' + name
            
    return retStr

#after level0
def get_level1_list():
    retStr = ''
    cid = session.cid    
    level1ParentId = request.vars.level1ParentId
    if not(level1ParentId=='' or level1ParentId==None):
        rows = db((db.sm_level.cid == cid)&(db.sm_level.parent_level_id == level1ParentId)&(db.sm_level.depth == 1)).select(db.sm_level.level_id, db.sm_level.level_name, orderby=db.sm_level.level_name)
    else:
        rows = db((db.sm_level.cid == cid)&(db.sm_level.depth == 1)).select(db.sm_level.level_id, db.sm_level.level_name, orderby=db.sm_level.level_name)
        
    for row in rows:
        level_id = str(row.level_id)
        name = str(row.level_name).replace('|', ' ').replace(',', ' ')

        if retStr == '':
            retStr = level_id + '|' + name
        else:
            retStr += ',' + level_id + '|' + name
            
    return retStr

#after level1
def get_level2_list():
    retStr = ''
    cid = session.cid    
    level2ParentId = request.vars.level2ParentId
    if not(level2ParentId=='' or level2ParentId==None):
        rows = db((db.sm_level.cid == cid)&(db.sm_level.parent_level_id == level2ParentId)&(db.sm_level.depth == 2)).select(db.sm_level.level_id, db.sm_level.level_name, orderby=db.sm_level.level_name)
    else:
        rows = db((db.sm_level.cid == cid)&(db.sm_level.depth == 2)).select(db.sm_level.level_id, db.sm_level.level_name, orderby=db.sm_level.level_name)
        
    for row in rows:
        level_id = str(row.level_id)
        name = str(row.level_name).replace('|', ' ').replace(',', ' ')

        if retStr == '':
            retStr = level_id + '|' + name
        else:
            retStr += ',' + level_id + '|' + name
            
    return retStr

#after level2
def get_level3_list():
    retStr = ''
    cid = session.cid    
    level3ParentId = request.vars.level3ParentId
    if not(level3ParentId=='' or level3ParentId==None):
        rows = db((db.sm_level.cid == cid)&(db.sm_level.parent_level_id == level3ParentId)&(db.sm_level.depth == 3)).select(db.sm_level.level_id, db.sm_level.level_name, orderby=db.sm_level.level_name)
    else:
        rows = db((db.sm_level.cid == cid)&(db.sm_level.depth == 3)).select(db.sm_level.level_id, db.sm_level.level_name, orderby=db.sm_level.level_name)
        
    for row in rows:
        level_id = str(row.level_id)
        name = str(row.level_name).replace('|', ' ').replace(',', ' ')

        if retStr == '':
            retStr = level_id + '|' + name
        else:
            retStr += ',' + level_id + '|' + name
            
    return retStr

def get_only_level_list():
    retStr = ''
    cid = session.cid
    
    if session.user_type=='Supervisor':
        level = 'level' + str(session.depthNo)
        levelId=session.level_id
        
        rows = db((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '0') & (db.sm_level.level_id == levelId)).select(db.sm_level.level_id, db.sm_level.level_name, orderby=db.sm_level.level_name)
    else:
        rows = db((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '0')).select(db.sm_level.level_id, db.sm_level.level_name, orderby=db.sm_level.level_name)
    
    for row in rows:
        level_id = str(row.level_id)
        name = str(row.level_name).replace('|', ' ').replace(',', ' ')

        if retStr == '':
            retStr = level_id + '|' + name
        else:
            retStr += ',' + level_id + '|' + name

    return retStr


def get_region_list():
    retStr = ''
    cid = session.cid
    
    #---- supervisor
    if session.user_type=='Supervisor':
        level_id=session.level_id
        depthNo=session.depthNo
        level = 'level' + str(depthNo)
        
        rows = db((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '0') & (db.sm_level.depth == 0)& (db.sm_level[level] == level_id)).select(db.sm_level.level_id, db.sm_level.level_name, orderby=db.sm_level.level_name)
        
    else:
        rows = db((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '0') & (db.sm_level.depth == 0)).select(db.sm_level.level_id, db.sm_level.level_name, orderby=db.sm_level.level_name)
    
    for row in rows:
        level_id = str(row.level_id)
        name = str(row.level_name).replace('|', ' ').replace(',', ' ')
        
        if retStr == '':
            retStr = level_id + '|' + name
        else:
            retStr += ',' + level_id + '|' + name
            
    return retStr

def get_area_list():
    retStr = ''
    cid = session.cid
    repid = str(request.vars.repid).split('|')[0].upper()
    depot = str(request.vars.depot).split('|')[0].upper()
    
#    if not(repid=='' or repid=='NONE'):
#        repRows = db((db.sm_rep.cid == cid) & (db.sm_rep.user_type == 'rep')& (db.sm_rep.rep_id == repid)).select(db.sm_rep.depot_id,limitby=(0,1))
#        if repRows:
#            depot=repRows[0].depot_id
    #& (db.sm_level.depot_id == session.depot_id) level not used in level
    
    if session.user_type == 'Depot':
        rows = db((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '1')).select(db.sm_level.level_id, db.sm_level.level_name, orderby=db.sm_level.level_name)
    else:
        if session.user_type=='Supervisor':
            level = 'level' + str(session.depthNo)
            levelId=session.level_id
            
            rows = db((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '1') & (db.sm_level[level] == levelId)).select(db.sm_level.level_id, db.sm_level.level_name, orderby=db.sm_level.level_name)
        else:
            if depot=='' or depot=='NONE':
                rows = db((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '1')).select(db.sm_level.level_id, db.sm_level.level_name, orderby=db.sm_level.level_name)
            else:
                rows = db((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '1')).select(db.sm_level.level_id, db.sm_level.level_name, orderby=db.sm_level.level_name)
                #& (db.sm_level.depot_id == depot) level not used in level
    for row in rows:
        level_id = str(row.level_id)
        name = str(row.level_name).replace('|', ' ').replace(',', ' ')

        if retStr == '':
            retStr = level_id + '|' + name
        else:
            retStr += ',' + level_id + '|' + name
            
    return retStr

def get_rep_list():
    retStr = ''
    cid = session.cid
    
#    if session.user_type == 'Depot':
#        rows = db((db.sm_rep.cid == cid) & (db.sm_rep.user_type == 'rep') & (db.sm_rep.depot_id == session.depot_id)).select(db.sm_rep.rep_id, db.sm_rep.name, db.sm_rep.mobile_no, orderby=db.sm_rep.name)
#    else:
    if session.user_type=='Supervisor':
        repList=[]
        reprows = db((db.sm_rep_area.cid == cid)&(db.sm_rep_area.area_id.belongs(session.marketList))).select(db.sm_rep_area.rep_id,groupby=db.sm_rep_area.rep_id)
        for reprow in reprows:
            repList.append(reprow.rep_id)
            
        rows = db((db.sm_rep.cid == cid) & (db.sm_rep.user_type == 'rep')& (db.sm_rep.rep_id.belongs(repList))).select(db.sm_rep.rep_id, db.sm_rep.name, db.sm_rep.mobile_no, orderby=db.sm_rep.name)
        
    else:
        rows = db((db.sm_rep.cid == cid) & (db.sm_rep.user_type == 'rep')).select(db.sm_rep.rep_id, db.sm_rep.name, db.sm_rep.mobile_no, orderby=db.sm_rep.name)
            
    for row in rows:
        rep_id = str(row.rep_id)
        name = str(row.name).replace('|', ' ').replace(',', ' ')
        mobile_no = str(row.mobile_no)

        if retStr == '':
            retStr = rep_id + '|' + name + '|' + mobile_no
        else:
            retStr += ',' + rep_id + '|' + name + '|' + mobile_no

    return retStr

def get_depot_rep_list():
    retStr = ''
    cid = session.cid
    #depot = request.vars.depot  # depot id not used in rep
    
#    if session.user_type == 'Depot':
#        rows = db((db.sm_rep.cid == cid) & (db.sm_rep.user_type == 'rep') & (db.sm_rep.status == 'ACTIVE')& (db.sm_rep.depot_id == session.depot_id)).select(db.sm_rep.rep_id, db.sm_rep.name, db.sm_rep.mobile_no, orderby=db.sm_rep.name)
#    else:
#    if session.user_type=='Supervisor':        
#        rows = db((db.sm_rep.cid == cid) & (db.sm_rep.user_type == 'rep') & (db.sm_rep.status == 'ACTIVE')& (db.sm_rep.depot_id.belongs(session.distributorList))).select(db.sm_rep.rep_id, db.sm_rep.name, db.sm_rep.mobile_no, orderby=db.sm_rep.name)
#    else:
    rows = db((db.sm_rep.cid == cid) & (db.sm_rep.user_type == 'rep') & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.rep_id, db.sm_rep.name, db.sm_rep.mobile_no, orderby=db.sm_rep.name)
    
    for row in rows:
        rep_id = str(row.rep_id)
        name = str(row.name).replace('|', ' ').replace(',', ' ')
        mobile_no = str(row.mobile_no)

        if retStr == '':
            retStr = rep_id + '|' + name + '|' + mobile_no
        else:
            retStr += ',' + rep_id + '|' + name + '|' + mobile_no

    return retStr


def get_customer_rep_list():
    retStr = ''
    cid = session.cid
    clientID = request.vars.clientID
    
    if session.user_type == 'Depot':
        rows = db((db.sm_client.cid == cid) & (db.sm_client.depot_id == session.depot_id)& (db.sm_client.client_id == clientID)).select(db.sm_client.area_id,limitby=(0,1))
    else:
        rows = db((db.sm_client.cid == cid)& (db.sm_client.client_id == clientID)).select(db.sm_client.area_id,limitby=(0,1))
    area_id=''
    if rows:
        area_id=rows[0].area_id
    
    rows = db((db.sm_rep_area.cid == cid) & (db.sm_rep_area.area_id == area_id)&(db.sm_rep.cid == cid) &(db.sm_rep.status == 'ACTIVE') & (db.sm_rep.rep_id == db.sm_rep_area.rep_id)).select(db.sm_rep.rep_id, db.sm_rep.name,orderby=db.sm_rep.name)
    for row in rows:
        rep_id = str(row.rep_id)
        name = str(row.name).replace('|', ' ').replace(',', ' ')
        
        if retStr == '':
            retStr = rep_id + '|' + name
        else:
            retStr += ',' + rep_id + '|' + name

    return retStr


def get_customer_ff_list():
    retStr = ''
    cid = session.cid
    
    clientID = request.vars.clientID
    
    if session.user_type == 'Depot':
        rows = db((db.sm_client.cid == cid) & (db.sm_client.depot_id == session.depot_id)& (db.sm_client.client_id == clientID)).select(db.sm_client.area_id,limitby=(0,1))
    else:
        rows = db((db.sm_client.cid == cid)& (db.sm_client.client_id == clientID)).select(db.sm_client.area_id,limitby=(0,1))
    area_id=''
    if rows:
        area_id=rows[0].area_id
    
    rows = db((db.sm_rep_area.cid == cid) & (db.sm_rep_area.area_id == area_id)&(db.sm_rep.cid == cid) &(db.sm_rep.status == 'ACTIVE') & (db.sm_rep.rep_id == db.sm_rep_area.rep_id)).select(db.sm_rep.rep_id, db.sm_rep.name,orderby=db.sm_rep.name)
    for row in rows:
        rep_id = str(row.rep_id)
        name = str(row.name).replace('|', ' ').replace(',', ' ')
        
        if retStr == '':
            retStr = rep_id + '|' + name
        else:
            retStr += ',' + rep_id + '|' + name
            
    #-------------------
    levelList=[]
    levelRows = db((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '1') & (db.sm_level.level_id == area_id)).select(db.sm_level.level0,db.sm_level.level1,db.sm_level.level2,db.sm_level.level3,limitby=(0,1))
    if levelRows:
        levelList.append(levelRows[0].level0)
        levelList.append(levelRows[0].level1)
        levelList.append(levelRows[0].level2)
        levelList.append(levelRows[0].level3)
    
    rows = db((db.sm_supervisor_level.cid == cid) & (db.sm_supervisor_level.level_id.belongs(levelList))& (db.sm_rep.cid == cid)& (db.sm_rep.user_type == 'sup')& (db.sm_rep.rep_id == db.sm_supervisor_level.sup_id)).select(db.sm_rep.rep_id, db.sm_rep.name, orderby=db.sm_rep.name)
    for row in rows:
        rep_id = str(row.rep_id)
        name = str(row.name).replace('|', ' ').replace(',', ' ')
        
        if retStr == '':
            retStr = rep_id + '|' + name
        else:
            retStr += ',' + rep_id + '|' + name
    
    return retStr



def get_all_ff_list():
    retStr = ''
    cid = session.cid
    depot = str(request.vars.depot).split('|')[0].upper()
    
    if session.user_type=='Supervisor':
        repList=[]
        reprows = db((db.sm_rep_area.cid == cid)&(db.sm_rep_area.area_id.belongs(session.marketList))).select(db.sm_rep_area.rep_id,groupby=db.sm_rep_area.rep_id)
        for reprow in reprows:
            repList.append(reprow.rep_id)
            
        rows = db((db.sm_rep.cid == cid) & (db.sm_rep.user_type == 'rep')& (db.sm_rep.rep_id.belongs(repList))).select(db.sm_rep.rep_id, db.sm_rep.name, db.sm_rep.mobile_no, orderby=db.sm_rep.name)
        
    else:
#        if session.user_type == 'Depot':
#            rows = db((db.sm_rep.cid == cid) & (db.sm_rep.user_type == 'rep') & (db.sm_rep.depot_id == session.depot_id)).select(db.sm_rep.rep_id, db.sm_rep.name, db.sm_rep.mobile_no, orderby=db.sm_rep.name)
#        else:
#        if depot=='' or depot=='NONE':
        rows = db(db.sm_rep.cid == cid).select(db.sm_rep.rep_id, db.sm_rep.name, db.sm_rep.mobile_no, orderby=db.sm_rep.name)
#        else:
#            rows = db((db.sm_rep.cid == cid) & (db.sm_rep.depot_id == depot)).select(db.sm_rep.rep_id, db.sm_rep.name, db.sm_rep.mobile_no, orderby=db.sm_rep.name)
    
    for row in rows:
        rep_id = str(row.rep_id)
        name = str(row.name).replace('|', ' ').replace(',', ' ')
        mobile_no = str(row.mobile_no)
        
        if retStr == '':
            retStr = rep_id + '|' + name + '|' + mobile_no
        else:
            retStr += ',' + rep_id + '|' + name + '|' + mobile_no
    
    
    # with sup list
    if session.user_type=='Supervisor':        
        supList=[]
        level = 'level' + str(session.depthNo)
        levelId=session.level_id
        
        supRows = db((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '0') & (db.sm_level[level] == levelId)).select(db.sm_level.level_id,orderby=db.sm_level.level_id)
        for supRow in supRows:
            supList.append(supRow.level_id)
        
        rows = db((db.sm_rep.cid == cid) & (db.sm_rep.user_type == 'sup')& (db.sm_rep.level_id.belongs(supList))).select(db.sm_rep.rep_id, db.sm_rep.name, db.sm_rep.mobile_no, orderby=db.sm_rep.name)
        for row in rows:
            rep_id = str(row.rep_id)
            name = str(row.name).replace('|', ' ').replace(',', ' ')
            mobile_no = str(row.mobile_no)
            
            if retStr == '':
                retStr = rep_id + '|' + name + '|' + mobile_no
            else:
                retStr += ',' + rep_id + '|' + name + '|' + mobile_no
    
    return retStr



def get_supervisor_list():
    retStr = ''
    cid = session.cid

    rows = db((db.sm_rep.cid == cid) & (db.sm_rep.user_type == 'sup')).select(db.sm_rep.rep_id, db.sm_rep.name, db.sm_rep.mobile_no, orderby=db.sm_rep.name)

    for row in rows:
        rep_id = str(row.rep_id)
        name = str(row.name).replace('|', ' ').replace(',', ' ')
        mobile_no = str(row.mobile_no)

        if retStr == '':
            retStr = rep_id + '|' + name + '|' + mobile_no
        else:
            retStr += ',' + rep_id + '|' + name + '|' + mobile_no

    return retStr

def get_delivery_man_list():
    retStr = ''
    cid = session.cid
    
    if session.user_type == 'Depot':
        rows = db((db.sm_delivery_man.cid == cid) & (db.sm_delivery_man.depot_id == session.depot_id)).select(db.sm_delivery_man.d_man_id, db.sm_delivery_man.name, orderby=db.sm_delivery_man.name)
    else:
        rows = db(db.sm_delivery_man.cid == cid).select(db.sm_delivery_man.d_man_id, db.sm_delivery_man.name, orderby=db.sm_delivery_man.name)
        
    for row in rows:
        d_man_id = str(row.d_man_id)
        name = str(row.name).replace('|', ' ').replace(',', ' ')
        
        if retStr == '':
            retStr = d_man_id + '|' + name
        else:
            retStr += ',' + d_man_id + '|' + name

    return retStr

def get_depot_delivery_man_list():
    retStr = ''
    cid = session.cid
    depot = request.vars.depot
    
    rows = db((db.sm_delivery_man.cid == cid) & (db.sm_delivery_man.depot_id == depot) & (db.sm_delivery_man.status == 'ACTIVE')).select(db.sm_delivery_man.d_man_id, db.sm_delivery_man.name, orderby=db.sm_delivery_man.name)

    for row in rows:
        d_man_id = str(row.d_man_id)
        name = str(row.name).replace('|', ' ').replace(',', ' ')

        if retStr == '':
            retStr = d_man_id + '|' + name
        else:
            retStr += ',' + d_man_id + '|' + name

    return retStr

def get_client_list():
    retStr = ''
    cid = session.cid

    if session.user_type == 'Depot':
        rows = db((db.sm_client.cid == cid) & (db.sm_client.depot_id == session.depot_id)).select(db.sm_client.client_id, db.sm_client.name, orderby=db.sm_client.name)
    else:
        if session.user_type=='Supervisor':
            rows = db((db.sm_client.cid == cid)&(db.sm_client.area_id.belongs(session.marketList))).select(db.sm_client.client_id, db.sm_client.name, orderby=db.sm_client.name)
        else:
            rows = db(db.sm_client.cid == cid).select(db.sm_client.client_id, db.sm_client.name, orderby=db.sm_client.name)
    
    for row in rows:
        client_id = str(row.client_id)
        name = str(row.name).replace('|', ' ').replace(',', ' ')

        if retStr == '':
            retStr = client_id + '|' + name
        else:
            retStr += ',' + client_id + '|' + name

    return retStr
    
def get_depot_client_list():
    retStr = ''
    cid = session.cid
    depot = request.vars.depot
    
    rows = db((db.sm_client.cid == cid) & (db.sm_client.depot_id == depot) & (db.sm_client.status == 'ACTIVE')).select(db.sm_client.client_id, db.sm_client.name, orderby=db.sm_client.name)

    for row in rows:
        client_id = str(row.client_id)
        name = str(row.name).replace('|', ' ').replace(',', ' ')

        if retStr == '':
            retStr = client_id + '|' + name
        else:
            retStr += ',' + client_id + '|' + name
            
    return retStr

def get_depot_client_all_list():
    retStr = ''
    cid = session.cid
    depot = request.vars.depot
    
    rows = db((db.sm_client.cid == cid) & (db.sm_client.depot_id == depot)).select(db.sm_client.client_id, db.sm_client.name, orderby=db.sm_client.name)

    for row in rows:
        client_id = str(row.client_id)
        name = str(row.name).replace('|', ' ').replace(',', ' ')

        if retStr == '':
            retStr = client_id + '|' + name
        else:
            retStr += ',' + client_id + '|' + name
            
    return retStr

def get_depot_user_list():
    retStr = ''
    cid = session.cid
    depotid = request.vars.depotid
    
    if session.user_type == 'Depot':
        rows = db((db.sm_depot_user.cid == cid) & (db.sm_depot_user.depot_id == session.depot_id)).select(db.sm_depot_user.user_id,orderby=db.sm_depot_user.user_id)
    else:
        if depotid=='' or depotid==None:        
            rows = db(db.sm_depot_user.cid == cid).select(db.sm_depot_user.user_id,orderby=db.sm_depot_user.user_id)
        else:
            rows = db((db.sm_depot_user.cid == cid) & (db.sm_depot_user.depot_id == depotid)).select(db.sm_depot_user.user_id,orderby=db.sm_depot_user.user_id)
            
    for row in rows:
        user_id = str(row.user_id)
        
        if retStr == '':
            retStr = user_id
        else:
            retStr += ',' + user_id

    return retStr

def get_depot_belt_list():
    retStr = ''
    cid = session.cid
    depot = request.vars.depotid
    
    rows=db((db.sm_depot_belt.cid==cid) & (db.sm_depot_belt.depot_id==depot)).select(db.sm_depot_belt.belt_name,orderby=db.sm_depot_belt.belt_name)
    for row in rows:
        belt_name = str(row.belt_name).strip()
        if retStr == '':
            retStr = belt_name
        else:
            retStr += ',' + belt_name    
    return retStr

def get_depot_store_list():
    retStr = ''
    cid = session.cid
    depot = request.vars.depotid
    
    rows=db((db.sm_depot_store.cid==cid) & (db.sm_depot_store.depot_id==depot)& (db.sm_depot_store.store_type=='SALES')).select(db.sm_depot_store.store_id,db.sm_depot_store.store_name,orderby=db.sm_depot_store.store_name)
    for row in rows:
        store_id = str(row.store_id).strip()
        store_name = str(row.store_name).strip().replace(',', ' ')
        
        if retStr == '':
            retStr = store_id+'|'+store_name
        else:
            retStr += ',' + store_id+'|'+store_name
    return retStr

def get_depot_store_all_list():
    retStr = ''
    cid = session.cid
    depot = request.vars.depotid
    
    rows=db((db.sm_depot_store.cid==cid) & (db.sm_depot_store.depot_id==depot)).select(db.sm_depot_store.store_id,db.sm_depot_store.store_name,orderby=db.sm_depot_store.store_name)
    for row in rows:
        store_id = str(row.store_id).strip()
        store_name = str(row.store_name).strip().replace(',', ' ')
        
        if retStr == '':
            retStr = store_id+'|'+store_name
        else:
            retStr += ',' + store_id+'|'+store_name
    return retStr

def get_depot_store_list_all():
    retStr = ''
    cid = session.cid
    depot = request.vars.depotid
    
    rows=db((db.sm_depot_store.cid==cid) & (db.sm_depot_store.depot_id==depot)).select(db.sm_depot_store.store_id,db.sm_depot_store.store_name,orderby=db.sm_depot_store.store_name)
    for row in rows:
        store_id = str(row.store_id).strip()
        store_name = str(row.store_name).strip().replace(',', ' ')
        
        if retStr == '':
            retStr = store_id+'|'+store_name
        else:
            retStr += ',' + store_id+'|'+store_name
    return retStr


def get_depot_market_list():
    retStr = ''
    cid = session.cid
    depot = request.vars.depotid
    
    rows=db((db.sm_depot_market.cid==cid) & (db.sm_depot_market.depot_id==depot)).select(db.sm_depot_market.market_id,db.sm_depot_market.market_name,orderby=db.sm_depot_market.market_name)
    for row in rows:
        market_id = str(row.market_id).strip()
        market_name = str(row.market_name).strip().replace(',', ' ')
        
        if retStr == '':
            retStr = market_id+'|'+market_name
        else:
            retStr += ',' + market_id+'|'+market_name 
    return retStr

def get_all_client_list():
    retStr = ''
    cid = session.cid
    depot = str(request.vars.depot).split('|')[0].upper()
    
    if session.user_type=='Supervisor':
        rows = db((db.sm_client.cid == cid)&(db.sm_client.area_id.belongs(session.marketList))).select(db.sm_client.client_id, db.sm_client.name, orderby=db.sm_client.name)
    else:
        if session.user_type == 'Depot':
            rows = db((db.sm_client.cid == cid) & (db.sm_client.depot_id == session.depot_id)).select(db.sm_client.client_id, db.sm_client.name, orderby=db.sm_client.name)
        else:
            if depot=='' or depot==None:
                rows = db(db.sm_client.cid == cid).select(db.sm_client.client_id, db.sm_client.name, orderby=db.sm_client.name)
            else:
                rows = db((db.sm_client.cid == cid) & (db.sm_client.depot_id == depot)).select(db.sm_client.client_id, db.sm_client.name, orderby=db.sm_client.name)
                
    for row in rows:
        client_id = str(row.client_id)
        name = str(row.name).replace('|', ' ').replace(',', ' ')
        
        if retStr == '':
            retStr = client_id + '|' + name
        else:
            retStr += ',' + client_id + '|' + name
            
    return retStr

def get_task_type_list():
    retStr = ''
    cid = session.cid
    rows = db((db.sm_category_type.cid == cid) & (db.sm_category_type.type_name == 'TASK_TYPE')).select(db.sm_category_type.cat_type_id, orderby=db.sm_category_type.cat_type_id)
    for row in rows:
        cat_type_id = str(row.cat_type_id)
        
        if retStr == '':
            retStr = cat_type_id
        else:
            retStr += ',' + cat_type_id
            
    return retStr


def get_complain_from_list():
    retStr = ''
    cid = session.cid
    rows = db((db.sm_category_type.cid == cid) & (db.sm_category_type.type_name == 'COMPLAIN_FROM')).select(db.sm_category_type.cat_type_id, orderby=db.sm_category_type.cat_type_id)
    for row in rows:
        cat_type_id = str(row.cat_type_id)
        
        if retStr == '':
            retStr = cat_type_id
        else:
            retStr += ',' + cat_type_id
            
    return retStr


def get_complain_type_list():
    retStr = ''
    cid = session.cid
    rows = db((db.sm_category_type.cid == cid) & (db.sm_category_type.type_name == 'COMPLAIN_TYPE')).select(db.sm_category_type.cat_type_id, orderby=db.sm_category_type.cat_type_id)
    for row in rows:
        cat_type_id = str(row.cat_type_id)
        
        if retStr == '':
            retStr = cat_type_id
        else:
            retStr += ',' + cat_type_id
            
    return retStr

def get_district_list():
    retStr = ''
    cid = session.cid
    rows = db(db.district.cid==session.cid).select(db.district.district_id,db.district.name, orderby=db.district.name)
    for row in rows:
        district_id = str(row.district_id)
        name = str(row.name)
        if retStr == '':
            retStr = district_id+'|'+name
        else:
            retStr += ',' + district_id+'|'+name
            
    return retStr


#for analysis
def get_region_area_list():
    
    retStr = ''
    cid = session.cid
    regionCode = str(request.vars.regionCode).strip()
    
    qset=db()
    qset=qset((db.sm_level.cid == cid)&(db.sm_level.depth == 1))
    
    if regionCode!='':
        qset=qset(db.sm_level.level0 == regionCode)
    
    rows = qset.select(db.sm_level.level_id, db.sm_level.level_name, orderby=db.sm_level.level_name)
    for row in rows:
        level_id = str(row.level_id)
        name = str(row.level_name).replace('|', ' ').replace(',', ' ')
        
        if retStr == '':
            retStr = level_id + '|' + name
        else:
            retStr += ',' + level_id + '|' + name
            
    return retStr

#for analysis
def get_region_area_territory_list():
    
    retStr = ''
    cid = session.cid
    regionCode = str(request.vars.regionCode).strip()
    areaCode = str(request.vars.areaCode).strip()
    
    qset=db()
    qset=qset((db.sm_level.cid == cid)&(db.sm_level.depth == 2))
    
    if regionCode!='':
        qset=qset(db.sm_level.level0 == regionCode)
    
    if areaCode!='':
        qset=qset(db.sm_level.level1 == areaCode)
        
    rows = qset.select(db.sm_level.level_id, db.sm_level.level_name, orderby=db.sm_level.level_name)
    
    for row in rows:
        level_id = str(row.level_id)
        name = str(row.level_name).replace('|', ' ').replace(',', ' ')
        
        if retStr == '':
            retStr = level_id + '|' + name
        else:
            retStr += ',' + level_id + '|' + name
            
    return retStr

#for analysis
def get_reg_area_terr_market_list():    
    retStr = ''
    cid = session.cid
    regionCode = str(request.vars.regionCode).strip()
    areaCode = str(request.vars.areaCode).strip()
    territoryCode = str(request.vars.territoryCode).strip()
    
    qset=db()
    qset=qset((db.sm_level.cid == cid)&(db.sm_level.depth == 3))
    
    if regionCode!='':
        qset=qset(db.sm_level.level0 == regionCode)
    
    if areaCode!='':
        qset=qset(db.sm_level.level1 == areaCode)
    
    if territoryCode!='':
        qset=qset(db.sm_level.level2 == territoryCode)
    
    rows = qset.select(db.sm_level.level_id, db.sm_level.level_name, orderby=db.sm_level.level_name)
    
    for row in rows:
        level_id = str(row.level_id)
        name = str(row.level_name).replace('|', ' ').replace(',', ' ')
        
        if retStr == '':
            retStr = level_id + '|' + name
        else:
            retStr += ',' + level_id + '|' + name
            
    return retStr


#============= Doctor List
def get_doctor_list():
    retStr = ''
    cid = session.cid
    
    rows = db(db.sm_doctor.cid == cid).select(db.sm_doctor.doc_id, db.sm_doctor.doc_name, db.sm_doctor.mobile, orderby=db.sm_doctor.doc_name)
     
    for row in rows:
        doc_id = str(row.doc_id)
        name = str(row.doc_name).replace('|', ' ').replace(',', ' ')
        mobile_no = str(row.mobile)

        if retStr == '':
            retStr = doc_id + '|' + name + '|' + mobile_no
        else:
            retStr += ',' + doc_id + '|' + name + '|' + mobile_no

    return retStr
#============= Doctor specialty
def get_doctor_specialty():
    retStr = ''
    cid = session.cid
    
    rows = db(db.sm_doctor.cid == cid).select(db.sm_doctor.specialty, orderby=db.sm_doctor.specialty, groupby=db.sm_doctor.specialty)
     
    for row in rows:
        specialty = str(row.specialty)
        
        if retStr == '':
            retStr = specialty
        else:
            retStr += ',' + specialty

    return retStr


#============= Device user list
def get_device_user_list():
    retStr = ''
    cid = session.cid
    
    rows = db(db.sm_login_device.cid == cid).select(db.sm_login_device.user_id, orderby=db.sm_login_device.user_id, groupby=db.sm_login_device.user_id)
    for row in rows:
        user_id = str(row.user_id)        
        if retStr == '':
            retStr = user_id
        else:
            retStr += ',' + user_id
    return retStr


def get_tl_list():
    retStr = ''
    cid = session.cid
    
    #---- supervisor
    if session.user_type=='Supervisor':
        level_id=session.level_id
        depthNo=session.depthNo
        level = 'level' + str(depthNo)
        
        rows = db((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '1') & (db.sm_level[level] == level_id)).select(db.sm_level.level_id, db.sm_level.level_name, orderby=db.sm_level.level_name)
        
    else:
        rows = db((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '1') ).select(db.sm_level.level_id, db.sm_level.level_name, orderby=db.sm_level.level_name)
    
    for row in rows:
        level_id = str(row.level_id)
        name = str(row.level_name).replace('|', ' ').replace(',', ' ')
        
        if retStr == '':
            retStr = level_id + '|' + name
        else:
            retStr += ',' + level_id + '|' + name
            
    return retStr


# =================================
def get_fm_list():
    retStr = ''
    cid = session.cid
    
    #---- supervisor

    rows = db((db.sm_level.cid == cid) & (db.sm_level.depth == '2') ).select(db.sm_level.level_id, db.sm_level.level_name, orderby=db.sm_level.level_name)
    
    for row in rows:
        level_id = str(row.level_id)
        name = str(row.level_name).replace('|', ' ').replace(',', ' ')
        
        if retStr == '':
            retStr = level_id + '|' + name
        else:
            retStr += ',' + level_id + '|' + name
    return retStr
def get_rsm_list():
    retStr = ''
    cid = session.cid
    
    #---- supervisor

    rows = db((db.sm_level.cid == cid) & (db.sm_level.depth == '1') ).select(db.sm_level.level_id, db.sm_level.level_name, orderby=db.sm_level.level_name)
    
    for row in rows:
        level_id = str(row.level_id)
        name = str(row.level_name).replace('|', ' ').replace(',', ' ')
        
        if retStr == '':
            retStr = level_id + '|' + name
        else:
            retStr += ',' + level_id + '|' + name
    return retStr

def get_doc_list():
    retStr = ''
    cid = session.cid
    
    #---- supervisor

    rows = db((db.sm_doctor.cid == cid) & (db.sm_doctor.status == 'ACTIVE') ).select(db.sm_doctor.doc_id, db.sm_doctor.doc_name, orderby=db.sm_doctor.doc_name)
    
    for row in rows:
        doc_id = str(row.doc_id)
        name = str(row.doc_name).replace('|', ' ').replace(',', ' ')
        
        if retStr == '':
            retStr = doc_id + '|' + name
        else:
            retStr += ',' + doc_id + '|' + name
    return retStr
# ===================================
def get_clientCat_list():
    retStr = ''
    cid = session.cid
    
    #---- supervisor
    
    
    rows =db((db.sm_category_type.cid == cid)&(db.sm_category_type.type_name=='CLIENT_CATEGORY')).select(db.sm_category_type.cat_type_id, db.sm_category_type.cat_type_name    , orderby=db.sm_category_type.cat_type_id)
    
    for row in rows:
        cat_type_id = str(row.cat_type_id)
        name = str(row.cat_type_name).replace('|', ' ').replace(',', ' ')
        
        if retStr == '':
            retStr = cat_type_id + '|' + name
        else:
            retStr += ',' + cat_type_id + '|' + name
            
    return retStr
def get_clientCatSub_list():
    retStr = ''
    cid = session.cid
    #---- supervisor
    rows =db((db.sm_category_type.cid == cid)&(db.sm_category_type.type_name=='CLIENT_SUB_CATEGORY')).select(db.sm_category_type.cat_type_id, db.sm_category_type.cat_type_name    , orderby=db.sm_category_type.cat_type_id)
    for row in rows:
        cat_type_id = str(row.cat_type_id)
        name = str(row.cat_type_name).replace('|', ' ').replace(',', ' ')
        if retStr == '':
            retStr = cat_type_id + '|' + name
        else:
            retStr += ',' + cat_type_id + '|' + name
            
    return retStr

#============= Device name list
def get_device_name_list():
    retStr = ''
    cid = session.cid
    
    rows = db(db.sm_login_device.cid == cid).select(db.sm_login_device.device_name, orderby=db.sm_login_device.device_name, groupby=db.sm_login_device.device_name)
    for row in rows:
        device_name = str(row.device_name)        
        if retStr == '':
            retStr = device_name
        else:
            retStr += ',' + device_name
    return retStr
    
def test():
    return str(date_fixed.strftime('%A'))
    #return str(random.sample(string.letters+string.digits,8)).replace("['","").replace("']","").replace("', '","")
    
#http://127.0.0.1:8000/mrepbiopharma/default/tempdoctorvisitfdate
#http://e2.businesssolutionapps.com/mrepbiopharma/default/tempdoctorvisitfdate
def tempdoctorvisitfdate():    
    rows=db().select(db.sm_doctor_visit.id, db.sm_doctor_visit.visit_date, orderby=db.sm_doctor_visit.visit_date)
    for row in rows:
        visit_date=row.visit_date        
        row.update_record(visit_firstdate=str(visit_date)[0:7]+'-01')
    
    return 'success'
    
    
    


