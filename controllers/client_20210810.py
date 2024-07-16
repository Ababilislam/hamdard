
#---------------catagory-----------------------
def catagory_validation(form):    
    category_id=str(request.vars.cat_type_id).strip().upper()
    cat_type_name=str(request.vars.cat_type_name).strip()
    
    rows_check=db((db.sm_category_type.cid==session.cid) & (db.sm_category_type.type_name=='CLIENT_CATEGORY') &(db.sm_category_type.cat_type_id==category_id)).select(db.sm_category_type.cat_type_id,limitby=(0,1))
    if rows_check:
        form.errors.cat_type_id=''
        response.flash = 'please choose a new '
    else:
        form.vars.cid=session.cid
        form.vars.type_name='CLIENT_CATEGORY'
        form.vars.cat_type_id=category_id
        form.vars.cat_type_name=cat_type_name
def catagory():
    response.title='Category'    
    task_id='rm_client_cat_manage'
    task_id_view='rm_client_cat_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)    
    if ((access_permission==False) and (access_permission_view==False)):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))
    
    #---------------------    
    form =SQLFORM(db.sm_category_type,
                  fields=['cat_type_id','cat_type_name'],
                  submit_button='Save'
                  )
    
    if form.accepts(request.vars,session,onvalidation=catagory_validation):
       response.flash = 'Saved Successfully'
    
    #--------------------------------
    btn_delete=request.vars.btn_delete
    record_id=request.vars.record_id
    if btn_delete:
        record_id=request.args[1]
        category_id=request.args[2]
        records=db((db.sm_client.cid==session.cid) & (db.sm_client.category_id==category_id)).select(db.sm_client.category_id,limitby=(0,1))
        if not records:
            db((db.sm_category_type.id == record_id)&(db.sm_category_type.type_name=='CLIENT_CATEGORY')).delete()
        else:
            response.flash='This category is used in client'
    
    #--------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=session.items_per_page
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #--------end paging
    
    records=db((db.sm_category_type.cid==session.cid)&(db.sm_category_type.type_name=='CLIENT_CATEGORY')).select(db.sm_category_type.ALL,orderby=db.sm_category_type.cat_type_id,limitby=limitby)

    return dict(form=form,records=records,page=page,items_per_page=items_per_page,access_permission=access_permission)
#---------------end  catagory-----------------------

#---------------sub_catagory-----------------------
def sub_catagory_validation(form):    
    category_id=str(request.vars.cat_type_id).strip().upper()
    cat_type_name=str(request.vars.cat_type_name).strip()
    
    rows_check=db((db.sm_category_type.cid==session.cid) & (db.sm_category_type.type_name=='CLIENT_SUB_CATEGORY') &(db.sm_category_type.cat_type_id==category_id)).select(db.sm_category_type.cat_type_id,orderby=db.sm_category_type.cat_type_id,limitby=(0,1))
    if rows_check:
        form.errors.cat_type_id=''
        response.flash = 'please choose a new '
    else:
        form.vars.cid=session.cid
        form.vars.type_name='CLIENT_SUB_CATEGORY'
        form.vars.cat_type_id=category_id
        form.vars.cat_type_name=cat_type_name
def sub_catagory():
     
    task_id='rm_client_cat_manage'
    task_id_view='rm_client_cat_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)    
    if ((access_permission==False) and (access_permission_view==False)):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))
    
    
    response.title='Sub Category'
    
    #---------------------    
    form =SQLFORM(db.sm_category_type,
                  fields=['cat_type_id','cat_type_name'],
                  submit_button='Save'
                  )
    
    if form.accepts(request.vars,session,onvalidation=sub_catagory_validation):
       response.flash = 'Saved Successfully'
    
    #--------------------------------
    btn_delete=request.vars.btn_delete
    record_id=request.vars.record_id
    if btn_delete:
        record_id=request.args[1]
        category_id=request.args[2]
        records=db((db.sm_client.cid==session.cid) & (db.sm_client.category_id==category_id)).select(db.sm_client.category_id,limitby=(0,1))
        if not records:
            db((db.sm_category_type.id == record_id)&(db.sm_category_type.type_name=='CLIENT_SUB_CATEGORY')).delete()
        else:
            response.flash='This category is used in client'
    
    #--------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=session.items_per_page
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #--------end paging
    
    records=db((db.sm_category_type.cid==session.cid)&(db.sm_category_type.type_name=='CLIENT_SUB_CATEGORY')).select(db.sm_category_type.ALL,orderby=db.sm_category_type.cat_type_id,limitby=limitby)

    return dict(form=form,records=records,page=page,items_per_page=items_per_page,access_permission=access_permission)
#---------------end  catagory-----------------------


#client List
def client():
    #----------Task assaign----------
    task_id='rm_client_manage'
    task_id_view='rm_client_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))        
    
    #   --------------------- 
    response.title='Client List'   
    
    cid=session.cid
    
    #------------------filter
    btn_filter_client=request.vars.btn_filter
    btn_filter_client_all=request.vars.btn_filter_client_all
    reqPage=len(request.args)
    if btn_filter_client:
        session.btn_filter_client=btn_filter_client
        session.search_type_client=request.vars.search_type
        session.search_value_client=str(request.vars.search_value).strip().upper()
        reqPage=0
    elif btn_filter_client_all:
        session.btn_filter_client=None
        session.search_type_client=None
        session.search_value_client=None
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
    qset=qset(db.sm_client.cid==session.cid)
    
    #---- supervisor
    if session.user_type=='Supervisor':
        level_id=session.level_id
        depthNo=session.depthNo
        level = 'level' + str(depthNo)
        
        qset=qset((db.sm_level.cid==cid)&(db.sm_level.is_leaf=='1')& (db.sm_level[level] == level_id)&(db.sm_level.level_id==db.sm_client.area_id))
        
    else:
        qset=qset((db.sm_level.cid==cid)&(db.sm_level.is_leaf=='1')&(db.sm_level.level_id==db.sm_client.area_id))
    
    if session.user_type=='Depot':
        qset=qset(db.sm_client.depot_id==session.depot_id)    
    else:
        if (session.btn_filter_client and session.search_type_client=='DepotID'):
            searchValue=str(session.search_value_client).split('|')[0]
            qset=qset(db.sm_client.depot_id==searchValue)
    
    if session.btn_filter_client:
        if (session.search_type_client=='ClientID'):
            searchValue=str(session.search_value_client).split('|')[0]
            
            qset=qset(db.sm_client.client_id==str(searchValue).strip())
            
        elif (session.search_type_client=='AreaID'):
            searchValue=str(session.search_value_client).split('|')[0]
            qset=qset(db.sm_client.area_id==searchValue)
            
        elif (session.search_type_client=='Status'):            
            qset=qset(db.sm_client.status==session.search_value_client)
        
        elif (session.search_type_client=='District'):
            searchValue=str(session.search_value_client).split('|')[0]         
            qset=qset(db.sm_client.district_id==searchValue)
            
        elif (session.search_type_client=='Region'):
            searchValue=str(session.search_value_client).split('|')[0]         
            qset=qset(db.sm_level.level0==searchValue)
    
    records=qset.select(db.sm_client.ALL,db.sm_level.level_name,db.sm_level.level0,db.sm_level.level0_name,orderby=db.sm_client.name,limitby=limitby)
    #return db._lastsql
    totalCount=qset.count()
    
    
    return dict(records=records,totalCount=totalCount,page=page,items_per_page=items_per_page,access_permission=access_permission,access_permission_view=access_permission_view)

