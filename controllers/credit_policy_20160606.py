import calendar


#===================Credit Policy================

def approved_credit_validation(form):    
    cid=session.cid
    
    approved_date=form.vars.approved_date
    client_id=str(request.vars.client_id).strip().upper().split('|')[0]
    credit_amount=form.vars.credit_amount
    
    clientId_rows_check=db((db.sm_client.cid==cid) & (db.sm_client.client_id==client_id)).select(db.sm_client.client_id,limitby=(0,1))
    if not clientId_rows_check:
        form.errors.client_id=''
        response.flash = 'Invalid Client Id '
    else:
        dateFlag=True
        try:
            approved_date=datetime.datetime.strptime(str(approved_date),'%Y-%m-%d') 
            if approved_date==False:
                dateFlag=False
        except:
            dateFlag=False
        
        if dateFlag==False:
            form.errors.approved_date=''
            response.flash="Invalid Approval Date"   
        else:
            if credit_amount<=0:
                form.errors.credit_amount=''
                response.flash = 'Invalid Credit Amount' 
            else:
                form.vars.client_id=client_id
                   
def approved_credit():
    task_id='rm_credit_policy_manage'
    task_id_view='rm_credit_policy_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))
     
    response.title='Approved Credit'
     
    cid=session.cid
    
  
    form =SQLFORM(db.sm_cp_approved,
                  fields=['approved_date','client_id','credit_amount','status'],       
                  submit_button='Save'
                  )
     
    form.vars.cid=cid
    if form.accepts(request.vars,session,onvalidation=approved_credit_validation):
       response.flash = 'Submitted Successfully'
     
         
    #  Set text for filter
    btn_filter_declared_item=request.vars.btn_filter_item
    btn_all=request.vars.btn_all
    reqPage=len(request.args)
     
    if btn_filter_declared_item:
        session.btn_filter_declared_item=btn_filter_declared_item
        session.search_type_declared_item=request.vars.search_type
        session.search_value_declared_item=request.vars.search_value
 
        reqPage=0
    elif btn_all:
        session.btn_filter_declared_item=None
        session.search_type_declared_item=None
        session.search_value_declared_item=None
        reqPage=0
     
    #--------paging
    if reqPage:
        page=int(request.args[0])
    else:
        page=0
    items_per_page=session.items_per_page
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #--------end paging  
    #Set query based on search type
    qset=db()
    qset=qset(db.sm_cp_approved.cid==cid)
    qset=qset(db.sm_client.cid==cid)
    #qset=qset(db.sm_level.cid==cid)
    qset=qset(db.sm_cp_approved.client_id==db.sm_client.client_id)
    #qset=qset(db.sm_client.area_id==db.sm_level.level_id)
    
    if (session.btn_filter_declared_item and session.search_type_declared_item=='Client_id'):
        searchValue=str(session.search_value_declared_item).split('|')[0]        
        qset=qset(db.sm_cp_approved.client_id==searchValue.upper())
        
    elif (session.btn_filter_declared_item and session.search_type_declared_item=='Status'):
        qset=qset(db.sm_cp_approved.status==session.search_value_declared_item.upper())
        
    records=qset.select(db.sm_cp_approved.ALL,db.sm_client.name,orderby=db.sm_cp_approved.client_id,limitby=limitby)
    totalCount=qset.count()
   
    #----------------- filter end
    return dict(form=form,records=records,totalCount=totalCount,page=page,items_per_page=items_per_page,access_permission=access_permission)
 
 
#Validation for item edit
def approved_credit_edit_validation(form):
     
    product_name_row=str(request.vars.product_name)
    product_name=check_special_char(product_name_row)
     
    form.vars.product_name=product_name
     
def approved_credit_edit():
    task_id='rm_credit_policy_manage'
    access_permission=check_role(task_id)
    if (access_permission==False):
        session.flash='Access is Denied !'
        redirect (URL('promotion','declared_item'))
     
    #Set combos for unit and catagory    
    response.title='Approved Credit'
    
    cid=session.cid
    page=request.args(0)
    rowID=request.args(1)
    record= db.sm_cp_approved(rowID) #or redirect(URL('index'))  
      
    form =SQLFORM(db.sm_cp_approved,
                  record=record,
                  deletable=True,
                  fields=['approved_date','client_id','credit_amount','status'],         
                  submit_button='Update'
                  )
     
    if form.accepts(request.vars, session,onvalidation=approved_credit_edit_validation):
        response.flash = 'Updated Successfully'        
        redirect(URL('approved_credit',args=[page]))
    
    recordRows=db((db.sm_cp_approved.cid==cid)&(db.sm_cp_approved.id==rowID)).select(db.sm_cp_approved.ALL,limitby=(0,1))
         
    return dict(form=form,page=page,recordRows=recordRows)
 
 
#====================================== Approved Credit BATCH UPLOAD 

def approved_credit_batch_upload():
    response.title='Approved Credit Batch upload'
    
    #----------Task assaign----------
    task_id='rm_campaign_manage'
    access_permission=check_role(task_id)
