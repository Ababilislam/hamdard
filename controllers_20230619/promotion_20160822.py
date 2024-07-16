import calendar

#Validation for item
def approved_rate_validation(form):    
    cid=session.cid
    
    client_id=str(request.vars.client_id).strip().upper().split('|')[0]
    
    from_date=request.vars.from_date
    to_date=request.vars.to_date
    
    product_id=str(request.vars.product_id).strip().upper().split('|')[0]
    
    fixed_percent_rate=form.vars.fixed_percent_rate
    
    rows_check=db((db.sm_client.cid==cid) & (db.sm_client.client_id==client_id)).select(db.sm_client.name,db.sm_client.depot_id,db.sm_client.depot_name,limitby=(0,1))
    if not rows_check:
        form.errors.client_id=''
        response.flash = 'Invalid Client Id '
    else:
        client_name=rows_check[0].name
        depot_id=rows_check[0].depot_id
        depot_name=rows_check[0].depot_name
        
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
            if fixed_percent_rate<=0:
                form.errors.fixed_percent_rate=''
                response.flash = 'Invalid Rate '    
            else:
                product_rows_check=db((db.sm_item.cid==cid) & (db.sm_item.item_id==product_id)).select(db.sm_item.name,limitby=(0,1))
                if not product_rows_check:
                    form.errors.product_id=''
                    response.flash = 'Invalid Product Id '
                else:
                    product_name=product_rows_check[0].name
                    
                    form.vars.client_id=client_id
                    form.vars.client_name=client_name
                    form.vars.product_id=product_id
                    form.vars.product_name=product_name
                    form.vars.depot_id=depot_id
                    form.vars.depot_name=depot_name
                    
def approved_rate():
    task_id='rm_campaign_manage'
    task_id_view='rm_campaign_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))
    
    response.title='Approved Rate'
    
    cid=session.cid
    
    form =SQLFORM(db.sm_promo_approved_rate,
                  fields=['client_id','client_name','from_date','to_date','product_id','product_name','bonus_type','fixed_percent_rate','status'],       
                  submit_button='Save'
                  )
    
    form.vars.cid=cid
    if form.accepts(request.vars,session,onvalidation=approved_rate_validation):       
       db((db.sm_settings.cid == cid)&(db.sm_settings.s_key == 'PROMO_DATE')).update(s_value=datetime_fixed)
       
       response.flash = 'Submitted Successfully'
    
    btn_clean=request.vars.btn_clean    
    if btn_clean:
        check_clean=request.vars.check_clean
        if check_clean!='YES':
            response.flash = 'Required checked confirmation'
        else:
            if (session.btn_filter_approved_rate and session.search_type_approved_rate=='Client_id'):
                searchValue=str(session.search_value_approved_rate).upper().split('|')[0]
                db((db.sm_promo_approved_rate.cid==cid)&(db.sm_promo_approved_rate.client_id==searchValue)).delete()
                response.flash = 'Data cleaned successfully. Client :'+str(session.search_value_approved_rate)
                
            elif (session.btn_filter_approved_rate and session.search_type_approved_rate=='Product_id'):
                searchValue=str(session.search_value_approved_rate).upper().split('|')[0]
                db((db.sm_promo_approved_rate.cid==cid)&(db.sm_promo_approved_rate.product_id==searchValue)).delete()
                response.flash = 'Data cleaned successfully. Product :'+str(session.search_value_approved_rate)
                
            else:
                response.flash = 'Required filter by client or Product'
                
    #  Set text for filter
    btn_filter_approved_rate=request.vars.btn_filter_item
    btn_all=request.vars.btn_all
    reqPage=len(request.args)
    
    if btn_filter_approved_rate:
        session.btn_filter_approved_rate=btn_filter_approved_rate
        session.search_type_approved_rate=request.vars.search_type
        session.search_value_approved_rate=request.vars.search_value

        reqPage=0
    elif btn_all:
        session.btn_filter_approved_rate=None
        session.search_type_approved_rate=None
        session.search_value_approved_rate=None
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
    qset=qset(db.sm_promo_approved_rate.cid==cid)
    if (session.user_type=='Depot'):
        qset=qset(db.sm_promo_approved_rate.depot_id==session.depot_id)
        
    if (session.user_type!='Depot'):
        if (session.btn_filter_approved_rate and session.search_type_approved_rate=='DepotId'):
            searchValue=str(session.search_value_approved_rate).split('|')[0]        
            qset=qset(db.sm_promo_approved_rate.depot_id==searchValue.upper())
        else:
            qset=qset(db.sm_promo_approved_rate.depot_id!='')
            
    if (session.btn_filter_approved_rate and session.search_type_approved_rate=='Client_id'):
        searchValue=str(session.search_value_approved_rate).split('|')[0]        
        qset=qset(db.sm_promo_approved_rate.client_id==searchValue.upper())
        
    elif (session.btn_filter_approved_rate and session.search_type_approved_rate=='Product_id'):
         searchValue=str(session.search_value_approved_rate).split('|')[0]    
         qset=qset(db.sm_promo_approved_rate.product_id==searchValue.upper())
        
    elif (session.btn_filter_approved_rate and session.search_type_approved_rate=='Status'):
        qset=qset(db.sm_promo_approved_rate.status==session.search_value_approved_rate.upper())
        
    records=qset.select(db.sm_promo_approved_rate.ALL,orderby=db.sm_promo_approved_rate.client_name,limitby=limitby)
    totalCount=qset.count()
    
    #----------------- filter end
    return dict(form=form,records=records,totalCount=totalCount,page=page,items_per_page=items_per_page,access_permission=access_permission)


#Validation for item edit
def approved_rate_edit_validation(form):
    
    item_name_row=str(request.vars.client_name)
    client_name=check_special_char(item_name_row)
    
    
    form.vars.client_name=client_name

def approved_rate_edit():
    task_id='rm_campaign_manage'
    access_permission=check_role(task_id)
    if (access_permission==False):
        session.flash='Access is Denied !'
        redirect (URL('promotion','approved_rate'))
    
    #Set combos for unit and catagory    
    response.title='Approved Rate'
    
    cid=session.cid
    
    page=request.args(0)
    rowID=request.args(1)
    record= db.sm_promo_approved_rate(rowID) #or redirect(URL('index'))  
     
    form =SQLFORM(db.sm_promo_approved_rate,
                  record=record,
                  deletable=True,                  
                  fields=['client_id','client_name','from_date','to_date','product_id','product_name','bonus_type','fixed_percent_rate','status'],       
                  submit_button='Update'
                  )
    
    if form.accepts(request.vars, session,onvalidation=approved_rate_edit_validation):
        db((db.sm_settings.cid == cid)&(db.sm_settings.s_key == 'PROMO_DATE')).update(s_value=datetime_fixed)
        
        response.flash = 'Updated Successfully'        
        redirect(URL('approved_rate',args=[page]))
     
    recordRows=db((db.sm_promo_approved_rate.cid==cid)&(db.sm_promo_approved_rate.id==rowID)).select(db.sm_promo_approved_rate.ALL,limitby=(0,1))
    
    return dict(form=form,page=page,recordRows=recordRows)


