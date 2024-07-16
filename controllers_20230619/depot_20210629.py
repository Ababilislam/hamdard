#depot_catagory_validation
#depot_catagory

#depot_validation
#depot
#depot_edit_validation
#depot_edit
#depot_batch_upload
#depot_settings_validation
#depot_settings
#depot_update_settings_validation
#depot_settings_edit
#depot_stock_validation
#depot_stock------# Not view. Not used for online
#depot_stock_edit----# Not view. Not used for online
#depot_stock_summary_balance---# Not view. Not used for online
#depot_stock_batch_upload----# Not view. Not used for online

#depot_stock_requisition_list
#process_requisition
#depot_stock_requisition
#get_item
#delete_requisition_item
#post_cancel_requisition
#item_selector-----Not used
#depot_stock_issue_list
#process_issue
#depot_stock_issue
#delete_issue_item
#post_cancel_issue
#show_pending_requisition
#depot_stock_receive_list
#process_receive
#depot_stock_receive
#show_pending_issue
#delete_receive_item
#post_cancel_receive
#depot_stock_damage_list
#process_damage
#depot_stock_damage
#delete_damage_item
#post_cancel_damage

#preview_requisition
#preview_issue
#preview_receive
#preview_damage

#depot_area_validation---Not used
#rep_area---Not used
#download_depot_stock_balance---Not used
#download_depot_stock---Not used

#depot_trans_dispute
#depot_trans_dispute_list---Not used

#Validation for catagory
def depot_catagory_validation(form):
    category_id=str(request.vars.cat_type_id).strip().upper()
    if ((category_id!='') and (session.cid!='')):
        rows_check=db((db.sm_category_type.cid==session.cid) & (db.sm_category_type.type_name=='DEPOT_CATEGORY') &(db.sm_category_type.cat_type_id==category_id)).select(db.sm_category_type.cat_type_id,orderby=db.sm_category_type.cat_type_id,limitby=(0,1))
        if rows_check:
            form.errors.cat_type_id=''
            response.flash = 'please choose a new'
        else:
            form.vars.cid=session.cid
            form.vars.type_name='DEPOT_CATEGORY'
            form.vars.cat_type_id=category_id
            
def depot_catagory():
    task_id='rm_depot_type_manage'
    task_id_view='rm_depot_type_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))
    # ---------------------
    response.title='Depot/Distributor Category'
    
    form =SQLFORM(db.sm_category_type,
                  fields=['cat_type_id'],
                  submit_button='Save'          
                  )
    
    #Insert with validation
    if form.accepts(request.vars,session,onvalidation=depot_catagory_validation):
       response.flash = 'Saved Successfully'
    
    #--------------------------------
    btn_delete=request.vars.btn_delete
    record_id=request.vars.record_id
    
    #If catagorey not in item it can be delete
    if btn_delete:
        record_id=request.args[1]
        category_id=request.args[2]
        records=db((db.sm_depot.cid==session.cid) & (db.sm_depot.depot_category==category_id)).select(db.sm_depot.depot_category,limitby=(0,1))
        if not records:
            db((db.sm_category_type.id==record_id)&(db.sm_category_type.type_name=='DEPOT_CATEGORY')).delete()
        else:
            response.flash='This category is used in Depot/Distributor'
    
    #--------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=session.items_per_page
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #--------end paging
    
    records=db((db.sm_category_type.cid==session.cid)& (db.sm_category_type.type_name=='DEPOT_CATEGORY')).select(db.sm_category_type.ALL,orderby=db.sm_category_type.cat_type_id,limitby=limitby)
    
    return dict(form=form,records=records,page=page,items_per_page=items_per_page,access_permission=access_permission)

#---------------depot
def depot_validation(form):
    c_id=session.cid
    dm_pass=request.vars.dm_pass
    depot_id=str(form.vars.depot_id).strip().upper()
#    reporting_level_id=str(form.vars.reporting_level_id).strip().upper()
#    op_balance=request.vars.op_balance
    
    name_row=str(form.vars.name)
    name=check_special_char(name_row)
    form.vars.name=name
    
    rows_check=db((db.sm_depot.cid==c_id) & (db.sm_depot.depot_id==depot_id)).select(db.sm_depot.depot_id,limitby=(0,1))
    if rows_check:
        form.errors.depot_id=''
        response.flash = 'please choose a new '
    else:
#            if reporting_level_id!='':
#                levelRecords=db((db.sm_level.cid==c_id) & (db.sm_level.level_id==reporting_level_id)& (db.sm_level.is_leaf == '0')).select(db.sm_level.level_name,limitby=(0,1))
#                if not levelRecords:
#                    form.errors.reporting_level_id='invalid level id!'
#                else:
#                    level_name=levelRecords[0].level_name
#                    form.vars.reporting_level_name=level_name
        
        form.vars.depot_id=depot_id
        form.vars.name=name            
        form.vars.dm_pass=dm_pass
#            form.vars.balance=op_balance

def depot():
#    Check access permission
    task_id='rm_depot_manage'
    task_id_view='rm_depot_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))
    
    #   ---------------------
    response.title='Depot/Branch'
    
    c_id=session.cid
    
    db.sm_depot.status.requires=IS_IN_SET(('ACTIVE','INACTIVE'))
    
    # depot_category used for Dealer Type
    db.sm_depot.depot_category.requires=IS_IN_DB(db((db.sm_category_type.cid == session.cid)&(db.sm_category_type.type_name=='DEPOT_CATEGORY')),db.sm_category_type.cat_type_id,orderby=db.sm_category_type.cat_type_id)
    
    form =SQLFORM(db.sm_depot,
                  fields=['depot_id','name','dm_pass','status','depot_category','short_name','field1'],
                  submit_button='Save'
                  )
    
    #    Insert with validation
    if form.accepts(request.vars,session,onvalidation=depot_validation):
       response.flash = 'Submitted Successfully'

    #  ---------------filter-------
    
    btn_filter_depot=request.vars.btn_filter_depot
    btn_all=request.vars.btn_all
    reqPage=len(request.args)
    
    if btn_filter_depot:
        session.search_type_depot=request.vars.search_type
        session.search_value_depot=str(request.vars.search_value).strip().upper()
        reqPage=0
    elif btn_all:
        session.search_type_depot=None
        session.search_value_depot=None
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
    qset=qset(db.sm_depot.cid==c_id)
    
    #---- supervisor
    if session.user_type=='Supervisor':        
        qset=qset(db.sm_depot.depot_id.belongs(session.distributorList))
    else:
        pass
    #----
    
    if (session.search_type_depot=='DepotID'):
        searchValue=str(session.search_value_depot).split('|')[0]
        qset=qset(db.sm_depot.depot_id==searchValue)
        
    elif (session.search_type_depot=='DepotType'):
        qset=qset(db.sm_depot.depot_category==session.search_value_depot)
    
    elif (session.search_type_depot=='Status'):
        qset=qset(db.sm_depot.status==session.search_value_depot)
        
    records=qset.select(db.sm_depot.ALL ,orderby=db.sm_depot.name,limitby=limitby)
    recordsCount=qset.count()
    
    return dict(form=form,records=records,recordsCount=recordsCount,page=page,items_per_page=items_per_page,access_permission=access_permission,access_permission_view=access_permission_view)


#-----------------depot edit---------------------

def depot_edit_validation(form):
    c_id=session.cid
#    reporting_level_id=str(form.vars.reporting_level_id).strip().upper()
#    if reporting_level_id!='':
#        levelRecords=db((db.sm_level.cid==c_id) & (db.sm_level.level_id==reporting_level_id)& (db.sm_level.is_leaf == '0')).select(db.sm_level.level_name,limitby=(0,1))
#        if not levelRecords:
#            form.errors.reporting_level_id='invalid level id!'
#        else:
#            level_name=levelRecords[0].level_name
#            form.vars.reporting_level_name=level_name
    
    name_row=str(form.vars.name)
    name=check_special_char(name_row)
    form.vars.name=name

    form.vars.name=name
        
def depot_edit():
    task_id='rm_depot_manage'
    access_permission=check_role(task_id)
    if (access_permission==False):
        session.flash='Access is Denied !'
        redirect (URL('depot'))
    
    response.title='Depot/Branch'
    #   --------------------- 
    c_id=session.cid
        
    page=request.args(0)
    record= db.sm_depot(request.args(1)) or redirect(URL('depot'))   
    
    db.sm_depot.status.requires=IS_IN_SET(('ACTIVE','INACTIVE'))
    
    # depot_category used for Dealer Type
    db.sm_depot.depot_category.requires=IS_IN_DB(db((db.sm_category_type.cid == session.cid)&(db.sm_category_type.type_name=='DEPOT_CATEGORY')),db.sm_category_type.cat_type_id,orderby=db.sm_category_type.cat_type_id)

    form =SQLFORM(db.sm_depot,
                  record=record,
                  deletable=True,
                  fields=['name','status','dm_pass','depot_category','short_name','field1'],
                  submit_button='Update'
                  )
    
#    Get all data for selected depot
    records_depot=db((db.sm_depot.cid==c_id) & (db.sm_depot.id==request.args(1))).select(db.sm_depot.ALL,limitby=(0,1))
    depot_id=''
    pre_balance=0
    pre_op_bal=0
    requisition_sl=0
    issue_sl=0
    receive_sl=0
    damage_sl=0
    order_sl=0
    del_sl=0
    return_sl=0
    client_payment_sl=0
    depot_payment_sl=0
    for records_show_id in records_depot :
        depot_id=records_show_id.depot_id 
        dm_pass=records_show_id.dm_pass
        pre_op_bal=records_show_id.op_balance
        pre_balance=records_show_id.balance
        requisition_sl=records_show_id.requisition_sl
        issue_sl=records_show_id.issue_sl
        receive_sl=records_show_id.receive_sl
        damage_sl=records_show_id.damage_sl
        order_sl=records_show_id.order_sl
        del_sl=records_show_id.del_sl
        return_sl=records_show_id.return_sl
        client_payment_sl=records_show_id.client_payment_sl
        depot_payment_sl=records_show_id.depot_payment_sl        
        break
    
    if form.accepts(request.vars, session,onvalidation=depot_edit_validation):
        depotName=form.vars.name        
        db((db.sm_client.cid==c_id) & (db.sm_client.depot_id==depot_id)).update(depot_name=depotName)
        
        response.flash = 'Updated Successfully'        
        redirect(URL('depot',args=[page]))
    
    #-------------- use flag
    
#    if depot used then delete option will be hide based on used flag
    
    useFlag=False
    repRecords=db((db.sm_client.cid==c_id) & (db.sm_client.depot_id==depot_id)).select(db.sm_client.depot_id,limitby=(0,1))
    if repRecords:
        useFlag=True
    else:
        if requisition_sl >0 or issue_sl>0 or receive_sl>0 or damage_sl>0 or order_sl>0 or del_sl>0 or client_payment_sl>0 or depot_payment_sl>0:
            useFlag=True
            
    #-----------------
    return dict(form=form,depot_id=depot_id,dm_pass=dm_pass,pre_op_bal=pre_op_bal,pre_balance=pre_balance,page=page,access_permission=access_permission,useFlag=useFlag)
    
def depot_batch_upload():
    #   Check accesspermission
   #----------Task assaign----------
    task_id='rm_depot_manage'
    access_permission=check_role(task_id)
    if access_permission==False:
        session.flash='Access is Denied !'
        redirect (URL('depot'))
        
    #   --------------------- 
    response.title='Depot/Distributor Batch upload'
    c_id=session.cid
    if (c_id=='' or c_id==None):
        redirect(URL('default','index'))
        
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
            
        depotid_list_excel=[]
        depotid_list_exist=[]
        
        category_list_exist=[]
        
        excelDepotList=[]
        levelID_list_excel=[]
        validLevelList=[]
        
        ins_list=[]
        ins_dict={}

        #---------- create depot list based on excel sheet
        for i in range(total_row):
            if i>=30:
                break
            else:
                row_data=row_list[i]                    
                coloum_list=row_data.split( '\t')
                if len(coloum_list)==4:
                    depotid_list_excel.append(str(coloum_list[0]).strip())
        
#        Check if excel depot list already exist in database
        existRows=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id.belongs(depotid_list_excel))).select(db.sm_depot.depot_id,orderby=db.sm_depot.depot_id)
        depotid_list_exist=existRows.as_list()
        
        #Check valid category list based on excel sheet
        catRows=db((db.sm_category_type.cid==c_id)& (db.sm_category_type.type_name=='DEPOT_CATEGORY')).select(db.sm_category_type.cat_type_id,orderby=db.sm_category_type.cat_type_id)
        category_list_exist=catRows.as_list()
        
        #Check valid level list based on excel sheet
#        levelRows=db((db.sm_level.cid==c_id) & (db.sm_level.level_id.belongs(levelID_list_excel))& (db.sm_level.is_leaf == '0')).select(db.sm_level.level_id,db.sm_level.level_name)
#        validLevelList=levelRows.as_list()

        #   --------------------  main loop   
        for i in range(total_row):
            if i>=30: 
                break
            else:
                row_data=row_list[i]
            coloum_list=row_data.split( '\t')            
            
            if len(coloum_list)==4:
                depot_id=str(coloum_list[0]).strip().upper()
                name=str(coloum_list[1]).strip()
                name=check_special_char(name)#Check spacial char
                
                depotType=str(coloum_list[2]).strip().upper()
                shortName=str(coloum_list[3]).strip()
                
                #Check depot id in  depotid_list_exist list.It will not if no duplicate depot in excel sheet            
                try:
                    valid_category=False
                    duplicate_depot=False
                    levelFlag=True
                                        
                    #Check valid category                          
                    for i in range(len(category_list_exist)):
                        myRowData=category_list_exist[i]                                
                        cat_id=myRowData['cat_type_id']
                        if (str(cat_id).strip()==str(depotType).strip()):
                            valid_category=True
                            break
                    
                    if valid_category==True:                                                                         
                        for i in range(len(depotid_list_exist)):
                            myRowData=depotid_list_exist[i]                                
                            depotId=myRowData['depot_id']
                            if (str(depotId).strip()==str(depot_id).strip()):
                                duplicate_depot=True                                 
                                break
                            
                        #-----------------
                        if duplicate_depot==False:
                            if (name!=''):
                                if levelFlag==True:
                                    #Check duplicate in excel sheet depot list
                                    if depot_id not in excelDepotList:
                                        excelDepotList.append(depot_id)
                                        #Create insert list
                                        ins_dict= {'cid':c_id,'depot_id':depot_id,'name':name,'status':'ACTIVE','depot_category':depotType,'short_name':shortName}
                                        ins_list.append(ins_dict)                               
                                        count_inserted+=1
                                        
                                    else:
                                        error_data=row_data+'(duplicate in excel)\n'
                                        error_str=error_str+error_data
                                        count_error+=1
                                        continue     
                                else:
                                    error_data=row_data+'(Invalid level)\n'
                                    error_str=error_str+error_data
                                    count_error+=1
                                    continue
                            else:
                                error_data=row_data+'(Name needed)\n'
                                error_str=error_str+error_data
                                count_error+=1
                                continue                            
                        else:
                            error_data=row_data+'(already exist depot)\n'
                            error_str=error_str+error_data
                            count_error+=1
                            continue
                    else:
                        error_data=row_data+'(Invalid Category)\n'
                        error_str=error_str+error_data
                        count_error+=1
                        continue                       
                except:
                    error_data=row_data+'(error in process)\n'
                    error_str=error_str+error_data
                    count_error+=1
                    continue
            else:
                error_data=row_data+'(4 columns need in a row)\n'
                error_str=error_str+error_data
                count_error+=1
                continue
        
        if error_str=='':
            error_str='No error'
        # bulk insert 
        if len(ins_list) > 0:
            inCountList=db.sm_depot.bulk_insert(ins_list)
            
        return dict(count_inserted=count_inserted,count_error=count_error,error_str=error_str,total_row=total_row)        
    
    return dict(count_inserted=count_inserted,count_error=count_error,error_str=error_str,total_row=total_row)

#------------------item end----------------------

def download_depot():
    task_id='rm_depot_manage'
    task_id_view='rm_depot_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))
    
    #   ---------------------
    c_id=session.cid
    
    #   -----------
    
    records=''
    
    qset=db()
    qset=qset(db.sm_depot.cid==c_id)
    
    #---- supervisor
    if session.user_type=='Supervisor':        
        qset=qset(db.sm_depot.depot_id.belongs(session.distributorList))
    else:
        pass
    #----
    
    if (session.search_type_depot=='DepotID'):
        searchValue=str(session.search_value_depot).split('|')[0]
        qset=qset(db.sm_depot.depot_id==searchValue)
        
    elif (session.search_type_depot=='DepotType'):
        qset=qset(db.sm_depot.depot_category==session.search_value_depot)
    
    elif (session.search_type_depot=='Status'):
        qset=qset(db.sm_depot.status==session.search_value_depot)
        
    records=qset.select(db.sm_depot.ALL ,orderby=db.sm_depot.name)
    
    #Set column name
    myString='Depot/Distributor List\n\n'
    myString+='ID,Name,Short Name,Type,Status\n'
    for rec in records:
        depot_id=str(rec.depot_id)
        name=str(rec.name).replace(',', ' ')        
        short_name=str(rec.short_name)
        depot_category=str(rec.depot_category)
        status=str(rec.status)
        
        myString+=depot_id+','+name+','+short_name+','+depot_category+','+status+'\n'
        
    #Sve as csv
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_depot.csv'   
    return str(myString)
    
#============================ depot settings
def depot_settings_validation(form):
    c_id=session.cid
    depot_id=str(form.vars.depot_id).strip().upper().split('|')[0]
    depot_id_from_to=str(form.vars.depot_id_from_to).strip().upper().split('|')[0]
    
    depot_id=check_special_char(depot_id)    
    depot_id_from_to=check_special_char(depot_id_from_to)
    
    depotRows1=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.depot_id,limitby=(0,1))
    if not depotRows1:
        form.errors.depot_id=''
        response.flash = 'Invalid Depot ID/External Source'
    else:
        depotRows2=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id_from_to)).select(db.sm_depot.depot_id,limitby=(0,1))
        if not depotRows2:
            form.errors.depot_id=''
            response.flash = 'Invalid Receive From Depot ID/External Source'
        else:
            if (depot_id==depot_id_from_to):
                form.errors.depot_id=''
                response.flash = 'Depot ID and Receive From can not be same'
            else:
                if ((depot_id!='') and (depot_id_from_to!='')):
                    rows_check=db((db.sm_depot_settings.cid==c_id) & (db.sm_depot_settings.depot_id==depot_id)& (db.sm_depot_settings.depot_id_from_to==depot_id_from_to)).select(db.sm_depot_settings.depot_id,limitby=(0,1))
                    if rows_check:
                        form.errors.depot_id=''
                        response.flash = 'already exist'
                    else:
                        form.vars.depot_id=depot_id
                        form.vars.depot_id_from_to=depot_id_from_to

def depot_settings():
    response.title='Depot/Distributor Settings'
    #Check access permission
     #----------Task assaign----------
    task_id='rm_depot_setting_manage'
    task_id_view='rm_depot_setting_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL('depot','depot'))
        
#   --------------------- 
    
    c_id=session.cid
    
#    depotRows=db(db.sm_depot.cid==c_id).select(db.sm_depot.depot_id,db.sm_depot.name,orderby=db.sm_depot.name)
    
#    db.sm_depot_settings.depot_id.requires=IS_IN_DB(db(db.sm_depot.cid==c_id),db.sm_depot.depot_id,orderby=db.sm_depot.depot_id)
    
    form =SQLFORM(db.sm_depot_settings,
                  fields=['depot_id','depot_id_from_to'],
                  submit_button='Save'       
                  )
    #Insert with validation
    if form.accepts(request.vars,session,onvalidation=depot_settings_validation):
       response.flash = 'Submitted Successfully'
    
    reqPage=len(request.args)

    btn_filter_ds=request.vars.btn_filter
    btn_all=request.vars.btn_all
    
    
    #Ready filter text
    depot_id_value=str(request.vars.depot_id_value).strip()
    
    v_type=str(request.vars.type_value).strip()
    
    reqPage=len(request.args)
    #Filter
    if btn_filter_ds:
        session.btn_filter_ds=btn_filter_ds
        
        session.depot_id_value=depot_id_value
        session.v_type_ds=v_type
        
        reqPage=0
        
    elif btn_all:
        session.btn_filter_ds=None
        session.depot_id_value=None
        session.v_type_ds=None
    
    #--------paging
    if reqPage:
        page=int(request.args[0])
    else:
        page=0
    items_per_page=session.items_per_page
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #--------end paging  
    
    qset=db()
    qset=qset(db.sm_depot_settings.cid==c_id)
    qset=qset(db.sm_depot.cid==c_id)
    qset=qset(db.sm_depot.depot_id==db.sm_depot_settings.depot_id)
    
    if (session.btn_filter_ds):
        if not (session.depot_id_value=='' or session.depot_id_value==None):
            qset=qset(db.sm_depot_settings.from_to_type=='Receive')
            
            searchValue=str(session.depot_id_value).split('|')[0]
            qset=qset(db.sm_depot_settings.depot_id_from_to==searchValue)        
            
                
    records=qset.select(db.sm_depot_settings.id,db.sm_depot_settings.depot_id,db.sm_depot_settings.depot_id_from_to,db.sm_depot.name,orderby=db.sm_depot_settings.depot_id,limitby=limitby)
#------------------------------------------------

    return dict(form=form,records=records,page=page,items_per_page=items_per_page,access_permission=access_permission,access_permission_view=access_permission_view)


#-----------------depot settings edit---------------------
def depot_update_settings_validation(form):
    c_id=session.cid
    
    row_id= request.vars.row_id
    
    depot_id=str(form.vars.depot_id).strip().upper().split('|')[0]
    depot_id_from_to=str(form.vars.depot_id_from_to).strip().upper().split('|')[0]
    
    depot_id=check_special_char(depot_id)    
    depot_id_from_to=check_special_char(depot_id_from_to)
    
    depotRows1=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.depot_id,limitby=(0,1))
    if not depotRows1:
        form.errors.depot_id=''
        response.flash = 'Invalid Depot ID/External Source'
    else:
        depotRows2=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id_from_to)).select(db.sm_depot.depot_id,limitby=(0,1))
        if not depotRows2:
            form.errors.depot_id=''
            response.flash = 'Invalid Receive From Depot ID/External Source'
        else:
            if (depot_id==depot_id_from_to):
                form.errors.depot_id=''
                response.flash = 'Depot ID and Receive From can not be same! '
            else:
                if ((depot_id!='') and (depot_id_from_to!='')):
                    rows_check=db((db.sm_depot_settings.id!=row_id) &(db.sm_depot_settings.cid==c_id) & (db.sm_depot_settings.depot_id==depot_id)& (db.sm_depot_settings.depot_id_from_to==depot_id_from_to)).select(db.sm_depot_settings.depot_id,limitby=(0,1))
                    if rows_check:
                        form.errors.depot_id=''
                        response.flash = 'already exist! '
                    else:            
                        form.vars.depot_id=depot_id
                        form.vars.depot_id_from_to=depot_id_from_to

def depot_settings_edit():
    # Check permission
     #----------Task assaign----------
    task_id='rm_depot_setting_manage'
    task_id_view='rm_depot_setting_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL('depot','depot'))
    
    response.title='Depot/Distributor Settings'
    
    #   ---------------------
    c_id=session.cid
    
    page=request.args(0)
    rowID=request.args(1)
    
    record= db.sm_depot_settings(rowID) or redirect(URL('depot_settings'))  
    
#    depotRows=db(db.sm_depot.cid==c_id).select(db.sm_depot.depot_id,db.sm_depot.name,orderby=db.sm_depot.name)
    
#    db.sm_depot_settings.depot_id.requires=IS_IN_DB(db(db.sm_depot.cid==c_id),db.sm_depot.depot_id,orderby=db.sm_depot.depot_id)
    
    form =SQLFORM(db.sm_depot_settings,
                  record=record,
                  deletable=True,
                  fields=['depot_id','depot_id_from_to'],
                  submit_button='Update'
                  )
    
    records_depot=db((db.sm_depot_settings.cid==c_id) & (db.sm_depot_settings.id==rowID)).select(db.sm_depot_settings.depot_id,db.sm_depot_settings.depot_id_from_to,limitby=(0,1))
    depot_id=''
    depot_id_from_to=''
    for records_show_id in records_depot :
         depot_id=records_show_id.depot_id 
         depot_id_from_to=records_show_id.depot_id_from_to
         break
    
    #Update depot with validation
    if form.accepts(request.vars, session,onvalidation=depot_update_settings_validation):
        response.flash = 'Updated Successfully'        
        redirect(URL('depot_settings',args=[page]))
        
    return dict(form=form,depot_id=depot_id,depot_id_from_to=depot_id_from_to,page=page,rowID=rowID,access_permission=access_permission,access_permission_view=access_permission_view)


def depot_settings_batch_upload():
   #----------Task assaign----------
    task_id='rm_depot_setting_manage'
    access_permission=check_role(task_id)
    if (access_permission==False):
        session.flash='Access is Denied !'
        redirect (URL('depot','depot'))
        
    #   --------------------- 
    response.title='Depot/Distributor Settings Batch upload'
    c_id=session.cid
    
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
            
        depotid_list_excel=[]
        valid_depotid_list=[]   
             
        from_depotid_list_excel=[]
        valid_from_depotid_list=[]
        
        exist_depotid_list=[]
        
        excelDepotList=[]
        
        
        ins_list=[]
        ins_dict={}

        #---------- create depot list based on excel sheet
        for i in range(total_row):
            if i>=30:
                break
            else:
                row_data=row_list[i]                    
                coloum_list=row_data.split( '\t')
                if len(coloum_list)==2:
                    depotid_list_excel.append(str(coloum_list[0]).strip().upper())
                    from_depotid_list_excel.append(str(coloum_list[1]).strip().upper())
        
#       To Check valid depot
        validDepotRows=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id.belongs(depotid_list_excel))).select(db.sm_depot.depot_id,orderby=db.sm_depot.depot_id)
        valid_depotid_list=validDepotRows.as_list()
        
#       To Check valid from depot
        validFromDepotRows=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id.belongs(from_depotid_list_excel))).select(db.sm_depot.depot_id,orderby=db.sm_depot.depot_id)
        valid_from_depotid_list=validFromDepotRows.as_list()
        
#       To Check already exist
        existRows=db((db.sm_depot_settings.cid==c_id) & (db.sm_depot_settings.depot_id.belongs(depotid_list_excel))).select(db.sm_depot_settings.depot_id,db.sm_depot_settings.depot_id_from_to,orderby=db.sm_depot_settings.depot_id)
        exist_depotid_list=existRows.as_list()
        
        #   --------------------  main loop   
        for i in range(total_row):
            if i>=30: 
                break
            else:
                row_data=row_list[i]
            coloum_list=row_data.split( '\t')            
            
            if len(coloum_list)==2:
                depot_id=str(coloum_list[0]).strip().upper()
                from_depotid=str(coloum_list[1]).strip().upper()
                
                if (depot_id!='' and from_depotid!=''):
                    try:
                        valid_dpt_flag=False
                        valid_fromdpt_flag=False
                        duplicate_depot=False
                        
                        #Check valid depot                          
                        for i in range(len(valid_depotid_list)):
                            myRowData=valid_depotid_list[i]                                
                            depotID=myRowData['depot_id']
                            if (str(depotID).strip()==str(depot_id).strip()):
                                valid_dpt_flag=True
                                break
                        
                        if valid_dpt_flag==True:                                                                         
                            for i in range(len(valid_from_depotid_list)):
                                myRowData=valid_from_depotid_list[i]                                
                                depotId=myRowData['depot_id']
                                if (str(depotId).strip()==str(from_depotid).strip()):
                                    valid_fromdpt_flag=True                                
                                    break
                        
                            #-----------------
                            if valid_fromdpt_flag==True:
                                for i in range(len(exist_depotid_list)):
                                    myRowData=exist_depotid_list[i]                                
                                    depotID=myRowData['depot_id']
                                    fromDepotID=myRowData['depot_id_from_to']
                                    if (str(depotID).strip()==str(depot_id).strip() and str(fromDepotID).strip()==str(from_depotid).strip()):
                                        duplicate_depot=True
                                        break
                                
                                #-----------------
                                if duplicate_depot==False:
                                    tempData=depot_id+'|'+from_depotid
                                    if tempData not in excelDepotList:
                                        excelDepotList.append(tempData)
                                        #Create insert list
                                        ins_dict= {'cid':c_id,'depot_id':depot_id,'from_to_type':'Receive','depot_id_from_to':from_depotid}
                                        ins_list.append(ins_dict)                               
                                        count_inserted+=1
                                    
                                    else:
                                        error_data=row_data+'(duplicate in excel)\n'
                                        error_str=error_str+error_data
                                        count_error+=1
                                        continue
                                else:
                                    error_data=row_data+'(already exist)\n'
                                    error_str=error_str+error_data
                                    count_error+=1
                                    continue                            
                            else:
                                error_data=row_data+'(Invalid from Depot)\n'
                                error_str=error_str+error_data
                                count_error+=1
                                continue
                        else:
                            error_data=row_data+'(Invalid Depot/Distributor)\n'
                            error_str=error_str+error_data
                            count_error+=1
                            continue                       
                    except:
                        error_data=row_data+'(error in process)\n'
                        error_str=error_str+error_data
                        count_error+=1
                        continue
                else:
                    error_data=row_data+'(all value needed)\n'
                    error_str=error_str+error_data
                    count_error+=1
                    continue
            else:
                error_data=row_data+'(2 columns need in a row)\n'
                error_str=error_str+error_data
                count_error+=1
                continue
        
        if error_str=='':
            error_str='No error'
        
        # bulk insert 
        if len(ins_list) > 0:
            inCountList=db.sm_depot_settings.bulk_insert(ins_list)
            
        return dict(count_inserted=count_inserted,count_error=count_error,error_str=error_str,total_row=total_row)        
        
    return dict(count_inserted=count_inserted,count_error=count_error,error_str=error_str,total_row=total_row)
    
#------------------end----------------------

#============================ Sub depot list
def sub_depot_list():
    c_id=session.cid
    response.title='Sub-Dealer List'
    #----------Task assaign----------
    if (c_id=='' or c_id==None):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))
        
    #--------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=500#session.items_per_page
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #--------end paging
    
    fromDepot=request.vars.fromDepot
    
    records=''
    depotRecords=''
    if not(fromDepot==None or fromDepot==''):
        searchValue=str(fromDepot).split('|')[0]        
        records=db((db.sm_depot_settings.cid==c_id) & (db.sm_depot_settings.depot_id_from_to==searchValue)& (db.sm_depot_settings.from_to_type=='Receive')&(db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==db.sm_depot_settings.depot_id)).select(db.sm_depot_settings.depot_id,db.sm_depot.name,orderby=db.sm_depot_settings.depot_id,limitby=limitby)
    
    #------------
    return dict(records=records,fromDepot=fromDepot,page=page,items_per_page=items_per_page)
    
