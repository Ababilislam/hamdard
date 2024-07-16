
#Validation for depot
def depot_market_add_validation(form):
    c_id=session.cid
    depot_id=str(request.vars.depot_id).strip().upper().split('|')[0]
    market_id=str(request.vars.market_id).strip().upper()
    
    market_name=str(request.vars.market_name).strip().title()
    market_name=check_special_char(market_name)
    
    if session.user_type=='Depot':
        depot_id=session.depot_id
        
    rows_check=db((db.sm_depot.cid==c_id) & (db.sm_depot.depot_id==depot_id)).select(db.sm_depot.depot_id,limitby=(0,1))
    if not rows_check:
        form.errors.depot_id=''
        response.flash = 'Invalid Depot Id'
    else:
        rows_check2=db((db.sm_depot_market.cid==c_id) & (db.sm_depot_market.depot_id==depot_id) & (db.sm_depot_market.market_id==market_id)).select(db.sm_depot_market.depot_id,limitby=(0,1))
        if rows_check2:
            form.errors.depot_id=''
            response.flash = 'Already exist'
        else:
            form.vars.depot_id=depot_id
            form.vars.market_id=market_id
            form.vars.market_name=market_name
            
def depot_market_add():
    task_id='rm_depot_market_manage'
    task_id_view='rm_depot_market_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))
    # ---------------------
    response.title='Branch Market'
    
    c_id=session.cid
    
    form =SQLFORM(db.sm_depot_market,
                  fields=['depot_id','market_id','market_name'],
                  submit_button='Save'          
                  )
    
    if session.user_type=='Depot':
        form.vars.depot_id=str(session.depot_id)+'|'+str(session.user_depot_name)
        
    #Insert with validation
    if form.accepts(request.vars,session,onvalidation=depot_market_add_validation):
        response.flash = 'Saved Successfully'
    
    #  ---------------filter-------    
    btn_filter_depot_market=request.vars.btn_filter_depot_market
    btn_all=request.vars.btn_all
    reqPage=len(request.args)
    
    if btn_filter_depot_market:
        session.search_type_depot_market=request.vars.search_type
        session.search_value_depot_market=str(request.vars.search_value).strip().upper()
        reqPage=0
    elif btn_all:
        session.search_type_depot_market=None
        session.search_value_depot_market=None
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
    qset=qset(db.sm_depot_market.cid==c_id)
    qset=qset(db.sm_depot.cid==c_id)
    qset=qset((db.sm_depot.depot_id==db.sm_depot_market.depot_id))
    
    if session.user_type=='Depot':
        qset=qset(db.sm_depot_market.depot_id==session.depot_id)
    else:
        if (session.search_type_depot_market=='Depot_id'):
            searchValue=str(session.search_value_depot_market).split('|')[0]        
            qset=qset(db.sm_depot_market.depot_id==searchValue)
    
    records=qset.select(db.sm_depot_market.ALL,db.sm_depot.name,db.sm_depot.short_name,orderby=db.sm_depot_market.depot_id|db.sm_depot_market.market_id,limitby=limitby)
    recordsCount=qset.count()
    
    return dict(form=form,records=records,recordsCount=recordsCount,page=page,items_per_page=items_per_page,access_permission=access_permission,access_permission_view=access_permission_view)


def depot_market_edit_validation(form):
    c_id=session.cid
   
    depot_id=str(form.vars.depot_id).upper().split('|')[0]
    market_name=str(request.vars.market_name).strip().title()
    market_name=check_special_char(market_name)
    
    if session.user_type=='Depot':
        depot_id=session.depot_id
    
    form.vars.depot_id=depot_id
    form.vars.market_name=market_name
        
def depot_market_edit():
    task_id='rm_depot_market_manage'
    access_permission=check_role(task_id)
    if (access_permission==False):
        session.flash='Access is Denied !'
        redirect (URL('depot_market_add'))
    
    response.title='Brance Market'
    #   --------------------- 
    c_id=session.cid
        
    page=request.args(0)
    record= db.sm_depot_market(request.args(1)) or redirect(URL('depot_market_add'))   
    
    form =SQLFORM(db.sm_depot_market,
                  record=record,
                  deletable=True,
                  fields=['depot_id','market_id','market_name'],
                  submit_button='Update'
                  )
    
    if form.accepts(request.vars, session,onvalidation=depot_market_edit_validation):
        response.flash = 'Updated Successfully'        
        redirect(URL('depot_market_add',args=[page]))
    
    return dict(form=form,page=page)
    