def approved_rate_product_add():
    task_id='rm_campaign_manage'
    access_permission=check_role(task_id)
    if (access_permission==False):
        session.flash='Access is Denied !'
        redirect (URL('promotion','approved_rate'))
       
    response.title='Add New Product'    
    c_id=session.cid    
    if (c_id=='' or c_id==None):
        redirect(URL('default','index'))
    
    
    btn_percentage_add=request.vars.btn_percentage_add
    btn_fixed_add=request.vars.btn_fixed_add
    if btn_percentage_add:
        percentage_prod_id_new=request.vars.percentage_prod_id_new
        percentage_prod_id_exist=request.vars.percentage_prod_id_exist
        if percentage_prod_id_new=='' or percentage_prod_id_exist=='':
            response.flash='Required Both Product ID'
        else:
            if percentage_prod_id_new==percentage_prod_id_exist:
                response.flash='Both Product ID can not be same'
            else:
                newIdRow=db((db.sm_item.cid==c_id) & (db.sm_item.item_id==percentage_prod_id_new)).select(db.sm_item.name,limitby=(0,1))
                if not newIdRow:
                    response.flash='Invalid New Product ID'
                else:
                    newIdName=newIdRow[0].name
                    
                    existIdRows=db((db.sm_promo_approved_rate.cid==c_id) & (db.sm_promo_approved_rate.product_id==percentage_prod_id_new) & (db.sm_promo_approved_rate.status=='ACTIVE')).select(db.sm_promo_approved_rate.id,limitby=(0,1))
                    if existIdRows:
                        response.flash='New Product ID already exist, Required New'
                    else:
                        existRows=db((db.sm_promo_approved_rate.cid==c_id) & (db.sm_promo_approved_rate.product_id==percentage_prod_id_exist) & (db.sm_promo_approved_rate.bonus_type=='Percentage') & (db.sm_promo_approved_rate.status=='ACTIVE')).select(db.sm_promo_approved_rate.ALL)
                        if not existRows:
                            response.flash='Existing Product ID not available in approved rate (Percentage)'
                        else:
                            dataList=[]
                            count_inserted=0
                            for existRow in existRows:
                                client_id=existRow.client_id
                                client_name=existRow.client_name
                                depot_id=existRow.depot_id
                                depot_name=existRow.depot_name
                                from_date=existRow.from_date
                                to_date=existRow.to_date
                                
                                bonus_type=existRow.bonus_type
                                fixed_percent_rate=existRow.fixed_percent_rate
                                status=existRow.status
                                
                                product_id=percentage_prod_id_new
                                product_name=newIdName
                                
                                dataList.append({'cid':c_id,'client_id':client_id,'client_name':client_name,'depot_id':depot_id,'depot_name':depot_name,'from_date':from_date,'to_date':to_date,'product_id':product_id,'product_name':product_name,'bonus_type':bonus_type,'fixed_percent_rate':fixed_percent_rate,'status':status})
                                count_inserted+=1
                                
                            if len(dataList)>0:
                                db.sm_promo_approved_rate.bulk_insert(dataList)
                                response.flash='New Product ID:'+percentage_prod_id_new+', Name:'+newIdName+'; successfully added in '+str(count_inserted)+' Customer(s)'
    
    elif btn_fixed_add:
        fixed_prod_id_new=request.vars.fixed_prod_id_new
        fixedcpp=request.vars.fixed_cpp
        
        try:
            fixed_cpp=float(fixedcpp)
        except:
            fixed_cpp=0
            
        if fixed_prod_id_new=='' or fixed_cpp=='' or fixed_cpp<=0:
            response.flash='Required New Product ID and valid Fixed CPP'
        else:                     
            newIdRow=db((db.sm_item.cid==c_id) & (db.sm_item.item_id==fixed_prod_id_new)).select(db.sm_item.name,db.sm_item.vat_amt,limitby=(0,1))
            if not newIdRow:
                response.flash='Invalid New Product ID'
            else:
                newIdName=newIdRow[0].name
                vat_amt=newIdRow[0].vat_amt
                
                if fixed_cpp<=vat_amt:
                    response.flash='CPP should be greater than VAT amount of the New Product'
                else:
                    existIdRows=db((db.sm_promo_approved_rate.cid==c_id) & (db.sm_promo_approved_rate.product_id==fixed_prod_id_new) & (db.sm_promo_approved_rate.status=='ACTIVE')).select(db.sm_promo_approved_rate.id,limitby=(0,1))
                    if existIdRows:
                        response.flash='New Product ID already exist, Required New'
                    else:
                        existIdRows=db((db.sm_promo_approved_rate.cid==c_id) & (db.sm_promo_approved_rate.status=='ACTIVE')).select(db.sm_promo_approved_rate.client_id,db.sm_promo_approved_rate.client_name,db.sm_promo_approved_rate.depot_id,db.sm_promo_approved_rate.depot_name,db.sm_promo_approved_rate.from_date.max(),db.sm_promo_approved_rate.to_date,db.sm_promo_approved_rate.status,groupby=db.sm_promo_approved_rate.client_id,orderby=db.sm_promo_approved_rate.client_name)
                        if not existIdRows:
                            response.flash='Existing Product ID not available in approved rate (Fixed)'
                        else:
                            dataList=[]
                            count_inserted=0
                            for existIdRow in existIdRows:
                                client_id=existIdRow.sm_promo_approved_rate.client_id
                                client_name=existIdRow.sm_promo_approved_rate.client_name
                                depot_id=existIdRow.sm_promo_approved_rate.depot_id
                                depot_name=existIdRow.sm_promo_approved_rate.depot_name
                                from_date=existIdRow[db.sm_promo_approved_rate.from_date.max()]
                                to_date=existIdRow.sm_promo_approved_rate.to_date
                                status=existIdRow.sm_promo_approved_rate.status
                                
                                product_id=fixed_prod_id_new
                                product_name=newIdName
                                
                                bonus_type='Fixed'
                                fixed_percent_rate=round(fixed_cpp-vat_amt,2)
                                
                                
                                dataList.append({'cid':c_id,'client_id':client_id,'client_name':client_name,'depot_id':depot_id,'depot_name':depot_name,'from_date':from_date,'to_date':to_date,'product_id':product_id,'product_name':product_name,'bonus_type':bonus_type,'fixed_percent_rate':fixed_percent_rate,'status':status})
                                count_inserted+=1
                                
                            if len(dataList)>0:
                                db.sm_promo_approved_rate.bulk_insert(dataList)
                                response.flash='New Product ID:'+fixed_prod_id_new+', Name:'+newIdName+'; successfully added in '+str(count_inserted)+' Customer(s)'
    
    return dict()


#====================================== approved_rate BATCH UPLOAD
def approved_rate_batch_upload():
    response.title='Approved Rate Batch upload'
    
    #----------Task assaign----------
    task_id='rm_campaign_manage'
    access_permission=check_role(task_id)
#    access_permission_view=check_role(task_id_view)
    if access_permission==False:
        session.flash='Access is Denied !'
        redirect (URL('promotion','approved_rate'))
    
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
        item_id_list_exist=[]
        
        item_id_list_excel=[]
        client_id_list_excel=[]
                
        ins_list=[]
        ins_dict={}
        #   ----------------------
        #---------- rep area
        for i in range(total_row):
            if i>=500:
                break
            else:
                row_data=row_list[i]                    
                coloum_list=row_data.split( '\t')
                if len(coloum_list)==6:
                    clientIDExcel=str(coloum_list[0]).strip().upper()
                    productIDExcel=str(coloum_list[3]).strip().upper()
                    
                    if clientIDExcel!='':
                        if clientIDExcel not in client_id_list_excel:
                            client_id_list_excel.append(clientIDExcel)
                    
                    if productIDExcel!='':
                        if productIDExcel not in item_id_list_excel:
                            item_id_list_excel.append(productIDExcel)
        
        #Create list based on excel sheet which items are already exist in database
#         existRows=db((db.sm_promo_approved_rate.cid==c_id)&(db.sm_promo_approved_rate.client_id.belongs(item_id_list_excel))).select(db.sm_promo_approved_rate.client_id,orderby=db.sm_promo_approved_rate.client_id)
#         item_id_list_exist=existRows.as_list()
        
        
        #Check valid client list based on excel sheet
        clientRows=db((db.sm_client.cid==c_id)&(db.sm_client.client_id.belongs(client_id_list_excel))&(db.sm_client.status=='ACTIVE')).select(db.sm_client.client_id,db.sm_client.name,db.sm_client.depot_id,db.sm_client.depot_name,orderby=db.sm_client.client_id)
        client_list_exist=clientRows.as_list()
        
        itemRows=db((db.sm_item.cid==c_id)&(db.sm_item.item_id.belongs(item_id_list_excel))).select(db.sm_item.item_id,db.sm_item.name,orderby=db.sm_item.item_id)
        item_id_list_exist=itemRows.as_list()
        
        #--------- update promo
        db((db.sm_settings.cid == c_id)&(db.sm_settings.s_key == 'PROMO_DATE')).update(s_value=datetime_fixed)
        
        # main loop   
        for i in range(total_row):
            if i>=500: 
                break
            else:
                row_data=row_list[i]
            coloum_list=row_data.split( '\t')            
            
            if len(coloum_list)!=6:
                error_data=row_data+'(6 columns need in a row)\n'
                error_str=error_str+error_data
                count_error+=1
                continue
            else:
                client_idExcel=str(coloum_list[0]).strip().upper()                                
                from_date=str(coloum_list[1]).strip()
                to_date=str(coloum_list[2]).strip()
                item_idExcel=str(coloum_list[3]).strip().upper()                
                bonus_type=str(coloum_list[4]).strip()
                fixed_percent_rate=str(coloum_list[5]).strip()     
                
                bonusTypeList=['Fixed','Percentage']
                status='ACTIVE'
                
                #------------------
                if client_idExcel=='' or from_date=='' or to_date=='' or item_idExcel=='' or bonus_type=='' or fixed_percent_rate=='':
                    error_data=row_data+'(Required all value)\n'
                    error_str=error_str+error_data
                    count_error+=1
                    continue
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
                        fixed_percent_rate=float(fixed_percent_rate)
                    except:
                        fixed_percent_rate=0
                     
                    #-------------------
                    
                    try:
                        valid_client_id=False
                        valid_product_id=False
                        duplicate_item_id=False
                        
                        clientName=''
                        itemName=''   
                        depot_id=''
                        depot_name=''
                        #Check valid client_list                         
                        for i in range(len(client_list_exist)):
                            myRowData=client_list_exist[i]                                
                            client_id=myRowData['client_id']
                            if (str(client_id).strip()==str(client_idExcel).strip()):
                                valid_client_id=True
                                clientName=myRowData['name']                                
                                depot_id=myRowData['depot_id']
                                depot_name=myRowData['depot_name']
                                break
                                
                        if valid_client_id==True:# check item                                                     
                            for i in range(len(item_id_list_exist)):
                                myRowData=item_id_list_exist[i]                                
                                item_id=myRowData['item_id']
                                if (str(item_id).strip()==str(item_idExcel).strip()):
                                    valid_product_id=True
                                    itemName=myRowData['name']
                                    break
                                    
                        #-----------------
                        if valid_client_id==False:
                            error_data=row_data+'(Invalid Client ID)\n'
                            error_str=error_str+error_data
                            count_error+=1
                            continue
                        else:
                            if valid_product_id==False:
                                error_data=row_data+'(Invalid Product ID)\n'
                                error_str=error_str+error_data
                                count_error+=1
                                continue
                            else:                                
                                existCheckRows=db((db.sm_promo_approved_rate.cid==c_id)&(db.sm_promo_approved_rate.client_id==client_idExcel)&(db.sm_promo_approved_rate.to_date>=from_date)&(db.sm_promo_approved_rate.product_id==item_idExcel)).select(db.sm_promo_approved_rate.id,limitby=(0,1))
                                if existCheckRows:
                                    error_data=row_data+'(Duplicate check for ClientID, From Date,To Date and Product ID)\n'
                                    error_str=error_str+error_data
                                    count_error+=1
                                    continue
                                else:                                    
                                    if bonus_type not in bonusTypeList:
                                        error_data=row_data+'(Invalid Bonus Type!)\n'
                                        error_str=error_str+error_data
                                        count_error+=1
                                        continue
                                    else:
                                        if fixed_percent_rate<=0:
                                            error_data=row_data+'(Invalid Rate!)\n'
                                            error_str=error_str+error_data
                                            count_error+=1
                                            continue
                                        else:
                                            db.sm_promo_approved_rate.insert(cid=c_id,client_id=client_idExcel,client_name=clientName,depot_id=depot_id,depot_name=depot_name,from_date=from_date,to_date=to_date,product_id=item_idExcel,product_name=itemName,bonus_type=bonus_type,fixed_percent_rate=fixed_percent_rate,status=status)
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
def approved_rate_download():
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
    qset=qset(db.sm_promo_approved_rate.cid==cid)
    if (session.user_type=='Depot'):
        qset=qset(db.sm_promo_approved_rate.depot_id==session.depot_id)
        
    if (session.user_type!='Depot'):
        if (session.btn_filter_approved_rate and session.search_type_approved_rate=='DepotId'):
            searchValue=str(session.search_value_approved_rate).split('|')[0]        
            qset=qset(db.sm_promo_approved_rate.depot_id==searchValue.upper())
        else:
            qset=qset(db.sm_promo_approved_rate.depot_id!='')
            
    if (session.btn_filter_approved_rate and session.search_type_approved_rate=='Client_id'):
        searchValue=str(session.search_value_approved_rate).split('|')[0]        
        qset=qset(db.sm_promo_approved_rate.client_id==searchValue.upper())
        
    elif (session.btn_filter_approved_rate and session.search_type_approved_rate=='Product_id'):
         searchValue=str(session.search_value_approved_rate).split('|')[0]    
         qset=qset(db.sm_promo_approved_rate.product_id==searchValue.upper())
        
    elif (session.btn_filter_approved_rate and session.search_type_approved_rate=='Status'):
        qset=qset(db.sm_promo_approved_rate.status==session.search_value_approved_rate.upper())
        
    records=qset.select(db.sm_promo_approved_rate.ALL,orderby=db.sm_promo_approved_rate.client_name)
    
    #Create string for download as excel file
    myString='Approved Rate List\n'
    myString+='Branch ID,Branch Name,Client ID,Client Name,From-date,To-date,Product Id,Product Name,Bonus Type,Fixed Percent Rate,Status\n'
    #Replace coma from records. cause coma means new Column    
    for rec in records:
        depot_id=rec.depot_id
        depot_name=str(rec.depot_name).replace(',', ' ')
        client_id=rec.client_id
        client_name=str(rec.client_name).replace(',', ' ')
        from_date=str(rec.from_date).replace(',', ' ')
        to_date=rec.to_date
        product_id=rec.product_id
        product_name=str(rec.product_name).replace(',', ' ')
        bonus_type=str(rec.bonus_type)
        fixed_percent_rate=str(rec.fixed_percent_rate)
        status=str(rec.status)
        
        myString+=str(depot_id)+','+str(depot_name)+','+str(client_id)+','+str(client_name)+','+str(from_date)+','+str(to_date)+','+str(product_id)+','+str(product_name)+','+str(bonus_type)+','+str(fixed_percent_rate)+','+str(status)+'\n'

    #-----------
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_approved_rate.csv'   
    return str(myString)

