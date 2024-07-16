#catagory_validation
#catagory
#unit_validation
#unit
#item_validation
#item
#item_edit_validation
#item_edit
#item_batch_upload
#download_item
#----------------------------------------------
import time

#Validation for catagory
def catagory_validation(form):    
    category_id=str(request.vars.cat_type_id).strip().upper()
    if ((category_id!='') and (session.cid!='')):
        rows_check=db((db.sm_category_type.cid==session.cid) & (db.sm_category_type.type_name=='ITEM_CATEGORY') &(db.sm_category_type.cat_type_id==category_id)).select(db.sm_category_type.cat_type_id,orderby=db.sm_category_type.cat_type_id,limitby=(0,1))
        if rows_check:
            form.errors.cat_type_id=''
            response.flash = 'please choose a new '
        else:
            form.vars.cid=session.cid
            form.vars.type_name='ITEM_CATEGORY'
            form.vars.cat_type_id=category_id
def catagory():
    #----------Task assaign----------
    task_id='rm_item_cat_unit_manage'
    task_id_view='rm_item_cat_unit_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))
    # ---------------------
    
    response.title='Category'
    
    form =SQLFORM(db.sm_category_type,
                  fields=['cat_type_id'],
                  submit_button='Save'          
                  )
    
    #Insert with validation
    if form.accepts(request.vars,session,onvalidation=catagory_validation):
       response.flash = 'Saved Successfully'
       
    #--------------------------------
    btn_delete=request.vars.btn_delete
    record_id=request.vars.record_id
    
    #If catagorey not in item it can be delete
    if btn_delete:
        record_id=request.args[1]
        category_id=request.args[2]
        records=db((db.sm_item.cid==session.cid) & (db.sm_item.category_id==category_id)).select(db.sm_item.category_id,limitby=(0,1))
        if not records:
            db((db.sm_category_type.id==record_id)&(db.sm_category_type.type_name=='ITEM_CATEGORY')).delete()
        else:
            response.flash='This category is used in Item'
    
    #--------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=session.items_per_page
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #--------end paging
    
    records=db((db.sm_category_type.cid==session.cid)& (db.sm_category_type.type_name=='ITEM_CATEGORY')).select(db.sm_category_type.ALL,orderby=db.sm_category_type.cat_type_id,limitby=limitby)

    return dict(form=form,records=records,page=page,items_per_page=items_per_page,access_permission=access_permission)


#Validation for unit
def unit_validation(form):
    unit_type=str(request.vars.cat_type_id).strip()

    if ((unit_type!='') and (session.cid!='')):
        rows_check=db((db.sm_category_type.cid==session.cid) & (db.sm_category_type.type_name=='ITEM_UNIT') &(db.sm_category_type.cat_type_id==unit_type)).select(db.sm_category_type.cat_type_id,orderby=db.sm_category_type.cat_type_id,limitby=(0,1))
        if rows_check:
            form.errors.cat_type_id=''
            response.flash = 'please choose a new '
        else:
            form.vars.cid=session.cid
            form.vars.type_name='ITEM_UNIT'
            form.vars.cat_type_id=unit_type
def unit():
    task_id='rm_item_cat_unit_manage'
    task_id_view='rm_item_cat_unit_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))
    
    response.title='Unit Type'
    
    #   ---------------------
    
    form =SQLFORM(db.sm_category_type,
                  fields=['cat_type_id'],
                  submit_button='Save'
                  )
    #Insert with validation
    if form.accepts(request.vars,session,onvalidation=unit_validation):
       response.flash = 'Submitted Successfully'
#       redirect (URL('item','unit'))
    #--------------------------------
    btn_delete=request.vars.btn_delete
    record_id=request.vars.record_id
    if btn_delete:
        record_id=request.args[1]
        
        unitRow=db((db.sm_category_type.id == record_id)&(db.sm_category_type.type_name=='ITEM_UNIT')).select(db.sm_category_type.cat_type_id,limitby=(0,1))
        if not unitRow:
            response.flash = 'Invalid Request'
        else:
            unit_type=unitRow[0].cat_type_id
            records=db((db.sm_item.cid==session.cid) & (db.sm_item.unit_type==unit_type)).select(db.sm_item.unit_type,limitby=(0,1))
            if not records:
                db((db.sm_category_type.id == record_id)&(db.sm_category_type.type_name=='ITEM_UNIT')).delete()
            else:
                response.flash='This type is used in another object!'
    
    #--------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=session.items_per_page
    limitby=(page*items_per_page,(page+1)*items_per_page+1)   
    #--------end paging    
    
    records=db((db.sm_category_type.cid==session.cid)& (db.sm_category_type.type_name=='ITEM_UNIT')).select(db.sm_category_type.ALL,orderby=db.sm_category_type.cat_type_id,limitby=limitby)

    return dict(form=form,records=records,page=page,items_per_page=items_per_page,access_permission=access_permission)


#Validation for item

def item_validation(form):    
    cid=session.cid
    
    item_id=str(request.vars.item_id).strip().upper()
    item_name_row=str(request.vars.name)
    item_name=check_special_char(item_name_row)#Check spacial char
    #dist_price=request.vars.dist_price
    try:
        item_carton=int(request.vars.item_carton)
    except:
        item_carton=0
        
    price=request.vars.price
    vat_amt=request.vars.vat_amt
    
    category_id=request.vars.category_id
    category_id_sp=request.vars.category_id_sp
    
    rows_check=db((db.sm_item.cid==cid) & (db.sm_item.item_id==item_id)).select(db.sm_item.item_id,limitby=(0,1))
    if rows_check:
        form.errors.item_id=''
        response.flash = 'Item ID already exist'
    else:
        if category_id== category_id_sp:
            category_id_sp=''
        
#         catFlag=True
#         if category_id=='C' and category_id_sp=='':
#             catFlag=False
#         
#         if catFlag==False:
#             form.errors.category_id_sp='Required special category for Primary category "C" '
#         else:
#             if category_id!='C' and category_id_sp!='':
#                 form.errors.category_id_sp='Required special category empty except for Primary Category "C" '
#             else:
        if price < 0 :
            form.errors.price='Enter M.R.P accurately'
        else:
            if vat_amt < 0 :
                form.errors.vat_amt='Enter VAT accurately'
            else:
                total_amt=round(float(price)+float(vat_amt),2) #TP+VAT
                
                form.vars.item_id=item_id
                form.vars.name=item_name
                form.vars.total_amt=total_amt
                form.vars.item_carton=item_carton
                
                form.vars.category_id=category_id
                form.vars.category_id_sp=category_id_sp
                form.vars.status='ACTIVE'
                
def item():
    task_id='rm_item_manage'
    task_id_view='rm_item_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))
    
    response.title='Item'
    
    cid=session.cid
    
    # Set combo for catagory and unit
    db.sm_item.category_id.requires=IS_IN_DB(db((db.sm_category_type.cid == cid)&(db.sm_category_type.type_name=='ITEM_CATEGORY')),db.sm_category_type.cat_type_id,error_message='Select a value',orderby=db.sm_category_type.cat_type_id)
    db.sm_item.category_id_sp.requires=IS_EMPTY_OR(IS_IN_DB(db((db.sm_category_type.cid == cid)&(db.sm_category_type.type_name=='ITEM_CATEGORY')),db.sm_category_type.cat_type_id,orderby=db.sm_category_type.cat_type_id))
    db.sm_item.unit_type.requires=IS_IN_DB(db((db.sm_category_type.cid == session.cid)&(db.sm_category_type.type_name=='ITEM_UNIT')),db.sm_category_type.cat_type_id,error_message='Select a value',orderby=db.sm_category_type.cat_type_id)
    
    form =SQLFORM(db.sm_item,
                  fields=['item_id','name','des','category_id','category_id_sp','unit_type','manufacturer','item_carton','price','vat_amt'],       
                  submit_button='Save'
                  )
    
    #Insert with validation
    if form.accepts(request.vars,session,onvalidation=item_validation):
        #Select item string from company settings 
        item_id=","+str(form.vars.item_id).strip().upper()+","
        try:
            settings_records=db(db.sm_company_settings.cid==cid).select(db.sm_company_settings.id,db.sm_company_settings.item_list)
            item_list=settings_records[0].item_list
            if item_list==None:
                item_list=''
            
            
            #If item is not in item string then update string with new item id                    
            itemListStr=str(item_list).strip() 
            if (itemListStr.find(item_id)== (-1)):
                if itemListStr=='':
                    itemListStr=item_id
                else:
                    itemListStr=itemListStr+item_id
                
                #replace double com from string    
                itemListStr=itemListStr.replace(",,",",")
                settings_records[0].update_record(item_list=itemListStr)
                response.flash = 'Saved successfully '
