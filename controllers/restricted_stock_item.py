
#---------------------------- ADD VALIDATION
def restricted_stock_item_validation(form):
    c_id=session.cid
    item_id=str(form.vars.item_id).strip().upper()
    
    #------- check duplicate
    existRows=db((db.sm_restricted_item.cid==c_id) & (db.sm_restricted_item.item_id==item_id)).select(db.sm_restricted_item.item_id,limitby=(0,1))
    if existRows:
        form.errors.item_id='already exist'
    else:
        itemRows=db((db.sm_item.cid==c_id) & (db.sm_item.item_id==item_id)).select(db.sm_item.item_id,db.sm_item.name,db.sm_item.category_id,db.sm_item.price,db.sm_item.dist_price,limitby=(0,1))
        if not itemRows:
            form.errors.item_id='invalid item id'
        else:
            name=itemRows[0].name
            category_id=itemRows[0].category_id
            dist_price=itemRows[0].dist_price
            retail_price=itemRows[0].price
            
            
            form.vars.item_id=item_id
            form.vars.item_name=name
            form.vars.item_cat=category_id
            form.vars.dist_price=dist_price
            form.vars.retail_price=retail_price

#---------------------------- ADD
def restricted_stock_item_add():
    c_id=session.cid    
    if (session.user_type!='Admin'):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))
    elif session.utility_settings!=1:
        session.flash='Access is Denied !'
        redirect (URL('default','home'))
    
    response.title='Restricted Stock Item'
    
    #   ---------------------
    db.sm_restricted_item.item_qty.requires=[IS_NOT_EMPTY(),IS_INT_IN_RANGE(1, 999999,error_message='enter greater than 0')]
    
    form =SQLFORM(db.sm_restricted_item,
                  fields=['item_id','item_qty','auto_voucher','status'],
                  submit_button='Save'
                  )
    
    
    form.vars.cid=c_id
    form.vars.item_qty=''
    if form.accepts(request.vars,session,onvalidation=restricted_stock_item_validation):
       response.flash = 'Submitted Successfully'

    #  ---------------filter-------
    btn_filter=request.vars.btn_filter
    btn_all=request.vars.btn_all
    reqPage=len(request.args)    
    if btn_filter:
        session.btn_filter_restr=btn_filter
        session.item_id_value_restr=str(request.vars.item_id_value).strip().upper()
        reqPage=0
    elif btn_all:
        session.btn_filter_restr=None
        session.item_id_value_restr=None
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
    qset=qset(db.sm_restricted_item.cid==c_id)    
    if ((session.btn_filter_restr) and (session.item_id_value_restr!='')):
        searchValue=str(session.item_id_value_restr).split('-')[0]
        qset=qset(db.sm_restricted_item.item_id==searchValue)
        
    records=qset.select(db.sm_restricted_item.ALL,orderby=db.sm_restricted_item.item_id,limitby=limitby)
    
    #------------------
    
    return dict(form=form,records=records,page=page,items_per_page=items_per_page)


#---------------------------- EDIT
def restricted_stock_item_edit():
    c_id=session.cid    
    if (session.user_type!='Admin'):
        session.flash='Access is Denied'
        redirect (URL('default','home'))
    elif session.utility_settings!=1:
        session.flash='Access is Denied'
        redirect (URL('default','home'))
    
    
    #   --------------------- 
    response.title='Restricted Stock Item-Edit'
    
    page=request.args(0)
    rowID=request.args(1)
        
    record= db.sm_restricted_item(rowID) or redirect(URL('restricted_stock_item_add'))   
    
    db.sm_restricted_item.item_qty.requires=[IS_NOT_EMPTY(),IS_INT_IN_RANGE(1, 999999,error_message='enter greater than 0')]
    form =SQLFORM(db.sm_restricted_item,
                  record=record,
                  deletable=True,
                  fields=['item_qty','auto_voucher','status'],
                  submit_button='Update'
                  )
    
    if form.accepts(request.vars, session):
        response.flash = 'Updated Successfully'        
        redirect(URL('restricted_stock_item_add',args=[page]))
    
    records=db((db.sm_restricted_item.cid==c_id)&(db.sm_restricted_item.id==rowID)).select(db.sm_restricted_item.ALL,limitby=(0,1))
    if not records:
        session.flash = 'Invalid request'
        redirect(URL('restricted_stock_item_add',args=[page]))
    else:
        pass
    
    return dict(form=form,page=page,rowID=rowID,records=records)

