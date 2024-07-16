
#Validation for depot
def depot_store_add_validation(form):
    c_id=session.cid
    depot_id=str(request.vars.depot_id).strip().upper().split('|')[0]
    store_id=str(request.vars.store_id).strip().upper()
    
    store_name=str(request.vars.store_name).strip()
    store_name=check_special_char(store_name)
    store_name=store_name.title()
    
    rows_check=db((db.sm_depot.cid==c_id) & (db.sm_depot.depot_id==depot_id)).select(db.sm_depot.depot_id,limitby=(0,1))
    if not rows_check:
        form.errors.depot_id=''
        response.flash = 'Invalid Depot Id'
    else:
        rows_check2=db((db.sm_depot_store.cid==c_id) & (db.sm_depot_store.depot_id==depot_id) & (db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.depot_id,limitby=(0,1))
        if rows_check2:
            form.errors.depot_id=''
            response.flash = 'Already exist'
        else:
            form.vars.depot_id=depot_id
            form.vars.store_id=store_id
            form.vars.store_name=store_name
            
def depot_store_add():
    task_id='rm_depot_manage'
    task_id_view='rm_depot_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))
    # ---------------------
    response.title='Branch Store'
    
    c_id=session.cid
    
    form =SQLFORM(db.sm_depot_store,
                  fields=['depot_id','store_id','store_name','store_type'],
                  submit_button='Save'          
                  )
    
    #Insert with validation
    if form.accepts(request.vars,session,onvalidation=depot_store_add_validation):        
        depot_id=form.vars.depot_id
        store_id=form.vars.store_id
        store_name=form.vars.store_name
        
        insertRecords="insert into sm_depot_stock_balance(cid,depot_id,store_id,store_name,item_id,batch_id,expiary_date,quantity)(select cid,'"+str(depot_id)+"','"+str(store_id)+"','"+str(store_name)+"',item_id,batch_id,expiary_date,0 from sm_item_batch where cid='"+c_id+"')"
        db.executesql(insertRecords)
        
        response.flash = 'Saved Successfully'
    
    #  ---------------filter-------    
    btn_filter_depot_store=request.vars.btn_filter_depot_store
    btn_all=request.vars.btn_all
    reqPage=len(request.args)
    
    if btn_filter_depot_store:
        session.search_type_depot_store=request.vars.search_type
        session.search_value_depot_store=str(request.vars.search_value).strip().upper()
        reqPage=0
    elif btn_all:
        session.search_type_depot_store=None
        session.search_value_depot_store=None
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
    qset=qset(db.sm_depot_store.cid==c_id)
    qset=qset(db.sm_depot.cid==c_id)
    qset=qset((db.sm_depot.depot_id==db.sm_depot_store.depot_id))
    
    if (session.search_type_depot_store=='Depot_id'):
        searchValue=str(session.search_value_depot_store).split('|')[0]        
        qset=qset(db.sm_depot_store.depot_id==searchValue)
    elif (session.search_type_depot_store=='TYPE'):
        searchValue=str(session.search_value_depot_store)
        qset=qset(db.sm_depot_store.store_type==searchValue)
    
    
    records=qset.select(db.sm_depot_store.ALL,db.sm_depot.name,db.sm_depot.short_name,orderby=db.sm_depot_store.depot_id,limitby=limitby)
    recordsCount=qset.count()
    
    return dict(form=form,records=records,recordsCount=recordsCount,page=page,items_per_page=items_per_page,access_permission=access_permission,access_permission_view=access_permission_view)


def depot_store_edit_validation(form):
    c_id=session.cid
   
    depot_id=str(form.vars.depot_id).upper().split('|')[0]
    store_name=str(request.vars.store_name).strip()
    store_name=check_special_char(store_name)
    store_name=store_name.title()
    
    form.vars.depot_id=depot_id
    form.vars.store_name=store_name
        
def depot_store_edit():
    task_id='rm_depot_manage'
    access_permission=check_role(task_id)
    if (access_permission==False):
        session.flash='Access is Denied !'
        redirect (URL('depot_store_add'))
    
    response.title='Branch Store'
    #   --------------------- 
    c_id=session.cid
    
    page=request.args(0)
    record= db.sm_depot_store(request.args(1)) or redirect(URL('depot_store_add'))   
    
    form =SQLFORM(db.sm_depot_store,
                  record=record,
                  deletable=True,
                  fields=['depot_id','store_id','store_name'],
                  submit_button='Update'
                  )
    
    if form.accepts(request.vars, session,onvalidation=depot_store_edit_validation):
        if form.vars.get('delete_this_record', False):
            depot_id=form.vars.depot_id
            store_id=form.vars.store_id
            
            balanceRecords=db((db.sm_depot_stock_balance.cid==c_id)&(db.sm_depot_stock_balance.depot_id==depot_id)&(db.sm_depot_stock_balance.store_id==store_id)&(db.sm_depot_stock_balance.quantity>0)).select(db.sm_depot_stock_balance.id,limitby=(0,1))
            if balanceRecords:
                session.flash = 'Already used in Stock'
                db.rollback()
            else:
                issueRow=db((db.sm_issue.cid==c_id)&(db.sm_issue.depot_id==depot_id)&(db.sm_issue.store_id==store_id)&(db.sm_issue.status!='Cancelled')).select(db.sm_issue.id,limitby=(0,1))
                if issueRow:
                    session.flash = 'Already used in Issue'
                    db.rollback()
                else:
                    recRow=db((db.sm_receive.cid==c_id)&(db.sm_receive.depot_id==depot_id)&(db.sm_receive.store_id==store_id)&(db.sm_receive.status!='Cancelled')).select(db.sm_receive.id,limitby=(0,1))
                    if recRow:
                        session.flash = 'Already used in Receive'
                        db.rollback()
                    else:
                        damRow=db((db.sm_damage.cid==c_id)&(db.sm_damage.depot_id==depot_id)&(db.sm_damage.store_id==store_id)&(db.sm_damage.status!='Cancelled')).select(db.sm_damage.id,limitby=(0,1))
                        if damRow:
                            session.flash = 'Already used in Adjustment'
                            db.rollback()
                        else:
                            invRow=db((db.sm_invoice.cid==c_id)&(db.sm_invoice.depot_id==depot_id)&(db.sm_invoice.store_id==store_id)&(db.sm_invoice.status!='Cancelled')).select(db.sm_invoice.id,limitby=(0,1))
                            if invRow:
                                session.flash = 'Already used in Invoice'
                                db.rollback()
                            else:
                                retRow=db((db.sm_return.cid==c_id)&(db.sm_return.depot_id==depot_id)&(db.sm_return.store_id==store_id)&(db.sm_return.status!='Cancelled')).select(db.sm_return.id,limitby=(0,1))
                                if retRow:
                                    session.flash = 'Already used in Return'
                                    db.rollback()
                                else:
                                    db((db.sm_depot_stock_balance.cid==c_id)&(db.sm_depot_stock_balance.depot_id==depot_id)&(db.sm_depot_stock_balance.store_id==store_id)).delete()
                                    session.flash = 'Deleted successfully'
            redirect(URL('depot_store_add',args=[page]))
                                    
        session.flash = 'Updated Successfully'        
        redirect(URL('depot_store_add',args=[page]))
         
    return dict(form=form,page=page)
    

def depot_store_batch_upload():
    task_id='rm_depot_manage'
    access_permission=check_role(task_id)
    if access_permission==False:
        session.flash='Access is Denied !'
        redirect (URL('depot_store','depot_store_add'))
    
    c_id=session.cid
    
    response.title='Branch Store Batch upload'
    
    btn_upload=request.vars.btn_upload
    btn_delete=request.vars.btn_delete
        
    count_inserted=0
    count_error=0
    error_str=''
    total_row=0
    
#     if btn_delete:
#         delete_check=request.vars.delete_check
#         if delete_check!='YES':
#             response.flash='Confirmation Required'            
#         else:            
#             db.sm_depot_store.truncate()          
#             response.flash='ALL Depot Store cleaned successfully'            
#     el
    if btn_upload=='Upload':        
        excel_data=str(request.vars.excel_data)
        inserted_count=0
        error_count=0
        
        row_list=excel_data.split( '\n')
        total_row=len(row_list)
        
        depot_list_exist=[]   
        
        depot_id_list_excel=[]
                
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
                if len(coloum_list)==4:
                    depotIDExcel=str(coloum_list[0]).strip().upper()
                    
                    if depotIDExcel!='':
                        if depotIDExcel not in depot_id_list_excel:
                            depot_id_list_excel.append(depotIDExcel)
                            
        #Check valid depot list based on excel sheet
        depotRows=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id.belongs(depot_id_list_excel))&(db.sm_depot.status=='ACTIVE')).select(db.sm_depot.depot_id,orderby=db.sm_depot.depot_id)
        depot_list_exist=depotRows.as_list()
       
        # main loop   
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
                depot_idExcel=str(coloum_list[0]).strip().upper()
                store_idExcel=str(coloum_list[1]).strip().upper()
                store_nameExcel=str(coloum_list[2]).strip().title()
                store_nameExcel=check_special_char(store_nameExcel)
                
                store_typeExcel=str(coloum_list[3]).strip().upper()
                
                typeList=['SALES','OTHERS']
                #------------------
                if depot_idExcel=='' or store_idExcel=='' or store_nameExcel=='' or store_typeExcel=='':
                    error_data=row_data+'(Required all value)\n'
                    error_str=error_str+error_data
                    count_error+=1
                    continue
                    
                #-------------------                
                
                valid_depot_id=False
                  
                #Check valid depot_list                         
                for i in range(len(depot_list_exist)):
                    myRowData=depot_list_exist[i]                                
                    depot_id=myRowData['depot_id']
                    if (str(depot_id).strip()==str(depot_idExcel).strip()):
                        valid_depot_id=True
                        break
                        
                #-----------------
                if valid_depot_id==False:
                    error_data=row_data+'(Invalid Depot ID)\n'
                    error_str=error_str+error_data
                    count_error+=1
                    continue
                else:
                    if store_typeExcel not in typeList:
                        error_data=row_data+'(Invalid Type)\n'
                        error_str=error_str+error_data
                        count_error+=1
                        continue
                    else:
                        existCheckRows=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_idExcel)&(db.sm_depot_store.store_id==store_idExcel)).select(db.sm_depot_store.id,limitby=(0,1))
                        if existCheckRows:
                            error_data=row_data+'(Duplicate check for Depot Store)\n'
                            error_str=error_str+error_data
                            count_error+=1
                            continue
                        else:
                            
                            try:
                                db.sm_depot_store.insert(cid=c_id,depot_id=depot_idExcel,store_id=store_idExcel,store_name=store_nameExcel,store_type=store_typeExcel)
                                
                                insertRecords="insert into sm_depot_stock_balance(cid,depot_id,store_id,store_name,item_id,batch_id,expiary_date,quantity)(select cid,'"+str(depot_idExcel)+"','"+str(store_idExcel)+"','"+str(store_nameExcel)+"',item_id,batch_id,expiary_date,0 from sm_item_batch where cid='"+c_id+"')"
                                db.executesql(insertRecords)
                                
                                count_inserted+=1
                            except:
                                error_data=row_data+'(error in process!)\n'
                                error_str=error_str+error_data
                                count_error+=1
                                continue
                
        if error_str=='':
            error_str='No error'
    
    return dict(count_inserted=count_inserted,count_error=count_error,error_str=error_str,total_row=total_row)



