
#==============================(Invoice Terms / Payment Mode) Cash,Credit
def validation_payment_mode(form): 
    category_id=str(request.vars.cat_type_id).strip().upper()
    if ((category_id!='') and (session.cid!='')):
        rows_check=db((db.sm_category_type.cid==session.cid) & (db.sm_category_type.type_name=='PAYMENT_MODE') &(db.sm_category_type.cat_type_id==category_id)).select(db.sm_category_type.cat_type_id,orderby=db.sm_category_type.cat_type_id,limitby=(0,1))
        if rows_check:
            form.errors.cat_type_id=''
            response.flash = 'please choose a new '
        else:
            form.vars.cid=session.cid
            form.vars.type_name='PAYMENT_MODE'
            form.vars.cat_type_id=category_id
def payment_mode():
    task_id='rm_utility_manage'
    access_permission=check_role(task_id)
    if (access_permission==False):    
        session.flash='Access is Denied'
        redirect (URL('default','home'))
        
    response.title='Invocie Term (Payment Mode)'
    
    #---------------------
    form =SQLFORM(db.sm_category_type,
                  fields=['cat_type_id'],
                  submit_button='Save'
                  )
    
    if form.accepts(request.vars,session,onvalidation=validation_payment_mode):
       response.flash = 'Saved Successfully'
    
    #--------------------------------
    btn_delete=request.vars.btn_delete
    record_id=request.vars.record_id
    if btn_delete:
        record_id=request.args[1]
        category_id=request.args[2]
        
        records=db((db.sm_invoice_head.cid==session.cid) & (db.sm_invoice_head.payment_mode==category_id)).select(db.sm_invoice_head.payment_mode,limitby=(0,1))
        if not records:
            records2=db((db.sm_payment_collection.cid==session.cid) & (db.sm_payment_collection.payment_mode==category_id)).select(db.sm_payment_collection.payment_mode,limitby=(0,1))
            if not records2:
                db((db.sm_category_type.cid==session.cid) & (db.sm_category_type.id == record_id)&(db.sm_category_type.type_name=='PAYMENT_MODE')).delete()
            else:
                response.flash='Already used'
        else:
            response.flash='Already used'
            
            
    #--------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=session.items_per_page
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #--------end paging
    
    records=db((db.sm_category_type.cid==session.cid)&(db.sm_category_type.type_name=='PAYMENT_MODE')).select(db.sm_category_type.ALL,orderby=db.sm_category_type.cat_type_id,limitby=limitby)

    return dict(form=form,records=records,page=page,items_per_page=items_per_page,access_permission=access_permission)


#==============================(Invoice Terms / Payment Mode) Cash,Credit
def validation_credit_note(form): 
    category_id=str(request.vars.cat_type_id).strip().upper()
    if ((category_id!='') and (session.cid!='')):
        rows_check=db((db.sm_category_type.cid==session.cid) & (db.sm_category_type.type_name=='CREDIT_NOTE') &(db.sm_category_type.cat_type_id==category_id)).select(db.sm_category_type.cat_type_id,orderby=db.sm_category_type.cat_type_id,limitby=(0,1))
        if rows_check:
            form.errors.cat_type_id=''
            response.flash = 'please choose a new '
        else:
            form.vars.cid=session.cid
            form.vars.type_name='CREDIT_NOTE'
            form.vars.cat_type_id=category_id
def credit_note():
    task_id='rm_utility_manage'
    access_permission=check_role(task_id)
    if (access_permission==False):    
        session.flash='Access is Denied'
        redirect (URL('default','home'))
        
    response.title='Credit Type'
    
    #---------------------
    form =SQLFORM(db.sm_category_type,
                  fields=['cat_type_id'],
                  submit_button='Save'
                  )
    
    if form.accepts(request.vars,session,onvalidation=validation_credit_note):
       response.flash = 'Saved Successfully'
       
    #---------------------------------
    btn_delete=request.vars.btn_delete
    record_id=request.vars.record_id
    if btn_delete:
        record_id=request.args[1]
        category_id=request.args[2]
        
        records=db((db.sm_invoice_head.cid==session.cid) & (db.sm_invoice_head.credit_note==category_id)).select(db.sm_invoice_head.credit_note,limitby=(0,1))
        if not records:
            db((db.sm_category_type.cid==session.cid) & (db.sm_category_type.id == record_id)&(db.sm_category_type.type_name=='CREDIT_NOTE')).delete()
        else:
            response.flash='Already used'
            
    #--------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=session.items_per_page
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #--------end paging
    
    records=db((db.sm_category_type.cid==session.cid)&(db.sm_category_type.type_name=='CREDIT_NOTE')).select(db.sm_category_type.ALL,orderby=db.sm_category_type.cat_type_id,limitby=limitby)

    return dict(form=form,records=records,page=page,items_per_page=items_per_page,access_permission=access_permission)