#============================ preview sub depot list
def preview_sub_depot_list():
    c_id=session.cid
    response.title='Preview Sub-Dealer List'
    if (c_id=='' or c_id==None):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))
        
    fromDepot=request.vars.fromDepot
    
    records=''
    depotRecords=''
    if not(fromDepot==None or fromDepot==''):
        searchValue=str(fromDepot).split('|')[0]
        records=db((db.sm_depot_settings.cid==c_id) & (db.sm_depot_settings.depot_id_from_to==searchValue)& (db.sm_depot_settings.from_to_type=='Receive')&(db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==db.sm_depot_settings.depot_id)).select(db.sm_depot_settings.depot_id,db.sm_depot.name,orderby=db.sm_depot_settings.depot_id)
        
    #------------
    return dict(records=records,fromDepot=fromDepot)
    

##====== PRIMARY SALE HOME

def depot_stock_requisition_list():
   #----------Task assaign----------
    task_id='rm_requisition_manage'
    task_id_view='rm_requisition_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))       
#   --------------------- 
    response.title='Depot Stock Requisition'
    
    c_id=session.cid
    
    #  Set text for filter
    btn_filter_req=request.vars.btn_filter
    btn_all=request.vars.btn_all
    depot_id_value=str(request.vars.depot_id_value).strip()
    search_type=str(request.vars.search_type).strip()
    search_value=str(request.vars.search_value).strip()
    
    reqPage=len(request.args)
    
    if btn_filter_req:
        session.btn_filter_req=btn_filter_req
        session.depot_id_value_req=depot_id_value 
        session.search_type_req=search_type
        session.search_value_req=search_value
        
        # Check sl is integer or not
        if (session.search_type_req=='SL'):
            sl=0
            if not(session.search_value_req=='' or session.search_value_req==None):
                try:       
                    sl=int(session.search_value_req)
                    session.search_value_req=sl
                except:
                    session.search_value_req=sl
                    response.flash='sl needs number value'
            else:
                session.search_value_req=sl
                
        reqPage=0
        
    elif btn_all:
        session.btn_filter_req=None
        session.depot_id_value_req=None
        session.search_type_req=None
        session.search_value_req=None
        reqPage=0
    
    #--------paging
    if reqPage:
        page=int(request.args[0])
    else:
        page=0
    items_per_page=session.items_per_page*10
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #--------end paging  
    
    qset=db()
    qset=qset(db.sm_requisition_head.cid==c_id)
    
    if (session.user_type=='Depot'):
        qset=qset(db.sm_requisition_head.depot_id==session.depot_id)
        
    # set query by search type    
    if (session.btn_filter_req):        
        if (session.user_type!='Depot'):
            if not (session.depot_id_value_req=='' or session.depot_id_value_req==None):
                searchValue=str(session.depot_id_value_req).split('|')[0]
                qset=qset(db.sm_requisition_head.depot_id==searchValue)
            else:
                qset=qset(db.sm_requisition_head.depot_id!='')        
        
        #------------
        if (session.search_type_req=='SL'):
            qset=qset(db.sm_requisition_head.sl==session.search_value_req)
            
        elif (session.search_type_req=='DATE'):
            qset=qset(db.sm_requisition_head.req_date==session.search_value_req)
            
        elif (session.search_type_req=='STATUS'):
            qset=qset(db.sm_requisition_head.status==session.search_value_req)
            
        elif (session.search_type_req=='RequisitionTo'):
            qset=qset(db.sm_requisition_head.requisition_to==session.search_value_req)
            
        elif (session.search_type_req=='UserID'):
            qset=qset(db.sm_requisition_head.updated_by==session.search_value_req.upper())
            
    #-------------        
    records=qset.select(db.sm_requisition_head.ALL,orderby=~db.sm_requisition_head.id,limitby=limitby)
    
    #----------------------------------------
    search_form =SQLFORM(db.sm_search_date)
    
    #-------------
    
    return dict(records=records,search_form=search_form,page=page,items_per_page=items_per_page,access_permission=access_permission,access_permission_view=access_permission_view)

#======================= Stock Requisition 
def validation_requisition(form):#Validation for depot_stock_requisition
    c_id=session.cid   
    
    depot_id=str(form.vars.depot_id).strip().split('|')[0]    
    depot_name=str(form.vars.depot_id).strip().split('|')[1]
    
    requisition_to=str(form.vars.requisition_to).strip().split('|')[0]
    depot_to_name=str(form.vars.requisition_to).strip().split('|')[1]
    
    sl=int(form.vars.sl)
    ym_date=str(form.vars.req_date)[0:7]+'-01'
    
    item_id=form.vars.item_id
    item_name=form.vars.item_name
    quantity=form.vars.quantity
    dist_rate=0#form.vars.dist_rate
    short_note=''#form.vars.short_note
    
    
    if depot_id=='' or depot_id==None:
        form.errors.quantity=''
        response.flash='Select Requisition To'
    else:
        if item_id=='' or item_id==None:
            form.errors.quantity=''
            response.flash='Select Item'
        else:            
            itemRow=db((db.sm_item.cid==c_id) & (db.sm_item.item_id==item_id)).select(db.sm_item.id,db.sm_item.price,limitby=(0,1))
            if not itemRow:
                form.errors.quantity=''
                response.flash='Invalid Item'
            else:
                dist_rate=itemRow[0].price
                
                existRecords=db((db.sm_requisition.cid==c_id) & (db.sm_requisition.depot_id==depot_id)& (db.sm_requisition.sl==sl)& (db.sm_requisition.item_id==item_id)).select(db.sm_requisition.id,db.sm_requisition.sl,limitby=(0,1))
                if existRecords:
                    existRecords[0].update_record(item_name=item_name,quantity=quantity,dist_rate=dist_rate,short_note=short_note)        
                    form.errors.short_note=''  
                    response.flash='Item replaced!'      
                
                elif int(form.vars.quantity)<=0:
                    form.errors.quantity=''
                    response.flash='need item quantity!'
                
                else:
                    if sl==0:
                        maxSl=1
                        records=db((db.sm_depot.cid==c_id) & (db.sm_depot.depot_id==depot_id)).select(db.sm_depot.id,db.sm_depot.requisition_sl,limitby=(0,1))
                        if records:
                            sl=records[0].requisition_sl
                            maxSl=int(sl)+1
                            
                        #----------- UPDATE SL IN DEPOT
                        records[0].update_record(requisition_sl=maxSl)
                        
                        form.vars.sl=maxSl
                        
    #                 depot_to_name=''
    #                 dptRecords=db((db.sm_depot.cid==c_id) & (db.sm_depot.depot_id==requisition_to)).select(db.sm_depot.name,limitby=(0,1))
    #                 if dptRecords:
    #                     depot_to_name=dptRecords[0].name
                    
                    form.vars.ym_date=ym_date
                    form.vars.depot_id=depot_id
                    form.vars.depot_name=depot_name
                    form.vars.requisition_to=requisition_to
                    form.vars.depot_to_name=depot_to_name
                    form.vars.dist_rate=dist_rate #used as tp rate
                    
def depot_stock_requisition():
    task_id='rm_requisition_manage'
    task_id_view='rm_requisition_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))      
    
    response.title='Depot Stock Requisition'
    #   --------------------- 
    c_id=session.cid
    #------------------- variable for batch upload
    count_inserted=request.vars.count_inserted
    count_error=request.vars.count_error
    error_str=request.vars.error_str
    total_row=request.vars.total_row
    
    #------------------
    btn_update=request.vars.btn_update
    btn_batch_upload=request.vars.btn_batch_upload
    
    #------------------ UPDATE BUTTON
    if btn_update:
        req_depot_id=str(request.vars.depot_id).split('|')[0]        
        reqSl=request.vars.sl
        req_to=str(request.vars.requisition_to).split('|')[0]
        req_date=request.vars.req_date        
        ym_date=str(req_date)[0:7]+'-01'        
        req_note=request.vars.note        
        if req_to!='':
            db((db.sm_requisition_head.cid==c_id)& (db.sm_requisition_head.depot_id==req_depot_id) & (db.sm_requisition_head.sl==reqSl)).update(requisition_to=req_to,req_date=req_date,note=req_note,ym_date=ym_date)
            db((db.sm_requisition.cid==c_id)& (db.sm_requisition.depot_id==req_depot_id) & (db.sm_requisition.sl==reqSl)).update(requisition_to=req_to,req_date=req_date,note=req_note,ym_date=ym_date)
            redirect(URL(c='depot',f='depot_stock_requisition',vars=dict(req_sl=reqSl)))
    
    #------------------ BATCH UPLOAD
    elif (btn_batch_upload and str(request.vars.input_data)!='' and int(request.vars.sl)> 0):
        #--------- existing
        req_depot_id=str(request.vars.depot_id).split('|')[0]
        reqSl=request.vars.sl
        req_to=str(request.vars.requisition_to).split('|')[0]
        req_date=request.vars.req_date
        ym_date=str(req_date)[0:7]+'-01'  #Always saved on first date of month
        req_note=request.vars.note
        
        depot_name=''
        depotRecords=db((db.sm_depot.cid==c_id) & (db.sm_depot.depot_id==req_depot_id)).select(db.sm_depot.name,limitby=(0,1))
        if depotRecords:
            depot_name=depotRecords[0].name
        
        depot_to_name=''
        issueToRecords=db((db.sm_depot.cid==c_id) & (db.sm_depot.depot_id==req_to)).select(db.sm_depot.name,limitby=(0,1))
        if issueToRecords:
            depot_to_name=issueToRecords[0].name
        
        #----------- variable declaration
        count_inserted=0
        count_error=0
        error_str=''
        total_row=0

        item_list=[]
        item_list_table=[]
        item_exist_table=[]
        
        excelList=[]
        
        ins_dict={}
        ins_list=[]
        
        headFlag=False
       #---------
        input_data=str(request.vars.input_data)
        inserted_count=0
        error_count=0
        error_list=[]
        row_list=input_data.split( '\n')
        total_row=len(row_list)
        
        #   ---------------------- valid item list loop
        for i in range(total_row):
            if i>=30:
                break
            else:
                row_data=row_list[i]                    
                coloum_list=row_data.split( '\t')
                if len(coloum_list)==2:
                    item_list.append(str(coloum_list[0]).strip().upper())
                    
        #Create list from item table
        itemRows=db((db.sm_item.cid==c_id)&(db.sm_item.item_id.belongs(item_list))).select(db.sm_item.item_id,db.sm_item.name,db.sm_item.dist_price,db.sm_item.price,orderby=db.sm_item.item_id)
        item_list_table=itemRows.as_list()
        #Creatre list from excel sheet that already exist in database
        existRecords=db((db.sm_requisition.cid==c_id) & (db.sm_requisition.depot_id==req_depot_id)& (db.sm_requisition.sl==reqSl)& (db.sm_requisition.item_id.belongs(item_list))).select(db.sm_requisition.item_id)
        item_exist_table=existRecords.as_list()
        
        #   --------------------  excel main loop
        for i in range(total_row):
            if i>=30: 
                break
            else:
                row_data=row_list[i]        
                coloum_list=row_data.split( '\t')            
            
            if len(coloum_list)==2:
                item_id_value=str(coloum_list[0]).strip().upper()
                item_qty_value=coloum_list[1]
                
                try:                
                    #----------- check valid item
                    name=''
                    dist_price=0    #used as tp rate
                    valid_item=False  
                    #Check item valid or not
                    if len(item_list_table) > 0:
                        for i in range(len(item_list_table)):
                            myRowData=item_list_table[i]                                
                            item_id=myRowData['item_id']
                            name=myRowData['name']
                            #dist_price=myRowData['dist_price']
                            dist_price=myRowData['price']
                            if (str(item_id).strip()==str(item_id_value).strip()):
                                valid_item=True
                                break
                                
                    #-----------------
                    # Check item in item_exist_table for duplicate
                    if valid_item==True:#----------- check duplicate                       
                        duplicate_item=False  
                        if len(item_exist_table) > 0:
                            for j in range(len(item_exist_table)):
                                myRowData=item_exist_table[j]                                
                                item_id=myRowData['item_id']
                                if (str(item_id).strip()==str(item_id_value).strip()):
                                    duplicate_item=True
                                    break
                        #-----------------
                    
                    if int(item_qty_value) > 0:
                        if (valid_item==True):
                            if(duplicate_item==False):                                
                                if item_id_value not in excelList:
                                    #Check duplicate in excel sheet
                                    excelList.append(item_id_value)
                                    
                                    ins_dict= {'cid':c_id,'depot_id':req_depot_id,'depot_name':depot_name,'sl':reqSl,'requisition_to':req_to,'depot_to_name':depot_to_name,'req_date':req_date,'note':req_note,
                                           'item_id':item_id_value,'item_name':name,'quantity':item_qty_value,'dist_rate':dist_price,'ym_date':ym_date}
                                    ins_list.append(ins_dict)                               
    
                                    count_inserted+=1                                    
                                else:
                                    error_data=row_data+'(duplicate in excel!)\n'
                                    error_str=error_str+error_data
                                    count_error+=1
                                    continue 
                                
                            else:
                                error_data=row_data+'(duplicate item)\n'
                                error_str=error_str+error_data
                                count_error+=1
                                continue
                                
                        else:
                            error_data=row_data+'(Invalid Item)\n'
                            error_str=error_str+error_data
                            count_error+=1
                            continue

                    else:
                        error_data=row_data+'(need quantity)\n'
                        error_str=error_str+error_data
                        count_error+=1
                        continue

                except:
                    error_data=row_data+'(process error)\n'
                    error_str=error_str+error_data
                    count_error+=1
                    continue
            else:
                error_data=row_data+'(2 columns need in a row)\n'
                error_str=error_str+error_data
                count_error+=1
                continue
        
        if error_str=='':
            error_str='No error'
        
        # Bulk insert
        inCountList=db.sm_requisition.bulk_insert(ins_list)             
        
        redirect(URL('depot_stock_requisition',vars=dict(req_sl=reqSl,count_inserted=count_inserted,count_error=count_error,error_str=error_str,total_row=total_row)))
        
    #------------------ SAVE ITEM/REPLACE IF EXIST
    form =SQLFORM(db.sm_requisition,
                  fields=['depot_id','sl','requisition_to','req_date','status','req_process_status','item_id','item_name','quantity','note'],
                  submit_button='Save'   
                  )
    form.vars.cid=c_id
    form.vars.quantity=''
    # Insert requisition with validation
    if form.accepts(request.vars,session,onvalidation=validation_requisition):
       sl=form.vars.sl
       depot_id=form.vars.depot_id
       depot_name=form.vars.depot_name
       requisition_to=form.vars.requisition_to
       depot_to_name=form.vars.depot_to_name
       req_date=form.vars.req_date
       ym_date=str(req_date)[0:7]+'-01'
       note=form.vars.note      
       
       #---Requisition Head Insert/Update
       headRows=db((db.sm_requisition_head.cid==c_id)& (db.sm_requisition_head.depot_id==depot_id) & (db.sm_requisition_head.sl==sl)).select(db.sm_requisition_head.id,db.sm_requisition_head.depot_id,limitby=(0,1))
       if headRows:
            headRows[0].update_record(requisition_to=requisition_to,depot_to_name=depot_to_name,req_date=req_date,note=note,ym_date=ym_date)
       else:
           db.sm_requisition_head.insert(cid=c_id,depot_id=depot_id,depot_name=depot_name,sl=sl,requisition_to=requisition_to,depot_to_name=depot_to_name,req_date=req_date,ym_date=ym_date,note=note)
       
       #------------- UPDATE SAME SL DATA
       db((db.sm_requisition.cid==c_id)& (db.sm_requisition.depot_id==depot_id) & (db.sm_requisition.sl==sl)).update(requisition_to=requisition_to,depot_to_name=depot_to_name,req_date=req_date,note=note,ym_date=ym_date)
       
       redirect(URL(c='depot',f='depot_stock_requisition',vars=dict(req_sl=sl)))
    
    #------------------ NEW REQUISITION/ SHOW VALUE IF ALREADY CREATED
    depot_name=''
    requisition_to_name=''
    
    req_sl=request.vars.req_sl    
    depotid=request.vars.depotid 
    if depotid=='' or depotid==None:
        depot_id=session.depot_id
        depot_name=session.user_depot_name
    else:
        depot_id=depotid # Depot ID
    
    
    sl=0
    status='Draft'
    req_process_status='Requisition'
    requisition_to=''
    req_date=current_date
    note='' 
    
    records=db((db.sm_requisition.cid==c_id)& (db.sm_requisition.depot_id==depot_id) & (db.sm_requisition.sl==req_sl)).select(db.sm_requisition.ALL,orderby=db.sm_requisition.item_name)
    for rec in records:
        depot_id=rec.depot_id
        depot_name=rec.depot_name
        sl=rec.sl
        status=rec.status
        req_process_status=rec.req_process_status
        requisition_to=rec.requisition_to
        requisition_to_name=rec.depot_to_name
        req_date=rec.req_date
        note=rec.note
        break    
    
    #------------------ DEPOT IN COMBO
    reqRecords=''
    # if requisition_to=='':
    #     #reqRecords=db((db.sm_depot_settings.cid==c_id) & (db.sm_depot_settings.depot_id==session.depot_id)& (db.sm_depot_settings.from_to_type=='Receive')&(db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==db.sm_depot_settings.depot_id_from_to)).select(db.sm_depot.name,db.sm_depot_settings.depot_id_from_to,orderby=db.sm_depot_settings.depot_id_from_to)
    #     reqRecords=db((db.sm_depot.cid==c_id) & (db.sm_depot.depot_id!=session.depot_id)).select(db.sm_depot.depot_id,db.sm_depot.name,orderby=db.sm_depot.name)
        
    #-------------------
    return dict(form=form,reqRecords=reqRecords,records=records,depot_id=depot_id,depot_name=depot_name,sl=sl,requisition_to=requisition_to,requisition_to_name=requisition_to_name,req_date=req_date,status=status,req_process_status=req_process_status,note=note,
                count_inserted=count_inserted,count_error=count_error,error_str=error_str,total_row=total_row,access_permission=access_permission,access_permission_view=access_permission_view)
    
#------------------ get Item List
#Used for item auto complete--called at home link
def get_item():    
    records=db(db.sm_item.cid==session.cid).select(db.sm_item.id,db.sm_item.item_id,db.sm_item.name,db.sm_item.dist_price,db.sm_item.category_id,orderby=db.sm_item.name)
    return dict(records=records)

#=================== Delete item
#If more than one item in requisition list, item canbe delete
def delete_requisition_item():
    c_id=session.cid
    
    btn_delete=request.vars.btn_delete
    
    req_depot=request.args(0)
    req_sl=request.args(1)    
    req_item=request.args(2)
    
    if btn_delete:
        countRecords=db((db.sm_requisition.cid==c_id)& (db.sm_requisition.depot_id==req_depot) & (db.sm_requisition.sl==req_sl)).count()
        if int(countRecords)==1:
            session.flash='At least one item needs in a requisition, You can cancel if required!'
        else:
            db((db.sm_requisition.cid==c_id) & (db.sm_requisition.depot_id==req_depot) & (db.sm_requisition.sl==req_sl)& (db.sm_requisition.item_id==req_item)).delete()
            
        redirect(URL(c='depot',f='depot_stock_requisition',vars=dict(req_sl=req_sl)))
    #  ---------------------
    return dict()

#=================== Post and Cancel


#Update status field as posted or cancel
def post_cancel_requisition():
    c_id=session.cid
    
    btn_post=request.vars.btn_post
    btn_cancel=request.vars.btn_cancel
    
    req_depot=request.args(0)
    req_sl=request.args(1)
    req_date=request.args(2)    
    ym_date=str(req_date)[0:7]+'-01'
    
    if btn_post:
        countRecords=db((db.sm_requisition.cid==c_id)& (db.sm_requisition.depot_id==req_depot) & (db.sm_requisition.sl==req_sl)).count()
        if int(countRecords)==0:
            session.flash='At least one item needs in a requisition!'
        else:
            db((db.sm_requisition_head.cid==c_id)& (db.sm_requisition_head.depot_id==req_depot) & (db.sm_requisition_head.sl==req_sl)).update(status='Posted')
            db((db.sm_requisition.cid==c_id)& (db.sm_requisition.depot_id==req_depot) & (db.sm_requisition.sl==req_sl)).update(status='Posted')
            session.flash='Posted successfully!'
            
        redirect(URL(c='depot',f='depot_stock_requisition',vars=dict(req_sl=req_sl)))
        
    elif btn_cancel:
        countRecords=db((db.sm_requisition.cid==c_id)& (db.sm_requisition.depot_id==req_depot) & (db.sm_requisition.sl==req_sl)).count()
        if int(countRecords)==0:
            session.flash='At least one item needs in a requisition!'
        else:
            db((db.sm_requisition_head.cid==c_id)& (db.sm_requisition_head.depot_id==req_depot) & (db.sm_requisition_head.sl==req_sl)).update(status='Cancelled')
            db((db.sm_requisition.cid==c_id)& (db.sm_requisition.depot_id==req_depot) & (db.sm_requisition.sl==req_sl)).update(status='Cancelled')
            session.flash='Cancelled successfully!'
            
        redirect(URL(c='depot',f='depot_stock_requisition',vars=dict(req_sl=req_sl)))
        
    return dict()


#==============================Not used
def item_selector():#Not used
    c_id=session.cid
    txt_item= str(request.vars.txt_item).upper()

    selected=[]
            #--------------------------
    rows=db(db.sm_item.cid==c_id).select(db.sm_item.item_id,db.sm_item.name,db.sm_item.dist_price,orderby=db.sm_item.name)
    for row in rows:
        item_id=str(row.item_id).replace('|', ' ')
        name=str(row.name).replace('|', ' ')
        dist_price=row.dist_price
        
        temp=name+item_id
        temp=temp.upper()
        
        if (temp.find(txt_item)== (-1)):
            continue
        else:
            data=name+'|'+item_id+'|'+str(dist_price)
            selected.append(data)
            if len(selected)==100:
                break
            
        #----------------       

    return ''.join([DIV(k,
                 _onclick="jQuery('#txt_item').val('%s')" % k ,
                 _onmouseover="this.style.backgroundColor='yellow'",
                 _onmouseout="this.style.backgroundColor='white'"
                 ).xml() for k in selected])


#=========================================== Issue List

#---------------catagory-----------------------
def validation_issue_reference(form):    
    category_id=str(request.vars.cat_type_id).strip().title()
    if category_id!='':
        rows_check=db((db.sm_category_type.cid==session.cid) & (db.sm_category_type.type_name=='ISSUE_CAUSE') &(db.sm_category_type.cat_type_id==category_id)).select(db.sm_category_type.cat_type_id,limitby=(0,1))
        if rows_check:
            form.errors.cat_type_id=''
            response.flash = 'Already exist, Please choose a new'
        else:
            form.vars.cid=session.cid
            form.vars.type_name='ISSUE_CAUSE'
            form.vars.cat_type_id=category_id
def issue_reference():    
    task_id='rm_utility_manage'
    access_permission=check_role(task_id)
    if (access_permission==False and session.user_type=="Admin"):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))
        
    response.title='Transfer Note Cause'
    
    cid=session.cid
    
    #---------------------
    form =SQLFORM(db.sm_category_type,
                  fields=['cat_type_id'],
                  submit_button='Save'
                  )
    
    if form.accepts(request.vars,session,onvalidation=validation_issue_reference):
        response.flash = 'Saved Successfully'
        
    #--------------------------------
    btn_delete=request.vars.btn_delete
    if btn_delete:
        record_id=request.args[1]
        category_id=''
        catRow=db((db.sm_category_type.cid == cid)&(db.sm_category_type.id==record_id)&(db.sm_category_type.type_name=='ISSUE_CAUSE')).select(db.sm_category_type.cat_type_id,limitby=(0,1))
        if not catRow:
            response.flash='Invalid request'
        else:
            category_id=catRow[0].cat_type_id
            
            records=db((db.sm_issue_head.cid==cid) & (db.sm_issue_head.transaction_cause==category_id)).select(db.sm_issue_head.transaction_cause,limitby=(0,1))
            if records:
                response.flash='Already used in Transfer Note'            
            else:
                db((db.sm_category_type.cid == cid)&(db.sm_category_type.id == record_id)&(db.sm_category_type.type_name=='ISSUE_CAUSE')).delete()
                response.flash='Deleted successfully'
    
    #--------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=session.items_per_page
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #--------end paging
    
    records=db((db.sm_category_type.cid==cid)&(db.sm_category_type.type_name=='ISSUE_CAUSE')).select(db.sm_category_type.ALL,orderby=db.sm_category_type.cat_type_id,limitby=limitby)
    
    return dict(form=form,records=records,page=page,items_per_page=items_per_page,access_permission=access_permission)
#---------------

def depot_stock_issue_list():
    #----------Task assaign----------
    task_id='rm_stock_issue_manage'
    task_id_view='rm_stock_issue_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))   
        
    #return access_permission
    #   ---------------------
    response.title='Transfer List(Branch To Branch)'
    c_id=session.cid
    
    #  Set text for filter    
    btn_filter_issue=request.vars.btn_filter_issue
    btn_all=request.vars.btn_all
    depot_id_value=str(request.vars.depot_id_value).strip()
    search_type=str(request.vars.search_type).strip()
    search_value=str(request.vars.search_value).strip()
    
    reqPage=len(request.args)
    # set session for filter
    if btn_filter_issue:
        session.btn_filter_issue=btn_filter_issue
        session.depot_id_value_issue=depot_id_value 
        session.search_type_issue=search_type
        session.search_value_issue=search_value
        # Check sl is integer or not
        if (session.search_type_issue=='SL'):
            sl=0
            if not(session.search_value_issue=='' or session.search_value_issue==None):
                try:       
                    sl=int(session.search_value_issue)
                    session.search_value_issue=sl
                except:
                    session.search_value_issue=sl
                    response.flash='sl needs number value'
            else:
                session.search_value_issue=sl
                
        reqPage=0
        
    elif btn_all:
        session.btn_filter_issue=None
        session.depot_id_value_issue=None
        session.search_type_issue=None
        session.search_value_issue=None
        reqPage=0
        
    #--------paging
    if reqPage:
        page=int(request.args[0])
    else:
        page=0
    items_per_page=session.items_per_page*10
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #--------end paging  
    
    qset=db()
    qset=qset(db.sm_issue_head.cid==c_id)
    
    if (session.user_type=='Depot'):
        qset=qset(db.sm_issue_head.depot_id==session.depot_id)
    # Set filter type. Create select sql based on search type    
    if (session.btn_filter_issue):
        
        if (session.user_type!='Depot'):
            if not (session.depot_id_value_issue=='' or session.depot_id_value_issue==None):
                searchValue=str(session.depot_id_value_issue).split('|')[0]
                qset=qset(db.sm_issue_head.depot_id==searchValue)
            else:
                qset=qset(db.sm_issue_head.depot_id!='')
        
        #------------
        if (session.search_type_issue=='SL'):
            qset=qset(db.sm_issue_head.sl==session.search_value_issue)
        
        elif (session.search_type_issue=='DATE'):
            qset=qset(db.sm_issue_head.issue_date==session.search_value_issue)
        
        elif (session.search_type_issue=='STATUS'):
            qset=qset(db.sm_issue_head.status==session.search_value_issue)
            
        elif (session.search_type_issue=='IssueTo'):
            search_value_issue=str(session.search_value_issue).split('|')[0]
            qset=qset(db.sm_issue_head.issued_to==search_value_issue)
            
        elif (session.search_type_issue=='UserID'):
            search_value_issue=str(session.search_value_issue).upper()
            qset=qset(db.sm_issue_head.updated_by==search_value_issue)
        
        
        #------------
    records=qset.select(db.sm_issue_head.ALL,orderby=~db.sm_issue_head.id,limitby=limitby)
    
    #------------------------------------------------
    search_form =SQLFORM(db.sm_search_date)
    #-------------
    
    return dict(search_form=search_form,records=records,page=page,items_per_page=items_per_page,access_permission=access_permission,access_permission_view=access_permission_view)


#======================= Stock Issue 

