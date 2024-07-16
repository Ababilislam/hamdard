#Validation for delivery_man
def validation_delivery_man(form):
    from random import randint
    randNumber=randint(1001, 9999)
    
    c_id=session.cid
    d_man_id=str(request.vars.d_man_id).strip().upper().split('|')[0]
    status=str(request.vars.status).strip()
    mobile_no=request.vars.mobile_no
    
    name_row=str(request.vars.name).strip()
    name=check_special_char(name_row)
    form.vars.name=name
    
    depot_idStr=str(request.vars.depot_id).strip()
    
    depotFlag=True
    depot_id=''
    if depot_idStr!='':
        depot_id=depot_idStr.split('|')[0]
        depotrows=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.depot_id,db.sm_depot.name,limitby=(0,1))
        if not depotrows:
            depotFlag=False
            
    if depotFlag==False:
        form.errors.d_man_id=''
        response.flash = 'Invalid depot'
    else:
        form.vars.depot_id=depot_id
        
        #if status Active then mobile number must. If inactive mobile number will blank
        if not (mobile_no=='' or mobile_no=='0'):
            
            #Check mobile number already used or not
            mobRows=db((db.sm_delivery_man.cid==c_id) & (db.sm_delivery_man.mobile_no==mobile_no)).select(db.sm_delivery_man.mobile_no,limitby=(0,1))
            if not mobRows:
                rows_check=db((db.sm_delivery_man.cid==c_id) & (db.sm_delivery_man.d_man_id==d_man_id)).select(db.sm_delivery_man.d_man_id,limitby=(0,1))
                if rows_check:
                    form.errors.d_man_id=''
                    response.flash = 'please choose a new '
                else:
                    if (status=='ACTIVE'):
                        if depot_id=='':
                            form.errors.d_man_id=''
                            response.flash = 'Invalid depot for ACTIVE Representative '
                            
                    form.vars.d_man_id=d_man_id
                    form.vars.password=randNumber
                    form.vars.mobile_no=mobile_no
                    
            else:
                form.errors.mobile_no='mobile no already exist!'
        
        else:
            rows_check=db((db.sm_delivery_man.cid==c_id) & (db.sm_delivery_man.d_man_id==d_man_id)).select(db.sm_delivery_man.d_man_id,limitby=(0,1))
            if rows_check:
                form.errors.d_man_id=''
                response.flash = 'please choose a new '
            else:
                if (status=='ACTIVE'):
                    if depot_id=='':
                        form.errors.d_man_id=''
                        response.flash = 'Invalid depot for ACTIVE Representative '
                
                form.vars.mobile_no='0'
                form.vars.d_man_id=d_man_id
                form.vars.password='123'
        
            
def delivery_man():
    task_id='rm_delivery_man_manage'
    task_id_view='rm_delivery_man_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL(c='default', f='home'))
    
    response.title='Delivery Man'
    
    c_id=session.cid
    
    #======================
    form =SQLFORM(db.sm_delivery_man,
                  fields=['d_man_id','name','mobile_no','status','depot_id'],
                  submit_button='Save'
                  )
    
    #Insert after validation
    if form.accepts(request.vars,session,onvalidation=validation_delivery_man):
       response.flash = 'Submitted Successfully'
       
    #------------------------filter
    btn_filter_dman=request.vars.btn_filter
    btn_rep_all=request.vars.btn_rep_all
    if btn_filter_dman:
        session.btn_filter_dman=btn_filter_dman
        session.search_type_dman=str(request.vars.search_type).strip()
        session.search_value_dman=str(request.vars.search_value).strip().upper()
        
    elif btn_rep_all:
        session.btn_filter_dman=None
        session.search_type_dman=None
        session.search_value_dman=None
        
    #--------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=session.items_per_page
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #--------end paging    
    
    #   -----------
    qset=db()
    qset=qset(db.sm_delivery_man.cid==c_id)
    
    if (session.user_type=='Depot'):
        qset=qset(db.sm_delivery_man.depot_id==session.depot_id)
    
    else:
        if (session.search_type_dman=='Depot'):
            searchValue=str(session.search_value_dman).split('|')[0]
            qset=qset(db.sm_delivery_man.depot_id==searchValue)
            
    # Set filter type. Create select sql based on search type    
    if (session.btn_filter_dman):
        #------------
        if (session.search_type_dman=='DManID'):
            searchValue=str(session.search_value_dman).split('|')[0]
            qset=qset(db.sm_delivery_man.d_man_id==searchValue)            
            
        elif (session.search_type_dman=='Status'):
            qset=qset(db.sm_delivery_man.status==session.search_value_dman)
            
    #------------
    records=qset.select(db.sm_delivery_man.ALL,orderby=db.sm_delivery_man.d_man_id,limitby=limitby)
    totalCount=qset.count()
    #-------------- filter end
    
    return dict(form=form,records=records,totalCount=totalCount,page=page,items_per_page=items_per_page,access_permission=access_permission)
    
    #---------------end  rep-----------------------