#============================== Cash,Credit,Cheque,Pay-order
def validation_payment_type(form): 
    category_id=str(request.vars.cat_type_id).strip().upper()
    if ((category_id!='') and (session.cid!='')):
        rows_check=db((db.sm_category_type.cid==session.cid) & (db.sm_category_type.type_name=='PAYMENT_TYPE') &(db.sm_category_type.cat_type_id==category_id)).select(db.sm_category_type.cat_type_id,orderby=db.sm_category_type.cat_type_id,limitby=(0,1))
        if rows_check:
            form.errors.cat_type_id=''
            response.flash = 'please choose a new '
        else:
            form.vars.cid=session.cid
            form.vars.type_name='PAYMENT_TYPE'
            form.vars.cat_type_id=category_id
def payment_type():
    task_id='rm_utility_manage'
    access_permission=check_role(task_id)
    if (access_permission==False):    
        session.flash='Access is Denied'
        redirect (URL('default','home'))
        
    response.title='Payment Type'
    
    #---------------------
    form =SQLFORM(db.sm_category_type,
                  fields=['cat_type_id'],
                  submit_button='Save'
                  )
    
    if form.accepts(request.vars,session,onvalidation=validation_payment_type):
       response.flash = 'Saved Successfully'
       
    #--------------------------------
    btn_delete=request.vars.btn_delete
    record_id=request.vars.record_id
    if btn_delete:
        record_id=request.args[1]
        category_id=request.args[2]
        
        records2=db((db.sm_payment_collection.cid==session.cid) & (db.sm_payment_collection.payment_type==category_id)).select(db.sm_payment_collection.payment_type,limitby=(0,1))
        if not records2:
            db((db.sm_category_type.cid==session.cid) & (db.sm_category_type.id == record_id)&(db.sm_category_type.type_name=='PAYMENT_TYPE')).delete()
        else:
            response.flash='Already used'
            
    #--------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=session.items_per_page
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #--------end paging
    
    records=db((db.sm_category_type.cid==session.cid)&(db.sm_category_type.type_name=='PAYMENT_TYPE')).select(db.sm_category_type.ALL,orderby=db.sm_category_type.cat_type_id,limitby=limitby)
    
    return dict(form=form,records=records,page=page,items_per_page=items_per_page,access_permission=access_permission)


#============================== Cash,Credit,Cheque,Pay-order
def validation_payment_adjustment_type(form): 
    category_id=str(request.vars.cat_type_id).strip().upper()
    if ((category_id!='') and (session.cid!='')):
        rows_check=db((db.sm_category_type.cid==session.cid) & (db.sm_category_type.type_name=='PAYMENT_ADJUSTMENT_TYPE') &(db.sm_category_type.cat_type_id==category_id)).select(db.sm_category_type.cat_type_id,limitby=(0,1))
        if rows_check:
            form.errors.cat_type_id=''
            response.flash = 'please choose a new '
        else:
            form.vars.cid=session.cid
            form.vars.type_name='PAYMENT_ADJUSTMENT_TYPE'
            form.vars.cat_type_id=category_id
def payment_adjustment_type():
    task_id='rm_utility_manage'
    access_permission=check_role(task_id)
    if (access_permission==False):    
        session.flash='Access is Denied'
        redirect (URL('default','home'))
        
    response.title='Payment Adjustment Cause'
    
    #---------------------
    form =SQLFORM(db.sm_category_type,
                  fields=['cat_type_id'],
                  submit_button='Save'
                  )
    
    if form.accepts(request.vars,session,onvalidation=validation_payment_adjustment_type):
       response.flash = 'Saved Successfully'
       
    #--------------------------------
    btn_delete=request.vars.btn_delete
    record_id=request.vars.record_id
    if btn_delete:
        record_id=request.args[1]
        category_id=request.args[2]
        
        records2=db((db.sm_payment_collection.cid==session.cid) & (db.sm_payment_collection.transaction_cause==category_id)).select(db.sm_payment_collection.transaction_cause,limitby=(0,1))
        if not records2:
            db((db.sm_category_type.cid==session.cid) & (db.sm_category_type.id == record_id)&(db.sm_category_type.type_name=='PAYMENT_ADJUSTMENT_TYPE')).delete()
        else:
            response.flash='Already used'
            
    #--------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=session.items_per_page
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #--------end paging
    
    records=db((db.sm_category_type.cid==session.cid)&(db.sm_category_type.type_name=='PAYMENT_ADJUSTMENT_TYPE')).select(db.sm_category_type.ALL,orderby=db.sm_category_type.id,limitby=limitby)
    
    return dict(form=form,records=records,page=page,items_per_page=items_per_page,access_permission=access_permission)
    
#==============================(Invoice Terms / Payment Mode) Cash,Credit
def validation_return_cause(form): 
    category_id=str(request.vars.cat_type_id).strip().upper()
    if ((category_id!='') and (session.cid!='')):
        rows_check=db((db.sm_category_type.cid==session.cid) & (db.sm_category_type.type_name=='RET_REASON') &(db.sm_category_type.cat_type_id==category_id)).select(db.sm_category_type.cat_type_id,orderby=db.sm_category_type.cat_type_id,limitby=(0,1))
        if rows_check:
            form.errors.cat_type_id=''
            response.flash = 'please choose a new '
        else:
            form.vars.cid=session.cid
            form.vars.type_name='RET_REASON'
            form.vars.cat_type_id=category_id