#================Product Bonus=============
def product_bonus_validation(form):    
    cid=session.cid
    from_date=request.vars.from_date
    to_date=request.vars.to_date
    
    min_qty=form.vars.min_qty
    
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
        if min_qty<=0:
            form.errors.min_qty=''
            response.flash = 'Invalid Min Qty' 
        else:            
            pass

def product_bonus():
    task_id='rm_campaign_manage'
    task_id_view='rm_campaign_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))
        
    response.title='Product Bonus'
    
    cid=session.cid
    
    form =SQLFORM(db.sm_promo_product_bonus,
                  fields=['from_date','to_date','min_qty','circular_number','note','allowed_credit_inv','regular_discount_apply','status'],       
                  submit_button='Save'
                  )
     
    form.vars.cid=cid
    if form.accepts(request.vars,session,onvalidation=product_bonus_validation):
        #--------- update promo
        db((db.sm_settings.cid == session.cid)&(db.sm_settings.s_key == 'PROMO_DATE')).update(s_value=datetime_fixed)
        
        response.flash = 'Submitted Successfully'
       
    #  Set text for filter
    btn_filter_product_bonus=request.vars.btn_filter_item
    btn_all=request.vars.btn_all
    reqPage=len(request.args)
     
    if btn_filter_product_bonus:
        session.btn_filter_product_bonus=btn_filter_product_bonus
        session.search_type_product_bonus=request.vars.search_type
        session.search_value_product_bonus=request.vars.search_value
 
        reqPage=0
    elif btn_all:
        session.btn_filter_product_bonus=None
        session.search_type_product_bonus=None
        session.search_value_product_bonus=None
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
    qset=qset(db.sm_promo_product_bonus.cid==cid)
    
    if (session.btn_filter_product_bonus and session.search_type_product_bonus=='Status'):
        qset=qset(db.sm_promo_product_bonus.status==session.search_value_product_bonus.upper())
        
    records=qset.select(db.sm_promo_product_bonus.ALL,orderby=~db.sm_promo_product_bonus.id,limitby=limitby)
    totalCount=qset.count()
    
    #----------------- filter end
    return dict(form=form,records=records,totalCount=totalCount,page=page,items_per_page=items_per_page,access_permission=access_permission)
 
 
#Validation for item edit
def product_bonus_edit_validation(form):
    from_date=request.vars.from_date
    to_date=request.vars.to_date
    
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
        pass
        
def product_bonus_edit():
    task_id='rm_campaign_manage'
    access_permission=check_role(task_id)
    if (access_permission==False):
        session.flash='Access is Denied !'
        redirect (URL('promotion','product_bonus'))
     
    #Set combos for unit and catagory    
    response.title='Product Bonus Edit'
    cid=session.cid
    
    page=request.args(0)
    rowID=request.args(1)
    
    
    recordRows=db((db.sm_promo_product_bonus.cid==cid)&(db.sm_promo_product_bonus.id==rowID)).select(db.sm_promo_product_bonus.ALL,limitby=(0,1))
    if not recordRows:
        session.flash='Invalid request'
        redirect (URL('promotion','product_bonus'))
    else:
        pass
    
    record= db.sm_promo_product_bonus(rowID) #or redirect(URL('index')) 
    form =SQLFORM(db.sm_promo_product_bonus,
                  record=record,
                  deletable=True,
                  fields=['from_date','to_date','min_qty','circular_number','note','allowed_credit_inv','regular_discount_apply','status'],    
                  submit_button='Update'
                  )
    
    if form.accepts(request.vars, session,onvalidation=product_bonus_edit_validation):
        to_date=form.vars.to_date
        note=form.vars.note
        status=form.vars.status
        if form.vars.get('delete_this_record', False):
            db((db.sm_promo_product_bonus_products.cid==cid)&(db.sm_promo_product_bonus_products.refrowid==rowID)).delete()
            db((db.sm_promo_product_bonus_bonuses.cid==cid)&(db.sm_promo_product_bonus_bonuses.refrowid==rowID)).delete()            
        else:
            db((db.sm_promo_product_bonus_products.cid==cid)&(db.sm_promo_product_bonus_products.refrowid==rowID)).update(to_date=to_date,note=note,status=status)
            db((db.sm_promo_product_bonus_bonuses.cid==cid)&(db.sm_promo_product_bonus_bonuses.refrowid==rowID)).update(to_date=to_date,status=status)
            
        #--------- update promo
        db((db.sm_settings.cid == session.cid)&(db.sm_settings.s_key == 'PROMO_DATE')).update(s_value=datetime_fixed)
        
        session.flash = 'Updated Successfully'        
        redirect(URL('product_bonus',args=[page]))
        
    return dict(form=form,page=page,recordRows=recordRows)
    

#================Product Bonus=============
def validation_product_bonus_products_add(formP):    
    cid=session.cid
    refrowid=formP.vars.refrowid
    product_id=str(formP.vars.product_id).strip().upper().split('|')[0]        
    
    product_rows_check=db((db.sm_item.cid==cid) & (db.sm_item.item_id==product_id)).select(db.sm_item.name,limitby=(0,1))
    if not product_rows_check:
        formP.errors.product_id='Invalid Product Id'
    else:
        product_name=product_rows_check[0].name
        
        exist_rows_check=db((db.sm_promo_product_bonus_products.cid==cid)&(db.sm_promo_product_bonus_products.refrowid==refrowid)&(db.sm_promo_product_bonus_products.product_id==product_id)).select(db.sm_promo_product_bonus_products.id,limitby=(0,1))
        if exist_rows_check:
            formP.errors.product_id='Already exist'
        else:
            formP.vars.product_id=product_id
            formP.vars.product_name=product_name
            
#================Product Bonus=============
def validation_product_bonus_bonuses_add(formB):
    cid=session.cid
    refrowid=formB.vars.refrowid
    bonus_product_id=str(formB.vars.bonus_product_id).strip().upper().split('|')[0] 
    bonus_qty=formB.vars.bonus_qty
    
    product_rows_check2=db((db.sm_item.cid==cid) & (db.sm_item.item_id==bonus_product_id)).select(db.sm_item.name,limitby=(0,1))
    if not product_rows_check2:
        formB.errors.bonus_product_id='Invalid Bonus Product Id'
    else:
        bonus_product_name=product_rows_check2[0].name
        
        exist_rows_check=db((db.sm_promo_product_bonus_bonuses.cid==cid)&(db.sm_promo_product_bonus_bonuses.refrowid==refrowid)&(db.sm_promo_product_bonus_bonuses.bonus_product_id==bonus_product_id)).select(db.sm_promo_product_bonus_bonuses.id,limitby=(0,1))
        if exist_rows_check:
            formB.errors.bonus_product_id='Already exist'
        else:
            if bonus_qty<=0:
                formB.errors.bonus_qty=''
                response.flash = 'Invalid Bonus Qty' 
            else:            
                formB.vars.bonus_product_id=bonus_product_id
                formB.vars.bonus_product_name=bonus_product_name