#=========================

def client_validation(form):
    cid=session.cid
    
    client_ID=str(request.vars.client_id).strip().upper()
    client_old_id=check_special_char_id(client_ID)
    
    depot_id=str(request.vars.depot_id).strip().upper().split('|')[0]
    store_id=str(request.vars.store_id).strip().upper().split('|')[0]
    
    if session.user_type=='Depot':
        depot_id=session.depot_id
        
    name_row=str(request.vars.name)
    name=check_special_char(name_row)
    form.vars.name=name
    
    area_id=str(request.vars.area_id).strip().upper().split('|')[0]
    
    address=str(request.vars.address)
    
    category_id=str(request.vars.category_id).strip()
    sub_category_id=str(request.vars.sub_category_id).strip()    
    depot_belt_name=str(request.vars.depot_belt_name).strip().title()
    
    market_id=str(request.vars.market_id).strip().split('|')[0]
    
    thana=str(request.vars.thana).strip().title()
    district_id=str(request.vars.district_id).strip()
    
    contact_no1=form.vars.contact_no1
    contact_no2=form.vars.contact_no2
    if contact_no1=='':
        contact_no1=0
    if contact_no2=='':
        contact_no2=0
    
    dipotId_rows_check=db((db.sm_depot.cid==cid) & (db.sm_depot.depot_id==depot_id)).select(db.sm_depot.depot_id,db.sm_depot.name,limitby=(0,1))
    if not dipotId_rows_check:
        form.errors.depot_id=''
        response.flash = 'Invalid Branch/Depot Id '
    else:
        depot_name=dipotId_rows_check[0].name
        
        store_rows_check=db((db.sm_depot_store.cid==cid) & (db.sm_depot_store.depot_id==depot_id) & (db.sm_depot_store.store_id==store_id)& (db.sm_depot_store.store_type=='SALES')).select(db.sm_depot_store.store_name,limitby=(0,1))
        if not store_rows_check:
            form.errors.store_id=''
            response.flash = 'Invalid Branch/Depot Store ID'
        else:
            store_name=store_rows_check[0].store_name
            
            #-----
            check_area=db((db.sm_level.cid==cid) & (db.sm_level.level_id==area_id) & (db.sm_level.is_leaf == '1')).select(db.sm_level.level_id,limitby=(0,1))
            if not check_area:
                form.errors.area_id='Invalid Territory'
            else:
                #----
                rows_check=db((db.sm_category_type.cid==cid) & (db.sm_category_type.type_name=='CLIENT_CATEGORY') &(db.sm_category_type.cat_type_id==category_id)).select(db.sm_category_type.cat_type_name,limitby=(0,1))
                if not rows_check:
                    form.errors.category_id=''
                    response.flash = 'Invalid Category'
                else:
                    cat_name=rows_check[0].cat_type_name
                    
                    #----
                    rows_check2=db((db.sm_category_type.cid==cid) & (db.sm_category_type.type_name=='CLIENT_SUB_CATEGORY') &(db.sm_category_type.cat_type_id==sub_category_id)).select(db.sm_category_type.cat_type_name,limitby=(0,1))
                    if not rows_check2:
                        form.errors.sub_category_id=''
                        response.flash = 'Invalid Sub Category'
                    else:
                        sub_cat_name=rows_check2[0].cat_type_name
                        
                        #-----
                        if depot_belt_name!='':
                            dipotBelt_rows_check=db((db.sm_depot_belt.cid==cid) & (db.sm_depot_belt.depot_id==depot_id) & (db.sm_depot_belt.belt_name==depot_belt_name)).select(db.sm_depot_belt.depot_id,limitby=(0,1))
                            if not dipotBelt_rows_check:
                                form.errors.depot_belt_name=''
                                response.flash = 'Invalid Belt of the Depot/Branch'
                            else:
                                pass
                        
                        rows_check3=db((db.sm_depot_market.cid==cid) & (db.sm_depot_market.depot_id==depot_id) & (db.sm_depot_market.market_id==market_id)).select(db.sm_depot_market.market_name,limitby=(0,1))
                        if not rows_check3:
                            form.errors.market_id=''
                            response.flash = 'Invalid Market of the Depot/Branch'
                        else:
                            market_name=rows_check3[0].market_name
                            
                            #----------
                            rows_check4=db((db.district.cid==cid) & (db.district.district_id==district_id)).select(db.district.name,limitby=(0,1))
                            if not rows_check4:
                                form.errors.district_id=''
                                response.flash = 'Invalid District'
                            else:
                                district_name=rows_check4[0].name
                        
                                #---------
                                if client_old_id!='':
                                    newClientId=depot_id+client_old_id
                                else:
                                    check_clientRow=db((db.sm_client.cid==cid) & ((db.sm_client.client_id.len()>10) & (db.sm_client.client_id.like('9%')))).select(db.sm_client.client_id,orderby=~db.sm_client.client_id,limitby=(0,1))
                                    if check_clientRow:
                                        newClientId=int(check_clientRow[0].client_id)+1
                                    else:
                                        newClientId='90000000001'
                                
                                #----------
                                check_client=db((db.sm_client.cid==cid) & (db.sm_client.client_id==newClientId)).select(db.sm_client.client_id,db.sm_client.client_id,limitby=(0,1))
                                if check_client:            
                                    form.errors.client_id=''
                                    response.flash = 'Duplicate Client Id '+ str(newClientId)
                                else:
                                    
                                    if len(address)>200:
                                        form.errors.address='enter maximum 200 character'
                                    else:                                        
                                        form.vars.client_id=newClientId
                                        form.vars.client_old_id=client_old_id
                                        form.vars.category_name=cat_name
                                        form.vars.sub_category_name=sub_cat_name
                                        
                                        form.vars.area_id=area_id
                                        form.vars.depot_id=depot_id
                                        form.vars.depot_name=depot_name
                                        form.vars.store_id=store_id
                                        form.vars.store_name=store_name
                                        
                                        form.vars.depot_belt_name=depot_belt_name
                                        
                                        form.vars.market_id=market_id
                                        form.vars.market_name=market_name
                                        form.vars.thana=thana
                                        form.vars.district=district_name
                                        form.vars.contact_no1=contact_no1
                                        form.vars.contact_no2=contact_no2
                            