def return_cause():
    task_id='rm_utility_manage'
    access_permission=check_role(task_id)
    if (access_permission==False):
        session.flash='Access is Denied'
        redirect (URL('default','home'))
        
    response.title='Return Cause'
    
    #---------------------
    form =SQLFORM(db.sm_category_type,
                  fields=['cat_type_id'],
                  submit_button='Save'
                  )
    
    if form.accepts(request.vars,session,onvalidation=validation_return_cause):
       response.flash = 'Saved Successfully'
       
    #--------------------------------
    btn_delete=request.vars.btn_delete
    record_id=request.vars.record_id
    if btn_delete:
        record_id=request.args[1]
        category_id=request.args[2]
        
        records=db((db.sm_return_head.cid==session.cid) & (db.sm_return_head.ret_reason==category_id)).select(db.sm_return_head.ret_reason,limitby=(0,1))
        if not records:
            db((db.sm_category_type.cid==session.cid) & (db.sm_category_type.id == record_id)&(db.sm_category_type.type_name=='RET_REASON')).delete()
        else:
            response.flash='Already used'
            
    #--------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=session.items_per_page
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #--------end paging
    
    records=db((db.sm_category_type.cid==session.cid)&(db.sm_category_type.type_name=='RET_REASON')).select(db.sm_category_type.ALL,orderby=db.sm_category_type.cat_type_id,limitby=limitby)
    
    return dict(form=form,records=records,page=page,items_per_page=items_per_page,access_permission=access_permission)
    
#Validation
def validation_merchandizing(form):
    
    cid=session.cid
    item_id=str(form.vars.item_id).strip()
    name_row=str(form.vars.name).strip()
    
    item_name=check_special_char(name_row)
        
    rows_check=db((db.sm_merchandizing_item.cid==cid) & (db.sm_merchandizing_item.item_id==item_id)).select(db.sm_merchandizing_item.item_id,limitby=(0,1))
    if rows_check:
        form.errors.item_id='please choose a new'
    else:
        rows_check2=db((db.sm_merchandizing_item.cid==cid) & (db.sm_merchandizing_item.name==item_name)).select(db.sm_merchandizing_item.item_id,limitby=(0,1))
        if rows_check2:
            form.errors.name='please choose a new'
        else:
            form.vars.item_id=item_id
            form.vars.name=item_name

# merchandizing Item
def merchandizing_item():
    #----------Task assaign----------
    task_id='rm_merchandizing_manage'
    access_permission=check_role(task_id)
    if (access_permission==False):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))        
    
    #   --------------------- 
    response.title='Merchandizing Item'
    
    cid=session.cid
    
    #======================
    form =SQLFORM(db.sm_merchandizing_item,
                  fields=['item_id','name','des'],
                  submit_button='Save'
                  )
    
    #Insert after validation
    if form.accepts(request.vars,session,onvalidation=validation_merchandizing):
       response.flash = 'Submitted Successfully'
    
    
    #--------------------------------
    btn_delete=request.vars.btn_delete    
    if btn_delete:
        record_id=request.vars.rid
        db((db.sm_merchandizing_item.cid==cid) & (db.sm_merchandizing_item.id==record_id)).delete()
        response.flash='Deleted successfully'
    
    
    #------------------filter
    btn_filter_mitem=request.vars.btn_filter
    btn_filter_mitem_all=request.vars.btn_all
    reqPage=len(request.args)
    if btn_filter_mitem:
        session.btn_filter_mitem=btn_filter_mitem
        session.search_type_mitem=request.vars.search_type
        session.search_value_mitem=str(request.vars.search_value).strip().upper()
        reqPage=0
    elif btn_filter_mitem_all:
        session.btn_filter_mitem=None
        session.search_type_mitem=None
        session.search_value_mitem=None
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
    qset=qset(db.sm_merchandizing_item.cid==cid)
        
    if session.btn_filter_mitem:
        if (session.search_type_mitem=='ItemID'):
            searchValue=str(session.search_value_mitem).split('-')[0]
            qset=qset(db.sm_merchandizing_item.item_id==searchValue)
        
    records=qset.select(db.sm_merchandizing_item.ALL,orderby=db.sm_merchandizing_item.item_id,limitby=limitby) 
    
    return dict(form=form,records=records,page=page,items_per_page=items_per_page,access_permission=access_permission)

def download_merchandizing_item():
    task_id='rm_merchandizing_manage'
    access_permission=check_role(task_id)
    if (access_permission==False):
        session.flash='Access is Denied !'
        redirect (URL('merchandizing_item')) 
    
    
    cid=session.cid
    records=''
    #Create query based on search type
    qset=db()
    qset=qset(db.sm_merchandizing_item.cid==session.cid)
        
    if session.btn_filter_mitem:
        if (session.search_type_mitem=='ItemID'):
            searchValue=str(session.search_value_mitem).split('-')[0]
            qset=qset(db.sm_merchandizing_item.item_id==searchValue)
        
    records=qset.select(db.sm_merchandizing_item.ALL,orderby=db.sm_merchandizing_item.item_id) 
    
    #Create string for download as excel file
    myString='Merchandizing Item\n'
    myString+='Item ID,Name,Description\n'  
    for rec in records:
        item_id=rec.item_id
        name=str(rec.name).replace(',', ' ')
        des=str(rec.des).replace(',', ' ')
        
        myString+=str(item_id)+','+str(name)+','+str(des)+'\n'
        
    #-----------
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_merchandizing_item.csv'   
    return str(myString)