def depot_market_batch_upload():
    task_id='rm_depot_market_manage'
    access_permission=check_role(task_id)
    if access_permission==False:
        session.flash='Access is Denied !'
        redirect (URL('depot_market','depot_market_add'))
    
    c_id=session.cid
    
    response.title='Branch Market-Batch upload'
    
    btn_upload=request.vars.btn_upload
    btn_delete=request.vars.btn_delete
        
    count_inserted=0
    count_error=0
    error_str=''
    total_row=0
    
    if btn_delete:
        delete_check=request.vars.delete_check
        if delete_check!='YES':
            response.flash='Confirmation Required'            
        else:
            db.sm_depot_market.truncate()          
            response.flash='ALL Depot Market cleaned successfully'
            
    elif btn_upload=='Upload':        
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
        #---------- 
        for i in range(total_row):
            if i>=500:
                break
            else:
                row_data=row_list[i]                    
                coloum_list=row_data.split( '\t')
                if len(coloum_list)==3:
                    depotIDExcel=str(coloum_list[0]).strip().upper()
                    
                    if depotIDExcel!='':
                        if depotIDExcel not in depot_id_list_excel:
                            depot_id_list_excel.append(depotIDExcel)
                            
        #Check valid depot list based on excel sheet
        if session.user_type=='Depot':            
            depotRows=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==session.depot_id)&(db.sm_depot.status=='ACTIVE')).select(db.sm_depot.depot_id,orderby=db.sm_depot.depot_id)
        else:
            depotRows=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id.belongs(depot_id_list_excel))&(db.sm_depot.status=='ACTIVE')).select(db.sm_depot.depot_id,orderby=db.sm_depot.depot_id)
        
        depot_list_exist=depotRows.as_list()
       
        # main loop   
        for i in range(total_row):
            if i>=500:
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
                depot_idExcel=str(coloum_list[0]).strip().upper()
                market_idExcel=str(coloum_list[1]).strip().upper()
                market_nameExcel=str(coloum_list[2]).strip().title() 
                market_nameExcel=check_special_char(market_nameExcel)
                                
                #------------------
                if depot_idExcel=='' or market_idExcel=='' or market_nameExcel=='':
                    error_data=row_data+'(Required all value)\n'
                    error_str=error_str+error_data
                    count_error+=1
                    continue
                
                #-------------------                
                try:
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
                        existCheckRows=db((db.sm_depot_market.cid==c_id)&(db.sm_depot_market.depot_id==depot_idExcel)&(db.sm_depot_market.market_id==market_idExcel)).select(db.sm_depot_market.id,limitby=(0,1))
                        if existCheckRows:
                            error_data=row_data+'(Duplicate check for Depot Market)\n'
                            error_str=error_str+error_data
                            count_error+=1
                            continue
                        else:
                            db.sm_depot_market.insert(cid=c_id,depot_id=depot_idExcel,market_id=market_idExcel,market_name=market_nameExcel)
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
def depot_market_download():
    task_id='rm_depot_market_manage'
    task_id_view='rm_depot_market_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))
        
    c_id=session.cid
    records=''
    #Create query based on search type
    qset=db()
    qset=qset(db.sm_depot_market.cid==c_id)
    qset=qset(db.sm_depot.cid==c_id)
    qset=qset((db.sm_depot.depot_id==db.sm_depot_market.depot_id))
    
    if session.user_type=='Depot':
        qset=qset(db.sm_depot_market.depot_id==session.depot_id)
    else:
        if (session.search_type_depot_market=='Depot_id'):
            searchValue=str(session.search_value_depot_market).split('|')[0]        
            qset=qset(db.sm_depot_market.depot_id==searchValue)
    
    records=qset.select(db.sm_depot_market.ALL,db.sm_depot.name,db.sm_depot.short_name,orderby=db.sm_depot_market.depot_id)
    
    #Create string for download as excel file
    myString='Branch Store List\n'
    myString+='Branch ID,Branch Name,Market ID, Market Name,Short Name\n'
    #Replace coma from records. cause coma means new Column    
    for rec in records:
        depot_id=str(rec.sm_depot_market.depot_id)        
        depot_name=str(rec.sm_depot.name)
        short_name=str(rec.sm_depot.short_name)
        market_id=str(rec.sm_depot_market.market_id)
        market_name=str(rec.sm_depot_market.market_name)
        
        myString+=str(depot_id)+','+str(depot_name)+',`'+str(market_id)+','+str(market_name)+','+str(short_name)+'\n'
        
    #-----------
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_depot_market.csv'   
    return str(myString)