def client_add():
    task_id='rm_client_manage'
    access_permission=check_role(task_id)
    if (access_permission==False):
        session.flash='Access is Denied !'
        redirect (URL('client'))        
        
    #   --------------------- 
    response.title='Client'   
    
    cid=session.cid
    
#     db.sm_client.thana_id.requires=IS_EMPTY_OR(IS_IN_DB(db(db.thana.cid == session.cid),db.thana.id,'%(district)s - %(name)s',orderby=db.thana.district|db.thana.name))
    db.sm_client.category_id.requires=IS_IN_DB(db((db.sm_category_type.cid == session.cid)&(db.sm_category_type.type_name=='CLIENT_CATEGORY')),db.sm_category_type.cat_type_id,'%(cat_type_id)s | %(cat_type_name)s',orderby=db.sm_category_type.cat_type_id)
    db.sm_client.sub_category_id.requires=IS_IN_DB(db((db.sm_category_type.cid == cid)&(db.sm_category_type.type_name=='CLIENT_SUB_CATEGORY')),db.sm_category_type.cat_type_id,'%(cat_type_id)s | %(cat_type_name)s',orderby=db.sm_category_type.cat_type_id)
    db.sm_client.district_id.requires=IS_IN_DB(db(db.district.cid == cid),db.district.district_id,'%(district_id)s | %(name)s',orderby=db.district.name)
    
    form =SQLFORM(db.sm_client,
                  fields=['client_id','name','area_id','depot_id','store_id','category_id','sub_category_id','depot_belt_name','owner_name','contact_no1','contact_no2','address','market_id','thana','district_id','drug_registration_num','nid','doctor','status'],
                  submit_button='Save'       
                  )
    
    form.vars.cid=cid
    if session.user_type=='Depot':
        form.vars.depot_id=str(session.depot_id)+'|'+str(session.user_depot_name)
        
    if form.accepts(request.vars,session,onvalidation=client_validation):
       session.flash = 'Submitted Successfully'
       redirect(URL('client'))
    
    return dict(form=form,access_permission=access_permission)


#-----------------client edit-------------------
def client_edit_validation(form):
    cid=session.cid
    
    depot_id=str(request.vars.depot_id).strip().upper().split('|')[0]
    store_id=str(request.vars.store_id).strip().upper().split('|')[0]
    if session.user_type=='Depot':
        depot_id=session.depot_id
        
    name_row=str(request.vars.name)
    name=check_special_char(name_row)
    form.vars.name=name
    
    area_id=str(request.vars.area_id).strip().upper().split('|')[0]
    
    address=str(request.vars.address)
    
    category_id=str(request.vars.category_id).strip()
    sub_category_id=str(request.vars.sub_category_id).strip()    
    depot_belt_name=str(request.vars.depot_belt_name).strip().title()
    
    market_id=str(request.vars.market_id).strip().split('|')[0]
    
    thana=str(request.vars.thana).strip().title()
    district_id=str(request.vars.district_id).strip()
    
    contact_no1=form.vars.contact_no1
    contact_no2=form.vars.contact_no2
    if contact_no1=='':
        contact_no1=0
    if contact_no2=='':
        contact_no2=0
    
    
    dipotId_rows_check=db((db.sm_depot.cid==cid) & (db.sm_depot.depot_id==depot_id)).select(db.sm_depot.depot_id,db.sm_depot.name,limitby=(0,1))
    if not dipotId_rows_check:
        form.errors.depot_id=''
        response.flash = 'Invalid Branch Id '
    else:
        depot_name=dipotId_rows_check[0].name
        store_rows_check=db((db.sm_depot_store.cid==cid) & (db.sm_depot_store.depot_id==depot_id) & (db.sm_depot_store.store_id==store_id)& (db.sm_depot_store.store_type=='SALES')).select(db.sm_depot_store.store_name,limitby=(0,1))
        if not store_rows_check:
            form.errors.store_id=''
            response.flash = 'Invalid Branch/Depot Store ID'
        else:
            store_name=store_rows_check[0].store_name
            #-----
            check_area=db((db.sm_level.cid==cid) & (db.sm_level.level_id==area_id) & (db.sm_level.is_leaf == '1')).select(db.sm_level.level_id,limitby=(0,1))
            if not check_area:
                form.errors.area_id='Invalid Territory'
            else:
                #----
                rows_check=db((db.sm_category_type.cid==cid) & (db.sm_category_type.type_name=='CLIENT_CATEGORY') &(db.sm_category_type.cat_type_id==category_id)).select(db.sm_category_type.cat_type_name,limitby=(0,1))
                if not rows_check:
                    form.errors.category_id=''
                    response.flash = 'Invalid Category'
                else:
                    cat_name=rows_check[0].cat_type_name
                    
                    #----
                    rows_check2=db((db.sm_category_type.cid==cid) & (db.sm_category_type.type_name=='CLIENT_SUB_CATEGORY') &(db.sm_category_type.cat_type_id==sub_category_id)).select(db.sm_category_type.cat_type_name,limitby=(0,1))
                    if not rows_check2:
                        form.errors.sub_category_id=''
                        response.flash = 'Invalid Sub Category'
                    else:
                        sub_cat_name=rows_check2[0].cat_type_name
                        
                        #-----
                        if depot_belt_name!='':
                            dipotBelt_rows_check=db((db.sm_depot_belt.cid==cid) & (db.sm_depot_belt.depot_id==depot_id) & (db.sm_depot_belt.belt_name==depot_belt_name)).select(db.sm_depot_belt.depot_id,limitby=(0,1))
                            if not dipotBelt_rows_check:
                                form.errors.depot_belt_name=''
                                response.flash = 'Invalid Belt of the Depot/Branch'
                            else:
                                pass
                        
                        rows_check3=db((db.sm_depot_market.cid==cid) & (db.sm_depot_market.depot_id==depot_id) & (db.sm_depot_market.market_id==market_id)).select(db.sm_depot_market.market_name,limitby=(0,1))
                        if not rows_check3:
                            form.errors.market_id=''
                            response.flash = 'Invalid Market of the Depot/Branch'
                        else:
                            market_name=rows_check3[0].market_name
                            
                            #----------
                            rows_check4=db((db.district.cid==cid) & (db.district.district_id==district_id)).select(db.district.name,limitby=(0,1))
                            if not rows_check4:
                                form.errors.district_id=''
                                response.flash = 'Invalid District'
                            else:
                                district_name=rows_check4[0].name
                                
                                #---------                            
                                if len(address)>200:
                                    form.errors.address='enter maximum 200 character'
                                else:
                                    
                                    form.vars.category_name=cat_name
                                    form.vars.sub_category_name=sub_cat_name
                                    
                                    form.vars.area_id=area_id
                                    form.vars.depot_id=depot_id
                                    form.vars.depot_name=depot_name
                                    form.vars.store_id=store_id
                                    form.vars.store_name=store_name
                                    form.vars.depot_belt_name=depot_belt_name                                        
                                    form.vars.market_id=market_id
                                    form.vars.market_name=market_name
                                    form.vars.thana=thana
                                    form.vars.district=district_name
                                    form.vars.contact_no1=contact_no1
                                    form.vars.contact_no2=contact_no2