def product_bonus_details_add():
    task_id='rm_campaign_manage'
    access_permission=check_role(task_id)
    if (access_permission==False):
        session.flash='Access is Denied !'
        redirect (URL('promotion','product_bonus'))
    
    #Set combos for unit and catagory    
    response.title='Product Bonus Edit'
    cid=session.cid
    
    page=request.args(0)
    rowID=request.args(1)
    
    from_date=''
    to_date=''
    min_qty=''
    circular_number=''
    head_note=''
    status=''
    until_stock_last=''
    allowed_credit_inv=''
    regular_discount_apply=''
    
    recordRows=db((db.sm_promo_product_bonus.cid==cid)&(db.sm_promo_product_bonus.id==rowID)).select(db.sm_promo_product_bonus.ALL,limitby=(0,1))
    if not recordRows:
        session.flash='Invalid request'
        redirect (URL('promotion','product_bonus'))
    else:
        from_date=recordRows[0].from_date
        to_date=recordRows[0].to_date
        min_qty=recordRows[0].min_qty
        circular_number=recordRows[0].circular_number
        head_note=recordRows[0].note
        status=recordRows[0].status
        until_stock_last=recordRows[0].until_stock_last
        allowed_credit_inv=recordRows[0].allowed_credit_inv
        regular_discount_apply=recordRows[0].regular_discount_apply
                
    #-------------- Delete
    btn_product_delete=request.vars.btn_product_delete
    btn_bonus_delete=request.vars.btn_bonus_delete
    
    if btn_product_delete:
        pRowid=request.vars.pRowid
        db((db.sm_promo_product_bonus_products.cid==cid)&(db.sm_promo_product_bonus_products.id==pRowid)).delete()
        
        #--------- update promo
        db((db.sm_settings.cid == session.cid)&(db.sm_settings.s_key == 'PROMO_DATE')).update(s_value=datetime_fixed)
        
        response.flash = 'Product ID Deleted Successfully'
        
    elif btn_bonus_delete:
        bRowid=request.vars.bRowid
        db((db.sm_promo_product_bonus_bonuses.cid==cid)&(db.sm_promo_product_bonus_bonuses.id==bRowid)).delete()
        
        #--------- update promo
        db((db.sm_settings.cid == session.cid)&(db.sm_settings.s_key == 'PROMO_DATE')).update(s_value=datetime_fixed)
        
        response.flash = 'Bonus Product ID Deleted Successfully'
    
    #------- Product Form
    formP =SQLFORM(db.sm_promo_product_bonus_products,
                  fields=['product_id','product_name'],       
                  submit_button='Save'
                  ) 
    formP.vars.cid=cid
    formP.vars.refrowid=rowID
    formP.vars.circular_number=circular_number
    formP.vars.from_date=from_date
    formP.vars.to_date=to_date
    formP.vars.note=head_note
    formP.vars.status=status
    if formP.accepts(request.vars, session,onvalidation=validation_product_bonus_products_add):        
        #--------- update promo
        db((db.sm_settings.cid == session.cid)&(db.sm_settings.s_key == 'PROMO_DATE')).update(s_value=datetime_fixed)        
        response.flash = 'Submitted Successfully'
    productsRecors=db((db.sm_promo_product_bonus_products.cid==cid)&(db.sm_promo_product_bonus_products.refrowid==rowID)).select(db.sm_promo_product_bonus_products.ALL,orderby=db.sm_promo_product_bonus_products.product_id)
    
    #----- Bonus form
    formB =SQLFORM(db.sm_promo_product_bonus_bonuses,
                  fields=['bonus_product_id','bonus_product_name','bonus_qty'],       
                  submit_button='Save'
                  )
    formB.vars.cid=cid
    formB.vars.refrowid=rowID
    formB.vars.circular_number=circular_number
    formB.vars.from_date=from_date
    formB.vars.to_date=to_date    
    formB.vars.status=status
    if formB.accepts(request.vars, session,onvalidation=validation_product_bonus_bonuses_add):
        #--------- update promo
        db((db.sm_settings.cid == session.cid)&(db.sm_settings.s_key == 'PROMO_DATE')).update(s_value=datetime_fixed)
        
        response.flash = 'Submitted Successfully'
    bonusRecors=db((db.sm_promo_product_bonus_bonuses.cid==cid)&(db.sm_promo_product_bonus_bonuses.refrowid==rowID)).select(db.sm_promo_product_bonus_bonuses.ALL,orderby=db.sm_promo_product_bonus_bonuses.bonus_product_id)
    
    return dict(rowID=rowID,formP=formP,formB=formB,productsRecors=productsRecors,bonusRecors=bonusRecors,page=page,from_date=from_date,to_date=to_date,min_qty=min_qty,circular_number=circular_number,head_note=head_note,status=status,until_stock_last=until_stock_last,allowed_credit_inv=allowed_credit_inv,regular_discount_apply=regular_discount_apply,access_permission=access_permission)
 
 
 #==================== Download
def product_bonus_download():
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
    qset=qset(db.sm_promo_product_bonus.cid==cid)
        
    if (session.btn_filter_product_bonus and session.search_type_product_bonus=='Status'):
        qset=qset(db.sm_promo_product_bonus.status==session.search_value_product_bonus.upper())
        
    records=qset.select(db.sm_promo_product_bonus.ALL,orderby=~db.sm_promo_product_bonus.id)
    
    #Create string for download as excel file
    myString='Product Bonus List\n'
    myString+='Ref,Circular Number,From-date,To-date,Note,Min Qty,Status\n'
    #Replace coma from records. cause coma means new Column    
    for rec in records:
        refrowid=str(rec.id)
        circular_number=str(rec.circular_number).replace(',', ' ')
        from_date=str(rec.from_date)
        to_date=str(rec.to_date)
        min_qty=str(rec.min_qty)
        status=str(rec.status)
        note=str(rec.note).replace(',', ' ')
        
        myString+=str(refrowid)+','+str(circular_number)+','+str(from_date)+','+str(to_date)+','+str(note)+','+str(min_qty)+','+str(status)+',,,\n'
        
        myString+=',,,,,,Product List,,\n'
        
        product_id=''
        product_name=''
        pRows=db((db.sm_promo_product_bonus_products.cid==cid)&(db.sm_promo_product_bonus_products.refrowid==refrowid)).select(db.sm_promo_product_bonus_products.ALL,orderby=db.sm_promo_product_bonus_products.product_id)
        for pRow in pRows:        
            product_id=str(pRow.product_id)
            product_name=str(pRow.product_name).replace(',', ' ')
            
            myString+=',,,,,,'+str(product_id)+','+str(product_name)+',,,\n'
            
        myString+=',,,,,,Bonus Product List,,\n'
        
        bonus_product_id=''
        bonus_product_name=''
        bonus_qty=''
        bRows=db((db.sm_promo_product_bonus_bonuses.cid==cid)&(db.sm_promo_product_bonus_bonuses.refrowid==refrowid)).select(db.sm_promo_product_bonus_bonuses.ALL,orderby=db.sm_promo_product_bonus_bonuses.bonus_product_id)
        for bRow in bRows:        
            bonus_product_id=str(bRow.bonus_product_id)
            bonus_product_name=str(bRow.bonus_product_name).replace(',', ' ')
            bonus_qty=str(bRow.bonus_qty)
            
            myString+=',,,,,,'+str(bonus_product_id)+','+str(bonus_product_name)+','+str(bonus_qty)+'\n'
    
    #-----------
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_product_bonus.csv'   
    return str(myString)




#===================Special Rate================

def special_rate_validation(form):    
    cid=session.cid
       
    product_id=str(request.vars.product_id).strip().upper().split('|')[0]
    
    min_qty=form.vars.min_qty
    
    if min_qty=='' or min_qty==None:
        min_qty=0
    
    from_date=request.vars.from_date
    to_date=request.vars.to_date
    
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
        product_rows_check=db((db.sm_item.cid==cid) & (db.sm_item.item_id==product_id)).select(db.sm_item.name,db.sm_item.price,db.sm_item.vat_amt,limitby=(0,1))
        if not product_rows_check:
            form.errors.product_id=''
            response.flash = 'Invalid Product Id '
        else:
            product_name=product_rows_check[0].name
            price=product_rows_check[0].price
            vat_amt=product_rows_check[0].vat_amt
            
            if min_qty<=0:
                form.errors.min_qty=''
                response.flash = 'Invalid Minimum Qty ' 
            else:
                form.vars.product_id=product_id
                form.vars.product_name=product_name
                form.vars.tp=price
                form.vars.vat=vat_amt
                
def special_rate():
    task_id='rm_campaign_manage'
    task_id_view='rm_campaign_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))
        
    response.title='Special Rate'
    
    cid=session.cid
    
    form =SQLFORM(db.sm_promo_special_rate,
                  fields=['from_date','to_date','campaign_ref','product_id','min_qty','special_rate_tp','special_rate_vat','allowed_credit_inv','status'],  #'regular_discount_apply',     
                  submit_button='Save'
                  )
    
    form.vars.cid=cid
    if form.accepts(request.vars,session,onvalidation=special_rate_validation):        
        #--------- update promo
        db((db.sm_settings.cid == session.cid)&(db.sm_settings.s_key == 'PROMO_DATE')).update(s_value=datetime_fixed)        
        response.flash = 'Submitted Successfully'
    
    #  Set text for filter
    btn_filter_special_rate=request.vars.btn_filter_item
    btn_all=request.vars.btn_all
    reqPage=len(request.args)
     
    if btn_filter_special_rate:
        session.btn_filter_special_rate=btn_filter_special_rate
        session.search_type_special_rate=request.vars.search_type
        session.search_value_special_rate=request.vars.search_value
 
        reqPage=0
    elif btn_all:
        session.btn_filter_special_rate=None
        session.search_type_special_rate=None
        session.search_value_special_rate=None
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
    qset=qset(db.sm_promo_special_rate.cid==cid)
     
    if (session.btn_filter_special_rate and session.search_type_special_rate=='Product_id'):
        searchValue=str(session.search_value_special_rate).split('|')[0]        
        qset=qset(db.sm_promo_special_rate.product_id==searchValue.upper())
        
    elif (session.btn_filter_special_rate and session.search_type_special_rate=='Status'):
        qset=qset(db.sm_promo_special_rate.status==session.search_value_special_rate.upper())
        
    records=qset.select(db.sm_promo_special_rate.ALL,orderby=~db.sm_promo_special_rate.from_date|db.sm_promo_special_rate.product_name,limitby=limitby)
    totalCount=qset.count()
    
    #----------------- filter end
    return dict(form=form,records=records,totalCount=totalCount,page=page,items_per_page=items_per_page,access_permission=access_permission)
 
 