#Validation for rep

#==============================
def validation_brand(form): 
    category_id=str(request.vars.cat_type_id).strip()
    if ((category_id!='') and (session.cid!='')):
        rows_check=db((db.sm_category_type.cid==session.cid) & (db.sm_category_type.type_name=='BRAND_NAME') &(db.sm_category_type.cat_type_id==category_id)).select(db.sm_category_type.cat_type_id,orderby=db.sm_category_type.cat_type_id,limitby=(0,1))
        if rows_check:
            form.errors.cat_type_id=''
            response.flash = 'please choose a new '
        else:
            form.vars.cid=session.cid
            form.vars.type_name='BRAND_NAME'
            form.vars.cat_type_id=category_id
def brand():
    task_id='rm_utility_manage'
    access_permission=check_role(task_id)
    if (access_permission==False):    
        session.flash='Access is Denied'
        redirect (URL('default','home'))
    
    response.title='Brand'
    
    #---------------------
    form =SQLFORM(db.sm_category_type,
                  fields=['cat_type_id'],
                  submit_button='Save'
                  )
    
    if form.accepts(request.vars,session,onvalidation=validation_brand):
       response.flash = 'Saved Successfully'
    
    #--------------------------------
    btn_delete=request.vars.btn_delete
    record_id=request.vars.record_id
    if btn_delete:
        record_id=request.args[1]
        category_id=request.args[2]
        records=db((db.visit_market_info.cid==session.cid) & (db.visit_market_info.brand_name==category_id)).select(db.visit_market_info.brand_name,limitby=(0,1))
        if not records:
            db((db.sm_category_type.id == record_id)&(db.sm_category_type.type_name=='BRAND_NAME')).delete()
        else:
            response.flash='This Brand already used'
    
    #--------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=session.items_per_page
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #--------end paging
    
    records=db((db.sm_category_type.cid==session.cid)&(db.sm_category_type.type_name=='BRAND_NAME')).select(db.sm_category_type.ALL,orderby=db.sm_category_type.cat_type_id,limitby=limitby)

    return dict(form=form,records=records,page=page,items_per_page=items_per_page,access_permission=access_permission)



#==============================
def validation_complain_type(form): 
    category_id=str(request.vars.cat_type_id).strip()
    if ((category_id!='') and (session.cid!='')):
        rows_check=db((db.sm_category_type.cid==session.cid) & (db.sm_category_type.type_name=='COMPLAIN_TYPE') &(db.sm_category_type.cat_type_id==category_id)).select(db.sm_category_type.cat_type_id,orderby=db.sm_category_type.cat_type_id,limitby=(0,1))
        if rows_check:
            form.errors.cat_type_id=''
            response.flash = 'please choose a new '
        else:
            form.vars.cid=session.cid
            form.vars.type_name='COMPLAIN_TYPE'
            form.vars.cat_type_id=category_id
def complain_type():
    task_id='rm_feedback_manage'
    access_permission=check_role(task_id)
    if (access_permission==False):    
        session.flash='Access is Denied'
        redirect (URL('default','home'))
    
    response.title='Complain Type'
    
    #---------------------
    form =SQLFORM(db.sm_category_type,
                  fields=['cat_type_id'],
                  submit_button='Save'
                  )
    
    if form.accepts(request.vars,session,onvalidation=validation_complain_type):
       response.flash = 'Saved Successfully'
    
    #--------------------------------
    btn_delete=request.vars.btn_delete
    record_id=request.vars.record_id
    if btn_delete:
        record_id=request.args[1]
        category_id=request.args[2]
#        records=db((db.visit_market_info.cid==session.cid) & (db.visit_market_info.brand_name==category_id)).select(db.visit_market_info.brand_name,limitby=(0,1))
#        if not records:
        db((db.sm_category_type.id == record_id)&(db.sm_category_type.type_name=='COMPLAIN_TYPE')).delete()
#        else:
#            response.flash='This Type already used'
    
    #--------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=session.items_per_page
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #--------end paging
    
    records=db((db.sm_category_type.cid==session.cid)&(db.sm_category_type.type_name=='COMPLAIN_TYPE')).select(db.sm_category_type.ALL,orderby=db.sm_category_type.cat_type_id,limitby=limitby)

    return dict(form=form,records=records,page=page,items_per_page=items_per_page,access_permission=access_permission)


#==============================
def validation_complain_from(form): 
    category_id=str(request.vars.cat_type_id).strip()
    if ((category_id!='') and (session.cid!='')):
        rows_check=db((db.sm_category_type.cid==session.cid) & (db.sm_category_type.type_name=='COMPLAIN_FROM') &(db.sm_category_type.cat_type_id==category_id)).select(db.sm_category_type.cat_type_id,orderby=db.sm_category_type.cat_type_id,limitby=(0,1))
        if rows_check:
            form.errors.cat_type_id=''
            response.flash = 'please choose a new '
        else:
            form.vars.cid=session.cid
            form.vars.type_name='COMPLAIN_FROM'
            form.vars.cat_type_id=category_id