def client_edit():
    task_id='rm_client_manage'
    task_id_view='rm_client_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL('client'))
    
    response.title='Client-Edit'
    cid=session.cid
    
    
    page=request.args(0)
    rowid=request.args(1)    
    record= db.sm_client(rowid)
        
    btn_reset_location=request.vars.btn_reset_location
    if btn_reset_location:
        location_checked=request.vars.location_checked        
        if location_checked=='YES':            
            records_update=db((db.sm_client.cid==cid) & (db.sm_client.id==rowid)).update(latitude='0',longitude='0')            
            response.flash = 'Location Reset Successful'
    
    #----------
    latValue=0
    longValue=0    
    client_id=''
    client_old_id=''
    photo=''
    depot_name=''
    store_name=''
    market_name=''
    district_name=''
    
    records_client=db((db.sm_client.cid==cid) & (db.sm_client.id==rowid)).select(db.sm_client.ALL,limitby=(0,1))
    if not records_client :
        session.flash='Invalid request'
        redirect (URL('client'))
    else:
        depot_id=str(records_client[0].depot_id)
        depot_name=str(records_client[0].depot_name)
        store_id=str(records_client[0].store_id)
        store_name=str(records_client[0].store_name)
        
        client_id=str(records_client[0].client_id)
        client_old_id=str(records_client[0].client_old_id)
        photo=records_client[0].photo        
        latValue=records_client[0].latitude
        longValue=records_client[0].longitude
        
        market_id=str(records_client[0].market_id)
        market_name=str(records_client[0].market_name)
        district_name=str(records_client[0].district)
        area_id=str(records_client[0].area_id)
        area_name=''        
        check_area=db((db.sm_level.cid==cid) & (db.sm_level.level_id==area_id) & (db.sm_level.is_leaf == '1')).select(db.sm_level.level_name,limitby=(0,1))
        if check_area:
            area_name=check_area[0].level_name
            
    #-----------    
    db.sm_client.category_id.requires=IS_IN_DB(db((db.sm_category_type.cid == cid)&(db.sm_category_type.type_name=='CLIENT_CATEGORY')),db.sm_category_type.cat_type_id,'%(cat_type_id)s | %(cat_type_name)s',orderby=db.sm_category_type.cat_type_id)
    db.sm_client.sub_category_id.requires=IS_IN_DB(db((db.sm_category_type.cid == cid)&(db.sm_category_type.type_name=='CLIENT_SUB_CATEGORY')),db.sm_category_type.cat_type_id,'%(cat_type_id)s | %(cat_type_name)s',orderby=db.sm_category_type.cat_type_id)
    db.sm_client.district_id.requires=IS_IN_DB(db(db.district.cid == cid),db.district.district_id,'%(district_id)s | %(name)s',orderby=db.district.name)
    
    form =SQLFORM(db.sm_client,
                  record=record,
                  deletable=False,
                  fields=['name','area_id','depot_id','store_id','category_id','sub_category_id','depot_belt_name','owner_name','contact_no1','contact_no2','address','market_id','thana','district_id','drug_registration_num','nid','doctor','status'],
                  submit_button='Update'
                  )
    #upload=URL('download'),
    #--------------
    
    form.vars.depot_id=depot_id+'|'+depot_name
    form.vars.store_id=store_id+'|'+store_name
    form.vars.market_id=market_id+'|'+market_name
    form.vars.area_id=area_id+'|'+area_name
    
    if form.accepts(request.vars, session,onvalidation=client_edit_validation):
        session.flash = 'Updated Successfully'        
        redirect(URL('client'))
    
#     elif form.errors:
#         for fieldname in form.errors:
#             response.flash = form.errors[fieldname]
#             break
    
    #------------------
    useFlag=False
