#rep_validation
#rep
#rep_edit_validation
#rep_edit
#
#sup_validation
#supervisor_create
#supervisor_edit_validation
#supervisor_edit
#
#rep_area_validation
#rep_area
#area_batch_upload
#
#download_representative
#download_rep_area
#download_supervisor
#
#rep_batch_upload
#rep_online_upload
#
#rep_area_online_upload
#active_mobile_list
#download_active_mobile_list
#======================================

#Validation for rep-----------------------
def rep_validation(form):
    from random import randint
    randNumber=randint(1001, 9999)
    
    c_id=session.cid
    rep_id=str(request.vars.rep_id).strip().upper()
    status=str(request.vars.status).strip()
    mobile_no=request.vars.mobile_no
    
    name_row=str(request.vars.name).strip()
    name=check_special_char(name_row)
    form.vars.name=name
    
    rows_check=db((db.sm_rep.cid==c_id) & (db.sm_rep.rep_id==rep_id)).select(db.sm_rep.rep_id,limitby=(0,1))
    if rows_check:
        form.errors.rep_id=''
        response.flash = 'ID already exist, please choose a new ID'
    else:
        form.vars.rep_id=rep_id
        form.vars.password=randNumber
        
        if (status=='INACTIVE'):
            form.vars.mobile_no='0'
        else:
            compMobRecords=db((db.sm_comp_mobile.cid==c_id) & (db.sm_comp_mobile.mobile_no == mobile_no)).select(db.sm_comp_mobile.mobile_no,limitby=(0,1))
            if not compMobRecords:
                form.errors.mobile_no='invalid mobile no!'
            else:
                mobRows=db((db.sm_rep.cid==c_id) & (db.sm_rep.mobile_no==mobile_no)).select(db.sm_rep.mobile_no,limitby=(0,1))
                if mobRows:
                    form.errors.mobile_no='mobile no already exist!'
                else:
                    form.vars.mobile_no=mobile_no

def rep():
    #Check access permission
    #----------Task assaign----------
    task_id='rm_rep_manage'
    task_id_view='rm_rep_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL(c='default', f='home'))
    
    c_id=session.cid
    response.title='Representative'
    
    #======================
    form =SQLFORM(db.sm_rep,
                  fields=['rep_id','name','mobile_no','status'],
                  submit_button='Save'
                  )
    
    #Insert after validation
    if form.accepts(request.vars,session,onvalidation=rep_validation):
       response.flash = 'Submitted Successfully'
       
    #------------------------filter
    btn_filter_rep=request.vars.btn_filter
    btn_rep_all=request.vars.btn_rep_all
    if btn_filter_rep:
        session.btn_filter_rep=btn_filter_rep
        session.search_type_rep=str(request.vars.search_type).strip()
        session.search_value_rep=str(request.vars.search_value).strip().upper()
        
    elif btn_rep_all:
        session.btn_filter_rep=None
        session.search_type_rep=None
        session.search_value_rep=None
        
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
    qset=qset(db.sm_rep.cid==c_id)
    qset=qset(db.sm_rep.user_type=='rep')
    
    
    # Set filter type. Create select sql based on search type    
    if (session.btn_filter_rep):
        #------------
        if (session.search_type_rep=='RepID'):
            searchValue=str(session.search_value_rep).split('|')[0]
            qset=qset(db.sm_rep.rep_id==searchValue)            
        elif (session.search_type_rep=='Status'):
            qset=qset(db.sm_rep.status==session.search_value_rep)
            
    #------------
    records=qset.select(db.sm_rep.ALL,orderby=db.sm_rep.name,limitby=limitby)
    totalCount=qset.count()
    
    #-------------- filter end
    
    return dict(form=form,records=records,totalCount=totalCount,page=page,items_per_page=items_per_page,access_permission=access_permission)
    
    #---------------end  rep-----------------------

#-----------------rep edit---------------------
# Validation rep_edit
def rep_edit_validation(form):
    c_id=session.cid
    
    current_rep=str(request.vars.current_rep).strip()
    status=str(request.vars.status).strip()
    mobile_no=request.vars.mobile_no
    
    name_row=str(request.vars.name).strip()
    name=check_special_char(name_row)
    form.vars.name=name
    
    if (status=='INACTIVE'):
        form.vars.mobile_no='0'
    elif (status=='ACTIVE'):
        compMobRecords=db((db.sm_comp_mobile.cid==c_id) & (db.sm_comp_mobile.mobile_no == mobile_no)).select(db.sm_comp_mobile.mobile_no,limitby=(0,1))
        if not compMobRecords:
            form.errors.mobile_no='invalid mobile no!'
        else:
            mobRows=db((db.sm_rep.cid==c_id) & (db.sm_rep.mobile_no==mobile_no)& (db.sm_rep.rep_id!=current_rep)).select(db.sm_rep.mobile_no,limitby=(0,1))
            if mobRows:
                form.errors.mobile_no='mobile no already exist!'
            else:
                form.vars.mobile_no=mobile_no
            
def rep_edit():
    response.title='Representative'
    
    #Check access permission
       #----------Task assaign----------
    task_id='rm_rep_manage'
    task_id_view='rm_rep_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL('representative','rep'))
    
    c_id=session.cid

    #----------
    #   depot_combo

#    if (session.user_type=='Admin'):
#        rec_depot_combo=db((db.sm_depot.cid==session.cid)).select(db.sm_depot.depot_id,db.sm_depot.name,orderby=db.sm_depot.name)
#    elif (session.user_type=='Depot'):
#        rec_depot_combo=db((db.sm_depot.cid==session.cid) & (db.sm_depot.depot_id==session.depot_id)).select(db.sm_depot.depot_id,db.sm_depot.name,orderby=db.sm_depot.name)
#    else:
#        rec_depot_combo=db((db.sm_depot.cid==session.cid)).select(db.sm_depot.depot_id,db.sm_depot.name,orderby=db.sm_depot.name)
    
    
#    show_List=[]
#    for row in rec_depot_combo:
#        depot_id=row.depot_id
#        depot_name=row.name
#        
#        dictData= {'depot_id':depot_id,'depot_name': depot_name}
#        show_List.append(dictData)
#======================
   
    page= request.args(0)
    record= db.sm_rep(request.args(1)) #or redirect(URL('index'))   

    form =SQLFORM(db.sm_rep,
                  record=record,
                  deletable=True,
                  fields=['name','mobile_no','status'],
                  submit_button='Update'
                  )
    
    records_rep=db((db.sm_rep.cid==session.cid) & (db.sm_rep.id==request.args(1))).select(db.sm_rep.rep_id,limitby=(0,1))
    rep_id=''
    for records_show_id in records_rep :
         rep_id=records_show_id.rep_id
         break
    
    if form.accepts(request.vars, session,onvalidation=rep_edit_validation):
        rep_name=form.vars.name
        db((db.sm_rep_area.cid==session.cid) & (db.sm_rep_area.rep_id==rep_id)).update(rep_name=rep_name)
        
        session.flash = 'Update Successfully'
        redirect(URL('rep',args=[page]))
    
    #If rep exist in rep area useflag will true
    useFlag=False
    repareaRows=db((db.sm_rep_area.cid==session.cid) & (db.sm_rep_area.rep_id==rep_id)).select(db.sm_rep_area.rep_id,orderby=db.sm_rep_area.rep_id,limitby=(0,1))
    if repareaRows:
        useFlag=True
    #------------------
    
    return dict(form=form,rep_id=rep_id,useFlag=useFlag,page=page)

#------------------rep end----------------------

#====================Supervisor===================(Billal)
def rep_batch_upload():
    
    from random import randint
    
    response.title='Representative Batch Upload'
    
    #Check access permission
       #----------Task assaign----------
    task_id='rm_rep_manage'
    task_id_view='rm_rep_view'
    access_permission=check_role(task_id)