#                redirect (URL('item','item'))
            else:
                db.rollback()
                response.flash = 'ItemID already exist!'
        except:
            db.rollback()
            response.flash = 'Process error!'
#            redirect (URL('item','item'))
        #-------------
        
        
    #  Set text for filter
    btn_filter_item=request.vars.btn_filter_item
    btn_all=request.vars.btn_all
    reqPage=len(request.args)
    
    if btn_filter_item:
        session.btn_filter_item=btn_filter_item
        session.search_type_item=request.vars.search_type
        session.search_value_item=request.vars.search_value

        reqPage=0
    
    elif btn_all:
        session.btn_filter_item=None
        session.search_type_item=None
        session.search_value_item=None
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
    qset=qset(db.sm_item.cid==cid)
    
    if (session.btn_filter_item and session.search_type_item=='ItemID'):
        searchValue=str(session.search_value_item).split('|')[0]        
        qset=qset(db.sm_item.item_id==searchValue.upper())
        
    elif (session.btn_filter_item and session.search_type_item=='Catagory'):
        qset=qset(db.sm_item.category_id==session.search_value_item.upper())
        
    elif (session.btn_filter_item and session.search_type_item=='Unit'):
        qset=qset(db.sm_item.unit_type==session.search_value_item.upper())
        
    records=qset.select(db.sm_item.ALL,orderby=db.sm_item.name,limitby=limitby)
    totalCount=qset.count()
    
    #----------------- filter end
    return dict(form=form,records=records,totalCount=totalCount,page=page,items_per_page=items_per_page,access_permission=access_permission)


#Validation for item edit
def item_edit_validation(form):
    #dist_price=request.vars.dist_price
    
    item_name_row=str(request.vars.name)
    item_name=check_special_char(item_name_row)
    
    try:
        item_carton=int(request.vars.item_carton)
    except:
        item_carton=0
    
    price=request.vars.price
    vat_amt=request.vars.vat_amt
    status=request.vars.status
    category_id=request.vars.category_id
    category_id_sp=request.vars.category_id_sp
    if category_id== category_id_sp:
        category_id_sp=''
#         form.errors.category_id_sp='Primary and Special Category can not be same'
#     else:
#         catFlag=True
#         if category_id=='C' and category_id_sp=='':
#             catFlag=False
#             
#         if catFlag==False:
#             form.errors.category_id_sp='Required special category for Primary category "C" '
#         else:
#             if category_id!='C' and category_id_sp!='':
#                 form.errors.category_id_sp='Required special category empty except for Primary Category "C" '
#             else:                
    if price < 0 :
        form.errors.price='Enter M.R.P accurately'
    else:
        if vat_amt < 0 :
            form.errors.vat_amt='Enter VAT accurately'
        else:
            total_amt=round(float(price)+float(vat_amt),2) #TP+VAT
            
            form.vars.name=item_name
            form.vars.total_amt=total_amt
            form.vars.item_carton=item_carton
            form.vars.category_id=category_id
            form.vars.category_id_sp=category_id_sp
def item_edit():
    task_id='rm_item_manage'
    access_permission=check_role(task_id)
    if (access_permission==False):
        session.flash='Access is Denied !'
        redirect (URL('item','item'))
    
    cid=session.cid
    #Set combos for unit and catagory    
    response.title='Item'

    db.sm_item.category_id.requires=IS_IN_DB(db((db.sm_category_type.cid == cid)&(db.sm_category_type.type_name=='ITEM_CATEGORY')),db.sm_category_type.cat_type_id,error_message='Select a value',orderby=db.sm_category_type.cat_type_id)
    db.sm_item.category_id_sp.requires=IS_EMPTY_OR(IS_IN_DB(db((db.sm_category_type.cid == cid)&(db.sm_category_type.type_name=='ITEM_CATEGORY')),db.sm_category_type.cat_type_id,orderby=db.sm_category_type.cat_type_id))
    db.sm_item.unit_type.requires=IS_IN_DB(db((db.sm_category_type.cid == cid)&(db.sm_category_type.type_name=='ITEM_UNIT')),db.sm_category_type.cat_type_id,error_message='Select a value',orderby=db.sm_category_type.cat_type_id)
    
    page=request.args(0)
    record= db.sm_item(request.args(1)) #or redirect(URL('index'))  
    
    form =SQLFORM(db.sm_item,
                  record=record,
                  deletable=True,
                  linkto=None,
                  upload=None,
                  fields=['name','des','category_id','category_id_sp','unit_type','manufacturer','item_carton','price','vat_amt','status'],
                  submit_button='Update'
                  )
    
    records_item=db((db.sm_item.cid==session.cid) & (db.sm_item.id==request.args(1))).select(db.sm_item.item_id,limitby=(0,1))
    item_id=''
    for records_show_id in records_item :
         item_id=records_show_id.item_id     
         break
    #Edit item with validation 
    if form.accepts(request.vars,session,onvalidation=item_edit_validation):
        #Catch delete variable.Selectitem string from company settings table 
        status=form.vars.status
        
        if form.vars.get('delete_this_record', False): #or status=='INACTIVE'
            settings_records=db(db.sm_company_settings.cid==cid).select(db.sm_company_settings.id,db.sm_company_settings.item_list,limitby=(0,1))
            item_list=settings_records[0].item_list
            if item_list==None:
                item_list=''
                
            itemListStr=str(item_list).strip() 
            
            item_id=','+str(item_id).strip()+','
            #Replace item as blank,replace double coma 
            if (itemListStr.find(item_id)!= (-1)):
                itemListStr=itemListStr.replace(item_id,",")
                
                itemListStr=itemListStr.replace(",,",",")
                settings_records[0].update_record(item_list=itemListStr)
                
            #---------
        session.flash = 'Updated Successfully'
        redirect(URL(c='item',f='item',args=[page]))

    return dict(form=form,item_id=item_id,page=page)


#====================================== BATCH UPLOAD 
def item_batch_upload():
    response.title='Item Batch upload'
    
    #----------Task assaign----------
    task_id='rm_item_manage'
    access_permission=check_role(task_id)
