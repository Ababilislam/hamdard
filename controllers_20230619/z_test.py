from random import randint
import urllib2
import calendar
import urllib
import time


def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month / 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year, month)[1])
    return datetime.date(year, month, day)
def deduct_months(sourcedate, months):
    month = sourcedate.month - 1 - months
    year = sourcedate.year + month / 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year, month)[1])
    return datetime.date(year, month, day)




# Unscheduled
# http://127.0.0.1:8000/vitalac/z_test/order?cid=VITALAC&uid=0469&password=123

# http://127.0.0.1:8000/lscmreporting/syncmobile/visitSubmit?cid=LSCRM&rep_id=101&rep_pass=123&synccode=5771&client_id=1&visit_type=&schedule_date=&market_info=1&order_info=1&merchandizing=1&lat=0&long=0
# http://127.0.0.1:8000/lscmreporting/syncmobile/visitSubmit?cid=LSCRM&rep_id= 1004&rep_pass=6085&synccode=&client_id=R100585&visit_type=Scheduled&market_info= Akiz <fd> 500 <fd> 2000 <fd> 12000 <fd> 320 <fd> 2 <fd> 1.0 <fd> Good <rd>Seven Ring <fd> 200 <fd> 800 <fd> 3000 <fd> 400 <fd> 0  <fd> 5 <fd> So Good &order_info=1800106001 <fd> 5 <rd>1800201001<fd> 100&merchandizing=1 <fd> Calender <fd> 2 <fd> 2014-09-08 <fd> YES <fd> GOOD<fd> NO <fd> 0 <rd>2 <fd> Wall Paint <fd> 1 <fd> 2014-09-01 <fd> NO <fd> BAD <fd> NO<fd> 1 &lat=0&long=0
def order():
    cid = str(request.vars.cid).strip().upper()
    uid = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.rep_pass).strip()
#     return password
    session.cid = cid
    session.uid = uid
    session.password = password

    visit = ''
    
    # if cid,userid,pass blank
    if (cid == '' or uid == '' or password == ''):
        session.flash = 'CID,User ID and Password required !'
        redirect(URL('index'))
        
    mac_hdd = str(request.vars.uploadkey)
    # Note: Supervisor device checking depend on settings, others device checking from cpanel
    
    # mac_hdd='123HDSN123'    # temporary used for java
    
    
    supervisorRows=db((db.sm_rep.cid==cid) & (db.sm_rep.rep_id==uid)  & (db.sm_rep.password==password)  & (db.sm_rep.user_type=='sup') & (db.sm_rep.status=='ACTIVE')).select(db.sm_rep.level_id,db.sm_rep.field2,limitby=(0,1))
#     return supervisorRows
#     return db._lastsql
    if supervisorRows:
        level_id=supervisorRows[0].level_id
       
        
        level_idList=[]
        depthList=[]        
#         marketList=[]
        levelList=[]
        distributorList = []

        compSettingsRows = db((db.sm_company_settings.cid == cid) & (db.sm_company_settings.status == 'ACTIVE')).select(db.sm_company_settings.status, limitby=(0, 1))
#         return db._lastsql
#         return compSettingsRows
        if compSettingsRows:
            sysItemPerPageRows = db(db.sm_settings.cid == session.cid).select()
            for records in sysItemPerPageRows:
                s_key = records.s_key
                value = records.s_value
                if (s_key == 'ITEM_PER_PAGE'):
                    itemPerPage = int(value)
#                     return itemPerPage
                    session.items_per_page = itemPerPage


            #======= Level Name Settings
            level0Name = ''
            level1Name = ''
            level2Name = ''
            level3Name = ''
            level4Name = ''
            level5Name = ''
            level6Name = ''
            level7Name = ''
            level8Name = ''
            
            records_levelsettings = db(db.level_name_settings.cid == cid).select(db.level_name_settings.ALL, orderby=db.level_name_settings.depth)
            for records_level in records_levelsettings:
                levelDepth = str(records_level.depth)
                levelName = str(records_level.name)
                if levelDepth == '0':
                    level0Name = levelName
                elif levelDepth == '1':
                    level1Name = levelName
                elif levelDepth == '2':
                    level2Name = levelName
                elif levelDepth == '3':
                    level3Name = levelName
                elif levelDepth == '4':
                    level4Name = levelName
                elif levelDepth == '5':
                    level5Name = levelName
                elif levelDepth == '6':
                    level6Name = levelName
                elif levelDepth == '7':
                    level7Name = levelName
                elif levelDepth == '8':
                    level8Name = levelName
            
            session.level0Name = level0Name
            session.level1Name = level1Name
            session.level2Name = level2Name
            session.level3Name = level3Name
            session.level4Name = level4Name
            session.level5Name = level5Name
            session.level6Name = level6Name
            session.level7Name = level7Name
            session.level8Name = level8Name
            #=========== End Level Name Settings

        supLevelRows=db((db.sm_supervisor_level.cid==cid) & (db.sm_supervisor_level.sup_id==uid)).select(db.sm_supervisor_level.level_id,db.sm_supervisor_level.level_depth_no)