#    access_permission_view=check_role(task_id_view)
    if access_permission==False:
        session.flash='Access is Denied !'
        redirect (URL('representative','rep'))
    
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
                if len(coloum_list)==4:
                    rep_list_excel.append(str(coloum_list[0]).strip().upper())
                    mobile_list_excel.append(str(coloum_list[2]).strip())
                    
        #Create list of rep already exist in database based on excel sheet        
        existRepRows=db((db.sm_rep.cid==c_id)&(db.sm_rep.rep_id.belongs(rep_list_excel))).select(db.sm_rep.rep_id,orderby=db.sm_rep.rep_id)
        rep_list_exist=existRepRows.as_list()
        
        #----------------- exist mobile
        existMobRows=db((db.sm_rep.cid==c_id)&(db.sm_rep.mobile_no.belongs(mobile_list_excel))).select(db.sm_rep.mobile_no)
        mob_list_exist=existMobRows.as_list()
        
        #------------------- valid mobile
        validMobRows=db((db.sm_comp_mobile.cid==c_id)&(db.sm_comp_mobile.mobile_no.belongs(mobile_list_excel))).select(db.sm_comp_mobile.mobile_no)
        valid_mob_list=validMobRows.as_list()
        
#   --------------------     
        for i in range(total_row):
            if i>=30: 
                break
            else:
                row_data=row_list[i]
            coloum_list=row_data.split( '\t')            

            if len(coloum_list)==4:
                repID_excel=str(coloum_list[0]).strip().upper()
                repName_excel=str(coloum_list[1]).strip().upper()
                mobile_excel=str(coloum_list[2]).strip()
                status_excel=str(coloum_list[3]).strip().upper()
                                
                try:
                    duplicate_rep=False
                    duplicate_mobile=False
                    
                    valid_field=True
                    valid_mob=False
                                        
                    if repID_excel=='' or repName_excel=='' or mobile_excel=='' or status_excel=='':
                        valid_field=False
                    
                    if valid_field==True:
                        #----------- check duplicate rep                                                
                        for i in range(len(rep_list_exist)):
                            myRowData=rep_list_exist[i]                      
                            rep_id=myRowData['rep_id']
                            if (str(rep_id).strip()==str(repID_excel).strip()):
                                duplicate_rep=True
                                break
                        
                        if duplicate_rep==False:                                
                            if status_excel=='ACTIVE':                                                                           
                                #---------- check duplicate_mobile  
                                for i in range(len(mob_list_exist)):
                                    myRowData=mob_list_exist[i]                              
                                    mobile_no=myRowData['mobile_no']
                                    if (str(mobile_no).strip()==str(mobile_excel).strip()):
                                        duplicate_mobile=True                                   
                                        break
                                
                                #---------- check valid mobile  
                                for i in range(len(valid_mob_list)):
                                    myRowData=valid_mob_list[i]                              
                                    mobileNo=myRowData['mobile_no']
                                    if (str(mobileNo).strip()==str(mobile_excel).strip()):
                                        valid_mob=True                                   
                                        break
                                                                    
                            else:
                                valid_mob=True 
                                mobile_excel=0
                                status_excel='INACTIVE'
                                
                            
                            #-----------------
                            if(duplicate_mobile==False):                             
                                if valid_mob==True:
                                    # Check duplicate in excel sheet
                                    if repID_excel not in repExcelDuplicateList:
                                        #random password
                                        randNumber=randint(1001, 9999)
                                        
                                        #Create list for bulk insert
                                        ins_dict= {'cid':c_id,'rep_id':repID_excel,'name':repName_excel,'mobile_no':mobile_excel,'password':randNumber,'status':status_excel}
                                        
                                        ins_list.append(ins_dict)                               
                                        count_inserted+=1    
                                        repExcelDuplicateList.append(repID_excel)
                                    
                                    else:
                                        error_data=row_data+'(duplicate in excel!)\n'
                                        error_str=error_str+error_data
                                        count_error+=1
                                        continue
                                else:
                                    error_data=row_data+'(invalid mobile !)\n'
                                    error_str=error_str+error_data
                                    count_error+=1
                                    continue      
                            else:
                                error_data=row_data+'(duplicate mobile no!)\n'
                                error_str=error_str+error_data
                                count_error+=1
                                continue                        
                        else:
                            error_data=row_data+'(duplicate Rep!)\n'
                            error_str=error_str+error_data
                            count_error+=1
                            continue
                    else:
                        error_data=row_data+'(all fields required value)\n'
                        error_str=error_str+error_data
                        count_error+=1
                        continue
                        
                except:
                    error_data=row_data+'(error in process!)\n'
                    error_str=error_str+error_data
                    count_error+=1
                    continue
            else:
                error_data=row_data+'(5 columns need in a row)\n'
                error_str=error_str+error_data
                count_error+=1
                continue
        
        if error_str=='':
            error_str='No error'
        #Bulk insert
        if len(ins_list) > 0:
            inCountList=db.sm_rep.bulk_insert(ins_list)             

        return dict(count_inserted=count_inserted,count_error=count_error,error_str=error_str,total_row=total_row)        
    
    return dict(count_inserted=count_inserted,count_error=count_error,error_str=error_str,total_row=total_row)

def sup_validation(form):       #validation
    from random import randint
    randNumber=randint(1001, 9999)
    
    c_id=session.cid
    
    rep_id=str(form.vars.rep_id).strip().upper()
    status=str(form.vars.status).strip()
    mobile_no=form.vars.mobile_no
    
    name_row=str(form.vars.name).strip()
    name=check_special_char(name_row)
    
    form.vars.name=name
    form.vars.user_type='sup'
    
    rows_check=db((db.sm_rep.cid==c_id) & (db.sm_rep.rep_id==rep_id)).select(db.sm_rep.rep_id,limitby=(0,1))
    if rows_check:
        form.errors.rep_id=''
        response.flash = 'ID already exist, please choose a new ID'
    else:
        form.vars.rep_id=rep_id
        form.vars.password=randNumber
        
        if (status=='INACTIVE'):
            form.vars.mobile_no='0'
        else:
            compMobRecords=db((db.sm_comp_mobile.cid==c_id) & (db.sm_comp_mobile.mobile_no == mobile_no)).select(db.sm_comp_mobile.mobile_no,limitby=(0,1))
            if not compMobRecords:
                form.errors.mobile_no='invalid mobile no!'
            else:
                mobRows=db((db.sm_rep.cid==c_id) & (db.sm_rep.mobile_no==mobile_no)).select(db.sm_rep.mobile_no,limitby=(0,1))
                if mobRows:
                    form.errors.mobile_no='mobile no already exist!'
                else:
                    form.vars.mobile_no=mobile_no
                    
def supervisor_create():       #add supervisor 
    response.title='Supervisor'
    
    #Check access permission
    #----------Task assaign----------
    task_id='rm_sup_manage'
    task_id_view='rm_sup_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))
#   ---------------------
    
    c_id=session.cid

    form =SQLFORM(db.sm_rep,
                  fields=['rep_id','name','mobile_no','status'],
                  submit_button='Save'         
                  )
    #Insert after validation
    if form.accepts(request.vars,session,onvalidation=sup_validation):
       response.flash = 'New supervisor created'

      

    #Set text for filter filter--------------------------
    search_type_sup=str(request.vars.search_type).strip()
    search_value=str(request.vars.search_value).strip()
    
    btn_filter=request.vars.btn_filter
    btn_filter_all=request.vars.btn_filter_all
    reqPage=len(request.args)
    
    if btn_filter and search_type_sup!='' and search_value!='':
        session.btn_filter_sup=request.vars.btn_filter
        session.search_type_sup=search_type_sup
        session.search_value_sup=search_value
        reqPage=0
    elif btn_filter_all:
        session.btn_filter_sup=None
        session.search_type_sup=None
        session.search_value_sup=None
        reqPage=0
        
    #--------paging
    if reqPage:
        page=int(request.args[0])
    else:
        page=0
    items_per_page=session.items_per_page
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #--------end paging  
    
    
    #   -----------
    qset=db()
    qset=qset(db.sm_rep.cid==c_id)
    qset=qset(db.sm_rep.user_type=='sup')
    
    #---- supervisor
    if session.user_type=='Supervisor':
        qset=qset(db.sm_rep.level_id == session.level_id)
    else:
        pass
    #----
    
    # Set filter type. Create select sql based on search type    
    if (session.btn_filter_sup):
        #------------
        if (session.search_type_sup=='SupID'):
            searchValue=str(session.search_value_sup).split('|')[0]
            qset=qset(db.sm_rep.rep_id==searchValue)            
        elif (session.search_type_sup=='Status'):
            qset=qset(db.sm_rep.status==session.search_value_sup)
            
    #------------
    records=qset.select(db.sm_rep.ALL,orderby=db.sm_rep.name,limitby=limitby)
    totalCount=qset.count()
    
    return dict(form=form,records=records,totalCount=totalCount,page=page,items_per_page=items_per_page,access_permission=access_permission,)