#Validation for item edit
def special_rate_edit_validation(form):
    cid=session.cid
    product_id=str(request.vars.product_id).strip().upper().split('|')[0]
    
    min_qty=form.vars.min_qty
    
    if min_qty=='' or min_qty==None:
        min_qty=0
    
    from_date=request.vars.from_date
    to_date=request.vars.to_date
    
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
        product_rows_check=db((db.sm_item.cid==cid) & (db.sm_item.item_id==product_id)).select(db.sm_item.name,db.sm_item.price,db.sm_item.vat_amt,limitby=(0,1))
        if not product_rows_check:
            form.errors.product_id=''
            response.flash = 'Invalid Product Id '
        else:
            product_name=product_rows_check[0].name
            price=product_rows_check[0].price
            vat_amt=product_rows_check[0].vat_amt
            
            form.vars.product_name=product_name
            form.vars.tp=price
            form.vars.vat=vat_amt
            
def special_rate_edit():
    task_id='rm_campaign_manage'
    access_permission=check_role(task_id)
    if (access_permission==False):
        session.flash='Access is Denied !'
        redirect (URL('promotion','special_rate'))
     
    #Set combos for unit and catagory    
    response.title='Special Rate'
    
    cid=session.cid
    
    page=request.args(0)
    rowID=request.args(1)
    record= db.sm_promo_special_rate(rowID) #or redirect(URL('index'))  
      
    form =SQLFORM(db.sm_promo_special_rate,
                  record=record,
                  deletable=True,
                  fields=['from_date','to_date','campaign_ref','product_id','product_name','min_qty','special_rate_tp','special_rate_vat','allowed_credit_inv','status'], #'regular_discount_apply',       
                  submit_button='Update'
                  )
     
    if form.accepts(request.vars, session,onvalidation=special_rate_edit_validation):
        #--------- update promo
        db((db.sm_settings.cid == session.cid)&(db.sm_settings.s_key == 'PROMO_DATE')).update(s_value=datetime_fixed)
        
        response.flash = 'Updated Successfully'        
        redirect(URL('special_rate',args=[page]))
    
    recordRows=db((db.sm_promo_special_rate.cid==cid)&(db.sm_promo_special_rate.id==rowID)).select(db.sm_promo_special_rate.ALL,limitby=(0,1))
    
    return dict(form=form,page=page,recordRows=recordRows)

#====================================== Special Rate BATCH UPLOAD    
def special_rate_batch_upload():
    response.title='Special Rate Batch upload' 
     
     #----------Task assaign----------
    task_id='rm_campaign_manage'
    access_permission=check_role(task_id)
#    access_permission_view=check_role(task_id_view)
    if access_permission==False:
        session.flash='Access is Denied !'
        redirect (URL('promotion','special_rate'))
    
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
              
        item_id_list_exist=[]
        
        item_id_list_excel=[]
                
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
                    itemIDExcel=str(coloum_list[3]).strip().upper()
                    
                    if itemIDExcel!='':
                        if itemIDExcel not in item_id_list_excel:
                            item_id_list_excel.append(itemIDExcel)
                    
        
        #Check valid item list based on excel sheet        
        itemRows=db((db.sm_item.cid==c_id)&(db.sm_item.item_id.belongs(item_id_list_excel))).select(db.sm_item.item_id,db.sm_item.name,orderby=db.sm_item.item_id)
        item_id_list_exist=itemRows.as_list()
        
        #--------- update promo
        db((db.sm_settings.cid == session.cid)&(db.sm_settings.s_key == 'PROMO_DATE')).update(s_value=datetime_fixed)
        
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
                from_date=str(coloum_list[0]).strip()
                to_date=str(coloum_list[1]).strip()
                campaignRef=str(coloum_list[2]).strip()
                item_idExcel=str(coloum_list[3]).strip().upper()
                minQtyExcel=str(coloum_list[4]).strip()
                specialRateTpExcel=str(coloum_list[5]).strip()  
                specialRateVatExcel=str(coloum_list[6]).strip()   
                status='ACTIVE'
                
                #------------------
                if from_date=='' or to_date=='' or campaignRef=='' or item_idExcel=='' or minQtyExcel==''or specialRateTpExcel=='' or specialRateVatExcel=='':
                    error_data=row_data+'(Required all value)\n'
                    error_str=error_str+error_data
                    count_error+=1
                    continue
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
                        minQtyExcel=float(minQtyExcel)
                    except:
                        minQtyExcel=0
                        
                    try:
                        specialRateTpExcel=float(specialRateTpExcel)
                    except:
                        specialRateTpExcel=0    
                        
                    try:
                        specialRateVatExcel=float(specialRateVatExcel)
                    except:
                        specialRateVatExcel=0     
                    #-------------------
                    
                    
                    valid_item_id=False
                    
                    itemName='' 
                      
                    #Check valid client_list                         
                    for i in range(len(item_id_list_exist)):
                        myRowData=item_id_list_exist[i]                                
                        item_id=myRowData['item_id']
                        if (str(item_id).strip()==str(item_idExcel).strip()):
                            valid_item_id=True
                            itemName=myRowData['name']
                            break
                                        
                    #-----------------
                    
                    if valid_item_id==False:
                        error_data=row_data+'(Invalid Product ID)\n'
                        error_str=error_str+error_data
                        count_error+=1
                        continue
                    else:                                
                        existCheckRows=db((db.sm_promo_special_rate.cid==c_id)&(db.sm_promo_special_rate.to_date==from_date)&(db.sm_promo_special_rate.product_id==item_idExcel)&(db.sm_promo_special_rate.min_qty==minQtyExcel)).select(db.sm_promo_special_rate.id,limitby=(0,1))
                        if existCheckRows:
                            error_data=row_data+'(Duplicate for From Date and Product ID )\n'
                            error_str=error_str+error_data
                            count_error+=1
                            continue
                        else:
                            if minQtyExcel<=0:
                                error_data=row_data+'(Invalid Minimum Qty!)\n'
                                error_str=error_str+error_data
                                count_error+=1
                                continue
                            else:
                                if specialRateTpExcel<0:
                                    error_data=row_data+'(Invalid Special TP!)\n'
                                    error_str=error_str+error_data
                                    count_error+=1
                                    continue
                                else:
                                    if specialRateVatExcel<0:
                                        error_data=row_data+'(Invalid Special VAT!)\n'
                                        error_str=error_str+error_data
                                        count_error+=1
                                        continue
                                    else:
                                        
                                        try:
                                            db.sm_promo_special_rate.insert(cid=c_id,from_date=from_date,to_date=to_date,campaign_ref=campaignRef,product_id=item_idExcel,product_name=itemName,min_qty=minQtyExcel,special_rate_tp=specialRateTpExcel,special_rate_vat=specialRateVatExcel,status=status)
                                            count_inserted+=1                                    
                                        except:
                                            error_data=row_data+'(error in process!)\n'
                                            error_str=error_str+error_data
                                            count_error+=1
                                            continue
            
        if error_str=='':
            error_str='No error'
    
    return dict(count_inserted=count_inserted,count_error=count_error,error_str=error_str,total_row=total_row)
   
#------------------item end----------------------
 
 
 
        
 
#============================================== Download
 
def special_rate_download():
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
    qset=qset(db.sm_promo_special_rate.cid==cid)
     
    if (session.btn_filter_special_rate and session.search_type_special_rate=='Product_id'):
        searchValue=str(session.search_value_special_rate).split('|')[0]        
        qset=qset(db.sm_promo_special_rate.product_id==searchValue.upper())
        
    elif (session.btn_filter_special_rate and session.search_type_special_rate=='Status'):
        qset=qset(db.sm_promo_special_rate.status==session.search_value_special_rate.upper())
         
    records=qset.select(db.sm_promo_special_rate.ALL,orderby=db.sm_promo_special_rate.product_name)
     
    #Create string for download as excel file
    myString='Special Rate List\n'
    myString+='From-date,To-date,Campaign Ref,Product Id,Product Name,Min Qty,Premium TP,Vat,Allowed Credit Invoice,Status\n'
    #Replace coma from records. cause coma means new Column    
    for rec in records:
        from_date=rec.from_date
        to_date=str(rec.to_date)
        campaign_ref=str(rec.campaign_ref)
        product_id=rec.product_id
        product_name=str(rec.product_name).replace(',', ' ')        
        min_qty=str(rec.min_qty)
        special_rate_tp=str(rec.special_rate_tp)
        special_rate_vat=str(rec.special_rate_vat)
        allowed_credit_inv=str(rec.allowed_credit_inv)
        #regular_discount_apply=str(rec.regular_discount_apply) +','+str(regular_discount_apply) ,Regular Discount Apply
        status=str(rec.status)
        
        myString+=str(from_date)+','+str(to_date)+','+str(campaign_ref)+','+str(product_id)+','+str(product_name)+','+str(min_qty)+','+str(special_rate_tp)+','+str(special_rate_vat)+','+str(allowed_credit_inv)+','+str(status)+'\n'
 
    #-----------
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_special_rate.csv'   
    return str(myString)




