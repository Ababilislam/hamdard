#device
#password
#============================= 
import urllib2, random, string

import datetime
import time

#====================== Mobile Get Password
# http://127.0.0.1:8000/mrepconfidence/utility/getPassword?cid=CONFIDENCE&mobile=8801713334107&msg=PASSWORD&httppass=Compaq510DuoDuo
def getPassword():
    returnStr = ''
    
    cid = str(request.vars.cid).strip().upper()
    mobileNo = request.vars.mobile
    keyword = str(request.vars.msg).strip().upper()
    httppass = str(request.vars.httppass).strip()
    
    if httppass != 'Compaq510DuoDuo':
        returnStr = 'Invalid request'
    else:
        if keyword != 'PASSWORD':
            returnStr = 'Invalid Keyword'
        else:
            repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.mobile_no == mobileNo) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.id, db.sm_rep.rep_id,db.sm_rep.user_type, limitby=(0, 1))
#            return db._lastsql
            if not repRow:
                returnStr = 'Invalid User'
            else:
                user_type=repRow[0].user_type
                fieldForceId = repRow[0].rep_id                
                randNumber = randint(1001, 9999)
                
                if user_type=='sup':
                    repRow[0].update_record(password=randNumber, syncCode='')
                else:
                    repRow[0].update_record(password=randNumber, syncCode='', field2=0)
                
                returnStr = 'User ID: ' + str(fieldForceId) + ', Password: ' + str(randNumber)  + '  Download Link:  http://im-gp.com/d/pharma-30/ '
    
    return returnStr


#Used for device registration
def device():
    #----------
    response.title='Device Registration'
    
    #----------
    btn_device_settings=request.vars.btn_device_settings
    if btn_device_settings:
        c_id=str(request.vars.c_id.strip()).upper()
        user_id=str(request.vars.user_id.strip()).upper()
        password=request.vars.password.strip() 
        device_name=str(request.vars.device_name).strip() 
#        ipAddress='192.168.68.1'
        ipAddress=request.client
        if (ipAddress=='' or ipAddress==None):
            ipAddress='192.168.68.1'
        
        mac_hdd=request.vars.uploadkey.strip()
        
        #Split mac and hdd
        ip_mac_flag=True
        if mac_hdd!='':
            try:
                sepStr='HDSN'
                countSep=mac_hdd.count(sepStr)                
                mhList=mac_hdd.split(sepStr,countSep)
                macAddress=mhList[0]
                hddAddress=mhList[1]
                if (macAddress=='' and hddAddress==''):
                    ip_mac_flag=False                
            except:
                ip_mac_flag=False
        else:
            ip_mac_flag=False
            
        if ip_mac_flag:
            if ((c_id != '') and (user_id != '')and (password != '')and (device_name != '')):
                #---------------------------------------
                userText=str(c_id).strip()+'<url>'+str(user_id).strip()+'<url>'+str(password).strip()+'<url>'+str(device_name)+'<url>'+str(ipAddress).strip()+'<url>'+str(macAddress).strip()+'<url>'+str(hddAddress).strip()
                #Submit to cpanel
                request_text=urllib2.quote(userText)
                
                #url = 'http://www.businesssolutionapps.appspot.com/cpanel/default/device_registration?device_data='+request_text
                #url = 'http://127.0.0.1:8000/cpanel/default/device_registration?device_data='+request_text
                url = 'http://e.businesssolutionapps.com/cpanel/default/device_registration?device_data='+request_text
                
#                result= urllib2.urlopen(url)
#                result= result.read()
                result=fetch(url)

                if (str(result).find('START')==(-1) or str(result).find('END')==(-1)):
                    session.flash='Communication error'
                    redirect(URL('device'))
                else:
                    encResult=str(result)[5:-3]
                    
                if encResult!='':        
                    separator='<fd>'    
                    sepCount=encResult.count(separator)
                    
                    urlList=encResult.split(separator,sepCount)

                    if len(urlList)==2:
                        msgFlag=urlList[0]
                        msg=urlList[1]
                                                
                        response.flash=msg
                                   
                    else:
                        response.flash='Process error!'
                else:
                    response.flash='process error!'
            else:
                response.flash = 'All fields must be required !'
        else:
            response.flash = 'IP/MAC/HDD not found !'

    return dict(message=T('Device Registration'))
    
    #---------------------
def password(): #Used to change password
    #----------
    response.title='Change Password'
    #----------
    
    btn_change_password=request.vars.btn_change_password
    
    if btn_change_password:
        c_id=str(request.vars.c_id.strip()).upper()
        user_id=str(request.vars.user_id.strip()).upper()
        old_password=str(request.vars.old_pass).strip()
        new_password=str(request.vars.new_pass).strip()
        confirm_password=str(request.vars.confirm_pass).strip()
        
        if not(c_id==''or user_id==''or old_password==''or new_password==''or confirm_password==''):
            if new_password==confirm_password:
                #Create string for cpanel password_change function
                #Submit to cpanel
                userText=str(c_id).strip()+'<url>'+str(user_id).strip()+'<url>'+str(old_password).strip()+'<url>'+str(new_password)
                
                request_text=urllib2.quote(userText)
                #url = 'http://www.businesssolutionapps.appspot.com/cpanel/default/password_change?password_data='+request_text
                #url = 'http://127.0.0.1:8000/cpanel/default/password_change?password_data='+request_text
                url = 'http://e.businesssolutionapps.com/cpanel/default/password_change?password_data='+request_text
                
#                result= urllib2.urlopen(url)
#                result= result.read()
                result= fetch(url)
                
                if (str(result).find('START')==(-1) or str(result).find('END')==(-1)):
                    session.flash='Communication error'
                    redirect(URL('password'))
                else:
                    encResult=str(result)[5:-3]
                
                if encResult!='':        
                    separator='<fd>'    
                    sepCount=encResult.count(separator)
                      
                    urlList=encResult.split(separator,sepCount)
                    
                    if len(urlList)==2:
                        msgFlag=urlList[0]
                        msg=urlList[1]
                        
                        response.flash=msg
                        
                    else:
                        response.flash='Process error!'
                else:
                    response.flash='process error!'
            else:
                response.flash='New password and Confirm password should be same!'
        else:
            response.flash = 'All fields must be required !'

    return dict(message=T('Device Registration'))
    
    #---------------------


def device_reg():
    #----------
    response.title='Device Registration'
    
    retResult=''
    randomCode=str(random.sample(string.letters+string.digits,8)).replace("['","").replace("']","").replace("', '","")
        
    #----------
    btn_device_settings=request.vars.btn_device_settings
    if btn_device_settings:
        c_id=str(request.vars.cid.strip()).upper()
        user_id=str(request.vars.user_id.strip()).upper()
        password=request.vars.password.strip() 
        device_name=str(request.vars.device_name).strip()
        user_agent=str(request.vars.userAgentKey).strip()
        request_ip=request.client
        
        if (request_ip=='' or request_ip==None):
            request_ip='127.0.0.1'
        
        #Check
        if (c_id == '' or user_id == '' or password == '' or device_name == ''):
            retResult = 'FAILD'
            response.flash='CID,User ID,Password and Device Name Required'
        else:
            if (user_agent == ''):
                retResult = 'FAILD'
                response.flash='User Agent Not Found'
            else:
                if (request_ip == ''):
                    retResult = 'FAILD'
                    response.flash='User IP Not Found'
                else:
                    maxDevice=0
                    sysRows = db((db.sm_settings.cid == c_id)&(db.sm_settings.s_key == 'DEVICE_MAX')).select(db.sm_settings.s_value,limitby=(0,1))
                    if sysRows:
                        try:
                            maxDevice=int(sysRows[0].s_value)
                        except:
                            maxDevice=0
                        
                    #-----------
                    supervisorRows=db((db.sm_rep.cid==c_id) & (db.sm_rep.rep_id==user_id)  & (db.sm_rep.password==password)  & (db.sm_rep.user_type=='sup') & (db.sm_rep.status=='ACTIVE')).select(db.sm_rep.rep_id,limitby=(0,1))
                    if supervisorRows:
                        
                        deviceRows=db((db.sm_login_device.cid==c_id) & (db.sm_login_device.user_id==user_id) & (db.sm_login_device.device_name==device_name)).select(db.sm_login_device.user_id,limitby=(0,1))
                        if deviceRows:
                            retResult = 'FAILD'
                            response.flash='Device Registration request already submitted. To activated or reset the existing request, please communicate with administrator.'
                        else:
                            deviceCount=db(db.sm_login_device.cid==c_id).count()
                            if deviceCount>=maxDevice:
                                retResult = 'FAILD'
                                response.flash='Device registration not available. Maximum device allowed '+str(maxDevice)
                            else:
                                session.loginSyncCode=randomCode                            
                                db.sm_login_device.insert(cid=c_id,user_id=user_id,device_name=device_name,user_agent=user_agent,sync_code=randomCode,request_ip=request_ip)
                                
                                retResult = 'SUCCESS'
                                response.flash='Submitted Successfully'
                                
                    else:
                        #---------------------------------------
                        userText=str(c_id).strip()+'<url>'+str(user_id).strip()+'<url>'+str(password).strip()
                        request_text=urllib2.quote(userText)
                        
                        #url = 'http://www.businesssolutionapps.appspot.com/cpanel/get_user/check_valid_user?device_data='+request_text
                        #url = 'http://127.0.0.1:8000/cpanel/get_user/check_valid_user?device_data='+request_text
                        url = 'http://e.businesssolutionapps.com/cpanel/get_user/check_valid_user?device_data='+request_text
                        
                        result=fetch(url)
                        
                        if (str(result).find('START')==(-1) or str(result).find('END')==(-1)):
                            retResult = 'FAILD'
                            response.flash='Communication error'
                        else:
                            encResult=str(result)[5:-3]
                            
                        if encResult=='':
                            retResult = 'FAILD'
                            response.flash='process error'
                        else:
                            separator='<fd>'
                            sepCount=encResult.count(separator)
                            
                            urlList=encResult.split(separator,sepCount)
                            
                            if len(urlList)!=2:
                                retResult = 'FAILD'
                                esponse.flash='process error'
                            else:
                                msgFlag=urlList[0]
                                msg=urlList[1]
                                                                
                                if msgFlag!='SUCCESS':
                                    retResult = 'FAILD';
                                    response.flash=msg;
                                
                                else:                                    
                                    deviceRows=db((db.sm_login_device.cid==c_id) & (db.sm_login_device.user_id==user_id) & (db.sm_login_device.device_name==device_name)).select(db.sm_login_device.user_id,limitby=(0,1))
                                    if deviceRows:
                                        retResult = 'FAILD'
                                        response.flash='Device Registration request already submitted. To activated or reset the existing request, please communicate with administrator.'
                                    else:
                                        deviceCount=db(db.sm_login_device.cid==c_id).count()
                                        if deviceCount>=maxDevice:
                                            retResult = 'FAILD'
                                            response.flash='Device registration not available. Maximum device allowed '+str(maxDevice)
                                        else:                                  
                                            session.loginSyncCode=randomCode                                        
                                            db.sm_login_device.insert(cid=c_id,user_id=user_id,device_name=device_name,user_agent=user_agent,sync_code=randomCode,request_ip=request_ip)
                                            
                                            retResult = 'SUCCESS'
                                            response.flash='Submitted Successfully'
    
    return dict(retResult=retResult)



