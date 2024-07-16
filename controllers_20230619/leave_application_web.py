def leaveList():

    c_id=session.cid
    response.title='leave List'
    
    #------------------------filter
    btn_filter_leave=request.vars.btn_filter_leave
    btn_all_leave=request.vars.btn_all_leave
    reqPage=len(request.args)
    
    if btn_filter_leave:
        session.btn_filter_leave=btn_filter_leave        
        session.EMPID=request.vars.EMPID        
        session.from_date=request.vars.from_date 
        session.to_date=request.vars.to_date
        session.type_l=request.vars.type_l
        session.ah_status=request.vars.ah_status
        session.zh_status=request.vars.zh_status           
        session.dh_status=request.vars.dh_status
        session.ddm_status=request.vars.ddm_status
        session.dds_status=request.vars.dds_status  
        session.submit_date=request.vars.submit_date
        reqPage=0
    
    elif btn_all_leave:
        session.btn_filter_leave=None
        session.EMPID=None        
        session.from_date=None 
        session.to_date=None
        session.type_l=None
        session.ah_status=None
        session.zh_status=None
        session.dh_status=None
        session.ddm_status=None
        session.dds_status=None 
        session.submit_date=None  

        reqPage=0
        
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
    qset=qset(db.sm_leave_application.cid==c_id)
        
    # Set filter type. Create select sql based on search type    

    if (session.btn_filter_leave!=None and session.from_date!='' and session.from_date!=None and session.to_date!='' and session.to_date!=None):
        qset = qset(db.sm_leave_application.from_date >= session.from_date)
        qset = qset(db.sm_leave_application.to_date <= session.to_date)  

    
    if (session.btn_filter_leave!=None and session.EMPID!=None and session.EMPID!=''):        
        emp_id=str(session.EMPID).split('|')[0]       
        qset=qset(db.sm_leave_application.emp_id==emp_id)

    if (session.btn_filter_leave!=None and session.submit_date!='' and session.submit_date!=None ):
        submit_date=str(session.submit_date)
        date_from=submit_date
        now = datetime.datetime.strptime(submit_date, "%Y-%m-%d")
        date_ton=now + datetime.timedelta(days = 1)
        date_to=str(date_ton).split(' ')[0]
        # return submit_date
        # qset = qset(db.sm_leave_application.created_on >= submit_date)
        qset = qset(db.sm_leave_application.created_on >= submit_date)  
        qset = qset(db.sm_leave_application.created_on < date_to)  

    if (session.btn_filter_leave!=None and session.type_l!=None and session.type_l!=''):        
        type_l=str(session.type_l)
        qset=qset(db.sm_leave_application.leave_type==type_l)

    if (session.btn_filter_leave!=None and session.ah_status!=None and session.ah_status!=''):        
        ah_status=str(session.ah_status)
        qset=qset(db.sm_leave_application.area_head_status==ah_status)

    if (session.btn_filter_leave!=None and session.zh_status!=None and session.zh_status!=''):        
        zh_status=str(session.zh_status)
        qset=qset(db.sm_leave_application.zonal_head_status==zh_status)

    
    if (session.btn_filter_leave!=None and session.dh_status!=None and session.dh_status!=''):        
        dh_status=str(session.dh_status)
        qset=qset(db.sm_leave_application.divisional_head_status==dh_status)

    
    if (session.btn_filter_leave!=None and session.ddm_status!=None and session.ddm_status!=''):        
        ddm_status=str(session.ddm_status)
        qset=qset(db.sm_leave_application.ddm_status==ddm_status)

    if (session.btn_filter_leave!=None and session.dds_status!=None and session.dds_status!=''):        
        dds_status=str(session.dds_status)
        qset=qset(db.sm_leave_application.director_marktng_status==dds_status)
    

    #------------
    records=qset.select(db.sm_leave_application.ALL,orderby=~db.sm_leave_application.id,limitby=limitby)
    totalCount=qset.count()
    
    return dict(records=records,totalCount=totalCount,page=page,items_per_page=items_per_page)
  