#         return db._lastsql
#         return supLevelRows
        for supRow in supLevelRows:
            level_id=supRow.level_id
            depthNo=supRow.level_depth_no
            
            level_idList.append(level_id)
            depthList.append(depthNo)
            
            level = 'level' + str(depthNo)
            
            areaList=[]
            levelRows = db((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '1') & (db.sm_level[level] == level_id)).select(db.sm_level.level_id, orderby=db.sm_level.level_id)
#             return db._lastsql
#             return levelRows
            for levelRow in levelRows:
                territoryid = levelRow.level_id            
#                 marketList.append(territoryid)
                areaList.append(territoryid)
            
#             session.marketList=marketList
            session.areaList=areaList
         #   session.user_type=='Supervisor'
    
        reqPage=len(request.args)
        
        
        #--------paging
        if reqPage:
            page=int(request.args[0])
        else:
            page=0
        items_per_page=session.items_per_page*1
        limitby=(page*items_per_page,(page+1)*items_per_page+1)
        #--------end paging  
        
#         #for default filter
#         if (session.btn_filter_ord=='' or session.btn_filter_ord==None):
#             session.pendingFlag='YES'
        #----------
        records = ''
        qset=db()
        qset=qset(db.sm_order_head.cid==cid)    
#         return session.user_type
        #---- supervisor
        
        
        qset=qset(db.sm_order_head.area_id.belongs(session.areaList))
        qset=qset(db.sm_order_head.status=='Submitted')
        qset=qset(db.sm_order_head.field1=='ORDER')
        qset=qset(db.sm_order_head.field2==0)
            
#         records=qset.select(db.sm_order_head.area_id,orderby=~db.sm_order_head.id,limitby=limitby)
                
        records=qset.select(db.sm_order_head.ALL,orderby=~db.sm_order_head.id,limitby=limitby)
#         return  records       

        totalCount=qset.count()
        totalRecords=len(records)
#         return totalRecords
        #-------------
#         return records
        return dict(totalCount=totalCount,records=records,totalRecords=totalRecords,page=page,items_per_page=items_per_page)


def order_details():
    
    response.title='Order-Review'
    
    c_id=session.cid
    
    #------------------
    btn_update=request.vars.btn_update
    
    try:
        page=int(request.args[0])
    except:
        page=0
    
#     return page
    #------------------
    depot_id=''
    depot_name=''    
    req_sl=request.vars.req_sl    
    if session.user_type=='Depot':
        depot_id=session.depot_id
        depot_name=session.user_depot_name
    else:
        depotidStr=request.vars.depot_id
        if (depotidStr=='' or depotidStr==None):
            dptid=request.vars.dptid
            if (dptid=='' or dptid==None):
                depot_id=''
            else:
                depotRows=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==dptid)).select(db.sm_depot.depot_id,db.sm_depot.name,limitby=(0,1))
                if depotRows:
                    depot_id=dptid
                    depot_name=depotRows[0].name
                else:
                    depot_id=''
                    depot_name=''
                
                depot_id=dptid
                
        else:
            depot_id=str(depotidStr).strip().upper().split('|')[0]
            depotRows=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.depot_id,db.sm_depot.name,limitby=(0,1))
            if depotRows:
                depot_name=depotRows[0].name                
            else:
                depot_id=''
        session.depot_id = depot_id
        session.depot_name = depot_name

    
    #--------------------------
    
    
    #-------- SAVE ITEM/ REPLACE IF EXIST
    form =SQLFORM(db.sm_order,
                  fields=['depot_id','sl','item_id','item_name','category_id','quantity','price','note'],
#                   submit_button='Add'
                  )
    #Insert after validations