#    access_permission_view=check_role(task_id_view)
    if access_permission==False:
        session.flash='Access is Denied !'
        redirect (URL('credit_policy','approved_credit'))
    
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
        
        row_list=excel_data.split( '\n')
        total_row=len(row_list)
        
        client_list_exist=[]   
        
        client_id_list_excel=[]
                
        ins_list=[]
        ins_dict={}
        #   ----------------------
        #---------- rep area
        for i in range(total_row):
            if i>=30:
                break
            else:
                row_data=row_list[i]                    
                coloum_list=row_data.split( '\t')
                if len(coloum_list)==3:
                    clientIDExcel=str(coloum_list[1]).strip().upper()
                    
                    if clientIDExcel!='':
                        if clientIDExcel not in client_id_list_excel:
                            client_id_list_excel.append(clientIDExcel)
                    
                
        #Check valid client list based on excel sheet
        clientRows=db((db.sm_client.cid==c_id)&(db.sm_client.client_id.belongs(client_id_list_excel))&(db.sm_client.status=='ACTIVE')).select(db.sm_client.client_id,db.sm_client.name,orderby=db.sm_client.client_id)
        client_list_exist=clientRows.as_list()
        
        
        # main loop   
        for i in range(total_row):
            if i>=30: 
                break
            else:
                row_data=row_list[i]
            coloum_list=row_data.split( '\t')            
            
            if len(coloum_list)!=3:
                error_data=row_data+'(3 columns need in a row)\n'
                error_str=error_str+error_data
                count_error+=1
                continue
            else:
                approved_dateExcel=str(coloum_list[0]).strip().upper()                  
                clientIdExcel=str(coloum_list[1]).strip()   
                creditAmountExcel=str(coloum_list[2]).strip()
                status='ACTIVE'
                
                #------------------
                if approved_dateExcel=='' or clientIdExcel=='' or creditAmountExcel=='':
                    error_data=row_data+'(Required all value)\n'
                    error_str=error_str+error_data
                    count_error+=1
                    continue
                else:
                    dateFlag=True                    
                    try:
                        approved_dateExcel=datetime.datetime.strptime(approved_dateExcel,'%Y-%m-%d')
                        if approved_dateExcel==False:
                            dateFlag=False
                    except:
                        dateFlag=False 
                    
                    try:
                        creditAmountExcel=float(creditAmountExcel)
                    except:
                        creditAmountExcel=0
                     
                    #-------------------
                    
                    try:
                        valid_client_id=False
                        
#                         clientName=''
#                         itemName=''    
                        #Check valid client_list                         
                        for i in range(len(client_list_exist)):
                            myRowData=client_list_exist[i]                                
                            client_id=myRowData['client_id']
                            if (str(client_id).strip()==str(clientIdExcel).strip()):
                                valid_client_id=True
#                                 clientName=myRowData['name']
                                break
                        
                        #-----------------
                        if valid_client_id==False:
                            error_data=row_data+'(Invalid Customer ID)\n'
                            error_str=error_str+error_data
                            count_error+=1
                            continue 
                        else:
                            if dateFlag==False:
                                error_data=row_data+'(Invalid Approval Date)\n'
                                error_str=error_str+error_data
                                count_error+=1
                                continue                        
                            else:                                
                                existCheckRows=db((db.sm_cp_approved.cid==c_id)&(db.sm_cp_approved.client_id==clientIdExcel)).select(db.sm_cp_approved.id,limitby=(0,1))
                                if existCheckRows:
                                    error_data=row_data+'(Duplicate check for Customer ID)\n'
                                    error_str=error_str+error_data
                                    count_error+=1
                                    continue                            
                                else:
                                    if creditAmountExcel<=0:
                                        error_data=row_data+'(Invalid Credit Amount!)\n'
                                        error_str=error_str+error_data
                                        count_error+=1
                                        continue
                                    else:
                                        db.sm_cp_approved.insert(cid=c_id,approved_date=approved_dateExcel,client_id=clientIdExcel,credit_amount=creditAmountExcel,status=status)
                                        count_inserted+=1                                    
                    except:
                        error_data=row_data+'(error in process!)\n'
                        error_str=error_str+error_data
                        count_error+=1
                        continue
        
        if error_str=='':
            error_str='No error'
    
    return dict(count_inserted=count_inserted,count_error=count_error,error_str=error_str,total_row=total_row)

 
#============================================== Download
 