#Validation for stock issue
def process_issue(form):
    c_id=session.cid
    
    depot_id=str(form.vars.depot_id).split('|')[0]
    depot_name=str(form.vars.depot_id).split('|')[1]
    
    store_idname=str(form.vars.store_id)
    
    issued_to=str(form.vars.issued_to).split('|')[0]
    depot_to_name=str(form.vars.issued_to).split('|')[1]    
    issued_to=str(issued_to).strip()
    depot_to_name=str(depot_to_name).strip()
    
    transaction_cause=str(form.vars.transaction_cause)
    
    item_id=str(request.vars.item_details).split('|')[1]
    item_name=str(request.vars.item_details).split('|')[0]
    
    quantity=form.vars.quantity
    bonus_qty=0 #form.vars.bonus_qty
    dist_rate=0#form.vars.dist_rate    #used as TP rate
    short_note=''#form.vars.short_note
    
    batch_id=str(request.vars.batch_id).split('|')[0]
    
    if store_idname=='':
        form.errors.store_id=''
        response.flash="Required From Store/Location"
    else:
        store_id=str(store_idname).split('|')[0]
        store_name=str(store_idname).split('|')[1]
        
        if issued_to=='':
            form.errors.issued_to=''
            response.flash="Required issued to"
        else:
            itemRows = db((db.sm_item.cid == c_id)&(db.sm_item.item_id == item_id)).select(db.sm_item.name,db.sm_item.price,db.sm_item.unit_type,db.sm_item.item_carton, limitby=(0,1))
            if not itemRows:
                form.errors.item_id=''
                response.flash="Invalid Item ID"
            else:                
                dist_rate=itemRows[0].price
                unit_type=itemRows[0].unit_type
                item_carton=itemRows[0].item_carton
                
                itemBatchRows = db((db.sm_item_batch.cid == c_id) & (db.sm_item_batch.item_id == item_id) & (db.sm_item_batch.batch_id == batch_id) & (db.sm_item_batch.expiary_date >= current_date)).select(db.sm_item_batch.item_id,db.sm_item_batch.expiary_date,limitby=(0,1))
                if not itemBatchRows:
                    form.errors.batch_id=''
                    response.flash="Invalid Item Batch ID"
                else:
                    expiary_date=itemBatchRows[0].expiary_date
                    
                    sl=int(form.vars.sl)
                    ym_date=str(form.vars.issue_date)[0:7]+'-01'
                    
                    existRecords=db((db.sm_issue.cid==c_id) & (db.sm_issue.depot_id==depot_id)& (db.sm_issue.sl==sl)& (db.sm_issue.item_id==item_id)& (db.sm_issue.batch_id==batch_id)).select(db.sm_issue.id,db.sm_issue.item_id,limitby=(0,1))
                    if existRecords:
                        existRecords[0].update_record(item_name=item_name,quantity=quantity,bonus_qty=bonus_qty,dist_rate=dist_rate,short_note=short_note)        
                        form.errors.short_note=''  
                        response.flash='Item replaced!'      
                    
                    elif int(quantity)<=0:
                        form.errors.quantity=''
                        response.flash='need item quantity!'
                        
                    else:
                        if sl==0:            
                            maxSl=1
                            records=db((db.sm_depot.cid==c_id) & (db.sm_depot.depot_id==depot_id)).select(db.sm_depot.id,db.sm_depot.issue_sl,limitby=(0,1))
                            if records:
                                issueSl=records[0].issue_sl
                                maxSl=int(issueSl)+1
                            
                            #----------- UPDATE SL IN DEPOT
                            records[0].update_record(issue_sl=maxSl)
                            
                            form.vars.sl=maxSl
                            
                        form.vars.item_id=item_id
                        form.vars.item_name=item_name
                        form.vars.ym_date=ym_date
                        form.vars.depot_id=depot_id
                        form.vars.depot_name=depot_name
                        form.vars.store_id=store_id
                        form.vars.store_name=store_name
                        form.vars.issued_to=issued_to
                        form.vars.depot_to_name=depot_to_name
                        form.vars.batch_id=batch_id
                        form.vars.dist_rate=dist_rate
                        form.vars.transaction_cause=transaction_cause
                        
                        form.vars.item_unit=unit_type
                        form.vars.item_carton=item_carton
                        form.vars.expiary_date=expiary_date
                        
                        ref_sl= request.vars.ref_sl
                        if int(sl)==0:
                            form.vars.req_sl=0
                        else:
                            form.vars.req_sl=ref_sl
                            
def depot_stock_issue():
    #----------Task assaign----------
    task_id='rm_stock_issue_manage'
    task_id_view='rm_stock_issue_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))   
        
    response.title='Transfer(Branch To Branch)'
    #   --------------------- 
    
    c_id=session.cid
    #Set variable for batch upload
    count_inserted=request.vars.count_inserted
    count_error=request.vars.count_error
    error_str=request.vars.error_str
    total_row=request.vars.total_row

    #------------------
    btn_update=request.vars.btn_update
    btn_batch_upload=request.vars.btn_batch_upload
    btn_import_req=request.vars.btn_import_req
    
    #UPDATE issue head
    if btn_update:
        req_depot_id=str(request.vars.depot_id).split('|')[0]
        reqSl=request.vars.sl
        req_to=str(request.vars.issued_to).split('|')[0]
        req_date=request.vars.issue_date
        ym_date=str(req_date)[0:7]+'-01'
        transaction_cause=request.vars.transaction_cause
        
        req_note=request.vars.note 
        total_discount=0#request.vars.total_discount        
        if req_to!='':
            db((db.sm_issue_head.cid==c_id)& (db.sm_issue_head.depot_id==req_depot_id) & (db.sm_issue_head.sl==reqSl)).update(issued_to=req_to,issue_date=req_date,note=req_note,total_discount=total_discount,ym_date=ym_date,transaction_cause=transaction_cause)
            db((db.sm_issue.cid==c_id)& (db.sm_issue.depot_id==req_depot_id) & (db.sm_issue.sl==reqSl)).update(issued_to=req_to,issue_date=req_date,note=req_note,total_discount=total_discount,ym_date=ym_date,transaction_cause=transaction_cause)
            redirect(URL(c='depot',f='depot_stock_issue',vars=dict(req_sl=reqSl)))
            
    # BATCH UPLOAD
    elif (btn_batch_upload and str(request.vars.input_data)!='' and int(request.vars.sl)> 0):
        req_depot_id=str(request.vars.depot_id).split('|')[0]
        
        store_id=str(request.vars.store_id).split('|')[0]
        store_name=str(request.vars.store_id).split('|')[1]
        
        reqSl=request.vars.sl
        req_to=str(request.vars.issued_to).split('|')[0]
        req_date=request.vars.issue_date
        ym_date=str(req_date)[0:7]+'-01'#Save on first date of month
        req_note=request.vars.note
        transaction_cause=request.vars.transaction_cause
        
        depot_name=''
        depotRecords=db((db.sm_depot.cid==c_id) & (db.sm_depot.depot_id==req_depot_id)).select(db.sm_depot.name,limitby=(0,1))
        if depotRecords:
            depot_name=depotRecords[0].name
        
        depot_to_name=''
        issueToRecords=db((db.sm_depot.cid==c_id) & (db.sm_depot.depot_id==req_to)).select(db.sm_depot.name,limitby=(0,1))
        if issueToRecords:
            depot_to_name=issueToRecords[0].name
        
        #----------- variable declaration
        count_inserted=0
        count_error=0
        error_str=''
        total_row=0
        
        item_list=[]
        item_list_table=[]
        item_exist_table=[]
        
        excelList=[]
        
        ins_dict={}
        ins_list=[]
        
       #---------
        input_data=str(request.vars.input_data)
        inserted_count=0
        error_count=0
        error_list=[]
        row_list=input_data.split( '\n')
        total_row=len(row_list)
        
        #   ---------------------- valid item list loop
        for i in range(total_row):
            if i>=30:
                break
            else:
                row_data=row_list[i]                    
                coloum_list=row_data.split( '\t')
                if len(coloum_list)==3:
                    item_list.append(str(coloum_list[0]).strip().upper())
                    
        #Create list from item table
        itemRows=db((db.sm_item.cid==c_id)&(db.sm_item.item_id.belongs(item_list))).select(db.sm_item.item_id,db.sm_item.name,db.sm_item.dist_price,db.sm_item.price,db.sm_item.unit_type,db.sm_item.item_carton,orderby=db.sm_item.name)
        item_list_table=itemRows.as_list()
        
        #Create list based on excel sheet that items are axist in database
        existRecords=db((db.sm_issue.cid==c_id) & (db.sm_issue.depot_id==req_depot_id)& (db.sm_issue.sl==reqSl)& (db.sm_issue.item_id.belongs(item_list))).select(db.sm_issue.item_id)
        item_exist_table=existRecords.as_list()
        
        # --------------------  excel main loop
        for i in range(total_row):
            if i>=30: 
                break
            else:
                row_data=row_list[i]        
                coloum_list=row_data.split( '\t')            
            
            if len(coloum_list)==3:
                try:
                    item_id_value=str(coloum_list[0]).strip().upper()
                    item_qty_value=int(coloum_list[1])
                    item_bonus_qty_value=int(coloum_list[2])
  
                    #----------- check valid item
                    name=''
                    dist_price=0
                    item_unit=''
                    item_carton=0
                    item_expiaryDate=''#not apply need to apply
                    
                    valid_item=False  
                    if len(item_list_table) > 0:
                        for i in range(len(item_list_table)):
                            myRowData=item_list_table[i]                                
                            item_id=myRowData['item_id']
                            name=myRowData['name']
                            #dist_price=myRowData['dist_price']
                            dist_price=myRowData['price']   #used as tp
                            item_unit=myRowData['unit_type']
                            item_carton=myRowData['item_carton']
                            if (str(item_id).strip()==str(item_id_value).strip()):                                
                                valid_item=True
                                break
                                
                    #-----------------
                    if valid_item==True:#----------- check duplicate                       
                        duplicate_item=False  
                        if len(item_exist_table) > 0:
                            for j in range(len(item_exist_table)):
                                myRowData=item_exist_table[j]                                
                                item_id=myRowData['item_id']
                                if (str(item_id).strip()==str(item_id_value).strip()):
                                    duplicate_item=True
                                    break
                        #-----------------
                    
                    if (int(item_qty_value) > 0 and item_bonus_qty_value>=0):
                        if (valid_item==True):
                            if(duplicate_item==False): 
                                #Check duplicate in excel list
                                if item_id_value not in excelList:
                                    excelList.append(item_id_value)
                                    
                                    ins_dict= {'cid':c_id,'depot_id':req_depot_id,'depot_name':depot_name,'sl':reqSl,'store_id':store_id,'store_name':store_name,'issued_to':req_to,'depot_to_name':depot_to_name,'issue_date':req_date,'ym_date':ym_date,'note':req_note,'transaction_cause':transaction_cause,
                                           'item_id':item_id_value,'item_name':name,'quantity':item_qty_value,'bonus_qty':item_bonus_qty_value,'dist_rate':dist_price,'item_unit':item_unit,'item_carton':item_carton,'expiary_date':item_expiaryDate}
                                
                                    ins_list.append(ins_dict)                               
    
                                    count_inserted+=1                        
                                else:
                                    error_data=row_data+'(duplicate in excel!)\n'
                                    error_str=error_str+error_data
                                    count_error+=1
                                    continue
                            
                            else:
                                error_data=row_data+'(duplicate item)\n'
                                error_str=error_str+error_data
                                count_error+=1
                                continue
                                
                        else:
                            error_data=row_data+'(Invalid Item)\n'
                            error_str=error_str+error_data
                            count_error+=1
                            continue

                    else:
                        error_data=row_data+'(need quantity)\n'
                        error_str=error_str+error_data
                        count_error+=1
                        continue

                except:
                    error_data=row_data+'(process error)\n'
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
        #Bulk insert 
        inCountList=db.sm_issue.bulk_insert(ins_list)             
        
        redirect(URL(c='depot',f='depot_stock_issue',vars=dict(req_sl=reqSl,count_inserted=count_inserted,count_error=count_error,error_str=error_str,total_row=total_row)))
    
    #-------------------IMPOT FROM REQUISITION
    elif btn_import_req:
        maxSl=0
        try:
            req_depot_id=str(request.vars.depot_id).split('|')[0]            
            reqSl=int(request.vars.sl)
            
            store_idname=str(request.vars.store_id)
        
            req_to=str(request.vars.issued_to).split('|')[0]
            issue_date=request.vars.issue_date
            ym_date=str(issue_date)[0:7]+'-01'
            req_note=request.vars.note 
            total_discount=0#request.vars.total_discount            
            
            transaction_cause=request.vars.transaction_cause 
            
            try:
                ref_sl=int(request.vars.ref_sl)     
            except:
                ref_sl=0
                
            if reqSl==0 :
                if store_idname!='':
                    store_id=str(store_idname).split('|')[0]
                    store_name=str(store_idname).split('|')[1]
                    
                    if (req_to!='' and issue_date!='' and ref_sl > 0):
                        #------------------- requisition items
                        #Select all atems from requisition table based on sl ,date,req to
                        reqRecords=db((db.sm_requisition.cid==c_id) & (db.sm_requisition.requisition_to==req_depot_id) & (db.sm_requisition.depot_id==req_to)&(db.sm_requisition.sl==ref_sl)&(db.sm_requisition.status=='Posted')&(db.sm_requisition.req_process_status=='Requisition')).select(db.sm_requisition.ALL,orderby=db.sm_requisition.item_name)
                        
                        if reqRecords:
                            maxSl=1
                            records=db((db.sm_depot.cid==c_id) & (db.sm_depot.depot_id==req_depot_id)).select(db.sm_depot.id,db.sm_depot.issue_sl,limitby=(0,1))
                            if records:
                                sl=records[0].issue_sl
                                maxSl=int(sl)+1
                            
                            
                            #Update issue_sl in sm_depot table
                            records[0].update_record(issue_sl=maxSl)
                            
                            #---------------                        
                            reqDict={}
                            insList=[]
                            headFlag=False
                            
                            #Set all records of import req in a list.Insert issue head and detail based on list
                            for row in reqRecords:
                                from_depot=row.depot_id
                                depot_to_name=row.depot_name
                                sl=row.sl
                                requisition_to=row.requisition_to
                                depot_name=row.depot_to_name
                                note=row.note
                                item_id=row.item_id
                                item_name=row.item_name
                                quantity=row.quantity
                                dist_rate=row.dist_rate
                                short_note=row.short_note
                                
                                item_unit=''
                                item_carton=0
                                expiary_date=''
                                
                                reqDict={'cid':c_id,'depot_id':requisition_to,'depot_name':depot_name,'sl':maxSl,'store_id':store_id,'store_name':store_name,'issued_to':from_depot,'depot_to_name':depot_to_name,'issue_date':issue_date,'total_discount':total_discount,'req_sl':ref_sl,'transaction_cause':transaction_cause,
                                         'item_id':item_id,'item_name':item_name,'quantity':quantity,'dist_rate':dist_rate,'item_unit':item_unit,'item_carton':item_carton,'expiary_date':expiary_date,'short_note':short_note,'ym_date':ym_date}
                                insList.append(reqDict)
                                if headFlag==False:
                                    db.sm_issue_head.insert(cid=c_id,depot_id=requisition_to,depot_name=depot_name,sl=maxSl,store_id=store_id,store_name=store_name,req_sl=ref_sl,issued_to=from_depot,depot_to_name=depot_to_name,issue_date=issue_date,total_discount=total_discount,ym_date=ym_date,transaction_cause=transaction_cause)
                                    headFlag=True
                            
                            rows=db.sm_issue.bulk_insert(insList)
                            
                            #Update Status as Issued in requisition table
                            db((db.sm_requisition_head.cid==c_id) & (db.sm_requisition_head.requisition_to==req_depot_id) & (db.sm_requisition_head.depot_id==req_to)&(db.sm_requisition_head.sl==ref_sl)&(db.sm_requisition_head.status=='Posted')).update(req_process_status='Issued')
                            db((db.sm_requisition.cid==c_id) & (db.sm_requisition.requisition_to==req_depot_id) & (db.sm_requisition.depot_id==req_to)&(db.sm_requisition.sl==ref_sl)&(db.sm_requisition.status=='Posted')).update(req_process_status='Issued')
                            
                            session.flash='successfully imported'
                            
                        else:
                            session.flash='Reference not available!'
                    else:
                        session.flash='Issue to,Date and Reference needed!'
                else:
                    session.flash='Required From Store/Location'
            else:
                session.flash='need new issue!'
        except:
            session.flash='process error!'        
        
        if maxSl > 0:
            redirect(URL(c='depot',f='depot_stock_issue',vars=dict(req_sl=maxSl)))
        else:
            redirect(URL(c='depot',f='depot_stock_issue',vars=dict(req_sl=reqSl)))
            
    #-------------------SAVE ITEM/ REPLACES IF EXIST
    form =SQLFORM(db.sm_issue,
                  fields=['depot_id','sl','store_id','issued_to','req_sl','issue_date','transaction_cause','status','issue_process_status','item_id','item_name','batch_id','quantity','dist_rate','note'],
                  submit_button='Save'   
                  )
    #Insert with validation
    form.vars.cid=c_id
    form.vars.quantity=''
    
    if form.accepts(request.vars,session,onvalidation=process_issue):
       sl=form.vars.sl
       depot_id=form.vars.depot_id
       depot_name=form.vars.depot_name
       store_id=form.vars.store_id
       store_name=form.vars.store_name
       
       issued_to=form.vars.issued_to
       depot_to_name=form.vars.depot_to_name
       issue_date=form.vars.issue_date
       ym_date=str(issue_date)[0:7]+'-01'
       note=form.vars.note
       discount=form.vars.total_discount
       
       transaction_cause=form.vars.transaction_cause
       
#       item_id= form.vars.item_id
#       item_name= form.vars.item_name
#       return item_id
       
       #Insert /update sm_issue_head,sm_issue
       headRows=db((db.sm_issue_head.cid==c_id)& (db.sm_issue_head.depot_id==depot_id) & (db.sm_issue_head.sl==sl)).select(db.sm_issue_head.id,db.sm_issue_head.depot_id,limitby=(0,1))
       if headRows:
            headRows[0].update_record(issued_to=issued_to,depot_to_name=depot_to_name,issue_date=issue_date,note=note,transaction_cause=transaction_cause,total_discount=discount,ym_date=ym_date)
       else:
           ref_sl=0           
           db.sm_issue_head.insert(cid=c_id,depot_id=depot_id,depot_name=depot_name,sl=sl,store_id=store_id,store_name=store_name,issued_to=issued_to,depot_to_name=depot_to_name,issue_date=issue_date,req_sl=ref_sl,note=note,transaction_cause=transaction_cause,total_discount=discount,ym_date=ym_date)
           
       #---------------
       db((db.sm_issue.cid==c_id)& (db.sm_issue.depot_id==depot_id) & (db.sm_issue.sl==sl)).update(issued_to=issued_to,depot_to_name=depot_to_name,issue_date=issue_date,note=note,transaction_cause=transaction_cause,total_discount=discount,ym_date=ym_date)
       
       session.flash = ''
       redirect(URL(c='depot',f='depot_stock_issue',vars=dict(req_sl=sl)))
    
#     elif form.errors:
#         for fieldname in form.errors:
#             response.flash = fieldname+': '+form.errors[fieldname]
#             break
    
    #------------------- SHOW FIELD VALUE
    depot_name=''
    depot_to_name=''
    
    req_sl=request.vars.req_sl    
    depotid=request.vars.depotid 
    if depotid=='' or depotid==None:
        depot_id=session.depot_id
        depot_name=session.user_depot_name
    else:
        depot_id=depotid
        
    sl=0
    status='Draft'
    issue_process_status='Issued'
    issued_to=''
    issue_date=current_date
    note='' 
    discount=0  
    ref_sl=0
    field2=0
    store_id=''
    store_name=''
    transaction_cause=''
    records=db((db.sm_issue.cid==c_id)& (db.sm_issue.depot_id==depot_id) & (db.sm_issue.sl==req_sl)).select(db.sm_issue.ALL,orderby=db.sm_issue.item_name)
    for rec in records:
        depot_id=rec.depot_id
        depot_name=rec.depot_name
        sl=rec.sl        
        store_id=rec.store_id
        store_name=rec.store_name        
        status=rec.status
        issue_process_status=rec.issue_process_status
        issued_to=rec.issued_to
        depot_to_name=rec.depot_to_name
        issue_date=rec.issue_date
        note=rec.note
        discount=rec.total_discount
        ref_sl=rec.req_sl
        field2=rec.field2
        transaction_cause=rec.transaction_cause
        break
    
    #------------------- DEPOT SHOW IN COMBO
    reqRecords=''
    # if issued_to=='':
    #     #reqRecords=db((db.sm_depot_settings.cid==c_id) & (db.sm_depot_settings.depot_id_from_to==session.depot_id) & (db.sm_depot_settings.from_to_type=='Receive') & (db.sm_depot_settings.cid==c_id) & (db.sm_depot_settings.cid==db.sm_depot.cid)).select(db.sm_depot.depot_id, db.sm_depot.name ,groupby = db.sm_depot.depot_id, orderby=db.sm_depot.name)
    #     reqRecords=db((db.sm_depot.cid==c_id) & (db.sm_depot.depot_id!=session.depot_id)).select(db.sm_depot.depot_id,db.sm_depot.name,orderby=db.sm_depot.name)
        
    storeRecords=''
    if sl==0:
        storeRecords=db((db.sm_depot_store.cid==c_id) & (db.sm_depot_store.depot_id==depot_id) & (db.sm_depot_store.store_type=='SALES')).select(db.sm_depot_store.store_id,db.sm_depot_store.store_name,orderby=db.sm_depot_store.store_name)
    
    #-------------------    
    refRecords=''
    if transaction_cause=='':
        refRecords=db((db.sm_category_type.cid==c_id) & (db.sm_category_type.type_name=='ISSUE_CAUSE')).select(db.sm_category_type.cat_type_id,orderby=db.sm_category_type.cat_type_id)
    
    #--------------------
    return dict(form=form,reqRecords=reqRecords,records=records,storeRecords=storeRecords,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,sl=sl,ref_sl=ref_sl,issued_to=issued_to,depot_to_name=depot_to_name,issue_date=issue_date,status=status,issue_process_status=issue_process_status,note=note,field2=field2,
                transaction_cause=transaction_cause,refRecords=refRecords,discount=discount,count_inserted=count_inserted,count_error=count_error,error_str=error_str,total_row=total_row,access_permission=access_permission,access_permission_view=access_permission_view)
def delete_update_issue_item():
    
    c_id=session.cid
    
    btn_delete=request.vars.btn_delete
    btn_update=request.vars.btn_update
    
    req_depot=request.args(0)
    req_sl=request.args(1)    
    req_item=request.args(2)
    rowid=request.args(3)
    
    if btn_delete:
        countRecords=db((db.sm_issue.cid==c_id)& (db.sm_issue.depot_id==req_depot) & (db.sm_issue.sl==req_sl)).count()
        if int(countRecords)==1:
            session.flash='At least one item needs in a issue, You can cancel if required!'
        else:
            db((db.sm_issue.cid==c_id) & (db.sm_issue.depot_id==req_depot) & (db.sm_issue.sl==req_sl)& (db.sm_issue.item_id==req_item)& (db.sm_issue.id==rowid)).delete()
            session.flash='Deleted successfully'
            
        redirect(URL(c='depot',f='depot_stock_issue',vars=dict(req_sl=req_sl)))
        
    elif btn_update:        
        batchIdVar='batch_id_update_'+str(req_item)+'_'+str(rowid)
        batchId=str(request.vars[batchIdVar]).strip().upper().split('|')[0]
        item_qty=request.vars.item_qty
        
        if batchId=='':
            session.flash='Required Batch ID'
        else:
            try:
                item_qty=int(item_qty)
                if item_qty<=0:
                    item_qty=0
            except:
                item_qty=0
                
            if item_qty==0:
                session.flash='Invalid Qty'
            else:
                itemBatchRows = db((db.sm_item_batch.cid == c_id) & (db.sm_item_batch.item_id == req_item) & (db.sm_item_batch.batch_id == batchId) & (db.sm_item_batch.expiary_date >= current_date)).select(db.sm_item_batch.item_id,db.sm_item_batch.expiary_date,limitby=(0,1))
                if not itemBatchRows:
                    session.flash='Invalid Item Batch ID'
                else:
                    expiary_date=itemBatchRows[0].expiary_date
                    
                    db((db.sm_issue.cid==c_id) & (db.sm_issue.depot_id==req_depot) & (db.sm_issue.sl==req_sl)& (db.sm_issue.item_id==req_item)& (db.sm_issue.id==rowid)).update(batch_id=batchId,quantity=item_qty,expiary_date=expiary_date)
                    session.flash='Updated successfully'
                    
        redirect(URL(c='depot',f='depot_stock_issue',vars=dict(req_sl=req_sl)))
    #  ---------------------
    
    return dict()

#=================== Post and Cancel

#Update Status sm_issue_head
def post_cancel_issue():
    c_id=session.cid
    
    btn_post=request.vars.btn_post
    btn_cancel=request.vars.btn_cancel
    
    req_depot=request.args(0)
    req_sl=request.args(1)    
    req_date=request.args(2)    
    ym_date=str(req_date)[0:7]+'-01'
    
    if btn_post:
        countRecords=db((db.sm_issue.cid==c_id)& (db.sm_issue.depot_id==req_depot) & (db.sm_issue.sl==req_sl)).count()
        if int(countRecords)==0:
            session.flash='At least one item needs in a issue!'
        else:
            batchIdrows=db((db.sm_issue.cid==c_id)& (db.sm_issue.depot_id==req_depot) & (db.sm_issue.sl==req_sl) & (db.sm_issue.batch_id=='')).select(db.sm_issue.issued_to,limitby=(0,1))
            if batchIdrows:
                session.flash = 'Required Batch ID for all Items'
            else:                
                
                #--------------------------- chcek stock cron flag
                autDelCronRows=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==req_depot)&(db.sm_depot.auto_del_cron_flag==0)).select(db.sm_depot.id,db.sm_depot.cid,limitby=(0,1))
                if not autDelCronRows:
                    session.flash='One process running, please try again'
                else:
                    autDelCronRows[0].update_record(auto_del_cron_flag=1)
                    #---------------------
                    
                    diffRecords="select iss.item_id as item_id from sm_depot_stock_balance dsb,sm_issue iss  where (iss.cid='"+str(c_id)+"' and iss.depot_id='"+str(req_depot)+"' and iss.sl="+str(req_sl)+" and dsb.cid='"+str(c_id)+"' and dsb.depot_id='"+str(req_depot)+"' and iss.store_id=dsb.store_id and iss.item_id=dsb.item_id and iss.batch_id=dsb.batch_id and  (dsb.quantity-dsb.block_qty)<(iss.quantity+iss.bonus_qty))"
                    diffRowsList=db.executesql(diffRecords,as_dict=True)                    
                    itemStrForQty=''
                    for i in range(len(diffRowsList)):
                        diffDictData=diffRowsList[i]
                        if itemStrForQty=='':
                            itemStrForQty=diffDictData['item_id']
                        else:
                            itemStrForQty+=','+diffDictData['item_id']
                    
                    if itemStrForQty!='':
                        session.flash='Quantity not available for item ID '+str(itemStrForQty)                        
                    else:
                        
                        #--------------------
                        issued_to=''
                        totalAmount=0
                        total_discount=0
                        
                        #----- Auto receive YES or NO (Pharma auto receive NO)
                        if session.auto_receive=='YES':#Not used
                            receiveHeadList=[]
                            receiveDetailsList=[]
                            recHeadDict={}
                            recDetailsDict={}
                            maxSl=0
                            
                            #------------------------ Receive SL
                            issueRows=db((db.sm_issue.cid==c_id)& (db.sm_issue.depot_id==req_depot) & (db.sm_issue.sl==req_sl)).select(db.sm_issue.issued_to,limitby=(0,1))
                            issued_to=issueRows[0].issued_to
                            
                            maxSl=1
                            records=db((db.sm_depot.cid==c_id) & (db.sm_depot.depot_id==issued_to)).select(db.sm_depot.id,db.sm_depot.receive_sl,limitby=(0,1))
                            if records:
                                sl=records[0].receive_sl
                                maxSl=int(sl)+1
                            
                            #----------- update depot sl
                            if records:
                                records[0].update_record(receive_sl=maxSl)
                            
                            #--------------
                            rows=db((db.sm_issue.cid==c_id)& (db.sm_issue.depot_id==req_depot) & (db.sm_issue.sl==req_sl)).select(db.sm_issue.ALL)  
                            for row in rows:
                                depot_from_name=row.depot_name
                                
                                issued_to=row.issued_to
                                depot_name=row.depot_to_name
                                
                                issue_date=row.issue_date
                                item_id=row.item_id
                                item_name=row.item_name
                                quantity=int(row.quantity)
                                bonus_qty=int(row.bonus_qty)
                                dist_rate=float(row.dist_rate)
                                short_note=row.short_note
                                
                                batch_id=row.batch_id
                                
                                total_discount=float(row.total_discount)  
                                
                                ym_date=row.ym_date
                                note=row.note
                                
                                totalAmount+=dist_rate*quantity
                                
                                #required value if needed (auto receive yes)
                                store_id=''
                                store_name=''
                                #---
                                
                                recDetailsDict={'cid':c_id,'depot_id':issued_to,'depot_name':depot_name,'sl':maxSl,'store_id':store_id,'store_name':store_name, 'receive_from':req_depot,'depot_from_name':depot_from_name,'receive_date':issue_date,'status':'Posted','total_discount':total_discount,'ref_sl':req_sl,'item_id':item_id,'item_name':item_name,
                                                'quantity':quantity,'bonus_qty':bonus_qty,'dist_rate':dist_rate,'short_note':short_note,'ym_date':ym_date,'note':note,'batch_id':batch_id}
                                receiveDetailsList.append(recDetailsDict)
                                
                            recHeadDict={'cid':c_id,'depot_id':issued_to,'depot_name':depot_name,'sl':maxSl,'store_id':store_id,'store_name':store_name,'receive_from':req_depot,'depot_from_name':depot_from_name,'receive_date':issue_date,'status':'Posted','total_discount':total_discount,'ref_sl':req_sl,'ym_date':ym_date,'note':note}
                            receiveHeadList.append(recHeadDict)
                            
                            totalAmount=totalAmount-total_discount
                            
                            #--------------------- depot balance
                            #format:cid<fdfd>tx_type<fdfd>sl<fdfd>datetime<fdfd>reference<fdfd>1st account with prefix<fdfd>2nd account with prefix<fdfd>tx_amount
                            
                            #------- condition used for IMPORT/FACTORY/OPENING
                            depotRows=db((db.sm_depot.cid==c_id) & (db.sm_depot.depot_id==issued_to)&(db.sm_depot.depot_category=='EXTERNAL')).select(db.sm_depot.depot_id,limitby=(0,1))
                            if depotRows:
                                if session.primaryLedgerCreate=='YES':
                                    strData2=str(c_id)+'<fdfd>ISSUERECEIVE<fdfd>'+str(req_sl)+'<fdfd>'+str(datetime_fixed)+'<fdfd>'+str(req_depot)+'-'+str(req_sl)+':'+str(req_depot)+'-'+str(req_sl)+'<fdfd>DPT-'+str(req_depot)+'<fdfd>DPT-'+str(issued_to)+'<fdfd>'+str(totalAmount)
                                    resStr2=set_balance_transaction(strData2)                        
                                    resStrList2=resStr2.split('<sep>',resStr2.count('<sep>'))
                                    flag2=resStrList2[0]
                                    msg2=resStrList2[1]
                                else:
                                    flag2='True'
                                    
                                if flag2=='True':
                                    db((db.sm_issue.cid==c_id)& (db.sm_issue.depot_id==req_depot) & (db.sm_issue.sl==req_sl)).update(status='Posted')
                                    db((db.sm_issue_head.cid==c_id)& (db.sm_issue_head.depot_id==req_depot) & (db.sm_issue_head.sl==req_sl)).update(status='Posted')
            #                        db((db.sm_issue.cid==c_id)& (db.sm_issue.depot_id==req_depot) & (db.sm_issue.sl==req_sl)).update(status='Posted',issue_process_status='Received')
            #                        db((db.sm_issue_head.cid==c_id)& (db.sm_issue_head.depot_id==req_depot) & (db.sm_issue_head.sl==req_sl)).update(status='Posted',issue_process_status='Received')
                                    
                                    # call update depot stock (type,cid,depotid,sl)
                                    update_depot_stock('ISSUE',c_id,req_depot,req_sl)
                                    
                                    #update_depot_stock('RECEIVE',c_id,issued_to,maxSl)
                                    
                                    session.flash = 'success'            
                                else:
                                    db.rollback()
                                    session.flash = 'process error:101'
                                
                            else:                        
                                if session.primaryLedgerCreate=='YES':
                                    strData2=str(c_id)+'<fdfd>ISSUERECEIVE<fdfd>'+str(req_sl)+'<fdfd>'+str(datetime_fixed)+'<fdfd>'+str(req_depot)+'-'+str(req_sl)+':'+str(issued_to)+'-'+str(maxSl)+'<fdfd>DPT-'+str(req_depot)+'<fdfd>DPT-'+str(issued_to)+'<fdfd>'+str(totalAmount)
                                    resStr2=set_balance_transaction(strData2)
                                    resStrList2=resStr2.split('<sep>',resStr2.count('<sep>'))
                                    flag2=resStrList2[0]
                                    msg2=resStrList2[1]
                                else:
                                    flag2='True'
                                
                                if flag2=='True':
                                    headInsert=db.sm_receive_head.bulk_insert(receiveHeadList)
                                    detailInsert=db.sm_receive.bulk_insert(receiveDetailsList)
                                    
                                    db((db.sm_issue.cid==c_id)& (db.sm_issue.depot_id==req_depot) & (db.sm_issue.sl==req_sl)).update(status='Posted',issue_process_status='Received')
                                    db((db.sm_issue_head.cid==c_id)& (db.sm_issue_head.depot_id==req_depot) & (db.sm_issue_head.sl==req_sl)).update(status='Posted',issue_process_status='Received')
                                    
                                    # call update depot stock (type,cid,depotid,sl)
                                    update_depot_stock('ISSUE',c_id,req_depot,req_sl)
                                    
                                    update_depot_stock('RECEIVE',c_id,issued_to,maxSl)
                                    
                                    session.flash = 'success'            
                                else:
                                    db.rollback()
                                    session.flash = 'process error:101'
                                
                        #Auto receive no                 
                        else:
                            #check ledger create or Not
                            if session.primaryLedgerCreate=='YES':
                                rows=db((db.sm_issue.cid==c_id)& (db.sm_issue.depot_id==req_depot) & (db.sm_issue.sl==req_sl)).select(db.sm_issue.issued_to,db.sm_issue.quantity,db.sm_issue.dist_rate,db.sm_issue.total_discount)            
                                for row in rows:
                                    issued_to=row.issued_to
                                    quantity=int(row.quantity)
                                    dist_rate=float(row.dist_rate)
                                    total_discount=float(row.total_discount)                
                                    totalAmount+=dist_rate*quantity
                                
                                totalAmount=totalAmount-total_discount
                            #-------------
                            
                            #--------------------- depot balance
                            #format:cid<fdfd>TodepotID<fdfd>FromDepotID<fdfd>typeName(keyword)<fdfd>paymtent_amount
                            depotRows=db((db.sm_depot.cid==c_id) & (db.sm_depot.depot_id==issued_to)&(db.sm_depot.depot_category=='EXTERNAL')).select(db.sm_depot.depot_id,limitby=(0,1))
                            if depotRows:
                                #check ledger create or Not
                                if session.primaryLedgerCreate=='YES':
                                    strData2=str(c_id)+'<fdfd>ISSUERECEIVE<fdfd>'+str(req_sl)+'<fdfd>'+str(datetime_fixed)+'<fdfd>'+str(req_depot)+'-'+str(req_sl)+':'+str(req_depot)+'-'+str(req_sl)+'<fdfd>DPT-'+str(req_depot)+'<fdfd>DPT-'+str(issued_to)+'<fdfd>'+str(totalAmount)                                            
                                    resStr2=set_balance_transaction(strData2)                        
                                    resStrList2=resStr2.split('<sep>',resStr2.count('<sep>'))
                                    flag2=resStrList2[0]
                                    msg2=resStrList2[1]
                                else:
                                    flag2='True'
                                #-----------
                                
                                if flag2=='True':
                                    db((db.sm_issue.cid==c_id)& (db.sm_issue.depot_id==req_depot) & (db.sm_issue.sl==req_sl)).update(status='Posted')
                                    db((db.sm_issue_head.cid==c_id)& (db.sm_issue_head.depot_id==req_depot) & (db.sm_issue_head.sl==req_sl)).update(status='Posted')
                                    
                                    # call update depot stock (type,cid,depotid,sl)
                                    update_depot_stock('ISSUE',c_id,req_depot,req_sl)
                                    
                                    session.flash = 'success'
                                else:
                                    db.rollback()
                                    session.flash = 'process error:101'
                                
                            else:
                                #check ledger create or Not
                                if session.primaryLedgerCreate=='YES':
                                    strData2=str(c_id)+'<fdfd>ISSUE<fdfd>'+str(req_sl)+'<fdfd>'+str(datetime_fixed)+'<fdfd>'+str(req_depot)+'-'+str(req_sl)+'<fdfd>DPT-'+str(req_depot)+'<fdfd>DPT-'+str(issued_to)+'<fdfd>'+str(totalAmount)              
                                    resStr2=set_balance_transaction(strData2)  # call function
                                    resStrList2=resStr2.split('<sep>',resStr2.count('<sep>'))
                                    flag2=resStrList2[0]
                                    msg2=resStrList2[1]
                                else:
                                    flag2='True'
                                #-----------
                                
                                if flag2=='True':
                                    db((db.sm_issue.cid==c_id)& (db.sm_issue.depot_id==req_depot) & (db.sm_issue.sl==req_sl)).update(status='Posted')
                                    db((db.sm_issue_head.cid==c_id)& (db.sm_issue_head.depot_id==req_depot) & (db.sm_issue_head.sl==req_sl)).update(status='Posted')
                                    
                                    # call update depot stock (type,cid,depotid,sl)
                                    update_depot_stock('ISSUE',c_id,req_depot,req_sl)
                                    
                                    session.flash = 'success'                         
                                else:
                                    db.rollback()
                                    session.flash = 'process error:102'
                        
                    #---------------------
                    autDelCronRows[0].update_record(auto_del_cron_flag=0)
                    #db.commit()
                    #--------------
                
                #------------------------------------------        
        redirect(URL(c='depot',f='depot_stock_issue',vars=dict(req_sl=req_sl)))


    elif btn_cancel:
        countRecords=db((db.sm_issue.cid==c_id)& (db.sm_issue.depot_id==req_depot) & (db.sm_issue.sl==req_sl)).count()
        if int(countRecords)==0:
            session.flash='At least one item needs in a issue!'
        else:
            db((db.sm_issue.cid==c_id)& (db.sm_issue.depot_id==req_depot) & (db.sm_issue.sl==req_sl)).update(status='Cancelled')
            db((db.sm_issue_head.cid==c_id)& (db.sm_issue_head.depot_id==req_depot) & (db.sm_issue_head.sl==req_sl)).update(status='Cancelled')

        redirect(URL(c='depot',f='depot_stock_issue',vars=dict(req_sl=req_sl)))
    return dict()