#-----------------supervisor edit---------------------
#Validation supervisor_edit
def supervisor_edit_validation(form):
    c_id=session.cid
    
    current_sup=str(request.vars.current_sup).strip().upper()
    status=str(request.vars.status).strip()
    mobile_no=request.vars.mobile_no
    
    name_row=str(request.vars.name)
    name=check_special_char(name_row)
    form.vars.name=name
    #------------
    
    if (status=='INACTIVE'):
        form.vars.mobile_no='0'
        
    elif (status=='ACTIVE'):        
        compMobRecords=db((db.sm_comp_mobile.cid==c_id) & (db.sm_comp_mobile.mobile_no == mobile_no)).select(db.sm_comp_mobile.mobile_no,limitby=(0,1))
        if not compMobRecords:
            form.errors.mobile_no='invalid mobile no!'
        else:
            mobRows=db((db.sm_rep.cid==c_id) & (db.sm_rep.mobile_no==mobile_no)& (db.sm_rep.rep_id!=current_sup)).select(db.sm_rep.mobile_no,limitby=(0,1))
            if mobRows:
                form.errors.mobile_no='mobile no already exist!'
            else:
                form.vars.mobile_no=mobile_no

def supervisor_edit():
    response.title='Supervisor'
    
    
    #Check access permission
    #----------Task assaign----------
    task_id='rm_sup_manage'
    task_id_view='rm_sup_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL('representative','supervisor_create'))
#   ---------------------
    
    c_id=session.cid

    page=request.args(0)
    record= db.sm_rep(request.args(1)) or redirect(URL('supervisor_create'))   
    form =SQLFORM(db.sm_rep,
                  record=record,
                  deletable=True,
                  fields=['name','mobile_no','status'],
                  submit_button='Update'
                  )

    records_rep=db((db.sm_rep.cid==c_id) & (db.sm_rep.id==request.args(1))).select(db.sm_rep.rep_id,limitby=(0,1))
    rep_id=''
    corrent_pass=''
    for records_show_id in records_rep :
         rep_id=records_show_id.rep_id
         break
     #Edit with validation
    if form.accepts(request.vars, session,onvalidation=supervisor_edit_validation):
        rep_name=form.vars.name
        db((db.sm_supervisor_level.cid==session.cid) & (db.sm_supervisor_level.sup_id==rep_id)).update(sup_name=rep_name)
        
        response.flash = 'Update Successfully'        
        redirect(URL(f='supervisor_create',args=[page]))
  
    #----------    
    return dict(form=form,rep_id=rep_id,page=page)

    
#===================supervisor end



#=======================rep area=======================
#Validation for rep area
def supervisor_batch_upload():
    
    from random import randint
    
    response.title='Supervisor Batch Upload'
    
    #Check access permission
       #----------Task assaign----------
    task_id='rm_sup_manage'
    access_permission=check_role(task_id)
    if access_permission==False:
        session.flash='Access is Denied !'
        redirect (URL('representative','supervisor_create'))
    
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
        validLevel_list=[]
        
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
                if len(coloum_list)==4:
                    rep_list_excel.append(str(coloum_list[0]).strip().upper())
                    mobile_list_excel.append(str(coloum_list[2]).strip())
                    
        #Create list of rep already exist in database based on excel sheet        
        existRepRows=db((db.sm_rep.cid==c_id)&(db.sm_rep.rep_id.belongs(rep_list_excel))).select(db.sm_rep.rep_id,orderby=db.sm_rep.rep_id)
        rep_list_exist=existRepRows.as_list()
        
        #----------------- exist mobile
        existMobRows=db((db.sm_rep.cid==c_id)&(db.sm_rep.mobile_no.belongs(mobile_list_excel))).select(db.sm_rep.mobile_no)
        mob_list_exist=existMobRows.as_list()
        
        #------------------- valid mobile
        validMobRows=db((db.sm_comp_mobile.cid==c_id)&(db.sm_comp_mobile.mobile_no.belongs(mobile_list_excel))).select(db.sm_comp_mobile.mobile_no)
        valid_mob_list=validMobRows.as_list()
        
        
        #-------valid area(level) list           
        validLevelRows=db((db.sm_level.cid==c_id)&(db.sm_level.is_leaf=='0')).select(db.sm_level.level_id,db.sm_level.depth,orderby=db.sm_level.level_name)
        validLevel_list=validLevelRows.as_list()
        
        #   --------------------
        for i in range(total_row):
            if i>=30: 
                break
            else:
                row_data=row_list[i]
            coloum_list=row_data.split( '\t')            

            if len(coloum_list)==4:
                repID_excel=str(coloum_list[0]).strip().upper()
                repName_excel=str(coloum_list[1]).strip().upper()
                mobile_excel=str(coloum_list[2]).strip()
                status_excel=str(coloum_list[3]).strip().upper()
                                
                try:
                    duplicate_rep=False
                    duplicate_mobile=False
                    
                    valid_field=True
                    valid_mob=False
                    
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
                            rep_id=myRowData['rep_id']
                            if (str(rep_id).strip()==str(repID_excel).strip()):
                                duplicate_rep=True
                                break
                        
                        if duplicate_rep==True:
                            error_data=row_data+'(duplicate Rep)\n'
                            error_str=error_str+error_data
                            count_error+=1
                            continue
                        else:
                            if status_excel=='ACTIVE':                                                                           
                                #---------- check duplicate_mobile  
                                for i in range(len(mob_list_exist)):
                                    myRowData=mob_list_exist[i]                              
                                    mobile_no=myRowData['mobile_no']
                                    if (str(mobile_no).strip()==str(mobile_excel).strip()):
                                        duplicate_mobile=True                                   
                                        break
                                
                                #---------- check valid mobile  
                                for i in range(len(valid_mob_list)):
                                    myRowData=valid_mob_list[i]                              
                                    mobileNo=myRowData['mobile_no']
                                    if (str(mobileNo).strip()==str(mobile_excel).strip()):
                                        valid_mob=True                                   
                                        break
                                                                    
                            else:
                                valid_mob=True 
                                mobile_excel=0
                                status_excel='INACTIVE'
                                                            
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
                                        ins_dict= {'cid':c_id,'rep_id':repID_excel,'name':repName_excel,'mobile_no':mobile_excel,'password':randNumber,'status':status_excel,'user_type':'sup'}
                                        
                                        ins_list.append(ins_dict)                               
                                        count_inserted+=1    
                                        repExcelDuplicateList.append(repID_excel)
                                            
                except:
                    error_data=row_data+'(error in process!)\n'
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
        #Bulk insert
        if len(ins_list) > 0:
            inCountList=db.sm_rep.bulk_insert(ins_list)             
            
    return dict(count_inserted=count_inserted,count_error=count_error,error_str=error_str,total_row=total_row)