#    rows=db((db.sm_client_user.cid==session.cid) & (db.sm_client_user.client_id==client_id)).select(db.sm_client_user.client_id,limitby=(0,1))
#    if rows:
#        useFlag=True
    
    sl=''
    rep_id=''
    rep_name=''
    order_date=''
    visit_type=''
    mobile_no=''    
    visitRows=db((db.sm_order_head.cid==cid) & (db.sm_order_head.client_id==client_id)).select(db.sm_order_head.sl,db.sm_order_head.rep_id,db.sm_order_head.rep_name,db.sm_order_head.order_date,db.sm_order_head.visit_type,db.sm_order_head.mobile_no,orderby=~db.sm_order_head.sl,limitby=(0,1))
    if visitRows:
        sl=visitRows[0].sl
        rep_id=visitRows[0].rep_id
        rep_name=visitRows[0].rep_name
        order_date=visitRows[0].order_date
        visit_type=visitRows[0].visit_type
        mobile_no=visitRows[0].mobile_no
        useFlag=True
    else:
        invoiceRows=db((db.sm_invoice_head.cid==cid) & (db.sm_invoice_head.client_id==client_id)).select(db.sm_invoice_head.cid,limitby=(0,1))
        if invoiceRows:
            useFlag=True
        else:
            paymentRows=db((db.sm_client_payment.cid==cid) & (db.sm_client_payment.client_id==client_id)).select(db.sm_client_payment.cid,limitby=(0,1))
            if paymentRows:
                useFlag=True
            else:
                ledgerRows=db((db.sm_transaction.cid==cid) & (db.sm_transaction.tx_account=='CLT-'+str(client_id))).select(db.sm_transaction.cid,limitby=(0,1))
                if ledgerRows:
                    useFlag=True
    #----------
    return dict(form=form,rowid=rowid,client_id=client_id,client_old_id=client_old_id,depot_name=depot_name,store_name=store_name,market_name=market_name,photo=photo,sl=sl,latValue=latValue,longValue=longValue,rep_id=rep_id,rep_name=rep_name,order_date=order_date,visit_type=visit_type,mobile_no=mobile_no,access_permission=access_permission,page=page,useFlag=useFlag)

#------------ClientProfile-------------
def client_profile():
    task_id='rm_client_manage'
    task_id_view='rm_client_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL('client'))
    
    response.title='Client-Profile'
    cid=session.cid
    
    #----------------    
    client_id=request.vars.client_id
    
    records=db((db.sm_client.cid==cid) & (db.sm_client.client_id==client_id)).select(db.sm_client.ALL,limitby=(0,1))
    photo=''
    territory_name=''
    if not records :
        session.flash='Invalid Client'
        redirect (URL('client'))
    else:
        photo=records[0].photo
        market_id=records[0].area_id
                
        levelRow=db((db.sm_level.cid==cid) & (db.sm_level.level_id==market_id)).select(db.sm_level.level_name,limitby=(0,1))
        if levelRow:
            territory_name=levelRow[0].level_name
    
    #------------------ Last visit   
    vsl=''
    sl=''
    rep_id=''
    rep_name=''
    order_date=''
    visit_type=''
    mobile_no=''    
    visitRows=db((db.sm_order_head.cid==cid) & (db.sm_order_head.client_id==client_id)).select(db.sm_order_head.id,db.sm_order_head.sl,db.sm_order_head.rep_id,db.sm_order_head.rep_name,db.sm_order_head.order_date,db.sm_order_head.visit_type,db.sm_order_head.mobile_no,orderby=~db.sm_order_head.sl,limitby=(0,1))
    if visitRows:
        vsl=visitRows[0].id
        sl=visitRows[0].sl
        rep_id=visitRows[0].rep_id
        rep_name=visitRows[0].rep_name
        order_date=visitRows[0].order_date
        visit_type=visitRows[0].visit_type
        mobile_no=visitRows[0].mobile_no
    
    return dict(records=records,client_id=client_id,territory_name=territory_name,photo=photo,sl=vsl,rep_id=rep_id,rep_name=rep_name,order_date=order_date,visit_type=visit_type,mobile_no=mobile_no)
    
#====================================== CLIENT BATCH UPLOAD ---------- (Billal)

def client_batch_upload():
    task_id='rm_client_manage'
    access_permission=check_role(task_id)
    if access_permission==False:
        session.flash='Access is Denied !'
        redirect (URL('client','client'))
    
    response.title='Client Batch Upload'
    
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
        
        client_list_excel=[]
        branch_list_excel=[]
        area_list_excel=[]
        district_exist=[]
        
        client_category_exist=[]
        client_sub_category_exist=[]
        branch_list_exist=[]
        depot_exist=[]
        
        excelList=[]
        existLevel_list=[]
        
        ins_list=[]
        ins_dict={}
        
        for i in range(total_row):
            if i>=500:
                break
            else:
                row_data=row_list[i]                    
                coloum_list=row_data.split( '\t')
#                 return len(coloum_list)
                if len(coloum_list)==18:
#                     return str(coloum_list[2])
                    area_list_excel.append(str(coloum_list[2]).strip().upper())
                    depotIdExcel=str(coloum_list[3]).strip().upper()
                    if depotIdExcel not in branch_list_excel:
                        branch_list_excel.append(depotIdExcel)
                        
        
        clCategoryRows=db((db.sm_category_type.cid==c_id)&(db.sm_category_type.type_name=='CLIENT_CATEGORY')).select(db.sm_category_type.cat_type_id,db.sm_category_type.cat_type_name,orderby=db.sm_category_type.cat_type_id)
        client_category_exist=clCategoryRows.as_list()
        
        clSubCategoryRows=db((db.sm_category_type.cid==c_id)&(db.sm_category_type.type_name=='CLIENT_SUB_CATEGORY')).select(db.sm_category_type.cat_type_id,db.sm_category_type.cat_type_name,orderby=db.sm_category_type.cat_type_id)
        client_sub_category_exist=clSubCategoryRows.as_list()
        
        if session.user_type=='Depot':
            depotRows=db((db.sm_depot.cid == c_id)&(db.sm_depot.depot_id==session.depot_id)&(db.sm_depot.status=='ACTIVE')).select(db.sm_depot.depot_id,db.sm_depot.name,orderby=db.sm_depot.depot_id)
        else:
            depotRows=db((db.sm_depot.cid == c_id)&(db.sm_depot.depot_id.belongs(branch_list_excel))&(db.sm_depot.status=='ACTIVE')).select(db.sm_depot.depot_id,db.sm_depot.name,orderby=db.sm_depot.depot_id)
        depot_exist=depotRows.as_list()
        
        districtRows=db(db.district.cid==c_id).select(db.district.district_id,db.district.name,orderby=db.district.district_id)
        district_exist=districtRows.as_list()