#----------------- Show pending Requisition
def show_pending_requisition():
    #----------Task assaign----------
    task_id='rm_stock_issue_manage'
    task_id_view='rm_stock_issue_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))   
    
     
    depotId=request.vars.depotId
    
    response.title='Pending Requisition'
    
    records=db((db.sm_requisition_head.cid==session.cid) & (db.sm_requisition_head.requisition_to==depotId)&(db.sm_requisition_head.status=='Posted')&(db.sm_requisition_head.req_process_status=='Requisition')).select(db.sm_requisition_head.ALL,orderby=db.sm_requisition_head.sl)    
    
    return dict(records=records)

#=========================================== Receive List ===============================

#---------------catagory-----------------------
def validation_receive_reference(form):    
    category_id=str(request.vars.cat_type_id).strip().title()
    if category_id!='':
        rows_check=db((db.sm_category_type.cid==session.cid) & (db.sm_category_type.type_name=='RECEIVE_CAUSE') &(db.sm_category_type.cat_type_id==category_id)).select(db.sm_category_type.cat_type_id,limitby=(0,1))
        if rows_check:
            form.errors.cat_type_id=''
            response.flash = 'Already exist, Please choose a new'
        else:
            form.vars.cid=session.cid
            form.vars.type_name='RECEIVE_CAUSE'
            form.vars.cat_type_id=category_id
def receive_reference():    
    task_id='rm_utility_manage'
    access_permission=check_role(task_id)
    if (access_permission==False and session.user_type=="Admin"):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))
        
    response.title='Internal GR Note Cause'
    
    cid=session.cid
    
    #---------------------
    form =SQLFORM(db.sm_category_type,
                  fields=['cat_type_id'],
                  submit_button='Save'
                  )
    
    if form.accepts(request.vars,session,onvalidation=validation_receive_reference):
        response.flash = 'Saved Successfully'
        
    #--------------------------------
    btn_delete=request.vars.btn_delete
    if btn_delete:
        record_id=request.args[1]
        category_id=''
        catRow=db((db.sm_category_type.cid == cid)&(db.sm_category_type.id==record_id)&(db.sm_category_type.type_name=='RECEIVE_CAUSE')).select(db.sm_category_type.cat_type_id,limitby=(0,1))
        if not catRow:
            response.flash='Invalid request'
        else:
            category_id=catRow[0].cat_type_id
            
            records=db((db.sm_receive_head.cid==cid) & (db.sm_receive_head.transaction_cause==category_id)).select(db.sm_receive_head.transaction_cause,limitby=(0,1))
            if records:
                response.flash='Already used in GR Note'            
            else:
                db((db.sm_category_type.cid == cid)&(db.sm_category_type.id == record_id)&(db.sm_category_type.type_name=='RECEIVE_CAUSE')).delete()
                response.flash='Deleted successfully'
                
    #--------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=session.items_per_page
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #--------end paging
    
    records=db((db.sm_category_type.cid==cid)&(db.sm_category_type.type_name=='RECEIVE_CAUSE')).select(db.sm_category_type.ALL,orderby=db.sm_category_type.cat_type_id,limitby=limitby)
    
    return dict(form=form,records=records,page=page,items_per_page=items_per_page,access_permission=access_permission)
#---------------


def depot_stock_receive_list():
    #----------Task assaign----------
    task_id='rm_stock_receive_manage'
    task_id_view='rm_stock_receive_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))   
        
    # --------------------- 
    c_id=session.cid
    
    response.title='GR Note(Receive List)'
    
    # Set text for filter    
    btn_filter_receive=request.vars.btn_filter
    btn_all=request.vars.btn_all
    depot_id_value=str(request.vars.depot_id_value).strip()
    search_type=str(request.vars.search_type).strip()
    search_value=str(request.vars.search_value).strip()
    
    reqPage=len(request.args)
    
    #Set sessions for filter
    if btn_filter_receive:
        session.btn_filter_receive=btn_filter_receive
        session.depot_id_value_rec=depot_id_value 
        session.search_type_rec=search_type
        session.search_value_rec=search_value
        
        #Check SL in integer or not
        if (session.search_type_rec=='SL'):
            sl=0
            if not(session.search_value_rec=='' or session.search_value_rec==None):
                try:       
                    sl=int(session.search_value_rec)
                    session.search_value_rec=sl
                except:
                    session.search_value_rec=sl
                    response.flash='sl needs number value'
            else:
                session.search_value_rec=sl
                
        reqPage=0
        
    elif btn_all:
        session.btn_filter_receive=None
        session.depot_id_value_rec=None
        session.search_type_rec=None
        session.search_value_rec=None
        reqPage=0    
    
    
    #--------paging
    if reqPage:
        page=int(request.args[0])
    else:
        page=0
    items_per_page=session.items_per_page*10
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #--------end paging  
    # Create sql according to search type
    qset=db()
    qset=qset(db.sm_receive_head.cid==c_id)
    
    if (session.user_type=='Depot'):
        qset=qset(db.sm_receive_head.depot_id==session.depot_id)
        
    if (session.btn_filter_receive):
        
        if (session.user_type!='Depot'):
            if not (session.depot_id_value_rec=='' or session.depot_id_value_rec==None):
                searchValue=str(session.depot_id_value_rec).split('|')[0]
                qset=qset(db.sm_receive_head.depot_id==searchValue)
            else:
                qset=qset(db.sm_receive_head.depot_id!='')
                
        #------------
        if (session.search_type_rec=='SL'):
            qset=qset(db.sm_receive_head.sl==session.search_value_rec)
            
        elif (session.search_type_rec=='DATE'):
            qset=qset(db.sm_receive_head.receive_date==session.search_value_rec)
            
        elif (session.search_type_rec=='STATUS'):
            qset=qset(db.sm_receive_head.status==session.search_value_rec)
            
        elif (session.search_type_rec=='ReceiveFrom'):
            search_value_rec=str(session.search_value_rec).split('|')[0]
            qset=qset(db.sm_receive_head.receive_from==search_value_rec)
        
        elif (session.search_type_rec=='UserID'):
            search_value_rec=str(session.search_value_rec).upper()
            qset=qset(db.sm_receive_head.updated_by==search_value_rec)
            
        
    records=qset.select(db.sm_receive_head.ALL,orderby=~db.sm_receive_head.id,limitby=limitby)


    #-Create a form from database table for search in date range
    search_form =SQLFORM(db.sm_search_date)
    #-------------
    
    return dict(search_form=search_form,records=records,page=page,items_per_page=items_per_page,access_permission=access_permission,access_permission_view=access_permission_view)

#======================= Stock Requisition (Billal)
#Vlidation for recieve
def validation_receive(form):
    c_id=session.cid   
    depot_id=str(form.vars.depot_id).split('|')[0]
    depot_name=str(form.vars.depot_id).split('|')[1]
    
    store_idname=str(form.vars.store_id)
    
    receive_from=str(request.vars.receive_from).split('|')[0]
    
    transaction_cause=str(form.vars.transaction_cause)
    
    item_id=str(form.vars.item_id).upper().strip()
    item_name=str(form.vars.item_name)
    
    batch_id=str(request.vars.batch_id).upper().strip().split('|')[0]    
    quantity=form.vars.quantity
    
    bonus_qty=0     #form.vars.bonus_qty
    dist_rate=0     #form.vars.dist_rate
    short_note=''   #form.vars.short_note
    
    if quantity=='' or quantity==None:
        quantity=0
    if bonus_qty=='' or bonus_qty==None:
        bonus_qty=0
    if dist_rate=='' or dist_rate==None:
        dist_rate=0
    
    if store_idname=='':
        form.errors.store_id=''
        response.flash="Required From Store/Location"
    else:
        store_id=str(store_idname).split('|')[0]
        store_name=str(store_idname).split('|')[1]
        
        depotRows=db((db.sm_depot.cid==c_id) & (db.sm_depot.depot_id==receive_from)& (db.sm_depot.status=='ACTIVE')).select(db.sm_depot.depot_id,db.sm_depot.name,db.sm_depot.depot_category,limitby=(0,1))
        if not depotRows:
            form.errors.short_note=''  
            response.flash='Receive from not available'  
        else:
            depot_from_name=depotRows[0].name
            depot_category=str(depotRows[0].depot_category).strip().upper()
            
            itemRows = db((db.sm_item.cid == c_id)&(db.sm_item.item_id == item_id)).select(db.sm_item.name,db.sm_item.price,db.sm_item.unit_type,db.sm_item.item_carton, limitby=(0,1))
            if not itemRows:
                form.errors.item_id=''
                response.flash="Invalid Item ID"
            else:
                dist_rate=itemRows[0].price
                unit_type=itemRows[0].unit_type
                item_carton=itemRows[0].item_carton
                
                itemBatchRows = db((db.sm_item_batch.cid == c_id) & (db.sm_item_batch.item_id == item_id) & (db.sm_item_batch.batch_id == batch_id) & (db.sm_item_batch.expiary_date >= current_date)).select(db.sm_item_batch.item_id,db.sm_item_batch.expiary_date,limitby=(0,1))
                if not itemBatchRows:
                    form.errors.batch_id=''
                    response.flash="Invalid Item Batch ID"
                else:
            #        if depot_category!='EXTERNAL':
            #            form.errors.short_note=''  
            #            response.flash='Receive from only active EXTERNAL source allowed'
            #        else:
                    
                    expiary_date=itemBatchRows[0].expiary_date
                    
                    sl=int(form.vars.sl)
                    ym_date=str(form.vars.receive_date)[0:7]+'-01'
                    
                    existRecords=db((db.sm_receive.cid==c_id) & (db.sm_receive.depot_id==depot_id)& (db.sm_receive.sl==sl)& (db.sm_receive.item_id==item_id)& (db.sm_receive.batch_id==batch_id)).select(db.sm_receive.id,db.sm_receive.item_id,limitby=(0,1))
                    if existRecords:
                        existRecords[0].update_record(item_name=item_name,quantity=quantity,bonus_qty=bonus_qty,dist_rate=dist_rate,short_note=short_note)        
                        form.errors.short_note=''  
                        response.flash='Item replaced!'      
                    
                    elif int(quantity)<=0:
                        form.errors.quantity=''
                        response.flash='need item quantity!'
                    
                    else:
                        if sl==0:
                            maxSl=1
                            records=db((db.sm_depot.cid==c_id) & (db.sm_depot.depot_id==depot_id)).select(db.sm_depot.id,db.sm_depot.receive_sl,limitby=(0,1))
                            if records:
                                recSl=records[0].receive_sl
                                maxSl=int(recSl)+1                
                            
                            #----------- UPDATE SL IN DEPOT
                            records[0].update_record(receive_sl=maxSl)
                            
                            form.vars.sl=maxSl
                        
                        #-----------------            
                        form.vars.depot_id=depot_id
                        form.vars.depot_name=depot_name
                        form.vars.ym_date=ym_date
                        
                        form.vars.store_id=store_id
                        form.vars.store_name=store_name
                        
                        form.vars.receive_from=receive_from
                        form.vars.depot_from_name=depot_from_name
                        
                        form.vars.item_id=item_id
                        form.vars.item_name=item_name
                        form.vars.batch_id=batch_id
                        form.vars.dist_rate=dist_rate
                        form.vars.transaction_cause=transaction_cause
                        form.vars.item_unit=unit_type
                        form.vars.item_carton=item_carton
                        form.vars.expiary_date=expiary_date
                        
                        ref_sl= request.vars.ref_sl
                        if sl==0:
                            form.vars.ref_sl=0
                        else:
                            form.vars.ref_sl=ref_sl
def depot_stock_receive():
    #----------Task assaign----------
    task_id='rm_stock_receive_manage'
    task_id_view='rm_stock_receive_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))   
    
    response.title='GR Note(Receive)'    
#   --------------------- 
    c_id=session.cid
    #Variable for batch upload
    count_inserted=request.vars.count_inserted
    count_error=request.vars.count_error
    error_str=request.vars.error_str
    total_row=request.vars.total_row
    
    #------------------
    btn_update=request.vars.btn_update
    btn_batch_upload=request.vars.btn_batch_upload
    btn_import_req=request.vars.btn_import_req
    
    #---------------------- UPDATE
#    return btn_batch_upload
    if btn_update:
        req_depot_id=str(request.vars.depot_id).split('|')[0]
        reqSl=request.vars.sl
        receive_from=str(request.vars.receive_from).split('|')[0]
        receive_date=request.vars.receive_date
        ym_date=str(receive_date)[0:7]+'-01'#Save on first date of month
        req_note=request.vars.note 
        transaction_cause=request.vars.transaction_cause 
        
        total_discount=0    #request.vars.total_discount
        # Update receive head nad receive
        if receive_from!='':
            db((db.sm_receive_head.cid==c_id)& (db.sm_receive_head.depot_id==req_depot_id) & (db.sm_receive_head.sl==reqSl)).update(receive_date=receive_date,note=req_note,total_discount=total_discount,ym_date=ym_date,transaction_cause=transaction_cause)
            db((db.sm_receive.cid==c_id)& (db.sm_receive.depot_id==req_depot_id) & (db.sm_receive.sl==reqSl)).update(receive_date=receive_date,note=req_note,total_discount=total_discount,ym_date=ym_date,transaction_cause=transaction_cause)
            redirect(URL(c='depot',f='depot_stock_receive',vars=dict(req_sl=reqSl)))
            
    #----------------- BATCH UPLOAD
        
    elif (btn_batch_upload):  # and str(request.vars.input_data)!='' and int(request.vars.sl)> 0
        #--------- existing
        req_depot_id=str(request.vars.depot_id).split('|')[0]
        
        storeIdName=str(request.vars.store_id)
        store_id=''
        store_name=''
        if storeIdName!='':
            store_id=str(storeIdName).split('|')[0]
            store_name=str(storeIdName).split('|')[1]            
            store_id=str(store_id).strip()
            store_name=str(store_name).strip()
        
        reqSl=int(request.vars.sl)
        receive_from=str(request.vars.receive_from).split('|')[0]
        receive_date=request.vars.receive_date
        ym_date=str(receive_date)[0:7]+'-01'#Save on first date of month
        req_note=request.vars.note
        transaction_cause=request.vars.transaction_cause
        
        input_data=str(request.vars.input_data)
        
        if store_id=='' or receive_from=='' or receive_date=='':
            session.flash='Required Store To, Receive From and Receive Date'
            redirect(URL(c='depot',f='depot_stock_receive',vars=dict(req_sl=0)))        
        else:            
            if input_data=='':
                session.flash='Required upload data'
                redirect(URL(c='depot',f='depot_stock_receive',vars=dict(req_sl=0)))
            else:            
                pass
            
            if reqSl==0 or reqSl=='':
                records=db((db.sm_depot.cid==c_id) & (db.sm_depot.depot_id==req_depot_id)).select(db.sm_depot.id,db.sm_depot.receive_sl,limitby=(0,1))
                if records:
                    sl=records[0].receive_sl
                    maxSl=int(sl)+1
                else:
                    maxSl=1
                
                #----------- UPDATE SL IN DEPOT
                records[0].update_record(receive_sl=maxSl)
                reqSl=maxSl
                
            
            depot_name=''
            depotRecords=db((db.sm_depot.cid==c_id) & (db.sm_depot.depot_id==req_depot_id)).select(db.sm_depot.name,limitby=(0,1))
            if depotRecords:
                depot_name=depotRecords[0].name
                
            depot_from_name=''
            receive_fromRecords=db((db.sm_depot.cid==c_id) & (db.sm_depot.depot_id==receive_from)).select(db.sm_depot.name,limitby=(0,1))
            if receive_fromRecords:
                depot_from_name=receive_fromRecords[0].name
                
            #----------- variable declaration
            count_inserted=0
            count_error=0
            error_str=''
            total_row=0
    
            item_list=[]
            item_list_table=[]
            
            ins_dict={}
            ins_list=[]
            
            itemIdBatchIdList=[]
            
            currentDate=datetime.datetime.strptime(str(current_date),'%Y-%m-%d')
            
            #---------
            
            inserted_count=0
            error_count=0
            error_list=[]
            row_list=input_data.split( '\n')
            total_row=len(row_list)
            
            #   ---------------------- valid item list loop
            for i in range(total_row):
                if i>=100:
                    break
                else:
                    row_data=row_list[i]                    
                    coloum_list=row_data.split( '\t')
                    if len(coloum_list)==4:
                        item_list.append(str(coloum_list[0]).strip().upper())
                        
            # Create item list from sm_item table
            itemRows=db((db.sm_item.cid==c_id)&(db.sm_item.item_id.belongs(item_list))).select(db.sm_item.item_id,db.sm_item.name,db.sm_item.price,db.sm_item.dist_price,db.sm_item.unit_type,db.sm_item.item_carton,orderby=db.sm_item.name)
            item_list_table=itemRows.as_list()
            
                
            headFlag=False
            headRecords=db((db.sm_receive_head.cid==c_id) & (db.sm_receive_head.depot_id==req_depot_id)& (db.sm_receive_head.sl==reqSl)).select(db.sm_receive_head.id,limitby=(0,1))
            if headRecords:
                headFlag=True
                
            #   --------------------  excel main loop
            for i in range(total_row):
                if i>=100: 
                    break
                else:
                    row_data=row_list[i]        
                    coloum_list=row_data.split( '\t')            
                
                if len(coloum_list)!=4:
                    error_data=row_data+'(4 columns need in a row)\n'
                    error_str=error_str+error_data
                    count_error+=1
                    continue
                else:             
                    item_id_value=str(coloum_list[0]).strip().upper()
                    item_batchid_value=str(coloum_list[1]).strip().upper()
                    item_qty_value=coloum_list[2]
                    item_expiary_date=str(coloum_list[3]).strip()
                    item_bonus_qty_value=0
                    
                    
                    if (item_id_value=='' or item_batchid_value=='' or item_qty_value=='' or item_expiary_date==''):
                        error_data=row_data+'(Required all value)\n'
                        error_str=error_str+error_data
                        count_error+=1
                        continue
                    else:
                        pass
                    #----------------
                    try:
                        item_qty_value=int(item_qty_value)
                        if item_qty_value<0:
                            item_qty_value=0
                    except:
                        item_qty_value=0
                                    
                    if item_qty_value==0:
                        error_data=row_data+'(Invalid Qty)\n'
                        error_str=error_str+error_data
                        count_error+=1
                        continue
                    else:
                        pass
                    #-------------
                    dateFlag=True
                    try:
                        item_expiaryDate=datetime.datetime.strptime(item_expiary_date,'%Y-%m-%d')                    
                        if item_expiaryDate<currentDate:
                            dateFlag=False                    
                    except:
                        dateFlag=False
                        
                    if dateFlag==False:
                        error_data=row_data+'(Invalid Expiry Date)\n'
                        error_str=error_str+error_data
                        count_error+=1
                        continue
                        
                    #----------- check valid item
                    name=''
                    item_unit=''
                    item_carton=''
                    tp_price=0
                    valid_item=False  
                    valid_item_batch=True
                    duplicate_item=False
                    
                    for i in range(len(item_list_table)):
                        myRowData=item_list_table[i]                                
                        item_id=myRowData['item_id']                        
                        if (str(item_id).strip()==str(item_id_value).strip()):
                            name=myRowData['name']
                            tp_price=myRowData['price']
                            item_unit=myRowData['unit_type']
                            item_carton=myRowData['item_carton']                               
                            valid_item=True
                            break
                    
                    #-----------------                
                    if valid_item==False:
                        error_data=row_data+'(Invalid Item ID)\n'
                        error_str=error_str+error_data
                        count_error+=1
                        continue
                    else:
                        itemBatchRows = db((db.sm_item_batch.cid == c_id) & (db.sm_item_batch.item_id == item_id_value) & (db.sm_item_batch.batch_id == item_batchid_value)).select(db.sm_item_batch.item_id,db.sm_item_batch.expiary_date,limitby=(0,1))
                        if not itemBatchRows:
                        #     item_expiaryDate=datetime.datetime.strptime(str(itemBatchRows[0].expiary_date),'%Y-%m-%d')
                        #     if item_expiaryDate<currentDate:
                              valid_item_batch=False
                        # else:
                        #     #insert into itembatch and stock balance
                        #     db.sm_item_batch.insert(cid=c_id,item_id=item_id_value,name=name,batch_id=item_batchid_value,expiary_date=item_expiaryDate)
                        #
                        #     insertRecords="insert into sm_depot_stock_balance(cid,depot_id,store_id,store_name,item_id,batch_id,expiary_date,quantity)(select cid,depot_id,store_id,store_name,'"+str(item_id_value)+"','"+str(item_batchid_value)+"','"+str(item_expiaryDate)+"',0 from sm_depot_store where cid='"+c_id+"')"
                        #     db.executesql(insertRecords)
                            
                        if valid_item_batch==False:
                            error_data=row_data+'(Invalid Batch)\n' #Existing Item Batch Expiry Date over
                            error_str=error_str+error_data
                            count_error+=1
                            continue
                        else:                               
                            existRecords=db((db.sm_receive.cid==c_id) & (db.sm_receive.depot_id==req_depot_id)& (db.sm_receive.sl==reqSl)&(db.sm_receive.item_id==item_id_value)&(db.sm_receive.batch_id==item_batchid_value)).select(db.sm_receive.id,db.sm_receive.item_id,limitby=(0,1))
                            if existRecords:
                                error_data=row_data+'(already exist)\n'
                                error_str=error_str+error_data
                                count_error+=1
                                continue
                            else:
                                itemIdBatchId=item_id_value+'-'+item_batchid_value
                                if itemIdBatchId in itemIdBatchIdList:
                                    error_data=row_data+'(duplicate in excel)\n'
                                    error_str=error_str+error_data
                                    count_error+=1
                                    continue
                                else:                                           
                                    try:                                    
                                        ins_dict= {'cid':c_id,'depot_id':req_depot_id,'depot_name':depot_name,'sl':reqSl,'store_id':store_id,'store_name':store_name,'receive_from':receive_from,'depot_from_name':depot_from_name,'receive_date':receive_date,'note':req_note,'transaction_cause':transaction_cause,
                                               'item_id':item_id_value,'item_name':name,'batch_id':item_batchid_value,'quantity':item_qty_value,'bonus_qty':item_bonus_qty_value,'dist_rate':tp_price,'item_unit':item_unit,'item_carton':item_carton,'expiary_date':item_expiaryDate,'ym_date':ym_date}
                                        
                                        ins_list.append(ins_dict)
                                        
                                        count_inserted+=1
                                        itemIdBatchIdList.append(itemIdBatchId)
                                        
                                        if headFlag==False:
                                            db.sm_receive_head.insert(cid=c_id,depot_id=req_depot_id,depot_name=depot_name,sl=reqSl,store_id=store_id,store_name=store_name,ref_sl=0,receive_from=receive_from,depot_from_name=depot_from_name,receive_date=receive_date,total_discount=0,ym_date=ym_date,transaction_cause=transaction_cause,note=req_note)
                                            headFlag=True
                                            
                                    except:
                                        error_data=row_data+'(process error)\n'
                                        error_str=error_str+error_data
                                        count_error+=1
                                        continue
                                    
            if error_str=='':
                error_str='No error'
            #Bulk insert
            inCountList=db.sm_receive.bulk_insert(ins_list)             
            
            redirect(URL(c='depot',f='depot_stock_receive',vars=dict(req_sl=reqSl,count_inserted=count_inserted,count_error=count_error,error_str=error_str,total_row=total_row)))
        
    # IMPORT FROM ISSUE
    elif btn_import_req:
        maxSl=0
        
