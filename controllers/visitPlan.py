

def index():
    c_id=session.cid
    response.title='Tour Plan'
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=session.items_per_page
    limitby=(page*items_per_page,(page+1)*items_per_page+1)

    
    
    firstDate = request.vars.firstDate
    btn_summary=request.vars.btn_summary
    btn_detail=request.vars.btn_detail
    
    
    if btn_summary: 
        search_year=request.vars.search_year
        search_month=request.vars.search_month
        from_date=str(search_year)+'-'+str(search_month)+'-'+'01'
        to_month=int(search_month)+1
        
        if (int(to_month)<10):
            to_month='0'+str(to_month)
            
        if (int(to_month)==12):
            search_year_1=int(search_year)+1
            search_year_to=str(search_year_1)
        else:
            search_year_to=search_year
            
        to_date=str(search_year_to)+'-'+str(to_month)+'-'+'01'
        

        redirect (URL('visitPlan','summary',vars=dict(from_date=from_date,to_date=to_date,s_flag=1)))
    elif btn_detail:
        redirect (URL(c='visitPlan', f='visitPlan'))




    return dict()



def visitPlan():
    c_id=session.cid
    
    search_form =SQLFORM(db.sm_search_date)
    
    response.title='Visit Plan'
    
       
    #------------------------filter
    btn_filter=request.vars.btn_filter
    btn_rep_all=request.vars.btn_rep_all
    if btn_filter:
        session.btn_filter=btn_filter
        session.from_dt=str(request.vars.from_dt).strip()        
        session.to_dt=str(request.vars.to_dt).strip()
        session.search_rep=str(request.vars.search_rep).strip()
        session.search_microunion=str(request.vars.search_microunion).strip()
        session.search_area=str(request.vars.search_area).strip()
        session.search_reg=str(request.vars.search_reg).strip().upper()
        session.search_zone=str(request.vars.search_zone).strip().upper()
#         return session.search_rep
    elif btn_rep_all:
        session.btn_filter=None
        session.from_dt=None
        session.to_dt=None
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

        if ((session.from_dt!="") & (session.to_dt!="")):
            qset=qset((db.sm_doctor_visit_plan.schedule_date>=session.from_dt) & (db.sm_doctor_visit_plan.schedule_date<=session.to_dt))
       
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
#     return records
    totalCount=qset.count()
#     return db._lastsql
    #-------------- filter end
    
    return dict(search_form=search_form,records=records,totalCount=totalCount,page=page,items_per_page=items_per_page)
    


def download_visit_plan():
    
    c_id=session.cid

    btn_filter=request.vars.btn_filter
    btn_rep_all=request.vars.btn_rep_all
    
    
    if btn_filter:
        session.btn_filter=btn_filter
        session.from_dt=str(request.vars.from_dt).strip()
        session.to_dt=str(request.vars.to_dt).strip()
        session.search_rep=str(request.vars.search_rep).strip()
        session.search_microunion=str(request.vars.search_microunion).strip()
        session.search_area=str(request.vars.search_area).strip()
        session.search_reg=str(request.vars.search_reg).strip().upper()
        session.search_zone=str(request.vars.search_zone).strip().upper()
        
    elif btn_rep_all:
        session.btn_filter=None
        session.from_dt=None
        session.to_dt=None
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

        if ((session.from_dt!="") & (session.to_dt!="")):
            qset=qset((db.sm_doctor_visit_plan.schedule_date>=session.from_dt) & (db.sm_doctor_visit_plan.schedule_date<=session.to_dt))
        
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
            
                
    else:
        session.flash = 'Filter Required'
        redirect (URL('visitPlan'))
    
    records=qset.select(db.sm_doctor_visit_plan.rep_id,db.sm_doctor_visit_plan.rep_name,db.sm_microunion.microunion_id,db.sm_microunion.microunion_name,db.sm_microunion.area_id,db.sm_microunion.area_name,db.sm_microunion.level1,db.sm_microunion.level1_name,db.sm_microunion.level2,db.sm_microunion.level2_name,db.sm_doctor_visit_plan.schedule_date,db.sm_doctor_visit_plan.status,orderby=db.sm_doctor_visit_plan.rep_name|db.sm_doctor_visit_plan.schedule_date)