def approved_credit_download():
    #Check access permission
    #----------Task assaign----------
    task_id='rm_credit_policy_manage'
    task_id_view='rm_credit_policy_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))
      
     
    cid=session.cid
    records=''
    #Create query based on search type
    qset=db()
    qset=qset(db.sm_cp_approved.cid==cid)
    qset=qset(db.sm_client.cid==cid)
    qset=qset(db.sm_level.cid==cid)
    qset=qset(db.sm_cp_approved.client_id==db.sm_client.client_id)
    qset=qset(db.sm_client.area_id==db.sm_level.level_id)
     
    if (session.btn_filter_declared_item and session.search_type_declared_item=='Client_id'):
        searchValue=str(session.search_value_declared_item).split('|')[0]        
        qset=qset(db.sm_cp_approved.client_id==searchValue.upper())
        
    elif (session.btn_filter_declared_item and session.search_type_declared_item=='Status'):
        qset=qset(db.sm_cp_approved.status==session.search_value_declared_item.upper())
         
    records=qset.select(db.sm_cp_approved.ALL,db.sm_client.name,db.sm_level.level0_name,db.sm_level.level1_name,db.sm_level.level2_name,db.sm_level.level3_name,orderby=db.sm_cp_approved.client_id)
     
    #Create string for download as excel file
    myString='Approved Credit List\n'
    myString+='Approval Date,'+session.level1Name+',Area,Territory,Customer ID,Customer Name,Credit Amount,Status\n'
    #Replace coma from records. cause coma means new Column    
    for rec in records:
        approved_date=rec.sm_cp_approved.approved_date
        level1_name=str(rec.sm_level.level1_name)
        level2_name=str(rec.sm_level.level2_name)
        level3_name=str(rec.sm_level.level3_name)
        client_id=str(rec.sm_cp_approved.client_id)
        name=str(rec.sm_client.name)
        credit_amount=str(rec.sm_cp_approved.credit_amount)  
        status=str(rec.sm_cp_approved.status)
         
        myString+=str(approved_date)+','+str(level1_name)+','+str(level2_name)+','+str(level3_name)+','+str(client_id)+','+str(name)+','+str(credit_amount)+','+str(status)+'\n'
 
    #-----------
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_approved_credit.csv'   
    return str(myString)



#===================Rsm Credit===============
# def get_region_list():
#     c_id=session.cid
#     
#     refStr=''
#     
#     records=db(db.sm_level.cid==c_id).select(db.sm_level.ALL,orderby=db.sm_level.id)
#         
#     for row in records:
#         level1=str(row.level1)
# #         name=str(row.name)      
#         if refStr=='':
#             refStr=level1#+'|'+name
#         else:
#             refStr+=','+level1#+'|'+name        
#     
#     return refStr
# 
# 
# def get_brance_list():
#     c_id=session.cid
#     
#     refStr=''
#     
#     records=db(db.sm_depot.cid==c_id).select(db.sm_depot.ALL,orderby=db.sm_depot.id)
#         
#     for row in records:
#         depot_id=str(row.depot_id)
# #         name=str(row.name)      
#         if refStr=='':
#             refStr=depot_id#+'|'+name
#         else:
#             refStr+=','+depot_id#+'|'+name        
#     
#     return refStr

#=======get_regionId_ftr

def rsm_credit_validation(form):    
    cid=session.cid
    
    approved_date=form.vars.approved_date 
    region_id=str(request.vars.region_id).strip().upper().split('|')[0]
    branch_id=str(request.vars.branch_id).strip().upper().split('|')[0]
    
    credit_amount=form.vars.credit_amount
    
    regionId_rows_check=db((db.sm_level.cid==cid) & (db.sm_level.level1==region_id)).select(db.sm_level.depot_id,limitby=(0,1))
    if not regionId_rows_check:
        form.errors.region_id=''
        response.flash = 'Invalid Region ID '
    else:
        depotId_rows_check=db((db.sm_depot.cid==cid) & (db.sm_depot.depot_id==branch_id)).select(db.sm_depot.depot_id,limitby=(0,1))
        if not depotId_rows_check:
            form.errors.branch_id=''
            response.flash = 'Invalid Brance ID '
        else:
            dateFlag=True
            try:
                approved_date=datetime.datetime.strptime(str(approved_date),'%Y-%m-%d') 
                if approved_date==False:
                    dateFlag=False
            except:
                dateFlag=False
            
            if dateFlag==False:
                form.errors.approved_date=''
                response.flash="Invalid Approval Date"  
            else: 
                if credit_amount<=0:
                    form.errors.credit_amount=''
                    response.flash = 'Invalid Credit Amount' 
                else:
                    form.vars.branch_id=branch_id
                    form.vars.region_id=region_id 
                   