#-----------------rep edit---------------------
# Validation rep_edit
def validation_delivery_man_edit(form):
    c_id=session.cid
    
    current_rep=str(request.vars.current_rep).strip().split('|')[0]
    status=str(request.vars.status).strip()
    mobile_no=request.vars.mobile_no
    
    name_row=str(request.vars.name).strip()
    name=check_special_char(name_row)
    form.vars.name=name
    
    if str(mobile_no)=='':
        mobile_no=0
    
    
    depot_idStr=str(request.vars.depot_id).strip()
    
    depotFlag=True
    depot_id=''
    if depot_idStr!='':
        depot_id=depot_idStr.split('|')[0]
        depotrows=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.depot_id,db.sm_depot.name,limitby=(0,1))
        if not depotrows:
            depotFlag=False
    
    if depotFlag==False:
        form.errors.d_man_id=''
        response.flash = 'Invalid depot'
    else:
        form.vars.depot_id=depot_id
        
        if (str(depot_id).strip()!=''):
            depot_old=db((db.sm_delivery_man.cid==c_id) & (db.sm_delivery_man.d_man_id == current_rep)).select(db.sm_delivery_man.depot_id,limitby=(0,1))
            depot_check=''
            if depot_old:
                depot_check=depot_old[0].depot_id
            
            if(str(depot_check).strip()==''):
                pass
            if (str(depot_id).strip()==str(depot_check).strip()):
                pass
            else:
                pass
        
        if (status=='ACTIVE'):
            if ((current_rep!='') and (str(mobile_no)!='0')):
                mobRows=db((db.sm_delivery_man.cid==c_id) & (db.sm_delivery_man.mobile_no==mobile_no)& (db.sm_delivery_man.d_man_id!=current_rep)).select(db.sm_delivery_man.mobile_no,limitby=(0,1))
                if not mobRows:
                    form.vars.mobile_no=mobile_no
                else:
                    form.errors.mobile_no='mobile no already exist'
            else:
                pass
                
        else:
            pass
            
            
            
def delivery_man_edit():
    #----------Task assaign----------
    task_id='rm_delivery_man_manage'
    task_id_view='rm_delivery_man_view'
    access_permission=check_role(task_id)
    if (access_permission==False):
        session.flash='Access is Denied'
        redirect (URL('delivery_man','delivery_man'))
        
    response.title='Delivery Man - Edit'
    
    c_id=session.cid
    
    #----------    
    page= request.args(0)
    record= db.sm_delivery_man(request.args(1)) #or redirect(URL('index'))   
    
    form =SQLFORM(db.sm_delivery_man,
                  record=record,
                  deletable=True,
                  fields=['name','mobile_no','status','depot_id'],
                  submit_button='Update'
                  )
    
    #------------------    
    if form.accepts(request.vars, session,onvalidation=validation_delivery_man_edit):
        response.flash = 'Update Successfully'        
        redirect(URL('delivery_man',args=[page]))
    
    records=db((db.sm_delivery_man.cid==c_id) & (db.sm_delivery_man.id==request.args(1))).select(db.sm_delivery_man.d_man_id,db.sm_delivery_man.depot_id,limitby=(0,1))
    d_man_id=''
    depot_id_show=''
    depot_name_show=''
    if records:
         d_man_id=records[0].d_man_id
         depot_id_show=records[0].depot_id
         
    depotrows=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id_show)).select(db.sm_depot.name,limitby=(0,1))
    if depotrows:
        depot_name_show=depotrows[0].name
    
    return dict(form=form,d_man_id=d_man_id,depot_id_show=depot_id_show,depot_name_show=depot_name_show,page=page)
    
#------------------rep end----------------------

