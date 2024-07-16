

def visitPlan():
    c_id=session.cid
    response.title='Visit Plan'
    
       
    #------------------------filter
    btn_filter=request.vars.btn_filter
    btn_rep_all=request.vars.btn_rep_all
    if btn_filter:
        session.btn_filter=btn_filter
        session.search_dateFrom=str(request.vars.search_dateFrom).strip()
        session.search_dateTo=str(request.vars.search_dateTo).strip()
        session.search_rep=str(request.vars.search_rep).strip()
        session.search_microunion=str(request.vars.search_microunion).strip()
        session.search_area=str(request.vars.search_area).strip()
        session.search_reg=str(request.vars.search_reg).strip().upper()
        session.search_zone=str(request.vars.search_zone).strip().upper()
        
    elif btn_rep_all:
        session.btn_filter=None
        session.search_dateFrom=None
        session.search_dateTo=None
        session.search_rep=None
        session.search_microunion=None
        session.search_area=None
        session.search_reg=None
        session.search_zone=None
        
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
    qset=qset(db.sm_doctor_visit_plan.cid==c_id)
    qset=qset(db.sm_microunion.cid==c_id)
    qset=qset(db.sm_doctor_visit_plan.route_id==db.sm_microunion.microunion_id)
    qset=qset(db.sm_doctor_visit_plan.route_name==db.sm_microunion.microunion_name)
    
    
  
    if (session.btn_filter):
        #------------

        if ((session.search_dateFrom!="") & (session.search_dateTo!="")):
            qset=qset((db.sm_doctor_visit_plan.schedule_date>=session.search_dateFrom) & (db.sm_doctor_visit_plan.schedule_date<=session.search_dateTo))
        if (session.search_rep!="") :
            searchrep=str(session.search_rep).split('|')[0]
            qset=qset(db.sm_doctor_visit_plan.rep_id==searchrep)
        if (session.search_microunion!="") :
            searchMicrounion=str(session.search_microunion).split('|')[0]
            qset=qset(db.sm_microunion.microunion_id==searchMicrounion)
        if (session.search_area!="") :
            searchArea=str(session.search_area).split('|')[0]
            qset=qset(db.sm_microunion.area_id==searchArea)
        if (session.search_reg!="") :
            searchReg=str(session.search_reg).split('|')[0]
            qset=qset(db.sm_microunion.level2==searchReg)
        if (session.search_zone!="") :
            searchZone=str(session.search_zone).split('|')[0]
            qset=qset(db.sm_microunion.level1==searchZone)
            
            
    #------------
    records=qset.select(db.sm_doctor_visit_plan.rep_id,db.sm_doctor_visit_plan.rep_name,db.sm_microunion.microunion_id,db.sm_microunion.microunion_name,db.sm_microunion.area_id,db.sm_microunion.area_name,db.sm_microunion.level1,db.sm_microunion.level1_name,db.sm_microunion.level2,db.sm_microunion.level2_name,db.sm_doctor_visit_plan.schedule_date,db.sm_doctor_visit_plan.status,orderby=db.sm_doctor_visit_plan.rep_name|db.sm_doctor_visit_plan.schedule_date,limitby=limitby)
#     return db._lastsql
    totalCount=qset.count()
#     return db._lastsql
    #-------------- filter end
    
    return dict(records=records,totalCount=totalCount,page=page,items_per_page=items_per_page)
    


def get_rep_list():
    retStr = ''
    cid = session.cid


    rows = db((db.sm_rep.cid == cid) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.rep_id, db.sm_rep.name, db.sm_rep.mobile_no, orderby=db.sm_rep.name)
            
    for row in rows:
        rep_id = str(row.rep_id)
        name = str(row.name).replace('|', ' ').replace(',', ' ')
        mobile_no = str(row.mobile_no)

        if retStr == '':
            retStr = rep_id + '|' + name 
        else:
            retStr += ',' + rep_id + '|' + name 

    return retStr

def get_microunion_list():
    retStr = ''
    cid = session.cid
    rows = db((db.sm_microunion.cid == cid) ).select(db.sm_microunion.microunion_id, db.sm_microunion.microunion_name, orderby=db.sm_microunion.microunion_name)
            
    for row in rows:
        get_id = str(row.microunion_id)
        name = str(row.microunion_name).replace('|', ' ').replace(',', ' ')
        

        if retStr == '':
            retStr = get_id + '|' + name 
        else:
            retStr += ',' + get_id + '|' + name 

    return retStr

def get_area_list():
    retStr = ''
    cid = session.cid
    rows = db((db.sm_microunion.cid == cid) ).select(db.sm_microunion.area_id, db.sm_microunion.area_name, orderby=db.sm_microunion.area_name)
            
    for row in rows:
        get_id = str(row.area_id)
        name = str(row.area_name).replace('|', ' ').replace(',', ' ')
        

        if retStr == '':
            retStr = get_id + '|' + name 
        else:
            retStr += ',' + get_id + '|' + name 
    return retStr

def get_region_list():
    retStr = ''
    cid = session.cid
    rows = db((db.sm_microunion.cid == cid) ).select(db.sm_microunion.level2, db.sm_microunion.level2_name, orderby=db.sm_microunion.level2_name)
            
    for row in rows:
        get_id = str(row.level2)
        name = str(row.level2_name).replace('|', ' ').replace(',', ' ')
        

        if retStr == '':
            retStr = get_id + '|' + name 
        else:
            retStr += ',' + get_id + '|' + name 


    return retStr

def get_zone_list():
    retStr = ''
    cid = session.cid
    rows = db((db.sm_microunion.cid == cid) ).select(db.sm_microunion.level1, db.sm_microunion.level1_name, orderby=db.sm_microunion.level1_name)
      
    for row in rows:
        get_id = str(row.level1)
        name = str(row.level1_name).replace('|', ' ').replace(',', ' ')
        if retStr == '':
            retStr = get_id + '|' + name 
        else:
            retStr += ',' + get_id + '|' + name 
  
    return retStr