def rep_area_validation(form):
    
    rep_id=str(request.vars.rep_id).strip().upper().split('|')[0]
    area_id=str(request.vars.area_id).strip().upper().split('|')[0]
    rep_category=str(request.vars.rep_category).strip().upper()
    
    if ((rep_id!='') and (area_id!='') and (session.cid!='')):
        check_rep=db((db.sm_rep.cid==session.cid) & (db.sm_rep.rep_id==rep_id) & (db.sm_rep.user_type=='rep')).select(db.sm_rep.id,db.sm_rep.rep_id,db.sm_rep.name,limitby=(0,1))
        
        if check_rep:
            rep_name=check_rep[0].name
            
            area_name=''
            if session.user_type=='Depot':
                check_area=db((db.sm_level.cid==session.cid) & (db.sm_level.depot_id==session.depot_id) & (db.sm_level.level_id==area_id) & (db.sm_level.is_leaf == '1') ).select(db.sm_level.level_id,db.sm_level.level_name,limitby=(0,1))
            else:
                check_area=db((db.sm_level.cid==session.cid) & (db.sm_level.level_id==area_id) & (db.sm_level.is_leaf == '1') ).select(db.sm_level.level_id,db.sm_level.level_name,db.sm_level.depot_id,limitby=(0,1))
            
            if check_area:
                area_name=check_area[0].level_name
                
                rows_check=db((db.sm_rep_area.cid==session.cid) & (db.sm_rep_area.rep_id==rep_id) & (db.sm_rep_area.area_id==area_id)).select(db.sm_rep_area.rep_id,limitby=(0,1))
                if rows_check:
                    form.errors.rep_id=''
                    response.flash = 'please choose a new '
                else:
                    form.vars.rep_id=rep_id
                    form.vars.rep_name=rep_name
                    
                    form.vars.area_id=area_id
                    form.vars.area_name=area_name                    
            else:
                form.errors.area_id=''
                response.flash = 'Invalid Market/Route '
        else:
            form.errors.rep_id=''
            response.flash = 'Invalid Rep '
    else:
        form.errors.rep_id=''
        response.flash = 'enter accurate value '
def rep_area():
    task_id='rm_reparea_manage'
    task_id_view='rm_reparea_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))
    
    response.title='Rep-Market'
    c_id=session.cid
    
    form =SQLFORM(db.sm_rep_area,
                  fields=['rep_id','area_id','rep_category'],
                  submit_button='Save'         
                  )   
    #Insert with validation
    if form.accepts(request.vars,session,onvalidation=rep_area_validation):
       response.flash = 'Submitted Successfully'

    #----------delete rep area---
    btn_delete=request.vars.btn_delete    
    if btn_delete:
        id_delete=request.vars.record_id
        db((db.sm_rep_area.id == id_delete)).delete()
    
    #------------------------
    btn_filter_rep_area=request.vars.btn_filter
    btn_rep_area_all=request.vars.btn_rep_area_all
    if btn_filter_rep_area:
        session.btn_filter_rep_area=btn_filter_rep_area
        
        session.search_type_reparea=request.vars.search_type
        session.search_value_reparea=str(request.vars.search_value).strip()
        
    elif btn_rep_area_all:
        session.btn_filter_rep_area=None
        session.search_type_reparea=None
        session.search_value_reparea=None

    #--------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=session.items_per_page
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #--------end paging    
    
    qset=db()
    qset=qset(db.sm_rep_area.cid==c_id)   
    
#     if session.user_type=='Depot':
#         qset=qset(db.sm_rep_area.depot_id==session.depot_id)
#     else:
#         if (session.btn_filter_rep_area and session.search_type_reparea=='DepotID'):
#             searchValue=str(session.search_value_reparea).split('|')[0]
#             qset=qset(db.sm_rep_area.depot_id==searchValue)
    
    #---- supervisor
    if session.user_type=='Supervisor':
        qset=qset(db.sm_rep_area.area_id.belongs(session.marketList))        
    else:
        pass
    
    if (session.btn_filter_rep_area and session.search_type_reparea=='RepID'):
        searchValue=str(session.search_value_reparea).split('|')[0]
        qset=qset(db.sm_rep_area.rep_id==searchValue)
        
    elif (session.btn_filter_rep_area and session.search_type_reparea=='AreaID'):
        searchValue=str(session.search_value_reparea).split('|')[0]
        qset=qset(db.sm_rep_area.area_id==searchValue)
        
    elif (session.btn_filter_rep_area and session.search_type_reparea=='CategoryID'):
        searchValue=str(session.search_value_reparea).split('|')[0]
        qset=qset(db.sm_rep_area.rep_category==searchValue)
        
    records=qset.select(db.sm_rep_area.ALL,orderby=db.sm_rep_area.rep_name|db.sm_rep_area.area_name,limitby=limitby)
    totalCount=qset.count()
    
    return dict(form=form,records=records,totalCount=totalCount,page=page,items_per_page=items_per_page,access_permission=access_permission)
#---------------end  rep_area-----------------------


#====================================== REP AREA BATCH UPLOAD ---------- 
def area_batch_upload():#Rep area batch upload
    response.title='Rep-Market Batch upload'
    c_id=session.cid
    if (c_id=='' or c_id==None):
        redirect(URL('default','index'))
    
    #Check access permission
#----------Task assaign----------
    task_id='rm_reparea_manage'
    task_id_view='rm_reparea_view'
    access_permission=check_role(task_id)
#    access_permission_view=check_role(task_id_view)

    if access_permission==False:
        session.flash='Access is Denied !'
        redirect (URL('representative','rep'))
        
#   ---------------------  
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
        rep_area_list_exist=[]
        rep_list_exist=[]
        
        
        area_list_excel=[]
        existLevel_list=[]
        
        ins_list=[]
        ins_dict={}
        
        duplicateExcelList=[]
        
#   ----------------------
        #---------- rep area
        for i in range(total_row):
            if i>=100:
                break
            else:
                row_data=row_list[i]                    
                coloum_list=row_data.split( '\t')
                if len(coloum_list)==3:
                    rep_list_excel.append(str(coloum_list[0]).strip().upper())
                    area_list_excel.append(str(coloum_list[1]).strip().upper())
        
        #Create list of rep already exist in rep area table based on excel sheet
        existRepRows=db((db.sm_rep_area.cid==c_id)&(db.sm_rep_area.rep_id.belongs(rep_list_excel))).select(db.sm_rep_area.rep_id,db.sm_rep_area.area_id,orderby=db.sm_rep_area.rep_id)
        rep_area_list_exist=existRepRows.as_list()
        
        #---------- valid rep list based onexcel sheet                           
        repRows=db((db.sm_rep.cid==c_id)&(db.sm_rep.user_type=='rep')&(db.sm_rep.rep_id.belongs(rep_list_excel))).select(db.sm_rep.rep_id,db.sm_rep.name)
        rep_list_exist=repRows.as_list()
        
        #-------valid area(level) list based onexcel sheet
        if session.user_type=='Depot':
            existLevelRows=db((db.sm_level.cid==c_id) & (db.sm_level.depot_id==session.depot_id)&(db.sm_level.is_leaf=='1')&(db.sm_level.level_id.belongs(area_list_excel))).select(db.sm_level.level_id,db.sm_level.level_name,db.sm_level.depot_id,orderby=db.sm_level.level_id)
        else:
            existLevelRows=db((db.sm_level.cid==c_id) &(db.sm_level.is_leaf=='1')&(db.sm_level.level_id.belongs(area_list_excel))).select(db.sm_level.level_id,db.sm_level.level_name,db.sm_level.depot_id,orderby=db.sm_level.level_id)
        existLevel_list=existLevelRows.as_list()
        