#====================Supervisor===================(Billal)
def delivery_man_batch_upload():
    
    from random import randint
    
    response.title='Delivery Man Batch Upload'
    
    #Check access permission
       #----------Task assaign----------
    task_id='rm_delivery_man_manage'
    task_id_view='rm_delivery_man_view'
    access_permission=check_role(task_id)
#    access_permission_view=check_role(task_id_view)
    if access_permission==False:
        session.flash='Access is Denied'
        redirect (URL('delivery_man','delivery_man'))
    
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
        
        rep_list_excel=[]
        mobile_list_excel=[]
        
        rep_list_exist=[]
        mob_list_exist=[]
        
        valid_mob_list=[]
        validDepot_list=[]
        
        repExcelDuplicateList=[]
        
        ins_list=[]
        ins_dict={}
        #---------- rep area
        for i in range(total_row):
            if i>=30:
                break
            else:
                row_data=row_list[i]                    
                coloum_list=row_data.split( '\t')
                if len(coloum_list)==5:
                    rep_list_excel.append(str(coloum_list[0]).strip().upper())
                    mobile_list_excel.append(str(coloum_list[2]).strip())
                    
        #Create list of rep already exist in database based on excel sheet        
        existRepRows=db((db.sm_delivery_man.cid==c_id)&(db.sm_delivery_man.d_man_id.belongs(rep_list_excel))).select(db.sm_delivery_man.d_man_id,orderby=db.sm_delivery_man.d_man_id)
        rep_list_exist=existRepRows.as_list()
        
        #----------------- exist mobile
        existMobRows=db((db.sm_delivery_man.cid==c_id)&(db.sm_delivery_man.mobile_no.belongs(mobile_list_excel))).select(db.sm_delivery_man.mobile_no)
        mob_list_exist=existMobRows.as_list()
                
        #-------valid area(level) list           
        validDepotRows=db(db.sm_depot.cid==c_id).select(db.sm_depot.depot_id,orderby=db.sm_depot.depot_id)
        validDepot_list=validDepotRows.as_list()
        
        #--------------------     
        for i in range(total_row):
            if i>=30: 
                break
            else:
                row_data=row_list[i]
            coloum_list=row_data.split( '\t')            
            
            if len(coloum_list)!=5:
                error_data=row_data+'(5 columns need in a row)\n'
                error_str=error_str+error_data
                count_error+=1
                continue
            else:
                repID_excel=str(coloum_list[0]).strip().upper()
                repName_excel=str(coloum_list[1]).strip().upper()
                mobile_excel=str(coloum_list[2]).strip()
                status_excel=str(coloum_list[3]).strip().upper()
                depot_excel=str(coloum_list[4]).strip().upper()
                
                try:
                    duplicate_rep=False
                    duplicate_mobile=False
                    
                    valid_field=True
                    valid_mob=True
                    valid_depot=False
                    
                    if repID_excel=='' or repName_excel=='' or mobile_excel=='' or status_excel=='':
                        valid_field=False
                    
                    if valid_field==False:
                        error_data=row_data+'(all fields required value)\n'
                        error_str=error_str+error_data
                        count_error+=1
                        continue
                    else:
                        #----------- check duplicate rep                                                
                        for i in range(len(rep_list_exist)):
                            myRowData=rep_list_exist[i]                      
                            d_man_id=myRowData['d_man_id']
                            if (str(d_man_id).strip()==str(repID_excel).strip()):
                                duplicate_rep=True
                                break
                        
                        if duplicate_rep==True:
                            error_data=row_data+'(duplicate Delivery Man ID)\n'
                            error_str=error_str+error_data
                            count_error+=1
                            continue
                        else:
                            try:
                                mobile_excel=int(mobile_excel)
                                if mobile_excel<=0:
                                    mobile_excel=0
                            except:
                                mobile_excel=0
                            
                            if status_excel=='ACTIVE':
                                
                                if mobile_excel!=0:                    
                                    #---------- check duplicate_mobile  
                                    for i in range(len(mob_list_exist)):
                                        myRowData=mob_list_exist[i]                              
                                        mobile_no=myRowData['mobile_no']
                                        if (str(mobile_no).strip()==str(mobile_excel).strip()):
                                            duplicate_mobile=True                                   
                                            break
                                
                                #---------- check valid depot  
                                for i in range(len(validDepot_list)):
                                    myRowData=validDepot_list[i]                              
                                    depot_id=myRowData['depot_id']
                                    if (str(depot_id).strip()==str(depot_excel).strip()):
                                        valid_depot=True                                   
                                        break
                            
                            else:
                                valid_mob=True 
                                mobile_excel=0
                                status_excel='INACTIVE'
                                
                                if str(depot_excel).strip()=='0' or str(depot_excel).strip()=='':
                                    valid_depot=True
                                    depot_excel=''                                
                                else:
                                    #---------- check valid depot  
                                    for i in range(len(validDepot_list)):
                                        myRowData=validDepot_list[i]                              
                                        depot_id=myRowData['depot_id']
                                        if (str(depot_id).strip()==str(depot_excel).strip()):
                                            valid_depot=True                                   
                                            break
                            
                            #-----------------
                            if(duplicate_mobile==True):
                                error_data=row_data+'(duplicate mobile no)\n'
                                error_str=error_str+error_data
                                count_error+=1
                                continue
                            else:
                                if valid_mob==False:
                                    error_data=row_data+'(invalid mobile)\n'
                                    error_str=error_str+error_data
                                    count_error+=1
                                    continue
                                else:
                                    if valid_depot==False:
                                        error_data=row_data+'(invalid depot)\n'
                                        error_str=error_str+error_data
                                        count_error+=1
                                        continue
                                    else:
                                        # Check duplicate in excel sheet
                                        if repID_excel in repExcelDuplicateList:
                                            error_data=row_data+'(duplicate in excel)\n'
                                            error_str=error_str+error_data
                                            count_error+=1
                                            continue
                                        else:
                                            #random password
                                            randNumber=randint(1001, 9999)
                                            
                                            #Create list for bulk insert
                                            ins_dict= {'cid':c_id,'d_man_id':repID_excel,'name':repName_excel,'mobile_no':mobile_excel,'password':randNumber,'status':status_excel,'depot_id':depot_excel}
                                            
                                            ins_list.append(ins_dict)                               
                                            count_inserted+=1    
                                            repExcelDuplicateList.append(repID_excel)
                
                except:
                    error_data=row_data+'(error in process!)\n'
                    error_str=error_str+error_data
                    count_error+=1
                    continue
        
        
        if error_str=='':
            error_str='No error'
        #Bulk insert
        if len(ins_list) > 0:
            inCountList=db.sm_delivery_man.bulk_insert(ins_list)             
            
    return dict(count_inserted=count_inserted,count_error=count_error,error_str=error_str,total_row=total_row)
    