#===================== Download 
def depot_store_download():
    task_id='rm_depot_manage'
    task_id_view='rm_depot_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))
        
    c_id=session.cid
    records=''
    #Create query based on search type
    qset=db()
    qset=qset(db.sm_depot_store.cid==c_id)
    qset=qset(db.sm_depot.cid==c_id)
    qset=qset((db.sm_depot.depot_id==db.sm_depot_store.depot_id))
    
    if (session.search_type_depot_store=='Depot_id'):
        searchValue=str(session.search_value_depot_store).split('|')[0]        
        qset=qset(db.sm_depot_store.depot_id==searchValue)
    
    records=qset.select(db.sm_depot_store.ALL,db.sm_depot.name,db.sm_depot.short_name,orderby=db.sm_depot_store.depot_id)
    
    #Create string for download as excel file
    myString='Branch Store List\n'
    myString+='Branch ID,Branch Name,Short Name,Store ID,Store Name,Type\n'
    #Replace coma from records. cause coma means new Column    
    for rec in records:
        depot_id=str(rec.sm_depot_store.depot_id)        
        depot_name=str(rec.sm_depot.name)
        short_name=str(rec.sm_depot.short_name)
        store_id=str(rec.sm_depot_store.store_id)
        store_name=str(rec.sm_depot_store.store_name)
        store_type=str(rec.sm_depot_store.store_type)
        
        myString+=str(depot_id)+','+str(depot_name)+','+str(short_name)+',`'+str(store_id)+','+str(store_name)+','+str(store_type)+'\n'
 
    #-----------
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_depot_store.csv'   
    return str(myString)