def complain_from():
    task_id='rm_feedback_manage'
    access_permission=check_role(task_id)
    if (access_permission==False):    
        session.flash='Access is Denied'
        redirect (URL('default','home'))
    
    response.title='Complain From'
    
    #---------------------
    form =SQLFORM(db.sm_category_type,
                  fields=['cat_type_id'],
                  submit_button='Save'
                  )
    
    if form.accepts(request.vars,session,onvalidation=validation_complain_from):
       response.flash = 'Saved Successfully'
    
    #--------------------------------
    btn_delete=request.vars.btn_delete
    record_id=request.vars.record_id
    if btn_delete:
        record_id=request.args[1]
        category_id=request.args[2]
#        records=db((db.visit_market_info.cid==session.cid) & (db.visit_market_info.brand_name==category_id)).select(db.visit_market_info.brand_name,limitby=(0,1))
#        if not records:
        db((db.sm_category_type.id == record_id)&(db.sm_category_type.type_name=='COMPLAIN_FROM')).delete()
#        else:
#            response.flash='This Type already used'
    
    #--------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=session.items_per_page
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #--------end paging
    
    records=db((db.sm_category_type.cid==session.cid)&(db.sm_category_type.type_name=='COMPLAIN_FROM')).select(db.sm_category_type.ALL,orderby=db.sm_category_type.cat_type_id,limitby=limitby)

    return dict(form=form,records=records,page=page,items_per_page=items_per_page,access_permission=access_permission)



#==============================
def validation_task_type(form): 
    category_id=str(request.vars.cat_type_id).strip()
    if ((category_id!='') and (session.cid!='')):
        rows_check=db((db.sm_category_type.cid==session.cid) & (db.sm_category_type.type_name=='TASK_TYPE') &(db.sm_category_type.cat_type_id==category_id)).select(db.sm_category_type.cat_type_id,orderby=db.sm_category_type.cat_type_id,limitby=(0,1))
        if rows_check:
            form.errors.cat_type_id=''
            response.flash = 'please choose a new '
        else:
            form.vars.cid=session.cid
            form.vars.type_name='TASK_TYPE'
            form.vars.cat_type_id=category_id
def task_type():
    task_id='rm_task_manage'
    access_permission=check_role(task_id)
    if (access_permission==False):    
        session.flash='Access is Denied'
        redirect (URL('default','home'))
    
    response.title='Task Type'
    
    #---------------------
    form =SQLFORM(db.sm_category_type,
                  fields=['cat_type_id'],
                  submit_button='Save'
                  )
    
    if form.accepts(request.vars,session,onvalidation=validation_task_type):
       response.flash = 'Saved Successfully'
    
    #--------------------------------
    btn_delete=request.vars.btn_delete
    record_id=request.vars.record_id
    if btn_delete:
        record_id=request.args[1]
        category_id=request.args[2]
#        records=db((db.visit_market_info.cid==session.cid) & (db.visit_market_info.brand_name==category_id)).select(db.visit_market_info.brand_name,limitby=(0,1))
#        if not records:
        db((db.sm_category_type.id == record_id)&(db.sm_category_type.type_name=='TASK_TYPE')).delete()
#        else:
#            response.flash='This Type already used'
    
    #--------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=session.items_per_page
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #--------end paging
    
    records=db((db.sm_category_type.cid==session.cid)&(db.sm_category_type.type_name=='TASK_TYPE')).select(db.sm_category_type.ALL,orderby=db.sm_category_type.cat_type_id,limitby=limitby)

    return dict(form=form,records=records,page=page,items_per_page=items_per_page,access_permission=access_permission)



#======================================= District
def validation_district(form):    
    c_id=session.cid
    district_id=str(form.vars.district_id).strip().upper()
    name=str(form.vars.name).strip().replace("'","").capitalize()
    
    rows_check=db((db.district.cid==c_id) & (db.district.district_id==district_id)).select(db.district.district_id,limitby=(0,1))
    if rows_check:
        form.errors.district_id='already exist'
    else:
        rows_check2=db((db.district.cid==c_id) & (db.district.name==name)).select(db.district.name,limitby=(0,1))
        if rows_check2:
            form.errors.name='already exist'
        else:
            form.vars.district_id=district_id
            form.vars.name=name
            