def download_delivery_man():
    c_id=session.cid
    
    #----------Task assaign
    task_id='rm_delivery_man_manage'
    task_id_view='rm_delivery_man_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL('delivery_man','delivery_man'))
    
    records=''
    
    # Set query base onsearch type
    qset=db()
    qset=qset(db.sm_delivery_man.cid==c_id)
    
    if (session.user_type=='Depot'):
        qset=qset(db.sm_delivery_man.depot_id==session.depot_id)
    
    else:
        if (session.search_type_dman=='Depot'):
            searchValue=str(session.search_value_dman).split('-')[0]
            qset=qset(db.sm_delivery_man.depot_id==searchValue)
            
    # Set filter type. Create select sql based on search type    
    if (session.btn_filter_dman):
        #------------
        if (session.search_type_dman=='DManID'):
            searchValue=str(session.search_value_dman).split('-')[0]
            qset=qset(db.sm_delivery_man.d_man_id==searchValue)            
            
        elif (session.search_type_dman=='Status'):
            qset=qset(db.sm_delivery_man.status==session.search_value_dman)
        
    #------------
    records=qset.select(db.sm_delivery_man.ALL,orderby=db.sm_delivery_man.d_man_id)
    
    #=======
    myString='Delivery Man List\n'
    myString+='Delivery Man ID,Name,Mobile,Status,Depot ID\n'
    for rec in records:
        d_man_id=rec.d_man_id
        name=str(rec.name).replace(',', ' ')
        mobile_no=rec.mobile_no
        status=rec.status
        depot_id=rec.depot_id
        #Create string for csv download
        myString+=str(d_man_id)+','+str(name)+','+str(mobile_no)+','+str(status)+','+str(depot_id)+'\n'

    #Save as csv
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_delivery_man.csv'   
    return str(myString)

#------------------ 