def rsm_credit():
    task_id='rm_credit_policy_manage'
    task_id_view='rm_credit_policy_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))
     
    response.title='Rsm Credit'
     
    cid=session.cid
     
    form =SQLFORM(db.sm_cp_rsm,
                  fields=['approved_date','region_id','branch_id','credit_amount','status'],       
                  submit_button='Save'
                  )
     
    form.vars.cid=cid
    if form.accepts(request.vars,session,onvalidation=rsm_credit_validation):
       response.flash = 'Submitted Successfully'
     
         
    #  Set text for filter
    btn_filter_region_id=request.vars.btn_filter_item
    btn_all=request.vars.btn_all
    reqPage=len(request.args)
     
    if btn_filter_region_id:
        session.btn_filter_region_id=btn_filter_region_id
        session.search_type_regionId=request.vars.search_type
        session.search_value_regionId=request.vars.search_value
 
        reqPage=0
    elif btn_all:
        session.btn_filter_region_id=None
        session.search_type_regionId=None
        session.search_value_regionId=None
        reqPage=0
     
    #--------paging
    if reqPage:
        page=int(request.args[0])
    else:
        page=0
    items_per_page=session.items_per_page
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #--------end paging  
    #Set query based on search type
    qset=db()
    qset=qset(db.sm_cp_rsm.cid==cid)
     
    if (session.btn_filter_region_id and session.search_type_regionId=='Region_id'):
        searchValue=str(session.search_value_regionId).split('|')[0]        
        qset=qset(db.sm_cp_rsm.region_id==searchValue.upper())
        
    elif (session.btn_filter_region_id and session.search_type_regionId=='Brance_id'):
        searchValue=str(session.search_value_regionId).split('|')[0]        
        qset=qset(db.sm_cp_rsm.branch_id==searchValue.upper())
        
    elif (session.btn_filter_region_id and session.search_type_regionId=='Status'):
        qset=qset(db.sm_cp_rsm.status==session.search_value_regionId.upper())
         
    records=qset.select(db.sm_cp_rsm.ALL,orderby=db.sm_cp_rsm.region_id,limitby=limitby)
    totalCount=qset.count()
     
    #----------------- filter end
    return dict(form=form,records=records,totalCount=totalCount,page=page,items_per_page=items_per_page,access_permission=access_permission)
 
 
#Validation for item edit
def rsm_credit_edit_validation(form):
     
    region_id=str(request.vars.region_id).split('|')[0]
    
    form.vars.region_id=region_id
     
def rsm_credit_edit():
    task_id='rm_campaign_manage'
    access_permission=check_role(task_id)
    if (access_permission==False):
        session.flash='Access is Denied !'
        redirect (URL('credit_policy','rsm_credit'))
     
    #Set combos for unit and catagory    
    response.title='Rsm Credit'
    
    cid=session.cid
    page=request.args(0)
    rowID=request.args(1)
    record= db.sm_cp_rsm(rowID) #or redirect(URL('index'))  
      
    form =SQLFORM(db.sm_cp_rsm,
                  record=record,
                  deletable=True,
                  fields=['approved_date','region_id','branch_id','credit_amount','status'],           
                  submit_button='Update'
                  )
     
    if form.accepts(request.vars, session,onvalidation=rsm_credit_edit_validation):
        response.flash = 'Updated Successfully'        
        redirect(URL('rsm_credit',args=[page]))
    
    recordRows=db((db.sm_cp_rsm.cid==cid)&(db.sm_cp_rsm.id==rowID)).select(db.sm_cp_rsm.ALL,limitby=(0,1))
             
    return dict(form=form,page=page,recordRows=recordRows)
 
 


#====================================== Rsm Credit BATCH UPLOAD 

def rsm_credit_batch_upload():
    response.title='RSM Credit Batch upload'
    
    #----------Task assaign----------
    task_id='rm_campaign_manage'
    access_permission=check_role(task_id)
#    access_permission_view=check_role(task_id_view)
    if access_permission==False:
        session.flash='Access is Denied !'
        redirect (URL('credit_policy','rsm_credit'))
    
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
        
        row_list=excel_data.split( '\n')
        total_row=len(row_list)
        
        region_list_exist=[] 
        brance_list_exist=[]  
        
        region_id_list_excel=[]
        brance_id_list_excel=[]
                
        ins_list=[]
        ins_dict={}
        #   ----------------------
        #---------- rep area
        for i in range(total_row):
            if i>=30:
                break
            else:
                row_data=row_list[i]                    
                coloum_list=row_data.split( '\t')
                if len(coloum_list)==4:
                    regionIDExcel=str(coloum_list[1]).strip().upper()
                    branceIDExcel=str(coloum_list[2]).strip().upper()
                    
                    if regionIDExcel!='':
                        if regionIDExcel not in region_id_list_excel:
                            region_id_list_excel.append(regionIDExcel)
                    
                    if branceIDExcel!='':
                        if branceIDExcel not in brance_id_list_excel:
                            brance_id_list_excel.append(branceIDExcel)
                    