#===================Flat Rate================

def flat_rate_validation(form):    
    cid=session.cid
         
    product_id=str(request.vars.product_id).strip().upper().split('|')[0]
    
    min_qty=form.vars.min_qty
    
    flat_rate=form.vars.flat_rate
    
    from_date=request.vars.from_date
    to_date=request.vars.to_date
    
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
        product_rows_check=db((db.sm_item.cid==cid) & (db.sm_item.item_id==product_id)).select(db.sm_item.name,db.sm_item.vat_amt,limitby=(0,1))
        if not product_rows_check:
            form.errors.product_id=''
            response.flash = 'Invalid Product ID '
        else:
            product_name=product_rows_check[0].name
            vat_amt=product_rows_check[0].vat_amt
            
            if min_qty<=0:
                form.errors.min_qty=''
                response.flash = 'Invalid Minimum Qty' 
            else:
                if flat_rate<=0:
                    form.errors.flat_rate=''
                    response.flash = 'Invalid Flat Rate' 
                else:
                    form.vars.product_id=product_id
                    form.vars.product_name=product_name
                    form.vars.vat=vat_amt
                    
def flat_rate():
    task_id='rm_campaign_manage'
    task_id_view='rm_campaign_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))
     
    response.title='Flat Rate'
    
    cid=session.cid
    
    form =SQLFORM(db.sm_promo_flat_rate,
                  fields=['from_date','to_date','campaign_ref','product_id','product_name','min_qty','flat_rate','allowed_credit_inv','regular_discount_apply','allow_bundle','status'],       
                  submit_button='Save'
                  )
     
    form.vars.cid=cid
    if form.accepts(request.vars,session,onvalidation=flat_rate_validation):        
        #--------- update promo
        db((db.sm_settings.cid == session.cid)&(db.sm_settings.s_key == 'PROMO_DATE')).update(s_value=datetime_fixed)
        response.flash = 'Submitted Successfully'
     
         
    #  Set text for filter
    btn_filter_flat_rate=request.vars.btn_filter_item
    btn_all=request.vars.btn_all
    reqPage=len(request.args)
     
    if btn_filter_flat_rate:
        session.btn_filter_flat_rate=btn_filter_flat_rate
        session.search_type_flat_rate=request.vars.search_type
        session.search_value_flat_rate=request.vars.search_value
 
        reqPage=0
    elif btn_all:
        session.btn_filter_flat_rate=None
        session.search_type_flat_rate=None
        session.search_value_flat_rate=None
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
    qset=qset(db.sm_promo_flat_rate.cid==cid)
    
    if (session.btn_filter_flat_rate and session.search_type_flat_rate=='Product_id'):
        searchValue=str(session.search_value_flat_rate).split('|')[0]        
        qset=qset(db.sm_promo_flat_rate.product_id==searchValue.upper())
        
    elif (session.btn_filter_flat_rate and session.search_type_flat_rate=='Status'):
        qset=qset(db.sm_promo_flat_rate.status==session.search_value_flat_rate.upper())
        
    records=qset.select(db.sm_promo_flat_rate.ALL,orderby=db.sm_promo_flat_rate.product_name,limitby=limitby)
    totalCount=qset.count()
     
    #----------------- filter end
    return dict(form=form,records=records,totalCount=totalCount,page=page,items_per_page=items_per_page,access_permission=access_permission)
 
 
#Validation for item edit
def flat_rate_edit_validation(form):
    cid=session.cid
    product_id=str(request.vars.product_id).strip().upper().split('|')[0]
        
    from_date=request.vars.from_date
    to_date=request.vars.to_date
    
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
        product_rows_check=db((db.sm_item.cid==cid) & (db.sm_item.item_id==product_id)).select(db.sm_item.name,db.sm_item.vat_amt,limitby=(0,1))
        if not product_rows_check:
            form.errors.product_id=''
            response.flash = 'Invalid Product ID '
        else:
            product_name=product_rows_check[0].name
            vat_amt=product_rows_check[0].vat_amt
            
            form.vars.product_name=product_name
            form.vars.vat=vat_amt

def flat_rate_edit():
    task_id='rm_campaign_manage'
    access_permission=check_role(task_id)
    if (access_permission==False):
        session.flash='Access is Denied !'
        redirect (URL('promotion','flat_rate'))
    
    #Set combos for unit and catagory    
    response.title='Flat Rate'
    
    cid=session.cid
    
    page=request.args(0)
    rowID=request.args(1)
    record= db.sm_promo_flat_rate(rowID) #or redirect(URL('index'))  
      
    form =SQLFORM(db.sm_promo_flat_rate,
                  record=record,
                  deletable=True,
                  fields=['from_date','to_date','campaign_ref','product_id','product_name','min_qty','flat_rate','allowed_credit_inv','regular_discount_apply','allow_bundle','status'],       
                  submit_button='Update'
                  )
    
    if form.accepts(request.vars, session,onvalidation=flat_rate_edit_validation):
        #--------- update promo
        db((db.sm_settings.cid == session.cid)&(db.sm_settings.s_key == 'PROMO_DATE')).update(s_value=datetime_fixed)
        response.flash = 'Updated Successfully'        
        redirect(URL('flat_rate',args=[page]))
        
    recordRows=db((db.sm_promo_flat_rate.cid==cid)&(db.sm_promo_flat_rate.id==rowID)).select(db.sm_promo_flat_rate.ALL,limitby=(0,1))
    
    return dict(form=form,page=page,recordRows=recordRows)
 
 
#====================================== REP AREA BATCH UPLOAD 
   
def flat_rate_batch_upload():
    response.title='Flat Rate Batch upload'
     
     #----------Task assaign----------
    task_id='rm_campaign_manage'
    access_permission=check_role(task_id)
#    access_permission_view=check_role(task_id_view)
    if access_permission==False:
        session.flash='Access is Denied !'
        redirect (URL('default','home'))
    
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
        
        row_list=excel_data.split( '\n')
        total_row=len(row_list)
              
        item_id_list_exist=[]
        
        item_id_list_excel=[]
                
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
                if len(coloum_list)==6:
                    itemIDExcel=str(coloum_list[3]).strip().upper()
                    
                    if itemIDExcel!='':
                        if itemIDExcel not in item_id_list_excel:
                            item_id_list_excel.append(itemIDExcel)
                    
        
        #Check valid item list based on excel sheet        
        itemRows=db((db.sm_item.cid==c_id)&(db.sm_item.item_id.belongs(item_id_list_excel))).select(db.sm_item.item_id,db.sm_item.name,db.sm_item.vat_amt,orderby=db.sm_item.item_id)
        item_id_list_exist=itemRows.as_list()
        #--------- update promo
        db((db.sm_settings.cid == session.cid)&(db.sm_settings.s_key == 'PROMO_DATE')).update(s_value=datetime_fixed)
        
        # main loop   
        for i in range(total_row):
            if i>=30: 
                break
            else:
                row_data=row_list[i]
            coloum_list=row_data.split( '\t')            
            
            if len(coloum_list)!=6:
                error_data=row_data+'(6 columns need in a row)\n'
                error_str=error_str+error_data
                count_error+=1
                continue
            else:                               
                from_date=str(coloum_list[0]).strip()
                to_date=str(coloum_list[1]).strip()
                campaignRef=str(coloum_list[2]).strip()
                item_idExcel=str(coloum_list[3]).strip().upper()                                
                minQtyExcel=str(coloum_list[4]).strip()
                flat_rateExcel=str(coloum_list[5]).strip()
                status='ACTIVE'
                
                #------------------
                if from_date=='' or to_date=='' or campaignRef=='' or item_idExcel=='' or minQtyExcel==''or flat_rateExcel=='':
                    error_data=row_data+'(Required all value)\n'
                    error_str=error_str+error_data
                    count_error+=1
                    continue
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
                        minQtyExcel=float(minQtyExcel)
                    except:
                        minQtyExcel=0
                        
                    try:
                        flat_rate=float(flat_rateExcel)
                    except:
                        flat_rate=0    
                       
                    #-------------------                    
                    valid_item_id=False
                    
                    itemName='' 
                    vat_amt=0
                    #Check valid client_list                         
                    for i in range(len(item_id_list_exist)):
                        myRowData=item_id_list_exist[i]                                
                        item_id=myRowData['item_id']
                        vatAmt=myRowData['vat_amt']
                        if (str(item_id).strip()==str(item_idExcel).strip()):
                            valid_item_id=True
                            itemName=myRowData['name']
                            vat_amt=vatAmt
                            break
                    
                    #-----------------                    
                    if valid_item_id==False:
                        error_data=row_data+'(Invalid Product ID)\n'
                        error_str=error_str+error_data
                        count_error+=1
                        continue
                    else:                                
                        existCheckRows=db((db.sm_promo_flat_rate.cid==c_id)&(db.sm_promo_flat_rate.from_date==from_date)&(db.sm_promo_flat_rate.product_id==item_idExcel)&(db.sm_promo_flat_rate.min_qty==minQtyExcel)).select(db.sm_promo_flat_rate.id,limitby=(0,1))
                        if existCheckRows:
                            error_data=row_data+'(Duplicate for From Date,Product ID and Minimum Rate)\n'
                            error_str=error_str+error_data
                            count_error+=1
                            continue
                        else:
                            if minQtyExcel<=0:
                                error_data=row_data+'(Invalid Minimum Qty!)\n'
                                error_str=error_str+error_data
                                count_error+=1
                                continue
                            else:
                                if flat_rate<=0:
                                    error_data=row_data+'(Invalid Flat Rate With Vat!)\n'
                                    error_str=error_str+error_data
                                    count_error+=1
                                    continue
                                else:                                    
                                    try:
                                        db.sm_promo_flat_rate.insert(cid=c_id,from_date=from_date,to_date=to_date,campaign_ref=campaignRef,product_id=item_idExcel,product_name=itemName,min_qty=minQtyExcel,flat_rate=flat_rate,vat=vat_amt,status=status)
                                        count_inserted+=1                                    
                                    except:
                                        error_data=row_data+'(error in process!)\n'
                                        error_str=error_str+error_data
                                        count_error+=1
                                        continue
            
        if error_str=='':
            error_str='No error'
    
    return dict(count_inserted=count_inserted,count_error=count_error,error_str=error_str,total_row=total_row)
   
