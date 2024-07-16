#---------------Notice-----------------------
def notice_validation(form):
   
    if (session.cid!=''):
        limitby=(0,1)
        rows_check=db(db.sm_notice.cid==session.cid) .select(db.sm_notice.sl, orderby= ~db.sm_notice.sl,limitby=limitby)
#        form.errors.notice_date=''
        
#        return rows_check
        
        sl=0
        for row in rows_check:
            sl=row.sl
        sl=sl+1    
        form.vars.sl=sl
        form.vars.cid=session.cid


def notice(): 
    response.title='Notice'    
       #----------Task assaign----------
    task_id='rep_manage'
    task_id_view='rep_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (task_id_view==False):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))
        

    form =SQLFORM(db.sm_notice,
                  fields=['notice_date','notice']
                           
                  )
    
    notice=request.vars.notice

   
    if form.accepts(request.vars,session,onvalidation=notice_validation):
       response.flash = 'Data Submitted Successfully'

    #------------------------
    btn_filter_doctor=request.vars.btn_filter_doctor
    btn_doctor_all=request.vars.btn_doctor_all
    if btn_filter_doctor:
        session.search_type_doctor=request.vars.search_type
        session.search_value=request.vars.search_value
    elif btn_doctor_all:
        session.search_type_doctor=''
        session.search_value=''
    
    #--------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=session.items_per_page
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #--------end paging    

    #   --------------------------- filter--------------------------
    
    records=db((db.sm_notice.cid==session.cid) ).select(db.sm_notice.ALL,
        orderby=~db.sm_notice.notice_date,limitby=limitby)
#------------------------------------ filter end--------------------
    return dict(form=form,records=records,page=page,items_per_page=items_per_page,access_permission=access_permission)
#---------------end  doctor-----------------------



#-----------------doctor edit---------------------

def notice_edit():
    response.title='Notice'
    page= request.args(0)
    record= db.sm_notice(request.args(1)) #or redirect(URL('index'))   

    form =SQLFORM(db.sm_notice,
                  record=record,
                  deletable=True,
                  fields=['notice_date','notice']
                  )
    
    records=db((db.sm_notice.cid==session.cid) & (db.sm_notice.id==request.args(1))).select(db.sm_notice.notice)
    notice_show=''
    
    
    for records_show in records :
         notice_show=records_show.notice  
         break   
    notice=request.vars.notice

    if form.accepts(request.vars, session):
        response.flash = 'Data Update Successfully'        
        redirect(URL('notice',args=[page]))
        
    return dict(form=form,notice_show=notice_show)

#------------------Notice end----------------------




#---------------Payment Type-----------------------
def pay_type_validation(form):
   
    paytype=request.vars.paytype
   

    if ((paytype!='') and (session.cid!='')):
        rows_check=db((db.sm_paytype.cid==session.cid) & (db.sm_paytype.paytype==paytype.upper())).select(db.sm_paytype.paytype)
        if rows_check:
            form.errors.paytype=''
            response.flash = 'please choose a new '
            valid_business=False
        
        else:
            form.vars.paytype=paytype.upper()
            form.vars.cid=session.cid
        


def pay_type():    
    response.title='Pay Type' 
       #----------Task assaign----------
    task_id='rep_manage'
    task_id_view='rep_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (task_id_view==False):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))
        

    form =SQLFORM(db.sm_paytype,
                  fields=['paytype','detail']
                           
                  )
    
    if form.accepts(request.vars,session,onvalidation=pay_type_validation):
       response.flash = 'Data Submitted Successfully'

    #------------------------
    btn_filter_doctor=request.vars.btn_filter_doctor
    btn_doctor_all=request.vars.btn_doctor_all
    if btn_filter_doctor:
        session.search_type_doctor=request.vars.search_type
        session.search_value=request.vars.search_value
    elif btn_doctor_all:
        session.search_type_doctor=''
        session.search_value=''
    
    #--------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=session.items_per_page
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #--------end paging    

    #   --------------------------- filter--------------------------
    
    records=db((db.sm_paytype.cid==session.cid) ).select(db.sm_paytype.ALL,
        orderby=db.sm_paytype.paytype,limitby=limitby)
#------------------------------------ filter end--------------------
    return dict(form=form,records=records,page=page,items_per_page=items_per_page,access_permission=access_permission)
#---------------end  pay type-----------------------



#-----------------pay type edit---------------------


    

def pay_type_edit():
    response.title='pay Type'
    page= request.args(0)
    record= db.sm_paytype(request.args(1)) #or redirect(URL('index'))   

    form =SQLFORM(db.sm_paytype,
                  record=record,
                  deletable=True,
                  fields=['detail']
                  )
    
    records=db((db.sm_paytype.cid==session.cid) & (db.sm_paytype.id==request.args(1))).select(db.sm_paytype.paytype)
    paytype_show=''

    for records_show in records :
         paytype_show=records_show.paytype     
         break

    if form.accepts(request.vars, session):
        response.flash = 'Data Update Successfully'        
        redirect(URL('pay_type',args=[page]))
        
    return dict(form=form,paytype_show=paytype_show)