def district():
    task_id='rm_utility_manage'
    access_permission=check_role(task_id)
    if (access_permission==False):    
        session.flash='Access is Denied'
        redirect (URL('default','home'))
    
    response.title='District'
    
    c_id=session.cid
    
    form =SQLFORM(db.district,
                  fields=['district_id','name'],       
                  submit_button='Save'
                  )
    
    form.vars.cid=c_id
    if form.accepts(request.vars,session,onvalidation=validation_district):
        response.flash = 'Saved successfully'
        #-------------
    
    #----------- delete
    btn_delete=request.vars.btn_delete
        
    if btn_delete:
        record_id=request.vars.recordID
        distname=request.vars.distname
        thanaRecords=db((db.district_thana.cid==c_id) & (db.district_thana.district==distname)).select(db.district_thana.district,limitby=(0,1))
        if not thanaRecords:
            db((db.district.cid==c_id)&(db.district.id == record_id)).delete()
        else:
            response.flash='This data is already used'
    
    # --------- Set text for filter
    btn_filter=request.vars.btn_filter
    btn_all=request.vars.btn_all
    reqPage=len(request.args)
    
    if btn_filter:
        session.btn_filter=btn_filter
        session.search_type=request.vars.search_type
        session.search_value=request.vars.search_value

        reqPage=0
    elif btn_all:
        session.btn_filter=None
        session.search_type=None
        session.search_value=None
        reqPage=0
    
    #--------paging
    if reqPage:
        page=int(request.args[0])
    else:
        page=0
    items_per_page=session.items_per_page*2
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #--------end paging  
    #Set query based on search type
    
    qset=db()
    qset=qset(db.district.cid==c_id)    
    records=qset.select(db.district.ALL,orderby=db.district.name,limitby=limitby)
    totalCount=qset.count()
    #------------------------------------ filter end
    return dict(form=form,records=records,totalCount=totalCount,page=page,items_per_page=items_per_page,access_permission=access_permission)


def district_batch_upload():
    task_id='rm_utility_manage'
    access_permission=check_role(task_id)
    if (access_permission==False):    
        session.flash='Access is Denied'
        redirect (URL('default','home'))
    
    c_id=session.cid
    
    response.title='District Batch upload'
    
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
            db.district.truncate()
            db.district_thana.truncate()     
            response.flash='ALL District cleaned successfully'
            
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
        
        # main loop   
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
                district_idExcel=str(coloum_list[0]).strip().upper()
                district_nameExcel=str(coloum_list[1]).strip().replace("'","").capitalize()
                district_nameExcel=check_special_char(district_nameExcel)
                
                #------------------
                if district_idExcel=='' or district_nameExcel=='':
                    error_data=row_data+'(Required all value)\n'
                    error_str=error_str+error_data
                    count_error+=1
                    continue
                    
                #-------------------
                try:
                    existCheckRows=db((db.district.cid==c_id)&((db.district.district_id==district_idExcel)|(db.district.name==district_nameExcel))).select(db.district.id,limitby=(0,1))
                    if existCheckRows:
                        error_data=row_data+'(Duplicate ID/Name check)\n'
                        error_str=error_str+error_data
                        count_error+=1
                        continue
                    else:
                        db.district.insert(cid=c_id,district_id=district_idExcel,name=district_nameExcel)
                        count_inserted+=1
                except:
                    error_data=row_data+'(error in process!)\n'
                    error_str=error_str+error_data
                    count_error+=1
                    continue
                
        if error_str=='':
            error_str='No error'
    
    return dict(count_inserted=count_inserted,count_error=count_error,error_str=error_str,total_row=total_row)



def validation_thana(form):    
    c_id=session.cid
    district=str(form.vars.district).strip()
    name=str(form.vars.name).strip().capitalize()
    
    rows_check=db((db.district_thana.cid==c_id)& (db.district_thana.district==district) & (db.district_thana.name==name)).select(db.district_thana.name,limitby=(0,1))
    if rows_check:
        form.errors.name='already exist'
    else:
        form.vars.name=name
def thana():
    task_id='rm_utility_manage'
    access_permission=check_role(task_id)
    if (access_permission==False):    
        session.flash='Access is Denied'
        redirect (URL('default','home'))
    
    response.title='Thana'
    
    
    c_id=session.cid
    
    dPage=request.args(0)
    page=request.args(1)
    
    distname=request.vars.distname  
    
    #--------------
    
    #   ---------------------
    
    form =SQLFORM(db.district_thana,
                  fields=['name'],
                  submit_button='Save'
                  )
    
    form.vars.cid=session.cid
    form.vars.district=distname
    
    if form.accepts(request.vars,session,onvalidation=validation_thana):
       response.flash = 'Submitted Successfully'
    
    #----------- delete
    btn_delete=request.vars.btn_delete    
    if btn_delete:
        record_id=request.vars.recordID
        db((db.district_thana.cid==c_id)&(db.district_thana.id == record_id)).delete()
        
    
    #--------paging
    
    #--------end paging   
    
    qset=db()
    qset=qset(db.district_thana.district==distname)
    records=qset.select(db.district_thana.ALL,orderby=db.district_thana.name)
    
    return dict(form=form,records=records,distname=distname,page=page,dPage=dPage,access_permission=access_permission)


