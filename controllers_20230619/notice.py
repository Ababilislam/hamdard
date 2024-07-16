#notice


#Validation for catagory

            

def notice_validation(form):
    notice=str(request.vars.notice).strip().upper()
    notice=check_special_char(notice)
    form.vars.cid=session.cid
    

            

def notice():
    task_id='rm_item_manage'
    task_id_view='rm_item_manage'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))
    # ---------------------
    response.title='Noice'
    
    form =SQLFORM(db.sm_notice,
                  fields=['notice','notice_date'],
                  submit_button='Save'          
                  )
    
    records=db((db.sm_notice.cid==session.cid)).select(db.sm_notice.sl,orderby=~db.sm_notice.sl,limitby=(0,1))
    slmax='0'
    for records in records:
        slmax=records.sl
    slEntry=int(slmax)+1
#     return slEntry
    form.vars.sl=slEntry
    #Insert with validation
    if form.accepts(request.vars,session,onvalidation=notice_validation):
       response.flash = 'Saved Successfully'
    
    #--------------------------------
    btn_delete=request.vars.btn_delete
    record_id=request.vars.record_id
    
    #If catagorey not in item it can be delete
    if btn_delete:
        record_id=request.args[1]
        records=db((db.sm_notice.cid==session.cid) & (db.sm_notice.id==record_id)).select(db.sm_notice.cid,limitby=(0,1))
        if records:
            db((db.sm_notice.id==record_id)).delete()
        else:
            response.flash='Failed'
    
    #--------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=session.items_per_page
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #--------end paging
    
    records=db((db.sm_notice.cid==session.cid)).select(db.sm_notice.ALL,orderby=~db.sm_notice.id,limitby=limitby)
#     return db._lastsql
#     return records
    
    return dict(form=form,records=records,page=page,items_per_page=items_per_page,access_permission=access_permission)