#     return records

    myString='Visit Plan List\n''\n'
    
    myString+='From:'+str(session.from_dt)+','+'To:'+str(session.to_dt)+'\n''\n'
    
    myString+='RepID, RepName, MicrounionID, MicrounionName, Territory ID, Territory Name, AreaID, Area Name, Region ID, Region Name\n' 
    
    for rec in records:
        rep_id=str(rec.sm_doctor_visit_plan.rep_id)
        rep_name=str(rec.sm_doctor_visit_plan.rep_name).replace(',', ' ')        
        
        microunion_id=str(rec.sm_microunion.microunion_id)
        microunion_name=str(rec.sm_microunion.microunion_name).replace(',', ' ')
        area_id=str(rec.sm_microunion.area_id)
        area_name=str(rec.sm_microunion.area_name).replace(',', ' ')        
        
        level2=str(rec.sm_microunion.level2)
        level2_name=str(rec.sm_microunion.level2_name).replace(',', ' ')
        
        level1=str(rec.sm_microunion.level1)
        level1_name=str(rec.sm_microunion.level1_name).replace(',', ' ')        
        

     
        myString+=str(rep_id)+','+str(rep_name)+','+str(microunion_id)+','+str(microunion_name)+','+str(area_id)+','+str(area_name)+','+str(level2)+','+str(level2_name)+','+str(level1)+','+str(level1_name)+'\n'

    #Save as csv
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_visit_plan.csv'   
    return str(myString)



def summary():
    c_id=session.cid
    response.title='Summary'

    #  ---------------filter-------
    from_date=request.vars.from_date
    session.from_date=from_date
    to_date=request.vars.to_date
    s_flag=request.vars.s_flag

    btn_filter_s = request.vars.btn_filter
    btn_all = request.vars.btn_filter_all
    reqPage = len(request.args)

    if reqPage:
        page=int(request.args[0])
    else:
        page=0

    items_per_page=session.items_per_page
    limitby=(page*items_per_page,(page+1)*items_per_page+1)

    
    if s_flag==1:
        
        session.searchType_s = None
        session.searchValue_s = None
 
    if btn_filter_s:
        session.searchType_s = str(request.vars.search_type).strip()
        session.searchValue_s = str(request.vars.search_value).strip().upper()
        session.from_date=str(request.vars.from_date).strip()
        session.to_date=str(request.vars.to_date).strip()
        reqPage = 0

    elif btn_all:
       
        session.searchType_s = None
        session.searchValue_s = None
        session.from_date = None
        session.to_date = None
       
        reqPage = 0
    session.items_per_page=20
    if reqPage:
        page=int(request.args[0])
    else:
        page=0

#     #--------paging
    qset=db()
    qset = qset(db.sm_doctor_visit_plan.cid == c_id)
    qset = qset(db.sm_doctor_visit_plan.first_date >= from_date) 
    qset=qset(db.sm_doctor_visit_plan.first_date < to_date)
  
    

    if (btn_filter_s):
        if (session.searchType_s == 'empID'):
            searchValue=str(session.searchValue_s).split('|')[0]
            qset = qset(db.sm_doctor_visit_plan.rep_id == searchValue)


    records=qset.select(db.sm_doctor_visit_plan.first_date,db.sm_doctor_visit_plan.rep_id,db.sm_doctor_visit_plan.rep_name,db.sm_doctor_visit_plan.schedule_date,db.sm_doctor_visit_plan.status,orderby=~db.sm_doctor_visit_plan.first_date|db.sm_doctor_visit_plan.rep_id,groupby=db.sm_doctor_visit_plan.first_date|db.sm_doctor_visit_plan.rep_id,limitby=limitby)
    # return records
    totalCount=qset.count()
    return dict(records=records,totalCount=totalCount, page=page, items_per_page=items_per_page,from_date=from_date,to_date=to_date)