#     form.vars.cid=c_id
#     if form.accepts(request.vars,session,onvalidation=process_order):
#         sl=form.vars.sl
#         depot_id=form.vars.depot_id
#         depot_name=form.vars.depot_name
#         
#         
#         req_sl=sl
#         
#         response.flash = 'Add successfully'
#        redirect(URL('order_add',vars=dict(req_sl=sl)))
    
    #  --------------------- NEW ORDER/ SHOW FIELD VALUE
    
    rowid=0
      # Depot ID
    
    sl=0
    status='Submitted'  #'Draft'
    client_id=''
    rep_id=''
    order_date=''
    delivery_date=''
    order_datetime=str(date_fixed)[0:19]
    payment_mode=''
    note=''
    
    client_name=''
    rep_name=''
    visit_sl=0
    invoice_ref=0
    
    level0_id=''
    level0_name=''
    level1_id=''
    level1_name=''
    level2_id=''
    level2_name=''
    level3_id=''
    level3_name=''
    
    hRecords=db((db.sm_order_head.cid==c_id)& (db.sm_order_head.depot_id==depot_id) & (db.sm_order_head.sl==req_sl)).select(db.sm_order_head.ALL,limitby=(0,1))
    if hRecords:
        rowid=hRecords[0].id
        depot_id=hRecords[0].depot_id
        depot_name=hRecords[0].depot_name        
        sl=hRecords[0].sl
        status=hRecords[0].status
        client_id=hRecords[0].client_id
        rep_id=hRecords[0].rep_id
        order_date=hRecords[0].order_date
        order_datetime=str(hRecords[0].order_datetime)[0:19]
        delivery_date=hRecords[0].delivery_date        
        client_name=hRecords[0].client_name
        rep_name=hRecords[0].rep_name        
        visit_sl=hRecords[0].id
        payment_mode=hRecords[0].payment_mode
        note=hRecords[0].note
        invoice_ref=hRecords[0].invoice_ref
                
        level0_id=hRecords[0].level0_id
        level0_name=hRecords[0].level0_name
        level1_id=hRecords[0].level1_id
        level1_name=hRecords[0].level1_name
        level2_id=hRecords[0].level2_id
        level2_name=hRecords[0].level2_name
        level3_id=hRecords[0].level3_id
        level3_name=hRecords[0].level3_name
        
    records=db((db.sm_order.cid==c_id)& (db.sm_order.depot_id==depot_id) & (db.sm_order.sl==req_sl)).select(db.sm_order.ALL,orderby=db.sm_order.item_name)
    
    #-------------------- SHOW VALUE OF THE RECORD ID
    
    return dict(rowid=rowid,form=form,visit_sl=visit_sl,records=records,depot_id=depot_id,depot_name=depot_name,sl=sl,invoice_ref=invoice_ref,client_id=client_id,rep_id=rep_id,client_name=client_name,rep_name=rep_name,order_date=order_date,order_datetime=order_datetime,delivery_date=delivery_date,status=status,level0_id=level0_id,level0_name=level0_name,level1_id=level1_id,level1_name=level1_name,level2_id=level2_id,level2_name=level2_name,level3_id=level3_id,level3_name=level3_name,payment_mode=payment_mode,note=note,page=page)