#         regionId_rows_check=db((db.sm_level.cid==cid) & (db.sm_level.level0==region_id)).select(db.sm_level.depot_id,limitby=(0,1))
#     if not regionId_rows_check:
#         form.errors.region_id=''
#         response.flash = 'Invalid Region Id '
#     else:
#         depotId_rows_check=db((db.sm_depot.cid==cid) & (db.sm_depot.depot_id==branch_id)).select(db.sm_depot.depot_id,limitby=(0,1))
#         if not depotId_rows_check:
#             form.errors.branch_id=''
#             response.flash = 'Invalid Brance Id '
                        
        #Check valid Region list based on excel sheet
        regionRows=db((db.sm_level.cid==c_id)&(db.sm_level.level1.belongs(region_id_list_excel))).select(db.sm_level.level1,orderby=db.sm_level.level1)
        region_list_exist=regionRows.as_list()
        
        branceRows=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id.belongs(brance_id_list_excel))).select(db.sm_depot.depot_id,orderby=db.sm_depot.depot_id)
        brance_list_exist=branceRows.as_list()
        
        
        # main loop   
        for i in range(total_row):
            if i>=30: 
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
                approved_dateExcel=str(coloum_list[0]).strip().upper()                  
                regionIdExcel=str(coloum_list[1]).strip()   
                branceIdExcel=str(coloum_list[2]).strip() 
                creditAmountExcel=str(coloum_list[3]).strip()
                status='ACTIVE'
                
                #------------------
                if approved_dateExcel=='' or regionIdExcel==''or branceIdExcel=='' or creditAmountExcel=='':
                    error_data=row_data+'(Required all value)\n'
                    error_str=error_str+error_data
                    count_error+=1
                    continue
                else:
                    dateFlag=True                    
                    try:
                        approved_dateExcel=datetime.datetime.strptime(approved_dateExcel,'%Y-%m-%d')
                        if approved_dateExcel==False:
                            dateFlag=False
                    except:
                        dateFlag=False
                    
                    try:
                        creditAmountExcel=float(creditAmountExcel)
                    except:
                        creditAmountExcel=0
                     
                    #-------------------
                    
                    try:
                        valid_region_id=False
                        valid_brance_id=False
#                         clientName=''
#                         itemName=''    
                        #Check valid client_list                         
                        for i in range(len(region_list_exist)):
                            myRowData=region_list_exist[i]                                
                            region_id=myRowData['level1']
                            if (str(region_id).strip()==str(regionIdExcel).strip()):
                                valid_region_id=True
#                                 clientName=myRowData['name']
                                break                        
                        
                        if valid_region_id==True:# check item                                                     
                            for i in range(len(brance_list_exist)):
                                myRowData=brance_list_exist[i]                                
                                depot_id=myRowData['depot_id']
                                if (str(depot_id).strip()==str(branceIdExcel).strip()):
                                    valid_brance_id=True
#                                     itemName=myRowData['name']
                                    break
                        
                        #-----------------
                        if valid_region_id==False:
                               error_data=row_data+'(Invalid Region ID)\n'
                               error_str=error_str+error_data
                               count_error+=1
                               continue  
                        else:
                            if dateFlag==False:
                                error_data=row_data+'(Invalid Approval Date)\n'
                                error_str=error_str+error_data
                                count_error+=1
                                continue
                            else:
                                if valid_brance_id==False:
                                    error_data=row_data+'(Invalid Brance ID)\n'
                                    error_str=error_str+error_data
                                    count_error+=1
                                    continue                      
                                else:                                
                                    existCheckRows=db((db.sm_cp_rsm.cid==c_id)&(db.sm_cp_rsm.approved_date==approved_dateExcel)&(db.sm_cp_rsm.region_id==regionIdExcel)&(db.sm_cp_rsm.branch_id==branceIdExcel)).select(db.sm_cp_rsm.id,limitby=(0,1))
                                    if existCheckRows:
                                        error_data=row_data+'(Duplicate check for Approval Date, Region ID and Brance ID)\n'
                                        error_str=error_str+error_data
                                        count_error+=1
                                        continue                            
                                    else:
                                        if creditAmountExcel<=0:
                                            error_data=row_data+'(Invalid Credit Amount!)\n'
                                            error_str=error_str+error_data
                                            count_error+=1
                                            continue
                                        else:
                                            db.sm_cp_rsm.insert(cid=c_id,approved_date=approved_dateExcel,region_id=regionIdExcel,branch_id=branceIdExcel,credit_amount=creditAmountExcel,status=status)
                                            count_inserted+=1                                    
                    except:
                        error_data=row_data+'(error in process!)\n'
                        error_str=error_str+error_data
                        count_error+=1
                        continue
        
        if error_str=='':
            error_str='No error'
    
    return dict(count_inserted=count_inserted,count_error=count_error,error_str=error_str,total_row=total_row)


 
#============================================== Download
 
def rsm_credit_download():
    #Check access permission
    #----------Task assaign----------
    task_id='rm_campaign_manage'
    task_id_view='rm_campaign_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))
     
     
    cid=session.cid
    records=''
    #Create query based on search type
    qset=db()
    qset=qset(db.sm_cp_rsm.cid==cid)
     
    if (session.btn_filter_region_id and session.search_type_regionId=='Region_id'):
        searchValue=str(session.search_value_regionId).split('|')[0]        
        qset=qset(db.sm_cp_rsm.region_id==searchValue.upper())
        
    elif (session.btn_filter_region_id and session.search_type_regionId=='Brance_id'):
        searchValue=str(session.search_value_regionId).split('|')[0]        
        qset=qset(db.sm_cp_rsm.branch_id==searchValue.upper())
        
    elif (session.btn_filter_region_id and session.search_type_regionId=='Status'):
        qset=qset(db.sm_cp_rsm.status==session.search_value_regionId.upper())
         
    records=qset.select(db.sm_cp_rsm.ALL,orderby=db.sm_cp_rsm.region_id)
     
    #Create string for download as excel file
    myString='Rsm Credit List\n'
    myString+='Approved date, '+session.level1Name+' ID,Brance ID,Credit Amount,Status\n'
    #Replace coma from records. cause coma means new Column    
    for rec in records:
        approved_date=rec.approved_date
        region_id=str(rec.region_id)
        branch_id=str(rec.branch_id)  
        credit_amount=str(rec.credit_amount)      
        status=str(rec.status)
         
        myString+=str(approved_date)+','+str(region_id)+','+str(branch_id)+','+str(credit_amount)+','+str(status)+'\n'
 
    #-----------
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_rsm_credit.csv'   
    return str(myString)