#         return area_list_excel 
        existLevelRows=db((db.sm_level.cid==c_id) & (db.sm_level.is_leaf=='1') & (db.sm_level.level_id.belongs(area_list_excel))).select(db.sm_level.level_id,db.sm_level.level_name,orderby=db.sm_level.level_id)
        
        existLevel_list=existLevelRows.as_list()
#         return existLevelRows
        #   --------------------
        for i in range(total_row):
            if i>=500:
                break
            else:
                row_data=row_list[i]
            coloum_list=row_data.split( '\t')
            
            if len(coloum_list)!=18:
                error_data=row_data+'(18 columns need in a row)\n'
                error_str=error_str+error_data
                count_error+=1
                continue
            else:
                clID_ex=str(coloum_list[0]).strip().upper()
                cl_name_ex=str(coloum_list[1]).strip() 
                territory_ex=str(coloum_list[2]).strip()        
                branch_ex=str(coloum_list[3]).strip()  
                store_ex=str(coloum_list[4]).strip()  
                category_ex=str(coloum_list[5]).strip()
                sub_category_ex=str(coloum_list[6]).strip()
                depotbelt_ex=str(coloum_list[7]).strip().title()
                ownername_ex=str(coloum_list[8]).strip()           
                contact1_ex=coloum_list[9]
                contact2_ex=coloum_list[10]
                address_ex=str(coloum_list[11]).strip()
                market_ex=str(coloum_list[12]).strip().title()
                thana_ex=str(coloum_list[13]).title()
                district_ex=str(coloum_list[14]).title()
                drug_reg_num_ex=str(coloum_list[15]).strip()
                nid_ex=str(coloum_list[16]).strip()
                doctor_ex=str(coloum_list[17]).strip()
                client_old_id=''
                
                try:
                    contact1_ex=int(contact1_ex)                    
                except:
                    contact1_ex=0
                    
                try:
                    contact2_ex=int(contact2_ex)                    
                except:
                    contact2_ex=0
                    
                try:
                    nid_ex=int(nid_ex)
                except:
                    nid_ex=0
                    
                if clID_ex!='':
                    newClientId=branch_ex+clID_ex
                    client_old_id=clID_ex
                else:
                    check_clientRow=db((db.sm_client.cid==c_id) & ((db.sm_client.client_id.len()>10) & (db.sm_client.client_id.like('9%')))).select(db.sm_client.client_id,orderby=~db.sm_client.client_id,limitby=(0,1))
                    if check_clientRow:
                        newClientId=int(check_clientRow[0].client_id)+1
                    else:
                        newClientId='90000000001'
                        
                clID_ex=newClientId
                
                #----------
                if (cl_name_ex=='' or territory_ex=='' or branch_ex=='' or store_ex=='' or category_ex=='' or sub_category_ex=='' or market_ex=='' or thana_ex=='' or district_ex=='' or doctor_ex=='' ):
                    error_data=row_data+'(Must value required)\n'
                    error_str=error_str+error_data
                    count_error+=1
                    continue
                else:
                    
                    #-----------------------
                    duplicate_client=False
                    valid_area=False
                    valid_category=False
                    valid_sub_category=False
                    valid_depot=False
                    valid_distrct=False
                    
                    depotID=''
                    depot_name=''
                    store_name=''
                    category_name=''
                    sub_category_name=''
                    market_name=''
                    district_name=''
                    territory_id=''
                    #----------- check duplicate client id                                                       
                    check_client=db((db.sm_client.cid==c_id) & (db.sm_client.client_id==newClientId)).select(db.sm_client.client_id,db.sm_client.client_id,limitby=(0,1))
                    if check_client:            
                        duplicate_client=True
                    else:
                        pass
                    
                    
                    if duplicate_client==False:#---------- check valid territory        
                          
                                                          
                        for i in range(len(existLevel_list)):
                            
                            myRowData=existLevel_list[i]                        
                            level_name=myRowData['level_id']       
#                             return level_name                  
                            if (str(level_name).strip()==str(territory_ex).strip().upper()):                                
                                valid_area=True
                                territory_id=myRowData['level_id']   