def device_list():
    task_id='rm_device_manage'
    task_id_view='rm_device_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))
    
    #   ---------------------
    response.title='Device List'
    
    c_id=session.cid
    
    #  ---------------filter-------    
    btn_filter_device=request.vars.btn_filter_device
    btn_all=request.vars.btn_all
    reqPage=len(request.args)
    
    if btn_filter_device:
        session.search_type_device=request.vars.search_type
        session.search_value_device=str(request.vars.search_value).strip().upper()
        reqPage=0
    elif btn_all:
        session.search_type_device=None
        session.search_value_device=None
        reqPage=0
    
    #--------paging
    if reqPage:
        page=int(request.args[0])
    else:
        page=0
    items_per_page=session.items_per_page
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #--------end paging   
    
    qset=db()
    qset=qset(db.sm_login_device.cid==c_id)
    
    if (session.search_type_device=='UserID'):
        searchValue=str(session.search_value_device)
        qset=qset(db.sm_login_device.user_id==searchValue)
        
    elif (session.search_type_device=='DeviceName'):
        qset=qset(db.sm_login_device.device_name==session.search_value_device)
    
    elif (session.search_type_device=='Status'):
        qset=qset(db.sm_login_device.status==session.search_value_device)
        
    records=qset.select(db.sm_login_device.ALL ,orderby=~db.sm_login_device.id,limitby=limitby)
    recordsCount=qset.count()
    
    return dict(records=records,recordsCount=recordsCount,page=page,items_per_page=items_per_page,access_permission=access_permission)
    

#-----------------depot edit-----------
def device_edit():
    task_id='rm_device_manage'
    access_permission=check_role(task_id)
    if (access_permission==False):
        session.flash='Access is Denied !'
        redirect (URL('device_list'))
    
    response.title='Device Edit'
    
    #   --------------------- 
    c_id=session.cid
    
    page=request.args(0)
    record= db.sm_login_device(request.args(1)) or redirect(URL('device_list'))   
    
    form =SQLFORM(db.sm_login_device,
                  record=record,
                  deletable=True,
                  fields=['status'],
                  submit_button='Update'
                  )
    
    if form.accepts(request.vars, session):
        response.flash = 'Updated Successfully'        
        redirect(URL('device_list',args=[page]))
    
    #    Get all data for selected depot
    records=db((db.sm_login_device.cid==c_id) & (db.sm_login_device.id==request.args(1))).select(db.sm_login_device.ALL,limitby=(0,1))
    
#    if depot used then delete option will be hide based on used flag
    useFlag=False
    
    #-----------------
    return dict(form=form,records=records,page=page,access_permission=access_permission,useFlag=useFlag)

def user_log():
    task_id_view='rm_user_log_view'
    access_permission_view=check_role(task_id_view)
    if (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))
        
    #   ---------------------
    response.title='User Log'
    
    c_id=session.cid
    
    #  ---------------filter-------    
    btn_filter_userlog=request.vars.btn_filter
    btn_all=request.vars.btn_all
    reqPage=len(request.args)
    
    if btn_filter_userlog:
        session.search_type_userlog=request.vars.search_type
        session.search_value_userlog=str(request.vars.search_value).strip().upper()
        reqPage=0
    elif btn_all:
        session.search_type_userlog=None
        session.search_value_userlog=None
        reqPage=0
    
    #--------paging
    if reqPage:
        page=int(request.args[0])
    else:
        page=0
    items_per_page=session.items_per_page
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #--------end paging   
    
    qset=db()
    qset=qset(db.sm_login_log.cid==c_id)
    
    if (session.search_type_userlog=='UserID'):
        searchValue=str(session.search_value_userlog)
        qset=qset(db.sm_login_log.user_id==searchValue)
        
    elif (session.search_type_userlog=='DeviceName'):
        qset=qset(db.sm_login_log.device_name==session.search_value_userlog)
    
    records=qset.select(db.sm_login_log.ALL ,orderby=~db.sm_login_log.id,limitby=limitby)
        
    return dict(records=records,page=page,items_per_page=items_per_page,access_permission_view=access_permission_view)
    

#Not used
def settings_home():
    if (session.cid=='' or session.cid==None):        
        session.flash='Access is Denied !'
        redirect (URL('default','home'))
    
    response.title='Settings Home'
    #-----------------
    
    #----------
    btn_trade_promotion=request.vars.btn_trade_promotion
    btn_restricted_item=request.vars.btn_restricted_item
    btn_depot_opening=request.vars.btn_depot_opening 
    btn_client_opening=request.vars.btn_client_opening
        
    #---------------------
    if btn_trade_promotion:
        redirect(URL(c='invoice_rules',f='invoice_rules_add'))                
    elif btn_restricted_item:
        redirect(URL(c='restricted_stock_item',f='restricted_stock_item_add'))
    elif btn_depot_opening:
        redirect(URL(c='utility',f='depot_opening_balance'))    
    elif btn_client_opening:
        redirect(URL(c='utility',f='client_opening_balance'))    
    else:
        return dict()
    #--------------