#==================special Credit
def special_credit_validation(form):    
    cid=session.cid
     
    region_id=str(request.vars.region_id).strip().upper().split('|')[0]
    branch_id=str(request.vars.branch_id).strip().upper().split('|')[0]
    
    credit_amount=form.vars.credit_amount    
    approved_date=request.vars.approved_date
    from_date=request.vars.from_date
    to_date=request.vars.to_date
    
    appdateFlag=True
    try:
        approved_date=datetime.datetime.strptime(str(approved_date),'%Y-%m-%d')          
        if approved_date==False:
            appdateFlag=False
    except:
        appdateFlag=False
    
    if appdateFlag==False:
        form.errors.approved_date=''
        response.flash="Invalid Approval Date"
    else:
        dateFlag=True
        try:
            from_date=datetime.datetime.strptime(str(from_date),'%Y-%m-%d')
            to_date=datetime.datetime.strptime(str(to_date),'%Y-%m-%d')            
            if from_date>to_date:
                dateFlag=False
        except:
            dateFlag=False
        
        if dateFlag==False:
            form.errors.from_date=''
            response.flash="Invalid Date Range"
        else:
            regionId_rows_check=db((db.sm_level.cid==cid) & (db.sm_level.level1==region_id)).select(db.sm_level.depot_id,limitby=(0,1))
            if not regionId_rows_check:
                form.errors.region_id=''
                response.flash = 'Invalid Region Id '
            else:
                depotId_rows_check=db((db.sm_depot.cid==cid) & (db.sm_depot.depot_id==branch_id)).select(db.sm_depot.depot_id,limitby=(0,1))
                if not depotId_rows_check:
                    form.errors.branch_id=''
                    response.flash = 'Invalid Brance Id '
                else: 
                    if credit_amount<=0:
                        form.errors.credit_amount=''
                        response.flash = 'Invalid Credit Amount' 
                    else:
                        form.vars.branch_id=branch_id
                        form.vars.region_id=region_id 
                   
def special_credit():
    task_id='rm_credit_policy_manage'
    task_id_view='rm_credit_policy_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))
     
    response.title='Special Credit'
     
    cid=session.cid
     
    form =SQLFORM(db.sm_cp_special,
                  fields=['approved_date','from_date','to_date','credit_type','region_id','branch_id','credit_amount','status'],       
                  submit_button='Save'
                  )
     
    form.vars.cid=cid
    if form.accepts(request.vars,session,onvalidation=special_credit_validation):
       response.flash = 'Submitted Successfully'
     
         
    #  Set text for filter
    btn_filter_special_credit=request.vars.btn_filter_item
    btn_all=request.vars.btn_all
    reqPage=len(request.args)
     
    if btn_filter_special_credit:
        session.btn_filter_special_credit=btn_filter_special_credit
        session.search_type_special_credit=request.vars.search_type
        session.search_value_special_credit=request.vars.search_value
 
        reqPage=0
    elif btn_all:
        session.btn_filter_special_credit=None
        session.search_type_special_credit=None
        session.search_value_special_credit=None
        reqPage=0
     
    #--------paging
    if reqPage:
        page=int(request.args[0])
    else:
        page=0
    items_per_page=session.items_per_page
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #--------end paging  
    #Set query based on search type
    qset=db()
    qset=qset(db.sm_cp_special.cid==cid)
     
    if (session.btn_filter_special_credit and session.search_type_special_credit=='Region_id'):
        searchValue=str(session.search_value_special_credit).split('|')[0]        
        qset=qset(db.sm_cp_special.region_id==searchValue.upper())
        
    elif (session.btn_filter_special_credit and session.search_type_special_credit=='Brance_id'):
        searchValue=str(session.search_value_special_credit).split('|')[0]        
        qset=qset(db.sm_cp_special.branch_id==searchValue.upper())
        
    elif (session.btn_filter_special_credit and session.search_type_special_credit=='Status'):
        qset=qset(db.sm_cp_special.status==session.search_value_special_credit.upper())
         
    records=qset.select(db.sm_cp_special.ALL,orderby=db.sm_cp_special.region_id,limitby=limitby)
    totalCount=qset.count()
     
    #----------------- filter end
    return dict(form=form,records=records,totalCount=totalCount,page=page,items_per_page=items_per_page,access_permission=access_permission)
 
 