#        try:
        req_depot_id=str(request.vars.depot_id).split('|')[0]
        reqSl=int(request.vars.sl)
        
        store_idname=str(request.vars.store_id)
        
        receive_from=str(request.vars.receive_from).split('|')[0]
        receive_date=request.vars.receive_date
        ym_date=str(receive_date)[0:7]+'-01'#Save as first date of month 
        req_note=request.vars.note
        transaction_cause=request.vars.transaction_cause
        
        total_discount=0    #request.vars.total_discount
        
        try:
            ref_sl=int(request.vars.ref_sl)   
        except:
            ref_sl=0
            
        if reqSl==0 :
            if store_idname!='':
                store_id=str(store_idname).split('|')[0]
                store_name=str(store_idname).split('|')[1]
            
                depot_category=''
                depotRows=db((db.sm_depot.cid==c_id) & (db.sm_depot.depot_id==receive_from)).select(db.sm_depot.depot_id,db.sm_depot.name,db.sm_depot.depot_category,limitby=(0,1))
                if depotRows:
                    depot_category=str(depotRows[0].depot_category).strip().upper()
                
    #            if (not(receive_from=='' or depot_category=='EXTERNAL') and receive_date!='' and ref_sl > 0):
                if (not(receive_from=='') and receive_date!='' and ref_sl > 0):
                    
                    recRows=db((db.sm_receive.cid==c_id)& (db.sm_receive.depot_id==req_depot_id) & (db.sm_receive.ref_sl==ref_sl)).select(db.sm_receive.ref_sl,limitby=(0,1))
                    if not recRows:
                        
                        reqRecords=db((db.sm_issue.cid==c_id) & (db.sm_issue.issued_to==req_depot_id) & (db.sm_issue.depot_id==receive_from)&(db.sm_issue.sl==ref_sl)&(db.sm_issue.status=='Posted')&(db.sm_issue.issue_process_status=='Issued')).select(db.sm_issue.ALL,orderby=db.sm_issue.item_name)
                        #-Get max sl from depot table
                        if reqRecords:
                            records=db((db.sm_depot.cid==c_id) & (db.sm_depot.depot_id==req_depot_id)).select(db.sm_depot.id,db.sm_depot.receive_sl,limitby=(0,1))
                            if records:
                                sl=records[0].receive_sl
                                maxSl=int(sl)+1
                            else:
                                maxSl=1
                            
                            #----------- UPDATE SL IN DEPOT
                            records[0].update_record(receive_sl=maxSl)
                            
                            #---------------                        
                            reqDict={}
                            insList=[]
                            headFlag=False
                            #Create item list from item table
                            
                            for row in reqRecords:
                                from_depot=row.depot_id
                                depot_from_name=row.depot_name
                                
                                sl=row.sl
                                issued_to=row.issued_to
                                depot_name=row.depot_to_name
                                
                                note=row.note
                                item_id=row.item_id
                                item_name=row.item_name
                                quantity=row.quantity
                                bonus_qty=row.bonus_qty
                                dist_rate=row.dist_rate
                                short_note=row.short_note
                                total_discount=row.total_discount
                                
                                batch_id=row.batch_id
                                
                                item_unit=row.item_unit
                                item_carton=row.item_carton
                                expiary_date=row.expiary_date
                                
                                reqDict={'cid':c_id,'depot_id':issued_to,'depot_name':depot_name,'sl':maxSl,'store_id':store_id,'store_name':store_name,'receive_from':from_depot,'depot_from_name':depot_from_name,'receive_date':receive_date,'total_discount':total_discount,'ref_sl':ref_sl,'transaction_cause':transaction_cause,
                                         'item_id':item_id,'item_name':item_name,'quantity':quantity,'bonus_qty':bonus_qty,'dist_rate':dist_rate,'item_unit':item_unit,'item_carton':item_carton,'expiary_date':expiary_date,'short_note':short_note,'ym_date':ym_date,'batch_id':batch_id}
                                insList.append(reqDict)
                                
                                if headFlag==False:
                                    db.sm_receive_head.insert(cid=c_id,depot_id=issued_to,depot_name=depot_name,sl=maxSl,store_id=store_id,store_name=store_name,ref_sl=ref_sl,receive_from=from_depot,depot_from_name=depot_from_name,receive_date=receive_date,total_discount=total_discount,ym_date=ym_date,transaction_cause=transaction_cause)
                                    headFlag=True
                                
                           #Bulk insert in recieve     
                            rows=db.sm_receive.bulk_insert(insList)
                            #Insert in recieve head table
                            db((db.sm_issue_head.cid==c_id) & (db.sm_issue_head.issued_to==req_depot_id) & (db.sm_issue_head.depot_id==receive_from)&(db.sm_issue_head.sl==ref_sl)&(db.sm_issue_head.status=='Posted')).update(issue_process_status='Received')
                            db((db.sm_issue.cid==c_id) & (db.sm_issue.issued_to==req_depot_id) & (db.sm_issue.depot_id==receive_from)&(db.sm_issue.sl==ref_sl)&(db.sm_issue.status=='Posted')).update(issue_process_status='Received')
                            
                            session.flash='successfully imported'
                        else:
                            session.flash='Reference not available!'
                    else:
                        session.flash='already imported!'
                else:
                    session.flash='Receive from Depot/External,Date and Reference needed!'
            else:
                session.flash='Required Store To'
        else:
            session.flash='need new issue!'
            
        if maxSl > 0:
            redirect(URL(c='depot',f='depot_stock_receive',vars=dict(req_sl=maxSl)))
        else:
            redirect(URL(c='depot',f='depot_stock_receive',vars=dict(req_sl=reqSl)))
              
    #---------------- SAVE ITEM/ REPLACE IF EXIST
    form =SQLFORM(db.sm_receive,
                  fields=['depot_id','sl','store_id','receive_from','ref_sl','receive_date','status','receive_process_status','transaction_cause','item_id','item_name','batch_id','quantity','dist_rate','note','ref_sl'],
                  submit_button='Save'   
                  )
    #insert with validation
    form.vars.cid=c_id
    form.vars.quantity=''
    
    if form.accepts(request.vars,session,onvalidation=validation_receive):
       sl=form.vars.sl
       depot_id=form.vars.depot_id
       depot_name=form.vars.depot_name
       receive_from=form.vars.receive_from
       depot_from_name=form.vars.depot_from_name
       receive_date=form.vars.receive_date
       ym_date=str(receive_date)[0:7]+'-01'
       note=form.vars.note
       discount=form.vars.total_discount
       store_id=form.vars.store_id
       store_name=form.vars.store_name
       
       ref_sl=form.vars.ref_sl
       transaction_cause=form.vars.transaction_cause
       
       #------head Insert/update
       headRows=db((db.sm_receive_head.cid==c_id)& (db.sm_receive_head.depot_id==depot_id) & (db.sm_receive_head.sl==sl)).select(db.sm_receive_head.id,db.sm_receive_head.depot_id,limitby=(0,1))
       if headRows:
            headRows[0].update_record(receive_from=receive_from,receive_date=receive_date,note=note,transaction_cause=transaction_cause,total_discount=discount,ym_date=ym_date)
       else:
           db.sm_receive_head.insert(cid=c_id,depot_id=depot_id,depot_name=depot_name,sl=sl,store_id=store_id,store_name=store_name,receive_from=receive_from,depot_from_name=depot_from_name,ref_sl=ref_sl,receive_date=receive_date,note=note,transaction_cause=transaction_cause,total_discount=discount,ym_date=ym_date)
           
       #-----------UPDATE SAME SL VALUE
       db((db.sm_receive.cid==c_id)& (db.sm_receive.depot_id==depot_id) & (db.sm_receive.sl==sl)).update(receive_from=receive_from,depot_from_name=depot_from_name,receive_date=receive_date,note=note,transaction_cause=transaction_cause,total_discount=discount,ym_date=ym_date)
       
       #-----
       #session.flash = ''
       redirect(URL(c='depot',f='depot_stock_receive',vars=dict(req_sl=sl)))
       
#    elif form.errors:
#        redirect(URL(c='depot',f='depot_stock_receive',vars=dict(req_sl=form.vars.sl)))
    
    elif form.errors:
        for fieldname in form.errors:
            response.flash = form.errors[fieldname]
            break
    #  ---------------------SHOW FIELD VALUE
    
    depot_name=''
    depot_from_name=''
    
    req_sl=request.vars.req_sl    
    depotid=request.vars.depotid 
    if depotid=='' or depotid==None:
        depot_id=session.depot_id
        depot_name=session.user_depot_name
    else:
        depot_id=depotid
        
    sl=0
    status='Draft'
    receive_process_status='Received'
    receive_from=''
    receive_date=current_date
    note=''  
    discount=0  
    ref_sl=0
    store_id=''
    store_name=''
    transaction_cause=''
    records=db((db.sm_receive.cid==c_id)& (db.sm_receive.depot_id==depot_id) & (db.sm_receive.sl==req_sl)).select(db.sm_receive.ALL,orderby=db.sm_receive.item_name)
    for rec in records:
        depot_id=rec.depot_id
        depot_name=rec.depot_name
        sl=rec.sl
        status=rec.status
        receive_process_status=rec.receive_process_status
        receive_from=rec.receive_from
        depot_from_name=rec.depot_from_name
        receive_date=rec.receive_date
        note=rec.note
        discount=rec.total_discount
        ref_sl=rec.ref_sl
        store_id=rec.store_id
        store_name=rec.store_name   
        transaction_cause=rec.transaction_cause
        break
        
    #-------------------
    reqRecords=''
    # if receive_from=='':
    #     #----------------- DEPOT IN COMBO
    #     #reqRecords=db((db.sm_depot_settings.cid==c_id) & (db.sm_depot_settings.depot_id==session.depot_id)& (db.sm_depot_settings.from_to_type=='Receive') & (db.sm_depot.cid==c_id) & (db.sm_depot.depot_id==db.sm_depot_settings.depot_id_from_to) ).select(db.sm_depot_settings.depot_id_from_to,db.sm_depot.name,groupby=db.sm_depot.depot_id ,orderby=db.sm_depot_settings.depot_id_from_to)
    #     reqRecords=db((db.sm_depot.cid==c_id) & (db.sm_depot.depot_id!=session.depot_id)).select(db.sm_depot.depot_id,db.sm_depot.name,orderby=db.sm_depot.name)
    
    disputeSl=0
    disputeRow=db((db.sm_transaction_dispute_head.cid==c_id)& (db.sm_transaction_dispute_head.depot_id==depot_id) & (db.sm_transaction_dispute_head.recieve_sl==sl)).select(db.sm_transaction_dispute_head.sl,limitby=(0,1))
    if disputeRow:
        disputeSl=disputeRow[0].sl
    
    storeRecords=''
    if sl==0:
        storeRecords=db((db.sm_depot_store.cid==c_id) & (db.sm_depot_store.depot_id==depot_id)& (db.sm_depot_store.store_type=='SALES')).select(db.sm_depot_store.store_id,db.sm_depot_store.store_name,orderby=db.sm_depot_store.store_name)
    
    #-------------------    
    refRecords=''
    if transaction_cause=='':
        refRecords=db((db.sm_category_type.cid==c_id) & (db.sm_category_type.type_name=='RECEIVE_CAUSE')).select(db.sm_category_type.cat_type_id,orderby=db.sm_category_type.cat_type_id)
        
    return dict(form=form,reqRecords=reqRecords,records=records,storeRecords=storeRecords,depot_id=depot_id,depot_name=depot_name,sl=sl,store_id=store_id,store_name=store_name,receive_from=receive_from,depot_from_name=depot_from_name,receive_date=receive_date,status=status,receive_process_status=receive_process_status,note=note,
                transaction_cause=transaction_cause,refRecords=refRecords,discount=discount,ref_sl=ref_sl,count_inserted=count_inserted,count_error=count_error,error_str=error_str,total_row=total_row,access_permission=access_permission,access_permission_view=access_permission_view,disputeSl=disputeSl)

#----------------- Show pending Issue
def show_pending_issue():
    #----------Task assaign----------
    task_id='rm_stock_receive_manage'
    task_id_view='rm_stock_receive_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL('default','home')) 
    
    response.title='Pending Transfer (Branch To Branch)'
    depotId=request.vars.depotId
    
    if depotId:
        records=db((db.sm_issue_head.cid==session.cid) & (db.sm_issue_head.issued_to==depotId) &(db.sm_issue_head.status=='Posted')&(db.sm_issue_head.issue_process_status=='Issued')).select(db.sm_issue_head.ALL,orderby=db.sm_issue_head.sl)
    else:
        if session.user_type=='Depot':
            records=db((db.sm_issue_head.cid==session.cid) & (db.sm_issue_head.issued_to==session.depot_id) &(db.sm_issue_head.status=='Posted')&(db.sm_issue_head.issue_process_status=='Issued')).select(db.sm_issue_head.ALL,orderby=db.sm_issue_head.sl)
        else:
            records=db((db.sm_issue_head.cid==session.cid) &(db.sm_issue_head.status=='Posted')&(db.sm_issue_head.issue_process_status=='Issued')).select(db.sm_issue_head.ALL,orderby=db.sm_issue_head.sl)
    
    return dict(records=records)


#=================== Delete item
#Delete items from recieve
def delete_update_receive_item():
    c_id=session.cid
    
    btn_delete=request.vars.btn_delete
    btn_update=request.vars.btn_update
    
    req_depot=request.args(0)
    req_sl=request.args(1)    
    req_item=request.args(2)
    rowid=request.args(3)
    
    if btn_delete:
        countRecords=db((db.sm_receive.cid==c_id)& (db.sm_receive.depot_id==req_depot) & (db.sm_receive.sl==req_sl)).count()
        if int(countRecords)==1:
            session.flash='At least one item needs in a receive, You can cancel if required!'
        else:
            db((db.sm_receive.cid==c_id) & (db.sm_receive.depot_id==req_depot) & (db.sm_receive.sl==req_sl) & (db.sm_receive.item_id==req_item) & (db.sm_receive.id==rowid)).delete()
            
        redirect(URL(c='depot',f='depot_stock_receive',vars=dict(req_sl=req_sl)))
        
    if btn_update:
        batchIdVar='batch_id_update_'+str(req_item)+'_'+str(rowid)
        batchId=str(request.vars[batchIdVar]).strip().upper().split('|')[0]
        item_qty=request.vars.item_qty       
        if batchId=='':
            session.flash='Required Batch ID'
        else:
            try:
                item_qty=int(item_qty)
                if item_qty<=0:
                    item_qty=0
            except:
                item_qty=0
            
            
            if item_qty==0:
                session.flash='Invalid Qty'
            else:            
                itemBatchRows = db((db.sm_item_batch.cid == c_id) & (db.sm_item_batch.item_id == req_item) & (db.sm_item_batch.batch_id == batchId) & (db.sm_item_batch.expiary_date >= current_date)).select(db.sm_item_batch.item_id,db.sm_item_batch.expiary_date,limitby=(0,1))
                if not itemBatchRows:
                    session.flash='Invalid Item Batch ID'
                else:
                    expiary_date=itemBatchRows[0].expiary_date
                    
                    db((db.sm_receive.cid==c_id) & (db.sm_receive.depot_id==req_depot) & (db.sm_receive.sl==req_sl)& (db.sm_receive.item_id==req_item) & (db.sm_receive.id==rowid)).update(batch_id=batchId,quantity=item_qty,expiary_date=expiary_date)
                    session.flash='Updated successfully'
                    
        redirect(URL(c='depot',f='depot_stock_receive',vars=dict(req_sl=req_sl)))
    #  ---------------------
    return dict()

#=================== Post and Cancel
#Update status of receive as posted or cancel
def post_cancel_receive():
    c_id=session.cid
    
    btn_post=request.vars.btn_post
    btn_cancel=request.vars.btn_cancel
    
    req_depot=request.args(0)
    req_sl=request.args(1)
    ref_sl=int(request.args(2))   
    
    if btn_post:
        countRecords=db((db.sm_receive.cid==c_id)& (db.sm_receive.depot_id==req_depot) & (db.sm_receive.sl==req_sl)).count()
        if int(countRecords)==0:
            session.flash='At least one item needs in a receive!'
        else:
            batchIdrows=db((db.sm_receive.cid==c_id)& (db.sm_receive.depot_id==req_depot) & (db.sm_receive.sl==req_sl) & (db.sm_receive.batch_id=='')).select(db.sm_receive.id,limitby=(0,1))
            if batchIdrows:
                session.flash = 'Required Batch ID for all Items'
            else:
                #--------------------------- chcek stock cron flag
                autDelCronRows=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==req_depot)&(db.sm_depot.auto_del_cron_flag==0)).select(db.sm_depot.id,db.sm_depot.cid,limitby=(0,1))
                if not autDelCronRows:
                    session.flash='One process running, please try again'
                else:
                    autDelCronRows[0].update_record(auto_del_cron_flag=1)
                    #---------------------
                    
                    #--------------------------------
                    issued_to=''
                    totalAmount=0
                    total_discount=0
                    if session.primaryLedgerCreate=='YES':
                        #-----------------------
                        rows=db((db.sm_receive.cid==c_id)& (db.sm_receive.depot_id==req_depot) & (db.sm_receive.sl==req_sl)).select(db.sm_receive.receive_from,db.sm_receive.quantity,db.sm_receive.dist_rate,db.sm_receive.total_discount)            
                        for row in rows:
                            receive_from=row.receive_from
                            quantity=int(row.quantity)
                            dist_rate=float(row.dist_rate)
                            total_discount=float(row.total_discount)    
                                        
                            totalAmount+=dist_rate*quantity
                        
                        totalAmount=totalAmount-total_discount
                        
                        #--------------------- depot balance
                        #format:cid<fdfd>TodepotID<fdfd>FromDepotID<fdfd>typeName(keyword)<fdfd>paymtent_amount
                        
                        #------- condition used for IMPORT/FACTORY/OPENING
                        depotRows=db((db.sm_depot.cid==c_id) & (db.sm_depot.depot_id==receive_from)&(db.sm_depot.depot_category!='EXTERNAL')).select(db.sm_depot.depot_id,limitby=(0,1))
                        if depotRows:
                            strData2=str(c_id)+'<fdfd>RECEIVE<fdfd>'+str(req_sl)+'<fdfd>'+str(datetime_fixed)+'<fdfd>'+str(req_depot)+'-'+str(req_sl)+'<fdfd>DPT-'+str(receive_from)+'<fdfd>DPT-'+str(req_depot)+'<fdfd>'+str(totalAmount)              
                        else:
                            strData2=str(c_id)+'<fdfd>ISSUERECEIVE<fdfd>'+str(req_sl)+'<fdfd>'+str(datetime_fixed)+'<fdfd>'+str(req_depot)+'-'+str(req_sl)+'<fdfd>DPT-'+str(receive_from)+'<fdfd>DPT-'+str(req_depot)+'<fdfd>'+str(totalAmount)
                            
                            # call update depot stock (type,cid,depotid,sl)
                            # update_depot_stock('ISSUE',c_id,receive_from,req_sl)
                            
                            
                        resStr2=set_balance_transaction(strData2)  # call function
                        resStrList2=resStr2.split('<sep>',resStr2.count('<sep>'))
                        flag2=resStrList2[0]
                        msg2=resStrList2[1]
                    else:
                        flag2='True'
                    
                    
                    #----------------------------
                    if flag2=='True':
                        db((db.sm_receive_head.cid==c_id)& (db.sm_receive_head.depot_id==req_depot) & (db.sm_receive_head.sl==req_sl)).update(status='Posted')
                        db((db.sm_receive.cid==c_id)& (db.sm_receive.depot_id==req_depot) & (db.sm_receive.sl==req_sl)).update(status='Posted')
                        session.flash='Posted successfully'
                        
                        # For Transit Dispute
                        depot_recieve_confirm(req_depot,req_sl,ref_sl)
                        
                        # call update depot stock (type,cid,depotid,sl)
                        update_depot_stock('RECEIVE',c_id,req_depot,req_sl)
                        
                    else:
                        db.rollback()
                        session.flash = 'process error:103'                    
                        #------------------------------
                        
                    #---------------------
                    autDelCronRows[0].update_record(auto_del_cron_flag=0)
                    #db.commit()
                    #--------------
                
        redirect(URL(c='depot',f='depot_stock_receive',vars=dict(req_sl=req_sl)))
        
    elif btn_cancel:
        countRecords=db((db.sm_receive.cid==c_id)& (db.sm_receive.depot_id==req_depot) & (db.sm_receive.sl==req_sl)).count()
        if int(countRecords)==0:
            session.flash='At least one item needs in a receive!'
        else:
            db((db.sm_receive_head.cid==c_id)& (db.sm_receive_head.depot_id==req_depot) & (db.sm_receive_head.sl==req_sl)).update(status='Cancelled')
            db((db.sm_receive.cid==c_id)& (db.sm_receive.depot_id==req_depot) & (db.sm_receive.sl==req_sl)).update(status='Cancelled')

        redirect(URL(c='depot',f='depot_stock_receive',vars=dict(req_sl=req_sl)))

    return dict()


##=========================================== Damage List ===============================
#---------------catagory-----------------------
def validation_damage_reference(form):    
    category_id=str(request.vars.cat_type_id).strip().title()
    if category_id!='':
        rows_check=db((db.sm_category_type.cid==session.cid) & (db.sm_category_type.type_name=='ADJUSTMENT_TYPE') &(db.sm_category_type.cat_type_id==category_id)).select(db.sm_category_type.cat_type_id,limitby=(0,1))
        if rows_check:
            form.errors.cat_type_id=''
            response.flash = 'Already exist, Please choose a new'
        else:
            form.vars.cid=session.cid
            form.vars.type_name='ADJUSTMENT_TYPE'
            form.vars.cat_type_id=category_id
def damage_reference():    
    task_id='rm_utility_manage'
    access_permission=check_role(task_id)
    if (access_permission==False and session.user_type=="Admin"):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))
        
    response.title='Internal Adjustment Cause'
    
    cid=session.cid
    
    #---------------------  
    db.sm_category_type.field1.requires=IS_IN_SET(('Increase','Decrease'))  
    form =SQLFORM(db.sm_category_type,
                  fields=['cat_type_id','field1'],
                  submit_button='Save'
                  )
    
    if form.accepts(request.vars,session,onvalidation=validation_damage_reference):
        response.flash = 'Saved Successfully'
        
    #--------------------------------
    btn_delete=request.vars.btn_delete
    record_id=request.vars.record_id
    if btn_delete:
        record_id=request.args[1]
        category_id=''
        catRow=db((db.sm_category_type.cid == cid)&(db.sm_category_type.id==record_id)&(db.sm_category_type.type_name=='ADJUSTMENT_TYPE')).select(db.sm_category_type.cat_type_id,limitby=(0,1))
        if not catRow:
            response.flash='Invalid request'
        else:
            category_id=catRow[0].cat_type_id
            
            records=db((db.sm_damage_head.cid==cid) & (db.sm_damage_head.adjustment_reference==category_id)).select(db.sm_damage_head.adjustment_type,limitby=(0,1))
            if records:
                response.flash='Already used in Adjustment'            
            else:
                db((db.sm_category_type.cid == cid)&(db.sm_category_type.id == record_id)&(db.sm_category_type.type_name=='ADJUSTMENT_TYPE')).delete()
                response.flash='Deleted successfully'
                
    #--------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=session.items_per_page
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #--------end paging
    
    records=db((db.sm_category_type.cid==cid)&(db.sm_category_type.type_name=='ADJUSTMENT_TYPE')).select(db.sm_category_type.ALL,orderby=db.sm_category_type.cat_type_id,limitby=limitby)
    
    return dict(form=form,records=records,page=page,items_per_page=items_per_page,access_permission=access_permission)
#---------------


def depot_stock_damage_list():
    #----------Task assaign----------
    task_id='rm_stock_damage_manage'
    task_id_view='rm_stock_damage_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))   
    
    response.title='Internal Transfer List'    
    #   --------------------- 
    c_id=session.cid
    
    #  ---------------filter-------    
    btn_filter_damage=request.vars.btn_filter
    btn_all=request.vars.btn_all
    depot_id_value=str(request.vars.depot_id_value).strip()
    search_type=str(request.vars.search_type).strip()
    search_value=str(request.vars.search_value).strip()
    
    reqPage=len(request.args)
    #Set text for filter
    if btn_filter_damage:
        session.btn_filter_damage=btn_filter_damage
        session.depot_id_value_dam=depot_id_value 
        session.search_type_dam=search_type
        session.search_value_dam=search_value
        
        #Check SL is numeric or not
        if (session.search_type_dam=='SL'):
            sl=0
            if not(session.search_value_dam=='' or session.search_value_dam==None):
                try:       
                    sl=int(session.search_value_dam)
                    session.search_value_dam=sl
                except:
                    session.search_value_dam=sl
                    response.flash='sl needs number value'
            else:
                session.search_value_dam=sl
                
        reqPage=0
        
    elif btn_all:
        session.btn_filter_damage=None
        session.depot_id_value_dam=None
        session.search_type_dam=None
        session.search_value_dam=None
        reqPage=0
        
    #--------paging
    if reqPage:
        page=int(request.args[0])
    else:
        page=0
    items_per_page=session.items_per_page*10
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #--------end paging  
    
    qset=db()
    qset=qset(db.sm_damage_head.cid==c_id)    
    qset=qset(db.sm_damage_head.transfer_type=='ADJUSTMENT')
    
    if (session.user_type=='Depot'):
        qset=qset(db.sm_damage_head.depot_id==session.depot_id)
    
    #Set query bsed on search type
    if (session.btn_filter_damage):
        if (session.user_type!='Depot'):
            if not (session.depot_id_value_dam=='' or session.depot_id_value_dam==None):
                searchValue=str(session.depot_id_value_dam).split('|')[0]
                qset=qset(db.sm_damage_head.depot_id==searchValue)
            else:
                qset=qset(db.sm_damage_head.depot_id!='')
                
        #------------
        if (session.search_type_dam=='SL'):
            qset=qset(db.sm_damage_head.type_sl==session.search_value_dam)
        
        elif (session.search_type_dam=='DATE'):
            qset=qset(db.sm_damage_head.damage_date==session.search_value_dam)
        
        elif (session.search_type_dam=='STATUS'):
            qset=qset(db.sm_damage_head.status==session.search_value_dam)
        
        elif (session.search_type_dam=='UserID'):
            qset=qset(db.sm_damage_head.updated_by==session.search_value_dam)
        
        
    records=qset.select(db.sm_damage_head.ALL,orderby=~db.sm_damage_head.id,limitby=limitby)
    
    #------------------------------------------------
    search_form =SQLFORM(db.sm_search_date)
    #-------------
    
    return dict(search_form=search_form,records=records,page=page,items_per_page=items_per_page,access_permission=access_permission,access_permission_view=access_permission_view)

#======================= Stock Damage 
#Validation damage
def validation_damage(form):
    c_id=session.cid   
    
    depot_id=str(form.vars.depot_id).split('|')[0]
    depot_name=str(form.vars.depot_id).split('|')[1]
    
    store_idname=str(form.vars.store_id)
    store_to_idname=str(form.vars.store_id_to)
    
    item_id=str(form.vars.item_id)
    item_name=str(form.vars.item_name)
    quantity=str(form.vars.quantity)
    dist_rate=0     #str(form.vars.dist_rate)
    short_note=''   #str(form.vars.short_note)
    
    typeList=str(request.vars.adjustment_reference).split('|')
    
    batch_id=str(form.vars.batch_id).strip().split('|')[0]
    
    if store_idname=='':
        form.errors.store_id=''
        response.flash="Required From Store"
    else:
        store_id=str(store_idname).split('|')[0]
        store_name=str(store_idname).split('|')[1]
        
        store_id_to=''
        store_name_to=''
        
        if not(store_to_idname=='' or store_to_idname=='|'):
            store_id_to=str(store_to_idname).split('|')[0]
            store_name_to=str(store_to_idname).split('|')[1]
            
        if store_id==store_id_to:
            form.errors.store_id=''
            response.flash="Required accurate store selection"
        else:
            if len(typeList)!=2:
                form.errors.adjustment_type=''
                response.flash="Required Cause"
            else:
                adjustment_reference=typeList[0]
                adjustment_type=typeList[1]
                
                itemRows = db((db.sm_item.cid == c_id)&(db.sm_item.item_id == item_id)).select(db.sm_item.name,db.sm_item.price,db.sm_item.unit_type,db.sm_item.item_carton,limitby=(0,1))
                if not itemRows:
                    form.errors.item_id=''
                    response.flash="Invalid Item ID"
                else:                    
                    dist_rate=itemRows[0].price
                    unit_type=itemRows[0].unit_type
                    item_carton=itemRows[0].item_carton
                    
                    itemBatchRows = db((db.sm_item_batch.cid == c_id) & (db.sm_item_batch.item_id == item_id) & (db.sm_item_batch.batch_id == batch_id)).select(db.sm_item_batch.item_id,db.sm_item_batch.expiary_date,limitby=(0,1))
                    if not itemBatchRows:
                        form.errors.batch_id=''
                        response.flash="Invalid Item Batch ID"
                    else:
                        expiary_date=itemBatchRows[0].expiary_date
                        
                        sl=int(form.vars.sl)
                        ym_date=str(form.vars.damage_date)[0:7]+'-01'
                        
                        existRecords=db((db.sm_damage.cid==c_id) & (db.sm_damage.depot_id==depot_id)& (db.sm_damage.sl==sl) & (db.sm_damage.item_id==item_id) & (db.sm_damage.batch_id==batch_id)).select(db.sm_damage.id,db.sm_damage.item_id,limitby=(0,1))
                        if existRecords:
                            existRecords[0].update_record(item_name=item_name,quantity=quantity,dist_rate=dist_rate,short_note=short_note)        
                            form.errors.short_note=''  
                            response.flash='Item replaced!'      
                            
                        elif int(quantity)<=0:
                            form.errors.quantity=''
                            response.flash='need item quantity!'
                            
                        else:
                            if sl==0:
                                maxSl=1
                                records=db((db.sm_depot.cid==c_id) & (db.sm_depot.depot_id==depot_id)).select(db.sm_depot.id,db.sm_depot.damage_sl,limitby=(0,1))
                                if records:
                                    sl=records[0].damage_sl
                                    maxSl=int(sl)+1
                                #-------- update sl in depot
                                records[0].update_record(damage_sl=maxSl)
                                
                                form.vars.sl=maxSl
                                
                                #-------------
                                typeSl=1
                                typeRecords=db((db.sm_damage_head.cid==c_id) & (db.sm_damage_head.depot_id==depot_id) & (db.sm_damage_head.transfer_type=='ADJUSTMENT')).select(db.sm_damage_head.type_sl,orderby=~db.sm_damage_head.type_sl,limitby=(0,1))
                                if typeRecords:
                                    typeSl=typeRecords[0].type_sl+1
                                
                                form.vars.type_sl=typeSl
                                
                            form.vars.ym_date=ym_date
                            form.vars.depot_id=depot_id
                            form.vars.depot_name=depot_name
                            form.vars.batch_id = batch_id
                            form.vars.dist_rate = dist_rate
                            form.vars.adjustment_reference = adjustment_reference
                            form.vars.adjustment_type = adjustment_type                        
                            form.vars.store_id=store_id
                            form.vars.store_name=store_name
                            form.vars.store_id_to=store_id_to
                            form.vars.store_name_to=store_name_to
                            form.vars.item_unit=unit_type
                            form.vars.item_carton=item_carton
                            form.vars.expiary_date=expiary_date
                            