#   --------------------     
        for i in range(total_row):
            if i>=100: 
                break
            else:
                row_data=row_list[i]
            coloum_list=row_data.split( '\t')            

            if len(coloum_list)==3:
                repID_excel=str(coloum_list[0]).strip().upper()
                areaID_excel=str(coloum_list[1]).strip().upper()
                rep_category=str(coloum_list[2]).strip().upper()
                
                try:      
                    valid_rep=False
                    duplicate_rep_area=False
                    valid_level=False  
                    valid_depot=True
                    valid_category=True
                    depotID=''
                    #----------- check valid rep                          
                    for i in range(len(rep_list_exist)):
                        myRowData=rep_list_exist[i]                                
                        rep_id=myRowData['rep_id']
                        rep_name=myRowData['name']                        
                        if (str(rep_id).strip()==str(repID_excel).strip()):
                            valid_rep=True
                            break
                    
                    #----------- check duplicate rep-area   
                    if valid_rep==True:                                                       
                        #Get area of exist rep and check duplicate of rep area 
                        for i in range(len(rep_area_list_exist)):
                            myRowData=rep_area_list_exist[i]                                
                            rep_id_exist=myRowData['rep_id']
                            area_id=myRowData['area_id']
                            if ((str(rep_id_exist).strip()==str(repID_excel).strip())and (str(area_id).strip()==str(areaID_excel).strip())):
                                duplicate_rep_area=True
                                break
                        
                        if duplicate_rep_area==False:#---------- check valid level/depot                                                
                            for i in range(len(existLevel_list)):
                                myRowData=existLevel_list[i]                                
                                level_id=myRowData['level_id']
                                level_name=myRowData['level_name']
                                if (str(level_id).strip()==str(areaID_excel).strip()):                                                                        
                                    valid_level=True                                    
                                    break
                    
                    if valid_level==True:
                        if rep_category not in ['A','B','C']:
                            valid_category=False
                    
                    #-----------------
                    if valid_rep==True:
                        if(duplicate_rep_area==False):                             
                            if valid_level==True:
                                #Create list for bulk insert
                                if valid_category==True:
                                    
                                    repMarket=repID_excel+'-'+areaID_excel
                                    
                                    if repMarket not in duplicateExcelList:
                                        duplicateExcelList.append(repMarket)
                                        
                                        ins_dict= {'cid':c_id,'rep_id':repID_excel,'rep_name':rep_name,'rep_category':rep_category,'area_id':areaID_excel,'area_name':level_name}
                                        ins_list.append(ins_dict)
                                        count_inserted+=1
                                        
                                    else:
                                        error_data=row_data+'(duplicate in excel!)\n'
                                        error_str=error_str+error_data
                                        count_error+=1
                                        continue  
                                        
                                else:
                                    error_data=row_data+'(invalid category!)\n'
                                    error_str=error_str+error_data
                                    count_error+=1
                                    continue                            
                            else:
                                error_data=row_data+'(invalid territory/Route!)\n'
                                error_str=error_str+error_data
                                count_error+=1
                                continue
                        else:
                            error_data=row_data+'(duplicate mso-territory)\n'
                            error_str=error_str+error_data
                            count_error+=1
                            continue
                    else:
                        error_data=row_data+'(Invalid MSO ID!)\n'
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
            inCountList=db.sm_rep_area.bulk_insert(ins_list)             
     
        
        return dict(count_inserted=count_inserted,count_error=count_error,error_str=error_str,total_row=total_row)        
    
    return dict(count_inserted=count_inserted,count_error=count_error,error_str=error_str,total_row=total_row)

def validation_supervisor_level(form):    
    sup_id=str(request.vars.sup_id).strip().upper().split('|')[0]
    level_id=str(request.vars.level_id).strip().upper().split('|')[0]
    
    if ((sup_id!='') and (level_id!='')):
        check_rep=db((db.sm_rep.cid==session.cid) & (db.sm_rep.rep_id==sup_id) & (db.sm_rep.user_type=='sup')).select(db.sm_rep.id,db.sm_rep.rep_id,db.sm_rep.name,limitby=(0,1))
        if check_rep:
            sup_name=check_rep[0].name
            
            check_area=db((db.sm_level.cid==session.cid) & (db.sm_level.level_id==level_id) & (db.sm_level.is_leaf == '0')).select(db.sm_level.level_id,db.sm_level.level_name,db.sm_level.depth,limitby=(0,1))
            if check_area:
                level_name=check_area[0].level_name
                level_depth_no=check_area[0].depth
                
                rows_check=db((db.sm_supervisor_level.cid==session.cid) & (db.sm_supervisor_level.sup_id==sup_id) & (db.sm_supervisor_level.level_id==level_id)).select(db.sm_supervisor_level.sup_id,limitby=(0,1))
                if rows_check:
                    form.errors.sup_id=''
                    response.flash = 'Supervisor level already exist'
                else:
                    depthFlag=True
                    existingDepth=0
                    rows_check2=db((db.sm_supervisor_level.cid==session.cid) & (db.sm_supervisor_level.sup_id==sup_id)).select(db.sm_supervisor_level.level_depth_no,limitby=(0,1))
                    if rows_check2:
                        existingDepth=rows_check2[0].level_depth_no
                        if existingDepth!=level_depth_no:
                            depthFlag=False
                    
                    if depthFlag==False:    
                        form.errors.level_id=''
                        response.flash = 'Required the level of depth '+str(existingDepth)             
                    else:
                        form.vars.sup_id=sup_id
                        form.vars.sup_name=sup_name
                        form.vars.level_id=level_id                        
                        form.vars.level_name=level_name
                        form.vars.level_depth_no=level_depth_no
            else:
                form.errors.level_id=''
                response.flash = 'Invalid Level'
        else:
            form.errors.sup_id=''
            response.flash = 'Invalid Sup '
    else:
        form.errors.rep_id=''
        response.flash = 'Enter accurate value '
def supervisor_level():
    task_id='rm_sup_manage'
    task_id_view='rm_sup_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)    
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))
    
    response.title='Supervisor Level'
    
    c_id=session.cid
    
    form =SQLFORM(db.sm_supervisor_level,
                  fields=['sup_id','level_id'],
                  submit_button='Save'         
                  )   
    #Insert with validation
    if form.accepts(request.vars,session,onvalidation=validation_supervisor_level):
        response.flash = 'Submitted Successfully'
    
#     elif form.errors:
#         for fieldname in form.errors:
#             response.flash = str(fieldname)+' error: '+str(form.errors[fieldname])
#             break
    
    #----------delete rep area---
    btn_delete=request.vars.btn_delete    
    if btn_delete:
        id_delete=request.vars.record_id
        db((db.sm_supervisor_level.id == id_delete)).delete()
    
    #------------------------
    btn_filter_sup_level=request.vars.btn_filter
    btn_rep_area_all=request.vars.btn_rep_area_all
    if btn_filter_sup_level:
        session.btn_filter_sup_level=btn_filter_sup_level
        
        session.search_type_reparea=request.vars.search_type
        session.search_value_reparea=str(request.vars.search_value).strip()
        
    elif btn_rep_area_all:
        session.btn_filter_sup_level=None
        session.search_type_reparea=None
        session.search_value_reparea=None
        
    #--------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=session.items_per_page
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #--------end paging    
    
    qset=db()
    qset=qset(db.sm_supervisor_level.cid==c_id)   
    
    #---- supervisor
    if session.user_type=='Supervisor':
        qset=qset(db.sm_supervisor_level.level_id.belongs(session.levelList))        
    else:
        pass
    
    if (session.btn_filter_sup_level and session.search_type_reparea=='SupID'):
        searchValue=str(session.search_value_reparea).split('|')[0]
        qset=qset(db.sm_supervisor_level.sup_id==searchValue)
        
    elif (session.btn_filter_sup_level and session.search_type_reparea=='LevelID'):
        searchValue=str(session.search_value_reparea).split('|')[0]
        qset=qset(db.sm_supervisor_level.level_id==searchValue)
    
    elif (session.btn_filter_sup_level and session.search_type_reparea=='DepthNo'):
        searchValue=str(session.search_value_reparea).split('|')[0].upper()
        
        if searchValue==str(session.level0Name).upper():
            searchValueNo=0
        elif searchValue==str(session.level1Name).upper():
            searchValueNo=1
        elif searchValue==str(session.level2Name).upper():
            searchValueNo=2
        elif searchValue==str(session.level3Name).upper():
            searchValueNo=3
        elif searchValue==str(session.level4Name).upper():
            searchValueNo=4
        elif searchValue==str(session.level5Name).upper():
            searchValueNo=5
        else:
            searchValueNo=''
            
        try:
            searchValueNo=int(searchValueNo)
            qset=qset(db.sm_supervisor_level.level_depth_no==searchValueNo)            
        except:
            response.flash='Invalid Depth'
    
    records=qset.select(db.sm_supervisor_level.ALL,orderby=db.sm_supervisor_level.sup_name|db.sm_supervisor_level.level_name,limitby=limitby)
    totalCount=qset.count()
    
    return dict(form=form,records=records,totalCount=totalCount,page=page,items_per_page=items_per_page,access_permission=access_permission)