def validation_market_day_add(form):
    area_id=str(request.vars.area_id).strip().upper().split('|')[0]
    day_name=str(request.vars.day_name).strip()
    
    if ((area_id!='') and (session.cid!='')):        
        area_name=''
        if session.user_type=='Depot':
            check_area=db((db.sm_level.cid==session.cid) & (db.sm_level.depot_id==session.depot_id) & (db.sm_level.level_id==area_id) & (db.sm_level.is_leaf == '1') ).select(db.sm_level.level_id,db.sm_level.level_name,limitby=(0,1))
        else:
            check_area=db((db.sm_level.cid==session.cid) & (db.sm_level.level_id==area_id) & (db.sm_level.is_leaf == '1') ).select(db.sm_level.level_id,db.sm_level.level_name,db.sm_level.depot_id,limitby=(0,1))
            
        if check_area:
            area_name=check_area[0].level_name
            depot_id=check_area[0].depot_id
            if (depot_id=='-' or depot_id==''):
                form.errors.rep_id=''
                response.flash = 'Invalid Depot in working area '
                
            else:                
                rows_check=db((db.sm_market_day.cid==session.cid) & (db.sm_market_day.area_id==area_id) & (db.sm_market_day.day_name==day_name)).select(db.sm_market_day.day_name,limitby=(0,1))
                if rows_check:
                    form.errors.area_id=''
                    response.flash = 'please choose a new '
                else:
                    depot_name=''
                    depotRow=db((db.sm_depot.cid==session.cid) & (db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
                    if depotRow:
                        depot_name=depotRow[0].name
                    
                    form.vars.area_id=area_id
                    form.vars.area_name=area_name
                    form.vars.depot_id=depot_id
                    form.vars.depot_name=depot_name
                    form.vars.day_name=day_name                    
                    
        else:
            form.errors.area_id=''
            response.flash = 'Invalid Market/Route '
        
    else:
        form.errors.area_id=''
        response.flash = 'enter accurate value '


def market_day_add():
    task_id='rm_utility_manage'
    task_id_view='rm_utility_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)    
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))
    
    
    response.title='Market-Day'
    c_id=session.cid
        
    db.sm_market_day.day_name.requires=IS_IN_SET(('Saturday','Sunday','Monday','Tuesday','Wednesday','Thursday','Friday'))
    
    form =SQLFORM(db.sm_market_day,
                  fields=['area_id','day_name'],
                  submit_button='Save'         
                  )
    #Insert with validation
    if form.accepts(request.vars,session,onvalidation=validation_market_day_add):
       response.flash = 'Data Submitted Successfully'
       
    #----------delete rep area---
    btn_delete=request.vars.btn_delete    
    if btn_delete:
        id_delete=request.vars.record_id
        db((db.sm_market_day.id == id_delete)).delete()
    
    #------------------------
    btn_filter_mday=request.vars.btn_filter
    btn_mday_all=request.vars.btn_all
    if btn_filter_mday:
        session.btn_filter_mday=btn_filter_mday
        
        session.search_type_mday=request.vars.search_type
        session.search_value_mday=str(request.vars.search_value).strip()
        
    elif btn_mday_all:
        session.btn_filter_mday=None
        session.search_type_mday=None
        session.search_value_mday=None

    #--------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=session.items_per_page
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #--------end paging    
    
    qset=db()
    qset=qset(db.sm_market_day.cid==c_id)   
    
    if session.user_type=='Depot':
        qset=qset(db.sm_market_day.depot_id==session.depot_id)
    else:
        if (session.btn_filter_mday and session.search_type_mday=='DepotID'):
            searchValue=str(session.search_value_mday).split('|')[0]
            qset=qset(db.sm_market_day.depot_id==searchValue)
    
    #---- supervisor
    if session.user_type=='Supervisor':
        qset=qset(db.sm_market_day.area_id.belongs(session.marketList))        
    else:
        pass
    
    if (session.btn_filter_mday and session.search_type_mday=='DayName'):
        searchValue=str(session.search_value_mday)
        qset=qset(db.sm_market_day.day_name==searchValue)
        
    elif (session.btn_filter_mday and session.search_type_mday=='AreaID'):
        searchValue=str(session.search_value_mday).split('|')[0]
        qset=qset(db.sm_market_day.area_id==searchValue)
    
    records=qset.select(db.sm_market_day.ALL,orderby=db.sm_market_day.area_id,limitby=limitby)
    totalCount=qset.count()
    
    return dict(form=form,records=records,totalCount=totalCount,page=page,items_per_page=items_per_page,access_permission=access_permission)
#---------------end  rep_area-----------------------


#====================================== REP AREA BATCH UPLOAD ---------- 
def market_day_batch_upload():#Rep area batch upload
    task_id='rm_utility_manage'
    task_id_view='rm_utility_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)    
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))
    
    response.title='Market-Day Batch upload'
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
                if len(coloum_list)==2:
                    area_list_excel.append(str(coloum_list[0]).strip().upper())
        
        #-------valid area(level) list based onexcel sheet
        if session.user_type=='Depot':
            existLevelRows=db((db.sm_level.cid==c_id) & (db.sm_level.depot_id==session.depot_id)&(db.sm_level.is_leaf=='1')&(db.sm_level.level_id.belongs(area_list_excel))).select(db.sm_level.level_id,db.sm_level.level_name,db.sm_level.depot_id,orderby=db.sm_level.level_id)
        else:
            existLevelRows=db((db.sm_level.cid==c_id) &(db.sm_level.is_leaf=='1')&(db.sm_level.level_id.belongs(area_list_excel))).select(db.sm_level.level_id,db.sm_level.level_name,db.sm_level.depot_id,orderby=db.sm_level.level_id)
        existLevel_list=existLevelRows.as_list()
        
        dayList=['Saturday','Sunday','Monday','Tuesday','Wednesday','Thursday','Friday']
        