def download_summary():
    to_date=''
    totalCount=''
    c_id=session.cid
    response.title='Summary'

    #  ---------------filter-------
    from_date=request.vars.from_date
    to_date=request.vars.to_date
    s_flag=request.vars.s_flag
#     return s_flag
    btn_filter_s = request.vars.btn_filter
    btn_all = request.vars.btn_filter_all
    reqPage=len(request.args)

    
    if s_flag==1:
        
        session.searchType_s = None
        session.searchValue_s = None
        # reqPage = 0
    if btn_filter_s:
        session.searchType_s = str(request.vars.search_type).strip()
        session.searchValue_s = str(request.vars.search_value).strip().upper()
        session.from_date=str(request.vars.from_date).strip()
        session.to_date=str(request.vars.to_date).strip()

        reqPage = 0

    elif btn_all:
       
        session.searchType_s = None
        session.searchValue_s = None
        session.from_date = None
        session.to_date = None

        reqPage = 0
    session.items_per_page=20
    if reqPage:
        page=int(request.args[0])
    else:
        page=0

    items_per_page=session.items_per_page
    limitby=(page*items_per_page,(page+1)*items_per_page+1)

#     #--------paging
    qset=db()
    qset = qset(db.sm_doctor_visit_plan.cid == c_id)
    qset = qset(db.sm_doctor_visit_plan.first_date >= from_date) 
    qset=qset(db.sm_doctor_visit_plan.first_date < to_date)
#     
    

    if (btn_filter_s):
        if (session.searchType_s == 'empID'):
            searchValue=str(session.searchValue_s).split('|')[0]
            qset = qset(db.sm_doctor_visit_plan.rep_id == searchValue)
            
            
    records=qset.select(db.sm_doctor_visit_plan.first_date,db.sm_doctor_visit_plan.rep_id,db.sm_doctor_visit_plan.rep_name,db.sm_doctor_visit_plan.schedule_date,db.sm_doctor_visit_plan.status,orderby=~db.sm_doctor_visit_plan.first_date|db.sm_doctor_visit_plan.rep_id,groupby=db.sm_doctor_visit_plan.first_date|db.sm_doctor_visit_plan.rep_id,limitby=limitby)  
    

    myString='Summary List\n\n'
    myString+='FirstDate,Employee ID,Employee Name,Status\n'
    for rec in records:
        first_date=str(rec.first_date)
        rep_id=str(rec.rep_id)
        rep_name=str(rec.rep_name)
        status=str(rec.status)

        myString+=first_date+','+rep_id+','+rep_name+','+status+'\n'

    #Sve as csv
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_summary.csv'
    return str(myString)


def visitDetail():
    c_id=session.cid
    response.title='Detail'

    #  ---------------filter-------
    from_date=request.vars.from_date
    to_date=request.vars.to_date
    firstDate = request.vars.firstDate
    repID = request.vars.repID
    btn_back = request.vars.btn_back
    
    if btn_back:
        session.from_date=str(request.vars.from_date).strip()
        session.to_date=str(request.vars.to_date).strip()
    reqPage = len(request.args)
#     return firstDate
    #--------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=session.items_per_page
    limitby=(page*items_per_page,(page+1)*items_per_page+1)

    # limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #--------end paging

    qset=db()
    qset = qset(db.sm_doctor_visit_plan.cid == c_id)
    qset = qset(db.sm_doctor_visit_plan.first_date == firstDate)
    qset = qset(db.sm_doctor_visit_plan.rep_id == repID)
#     qset=qset(db.sm_doctor_visit_plan.route_id==db.sm_microunion.microunion_id)
#     qset=qset(db.sm_doctor_visit_plan.route_name==db.sm_microunion.microunion_name)

    records=qset.select(db.sm_doctor_visit_plan.note,db.sm_doctor_visit_plan.first_date,db.sm_doctor_visit_plan.rep_id,db.sm_doctor_visit_plan.rep_name,db.sm_doctor_visit_plan.route_id,db.sm_doctor_visit_plan.route_name,db.sm_doctor_visit_plan.schedule_date,db.sm_doctor_visit_plan.status,orderby=db.sm_doctor_visit_plan.schedule_date)