#    access_permission_view=check_role(task_id_view)
    if access_permission==False:
        session.flash='Access is Denied !'
        redirect (URL('item','item'))
    
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
        
        item_id_list_excel=[]
        item_id_list_exist=[]
        category_list_exist=[]
        
        unit_list=[]
        
        ins_list=[]
        ins_dict={}
        #   ----------------------
        #---------- rep area
        for i in range(total_row):
            if i>=100:
                break
            else:
                row_data=row_list[i]                    
                coloum_list=row_data.split( '\t')
                if len(coloum_list)==11:
                    item_id_list_excel.append(coloum_list[0])
        
        
        #Create list based on excel sheet which items are already exist in database
        existRows=db((db.sm_item.cid==c_id)&(db.sm_item.item_id.belongs(item_id_list_excel))).select(db.sm_item.item_id,orderby=db.sm_item.item_id)
        item_id_list_exist=existRows.as_list()
        
        #Check valid category list based on excel sheet
        catRows=db((db.sm_category_type.cid==c_id)& (db.sm_category_type.type_name=='ITEM_CATEGORY')).select(db.sm_category_type.cat_type_id,orderby=db.sm_category_type.cat_type_id)
        category_list_exist=catRows.as_list()
        
        #Check valid unit list based on excel sheet
        unitRows=db((db.sm_category_type.cid==c_id)& (db.sm_category_type.type_name=='ITEM_UNIT')).select(db.sm_category_type.cat_type_id,orderby=db.sm_category_type.cat_type_id)
        unit_list=unitRows.as_list()
        
        #Select item string sm_company_settings
        settings_records=db(db.sm_company_settings.cid==session.cid).select(db.sm_company_settings.id,db.sm_company_settings.item_list,limitby=(0,1))
        item_list=settings_records[0].item_list
        if item_list==None:
            item_list=''        
        itemListStr=str(item_list).strip()
        
        # main loop   
        for i in range(total_row):
            if i>=100: 
                break
            else:
                row_data=row_list[i]
            coloum_list=row_data.split( '\t')            
            
            if len(coloum_list)==11:
                item_id=str(coloum_list[0]).strip().upper()
                name=str(coloum_list[1]).strip()
                name=check_special_char(name)#Check spacial char
                
                des=str(coloum_list[2]).strip()
                category_id=str(coloum_list[3]).strip().upper()
                category_id_sp=str(coloum_list[4]).strip().upper()#special category
                unit_type=str(coloum_list[5]).strip()
                manufacturer=str(coloum_list[6]).strip()
                mCarton=str(coloum_list[7]).strip()
                price=str(coloum_list[8]).strip()  #Distributor Price
                vat_amt=str(coloum_list[9]).strip()       #Retailer Price
                status=str(coloum_list[10]).strip().upper()
                
                if des=='':
                    des='-'
                
                if manufacturer=='':
                    manufacturer='-'
                
                try:
                    mCarton=int(mCarton)                    
                except:
                    mCarton=0
                    
                #------------------
                if price=='':
                    price=0.0
                    
                if vat_amt=='':
                    vat_amt=0.0
                
                
                #-------------------
                total_amt=0
                try:
                    price=float(price)
                    vat_amt=float(vat_amt)
                    total_amt=round(price+vat_amt,2)
                except:
                    price=0
                    vat_amt=0
                    
                try:                    
                    if item_id=='' or name=='' or category_id=='' or unit_type=='':
                        error_data=row_data+'(Required value can not empty)\n'
                        error_str=error_str+error_data
                        count_error+=1
                        continue
                    else:                    
                        if category_id==category_id_sp:
                            category_id_sp=''
                        
                        valid_category=False
                        valid_unit=False
                        duplicate_item=False                        
                        valid_category_sp=False
                        duplicate_category_sp=False
                        
                        #Check valid category                          
                        for i in range(len(category_list_exist)):
                            myRowData=category_list_exist[i]                                
                            cat_id=myRowData['cat_type_id']
                            if (str(cat_id).strip()==str(category_id).strip()):
                                valid_category=True
                                break
                        
                        if valid_category==True:
                            if category_id==category_id_sp:
                                duplicate_category_sp=True
                            else:
                                if category_id_sp!='':                                    
                                    #Check valid category                          
                                    for i in range(len(category_list_exist)):
                                        myRowData=category_list_exist[i]                                
                                        cat_id_sp=myRowData['cat_type_id']
                                        if (str(cat_id_sp).strip()==str(category_id_sp).strip()):
                                            valid_category_sp=True
                                            break
                                
                                elif category_id_sp=='':                                    
                                    valid_category_sp=True
                                
                        if valid_category==True and valid_category_sp==True: # check unit type                                                         
                            for i in range(len(unit_list)):
                                myRowData=unit_list[i]                                
                                u_type=myRowData['cat_type_id']
                                if (str(u_type).strip()==str(unit_type).strip()):
                                    valid_unit=True
                                    break
                        
                        if valid_unit==True:# check duplicate item                                                     
                            for i in range(len(item_id_list_exist)):
                                myRowData=item_id_list_exist[i]                                
                                itemId=myRowData['item_id']
                                if (str(itemId).strip()==str(item_id).strip()):
                                    duplicate_item=True                                 
                                    break
                        
                        #-----------------
                        if valid_category==False:
                            error_data=row_data+'(Invalid Primary Category!)\n'
                            error_str=error_str+error_data
                            count_error+=1
                            continue
                        else:
                            if duplicate_category_sp==True:
                                error_data=row_data+'(Primary Category and Special Category can not be same!)\n'
                                error_str=error_str+error_data
                                count_error+=1
                                continue
                            else:
                                if valid_category_sp==False:
                                    error_data=row_data+'(Required empty or valid special category according to Primary category!)\n'
                                    error_str=error_str+error_data
                                    count_error+=1
                                    continue
                                else:
                                    if valid_unit==False:
                                        error_data=row_data+'(Invalid Unit Type)\n'
                                        error_str=error_str+error_data
                                        count_error+=1
                                        continue
                                    else:
                                        if duplicate_item==True:
                                            error_data=row_data+'(Duplicate Item)\n'
                                            error_str=error_str+error_data
                                            count_error+=1
                                            continue
                                        else:
                                            if price<0 or vat_amt<0:
                                                error_data=row_data+'(Valid TP/VAT Required)\n'
                                                error_str=error_str+error_data
                                                count_error+=1
                                                continue
                                            else:
                                                
                                                #Add item in item string
                                                temp_item=","+item_id+","                                                    
                                                if (itemListStr.find(temp_item)== (-1)):
                                                    if itemListStr=='':
                                                        itemListStr=temp_item
                                                    else:
                                                        itemListStr=itemListStr+temp_item
                                                    
                                                    #Create dictionary for bulk insert                                        
                                                    ins_dict= {'cid':c_id,'item_id':item_id,'name':name,'des':des,'category_id':category_id,'category_id_sp':category_id_sp,'unit_type':unit_type,'manufacturer':manufacturer,'item_carton':mCarton,'price':price,'vat_amt':vat_amt,'total_amt':total_amt,'status':status}
                                                    ins_list.append(ins_dict)                               
                                                    count_inserted+=1
                                                    
                                                else:
                                                    error_data=row_data+'(already exist in item list)\n'
                                                    error_str=error_str+error_data
                                                    count_error+=1
                                                    continue
                
                except:
                    error_data=row_data+'(error in process!)\n'
                    error_str=error_str+error_data
                    count_error+=1
                    continue
            else:
                error_data=row_data+'(10 columns need in a row)\n'
                error_str=error_str+error_data
                count_error+=1
                continue
        
        if error_str=='':
            error_str='No error'
        
        if len(ins_list) > 0:
            #Bulk insert
            #Replace double com
            #Update item string in company settings table
            inCountList=db.sm_item.bulk_insert(ins_list)
            itemListStr=itemListStr.replace(",,",",")
            settings_records[0].update_record(item_list=itemListStr)
            
    return dict(count_inserted=count_inserted,count_error=count_error,error_str=error_str,total_row=total_row)

#------------------ end----------------------

#============================================== Download
def download_item():
    #Check access permission
    #----------Task assaign----------
    task_id='rm_item_manage'
    task_id_view='rm_item_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))
    
    
    cid=session.cid
    records=''
    #Create query based on search type
    qset=db()
    qset=qset(db.sm_item.cid==cid)
    
    if (session.btn_filter_item and session.search_type_item=='ItemID'):
        searchValue=str(session.search_value_item).split('|')[0]        
        qset=qset(db.sm_item.item_id==searchValue.upper())
        
    elif (session.btn_filter_item and session.search_type_item=='Catagory'):
        qset=qset(db.sm_item.category_id==session.search_value_item.upper())
        
    elif (session.btn_filter_item and session.search_type_item=='Unit'):
        qset=qset(db.sm_item.unit_type==session.search_value_item.upper())
        
    records=qset.select(db.sm_item.ALL,orderby=db.sm_item.name)
    
    #Create string for download as excel file
    myString='Item List\n'
    myString+='Item ID,Name,Description,Group/Category,Base Group/Category,Unit Type,Manufacturer,M.Carton,TP Amount,VAT Amount,Total Amount,Status\n'
    #Replace coma from records. cause coma means new Column    
    for rec in records:
        item_id=rec.item_id
        name=str(rec.name).replace(',', ' ')
        des=str(rec.des).replace(',', ' ')
        category_id=rec.category_id
        category_id_sp=rec.category_id_sp
        unit_type=rec.unit_type
        manufacturer=str(rec.manufacturer).replace(',', ' ')
        item_carton=rec.item_carton
        price=rec.price
        vat_amt=rec.vat_amt        
        total_amt=rec.total_amt
        status=rec.status
                
        if category_id_sp==None:
            category_id_sp=''
        myString+=str(item_id)+','+str(name)+','+str(des)+','+str(category_id)+','+str(category_id_sp)+','+str(unit_type)+','+str(manufacturer)+','+str(item_carton)+','+str(price)+','+str(vat_amt)+','+str(total_amt)+','+str(status)+'\n'
        
    #-----------
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_item.csv'   
    return str(myString)
    