#                                 return     territory_id                            
                                break
                    
                    if valid_area==True:#---------- check valid depot                                                  
                        for i in range(len(depot_exist)):
                            myRowData=depot_exist[i]                        
                            depotID=myRowData['depot_id']                            
                            if (str(depotID).strip()==str(branch_ex).strip()):                                
                                valid_depot=True
                                depot_name=myRowData['name']                 
                                break
                    
                    if valid_depot==True:
                        storeRow=db((db.sm_depot_store.cid==c_id) & (db.sm_depot_store.depot_id==branch_ex) & (db.sm_depot_store.store_id==store_ex)& (db.sm_depot_store.store_type=='SALES')).select(db.sm_depot_store.store_name,limitby=(0,1))
                        if not storeRow:
                            error_data=row_data+'(Invalid Store ID of the Depot/Branch!)\n'
                            error_str=error_str+error_data
                            count_error+=1
                            continue                                        
                        else:
                            store_name=storeRow[0].store_name
                    
                    if valid_area==True:#---------- check valid category                                        
                        for i in range(len(client_category_exist)):
                            myRowData=client_category_exist[i]                        
                            cat_type_id=myRowData['cat_type_id']
                            if (str(cat_type_id).strip()==str(category_ex).strip()):
                                valid_category=True
                                category_name=myRowData['cat_type_name']                         
                                break
                                
                    if valid_category==True:#---------- check valid category                                        
                        for i in range(len(client_sub_category_exist)):
                            myRowData=client_sub_category_exist[i]                        
                            cat_type_id=myRowData['cat_type_id']
                            if (str(cat_type_id).strip()==str(sub_category_ex).strip()):
                                valid_sub_category=True
                                sub_category_name=myRowData['cat_type_name']                             
                                break
                    
                    if valid_sub_category==True:#---------- check valid category                                        
                        for i in range(len(district_exist)):
                            myRowData=district_exist[i]                        
                            district_id=myRowData['district_id']
                            if (str(district_id).strip()==str(district_ex).strip()):
                                valid_distrct=True
                                district_name=myRowData['name']                             
                                break
                            
                    #-----------------
                    if(duplicate_client==True):
                        error_data=row_data+'(duplicate client!)\n'
                        error_str=error_str+error_data
                        count_error+=1
                        continue
                    else:
                        if valid_area==False:
                            error_data=row_data+'(invalid Territory!)\n'
                            error_str=error_str+error_data
                            count_error+=1
                            continue
                        else:
                            if valid_depot==False:
                                error_data=row_data+'(invalid/inactive Depot!)\n'
                                error_str=error_str+error_data
                                count_error+=1
                                continue
                            else:
                                
                                if valid_category==False:
                                    error_data=row_data+'(invalid category!)\n'
                                    error_str=error_str+error_data
                                    count_error+=1
                                    continue
                                else:
                                    if valid_sub_category==False:
                                        error_data=row_data+'(invalid Sub category!)\n'
                                        error_str=error_str+error_data
                                        count_error+=1
                                        continue
                                    else:
                                        if valid_distrct==False:
                                            error_data=row_data+'(invalid District!)\n'
                                            error_str=error_str+error_data
                                            count_error+=1
                                            continue
                                        else:
                                            marketRow=db((db.sm_depot_market.cid==c_id) & (db.sm_depot_market.depot_id==branch_ex) & (db.sm_depot_market.market_id==market_ex)).select(db.sm_depot_market.market_name,limitby=(0,1))
                                            if not marketRow:                                                    
                                                error_data=row_data+'(Invalid Market of the Depot/Branch)\n'
                                                error_str=error_str+error_data
                                                count_error+=1
                                                continue                                                    
                                            else:
                                                market_name=marketRow[0].market_name
                                                
                                                if depotbelt_ex!='':
                                                    dipotBelt_rows_check=db((db.sm_depot_belt.cid==c_id) & (db.sm_depot_belt.depot_id==branch_ex) & (db.sm_depot_belt.belt_name==depotbelt_ex)).select(db.sm_depot_belt.depot_id,limitby=(0,1))
                                                    if not dipotBelt_rows_check:
                                                        error_data=row_data+'(Invalid Belt of the Depot/Branch!)\n'
                                                        error_str=error_str+error_data
                                                        count_error+=1
                                                        continue                                        
                                                    else:
                                                        pass
                                                
                                                try:
                                                    #------------
                                                    db.sm_client.insert(cid=c_id,client_id=clID_ex,client_old_id=client_old_id,name=cl_name_ex,area_id=territory_id,depot_id=branch_ex,depot_name=depot_name,store_id=store_ex,store_name=store_name,category_id=category_ex,category_name=category_name,sub_category_id=sub_category_ex,sub_category_name=sub_category_name,depot_belt_name=depotbelt_ex,owner_name=ownername_ex,contact_no1=contact1_ex,contact_no2=contact2_ex,address=address_ex,market_id=market_ex,market_name=market_name,thana=thana_ex,district_id=district_ex,district=district_name,drug_registration_num=drug_reg_num_ex,nid=nid_ex,doctor=doctor_ex)
                                                    count_inserted+=1                                                    
                                                    #-------------
                                                except:
                                                    error_data=row_data+'(error in process!)\n'
                                                    error_str=error_str+error_data
                                                    count_error+=1
                                                    continue
                                                
        if error_str=='':
            error_str='No error'
                  
            
    return dict(count_inserted=count_inserted,count_error=count_error,error_str=error_str,total_row=total_row)


def client_territory_update():
    task_id='rm_client_manage'
    access_permission=check_role(task_id)
    if access_permission==False:
        session.flash='Access is Denied !'
        redirect (URL('client','client'))
    
    response.title='Client Batch Upload'
    
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
        
        area_list_excel=[]
                
        ins_list=[]
        ins_dict={}
        
        for i in range(total_row):
            if i>=100:
                break
            else:
                row_data=row_list[i]                    
                coloum_list=row_data.split( '\t')
                if len(coloum_list)==2:                    
                    territoryID=str(coloum_list[1]).strip().upper()                    
                    if territoryID not in area_list_excel:
                        area_list_excel.append(territoryID)
                        
        #----------
        existLevelRows=db((db.sm_level.cid==c_id)&(db.sm_level.is_leaf=='1')&(db.sm_level.level_id.belongs(area_list_excel))).select(db.sm_level.level_id,db.sm_level.level_name,orderby=db.sm_level.level_id)
        existLevel_list=existLevelRows.as_list()
        
        #   --------------------
        for i in range(total_row):
            if i>=100:
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
                clID_ex=str(coloum_list[0]).strip().upper()                
                territory_ex=str(coloum_list[1]).strip().upper()
                
                #----------
                if (clID_ex=='' or territory_ex==''):
                    error_data=row_data+'(Must value required)\n'
                    error_str=error_str+error_data
                    count_error+=1
                    continue
                else:                    
                    #-----------------------                    
                    valid_area=False
                    
                    #---------- check valid territory                                                  
                    for i in range(len(existLevel_list)):
                        myRowData=existLevel_list[i]                        
                        level_id=myRowData['level_id']                            
                        if (str(level_id).strip()==str(territory_ex).strip().upper()):                                
                            valid_area=True                                
                            break
                    
                    #-----------------                    
                    if valid_area==False:
                        error_data=row_data+'(Invalid Territory)\n'
                        error_str=error_str+error_data
                        count_error+=1
                        continue
                    else:
                        check_client=db((db.sm_client.cid==c_id) &(db.sm_client.depot_id==session.depot_id) & (db.sm_client.client_id==clID_ex)).select(db.sm_client.id,limitby=(0,1))
                        if not check_client:            
                            error_data=row_data+'(Invalid client ID)\n'
                            error_str=error_str+error_data
                            count_error+=1
                            continue
                        else:
                            check_client[0].update_record(area_id=territory_ex)
                            count_inserted+=1                                                    
        
        if error_str=='':
            error_str='No error'
            
    return dict(count_inserted=count_inserted,count_error=count_error,error_str=error_str,total_row=total_row)



#===================================== Download