#------------------item end----------------------

 
#============================================== Download
 
def flat_rate_download():
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
    qset=qset(db.sm_promo_flat_rate.cid==cid)
     
    if (session.btn_filter_flat_rate and session.search_type_flat_rate=='Product_id'):
        searchValue=str(session.search_value_flat_rate).split('|')[0]        
        qset=qset(db.sm_promo_flat_rate.product_id==searchValue.upper())
        
    elif (session.btn_filter_flat_rate and session.search_type_flat_rate=='Status'):
        qset=qset(db.sm_promo_flat_rate.status==session.search_value_flat_rate.upper())
        
    records=qset.select(db.sm_promo_flat_rate.ALL,orderby=db.sm_promo_flat_rate.product_name)
     
    #Create string for download as excel file
    myString='Flat Rate List\n'
    myString+='From-date,To-date,Campaign Ref,Product ID,Product Name,Minimum Qty,Flat TP (Excluding Vat),Vat,Total,Allowed Credit Invoice,Regular Discount Apply,Allow Bundle,Status\n'
    #Replace coma from records. cause coma means new Column    
    for rec in records:
        from_date=rec.from_date
        to_date=str(rec.to_date)
        campaign_ref=str(rec.campaign_ref)
        product_id=rec.product_id
        product_name=str(rec.product_name).replace(',', ' ')
        min_qty=str(rec.min_qty)
        flat_rate=rec.flat_rate
        vat_amt=rec.vat
        allowed_credit_inv=str(rec.allowed_credit_inv)
        regular_discount_apply=str(rec.regular_discount_apply)
        allow_bundle=str(rec.allow_bundle)        
        status=str(rec.status)
        
        totalAmt=str(flat_rate+vat_amt)
        
        myString+=str(from_date)+','+str(to_date)+','+str(campaign_ref)+','+str(product_id)+','+str(product_name)+','+str(min_qty)+','+str(flat_rate)+','+str(vat_amt)+','+str(totalAmt)+','+str(allowed_credit_inv)+','+str(regular_discount_apply)+','+str(allow_bundle)+','+str(status)+'\n'
        
    #-----------
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_flat_rate.csv'   
    return str(myString)
    


#===================Regular Discount================

def regular_discount_validation(form):    
    cid=session.cid
        
    min_amount=form.vars.min_amount
    discount_percent=form.vars.discount_precent
    
    from_date=request.vars.from_date
    to_date=request.vars.to_date
    
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
        if min_amount<=0:
            form.errors.min_amount=''
            response.flash = 'Invalid Min Amount' 
        elif discount_percent<=0:
            form.errors.discount_precent=''
            response.flash = 'Invalid Discount Percent' 
        
        
#         else:
#             if discount_precent
                
def regular_discount():
    task_id='rm_campaign_manage'
    task_id_view='rm_campaign_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))
     
    response.title='Regular Discount'
     
    cid=session.cid
     
    form =SQLFORM(db.sm_promo_regular_discount,
                  fields=['from_date','to_date','min_amount','discount_precent','circular_number','status'],       
                  submit_button='Save'
                  )
     
    form.vars.cid=cid
    if form.accepts(request.vars,session,onvalidation=regular_discount_validation):
       response.flash = 'Submitted Successfully'
     
         
    #  Set text for filter
    btn_filter_regular_discount=request.vars.btn_filter_item
    btn_all=request.vars.btn_all
    reqPage=len(request.args)
     
    if btn_filter_regular_discount:
        session.btn_filter_regular_discount=btn_filter_regular_discount
        session.search_type_regular_discount=request.vars.search_type
        session.search_value_regular_discount=request.vars.search_value
 
        reqPage=0
    elif btn_all:
        session.btn_filter_regular_discount=None
        session.search_type_regular_discount=None
        session.search_value_regular_discount=None
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
    qset=qset(db.sm_promo_regular_discount.cid==cid)
             
    if (session.btn_filter_regular_discount and session.search_type_regular_discount=='Min_Amount'):
        qset=qset(db.sm_promo_regular_discount.min_amount>=session.search_value_regular_discount)    
        
    elif (session.btn_filter_regular_discount and session.search_type_regular_discount=='Status'):
        qset=qset(db.sm_promo_regular_discount.status==session.search_value_regular_discount.upper())
         
    records=qset.select(db.sm_promo_regular_discount.ALL,orderby=db.sm_promo_regular_discount.discount_precent,limitby=limitby)
    totalCount=qset.count()
     
    #----------------- filter end
    return dict(form=form,records=records,totalCount=totalCount,page=page,items_per_page=items_per_page,access_permission=access_permission)
 
 
#Validation for item edit
def regular_discount_edit_validation(form):
    cid=session.cid
    
    from_date=request.vars.from_date
    to_date=request.vars.to_date
    
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
        pass
     
def regular_discount_edit():
    task_id='rm_campaign_manage'
    access_permission=check_role(task_id)
    if (access_permission==False):
        session.flash='Access is Denied !'
        redirect (URL('promotion','regular_discount'))
     
    #Set combos for unit and catagory    
    response.title='Regular Discount '
    
    cid=session.cid
    page=request.args(0)
    rowID=request.args(1)
    record= db.sm_promo_regular_discount(rowID) #or redirect(URL('index'))  
      
    form =SQLFORM(db.sm_promo_regular_discount,
                  record=record,
                  deletable=True,
                  fields=['from_date','to_date','min_amount','discount_precent','circular_number','status'],       
                  submit_button='Update'
                  )
     
    if form.accepts(request.vars, session,onvalidation=regular_discount_edit_validation):
        response.flash = 'Updated Successfully'        
        redirect(URL('regular_discount',args=[page]))
    
    recordRows=db((db.sm_promo_regular_discount.cid==cid)&(db.sm_promo_regular_discount.id==rowID)).select(db.sm_promo_regular_discount.ALL,limitby=(0,1))
    
         
    return dict(form=form,page=page,recordRows=recordRows)
 
 
#====================================== Regular Discount BATCH UPLOAD 
   
def regular_discount_batch_upload():
    response.title='Regular Discount Batch upload'
     
     #----------Task assaign----------
    task_id='rm_campaign_manage'
    access_permission=check_role(task_id)
#    access_permission_view=check_role(task_id_view)
    if access_permission==False:
        session.flash='Access is Denied !'
        redirect (URL('promotion','regular_discount'))
    
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
                
        ins_list=[]
        ins_dict={}
        #   ----------------------
               
        # main loop   
        for i in range(total_row):
            if i>=30: 
                break
            else:
                row_data=row_list[i]
            coloum_list=row_data.split( '\t')            
            
            if len(coloum_list)!=6:
                error_data=row_data+'(6 columns need in a row)\n'
                error_str=error_str+error_data
                count_error+=1
                continue
            else:                               
                from_date=str(coloum_list[0]).strip()
                to_date=str(coloum_list[1]).strip()
                minAmount=str(coloum_list[2]).strip()               
                discountPrecent=str(coloum_list[3]).strip()
                discountAmount=str(coloum_list[4]).strip()   
                circular_number=str(coloum_list[5]).strip() 
                status='ACTIVE'
                
                #------------------
                if from_date=='' or to_date=='' or minAmount=='' or (discountPrecent=='' and discountAmount=='') or circular_number=='':
                    error_data=row_data+'(Required value)\n'
                    error_str=error_str+error_data
                    count_error+=1
                    continue
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
                        minAmount=float(minAmount)
                    except:
                        minAmount=0
                    
                    try:
                        discountPrecent=float(discountPrecent)
                    except:
                        discountPrecent=0
                    
                    try:
                        discountAmount=float(discountAmount)
                    except:
                        discountAmount=0
                    
                    
                    #-------------------
                                           
#                     existCheckRows=db((db.sm_promo_regular_discount.cid==c_id)&(db.sm_promo_regular_discount.from_date>to_date)).select(db.sm_promo_regular_discount.id,limitby=(0,1))
                    if dateFlag==False:
                        error_data=row_data+'(Invalid Date Range)\n'
                        error_str=error_str+error_data
                        count_error+=1
                        continue
                    else:
                        if minAmount<=0:
                            error_data=row_data+'(Invalid Min Amount!)\n'
                            error_str=error_str+error_data
                            count_error+=1
                            continue
                        else:
                            if discountPrecent==0 and discountAmount==0:
                                error_data=row_data+'(Required valid Discount Percent or Amount!)\n'
                                error_str=error_str+error_data
                                count_error+=1
                                continue
                            else:                                        
                                try:
                                    db.sm_promo_regular_discount.insert(cid=c_id,from_date=from_date,to_date=to_date,min_amount=minAmount,discount_precent=discountPrecent,discount_amount=discountAmount,circular_number=circular_number,status=status)
                                    count_inserted+=1                                    
                                except:
                                    error_data=row_data+'(error in process!)\n'
                                    error_str=error_str+error_data
                                    count_error+=1
                                    continue
        
        if error_str=='':
            error_str='No error'
    
    return dict(count_inserted=count_inserted,count_error=count_error,error_str=error_str,total_row=total_row)
   
#------------------item end----------------------
 
#============================================== Download
 