def depot_stock_damage():
    #----------Task assaign----------
    task_id='rm_stock_damage_manage'
    task_id_view='rm_stock_damage_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))   
        
#   --------------------- 
    response.title='Internal Adjustment'
    c_id=session.cid
    
    #------------------
    btn_update=request.vars.btn_update
    
    #------------------- UPDATE
    if btn_update:
        req_depot_id=str(request.vars.depot_id).split('|')[0]
        reqSl=request.vars.sl
        req_date=request.vars.damage_date
        ym_date=str(req_date)[0:7]+'-01'#Save as first day of month
        req_note=request.vars.note
        
        typeList=str(request.vars.adjustment_reference).split('|')
        adjustment_reference=''
        adjustment_type=''
        if len(typeList)==2:            
            adjustment_reference=typeList[0]
            adjustment_type=typeList[1]
            
        if req_date!='':
            db((db.sm_damage_head.cid==c_id)& (db.sm_damage_head.depot_id==req_depot_id) & (db.sm_damage_head.sl==reqSl)).update(damage_date=req_date,note=req_note,ym_date=ym_date,adjustment_reference=adjustment_reference,adjustment_type=adjustment_type)
            db((db.sm_damage.cid==c_id)& (db.sm_damage.depot_id==req_depot_id) & (db.sm_damage.sl==reqSl)).update(damage_date=req_date,note=req_note,ym_date=ym_date,adjustment_reference=adjustment_reference,adjustment_type=adjustment_type)
            session.flash='Updated successfully'
            redirect(URL(c='depot',f='depot_stock_damage',vars=dict(req_sl=reqSl)))
            
    #-------- SAVE ITEM/ REPLACED IF EXIST
    form =SQLFORM(db.sm_damage,
                  fields=['depot_id','sl','type_sl','store_id','store_id_to','damage_date','status','item_id','item_name','batch_id','quantity','dist_rate','note','adjustment_type'],
                  submit_button='Save'
                  )
    form.vars.cid=c_id
    form.vars.transfer_type='ADJUSTMENT'
    form.vars.quantity=''
    
    if form.accepts(request.vars,session,onvalidation=validation_damage):
        depot_id=form.vars.depot_id
        depot_name=form.vars.depot_name
        
        sl=form.vars.sl
        req_date=form.vars.damage_date
        ym_date=str(req_date)[0:7]+'-01'
        
        note=form.vars.note
        
        type=request.vars.adjustment_type
        
        adjustment_reference=form.vars.adjustment_reference
        adjustment_type=form.vars.adjustment_type 
        
        store_id=form.vars.store_id
        store_name=form.vars.store_name
        
        store_id_to=form.vars.store_id_to
        store_name_to=form.vars.store_name_to
        
        transfer_type=form.vars.transfer_type
        type_sl=form.vars.type_sl
        
        #---------- head insert/update
        headRows=db((db.sm_damage_head.cid==c_id)& (db.sm_damage_head.depot_id==depot_id) & (db.sm_damage_head.sl==sl)).select(db.sm_damage_head.id,db.sm_damage_head.depot_id,limitby=(0,1))
        if headRows:
             headRows[0].update_record(damage_date=req_date,note=note,ym_date=ym_date,adjustment_reference=adjustment_reference,adjustment_type=adjustment_type)
        else:
            db.sm_damage_head.insert(cid=c_id,depot_id=depot_id,depot_name=depot_name,sl=sl,transfer_type=transfer_type,type_sl=type_sl,store_id=store_id,store_name=store_name,store_id_to=store_id_to,store_name_to=store_name_to,damage_date=req_date,note=note,ym_date=ym_date,adjustment_reference=adjustment_reference,adjustment_type=adjustment_type)
            
        #----------SAME SL DATA UPDATE
        db((db.sm_damage.cid==c_id)& (db.sm_damage.depot_id==depot_id) & (db.sm_damage.sl==sl)).update(damage_date=req_date,note=note,ym_date=ym_date,adjustment_reference=adjustment_reference,adjustment_type=adjustment_type)
        
        session.flash = ''
        redirect(URL(c='depot',f='depot_stock_damage',vars=dict(req_sl=sl)))
        
#    elif form.errors:
#        session.flash=''
#        redirect(URL(c='depot',f='depot_stock_damage',vars=dict(req_sl=form.vars.sl)))
        
    #  --------------------- NEW DAMAGE/SHOW FIELD VALUE
    depot_name=''
    
    req_sl=request.vars.req_sl
    depotid=request.vars.depotid
    if depotid=='' or depotid==None:
        depot_id=session.depot_id
        depot_name=session.user_depot_name
    else:
        depot_id=depotid
        
    sl=0
    type_sl=0
    status='Draft'
    damage_date=current_date
    note=''
    adjustment_reference=''
    adjustment_type=''
    store_id=''
    store_name=''
    store_id_to=''
    store_name_to=''
    records=db((db.sm_damage.cid==c_id)& (db.sm_damage.depot_id==depot_id) & (db.sm_damage.sl==req_sl)).select(db.sm_damage.ALL,orderby=db.sm_damage.item_name)
    for rec in records:
        depot_id=rec.depot_id
        depot_name=rec.depot_name
        sl=rec.sl
        status=rec.status
        damage_date=rec.damage_date
        note=rec.note
        adjustment_reference=rec.adjustment_reference
        adjustment_type=rec.adjustment_type
        store_id=rec.store_id
        store_name=rec.store_name
        store_id_to=rec.store_id_to
        store_name_to=rec.store_name_to    
        type_sl=rec.type_sl
        break
        
    #-------------------    
    refRecords=''
    if adjustment_reference=='':
        refRecords=db((db.sm_category_type.cid==c_id) & (db.sm_category_type.type_name=='ADJUSTMENT_TYPE')).select(db.sm_category_type.cat_type_id,db.sm_category_type.field1,orderby=db.sm_category_type.cat_type_id)
        
    storeRecords=''
    if sl==0:
        storeRecords=db((db.sm_depot_store.cid==c_id) & (db.sm_depot_store.depot_id==depot_id)).select(db.sm_depot_store.store_id,db.sm_depot_store.store_name,orderby=db.sm_depot_store.store_name)
        
    return dict(form=form,records=records,storeRecords=storeRecords,depot_id=depot_id,depot_name=depot_name,sl=sl,type_sl=type_sl,store_id=store_id,store_name=store_name,store_id_to=store_id_to,store_name_to=store_name_to,damage_date=damage_date,status=status,note=note,adjustment_type=adjustment_type,adjustment_reference=adjustment_reference,refRecords=refRecords,access_permission=access_permission,access_permission_view=access_permission_view)


#=================== Delete item
# delete damage if more than one item is a sl
def delete_damage_item():
    c_id=session.cid
    
    btn_delete=request.vars.btn_delete
    
    req_depot=request.args(0)
    req_sl=request.args(1)
    req_item=request.args(2)
    rowid=request.args(3)
    
    if btn_delete:
        countRecords=db((db.sm_damage.cid==c_id)& (db.sm_damage.depot_id==req_depot) & (db.sm_damage.sl==req_sl)).count()
        if int(countRecords)==1:
            session.flash='At least one item needs, You can cancel if required!'
        else:
            db((db.sm_damage.cid==c_id) & (db.sm_damage.depot_id==req_depot) & (db.sm_damage.sl==req_sl)& (db.sm_damage.item_id==req_item)& (db.sm_damage.id==rowid)).delete()
            
        redirect(URL(c='depot',f='depot_stock_damage',vars=dict(req_sl=req_sl)))
    #  ---------------------
    return dict()
    
#=================== Post and Cancel
#Update sattus as post or cancel
def post_cancel_damage():
    c_id=session.cid
    
    btn_post=request.vars.btn_post
    btn_cancel=request.vars.btn_cancel
    
    req_depot=request.args(0)
    req_sl=request.args(1)   
    req_date=request.args(2)    
    
    if btn_post:
        countRecords=db((db.sm_damage.cid==c_id)& (db.sm_damage.depot_id==req_depot) & (db.sm_damage.sl==req_sl)).count()
        if int(countRecords)==0:
            session.flash='At least one item needs!'
        else:
            batchIdrows=db((db.sm_damage.cid==c_id)& (db.sm_damage.depot_id==req_depot) & (db.sm_damage.sl==req_sl) & (db.sm_damage.batch_id=='')).select(db.sm_damage.id,limitby=(0,1))
            if batchIdrows:
                session.flash = 'Required Batch ID for all Items'
            else:
                adjustment_type=''
                damageRow=db((db.sm_damage.cid==c_id)& (db.sm_damage.depot_id==req_depot) & (db.sm_damage.sl==req_sl)).select(db.sm_damage.store_id,db.sm_damage.adjustment_type,limitby=(0,1))
                if damageRow:
                    adjustment_type=damageRow[0].adjustment_type
                    
                #--------------------------- chcek stock cron flag
                autDelCronRows=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==req_depot)&(db.sm_depot.auto_del_cron_flag==0)).select(db.sm_depot.id,db.sm_depot.cid,limitby=(0,1))
                if not autDelCronRows:
                    session.flash='One process running, please try again'
                else:
                    autDelCronRows[0].update_record(auto_del_cron_flag=1)
                    #---------------------
                    
                    itemStrForQty=''
                    if adjustment_type=='Decrease':
                        diffRecords="select dam.item_id as item_id from sm_depot_stock_balance dsb,sm_damage dam  where (dam.cid='"+str(c_id)+"' and dam.depot_id='"+str(req_depot)+"' and dam.sl="+str(req_sl)+" and dsb.cid='"+str(c_id)+"' and dsb.depot_id='"+str(req_depot)+"' and dam.store_id=dsb.store_id and dam.item_id=dsb.item_id and dam.batch_id=dsb.batch_id and (dsb.quantity-dsb.block_qty)<dam.quantity)"
                        diffRowsList=db.executesql(diffRecords,as_dict=True)
                        for i in range(len(diffRowsList)):
                            diffDictData=diffRowsList[i]
                            if itemStrForQty=='':
                                itemStrForQty=diffDictData['item_id']
                            else:
                                itemStrForQty+=','+diffDictData['item_id']
                    
                    if adjustment_type=='Decrease' and itemStrForQty!='':
                        session.flash='Quantity not available for item ID '+str(itemStrForQty)                        
                    else:
                        totalAmount=0
                        
                        flag2='True'
                        #--------------------- depot balance
                        if session.primaryLedgerCreate=='YES':
        #                     rows=db((db.sm_damage.cid==c_id)& (db.sm_damage.depot_id==req_depot) & (db.sm_damage.sl==req_sl)).select(db.sm_damage.ALL,orderby=db.sm_damage.item_name)
        #                     for row in rows:
        #                         quantity=int(row.quantity)
        #                         dist_rate=float(row.dist_rate)                
        #                         totalAmount+=dist_rate*quantity
        #                         
        #                     #format:cid<fdfd>TodepotID<fdfd>FromDepotID<fdfd>typeName(keyword)<fdfd>paymtent_amount
        #                     strData2=str(c_id)+'<fdfd>DAMAGE<fdfd>'+str(req_sl)+'<fdfd>'+str(datetime_fixed)+'<fdfd>'+str(req_depot)+'-'+str(req_sl)+'<fdfd>DPT-'+str(req_depot)+'<fdfd>DPT-DAMAGE<fdfd>'+str(totalAmount)              
        #                     resStr2=set_balance_transaction(strData2)  # call function
        #                     resStrList2=resStr2.split('<sep>',resStr2.count('<sep>'))
        #                     flag2=resStrList2[0]
        #                     msg2=resStrList2[1]
                            pass
                            #Transfer not settings for ledger
                            
                        else:
                            flag2='True'
                            
                        if flag2=='True':
                            db((db.sm_damage_head.cid==c_id)& (db.sm_damage_head.depot_id==req_depot) & (db.sm_damage_head.sl==req_sl)).update(status='Posted')
                            db((db.sm_damage.cid==c_id)& (db.sm_damage.depot_id==req_depot) & (db.sm_damage.sl==req_sl)).update(status='Posted')
                            
                            # call update depot stock (type,cid,depotid,sl)                    
                            #damage type ('Increase' +,'Decrease' -)
                            update_depot_stock('DAMAGE',c_id,req_depot,req_sl)
                            
                            #update_depot_stock('TRANSFER',c_id,req_depot,req_sl)
                            
                            session.flash='Posted successfully'
                        else:
                            db.rollback()
                            session.flash = 'process error:102'
                    
                    #---------------------
                    autDelCronRows[0].update_record(auto_del_cron_flag=0)
                    #db.commit()
                    #--------------
                
        redirect(URL(c='depot',f='depot_stock_damage',vars=dict(req_sl=req_sl)))

    elif btn_cancel:
        countRecords=db((db.sm_damage.cid==c_id)& (db.sm_damage.depot_id==req_depot) & (db.sm_damage.sl==req_sl)).count()
        if int(countRecords)==0:
            session.flash='At least one item needs!'
        else:
            db((db.sm_damage_head.cid==c_id)& (db.sm_damage_head.depot_id==req_depot) & (db.sm_damage_head.sl==req_sl)).update(status='Cancelled')
            db((db.sm_damage.cid==c_id)& (db.sm_damage.depot_id==req_depot) & (db.sm_damage.sl==req_sl)).update(status='Cancelled')

        redirect(URL(c='depot',f='depot_stock_damage',vars=dict(req_sl=req_sl)))

    return dict()

#---------------catagory-----------------------
def validation_transfer_reference(form):    
    category_id=str(request.vars.cat_type_id).strip().title()
    if category_id!='':
        rows_check=db((db.sm_category_type.cid==session.cid) & (db.sm_category_type.type_name=='TRANSFER_TYPE') &(db.sm_category_type.cat_type_id==category_id)).select(db.sm_category_type.cat_type_id,limitby=(0,1))
        if rows_check:
            form.errors.cat_type_id=''
            response.flash = 'Already exist, Please choose a new'
        else:
            form.vars.cid=session.cid
            form.vars.type_name='TRANSFER_TYPE'
            form.vars.cat_type_id=category_id
def transfer_reference():    
    task_id='rm_utility_manage'
    access_permission=check_role(task_id)
    if (access_permission==False and session.user_type=="Admin"):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))
        
    response.title='Internal Transfer Cause'
    
    cid=session.cid
    
    #---------------------
    form =SQLFORM(db.sm_category_type,
                  fields=['cat_type_id'],
                  submit_button='Save'
                  )
    
    if form.accepts(request.vars,session,onvalidation=validation_transfer_reference):
        response.flash = 'Saved Successfully'
        
    #--------------------------------
    btn_delete=request.vars.btn_delete
    if btn_delete:
        record_id=request.args[1]
        category_id=''
        catRow=db((db.sm_category_type.cid == cid)&(db.sm_category_type.id==record_id)&(db.sm_category_type.type_name=='TRANSFER_TYPE')).select(db.sm_category_type.cat_type_id,limitby=(0,1))
        if not catRow:
            response.flash='Invalid request'
        else:
            category_id=catRow[0].cat_type_id
            
            records=db((db.sm_damage_head.cid==cid) & (db.sm_damage_head.adjustment_reference==category_id)).select(db.sm_damage_head.adjustment_type,limitby=(0,1))
            if records:
                response.flash='Already used in Transfer'            
            else:
                db((db.sm_category_type.cid == cid)&(db.sm_category_type.id == record_id)&(db.sm_category_type.type_name=='TRANSFER_TYPE')).delete()
                response.flash='Deleted successfully'
                
    #--------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=session.items_per_page
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #--------end paging
    
    records=db((db.sm_category_type.cid==cid)&(db.sm_category_type.type_name=='TRANSFER_TYPE')).select(db.sm_category_type.ALL,orderby=db.sm_category_type.cat_type_id,limitby=limitby)
    
    return dict(form=form,records=records,page=page,items_per_page=items_per_page,access_permission=access_permission)
#---------------

def depot_stock_transfer_list():
    #----------Task assaign----------
    task_id='rm_stock_transfer_manage'
    task_id_view='rm_stock_transfer_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))   
        
    response.title='Internal Transfer List'    
    #   --------------------- 
    c_id=session.cid
    
    #  ---------------filter-------    
    btn_filter_damage=request.vars.btn_filter
    btn_all=request.vars.btn_all
    depot_id_value=str(request.vars.depot_id_value).strip()
    search_type=str(request.vars.search_type).strip()
    search_value=str(request.vars.search_value).strip()
    
    reqPage=len(request.args)
    #Set text for filter
    if btn_filter_damage:
        session.btn_filter_damage=btn_filter_damage
        session.depot_id_value_dam=depot_id_value 
        session.search_type_dam=search_type
        session.search_value_dam=search_value
        
        #Check SL is numeric or not
        if (session.search_type_dam=='SL'):
            sl=0
            if not(session.search_value_dam=='' or session.search_value_dam==None):
                try:       
                    sl=int(session.search_value_dam)
                    session.search_value_dam=sl
                except:
                    session.search_value_dam=sl
                    response.flash='Sl needs number value'
            else:
                session.search_value_dam=sl
                
        reqPage=0
        
    elif btn_all:
        session.btn_filter_damage=None
        session.depot_id_value_dam=None
        session.search_type_dam=None
        session.search_value_dam=None
        reqPage=0
    
    
    #--------paging
    if reqPage:
        page=int(request.args[0])
    else:
        page=0
    items_per_page=session.items_per_page*10
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #--------end paging  
    
    qset=db()
    qset=qset(db.sm_damage_head.cid==c_id)    
    qset=qset(db.sm_damage_head.transfer_type=='TRANSFER')
    
    if (session.user_type=='Depot'):
        qset=qset(db.sm_damage_head.depot_id==session.depot_id)
        
    #Set query bsed on search type
    if (session.btn_filter_damage):
        if (session.user_type!='Depot'):
            if not (session.depot_id_value_dam=='' or session.depot_id_value_dam==None):
                searchValue=str(session.depot_id_value_dam).split('|')[0]
                qset=qset(db.sm_damage_head.depot_id==searchValue)
            else:
                qset=qset(db.sm_damage_head.depot_id!='')
        
        #------------
        if (session.search_type_dam=='SL'):
            qset=qset(db.sm_damage_head.type_sl==session.search_value_dam)
            
        elif (session.search_type_dam=='DATE'):
            qset=qset(db.sm_damage_head.damage_date==session.search_value_dam)
        
        elif (session.search_type_dam=='STATUS'):
            qset=qset(db.sm_damage_head.status==session.search_value_dam)
        
        elif (session.search_type_dam=='UserID'):
            qset=qset(db.sm_damage_head.updated_by==session.search_value_dam)
        
        
    records=qset.select(db.sm_damage_head.ALL,orderby=~db.sm_damage_head.id,limitby=limitby)
    
    #------------------------------------------------
    search_form =SQLFORM(db.sm_search_date)
    #-------------
    
    return dict(search_form=search_form,records=records,page=page,items_per_page=items_per_page,access_permission=access_permission,access_permission_view=access_permission_view)
    
#======================= Stock Damage 
#Validation damage
def validation_transfer(form):
    c_id=session.cid   
    
    depot_id=str(form.vars.depot_id).split('|')[0]
    depot_name=str(form.vars.depot_id).split('|')[1]
    
    store_idname=str(form.vars.store_id)
    store_to_idname=str(form.vars.store_id_to)
    
    item_id=str(form.vars.item_id)
    item_name=str(form.vars.item_name)
    quantity=str(form.vars.quantity)
    dist_rate=0     #str(form.vars.dist_rate)
    short_note=''   #str(form.vars.short_note)
    
    typeList=str(request.vars.adjustment_reference)
    
    batch_id=str(form.vars.batch_id).strip().split('|')[0]
    
    if store_idname=='':
        form.errors.store_id=''
        response.flash="Required 'From Store'"
    else:
        store_id=str(store_idname).split('|')[0]
        store_name=str(store_idname).split('|')[1]
        
        store_id_to=''
        store_name_to=''
        
        if (store_to_idname=='' or store_to_idname=='|'):
            form.errors.store_id=''
            response.flash="Required 'To Store'"
        else:
            store_id_to=str(store_to_idname).split('|')[0]
            store_name_to=str(store_to_idname).split('|')[1]
            
            if store_id==store_id_to:
                form.errors.store_id=''
                response.flash="Required Different 'From Store' and 'To Store'"
            else:
#                 if len(typeList)!=2:
#                     form.errors.adjustment_type=''
#                     response.flash="Required Reference"
#                 else:
                
                if typeList=='':
                    form.errors.store_id=''
                    response.flash="Required Cause"
                else:
                    adjustment_reference=typeList
                    adjustment_type=''#typeList[1]
                    
                    itemRows = db((db.sm_item.cid == c_id)&(db.sm_item.item_id == item_id)).select(db.sm_item.name,db.sm_item.price,db.sm_item.unit_type,db.sm_item.item_carton,limitby=(0,1))
                    if not itemRows:
                        form.errors.item_id=''
                        response.flash="Invalid Item ID"
                    else:
                        dist_rate=itemRows[0].price
                        unit_type=itemRows[0].unit_type
                        item_carton=itemRows[0].item_carton
                
                        itemBatchRows = db((db.sm_item_batch.cid == c_id) & (db.sm_item_batch.item_id == item_id) & (db.sm_item_batch.batch_id == batch_id)).select(db.sm_item_batch.item_id,db.sm_item_batch.expiary_date,limitby=(0,1))
                        if not itemBatchRows:
                            form.errors.batch_id=''
                            response.flash="Invalid Item Batch ID"
                        else:
                            expiary_date=itemBatchRows[0].expiary_date
                            
                            sl=int(form.vars.sl)
                            ym_date=str(form.vars.damage_date)[0:7]+'-01'
                            
                            existRecords=db((db.sm_damage.cid==c_id) & (db.sm_damage.depot_id==depot_id)& (db.sm_damage.sl==sl) & (db.sm_damage.item_id==item_id) & (db.sm_damage.batch_id==batch_id)).select(db.sm_damage.id,db.sm_damage.item_id,limitby=(0,1))
                            if existRecords:
                                existRecords[0].update_record(item_name=item_name,quantity=quantity,dist_rate=dist_rate,short_note=short_note)        
                                form.errors.short_note=''  
                                response.flash='Item replaced!'      
                                
                            elif int(quantity)<=0:
                                form.errors.quantity=''
                                response.flash='need item quantity!'
                                
                            else:
                                if sl==0:
                                    maxSl=1
                                    records=db((db.sm_depot.cid==c_id) & (db.sm_depot.depot_id==depot_id)).select(db.sm_depot.id,db.sm_depot.damage_sl,limitby=(0,1))
                                    if records:
                                        sl=records[0].damage_sl
                                        maxSl=int(sl)+1                
                                    #-------- update sl in depot
                                    records[0].update_record(damage_sl=maxSl)
                                    
                                    form.vars.sl=maxSl
                                    
                                    #-------------
                                    typeSl=1
                                    typeRecords=db((db.sm_damage_head.cid==c_id) & (db.sm_damage_head.depot_id==depot_id) & (db.sm_damage_head.transfer_type=='TRANSFER')).select(db.sm_damage_head.type_sl,orderby=~db.sm_damage_head.type_sl,limitby=(0,1))
                                    if typeRecords:
                                        typeSl=typeRecords[0].type_sl+1
                                    
                                    form.vars.type_sl=typeSl
                                
                                form.vars.ym_date=ym_date
                                form.vars.depot_id=depot_id
                                form.vars.depot_name=depot_name
                                form.vars.batch_id = batch_id
                                form.vars.dist_rate = dist_rate
                                form.vars.adjustment_reference = adjustment_reference
                                form.vars.adjustment_type = adjustment_type                        
                                form.vars.store_id=store_id
                                form.vars.store_name=store_name
                                form.vars.store_id_to=store_id_to
                                form.vars.store_name_to=store_name_to
                                form.vars.item_unit=unit_type
                                form.vars.item_carton=item_carton
                                form.vars.expiary_date=expiary_date
                                
def depot_stock_transfer():
    #----------Task assaign----------
    task_id='rm_stock_transfer_manage'
    task_id_view='rm_stock_transfer_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))   
        
#   --------------------- 
    response.title='Internal Transfer'
    c_id=session.cid
    
    #------------------
    btn_update=request.vars.btn_update
    
    #------------------- UPDATE
    if btn_update:
        req_depot_id=str(request.vars.depot_id).split('|')[0]
        reqSl=request.vars.sl
        req_date=request.vars.damage_date
        ym_date=str(req_date)[0:7]+'-01'#Save as first day of month
        req_note=request.vars.note
        
        typeList=str(request.vars.adjustment_reference).split('|')
        adjustment_reference=''
        adjustment_type=''
        if len(typeList)==2:            
            adjustment_reference=typeList[0]
            adjustment_type=typeList[1]
        else:
            adjustment_reference=typeList[0]
            
        if req_date!='':
            db((db.sm_damage_head.cid==c_id)& (db.sm_damage_head.depot_id==req_depot_id) & (db.sm_damage_head.sl==reqSl)).update(damage_date=req_date,note=req_note,ym_date=ym_date,adjustment_reference=adjustment_reference,adjustment_type=adjustment_type)
            db((db.sm_damage.cid==c_id)& (db.sm_damage.depot_id==req_depot_id) & (db.sm_damage.sl==reqSl)).update(damage_date=req_date,note=req_note,ym_date=ym_date,adjustment_reference=adjustment_reference,adjustment_type=adjustment_type)
            session.flash='Updated successfully'
            redirect(URL(c='depot',f='depot_stock_transfer',vars=dict(req_sl=reqSl)))
            
    #-------- SAVE ITEM/ REPLACED IF EXIST
    form =SQLFORM(db.sm_damage,
                  fields=['depot_id','sl','type_sl','store_id','store_id_to','damage_date','status','item_id','item_name','batch_id','quantity','dist_rate','note','adjustment_type'],
                  submit_button='Save'
                  )
    form.vars.cid=c_id
    form.vars.transfer_type='TRANSFER'
    form.vars.quantity=''
    
    if form.accepts(request.vars,session,onvalidation=validation_transfer):
        depot_id=form.vars.depot_id
        depot_name=form.vars.depot_name
        
        sl=form.vars.sl
        req_date=form.vars.damage_date
        ym_date=str(req_date)[0:7]+'-01'
        
        note=form.vars.note
        
        type=request.vars.adjustment_type
        
        adjustment_reference=form.vars.adjustment_reference
        adjustment_type=form.vars.adjustment_type 
        
        store_id=form.vars.store_id
        store_name=form.vars.store_name
        
        store_id_to=form.vars.store_id_to
        store_name_to=form.vars.store_name_to
        
        transfer_type=form.vars.transfer_type
        type_sl=form.vars.type_sl
        
        #---------- head insert/update
        headRows=db((db.sm_damage_head.cid==c_id)& (db.sm_damage_head.depot_id==depot_id) & (db.sm_damage_head.sl==sl)).select(db.sm_damage_head.id,db.sm_damage_head.depot_id,limitby=(0,1))
        if headRows:
             headRows[0].update_record(damage_date=req_date,note=note,ym_date=ym_date,adjustment_reference=adjustment_reference,adjustment_type=adjustment_type)
        else:
            db.sm_damage_head.insert(cid=c_id,depot_id=depot_id,depot_name=depot_name,sl=sl,transfer_type=transfer_type,type_sl=type_sl,store_id=store_id,store_name=store_name,store_id_to=store_id_to,store_name_to=store_name_to,damage_date=req_date,note=note,ym_date=ym_date,adjustment_reference=adjustment_reference,adjustment_type=adjustment_type)
        
        #----------SAME SL DATA UPDATE
        db((db.sm_damage.cid==c_id)& (db.sm_damage.depot_id==depot_id) & (db.sm_damage.sl==sl)).update(damage_date=req_date,note=note,ym_date=ym_date,adjustment_reference=adjustment_reference,adjustment_type=adjustment_type)
        
        session.flash = ''
        redirect(URL(c='depot',f='depot_stock_transfer',vars=dict(req_sl=sl)))
        
#    elif form.errors:
#        session.flash=''
#        redirect(URL(c='depot',f='depot_stock_damage',vars=dict(req_sl=form.vars.sl)))
        
    #  --------------------- NEW DAMAGE/SHOW FIELD VALUE
    depot_name=''
    
    req_sl=request.vars.req_sl
    depotid=request.vars.depotid
    if depotid=='' or depotid==None:
        depot_id=session.depot_id
        depot_name=session.user_depot_name
    else:
        depot_id=depotid
        
    sl=0
    type_sl=0
    status='Draft'
    damage_date=current_date
    note=''
    adjustment_reference=''
    adjustment_type=''
    store_id=''
    store_name=''
    store_id_to=''
    store_name_to=''
    records=db((db.sm_damage.cid==c_id)& (db.sm_damage.depot_id==depot_id) & (db.sm_damage.sl==req_sl)).select(db.sm_damage.ALL,orderby=db.sm_damage.item_name)
    for rec in records:
        depot_id=rec.depot_id
        depot_name=rec.depot_name
        sl=rec.sl
        status=rec.status
        damage_date=rec.damage_date
        note=rec.note
        adjustment_reference=rec.adjustment_reference
        adjustment_type=rec.adjustment_type
        store_id=rec.store_id
        store_name=rec.store_name
        store_id_to=rec.store_id_to
        store_name_to=rec.store_name_to     
        type_sl=rec.type_sl   
        break
        
    #-------------------    
    refRecords=''
    if adjustment_reference=='':
        refRecords=db((db.sm_category_type.cid==c_id) & (db.sm_category_type.type_name=='TRANSFER_TYPE')).select(db.sm_category_type.cat_type_id,db.sm_category_type.field1,orderby=db.sm_category_type.cat_type_id)
        
    storeRecords=''
    if sl==0:
        storeRecords=db((db.sm_depot_store.cid==c_id) & (db.sm_depot_store.depot_id==depot_id)).select(db.sm_depot_store.store_id,db.sm_depot_store.store_name,orderby=db.sm_depot_store.store_name)
        
    return dict(form=form,records=records,storeRecords=storeRecords,depot_id=depot_id,depot_name=depot_name,sl=sl,type_sl=type_sl,store_id=store_id,store_name=store_name,store_id_to=store_id_to,store_name_to=store_name_to,damage_date=damage_date,status=status,note=note,adjustment_type=adjustment_type,adjustment_reference=adjustment_reference,refRecords=refRecords,access_permission=access_permission,access_permission_view=access_permission_view)