def download_client():
    #----------Task assaign----------
    task_id='rm_client_manage'
    task_id_view='rm_client_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL('client','client'))      
        
    #   ---------------------
    c_id=session.cid
    records=''
    
    qset=db()
    qset=qset(db.sm_client.cid==session.cid)
    
    #---- supervisor
    if session.user_type=='Supervisor':
        level_id=session.level_id
        depthNo=session.depthNo
        level = 'level' + str(depthNo)
        
        qset=qset((db.sm_level.cid==session.cid)&(db.sm_level.is_leaf=='1')& (db.sm_level[level] == level_id)&(db.sm_level.level_id==db.sm_client.area_id))
        
    else:
        qset=qset((db.sm_level.cid==session.cid)&(db.sm_level.is_leaf=='1')&(db.sm_level.level_id==db.sm_client.area_id))
    
    if session.user_type=='Depot':
        qset=qset(db.sm_client.depot_id==session.depot_id)    
    else:
        if (session.btn_filter_client and session.search_type_client=='DepotID'):
            searchValue=str(session.search_value_client).split('|')[0]
            qset=qset(db.sm_client.depot_id==searchValue)
    
    if (session.search_type_client=='ClientID'):
        searchValue=str(session.search_value_client).split('|')[0]
        qset=qset(db.sm_client.client_id==searchValue)
        
    elif (session.search_type_client=='AreaID'):
        searchValue=str(session.search_value_client).split('|')[0]
        qset=qset(db.sm_client.area_id==searchValue)
    
    elif (session.search_type_client=='District'):
            searchValue=str(session.search_value_client).split('|')[0]         
            qset=qset(db.sm_client.district_id==searchValue)
            
    elif (session.search_type_client=='Region'):
        searchValue=str(session.search_value_client).split('|')[0]         
        qset=qset(db.sm_level.level0==searchValue)
    
    else:
        session.flash='Need filter by '+str(session.level0Name)+'/District/Market/Client'
        redirect(URL('client'))
        
    records=qset.select(db.sm_client.ALL,db.sm_level.level_name,db.sm_level.level0,orderby=db.sm_client.name)
    
    #---------
    myString='Client List \n\n'
    myString+='Client New ID,Client Old ID,Name,Territory ID,Territory Name,Branch/Depot ID, Branch/Depot Name,Store ID,Store Name,Category ID,Category Name,Sub Category,Sub Category Name,Branch Belt,Contact Name,Contact1,Contact2,Address,Market ID,Market Name,Thana,District ID,District Name,Drug Registration Number,NID,Doctor,Status,\n'
    for rec in records:
        client_id=str(rec.sm_client.client_id)
        client_old_id=str(rec.sm_client.client_old_id)
        name=str(rec.sm_client.name).replace(',', ' ')
        area_id=str(rec.sm_client.area_id)
        depot_id=str(rec.sm_client.depot_id)
        depot_name=str(rec.sm_client.depot_name).replace(',', ' ')        
        level_name=str(rec.sm_level.level_name).replace(',', ' ')
        level0=str(rec.sm_level.level0)  
        
        store_id=str(rec.sm_client.store_id)
        store_name=str(rec.sm_client.store_name).replace(',', ' ')   
              
        category_id=str(rec.sm_client.category_id)
        category_name=str(rec.sm_client.category_name)
        sub_category_id=str(rec.sm_client.sub_category_id)
        sub_category_name=str(rec.sm_client.sub_category_name)
        depot_belt_name=str(rec.sm_client.depot_belt_name).replace(',', ' ')
        owner_name=str(rec.sm_client.owner_name).replace(',', ' ')
        contact_no1=str(rec.sm_client.contact_no1)
        contact_no2=str(rec.sm_client.contact_no2)
        address=str(rec.sm_client.address).replace(',', ' ')   
        
        market_id=str(rec.sm_client.market_id)
        market_name=str(rec.sm_client.market_name).replace(',', ' ') 
             
        thana=str(rec.sm_client.thana)
        district_id=str(rec.sm_client.district_id)
        district=str(rec.sm_client.district)
        nid=str(rec.sm_client.nid)
        drug_registration_num=str(rec.sm_client.drug_registration_num)
        doctor=str(rec.sm_client.doctor)
        status=str(rec.sm_client.status)

#         +level_name+','+level0+','
        myString+='`'+client_id+','+client_old_id+','+name+','+area_id+','+level_name+','+depot_id+','+depot_name+','+store_id+','+store_name+','+category_id+','+category_name+','+sub_category_id+','+sub_category_name+','+\
        depot_belt_name+','+owner_name+','+contact_no1+','+contact_no2+','+address+','+market_id+','+market_name+','+thana+','+district_id+','+district+','+drug_registration_num+','+nid+','+doctor+','+status+'\n'
        
    #-----------
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_client.csv'   
    return str(myString)
    
#===================================== Download client_without_matching_territory
def downlaod_client_without_matching_territory():
    #----------Task assaign----------
    task_id='rm_client_manage'
    task_id_view='rm_client_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL('client','client'))      
        
    #   ---------------------
    c_id=session.cid
    records=''
    
    sqlStr="select client_id,client_old_id,name,area_id,address,market_id,market_name,status from sm_client where cid='"+c_id+"' and depot_id='"+session.depot_id+"' and area_id NOT IN(select level_id from sm_level where cid='"+c_id+"' and is_leaf='1') order by name"
    recordList=db.executesql(sqlStr,as_dict = True)
    
    #---------
    myString='Client List without matching territory\n'
    myString+='Client New ID,Client Old ID,Name,Territory ID,Address,Market ID,Market Name,Status\n'
    for i in range(len(recordList)):
        dataDict=recordList[i]
        
        client_id=str(dataDict['client_id'])
        client_old_id=str(dataDict['client_old_id'])
        name=str(dataDict['name']).replace(',', ' ')
        area_id=str(dataDict['area_id'])
        
        address=str(dataDict['address']).replace(',', ' ')   
        
        market_id=str(dataDict['market_id'])
        market_name=str(dataDict['market_name']).replace(',', ' ') 
        
        status=str(dataDict['status'])
        
        myString+=client_id+','+client_old_id+','+name+','+area_id+','+address+','+market_id+','+market_name+','+status+'\n'
        
    #-----------
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_client_without_match_terr.csv'   
    return str(myString)


def download():    
    return response.download(request, db)