#======================================  BATCH UPLOAD
def supervisor_level_batch_upload():
    task_id='rm_sup_manage'
    access_permission=check_role(task_id)
    if access_permission==False:
        session.flash='Access is Denied !'
        redirect (URL('supervisor_level'))
    
    response.title='Supervisor Level Batch upload'
    c_id=session.cid
    
    #   ---------------------  
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
        
        sup_list_excel=[]
        sup_area_list_exist=[]
        sup_list_exist=[]
        
        level_list_excel=[]
        existLevel_list=[]
        
        #---------- sup area
        for i in range(total_row):
            if i>=30:
                break
            else:
                row_data=row_list[i]                    
                coloum_list=row_data.split( '\t')
                if len(coloum_list)==2:
                    sup_list_excel.append(str(coloum_list[0]).strip().upper())
                    level_list_excel.append(str(coloum_list[1]).strip().upper())
        
        #Create list of sup already exist in sup area table based on excel sheet
        existsupRows=db((db.sm_supervisor_level.cid==c_id)&(db.sm_supervisor_level.sup_id.belongs(sup_list_excel))).select(db.sm_supervisor_level.sup_id,db.sm_supervisor_level.level_id,db.sm_supervisor_level.level_depth_no,orderby=db.sm_supervisor_level.sup_id)
        sup_area_list_exist=existsupRows.as_list()
        
        #---------- valid sup list based onexcel sheet                &(db.sm_rep.rep_id.belongs(sup_list_excel))            
        supRows=db((db.sm_rep.cid==c_id)&(db.sm_rep.user_type=='sup')&(db.sm_rep.rep_id.belongs(sup_list_excel))).select(db.sm_rep.rep_id,db.sm_rep.name)
        sup_list_exist=supRows.as_list()
        
        #-------valid (level) list based onexcel sheet
        existLevelRows=db((db.sm_level.cid==c_id) &(db.sm_level.is_leaf=='0')&(db.sm_level.level_id.belongs(level_list_excel))).select(db.sm_level.level_id,db.sm_level.level_name,db.sm_level.depth,orderby=db.sm_level.level_id)
        existLevel_list=existLevelRows.as_list()
        
        #   --------------------
        for i in range(total_row):
            if i>=30: 
                break
            else:
                row_data=row_list[i]
            coloum_list=row_data.split( '\t')            

            if len(coloum_list)==2:
                supID_excel=str(coloum_list[0]).strip().upper()
                areaID_excel=str(coloum_list[1]).strip().upper()
                
                try:      
                    valid_sup=False
                    duplicate_sup_area=False
                    valid_level=False  
                    
                    #----------- check valid sup                          
                    for i in range(len(sup_list_exist)):
                        myRowData=sup_list_exist[i]                                
                        sup_id=myRowData['rep_id']
                        sup_name=myRowData['name']
                        if (str(sup_id).strip()==str(supID_excel).strip()):
                            valid_sup=True
                            break
                    
                    #----------- check duplicate sup-area   
                    if valid_sup==True:                                                       
                        #Get area of exist sup and check duplicate of sup area 
                        for i in range(len(sup_area_list_exist)):
                            myRowData=sup_area_list_exist[i]                                
                            sup_id_exist=myRowData['sup_id']
                            area_id=myRowData['level_id']                            
                            if ((str(sup_id_exist).strip()==str(supID_excel).strip())and (str(area_id).strip()==str(areaID_excel).strip())):
                                duplicate_sup_area=True
                                break
                        
                        if duplicate_sup_area==False:#---------- check valid level/depot                                                
                            for i in range(len(existLevel_list)):
                                myRowData=existLevel_list[i]                                
                                level_id=myRowData['level_id']
                                level_name=myRowData['level_name']
                                level_depth=myRowData['depth']
                                if (str(level_id).strip()==str(areaID_excel).strip()):                                    
                                    valid_level=True                                    
                                    break
                    
                    #-----------------
                    if valid_sup==True:
                        if(duplicate_sup_area==False):                             
                            if valid_level==True:                                
                                
                                depthFlag=True
                                existingDepth=0
                                rows_check2=db((db.sm_supervisor_level.cid==session.cid) & (db.sm_supervisor_level.sup_id==supID_excel)).select(db.sm_supervisor_level.level_depth_no,limitby=(0,1))
                                if rows_check2:
                                    existingDepth=rows_check2[0].level_depth_no
                                    if existingDepth!=level_depth:
                                        depthFlag=False
                                
                                if depthFlag==False:    
                                    error_data=row_data+'(Required the level of depth '+str(existingDepth)+')\n'
                                    error_str=error_str+error_data
                                    count_error+=1
                                    continue
                                else:
                                    db.sm_supervisor_level.insert(cid=c_id,sup_id=supID_excel,sup_name=sup_name,level_id=areaID_excel,level_name=level_name,level_depth_no=level_depth)
                                    count_inserted+=1
                                                                        
                            else:
                                error_data=row_data+'(invalid level ID!)\n'
                                error_str=error_str+error_data
                                count_error+=1
                                continue
                        else:
                            error_data=row_data+'(duplicate sup-market)\n'
                            error_str=error_str+error_data
                            count_error+=1
                            continue
                    else:
                        error_data=row_data+'(Invalid supID!)\n'
                        error_str=error_str+error_data
                        count_error+=1
                        continue

                except:
                    error_data=row_data+'(error in process!)\n'
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
        
    return dict(count_inserted=count_inserted,count_error=count_error,error_str=error_str,total_row=total_row)
    

#------------------ 
def download_supervisor_level():
    c_id=session.cid    
    task_id='rm_sup_manage'
    task_id_view='rm_sup_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)    
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL('supervisor_level'))
    
    records=''
    
    qset=db()
    qset=qset(db.sm_supervisor_level.cid==c_id)   
    
    #---- supervisor
    if session.user_type=='Supervisor':
        qset=qset(db.sm_supervisor_level.level_id.belongs(session.levelList))        
    else:
        pass
    
    if (session.btn_filter_sup_level and session.search_type_reparea=='SupID'):
        searchValue=str(session.search_value_reparea).split('|')[0]
        qset=qset(db.sm_supervisor_level.sup_id==searchValue)
        
    elif (session.btn_filter_sup_level and session.search_type_reparea=='LevelID'):
        searchValue=str(session.search_value_reparea).split('|')[0]
        qset=qset(db.sm_supervisor_level.level_id==searchValue)
    
    elif (session.btn_filter_sup_level and session.search_type_reparea=='DepthNo'):
        searchValue=str(session.search_value_reparea).split('|')[0].upper()
        
        if searchValue==str(session.level0Name).upper():
            searchValueNo=0
        elif searchValue==str(session.level1Name).upper():
            searchValueNo=1
        elif searchValue==str(session.level2Name).upper():
            searchValueNo=2
        elif searchValue==str(session.level3Name).upper():
            searchValueNo=3
        elif searchValue==str(session.level4Name).upper():
            searchValueNo=4
        elif searchValue==str(session.level5Name).upper():
            searchValueNo=5
        else:
            searchValueNo=''
            
        try:
            searchValueNo=int(searchValueNo)
            qset=qset(db.sm_supervisor_level.level_depth_no==searchValueNo)            
        except:
            response.flash='Invalid Depth'
    
    records=qset.select(db.sm_supervisor_level.ALL,orderby=db.sm_supervisor_level.sup_name|db.sm_supervisor_level.level_name)
    
    #---------
    myString='SupervisorID, SupervisorName, LevelID, LevelName, Depth/Level Name\n'
    for rec in records:
        sup_id=rec.sup_id
        sup_name=str(rec.sup_name).replace(',', ' ')
        level_id=rec.level_id
        level_name=str(rec.level_name).replace(',', ' ')
        level_depth_no=rec.level_depth_no
        level_depth_name=''
        if level_depth_no==0:
            level_depth_name=session.level0Name
        elif level_depth_no==1:
            level_depth_name=session.level1Name
        elif level_depth_no==2:
            level_depth_name=session.level2Name
        elif level_depth_no==3:
            level_depth_name=session.level3Name
        elif level_depth_no==4:
            level_depth_name=session.level4Name
        elif level_depth_no==5:
            level_depth_name=session.level5Name
            
        #Create string
        myString+=str(sup_id)+','+sup_name+','+str(level_id)+','+str(level_name)+','+str(level_depth_name)+'\n'

    #Save as csv
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_supervisor_level.csv'   
    return str(myString)


