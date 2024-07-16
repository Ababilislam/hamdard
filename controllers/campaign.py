
from random import randint

#---------------------------- ADD VALIDATION
def validation_campaign_add(form):
    c_id=session.cid
    
    offer_name=str(form.vars.offer_name).strip().replace('_', ' ')
    from_date=form.vars.from_date
    to_date=form.vars.to_date    
    target_qty=form.vars.target_qty
        
    if target_qty=='' or target_qty==None:
        target_qty=0
        
    dateFlag=True
    try:
        fromDt=datetime.datetime.strptime(str(from_date),"%Y-%m-%d" )
        toDt=datetime.datetime.strptime(str(to_date),"%Y-%m-%d" )                        
        if (fromDt > toDt):
            dateFlag=False            
            response.flash='To date need greater than From date'
    except:
        dateFlag=False
        response.flash='Required valid date'
    
    if dateFlag==False:
        form.errors.offer_name=''
    else:        
        if int(target_qty)<=0:
            form.errors.target_qty='Required greater than 0'
        else:
            existRows=db((db.trade_promotional_offer.cid==c_id) & (db.trade_promotional_offer.offer_name==offer_name) & (db.trade_promotional_offer.from_date==from_date) & (db.trade_promotional_offer.to_date==to_date) ).select(db.trade_promotional_offer.offer_name,limitby=(0,1))
            if existRows:
                form.errors.offer_name=''
                response.flash='already exist'
            else:
                form.vars.offer_name=offer_name


#---------------------------- ADD
def campaign_add():    
    task_id='rm_campaign_manage'
    task_id_view='rm_campaign_view'    
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))
    
    c_id=session.cid
    
    response.title='Campaign'
    
    #   ---------------------
    form =SQLFORM(db.trade_promotional_offer,
                  fields=['offer_name','from_date','to_date','target_qty','reward','bonus_con','status'],
                  submit_button='Save'
                  )
    
    form.vars.cid=c_id     
    if form.accepts(request.vars,session,onvalidation=validation_campaign_add):
       response.flash = 'Submitted Successfully'
       
    #  ---------------filter-------
    btn_filter=request.vars.btn_filter
    btn_all=request.vars.btn_all
    reqPage=len(request.args)    
    if btn_filter:
        session.btn_filter_tpcp=btn_filter
        session.searchType_tpcp=str(request.vars.searchType).strip()
        session.searchValue_tpcp=str(request.vars.searchValue).strip()
        reqPage=0
    elif btn_all:
        session.btn_filter_tpcp=None
        session.searchType_tpcp=None
        session.searchValue_tpcp=None
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
    qset=qset(db.trade_promotional_offer.cid==c_id)
    if ((session.btn_filter_tpcp) and (session.searchType_tpcp=='Reference')):
        qset=qset(db.trade_promotional_offer.offer_name==session.searchValue_tpcp)  
    
    elif ((session.btn_filter_tpcp) and (session.searchType_tpcp=='Status')):
        qset=qset(db.trade_promotional_offer.status==session.searchValue_tpcp)      
        
    records=qset.select(db.trade_promotional_offer.ALL,orderby=~db.trade_promotional_offer.to_date,limitby=limitby)
    
    #------------------
    return dict(form=form,records=records,access_permission=access_permission,page=page,items_per_page=items_per_page)



#---------------------------- EDIT
def campaign_edit():
    task_id='rm_campaign_manage'  
    access_permission=check_role(task_id)
    if (access_permission==False):
        session.flash='Access is Denied !'
        redirect (URL('campaign_add'))
        
    #   --------------------- 
    response.title='Campaign-Edit'
    
    c_id=session.cid
    
    page=request.args(0)
    rowID=request.args(1)
    
    record= db.trade_promotional_offer(rowID) or redirect(URL('campaign_add'))   
    
    form =SQLFORM(db.trade_promotional_offer,
                  record=record,
                  deletable=True,
                  fields=['status'],
                  submit_button='Update'
                  )
    
    if form.accepts(request.vars, session):
        session.flash = 'Updated Successfully'
        redirect(URL('campaign_add',args=[page]))
    
    records=db((db.trade_promotional_offer.cid==c_id)&(db.trade_promotional_offer.id==rowID)).select(db.trade_promotional_offer.ALL,limitby=(0,1))
    if not records:
        session.flash = 'Invalid request'
        redirect(URL('campaign_add',args=[page]))
    else:
        pass
    
    return dict(form=form,page=page,records=records,rowID=rowID)