#=================== Delete item
# delete damage if more than one item is a sl
def delete_transfer_item():
    c_id=session.cid
    
    btn_delete=request.vars.btn_delete
    
    req_depot=request.args(0)
    req_sl=request.args(1)
    req_item=request.args(2)
    rowid=request.args(3)
    
    if btn_delete:
        countRecords=db((db.sm_damage.cid==c_id)& (db.sm_damage.depot_id==req_depot) & (db.sm_damage.sl==req_sl)).count()
        if int(countRecords)==1:
            session.flash='At least one item needs, You can cancel if required!'
        else:
            db((db.sm_damage.cid==c_id) & (db.sm_damage.depot_id==req_depot) & (db.sm_damage.sl==req_sl)& (db.sm_damage.item_id==req_item)& (db.sm_damage.id==rowid)).delete()
            
        redirect(URL(c='depot',f='depot_stock_transfer',vars=dict(req_sl=req_sl)))
    #  ---------------------
    return dict()

#=================== Post and Cancel
#Update sattus as post or cancel
def post_cancel_transfer():
    c_id=session.cid
    
    btn_post=request.vars.btn_post
    btn_cancel=request.vars.btn_cancel
    
    req_depot=request.args(0)
    req_sl=request.args(1)   
    req_date=request.args(2)    
    
    if btn_post:
        countRecords=db((db.sm_damage.cid==c_id)& (db.sm_damage.depot_id==req_depot) & (db.sm_damage.sl==req_sl)).count()
        if int(countRecords)==0:
            session.flash='At least one item needs!'
        else:
            batchIdrows=db((db.sm_damage.cid==c_id)& (db.sm_damage.depot_id==req_depot) & (db.sm_damage.sl==req_sl) & (db.sm_damage.batch_id=='')).select(db.sm_damage.id,limitby=(0,1))
            if batchIdrows:
                session.flash = 'Required Batch ID for all Items'
            else:
                #--------------------------- chcek stock cron flag
                autDelCronRows=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==req_depot)&(db.sm_depot.auto_del_cron_flag==0)).select(db.sm_depot.id,db.sm_depot.cid,limitby=(0,1))
                if not autDelCronRows:
                    session.flash='One process running, please try again'
                else:
                    autDelCronRows[0].update_record(auto_del_cron_flag=1)
                    #---------------------
                    
                    itemStrForQty=''                    
                    diffRecords="select dam.item_id as item_id from sm_depot_stock_balance dsb,sm_damage dam  where (dam.cid='"+str(c_id)+"' and dam.depot_id='"+str(req_depot)+"' and dam.sl="+str(req_sl)+" and dsb.cid='"+str(c_id)+"' and dsb.depot_id='"+str(req_depot)+"' and dam.store_id=dsb.store_id and dam.item_id=dsb.item_id and dam.batch_id=dsb.batch_id and (dsb.quantity-dsb.block_qty)<dam.quantity)"
                    diffRowsList=db.executesql(diffRecords,as_dict=True)
                    for i in range(len(diffRowsList)):
                        diffDictData=diffRowsList[i]
                        if itemStrForQty=='':
                            itemStrForQty=diffDictData['item_id']
                        else:
                            itemStrForQty+=','+diffDictData['item_id']
                            
                    if itemStrForQty!='':
                        session.flash='Quantity not available for item ID '+str(itemStrForQty)                        
                    else:                        
                        totalAmount=0
                        
                        flag2='True'
                        #--------------------- depot balance
                        if session.primaryLedgerCreate=='YES':
        #                     rows=db((db.sm_damage.cid==c_id)& (db.sm_damage.depot_id==req_depot) & (db.sm_damage.sl==req_sl)).select(db.sm_damage.ALL,orderby=db.sm_damage.item_name)
        #                     for row in rows:
        #                         quantity=int(row.quantity)
        #                         dist_rate=float(row.dist_rate)                
        #                         totalAmount+=dist_rate*quantity
        #                         
        #                     #format:cid<fdfd>TodepotID<fdfd>FromDepotID<fdfd>typeName(keyword)<fdfd>paymtent_amount
        #                     strData2=str(c_id)+'<fdfd>DAMAGE<fdfd>'+str(req_sl)+'<fdfd>'+str(datetime_fixed)+'<fdfd>'+str(req_depot)+'-'+str(req_sl)+'<fdfd>DPT-'+str(req_depot)+'<fdfd>DPT-DAMAGE<fdfd>'+str(totalAmount)              
        #                     resStr2=set_balance_transaction(strData2)  # call function
        #                     resStrList2=resStr2.split('<sep>',resStr2.count('<sep>'))
        #                     flag2=resStrList2[0]
        #                     msg2=resStrList2[1]
                            pass
                            #Transfer not settings for ledger
                            
                        else:
                            flag2='True'
                            
                        if flag2=='True':
                            db((db.sm_damage_head.cid==c_id)& (db.sm_damage_head.depot_id==req_depot) & (db.sm_damage_head.sl==req_sl)).update(status='Posted')
                            db((db.sm_damage.cid==c_id)& (db.sm_damage.depot_id==req_depot) & (db.sm_damage.sl==req_sl)).update(status='Posted')
                            
                            # call update depot stock (type,cid,depotid,sl)                    
                            #damage type ('Increase' +,'Decrease' -)
                            update_depot_stock('TRANSFER',c_id,req_depot,req_sl)
                            
                            session.flash='Posted successfully'
                        else:
                            db.rollback()
                            session.flash = 'process error:102'
                            
                    #---------------------
                    autDelCronRows[0].update_record(auto_del_cron_flag=0)
                    #db.commit()
                    #--------------
                
        redirect(URL(c='depot',f='depot_stock_transfer',vars=dict(req_sl=req_sl)))

    elif btn_cancel:
        countRecords=db((db.sm_damage.cid==c_id)& (db.sm_damage.depot_id==req_depot) & (db.sm_damage.sl==req_sl)).count()
        if int(countRecords)==0:
            session.flash='At least one item!'
        else:
            db((db.sm_damage_head.cid==c_id)& (db.sm_damage_head.depot_id==req_depot) & (db.sm_damage_head.sl==req_sl)).update(status='Cancelled')
            db((db.sm_damage.cid==c_id)& (db.sm_damage.depot_id==req_depot) & (db.sm_damage.sl==req_sl)).update(status='Cancelled')

        redirect(URL(c='depot',f='depot_stock_transfer',vars=dict(req_sl=req_sl)))

    return dict()


def post_cancel_damage_bak():
    c_id=session.cid
    
    btn_post=request.vars.btn_post
    btn_cancel=request.vars.btn_cancel
    
    req_depot=request.args(0)
    req_sl=request.args(1)   
    req_date=request.args(2)    
    
    if btn_post:
        countRecords=db((db.sm_damage.cid==c_id)& (db.sm_damage.depot_id==req_depot) & (db.sm_damage.sl==req_sl)).count()
        if int(countRecords)==0:
            session.flash='At least one item needs in a damage!'
        else:
            batchIdrows=db((db.sm_damage.cid==c_id)& (db.sm_damage.depot_id==req_depot) & (db.sm_damage.sl==req_sl) & (db.sm_damage.batch_id=='')).select(db.sm_damage.id,limitby=(0,1))
            if batchIdrows:
                session.flash = 'Required Batch ID for all Items'
            else:
                totalAmount=0
                
                #--------------------- depot balance
                if session.primaryLedgerCreate=='YES':
                    rows=db((db.sm_damage.cid==c_id)& (db.sm_damage.depot_id==req_depot) & (db.sm_damage.sl==req_sl)).select(db.sm_damage.ALL,orderby=db.sm_damage.item_name)
                    for row in rows:
                        quantity=int(row.quantity)
                        dist_rate=float(row.dist_rate)                
                        totalAmount+=dist_rate*quantity
                        
                    #format:cid<fdfd>TodepotID<fdfd>FromDepotID<fdfd>typeName(keyword)<fdfd>paymtent_amount
                    strData2=str(c_id)+'<fdfd>DAMAGE<fdfd>'+str(req_sl)+'<fdfd>'+str(datetime_fixed)+'<fdfd>'+str(req_depot)+'-'+str(req_sl)+'<fdfd>DPT-'+str(req_depot)+'<fdfd>DPT-DAMAGE<fdfd>'+str(totalAmount)              
                    resStr2=set_balance_transaction(strData2)  # call function
                    resStrList2=resStr2.split('<sep>',resStr2.count('<sep>'))
                    flag2=resStrList2[0]
                    msg2=resStrList2[1]
                else:
                    flag2='True'
                    
                if flag2=='True':
                    db((db.sm_damage_head.cid==c_id)& (db.sm_damage_head.depot_id==req_depot) & (db.sm_damage_head.sl==req_sl)).update(status='Posted')
                    db((db.sm_damage.cid==c_id)& (db.sm_damage.depot_id==req_depot) & (db.sm_damage.sl==req_sl)).update(status='Posted')
                    
                    # call update depot stock (type,cid,depotid,sl)                    
                    #damage type (positive+ / negative-)
                    update_depot_stock('DAMAGE',c_id,req_depot,req_sl)
                    
                    session.flash='Posted successfully'
                else:
                    db.rollback()
                    session.flash = 'process error:102'
                    
        redirect(URL(c='depot',f='depot_stock_damage',vars=dict(req_sl=req_sl)))

    elif btn_cancel:
        countRecords=db((db.sm_damage.cid==c_id)& (db.sm_damage.depot_id==req_depot) & (db.sm_damage.sl==req_sl)).count()
        if int(countRecords)==0:
            session.flash='At least one item needs in a damage!'
        else:
            db((db.sm_damage_head.cid==c_id)& (db.sm_damage_head.depot_id==req_depot) & (db.sm_damage_head.sl==req_sl)).update(status='Cancelled')
            db((db.sm_damage.cid==c_id)& (db.sm_damage.depot_id==req_depot) & (db.sm_damage.sl==req_sl)).update(status='Cancelled')

        redirect(URL(c='depot',f='depot_stock_damage',vars=dict(req_sl=req_sl)))

    return dict()

#preview_requisition
def preview_requisition():
    c_id=session.cid
    depot_id=request.args(0)
    sl=request.args(1)

    #--------------- Title
    response.title='Preview Requisition'
    
    #-------------
    status=''
    req_process_status=''
    requisition_to=''
    req_date=current_date
    note='' 
    
    depotName=''
    depotNameTo=''
    
    records=db((db.sm_requisition.cid==c_id)& (db.sm_requisition.depot_id==depot_id) & (db.sm_requisition.sl==sl)).select(db.sm_requisition.ALL,limitby=(0,1))
    for rec in records:
        status=rec.status
        req_process_status=rec.req_process_status
        requisition_to=rec.requisition_to
        req_date=rec.req_date
        note=rec.note
        
        depotName=rec.depot_name
        depotNameTo=rec.depot_to_name
        break 
        
    #-----------
    #Get record for detail and ctreat as list
    detailRecords=db((db.sm_requisition.cid==c_id)& (db.sm_requisition.depot_id==depot_id) & (db.sm_requisition.sl==sl)).select(db.sm_requisition.item_id,db.sm_requisition.item_name,db.sm_requisition.quantity,db.sm_requisition.dist_rate,orderby=db.sm_requisition.item_name)

    #-----
    
    return dict(message=T('Show Requisition'),detailRecords=detailRecords,depot_id=depot_id,depotName=depotName,depotNameTo=depotNameTo,sl=sl,req_date=req_date,requisition_to=requisition_to,
                note=note,status=status,req_process_status=req_process_status)