def opening_balance_validation(form):
    c_id=session.cid
    amount=0
    
    tx_account='DPT-'+str(request.vars.tx_account).strip()
    opposite_account='DPT-'+str(request.vars.opposite_account).strip()
    
    amountType=request.vars.depot2DrCr
    
    if amountType=='':
        form.errors.tx_amount=''
        response.flash = 'Select Balance Type'
    else:
        pass

    
    amount=float(request.vars.tx_amount)
    
    if amount<=0:
        form.errors.tx_amount=''
        response.flash = 'need valid amount'
    else:
        amount=((amount*100)//1)/100
        
        if tx_account==opposite_account:
            form.errors.tx_account=''
            response.flash = 'Both Depot can not be same'
        else:
            records=db((db.sm_transaction.cid==session.cid) & (db.sm_transaction.tx_type=='OPENING')& (db.sm_transaction.tx_account==tx_account)& (db.sm_transaction.opposite_account==opposite_account)).select(db.sm_transaction.tx_account,limitby=(0,1))
            if records:
                form.errors.tx_amount=''
                response.flash = 'opening already exist'
            else:
                txRecords=db((db.sm_transaction.cid==session.cid) & (db.sm_transaction.tx_account==tx_account)& (db.sm_transaction.opposite_account==opposite_account)).select(db.sm_transaction.tx_account,limitby=(0,1))
                if txRecords:
                    form.errors.tx_amount=''
                    response.flash = 'Transaction already done, opening settings not allowed for these depots'
                else:
                    #-----------------         
                    form.vars.cid=session.cid
                    form.vars.txid='OPENING'+'-'+str(tx_account)
                    form.vars.tx_date=date_fixed                   #from_dt_filter
                    form.vars.tx_type='OPENING'
                    form.vars.sales_type='P'
                    form.vars.tx_account=tx_account
                    form.vars.opposite_account=opposite_account
                    
                    if amountType=='Cr':
                        form.vars.tx_amount=amount*(-1)
                        form.vars.tx_closing_balance=amount*(-1)
                        form.vars.tx_des=str(tx_account)+' will get from '+str(opposite_account)
                    else:
                        form.vars.tx_amount=amount
                        form.vars.tx_closing_balance=amount
                        form.vars.tx_des=str(tx_account)+' will pay to '+str(opposite_account)

def depot_opening_balance():
    #Check access permission
    task_id='rm_depot_payment_manage'
    task_id_view='rm_depot_payment_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL(c='default',f='home'))
        
    response.title=' Opening Balance Set'
      
    
    # ---------------------
    c_id=session.cid
    
    depotList=[]
    records=db((db.sm_depot.cid==c_id)&(db.sm_depot.status=='ACTIVE')).select(db.sm_depot.depot_id ,orderby=db.sm_depot.depot_id)
    for row in records:
        depot_id=row.depot_id
        depotList.append(depot_id)
    
    toDepot=''
    fromList=[]
    toList=[]
    
    depotRows=''
    if (session.user_type=='Depot'):
        toDepot=session.depot_id
        depotRows=db((db.sm_depot_settings.cid==c_id)&(db.sm_depot_settings.from_to_type=='Receive')&(db.sm_depot_settings.depot_id_from_to==toDepot)).select(db.sm_depot_settings.depot_id,db.sm_depot_settings.depot_id_from_to,orderby=db.sm_depot_settings.depot_id|db.sm_depot_settings.depot_id_from_to)
    else:
        depotRows=db((db.sm_depot_settings.cid==c_id)&(db.sm_depot_settings.from_to_type=='Receive')).select(db.sm_depot_settings.depot_id,db.sm_depot_settings.depot_id_from_to,orderby=db.sm_depot_settings.depot_id|db.sm_depot_settings.depot_id_from_to)
        
    for dRow in depotRows:
        depot_from=dRow.depot_id
        depot_to=dRow.depot_id_from_to
        
        if depot_from not in fromList:            
            if depot_from in depotList:
                fromList.append(depot_from)
        
        if depot_to not in toList: 
            if depot_to in depotList:
                toList.append(depot_to)
    
    fromDepotStr=''
    fromDptRows=db((db.sm_depot.cid==c_id) & (db.sm_depot.depot_id.belongs(fromList))).select(db.sm_depot.depot_id,db.sm_depot.name,orderby=db.sm_depot.name)
    for fromDpt in fromDptRows:
        fromDptId=str(fromDpt.depot_id)
        fromDptName=str(fromDpt.name).replace('-', ' ').replace(',', ' ')
        if fromDepotStr=='':
            fromDepotStr=fromDptId+'|'+fromDptName
        else:
            fromDepotStr+=','+fromDptId+'|'+fromDptName
        
        
    #----------- tx_account (cr) opposite_account (dr)
    if (session.user_type!='Depot'):
        db.sm_transaction.opposite_account.requires=IS_IN_SET(toList)
    
    db.sm_transaction.tx_account.requires=IS_IN_SET(fromList)
    form =SQLFORM(db.sm_transaction,
                  fields=['tx_account','opposite_account','tx_amount'],
                  submit_button='Post'       
                  )
    
    #-----------------    
    if form.accepts(request.vars,session,onvalidation=opening_balance_validation):
        cid=session.cid        
        tx_type='OPENING'
        sales_type='P'
        tx_date=form.vars.tx_date      
        tx_account=form.vars.tx_account
        opposite_account=form.vars.opposite_account
        txAmount=form.vars.tx_amount
        
        txAmount=float(txAmount)*(-1)
        
        txid='OPENING'+'-'+str(opposite_account)        
        
        if txAmount<0:#depot,client
            tx_des=str(opposite_account)+' will get from '+str(tx_account)
            
        else:
            tx_des=str(opposite_account)+' will pay to '+str(tx_account)
        
        insertRes=db.sm_transaction.insert(cid=cid,txid=txid,tx_type=tx_type,sales_type=sales_type,tx_date=tx_date,tx_account=opposite_account,opposite_account=tx_account,tx_amount=txAmount,tx_closing_balance=txAmount,tx_des=tx_des)
                
        if insertRes:
            response.flash = 'Posted successfully'
        else:
            db.rollback()
            response.flash = 'Posted failed'
    
    #------------------------------------------------
    search_form =SQLFORM(db.sm_search_date)
    
    # --------------------------- filter--------
    btn_filter_dop=request.vars.btn_filter
    btn_filter_all=request.vars.btn_filter_all
    reqPage=len(request.args)
    if btn_filter_dop:
        session.btn_filter_dop=btn_filter_dop
        
        tx_account_value_dop=request.vars.tx_account_value        
        session.tx_account_value_dop=str(tx_account_value_dop).upper()
        
        reqPage==0
        
    elif btn_filter_all:
        session.btn_filter_dop=None
        session.tx_account_value_dop=None
        
        reqPage=0
        
    #--------paging
    if reqPage:
        page=int(reqPage)
    else:
        page=0
    items_per_page=session.items_per_page
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #--------end paging    
    
    qset=db()
    qset=qset(db.sm_transaction.cid==c_id)
    qset=qset(db.sm_transaction.tx_type=='OPENING')
    qset=qset(db.sm_transaction.sales_type=='P')
    
    if (session.user_type=='Depot'):
        qset=qset(db.sm_transaction.tx_account=='DPT-'+str(session.depot_id))
        
    if (session.btn_filter_dop):
        searchValue=str(session.tx_account_value_dop).split('|')[0]
        
        if (session.user_type=='Depot'):
            qset=qset(db.sm_transaction.opposite_account=='DPT-'+searchValue)
        else:
            qset=qset(db.sm_transaction.tx_account=='DPT-'+searchValue)
    
    records=qset.select(db.sm_transaction.ALL,orderby=~db.sm_transaction.id,limitby=limitby)
    
    return dict(form=form,search_form=search_form,fromDepotStr=fromDepotStr,fromList=fromList,toDepot=toDepot,records=records,page=page,items_per_page=items_per_page,access_permission=access_permission,access_permission_view=access_permission_view)

def preview_depot_opening():
    #----------Task assaign----------
    task_id='rm_depot_payment_manage'
    task_id_view='rm_depot_payment_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL(c='default',f='home'))
    
    #------------------------
    c_id=session.cid
    tx_account=request.vars.tx_account
    opposite_account=request.vars.opposite_account

    #--------------- Title
    response.title='Preview Depot Opening'
    
    records=db((db.sm_transaction.cid==session.cid) & (db.sm_transaction.tx_type=='OPENING')& (db.sm_transaction.sales_type=='P')& (db.sm_transaction.tx_account==tx_account)& (db.sm_transaction.opposite_account==opposite_account)).select(db.sm_transaction.ALL,orderby=~db.sm_transaction.tx_date,limitby=(0,1))
    
    txid=0
    tx_date=''
    tx_type=''
    reference=''
    tx_account=''
    opposite_account=''
    tx_amount=0
    tx_des=''
    sales_type=''    
    for row in records:
        txid=row.txid
        tx_date=row.tx_date
        tx_type=row.tx_type
        reference=row.reference
        tx_account=row.tx_account
        opposite_account=row.opposite_account
        tx_amount=row.tx_amount
        tx_des=row.tx_des
        sales_type=row.sales_type      
        break
    
    #-----------  
    return dict(txid=txid,tx_date=tx_date,tx_type=tx_type,reference=reference,tx_account=tx_account,opposite_account=opposite_account,tx_amount=tx_amount,tx_des=tx_des,sales_type=sales_type)

def download_depot_opening():
    task_id='rm_depot_payment_manage'
    task_id_view='rm_depot_payment_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL(c='default',f='home'))
    
    c_id=session.cid
    
    records=''
    qset=db()
    qset=qset(db.sm_transaction.cid==c_id)
    qset=qset(db.sm_transaction.tx_type=='OPENING')
    qset=qset(db.sm_transaction.sales_type=='P')
    
    if (session.user_type=='Depot'):
        qset=qset(db.sm_transaction.tx_account=='DPT-'+str(session.depot_id))
        
    if (session.btn_filter_dop):
        searchValue=str(session.tx_account_value_dop).split('|')[0]
        qset=qset(db.sm_transaction.opposite_account=='DPT-'+searchValue)
        
    records=qset.select(db.sm_transaction.ALL,orderby=~db.sm_transaction.id)
    
    #---------
    myString='Depot Opening\n\n'
    myString+='ID,Depot,Balance Type,Depot,Amount,Dr/Cr,Date\n'
    
    for rec in records:
        txid=rec.txid
        tx_account=rec.tx_account
        tx_des=rec.tx_des
        opposite_account=rec.opposite_account
        tx_amount=rec.tx_amount
        
        tx_date=str(rec.tx_date)[0:10]
        amtType=''
        if float(tx_amount)<0:
            amtType='Cr'
        elif float(tx_amount)>0:
            amtType='Dr'
        
        myString+=str(txid)+','+str(tx_account)+','+str(tx_des)+','+str(opposite_account)+','+str(tx_amount)+','+str(amtType)+','+str(tx_date)+'\n'
        
    #-----------
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_depot_opening.csv'   
    return str(myString)


def client_opening_balance_validation(form):
    c_id=session.cid
    amount=0
    
    tx_account='CLT-'+str(request.vars.tx_account).strip()
    opposite_account='DPT-'+str(request.vars.opposite_account).strip()
    amountType=request.vars.clientDrCr
    
    if amountType=='':
        form.errors.tx_amount=''
        response.flash = 'Select Client Payment/Received'
    else:
        pass
        
    amount=float(request.vars.tx_amount)
    
    if amount<=0:
        form.errors.tx_amount=''
        response.flash = 'need valid amount'
    else:
        amount=((amount*100)//1)/100
                
        if tx_account==opposite_account:
            form.errors.tx_account=''
            response.flash = 'Both Account can not be same'
        else:
            records=db((db.sm_transaction.cid==session.cid) & (db.sm_transaction.tx_type=='OPENING')& (db.sm_transaction.tx_account==tx_account)& (db.sm_transaction.opposite_account==opposite_account)).select(db.sm_transaction.tx_account,limitby=(0,1))
            if records:
                form.errors.tx_amount=''
                response.flash = 'opening already exist'
            else:
                txRecords=db((db.sm_transaction.cid==session.cid) & (db.sm_transaction.tx_account==tx_account)& (db.sm_transaction.opposite_account==opposite_account)).select(db.sm_transaction.tx_account,limitby=(0,1))
                if txRecords:
                    form.errors.tx_amount=''
                    response.flash = 'Transaction already done, opening settings not allowed for these depots'
                else:
                    #-----------------         
                    form.vars.cid=session.cid
                    form.vars.txid='OPENING'+'-'+str(tx_account)
                    form.vars.tx_date=date_fixed    #from_dt_filter
                    form.vars.tx_type='OPENING'
                    form.vars.sales_type='S'
                    form.vars.tx_account=tx_account
                    form.vars.opposite_account=opposite_account
                    
                    if amountType=='Cr':
                        form.vars.tx_amount=amount*(-1)
                        form.vars.tx_closing_balance=amount*(-1)
                        form.vars.tx_des=str(tx_account)+' will get from '+str(opposite_account)
                        
                    else:
                        form.vars.tx_amount=amount
                        form.vars.tx_closing_balance=amount
                        form.vars.tx_des=str(tx_account)+' will pay to '+str(opposite_account)

def client_opening_balance():
    #Check access permission
    task_id='rm_client_payment_manage'
    task_id_view='rm_client_payment_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL(c='default',f='home'))
    
    response.title='Opening Balance Set'
        
    
    # ---------------------
    c_id=session.cid
    
#    depotList=[]
#    records=db((db.sm_depot.cid==c_id)&(db.sm_depot.status=='ACTIVE')).select(db.sm_depot.depot_id ,orderby=db.sm_depot.depot_id)
#    for row in records:
#        depot_id=row.depot_id
#        depotList.append(depot_id)
    
    toDepot=''
    fromList=[]
    toList=[]
    
    depotRows=''
    if (session.user_type=='Depot'):
        toDepot=session.depot_id
    
    fromClientStr=''
    if (session.user_type=='Depot'):
        clientRows=db((db.sm_client.cid==c_id)& (db.sm_client.depot_id==toDepot)).select(db.sm_client.client_id,db.sm_client.name,orderby=db.sm_client.name)
    else:
        clientRows=db(db.sm_client.cid==c_id).select(db.sm_client.client_id,db.sm_client.name,orderby=db.sm_client.name)
        
        
    for cRow in clientRows:
        client_id=str(cRow.client_id)
        client_name=str(cRow.name).replace('-', ' ').replace(',', ' ')
        if client_id not in fromList:            
            fromList.append(client_id)
        
        #--------------------
        if fromClientStr=='':
            fromClientStr=client_id+'|'+client_name
        else:
            fromClientStr+=','+client_id+'|'+client_name
        
    
    #----------- tx_account (cr) opposite_account (dr)
    if (session.user_type!='Depot'):
        db.sm_transaction.opposite_account.requires=IS_IN_SET(toList)
    
    db.sm_transaction.tx_account.requires=IS_IN_SET(fromList)
    form =SQLFORM(db.sm_transaction,
                  fields=['tx_account','opposite_account','tx_amount'],
                  submit_button='Post'       
                  )

    #-----------------    
    if form.accepts(request.vars,session,onvalidation=client_opening_balance_validation):
        cid=session.cid
        tx_type='OPENING'
        sales_type='S'
        tx_date=form.vars.tx_date      
        tx_account=form.vars.tx_account
        opposite_account=form.vars.opposite_account
        txAmount=form.vars.tx_amount
        
        txAmount=float(txAmount)*(-1)
        
        
        txid='OPENING'+'-'+str(opposite_account)        
        
        if txAmount<0:#depot,client
            tx_des=str(opposite_account)+' will get from '+str(tx_account)
            
        else:
            tx_des=str(opposite_account)+' will pay to '+str(tx_account)
        
        insertRes=db.sm_transaction.insert(cid=cid,txid=txid,tx_type=tx_type,sales_type=sales_type,tx_date=tx_date,tx_account=opposite_account,opposite_account=tx_account,tx_amount=txAmount,tx_closing_balance=txAmount,tx_des=tx_des)
        
        if insertRes:
            response.flash = 'Posted successfully'
        else:
            db.rollback()
            response.flash = 'Posted failed'
    
    #------------------------------------------------
    search_form =SQLFORM(db.sm_search_date)
    
    #   --------------------------- filter
    btn_filter=request.vars.btn_filter
    btn_filter_all=request.vars.btn_filter_all
    reqPage=len(request.args)
    if btn_filter:
        session.btn_filter_cop=btn_filter
        
        tx_account_value_cop=request.vars.tx_account_value        
        session.tx_account_value_cop=str(tx_account_value_cop).upper()
        
        reqPage==0
        
    elif btn_filter_all:
        session.btn_filter_cop=None
        session.tx_account_value_cop=None
        
        reqPage=0
        
    #--------paging
    if reqPage:
        page=int(reqPage)
    else:
        page=0
    items_per_page=session.items_per_page
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #--------end paging    
    
    qset=db()
    qset=qset(db.sm_transaction.cid==c_id)
    qset=qset(db.sm_transaction.tx_type=='OPENING')
    qset=qset(db.sm_transaction.sales_type=='S')
    
    if (session.user_type=='Depot'):
        qset=qset(db.sm_transaction.tx_account=='DPT-'+str(session.depot_id))
        
    if (session.btn_filter_cop):
        searchValue=str(session.tx_account_value_cop).split('|')[0]
        
        if (session.user_type=='Depot'):
            qset=qset(db.sm_transaction.opposite_account=='CLT-'+searchValue)
        else:
            qset=qset(db.sm_transaction.tx_account=='CLT-'+searchValue)
            
    records=qset.select(db.sm_transaction.ALL,orderby=~db.sm_transaction.id,limitby=limitby)
    
    return dict(form=form,search_form=search_form,fromClientStr=fromClientStr,fromList=fromList,toDepot=toDepot,records=records,page=page,items_per_page=items_per_page,access_permission=access_permission,access_permission_view=access_permission_view)

def preview_client_opening():
    #----------Task assaign----------
    task_id='rm_client_payment_manage'
    task_id_view='rm_client_payment_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL(c='default',f='home'))
    
    #------------------------
    c_id=session.cid
    tx_account=request.vars.tx_account
    opposite_account=request.vars.opposite_account

    #--------------- Title
    response.title='Preview Client Opening'
    
    records=db((db.sm_transaction.cid==session.cid) & (db.sm_transaction.tx_type=='OPENING')& (db.sm_transaction.sales_type=='S')& (db.sm_transaction.tx_account==tx_account)& (db.sm_transaction.opposite_account==opposite_account)).select(db.sm_transaction.ALL,orderby=~db.sm_transaction.tx_date,limitby=(0,1))
    
    txid=0
    tx_date=''
    tx_type=''
    reference=''
    tx_account=''
    opposite_account=''
    tx_amount=0
    tx_des=''
    sales_type=''    
    for row in records:
        txid=row.txid
        tx_date=row.tx_date
        tx_type=row.tx_type
        reference=row.reference
        tx_account=row.tx_account
        opposite_account=row.opposite_account
        tx_amount=row.tx_amount
        tx_des=row.tx_des
        sales_type=row.sales_type      
        break
        
    #-----------  
    return dict(message=T('Show Client Opening'),txid=txid,tx_date=tx_date,tx_type=tx_type,reference=reference,tx_account=tx_account,
                opposite_account=opposite_account,tx_amount=tx_amount,tx_des=tx_des,sales_type=sales_type)


#============================= Client Batch Upload
def client_opening_batch_upload():
    response.title='Client Batch Upload'
    #Check access permission
    task_id='rm_client_payment_manage'
    access_permission=check_role(task_id)
    if (access_permission==False):
        session.flash='Access is Denied !'
        redirect (URL(c='default',f='home'))
    
    c_id=session.cid
    
    if (session.depot_id=='') and (session.depot_id==None):
        session.flash='Only Depot user can done'
        redirect (URL('utility','client_opening_balance'))
    
    
    btn_upload=request.vars.btn_upload    
    count_inserted=0
    count_error=0
    error_str=''
    total_row=0
    if btn_upload=='Upload':        
        excel_data=str(request.vars.excel_data)
        inserted_count=0
        error_count=0
        error_list=[]
        row_list=excel_data.split( '\n')
        total_row=len(row_list)
        
        client_list_excel=[]
        valid_client_list=[]
        
        client_list_account=[]
        
        excelList=[]
        
        opening_exist=[]
        any_exist_list=[]
        
        ins_list=[]
        ins_dict={}
        
        for i in range(total_row):
            if i>=30:
                break
            else:
                row_data=row_list[i]                    
                coloum_list=row_data.split( '\t')
                if len(coloum_list)==3:
                    client_list_excel.append(str(coloum_list[1]).strip().upper())
                    client_list_account.append('CLT-'+str(coloum_list[1]).strip().upper())
                    
        #        create client list
        existClientRows=db((db.sm_client.cid==c_id)&(db.sm_client.client_id.belongs(client_list_excel))).select(db.sm_client.client_id,db.sm_client.depot_id,orderby=db.sm_client.client_id)
        valid_client_list=existClientRows.as_list()
        
        existRows=db((db.sm_transaction.cid==c_id) & (db.sm_transaction.tx_type=='OPENING')& (db.sm_transaction.sales_type=='S')& (db.sm_transaction.tx_account=='DPT-'+str(session.depot_id))& (db.sm_transaction.opposite_account.belongs(client_list_account))).select(db.sm_transaction.opposite_account,orderby=~db.sm_transaction.tx_date)
        opening_exist=existRows.as_list()
        
        existAllRows=db((db.sm_transaction.cid==c_id) & (db.sm_transaction.tx_account=='DPT-'+str(session.depot_id))& (db.sm_transaction.opposite_account.belongs(client_list_account))& (db.sm_transaction.row_flag=='0')).select(db.sm_transaction.opposite_account)
        any_exist_list=existAllRows.as_list()

        #   --------------------     
        for i in range(total_row):
            if i>=30: 
                break
            else:
                row_data=row_list[i]
            coloum_list=row_data.split( '\t')            

            if len(coloum_list)==3:
                balanceType=str(coloum_list[0]).strip().upper()
                clientID=str(coloum_list[1]).strip().upper() # tx account
                amount=str(coloum_list[2]).strip()
                
                
                dataFlag=True
                if (balanceType=='' or clientID=='' or amount==''):
                    dataFlag=False
                else:
                    #---------------
                    if (balanceType=='PAY TO' or balanceType=='GET FROM'):
                        pass                        
                    else:
                        dataFlag=False
                    
                    #-------------
                    txAccount='CLT-'+clientID
                    oppAccount='DPT-'+str(session.depot_id)
                    
                    #---------
                    try:
                        amount=float(amount)
                        if (amount > 0):                        
                            crAmount=amount*(-1)
                            drAmount=amount
                        else:
                            dataFlag=False
                    except:
                        dataFlag=False
                    
                try:
                    
                    valid_client=False
                    duplicate_client=False
                    data_entry_flag=False
                    
                    if dataFlag==True:                        
                        #----------- check valid client                                                 
                        for i in range(len(valid_client_list)):
                            myRowData=valid_client_list[i]                                
                            client_id=myRowData['client_id']
                            depot_id=myRowData['depot_id']
                            if (depot_id==session.depot_id and str(client_id).strip()==str(clientID).strip()):
                                valid_client=True
                                break
                        
                        #---------- check valid level/depot  
                        if valid_client==True:
                            for i in range(len(opening_exist)):
                                myRowData=opening_exist[i]                             
                                opposite_account=myRowData['opposite_account']
                                if (str(opposite_account).strip()==str(txAccount).strip()):
                                    duplicate_client=True                                   
                                    break
                            
                            for i in range(len(any_exist_list)):
                                myRowData=any_exist_list[i]                             
                                opposite_account=myRowData['opposite_account']
                                if (str(opposite_account).strip()==str(txAccount).strip()):
                                    data_entry_flag=True                                   
                                    break                            
                            
                            
                            #-----------------
                            if(duplicate_client==False):                             
                                if(data_entry_flag==False):                                    
                                    if clientID not in excelList:
                                        excelList.append(clientID)
                                        
                                        if (balanceType=='PAY TO'):
                                            
                                            txFirstID='OPENING'+'-'+str(txAccount)
                                            txSecondID='OPENING'+'-'+str(oppAccount)                                        
                                            txDate=date_fixed
                                            txType='OPENING'
                                            secondarySalesType='S'
                                            typeRef=''
                                            txAccount=txAccount
                                            oppAccount=oppAccount
                        
                                            txDescription=str(txAccount)+' will get from '+str(oppAccount)
                                            oppDescription=str(oppAccount)+' will pay to '+str(txAccount)
                                            
                                            txDict={'cid':c_id,'txid':txFirstID,'tx_date':txDate,'tx_type':txType,'sales_type':secondarySalesType,'reference':typeRef,'tx_account':txAccount,'opposite_account':oppAccount,'tx_op_balance':0,'tx_amount':crAmount,'tx_closing_balance':crAmount,'tx_des':txDescription}
                                            oppDict={'cid':c_id,'txid':txSecondID,'tx_date':txDate,'tx_type':txType,'sales_type':secondarySalesType,'reference':typeRef,'tx_account':oppAccount,'opposite_account':txAccount,'tx_op_balance':0,'tx_amount':drAmount,'tx_closing_balance':drAmount,'tx_des':oppDescription}
                                            ins_list.append(txDict)
                                            ins_list.append(oppDict)
                                                                          
                                            count_inserted+=1
                                        
                                        
                                        elif (balanceType=='GET FROM'):
                                            txFirstID='OPENING'+'-'+str(txAccount)
                                            txSecondID='OPENING'+'-'+str(oppAccount)                                        
                                            txDate=date_fixed
                                            txType='OPENING'
                                            secondarySalesType='S'
                                            typeRef=''
                                            txAccount=txAccount
                                            oppAccount=oppAccount
                        
                                            txDescription=str(txAccount)+' will pay to '+str(oppAccount)
                                            oppDescription=str(oppAccount)+' will get from '+str(txAccount)
                                            
                                            txDict={'cid':c_id,'txid':txFirstID,'tx_date':txDate,'tx_type':txType,'sales_type':secondarySalesType,'reference':typeRef,'tx_account':txAccount,'opposite_account':oppAccount,'tx_op_balance':0,'tx_amount':drAmount,'tx_closing_balance':drAmount,'tx_des':txDescription}
                                            oppDict={'cid':c_id,'txid':txSecondID,'tx_date':txDate,'tx_type':txType,'sales_type':secondarySalesType,'reference':typeRef,'tx_account':oppAccount,'opposite_account':txAccount,'tx_op_balance':0,'tx_amount':crAmount,'tx_closing_balance':crAmount,'tx_des':oppDescription}
                                            ins_list.append(txDict)
                                            ins_list.append(oppDict)
                                                                          
                                            count_inserted+=1
                                        
                                        
                                        else:
                                            error_data=row_data+'(invalid balance type)\n'
                                            error_str=error_str+error_data
                                            count_error+=1
                                            continue
                                        
                                    else:
                                        error_data=row_data+'(duplicate in excel!)\n'
                                        error_str=error_str+error_data
                                        count_error+=1
                                        continue
                                else:
                                    error_data=row_data+'(opening not allowed, data already submitted)\n'
                                    error_str=error_str+error_data
                                    count_error+=1
                                    continue
                            
                            else:
                                error_data=row_data+'(opening already exist)\n'
                                error_str=error_str+error_data
                                count_error+=1
                                continue                            
                        else:
                                error_data=row_data+'(invalid client)\n'
                                error_str=error_str+error_data
                                count_error+=1
                                continue                            
                    else:
                        error_data=row_data+'(required valid balance type, client and amount)\n'
                        error_str=error_str+error_data
                        count_error+=1
                        continue

                except:
                    error_data=row_data+'(error in process!)\n'
                    error_str=error_str+error_data
                    count_error+=1
                    continue
            else:
                error_data=row_data+'(3 columns need in a row)\n'
                error_str=error_str+error_data
                count_error+=1
                continue
        
        if error_str=='':
            error_str='No error'
        
        if len(ins_list) > 0:
            inCountList=db.sm_transaction.bulk_insert(ins_list)             
            
        return dict(count_inserted=count_inserted,count_error=count_error,error_str=error_str,total_row=total_row)        
    
    return dict(count_inserted=count_inserted,count_error=count_error,error_str=error_str,total_row=total_row)

def download_client_opening():  
    #Check access permission
    task_id='rm_client_payment_manage'
    task_id_view='rm_client_payment_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL(c='default',f='home'))
        
    c_id=session.cid
    
    records=''
    
    qset=db()
    qset=qset(db.sm_transaction.cid==c_id)
    qset=qset(db.sm_transaction.tx_type=='OPENING')
    qset=qset(db.sm_transaction.sales_type=='S')
    
    if (session.user_type=='Depot'):
        qset=qset(db.sm_transaction.tx_account=='DPT-'+str(session.depot_id))
        
    if (session.btn_filter_cop):
        searchValue=str(session.tx_account_value_cop).split('-')[0]
        
        if (session.user_type=='Depot'):
            qset=qset(db.sm_transaction.opposite_account=='CLT-'+searchValue)
        else:
            qset=qset(db.sm_transaction.tx_account=='CLT-'+searchValue)
            
    records=qset.select(db.sm_transaction.ALL,orderby=~db.sm_transaction.id)
    
    #---------
    myString='Client Opening\n\n'
    myString+='ID,Depot,Balance Type,Client,Amount,Dr/Cr,Date\n'
    
    for rec in records:
        txid=rec.txid
        tx_account=rec.tx_account
        tx_des=rec.tx_des
        opposite_account=rec.opposite_account
        tx_amount=rec.tx_amount
        
        tx_date=str(rec.tx_date)[0:10]
        amtType=''
        if float(tx_amount)<0:
            amtType='Cr'
        elif float(tx_amount)>0:
            amtType='Dr'
        
        myString+=str(txid)+','+str(tx_account)+','+str(tx_des)+','+str(opposite_account)+','+str(tx_amount)+','+str(amtType)+','+str(tx_date)+'\n'
        
    #-----------
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_client_opening.csv'   
    return str(myString)

def reports_home():
    c_id=session.cid
    if (session.cid=='' or session.cid==None):
        redirect (URL('default','home'))    
    if int(session.setting_report)!=1:
        session.flash='Access is Denied !'
        redirect (URL('default','home'))
    
    #----------------------------
    response.title='Ledger Reports'
    
    search_date=SQLFORM(db.sm_search_date,
                  fields=['from_dt','to_dt']           
                  )
    
    btn_present_balance=request.vars.btn_present_balance
    myAccountValue=str(request.vars.myAccountValue).strip()
    
    #---------------------
    accountList=[]
#    if (session.user_type=='Depot'):
#        myDepot='DPT-'+str(session.depot_id)
#        accountList.append(myDepot)    
#    else:
#        depotRecords=db(db.sm_depot.cid==c_id).select(db.sm_depot.depot_id ,orderby=db.sm_depot.name)
#        for row in depotRecords:
#            depot_id='DPT-'+str(row.depot_id)            
#            accountList.append(depot_id)   
#        
#        depotSttRows=db((db.sm_depot_settings.cid==c_id)&(db.sm_depot_settings.from_to_type=='Receive')).select(db.sm_depot_settings.depot_id,db.sm_depot_settings.depot_id_from_to,orderby=db.sm_depot_settings.depot_id|db.sm_depot_settings.depot_id_from_to)
#        
#        for dRow in depotSttRows:
#            depot_from=dRow.depot_id
#            
#            depot_to='DPT-'+str(dRow.depot_id_from_to)
#            if depot_to not in accountList:            
#                accountList.append(depot_to)
    
    depotStr=''
    if (session.user_type=='Depot'):
        myDepot='DPT-'+str(session.depot_id)
        myDepotName=str(session.user_depot_name)
        dptDict={'dptid':myDepot,'dptname':myDepotName}
        dptIdName=myDepot+':'+myDepotName
        #accountList.append(dptIdName)
        
        depotStr=dptIdName
        
    else:
        tempList=[]
        depotRecords=db(db.sm_depot.cid==c_id).select(db.sm_depot.depot_id,db.sm_depot.name ,orderby=db.sm_depot.name)
        for row in depotRecords:
            depot_id='DPT-'+str(row.depot_id) 
            depotName=str(row.name)            
            
            dptDict={'dptid':depot_id,'dptname':depotName}
            dptIdName=depot_id+':'+depotName
            #accountList.append(dptIdName)   
            
            tempList.append(depot_id)   
            
            if depotStr=='':
                depotStr=dptIdName
            else:
                depotStr+='fdrd'+dptIdName
            
        #get from depot settings
        depotSttRows=db((db.sm_depot_settings.cid==c_id)&(db.sm_depot_settings.from_to_type=='Receive')).select(db.sm_depot_settings.depot_id,db.sm_depot_settings.depot_id_from_to,orderby=db.sm_depot_settings.depot_id|db.sm_depot_settings.depot_id_from_to)
        for dRow in depotSttRows:
            depot_to='DPT-'+str(dRow.depot_id_from_to)
            
            if depot_to not in tempList:            
                depotName=str(dRow.depot_id_from_to)
                
                dptIdName=depot_to+':'+depotName
#                accountList.append(dptIdName)
                
                tempList.append(depot_to)
                
                if depotStr=='':
                    depotStr=dptIdName
                else:
                    depotStr+='fdrd'+dptIdName
                
    #-----------------    
    btn_ledger_details=request.vars.btn_ledger_details
    btn_ledger_summary=request.vars.btn_transaction_summary
    
    from_dt=request.vars.from_dt
    to_dt=request.vars.to_dt
    
    txAccountValue=str(request.vars.txAccountValue).strip().upper()
    txOppositeAccountValue=str(request.vars.txOppositeAccountValue).strip().upper()
    txType=request.vars.txType
    
    txReportType=request.vars.txReportType
    
    if btn_present_balance:
        if myAccountValue=='':
            response.flash='Account must needed'
        else:
            searchValue=str(myAccountValue).split(':')[0]
            
            redirect(URL(c='utility',f='present_balance_with_others',vars=dict(page=0,myAccountValue=searchValue)))
    
    elif btn_ledger_details:
        if from_dt=='' or to_dt=='' or txAccountValue=='':
            response.flash='Date and Account must needed'
        else:
            redirect(URL(c='utility',f='ledger_details',vars=dict(page=0,from_date=from_dt,to_date=to_dt,txAccountValue=txAccountValue,txOppositeAccountValue=txOppositeAccountValue,txType=txType)))
    
    elif btn_ledger_summary:
        if from_dt=='' or to_dt=='' or txAccountValue=='':
            response.flash='Date and Account must needed'
        else:
            redirect(URL(c='utility',f='transaction_summary',vars=dict(page=0,from_date=from_dt,to_date=to_dt,txAccountValue=txAccountValue,txOppositeAccountValue=txOppositeAccountValue,txType=txType,txReportType=txReportType)))

    return dict(message='Reports',accountList=accountList,depotStr=depotStr,search_date=search_date)

def present_balance_with_others():    
    if (session.cid=='' or session.cid==None):
        redirect (URL('default','home'))    
    if int(session.setting_report)!=1:
        session.flash='Access is Denied !'
        redirect (URL(c='default',f='home'))
    
    c_id=session.cid
    response.title='Report-Present Balance'
    
    #-------------
    myAccountValue=request.vars.myAccountValue
    clientIdName=request.vars.client_details
    if clientIdName==None:
        clientIdName=''
        
    clientId=''
    if clientIdName!='':
        clientId=clientIdName.split('|')[0]
    
    
    page=int(request.vars.page)
    #----------paging
    if (page > 0):
        page=page
    else:
        page=0
    items_per_page=session.items_per_page
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #----------end paging
    
    pageOpening=request.vars.pageOpening
    if (pageOpening=='' or pageOpening==None):
        pageOpening=0.0
    
    #--------------
    qset=db()    
    qset=qset(db.sm_transaction.cid==c_id)    
    qset=qset(db.sm_transaction.tx_account==myAccountValue)
    
    if clientId!='':
        oppositAcc='CLT-'+str(clientId)
        qset=qset(db.sm_transaction.opposite_account==oppositAcc)
    
    qset=qset(db.sm_transaction.row_flag=='0')
    
    # txReportType 0 for summary, '' for all
    
    txRecords=qset.select(db.sm_transaction.ALL,orderby=db.sm_transaction.sales_type|db.sm_transaction.tx_date,limitby=limitby)
    
    #-------------------------
    return dict(txRecords=txRecords,myAccountValue=myAccountValue,clientIdName=clientIdName,pageOpening=pageOpening,page=page,items_per_page=items_per_page)
def download_present_balance_with_others():
    if (session.cid=='' or session.cid==None):
        redirect (URL('default','home'))    
    if int(session.setting_report)!=1:
        session.flash='Access is Denied !'
        redirect (URL(c='default',f='home'))
    
    c_id=session.cid
    
    #-------------
    myAccountValue=request.vars.myAccountValue
    
    
    #--------------
    qset=db()    
    qset=qset(db.sm_transaction.cid==c_id)
 
    qset=qset(db.sm_transaction.tx_account==myAccountValue)
    qset=qset(db.sm_transaction.row_flag=='0')
    
    txRecords=qset.select(db.sm_transaction.ALL,orderby=db.sm_transaction.sales_type|db.sm_transaction.tx_date)
    
    #---------
    myString='Present Balance With Others\n\n'
    myString+='Account,:'+str(myAccountValue)+'\n\n'
    
    myString+='Opposite Account,Sales Type,Date,Last Description,Opening,Transaction,Closing,Dr/Cr\n'
    
    totalClosing=0
    for rec in txRecords:
        txid=rec.txid
        tx_account=rec.tx_account
        opposite_account=rec.opposite_account        
        tx_date=str(rec.tx_date)[0:10]
        tx_des=rec.tx_des        
        sales_type=rec.sales_type
        
        tx_op_balance=rec.tx_op_balance
        tx_amount=rec.tx_amount
        tx_closing_balance=rec.tx_closing_balance
        
        amtType=''
        if float(tx_closing_balance)<0:
            amtType='Cr'
        elif float(tx_closing_balance)>0:
            amtType='Dr'
        
        if sales_type=='P':
            sales_type='Primary'
        elif sales_type=='S':
            sales_type='Secondary'
        
        totalClosing+=float(tx_closing_balance)
        
        myString+=str(opposite_account)+','+str(sales_type)+','+str(tx_date)+','+str(tx_des)+','+str(tx_op_balance)+','+str(tx_amount)+','+str(tx_closing_balance)+','+str(amtType)+'\n'
    
    amtType=''
    if float(totalClosing)<0:
        amtType='Cr'
    elif float(totalClosing)>0:
        amtType='Dr'
    
    myString+=',,,,,Total,'+str(totalClosing)+','+str(amtType)+'\n'
    
    #-----------
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_present_balance_with_others.csv'   
    return str(myString)
    
def transaction_details():    
    if (session.cid=='' or session.cid==None):
        redirect (URL('default','home'))    
    if int(session.setting_report)!=1:
        session.flash='Access is Denied !'
        redirect (URL(c='default',f='home'))
    
    c_id=session.cid
    response.title='Report-Transaction Details'
    
    #-------------
    myAccountValue=request.vars.myAccountValue
    opposite_account=request.vars.opposite_account
    
    page=int(request.vars.page)
    #----------paging
    if (page > 0):
        page=page
    else:
        page=0
    items_per_page=session.items_per_page
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #----------end paging
    
    #--------------
    qset=db()
    qset=qset(db.sm_transaction.cid==c_id)

    qset=qset(db.sm_transaction.tx_account==myAccountValue)    
    qset=qset(db.sm_transaction.opposite_account==opposite_account)
    
    txRecords=qset.select(db.sm_transaction.ALL,orderby=~db.sm_transaction.id,limitby=limitby)
    
    depotName=''
    if myAccountValue!='':
        depotID=str(myAccountValue)[4:]
        rows_depot=db((db.sm_depot.cid==c_id) & (db.sm_depot.depot_id==depotID)).select(db.sm_depot.name,limitby=(0,1))
        if rows_depot:
            depotName=rows_depot[0].name
    
    customerName=''
    if opposite_account!='':
        custID=str(opposite_account)[4:]
        
        check_client=db((db.sm_client.cid==c_id) & (db.sm_client.client_id==custID)).select(db.sm_client.name,limitby=(0,1))
        if check_client:
            customerName=check_client[0].name
        
    #-------------------------
    return dict(txRecords=txRecords,myAccountValue=myAccountValue,depotName=depotName,opposite_account=opposite_account,customerName=customerName,page=page,items_per_page=items_per_page)
def download_transaction_details():
    if (session.cid=='' or session.cid==None):
        redirect (URL('default','home'))    
    if int(session.setting_report)!=1:
        session.flash='Access is Denied !'
        redirect (URL(c='default',f='home'))
        
    c_id=session.cid

    #-------------
    myAccountValue=request.vars.myAccountValue
    opposite_account=request.vars.opposite_account
    
    #--------------
    qset=db()
    
    qset=qset(db.sm_transaction.cid==c_id)

    qset=qset(db.sm_transaction.tx_account==myAccountValue)    
    qset=qset(db.sm_transaction.opposite_account==opposite_account)
    
    txRecords=qset.select(db.sm_transaction.ALL,orderby=~db.sm_transaction.id)
    
    #---------
    myString='Transaction Details\n\n'
    myString+='Account,:'+str(myAccountValue)+'\n'
    myString+='Opposite Account,:'+str(opposite_account)+'\n\n'
    
    myString+='Opposite Account,Date,Description,Type,Reference,Opening,Transaction,Closing,Dr/Cr\n'
    
    totalClosing=0
    for rec in txRecords:
        txid=rec.txid
        tx_account=rec.tx_account
        opposite_account=rec.opposite_account        
        tx_date=str(rec.tx_date)[0:10]
        tx_des=rec.tx_des   
        tx_type=rec.tx_type     
        sales_type=rec.sales_type
        reference=rec.reference
        
        tx_op_balance=rec.tx_op_balance
        tx_amount=rec.tx_amount
        tx_closing_balance=rec.tx_closing_balance
        
        amtType=''
        if float(tx_closing_balance)<0:
            amtType='Cr'
        elif float(tx_closing_balance)>0:
            amtType='Dr'

        myString+=str(opposite_account)+','+str(tx_date)+','+str(tx_des)+','+str(tx_type)+','+str(reference)+'.,'+str(tx_op_balance)+','+str(tx_amount)+','+str(tx_closing_balance)+','+str(amtType)+'\n'
        
    
    #-----------
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_transaction_details.csv'   
    return str(myString)


def process_report():
    c_id=session.cid
    task_id='rm_report_process_manage'
    access_permission=check_role(task_id)
    if (access_permission==False ):
        session.flash='Access is Denied'
        redirect (URL('default','home'))
    
    #----------------------------
    response.title='Process Report'
    
        
    btn_process_submit=request.vars.btn_process_submit
    btn_delete=request.vars.btn_delete
    btn_process=request.vars.btn_process
    
    if btn_process_submit:
        yearValue1=request.vars.yearValue1
        monthValue1=request.vars.monthValue1
        
        yearValue2=request.vars.yearValue2        
        monthValue2=request.vars.monthValue2
        
        if yearValue1=='' or monthValue1=='' or yearValue2=='' or monthValue2=='':
            response.flash='Valid Month-1 and Month-2 Required'
        else:
            month_1=str(yearValue1)+'-'+str(monthValue1)+'-01'
            month_2=str(yearValue2)+'-'+str(monthValue2)+'-01'
            
            process_key=str(yearValue1)+str(monthValue1)+'-'+str(yearValue2)+str(monthValue2)
            
            if month_1==month_2:
                response.flash='Month-1 and Month-2 can not be same'
                
            else:
                existRow=db(db.sm_temp_report_process.cid==c_id).select(db.sm_temp_report_process.ALL)
                if existRow:
                    response.flash='Already submitted, delete the existing process and submit new one'
                
                else:            
                    db.sm_temp_report_process.insert(cid=c_id,month_1=month_1,month_2=month_2,process_key=process_key,status='Submitted')
                    response.flash='Submitted successfully'
    
    elif btn_delete:        
        existRow=db((db.sm_temp_report_process.cid==c_id)&((db.sm_temp_report_process.status_flag==0)|(db.sm_temp_report_process.status_flag==3))).select(db.sm_temp_report_process.ALL)
        if not existRow:
            response.flash='Delete not applicable'
        else:
            db.sm_temp_report.truncate()
            db.sm_temp_report_process.truncate()
            response.flash='Deleted successfully'
    
    elif btn_process:
        existRow=db((db.sm_temp_report_process.cid==c_id)&(db.sm_temp_report_process.status_flag==0)).select(db.sm_temp_report_process.ALL,limitby=(0,1))
        if not existRow:
            response.flash='Process not applicable'
        else:
            created_date=str(existRow[0].created_date)
            
            month_1=str(existRow[0].month_1)
            month_2=str(existRow[0].month_2)
            process_key=existRow[0].process_key
            
            #--------------
            #dateRecords="SELECT L.level0 as level0,L.level1 as level1, O.rep_id as repId,O.rep_name as repName, sum(O.quantity*O.price) as orderTotal FROM sm_order O,sm_level L WHERE L.cid='"+c_id+"' And L.is_leaf='1'  And O.cid='"+c_id+"' And O.ym_date=='"+str(month_1)+"' And (O.area_id=L.level_id) Group by L.level0,L.level1,O.rep_id order by L.level0,L.level1,O.rep_id"
            
            sqlRows="INSERT INTO sm_temp_report(cid,created_date,month_date,process_key,region_id,tl_id,mpo_id,mpo_name,m1_amt,m2_amt,m1_order_count,m2_order_count) SELECT '"+c_id+"','"+created_date+"','"+month_1+"','"+process_key+"', L.level0 as level0,L.level1 as level1, O.rep_id as repId,O.rep_name as repName, sum(O.quantity*O.price) as orderTotal,'0',count(distinct O.vsl) as orderCount,'0' FROM sm_order O,sm_level L WHERE L.cid='"+c_id+"' And L.is_leaf='1'  And O.cid='"+c_id+"' And O.ym_date='"+str(month_1)+"' And (O.area_id=L.level_id) Group by L.level0,L.level1,O.rep_id order by L.level0,L.level1,O.rep_id"     
            insertRows=db.executesql(sqlRows)
            existRow[0].update_record(status_flag=1,status='Month-1 Completed')
            time.sleep(2)
            
            sqlRows2="INSERT INTO sm_temp_report(cid,created_date,month_date,process_key,region_id,tl_id,mpo_id,mpo_name,m1_amt,m2_amt,m1_order_count,m2_order_count) SELECT '"+c_id+"','"+created_date+"','"+month_2+"','"+process_key+"', L.level0 as level0,L.level1 as level1, O.rep_id as repId,O.rep_name as repName,'0', sum(O.quantity*O.price) as orderTotal,'0',count(distinct O.vsl) as orderCount FROM sm_order O,sm_level L WHERE L.cid='"+c_id+"' And L.is_leaf='1'  And O.cid='"+c_id+"' And O.ym_date='"+str(month_2)+"' And (O.area_id=L.level_id) Group by L.level0,L.level1,O.rep_id order by L.level0,L.level1,O.rep_id"     
            insertRows2=db.executesql(sqlRows2)
            existRow[0].update_record(status_flag=2,status='Month-2 Completed')
            
            updateSqlRows="UPDATE sm_temp_report,sm_level SET sm_temp_report.region_name = sm_level.level_name WHERE sm_level.level_id = sm_temp_report.region_id AND sm_level.depth =  '0'"
            updateRows=db.executesql(updateSqlRows)
            
            updateSqlRows2="UPDATE sm_temp_report,sm_level SET sm_temp_report.tl_name = sm_level.level_name WHERE sm_level.level_id = sm_temp_report.tl_id AND sm_level.depth =  '1'"
            updateRows2=db.executesql(updateSqlRows2)
            
            #---------------
            existRow[0].update_record(status_flag=3,status='Completed')
            response.flash='Successfully Processed'
            
    #--------------
    records=db(db.sm_temp_report_process.cid==c_id).select(db.sm_temp_report_process.ALL)
    
    return dict(records=records,access_permission=access_permission)
    
def process_report_show():
    c_id=session.cid
    task_id='rm_analysis_view'
    access_permission=check_role(task_id)
    if (access_permission==False ):
        session.flash='Access is Denied'
        redirect (URL('default','home'))
    
    #----------------------------
    response.title='Processed Tabulation Sheet'
    
    #--------------
    processRow=db(db.sm_temp_report_process.cid==c_id).select(db.sm_temp_report_process.ALL,limitby=(0,1))
    if not processRow:
        session.flash='Process report not available'
        redirect (URL('process_report'))
    
    #------------
    btn_filter_pReport=request.vars.btn_filter
    btn_all=request.vars.btn_all
    reqPage=len(request.args)
    
    if btn_filter_pReport:
        session.search_type_pReport=request.vars.search_type
        session.search_value_pReport=str(request.vars.search_value).strip().upper()
        reqPage=0
    elif btn_all:
        session.search_type_pReport=None
        session.search_value_pReport=None
        reqPage=0
    
    #--------paging
    if reqPage:
        page=int(request.args[0])
    else:
        page=0
    items_per_page=50
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #--------end paging  
    
    if (session.search_type_pReport=='RSM'):
        if session.search_value_pReport=='' or session.search_value_pReport==None:
            records=db(db.sm_temp_report.cid==c_id).select(db.sm_temp_report.region_id,db.sm_temp_report.region_name,db.sm_temp_report.m1_amt.sum(),db.sm_temp_report.m2_amt.sum(),db.sm_temp_report.m1_order_count.sum(),db.sm_temp_report.m2_order_count.sum(),orderby=db.sm_temp_report.region_id,groupby=db.sm_temp_report.region_id,limitby=limitby)
        else:
            region_id=str(session.search_value_pReport).split('|')[0]
            records=db((db.sm_temp_report.cid==c_id)&(db.sm_temp_report.region_id==region_id)).select(db.sm_temp_report.region_id,db.sm_temp_report.region_name,db.sm_temp_report.m1_amt.sum(),db.sm_temp_report.m2_amt.sum(),db.sm_temp_report.m1_order_count.sum(),db.sm_temp_report.m2_order_count.sum(),orderby=db.sm_temp_report.region_id,groupby=db.sm_temp_report.region_id,limitby=limitby)
    
    elif (session.search_type_pReport=='TL'):
        if session.search_value_pReport=='' or session.search_value_pReport==None:
            records=db(db.sm_temp_report.cid==c_id).select(db.sm_temp_report.region_id,db.sm_temp_report.region_name,db.sm_temp_report.tl_id,db.sm_temp_report.tl_name,db.sm_temp_report.m1_amt.sum(),db.sm_temp_report.m2_amt.sum(),db.sm_temp_report.m1_order_count.sum(),db.sm_temp_report.m2_order_count.sum(),orderby=db.sm_temp_report.region_id|db.sm_temp_report.tl_id,groupby=db.sm_temp_report.region_id|db.sm_temp_report.tl_id,limitby=limitby)
        else:
            tl_id=str(session.search_value_pReport).split('|')[0]
            records=db((db.sm_temp_report.cid==c_id)&(db.sm_temp_report.tl_id==tl_id)).select(db.sm_temp_report.region_id,db.sm_temp_report.region_name,db.sm_temp_report.tl_id,db.sm_temp_report.tl_name,db.sm_temp_report.m1_amt.sum(),db.sm_temp_report.m2_amt.sum(),db.sm_temp_report.m1_order_count.sum(),db.sm_temp_report.m2_order_count.sum(),orderby=db.sm_temp_report.region_id|db.sm_temp_report.tl_id,groupby=db.sm_temp_report.region_id|db.sm_temp_report.tl_id,limitby=limitby)
    
    elif (session.search_type_pReport=='MPO'):
        if session.search_value_pReport=='' or session.search_value_pReport==None:
            records=db(db.sm_temp_report.cid==c_id).select(db.sm_temp_report.region_id,db.sm_temp_report.region_name,db.sm_temp_report.tl_id,db.sm_temp_report.tl_name,db.sm_temp_report.mpo_id,db.sm_temp_report.mpo_name,db.sm_temp_report.m1_amt.sum(),db.sm_temp_report.m2_amt.sum(),db.sm_temp_report.m1_order_count.sum(),db.sm_temp_report.m2_order_count.sum(),orderby=db.sm_temp_report.region_id|db.sm_temp_report.tl_id|db.sm_temp_report.mpo_id,groupby=db.sm_temp_report.region_id|db.sm_temp_report.tl_id|db.sm_temp_report.mpo_id,limitby=limitby)
        else:
            mpo_id=str(session.search_value_pReport).split('|')[0]
            records=db((db.sm_temp_report.cid==c_id)&(db.sm_temp_report.mpo_id==mpo_id)).select(db.sm_temp_report.region_id,db.sm_temp_report.region_name,db.sm_temp_report.tl_id,db.sm_temp_report.tl_name,db.sm_temp_report.mpo_id,db.sm_temp_report.mpo_name,db.sm_temp_report.m1_amt.sum(),db.sm_temp_report.m2_amt.sum(),db.sm_temp_report.m1_order_count.sum(),db.sm_temp_report.m2_order_count.sum(),orderby=db.sm_temp_report.region_id|db.sm_temp_report.tl_id|db.sm_temp_report.mpo_id,groupby=db.sm_temp_report.region_id|db.sm_temp_report.tl_id|db.sm_temp_report.mpo_id,limitby=limitby)
                        
    else:
        records=db(db.sm_temp_report.cid==c_id).select(db.sm_temp_report.region_id,db.sm_temp_report.region_name,db.sm_temp_report.tl_id,db.sm_temp_report.tl_name,db.sm_temp_report.mpo_id,db.sm_temp_report.mpo_name,db.sm_temp_report.m1_amt.sum(),db.sm_temp_report.m2_amt.sum(),db.sm_temp_report.m1_order_count.sum(),db.sm_temp_report.m2_order_count.sum(),orderby=db.sm_temp_report.region_id|db.sm_temp_report.tl_id|db.sm_temp_report.mpo_id,groupby=db.sm_temp_report.region_id|db.sm_temp_report.tl_id|db.sm_temp_report.mpo_id,limitby=limitby)
        
    
    return dict(processRow=processRow,records=records,page=page,items_per_page=items_per_page,access_permission=access_permission)
    
    
def process_report_download():
    c_id=session.cid
    task_id='rm_analysis_view'
    access_permission=check_role(task_id)
    if (access_permission==False ):
        session.flash='Access is Denied'
        redirect (URL('default','home'))
    
    
    #--------------
    processRow=db(db.sm_temp_report_process.cid==c_id).select(db.sm_temp_report_process.ALL,limitby=(0,1))
    if not processRow:
        session.flash='Process report not available'
        redirect (URL('process_report'))
    
    #------------
    if (session.search_type_pReport=='RSM'):
        if session.search_value_pReport=='' or session.search_value_pReport==None:
            records=db(db.sm_temp_report.cid==c_id).select(db.sm_temp_report.region_id,db.sm_temp_report.region_name,db.sm_temp_report.m1_amt.sum(),db.sm_temp_report.m2_amt.sum(),db.sm_temp_report.m1_order_count.sum(),db.sm_temp_report.m2_order_count.sum(),orderby=db.sm_temp_report.region_id,groupby=db.sm_temp_report.region_id)
        else:
            region_id=str(session.search_value_pReport).split('|')[0]
            records=db((db.sm_temp_report.cid==c_id)&(db.sm_temp_report.region_id==region_id)).select(db.sm_temp_report.region_id,db.sm_temp_report.region_name,db.sm_temp_report.m1_amt.sum(),db.sm_temp_report.m2_amt.sum(),db.sm_temp_report.m1_order_count.sum(),db.sm_temp_report.m2_order_count.sum(),orderby=db.sm_temp_report.region_id,groupby=db.sm_temp_report.region_id)
    
    elif (session.search_type_pReport=='TL'):
        if session.search_value_pReport=='' or session.search_value_pReport==None:
            records=db(db.sm_temp_report.cid==c_id).select(db.sm_temp_report.region_id,db.sm_temp_report.region_name,db.sm_temp_report.tl_id,db.sm_temp_report.tl_name,db.sm_temp_report.m1_amt.sum(),db.sm_temp_report.m2_amt.sum(),db.sm_temp_report.m1_order_count.sum(),db.sm_temp_report.m2_order_count.sum(),orderby=db.sm_temp_report.region_id|db.sm_temp_report.tl_id,groupby=db.sm_temp_report.region_id|db.sm_temp_report.tl_id)
        else:
            tl_id=str(session.search_value_pReport).split('|')[0]
            records=db((db.sm_temp_report.cid==c_id)&(db.sm_temp_report.tl_id==tl_id)).select(db.sm_temp_report.region_id,db.sm_temp_report.region_name,db.sm_temp_report.tl_id,db.sm_temp_report.tl_name,db.sm_temp_report.m1_amt.sum(),db.sm_temp_report.m2_amt.sum(),db.sm_temp_report.m1_order_count.sum(),db.sm_temp_report.m2_order_count.sum(),orderby=db.sm_temp_report.region_id|db.sm_temp_report.tl_id,groupby=db.sm_temp_report.region_id|db.sm_temp_report.tl_id)
    
    elif (session.search_type_pReport=='MPO'):
        if session.search_value_pReport=='' or session.search_value_pReport==None:
            records=db(db.sm_temp_report.cid==c_id).select(db.sm_temp_report.region_id,db.sm_temp_report.region_name,db.sm_temp_report.tl_id,db.sm_temp_report.tl_name,db.sm_temp_report.mpo_id,db.sm_temp_report.mpo_name,db.sm_temp_report.m1_amt.sum(),db.sm_temp_report.m2_amt.sum(),db.sm_temp_report.m1_order_count.sum(),db.sm_temp_report.m2_order_count.sum(),orderby=db.sm_temp_report.region_id|db.sm_temp_report.tl_id|db.sm_temp_report.mpo_id,groupby=db.sm_temp_report.region_id|db.sm_temp_report.tl_id|db.sm_temp_report.mpo_id)
        else:
            mpo_id=str(session.search_value_pReport).split('|')[0]
            records=db((db.sm_temp_report.cid==c_id)&(db.sm_temp_report.mpo_id==mpo_id)).select(db.sm_temp_report.region_id,db.sm_temp_report.region_name,db.sm_temp_report.tl_id,db.sm_temp_report.tl_name,db.sm_temp_report.mpo_id,db.sm_temp_report.mpo_name,db.sm_temp_report.m1_amt.sum(),db.sm_temp_report.m2_amt.sum(),db.sm_temp_report.m1_order_count.sum(),db.sm_temp_report.m2_order_count.sum(),orderby=db.sm_temp_report.region_id|db.sm_temp_report.tl_id|db.sm_temp_report.mpo_id,groupby=db.sm_temp_report.region_id|db.sm_temp_report.tl_id|db.sm_temp_report.mpo_id)
    
    else:
        records=db(db.sm_temp_report.cid==c_id).select(db.sm_temp_report.region_id,db.sm_temp_report.region_name,db.sm_temp_report.tl_id,db.sm_temp_report.tl_name,db.sm_temp_report.mpo_id,db.sm_temp_report.mpo_name,db.sm_temp_report.m1_amt.sum(),db.sm_temp_report.m2_amt.sum(),db.sm_temp_report.m1_order_count.sum(),db.sm_temp_report.m2_order_count.sum(),orderby=db.sm_temp_report.region_id|db.sm_temp_report.tl_id|db.sm_temp_report.mpo_id,groupby=db.sm_temp_report.region_id|db.sm_temp_report.tl_id|db.sm_temp_report.mpo_id)
    
    myString='Tabulation Sheet\n'
    myString+='Process Date,'+str(processRow[0].created_date)+'\n'
    
    #----------------
    if session.search_type_pReport=='RSM':
        myString+='RSM Wise\n\n'
        
        myString+='RSM,'+str(processRow[0].month_1.strftime('%b-%Y'))+',,'+str(processRow[0].month_2.strftime('%b-%Y'))+'\n'
        myString+=',Order Count,Amount,Order Count,Amount\n'
        for record in records:
            region_id=record.sm_temp_report.region_id
            region_name=str(record.sm_temp_report.region_name).replace(',', ' ')
            
            m1_amt=round(record[db.sm_temp_report.m1_amt.sum()],2)
            m2_amt=round(record[db.sm_temp_report.m2_amt.sum()],2)
            
            m1_order_count=record[db.sm_temp_report.m1_order_count.sum()]
            m2_order_count=record[db.sm_temp_report.m2_order_count.sum()]
            
            myString+=str(region_id)+' | '+region_name+','+str(m1_order_count)+','+str(m1_amt)+','+str(m2_order_count)+','+str(m2_amt)+'\n'
    
    #-----------------
    elif session.search_type_pReport=='TL':
        myString+='TL Wise\n\n'
             
        myString+='RSM,TL,'+str(processRow[0].month_1.strftime('%b-%Y'))+',,'+str(processRow[0].month_2.strftime('%b-%Y'))+'\n'
        myString+=',,Order Count,Amount,Order Count,Amount\n'
        
        for record in records:
            region_id=record.sm_temp_report.region_id
            region_name=str(record.sm_temp_report.region_name).replace(',', ' ')
            
            tl_id=record.sm_temp_report.tl_id
            tl_name=str(record.sm_temp_report.tl_name).replace(',', ' ')
            
            m1_amt=round(record[db.sm_temp_report.m1_amt.sum()],2)
            m2_amt=round(record[db.sm_temp_report.m2_amt.sum()],2)
            
            m1_order_count=record[db.sm_temp_report.m1_order_count.sum()]
            m2_order_count=record[db.sm_temp_report.m2_order_count.sum()]
            
            myString+=str(region_id)+' | '+region_name+','+str(tl_id)+' | '+tl_name+','+str(m1_order_count)+','+str(m1_amt)+','+str(m2_order_count)+','+str(m2_amt)+'\n'
    
    #-----------------------
    elif session.search_type_pReport=='MPO' or session.search_type_pReport=='' or session.search_type_pReport==None:
        myString+='MPO Wise\n\n'
         
        myString+='RSM,TL,MPO,'+str(processRow[0].month_1.strftime('%b-%Y'))+',,'+str(processRow[0].month_2.strftime('%b-%Y'))+'\n'
        myString+=',,,Order Count,Amount,Order Count,Amount\n'
        for record in records:
            region_id=record.sm_temp_report.region_id
            region_name=str(record.sm_temp_report.region_name).replace(',', ' ')
            
            tl_id=record.sm_temp_report.tl_id
            tl_name=str(record.sm_temp_report.tl_name).replace(',', ' ')
            
            mpo_id=record.sm_temp_report.mpo_id
            mpo_name=str(record.sm_temp_report.mpo_name).replace(',', ' ')
            
            m1_amt=round(record[db.sm_temp_report.m1_amt.sum()],2)
            m2_amt=round(record[db.sm_temp_report.m2_amt.sum()],2)
            
            m1_order_count=record[db.sm_temp_report.m1_order_count.sum()]
            m2_order_count=record[db.sm_temp_report.m2_order_count.sum()]
            
            myString+=str(region_id)+' | '+region_name+','+str(tl_id)+' | '+tl_name+','+str(mpo_id)+' | '+mpo_name+','+str(m1_order_count)+','+str(m1_amt)+','+str(m2_order_count)+','+str(m2_amt)+'\n'
    
    
    #Sve as csv
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_process_report.csv'   
    return str(myString)



#---------
def utility_home():
    task_id = 'rm_utility_manage'
    access_permission = check_role(task_id)
    if (access_permission == False):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))
    
    c_id=session.cid
    
    response.title='Utility Home'
    
    #-----------------
    showLastIDType=''
    showLastID=''
    
    #----------
    btn_show_lastID=request.vars.btn_show_lastID
    
    #---------------------
    if btn_show_lastID:
        showLastIDType=str(request.vars.showLastIDType).strip()
        if showLastIDType=='':
            response.title='Select Type'
        else:
            if showLastIDType=='DOCTOR':
                doctorRows=db(db.sm_doctor.cid==c_id).select(db.sm_doctor.doc_id,orderby=~db.sm_doctor.doc_id,limitby=(0,1))
                if doctorRows:
                    showLastID=doctorRows[0].doc_id
                    
            elif showLastIDType=='RETAILER':
                clientRows=db(db.sm_client.cid==c_id).select(db.sm_client.client_id,orderby=~db.sm_client.client_id,limitby=(0,1))
                if clientRows:
                    showLastID=clientRows[0].client_id
            
                    
    return dict(showLastIDType=showLastIDType,showLastID=showLastID)
    
    