#================Item batch id=============
#Validation for item
def item_batch_validation(form):    
    cid=session.cid
    
    item_id=str(request.vars.item_id).strip().upper().split('|')[0]
    batch_id=str(request.vars.batch_id).strip().upper()
    
    item_row=db((db.sm_item.cid==cid) & (db.sm_item.item_id==item_id)).select(db.sm_item.name,limitby=(0,1))
    if not item_row:
        form.errors.item_id=''
        response.flash = 'Invalid ItemID '
    else:
        item_name=item_row[0].name
        
        rows_check=db((db.sm_item_batch.cid==cid) & (db.sm_item_batch.item_id==item_id)& (db.sm_item_batch.batch_id==batch_id)).select(db.sm_item_batch.item_id,limitby=(0,1))
        if rows_check:
            form.errors.item_id=''
            response.flash = 'Already exist'
        else:            
            form.vars.item_id=item_id
            form.vars.batch_id=batch_id
            form.vars.name=item_name
def item_batch():
    task_id='rm_item_batch_manage'
    task_id_view='rm_item_batch_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))
        
    response.title='Item Batch'
    
    cid=session.cid
    
    form =SQLFORM(db.sm_item_batch,
                  fields=['item_id','batch_id','expiary_date'],       
                  submit_button='Save'
                  )
    
    #Insert with validation
    if form.accepts(request.vars,session,onvalidation=item_batch_validation):
        item_id=form.vars.item_id
        batch_id=form.vars.batch_id
        expiary_date=form.vars.expiary_date
        
        insertRecords="insert into sm_depot_stock_balance(cid,depot_id,store_id,store_name,item_id,batch_id,expiary_date,quantity)(select cid,depot_id,store_id,store_name,'"+str(item_id)+"','"+str(batch_id)+"','"+str(expiary_date)+"',0 from sm_depot_store where cid='"+cid+"')"
        db.executesql(insertRecords)
        
        response.flash = 'Saved Successfully'
        
#    -------------Delete--------
    btn_delete=request.vars.btn_delete
    if btn_delete:
        row_id=request.args[1]
        check_delete=request.vars.check_delete
        
        if check_delete!='YES':
            response.flash = 'Required checked confirmation'
        else:
            itemRow=db((db.sm_item_batch.cid==cid)&(db.sm_item_batch.id==row_id)).select(db.sm_item_batch.item_id,db.sm_item_batch.batch_id,db.sm_item_batch.expiary_date,limitby=(0,1))
            if not itemRow:
                response.flash = 'Invalid request'
            else:
                item_id=itemRow[0].item_id
                batch_id=itemRow[0].batch_id
                
                balanceRecords=db((db.sm_depot_stock_balance.cid==cid)&(db.sm_depot_stock_balance.item_id==item_id)&(db.sm_depot_stock_balance.batch_id==batch_id)&(db.sm_depot_stock_balance.quantity>0)).select(db.sm_depot_stock_balance.id,limitby=(0,1))
                if balanceRecords:
                    response.flash = 'Already used in Stock'
                else:
                    issueRow=db((db.sm_issue.cid==cid)&(db.sm_issue.item_id==item_id)&(db.sm_issue.batch_id==batch_id)&(db.sm_issue.status!='Cancelled')).select(db.sm_issue.id,limitby=(0,1))
                    if issueRow:
                        response.flash = 'Already used in Issue'
                    else:
                        recRow=db((db.sm_receive.cid==cid)&(db.sm_receive.item_id==item_id)&(db.sm_receive.batch_id==batch_id)&(db.sm_receive.status!='Cancelled')).select(db.sm_receive.id,limitby=(0,1))
                        if recRow:
                            response.flash = 'Already used in Receive'
                        else:
                            damRow=db((db.sm_damage.cid==cid)&(db.sm_damage.item_id==item_id)&(db.sm_damage.batch_id==batch_id)&(db.sm_damage.status!='Cancelled')).select(db.sm_damage.id,limitby=(0,1))
                            if damRow:
                                response.flash = 'Already used in Adjustment'
                            else:
                                invRow=db((db.sm_invoice.cid==cid)&(db.sm_invoice.item_id==item_id)&(db.sm_invoice.batch_id==batch_id)&(db.sm_invoice.status!='Cancelled')).select(db.sm_invoice.id,limitby=(0,1))
                                if invRow:
                                    response.flash = 'Already used in Invoice'
                                else:
                                    retRow=db((db.sm_return.cid==cid)&(db.sm_return.item_id==item_id)&(db.sm_return.batch_id==batch_id)&(db.sm_return.status!='Cancelled')).select(db.sm_return.id,limitby=(0,1))
                                    if retRow:
                                        response.flash = 'Already used in Return'
                                    else:                                    
                                        db((db.sm_item_batch.id==row_id)).delete()
                                        db((db.sm_depot_stock_balance.cid==cid)&(db.sm_depot_stock_balance.item_id==item_id)&(db.sm_depot_stock_balance.batch_id==batch_id)).delete()
                                        response.flash = 'Deleted successfully'
    
    #-------------    
    #  Set text for filter
    btn_filter_item=request.vars.btn_filter_item
    btn_all=request.vars.btn_all
    reqPage=len(request.args)
    
    if btn_filter_item:
        session.btn_filter_item=btn_filter_item
        session.search_type_item=request.vars.search_type
        session.search_value_item=request.vars.search_value

        reqPage=0
    elif btn_all:
        session.btn_filter_item=None
        session.search_type_item=None
        session.search_value_item=None
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
    qset=qset(db.sm_item_batch.cid==cid)
    
    if (session.btn_filter_item and session.search_type_item=='ItemID'):
        searchValue=str(session.search_value_item).split('|')[0]        
        qset=qset(db.sm_item_batch.item_id==searchValue.upper())
        
    elif (session.btn_filter_item and session.search_type_item=='BatchID'):
        qset=qset(db.sm_item_batch.batch_id==session.search_value_item.upper())
        
    elif (session.btn_filter_item and session.search_type_item=='ExpiaryDate'):
        qset=qset(db.sm_item_batch.expiary_date==session.search_value_item.upper())
        
    records=qset.select(db.sm_item_batch.ALL,orderby=db.sm_item_batch.name,limitby=limitby)
    totalCount=qset.count()
    
    #----------------- filter end
    return dict(form=form,records=records,totalCount=totalCount,page=page,items_per_page=items_per_page,access_permission=access_permission)

#============================================== Download
def download_item_batch():
    #Check access permission
    #----------Task assaign----------
    task_id='rm_item_batch_manage'
    task_id_view='rm_item_batch_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))
    
    
    cid=session.cid
    records=''
    #Create query based on search type
    qset=db()
    qset=qset(db.sm_item_batch.cid==cid)
    
    if (session.btn_filter_item and session.search_type_item=='ItemID'):
        searchValue=str(session.search_value_item).split('|')[0]        
        qset=qset(db.sm_item_batch.item_id==searchValue.upper())
        
    elif (session.btn_filter_item and session.search_type_item=='BatchID'):
        qset=qset(db.sm_item_batch.batch_id==session.search_value_item.upper())
        
    elif (session.btn_filter_item and session.search_type_item=='ExpiaryDate'):
        qset=qset(db.sm_item_batch.expiary_date==session.search_value_item.upper())
        
    records=qset.select(db.sm_item_batch.ALL,orderby=db.sm_item_batch.name)
    
    #Create string for download as excel file
    myString='Item Batch List\n'
    myString+='Item ID,Name,Batch ID,Expiry Date\n'
    #Replace coma from records. cause coma means new Column    
    for rec in records:
        item_id=rec.item_id
        name=str(rec.name).replace(',', ' ')
        batch_id=str(rec.batch_id)
        expiary_date=str(rec.expiary_date)
        
        myString+=str(item_id)+','+str(name)+',`'+str(batch_id)+','+str(expiary_date)+'\n'
        
    #-----------
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_item_batch.csv'   
    return str(myString)
    