#------------------pay type end----------------------


#------------------TARGET--------------------------


def target_validation(form):
    cid=session.cid
    
    depot_id=str(request.vars.depot_id).upper()
    ym_date=str(request.vars.ym_date)[0:7]
    ym_date=ym_date+'-01'
    rep_id=str(request.vars.rep_id).upper()
    item_id=str(request.vars.item_id).upper()

    
    rows_check=db((db.sm_target.cid==cid) & (db.sm_target.depot_id==depot_id)& (db.sm_target.ym_date==ym_date)& (db.sm_target.rep_id==rep_id)& (db.sm_target.item_id==item_id)).select(db.sm_target.item_id)
    if rows_check:
        form.errors.depot_id=''
        response.flash = 'please choose a new '
    else:
        repRecords=db((db.sm_rep.cid==cid)& (db.sm_rep.depot_id==depot_id) & (db.sm_rep.rep_id==rep_id)& (db.sm_rep.status=='ACTIVE')).select(db.sm_rep.name)
        if repRecords:
            itemRecords=db((db.sm_item.cid==cid)&(db.sm_item.item_id==item_id)).select(db.sm_item.item_id,db.sm_item.name)
            if itemRecords:
                rep_name=repRecords[0].name
                item_name=itemRecords[0].name
                
                form.vars.cid=cid
                form.vars.depot_id=depot_id
                form.vars.ym_date=ym_date
                form.vars.rep_id=rep_id
                form.vars.rep_name=rep_name
                form.vars.item_id=item_id
                form.vars.item_name=item_name
                
            else:  
                form.errors.depot_id=''                
                response.flash='Invalid Item ID!'
        else:
            form.errors.depot_id=''                
            response.flash='Invalid Rep ID!'
                
        
def target():  
    response.title='Target'   
    cid=session.cid
    #----------Task assaign----------
    task_id='mrep_target_manage'
    task_id_view='mrep_target_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (task_id_view==False):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))
    
    db.sm_target.depot_id.requires=IS_IN_DB(db((db.sm_depot.cid==cid)&(db.sm_depot.status=='ACTIVE')),db.sm_depot.depot_id,orderby=db.sm_depot.depot_id)
    form =SQLFORM(db.sm_target,
                  fields=['depot_id','ym_date','rep_id','item_id','target_qty','achievement_qty','target_amount','achievement_amount'],
                  submit_button='Save'
                )
    
    if form.accepts(request.vars,session,onvalidation=target_validation):
       response.flash = 'Submitted Successfully'
    
    #------------------
#    dpotList=[]
#    dRows=db((db.sm_depot.cid==cid)&(db.sm_depot.status=='ACTIVE')).select(db.sm_depot.depot_id,orderby=db.sm_depot.depot_id)
#    for dRow in dRows:
#        d_id=dRow.depot_id
#        dpotList.append(d_id)
    
    #------------------------
    btn_filter_target=request.vars.btn_filter
    btn_all=request.vars.btn_all
    if btn_filter_target:
        session.btn_filter_target=btn_filter_target
        session.search_value_target=request.vars.depot_id_value
    elif btn_all:
        session.btn_filter_target=None
        session.search_value_target=None
    
    #--------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #--------end paging    
    
    qset=db()
    qset=qset(db.sm_target.cid==cid)
    
    if (session.user_type=='Depot'):
        qset=qset(db.sm_target.depot_id==str(session.depot_id))
        
    if (session.btn_filter_target):
        searchValue=str(session.search_value_target).split('-')[0]
        
        if (session.user_type!='Depot'):
            qset=qset(db.sm_target.depot_id==searchValue)
        
    records=qset.select(db.sm_target.ALL,orderby=db.sm_target.depot_id,limitby=limitby)
    
    return dict(form=form,records=records,page=page,items_per_page=items_per_page,access_permission=access_permission)

#---------------end  target-----------------------



#-----------------target edit---------------------
def target_edit():
    response.title='Target-Edit' 
    page= request.args(0)
    record= db.sm_target(request.args(1))

    form =SQLFORM(db.sm_target,
                  record=record,
                  deletable=True,
                  fields=['target_qty','achievement_qty','target_amount','achievement_amount'],
                  submit_button='Update'
                  )
    
    records=db((db.sm_target.cid==session.cid) & (db.sm_target.id==request.args(1))).select(db.sm_target.ALL)
    for row in records:
        depotId=row.depot_id
        ymDate=str(row.ym_date)[0:7]
        repId=row.rep_id
        itemId=row.item_id
        break

    if form.accepts(request.vars, session):
        session.flash = 'Update Successfully'        
        redirect(URL('target',args=[page]))
        
    return dict(form=form,page=page,depotId=depotId,ymDate=ymDate,repId=repId,itemId=itemId)
#------------------target end----------------------