def download_leave_list():
    c_id=session.cid
    task_id='rm_item_manage'
    task_id_view='rm_item_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))
    
    
    cid=session.cid
    qset=db()
    qset=qset(db.sm_leave_application.cid==c_id)
        
    # Set filter type. Create select sql based on search type    

    if (session.btn_filter_leave!=None and session.from_date!='' and session.from_date!=None and session.to_date!='' and session.to_date!=None):
        qset = qset(db.sm_leave_application.from_date >= session.from_date)
        qset = qset(db.sm_leave_application.to_date <= session.to_date)  

    
    if (session.btn_filter_leave!=None and session.EMPID!=None and session.EMPID!=''):        
        emp_id=str(session.EMPID).split('|')[0]       
        qset=qset(db.sm_leave_application.emp_id==emp_id)

    if (session.btn_filter_leave!=None and session.submit_date!='' and session.submit_date!=None ):
        submit_date=str(session.submit_date)
        date_from=submit_date
        now = datetime.datetime.strptime(submit_date, "%Y-%m-%d")
        date_ton=now + datetime.timedelta(days = 1)
        date_to=str(date_ton).split(' ')[0]
        # return submit_date
        # qset = qset(db.sm_leave_application.created_on >= submit_date)
        qset = qset(db.sm_leave_application.created_on >= submit_date)  
        qset = qset(db.sm_leave_application.created_on < date_to)  

    if (session.btn_filter_leave!=None and session.type_l!=None and session.type_l!=''):        
        type_l=str(session.type_l)
        qset=qset(db.sm_leave_application.leave_type==type_l)

    if (session.btn_filter_leave!=None and session.ah_status!=None and session.ah_status!=''):        
        ah_status=str(session.ah_status)
        qset=qset(db.sm_leave_application.area_head_status==ah_status)

    if (session.btn_filter_leave!=None and session.zh_status!=None and session.zh_status!=''):        
        zh_status=str(session.zh_status)
        qset=qset(db.sm_leave_application.zonal_head_status==zh_status)

    
    if (session.btn_filter_leave!=None and session.dh_status!=None and session.dh_status!=''):        
        dh_status=str(session.dh_status)
        qset=qset(db.sm_leave_application.divisional_head_status==dh_status)

    
    if (session.btn_filter_leave!=None and session.ddm_status!=None and session.ddm_status!=''):        
        ddm_status=str(session.ddm_status)
        qset=qset(db.sm_leave_application.ddm_status==ddm_status)

    if (session.btn_filter_leave!=None and session.dds_status!=None and session.dds_status!=''):        
        dds_status=str(session.dds_status)
        qset=qset(db.sm_leave_application.director_marktng_status==dds_status)
    

    #------------
    records=qset.select(db.sm_leave_application.ALL,orderby=~db.sm_leave_application.id)

    
    #Create string for download as excel file
    myString='Leave List\n\n'

    myString+='Employee,Name,Submit Date,From Date,To Date,Total Leave,Type,Area Head ID,Name,Area Head Status,Zonal Head ID,Name,Zonal Head Status,Divisional Head ID,Name, Divisional Head Status,DDM ID,Name,DDM Status,DM ID,Name,DM Status,Note\n'
    #Replace coma from records. cause coma means new Column    
    for rec in records:
        emp_id=rec.emp_id
        emp_name=str(rec.emp_name).replace(',', ' ')
        created_on=str(rec.created_on)
        from_date=rec.from_date
        to_date=rec.to_date
        total_leave=rec.total_leave
        leave_type=str(rec.leave_type)        
        ared_head_id=rec.ared_head_id
        ared_head_name=rec.ared_head_name
        area_head_status=rec.area_head_status        
        zonal_head_id=rec.zonal_head_id
        zonal_head_name=rec.zonal_head_name
        zonal_head_status=rec.zonal_head_status
        divisional_head_id=str(rec.divisional_head_id)
        divisional_head_name=str(rec.divisional_head_name).replace(',', ' ')
        divisional_head_status=rec.divisional_head_status
        ddm_id=rec.ddm_id
        ddm_name=rec.ddm_name
        ddm_status=str(rec.ddm_status)
        director_id=rec.director_id
        director_name=rec.director_name.replace(',', ' ')
        director_marktng_status=rec.director_marktng_status        
        note=rec.note
                
        
        myString+=str(emp_id)+','+str(emp_name)+','+str(created_on)+','+str(from_date)+','+str(to_date)+','+str(total_leave)+','+str(leave_type)+','+str(ared_head_id)+','+str(ared_head_name)+','+str(area_head_status)+','+str(zonal_head_id)+','+str(zonal_head_name)+','+str(zonal_head_status)+','+str(divisional_head_id)+','+str(divisional_head_name)+','+str(divisional_head_status)+','+str(ddm_id)+','+str(ddm_name)+','+str(ddm_status)+','+str(director_id)+','+str(director_name)+','+str(director_marktng_status)+','+str(note)+'\n'
        
    #-----------
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_leave_list.csv'   
    return str(myString)










def get_rep_list():
    retStr = ''
    cid = session.cid    

    rows = db((db.sm_rep.cid == cid) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.rep_id, db.sm_rep.name, db.sm_rep.mobile_no, orderby=db.sm_rep.name)
            
    for row in rows:
        rep_id = str(row.rep_id)
        name = str(row.name).replace('|', ' ').replace(',', ' ')
        mobile_no = str(row.mobile_no)

        if retStr == '':
            retStr = rep_id + '|' + name + '|' + mobile_no
        else:
            retStr += ',' + rep_id + '|' + name + '|' + mobile_no

    return retStr


def get_leave_type():
    relStr = ''
    cid = session.cid    

    rows = db((db.sm_leave_type.cid == cid)).select(db.sm_leave_type.leave_type, orderby=db.sm_leave_type.leave_type)
            
    for row in rows:
        leave_type = str(row.leave_type)
        
        if relStr == '':
            relStr = leave_type 
        else:
            relStr += ',' + leave_type 

    return relStr