#====================================== BATCH UPLOAD
def itembatch_batch_upload():
    response.title='Item Batch - Batch upload'
    
    #----------Task assaign----------
    task_id='rm_item_batch_manage'
    access_permission=check_role(task_id)
    if access_permission==False:
        session.flash='Access is Denied !'
        redirect (URL('item','item'))
    
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
        
        item_id_list_excel=[]
        item_id_list_exist=[]
        
        unit_list=[]
        
        ins_list=[]
        ins_dict={}
        
        #---------- rep area
        for i in range(total_row):
            if i>=100:
                break
            else:
                row_data=row_list[i]                    
                coloum_list=row_data.split( '\t')
                if len(coloum_list)==3:
                    item_id_list_excel.append(coloum_list[0])
                    
        #Create list based on excel sheet which items are already exist in database
        existRows=db((db.sm_item.cid==c_id)&(db.sm_item.item_id.belongs(item_id_list_excel))).select(db.sm_item.item_id,db.sm_item.name,orderby=db.sm_item.item_id)
        item_id_list_exist=existRows.as_list()
        
        # main loop   
        for i in range(total_row):
            if i>=100: 
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
                item_id=str(coloum_list[0]).strip().upper()
                batch_id=str(coloum_list[1]).strip().upper()
                expiaryDate=str(coloum_list[2]).strip()
                
                if item_id=='' or batch_id=='' or expiaryDate=='':
                    error_data=row_data+'(Required all value)\n'
                    error_str=error_str+error_data
                    count_error+=1
                    continue
                else:
                    #-------------------
                    dateFlag=True
                    try:
                        expiary_date=datetime.datetime.strptime(expiaryDate,'%Y-%m-%d')
                    except:
                        dateFlag=False
                        
                    #----------------
                    valid_item=False
                    itemName=''
                    #Check valid category                                            
                    for i in range(len(item_id_list_exist)):
                        myRowData=item_id_list_exist[i]                                
                        itemId=myRowData['item_id']
                        if (str(itemId).strip()==str(item_id).strip()):
                            valid_item=True
                            itemName=myRowData['name']
                            break
                    
                    #-----------------
                    if valid_item==False:
                        error_data=row_data+'(Invalid Item!)\n'
                        error_str=error_str+error_data
                        count_error+=1
                        continue
                    else:
                        if dateFlag==False:
                            error_data=row_data+'(Invalid Expiry Date)\n'
                            error_str=error_str+error_data
                            count_error+=1
                            continue
                        else:                            
                            existBatchRows=db((db.sm_item_batch.cid==c_id)&(db.sm_item_batch.item_id==item_id)&(db.sm_item_batch.batch_id==batch_id)).select(db.sm_item_batch.id,limitby=(0,1))
                            if existBatchRows:
                                error_data=row_data+'(Already exist the item ID with same batchID)\n'
                                error_str=error_str+error_data
                                count_error+=1
                                continue
                            else:                                
#                                 try:
                                    db.sm_item_batch.insert(cid=c_id,item_id=item_id,name=itemName,batch_id=batch_id,expiary_date=expiary_date)
                                    
                                    # insert into store for stock
                                    insertRecords="insert into sm_depot_stock_balance(cid,depot_id,store_id,store_name,item_id,batch_id,expiary_date,quantity)(select cid,depot_id,store_id,store_name,'"+str(item_id)+"','"+str(batch_id)+"','"+str(expiary_date)+"',0 from sm_depot_store where cid='"+c_id+"')"
                                    db.executesql(insertRecords)
                                    
                                    count_inserted+=1
#                                 except:
#                                     error_data=row_data+'(error in process!)\n'
#                                     error_str=error_str+error_data
#                                     count_error+=1
#                                     continue
        
        if error_str=='':
            error_str='No error'
            
    return dict(count_inserted=count_inserted,count_error=count_error,error_str=error_str,total_row=total_row)

#------------------ end----------------------
#============================================

#Validation for item

def temp_item_validation(form):    
    cid=session.cid
    
    item_id=str(request.vars.item_id).strip().upper()
    item_name_row=str(request.vars.name)
    item_name=check_special_char(item_name_row)#Check spacial char
    #dist_price=request.vars.dist_price
    
    try:
        item_carton=int(request.vars.item_carton)
    except:
        item_carton=0
        
    price=request.vars.price
    vat_amt=request.vars.vat_amt
    
    category_id=request.vars.category_id
    category_id_sp=request.vars.category_id_sp
    
    rows_check=db((db.sm_item_temp.cid==cid) & (db.sm_item_temp.item_id==item_id)).select(db.sm_item_temp.item_id,limitby=(0,1))
    if rows_check:
        form.errors.item_id=''
        response.flash = 'Item ID already exist'
    else:
        if category_id== category_id_sp:
            category_id_sp=''
#             form.errors.category_id_sp='Primary and Special Category can not be same'
#         else:
#             catFlag=True
#             if category_id=='C' and category_id_sp=='':
#                 catFlag=False
#             
#             if catFlag==False:
#                 form.errors.category_id_sp='Required special category for Primary category "C" '
#             else:
#                 if category_id!='C' and category_id_sp!='':
#                     form.errors.category_id_sp='Required special category empty except for Primary Category "C" '
#                 else:
        if price < 0 :
            form.errors.price='Enter M.R.P accurately'
        else:
            if vat_amt < 0 :
                form.errors.vat_amt='Enter VAT accurately'
            else:
                total_amt=round(float(price)+float(vat_amt),2) #TP+VAT
                
                form.vars.item_id=item_id
                form.vars.name=item_name
                form.vars.total_amt=total_amt
                form.vars.item_carton=item_carton
                form.vars.category_id=category_id
                form.vars.category_id_sp=category_id_sp

def validation_temp_item_process(formProcess):    
    cid=session.cid
    
    schedule_date=formProcess.vars.schedule_date
    
    pending_rows_check=db((db.sm_item_process_schedule.cid==cid) & (db.sm_item_process_schedule.process_flag!=1)).select(db.sm_item_process_schedule.id,limitby=(0,1))
    if pending_rows_check:
        formProcess.errors.schedule_date=''
        response.flash='Pending schedule exist'
    else:
        rows_check=db((db.sm_item_process_schedule.cid==cid) & (db.sm_item_process_schedule.schedule_date==schedule_date) & (db.sm_item_process_schedule.process_flag!=1)).select(db.sm_item_process_schedule.id,limitby=(0,1))
        if rows_check:
            formProcess.errors.schedule_date='Schedule already exist '
        else:
            rows_check2=db((db.sm_item_process_schedule.cid==cid) & (db.sm_item_process_schedule.schedule_date>schedule_date)).select(db.sm_item_process_schedule.id,limitby=(0,1))
            if rows_check2:
                formProcess.errors.schedule_date=''
                response.flash='Previous schedule not allowed'
            else:
                currentDate=datetime.datetime.strptime(str(current_date),'%Y-%m-%d')
                scheduleDate=datetime.datetime.strptime(str(schedule_date),'%Y-%m-%d')
                if scheduleDate<currentDate:
                    formProcess.errors.schedule_date=''
                    response.flash='Previous date not allowed'
                else:
                    pass