#   --------------------     
        for i in range(total_row):
            if i>=100: 
                break
            else:
                row_data=row_list[i]
            coloum_list=row_data.split( '\t')            

            if len(coloum_list)==2:
                areaID_excel=str(coloum_list[0]).strip().upper()
                dayname_excel=str(coloum_list[1]).strip().capitalize()
                
                try:      
                    valid_day=False                    
                    valid_level=False  
                    valid_depot=False
                    duplicateFlag=False
                    depotID=''
                    depotName=''
                    
                    #----------- check valid Day.
                    if dayname_excel in dayList:
                        valid_day=True
                    
                    #----------- check duplicate rep-area   
                    if valid_day==True:                                                       
                        for i in range(len(existLevel_list)):
                            myRowData=existLevel_list[i]                                
                            level_id=myRowData['level_id']
                            level_name=myRowData['level_name']
                            level_depot_id=myRowData['depot_id'] 
                            if (str(level_id).strip()==str(areaID_excel).strip()):
                                depotID=level_depot_id                                
                                valid_level=True
                                if not (depotID=='-' or depotID==''):
                                    valid_depot=True
                                    
                                    depotRow=db((db.sm_depot.cid==c_id) & (db.sm_depot.depot_id==depotID)).select(db.sm_depot.name,limitby=(0,1))
                                    if depotRow:
                                        depotName=depotRow[0].name
                                
                                break
                        
                        if (valid_level==True and valid_depot==True):                            
                            rows_check=db((db.sm_market_day.cid==c_id) & (db.sm_market_day.area_id==areaID_excel) & (db.sm_market_day.day_name==dayname_excel)).select(db.sm_market_day.day_name,limitby=(0,1))
                            if rows_check:
                                duplicateFlag=True
                    
                    #Create list for bulk insert
                    if valid_day==True:                        
                        if valid_level==True:
                            if valid_depot==True:
                                if duplicateFlag==False:
                                    
                                    ins_dict= {'cid':c_id,'area_id':areaID_excel,'area_name':level_name,'depot_id':depotID,'depot_name':depotName,'day_name':dayname_excel}
                                    ins_list.append(ins_dict)                               
                                    count_inserted+=1
                                    
                                else:
                                    error_data=row_data+'(already exist!)\n'
                                    error_str=error_str+error_data
                                    count_error+=1
                                    continue
                                    
                            else:
                                error_data=row_data+'(invalid depot in working area!)\n'
                                error_str=error_str+error_data
                                count_error+=1
                                continue                            
                        else:
                            error_data=row_data+'(invalid area or market!)\n'
                            error_str=error_str+error_data
                            count_error+=1
                            continue                        
                    else:
                        error_data=row_data+'(Invalid Day!)\n'
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
        
        if len(ins_list) > 0:
            inCountList=db.sm_market_day.bulk_insert(ins_list)             
     
    
    return dict(count_inserted=count_inserted,count_error=count_error,error_str=error_str,total_row=total_row)


#------------------ 
def download_market_day():    
    task_id='rm_utility_manage'
    task_id_view='rm_utility_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)    
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))
    
    c_id=session.cid
    
    records=''
    
    qset=db()
    qset=qset(db.sm_market_day.cid==c_id)   
    
    if session.user_type=='Depot':
        qset=qset(db.sm_market_day.depot_id==session.depot_id)
    else:
        if (session.btn_filter_mday and session.search_type_mday=='DepotID'):
            searchValue=str(session.search_value_mday).split('|')[0]
            qset=qset(db.sm_market_day.depot_id==searchValue)
    
    #---- supervisor
    if session.user_type=='Supervisor':
        qset=qset(db.sm_market_day.area_id.belongs(session.marketList))        
    else:
        pass
    
    if (session.btn_filter_mday and session.search_type_mday=='DayName'):
        searchValue=str(session.search_value_mday)
        qset=qset(db.sm_market_day.day_name==searchValue)
        
    elif (session.btn_filter_mday and session.search_type_mday=='AreaID'):
        searchValue=str(session.search_value_mday).split('|')[0]
        qset=qset(db.sm_market_day.area_id==searchValue)
    
    if session.btn_filter_mday and session.search_value_mday:
        records=qset.select(db.sm_market_day.ALL,orderby=db.sm_market_day.area_id)
    else:
        session.flash='Filter needed'
        redirect (URL('market_day_add'))
        
    #---------
    myString='MarketID, MarketName, Depot ID, Depot Name, DayName\n' #Set column name
    for rec in records:
        area_id=rec.area_id
        area_name=str(rec.area_name).replace(',', ' ')
        depot_id=rec.depot_id
        depot_name=str(rec.depot_name).replace(',', ' ')        
        day_name=str(rec.day_name)
        
        #Create string
        myString+=str(area_id)+','+str(area_name)+','+str(depot_id)+','+str(depot_name)+','+day_name+'\n'
        
    #Save as csv
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_market_day.csv'   
    return str(myString)


#------------------ 