#Validation for item edit
def special_credit_edit_validation(form):
     
    region_id=str(request.vars.region_id).split('|')[0]
     
    form.vars.region_id=region_id
     
def special_credit_edit():
    task_id='rm_campaign_manage'
    access_permission=check_role(task_id)
    if (access_permission==False):
        session.flash='Access is Denied !'
        redirect (URL('credit_policy','rsm_credit'))
     
    #Set combos for unit and catagory    
    response.title='Special Credit'
    
    cid=session.cid
    page=request.args(0)
    rowID=request.args(1)
    record= db.sm_cp_special(rowID) #or redirect(URL('index'))  
      
    form =SQLFORM(db.sm_cp_special,
                  record=record,
                  deletable=True,
                  fields=['approved_date','from_date','to_date','credit_type','region_id','branch_id','credit_amount','status'],           
                  submit_button='Update'
                  )
     
    if form.accepts(request.vars, session,onvalidation=special_credit_edit_validation):
        response.flash = 'Updated Successfully'        
        redirect(URL('special_credit',args=[page]))
     
    recordRows=db((db.sm_cp_special.cid==cid)&(db.sm_cp_special.id==rowID)).select(db.sm_cp_special.ALL,limitby=(0,1))
             
    return dict(form=form,page=page,recordRows=recordRows)
 
 
#====================================== Special Credit BATCH UPLOAD 

def special_credit_batch_upload():
    response.title='Special Credit Batch upload'
    
    #----------Task assaign----------
    task_id='rm_campaign_manage'
    access_permission=check_role(task_id)
#    access_permission_view=check_role(task_id_view)
    if access_permission==False:
        session.flash='Access is Denied !'
        redirect (URL('credit_policy','special_credit'))
    
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
        
        row_list=excel_data.split( '\n')
        total_row=len(row_list)
        
        region_list_exist=[] 
        brance_list_exist=[]  
        
        region_id_list_excel=[]
        brance_id_list_excel=[]
                
        ins_list=[]
        ins_dict={}
        #   ----------------------
        #---------- rep area
        for i in range(total_row):
            if i>=30:
                break
            else:
                row_data=row_list[i]                    
                coloum_list=row_data.split( '\t')
                if len(coloum_list)==7:
                    regionIDExcel=str(coloum_list[4]).strip().upper()
                    branceIDExcel=str(coloum_list[5]).strip().upper()
                    
                    if regionIDExcel!='':
                        if regionIDExcel not in region_id_list_excel:
                            region_id_list_excel.append(regionIDExcel)
                    
                    if branceIDExcel!='':
                        if branceIDExcel not in brance_id_list_excel:
                            brance_id_list_excel.append(branceIDExcel)
                   
                        
        #Check valid Region list based on excel sheet
        regionRows=db((db.sm_level.cid==c_id)&(db.sm_level.level1.belongs(region_id_list_excel))).select(db.sm_level.level1,orderby=db.sm_level.level1)
        region_list_exist=regionRows.as_list()
        
        branceRows=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id.belongs(brance_id_list_excel))).select(db.sm_depot.depot_id,orderby=db.sm_depot.depot_id)
        brance_list_exist=branceRows.as_list()
        
        
        # main loop   
        for i in range(total_row):
            if i>=30: 
                break
            else:
                row_data=row_list[i]
            coloum_list=row_data.split( '\t')            
            
            if len(coloum_list)!=7:
                error_data=row_data+'(7 columns need in a row)\n'
                error_str=error_str+error_data
                count_error+=1
                continue
            else:
                approved_dateExcel=str(coloum_list[0]).strip()  
                from_date=str(coloum_list[1]).strip()   
                to_date=str(coloum_list[2]).strip() 
                creditType=str(coloum_list[3]).strip()               
                regionIdExcel=str(coloum_list[4]).strip()   
                branceIdExcel=str(coloum_list[5]).strip() 
                creditAmountExcel=str(coloum_list[6]).strip()
                status='ACTIVE'
                
                #------------------
                if approved_dateExcel=='' or from_date==''or to_date=='' or creditType=='' or regionIdExcel==''or branceIdExcel=='' or creditAmountExcel=='':
                    error_data=row_data+'(Required all value)\n'
                    error_str=error_str+error_data
                    count_error+=1
                    continue
                else:
                    approvedDateFlag=True 
                    try:
                        approved_dateExcel=datetime.datetime.strptime(approved_dateExcel,'%Y-%m-%d')
                        if approved_dateExcel==False:
                            approvedDateFlag=False
                    except:
                        approvedDateFlag=False
                    else:
                        dateFlag=True                    
                        try:
                            from_date=datetime.datetime.strptime(from_date,'%Y-%m-%d')
                            to_date=datetime.datetime.strptime(to_date,'%Y-%m-%d')
                            if from_date>to_date:
                                dateFlag=False
                        except:
                            dateFlag=False
                        
                        try:
                            creditAmountExcel=float(creditAmountExcel)
                        except:
                            creditAmountExcel=0
                     
                    #-------------------
                    