def regular_discount_download():
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
    qset=qset(db.sm_promo_regular_discount.cid==cid)
     
    if (session.btn_filter_regular_discount and session.search_type_regular_discount=='Min_Amount'):
        qset=qset(db.sm_promo_regular_discount.min_amount>=session.search_value_regular_discount) 
        
    elif (session.btn_filter_regular_discount and session.search_type_regular_discount=='Status'):
        qset=qset(db.sm_promo_regular_discount.status==session.search_value_regular_discount.upper())
         
    records=qset.select(db.sm_promo_regular_discount.ALL,orderby=db.sm_promo_regular_discount.min_amount)
     
    #Create string for download as excel file
    myString='Regular Discount List\n'
    myString+='From-date,To-date,Min Amount,Discount Precent,Discount Amount,Circular Number,Status\n'
    #Replace coma from records. cause coma means new Column    
    for rec in records:
        from_date=rec.from_date
        to_date=str(rec.to_date)
        min_amount=str(rec.min_amount)
        discount_precent=rec.discount_precent
        discount_amount=str(rec.discount_amount)
        circular_number=str(rec.circular_number)   
        status=str(rec.status)
         
        myString+=str(from_date)+','+str(to_date)+','+str(min_amount)+','+str(discount_precent)+','+str(discount_amount)+','+str(circular_number)+','+str(status)+'\n'
 
    #-----------
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_regular_discount.csv'   
    return str(myString)





#===================Declared Item================

def declared_item_validation(form):    
    cid=session.cid
    
    approved_date=form.vars.approved_date
    
    product_id=str(request.vars.product_id).strip().upper()
    product_name_row=str(request.vars.product_name)
    product_name=check_special_char(product_name_row)#Check spacial char
    
    product_rows_check=db((db.sm_item.cid==cid) & (db.sm_item.item_id==product_id)).select(db.sm_item.item_id,limitby=(0,1))
    if not product_rows_check:
        form.errors.product_id=''
        response.flash = 'Invalid Product Id '
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
            response.flash="Invalid Approved Date"    
        else:
            form.vars.product_id=product_id
            form.vars.product_name=product_name
                    
def declared_item():
    task_id='rm_campaign_manage'
    task_id_view='rm_campaign_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))
     
    response.title='Declared Item'
     
    cid=session.cid
     
    form =SQLFORM(db.sm_promo_declared_item,
                  fields=['approved_date','product_id','product_name','status'],       
                  submit_button='Save'
                  )
     
    form.vars.cid=cid
    if form.accepts(request.vars,session,onvalidation=declared_item_validation):
        #--------- update promo
        db((db.sm_settings.cid == session.cid)&(db.sm_settings.s_key == 'PROMO_DATE')).update(s_value=datetime_fixed)
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
    qset=qset(db.sm_promo_declared_item.cid==cid)
     
    if (session.btn_filter_declared_item and session.search_type_declared_item=='Product_id'):
        searchValue=str(session.search_value_declared_item).split('|')[0]        
        qset=qset(db.sm_promo_declared_item.product_id==searchValue.upper())
        
    elif (session.btn_filter_declared_item and session.search_type_declared_item=='Status'):
        qset=qset(db.sm_promo_declared_item.status==session.search_value_declared_item.upper())
         
    records=qset.select(db.sm_promo_declared_item.ALL,orderby=db.sm_promo_declared_item.product_name,limitby=limitby)
    totalCount=qset.count()
     
    #----------------- filter end
    return dict(form=form,records=records,totalCount=totalCount,page=page,items_per_page=items_per_page,access_permission=access_permission)
 
 
#Validation for item edit
def declared_item_edit_validation(form):
     
    product_name_row=str(request.vars.product_name)
    product_name=check_special_char(product_name_row)
     
    form.vars.product_name=product_name
     
def declared_item_edit():
    task_id='rm_campaign_manage'
    access_permission=check_role(task_id)
    if (access_permission==False):
        session.flash='Access is Denied !'
        redirect (URL('promotion','declared_item'))
     
    #Set combos for unit and catagory    
    response.title='Declared Item'
    
    cid=session.cid
    page=request.args(0)
    rowID=request.args(1)
    record= db.sm_promo_declared_item(rowID) #or redirect(URL('index'))  
      
    form =SQLFORM(db.sm_promo_declared_item,
                  record=record,
                  deletable=True,
                  fields=['approved_date','product_id','product_name','status'],        
                  submit_button='Update'
                  )
     
    if form.accepts(request.vars, session,onvalidation=declared_item_edit_validation):
        #--------- update promo
        db((db.sm_settings.cid == session.cid)&(db.sm_settings.s_key == 'PROMO_DATE')).update(s_value=datetime_fixed)
        
        response.flash = 'Updated Successfully'        
        redirect(URL('declared_item',args=[page]))
    
    recordRows=db((db.sm_promo_declared_item.cid==cid)&(db.sm_promo_declared_item.id==rowID)).select(db.sm_promo_declared_item.ALL,limitby=(0,1))
    
         
    return dict(form=form,page=page,recordRows=recordRows)
 
 
#======================================Declared Item BATCH UPLOAD    
def declared_item_batch_upload():
    response.title='Declared Item Batch upload'
     
     #----------Task assaign----------
    task_id='rm_campaign_manage'
    access_permission=check_role(task_id)
#    access_permission_view=check_role(task_id_view)
    if access_permission==False:
        session.flash='Access is Denied !'
        redirect (URL('promotion','declared_item'))
    
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
              
        item_id_list_exist=[]
        
        item_id_list_excel=[]
                
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
                if len(coloum_list)==2:
                    itemIDExcel=str(coloum_list[1]).strip().upper()
                    
                    if itemIDExcel!='':
                        if itemIDExcel not in item_id_list_excel:
                            item_id_list_excel.append(itemIDExcel)
        
        #Check valid item list based on excel sheet        
        itemRows=db((db.sm_item.cid==c_id)&(db.sm_item.item_id.belongs(item_id_list_excel))).select(db.sm_item.item_id,db.sm_item.name,orderby=db.sm_item.item_id)
        item_id_list_exist=itemRows.as_list()
        
        #--------- update promo
        db((db.sm_settings.cid == session.cid)&(db.sm_settings.s_key == 'PROMO_DATE')).update(s_value=datetime_fixed)
        
        # main loop   
        for i in range(total_row):
            if i>=30: 
                break
            else:
                row_data=row_list[i]
            coloum_list=row_data.split( '\t')            
            
            if len(coloum_list)!=2:
                error_data=row_data+'(2 columns need in a row)\n'
                error_str=error_str+error_data
                count_error+=1
                continue
            else:                               
                approvedDate=str(coloum_list[0]).strip()
                item_idExcel=str(coloum_list[1]).strip()  
                status='ACTIVE'
                
                #------------------
                if approvedDate=='' or item_idExcel=='':
                    error_data=row_data+'(Required all value)\n'
                    error_str=error_str+error_data
                    count_error+=1
                    continue
                else:
                    dateFlag=True                    
                    try:
                        approvedDate=datetime.datetime.strptime(approvedDate,'%Y-%m-%d')
                        if approvedDate==False:
                            dateFlag=False
                    except:
                        dateFlag=False  
                    
#                     if  dateFlag==False:
#                         response.flash="Invalid Date Formate"
#                         
                    #-------------------
                    
                    valid_item_id=False
                    
                    itemName='' 
                      
                    #Check valid client_list                         
                    for i in range(len(item_id_list_exist)):
                        myRowData=item_id_list_exist[i]                                
                        item_id=myRowData['item_id']
                        if (str(item_id).strip()==str(item_idExcel).strip()):
                            valid_item_id=True
                            itemName=myRowData['name']
                            break
                    
                    #-----------------
                    
                    if valid_item_id==False:
                        error_data=row_data+'(Invalid Product ID)\n'
                        error_str=error_str+error_data
                        count_error+=1
                        continue
                    else:
                        if  dateFlag==False:
                            error_data=row_data+'(Invalid Approved Date)\n'
                            error_str=error_str+error_data
                            count_error+=1
                            continue  
                        else:                                
                            existCheckRows=db((db.sm_promo_declared_item.cid==c_id)&(db.sm_promo_declared_item.product_id==item_idExcel)).select(db.sm_promo_declared_item.id,limitby=(0,1))
                            if existCheckRows:
                                error_data=row_data+'(Duplicate check for Product ID)\n'
                                error_str=error_str+error_data
                                count_error+=1
                                continue
                            else:
                                
                                try:
                                    db.sm_promo_declared_item.insert(cid=c_id,approved_date=approvedDate,product_id=item_idExcel,product_name=itemName,status=status)
                                    count_inserted+=1                                    
                                except:
                                    error_data=row_data+'(error in process!)\n'
                                    error_str=error_str+error_data
                                    count_error+=1
                                    continue
        
        if error_str=='':
            error_str='No error'
    
    return dict(count_inserted=count_inserted,count_error=count_error,error_str=error_str,total_row=total_row)
   
#------------------item end----------------------
 
 
 
        
 
#============================================== Download
 
def declared_item_download():
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
    qset=qset(db.sm_promo_declared_item.cid==cid)
     
    if (session.btn_filter_declared_item and session.search_type_declared_item=='Product_id'):
        searchValue=str(session.search_value_declared_item).split('|')[0]        
        qset=qset(db.sm_promo_declared_item.product_id==searchValue.upper())
        
    elif (session.btn_filter_declared_item and session.search_type_declared_item=='Status'):
        qset=qset(db.sm_promo_declared_item.status==session.search_value_declared_item.upper())
         
    records=qset.select(db.sm_promo_declared_item.ALL,orderby=db.sm_promo_declared_item.product_name)
    
    #Create string for download as excel file
    myString='Declared Item List\n'
    myString+='Approved date,Product ID,Product Name,Status\n'
    #Replace coma from records. cause coma means new Column    
    for rec in records:
        approved_date=rec.approved_date
        product_id=str(rec.product_id)
        product_name=str(rec.product_name)       
        status=str(rec.status)
         
        myString+=str(approved_date)+','+str(product_id)+','+str(product_name)+','+str(status)+'\n'
 
    #-----------
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_declared_item.csv'   
    return str(myString)