#============================================== Download
def download_representative():
    c_id=session.cid
    
    #Check access permission
       #----------Task assaign----------
    task_id='rm_rep_manage'
    task_id_view='rm_rep_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL('representative','rep'))
    
    records=''
    
    # Set query base onsearch type
    qset=db()
    qset=qset(db.sm_rep.cid==c_id)
    qset=qset(db.sm_rep.user_type=='rep')
    
    # Set filter type. Create select sql based on search type    
    if (session.btn_filter_rep):
        #------------
        if (session.search_type_rep=='RepID'):
            searchValue=str(session.search_value_rep).split('|')[0]
            qset=qset(db.sm_rep.rep_id==searchValue)            
        elif (session.search_type_rep=='Status'):
            qset=qset(db.sm_rep.status==session.search_value_rep)
    
    #------------
    records=qset.select(db.sm_rep.ALL,orderby=db.sm_rep.name)
    
    #REmove , from record.Cause , means new column in excel
    myString='Rep List\n'
    myString+='Rep ID,Name,Mobile,Status\n'
    for rec in records:
        rep_id=rec.rep_id
        name=str(rec.name).replace(',', ' ')
        mobile_no=rec.mobile_no
        status=rec.status
        depot_id=rec.depot_id
        #Create string for csv download
        myString+=str(rep_id)+','+str(name)+','+str(mobile_no)+','+str(status)+'\n'
        
    #Save as csv
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_representative.csv'   
    return str(myString)

#------------------ 
def download_rep_area():
    c_id=session.cid
    
    #Check access permission
    task_id='rm_reparea_manage'
    task_id_view='rm_reparea_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL('representative','rep'))
        
    records=''
    
    qset=db()
    qset=qset(db.sm_rep_area.cid==c_id)   
    
#     if session.user_type=='Depot':
#         qset=qset(db.sm_rep_area.depot_id==session.depot_id)
#     else:
#         if (session.btn_filter_rep_area and session.search_type_reparea=='DepotID'):
#             searchValue=str(session.search_value_reparea).split('|')[0]
#             qset=qset(db.sm_rep_area.depot_id==searchValue)
    
    #---- supervisor
    if session.user_type=='Supervisor':
        qset=qset(db.sm_rep_area.area_id.belongs(session.marketList))
    else:
        pass
    
    if (session.btn_filter_rep_area and session.search_type_reparea=='RepID'):
        searchValue=str(session.search_value_reparea).split('|')[0]
        qset=qset(db.sm_rep_area.rep_id==searchValue)
        
    elif (session.btn_filter_rep_area and session.search_type_reparea=='AreaID'):
        searchValue=str(session.search_value_reparea).split('|')[0]
        qset=qset(db.sm_rep_area.area_id==searchValue)
     
    elif (session.btn_filter_rep_area and session.search_type_reparea=='CategoryID'):
        searchValue=str(session.search_value_reparea).split('|')[0]
        qset=qset(db.sm_rep_area.rep_category==searchValue)
        
    if session.btn_filter_rep_area and session.search_value_reparea:
        records=qset.select(db.sm_rep_area.ALL,orderby=db.sm_rep_area.rep_name|db.sm_rep_area.area_name)
    else:
        session.flash='Filter needed'
        redirect (URL('representative','rep_area'))
        
    #---------
    myString='RepID, RepName, TerritoryID, TerritoryName, Category\n' #Set column name
    for rec in records:
        rep_id=rec.rep_id
        rep_name=str(rec.rep_name).replace(',', ' ')#Replace csv
        area_id=rec.area_id
        area_name=str(rec.area_name).replace(',', ' ')
        rep_category=rec.rep_category
        
        #Create string
        myString+=str(rep_id)+','+rep_name+','+str(area_id)+','+str(area_name)+','+str(rep_category)+'\n'

    #Save as csv
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_rep_area.csv'   
    return str(myString)


#------------------ 
def download_supervisor():
    c_id=session.cid
    
    #----------Task assaign----------
    task_id='rm_sup_manage'
    task_id_view='rm_sup_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL('representative','supervisor_create'))
#   ---------------------
    
    
    records=''
    #   -----------
    qset=db()
    qset=qset(db.sm_rep.cid==c_id)
    qset=qset(db.sm_rep.user_type=='sup')
    
    # Set filter type. Create select sql based on search type    
    if (session.btn_filter_sup):
        #------------
        if (session.search_type_sup=='SupID'):
            searchValue=str(session.search_value_sup).split('|')[0]
            qset=qset(db.sm_rep.rep_id==searchValue)            
        elif (session.search_type_sup=='Status'):
            qset=qset(db.sm_rep.status==session.search_value_sup)
            
    #------------
    records=qset.select(db.sm_rep.ALL,orderby=db.sm_rep.name)
    
    #Set column name
    myString='Sup ID,Name,Mobile,Status\n'
    for rec in records:
        rep_id=rec.rep_id
        name=str(rec.name).replace(',', ' ')#Replce ,
        mobile_no=rec.mobile_no
        status=rec.status
        level_id=str(rec.level_id)
        #Create string for csv
        myString+=str(rep_id)+','+name+','+str(mobile_no)+','+str(status)+'\n'

    #Sve as csv
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_super_visor.csv'   
    return str(myString)

#===================================


#===================================
def rep_online_upload():   
    from random import randint
     
    urlStr=str(request.vars.str).strip()
    urlDataList=urlStr.split('<url>',urlStr.count('<url>'))
    if len(urlDataList)!=3:
        return '<STARTSTART>'+'Failed<fd>NONE<fd>invalid url data length'+'<ENDEND>'
    else:
        c_id=str(urlDataList[0]).strip().upper()
        mac=urlDataList[1]
        dataStr=urlDataList[2]
    
    macRows=db((db.sm_settings.cid==c_id)&(db.sm_settings.s_key=='UPLOAD_MAC')).select(db.sm_settings.id,db.sm_settings.s_value,limitby=(0,1))
    if macRows:
        s_value=macRows[0].s_value
        if s_value=='0':
            macRows[0].update_record(s_value=mac)
            return '<STARTSTART>'+'Failed<fd>NONE<fd>settings completed, try to connect again'+'<ENDEND>'
        
        else:
            if (str(mac).strip()!=str(s_value).strip()):
                return '<STARTSTART>'+'Failed<fd>NONE<fd>invalid settings'+'<ENDEND>'
    else:
        return '<STARTSTART>'+'Failed<fd>NONE<fd>required settings'+'<ENDEND>'
    
    
    repListStr=''
    errorIdListStr='NONE'
    error_str=''
    
    total_row=0
    
    if dataStr=='':
        return '<STARTSTART>'+'Failed<fd>NONE<fd>required rep data'+'<ENDEND>'
    else:
        excel_data=str(dataStr)
        error_list=[]
        row_list=excel_data.split( '<rd>',excel_data.count('<rd>'))
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
                row_data=str(row_list[i]).strip()                    
                coloum_list=row_data.split( '<fd>',row_data.count('<fd>'))                
                if len(coloum_list)==5:
                    rep_list_excel.append(str(coloum_list[0]).strip().upper())
                    mobile_list_excel.append(str(coloum_list[2]).strip())
                    
        existRepRows=db((db.sm_rep.cid==c_id)&(db.sm_rep.rep_id.belongs(rep_list_excel))).select(db.sm_rep.rep_id,orderby=db.sm_rep.rep_id)
        rep_list_exist=existRepRows.as_list()
        
        #----------------- exist mobile
        existMobRows=db((db.sm_rep.cid==c_id)&(db.sm_rep.mobile_no.belongs(mobile_list_excel))).select(db.sm_rep.mobile_no)
        mob_list_exist=existMobRows.as_list()
        
        #------------------- valid mobile
        validMobRows=db((db.sm_comp_mobile.cid==c_id)&(db.sm_comp_mobile.user_type=='rep')&(db.sm_comp_mobile.mobile_no.belongs(mobile_list_excel))).select(db.sm_comp_mobile.mobile_no)
        valid_mob_list=validMobRows.as_list()
        
        #-------valid area(level) list           
        validDepotRows=db(db.sm_depot.cid==c_id).select(db.sm_depot.depot_id,orderby=db.sm_depot.depot_id)
        validDepot_list=validDepotRows.as_list()
        