#     return records
    for rec in records:
        rep_name=rec[db.sm_doctor_visit_plan.rep_name]
        
    totalCount=qset.count()

    return dict(records=records,totalCount=totalCount, page=page,from_date=from_date,to_date=to_date, items_per_page=items_per_page,rep_name=rep_name,repID=repID,firstDate=firstDate)

def download_visitDetail():
    c_id=session.cid
    response.title='Detail'

    #  ---------------filter-------

    firstDate = request.vars.firstDate
    repID = request.vars.repID
    rep_name = request.vars.rep_name


#     return firstDate
    #--------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=session.items_per_page
    limitby=(page*items_per_page,(page+1)*items_per_page+1)


    # limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #--------end paging

    qset=db()
    qset = qset(db.sm_doctor_visit_plan.cid == c_id)
    qset = qset(db.sm_doctor_visit_plan.first_date == firstDate)
    qset = qset(db.sm_doctor_visit_plan.rep_id == repID)
#     qset=qset(db.sm_doctor_visit_plan.route_id==db.sm_microunion.microunion_id)
#     qset=qset(db.sm_doctor_visit_plan.route_name==db.sm_microunion.microunion_name)

    records=qset.select(db.sm_doctor_visit_plan.note,db.sm_doctor_visit_plan.first_date,db.sm_doctor_visit_plan.rep_id,db.sm_doctor_visit_plan.rep_name,db.sm_doctor_visit_plan.route_id,db.sm_doctor_visit_plan.route_name,db.sm_doctor_visit_plan.schedule_date,db.sm_doctor_visit_plan.status,orderby=db.sm_doctor_visit_plan.schedule_date)
    # return records
    myString='Detail List\nEmp, '
    myString+=str(rep_name)+','+repID+'\n\n'
    myString+='ScheduleDate,Territory ID,Territory Name,VisitTime,Status\n'
    
    for rec in records:
        rep_id=str(rec.rep_id)
        rep_name=str(rec.rep_name)
        
        schedule_date=str(rec.schedule_date)
        route_id=str(rec.route_id)
        route_name=str(rec.route_name)
        note=str(rec.note)
        status=str(rec.status)
        
        
        myString+=schedule_date+','+route_id+','+route_name+','+note+','+status+'\n'

    #Sve as csv
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_detail.csv'
    return str(myString)

def visitConfirm():
    c_id=session.cid
    response.title='Detail'

    #  ---------------filter-------
   
    firstDate = request.vars.firstDate
    repID = request.vars.repID
    db((db.sm_doctor_visit_plan.cid == c_id) & (db.sm_doctor_visit_plan.first_date == firstDate) & (db.sm_doctor_visit_plan.rep_id == repID)).update(status='Confirmed')

    redirect (URL('visitDetail',vars=dict(repID=repID,firstDate=firstDate)))

def visitCancel():
    c_id=session.cid
    response.title='Detail'

    firstDate = request.vars.firstDate
    repID = request.vars.repID
    db((db.sm_doctor_visit_plan.cid == c_id) & (db.sm_doctor_visit_plan.first_date == firstDate) & (db.sm_doctor_visit_plan.rep_id == repID)).update(status='Cancelled')
    
    redirect (URL('visitDetail',vars=dict(repID=repID,firstDate=firstDate)))

def get_empID_list():
    retStr = ''
    cid = session.cid


    rows = db(db.sm_doctor_visit_plan.cid == cid).select(db.sm_doctor_visit_plan.rep_id, db.sm_doctor_visit_plan.rep_name, orderby=db.sm_doctor_visit_plan.rep_id)

    for row in rows:
        rep_id = str(row.rep_id)
        name = str(row.rep_name).replace('|', ' ').replace(',', ' ')

        if retStr == '':
            retStr = rep_id + '|' + name
        else:
            retStr += ',' + rep_id + '|' + name

    return retStr

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
