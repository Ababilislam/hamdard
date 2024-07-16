import math
import os
import calendar
import urllib2

def sub_months(sourcedate, months):    
    month = sourcedate.month - 1 - months
    year = sourcedate.year + month / 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year, month)[1])
    return datetime.date(year, month, day)
    

# =============== 20190214 start===============

def tracking():
    
    c_id=session.cid
    response.title='Tracking'
     
    from_dt=request.vars.from_dt
    to_dt=request.vars.to_dt  
    #------------------------filter
    btn_filter_rep=request.vars.btn_filter
    btn_rep_all=request.vars.btn_rep_all
    if btn_filter_rep:
        session.btn_filter_rep=btn_filter_rep
        session.search_type_rep=str(request.vars.search_type).strip()
        session.search_value_rep=str(request.vars.search_value).strip().upper()
        session.from_dt=from_dt
        session.to_dt=to_dt
        
    elif btn_rep_all:
        session.btn_filter_rep=None
        session.search_type_rep=None
        session.search_value_rep=None
        session.from_dt=None
        session.to_dt=None
        
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
    qset=qset(db. sm_tracking_table.cid==c_id)
    
      
    if (session.btn_filter_rep):

       
        #------------
        if (session.search_type_rep=='RepID'):
            searchValue=str(session.search_value_rep).split('|')[0]
            qset=qset(db.sm_tracking_table.rep_id==searchValue)            
        
        
        elif (session.search_type_rep == 'Type'):
            searchValue=str(session.search_value_rep)
            qset = qset(db.sm_tracking_table.call_type == searchValue)
    
    if (session.from_dt and session.to_dt)!='' and (session.from_dt and session.to_dt)!=None:                    
        qset=qset((db.sm_tracking_table.visit_date >= session.from_dt) & (db.sm_tracking_table.visit_date <= session.to_dt))
    
        #------------
            
    #------------
    records=qset.select(db.sm_tracking_table.ALL,orderby=~db.sm_tracking_table.id,limitby=limitby)
    totalCount=qset.count()
    
    return dict(records=records,totalCount=totalCount,page=page,items_per_page=items_per_page,from_dt=from_dt,to_dt=to_dt)

#============================================== Download
def download_tracking():
    c_id=session.cid
    response.title='Tracking'
     
    from_dt=request.vars.from_dt
    to_dt=request.vars.to_dt  
    #------------------------filter
    btn_filter_rep=request.vars.btn_filter
    btn_rep_all=request.vars.btn_rep_all
    if btn_filter_rep:
        session.btn_filter_rep=btn_filter_rep
        session.search_type_rep=str(request.vars.search_type).strip()
        session.search_value_rep=str(request.vars.search_value).strip().upper()
        session.from_dt=from_dt
        session.to_dt=to_dt
        
    elif btn_rep_all:
        session.btn_filter_rep=None
        session.search_type_rep=None
        session.search_value_rep=None
        session.from_dt=None
        session.to_dt=None
        
    #   -----------
    qset=db()
    qset=qset(db.sm_tracking_table.cid==c_id)
    
      
    if (session.btn_filter_rep):
        
        if (session.search_type_rep=='RepID'):
            searchValue=str(session.search_value_rep).split('|')[0]
            qset=qset(db.sm_tracking_table.rep_id==searchValue)            
        
        
        elif (session.search_type_rep == 'Type'):
            searchValue=str(session.search_value_rep)
            qset = qset(db.sm_tracking_table.call_type == searchValue)
    
        if (session.from_dt and session.to_dt)!='' and (session.from_dt and session.to_dt)!=None:                    
            qset=qset((db.sm_tracking_table.visit_date >= session.from_dt) & (db.sm_tracking_table.visit_date <= session.to_dt))
    
        #------------
            
    #------------
    records=qset.select(db.sm_tracking_table.ALL,orderby=~db.sm_tracking_table.id)
   
    myString='Tracking List\n'

    myString+='Visit Date ,Visit Time,User Id,Name,Type,Visited Id,Visited Name,Location\n'
    for rec in records:
        visit_date=(rec.visit_date)
        visit_time=(str(rec.visit_time).split(' ')[1])
        rep_id=(rec.rep_id)
        rep_name=(rec.rep_name)
        call_type=(rec.call_type)
        visited_id=(rec.visited_id)
        visited_name=(rec.visited_name)

        myString+=str(visit_date)+','+str(visit_time)+','+str(rep_id)+','+str(rep_name)+','+str(call_type)+','+str(visited_id)+','+str(visited_name)+'\n'
        
    #Save as csv
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_tracking.csv'   
    return str(myString)


def get_type():
    retStr=''
    c_id = session.cid
#     return c_id
    
    records=db((db.sm_tracking_table.cid == c_id)).select(db.sm_tracking_table.call_type, orderby=db.sm_tracking_table.call_type, groupby=db.sm_tracking_table.call_type)
    
    for row in records:
        call_type=str(row.call_type)

        if retStr == '':
            retStr = call_type 
        else:
            retStr += ',' + call_type 
    
    return retStr

# =============== 20190214 end===============
    