#   --------------------     
        for i in range(total_row):
            if i>=30: 
                break
            else:
                row_data=str(row_list[i]).strip()
                
            coloum_list=row_data.split( '<fd>',row_data.count('<fd>'))       

            if len(coloum_list)==5:
                repID_excel=str(coloum_list[0]).strip().upper()
                repName_excel=str(coloum_list[1]).strip().upper()
                mobile_excel=str(coloum_list[2]).strip()
                status_excel=str(coloum_list[3]).strip().upper()
                depot_excel=str(coloum_list[4]).strip().upper()
                
                try:
                    duplicate_rep=False
                    duplicate_mobile=False
                    
                    valid_field=True
                    valid_mob=False
                    valid_depot=False
                    
                    if repID_excel=='' or repName_excel=='' or mobile_excel=='' or status_excel=='':
                        valid_field=False
                    
                    if valid_field==True:
                        #----------- check duplicate rep                                                
                        for i in range(len(rep_list_exist)):
                            myRowData=rep_list_exist[i]                      
                            rep_id=myRowData['rep_id']
                            if (str(rep_id).strip()==str(repID_excel).strip()):
                                duplicate_rep=True
                                break
                        
                        if duplicate_rep==False:                                
                            if status_excel=='ACTIVE':                                                                           
                                #---------- check duplicate_mobile  
                                for i in range(len(mob_list_exist)):
                                    myRowData=mob_list_exist[i]                              
                                    mobile_no=myRowData['mobile_no']
                                    if (str(mobile_no).strip()==str(mobile_excel).strip()):
                                        duplicate_mobile=True                                   
                                        break
                                
                                #---------- check valid mobile  
                                for i in range(len(valid_mob_list)):
                                    myRowData=valid_mob_list[i]                              
                                    mobileNo=myRowData['mobile_no']
                                    if (str(mobileNo).strip()==str(mobile_excel).strip()):
                                        valid_mob=True                                   
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
                            if(duplicate_mobile==False):                             
                                if valid_mob==True:  
                                    if valid_depot==True:                                         
                                        if repID_excel not in repExcelDuplicateList:      
                                            #random password
                                            randNumber=randint(1001, 9999)
                                            
                                            repExcelDuplicateList.append(repID_excel)                                  
                                            
                                            ins_dict= {'cid':c_id,'rep_id':repID_excel,'name':repName_excel,'mobile_no':mobile_excel,'password':randNumber,'status':status_excel,'depot_id':depot_excel}
                                            ins_list.append(ins_dict)
                                            
                                            if repListStr=='':
                                                repListStr="'"+repID_excel+"'"
                                            else:
                                                repListStr+=",'"+repID_excel+"'"                                            
                                        else:
                                            error_data='RepID:'+repID_excel+'( duplicate in excel )<rdrd>'
                                            error_str=error_str+error_data
                                            
                                            if errorIdListStr=='NONE':
                                                errorIdListStr="'"+repID_excel+"'"
                                            else:
                                                errorIdListStr+=",'"+repID_excel+"'"                                            
                                            continue                                        
                                    else:
                                        error_data='RepID:'+repID_excel+'( invalid depot )<rdrd>'
                                        error_str=error_str+error_data
                                        if errorIdListStr=='NONE':
                                            errorIdListStr="'"+repID_excel+"'"
                                        else:
                                            errorIdListStr+=",'"+repID_excel+"'"                                                
                                        continue 
                                else:
                                    error_data='RepID:'+repID_excel+'( invalid mobile )<rdrd>'
                                    error_str=error_str+error_data
                                    
                                    if errorIdListStr=='NONE':
                                        errorIdListStr="'"+repID_excel+"'"
                                    else:
                                        errorIdListStr+=",'"+repID_excel+"'"                                    
                                    continue      
                            else:
                                error_data='RepID:'+repID_excel+'( duplicate mobile no )<rdrd>'
                                error_str=error_str+error_data
                                if errorIdListStr=='NONE':
                                    errorIdListStr="'"+repID_excel+"'"
                                else:
                                    errorIdListStr+=",'"+repID_excel+"'"
                                
                                continue                        
                        else:
                            error_data='RepID:'+repID_excel+'( duplicate Rep )<rdrd>'
                            error_str=error_str+error_data
                            
                            if errorIdListStr=='NONE':
                                errorIdListStr="'"+repID_excel+"'"
                            else:
                                errorIdListStr+=",'"+repID_excel+"'"                            
                            continue
                    else:
                        error_data='RepID:'+repID_excel+'( all fields required value )<rdrd>'
                        error_str=error_str+error_data
                        
                        if errorIdListStr=='NONE':
                            errorIdListStr="'"+repID_excel+"'"
                        else:
                            errorIdListStr+=",'"+repID_excel+"'"                        
                        continue
                except:
                    error_data='RepID:'+repID_excel+'( error in process )<rdrd>'
                    error_str=error_str+error_data
                    
                    if errorIdListStr=='NONE':
                        errorIdListStr="'"+repID_excel+"'"
                    else:
                        errorIdListStr+=",'"+repID_excel+"'"                    
                    continue
            else:
                error_data='RepID:'+repID_excel+'( 5 columns need in a row )<rdrd>'
                error_str=error_str+error_data
                
                if errorIdListStr=='NONE':
                    errorIdListStr="'"+repID_excel+"'"
                else:
                    errorIdListStr+=",'"+repID_excel+"'"                
                continue
        
        if error_str=='':
            error_str='No Error'
        
        if len(ins_list) > 0:
            inCountList=db.sm_rep.bulk_insert(ins_list)             

        return '<STARTSTART>'+repListStr+'<fd>'+errorIdListStr+'<fd>'+error_str+'<ENDEND>'

#====================================== REP AREA ONLINE BATCH UPLOAD

def active_mobile_list():     
    response.title='Active Mobile List'
    
    #Check Access permission
    #----------Task assaign----------
    task_id='rm_rep_manage'
    task_id_view='rm_rep_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))
    
    #--------paging
    reqPage=len(request.args)
    if reqPage:
        page=int(request.args[0])
    else:
        page=0
    items_per_page=100
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #--------end paging 
    
    records=db(db.sm_comp_mobile.cid==session.cid).select(db.sm_comp_mobile.ALL,orderby=db.sm_comp_mobile.mobile_no,limitby=limitby)  
    
    usedList=[]
    mobRows=db(db.sm_rep.cid==session.cid).select(db.sm_rep.mobile_no)
    for mobRow in mobRows:
        mobile_no=str(mobRow.mobile_no)
        usedList.append(mobile_no)
    
    return dict(records=records,usedList=usedList,page=page,items_per_page=items_per_page)
    
#============================================== Download
def download_active_mobile_list():
    #Check Access permission
    #----------Task assaign----------
    task_id='rm_rep_manage'
    task_id_view='rm_rep_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))
        
    records=db(db.sm_comp_mobile.cid==session.cid).select(db.sm_comp_mobile.ALL,orderby=db.sm_comp_mobile.mobile_no)  
    
    usedList=[]
    #Create list for used mobile no
    mobRows=db(db.sm_rep.cid==session.cid).select(db.sm_rep.mobile_no)
    for mobRow in mobRows:
        mobile_no=str(mobRow.mobile_no)
        usedList.append(mobile_no)
    
    #Setring for column heading
    myString='Mobile No,User Type,Status\n'
    for rec in records:
        mobile_no=str(rec.mobile_no)
        user_type=str(rec.user_type).upper()
        
        status=''
        if mobile_no in usedList:
            status='USED'
                
        myString+=mobile_no+','+user_type+','+status+'\n'
    
    #-----------
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_active_MSISDN.csv'   
    return str(myString)