#preview_issue
def preview_issue():
    c_id=session.cid
    depot_id=request.args(0)
    sl=request.args(1)
    
    #--------------- Title
    response.title='Preview Transfer(Branch To Branch)'
    
    #-------------
    status=''
    issue_process_status=''
    issued_to=''
    issue_date=current_date    
    note=''
    discount=0
    ref_sl=0
    store_id=''
    store_name=''
    cause=''
    updatedBy=''
    receive_date=''
    detailRecords=db((db.sm_issue.cid==c_id)& (db.sm_issue.depot_id==depot_id) & (db.sm_issue.sl==sl)).select(db.sm_issue.ALL,orderby=db.sm_issue.item_name)
    for rec in detailRecords:
        status=rec.status
        issue_process_status=rec.issue_process_status
        issued_to=rec.issued_to
        issue_date=rec.issue_date
        note=rec.note
        discount=rec.total_discount
        ref_sl=rec.req_sl
        store_id=rec.store_id
        store_name=rec.store_name
        cause=rec.transaction_cause
        updatedBy=rec.updated_by
        
        recRows=db((db.sm_receive_head.cid==c_id)& (db.sm_receive_head.receive_from==depot_id) & (db.sm_receive_head.ref_sl==sl) & (db.sm_receive_head.status=='Posted')).select(db.sm_receive_head.receive_date,limitby=(0,1))
        if recRows:
            receive_date=recRows[0].receive_date.strftime('%d-%b-%Y')
        
        break
    
    depotName=''
    depotAddress=''
    depotRows=db((db.sm_depot.cid==c_id) & (db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,db.sm_depot.field1,limitby=(0,1))
    if depotRows:
        depotName=depotRows[0].name
        depotAddress=depotRows[0].field1
        
    if session.user_type!='Depot':
        session.user_depot_address=depotAddress
        
    depotNameTo=''
    depotRowsTo=db((db.sm_depot.cid==c_id) & (db.sm_depot.depot_id==issued_to)).select(db.sm_depot.name,limitby=(0,1))
    if depotRowsTo:
        depotNameTo=depotRowsTo[0].name
        
    #-----------   
    #Get record for detail and ctreat as list
    
    #detailRecords=db((db.sm_issue.cid==c_id)& (db.sm_issue.depot_id==depot_id) & (db.sm_issue.sl==sl)&(db.sm_item_batch.cid==c_id) & (db.sm_item_batch.item_id==db.sm_issue.item_id)& (db.sm_item_batch.batch_id==db.sm_issue.batch_id)&(db.sm_item.cid==c_id) & (db.sm_item_batch.item_id==db.sm_item.item_id)).select(db.sm_issue.ALL,db.sm_item.unit_type,db.sm_item.item_carton,db.sm_item.price,db.sm_item_batch.expiary_date,orderby=db.sm_issue.item_name)
    
    #----- 
    return dict(detailRecords=detailRecords,depot_id=depot_id,depotName=depotName,depotNameTo=depotNameTo,sl=sl,store_id=store_id,store_name=store_name,issue_date=issue_date,issued_to=issued_to,note=note,status=status,issue_process_status=issue_process_status,discount=discount,ref_sl=ref_sl,cause=cause,updatedBy=updatedBy,receive_date=receive_date)

#preview_receive
def preview_receive():
    c_id=session.cid
    depot_id=request.args(0)
    sl=request.args(1)
    
    #--------------- Title
    response.title='Preview GR Note(Receive)'
    
    #-------------
    status=''
    receive_process_status=''
    receive_from=''
    receive_date=current_date    
    note=''
    discount=0
    ref_sl=0
    store_id=''
    store_name=''
    cause=''
    updatedBy=''
    records=db((db.sm_receive.cid==c_id)& (db.sm_receive.depot_id==depot_id) & (db.sm_receive.sl==sl)).select(db.sm_receive.ALL,limitby=(0,1))
    for rec in records:
        status=rec.status
        receive_process_status=rec.receive_process_status
        receive_from=rec.receive_from
        receive_date=rec.receive_date
        note=rec.note
        discount=rec.total_discount
        ref_sl=rec.ref_sl
        store_id=rec.store_id
        store_name=rec.store_name
        cause=rec.transaction_cause
        updatedBy=rec.updated_by
        break
    
    depotName=''
    depotAddress=''
    depotRows=db((db.sm_depot.cid==c_id) & (db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,db.sm_depot.field1,limitby=(0,1))
    if depotRows:
        depotName=depotRows[0].name        
        depotAddress=depotRows[0].field1
        
    if session.user_type!='Depot':
        session.user_depot_address=depotAddress
        
    depotNameFrom=''
    depotRowsFrom=db((db.sm_depot.cid==c_id) & (db.sm_depot.depot_id==receive_from)).select(db.sm_depot.name,limitby=(0,1))
    if depotRowsFrom:
        depotNameFrom=depotRowsFrom[0].name
        
    #-----------   
    #Get record for detail and ctreat as list
    showList=[]
    detailRecords=db((db.sm_receive.cid==c_id)& (db.sm_receive.depot_id==depot_id) & (db.sm_receive.sl==sl)).select(db.sm_receive.ALL,orderby=db.sm_receive.item_name)
    
    #-----    
    return dict(detailRecords=detailRecords,depot_id=depot_id,depotName=depotName,store_id=store_id,store_name=store_name,depotNameFrom=depotNameFrom,sl=sl,receive_date=receive_date,receive_from=receive_from,
                note=note,status=status,receive_process_status=receive_process_status,discount=discount,ref_sl=ref_sl,cause=cause,updatedBy=updatedBy)


#preview_receive
def preview_received_note():
    c_id=session.cid
    depot_id=request.args(0)
    sl=request.args(1)
    
    #--------------- Title
    response.title='Preview RC(Receive)'
    
    #-------------
    status=''
    receive_process_status=''
    receive_from=''
    receive_date=current_date    
    note=''
    discount=0
    ref_sl=0
    store_id=''
    store_name=''
    cause=''
    updatedBy=''
    records=db((db.sm_receive.cid==c_id)& (db.sm_receive.depot_id==depot_id) & (db.sm_receive.sl==sl)).select(db.sm_receive.ALL,limitby=(0,1))
    for rec in records:
        status=rec.status
        receive_process_status=rec.receive_process_status
        receive_from=rec.receive_from
        receive_date=rec.receive_date
        note=rec.note
        discount=rec.total_discount
        ref_sl=rec.ref_sl
        store_id=rec.store_id
        store_name=rec.store_name
        cause=rec.transaction_cause
        updatedBy=rec.updated_by
        break
    
    depotName=''
    depotAddress=''
    depotRows=db((db.sm_depot.cid==c_id) & (db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,db.sm_depot.field1,limitby=(0,1))
    if depotRows:
        depotName=depotRows[0].name        
        depotAddress=depotRows[0].field1
        
    if session.user_type!='Depot':
        session.user_depot_address=depotAddress
        
    depotNameFrom=''
    depotAddressFrom=''
    depotRowsFrom=db((db.sm_depot.cid==c_id) & (db.sm_depot.depot_id==receive_from)).select(db.sm_depot.name,db.sm_depot.field1,limitby=(0,1))
    if depotRowsFrom:
        depotNameFrom=depotRowsFrom[0].name
        depotAddressFrom=depotRows[0].field1
        
    #-----------   
    #Get record for detail and ctreat as list
    showList=[]
    detailRecords=db((db.sm_receive.cid==c_id)& (db.sm_receive.depot_id==depot_id) & (db.sm_receive.sl==sl)&(db.sm_item_batch.cid==c_id) & (db.sm_item_batch.item_id==db.sm_receive.item_id)& (db.sm_item_batch.batch_id==db.sm_receive.batch_id)&(db.sm_item.cid==c_id) & (db.sm_item_batch.item_id==db.sm_item.item_id)).select(db.sm_receive.ALL,db.sm_item.unit_type,db.sm_item.item_carton,db.sm_item.price,db.sm_item_batch.expiary_date,orderby=db.sm_receive.item_name)
    
    disputeRecords=db((db.sm_receive.cid==c_id)& (db.sm_receive.depot_id==depot_id) & (db.sm_receive.sl==sl)&(db.sm_transaction_dispute.cid==c_id)& (db.sm_transaction_dispute.depot_id==depot_id) & (db.sm_transaction_dispute.recieve_sl==sl)& (db.sm_receive.item_id==db.sm_transaction_dispute.item_id)& (db.sm_receive.batch_id==db.sm_transaction_dispute.batch_id)).select(db.sm_transaction_dispute.item_id,db.sm_transaction_dispute.batch_id,db.sm_transaction_dispute.quantity,orderby=db.sm_transaction_dispute.item_id)
    disputeList=disputeRecords.as_list()
    
    #-----    
    return dict(detailRecords=detailRecords,depot_id=depot_id,depotName=depotName,store_id=store_id,store_name=store_name,depotNameFrom=depotNameFrom,sl=sl,receive_date=receive_date,receive_from=receive_from,
                note=note,status=status,receive_process_status=receive_process_status,discount=discount,ref_sl=ref_sl,cause=cause,updatedBy=updatedBy,depotAddress=depotAddress,depotAddressFrom=depotAddressFrom,disputeList=disputeList)


#preview_damage
def preview_damage():
    c_id=session.cid
    depot_id=request.args(0)
    sl=request.args(1)
    
    #--------------- Title
    response.title='Preview -IC Adjustment'
    
    #-------------
    status=''
    damage_date=current_date
    note=''
    store_id=''
    store_name=''
    store_id_to=''
    store_name_to=''
    type_sl=0
    cause=''
    updatedBy=''
    rowId=''
    records=db((db.sm_damage_head.cid==c_id)& (db.sm_damage_head.depot_id==depot_id) & (db.sm_damage_head.sl==sl)).select(db.sm_damage_head.ALL,limitby=(0,1))
    for rec in records:
        rowId=rec.sl
        status=rec.status
        damage_date=rec.damage_date
        note=rec.note
        store_id=rec.store_id
        store_name=rec.store_name
        store_id_to=rec.store_id_to
        store_name_to=rec.store_name_to    
        type_sl=rec.type_sl
        cause=rec.adjustment_reference
        updatedBy=rec.updated_by
        break
        
    depotName=''
    depotAddress=''
    depotRows=db((db.sm_depot.cid==c_id) & (db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,db.sm_depot.field1,limitby=(0,1))
    if depotRows:
        depotName=depotRows[0].name
        depotAddress=depotRows[0].field1
        
    if session.user_type!='Depot':
        session.user_depot_address=depotAddress
        
    #-----------   
    #Get record for detail and ctreat as list
    showList=[]
    #detailRecords=db((db.sm_damage.cid==c_id)& (db.sm_damage.depot_id==depot_id) & (db.sm_damage.sl==sl)&(db.sm_item_batch.cid==c_id) & (db.sm_item_batch.item_id==db.sm_damage.item_id)& (db.sm_item_batch.batch_id==db.sm_damage.batch_id)&(db.sm_item.cid==c_id) & (db.sm_item_batch.item_id==db.sm_item.item_id)).select(db.sm_damage.ALL,db.sm_item.unit_type,db.sm_item.item_carton,db.sm_item.price,db.sm_item_batch.expiary_date,orderby=db.sm_damage.item_name)
    
    detailRecords=db((db.sm_damage.cid==c_id)& (db.sm_damage.depot_id==depot_id) & (db.sm_damage.sl==sl)).select(db.sm_damage.ALL,orderby=db.sm_damage.item_name)
    
    #-----    
    return dict(detailRecords=detailRecords,rowId=rowId,depot_id=depot_id,depotName=depotName,sl=sl,type_sl=type_sl,store_id=store_id,store_name=store_name,store_id_to=store_id_to,store_name_to=store_name_to,damage_date=damage_date,note=note,cause=cause,status=status,updatedBy=updatedBy)


#preview_transfer
def preview_transfer():
    c_id=session.cid
    depot_id=request.args(0)
    sl=request.args(1)
    
    #--------------- Title
    response.title='Preview Internal Transfer'
    
    #-------------
    status=''
    damage_date=current_date
    note=''
    store_id=''
    store_name=''
    store_id_to=''
    store_name_to=''
    type_sl=0
    cause=''
    updatedBy=''
    detailRecords=db((db.sm_damage.cid==c_id)& (db.sm_damage.depot_id==depot_id) & (db.sm_damage.sl==sl)).select(db.sm_damage.ALL,orderby=db.sm_damage.item_name)
    for rec in detailRecords:
        status=rec.status
        damage_date=rec.damage_date
        note=rec.note
        store_id=rec.store_id
        store_name=rec.store_name
        store_id_to=rec.store_id_to
        store_name_to=rec.store_name_to 
        type_sl=rec.type_sl 
        cause=rec.adjustment_reference
        updatedBy=rec.updated_by
        break
        
    depotName=''
    depotAddress=''
    depotRows=db((db.sm_depot.cid==c_id) & (db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,db.sm_depot.field1,limitby=(0,1))
    if depotRows:
        depotName=depotRows[0].name
        depotAddress=depotRows[0].field1
        
    if session.user_type!='Depot':
        session.user_depot_address=depotAddress
        
    #-----------   
    #Get record for detail and ctreat as list
    showList=[]
    #detailRecords=db((db.sm_damage.cid==c_id)& (db.sm_damage.depot_id==depot_id) & (db.sm_damage.sl==sl)&(db.sm_item_batch.cid==c_id) & (db.sm_item_batch.item_id==db.sm_damage.item_id)& (db.sm_item_batch.batch_id==db.sm_damage.batch_id)&(db.sm_item.cid==c_id) & (db.sm_item_batch.item_id==db.sm_item.item_id)).select(db.sm_damage.ALL,db.sm_item.unit_type,db.sm_item.item_carton,db.sm_item.price,db.sm_item_batch.expiary_date,orderby=db.sm_damage.item_name)
    #-----
    
    return dict(detailRecords=detailRecords,depot_id=depot_id,depotName=depotName,sl=sl,type_sl=type_sl,store_id=store_id,store_name=store_name,store_id_to=store_id_to,store_name_to=store_name_to,damage_date=damage_date,note=note,cause=cause,status=status,updatedBy=updatedBy)
    
    
#=======================
def recieve_reverse():
    c_id=session.cid
    depot_id=request.vars.depot_id
    sl=request.vars.sl
    issue_date=request.vars.issue_date
    issued_to=request.vars.issued_to
    discount=request.vars.discount
    note=request.vars.note
    ref_sl=request.vars.ref_sl
#    return ref_sl
    maxSl=sl

#    req_depot_id=depot_id
    reqSl=sl
    req_to=issued_to
    issue_date=issue_date
    ym_date=str(issue_date)[0:7]+'-01'
    req_note=note
#    total_discount=request.vars.total_discount            
    
#    try:
#        ref_sl=ref_sl    
#    except:
#        ref_sl=0
     
    #Confirm check box      
    checkbox=request.vars.checkbox
    btn_reverse=request.vars.btn_reverse
    if ((checkbox=='checkbox') and ((btn_reverse=='Reverse'))):
        pass
    else:
        session.flash = 'Please Confirm First'
        redirect (URL(c='depot',f='depot_stock_issue',vars=dict(req_sl=sl,depotid=depot_id)))
     #--------------------------------
     
#    return  btn_reverse
     
            #------------------- requisition items
            #Select all atems from requisition table based on sl ,date,req to
        
    store_id_rec=''
    store_name_rec=''
    recRecords=db((db.sm_receive.cid==c_id) & (db.sm_receive.depot_id==issued_to)& (db.sm_receive.receive_from==depot_id) & (db.sm_receive.ref_sl==reqSl)).select(db.sm_receive.store_id,db.sm_receive.store_name,limitby=(0,1))
    if recRecords:        
        store_id_rec=recRecords[0].store_id
        store_name_rec=recRecords[0].store_name
        
    reqRecords=db((db.sm_issue.cid==c_id) & (db.sm_issue.depot_id==depot_id) & (db.sm_issue.issued_to==issued_to)&(db.sm_issue.sl==sl)&(db.sm_issue.status=='Posted')&(db.sm_issue.issue_process_status=='Received')&(db.sm_issue.field2==0)).select(db.sm_issue.ALL,orderby=db.sm_issue.item_name)
            
#    return reqRecords
    if reqRecords:
        to_depot_name=''
        from_depot_name=''
        
        records=db((db.sm_depot.cid==c_id) & (db.sm_depot.depot_id==issued_to)).select(db.sm_depot.id,db.sm_depot.name,db.sm_depot.issue_sl,limitby=(0,1))
        if records:
            sl=records[0].issue_sl
            to_depot_name=records[0].name            
            maxSl=int(sl)+1
        else:
            maxSl=1
        records[0].update_record(issue_sl=maxSl)
        
        #Recieve SL
        sl_rec=0
        records=db((db.sm_depot.cid==c_id) & (db.sm_depot.depot_id==depot_id)).select(db.sm_depot.id,db.sm_depot.name,db.sm_depot.receive_sl,limitby=(0,1))
        if records:
            sl_rec=records[0].receive_sl
            from_depot_name=records[0].name
            sl_rec=int(sl_rec)+1
        else:
            sl_rec=1
        
        #Update issue_sl in sm_depot table
        records[0].update_record(receive_sl=sl_rec)
        
        #---------------                        
        reqDict={}
        insList=[]
        headFlag=False
        
        
        #---Recieve
        receiveHeadList=[]
        receiveDetailsList=[]
        recHeadDict={}
        recDetailsDict={}
        
        #Set all records of import req in a list.Insert issue head and detail based on list
#        return reqRecords
        totalAmount=0
        for row in reqRecords:            
            from_depot=row.depot_id
            sl=row.sl
            store_id=row.store_id
            store_name=row.store_name       
            issued_to=row.issued_to
            note=row.note
            req_sl=row.req_sl
            item_id=row.item_id
            item_name=row.item_name
            quantity=row.quantity
            dist_rate=row.dist_rate
            short_note=row.short_note
            total_discount=row.total_discount
            bonus_qty=row.bonus_qty
            totalAmount=totalAmount+(quantity*dist_rate)
            reqDict={'cid':c_id,'depot_id':issued_to,'depot_name':to_depot_name,'sl':maxSl,'store_id':store_id_rec,'store_name':store_name_rec,'issued_to':from_depot,'depot_to_name':from_depot_name,'issue_date':issue_date,'total_discount':total_discount,'req_sl':ref_sl,
                     'item_id':item_id,'item_name':item_name,'quantity':quantity,'dist_rate':dist_rate,'short_note':short_note,'ym_date':ym_date,'status':'Posted','issue_process_status':'Received','field2':1,'note':'Reversed'}
            insList.append(reqDict)
            if headFlag==False:                
                db.sm_issue_head.insert(cid=c_id,depot_id=issued_to,depot_name=to_depot_name,sl=maxSl,store_id=store_id_rec,store_name=store_name_rec,req_sl=ref_sl,issued_to=from_depot,depot_to_name=from_depot_name,issue_date=issue_date,total_discount=total_discount,ym_date=ym_date,status='Posted',issue_process_status='Received',field2=1,note='Reversed')
                headFlag=True
                
            # Recieve---------
            recDetailsDict={'cid':c_id,'depot_id':from_depot,'depot_name':from_depot_name,'sl':sl_rec,'store_id':store_id,'store_name':store_name,'receive_from':issued_to,'depot_from_name':to_depot_name,'receive_date':issue_date,'status':'Posted','total_discount':total_discount,'ref_sl':ref_sl,'item_id':item_id,'item_name':item_name,
                                    'quantity':quantity,'bonus_qty':bonus_qty,'dist_rate':dist_rate,'short_note':short_note,'ym_date':ym_date,'note':'Reversed','field2':1}
            receiveDetailsList.append(recDetailsDict)
            
        recHeadDict={'cid':c_id,'depot_id':from_depot,'depot_name':from_depot_name,'sl':sl_rec,'store_id':store_id,'store_name':store_name,'receive_from':issued_to,'depot_from_name':to_depot_name,'receive_date':issue_date,'status':'Posted','total_discount':total_discount,'ref_sl':req_sl,'ym_date':ym_date,'note':'Reversed','field2':1}
        receiveHeadList.append(recHeadDict)      
        
        
            
        rows=db.sm_issue.bulk_insert(insList)
#        return db._lastsql
        # receive
        
        headInsert=db.sm_receive_head.bulk_insert(receiveHeadList)
        detailInsert=db.sm_receive.bulk_insert(receiveDetailsList)
#        return db._lastsql
        db((db.sm_issue.cid==c_id)& (db.sm_issue.depot_id==depot_id) & (db.sm_issue.sl==sl)).update(field2=1,note='Reversed')
        db((db.sm_issue_head.cid==c_id)& (db.sm_issue_head.depot_id==depot_id) & (db.sm_issue_head.sl==sl)).update(field2=1,note='Reversed')
#        return "jghj"

        #Set transactionfor issue
#        {'cid':c_id,'depot_id':issued_to,'sl':maxSl,'issued_to':from_depot,'issue_date':issue_date,'total_discount':total_discount,'req_sl':ref_sl,
#                     'item_id':item_id,'item_name':item_name,'quantity':quantity,'dist_rate':dist_rate,'short_note':short_note,'ym_date':ym_date,'status':'Posted','issue_process_status':'Received','field2':1,'note':'Reversed'}
        
        if session.ledgerCreate=='YES':
            strData2=str(c_id)+'<fdfd>ISSUERECEIVE<fdfd>'+str(maxSl)+'<fdfd>'+str(datetime_fixed)+'<fdfd>'+str(issued_to)+'-'+str(maxSl)+':'+str(issued_to)+'-'+str(maxSl)+'<fdfd>DPT-'+str(issued_to)+'<fdfd>DPT-'+str(from_depot)+'<fdfd>'+str(totalAmount)
            resStr2=set_balance_transaction(strData2)
            
            resStrList2=resStr2.split('<sep>',resStr2.count('<sep>'))
            flag2=resStrList2[0]
            msg2=resStrList2[1]
        else:
            flag2='True'
            msg2=''
        
        if flag2=='True':
            session.flash = 'Successfully Reversed'
        else:
            session.flash = 'Error in Transaction'
        
        redirect (URL(c='depot',f='depot_stock_issue',vars=dict(req_sl=sl,depotid=depot_id)))
    else:
        session.flash = 'Sorry Already Reversed'
        redirect (URL(c='depot',f='depot_stock_issue',vars=dict(req_sl=sl,depotid=depot_id)))

#Validation for depot Payment

def depot_payment_validation(form):
    c_id=session.cid
    
    from_depot=str(request.vars.from_depot).split('|')[0]
    to_depot=str(request.vars.to_depot).split('|')[0]
    
    amount=float(request.vars.amount)
    confirmAmt=request.vars.confirmAmt
    
    toDptRecords=db((db.sm_depot.cid==c_id) & (db.sm_depot.depot_id==to_depot)).select(db.sm_depot.id,db.sm_depot.name,limitby=(0,1))
    if not toDptRecords:
        form.errors.to_depot=''
        response.flash = 'Invalid Received At'
    else:
        depot_to_name=toDptRecords[0].name
        
        fromDptRecords=db((db.sm_depot.cid==c_id) & (db.sm_depot.depot_id==from_depot)).select(db.sm_depot.id,db.sm_depot.name,limitby=(0,1))
        if not fromDptRecords:
            form.errors.from_depot=''
            response.flash = 'Invalid Paid By'
        else:
            depot_from_name=fromDptRecords[0].name
            
            
            form.vars.from_depot=from_depot
            form.vars.depot_from_name=depot_from_name
            
            form.vars.to_depot=to_depot
            form.vars.depot_to_name=depot_to_name
            
            try:
                amount=float(amount)
            except:
                amount=0
            
            try:
                confirmAmt=float(confirmAmt)
            except:
                confirmAmt=0
            
            if amount<=0:
                form.errors.amount=''
                response.flash = 'Required valid amount'
            else:
                if (amount!=confirmAmt):
                    form.errors.amount=''
                    response.flash = 'Invalid confirm amount'
                else:
                    amount=((amount*100)//1)/100
                    form.vars.amount=amount
                    
                    if from_depot==to_depot:
                        form.errors.from_depot=''
                        response.flash = 'Received At and Paid By can not be same'
                    else:
                        #-----------------
                        maxSl=1         
                        records=db((db.sm_depot.cid==c_id) & (db.sm_depot.depot_id==to_depot)).select(db.sm_depot.id,db.sm_depot.depot_payment_sl,db.sm_depot.name,limitby=(0,1))
                        if records:
                            sl=records[0].depot_payment_sl               
                            if sl==None:
                                sl=0
                            maxSl=int(sl)+1                               
                        
                        # sl update in depot
                        records[0].update_record(depot_payment_sl=maxSl)
                        
                        form.vars.sl=maxSl
                        

def depot_payment():
    response.title='Depot-Payment'
    #Check access permission
    #----------Task assaign----------
    task_id='rm_depot_payment_manage'
    task_id_view='rm_depot_payment_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !' 
        redirect (URL(c='default', f='home'))     
#   ---------------------    
    c_id=session.cid
        
    form =SQLFORM(db.sm_depot_payment,
                  fields=['to_depot','from_depot','pay_date','paytype','amount','narration'],
                  submit_button='Post'       
                  )
    
    #-----------------
    form.vars.cid=session.cid
    form.vars.amount=''
    if form.accepts(request.vars,session,onvalidation=depot_payment_validation):
        toDepot_Id=form.vars.to_depot
        fromDepot_Id=form.vars.from_depot
        sl=form.vars.sl
        pay_date=form.vars.pay_date
        amount=form.vars.amount
        
        if session.ledgerCreate=='YES':
            #format:cid<fdfd>tx_type<fdfd>sl<fdfd>datetime<fdfd>reference<fdfd>1st account with prefix (cr)<fdfd>2nd account with prefix (dr)<fdfd>tx_amount
            strData=str(c_id)+'<fdfd>DPTPAYMENT<fdfd>'+str(sl)+'<fdfd>'+str(datetime_fixed)+'<fdfd>'+str(toDepot_Id)+'-'+str(sl)+'<fdfd>DPT-'+str(fromDepot_Id)+'<fdfd>DPT-'+str(toDepot_Id)+'<fdfd>'+str(amount)
            resStr=set_balance_transaction(strData) 
            resStrList=resStr.split('<sep>',resStr.count('<sep>'))
            flag=resStrList[0]
            msg=resStrList[1]
        else:
            flag='True'
            msg='Success'
            
        if flag=='True':
            response.flash = msg
        else:
            db.rollback()
            response.flash = msg
        
      
    #   --------------------------- filter--------------------------
    btn_filter=request.vars.btn_filter
    btn_filter_all=request.vars.btn_filter_all
    reqPage=len(request.args)
    if btn_filter:
        session.btn_filter_dpay=btn_filter
        
        from_depot_value=request.vars.from_depot_value        
        session.from_depot_value_dpay=from_depot_value.upper()
        
        reqPage==0
        
    elif btn_filter_all:
        session.btn_filter_dpay=None
        session.from_depot_value_dpay=None
        
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
    qset=qset(db.sm_depot_payment.cid==c_id)
    
    if (session.user_type=='Depot'):
        qset=qset(db.sm_depot_payment.to_depot==session.depot_id)
        
    if (session.btn_filter_dpay):
        searchValue=str(session.from_depot_value_dpay).split('|')[0]
        qset=qset(db.sm_depot_payment.from_depot==searchValue)
        
    records=qset.select(db.sm_depot_payment.ALL,orderby=~db.sm_depot_payment.id,limitby=limitby)
    
    return dict(form=form,records=records,page=page,items_per_page=items_per_page,access_permission=access_permission,access_permission_view=access_permission_view)

def preview_depot_payment():
    #----------Task assaign----------
    task_id='rm_depot_payment_manage'
    task_id_view='rm_depot_payment_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL(c='default', f='home')) 
    
    #------------------------
    c_id=session.cid
    depot_id=request.vars.depotId
    sl=request.vars.sl

    #--------------- Title
    response.title='Preview Payment Received'
    
    
    records=db((db.sm_depot_payment.cid==session.cid)& (db.sm_depot_payment.to_depot==depot_id)& (db.sm_depot_payment.sl==sl)).select(db.sm_depot_payment.ALL,limitby=(0,1))
    
    sl=0
    to_depot=''
    to_depot_name=''
    from_depot=''
    from_depot_name=''
    pay_date=''
    issue_ref=0
    receive_ref=0
    paytype=''
    amount=0
    narration=''
    
    for row in records:
        sl=row.sl
        to_depot=row.to_depot
        to_depot_name=row.depot_to_name
        from_depot=row.from_depot
        from_depot_name=row.depot_from_name
        pay_date=row.pay_date
        issue_ref=row.issue_ref
        receive_ref=row.receive_ref
        paytype=row.paytype
        amount=row.amount
        narration=row.narration                 
        break
        
    #-----------  
    return dict(sl=sl,to_depot=to_depot,to_depot_name=to_depot_name,from_depot=from_depot,from_depot_name=from_depot_name,
                pay_date=pay_date,issue_ref=issue_ref,receive_ref=receive_ref,paytype=paytype,amount=amount,narration=narration)

def get_payment_depot():
    cid=session.cid
    
    depotType=request.vars.type #fromDepot/toDepot
    
    retStr=''
    if depotType=='toDepot':
        if (session.user_type=='Depot'):
            retStr=str(session.depot_id)+'|'+str(session.user_depot_name)
        else:
            rows=db((db.sm_depot.cid==cid)&(db.sm_depot.status=='ACTIVE')).select(db.sm_depot.depot_id,db.sm_depot.name,orderby=db.sm_depot.name)
            for row in rows:
                depot_id=str(row.depot_id)
                name=str(row.name).replace('|', ' ').replace(',', ' ')
                
                if retStr=='':
                    retStr=depot_id+'|'+name
                else:
                    retStr+=','+depot_id+'|'+name
    
    elif depotType=='fromDepot':
#         if (session.user_type=='Depot'):
#             toDepot=session.depot_id
#             
#             depotRows=db((db.sm_depot_settings.cid==cid)&(db.sm_depot_settings.from_to_type=='Receive')&(db.sm_depot_settings.depot_id_from_to==toDepot)&(db.sm_depot.cid==cid)&(db.sm_depot.depot_id==db.sm_depot_settings.depot_id)).select(db.sm_depot_settings.depot_id,db.sm_depot.name,orderby=db.sm_depot_settings.depot_id)
#             for row in depotRows:
#                 depot_id=str(row.sm_depot_settings.depot_id)
#                 name=str(row.sm_depot.name).replace('|', ' ').replace(',', ' ')
#                 
#                 if retStr=='':
#                     retStr=depot_id+'|'+name
#                 else:
#                     retStr+=','+depot_id+'|'+name            
#         else:
            rows=db((db.sm_depot.cid==cid)&(db.sm_depot.status=='ACTIVE')).select(db.sm_depot.depot_id,db.sm_depot.name,orderby=db.sm_depot.name)
            for row in rows:
                depot_id=str(row.depot_id)
                name=str(row.name).replace('|', ' ').replace(',', ' ')
                
                if retStr=='':
                    retStr=depot_id+'|'+name
                else:
                    retStr+=','+depot_id+'|'+name
        
    return retStr
    
#==================Recieve Confirm=============================
def depot_recieve_confirm(depot_id,sl,ref_sl):
    from operator import itemgetter
    
    c_id=session.cid
    
    depot_id=depot_id
    sl=sl
    ref_sl=ref_sl
    
    if (int(ref_sl)>0):
         
        trans_disputeDetailsList=[]
        trans_disputeDetailsDict={}
        ym_date=str(current_date)[0:7]+'-01' 
        
        depot_name=''
        store_id=''
        store_name=''
        
#        ==============Issue============
        rows_issue=db((db.sm_issue.cid==c_id)&(db.sm_issue.issued_to==depot_id)&(db.sm_issue.sl==ref_sl)&(db.sm_issue.status=='Posted')).select(db.sm_issue.ALL,orderby=db.sm_issue.item_id)
        issue_list=[]
        issueDict={}
        
        for row_issue in rows_issue:
            depot_name=str(row_issue.depot_to_name)
            
            item_id=str(row_issue.item_id)
            item_name=str(row_issue.item_name)
            batch_id=str(row_issue.batch_id)
            quantity_issue=row_issue.quantity
            
            bonus_qty_issue=row_issue.bonus_qty
            dist_rate=row_issue.dist_rate
            
            item_unit=row_issue.item_unit
            item_carton=row_issue.item_carton
            expiary_date=row_issue.expiary_date
            
            item_batch_id=item_id+'_'+batch_id
            
            issueDict={'item_batch_id':item_batch_id,'item_id':item_id,'item_name':item_name,'batch_id':batch_id,'quantity':int(quantity_issue),'bonus_qty':int(bonus_qty_issue),'dist_rate':dist_rate,'item_unit':item_unit,'item_carton':item_carton,'expiary_date':expiary_date}
            issue_list.append(issueDict)
        
#        ================Recieve================    
        rows_recieve=db((db.sm_receive.cid==c_id)&(db.sm_receive.depot_id==depot_id)&(db.sm_receive.sl==sl)&(db.sm_receive.status=='Posted')).select(db.sm_receive.ALL,orderby=db.sm_receive.item_id)
        recieve_list=[]
        recieveDict={}
        for row_recieve in rows_recieve:
            depot_name=str(row_recieve.depot_name)
            store_id=str(row_recieve.store_id)
            store_name=str(row_recieve.store_name)
            
            item_id=str(row_recieve.item_id)
            item_name=str(row_recieve.item_name)
            batch_id=str(row_recieve.batch_id)
            quantity_recieve=row_recieve.quantity
            
            bonus_qty_recieve=row_recieve.bonus_qty
            dist_rate=row_recieve.dist_rate
            
            item_unit=row_recieve.item_unit
            item_carton=row_recieve.item_carton
            expiary_date=row_recieve.expiary_date
            
            item_batch_id=item_id+'_'+batch_id
            
            recieveDict={'item_batch_id':item_batch_id,'item_id':item_id,'item_name':item_name,'batch_id':batch_id,'quantity':int(quantity_recieve),'bonus_qty':int(bonus_qty_recieve),'dist_rate':dist_rate,'item_unit':item_unit,'item_carton':item_carton,'expiary_date':expiary_date}
            recieve_list.append(recieveDict)    
            
        #----------------- Get Max SL
        maxSl=0
        records=db((db.sm_transaction_dispute_head.cid==c_id) & (db.sm_transaction_dispute_head.depot_id==depot_id)).select(db.sm_transaction_dispute_head.sl, orderby=~db.sm_transaction_dispute_head.sl,limitby=(0,1))
        if records:
            lastSl=records[0].sl
            maxSl=int(lastSl)+1
        else:
            maxSl=1
            
#        =============check in issue list====    
        for i in range(len(issue_list)):
            dictData_issue=issue_list[i] 
            
            if dictData_issue in recieve_list:
                continue
            else:
                mismatch_item_batch_issue = dictData_issue['item_batch_id']
                mismatch_item_issue = dictData_issue['item_id']
                mismatch_itemName_issue = dictData_issue['item_name']
                mismatch_batch_id_issue= dictData_issue['batch_id']                
                mismatch_quantity_issue = dictData_issue['quantity']
                mismatch_bonus_qty_issue= dictData_issue['bonus_qty']
                mismatch_dist_rate_issue= dictData_issue['dist_rate']
                
                mismatch_item_unit_issue= dictData_issue['item_unit']
                mismatch_item_carton_issue= dictData_issue['item_carton']
                mismatch_expiary_date_issue= dictData_issue['expiary_date']
                
                rec_index=-1
                try:
                    rec_index=map(itemgetter('item_batch_id'), recieve_list).index(mismatch_item_batch_issue)    
                except:
                    rec_index=-1                   
                    
                quantity_dispute=0
                bonus_qty_dispute=0
                
                if (rec_index!=-1):
                    dictData_recieve=recieve_list[rec_index]
                    
                    mismatch_quantity_recieve = dictData_recieve['quantity']
                    mismatch_bonus_qty_recieve= dictData_recieve['bonus_qty']
                else:
                    mismatch_quantity_recieve = 0
                    mismatch_bonus_qty_recieve= 0
                    
                quantity_dispute = int(mismatch_quantity_recieve)-int(mismatch_quantity_issue)
                bonus_qty_dispute = int(mismatch_bonus_qty_recieve)-int(mismatch_bonus_qty_issue)
                
                # Transaction Dispute---------
                if (int(quantity_dispute)!=0):
                    trans_disputeDetailsDict={'cid':c_id,'depot_id':depot_id,'depot_name':depot_name,'sl':maxSl,'store_id':store_id,'store_name':store_name,'issu_sl':int(ref_sl),'recieve_sl':sl,'status':'Open','item_id':mismatch_item_issue,'item_name':mismatch_itemName_issue,'batch_id':mismatch_batch_id_issue,'issued_quantity':mismatch_quantity_issue,
                                              'recieved_quantity':mismatch_quantity_recieve,'issued_bonus_qty':mismatch_bonus_qty_issue,'recieved_bonus_qty':mismatch_bonus_qty_recieve,'quantity':int(quantity_dispute),'bonus_qty':int(bonus_qty_dispute),'price':mismatch_dist_rate_issue,'item_unit':mismatch_item_unit_issue,'item_carton':mismatch_item_carton_issue,'expiary_date':mismatch_expiary_date_issue,'dispute_date':current_date,'ym_date':ym_date}
                    
                    if trans_disputeDetailsDict not in trans_disputeDetailsList:
                        trans_disputeDetailsList.append(trans_disputeDetailsDict)
        
#        =============check in recieve list====    
        for i in range(len(recieve_list)):
            dictData_recieve=recieve_list[i] 
            
            if dictData_recieve in issue_list:
                continue
            else:
                mismatch_item_batch_recieve = dictData_recieve['item_batch_id']
                mismatch_item_recieve = dictData_recieve['item_id']
                mismatch_itemName_recieve = dictData_recieve['item_name']
                mismatch_batch_id_recieve= dictData_recieve['batch_id']
                mismatch_quantity_recieve = dictData_recieve['quantity']
                mismatch_bonus_qty_recieve= dictData_recieve['bonus_qty']
                mismatch_dist_rate_recieve= dictData_recieve['dist_rate']
                
                mismatch_item_unit_recieve= dictData_recieve['item_unit']
                mismatch_item_carton_recieve= dictData_recieve['item_carton']
                mismatch_expiary_date_recieve= dictData_recieve['expiary_date']
                
                issue_index=-1
                try:
                    issue_index=map(itemgetter('item_batch_id'), issue_list).index(mismatch_item_batch_recieve)    
                except:
                    issue_index=-1                   
                
                quantity_dispute=0
                bonus_qty_dispute=0
                
                if (issue_index!=-1):
                    dictData_issue=issue_list[issue_index]
                    
                    mismatch_quantity_issue = dictData_issue['quantity']
                    mismatch_bonus_qty_issue= dictData_issue['bonus_qty']                    
                else:
                    mismatch_quantity_issue = 0
                    mismatch_bonus_qty_issue= 0
                
                quantity_dispute = int(mismatch_quantity_recieve)-int(mismatch_quantity_issue)
                bonus_qty_dispute = int(mismatch_bonus_qty_recieve)-int(mismatch_bonus_qty_issue)
                
                # Transactio Dispute---------
                if (int(quantity_dispute)!=0):
                    trans_disputeDetailsDict={'cid':c_id,'depot_id':depot_id,'depot_name':depot_name,'sl':maxSl,'store_id':store_id,'store_name':store_name,'issu_sl':int(ref_sl),'recieve_sl':sl,'status':'Open','item_id':mismatch_item_recieve,'item_name':mismatch_itemName_recieve,'batch_id':mismatch_batch_id_recieve,'issued_quantity':mismatch_quantity_issue,
                                              'recieved_quantity':mismatch_quantity_recieve,'issued_bonus_qty':mismatch_bonus_qty_issue,'recieved_bonus_qty':mismatch_bonus_qty_recieve,'quantity':int(quantity_dispute),'bonus_qty':int(bonus_qty_dispute),'price':mismatch_dist_rate_recieve,'item_unit':mismatch_item_unit_recieve,'item_carton':mismatch_item_carton_recieve,'expiary_date':mismatch_expiary_date_recieve,'dispute_date':current_date,'ym_date':ym_date}
                    if trans_disputeDetailsDict not in trans_disputeDetailsList:
                        trans_disputeDetailsList.append(trans_disputeDetailsDict)    
                        
        #--------------
        if (len(trans_disputeDetailsList)>0):            
            db.sm_transaction_dispute_head.insert(cid=c_id,depot_id=depot_id,depot_name=depot_name,sl=maxSl,store_id=store_id,store_name=store_name,dispute_date=current_date,issu_sl=ref_sl,recieve_sl=sl,status='Open',ym_date=ym_date)
            rows=db.sm_transaction_dispute.bulk_insert(trans_disputeDetailsList)       
    
    return 'Done'

#==================Transuction Dispute=========================
def depot_trans_dispute_list():
    #----------Task assaign----------
    task_id='rm_stock_trans_dispute_manage'
    task_id_view='rm_stock_trans_dispute_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))   
    
    response.title='Excess/Shortage'    
    #   --------------------- 
    c_id=session.cid
    
    #  ---------------filter-------    
    btn_filter_dispute=request.vars.btn_filter
    btn_all=request.vars.btn_all
    depot_id_value=str(request.vars.depot_id_value).strip()
    search_type=str(request.vars.search_type).strip()
    search_value=str(request.vars.search_value).strip()
#    return depot_id_value
    reqPage=len(request.args)
    #Set text for filter
    if btn_filter_dispute:
        session.btn_filter_dispute=btn_filter_dispute
        session.depot_id_value_dispute=depot_id_value 
        session.search_type_dispute=search_type
        session.search_value_dispute=search_value
#        return  session.depot_id_value_dispute
        #Check SL is numeric or not
        if (session.search_type_dispute=='SL'):
            sl=0
            if not(session.search_value_dispute=='' or session.search_value_dispute==None):
                try:       
                    sl=int(session.search_value_dispute)
                    session.search_value_dispute=sl
                except:
                    session.search_value_dispute=sl
                    response.flash='sl needs number value'
            else:
                session.search_value_dispute=sl
                
        reqPage=0
        
    elif btn_all:
        session.btn_filter_dispute=None
        session.depot_id_value_dispute=None
        session.search_type_dispute=None
        session.search_value_dispute=None
        reqPage=0
    
    
    #--------paging
    reqPage=0
    if reqPage:
        page=int(request.args[0])
    else:
        page=0
    items_per_page=session.items_per_page*10
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #--------end paging  
    
    qset=db()
    qset=qset(db.sm_transaction_dispute_head.cid==c_id)    
        
    if (session.user_type=='Depot'):
        qset=qset(db.sm_transaction_dispute_head.depot_id==session.depot_id)
    
    #Set query bsed on search type
#    return session.btn_filter_dispute
    if (session.btn_filter_dispute):
        if (session.user_type!='Depot'):
            if not (session.depot_id_value_dispute=='' or session.depot_id_value_dispute==None):
                searchValue=str(session.depot_id_value_dispute).split('|')[0]
                qset=qset(db.sm_transaction_dispute_head.depot_id==searchValue)
                
            else:
                qset=qset(db.sm_transaction_dispute_head.depot_id!='')
                
        #------------
        if (session.user_type=='Depot'):
            qset=qset(db.sm_transaction_dispute_head.depot_id==session.depot_id)
            
        if (session.search_type_dispute=='SL'):
            qset=qset(db.sm_transaction_dispute_head.sl==session.search_value_dispute)
            
        if (session.search_type_dispute=='IssueSL'):
            qset=qset(db.sm_transaction_dispute_head.issu_sl==session.search_value_dispute)
            
        if (session.search_type_dispute=='RecieveSL'):
            qset=qset(db.sm_transaction_dispute_head.recieve_sl==session.search_value_dispute)
            
        elif (session.search_type_dispute=='DATE'):
            qset=qset(db.sm_transaction_dispute_head.dispute_date==session.search_value_dispute)
            
        elif (session.search_type_dispute=='STATUS'):
            qset=qset(db.sm_transaction_dispute_head.status==session.search_value_dispute)
            
        elif (session.search_type_dispute=='UserID'):
            qset=qset(db.sm_transaction_dispute_head.updated_by==session.search_value_dispute.upper())
            
        
    records=qset.select(db.sm_transaction_dispute_head.ALL,orderby=~db.sm_transaction_dispute_head.id,limitby=limitby)
#    return db._lastsql
    #------------------------------------------------
    search_form =SQLFORM(db.sm_search_date)
    #-------------
    
    return dict(search_form=search_form,records=records,page=page,items_per_page=items_per_page,access_permission=access_permission,access_permission_view=access_permission_view)


def depot_trans_dispute():
    #----------Task assaign----------
    task_id='rm_stock_trans_dispute_manage'
    task_id_view='rm_stock_trans_dispute_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))   
        
#   --------------------- 
    response.title='Excess/Shortage'
    c_id=session.cid
    #------------------
    
    btn_update=request.vars.btn_update    
    req_sl=request.vars.req_sl    
    depotid=request.vars.depotid 
    if depotid=='' or depotid==None:
        depot_id=session.depot_id
        depot_name=session.user_depot_name
    else:
        depot_id=depotid
    
    sl=0
    status='Draft'
    damage_date=current_date
    note=''
    store_id=''
    store_name=''
    records=db((db.sm_transaction_dispute.cid==c_id)& (db.sm_transaction_dispute.depot_id==depot_id) & (db.sm_transaction_dispute.sl==req_sl)).select(db.sm_transaction_dispute.ALL,orderby=db.sm_transaction_dispute.item_name)
    for rec in records:
        depot_id=rec.depot_id
        depot_name=rec.depot_name
        sl=rec.sl
        issu_sl=rec.issu_sl
        recieve_sl=rec.recieve_sl
        status=rec.status
        dispute_date=rec.dispute_date
        note=rec.note
        store_id=rec.store_id
        store_name=rec.store_name
        break
        
    #-------------------    
    return dict(records=records,depot_id=depot_id,depot_name=depot_name,sl=sl,store_id=store_id,store_name=store_name,dispute_date=dispute_date,status=status,note=note,access_permission=access_permission,access_permission_view=access_permission_view,issu_sl=issu_sl,recieve_sl=recieve_sl)
    
def close_update_dispute():
    #----------Task assaign----------
    task_id='rm_stock_trans_dispute_manage'
    task_id_view='rm_stock_trans_dispute_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))   
        
    #   ---------------------
    response.title='Excess/Shortage'
    c_id=session.cid
    
    #------------------
    btn_update=request.vars.btn_update
    btn_resolve=request.vars.btn_resolve
    
    depotid=request.vars.depot_id
    req_sl=request.vars.req_sl
    note=request.vars.note
    
    if btn_update:
        db((db.sm_transaction_dispute_head.cid==c_id) & (db.sm_transaction_dispute_head.depot_id==depotid) & (db.sm_transaction_dispute_head.sl==req_sl)).update(note=note)
        db((db.sm_transaction_dispute.cid==c_id) & (db.sm_transaction_dispute.depot_id==depotid) & (db.sm_transaction_dispute.sl==req_sl)).update(note=note)
        
    elif btn_resolve:
        db((db.sm_transaction_dispute_head.cid==c_id) & (db.sm_transaction_dispute_head.depot_id==depotid) & (db.sm_transaction_dispute_head.sl==req_sl)).update(status="Resolved")
        db((db.sm_transaction_dispute.cid==c_id) & (db.sm_transaction_dispute.depot_id==depotid) & (db.sm_transaction_dispute.sl==req_sl)).update(status="Resolved")
        
    redirect (URL(c='depot',f='depot_trans_dispute',vars=dict(req_sl=req_sl,depotid=depotid)))
    
def preview_trans_dispute(): 
    #----------Task assaign----------
    task_id='rm_stock_trans_dispute_manage'
    task_id_view='rm_stock_trans_dispute_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))   
        
#   --------------------- 
    response.title='Excess/Shortage'
    c_id=session.cid
    #------------------
    btn_update=request.vars.btn_update
    
    req_sl=request.vars.req_sl    
    depotid=request.vars.depotid 
    if depotid=='' or depotid==None:
        depot_id=session.depot_id
        depot_name=session.user_depot_name
    else:
        depot_id=depotid
        
    sl=0
    status='Draft'
    damage_date=current_date
    note=''
    dispute_date=''
    recieve_sl=''
    issu_sl=''
    store_id=''
    store_name=''
    records=db((db.sm_transaction_dispute.cid==c_id)& (db.sm_transaction_dispute.depot_id==depot_id) & (db.sm_transaction_dispute.sl==req_sl)).select(db.sm_transaction_dispute.ALL,orderby=db.sm_transaction_dispute.item_name)
    
    for rec in records:
        depot_id=rec.depot_id
        depot_name=rec.depot_name
        sl=rec.sl
        recieve_sl=rec.recieve_sl
        issu_sl=rec.issu_sl
        status=rec.status
        dispute_date=rec.dispute_date
        note=rec.note
        store_id=rec.store_id
        store_name=rec.store_name
        break
    
    #-------------------    
    return dict(records=records,depot_id=depot_id,depot_name=depot_name,sl=sl,store_id=store_id,store_name=store_name,dispute_date=dispute_date,status=status,note=note,access_permission=access_permission,access_permission_view=access_permission_view,recieve_sl=recieve_sl,issu_sl=issu_sl)