def temp_item():
    task_id='rm_item_manage'
    task_id_view='rm_item_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))
    
    response.title='Item Change Schedule'
    
    cid=session.cid
    
    #------------------------- Data clean
    btn_clean=request.vars.btn_clean
    if btn_clean:
        cmb_clean=str(request.vars.cmb_clean).strip()
        
        if cmb_clean!='YES':
            response.flash='Required Confirmation'
        else:
            db.sm_item_temp.truncate()
            db(db.sm_company_settings.cid==cid).update(temp_item_list='')
            db((db.sm_item_process_schedule.cid==cid)&(db.sm_item_process_schedule.process_flag==2)).update(process_flag=0,item_list_str='')
            
            response.flash='Item Change Schedule - Item cleaned successfully'
    
    #-----------------------
    
    # Set combo for catagory and unit
    db.sm_item_temp.category_id.requires=IS_IN_DB(db((db.sm_category_type.cid == cid)&(db.sm_category_type.type_name=='ITEM_CATEGORY')),db.sm_category_type.cat_type_id,error_message='Select a value',orderby=db.sm_category_type.cat_type_id)
    db.sm_item_temp.category_id_sp.requires=IS_EMPTY_OR(IS_IN_DB(db((db.sm_category_type.cid == cid)&(db.sm_category_type.type_name=='ITEM_CATEGORY')),db.sm_category_type.cat_type_id,orderby=db.sm_category_type.cat_type_id))
    db.sm_item_temp.unit_type.requires=IS_IN_DB(db((db.sm_category_type.cid == session.cid)&(db.sm_category_type.type_name=='ITEM_UNIT')),db.sm_category_type.cat_type_id,error_message='Select a value',orderby=db.sm_category_type.cat_type_id)
    
    form =SQLFORM(db.sm_item_temp,
                  fields=['item_id','name','des','category_id','category_id_sp','unit_type','manufacturer','item_carton','price','vat_amt'],       
                  submit_button='Save'
                  )
    
    #Insert with validation
    if form.accepts(request.vars,session,onvalidation=temp_item_validation):
        
        #Select item string from company settings 
        item_id=","+str(form.vars.item_id).strip().upper()+","
        try:
            settings_records=db(db.sm_company_settings.cid==cid).select(db.sm_company_settings.id,db.sm_company_settings.temp_item_list)
            item_list=settings_records[0].temp_item_list
            if item_list==None:
                item_list=''
            
            #If item is not in item string then update string with new item id                    
            itemListStr=str(item_list).strip() 
            if (itemListStr.find(item_id)== (-1)):
                if itemListStr=='':
                    itemListStr=item_id
                else:
                    itemListStr=itemListStr+item_id
                
                #replace double com from string    
                itemListStr=itemListStr.replace(",,",",")
                settings_records[0].update_record(temp_item_list=itemListStr)
                response.flash = 'Saved successfully'
            else:
                db.rollback()
                response.flash = 'ItemID already exist!'
        except:
            db.rollback()
            response.flash = 'Process error!'
            
    #  Set text for filter
    btn_filter_item=request.vars.btn_filter_item
    btn_all=request.vars.btn_all
    reqPage=len(request.args)
    
    if btn_filter_item:
        session.btn_filter_item=btn_filter_item
        session.search_type_item=request.vars.search_type
        session.search_value_item=request.vars.search_value

        reqPage=0
    elif btn_all:
        session.btn_filter_item=None
        session.search_type_item=None
        session.search_value_item=None
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
    qset=qset(db.sm_item_temp.cid==cid)
    
    if (session.btn_filter_item and session.search_type_item=='ItemID'):
        searchValue=str(session.search_value_item).split('|')[0]        
        qset=qset(db.sm_item_temp.item_id==searchValue.upper())
        
    elif (session.btn_filter_item and session.search_type_item=='Catagory'):
        qset=qset(db.sm_item_temp.category_id==session.search_value_item.upper())
        
    elif (session.btn_filter_item and session.search_type_item=='Unit'):
        qset=qset(db.sm_item_temp.unit_type==session.search_value_item.upper())
        
    records=qset.select(db.sm_item_temp.ALL,orderby=db.sm_item_temp.name,limitby=limitby)
    totalCount=qset.count()
    
    #------------------------- Delete process
    btn_delete_process=request.vars.btn_delete_process
    if btn_delete_process:
        pRowId=str(request.vars.pRowId).strip()
        
        if pRowId=='':
            response.flash='Invalid request'
        else:            
            db((db.sm_item_process_schedule.cid==cid)&(db.sm_item_process_schedule.id==pRowId)).delete()
            response.flash='Process request deleted successfully'
    
    #-----------------------
    
    #================= Process Schedule part
    formProcess =SQLFORM(db.sm_item_process_schedule,
                  fields=['schedule_date'],       
                  submit_button='Submit'
                  )    
    #Insert with validation
    if formProcess.accepts(request.vars,session,onvalidation=validation_temp_item_process):
        response.flash = 'Process request submitted successfully'
        
    processRows=db(db.sm_item_process_schedule.cid==cid).select(db.sm_item_process_schedule.ALL,orderby=~db.sm_item_process_schedule.id)
    
    #----------------- filter end
    return dict(form=form,records=records,formProcess=formProcess,processRows=processRows,totalCount=totalCount,page=page,items_per_page=items_per_page,access_permission=access_permission)
    

#Validation for item edit
def temp_item_edit_validation(form):
    #dist_price=request.vars.dist_price
    
    item_name_row=str(request.vars.name)
    item_name=check_special_char(item_name_row)
    try:
        item_carton=int(request.vars.item_carton)
    except:
        item_carton=0
    
    price=request.vars.price
    vat_amt=request.vars.vat_amt
    
    category_id=request.vars.category_id
    category_id_sp=request.vars.category_id_sp
    if category_id== category_id_sp:
        category_id_sp=''
#         form.errors.category_id_sp='Primary and Special Category can not be same'
#     else:
#         catFlag=True
#         if category_id=='C' and category_id_sp=='':
#             catFlag=False
#             
#         if catFlag==False:
#             form.errors.category_id_sp='Required special category for Primary category "C" '
#         else:
#             if category_id!='C' and category_id_sp!='':
#                 form.errors.category_id_sp='Required special category empty except for Primary Category "C" '
#             else:                
    if price < 0 :
        form.errors.price='Enter M.R.P accurately'
    else:
        if vat_amt < 0 :
            form.errors.vat_amt='Enter VAT accurately'
        else:
            total_amt=round(float(price)+float(vat_amt),2) #TP+VAT
            
            form.vars.name=item_name
            form.vars.total_amt=total_amt
            form.vars.item_carton=item_carton
            form.vars.category_id=category_id
            form.vars.category_id_sp=category_id_sp
def temp_item_edit():
    task_id='rm_item_manage'
    access_permission=check_role(task_id)
    if (access_permission==False):
        session.flash='Access is Denied !'
        redirect (URL('item','temp_item'))
    
    cid=session.cid
    #Set combos for unit and catagory    
    response.title='Item Change Schedule - Edit'

    db.sm_item_temp.category_id.requires=IS_IN_DB(db((db.sm_category_type.cid == cid)&(db.sm_category_type.type_name=='ITEM_CATEGORY')),db.sm_category_type.cat_type_id,error_message='Select a value',orderby=db.sm_category_type.cat_type_id)
    db.sm_item_temp.category_id_sp.requires=IS_EMPTY_OR(IS_IN_DB(db((db.sm_category_type.cid == cid)&(db.sm_category_type.type_name=='ITEM_CATEGORY')),db.sm_category_type.cat_type_id,orderby=db.sm_category_type.cat_type_id))
    db.sm_item_temp.unit_type.requires=IS_IN_DB(db((db.sm_category_type.cid == cid)&(db.sm_category_type.type_name=='ITEM_UNIT')),db.sm_category_type.cat_type_id,error_message='Select a value',orderby=db.sm_category_type.cat_type_id)
    
    page=request.args(0)
    record= db.sm_item_temp(request.args(1)) #or redirect(URL('index'))  
     
    form =SQLFORM(db.sm_item_temp,
                  record=record,
                  deletable=True,
                  linkto=None,
                  upload=None,
                  fields=['name','des','category_id','category_id_sp','unit_type','manufacturer','item_carton','price','vat_amt'],
                  submit_button='Update'
                  )
    
    records_item=db((db.sm_item_temp.cid==session.cid) & (db.sm_item_temp.id==request.args(1))).select(db.sm_item_temp.item_id,limitby=(0,1))
    item_id=''
    for records_show_id in records_item :
         item_id=records_show_id.item_id     
         break
    #Edit item with validation 
    if form.accepts(request.vars,session,onvalidation=temp_item_edit_validation):
        #Catch delete variable.Selectitem string from company settings table 
        if form.vars.get('delete_this_record', False):
            settings_records=db(db.sm_company_settings.cid==cid).select(db.sm_company_settings.id,db.sm_company_settings.temp_item_list,limitby=(0,1))
            item_list=settings_records[0].temp_item_list
            if item_list==None:
                item_list=''
            
            itemListStr=str(item_list).strip() 
            
            item_id=','+str(item_id).strip()+','
            #Replace item as blank,replace double coma 
            if (itemListStr.find(item_id)!= (-1)):
                itemListStr=itemListStr.replace(item_id,",")
                
                itemListStr=itemListStr.replace(",,",",")
                settings_records[0].update_record(temp_item_list=itemListStr)
                
            #---------
        session.flash = 'Updated Successfully'
        redirect(URL(c='item',f='temp_item',args=[page]))

    return dict(form=form,item_id=item_id,page=page)


#====================================== BATCH UPLOAD 
def temp_item_batch_upload():
    task_id='rm_item_manage'
    access_permission=check_role(task_id)