#Validation of order_add
# def process_order(form):
#     c_id=session.cid   
#     
#     depot_id=str(request.vars.depot_id).strip().upper().split('|')[0]
#     
#     sl=int(request.vars.sl)
#     ym_date=str(form.vars.order_datetime)[0:7]+'-01'
#     order_date=str(form.vars.order_datetime)[0:10]
#     delivery_date=order_date    #by default order date will be delivery date
#     #---------------
#     client_id=str(request.vars.client_id).strip().upper().split('|')[0]
#     rep_id=str(request.vars.rep_id).strip().upper().split('|')[0]
#     
#     #Depot check
#     depotRecords=db((db.sm_depot.cid==c_id)& (db.sm_depot.depot_id==depot_id)& (db.sm_depot.status=='ACTIVE')).select(db.sm_depot.name,limitby=(0,1))
#     if not depotRecords:
#         form.errors.quantity=''  
#         response.flash='Invalid Depot ID!' 
#     else:
#         dpName=depotRecords[0].name
#         form.vars.depot_id=depot_id
#         form.vars.depot_name=dpName
#         
#         #Client check
#         clientRecords=db((db.sm_client.cid==c_id)& (db.sm_client.depot_id==depot_id) & (db.sm_client.client_id==client_id)& (db.sm_client.status=='ACTIVE')).select(db.sm_client.name,db.sm_client.area_id,limitby=(0,1))
#         if not clientRecords:
#             form.errors.quantity=''  
#             response.flash='Invalid Client ID!' 
#         else:
#             clName=clientRecords[0].name
#             area_id=clientRecords[0].area_id
#             
#             levelRecords=db((db.sm_level.cid==c_id)& (db.sm_level.level_id==area_id)).select(db.sm_level.level_name,limitby=(0,1))
#             
#             form.vars.area_id=area_id
#             form.vars.area_name=levelRecords[0].level_name
#             form.vars.client_name=clName        
#             form.vars.client_id=client_id
#             
#             #--------------------rep check
#             repRecords=db((db.sm_rep.cid==c_id)& (db.sm_rep.depot_id==depot_id) & (db.sm_rep.rep_id==rep_id)& (db.sm_rep.status=='ACTIVE')).select(db.sm_rep.name,limitby=(0,1))
#             if not repRecords:
#                 form.errors.quantity=''  
#                 response.flash='Invalid Rep ID!'
#             else:
#                 repName=repRecords[0].name
#                 form.vars.rep_id=rep_id
#                 form.vars.rep_name=repName
#             
#                 #--------------
#                 existRecords=db((db.sm_order.cid==c_id) & (db.sm_order.depot_id==depot_id)& (db.sm_order.sl==sl)& (db.sm_order.item_id==form.vars.item_id)).select(db.sm_order.id,db.sm_order.item_id,limitby=(0,1))
#                 if existRecords:
#                     existRecords[0].update_record(item_name=form.vars.item_name,category_id=form.vars.category_id,quantity=form.vars.quantity,price=form.vars.price)        
#                     form.errors.quantity=''  
#                     response.flash='Item replaced!'      
#                 
#                 elif int(form.vars.quantity)<=0:
#                     form.errors.quantity=''
#                     response.flash='need item quantity!'
#                 
#                 else:
#                     if sl==0:            
#                         #Get max sl from sm_depot
#                         maxSl=1
#                         records=db((db.sm_depot.cid==c_id) & (db.sm_depot.depot_id==form.vars.depot_id)).select(db.sm_depot.id,db.sm_depot.order_sl,limitby=(0,1))
#                         if records:
#                             sl=records[0].order_sl
#                             maxSl=int(sl)+1                
#                                                 
#                         #--- sl update in depot
#                         records[0].update_record(order_sl=maxSl)
#                         
#                         form.vars.sl=maxSl
#                         
#                     form.vars.ym_date=ym_date
#                     form.vars.order_date=order_date
#                     form.vars.delivery_date=delivery_date
# 


##Update order status as Post or Cancel
def post_approved_order():
    c_id=session.cid
#     return c_id
   
  #  btn_cancel=request.vars.btn_cancel
    btn_approved=request.vars.btn_approved
    
    req_depot=request.args(0)
    req_sl=request.args(1) 
    req_date=request.args(2)    
    ym_date=str(req_date)[0:7]+'-01'
#     stat = ''
    session.msg=''
    
  
    # SUBMITTED
    if btn_approved:
#         return 'ss'
        countRecords=db((db.sm_order.cid==c_id)& (db.sm_order.depot_id==req_depot) & (db.sm_order.sl==req_sl)).count()
#         return countRecords
        if int(countRecords)==0:
            session.flash='At least one item needs in an order!'
        else:
#             return 'aa'
            db((db.sm_order_head.cid==c_id)& (db.sm_order_head.depot_id==req_depot) & (db.sm_order_head.sl==req_sl) & (db.sm_order_head.status=='Submitted')).update(status='Invoiced')
            db((db.sm_order.cid==c_id)& (db.sm_order.depot_id==req_depot) & (db.sm_order.sl==req_sl) & (db.sm_order.status=='Submitted')).update(status='Invoiced')
            
#             order_row=db((db.sm_order_head.cid==session.cid)& (db.sm_order_head.depot_id==req_depot) & (db.sm_order_head.sl==req_sl)  & (db.sm_order_head.status=='Invoiced')).select(db.sm_order_head.status,orderby=~db.sm_order_head.id,limitby=(0,1))
#             return order_row
#             if order_row:
#                asd= '<label  name="status" id="status"  >{{=order_row}}</label>'
#          
         
         #   records=qset.select(db.sm_order_head.ALL,orderby=~db.sm_order_head.id,limitby=limitby)
#             session.flash='Submitted successfully'



            session.msg = 'Approved Successfully'
            
            
                    #--------paging
                    
                    
#         reqPage=len(request.args)
#         if reqPage:
#             page=int(request.args[0])
#         else:
#             page=0
#         items_per_page=session.items_per_page*1
#         limitby=(page*items_per_page,(page+1)*items_per_page+1)
        #--------end paging  

        redirect(URL(c='z_test',f='order_details',vars=dict(req_sl=req_sl,dptid=req_depot)))
    
    
    return dict(result=result)