#                     try:
                        valid_region_id=False
                        valid_brance_id=False
#                         clientName=''
#                         itemName=''    
                        #Check valid region_list                         
                        for i in range(len(region_list_exist)):
                            myRowData=region_list_exist[i]                                
                            region_id=myRowData['level1']
                            if (str(region_id).strip()==str(regionIdExcel).strip()):
                                valid_region_id=True
#                                 clientName=myRowData['name']
                                break                        
                        
                        if valid_region_id==True:# check brance                                                     
                            for i in range(len(brance_list_exist)):
                                myRowData2=brance_list_exist[i]                                
                                depot_id=myRowData2['depot_id']
                                if (str(depot_id).strip()==str(branceIdExcel).strip()):
                                    valid_brance_id=True
#                                     itemName=myRowData['name']
                                    break
                        
                        #-----------------
                        if approvedDateFlag==False:
                            error_data=row_data+'(Invalid Approval Date)\n'
                            error_str=error_str+error_data
                            count_error+=1
                            continue 
                        else: 
                            if dateFlag==False:
                                error_data=row_data+'(Invalid Date Range)\n'
                                error_str=error_str+error_data
                                count_error+=1
                                continue 
                            else:
                                if valid_region_id==False:
                                    error_data=row_data+'(Invalid Region ID)\n'
                                    error_str=error_str+error_data
                                    count_error+=1
                                    continue   
                                else:
                                    if valid_brance_id==False:
                                        error_data=row_data+'(Invalid Brance ID)\n'
                                        error_str=error_str+error_data
                                        count_error+=1
                                        continue                      
                                    else:                                
                                        existCheckRows=db((db.sm_cp_special.cid==c_id)&(db.sm_cp_special.to_date>=from_date)&(db.sm_cp_special.region_id==regionIdExcel)&(db.sm_cp_special.branch_id==branceIdExcel)).select(db.sm_cp_special.id,limitby=(0,1))
                                        if existCheckRows:
                                            error_data=row_data+'(Duplicate check for Date, Region ID and Brance ID)\n'
                                            error_str=error_str+error_data
                                            count_error+=1
                                            continue                    
                                        else:
                                            if creditAmountExcel<=0:
                                                error_data=row_data+'(Invalid Credit Amount!)\n'
                                                error_str=error_str+error_data
                                                count_error+=1
                                                continue
                                            else:
                                                
                                                try:
                                                    db.sm_cp_special.insert(cid=c_id,approved_date=approved_dateExcel,from_date=from_date,to_date=to_date,credit_type=creditType,region_id=regionIdExcel,branch_id=branceIdExcel,credit_amount=creditAmountExcel,status=status)
                                                    count_inserted+=1                                    
                                                except:
                                                    error_data=row_data+'(error in process!)\n'
                                                    error_str=error_str+error_data
                                                    count_error+=1
                                                    continue
        
        if error_str=='':
            error_str='No error'

    return dict(count_inserted=count_inserted,count_error=count_error,error_str=error_str,total_row=total_row)

  
#============================================== Download
 
def special_credit_download():
    #Check access permission
    #----------Task assaign----------
    task_id='rm_campaign_manage'
    task_id_view='rm_campaign_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))
     
     
    cid=session.cid
    records=''
    #Create query based on search type
    qset=db()
    qset=qset(db.sm_cp_special.cid==cid)
     
    if (session.btn_filter_special_credit and session.search_type_special_credit=='Region_id'):
        searchValue=str(session.search_value_special_credit).split('|')[0]        
        qset=qset(db.sm_cp_special.region_id==searchValue.upper())
        
    elif (session.btn_filter_special_credit and session.search_type_special_credit=='Brance_id'):
        searchValue=str(session.search_value_special_credit).split('|')[0]        
        qset=qset(db.sm_cp_special.branch_id==searchValue.upper())
        
    elif (session.btn_filter_special_credit and session.search_type_special_credit=='Status'):
        qset=qset(db.sm_cp_special.status==session.search_value_special_credit.upper())
         
    records=qset.select(db.sm_cp_special.ALL,orderby=db.sm_cp_special.region_id)
     
    #Create string for download as excel file
    myString='Special Credit List\n'
    myString+='Approved date,From Date,To Date,Credit Type,Region ID,Brance ID,Credit Amount,Status\n'
    #Replace coma from records. cause coma means new Column    
    for rec in records:
        approved_date=rec.approved_date
        from_date=rec.from_date
        to_date=rec.to_date
        credit_type=rec.credit_type
        region_id=str(rec.region_id)
        branch_id=str(rec.branch_id)  
        credit_amount=str(rec.credit_amount)      
        status=str(rec.status)
         
        myString+=str(approved_date)+','+str(from_date)+','+str(to_date)+','+str(credit_type)+','+str(region_id)+','+str(branch_id)+','+str(credit_amount)+','+str(status)+'\n'
 
    #-----------
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_special_credit.csv'   
    return str(myString)