#    access_permission_view=check_role(task_id_view)
    if access_permission==False:
        session.flash='Access is Denied !'
        redirect (URL('item','temp_item'))
    
    response.title='Item Change Schedule - Batch upload'
    
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
        
        item_id_list_excel=[]
        item_id_list_exist=[]
        category_list_exist=[]
        
        unit_list=[]
        
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
                if len(coloum_list)==10:
                    item_id_list_excel.append(coloum_list[0])
        
        
        #Create list based on excel sheet which items are already exist in database
        existRows=db((db.sm_item_temp.cid==c_id)&(db.sm_item_temp.item_id.belongs(item_id_list_excel))).select(db.sm_item_temp.item_id,orderby=db.sm_item_temp.item_id)
        item_id_list_exist=existRows.as_list()
        
        #Check valid category list based on excel sheet
        catRows=db((db.sm_category_type.cid==c_id)& (db.sm_category_type.type_name=='ITEM_CATEGORY')).select(db.sm_category_type.cat_type_id,orderby=db.sm_category_type.cat_type_id)
        category_list_exist=catRows.as_list()
        
        #Check valid unit list based on excel sheet
        unitRows=db((db.sm_category_type.cid==c_id)& (db.sm_category_type.type_name=='ITEM_UNIT')).select(db.sm_category_type.cat_type_id,orderby=db.sm_category_type.cat_type_id)
        unit_list=unitRows.as_list()
        
        #Select item string sm_company_settings
        settings_records=db(db.sm_company_settings.cid==session.cid).select(db.sm_company_settings.id,db.sm_company_settings.temp_item_list,limitby=(0,1))
        item_list=settings_records[0].temp_item_list
        if item_list==None:
            item_list=''        
        itemListStr=str(item_list).strip()
        
        # main loop   
        for i in range(total_row):
            if i>=500: 
                break
            else:
                row_data=row_list[i]
            coloum_list=row_data.split( '\t')            
            # return len(coloum_list)
            if len(coloum_list)==10:
                item_id=str(coloum_list[0]).strip().upper()
                name=str(coloum_list[1]).strip()
                name=check_special_char(name)#Check spacial char
                
                des=str(coloum_list[2]).strip()
                category_id=str(coloum_list[3]).strip().upper()
                category_id_sp=str(coloum_list[4]).strip().upper()#special category
                unit_type=str(coloum_list[5]).strip()
                manufacturer=str(coloum_list[6]).strip()
                mCarton=str(coloum_list[7]).strip()
                price=str(coloum_list[8]).strip()  #Distributor Price
                vat_amt=str(coloum_list[9]).strip()       #Retailer Price
                
                if des=='':
                    des='-'
                    
                if manufacturer=='':
                    manufacturer='-'
                    
                try:
                    mCarton=int(mCarton)                    
                except:
                    mCarton=0
                    
                #------------------
                if price=='':
                    price=0.0
                    
                if vat_amt=='':
                    vat_amt=0.0
                #-------------------
                total_amt=0
                try:
                    price=float(price)
                    vat_amt=float(vat_amt)
                    total_amt=round(price+vat_amt,2)
                except:
                    price=0
                    vat_amt=0
                    
                try:                    
                    if item_id=='' or name=='' or category_id=='' or unit_type=='':
                        error_data=row_data+'(Required value can not empty)\n'
                        error_str=error_str+error_data
                        count_error+=1
                        continue
                    else:
                        if category_id==category_id_sp:
                            category_id_sp=''
                            
                        valid_category=False
                        valid_unit=False
                        duplicate_item=False                        
                        valid_category_sp=False
                        duplicate_category_sp=False
                        
                        #Check valid category                          
                        for i in range(len(category_list_exist)):
                            myRowData=category_list_exist[i]                                
                            cat_id=myRowData['cat_type_id']
                            if (str(cat_id).strip()==str(category_id).strip()):
                                valid_category=True
                                break
                        
                        if valid_category==True:
                            if category_id==category_id_sp:
                                duplicate_category_sp=True
                            else:
                                if category_id_sp!='':                                    
                                    #Check valid category                          
                                    for i in range(len(category_list_exist)):
                                        myRowData=category_list_exist[i]                                
                                        cat_id_sp=myRowData['cat_type_id']
                                        if (str(cat_id_sp).strip()==str(category_id_sp).strip()):
                                            valid_category_sp=True
                                            break
                                
                                elif category_id_sp=='':                                    
                                    valid_category_sp=True
                        
                        if valid_category==True and valid_category_sp==True: # check unit type                                                         
                            for i in range(len(unit_list)):
                                myRowData=unit_list[i]                                
                                u_type=myRowData['cat_type_id']
                                if (str(u_type).strip()==str(unit_type).strip()):
                                    valid_unit=True
                                    break
                        
                        if valid_unit==True:# check duplicate item                                                     
                            for i in range(len(item_id_list_exist)):
                                myRowData=item_id_list_exist[i]                                
                                itemId=myRowData['item_id']
                                if (str(itemId).strip()==str(item_id).strip()):
                                    duplicate_item=True                                 
                                    break
                        
                        #-----------------
                        if valid_category==False:
                            error_data=row_data+'(Invalid Primary Category!)\n'
                            error_str=error_str+error_data
                            count_error+=1
                            continue
                        else:
                            if duplicate_category_sp==True:
                                error_data=row_data+'(Primary Category and Special Category can not be same!)\n'
                                error_str=error_str+error_data
                                count_error+=1
                                continue
                            else:
                                if valid_category_sp==False:
                                    error_data=row_data+'(Required empty or valid special category according to Primary category!)\n'
                                    error_str=error_str+error_data
                                    count_error+=1
                                    continue
                                else:
                                    if valid_unit==False:
                                        error_data=row_data+'(Invalid Unit Type)\n'
                                        error_str=error_str+error_data
                                        count_error+=1
                                        continue
                                    else:
                                        if duplicate_item==True:
                                            error_data=row_data+'(Duplicate Item)\n'
                                            error_str=error_str+error_data
                                            count_error+=1
                                            continue
                                        else:
                                            if price<0 or vat_amt<0:
                                                error_data=row_data+'(Valid TP/VAT Required)\n'
                                                error_str=error_str+error_data
                                                count_error+=1
                                                continue
                                            else:
                                                
                                                #Add item in item string
                                                temp_item=","+item_id+","                                                    
                                                if (itemListStr.find(temp_item)== (-1)):
                                                    if itemListStr=='':
                                                        itemListStr=temp_item
                                                    else:
                                                        itemListStr=itemListStr+temp_item
                                                    
                                                    #Create dictionary for bulk insert                                        
                                                    ins_dict= {'cid':c_id,'item_id':item_id,'name':name,'des':des,'category_id':category_id,'category_id_sp':category_id_sp,'unit_type':unit_type,'manufacturer':manufacturer,'item_carton':mCarton,'price':price,'vat_amt':vat_amt,'total_amt':total_amt}
                                                    ins_list.append(ins_dict)                               
                                                    count_inserted+=1
                                                    
                                                else:
                                                    error_data=row_data+'(already exist in item list)\n'
                                                    error_str=error_str+error_data
                                                    count_error+=1
                                                    continue                                            
                
                except:
                    error_data=row_data+'(error in process!)\n'
                    error_str=error_str+error_data
                    count_error+=1
                    continue
            else:
                error_data=row_data+'(10 columns need in a row)\n'
                error_str=error_str+error_data
                count_error+=1
                continue
        
        if error_str=='':
            error_str='No error'
        
        if len(ins_list) > 0:
            #Bulk insert
            #Replace double com
            #Update item string in company settings table
            inCountList=db.sm_item_temp.bulk_insert(ins_list)
            itemListStr=itemListStr.replace(",,",",")
            settings_records[0].update_record(temp_item_list=itemListStr)
            
    return dict(count_inserted=count_inserted,count_error=count_error,error_str=error_str,total_row=total_row)

#------------------ end----------------------

#============================================== Download
def temp_download_item():
    #Check access permission
    #----------Task assaign----------
    task_id='rm_item_manage'
    task_id_view='rm_item_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))
    
    
    cid=session.cid
    records=''
    #Create query based on search type
    qset=db()
    qset=qset(db.sm_item_temp.cid==cid)
    
    if (session.btn_filter_item and session.search_type_item=='ItemID'):
        searchValue=str(session.search_value_item).split('|')[0]        
        qset=qset(db.sm_item_temp.item_id==searchValue.upper())
        
    elif (session.btn_filter_item and session.search_type_item=='Catagory'):
        qset=qset(db.sm_item_temp.category_id==session.search_value_item.upper())
        
    elif (session.btn_filter_item and session.search_type_item=='Unit'):
        qset=qset(db.sm_item_temp.unit_type==session.search_value_item.upper())
        
    records=qset.select(db.sm_item_temp.ALL,orderby=db.sm_item_temp.name)
    
    #Create string for download as excel file
    myString='Item Change Schedule List\n'
    myString+='Item ID,Name,Description,Group/Category,Base Group/Category,Unit Type,Manufacturer,M.Carton,TP Amount,VAT Amount,Total Amount\n'
    #Replace coma from records. cause coma means new Column    
    for rec in records:
        item_id=rec.item_id
        name=str(rec.name).replace(',', ' ')
        des=str(rec.des).replace(',', ' ')
        category_id=rec.category_id
        category_id_sp=rec.category_id_sp
        unit_type=rec.unit_type
        manufacturer=str(rec.manufacturer).replace(',', ' ')
        item_carton=rec.item_carton
        price=rec.price
        vat_amt=rec.vat_amt        
        total_amt=rec.total_amt
        
        if category_id_sp==None:
            category_id_sp=''
        myString+=str(item_id)+','+str(name)+','+str(des)+','+str(category_id)+','+str(category_id_sp)+','+str(unit_type)+','+str(manufacturer)+','+str(item_carton)+','+str(price)+','+str(vat_amt)+','+str(total_amt)+'\n'
        
    #-----------
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_temp_item.csv'   
    return str(myString)


#http://127.0.0.1:8000/mrepskf/item/process_change_item_manual?process_date=2016-02-13
def process_change_item_manual():
    cid=session.cid
    process_date=request.vars.process_date
    
    try:
        currentDate=datetime.datetime.strptime(str(process_date),'%Y-%m-%d').strftime('%Y-%m-%d')
    except:        
        session.flash='Invalid request'
        redirect (URL('temp_item'))
    
    #----------------------------------
    processRecords=db((db.sm_item_process_schedule.cid==cid)&(db.sm_item_process_schedule.process_flag==0)&(db.sm_item_process_schedule.schedule_date==currentDate)).select(db.sm_item_process_schedule.ALL,orderby=db.sm_item_process_schedule.schedule_date,limitby=(0,1))
    if not processRecords:
        session.flash='Process not available'
        redirect (URL('temp_item'))
    else:        
        processRecords[0].update_record(process_flag=2,note='process running...')
        #---------        
        db.sm_item.truncate()
        #itemTransfer="insert into sm_item select * from sm_item_temp where sm_item_temp.cid='"+cid+"'"
        itemTransfer="insert into sm_item(cid,item_id,name,des,category_id,category_id_sp,unit_type,manufacturer,item_carton,price,dist_price,vat_amt,total_amt,status,field1,field2,note,created_on,created_by,updated_on,updated_by) (select cid,item_id,name,des,category_id,category_id_sp,unit_type,manufacturer,item_carton,price,dist_price,vat_amt,total_amt,'ACTIVE',field1,field2,note,created_on,created_by,updated_on,updated_by from sm_item_temp where sm_item_temp.cid='"+cid+"')" 
        db.executesql(itemTransfer)
        
        itemIdListUpdate="update sm_company_settings set item_list=temp_item_list where cid='"+cid+"'"
        db.executesql(itemIdListUpdate)
        
        time.sleep(1)
        
        #----------------- Save in download formate
        records=db(db.sm_item.cid==cid).select(db.sm_item.ALL,orderby=db.sm_item.name)        
        myString='Item List\n'
        myString+='Process Date:'+str(currentDate)+'\n'
        
        myString+='Item ID,Name,Description,Group/Category,Base Group/Category,Unit Type,Manufacturer,M.Carton,TP Amount,VAT Amount,Total Amount\n'
        for rec in records:
            item_id=rec.item_id
            name=str(rec.name).replace(',', ' ')
            des=str(rec.des).replace(',', ' ')
            category_id=rec.category_id
            category_id_sp=rec.category_id_sp
            unit_type=rec.unit_type
            manufacturer=str(rec.manufacturer).replace(',', ' ')
            item_carton=rec.item_carton
            price=rec.price
            vat_amt=rec.vat_amt        
            total_amt=rec.total_amt
            
            if category_id_sp==None:
                category_id_sp=''
            myString+=str(item_id)+','+str(name)+','+str(des)+','+str(category_id)+','+str(category_id_sp)+','+str(unit_type)+','+str(manufacturer)+','+str(item_carton)+','+str(price)+','+str(vat_amt)+','+str(total_amt)+'\n'
            
        #This function is exist in common_fn in model
        set_product_list(cid)
        
        #------------
        processRecords[0].update_record(process_flag=1,item_list_str=myString,note='Successfully processed')
        db.commit()
    
    session.flash='Processed successfully'
    redirect (URL('temp_item'))
    

#Cron
#http://127.0.0.1:8000/mrepskf/item/process_change_item
def process_change_item():
    
    currentDate=current_date
    
    #----------------------------------
    processRecords=db((db.sm_item_process_schedule.process_flag==0)&(db.sm_item_process_schedule.schedule_date==currentDate)).select(db.sm_item_process_schedule.ALL,orderby=db.sm_item_process_schedule.schedule_date,limitby=(0,1))
    if not processRecords:
        return 'Process Not available'
    else:
        cid=str(processRecords[0].cid)
        
        processRecords[0].update_record(process_flag=2,note='process running...')
        #---------        
        db.sm_item.truncate()
        
        #itemTransfer="insert into sm_item select * from sm_item_temp where sm_item_temp.cid='"+cid+"'"
        itemTransfer="insert into sm_item(cid,item_id,name,des,category_id,category_id_sp,unit_type,manufacturer,item_carton,price,dist_price,vat_amt,total_amt,field1,field2,note,created_on,created_by,updated_on,updated_by) (select cid,item_id,name,des,category_id,category_id_sp,unit_type,manufacturer,item_carton,price,dist_price,vat_amt,total_amt,field1,field2,note,created_on,created_by,updated_on,updated_by from sm_item_temp where sm_item_temp.cid='"+cid+"')" 
        db.executesql(itemTransfer)
        
        itemIdListUpdate="update sm_company_settings set item_list=temp_item_list where cid='"+cid+"'"
        db.executesql(itemIdListUpdate)
        
        time.sleep(1)
        
        #----------------- Save in download formate
        records=db(db.sm_item.cid==cid).select(db.sm_item.ALL,orderby=db.sm_item.name)        
        myString='Item List\n'
        myString+='Process Date:'+str(currentDate)+'\n'
        
        myString+='Item ID,Name,Description,Group/Category,Base Group/Category,Unit Type,Manufacturer,M.Carton,TP Amount,VAT Amount,Total Amount\n'
        for rec in records:
            item_id=rec.item_id
            name=str(rec.name).replace(',', ' ')
            des=str(rec.des).replace(',', ' ')
            category_id=rec.category_id
            category_id_sp=rec.category_id_sp
            unit_type=rec.unit_type
            manufacturer=str(rec.manufacturer).replace(',', ' ')
            item_carton=rec.item_carton
            price=rec.price
            vat_amt=rec.vat_amt        
            total_amt=rec.total_amt
            
            if category_id_sp==None:
                category_id_sp=''
            myString+=str(item_id)+','+str(name)+','+str(des)+','+str(category_id)+','+str(category_id_sp)+','+str(unit_type)+','+str(manufacturer)+','+str(item_carton)+','+str(price)+','+str(vat_amt)+','+str(total_amt)+'\n'
            
        #This function is exist in common_fn in model not used
        #set_product_list(cid)
        
        #------------
        processRecords[0].update_record(process_flag=1,item_list_str=myString,note='Successfully processed',updated_by='SYSTEM')
        db.commit()
        
    return 'Done'


#============================================== Download into csv
def download_process_item():
    #----------Task assaign----------
    task_id='rm_item_manage'
    task_id_view='rm_item_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))
        
    cid=session.cid
    myString=''
    pRowId=str(request.vars.pRowId).strip()        
    if pRowId=='':
        response.flash='Invalid request'
    else:    
        processRecords=db(db.sm_item_process_schedule.id==pRowId).select(db.sm_item_process_schedule.item_list_str,limitby=(0,1))
        if not processRecords:
            response.flash='Data Not available'
        else:        
            myString=str(processRecords[0].item_list_str)
    
    
    #-----------
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_temp_item.csv'   
    return str(myString)    
    #-----------
