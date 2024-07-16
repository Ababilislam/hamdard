
#================================= order/Visit
# Note : field2 used for In Process Status (Ready for Auto Invoicing)
def order():
    c_id=session.cid
    #----------------
    task_id='rm_visit_manage'
    task_id_view='rm_visit_list_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))
        
    response.title='Visit-List'
    
    # Set text for filter
    btn_filter_ord=request.vars.btn_filter
    btn_all=request.vars.btn_all
    depot_id_value=str(request.vars.depot_id_value).strip()
    search_date_order=str(request.vars.to_dt).strip()
    search_date_delivery=str(request.vars.from_dt).strip()
    search_type=str(request.vars.search_type).strip()
    search_value=str(request.vars.search_value).strip()
    visit_type=str(request.vars.visit_type).strip() #ALL,ORDER,VISIT
    in_process=str(request.vars.in_process).strip()
    
    btn_submit_inprocess=request.vars.btn_submit_inprocess
    pendingFlag=request.vars.pendingFlag
    
    reqPage=len(request.args)
    
    #Check sl is integer or not
    if btn_filter_ord:
        session.btn_filter_ord=btn_filter_ord
        session.depot_id_value_order=depot_id_value         
        session.search_type_order=search_type
        session.search_value_order=search_value
        session.visit_type=visit_type
        session.in_process=in_process
        session.pendingFlag=pendingFlag
        
        try:
            searchDate=datetime.datetime.strptime(str(search_date_order),'%Y-%m-%d').strftime('%Y-%m-%d')
            session.search_date_order=searchDate
        except:
            session.search_date_order=''
            
        try:
            search_dateDelivery=datetime.datetime.strptime(str(search_date_delivery),'%Y-%m-%d').strftime('%Y-%m-%d')
            session.search_date_delivery=search_dateDelivery
        except:
            session.search_date_delivery=''
            
        if (session.search_type_order=='VSL'):
            vsl=0
            if not(session.search_value_order=='' or session.search_value_order==None):
                try:
                    vsl=int(session.search_value_order)
                    session.search_value_order=vsl
                except:
                    session.search_value_order=vsl
                    response.flash='VSl needs number value'
            else:
                session.search_value_order=vsl
        
        #-------------   
        if (session.search_type_order=='OrderSL'):
            sl=0
            if not(session.search_value_order=='' or session.search_value_order==None):
                try:
                    sl=int(session.search_value_order)
                    session.search_value_order=sl
                except:
                    session.search_value_order=sl
                    response.flash='Sl needs number value'
            else:
                session.search_value_order=sl
        
        #-------------   
        if (session.search_type_order=='InprocessStatus'):
            pStatus=0
            if not(session.search_value_order=='' or session.search_value_order==None):
                try:
                    pStatus=int(session.search_value_order)
                    session.search_value_order=pStatus
                except:
                    session.search_value_order=pStatus
                    response.flash='In Process status needs number value 0/1'
            else:
                session.search_value_order=pStatus
                
        reqPage=0
        
    elif btn_all:
        session.btn_filter_ord=None
        session.depot_id_value_order=None
        session.search_type_order=None
        session.search_value_order=None
        session.search_date_order=None
        session.search_date_delivery=None
        session.visit_type=None
        session.in_process=None
        
        reqPage=0
    
    
    elif btn_submit_inprocess:
        vslList=[]        
        vslList=request.vars.vslList
        rowList=[]
        if vslList==None:
            response.flash='need to select order'            
        else:            
            #----------------
            for i in range(len(vslList)):
                rowId=str(vslList[i]).strip()        
                if rowId=='-1' or rowId=='-':            
                    continue
                
                rowList.append(rowId)
                
            if len(rowList)>0:                
                db((db.sm_order_head.cid==c_id)&(db.sm_order_head.id.belongs(rowList))).update(field2=1)
                response.flash='Submitted successfully'
            
    
    #--------paging
    if reqPage:
        page=int(request.args[0])
    else:
        page=0
    items_per_page=session.items_per_page*1
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #--------end paging  
    
    #for default filter
    if (session.btn_filter_ord=='' or session.btn_filter_ord==None):
        session.pendingFlag='YES'
    #----------
        
    qset=db()
    qset=qset(db.sm_order_head.cid==c_id)    
    if (session.user_type=='Depot'):
        qset=qset(db.sm_order_head.depot_id==session.depot_id)
        
        #------------- for filter same depot and sub-depot
#         if not (session.depot_id_value_order=='' or session.depot_id_value_order==None):
#             searchValue=str(session.depot_id_value_order).split('|')[0].upper()
#             if (searchValue==session.depot_id):
#                 qset=qset(db.sm_order_head.depot_id==session.depot_id)  
#             else:
#                 depotRows=db((db.sm_depot_settings.cid==c_id) & (db.sm_depot_settings.depot_id==searchValue)& (db.sm_depot_settings.depot_id_from_to==session.depot_id)).select(db.sm_depot_settings.depot_id,limitby=(0,1))
#                 if depotRows:
#                     qset=qset(db.sm_order_head.depot_id==searchValue)
#                 else:
#                     qset=qset(db.sm_order_head.depot_id=='')
#                     response.flash='Unauthorized filter for depot'
#         else:
#             qset=qset(db.sm_order_head.depot_id==session.depot_id)
    
    #---- supervisor
    if session.user_type=='Supervisor':
        qset=qset(db.sm_order_head.area_id.belongs(session.marketList))
    else:
        pass
    #----
    
    #Set query based search type
    if (session.btn_filter_ord):
        if (session.user_type!='Depot'):
            if not (session.depot_id_value_order=='' or session.depot_id_value_order==None):
                searchValue=str(session.depot_id_value_order).split('|')[0].upper()
                qset=qset(db.sm_order_head.depot_id==searchValue)
            else:
                qset=qset(db.sm_order_head.depot_id!='')
        
        #----------
        if not(session.search_date_order=='' or session.search_date_order==None):
            qset=qset(db.sm_order_head.order_date==session.search_date_order)
            
        #----------
        if not(session.search_date_delivery=='' or session.search_date_delivery==None):
            qset=qset(db.sm_order_head.delivery_date==session.search_date_delivery)
        
        if (session.pendingFlag=='YES'):
            qset=qset(db.sm_order_head.status=='Submitted')
            qset=qset(db.sm_order_head.field1=='ORDER')
            qset=qset(db.sm_order_head.field2==0)
        else:
            #----------
            if not(session.visit_type=='' or session.visit_type==None):
                if session.visit_type=='ORDER':
                    qset=qset(db.sm_order_head.field1==session.visit_type)
                else:
                    qset=qset(db.sm_order_head.field1=='')
            
            #----------
            if not(session.in_process=='' or session.in_process==None):
                if session.in_process=='YES':
                    qset=qset(db.sm_order_head.field2==1)
                else:
                    qset=qset(db.sm_order_head.field2==0)
            
            if (session.search_type_order=='Status'):
                qset=qset(db.sm_order_head.status==session.search_value_order)
        
            
        #-----------
        if (session.search_type_order=='VSL'):
            qset=qset(db.sm_order_head.id==session.search_value_order)
        
        elif (session.search_type_order=='OrderSL'):
            qset=qset(db.sm_order_head.sl==session.search_value_order)
        
        elif (session.search_type_order=='CLIENTID'):
            searchValue=str(session.search_value_order).split('|')[0].upper()
            qset=qset(db.sm_order_head.client_id==searchValue)
        
        elif (session.search_type_order=='REPID'):
            searchValue=str(session.search_value_order).split('|')[0].upper()
            qset=qset(db.sm_order_head.rep_id==searchValue)
        
        elif (session.search_type_order=='MarketID'):
            searchValue=str(session.search_value_order).split('|')[0].upper()
            qset=qset(db.sm_order_head.area_id==searchValue)
            
        elif (session.search_type_order=='DownloadStatus'):
            qset=qset(db.sm_order_head.depot_status==session.search_value_order)
            
    #for default filter
    else:
        if (session.pendingFlag=='YES'):
            qset=qset(db.sm_order_head.status=='Submitted')
            qset=qset(db.sm_order_head.field1=='ORDER')
            qset=qset(db.sm_order_head.field2==0)
            
    records=qset.select(db.sm_order_head.ALL,orderby=~db.sm_order_head.id,limitby=limitby)
    totalCount=qset.count()
    totalRecords=len(records)
    
    #--------------- Date
    search_form =SQLFORM(db.sm_search_date)
    
    #Order Date
    if (session.search_date_order=='' or session.search_date_order==None):        
        search_form.vars.to_dt=''
    else:
        search_form.vars.to_dt=session.search_date_order
    
    #Delivery Date
    if (session.search_date_delivery=='' or session.search_date_delivery==None):        
        search_form.vars.from_dt=''
    else:
        search_form.vars.from_dt=session.search_date_delivery
    
    if search_form.accepts(request.vars,session):
        pass
    #-------------
    
    return dict(search_form=search_form,totalCount=totalCount,records=records,totalRecords=totalRecords,page=page,items_per_page=items_per_page,access_permission=access_permission,access_permission_view=access_permission_view)
    
    
#Validation of order_add
def process_order(form):
    c_id=session.cid   
    
    depot_id=str(request.vars.depot_id).strip().upper().split('|')[0]
    
    sl=int(request.vars.sl)
    ym_date=str(form.vars.order_datetime)[0:7]+'-01'
    order_date=str(form.vars.order_datetime)[0:10]
    delivery_date=order_date    #by default order date will be delivery date
    #---------------
    client_id=str(request.vars.client_id).strip().upper().split('|')[0]
    rep_id=str(request.vars.rep_id).strip().upper().split('|')[0]
    
    #Depot check
    depotRecords=db((db.sm_depot.cid==c_id)& (db.sm_depot.depot_id==depot_id)& (db.sm_depot.status=='ACTIVE')).select(db.sm_depot.name,limitby=(0,1))
    if not depotRecords:
        form.errors.quantity=''  
        response.flash='Invalid Depot ID!' 
    else:
        dpName=depotRecords[0].name
        form.vars.depot_id=depot_id
        form.vars.depot_name=dpName
        
        #Client check
        clientRecords=db((db.sm_client.cid==c_id)& (db.sm_client.depot_id==depot_id) & (db.sm_client.client_id==client_id)& (db.sm_client.status=='ACTIVE')).select(db.sm_client.name,db.sm_client.area_id,limitby=(0,1))
        if not clientRecords:
            form.errors.quantity=''  
            response.flash='Invalid Client ID!' 
        else:
            clName=clientRecords[0].name
            area_id=clientRecords[0].area_id
            
            levelRecords=db((db.sm_level.cid==c_id)& (db.sm_level.level_id==area_id)).select(db.sm_level.level_name,limitby=(0,1))
            
            form.vars.area_id=area_id
            form.vars.area_name=levelRecords[0].level_name
            form.vars.client_name=clName        
            form.vars.client_id=client_id
            
            #--------------------rep check
            repRecords=db((db.sm_rep.cid==c_id)& (db.sm_rep.depot_id==depot_id) & (db.sm_rep.rep_id==rep_id)& (db.sm_rep.status=='ACTIVE')).select(db.sm_rep.name,limitby=(0,1))
            if not repRecords:
                form.errors.quantity=''  
                response.flash='Invalid Rep ID!'
            else:
                repName=repRecords[0].name
                form.vars.rep_id=rep_id
                form.vars.rep_name=repName
            
                #--------------
                existRecords=db((db.sm_order.cid==c_id) & (db.sm_order.depot_id==depot_id)& (db.sm_order.sl==sl)& (db.sm_order.item_id==form.vars.item_id)).select(db.sm_order.id,db.sm_order.item_id,limitby=(0,1))
                if existRecords:
                    existRecords[0].update_record(item_name=form.vars.item_name,category_id=form.vars.category_id,quantity=form.vars.quantity,price=form.vars.price)        
                    form.errors.quantity=''  
                    response.flash='Item replaced!'      
                
                elif int(form.vars.quantity)<=0:
                    form.errors.quantity=''
                    response.flash='need item quantity!'
                
                else:
                    if sl==0:            
                        #Get max sl from sm_depot
                        maxSl=1
                        records=db((db.sm_depot.cid==c_id) & (db.sm_depot.depot_id==form.vars.depot_id)).select(db.sm_depot.id,db.sm_depot.order_sl,limitby=(0,1))
                        if records:
                            sl=records[0].order_sl
                            maxSl=int(sl)+1                
                                                
                        #--- sl update in depot
                        records[0].update_record(order_sl=maxSl)
                        
                        form.vars.sl=maxSl
                        
                    form.vars.ym_date=ym_date
                    form.vars.order_date=order_date
                    form.vars.delivery_date=delivery_date

def order_add():
    task_id='rm_visit_manage'
    task_id_view='rm_visit_list_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL('order'))
    
    response.title='Order-Review'
    
    c_id=session.cid
    
    #------------------
    btn_update=request.vars.btn_update
    
    try:
        page=int(request.args[0])
    except:
        page=0
    
    
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
    #--------------------------
    
    
    #UPDATE sm_order_head and sm_order
#     if btn_update:
#         req_depot_id=depot_id
#         reqSl=int(request.vars.sl)
#         order_datetime=request.vars.order_datetime
#         ym_date=str(order_datetime)[0:7]+'-01'#Save on first date of month
#         
#         payment_mode=str(request.vars.payment_mode).strip()
#         req_note=str(request.vars.note).strip()
#         order_date=str(order_datetime)[0:10]
#         
#         #---------------
#         client_id=str(request.vars.client_id).strip().upper().split('|')[0]
#         rep_id=str(request.vars.rep_id).strip().upper().split('|')[0]
#         
#         clientRecords=db((db.sm_client.cid==c_id)& (db.sm_client.depot_id==req_depot_id) & (db.sm_client.client_id==client_id)& (db.sm_client.status=='ACTIVE')).select(db.sm_client.client_id,db.sm_client.name,db.sm_client.area_id,limitby=(0,1))
#         if not clientRecords:
#             session.flash='Invalid Client' 
#         else:
#             clName=clientRecords[0].name
#             area_id=clientRecords[0].area_id            
#             levelRecords=db((db.sm_level.cid==c_id)& (db.sm_level.level_id==area_id)).select(db.sm_level.level_name,limitby=(0,1))
#             area_name=levelRecords[0].level_name
#             
#             repRecords=db((db.sm_rep.cid==c_id)& (db.sm_rep.depot_id==req_depot_id) & (db.sm_rep.rep_id==rep_id)& (db.sm_rep.status=='ACTIVE')).select(db.sm_rep.rep_id,db.sm_rep.name,limitby=(0,1))
#             if not repRecords:
#                 session.flash='Invalid Rep'
#             else:
#                 repName=repRecords[0].name
#                 
#                 db((db.sm_order_head.cid==c_id)& (db.sm_order_head.depot_id==req_depot_id) & (db.sm_order_head.sl==reqSl)).update(client_id=client_id,rep_id=rep_id,client_name=clName,rep_name=repName,area_name=area_name,order_date=order_date,order_datetime=order_datetime,payment_mode=payment_mode,note=req_note,ym_date=ym_date)
#                 #db((db.sm_order.cid==c_id)& (db.sm_order.depot_id==req_depot_id) & (db.sm_order.sl==reqSl)).update(client_id=client_id,rep_id=rep_id,client_name=clName,rep_name=repName,area_name=area_name,order_date=order_date,order_datetime=order_datetime,payment_mode=payment_mode,note=req_note,ym_date=ym_date)
#         
#         redirect(URL('order_add',vars=dict(req_sl=reqSl,dptid=req_depot_id)))
    
    #-------- SAVE ITEM/ REPLACE IF EXIST
    form =SQLFORM(db.sm_order,
                  fields=['depot_id','sl','item_id','item_name','category_id','quantity','price','note'],
                  submit_button='Add'
                  )
    #Insert after validations
    form.vars.cid=c_id
    if form.accepts(request.vars,session,onvalidation=process_order):
        sl=form.vars.sl
        depot_id=form.vars.depot_id
        depot_name=form.vars.depot_name
        
#         ym_date=str(order_datetime)[0:7]+'-01'#First day of month
#         order_date=str(order_datetime)[0:10]
#         delivery_date=order_date    #by default order date will be delivery date
#         
#         #I exist in head then update else insert
#         headRows=db((db.sm_order_head.cid==c_id)& (db.sm_order_head.depot_id==depot_id) & (db.sm_order_head.sl==sl)).select(db.sm_order_head.id,db.sm_order_head.depot_id,limitby=(0,1))
#         if headRows:
#             headRows[0].update_record(client_id=client_id,rep_id=rep_id,order_date=order_date,delivery_date=delivery_date,order_datetime=order_datetime,payment_mode=payment_mode,note=note,ym_date=ym_date,depot_name=depot_name,client_name=client_name,rep_name=rep_name,area_id=area_id,area_name=area_name)
#         else:
#            db.sm_order_head.insert(cid=c_id,depot_id=depot_id,sl=sl,client_id=client_id,rep_id=rep_id,order_date=order_date,order_datetime=order_datetime,delivery_date=delivery_date,
#                         depot_name=depot_name,client_name=client_name,rep_name=rep_name,area_id=area_id,area_name=area_name,payment_mode=payment_mode,note=note,ym_date=ym_date)
           
        #--------UPDATE SAME SL VALUE
        #db((db.sm_order.cid==c_id)& (db.sm_order.depot_id==depot_id) & (db.sm_order.sl==sl)).update(client_id=client_id,rep_id=rep_id,order_date=order_date,order_datetime=order_datetime,delivery_date=delivery_date,payment_mode=payment_mode,note=note,ym_date=ym_date,depot_name=depot_name,client_name=client_name,rep_name=rep_name,area_id=area_id,area_name=area_name)
        
        req_sl=sl
        
        response.flash = 'Add successfully'
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
    
    return dict(rowid=rowid,form=form,visit_sl=visit_sl,records=records,depot_id=depot_id,depot_name=depot_name,sl=sl,invoice_ref=invoice_ref,client_id=client_id,rep_id=rep_id,client_name=client_name,rep_name=rep_name,order_date=order_date,order_datetime=order_datetime,delivery_date=delivery_date,status=status,level0_id=level0_id,level0_name=level0_name,level1_id=level1_id,level1_name=level1_name,level2_id=level2_id,level2_name=level2_name,level3_id=level3_id,level3_name=level3_name,payment_mode=payment_mode,note=note,access_permission=access_permission,access_permission_view=access_permission_view,page=page)

def download_order():
    c_id=session.cid
    #----------------
    task_id='rm_visit_manage'
    task_id_view='rm_visit_list_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))
    
    response.title='Visit-List'
    
    qset=db()
    qset=qset(db.sm_order_head.cid==c_id)   
    qset=qset(db.sm_order.cid==c_id) 
    qset=qset((db.sm_order_head.depot_id==db.sm_order.depot_id)&(db.sm_order_head.sl==db.sm_order.sl))
     
    if (session.user_type=='Depot'):
        qset=qset(db.sm_order_head.depot_id==session.depot_id)
        #------------- for filter same depot and sub-depot
#         if not (session.depot_id_value_order=='' or session.depot_id_value_order==None):
#             searchValue=str(session.depot_id_value_order).split('|')[0].upper()
#             if (searchValue==session.depot_id):
#                 qset=qset(db.sm_order_head.depot_id==session.depot_id)  
#             else:
#                 depotRows=db((db.sm_depot_settings.cid==c_id) & (db.sm_depot_settings.depot_id==searchValue)& (db.sm_depot_settings.depot_id_from_to==session.depot_id)).select(db.sm_depot_settings.depot_id,limitby=(0,1))
#                 if depotRows:
#                     qset=qset(db.sm_order_head.depot_id==searchValue)
#                 else:
#                     qset=qset(db.sm_order_head.depot_id=='')
#                     response.flash='Unauthorized filter for depot'
#         else:
#             qset=qset(db.sm_order_head.depot_id==session.depot_id)
    
    #---- supervisor
    if session.user_type=='Supervisor':
        qset=qset(db.sm_order_head.area_id.belongs(session.marketList))
    else:
        pass
    #----
    
    #Set query based search type
    if (session.btn_filter_ord):        
        if (session.user_type!='Depot'):
            if not (session.depot_id_value_order=='' or session.depot_id_value_order==None):
                searchValue=str(session.depot_id_value_order).split('|')[0].upper()
                qset=qset(db.sm_order_head.depot_id==searchValue)
            else:
                session.flash='Filtered By Depot and Order Date Required'
                redirect (URL('order'))
                
        #------------
        if not(session.search_date_order=='' or session.search_date_order==None):
            qset=qset(db.sm_order_head.order_date==session.search_date_order)
            
        else:
            session.flash='Filter By Order Date Required'
            redirect (URL('order'))
    else:
        session.flash='Filter By Order Date Required'
        redirect (URL('order'))
        
    records=qset.select(db.sm_order_head.ALL,db.sm_order.sl,db.sm_order.item_id,db.sm_order.item_name,db.sm_order.category_id,db.sm_order.quantity,db.sm_order.price,db.sm_order.item_vat,orderby=~db.sm_order.sl|db.sm_order.item_name)
    
    #-------------------------------------
    myString='Order List'+'\n'
        
    myString+='VSL,DepotID,DepotName,D.O.SL,Order Date,Client/RetailerID,Client/RetailerName,MarketID,MarketName,Rep/SupID,Rep/SupName,ItemID,ItemName,Category,Qty,Price,Vat\n'
    for rec in records:
        vsl=str(rec.sm_order_head.id)
        depot_id=str(rec.sm_order_head.depot_id)
        depot_name=str(rec.sm_order_head.depot_name).replace(',', ' ')
        sl=str(rec.sm_order.sl)
        order_date=str(rec.sm_order_head.order_date)
        
        client_id=str(rec.sm_order_head.client_id)
        client_name=str(rec.sm_order_head.client_name).replace(',', ' ')   
           
        rep_id=str(rec.sm_order_head.rep_id)
        rep_name=str(rec.sm_order_head.rep_name).replace(',', ' ')
        
        area_id=str(rec.sm_order_head.area_id)
        area_name=str(rec.sm_order_head.area_name).replace(',', ' ')
        
        item_id=str(rec.sm_order.item_id)
        item_name=str(rec.sm_order.item_name).replace(',', ' ')
        category_id=str(rec.sm_order.category_id)
        quantity=str(rec.sm_order.quantity)
        price=str(rec.sm_order.price)
        item_vat=str(rec.sm_order.item_vat)
        
        myString+=vsl+','+depot_id+','+depot_name+','+sl+','+order_date+','+client_id+','+client_name+','+area_id+','+area_name+','+rep_id+','+rep_name+','+item_id+','+item_name+','+category_id+','+quantity+','+price+','+item_vat+'\n'
        
    #Save as csv
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_order_details.csv'   
    return str(myString)
    #-------------
    
def download_order_head():
    c_id=session.cid
    #----------------
    task_id='rm_visit_manage'
    task_id_view='rm_visit_list_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))
    
    response.title='Order/Visit-List'
    
    qset=db()
    qset=qset(db.sm_order_head.cid==c_id)    
    if (session.user_type=='Depot'):
        qset=qset(db.sm_order_head.depot_id==session.depot_id)
        
    #---- supervisor
    if session.user_type=='Supervisor':
        qset=qset(db.sm_order_head.area_id.belongs(session.marketList))
    else:
        pass
    #----
    
    #Set query based search type
    if (session.btn_filter_ord):
        if (session.user_type!='Depot'):
            if not (session.depot_id_value_order=='' or session.depot_id_value_order==None):
                searchValue=str(session.depot_id_value_order).split('|')[0].upper()
                qset=qset(db.sm_order_head.depot_id==searchValue)
            else:
                qset=qset(db.sm_order_head.depot_id!='')
        
        #----------
        if not(session.search_date_order=='' or session.search_date_order==None):
            qset=qset(db.sm_order_head.order_date==session.search_date_order)
            
        #----------
        if not(session.search_date_delivery=='' or session.search_date_delivery==None):
            qset=qset(db.sm_order_head.delivery_date==session.search_date_delivery)
            
        #----------
        if not(session.visit_type=='' or session.visit_type==None):
            if session.visit_type=='ORDER':
                qset=qset(db.sm_order_head.field1==session.visit_type)
            else:
                qset=qset(db.sm_order_head.field1=='')
                
        #-----------
        if ((session.search_date_order=='' or session.search_date_order==None) and (session.search_date_delivery=='' or session.search_date_delivery==None)):
            session.flash='Required filter by Order Date or Delivery Date with Visit Type'
            redirect (URL('order'))
        
    #for default filter
    else:
        session.flash='Required filter by Order Date or Delivery Date with Visit Type'
        redirect (URL('order'))
        
    records=qset.select(db.sm_order_head.ALL,orderby=~db.sm_order_head.id)
    
    #-------------------------------------
    myString='Order List'+'\n'
        
    myString+='VSL,DepotID,DepotName,D.O.SL,Order Date,Delivery Date,Client/RetailerID,Client/RetailerName,Territory,MarketID,MarketName,Rep/SupID,Rep/SupName,Visit Type,In Process, Status\n'
    for rec in records:
        vsl=str(rec.id)
        depot_id=str(rec.depot_id)
        depot_name=str(rec.depot_name).replace(',', ' ')
        sl=str(rec.sl)
        order_date=str(rec.order_date) 
        delivery_date=str(rec.delivery_date)        
        client_id=str(rec.client_id)
        client_name=str(rec.client_name).replace(',', ' ')
        area_id=str(rec.area_id)
        
        market_id=str(rec.market_id)
        market_name=str(rec.market_name).replace(',', ' ')
        rep_id=str(rec.rep_id)
        rep_name=str(rec.rep_name).replace(',', ' ')
        visitType=str(rec.field1)
        inprocess=str(rec.field2)
        status=str(rec.status)
        
        myString+=vsl+','+depot_id+','+depot_name+','+sl+','+order_date+','+delivery_date+','+client_id+','+client_name+','+area_id+','+market_id+','+market_name+','+rep_id+','+rep_name+','+visitType+','+inprocess+','+status+'\n'
        
    #Save as csv
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_order_list.csv'   
    return str(myString)
    #-------------


#======================= Invoice
def invoice_list():
    c_id=session.cid
    #----------------
    response.title='Invoice/Delivery-List'
    #Check access permission
    #----------Task assaign----------
    task_id='rm_invoice_manage'
    task_id_view='rm_invoice_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL(c='default', f='home'))
        
    
    #Set text for filter
    to_dt=''    
    btn_filter_invoice=request.vars.btn_filter
    btn_all=request.vars.btn_all
    
    depot_id_value=str(request.vars.depot_id_value).strip()
    search_type=str(request.vars.search_type).strip()
    search_value=str(request.vars.search_value).strip()
    
    reqPage=len(request.args)
    # Set sessions for filter
    if btn_filter_invoice:
        session.btn_filter_invoice=btn_filter_invoice
        session.depot_id_value_invoice=depot_id_value 
        session.search_type_invoice=search_type
        session.search_value_invoice=search_value
        # Check SL is integer or not
        if (session.search_type_invoice=='SL'):
            sl=0
            if not(session.search_value_invoice=='' or session.search_value_invoice==None):
                try:       
                    sl=int(session.search_value_invoice)
                    session.search_value_invoice=sl
                except:
                    session.search_value_invoice=sl
                    response.flash='sl needs number value'
            else:
                session.search_value_invoice=sl
        
        elif (session.search_type_invoice=='ROWID'):
            rowid=0
            if not(session.search_value_invoice=='' or session.search_value_invoice==None):
                try:       
                    rowid=int(session.search_value_invoice)
                    session.search_value_invoice=rowid
                except:
                    session.search_value_invoice=rowid
                    response.flash='Ref needs number value'
            else:
                session.search_value_invoice=rowid    
            
            
        reqPage=0

# ---------------------------  Date filter Start --------------------------- #
        
        from_dt=request.vars.from_dt
        to_dt=request.vars.to_dt


        if not(from_dt=='' or to_dt==''):
            try:
                fromDate_order=datetime.datetime.strptime(str(from_dt),'%Y-%m-%d')
                date_to_order=datetime.datetime.strptime(str(to_dt),'%Y-%m-%d')
                # date_to_m=toDate_v + datetime.timedelta(days = 1)

                if fromDate_order >date_to_order:
                    session.fromDate_order=None
                    session.date_to_order=None
                    dateFlag = False
                    response.flash='To Date should be greater than From Date'
                else:
                    # return 'df'
                    session.fromDate_order=fromDate_order#.strftime('%Y-%m-%d')
                    session.date_to_order=date_to_order#.strftime('%Y-%m-%d')

            except:
                session.fromDate_order=None
                session.date_to_order=None
                response.flash='Invalid date range'
                     
            
        reqPage=0


        
    elif btn_all:
        session.btn_filter_invoice=None
        session.depot_id_value_invoice=None
        session.search_type_invoice=None
        session.search_value_invoice=None
        session.fromDate_order=None
        session.date_to_order=None

        reqPage=0

    
    #--------paging
    if reqPage:
        page=int(request.args[0])
    else:
        page=0
    items_per_page=session.items_per_page*5
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #--------end paging  
    # Set query based on search type
    qset=db()
    qset=qset(db.sm_invoice_head.cid==c_id)    
    if (session.user_type=='Depot'):
        qset=qset(db.sm_invoice_head.depot_id==session.depot_id)
        
        #------------- for filter same depot and sub-depot
#         if not (session.depot_id_value_invoice=='' or session.depot_id_value_invoice==None):
#             searchValue=str(session.depot_id_value_invoice).split('|')[0].upper()
#             
#             if (searchValue==session.depot_id):
#                 qset=qset(db.sm_invoice_head.depot_id==session.depot_id)  
#             else:
#                 depotRows=db((db.sm_depot_settings.cid==c_id) & (db.sm_depot_settings.depot_id==searchValue)& (db.sm_depot_settings.depot_id_from_to==session.depot_id)).select(db.sm_depot_settings.depot_id,limitby=(0,1))
#                 if depotRows:
#                     qset=qset(db.sm_invoice_head.depot_id==searchValue)
#                 else:
#                     qset=qset(db.sm_invoice_head.depot_id=='')
#                     response.flash='Unauthorized filter for depot'
#         else:
#             qset=qset(db.sm_invoice_head.depot_id==session.depot_id)
    
    
    
    #---- supervisor
    if session.user_type=='Supervisor':
        qset=qset(db.sm_invoice_head.area_id.belongs(session.marketList))
    else:
        pass
    #----
    if (session.btn_filter_invoice):
        if not (session.fromDate_order==None or session.date_to_order==None):  
            qset=qset((db.sm_invoice_head.order_datetime >=session.fromDate_order)&(db.sm_invoice_head.order_datetime <= session.date_to_order))

    
    
    if (session.btn_filter_invoice):
        if (session.user_type!='Depot'):
            if not (session.depot_id_value_invoice=='' or session.depot_id_value_invoice==None):
                searchValue=str(session.depot_id_value_invoice).split('|')[0].upper()
                qset=qset(db.sm_invoice_head.depot_id==searchValue)
            else:
                qset=qset(db.sm_invoice_head.depot_id!='')
                
        #------------
        if (session.search_type_invoice=='SL'):
            qset=qset(db.sm_invoice_head.sl==session.search_value_invoice)
        
        elif (session.search_type_invoice=='PRODUCT'):#only for depot user
            searchValue=str(session.search_value_invoice).split('|')[0].upper()
            
            detSlList=[]
            detRows=db((db.sm_invoice.cid==c_id)&(db.sm_invoice.depot_id==session.depot_id)&(db.sm_invoice.item_id==searchValue)&(db.sm_invoice.batch_id!='')&(db.sm_invoice.status=='Submitted')).select(db.sm_invoice.sl,groupby=db.sm_invoice.sl)
            for detRow in detRows:
                detSlList.append(detRow.sl)
            
            qset=qset(db.sm_invoice_head.sl.belongs(detSlList))
        
        elif (session.search_type_invoice=='ROWID'):
            qset=qset(db.sm_invoice_head.id==session.search_value_invoice)
        
        elif (session.search_type_invoice=='ORDSL'):
            try:
                order_sl=int(session.search_value_invoice)
            except:
                order_sl=0
            
            qset=qset(db.sm_invoice_head.order_sl==order_sl)
        
        elif (session.search_type_invoice=='CLIENTID'):
            searchValue=str(session.search_value_invoice).split('|')[0].upper()
            qset=qset(db.sm_invoice_head.client_id==searchValue)
        
        elif (session.search_type_invoice=='REPID'):
            searchValue=str(session.search_value_invoice).split('|')[0].upper()
            qset=qset(db.sm_invoice_head.rep_id==searchValue)
        
        elif (session.search_type_invoice=='DPID'):
            searchValue=str(session.search_value_invoice).split('|')[0].upper()
            qset=qset(db.sm_invoice_head.d_man_id==searchValue)
        
        elif (session.search_type_invoice=='DATE'):
            qset=qset(db.sm_invoice_head.delivery_date==session.search_value_invoice)
        
        elif (session.search_type_invoice=='ORDDATE'):
            try:
                order_datetimeFrom=datetime.datetime.strptime(str(session.search_value_invoice),'%Y-%m-%d')
                order_datetimeTo=order_datetimeFrom+datetime.timedelta(days=1)
            except:
                order_datetimeFrom=''
                order_datetimeTo=''
            qset=qset((db.sm_invoice_head.order_datetime>=order_datetimeFrom)&(db.sm_invoice_head.order_datetime<order_datetimeTo))
        
        elif (session.search_type_invoice=='STATUS'):
            qset=qset(db.sm_invoice_head.status==session.search_value_invoice)
        
        elif (session.search_type_invoice=='DSTATUS'):
            qset=qset(db.sm_invoice_head.depot_status==session.search_value_invoice)
        
        elif (session.search_type_invoice=='HOSTATUS'):
            qset=qset(db.sm_invoice_head.ho_status==session.search_value_invoice)
        
    records=qset.select(db.sm_invoice_head.ALL,orderby=~db.sm_invoice_head.id,limitby=limitby)
    totalRecords=qset.count()
    
    #------------------------------------------------
    search_form =SQLFORM(db.sm_search_date)
    #-------------
    if not(session.fromDate_order==None or session.date_to_order==None):
        search_form.vars.from_dt=session.fromDate_order
        search_form.vars.to_dt=session.date_to_order
    else:
        search_form.vars.from_dt=''
        search_form.vars.to_dt=''
    if search_form.accepts(request.vars):
        pass


    return dict(search_form=search_form,records=records,totalRecords=totalRecords,page=page,items_per_page=items_per_page,access_permission=access_permission,access_permission_view=access_permission_view)


def download_invoice_head():
    c_id=session.cid
    #----------------
    task_id='rm_invoice_manage'
    task_id_view='rm_invoice_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL(c='default', f='home'))
        
    response.title='Invoice-List'
    
    qset=db()
    qset=qset(db.sm_invoice_head.cid==c_id)    
    if (session.user_type=='Depot'):
        qset=qset(db.sm_invoice_head.depot_id==session.depot_id)        
        #------------- for filter same depot and sub-depot
        
    #---- supervisor
    if session.user_type=='Supervisor':
        qset=qset(db.sm_invoice_head.area_id.belongs(session.marketList))
    else:
        pass
    #----
    
    if (session.btn_filter_invoice):
        if (session.user_type!='Depot'):
            if not (session.depot_id_value_invoice=='' or session.depot_id_value_invoice==None):
                searchValue=str(session.depot_id_value_invoice).split('|')[0].upper()
                qset=qset(db.sm_invoice_head.depot_id==searchValue)
            else:
                qset=qset(db.sm_invoice_head.depot_id!='')
                
        #------------
        if (session.search_type_invoice=='DATE'):
            qset=qset(db.sm_invoice_head.delivery_date==session.search_value_invoice)
            
        elif (session.search_type_invoice=='ORDDATE'):
            try:
                order_datetimeFrom=datetime.datetime.strptime(str(session.search_value_invoice),'%Y-%m-%d')
                order_datetimeTo=order_datetimeFrom+datetime.timedelta(days=1)
            except:
                order_datetimeFrom=''
                order_datetimeTo=''
            qset=qset((db.sm_invoice_head.order_datetime>=order_datetimeFrom)&(db.sm_invoice_head.order_datetime<order_datetimeTo))
            
        else:
            session.flash='Required filter by Order Date or Delivery Date'
            redirect (URL('invoice_list'))
            
    else:
        session.flash='Required filter by Order Date or Delivery Date'
        redirect (URL('invoice_list'))
        
    records=qset.select(db.sm_invoice_head.ALL,orderby=~db.sm_invoice_head.id)
    
    #-------------------------------------
    myString='Delivery List'+'\n'
    
    myString+='DepotID,DepotName,INV.SL,Order Sl,Order Date,Delivery Date,Client/RetailerID,Client/RetailerName,Territory,MarketID,MarketName,Rep/SupID,Rep/SupName,Status\n'
    for rec in records:        
        depot_id=str(rec.depot_id)
        depot_name=str(rec.depot_name).replace(',', ' ')
        sl=str(rec.sl)
        order_sl=str(rec.order_sl)
        order_date=str(rec.order_datetime)[0:10]
        delivery_date=str(rec.delivery_date)        
        client_id=str(rec.client_id)
        client_name=str(rec.client_name).replace(',', ' ')
        area_id=str(rec.area_id)
        
        market_id=str(rec.market_id)
        market_name=str(rec.market_name).replace(',', ' ')
        rep_id=str(rec.rep_id)
        rep_name=str(rec.rep_name).replace(',', ' ')        
        status=str(rec.status)
        
        myString+=depot_id+','+depot_name+','+sl+','+order_sl+','+order_date+','+delivery_date+','+client_id+','+client_name+','+area_id+','+market_id+','+market_name+','+rep_id+','+rep_name+','+status+'\n'
        
    #Save as csv
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_delivery_list.csv'   
    return str(myString)
    #-------------


# Validation for invoice_generate
def process_invoice(form):
    c_id=session.cid
    form.vars.cid=c_id
    
    depot_id=str(request.vars.depot_id).strip().upper().split('|')[0]
    store_idname=str(request.vars.store_id)
    
    sl=int(form.vars.sl)
    
    ym_date=str(request.vars.delivery_date)[0:7]+'-01'
    
    #---------------
    client_id=str(request.vars.client_id).strip().upper().split('|')[0]
    rep_id=str(request.vars.rep_id).strip().upper().split('|')[0]    
    d_man_id=str(form.vars.d_man_id).strip().upper().split('|')[0]
    
    payment_mode=str(form.vars.payment_mode).strip()
    credit_note=str(form.vars.credit_note).strip()
    if payment_mode!='CREDIT':
        credit_note=''
        
    item_id=form.vars.item_id
    item_name=form.vars.item_name
    quantity=form.vars.quantity
    bonus_qty=form.vars.bonus_qty
    short_note=form.vars.short_note
    
    try:
        quantity=int(quantity)
        if quantity < 0:
            quantity=0
    except:
        quantity=0
        
    try:
        bonus_qty=int(bonus_qty)
        if bonus_qty < 0:
            bonus_qty=0
    except:
        bonus_qty=0
        
    batch_id=str(request.vars.batch_id).split('|')[0]
    
    if d_man_id=='NONE':
        d_man_id=''
    
    if store_idname=='':
        form.errors.depot_id='Required Store'
    else:
        store_id=str(store_idname).split('|')[0]
        store_name=str(store_idname).split('|')[1]
        
        if item_id=='' or item_id==None:
            form.errors.item_id='Select Item'
        else:
            itemRows=db((db.sm_item.cid==c_id)&(db.sm_item.item_id==item_id)).select(db.sm_item.item_id,db.sm_item.unit_type,db.sm_item.item_carton,db.sm_item.price,db.sm_item.vat_amt,limitby=(0,1))
            if not itemRows:
                form.errors.item_id='Invalid Item'
            else:
                price=itemRows[0].price
                vat_amt=itemRows[0].vat_amt
                item_unit=itemRows[0].unit_type
                item_carton=itemRows[0].item_carton
                
                #--------------------depot check
                depotRecords=db((db.sm_depot.cid==c_id)& (db.sm_depot.depot_id==depot_id)& (db.sm_depot.status=='ACTIVE')).select(db.sm_depot.name,limitby=(0,1))
                if not depotRecords:
                    form.errors.depot_id='Invalid Depot ID %s' %(depot_id)                        
                else:
                    dpName=depotRecords[0].name
                    form.vars.depot_id=depot_id
                    form.vars.depot_name=dpName
                    
                    #--------------------client check
                    clientRecords=db((db.sm_client.cid==c_id)& (db.sm_client.depot_id==depot_id) & (db.sm_client.client_id==client_id)& (db.sm_client.status=='ACTIVE')).select(db.sm_client.id,db.sm_client.name,db.sm_client.area_id,db.sm_client.market_id,db.sm_client.market_name,limitby=(0,1))
                    if not clientRecords:
                        form.errors.client_id='Invalid Client'
                    else:
                        clName=clientRecords[0].name
                        area_id=clientRecords[0].area_id
                        market_id=clientRecords[0].market_id
                        market_name=clientRecords[0].market_name
                        
                        areaName=''
                        level0_id=''
                        level0_name=''
                        level1_id=''
                        level1_name=''
                        level2_id=''
                        level2_name=''
                        level3_id=''
                        level3_name=''
                        levelRecords=db((db.sm_level.cid==c_id)& (db.sm_level.level_id==area_id)).select(db.sm_level.ALL,limitby=(0,1))
                        if not levelRecords:
                            form.errors.client_id='Invalid territory id of the Client'
                        else:
                            areaName=levelRecords[0].level_name
                            level0_id=levelRecords[0].level0
                            level0_name=levelRecords[0].level0_name
                            level1_id=levelRecords[0].level1
                            level1_name=levelRecords[0].level1_name
                            level2_id=levelRecords[0].level2
                            level2_name=levelRecords[0].level2_name
                            level3_id=levelRecords[0].level3
                            level3_name=levelRecords[0].level3_name
                            
                            form.vars.area_id=area_id
                            form.vars.area_name=areaName
                            form.vars.client_id=client_id
                            form.vars.client_name=clName
                            form.vars.market_id=market_id
                            form.vars.market_name=market_name
                            
                            form.vars.level0_id=level0_id
                            form.vars.level0_name=level0_name
                            form.vars.level1_id=level1_id
                            form.vars.level1_name=level1_name
                            form.vars.level2_id=level2_id
                            form.vars.level2_name=level2_name
                            form.vars.level3_id=level3_id
                            form.vars.level3_name=level3_name
                            
                            #---------------------- rep check
                            repRecords=db((db.sm_rep.cid==c_id) & (db.sm_rep.rep_id==rep_id)& (db.sm_rep.status=='ACTIVE')).select(db.sm_rep.id,db.sm_rep.name,limitby=(0,1))
                            if not repRecords:
                                form.errors.rep_id='Invalid/Inactive Rep/Sup'
                            else:
                                repName=repRecords[0].name
                                form.vars.rep_id=rep_id
                                form.vars.rep_name=repName
                                
#                                 repClientRecords=db((db.sm_rep_area.cid==c_id)& (db.sm_rep_area.rep_id==rep_id)& (db.sm_rep_area.area_id==area_id)).select(db.sm_rep_area.rep_id,limitby=(0,1))
#                                 if not repClientRecords:                                    
#                                     form.errors.rep_id='Customer territory and MSO-Territory not matched'   
#                                 else:                       
                                d_man_flag=True
                                d_man_name=''
                                
                                if d_man_id!='':
                                    dmanRecords=db((db.sm_delivery_man.cid==c_id)& (db.sm_delivery_man.depot_id==depot_id) & (db.sm_delivery_man.d_man_id==d_man_id)& (db.sm_delivery_man.status=='ACTIVE')).select(db.sm_delivery_man.id,db.sm_delivery_man.name,limitby=(0,1))
                                    if not dmanRecords:                                                                               
                                        d_man_flag=False
                                    else:
                                        d_man_name=dmanRecords[0].name
                                    
                                #------------
                                if d_man_flag==False:
                                    form.errors.d_man_id='Invalid Delivery Man'
                                else:
                                    form.vars.d_man_id=d_man_id
                                    form.vars.d_man_name=d_man_name
                                    
                                    #------
                                    if quantity == 0 and bonus_qty == 0:
                                        form.errors.quantity='Invalid quantity'
                                        
                                    elif quantity > 0 and bonus_qty > 0:
                                        form.errors.quantity='Required only one (Qty/BonusQty) Quantity'                                                  
                                    else:
                                        if bonus_qty > 0:
                                            price=0
                                            vat_amt=0
                                            
                                        batchFlag=True
                                        if batch_id!='':                                                
                                            itemBatchRows = db((db.sm_item_batch.cid == c_id) & (db.sm_item_batch.item_id == item_id) & (db.sm_item_batch.batch_id == batch_id) & (db.sm_item_batch.expiary_date >= current_date)).select(db.sm_item_batch.item_id,limitby=(0,1))
                                            if not itemBatchRows:
                                                form.errors.item_id='Invalid Item Batch ID'
                                                batchFlag=False
                                            else:                                                    
                                                stockRows=db((db.sm_depot_stock_balance.cid==c_id)& (db.sm_depot_stock_balance.depot_id==depot_id) & (db.sm_depot_stock_balance.store_id==store_id) & (db.sm_depot_stock_balance.item_id==item_id)& (db.sm_depot_stock_balance.batch_id==batch_id)).select(db.sm_depot_stock_balance.id,db.sm_depot_stock_balance.quantity,db.sm_depot_stock_balance.block_qty,limitby=(0,1))
                                                if not stockRows:
                                                    form.errors.quantity='Stock settings of the Item Batch is not available'
                                                    batchFlag=False
                                                else:
                                                    stock_quantity=stockRows[0].quantity
                                                    block_qty=stockRows[0].block_qty
                                                    availableQty=stock_quantity-block_qty
                                                    
                                                    if int(quantity+bonus_qty)>availableQty:
                                                        form.errors.quantity='Qty not available of the Item Batch, available qty '+str(availableQty)
                                                        batchFlag=False                                                    
                                                    else:
                                                        pass
                                        
                                        if batchFlag==True:
                                            existRow=db((db.sm_invoice.cid==c_id)& (db.sm_invoice.depot_id==depot_id) & (db.sm_invoice.sl==sl) & (db.sm_invoice.item_id==item_id)).select(db.sm_invoice.item_id,limitby=(0,1))
                                            if existRow:
                                                form.errors.item_id='Item ID already exist'
                                                batchFlag=False
                                            else:
                                                form.vars.store_id=store_id
                                                form.vars.store_name=store_name
                                                form.vars.batch_id=batch_id
                                                form.vars.actual_tp=price
                                                form.vars.actual_vat=vat_amt
                                                form.vars.quantity=quantity
                                                form.vars.bonus_qty=bonus_qty
                                                form.vars.price=price
                                                form.vars.item_vat=vat_amt
                                                form.vars.item_unit=item_unit
                                                form.vars.item_carton=item_carton
                                                
                                                if sl<=0:
                                                    maxSl=1
                                                    records=db((db.sm_depot.cid==c_id) & (db.sm_depot.depot_id==depot_id)).select(db.sm_depot.id,db.sm_depot.del_sl,limitby=(0,1))
                                                    if records:
                                                        sl=records[0].del_sl
                                                        maxSl=int(sl)+1
                                                        
                                                    #--- sl update in depot
                                                    records[0].update_record(del_sl=maxSl)
                                                    
                                                    form.vars.sl=maxSl
                                                
                                                form.vars.ym_date=ym_date
                                                form.vars.status='Draft'
                                                form.vars.payment_mode=payment_mode
                                                form.vars.credit_note=credit_note
                                                
def invoice_generate():
    c_id=session.cid
    #----------------
    response.title='Invoice/Delivery-Add'
   #----------Task assaign----------
    task_id='rm_invoice_manage'
    task_id_view='rm_invoice_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL(c='invoice_list'))
        
    #------------------- variable for batch upload
    total_row=request.vars.total_row
    count_inserted=request.vars.count_inserted
    count_error=request.vars.count_error
    error_str=request.vars.error_str
    
    if total_row==None:
        total_row=0
    if count_inserted==None:
        count_inserted=0
    if count_error==None:
        count_error=0
    if error_str==None:
        error_str=''
    
    #------------------
    btn_update=request.vars.btn_update
    btn_batch_upload=request.vars.btn_batch_upload
    btn_import_req=request.vars.btn_import_req
    
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
    #--------------------------
    
    #BUTTON UPDATE
    if btn_update:        
        req_depot_id=depot_id
        reqSl=request.vars.sl
        client_id=str(request.vars.client_id).strip().upper().split('|')[0]
        rep_id=str(request.vars.rep_id).strip().upper().split('|')[0]
        d_man_id=str(request.vars.d_man_id).strip().upper().split('|')[0]        
        payment_mode=str(request.vars.payment_mode).strip()
        req_note=str(request.vars.note).strip()
        acknowledge_check=str(request.vars.acknowledge_check).strip()
        
        discount=request.vars.discount   
        req_sl=int(reqSl)
        
        credit_note=str(request.vars.credit_note).strip()
        
        if payment_mode=='CREDIT':
            if credit_note=='':
                session.flash='Required Credit Type for Credit Invoice'
                redirect(URL(c='order_invoice',f='invoice_generate',vars=dict(req_sl=reqSl,dptid=req_depot_id)))
        
        limitOverFlag=0
        acknowledge_flag=0
        if payment_mode=='CASH':
            credit_note=''
        else:
            if acknowledge_check!='YES':            
                acknowledge_flag=1
                
            creditPolicyRow=db((db.sm_cp_approved.cid==c_id)&(db.sm_cp_approved.client_id==client_id)&(db.sm_cp_approved.status=='ACTIVE')).select(db.sm_cp_approved.credit_amount,limitby=(0,1))
            if not creditPolicyRow:
                limitOverFlag=1
            else:
                credit_amount=creditPolicyRow[0].credit_amount
                totalAmount=0
                tx_closing_balance=0
                ledgerRow=db((db.sm_transaction.cid==c_id)&(db.sm_transaction.tx_account=='CLT-'+str(client_id))&(db.sm_transaction.opposite_account=='DPT-'+str(depot_id))).select(db.sm_transaction.tx_closing_balance,orderby=~db.sm_transaction.tx_date,limitby=(0,1))
                if ledgerRow:
                    tx_closing_balance=ledgerRow[0].tx_closing_balance            
                clientTotal=tx_closing_balance+totalAmount
                
                if clientTotal>credit_amount:
                    limitOverFlag=1
                    
        if d_man_id=='NONE':
            d_man_id=''
            
        clientRecords=db((db.sm_client.cid==c_id)& (db.sm_client.depot_id==req_depot_id) & (db.sm_client.client_id==client_id)& (db.sm_client.status=='ACTIVE')).select(db.sm_client.client_id,db.sm_client.name,db.sm_client.area_id,limitby=(0,1))
        if not clientRecords:
            session.flash='Invalid Client ID'
        else:
            clName=clientRecords[0].name
            area_id=clientRecords[0].area_id   
            
            levelRecords=db((db.sm_level.cid==c_id)& (db.sm_level.level_id==area_id)).select(db.sm_level.level_name,limitby=(0,1))
            if not levelRecords:
                session.flash='Invalid Client Territory'
            else:
                area_name=levelRecords[0].level_name
                
                repRecords=db((db.sm_rep.cid==c_id)& (db.sm_rep.rep_id==rep_id)& (db.sm_rep.status=='ACTIVE')).select(db.sm_rep.rep_id,db.sm_rep.name,limitby=(0,1))
                if not repRecords:
                    session.flash='Invalid/Inactive Rep/Sup'
                else:
                    repName=repRecords[0].name
                    
#                     repClientRecords=db((db.sm_rep_area.cid==c_id)& (db.sm_rep_area.rep_id==rep_id)& (db.sm_rep_area.area_id==area_id)).select(db.sm_rep_area.rep_id,limitby=(0,1))
#                     if not repClientRecords:
#                         session.flash='Client Market not assign for Rep'
#                     else:
                    
                    d_man_flag=True
                    d_man_name=''      
                    if d_man_id!='':              
                        dmanRecords=db((db.sm_delivery_man.cid==c_id)& (db.sm_delivery_man.depot_id==req_depot_id) & (db.sm_delivery_man.d_man_id==d_man_id)& (db.sm_delivery_man.status=='ACTIVE')).select(db.sm_delivery_man.id,db.sm_delivery_man.name,limitby=(0,1))
                        if not dmanRecords:
                            session.flash='Invalid Delivery Man'
                            d_man_flag=False
                        else:
                            d_man_name=dmanRecords[0].name
                            
                    if (client_id!='' and rep_id!='' and d_man_flag==True):
                        db((db.sm_invoice_head.cid==c_id)& (db.sm_invoice_head.depot_id==req_depot_id) & (db.sm_invoice_head.sl==reqSl)).update(client_id=client_id,rep_id=rep_id,d_man_id=d_man_id,d_man_name=d_man_name,payment_mode=payment_mode,credit_note=credit_note,note=req_note,discount=discount,client_limit_over=limitOverFlag,acknowledge_flag=acknowledge_flag)
                        db((db.sm_invoice.cid==c_id)& (db.sm_invoice.depot_id==req_depot_id) & (db.sm_invoice.sl==reqSl)).update(client_id=client_id,rep_id=rep_id,d_man_id=d_man_id,d_man_name=d_man_name,payment_mode=payment_mode,credit_note=credit_note,note=req_note,discount=discount)
                        
        redirect(URL(c='order_invoice',f='invoice_generate',vars=dict(req_sl=reqSl,dptid=req_depot_id)))
    
    # BATCH UPLOAD will get based on access permission and status
#    elif (btn_batch_upload and str(request.vars.input_data)!='' and str(depot_id)!=''):
#         req_depot_id=depot_id   #str(request.vars.depot_id).strip().upper().split('|')[0]
#         reqSl=request.vars.sl
#         client_id=str(request.vars.client_id).strip().upper().split('|')[0]
#         rep_id=str(request.vars.rep_id).strip().upper().split('|')[0]
#         d_man_id=str(request.vars.d_man_id).strip().upper().split('|')[0]
#         delivery_date=request.vars.delivery_date
#         ym_date=str(delivery_date)[0:7]+'-01'
#         payment_mode=request.vars.payment_mode
#         req_note=str(request.vars.note).strip()
#         discount=request.vars.discount
#         
#         order_datetime=datetime_fixed
#         
#         req_sl=reqSl
#         
#         if req_depot_id=='' or str(req_depot_id)=='None':
#             session.flash='Required Depot'
#         else:
#             if int(reqSl)!=0:
#                 session.flash='new invoice needed!'
#             else:
#                 clientRecords=db((db.sm_client.cid==c_id)& (db.sm_client.depot_id==req_depot_id) & (db.sm_client.client_id==client_id)& (db.sm_client.status=='ACTIVE')).select(db.sm_client.name,db.sm_client.area_id,limitby=(0,1))
#                 if not clientRecords:
#                     session.flash='Invalid Client ID!'
#                 else:
#                     repRecords=db((db.sm_rep.cid==c_id)& (db.sm_rep.depot_id==req_depot_id) & (db.sm_rep.rep_id==rep_id)& (db.sm_rep.status=='ACTIVE')).select(db.sm_rep.name,limitby=(0,1))
#                     if not repRecords:
#                         session.flash='Invalid Rep ID'              
#                     else:
#                         dmanRecords=db((db.sm_delivery_man.cid==c_id) & (db.sm_delivery_man.depot_id==req_depot_id) & (db.sm_delivery_man.d_man_id==d_man_id)& (db.sm_delivery_man.status=='ACTIVE')).select(db.sm_delivery_man.id,db.sm_delivery_man.name,limitby=(0,1))
#                         if not dmanRecords:
#                             session.flash='Invalid Delivery Man'
#                         else:
#                             d_man_name=dmanRecords[0].name
#                             
#                             #--------------------depot check
#                             depotRecords=db((db.sm_depot.cid==c_id)& (db.sm_depot.depot_id==req_depot_id)& (db.sm_depot.status=='ACTIVE')).select(db.sm_depot.name,limitby=(0,1))
#                             if not depotRecords:
#                                 session.flash='Invalid Depot ID'
#                             else:
#                                 dpName=depotRecords[0].name
#                                 #---------------------                        
#                                 clName=clientRecords[0].name
#                                 area_id=clientRecords[0].area_id
#                                 #---------------
#                                 area_name=''
#                                 levelRecords=db((db.sm_level.cid==c_id)& (db.sm_level.level_id==area_id)).select(db.sm_level.level_name,limitby=(0,1))
#                                 if levelRecords:
#                                     area_name=levelRecords[0].level_name
#                                 
#                                 #----------
#                                 repName=repRecords[0].name                        
#                                 
#                                 
#                                 #Get max sl from sm_depot
#                                 if (payment_mode!='' and delivery_date!=''):
#                                     maxSl=1
#                                     records=db((db.sm_depot.cid==c_id) & (db.sm_depot.depot_id==req_depot_id)).select(db.sm_depot.id,db.sm_depot.del_sl,limitby=(0,1))
#                                     if records:
#                                         sl=records[0].del_sl
#                                         maxSl=int(sl)+1
#                                     
#                                     #--- sl update in depot
#                                     records[0].update_record(del_sl=maxSl)
#                                     
#                                     #----------- variable declaration
#                                     count_inserted=0
#                                     count_error=0
#                                     error_str=''
#                                     total_row=0
#                                     
#                                     item_list=[]
#                                     item_list_table=[]
#                                     item_exist_table=[]
#                                     
#                                     excelList=[]
#                                     
#                                     ins_dict={}
#                                     ins_list=[]
#                                     
#                                     #---------
#                                     input_data=str(request.vars.input_data)
#                                     
#                                     error_list=[]
#                                     row_list=input_data.split( '\n')
#                                     total_row=len(row_list)
#                                     
#                                     #   ---------------------- valid item list loop
#                                     for i in range(total_row):
#                                         if i>=30:
#                                             break
#                                         else:
#                                             row_data=row_list[i]                    
#                                             coloum_list=row_data.split( '\t')
#                                             if len(coloum_list)==3:
#                                                 item_list.append(str(coloum_list[0]).strip().upper())
#                                     # Create from sm_item list
#                                     itemRows=db((db.sm_item.cid==c_id)&(db.sm_item.item_id.belongs(item_list))).select(db.sm_item.item_id,db.sm_item.name,db.sm_item.category_id,db.sm_item.price,orderby=db.sm_item.name)
#                                     item_list_table=itemRows.as_list()
#                                     
#                                     # Create item list already exist in  database based on excel sheet
#                                     existRecords=db((db.sm_invoice.cid==c_id) & (db.sm_invoice.depot_id==req_depot_id)& (db.sm_invoice.sl==maxSl)& (db.sm_invoice.item_id.belongs(item_list))).select(db.sm_invoice.item_id)
#                                     item_exist_table=existRecords.as_list()
#                                     
#                                     #   --------------------  excel main loop
#                                     headFlag=False
#                                     for i in range(total_row):
#                                         if i>=30: 
#                                             break
#                                         else:
#                                             row_data=row_list[i]        
#                                             coloum_list=row_data.split( '\t')            
#                                         
#                                         if len(coloum_list)==3:
#                                             try:
#                                                 item_id_value=str(coloum_list[0]).strip().upper()
#                                                 item_qty_value=int(coloum_list[1])
#                                                 item_bonus_qty_value=int(coloum_list[2])
#                                                 
#                                                 #----------- check valid item
#                                                 name=''
#                                                 category_id=''
#                                                 price=0
#                                                 valid_item=False  
#                                                 if len(item_list_table) > 0:
#                                                     #Get item info
#                                                     for i in range(len(item_list_table)):
#                                                         myRowData=item_list_table[i]                                
#                                                         item_id=myRowData['item_id']
#                                                         name=myRowData['name']
#                                                         category_id=myRowData['category_id']
#                                                         price=myRowData['price']
#                                                         if (str(item_id).strip()==str(item_id_value).strip()):
#                                                             valid_item=True
#                                                             break
#                                                 
#                                                 #-----------------
#                                                 if valid_item==True:#----------- check duplicate                       
#                                                     duplicate_item=False  
#                                                     if len(item_exist_table) > 0:
#                                                         for j in range(len(item_exist_table)):
#                                                             myRowData=item_exist_table[j]                                
#                                                             item_id=myRowData['item_id']
#                                                             if (str(item_id).strip()==str(item_id_value).strip()):
#                                                                 duplicate_item=True
#                                                                 break
#                                                 
#                                                 #Create list for bulk insert
#                                                 if (int(item_qty_value) > 0 and item_bonus_qty_value>=0):
#                                                     if (valid_item==True):
#                                                         if(duplicate_item==False): 
#                                                             if item_id_value not in excelList:
#                                                                 #Check duplicate in excel sheet
#                                                                 excelList.append(item_id_value)
#                                                                 
#                                                                 ins_dict= {'cid':c_id,'depot_id':req_depot_id,'depot_name':dpName,'sl':maxSl,'client_id':client_id,'client_name':clName,'rep_id':rep_id,'rep_name':repName,'d_man_id':d_man_id,'d_man_name':d_man_name,'order_datetime':order_datetime,'delivery_date':delivery_date,'payment_mode':payment_mode,'note':req_note,
#                                                                        'area_id':area_id,'area_name':area_name,'item_id':item_id_value,'item_name':name,'category_id':category_id,'quantity':item_qty_value,'bonus_qty':item_bonus_qty_value,'price':price,'ym_date':ym_date}
#                                                             
#                                                                 ins_list.append(ins_dict)                               
#                                                                 if headFlag==False:
#                                                                     db.sm_invoice_head.insert(cid=c_id,depot_id=req_depot_id,sl=maxSl,client_id=client_id,rep_id=rep_id,d_man_id=d_man_id,d_man_name=d_man_name,delivery_date=delivery_date,depot_name=dpName,client_name=clName,rep_name=repName,area_id=area_id,area_name=area_name,payment_mode=payment_mode,note=req_note,ym_date=ym_date)
#                                                                     headFlag=True
#                         
#                                                                 count_inserted+=1
#                                                             else:
#                                                                 error_data=row_data+'(duplicate in excel!)\n'
#                                                                 error_str=error_str+error_data
#                                                                 count_error+=1
#                                                                 continue
#                                                             
#                                                         else:
#                                                             error_data=row_data+'(duplicate item)\n'
#                                                             error_str=error_str+error_data
#                                                             count_error+=1
#                                                             continue
#                                                             
#                                                     else:
#                                                         error_data=row_data+'(Invalid Item)\n'
#                                                         error_str=error_str+error_data
#                                                         count_error+=1
#                                                         continue
#                             
#                                                 else:
#                                                     error_data=row_data+'(need quantity)\n'
#                                                     error_str=error_str+error_data
#                                                     count_error+=1
#                                                     continue
#                             
#                                             except:
#                                                 error_data=row_data+'(process error)\n'
#                                                 error_str=error_str+error_data
#                                                 count_error+=1
#                                                 continue
#                                         else:
#                                             error_data=row_data+'(3 columns need in a row)\n'
#                                             error_str=error_str+error_data
#                                             count_error+=1
#                                             continue
#                                     
#                                     if error_str=='':
#                                         error_str='No error'
#                                     
#                                     if len(ins_list)>0:
#                                         inCountList=db.sm_invoice.bulk_insert(ins_list)   
#                                         session.flash='Successfully uploaded'
#                                     else:
#                                         session.flash='Data not processed to upload'
#                                     
#                                     req_sl=maxSl
#                     #                
#                                 
#                                 else:
#                                     session.flash='need Date and Payment mode!'
#         
#         redirect(URL('invoice_generate',vars=dict(req_sl=req_sl,dptid=req_depot_id,count_inserted=count_inserted,count_error=count_error,error_str=error_str,total_row=total_row)))
#     
    #--------- IMPORT FROM ORDER
    #Order can be import based order status
    elif btn_import_req:
        req_depot_id=depot_id #str(request.vars.depot_id).strip().upper().split('|')[0]
        try:
            reqSl=int(request.vars.sl)
        except:
            reqSl=0
            
        #======================================== IMPORT ORDER
        settCompRows=db((db.sm_settings.cid==c_id)&(db.sm_settings.s_key=='AUTO_DELIVERY')).select(db.sm_settings.s_value,limitby=(0,1))
        autoDelivery=''        
        if settCompRows:
            autoDelivery=str(settCompRows[0].s_value).strip().upper()
            
        if autoDelivery=='':
            session.flash='Required auto delivery settings' #, auto delivery=NO
            redirect(URL(c='order_invoice',f='invoice_generate',vars=dict(req_sl=reqSl,dptid=req_depot_id)))            
        else:
            
            try:
                order_sl=int(request.vars.order_sl)
            except:
                order_sl=0
                
            if reqSl==0 :
                session.flash='Invalid invoice'
            else:
                payment_mode=''
                credit_note=''
                d_man_id=''
                d_man_name=''
                note=''
                status=''
                invRow=db((db.sm_invoice_head.cid==c_id) & (db.sm_invoice_head.depot_id==req_depot_id)& (db.sm_invoice_head.sl==reqSl)).select(db.sm_invoice_head.payment_mode,db.sm_invoice_head.credit_note,db.sm_invoice_head.d_man_id,db.sm_invoice_head.d_man_name,db.sm_invoice_head.status,db.sm_invoice_head.note,limitby=(0,1))
                if invRow:
                    payment_mode=invRow[0].payment_mode
                    credit_note=invRow[0].credit_note
                    d_man_id=invRow[0].d_man_id
                    d_man_name=invRow[0].d_man_name
                    note=invRow[0].note
                    status=invRow[0].status
                    
                if order_sl <= 0:
                    session.flash='Requird valid Order SL'
                else:
                              
                    orderRecords=db((db.sm_order_head.cid==c_id)& (db.sm_order_head.depot_id==req_depot_id)  & (db.sm_order_head.sl==order_sl)).select(db.sm_order_head.ALL,limitby=(0,1))
                    if not orderRecords:
                        session.flash='Order not available of the Depot'
                    else:
                        depot_name=orderRecords[0].depot_name
                        store_id=orderRecords[0].store_id
                        store_name=orderRecords[0].store_name
                        client_id=orderRecords[0].client_id
                        client_name=orderRecords[0].client_name
                        clientCategory=orderRecords[0].client_cat
                        rep_id=orderRecords[0].rep_id
                        rep_name=orderRecords[0].rep_name
                        area_id=orderRecords[0].area_id
                        area_name=orderRecords[0].area_name                                
                        order_datetime=orderRecords[0].order_datetime
                        order_media=orderRecords[0].order_media
                        delivery_date=orderRecords[0].delivery_date
                        #payment_mode=orderRecords[0].payment_mode
                        req_note=orderRecords[0].note        
                        market_id=orderRecords[0].market_id
                        market_name=orderRecords[0].market_name
                        #---delivery date get from order date
                        ym_date=str(delivery_date)[0:7]+'-01'
                        req_delivery_date=str(delivery_date)[0:10]
                        
                        level0_id=orderRecords[0].level0_id
                        level0_name=orderRecords[0].level0_name
                        level1_id=orderRecords[0].level1_id
                        level1_name=orderRecords[0].level1_name
                        level2_id=orderRecords[0].level2_id
                        level2_name=orderRecords[0].level2_name
                        level3_id=orderRecords[0].level3_id
                        level3_name=orderRecords[0].level3_name
                        
                        orderRows=db((db.sm_order.cid==c_id) & (db.sm_order.depot_id==req_depot_id) &(db.sm_order.sl==order_sl)).select(db.sm_order.ALL,orderby=db.sm_order.item_name)
                        if not orderRows:
                            session.flash='Order not available of the Depot'                            
                        else:
                            detailList=[]                            
                            for ordRec in orderRows:                                
                                item_id=str(ordRec.item_id).strip().upper()
                                item_name=ordRec.item_name
                                category_id=ordRec.category_id
                                item_qty_value=int(ordRec.quantity)
                                price=float(ordRec.price)   
                                item_vat=float(ordRec.item_vat)
                                item_unit=ordRec.item_unit
                                item_carton=ordRec.item_carton
                                actual_tp=price
                                actual_vat=item_vat
                                
                                detailDict={'cid':c_id,'depot_id':req_depot_id,'depot_name':depot_name,'sl':reqSl,'store_id':store_id,'store_name':store_name,'order_sl':order_sl,'order_datetime':order_datetime,'delivery_date':req_delivery_date,'client_id':client_id,'client_name':client_name,'rep_id':rep_id,'rep_name':rep_name,'market_id':market_id,'market_name':market_name,'area_id':area_id,'area_name':area_name,'level0_id':level0_id,'level0_name':level0_name,'level1_id':level1_id,'level1_name':level1_name,'level2_id':level2_id,'level2_name':level2_name,'level3_id':level3_id,'level3_name':level3_name,'invoice_media':order_media,'device_user_agent':'','ip_ref':'','ym_date':ym_date,'payment_mode':payment_mode,'credit_note':credit_note,'d_man_id':d_man_id,'d_man_name':d_man_name,'item_id':item_id,'item_name':item_name,'batch_id':'','category_id':category_id,'actual_tp':actual_tp,'actual_vat':actual_vat,'quantity':item_qty_value,'bonus_qty':0,'price':price,'item_vat':item_vat,'sp_discount_item':0,'item_unit':item_unit,'item_carton':item_carton,'note':note,'short_note':'','status':status}
                                detailList.append(detailDict)
                            
                            session.flash='Order imported successfully'
                            rows=db.sm_invoice.bulk_insert(detailList)
            
            #=======================
            redirect(URL(c='order_invoice',f='invoice_generate',vars=dict(req_sl=reqSl,dptid=req_depot_id)))
    
    #=========================== ITEM SAVE/ REPLACE IF EXIST
    db.sm_invoice.payment_mode.requires=IS_IN_DB(db((db.sm_category_type.cid == session.cid)&(db.sm_category_type.type_name=='PAYMENT_MODE')),db.sm_category_type.cat_type_id,'%(cat_type_id)s',orderby=db.sm_category_type.cat_type_id)
    db.sm_invoice.credit_note.requires=IS_EMPTY_OR(IS_IN_DB(db((db.sm_category_type.cid == session.cid)&(db.sm_category_type.type_name=='CREDIT_NOTE')),db.sm_category_type.cat_type_id,'%(cat_type_id)s',orderby=db.sm_category_type.cat_type_id))
    db.sm_invoice.quantity.requires=IS_INT_IN_RANGE(0, 999999,error_message='Invalid number')
    
    form =SQLFORM(db.sm_invoice,
                  fields=['depot_id','sl','store_id','payment_mode','credit_note','client_id','rep_id','d_man_id','order_sl','delivery_date','status','discount','item_id','item_name','category_id','batch_id','quantity','bonus_qty','price','item_vat','note','short_note'],
                  submit_button='Save'
                  )
    form.vars.cid=c_id
    form.vars.quantity=''
    if not(btn_update or btn_batch_upload or btn_import_req):
        if form.accepts(request.vars,session,onvalidation=process_invoice):
            sl=form.vars.sl
            depot_id=form.vars.depot_id
            depot_name=form.vars.depot_name
            store_id=form.vars.store_id
            store_name=form.vars.store_name
            
            payment_mode=form.vars.payment_mode
            credit_note=form.vars.credit_note
            
            client_id=form.vars.client_id
            client_name=form.vars.client_name
            rep_id=form.vars.rep_id
            rep_name=form.vars.rep_name
            area_id=form.vars.area_id
            area_name=form.vars.area_name
            market_id=form.vars.market_id
            market_name=form.vars.market_name
            
            level0_id=form.vars.level0_id
            level0_name=form.vars.level0_name
            level1_id=form.vars.level1_id
            level1_name=form.vars.level1_name
            level2_id=form.vars.level2_id
            level2_name=form.vars.level2_name
            level3_id=form.vars.level3_id
            level3_name=form.vars.level3_name
            
            d_man_id=form.vars.d_man_id
            d_man_name=form.vars.d_man_name
            discount=form.vars.discount
            note=form.vars.note
            
            delivery_date=form.vars.delivery_date
            ym_date=str(delivery_date)[0:7]+'-01'
            
            item_id=form.vars.item_id
            batch_id=form.vars.batch_id
            quantity=form.vars.quantity
            bonus_qty=form.vars.bonus_qty
            
            acknowledge_flag=0
            if payment_mode!='CASH':
                acknowledge_flag=1
                
            #--------------------- block qty free because of submitted to draft mode
            invoiceRows=db((db.sm_invoice.cid==c_id)& (db.sm_invoice.depot_id==depot_id) & (db.sm_invoice.sl==sl) & (db.sm_invoice.status=='Submitted') & (db.sm_invoice.batch_id!='')).select(db.sm_invoice.store_id,db.sm_invoice.item_id,db.sm_invoice.batch_id,db.sm_invoice.quantity,db.sm_invoice.bonus_qty)
            if invoiceRows:                
                #----------------- check stock cron flag
                autDelCronRows=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)&(db.sm_depot.auto_del_cron_flag==0)).select(db.sm_depot.id,db.sm_depot.cid,limitby=(0,1))
                if not autDelCronRows:
                    db.rollback()                    
                    session.flash='One process running, please try again'                    
                    req_sl=sl
                    redirect(URL(c='order_invoice',f='invoice_generate',vars=dict(req_sl=req_sl,dptid=depot_id)))
                else:
                    autDelCronRows[0].update_record(auto_del_cron_flag=1)
                    #-------------                    
                    for invRow in invoiceRows:
                        storeId=invRow.store_id
                        itemId=invRow.item_id
                        batchId=invRow.batch_id
                        invQquantity=invRow.quantity
                        invBbonus_qty=invRow.bonus_qty
                        
                        stockRows=db((db.sm_depot_stock_balance.cid==c_id)& (db.sm_depot_stock_balance.depot_id==depot_id) & (db.sm_depot_stock_balance.store_id==storeId) & (db.sm_depot_stock_balance.item_id==itemId)& (db.sm_depot_stock_balance.batch_id==batchId)).select(db.sm_depot_stock_balance.id,db.sm_depot_stock_balance.block_qty,limitby=(0,1))
                        if stockRows:                        
                            block_qty=stockRows[0].block_qty
                                                    
                            newBlockQty=block_qty-(invQquantity+invBbonus_qty)
                            if newBlockQty<0:
                                newBlockQty=0    
                                
                            stockRows[0].update_record(block_qty=newBlockQty)
                            
                    #---------------------
                    autDelCronRows[0].update_record(auto_del_cron_flag=0)
                    #db.commit()
                    #--------------
                    
            #---------------- bonus qty delete
            db((db.sm_invoice.cid==c_id) & (db.sm_invoice.depot_id==depot_id)& (db.sm_invoice.sl==sl)& (db.sm_invoice.bonus_qty>0)).delete()
            
            #------------ Head update
            discount=0
            status='Draft'
            batch_id=''
            
            #----------- head insert/update
            headRows=db((db.sm_invoice_head.cid==c_id)& (db.sm_invoice_head.depot_id==depot_id) & (db.sm_invoice_head.sl==sl)).select(db.sm_invoice_head.id,db.sm_invoice_head.order_datetime,limitby=(0,1))
            if headRows:
                order_datetime=headRows[0].order_datetime
                headRows[0].update_record(payment_mode=payment_mode,credit_note=credit_note,client_id=client_id,rep_id=rep_id,d_man_id=d_man_id,d_man_name=d_man_name,delivery_date=delivery_date,discount=discount,note=note,ym_date=ym_date,depot_name=depot_name,client_name=client_name,rep_name=rep_name,area_id=area_id,area_name=area_name,market_id=market_id,market_name=market_name,status=status,client_limit_over=0,empty_batch_flag=1,acknowledge_flag=acknowledge_flag)
            else:
                order_datetime=date_fixed
                db.sm_invoice_head.insert(cid=c_id,depot_id=depot_id,sl=sl,store_id=store_id,store_name=store_name,client_id=client_id,rep_id=rep_id,d_man_id=d_man_id,d_man_name=d_man_name,delivery_date=delivery_date,order_datetime=order_datetime,depot_name=depot_name,client_name=client_name,rep_name=rep_name,area_id=area_id,area_name=area_name,market_id=market_id,market_name=market_name,level0_id=level0_id,level0_name=level0_name,level1_id=level1_id,level1_name=level1_name,level2_id=level2_id,level2_name=level2_name,level3_id=level3_id,level3_name=level3_name,payment_mode=payment_mode,credit_note=credit_note,discount=discount,note=note,ym_date=ym_date,status=status,client_limit_over=0,empty_batch_flag=1,acknowledge_flag=acknowledge_flag)
                
            #----------UPDATE SAME SL DATA
            db((db.sm_invoice.cid==c_id)& (db.sm_invoice.depot_id==depot_id) & (db.sm_invoice.sl==sl)).update(d_man_id=d_man_id,d_man_name=d_man_name,payment_mode=payment_mode,credit_note=credit_note,client_id=client_id,rep_id=rep_id,delivery_date=delivery_date,discount=discount,note=note,ym_date=ym_date,depot_name=depot_name,order_datetime=order_datetime,client_name=client_name,rep_name=rep_name,area_id=area_id,area_name=area_name,market_id=market_id,market_name=market_name,status=status,batch_id='',short_note='')
            
            #change rate for rep-processing
            updateRecords1="update sm_invoice inv, sm_item itm set inv.actual_tp=itm.price,inv.actual_vat=itm.vat_amt,inv.price=itm.price,inv.item_vat=itm.vat_amt,inv.discount=0,inv.status='Draft',inv.batch_id='',inv.short_note='' where inv.cid='"+str(c_id)+"' and inv.depot_id='"+str(depot_id)+"' and inv.sl="+str(sl)+" and itm.cid='"+str(c_id)+"' and inv.item_id=itm.item_id"
            db.executesql(updateRecords1)
            
            #updateRecords="update sm_invoice set price=actual_tp,item_vat=actual_vat,discount=0,status='Draft',batch_id='',short_note='' where cid='"+str(c_id)+"' and depot_id='"+str(depot_id)+"' and sl="+str(sl)
            #db.executesql(updateRecords)
            
            duplicateCheck=True
            #-------------- delete duplicate row item
            if duplicateCheck==True:
                duplicateList=[]
                duplicatRows=db((db.sm_invoice.cid==c_id)& (db.sm_invoice.depot_id==depot_id) & (db.sm_invoice.sl==sl)).select(db.sm_invoice.item_id,db.sm_invoice.item_id.count(),db.sm_invoice.quantity.sum(),groupby=db.sm_invoice.item_id)
                for dupRow in duplicatRows:            
                    if int(dupRow[db.sm_invoice.item_id.count()])>1:
                        dupItemId=str(dupRow.sm_invoice.item_id)
                        dupItemQty=int(dupRow[db.sm_invoice.quantity.sum()])                
                        duplicateList.append({'item_id':dupItemId,'totalQty':dupItemQty})                
                
                if len(duplicateList)>0:
                    for i in range(len(duplicateList)):
                        dupItemID=duplicateList[i]['item_id']
                        dupItemQnty=duplicateList[i]['totalQty']
                        
                        updatedFlag=0
                        dupRows=db((db.sm_invoice.cid==c_id)& (db.sm_invoice.depot_id==depot_id) & (db.sm_invoice.sl==sl) & (db.sm_invoice.item_id==dupItemID)).select(db.sm_invoice.id,orderby=db.sm_invoice.id)
                        for dupRow in dupRows:
                            if updatedFlag==0:
                                dupRow.update_record(quantity=dupItemQnty)                                
                                updatedFlag=1
                            else:                            
                                dupRow.delete_record()
                #end duplicate row item
            
            
            #----------------
            req_sl=sl
            redirect(URL(c='order_invoice',f='invoice_generate',vars=dict(req_sl=req_sl,dptid=depot_id)))
            
        elif form.errors:
            response.flash = 'form has errors'
            for fieldname in form.errors:
                #response.flash =str(fieldname) +' error: '+ str(form.errors[fieldname])
                response.flash =str(form.errors[fieldname])
        #redirect(URL(c='order_invoice',f='invoice_generate',vars=dict(req_sl=req_sl,depot_id=depot_id)))
        
    #  --------------------- NEW INVOICE/SHOW FIELD VALUE
    
    rowid=0
    sl=0
    status='Submitted'
    client_id=''
    rep_id=''
    d_man_id=''
    
    delivery_dt=current_date
    note='' 
    order_sl=0  
    discount=0
    
    client_name=''
    rep_name=''
    d_man_name=''
    client_limit_over=0
    acknowledge_flag=0
    store_id=''
    store_name=''
    promo_ref=0
    empty_batch_flag=0
    discount_precent=0
    
    #Insert after validation
    hRecords=db((db.sm_invoice_head.cid==c_id)& (db.sm_invoice_head.depot_id==depot_id) & (db.sm_invoice_head.sl==req_sl)).select(db.sm_invoice_head.ALL,limitby=(0,1))
    if hRecords:
        rowid=hRecords[0].id
        depot_id=hRecords[0].depot_id
        depot_name=hRecords[0].depot_name
        store_id=hRecords[0].store_id
        store_name=hRecords[0].store_name
        sl=hRecords[0].sl
        order_sl=hRecords[0].order_sl
        delivery_dt=hRecords[0].delivery_date
        status=hRecords[0].status
        client_id=hRecords[0].client_id
        rep_id=hRecords[0].rep_id
        d_man_id=hRecords[0].d_man_id
        
        client_name=hRecords[0].client_name
        rep_name=hRecords[0].rep_name
        d_man_name=hRecords[0].d_man_name
        
        discount=hRecords[0].discount
        discount_precent=hRecords[0].discount_precent
        
        note=hRecords[0].note
        client_limit_over=hRecords[0].client_limit_over
        acknowledge_flag=hRecords[0].acknowledge_flag
        promo_ref=hRecords[0].promo_ref
        empty_batch_flag=hRecords[0].empty_batch_flag
        
    records=db((db.sm_invoice.cid==c_id)& (db.sm_invoice.depot_id==depot_id) & (db.sm_invoice.sl==req_sl)).select(db.sm_invoice.ALL,orderby=db.sm_invoice.item_name)
    
    storeRecords=''
    if sl<=0:
        storeRecords=db((db.sm_depot_store.cid==c_id) & (db.sm_depot_store.depot_id==depot_id)& (db.sm_depot_store.store_type=='SALES')).select(db.sm_depot_store.store_id,db.sm_depot_store.store_name,orderby=db.sm_depot_store.store_name)
        
    #-------------------- SHOW VALUE BY RECORD ID
    if rowid!=0:
        record= db.sm_invoice_head(rowid)
        
        db.sm_invoice_head.payment_mode.requires=IS_IN_DB(db((db.sm_category_type.cid == session.cid)&(db.sm_category_type.type_name=='PAYMENT_MODE')),db.sm_category_type.cat_type_id,'%(cat_type_id)s',orderby=db.sm_category_type.cat_type_id)
        db.sm_invoice_head.credit_note.requires=IS_EMPTY_OR(IS_IN_DB(db((db.sm_category_type.cid == session.cid)&(db.sm_category_type.type_name=='CREDIT_NOTE')),db.sm_category_type.cat_type_id,'%(cat_type_id)s',orderby=db.sm_category_type.cat_type_id))
        
        form_head =SQLFORM(db.sm_invoice_head,
                     record=record,
                     fields=['payment_mode','credit_note','discount','note'],
                     )
        
        if form_head.accepts(request.vars,session):
            pass
        
        return dict(form=form,form_head=form_head,rowid=rowid,records=records,storeRecords=storeRecords,depot_id=depot_id,depot_name=depot_name,sl=sl,store_id=store_id,store_name=store_name,order_sl=order_sl,client_id=client_id,rep_id=rep_id,d_man_id=d_man_id,d_man_name=d_man_name,client_name=client_name,rep_name=rep_name,status=status,discount=discount,discount_precent=discount_precent,note=note,client_limit_over=client_limit_over,acknowledge_flag=acknowledge_flag,
                promo_ref=promo_ref,empty_batch_flag=empty_batch_flag,count_inserted=count_inserted,count_error=count_error,error_str=error_str,total_row=total_row,delivery_dt=delivery_dt,access_permission=access_permission,access_permission_view=access_permission_view)
    else:
        return dict(form=form,rowid=rowid,records=records,storeRecords=storeRecords,depot_id=depot_id,depot_name=depot_name,sl=sl,store_id=store_id,store_name=store_name,order_sl=order_sl,client_id=client_id,rep_id=rep_id,d_man_id=d_man_id,d_man_name=d_man_name,client_name=client_name,rep_name=rep_name,status=status,discount=discount,discount_precent=discount_precent,note=note,client_limit_over=client_limit_over,acknowledge_flag=acknowledge_flag,
                promo_ref=promo_ref,empty_batch_flag=empty_batch_flag,count_inserted=count_inserted,count_error=count_error,error_str=error_str,total_row=total_row,delivery_dt=delivery_dt,access_permission=access_permission,access_permission_view=access_permission_view)

#----------------- Show pending Order
def show_pending_order():   
    response.title='Pending Order'
    
    # Set text for filter    
    btn_filter_pending_ord=request.vars.btn_filter_pending_ord
    btn_all=request.vars.btn_all
    
    reqPage=len(request.args)
    
    if btn_filter_pending_ord:
        session.btn_filter_pending_ord=btn_filter_pending_ord
        session.repID_value=str(request.vars.rep_id_value).strip().upper()        
        reqPage=0
        
    elif btn_all:
        session.btn_filter_pending_ord=None
        session.repID_value=None
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
    qset=qset(db.sm_order_head.cid==session.cid) 
    
    if session.user_type=='Depot':
        qset=qset(db.sm_order_head.depot_id==session.depot_id)
        
    if (session.btn_filter_pending_ord):
        qset=qset(db.sm_order_head.rep_id==session.repID_value)
        
    qset=qset(db.sm_order_head.status=='Submitted') 
    
    records=qset.select(db.sm_order_head.depot_id,db.sm_order_head.sl,db.sm_order_head.order_date,db.sm_order_head.client_id,db.sm_order_head.rep_id,db.sm_order_head.area_id,orderby=db.sm_order_head.sl,limitby=limitby)    
    
    return dict(records=records,page=page,items_per_page=items_per_page)
    
# Delete item if more than one item in a sl
def update_invoice_item():
    c_id=session.cid
    
    btn_delete=request.vars.btn_delete
    btn_qtyupdate=request.vars.btn_qtyupdate
    btn_delete_empty_batch=request.vars.btn_delete_empty_batch
    
    req_depot=request.args(0)
    req_sl=request.args(1)    
    req_item=request.args(2)
    rowid=request.args(3)
    
    if btn_delete:
        #--------------------------- chcek stock cron flag
        autDelCronRows=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==req_depot)&(db.sm_depot.auto_del_cron_flag==0)).select(db.sm_depot.id,db.sm_depot.cid,limitby=(0,1))
        if not autDelCronRows:
            session.flash='One process running, please try again'
        else:
            autDelCronRows[0].update_record(auto_del_cron_flag=1)
            #---------------------
            
            duplicateCheck=False
            
            countRecords=db((db.sm_invoice.cid==c_id)& (db.sm_invoice.depot_id==req_depot) & (db.sm_invoice.sl==req_sl)).count()
            if int(countRecords)==1:
                session.flash='At least one item needs in an invoice, You can cancel if required!'
            else:
                invoiceRows=db((db.sm_invoice.cid==c_id)& (db.sm_invoice.depot_id==req_depot) & (db.sm_invoice.sl==req_sl) & (db.sm_invoice.status=='Submitted') & (db.sm_invoice.batch_id!='')).select(db.sm_invoice.store_id,db.sm_invoice.item_id,db.sm_invoice.batch_id,db.sm_invoice.quantity,db.sm_invoice.bonus_qty)
                for invRow in invoiceRows:
                    store_id=invRow.store_id
                    item_id=invRow.item_id
                    batch_id=invRow.batch_id
                    quantity=invRow.quantity
                    bonus_qty=invRow.bonus_qty
                    
                    stockRows=db((db.sm_depot_stock_balance.cid==c_id)& (db.sm_depot_stock_balance.depot_id==req_depot) & (db.sm_depot_stock_balance.store_id==store_id) & (db.sm_depot_stock_balance.item_id==item_id)& (db.sm_depot_stock_balance.batch_id==batch_id)).select(db.sm_depot_stock_balance.id,db.sm_depot_stock_balance.block_qty,limitby=(0,1))
                    if stockRows:                        
                        block_qty=stockRows[0].block_qty
                                                
                        newBlockQty=block_qty-(quantity+bonus_qty)
                        if newBlockQty<0:
                            newBlockQty=0    
                              
                        stockRows[0].update_record(block_qty=newBlockQty)
                
                #----------------
                db((db.sm_invoice.cid==c_id) & (db.sm_invoice.depot_id==req_depot)& (db.sm_invoice.sl==req_sl)& (db.sm_invoice.item_id==req_item)& (db.sm_invoice.id==rowid)).delete()            
                db((db.sm_invoice.cid==c_id) & (db.sm_invoice.depot_id==req_depot)& (db.sm_invoice.sl==req_sl)& (db.sm_invoice.bonus_qty>0)).delete()
                
                #change rate
                updateRecords1="update sm_invoice inv, sm_item itm set inv.actual_tp=itm.price,inv.actual_vat=itm.vat_amt,inv.price=itm.price,inv.item_vat=itm.vat_amt,inv.discount=0,inv.status='Draft',inv.batch_id='',inv.short_note='' where inv.cid='"+str(c_id)+"' and inv.depot_id='"+str(req_depot)+"' and inv.sl="+str(req_sl)+" and itm.cid='"+str(c_id)+"' and inv.item_id=itm.item_id"
                db.executesql(updateRecords1)
                
                #-------------
                db((db.sm_invoice_head.cid==c_id) & (db.sm_invoice_head.depot_id==req_depot)& (db.sm_invoice_head.sl==req_sl)).update(discount=0,status='Draft',client_limit_over=0,empty_batch_flag=1)
                
                duplicateCheck=True
                session.flash='Item deleted successfully!'
                
            #-------------- delete duplicate row item
            if duplicateCheck==True:
                duplicateList=[]
                duplicatRows=db((db.sm_invoice.cid==c_id)& (db.sm_invoice.depot_id==req_depot) & (db.sm_invoice.sl==req_sl)).select(db.sm_invoice.item_id,db.sm_invoice.item_id.count(),db.sm_invoice.quantity.sum(),groupby=db.sm_invoice.item_id)
                for dupRow in duplicatRows:            
                    if int(dupRow[db.sm_invoice.item_id.count()])>1:
                        dupItemId=str(dupRow.sm_invoice.item_id)
                        dupItemQty=int(dupRow[db.sm_invoice.quantity.sum()])                
                        duplicateList.append({'item_id':dupItemId,'totalQty':dupItemQty})                
                
                if len(duplicateList)>0:
                    for i in range(len(duplicateList)):
                        dupItemID=duplicateList[i]['item_id']
                        dupItemQnty=duplicateList[i]['totalQty']
                        
                        updatedFlag=0
                        dupRows=db((db.sm_invoice.cid==c_id)& (db.sm_invoice.depot_id==req_depot) & (db.sm_invoice.sl==req_sl) & (db.sm_invoice.item_id==dupItemID)).select(db.sm_invoice.id,orderby=db.sm_invoice.id)
                        for dupRow in dupRows:
                            if updatedFlag==0:
                                dupRow.update_record(quantity=dupItemQnty)                                
                                updatedFlag=1
                            else:                            
                                dupRow.delete_record()
                #end duplicate row item
            
            
            #---------------------
            autDelCronRows[0].update_record(auto_del_cron_flag=0)
            db.commit()
            #--------------
    
    elif btn_delete_empty_batch:
        delete_check=request.vars.delete_check
        if delete_check!='YES':
            session.flash='Required checked confirmation'
        else:
            #--------------------------- chcek stock cron flag
            autDelCronRows=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==req_depot)&(db.sm_depot.auto_del_cron_flag==0)).select(db.sm_depot.id,db.sm_depot.cid,limitby=(0,1))
            if not autDelCronRows:
                session.flash='One process running, please try again'
            else:
                autDelCronRows[0].update_record(auto_del_cron_flag=1)
                #---------------------
                duplicateCheck=False
                
                countRecords=db((db.sm_invoice.cid==c_id)& (db.sm_invoice.depot_id==req_depot) & (db.sm_invoice.sl==req_sl)).count()
                if int(countRecords)==1:
                    session.flash='At least one item needs in an invoice!'
                else:
    #                 invRows=db((db.sm_invoice.cid==c_id)& (db.sm_invoice.depot_id==req_depot) & (db.sm_invoice.sl==req_sl) & (db.sm_invoice.status=='Submitted') & (db.sm_invoice.batch_id=='')).select(db.sm_invoice.id,limitby=(0,1))
    #                 if not invRows:
    #                     session.flash='Available stock processed successfully, empty batch not available'                    
    #                 else:
                    invoiceRows=db((db.sm_invoice.cid==c_id)& (db.sm_invoice.depot_id==req_depot) & (db.sm_invoice.sl==req_sl) & (db.sm_invoice.status=='Submitted') & (db.sm_invoice.batch_id!='')).select(db.sm_invoice.store_id,db.sm_invoice.item_id,db.sm_invoice.batch_id,db.sm_invoice.quantity,db.sm_invoice.bonus_qty)
                    for invRow in invoiceRows:
                        store_id=invRow.store_id
                        item_id=invRow.item_id
                        batch_id=invRow.batch_id
                        quantity=invRow.quantity
                        bonus_qty=invRow.bonus_qty
                        
                        stockRows=db((db.sm_depot_stock_balance.cid==c_id)& (db.sm_depot_stock_balance.depot_id==req_depot) & (db.sm_depot_stock_balance.store_id==store_id) & (db.sm_depot_stock_balance.item_id==item_id)& (db.sm_depot_stock_balance.batch_id==batch_id)).select(db.sm_depot_stock_balance.id,db.sm_depot_stock_balance.block_qty,limitby=(0,1))
                        if stockRows:
                            block_qty=stockRows[0].block_qty
                            
                            newBlockQty=block_qty-(quantity+bonus_qty)
                            if newBlockQty<0:
                                newBlockQty=0    
                                
                            stockRows[0].update_record(block_qty=newBlockQty)
                            
                    #----------------
                    db((db.sm_invoice.cid==c_id) & (db.sm_invoice.depot_id==req_depot)& (db.sm_invoice.sl==req_sl) & (db.sm_invoice.batch_id=='')).delete()  
                    db((db.sm_invoice.cid==c_id) & (db.sm_invoice.depot_id==req_depot)& (db.sm_invoice.sl==req_sl)& (db.sm_invoice.bonus_qty>0)).delete()
                    
                    #change rate
                    updateRecords1="update sm_invoice inv, sm_item itm set inv.actual_tp=itm.price,inv.actual_vat=itm.vat_amt,inv.price=itm.price,inv.item_vat=itm.vat_amt,inv.discount=0,inv.status='Draft',inv.batch_id='',inv.short_note='' where inv.cid='"+str(c_id)+"' and inv.depot_id='"+str(req_depot)+"' and inv.sl="+str(req_sl)+" and itm.cid='"+str(c_id)+"' and inv.item_id=itm.item_id"
                    db.executesql(updateRecords1)
                    
                    #updateRecords="update sm_invoice set price=actual_tp,item_vat=actual_vat,discount=0,status='Draft',batch_id='',short_note='' where cid='"+str(c_id)+"' and depot_id='"+str(req_depot)+"' and sl="+str(req_sl)
                    #db.executesql(updateRecords)
                    #db((db.sm_invoice.cid==c_id) & (db.sm_invoice.depot_id==req_depot)& (db.sm_invoice.sl==req_sl)).update(discount=0,status='Draft',batch_id='',short_note='')
                    
                    db((db.sm_invoice_head.cid==c_id) & (db.sm_invoice_head.depot_id==req_depot)& (db.sm_invoice_head.sl==req_sl)).update(discount=0,status='Draft',client_limit_over=0,empty_batch_flag=1)
                    
                    duplicateCheck=True
                    session.flash='Deleted successfully all empty batches!'
                    
                #-------------- delete duplicate row item
                if duplicateCheck==True:
                    duplicateList=[]
                    duplicatRows=db((db.sm_invoice.cid==c_id)& (db.sm_invoice.depot_id==req_depot) & (db.sm_invoice.sl==req_sl)).select(db.sm_invoice.item_id,db.sm_invoice.item_id.count(),db.sm_invoice.quantity.sum(),groupby=db.sm_invoice.item_id)
                    for dupRow in duplicatRows:            
                        if int(dupRow[db.sm_invoice.item_id.count()])>1:
                            dupItemId=str(dupRow.sm_invoice.item_id)
                            dupItemQty=int(dupRow[db.sm_invoice.quantity.sum()])                
                            duplicateList.append({'item_id':dupItemId,'totalQty':dupItemQty})                
                    
                    if len(duplicateList)>0:
                        for i in range(len(duplicateList)):
                            dupItemID=duplicateList[i]['item_id']
                            dupItemQnty=duplicateList[i]['totalQty']
                            
                            updatedFlag=0
                            dupRows=db((db.sm_invoice.cid==c_id)& (db.sm_invoice.depot_id==req_depot) & (db.sm_invoice.sl==req_sl) & (db.sm_invoice.item_id==dupItemID)).select(db.sm_invoice.id,orderby=db.sm_invoice.id)
                            for dupRow in dupRows:
                                if updatedFlag==0:
                                    dupRow.update_record(quantity=dupItemQnty)                                
                                    updatedFlag=1
                                else:                            
                                    dupRow.delete_record()
                    #end duplicate row item
                
                  
                #---------------------
                autDelCronRows[0].update_record(auto_del_cron_flag=0)
                db.commit()
                #--------------
                       
    elif btn_qtyupdate:        
        batchIdVar='batch_id_update_'+str(req_item)+'_'+str(rowid)
        batchId=str(request.vars[batchIdVar]).strip().upper().split('|')[0]
        
        rowQty=request.vars.rowQty
        rowBonusQty=request.vars.rowBonusQty        
        
        try:
            rowQty=int(rowQty)
            if rowQty<0:
                rowQty=0
        except:
            rowQty=0
            
        try:
            rowBonusQty=int(rowBonusQty)
            if rowBonusQty<0:
                rowBonusQty=0
        except:
            rowBonusQty=0
            
        if (rowQty == 0 and rowBonusQty==0):
            session.flash='Required valid Quantity!'
        else:
            if (rowQty > 0 and rowBonusQty > 0):
                session.flash=' Required Only one (Qty/BonusQty) Quantity'
            else:
                newTotalQty=rowQty+rowBonusQty
                
                #--------------------------- chcek stock cron flag
                autDelCronRows=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==req_depot)&(db.sm_depot.auto_del_cron_flag==0)).select(db.sm_depot.id,db.sm_depot.cid,limitby=(0,1))
                if not autDelCronRows:
                    session.flash='One process running, please try again'
                else:
                    autDelCronRows[0].update_record(auto_del_cron_flag=1)
                    #---------------------
                                 
                    invoiceRows=db((db.sm_invoice.cid==c_id)& (db.sm_invoice.depot_id==req_depot) & (db.sm_invoice.sl==req_sl)& (db.sm_invoice.item_id==req_item)& (db.sm_invoice.id==rowid)).select(db.sm_invoice.store_id,db.sm_invoice.item_id,db.sm_invoice.batch_id,db.sm_invoice.quantity,db.sm_invoice.bonus_qty,limitby=(0,1))
                    if not invoiceRows:
                        session.flash='Invalid request'
                    else:
                        store_id=invoiceRows[0].store_id
                        item_id=invoiceRows[0].item_id
                        batch_id=invoiceRows[0].batch_id
                        item_quantity=invoiceRows[0].quantity
                        bonus_qty=invoiceRows[0].bonus_qty
                        
                        oldTotalQty=item_quantity+bonus_qty
                        
                        duplicateCheck=False
                        
                        if newTotalQty!=oldTotalQty:#if qty change then blocked qty free, bonus qty delete,status Draft
                            
                            invRows=db((db.sm_invoice.cid==c_id)& (db.sm_invoice.depot_id==req_depot) & (db.sm_invoice.sl==req_sl) & (db.sm_invoice.status=='Submitted') & (db.sm_invoice.batch_id!='')).select(db.sm_invoice.store_id,db.sm_invoice.item_id,db.sm_invoice.batch_id,db.sm_invoice.quantity,db.sm_invoice.bonus_qty)
                            for invRow in invRows:
                                store_ID=invRow.store_id
                                item_ID=invRow.item_id
                                batch_ID=invRow.batch_id
                                inv_quantity=invRow.quantity
                                inv_bonus_qty=invRow.bonus_qty
                                
                                stockRows=db((db.sm_depot_stock_balance.cid==c_id)& (db.sm_depot_stock_balance.depot_id==req_depot) & (db.sm_depot_stock_balance.store_id==store_ID) & (db.sm_depot_stock_balance.item_id==item_ID)& (db.sm_depot_stock_balance.batch_id==batch_ID)).select(db.sm_depot_stock_balance.id,db.sm_depot_stock_balance.block_qty,limitby=(0,1))
                                if stockRows:                        
                                    block_qty=stockRows[0].block_qty
                                                     
                                    newBlockQty=block_qty-(inv_quantity+inv_bonus_qty)
                                    if newBlockQty<0:
                                        newBlockQty=0    
                                          
                                    stockRows[0].update_record(block_qty=newBlockQty)
                            
                            #----------------
                            db((db.sm_invoice.cid==c_id) & (db.sm_invoice.depot_id==req_depot)& (db.sm_invoice.sl==req_sl)& (db.sm_invoice.item_id==req_item)& (db.sm_invoice.id==rowid)).update(quantity=rowQty,bonus_qty=rowBonusQty)
                            db((db.sm_invoice.cid==c_id) & (db.sm_invoice.depot_id==req_depot)& (db.sm_invoice.sl==req_sl)& (db.sm_invoice.bonus_qty>0)).delete()
                            
                            #change rate
                            updateRecords1="update sm_invoice inv, sm_item itm set inv.actual_tp=itm.price,inv.actual_vat=itm.vat_amt,inv.price=itm.price,inv.item_vat=itm.vat_amt,inv.discount=0,inv.status='Draft',inv.batch_id='',inv.short_note='' where inv.cid='"+str(c_id)+"' and inv.depot_id='"+str(req_depot)+"' and inv.sl="+str(req_sl)+" and itm.cid='"+str(c_id)+"' and inv.item_id=itm.item_id"
                            db.executesql(updateRecords1)
                
                            #updateRecords="update sm_invoice set price=actual_tp,item_vat=actual_vat,discount=0,status='Draft',batch_id='',short_note='' where cid='"+str(c_id)+"' and depot_id='"+str(req_depot)+"' and sl="+str(req_sl)
                            #db.executesql(updateRecords)
                            #db((db.sm_invoice.cid==c_id) & (db.sm_invoice.depot_id==req_depot)& (db.sm_invoice.sl==req_sl)).update(discount=0,status='Draft',batch_id='',short_note='')
                            
                            db((db.sm_invoice_head.cid==c_id) & (db.sm_invoice_head.depot_id==req_depot)& (db.sm_invoice_head.sl==req_sl)).update(discount=0,status='Draft',client_limit_over=0,empty_batch_flag=1)
                            
                            duplicateCheck=True
                            session.flash='Updated successfully!'
                            
                        else: # old and new stock same but batch difference   
                            if batch_id==batchId:
                                session.flash='Required changing'
                            else:
                                if batch_id=='' and batchId!='':#old blank and new batch
                                    itemBatchRows = db((db.sm_item_batch.cid == c_id) & (db.sm_item_batch.item_id == req_item) & (db.sm_item_batch.batch_id == batchId) & (db.sm_item_batch.expiary_date >= current_date)).select(db.sm_item_batch.item_id,limitby=(0,1))
                                    if not itemBatchRows:
                                        session.flash='Invalid Item Batch ID'                            
                                    else:
                                        stockRows=db((db.sm_depot_stock_balance.cid==c_id)& (db.sm_depot_stock_balance.depot_id==req_depot) & (db.sm_depot_stock_balance.store_id==store_id) & (db.sm_depot_stock_balance.item_id==item_id)& (db.sm_depot_stock_balance.batch_id==batchId)).select(db.sm_depot_stock_balance.id,db.sm_depot_stock_balance.quantity,db.sm_depot_stock_balance.block_qty,limitby=(0,1))
                                        if not stockRows:
                                            session.flash='Stock not available'
                                        else:
                                            quantity=stockRows[0].quantity
                                            block_qty=stockRows[0].block_qty
                                            availableQty=quantity-block_qty
                                            
                                            if newTotalQty>availableQty:
                                                session.flash='bQty not available, available Qty '+str(availableQty)
                                            else:                                    
                                                newBlockQty=block_qty+newTotalQty
                                                db((db.sm_invoice.cid==c_id)& (db.sm_invoice.depot_id==req_depot) & (db.sm_invoice.sl==req_sl)& (db.sm_invoice.item_id==req_item)& (db.sm_invoice.id==rowid)).update(batch_id=batchId,quantity=rowQty,bonus_qty=rowBonusQty)#,price=newRate,item_vat=newVat
                                                stockRows[0].update_record(block_qty=newBlockQty)
                                                
                                                oldStockRows=db((db.sm_depot_stock_balance.cid==c_id)& (db.sm_depot_stock_balance.depot_id==req_depot) & (db.sm_depot_stock_balance.store_id==store_id) & (db.sm_depot_stock_balance.item_id==item_id)& (db.sm_depot_stock_balance.batch_id==batch_id)).select(db.sm_depot_stock_balance.id,db.sm_depot_stock_balance.quantity,db.sm_depot_stock_balance.block_qty,limitby=(0,1))
                                                if oldStockRows:
                                                    block_qty=oldStockRows[0].block_qty                                            
                                                    oldNewBlockQty=block_qty-oldTotalQty
                                                    oldStockRows[0].update_record(block_qty=oldNewBlockQty)
                                                
                                                duplicateCheck=True
                                                session.flash='Updated successfully!'
                                
                                elif batch_id!='' and batchId=='':#old not blank but new blank                                
                                    oldStockRows=db((db.sm_depot_stock_balance.cid==c_id)& (db.sm_depot_stock_balance.depot_id==req_depot) & (db.sm_depot_stock_balance.store_id==store_id) & (db.sm_depot_stock_balance.item_id==item_id)& (db.sm_depot_stock_balance.batch_id==batch_id)).select(db.sm_depot_stock_balance.id,db.sm_depot_stock_balance.quantity,db.sm_depot_stock_balance.block_qty,limitby=(0,1))
                                    if oldStockRows:
                                        block_qty=oldStockRows[0].block_qty                                            
                                        oldNewBlockQty=block_qty-oldTotalQty
                                        db((db.sm_invoice.cid==c_id)& (db.sm_invoice.depot_id==req_depot) & (db.sm_invoice.sl==req_sl)& (db.sm_invoice.item_id==req_item)& (db.sm_invoice.id==rowid)).update(batch_id=batchId)#,quantity=rowQty,bonus_qty=rowBonusQty,price=newRate,item_vat=newVat
                                        oldStockRows[0].update_record(block_qty=oldNewBlockQty)
                                        duplicateCheck=True
                                        
                                    session.flash='Updated successfully!'
                                    
                                elif batch_id!='' and batchId!='':#old and new batch yes
                                    itemBatchRows = db((db.sm_item_batch.cid == c_id) & (db.sm_item_batch.item_id == req_item) & (db.sm_item_batch.batch_id == batchId) & (db.sm_item_batch.expiary_date >= current_date)).select(db.sm_item_batch.item_id,limitby=(0,1))
                                    if not itemBatchRows:
                                        session.flash='Invalid Item Batch ID'                            
                                    else:
                                        stockRows=db((db.sm_depot_stock_balance.cid==c_id)& (db.sm_depot_stock_balance.depot_id==req_depot) & (db.sm_depot_stock_balance.store_id==store_id) & (db.sm_depot_stock_balance.item_id==item_id)& (db.sm_depot_stock_balance.batch_id==batchId)).select(db.sm_depot_stock_balance.id,db.sm_depot_stock_balance.quantity,db.sm_depot_stock_balance.block_qty,limitby=(0,1))
                                        if not stockRows:
                                            session.flash='Stock not available'
                                        else:
                                            quantity=stockRows[0].quantity
                                            block_qty=stockRows[0].block_qty
                                            availableQty=quantity-block_qty
                                            
                                            if newTotalQty>availableQty:
                                                session.flash='bQty not available, available Qty '+str(availableQty)
                                            else:
                                                newBlockQty=block_qty+newTotalQty
                                                db((db.sm_invoice.cid==c_id)& (db.sm_invoice.depot_id==req_depot) & (db.sm_invoice.sl==req_sl)& (db.sm_invoice.item_id==req_item)& (db.sm_invoice.id==rowid)).update(batch_id=batchId)#,quantity=rowQty,bonus_qty=rowBonusQty,price=newRate,item_vat=newVat
                                                stockRows[0].update_record(block_qty=newBlockQty)
                                                
                                                oldStockRows=db((db.sm_depot_stock_balance.cid==c_id)& (db.sm_depot_stock_balance.depot_id==req_depot) & (db.sm_depot_stock_balance.store_id==store_id) & (db.sm_depot_stock_balance.item_id==item_id)& (db.sm_depot_stock_balance.batch_id==batch_id)).select(db.sm_depot_stock_balance.id,db.sm_depot_stock_balance.quantity,db.sm_depot_stock_balance.block_qty,limitby=(0,1))
                                                if oldStockRows:
                                                    block_qty=oldStockRows[0].block_qty                                            
                                                    oldNewBlockQty=block_qty-oldTotalQty
                                                    oldStockRows[0].update_record(block_qty=oldNewBlockQty)
                                                
                                                duplicateCheck=True
                                                session.flash='Updated successfully!'
                                
                                emptyBatchRow=db((db.sm_invoice.cid==c_id) & (db.sm_invoice.depot_id==req_depot)& (db.sm_invoice.sl==req_sl) & (db.sm_invoice.batch_id=='')).select(db.sm_invoice.id,limitby=(0,1))
                                if not emptyBatchRow:
                                    db((db.sm_invoice_head.cid==c_id) & (db.sm_invoice_head.depot_id==req_depot)& (db.sm_invoice_head.sl==req_sl)).update(empty_batch_flag=0)
                    
                    
                    #-------------- delete duplicate row item
                    if duplicateCheck==True:
                        duplicateList=[]
                        duplicatRows=db((db.sm_invoice.cid==c_id)& (db.sm_invoice.depot_id==req_depot) & (db.sm_invoice.sl==req_sl)).select(db.sm_invoice.item_id,db.sm_invoice.item_id.count(),db.sm_invoice.quantity.sum(),groupby=db.sm_invoice.item_id)
                        for dupRow in duplicatRows:            
                            if int(dupRow[db.sm_invoice.item_id.count()])>1:
                                dupItemId=str(dupRow.sm_invoice.item_id)
                                dupItemQty=int(dupRow[db.sm_invoice.quantity.sum()])                
                                duplicateList.append({'item_id':dupItemId,'totalQty':dupItemQty})                
                        if len(duplicateList)>0:
                            for i in range(len(duplicateList)):
                                dupItemID=duplicateList[i]['item_id']
                                dupItemQnty=duplicateList[i]['totalQty']
                                
                                updatedFlag=0
                                dupRows=db((db.sm_invoice.cid==c_id)& (db.sm_invoice.depot_id==req_depot) & (db.sm_invoice.sl==req_sl) & (db.sm_invoice.item_id==dupItemID)).select(db.sm_invoice.id,orderby=db.sm_invoice.id)
                                for dupRow in dupRows:
                                    if updatedFlag==0:
                                        dupRow.update_record(quantity=dupItemQnty)                                
                                        updatedFlag=1
                                    else:                            
                                        dupRow.delete_record()
                        #end duplicate row item
                    
                    #---------------------
                    autDelCronRows[0].update_record(auto_del_cron_flag=0)
                    db.commit()
                    #--------------
                               
    redirect(URL(c='order_invoice',f='invoice_generate',vars=dict(req_sl=req_sl,dptid=req_depot)))
    
    #  ---------------------
    return dict()


# Delete item if more than one item in a sl

def update_status_invoice():
    c_id=session.cid
    
    btn_post=request.vars.btn_post
    btn_cancel=request.vars.btn_cancel
    btn_blocked=request.vars.btn_blocked
    btn_free=request.vars.btn_free
    btn_hold=request.vars.btn_hold
    btn_unhold=request.vars.btn_unhold
    btn_reProcess=request.vars.btn_reProcess
    btn_apply_regDiscount=request.vars.btn_apply_regDiscount
    btn_acknowledge=request.vars.btn_acknowledge
    
    btn_delete_empty_batch=request.vars.btn_delete_empty_batch
    
    #-----for return
    btn_return=request.vars.btn_return
    #---
    
    req_depot=request.args(0)
    req_sl=request.args(1)  
    #req_date=request.args(2)  
    req_date=current_date
    ym_date=str(req_date)[0:7]+'-01'
    
    #----------------- INVOICE POST
    if btn_post:
        countRecords=db((db.sm_invoice.cid==c_id)& (db.sm_invoice.depot_id==req_depot) & (db.sm_invoice.sl==req_sl)).select(db.sm_invoice.d_man_id,db.sm_invoice.d_man_name,limitby=(0,1))
        if not countRecords:
            session.flash='At least one item needs in an invoice!'
        else:
            d_man_id=countRecords[0].d_man_id
            d_man_name=countRecords[0].d_man_name
            
            if not (ym_date=='' or ym_date==None):
                
                if d_man_id=='' or d_man_id==None:
                    session.flash='Required Delivery Man!'
                else:
                    batchIdrows=db((db.sm_invoice.cid==c_id)& (db.sm_invoice.depot_id==req_depot) & (db.sm_invoice.sl==req_sl) & (db.sm_invoice.batch_id=='')).select(db.sm_invoice.id,limitby=(0,1))
                    if batchIdrows:
                        session.flash = 'Required Batch ID for all Items'
                    else:
                        #--------------------------------
        #                strData=str(c_id)+'<fdfd>'+str(req_depot)+'<fdfd>delivery<fdfd>'+ym_date+'<fdfd>'
                        resStr=''                    
                        discount=0
                        totalAmount=0
                        total_tp_amount=0
                        total_vat_amount=0
                        sp_discount=0
                        actual_total_tp=0
                        
                        hRows=db((db.sm_invoice_head.cid==c_id)& (db.sm_invoice_head.depot_id==req_depot) & (db.sm_invoice_head.sl==req_sl)).select(db.sm_invoice_head.store_id,db.sm_invoice_head.client_id,db.sm_invoice_head.discount,db.sm_invoice_head.acknowledge_flag,limitby=(0,1))
                        store_id=hRows[0].store_id
                        client_id=hRows[0].client_id
                        discount=float(hRows[0].discount)
                        acknowledge_flag=hRows[0].acknowledge_flag
                        
                        if acknowledge_flag==1:
                            session.flash = 'Required Client Credit Acknowledgment'
                        else:                            
                            #--------------------------- chcek stock cron flag
                            autDelCronRows=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==req_depot)&(db.sm_depot.auto_del_cron_flag==0)).select(db.sm_depot.id,db.sm_depot.cid,limitby=(0,1))
                            if not autDelCronRows:
                                session.flash='One process running, please try again'
                            else:
                                autDelCronRows[0].update_record(auto_del_cron_flag=1)
                                #---------------------
                                
                                itemStrForQty=''  
                                diffRecords="select inv.item_id as item_id from sm_depot_stock_balance dsb,(select invtemp.cid as cid,invtemp.depot_id as depot_id,invtemp.sl as sl,invtemp.store_id as store_id,invtemp.item_id as item_id,invtemp.batch_id as batch_id,sum(invtemp.quantity) as quantity,sum(invtemp.bonus_qty) as bonus_qty from sm_invoice invtemp where (invtemp.cid='"+str(c_id)+"' and invtemp.depot_id='"+str(req_depot)+"' and invtemp.sl="+str(req_sl)+" and invtemp.store_id='"+str(store_id)+"') group by invtemp.cid,invtemp.depot_id,invtemp.sl,invtemp.store_id,invtemp.item_id,invtemp.batch_id) inv  where (inv.cid='"+str(c_id)+"' and inv.depot_id='"+str(req_depot)+"' and inv.sl="+str(req_sl)+" and inv.store_id='"+str(store_id)+"' and dsb.cid='"+str(c_id)+"' and dsb.depot_id='"+str(req_depot)+"' and dsb.store_id='"+str(store_id)+"' and inv.item_id=dsb.item_id and inv.batch_id=dsb.batch_id and (dsb.quantity)<(inv.quantity+inv.bonus_qty))"
                                
                                #diffRecords="select inv.item_id as item_id from sm_depot_stock_balance dsb,sm_invoice inv  where (inv.cid='"+str(c_id)+"' and inv.depot_id='"+str(req_depot)+"' and inv.sl="+str(req_sl)+" and dsb.cid='"+str(c_id)+"' and dsb.depot_id='"+str(req_depot)+"' and inv.store_id=dsb.store_id and inv.item_id=dsb.item_id and inv.batch_id=dsb.batch_id and (dsb.quantity-dsb.block_qty)<inv.quantity+inv.bonus_qty)"
                                diffRowsList=db.executesql(diffRecords,as_dict=True)
                                for i in range(len(diffRowsList)):
                                    diffDictData=diffRowsList[i]
                                    if itemStrForQty=='':
                                        itemStrForQty=diffDictData['item_id']
                                    else:
                                        itemStrForQty+=','+diffDictData['item_id']
                                        
                                if itemStrForQty!='':
                                    session.flash='Quantity not available for item ID '+str(itemStrForQty)                        
                                else:
                                    rows=db((db.sm_invoice.cid==c_id)& (db.sm_invoice.depot_id==req_depot) & (db.sm_invoice.sl==req_sl)).select(db.sm_invoice.id,db.sm_invoice.actual_tp,db.sm_invoice.quantity,db.sm_invoice.price,db.sm_invoice.item_vat)
                                    for row in rows:
                                        actual_tp=float(row.actual_tp)
                                        quantity=int(row.quantity)
                                        price=float(row.price)
                                        item_vat=float(row.item_vat)                        
                                        
                                        actual_total_tp+=round(quantity*actual_tp,6)
                                        
                                        total_tp_amount+=round(quantity*price,6)
                                        total_vat_amount+=round(quantity*item_vat,6)
                                        
                                        spDiscount=(actual_tp-price)*quantity
                                        #if spDiscount>0:                                        
                                        sp_discount+=spDiscount                                            
                                        row.update_record(sp_discount_item=spDiscount)
                                        
                                    #-------------
                                    totalAmount=round((round(total_tp_amount,2)+round(total_vat_amount,2)-round(discount,2)),2) #with vat
                                    total_vat_amount=round(total_vat_amount,2)
                                    sp_discount=round(sp_discount,2)
                                    actual_total_tp=round(actual_total_tp,2)
                                    
                                    if session.ledgerCreate=='YES':
                                        strData=str(c_id)+'<fdfd>DELIVERY<fdfd>'+str(req_sl)+'<fdfd>'+str(datetime_fixed)+'<fdfd>'+str(req_depot)+'-'+str(req_sl)+'<fdfd>DPT-'+str(req_depot)+'<fdfd>CLT-'+str(client_id)+'<fdfd>'+str(totalAmount)
                                        resStr=set_balance_transaction(strData)
                                        resStrList=resStr.split('<sep>',resStr.count('<sep>'))
                                        flag=resStrList[0]
                                        msg=resStrList[1]
                                    else:
                                        flag='True'
                                        msg='Success'
                                        
                                    if flag=='True':
                                        #Update status of head and detail
                                        session.flash=msg
                                        db((db.sm_invoice.cid==c_id)& (db.sm_invoice.depot_id==req_depot) & (db.sm_invoice.sl==req_sl)).update(status='Invoiced',invoice_date=req_date,invoice_ym_date=ym_date)
                                        db((db.sm_invoice_head.cid==c_id)& (db.sm_invoice_head.depot_id==req_depot) & (db.sm_invoice_head.sl==req_sl)).update(status='Invoiced',invoice_date=req_date,invoice_ym_date=ym_date,actual_total_tp=actual_total_tp,total_amount=totalAmount,vat_total_amount=total_vat_amount,sp_discount=sp_discount,empty_batch_flag=0)
                                        
                                        # call update depot stock (type,cid,depotid,sl)
                                        update_depot_stock('DELIVERY',c_id,req_depot,req_sl)
                                        
                                #---------------------
                                autDelCronRows[0].update_record(auto_del_cron_flag=0)
                                db.commit()
                                #--------------
                                
            else:
                session.flash='Date format error'
        
        redirect(URL(c='order_invoice',f='invoice_generate',vars=dict(req_sl=req_sl,dptid=req_depot)))
    
    #-------------- INVOICE CANCEL
    elif btn_cancel:
        #--------------------------- chcek stock cron flag
        autDelCronRows=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==req_depot)&(db.sm_depot.auto_del_cron_flag==0)).select(db.sm_depot.id,db.sm_depot.cid,limitby=(0,1))
        if not autDelCronRows:
            session.flash='One process running, please try again'
        else:
            autDelCronRows[0].update_record(auto_del_cron_flag=1)
            #---------------------
            
            countRecords=db((db.sm_invoice.cid==c_id)& (db.sm_invoice.depot_id==req_depot) & (db.sm_invoice.sl==req_sl)).count()
            if int(countRecords)==0:
                session.flash='At least one item needs in an invoice!'
            else:
                invoiceRows=db((db.sm_invoice.cid==c_id)& (db.sm_invoice.depot_id==req_depot) & (db.sm_invoice.sl==req_sl)).select(db.sm_invoice.store_id,db.sm_invoice.item_id,db.sm_invoice.batch_id,db.sm_invoice.quantity,db.sm_invoice.bonus_qty)
                for invRow in invoiceRows:
                    store_id=invRow.store_id
                    item_id=invRow.item_id
                    batch_id=invRow.batch_id
                    quantity=invRow.quantity
                    bonus_qty=invRow.bonus_qty
                    
                    if batch_id!='':
                        stockRows=db((db.sm_depot_stock_balance.cid==c_id)& (db.sm_depot_stock_balance.depot_id==req_depot) & (db.sm_depot_stock_balance.store_id==store_id) & (db.sm_depot_stock_balance.item_id==item_id)& (db.sm_depot_stock_balance.batch_id==batch_id)).select(db.sm_depot_stock_balance.id,db.sm_depot_stock_balance.block_qty,limitby=(0,1))
                        if stockRows:                        
                            block_qty=stockRows[0].block_qty
                                                    
                            newBlockQty=block_qty-(quantity+bonus_qty)
                            if newBlockQty<0:
                                newBlockQty=0    
                                                    
                            stockRows[0].update_record(block_qty=newBlockQty)
                
                db((db.sm_invoice.cid==c_id)& (db.sm_invoice.depot_id==req_depot) & (db.sm_invoice.sl==req_sl)).update(status='Cancelled')
                db((db.sm_invoice_head.cid==c_id)& (db.sm_invoice_head.depot_id==req_depot) & (db.sm_invoice_head.sl==req_sl)).update(status='Cancelled')
                
                session.flash='Cancelled Successfully'
            
            #---------------------
            autDelCronRows[0].update_record(auto_del_cron_flag=0)
            db.commit()
            #--------------
            
        redirect(URL(c='order_invoice',f='invoice_generate',vars=dict(req_sl=req_sl,dptid=req_depot)))
    
    #------------------ INVOICE BLOCKED
    elif btn_blocked:
        countRecords=db((db.sm_invoice.cid==c_id)& (db.sm_invoice.depot_id==req_depot) & (db.sm_invoice.sl==req_sl)).count()
        if int(countRecords)==0:
            session.flash='At least one item needs in an order!'
        else:
            db((db.sm_invoice.cid==c_id)& (db.sm_invoice.depot_id==req_depot) & (db.sm_invoice.sl==req_sl)).update(status='Blocked')
            db((db.sm_invoice_head.cid==c_id)& (db.sm_invoice_head.depot_id==req_depot) & (db.sm_invoice_head.sl==req_sl)).update(status='Blocked')
            session.flash='Blocked successfully'
            
        redirect(URL(c='order_invoice',f='invoice_generate',vars=dict(req_sl=req_sl,dptid=req_depot)))
    
    #------------------ INVOCIE FREE/UNBLOCKED
    elif btn_free:
        countRecords=db((db.sm_invoice.cid==c_id)& (db.sm_invoice.depot_id==req_depot) & (db.sm_invoice.sl==req_sl)).count()
        if int(countRecords)==0:
            session.flash='At least one item needs in an order!'
        else:
            db((db.sm_invoice.cid==c_id)& (db.sm_invoice.depot_id==req_depot) & (db.sm_invoice.sl==req_sl)).update(status='Submitted')
            db((db.sm_invoice_head.cid==c_id)& (db.sm_invoice_head.depot_id==req_depot) & (db.sm_invoice_head.sl==req_sl)).update(status='Submitted')
            session.flash='Free successfully'
            
        redirect(URL(c='order_invoice',f='invoice_generate',vars=dict(req_sl=req_sl,dptid=req_depot)))
    
    #------------------ Acknowledge
    elif btn_acknowledge:
        countRecords=db((db.sm_invoice.cid==c_id)& (db.sm_invoice.depot_id==req_depot) & (db.sm_invoice.sl==req_sl)).count()
        if int(countRecords)==0:
            session.flash='At least one item needs in an order!'
        else:
            creditNotesRow=db((db.sm_invoice_head.cid==c_id)& (db.sm_invoice_head.depot_id==req_depot) & (db.sm_invoice_head.sl==req_sl) & (db.sm_invoice_head.credit_note=='')).select(db.sm_invoice_head.credit_note,limitby=(0,1))
            if creditNotesRow:
                session.flash='Required Credit Type'
            else:
                db((db.sm_invoice_head.cid==c_id)& (db.sm_invoice_head.depot_id==req_depot) & (db.sm_invoice_head.sl==req_sl)).update(acknowledge_flag=0)
                session.flash='Acknowledged successfully'
                
        redirect(URL(c='order_invoice',f='invoice_generate',vars=dict(req_sl=req_sl,dptid=req_depot)))
        
    elif btn_return:
        check_return=request.vars.check_return
        if check_return!='YES': 
            session.flash='Check Confirmation required'
            redirect(URL(c='order_invoice',f='invoice_generate',vars=dict(req_sl=req_sl,dptid=req_depot)))
        else:
            redirect(URL(c='order_invoice',f='return_add',vars=dict(btn_import_req='Yes',sl=0,invoice_sl=req_sl,dptid=req_depot,ret_reason='EXCHANGED',return_date=current_date,from_invoice_flag='Yes')))
            
    #-------------- INVOICE Hold
    elif btn_hold:
        #--------------------------- chcek stock cron flag
        autDelCronRows=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==req_depot)&(db.sm_depot.auto_del_cron_flag==0)).select(db.sm_depot.id,db.sm_depot.cid,limitby=(0,1))
        if not autDelCronRows:
            session.flash='One process running, please try again'
        else:
            autDelCronRows[0].update_record(auto_del_cron_flag=1)
            #---------------------
            
            invoiceRows=db((db.sm_invoice.cid==c_id)& (db.sm_invoice.depot_id==req_depot) & (db.sm_invoice.sl==req_sl) & (db.sm_invoice.batch_id!='')).select(db.sm_invoice.id,db.sm_invoice.store_id,db.sm_invoice.item_id,db.sm_invoice.batch_id,db.sm_invoice.quantity,db.sm_invoice.bonus_qty)
            if not invoiceRows:
                session.flash='Already Hold (Batch ID not available in this voucher)'
            else:
                for invRow in invoiceRows:
                    store_id=invRow.store_id
                    item_id=invRow.item_id
                    batch_id=invRow.batch_id
                    quantity=invRow.quantity
                    bonus_qty=invRow.bonus_qty
                    
                    stockRows=db((db.sm_depot_stock_balance.cid==c_id)& (db.sm_depot_stock_balance.depot_id==req_depot) & (db.sm_depot_stock_balance.store_id==store_id) & (db.sm_depot_stock_balance.item_id==item_id)& (db.sm_depot_stock_balance.batch_id==batch_id)).select(db.sm_depot_stock_balance.id,db.sm_depot_stock_balance.block_qty,limitby=(0,1))
                    if stockRows:                        
                        block_qty=stockRows[0].block_qty
                        
                        newBlockQty=block_qty-(quantity+bonus_qty)
                        if newBlockQty<0:
                            newBlockQty=0
                            
                        stockRows[0].update_record(block_qty=newBlockQty)
                        
                        invRow.update_record(batch_id='')
                        
                db((db.sm_invoice_head.cid==c_id)& (db.sm_invoice_head.depot_id==req_depot) & (db.sm_invoice_head.sl==req_sl)).update(empty_batch_flag=1)
                
                session.flash='Hold (Batch Cleaned) Successfully'
                
            #---------------------
            autDelCronRows[0].update_record(auto_del_cron_flag=0)
            db.commit()
            #--------------
        
        redirect(URL(c='order_invoice',f='invoice_generate',vars=dict(req_sl=req_sl,dptid=req_depot)))
        
    #-------------- INVOICE Un Hold (apply stock)
    elif btn_unhold: #or btn_delete_empty_batch
        #--------------------------- chcek stock cron flag
        autDelCronRows=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==req_depot)&(db.sm_depot.auto_del_cron_flag==0)).select(db.sm_depot.id,db.sm_depot.cid,limitby=(0,1))
        if not autDelCronRows:
            session.flash='One process running, please try again'
            redirect(URL(c='order_invoice',f='invoice_generate',vars=dict(req_sl=req_sl,dptid=req_depot)))
        else:
            autDelCronRows[0].update_record(auto_del_cron_flag=1)
            #---------------------
            
            countRecords=db((db.sm_invoice.cid==c_id)& (db.sm_invoice.depot_id==req_depot) & (db.sm_invoice.sl==req_sl) & (db.sm_invoice.batch_id=='')).count()
            if int(countRecords)==0:
                session.flash='At least one item batch needs empty in this voucher'
                #redirect(URL(c='order_invoice',f='invoice_generate',vars=dict(req_sl=req_sl,dptid=req_depot)))
            else:                
                #------------------- for btn_delete_empty_batch empty all batch id
#                 if btn_delete_empty_batch:
#                     invRows=db((db.sm_invoice.cid==c_id)& (db.sm_invoice.depot_id==req_depot) & (db.sm_invoice.sl==req_sl) & (db.sm_invoice.status=='Submitted') & (db.sm_invoice.batch_id!='')).select(db.sm_invoice.id,db.sm_invoice.store_id,db.sm_invoice.item_id,db.sm_invoice.batch_id,db.sm_invoice.quantity,db.sm_invoice.bonus_qty)
#                     for invoiceRow in invRows:
#                         store_id=invoiceRow.store_id
#                         item_id=invoiceRow.item_id
#                         batch_id=invoiceRow.batch_id
#                         quantity=invoiceRow.quantity
#                         bonus_qty=invoiceRow.bonus_qty
#                         
#                         stockRows=db((db.sm_depot_stock_balance.cid==c_id)& (db.sm_depot_stock_balance.depot_id==req_depot) & (db.sm_depot_stock_balance.store_id==store_id) & (db.sm_depot_stock_balance.item_id==item_id)& (db.sm_depot_stock_balance.batch_id==batch_id)).select(db.sm_depot_stock_balance.id,db.sm_depot_stock_balance.block_qty,limitby=(0,1))
#                         if stockRows:
#                             block_qty=stockRows[0].block_qty
#                             
#                             newBlockQty=block_qty-(quantity+bonus_qty)
#                             if newBlockQty<0:
#                                 newBlockQty=0    
#                                 
#                             stockRows[0].update_record(block_qty=newBlockQty)
#                             invoiceRow.update_record(batch_id='')
#                 else:
#                     pass
                
                #------------------------------ Apply stock
                totalAmountTP=0
                totalAmountVat=0
                emptyBatchFlag=0
                detailList=[]
                invoiceRows=db((db.sm_invoice.cid==c_id)& (db.sm_invoice.depot_id==req_depot) & (db.sm_invoice.sl==req_sl)).select(db.sm_invoice.ALL,orderby=db.sm_invoice.item_id)
                for invRow in invoiceRows:
                    depot_name=invRow.depot_name
                    store_name=invRow.store_name
                    payment_mode=invRow.payment_mode
                    d_man_id=invRow.d_man_id
                    d_man_name=invRow.d_man_name                
                    item_name=invRow.item_name
                    category_id=invRow.category_id
                    price=invRow.price
                    item_vat=invRow.item_vat
                    req_note=invRow.note
                    short_note=invRow.short_note
                    status=invRow.status
                    
                    item_unit=invRow.item_unit
                    item_carton=invRow.item_carton
                    actual_tp=invRow.actual_tp
                    actual_vat=invRow.actual_vat
                    market_id=invRow.market_id
                    market_name=invRow.market_name
                    
                    promotion_type=invRow.promotion_type
                    bonus_applied_on_qty=invRow.bonus_applied_on_qty
                    circular_no=invRow.circular_no
                    
                    order_sl=invRow.order_sl
                    order_datetime=invRow.order_datetime
                    delivery_date=invRow.delivery_date
                    client_id=invRow.client_id
                    client_name=invRow.client_name
                    rep_id=invRow.rep_id
                    rep_name=invRow.rep_name
                    area_id=invRow.area_id
                    area_name=invRow.area_name
                    
                    level0_id=invRow.level0_id
                    level0_name=invRow.level0_name
                    level1_id=invRow.level1_id
                    level1_name=invRow.level1_name
                    level2_id=invRow.level2_id
                    level2_name=invRow.level2_name
                    level3_id=invRow.level3_id
                    level3_name=invRow.level3_name
                    
                    rep_name=invRow.rep_name
                    invoice_media=invRow.invoice_media
                    ym_date=invRow.ym_date
                    
                    discount=invRow.discount
                    
                    store_id=invRow.store_id
                    item_id=invRow.item_id
                    
                    item_batch_id=invRow.batch_id
                    item_qty_value=invRow.quantity
                    bonus_qty=invRow.bonus_qty
                    
                    totalAmountTP+=round(item_qty_value*price,6)
                    totalAmountVat+=round(item_qty_value*item_vat,6)
                    
                    if item_batch_id!='':
                        continue
                    
                    firstBatchFlag=0
                    
                    
                    #Quantity part
                    if item_qty_value>0:
                        
                        #------------ set batch id after checking stock                        
                        requestBaseQty=item_qty_value
                        
                        stockRows=db((db.sm_depot_stock_balance.cid==c_id)& (db.sm_depot_stock_balance.depot_id==req_depot) & (db.sm_depot_stock_balance.store_id==store_id) & (db.sm_depot_stock_balance.item_id==item_id) & (db.sm_depot_stock_balance.quantity>db.sm_depot_stock_balance.block_qty)).select(db.sm_depot_stock_balance.id,db.sm_depot_stock_balance.batch_id,db.sm_depot_stock_balance.quantity,db.sm_depot_stock_balance.block_qty,orderby=db.sm_depot_stock_balance.expiary_date)
                        for stockRow in stockRows:
                            batch_id=stockRow.batch_id
                            quantity=stockRow.quantity
                            block_qty=stockRow.block_qty
                            availableQty=quantity-block_qty
                            
                            if requestBaseQty<=availableQty:
                                newBlockQty=block_qty+requestBaseQty
                                newBaseQty=requestBaseQty
                                requestBaseQty=0
                                
                                if firstBatchFlag==0:
                                    invRow.update_record(batch_id=batch_id,quantity=newBaseQty,bonus_qty=0)
                                else:
                                    detailDict={'cid':c_id,'depot_id':req_depot,'depot_name':depot_name,'sl':req_sl,'store_id':store_id,'store_name':store_name,'order_sl':order_sl,'order_datetime':order_datetime,'delivery_date':delivery_date,'client_id':client_id,'client_name':client_name,'rep_id':rep_id,'rep_name':rep_name,'market_id':market_id,'market_name':market_name,'area_id':area_id,'area_name':area_name,'level0_id':level0_id,'level0_name':level0_name,'level1_id':level1_id,'level1_name':level1_name,'level2_id':level2_id,'level2_name':level2_name,'level3_id':level3_id,'level3_name':level3_name,'invoice_media':invoice_media,'device_user_agent':'','ip_ref':'','ym_date':ym_date,'discount':discount,'payment_mode':payment_mode,'d_man_id':d_man_id,'d_man_name':d_man_name,'item_id':item_id,'item_name':item_name,'batch_id':batch_id,'category_id':category_id,'actual_tp':actual_tp,'actual_vat':actual_vat,'quantity':newBaseQty,'bonus_qty':0,'price':price,'item_vat':item_vat,'sp_discount_item':0,'item_unit':item_unit,'item_carton':item_carton,'promotion_type':promotion_type,'bonus_applied_on_qty':bonus_applied_on_qty,'circular_no':circular_no,'note':req_note,'short_note':short_note,'status':'Submitted'}
                                    detailList.append(detailDict)
                                    
                                stockRow.update_record(block_qty=newBlockQty) 
                                firstBatchFlag=1
                                break
                            else:
                                newBlockQty=block_qty+availableQty
                                newBaseQty=availableQty
                                requestBaseQty=requestBaseQty-availableQty
                                
                                if firstBatchFlag==0:
                                    invRow.update_record(batch_id=batch_id,quantity=newBaseQty,bonus_qty=0)
                                else:
                                    detailDict={'cid':c_id,'depot_id':req_depot,'depot_name':depot_name,'sl':req_sl,'store_id':store_id,'store_name':store_name,'order_sl':order_sl,'order_datetime':order_datetime,'delivery_date':delivery_date,'client_id':client_id,'client_name':client_name,'rep_id':rep_id,'rep_name':rep_name,'market_id':market_id,'market_name':market_name,'area_id':area_id,'area_name':area_name,'level0_id':level0_id,'level0_name':level0_name,'level1_id':level1_id,'level1_name':level1_name,'level2_id':level2_id,'level2_name':level2_name,'level3_id':level3_id,'level3_name':level3_name,'invoice_media':invoice_media,'device_user_agent':'','ip_ref':'','ym_date':ym_date,'discount':discount,'payment_mode':payment_mode,'d_man_id':d_man_id,'d_man_name':d_man_name,'item_id':item_id,'item_name':item_name,'batch_id':batch_id,'category_id':category_id,'actual_tp':actual_tp,'actual_vat':actual_vat,'quantity':newBaseQty,'bonus_qty':0,'price':price,'item_vat':item_vat,'sp_discount_item':0,'item_unit':item_unit,'item_carton':item_carton,'promotion_type':promotion_type,'bonus_applied_on_qty':bonus_applied_on_qty,'circular_no':circular_no,'note':req_note,'short_note':short_note,'status':'Submitted'}
                                    detailList.append(detailDict)
                                    
                                stockRow.update_record(block_qty=newBlockQty) 
                                firstBatchFlag=1                        
                                #--------------
                                
                        #--------------
                        if requestBaseQty>0:
                            emptyBatchFlag=1
                            if firstBatchFlag==1:                  
                                detailDict={'cid':c_id,'depot_id':req_depot,'depot_name':depot_name,'sl':req_sl,'store_id':store_id,'store_name':store_name,'order_sl':order_sl,'order_datetime':order_datetime,'delivery_date':delivery_date,'client_id':client_id,'client_name':client_name,'rep_id':rep_id,'rep_name':rep_name,'market_id':market_id,'market_name':market_name,'area_id':area_id,'area_name':area_name,'level0_id':level0_id,'level0_name':level0_name,'level1_id':level1_id,'level1_name':level1_name,'level2_id':level2_id,'level2_name':level2_name,'level3_id':level3_id,'level3_name':level3_name,'invoice_media':invoice_media,'device_user_agent':'','ip_ref':'','ym_date':ym_date,'discount':discount,'payment_mode':payment_mode,'d_man_id':d_man_id,'d_man_name':d_man_name,'item_id':item_id,'item_name':item_name,'batch_id':'','category_id':category_id,'actual_tp':actual_tp,'actual_vat':actual_vat,'quantity':requestBaseQty,'bonus_qty':0,'price':price,'item_vat':item_vat,'sp_discount_item':0,'item_unit':item_unit,'item_carton':item_carton,'promotion_type':promotion_type,'bonus_applied_on_qty':bonus_applied_on_qty,'circular_no':circular_no,'note':req_note,'short_note':short_note,'status':'Submitted'}
                                detailList.append(detailDict)
                    
                    #-------- Bonus quantity part
                    if bonus_qty>0:                        
                        #------------ set batch id after checking stock                    
                        requestBaseQty=bonus_qty
                        
                        stockRows=db((db.sm_depot_stock_balance.cid==c_id)& (db.sm_depot_stock_balance.depot_id==req_depot) & (db.sm_depot_stock_balance.store_id==store_id) & (db.sm_depot_stock_balance.item_id==item_id) & (db.sm_depot_stock_balance.quantity>db.sm_depot_stock_balance.block_qty)).select(db.sm_depot_stock_balance.id,db.sm_depot_stock_balance.batch_id,db.sm_depot_stock_balance.quantity,db.sm_depot_stock_balance.block_qty,orderby=db.sm_depot_stock_balance.expiary_date)
                        for stockRow in stockRows:
                            batch_id=stockRow.batch_id
                            quantity=stockRow.quantity
                            block_qty=stockRow.block_qty
                            availableQty=quantity-block_qty
                            
                            if requestBaseQty<=availableQty:
                                newBlockQty=block_qty+requestBaseQty
                                newBaseQty=requestBaseQty
                                requestBaseQty=0
                                
                                if firstBatchFlag==0:
                                    invRow.update_record(batch_id=batch_id,quantity=0,bonus_qty=newBaseQty)
                                else:
                                    detailDict={'cid':c_id,'depot_id':req_depot,'depot_name':depot_name,'sl':req_sl,'store_id':store_id,'store_name':store_name,'order_sl':order_sl,'order_datetime':order_datetime,'delivery_date':delivery_date,'client_id':client_id,'client_name':client_name,'rep_id':rep_id,'rep_name':rep_name,'market_id':market_id,'market_name':market_name,'area_id':area_id,'area_name':area_name,'level0_id':level0_id,'level0_name':level0_name,'level1_id':level1_id,'level1_name':level1_name,'level2_id':level2_id,'level2_name':level2_name,'level3_id':level3_id,'level3_name':level3_name,'invoice_media':invoice_media,'device_user_agent':'','ip_ref':'','ym_date':ym_date,'discount':discount,'payment_mode':payment_mode,'d_man_id':d_man_id,'d_man_name':d_man_name,'item_id':item_id,'item_name':item_name,'batch_id':batch_id,'category_id':category_id,'actual_tp':actual_tp,'actual_vat':actual_vat,'quantity':0,'bonus_qty':newBaseQty,'price':0,'item_vat':0,'sp_discount_item':0,'item_unit':item_unit,'item_carton':item_carton,'promotion_type':promotion_type,'bonus_applied_on_qty':bonus_applied_on_qty,'circular_no':circular_no,'note':req_note,'short_note':short_note,'status':'Submitted'}
                                    detailList.append(detailDict)
                                    
                                stockRow.update_record(block_qty=newBlockQty) 
                                firstBatchFlag=1
                                break
                                
                            else:
                                newBlockQty=block_qty+availableQty
                                newBaseQty=availableQty
                                requestBaseQty=requestBaseQty-availableQty
                                
                                #--------------
                                if firstBatchFlag==0:
                                    invRow.update_record(batch_id=batch_id,quantity=0,bonus_qty=newBaseQty)
                                else:
                                    detailDict={'cid':c_id,'depot_id':req_depot,'depot_name':depot_name,'sl':req_sl,'store_id':store_id,'store_name':store_name,'order_sl':order_sl,'order_datetime':order_datetime,'delivery_date':delivery_date,'client_id':client_id,'client_name':client_name,'rep_id':rep_id,'rep_name':rep_name,'market_id':market_id,'market_name':market_name,'area_id':area_id,'area_name':area_name,'level0_id':level0_id,'level0_name':level0_name,'level1_id':level1_id,'level1_name':level1_name,'level2_id':level2_id,'level2_name':level2_name,'level3_id':level3_id,'level3_name':level3_name,'invoice_media':invoice_media,'device_user_agent':'','ip_ref':'','ym_date':ym_date,'discount':discount,'payment_mode':payment_mode,'d_man_id':d_man_id,'d_man_name':d_man_name,'item_id':item_id,'item_name':item_name,'batch_id':batch_id,'category_id':category_id,'actual_tp':actual_tp,'actual_vat':actual_vat,'quantity':0,'bonus_qty':newBaseQty,'price':0,'item_vat':0,'sp_discount_item':0,'item_unit':item_unit,'item_carton':item_carton,'promotion_type':promotion_type,'bonus_applied_on_qty':bonus_applied_on_qty,'circular_no':circular_no,'note':req_note,'short_note':short_note,'status':'Submitted'}
                                    detailList.append(detailDict)
                                    
                                stockRow.update_record(block_qty=newBlockQty)
                                firstBatchFlag=1
                                
                        #--------------
                        if requestBaseQty>0:
                            emptyBatchFlag=1
                            if firstBatchFlag==1:                            
                                detailDict={'cid':c_id,'depot_id':req_depot,'depot_name':depot_name,'sl':req_sl,'store_id':store_id,'store_name':store_name,'order_sl':order_sl,'order_datetime':order_datetime,'delivery_date':delivery_date,'client_id':client_id,'client_name':client_name,'rep_id':rep_id,'rep_name':rep_name,'market_id':market_id,'market_name':market_name,'area_id':area_id,'area_name':area_name,'level0_id':level0_id,'level0_name':level0_name,'level1_id':level1_id,'level1_name':level1_name,'level2_id':level2_id,'level2_name':level2_name,'level3_id':level3_id,'level3_name':level3_name,'invoice_media':invoice_media,'device_user_agent':'','ip_ref':'','ym_date':ym_date,'discount':discount,'payment_mode':payment_mode,'d_man_id':d_man_id,'d_man_name':d_man_name,'item_id':item_id,'item_name':item_name,'batch_id':'','category_id':category_id,'actual_tp':actual_tp,'actual_vat':actual_vat,'quantity':0,'bonus_qty':requestBaseQty,'price':0,'item_vat':0,'sp_discount_item':0,'item_unit':item_unit,'item_carton':item_carton,'promotion_type':promotion_type,'bonus_applied_on_qty':bonus_applied_on_qty,'circular_no':circular_no,'note':req_note,'short_note':short_note,'status':'Submitted'}
                                detailList.append(detailDict)
                        #---------------------------------------
                
                hRows=db((db.sm_invoice_head.cid==c_id)& (db.sm_invoice_head.depot_id==req_depot) & (db.sm_invoice_head.sl==req_sl)).select(db.sm_invoice_head.client_id,db.sm_invoice_head.discount,limitby=(0,1))
                client_id=hRows[0].client_id
                discount=float(hRows[0].discount)
                
                discount=round(float(discount),2)
                totalAmount=(round(totalAmountTP,2)+round(totalAmountVat,2)-discount)
                
                #----------- check credit policy
                limitOverFlag=0        
                creditPolicyRow=db((db.sm_cp_approved.cid==c_id)&(db.sm_cp_approved.client_id==client_id)&(db.sm_cp_approved.status=='ACTIVE')).select(db.sm_cp_approved.credit_amount,limitby=(0,1))
                if creditPolicyRow:
                    credit_amount=creditPolicyRow[0].credit_amount
                    
                    tx_closing_balance=0
                    ledgerRow=db((db.sm_transaction.cid==c_id)&(db.sm_transaction.tx_account=='CLT-'+str(client_id))&(db.sm_transaction.opposite_account=='DPT-'+str(req_depot))).select(db.sm_transaction.tx_closing_balance,orderby=~db.sm_transaction.tx_date,limitby=(0,1))
                    if ledgerRow:
                        tx_closing_balance=ledgerRow[0].tx_closing_balance            
                    clientTotal=tx_closing_balance+totalAmount
                    
                    if clientTotal>credit_amount:
                        limitOverFlag=1
                #----------- end check credit policy
                if len(detailList) > 0:
                    rows=db.sm_invoice.bulk_insert(detailList)
                
                db((db.sm_invoice_head.cid==c_id)& (db.sm_invoice_head.depot_id==req_depot) & (db.sm_invoice_head.sl==req_sl)).update(client_limit_over=limitOverFlag,empty_batch_flag=emptyBatchFlag)
                
                session.flash='Processed Successfully'
            
            #---------------------
            autDelCronRows[0].update_record(auto_del_cron_flag=0)
            db.commit()
            #--------------
        
#         if btn_delete_empty_batch:            
#             redirect(URL(c='order_invoice',f='update_invoice_item',vars=dict(btn_delete_empty_batch='Yes'),args=[req_depot,req_sl,0,0]))
#         else:            
            redirect(URL(c='order_invoice',f='invoice_generate',vars=dict(req_sl=req_sl,dptid=req_depot)))
        
        
    #------------------ INVOCIE reprocess/promotional rules apply
    elif btn_reProcess:        
        #-----------------chcek stock cron flag
        autDelCronRows=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==req_depot)&(db.sm_depot.auto_del_cron_flag==0)).select(db.sm_depot.id,db.sm_depot.cid,limitby=(0,1))
        if not autDelCronRows:
            session.flash='One process running, please try again'
        else:
            autDelCronRows[0].update_record(auto_del_cron_flag=1)
            #-------------
            
            headRecords=db((db.sm_invoice_head.cid==c_id)& (db.sm_invoice_head.depot_id==req_depot) & (db.sm_invoice_head.sl==req_sl)).select(db.sm_invoice_head.ALL,limitby=(0,1))
            if not headRecords:
                session.flash='Invoice not available'
            else:
                #----- call function to create invoice with tp rules            
                depot_id=req_depot
                invoice_sl=req_sl
                order_sl=headRecords[0].order_sl
                clientId=headRecords[0].client_id
                try:
                    orderDate=str(headRecords[0].order_datetime)[0:10]  #current_date   2015-02-01
                except:
                    orderDate=current_date
                    
                retRes=get_order_to_delivery_detail_rules_manual(c_id,depot_id,invoice_sl,order_sl,clientId,orderDate)

                session.flash=retRes
                
            #---------------------
            autDelCronRows[0].update_record(auto_del_cron_flag=0)
            db.commit()
            #--------------
            
        redirect(URL(c='order_invoice',f='invoice_generate',vars=dict(req_sl=req_sl,dptid=req_depot)))
    
    #------------------ INVOCIE reprocess/promotional rules apply
    elif btn_apply_regDiscount:        
        #-----------------chcek stock cron flag
        autDelCronRows=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==req_depot)&(db.sm_depot.auto_del_cron_flag==0)).select(db.sm_depot.id,db.sm_depot.cid,limitby=(0,1))
        if not autDelCronRows:
            session.flash='One process running, please try again'
        else:
            autDelCronRows[0].update_record(auto_del_cron_flag=1)
            #-------------
            
            headRecords=db((db.sm_invoice_head.cid==c_id)& (db.sm_invoice_head.depot_id==req_depot) & (db.sm_invoice_head.sl==req_sl)).select(db.sm_invoice_head.ALL,limitby=(0,1))
            if not headRecords:
                session.flash='Invoice not available'
            else:
                #----- call function to create invoice with tp rules            
                depot_id=req_depot
                invoice_sl=req_sl
                order_sl=headRecords[0].order_sl
                clientId=headRecords[0].client_id
                try:
                    orderDate=str(headRecords[0].order_datetime)[0:10]  #current_date   2015-02-01
                except:
                    orderDate=current_date
                    
                retRes=get_order_to_delivery_detail_rules_manual_with_rd(c_id,depot_id,invoice_sl,order_sl,clientId,orderDate)
                
                session.flash=retRes
                
            #---------------------
            autDelCronRows[0].update_record(auto_del_cron_flag=0)
            db.commit()
            #--------------
            
        redirect(URL(c='order_invoice',f='invoice_generate',vars=dict(req_sl=req_sl,dptid=req_depot)))
    
    return dict()
    
#=========================================== Return List
def return_list():    
    #----------Task assaign----------
    task_id='rm_invoice_manage'
    task_id_view='rm_invoice_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL(c='default', f='home'))
    
    #----------------
    response.title='Return-List'
    
    c_id=session.cid
    
    
    # Set text for filter    
    btn_filter_return=request.vars.btn_filter
    btn_all=request.vars.btn_all
    depot_id_value=str(request.vars.depot_id_value).strip()
    search_type=str(request.vars.search_type).strip()
    search_value=str(request.vars.search_value).strip()
    
    reqPage=len(request.args)
    
    #Set sessions for validation
    if btn_filter_return:
        session.btn_filter_return=btn_filter_return
        session.depot_id_value_return=depot_id_value 
        session.search_type_return=search_type
        session.search_value_return=search_value
        
        if (session.search_type_return=='SL'):
            sl=0
            if not(session.search_value_return=='' or session.search_value_return==None):
                try:       
                    sl=int(session.search_value_return)
                    session.search_value_return=sl
                except:
                    session.search_value_return=sl
                    response.flash='sl needs number value'
            else:
                session.search_value_return=sl
        
        elif (session.search_type_return=='INVSL'):
            invsl=0
            if not(session.search_value_return=='' or session.search_value_return==None):
                try:       
                    invsl=int(session.search_value_return)
                    session.search_value_return=invsl
                except:
                    session.search_value_return=invsl
                    response.flash='Invoice sl needs number value'
            else:
                session.search_value_return=invsl
        
        reqPage=0
        
    elif btn_all:
        session.btn_filter_return=None
        session.depot_id_value_return=None
        session.search_type_return=None
        session.search_value_return=None
        reqPage=0
        
    #--------paging
    if reqPage:
        page=int(request.args[0])
    else:
        page=0
    items_per_page=session.items_per_page*20
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #--------end paging  
    
    #Set query based on search type
    qset=db()
    qset=qset(db.sm_return_head.cid==c_id)    
    if (session.user_type=='Depot'):
        #------------- for filter same depot and sub-depot
        #if not (session.depot_id_value_return=='' or session.depot_id_value_return==None):
        qset=qset(db.sm_return_head.depot_id==session.depot_id)
        
    #---- supervisor
    if session.user_type=='Supervisor':
        qset=qset(db.sm_return_head.area_id.belongs(session.marketList))
    else:
        pass
    #----
    
    if (session.btn_filter_return):
        if (session.user_type!='Depot'):
            if not (session.depot_id_value_return=='' or session.depot_id_value_return==None):
                searchValue=str(session.depot_id_value_return).split('|')[0].upper()
                qset=qset(db.sm_return_head.depot_id==searchValue)
            else:
                qset=qset(db.sm_return_head.depot_id!='')
                
        #------------
        if (session.search_type_return=='SL'):
            qset=qset(db.sm_return_head.sl==session.search_value_return)
        
        elif (session.search_type_return=='INVSL'):
            qset=qset(db.sm_return_head.invoice_sl==session.search_value_return)
            
        elif (session.search_type_return=='CLIENTID'):
            searchValue=str(session.search_value_return).split('|')[0].upper()
            qset=qset(db.sm_return_head.client_id==searchValue)
        
        elif (session.search_type_return=='REPID'):
            searchValue=str(session.search_value_return).split('|')[0].upper()
            qset=qset(db.sm_return_head.rep_id==searchValue)
        
        elif (session.search_type_return=='DATE'):
            qset=qset(db.sm_return_head.return_date==session.search_value_return)
            
    records=qset.select(db.sm_return_head.ALL,orderby=~db.sm_return_head.id,limitby=limitby)
    
    #------------------------------------------------
    search_form =SQLFORM(db.sm_search_date)
    #-------------
    
    return dict(search_form=search_form,records=records,page=page,items_per_page=items_per_page,access_permission=access_permission,access_permission_view=access_permission_view)


#======================= Return
#Validation return_add
def process_return(form):
    c_id=session.cid   
    
    depot_id=str(request.vars.depot_id).strip().upper().split('|')[0]
    store_idname=str(request.vars.store_id)
    
    sl=int(form.vars.sl)
    ym_date=str(form.vars.return_date)[0:7]+'-01'
    #---------------
    
    client_id=str(request.vars.client_id).strip().upper().split('|')[0]
    rep_id=str(request.vars.rep_id).strip().upper().split('|')[0]
    
    item_id=form.vars.item_id
    item_name=form.vars.item_name
    quantity=form.vars.quantity
    bonus_qty=form.vars.bonus_qty
    short_note=form.vars.short_note
    
    
    try:
        quantity=int(quantity)
        if quantity < 0:
            quantity=0
    except:
        quantity=0
    
    try:
        bonus_qty=int(bonus_qty)
        if bonus_qty < 0:
            bonus_qty=0
    except:
        bonus_qty=0
    
    
    batch_id=str(request.vars.batch_id).split('|')[0]
    
    if store_idname=='':
        form.errors.depot_id='Required Store'
    else:
        store_id=str(store_idname).split('|')[0]
        store_name=str(store_idname).split('|')[1]
        
        if item_id=='' or item_id==None:
            form.errors.quantity=''  
            session.flash='Select Item'
        else:
            itemRows=db((db.sm_item.cid==c_id)&(db.sm_item.item_id==item_id)).select(db.sm_item.item_id,db.sm_item.unit_type,db.sm_item.item_carton,db.sm_item.price,db.sm_item.vat_amt,limitby=(0,1))
            if not itemRows:
                form.errors.quantity=''  
                response.flash='Invalid Item' 
            else:
                price=itemRows[0].price
                vat_amt=itemRows[0].vat_amt
                item_unit=itemRows[0].unit_type
                item_carton=itemRows[0].item_carton
                
                #--------------------depot check
                depotRecords=db((db.sm_depot.cid==c_id)& (db.sm_depot.depot_id==depot_id)& (db.sm_depot.status=='ACTIVE')).select(db.sm_depot.name,limitby=(0,1))
                if not depotRecords:
                    form.errors.quantity=''  
                    response.flash='Invalid Depot ID %s' %(depot_id)
                else:
                    dpName=depotRecords[0].name
                    form.vars.depot_id=depot_id
                    form.vars.depot_name=dpName
                    
                    clientRecords=db((db.sm_client.cid==c_id)& (db.sm_client.depot_id==depot_id) & (db.sm_client.client_id==client_id)& (db.sm_client.status=='ACTIVE')).select(db.sm_client.client_id,db.sm_client.name,db.sm_client.area_id,limitby=(0,1))
                    if not clientRecords:
                        form.errors.quantity=''
                        response.flash='Invalid Client ID!' 
                    else:
                        clName=clientRecords[0].name
                        area_id=clientRecords[0].area_id
                        
                        areaName=''
                        level0_id=''
                        level0_name=''
                        level1_id=''
                        level1_name=''
                        level2_id=''
                        level2_name=''
                        level3_id=''
                        level3_name=''
                        levelRecords=db((db.sm_level.cid==c_id)& (db.sm_level.level_id==area_id)).select(db.sm_level.ALL,limitby=(0,1))
                        if not levelRecords:
                            form.errors.client_id='Invalid territory id of the Client'
                        else:
                            areaName=levelRecords[0].level_name
                            level0_id=levelRecords[0].level0
                            level0_name=levelRecords[0].level0_name
                            level1_id=levelRecords[0].level1
                            level1_name=levelRecords[0].level1_name
                            level2_id=levelRecords[0].level2
                            level2_name=levelRecords[0].level2_name
                            level3_id=levelRecords[0].level3
                            level3_name=levelRecords[0].level3_name
                            
                            form.vars.area_id=area_id
                            form.vars.area_name=areaName
                            form.vars.client_id=client_id
                            form.vars.client_name=clName
                            
                            form.vars.level0_id=level0_id
                            form.vars.level0_name=level0_name
                            form.vars.level1_id=level1_id
                            form.vars.level1_name=level1_name
                            form.vars.level2_id=level2_id
                            form.vars.level2_name=level2_name
                            form.vars.level3_id=level3_id
                            form.vars.level3_name=level3_name
                            
                            repRecords=db((db.sm_rep.cid==c_id) & (db.sm_rep.rep_id==rep_id)& (db.sm_rep.status=='ACTIVE')).select(db.sm_rep.rep_id,db.sm_rep.name,limitby=(0,1))
                            if not repRecords:
                                form.errors.quantity=''
                                response.flash='Invalid Rep ID!'
                            else:
                                repName=repRecords[0].name
                                form.vars.rep_id=rep_id
                                form.vars.rep_name=repName
                                
                                repClientRecords=db((db.sm_rep_area.cid==c_id)& (db.sm_rep_area.rep_id==rep_id)& (db.sm_rep_area.area_id==area_id)).select(db.sm_rep_area.rep_id,limitby=(0,1))
                                if not repClientRecords:
                                    form.errors.rep_id='Customer territory and MSO-Territory not matched'   
                                else:                                    
                                    #------
                                    if quantity == 0 and bonus_qty == 0:
                                        form.errors.quantity='Invalid quantity'
                                        
                                    elif quantity > 0 and bonus_qty > 0:
                                        form.errors.quantity='Required only one (Qty/BonusQty) Quantity'                                                  
                                    else:
                                        if bonus_qty > 0:
                                            price=0
                                            vat_amt=0
                                         
                                        batchFlag=True
                                        if batch_id!='':                                                
                                            itemBatchRows = db((db.sm_item_batch.cid == c_id) & (db.sm_item_batch.item_id == item_id) & (db.sm_item_batch.batch_id == batch_id) & (db.sm_item_batch.expiary_date >= current_date)).select(db.sm_item_batch.item_id,limitby=(0,1))
                                            if not itemBatchRows:
                                                form.errors.item_id='Invalid Item Batch ID'
                                                batchFlag=False
                                            else:                                                    
                                                stockRows=db((db.sm_depot_stock_balance.cid==c_id)& (db.sm_depot_stock_balance.depot_id==depot_id) & (db.sm_depot_stock_balance.store_id==store_id) & (db.sm_depot_stock_balance.item_id==item_id)& (db.sm_depot_stock_balance.batch_id==batch_id)).select(db.sm_depot_stock_balance.id,db.sm_depot_stock_balance.quantity,db.sm_depot_stock_balance.block_qty,limitby=(0,1))
                                                if not stockRows:
                                                    form.errors.quantity='Stock settings of the Item Batch is not available'
                                                    batchFlag=False
                                                else:
                                                    pass
                                        
                                        if batchFlag==True:
                                            form.vars.store_id=store_id
                                            form.vars.store_name=store_name
                                            form.vars.batch_id=batch_id
                                            form.vars.quantity=quantity
                                            form.vars.bonus_qty=bonus_qty                                            
                                            form.vars.price=price
                                            form.vars.item_vat=vat_amt
                                            form.vars.item_unit=item_unit
                                            form.vars.item_carton=item_carton
                                            
                                            if sl==0:
                                                # Get max sl
                                                maxSl=1
                                                records=db((db.sm_depot.cid==c_id) & (db.sm_depot.depot_id==depot_id)).select(db.sm_depot.id,db.sm_depot.return_sl,limitby=(0,1))
                                                if records:
                                                    sl=records[0].return_sl
                                                    maxSl=int(sl)+1
                                                    
                                                # sl update in depot
                                                records[0].update_record(return_sl=maxSl)
                                                
                                                form.vars.sl=maxSl    
                                                
                                            if (form.vars.order_sl==None):
                                                form.vars.order_sl=0
                                                
                                            if (form.vars.invoice_sl==None):
                                                form.vars.invoice_sl=0
                                                
                                            form.vars.ym_date=ym_date

#=============================================
def return_add():
    c_id=session.cid
    
    #----------Task assaign----------
    task_id='rm_invoice_manage'
    task_id_view='rm_invoice_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL(c='default', f='home'))
    
    #----------------
    response.title='Return-Add'
    
    #------------------- variable for batch upload
    total_row=request.vars.total_row
    count_inserted=request.vars.count_inserted
    count_error=request.vars.count_error
    error_str=request.vars.error_str
    
    if total_row==None:
        total_row=0
    if count_inserted==None:
        count_inserted=0
    if count_error==None:
        count_error=0
    if error_str==None:
        error_str=''
    #------------------
    btn_update=request.vars.btn_update
    btn_batch_upload=request.vars.btn_batch_upload
    btn_import_req=request.vars.btn_import_req
    
    #----
    from_invoice_flag=request.vars.from_invoice_flag
    
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
    #--------------------------
    
    #--------------- BUTTON UPDATE
    if btn_update:
        req_depot_id=depot_id
        reqSl=request.vars.sl
        client_id=str(request.vars.client_id).strip().upper().split('|')[0]
        rep_id=str(request.vars.rep_id).strip().upper().split('|')[0]
        
        return_date=request.vars.return_date
        ym_date=str(return_date)[0:7]+'-01'
        req_note=str(request.vars.note).strip()
        ret_reason=str(request.vars.ret_reason).strip() 
        
        try:
            discount=float(request.vars.discount)
        except:
            discount=0
            
        req_sl=int(reqSl)
        
        #Chech Client and rep
        clientRecords=db((db.sm_client.cid==c_id)& (db.sm_client.depot_id==req_depot_id) & (db.sm_client.client_id==client_id) & (db.sm_client.status=='ACTIVE')).select(db.sm_client.client_id,db.sm_client.area_id,db.sm_client.name,limitby=(0,1))
        if clientRecords:
            clName=clientRecords[0].name
            area_id=clientRecords[0].area_id
            area_name=''
            levelRecords=db((db.sm_level.cid==c_id)& (db.sm_level.level_id==area_id)).select(db.sm_level.level_name,limitby=(0,1))
            if not levelRecords:
                session.flash='Invalid Client Territory'
            else:
                area_name=levelRecords[0].level_name
               
            repRecords=db((db.sm_rep.cid==c_id) & (db.sm_rep.rep_id==rep_id)& (db.sm_rep.status=='ACTIVE')).select(db.sm_rep.rep_id,db.sm_rep.name,limitby=(0,1))
            if repRecords:
                repName=repRecords[0].name
                
                inv_discount=0
                prev_return_discount=0
                retRows=db((db.sm_return_head.cid==c_id)& (db.sm_return_head.depot_id==req_depot_id) & (db.sm_return_head.sl==reqSl)).select(db.sm_return_head.inv_discount,db.sm_return_head.prev_return_discount,limitby=(0,1))
                if retRows:
                    inv_discount=retRows[0].inv_discount
                    prev_return_discount=retRows[0].prev_return_discount
                    
                availableDiscount=round(inv_discount-prev_return_discount,2)
                
                if discount>availableDiscount:
                    session.flash='Discount can not be greater than available discount amount '+str(availableDiscount)
                else:
                    db((db.sm_return_head.cid==c_id)& (db.sm_return_head.depot_id==req_depot_id) & (db.sm_return_head.sl==reqSl)).update(client_id=client_id,rep_id=rep_id,area_id=area_id,client_name=clName,rep_name=repName,area_name=area_name,return_date=return_date,ret_reason=ret_reason,note=req_note,ym_date=ym_date,discount=discount)
                    db((db.sm_return.cid==c_id)& (db.sm_return.depot_id==req_depot_id) & (db.sm_return.sl==reqSl)).update(client_id=client_id,rep_id=rep_id,area_id=area_id,client_name=clName,rep_name=repName,area_name=area_name,return_date=return_date,ret_reason=ret_reason,note=req_note,ym_date=ym_date,discount=discount)
                    
                    session.flash='Updated successfully!'
            else:
                session.flash='Invalid Rep ID!'
        else:
            session.flash='Invalid Client ID!'
        
        redirect(URL(c='order_invoice',f='return_add',vars=dict(req_sl=reqSl,dptid=req_depot_id)))
        
    # BATCH UPLOAD will get based on status and access permission
    
    # IMPORT FROM INVOICE based on status
    elif btn_import_req:
        maxSl=0
#        try:
        req_depot_id=depot_id
        reqSl=int(request.vars.sl)
        
        return_date=request.vars.return_date
        ym_date=str(return_date)[0:7]+'-01'
        
        try:
            invoice_sl=int(request.vars.invoice_sl)
        except:
            invoice_sl=0
            
        ret_reason=str(request.vars.ret_reason).strip()         
        if ret_reason=='':
            session.flash='Required Cause'
        else:
            #Get records from invoice
            #Insert head in loop
            #Create list for bulk insert
            if reqSl!=0 :
                response.flash='need new Invoice!'
            else:
                if (return_date=='' or invoice_sl <= 0):
                    session.flash='Date and Invoice SL needed!'
                else:
                    #-------------------  items
                    reqRecords=db((db.sm_invoice.cid==c_id) & (db.sm_invoice.depot_id==req_depot_id) &(db.sm_invoice.sl==invoice_sl)&(db.sm_invoice.status=='Invoiced')).select(db.sm_invoice.ALL,orderby=db.sm_invoice.item_name)
                    if not reqRecords:
                        session.flash='Invoice not available!'
                    else:
                        retRecords=db((db.sm_return_head.cid==c_id) & (db.sm_return_head.depot_id==req_depot_id) &(db.sm_return_head.invoice_sl==invoice_sl)&(db.sm_return_head.status=='Draft')).select(db.sm_return_head.sl,limitby=(0,1))
                        if retRecords:
                            session.flash='Already Draft return available of the Invoice'
                        else:                            
                            inv_discount=0
                            return_discount=0
                            inv_sp_discount=0
                            return_sp_discount=0
                            cl_category_id=''
                            cl_category_name=''
                            cl_sub_category_id=''
                            cl_sub_category_name=''
                            special_territory_code=''
                            
                            market_id=''
                            market_name=''
                            d_man_id=''
                            d_man_name=''
                            shipment_no=''
                            invoice_date=''
                            invoice_ym_date=''
                            
                            discount_precent=0
                            sp_flat=0
                            sp_approved=0
                            sp_others=0
                            
                            inv_actual_total_tp=0
                            inv_regular_disc_tp=0
                            inv_flat_disc_tp=0
                            inv_approved_disc_tp=0
                            inv_others_disc_tp=0
                            inv_no_disc_tp=0
                            inv_vat_total_amount=0

                            dist_discount = 0
                            
                            invHeadRecords=db((db.sm_invoice_head.cid==c_id) & (db.sm_invoice_head.depot_id==req_depot_id) &(db.sm_invoice_head.sl==invoice_sl)).select(db.sm_invoice_head.ALL,limitby=(0,1))
                            if invHeadRecords:
                                inv_vat_total_amount=invHeadRecords[0].vat_total_amount
                                inv_discount=invHeadRecords[0].discount
                                return_discount=invHeadRecords[0].return_discount
                                inv_sp_discount=invHeadRecords[0].sp_discount
                                return_sp_discount=invHeadRecords[0].return_sp_discount
                                
                                market_id=invHeadRecords[0].market_id
                                market_name=invHeadRecords[0].market_name
                                d_man_id=invHeadRecords[0].d_man_id
                                d_man_name=invHeadRecords[0].d_man_name
                                shipment_no=invHeadRecords[0].shipment_no
                                invoice_date=invHeadRecords[0].invoice_date
                                invoice_ym_date=invHeadRecords[0].invoice_ym_date
                                
                                cl_category_id=invHeadRecords[0].cl_category_id
                                cl_category_name=invHeadRecords[0].cl_category_name
                                cl_sub_category_id=invHeadRecords[0].cl_sub_category_id
                                cl_sub_category_name=invHeadRecords[0].cl_sub_category_name
                                special_territory_code=invHeadRecords[0].special_territory_code
                                
                                discount_precent=invHeadRecords[0].discount_precent
                                sp_flat=invHeadRecords[0].sp_flat
                                sp_approved=invHeadRecords[0].sp_approved
                                sp_others=invHeadRecords[0].sp_others
                                
                                inv_actual_total_tp=invHeadRecords[0].actual_total_tp
                                inv_regular_disc_tp=invHeadRecords[0].regular_disc_tp
                                inv_flat_disc_tp=invHeadRecords[0].flat_disc_tp
                                inv_approved_disc_tp=invHeadRecords[0].approved_disc_tp
                                inv_others_disc_tp=invHeadRecords[0].others_disc_tp
                                inv_no_disc_tp=invHeadRecords[0].no_disc_tp
                                dist_discount = invHeadRecords[0].dist_discount
                                
                            #----------
                            maxSl=1
                            records=db((db.sm_depot.cid==c_id) & (db.sm_depot.depot_id==req_depot_id)).select(db.sm_depot.id,db.sm_depot.return_sl,limitby=(0,1))
                            if records:
                                sl=records[0].return_sl
                                maxSl=int(sl)+1                        
                            #---------------
                            # sl update in depot
                            if records:
                                records[0].update_record(return_sl=maxSl)
                            
                            reqDict={}
                            insList=[]
                            invoice_sl=0
                            headFlag=False
                            for row in reqRecords:
                                invdet_rowid=row.id
                                depot_id=row.depot_id
                                depot_name=row.depot_name
                                store_id=row.store_id
                                store_name=row.store_name
                                
                                invoice_sl=row.sl
                                order_sl=row.order_sl
                                client_id=row.client_id
                                client_name=row.client_name
                                rep_id=row.rep_id
                                rep_name=row.rep_name
                                req_note=row.note
                                area_id=row.area_id
                                area_name=row.area_name
                                
                                level0_id=row.level0_id
                                level0_name=row.level0_name
                                level1_id=row.level1_id
                                level1_name=row.level1_name
                                level2_id=row.level2_id
                                level2_name=row.level2_name
                                level3_id=row.level3_id
                                level3_name=row.level3_name
                                
                                item_id=row.item_id                            
                                item_name=row.item_name
                                batch_id=row.batch_id
                                category_id=row.category_id
                                actual_tp=row.actual_tp
                                actual_vat=row.actual_vat
                                
                                item_unit=row.item_unit
                                item_carton=row.item_carton
                                
                                inv_quantity=row.quantity
                                inv_bonus_qty=row.bonus_qty
                                inv_price=row.price
                                inv_item_vat=row.item_vat
                                short_note=row.short_note
                                
                                inv_sp_discount_item=row.sp_discount_item
                                prev_return_sp_discount_item=row.return_sp_discount_item
                                
                                inv_promotion_type=row.promotion_type
                                inv_bonus_applied_on_qty=row.bonus_applied_on_qty
                                inv_circular_no=row.circular_no
                                discount_type=row.discount_type
                                item_discount=row.item_discount
                                inv_item_discount_percent=row.item_discount_percent
                                inv_discount_type_quantity=row.discount_type_quantity
                                
                                prev_return_qty=row.return_qty
                                prev_return_bonus_qty=row.return_bonus_qty                                
                                prev_return_discount=return_discount
                                prev_return_sp_discount=return_sp_discount

                                inv_dist_discount_item = row.dist_discount_item
                                
                                itemAvailableQty=int(inv_quantity)-int(prev_return_qty)
                                itemAvailableBQty=int(inv_bonus_qty)-int(prev_return_bonus_qty)
                                availableDiscount=round(float(inv_discount)-float(prev_return_discount),2)
                                availableSpDiscount=round(float(inv_sp_discount)-float(prev_return_sp_discount),2)
                                
                                #if itemAvailableQty>0 or itemAvailableBQty>0:                            
                                reqDict={'cid':c_id,'depot_id':depot_id,'depot_name':depot_name,'sl':maxSl,'store_id':store_id,'store_name':store_name,'order_sl':order_sl,'invoice_sl':invoice_sl,'client_id':client_id,'client_name':client_name,'rep_id':rep_id,'rep_name':rep_name,'market_id':market_id,'market_name':market_name,'d_man_id':d_man_id,'d_man_name':d_man_name,'shipment_no':shipment_no,'invoice_date':invoice_date,'invoice_ym_date':invoice_ym_date,'area_id':area_id,'area_name':area_name,'level0_id':level0_id,'level0_name':level0_name,'level1_id':level1_id,'level1_name':level1_name,'level2_id':level2_id,'level2_name':level2_name,'level3_id':level3_id,'level3_name':level3_name,'cl_category_id':cl_category_id,'cl_category_name':cl_category_name,'cl_sub_category_id':cl_sub_category_id,'cl_sub_category_name':cl_sub_category_name,'special_territory_code':special_territory_code,'ret_reason':ret_reason,'return_date':return_date,'discount':availableDiscount,'note':req_note,
                                               'item_id':item_id,'item_name':item_name,'batch_id':batch_id,'category_id':category_id,'actual_tp':actual_tp,'actual_vat':actual_vat,'quantity':itemAvailableQty,'bonus_qty':itemAvailableBQty,'price':inv_price,'item_vat':inv_item_vat,'item_unit':item_unit,'item_carton':item_carton,'inv_promotion_type':inv_promotion_type,'inv_bonus_applied_on_qty':inv_bonus_applied_on_qty,'inv_circular_no':inv_circular_no,'discount_type':discount_type,'item_discount':item_discount,'inv_item_discount_percent':inv_item_discount_percent, 'inv_discount_type_quantity':inv_discount_type_quantity,'inv_quantity':inv_quantity,'inv_bonus_qty':inv_bonus_qty,'inv_price':inv_price,'inv_item_vat':inv_item_vat,'prev_return_qty':prev_return_qty,'prev_return_bonus_qty':prev_return_bonus_qty,'inv_discount':inv_discount,'prev_return_discount':prev_return_discount,'invdet_rowid':invdet_rowid,'inv_sp_discount_item':inv_sp_discount_item,'prev_return_sp_discount_item':prev_return_sp_discount_item,'short_note':short_note,'ym_date':ym_date,'inv_dist_discount_item':inv_dist_discount_item}
                                                
                                insList.append(reqDict)
                                if headFlag==False:
                                    db.sm_return_head.insert(cid=c_id,depot_id=depot_id,depot_name=depot_name,sl=maxSl,store_id=store_id,store_name=store_name,order_sl=order_sl,invoice_sl=invoice_sl,client_id=client_id,client_name=client_name,rep_id=rep_id,rep_name=rep_name,market_id=market_id,market_name=market_name,d_man_id=d_man_id,d_man_name=d_man_name,shipment_no=shipment_no,invoice_date=invoice_date,invoice_ym_date=invoice_ym_date,area_id=area_id,area_name=area_name,level0_id=level0_id,level0_name=level0_name,level1_id=level1_id,level1_name=level1_name,level2_id=level2_id,level2_name=level2_name,level3_id=level3_id,level3_name=level3_name,cl_category_id=cl_category_id,cl_category_name=cl_category_name,cl_sub_category_id=cl_sub_category_id,cl_sub_category_name=cl_sub_category_name,special_territory_code=special_territory_code,ret_reason=ret_reason,return_date=return_date,inv_actual_total_tp=inv_actual_total_tp,inv_regular_disc_tp=inv_regular_disc_tp,inv_flat_disc_tp=inv_flat_disc_tp,inv_approved_disc_tp=inv_approved_disc_tp,inv_others_disc_tp=inv_others_disc_tp,inv_no_disc_tp=inv_no_disc_tp,discount=availableDiscount,inv_vat_total_amount=inv_vat_total_amount,inv_discount=inv_discount,prev_return_discount=prev_return_discount,inv_sp_discount=inv_sp_discount,sp_discount=availableSpDiscount,prev_return_sp_discount=prev_return_sp_discount,inv_discount_precent=discount_precent,inv_sp_flat=sp_flat,inv_sp_approved=sp_approved,inv_sp_others=sp_others,note=req_note,ym_date=ym_date,inv_dist_discount=dist_discount)
                                    headFlag=True
                                    
                            if len(insList)>0:                        
                                rows=db.sm_return.bulk_insert(insList)                            
                                session.flash='Imported successfully'
                            else:
                                session.flash='Qty not available to return'
        
        req_sl=maxSl
        
        if maxSl > 0:
            if from_invoice_flag=='Yes':                
                redirect(URL('update_status_return',vars=dict(btn_post='Yes'),args=[req_depot_id,req_sl,invoice_sl,return_date]))
            else:
                redirect(URL('return_add',vars=dict(req_sl=maxSl,dptid=req_depot_id)))
        else:
            redirect(URL('return_add',vars=dict(req_sl=reqSl,dptid=req_depot_id)))
    
    #----------------- ITEM SAVE/ REPLACE IF EXIST
    db.sm_return.ret_reason.requires=IS_IN_DB(db((db.sm_category_type.cid == session.cid)&(db.sm_category_type.type_name=='RET_REASON')),db.sm_category_type.cat_type_id,orderby=db.sm_category_type.cat_type_id)
    
    form =SQLFORM(db.sm_return,
                  fields=['depot_id','sl','store_id','client_id','rep_id','order_sl','invoice_sl','return_date','ret_reason','status','item_id','item_name','category_id','batch_id','quantity','bonus_qty','price','item_vat','note','short_note'],         
                  submit_button='Save'
                  )
    
    #Insert with validation
    form.vars.cid=c_id
    
    if not(btn_update or btn_batch_upload or btn_import_req):
        if form.accepts(request.vars,session,onvalidation=process_return):
            sl=form.vars.sl
            depot_id=str(form.vars.depot_id).strip()
            depot_name=form.vars.depot_name
            store_id=form.vars.store_id
            store_name=form.vars.store_name
            
            client_id=str(form.vars.client_id).strip()
            client_name=form.vars.client_name
            rep_id=str(form.vars.rep_id).strip()
            rep_name=form.vars.rep_name
            return_date=form.vars.return_date
            ym_date=str(return_date)[0:7]+'-01'#Set first day of month
            
            note=str(form.vars.note).strip()
            area_id=str(form.vars.area_id).strip()
            area_name=form.vars.area_name
            
            ret_reason=str(form.vars.ret_reason).strip()
            
            level0_id=form.vars.level0_id
            level0_name=form.vars.level0_name
            level1_id=form.vars.level1_id
            level1_name=form.vars.level1_name
            level2_id=form.vars.level2_id
            level2_name=form.vars.level2_name
            level3_id=form.vars.level3_id
            level3_name=form.vars.level3_name
            
            discount=form.vars.discount
            note=form.vars.note
            
            #--- head insert/update
            headRows=db((db.sm_return_head.cid==c_id)& (db.sm_return_head.depot_id==depot_id) & (db.sm_return_head.sl==sl)).select(db.sm_return_head.id,db.sm_return_head.depot_id,limitby=(0,1))
            if headRows:
                headRows[0].update_record(client_id=client_id,rep_id=rep_id,area_id=area_id,ret_reason=ret_reason,depot_name=depot_name,client_name=client_name,rep_name=rep_name,area_name=area_name,level0_id=level0_id,level0_name=level0_name,level1_id=level1_id,level1_name=level1_name,level2_id=level2_id,level2_name=level2_name,level3_id=level3_id,level3_name=level3_name,return_date=return_date,note=note,ym_date=ym_date)
            else:
                db.sm_return_head.insert(cid=c_id,depot_id=depot_id,sl=sl,store_id=store_id,store_name=store_name,client_id=client_id,rep_id=rep_id,area_id=area_id,ret_reason=ret_reason,depot_name=depot_name,client_name=client_name,rep_name=rep_name,area_name=area_name,level0_id=level0_id,level0_name=level0_name,level1_id=level1_id,level1_name=level1_name,level2_id=level2_id,level2_name=level2_name,level3_id=level3_id,level3_name=level3_name,return_date=return_date,note=note,ym_date=ym_date)
                
            #-----UPDATE SAME SL VALUE
            db((db.sm_return.cid==c_id)& (db.sm_return.depot_id==depot_id) & (db.sm_return.sl==sl)).update(client_id=client_id,rep_id=rep_id,area_id=area_id,ret_reason=ret_reason,depot_name=depot_name,client_name=client_name,rep_name=rep_name,area_name=area_name,return_date=return_date,note=note,ym_date=ym_date)
            
            req_sl=int(sl)
    
    #  --------------------- SHOW FIELD VALUE
#    req_sl=request.vars.req_sl    
#    depotid=request.vars.depotid 
#    if depotid=='' or depotid==None:
#        depot_id=session.depot_id
#    else:
#        depot_id=depotid
    
    rowid=0
    sl=0
    status='Draft'
    client_id=''
    rep_id=''
    return_dt=current_date
    note='' 
    order_sl=0 
    invoice_sl=0 
    note=''
    discount=0
    retDiscount=0
    ret_reason=''
    client_name=''
    rep_name=''
    store_id=''
    store_name=''
    
    hRecords=db((db.sm_return_head.cid==c_id)& (db.sm_return_head.depot_id==depot_id) & (db.sm_return_head.sl==req_sl)).select(db.sm_return_head.ALL,limitby=(0,1))
    if hRecords:
        rowid=hRecords[0].id
        depot_id=hRecords[0].depot_id
        depot_name=hRecords[0].depot_name        
        sl=hRecords[0].sl
        store_id=hRecords[0].store_id
        store_name=hRecords[0].store_name
        
        order_sl=hRecords[0].order_sl
        invoice_sl=hRecords[0].invoice_sl
        return_dt=hRecords[0].return_date
        status=hRecords[0].status
        client_id=hRecords[0].client_id
        client_name=hRecords[0].client_name        
        rep_id=hRecords[0].rep_id
        rep_name=hRecords[0].rep_name
        discount=hRecords[0].discount
        ret_reason=hRecords[0].ret_reason
        retDiscount=hRecords[0].prev_return_discount
        
    records=db((db.sm_return.cid==c_id)& (db.sm_return.depot_id==depot_id) & (db.sm_return.sl==req_sl)).select(db.sm_return.ALL,orderby=db.sm_return.item_name)
    
    recordCount=len(records)
    
    storeRecords=''
    if sl<=0:
        storeRecords=db((db.sm_depot_store.cid==c_id) & (db.sm_depot_store.depot_id==depot_id)& (db.sm_depot_store.store_type=='SALES')).select(db.sm_depot_store.store_id,db.sm_depot_store.store_name,orderby=db.sm_depot_store.store_name)
        
    #-------------------- SHOW VALUE BY RECORD ID
    if rowid!=0:
        record= db.sm_return_head(rowid)  
        db.sm_return_head.ret_reason.requires=IS_IN_DB(db((db.sm_category_type.cid == session.cid)&(db.sm_category_type.type_name=='RET_REASON')),db.sm_category_type.cat_type_id,orderby=db.sm_category_type.cat_type_id)
        form_head =SQLFORM(db.sm_return_head,
                     record=record,
                     fields=['note','ret_reason'],
                     )
        
        return dict(form=form,form_head=form_head,rowid=rowid,records=records,recordCount=recordCount,storeRecords=storeRecords,discount=discount,retDiscount=retDiscount,depot_id=depot_id,depot_name=depot_name,sl=sl,store_id=store_id,store_name=store_name,order_sl=order_sl,invoice_sl=invoice_sl,client_id=client_id,rep_id=rep_id,client_name=client_name,rep_name=rep_name,ret_reason=ret_reason,status=status,
                count_inserted=count_inserted,count_error=count_error,error_str=error_str,total_row=total_row,return_dt=return_dt,access_permission=access_permission,access_permission_view=access_permission_view)
    else:
        return dict(form=form,rowid=rowid,records=records,recordCount=recordCount,storeRecords=storeRecords,discount=discount,retDiscount=retDiscount,depot_id=depot_id,depot_name=depot_name,sl=sl,store_id=store_id,store_name=store_name,order_sl=order_sl,invoice_sl=invoice_sl,client_id=client_id,rep_id=rep_id,client_name=client_name,rep_name=rep_name,ret_reason=ret_reason,status=status,
                count_inserted=count_inserted,count_error=count_error,error_str=error_str,total_row=total_row,return_dt=return_dt,access_permission=access_permission,access_permission_view=access_permission_view)

#=================== Delete item
#Delete item from sm_return if more than one item in a sl
def update_return_item():
    c_id=session.cid
    
    btn_delete=request.vars.btn_delete  #not used
    btn_qtyupdate=request.vars.btn_qtyupdate
    
    req_depot=request.args(0)
    req_sl=request.args(1)    
    req_item=request.args(2)
    req_rowid=request.args(3)
    
    if btn_delete:
        countRecords=db((db.sm_return.cid==c_id)& (db.sm_return.depot_id==req_depot) & (db.sm_return.sl==req_sl)).count()
        if int(countRecords)==1:
            session.flash='At least one item needs in a return, You can cancel if required!'
        else:
            delRow=db((db.sm_return.cid==c_id) & (db.sm_return.depot_id==req_depot) & (db.sm_return.sl==req_sl)& (db.sm_return.item_id==req_item)& (db.sm_return.id==req_rowid)).delete()
            if delRow:
                session.flash='Deleted successfully!'
            else:
                session.flash='Deleted failed!'
                
        redirect(URL(c='order_invoice',f='return_add',vars=dict(req_sl=req_sl,dptid=req_depot)))
        
    elif btn_qtyupdate:        
        rowQty=request.vars.rowQty
        rowBonusQty=request.vars.rowBonusQty        
        rowRate=request.vars.rowRate
        
        try:
            rowQty=int(rowQty)
            if rowQty<0:
                rowQty=0            
        except:
            rowQty=0
            
        try:
            rowBonusQty=int(rowBonusQty)
            if rowBonusQty<0:
                rowBonusQty=0
        except:
            rowBonusQty=0
        
        try:
            rowRate=float(rowRate)
            if rowRate<0:
                rowRate=0
        except:
            rowRate=0
        
        
#         if (rowQty == 0 and rowBonusQty==0):
#             session.flash='Required Valid Quantity!'
#         else:
        if (rowQty > 0 and rowBonusQty > 0):
            session.flash=' Required Only one (Qty/BonusQty) Quantity'
        else:            
            if rowQty > 0 and rowRate==0:
                session.flash=' Required valid Return Unit Price'
            else:
                retRows=db((db.sm_return.cid==c_id)& (db.sm_return.depot_id==req_depot) & (db.sm_return.sl==req_sl)& (db.sm_return.item_id==req_item)& (db.sm_return.id==req_rowid)).select(db.sm_return.id,db.sm_return.quantity,db.sm_return.bonus_qty,db.sm_return.inv_quantity,db.sm_return.inv_bonus_qty,db.sm_return.prev_return_qty,db.sm_return.prev_return_bonus_qty,db.sm_return.inv_price,limitby=(0,1))
                if not retRows:
                    session.flash='Invalid request'
                else:
                    inv_quantity=retRows[0].inv_quantity
                    inv_bonus_qty=retRows[0].inv_bonus_qty
                    inv_price=retRows[0].inv_price
                    prev_return_qty=retRows[0].prev_return_qty
                    prev_return_bonus_qty=retRows[0].prev_return_bonus_qty
                    
                    item_quantity=retRows[0].quantity
                    bonus_qty=retRows[0].bonus_qty
                    
                    itemAvailableQty=int(inv_quantity)-int(prev_return_qty)
                    itemAvailableBQty=int(inv_bonus_qty)-int(prev_return_bonus_qty)
                    
                    oldTotalAvailableQty=itemAvailableQty+itemAvailableBQty                    
                    newTotalQty=rowQty+rowBonusQty
                    
                    if newTotalQty>oldTotalAvailableQty:
                        session.flash='Qty+Bonus can not be greater than available Qty'
                    else:
                        if rowRate>inv_price:
                            session.flash='Return unit price can not be greater than invoice price '+str(inv_price)
                        else:
                            retRows[0].update_record(quantity=rowQty,bonus_qty=rowBonusQty,price=rowRate)
                            session.flash='Updated Successfully'
                    
        redirect(URL(c='order_invoice',f='return_add',vars=dict(req_sl=req_sl,dptid=req_depot)))
        
    #  ---------------------
    return dict()

#Update status as Post and Cancel

def update_status_return():
    c_id=session.cid
    
    btn_post=request.vars.btn_post
    btn_cancel=request.vars.btn_cancel
    
    btn_part_return=request.vars.btn_part_return
    btn_full_return=request.vars.btn_full_return
    btn_return_apply_rules=request.vars.btn_return_apply_rules
    
    btn_return_cancel=request.vars.btn_return_cancel
    check_return=request.vars.check_return
    
    req_depot=request.args(0)
    req_sl=request.args(1)
    invoiceSl=request.args(2)
    req_date=request.args(3)
    ym_date=str(req_date)[0:7]+'-01'
    
    #------------- POST
    if btn_post:
        #----------------- chcek stock cron flag
        autDelCronRows=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==req_depot)&(db.sm_depot.auto_del_cron_flag==0)).select(db.sm_depot.id,db.sm_depot.cid,limitby=(0,1))
        if not autDelCronRows:
            session.flash='One process running, please try again'
        else:
            autDelCronRows[0].update_record(auto_del_cron_flag=1)
            #-------------
            
            countRecords=db((db.sm_return.cid==c_id)& (db.sm_return.depot_id==req_depot) & (db.sm_return.sl==req_sl)).count()
            if int(countRecords)==0:
                session.flash='At least one item needs in a return!'
            else:
                if not (ym_date=='' or ym_date==None):
                    #Create string for client_balance_for_del_return to maintain client balance 
    #                strData=str(c_id)+'<fdfd>'+str(req_depot)+'<fdfd>returned<fdfd>'+ym_date+'<fdfd>'
                    
                    discount=0
                    sp_discount=0   #return discount
                    inv_discount=0
                    discount_adjustment=0
                    
                    inv_actual_total_tp=0   #actual total tp
                    inv_regular_disc_tp=0   #actual total tp-regular
                    inv_flat_disc_tp=0      #actual total tp-flat
                    inv_approved_disc_tp=0  #actual total tp-approved
                    inv_others_disc_tp=0    #actual total tp-others
                    
                    inv_sp_flat=0
                    inv_sp_approved=0
                    inv_sp_others=0

                    inv_dist_discount = 0
                    dist_discount = 0
                    
                    headRow=db((db.sm_return_head.cid==c_id)& (db.sm_return_head.depot_id==req_depot) & (db.sm_return_head.sl==req_sl)).select(db.sm_return_head.discount,db.sm_return_head.inv_discount,db.sm_return_head.inv_actual_total_tp,db.sm_return_head.inv_regular_disc_tp,db.sm_return_head.inv_flat_disc_tp,db.sm_return_head.inv_approved_disc_tp,db.sm_return_head.inv_others_disc_tp,db.sm_return_head.inv_sp_flat,db.sm_return_head.inv_sp_approved,db.sm_return_head.inv_sp_others,db.sm_return_head.inv_dist_discount,limitby=(0,1))
                    if headRow:
                        inv_discount=float(headRow[0].inv_discount)
                        discount=float(headRow[0].discount)                        
                        discount_adjustment=discount
                        inv_dist_discount = headRow[0].inv_dist_discount
                        
                        
                    rows=db((db.sm_return.cid==c_id)& (db.sm_return.depot_id==req_depot) & (db.sm_return.sl==req_sl) & ((db.sm_return.quantity>0)|(db.sm_return.bonus_qty>0))).select(db.sm_return.id,db.sm_return.store_id,db.sm_return.rep_id,db.sm_return.client_id,db.sm_return.item_id,db.sm_return.batch_id,db.sm_return.quantity,db.sm_return.bonus_qty,db.sm_return.actual_tp,db.sm_return.price,db.sm_return.item_vat,db.sm_return.discount,db.sm_return.invdet_rowid,db.sm_return.discount_type,db.sm_return.discount_type,db.sm_return.item_discount,db.sm_return.inv_quantity,db.sm_return.inv_price,db.sm_return.prev_return_qty,db.sm_return.short_note,db.sm_return.inv_dist_discount_item,db.sm_return.inv_quantity,db.sm_return.inv_price,db.sm_return.inv_dist_discount_item)
                    if not rows:
                        session.flash='Required Qty/Bonus Qty' 
                    else:
                        resStr=''
                        totalAmount=0
                        
                        total_tp_amount=0
                        total_vat_amount=0
                        total_ret_sp_amount=0
                        retRegTpAmt=0
                        
                        
                        ret_actual_total_tp=0   #actual total tp
                        ret_regular_disc_tp=0   #actual total tp-regular
                        ret_flat_disc_tp=0      #actual total tp-flat
                        ret_approved_disc_tp=0  #actual total tp-approved
                        ret_others_disc_tp=0    #actual total tp-others
                        
                        ret_sp_flat=0
                        ret_sp_approved=0
                        ret_sp_others=0
                        inv_total_tp_amount=0
                        
                        #if session.ledgerCreate=='YES':
                        for row in rows:
                            client_id=row.client_id
                            quantity=int(row.quantity)
                            actual_tp=float(row.actual_tp)
                            price=float(row.price)
                            item_vat=float(row.item_vat)
                            
                            prev_return_qty=int(row.prev_return_qty)
                            short_note=str(row.short_note).strip().upper()
                            
                            spDiscount=actual_tp-price
                            spAmt=round(spDiscount*quantity,6)
                            total_ret_sp_amount+=spAmt
                            
                            total_tp_amount+=round(quantity*price,6)
                            total_vat_amount+=round(quantity*item_vat,6)
                            
                            itemActualTp=round(quantity*actual_tp,6)
                            ret_actual_total_tp+=itemActualTp

                            inv_total_tp_amount += round(row.inv_quantity * row.inv_price, 6)

                            #-------------
                            discount_type=str(row.discount_type).strip().upper()
                            if discount_type=='RD':
                                rdQuantity=0
                                #----
                                rdQtyindex1=short_note.find('REGULAR DISCOUNT ON')
                                if (rdQtyindex1!=-1):
                                    rdQtyindex2=short_note.find('QUANTITY')
                                    try:
                                        disQty=int(short_note[(rdQtyindex1+19):rdQtyindex2])
                                    except:
                                        disQty=0
                                        
                                    if disQty>0:
                                        regQty=disQty-prev_return_qty
                                        if regQty>0:
                                            if regQty<=quantity:
                                                rdQuantity=regQty
                                            elif regQty>quantity:
                                                rdQuantity=quantity
                                else:
                                    rdQuantity=quantity
                                    
                                retRegTp=round(rdQuantity*price,2)                                
                                if retRegTp>0:
                                    retRegTpAmt+=retRegTp
                                    ret_regular_disc_tp+=round(rdQuantity*actual_tp,6)
                                    
                            elif discount_type=='FLAT':                                
                                ret_sp_flat+=spAmt
                                ret_flat_disc_tp+=itemActualTp
                                
                            elif discount_type=='APPROVED':
                                ret_sp_approved+=spAmt
                                ret_approved_disc_tp+=itemActualTp
                                
                            elif discount_type=='OTHERS':
                                ret_sp_others+=spAmt
                                ret_others_disc_tp+=itemActualTp
                                
                        #-------------
                        totalAmount=round((round(total_tp_amount,2)+round(total_vat_amount,2)-round(discount,2)),2) #with vat
                        total_vat_amount=round(total_vat_amount,2)
                        total_ret_sp_amount=round(total_ret_sp_amount,2)
                        
                        ret_actual_total_tp=round(ret_actual_total_tp,2)                                                
                        ret_regular_disc_tp=round(ret_regular_disc_tp,2)
                        ret_flat_disc_tp=round(ret_flat_disc_tp,2)
                        ret_approved_disc_tp=round(ret_approved_disc_tp,2)
                        ret_others_disc_tp=round(ret_others_disc_tp,2)                        
                        ret_sp_flat=round(ret_sp_flat,2)
                        ret_sp_approved=round(ret_sp_approved,2)
                        ret_sp_others=round(ret_sp_others,2)

                        #invTotalAmount = round((round(inv_total_tp_amount, 2) + round(inv_total_vat_amount, 2) - round(discount, 2)),2)  # with vat
                        invTotalAmount = round(inv_total_tp_amount, 2)

                        if invTotalAmount > 0:
                            dist_discount = round((inv_dist_discount * round(total_tp_amount,2)) / invTotalAmount, 2)
                        
                        if session.ledgerCreate=='YES':
                            strData=str(c_id)+'<fdfd>RETURN<fdfd>'+str(req_sl)+'<fdfd>'+str(datetime_fixed)+'<fdfd>'+str(req_depot)+'-'+str(req_sl)+'<fdfd>CLT-'+str(client_id)+'<fdfd>DPT-'+str(req_depot)+'<fdfd>'+str(totalAmount)
                            resStr=set_balance_transaction(strData)
                            resStrList=resStr.split('<sep>',resStr.count('<sep>'))
                            flag=resStrList[0]
                            msg=resStrList[1]
                            
                        else:
                            flag='True'
                            msg='Success'
                            
                        if flag=='True':
                            db((db.sm_return.cid==c_id)& (db.sm_return.depot_id==req_depot) & (db.sm_return.sl==req_sl)).update(status='Returned',returned_on=date_fixed,returned_by=session.user_id)
                            db((db.sm_return_head.cid==c_id)& (db.sm_return_head.depot_id==req_depot) & (db.sm_return_head.sl==req_sl)).update(status='Returned',ret_actual_total_tp=ret_actual_total_tp,ret_regular_disc_tp=ret_regular_disc_tp,ret_flat_disc_tp=ret_flat_disc_tp,ret_approved_disc_tp=ret_approved_disc_tp,ret_others_disc_tp=ret_others_disc_tp,ret_sp_flat=ret_sp_flat,ret_sp_approved=ret_sp_approved,ret_sp_others=ret_sp_others,total_amount=totalAmount,vat_total_amount=total_vat_amount,sp_discount=total_ret_sp_amount,returned_on=date_fixed,returned_by=session.user_id,dist_discount=dist_discount)
                            
                            db((db.sm_invoice.cid==c_id) & (db.sm_invoice.depot_id==req_depot) &(db.sm_invoice.sl==invoiceSl)).update(note='Returned')
                            db((db.sm_invoice_head.cid==c_id) & (db.sm_invoice_head.depot_id==req_depot) &(db.sm_invoice_head.sl==invoiceSl)).update(note='Returned')#,return_discount=discount
                            
                            invHRow=db((db.sm_invoice_head.cid==c_id) & (db.sm_invoice_head.depot_id==req_depot) &(db.sm_invoice_head.sl==invoiceSl)).select(db.sm_invoice_head.id,db.sm_invoice_head.return_tp,db.sm_invoice_head.return_vat,db.sm_invoice_head.return_discount,db.sm_invoice_head.return_sp_discount,db.sm_invoice_head.discount,db.sm_invoice_head.vat_total_amount,db.sm_invoice_head.sp_discount,db.sm_invoice_head.return_count,db.sm_invoice_head.actual_total_tp,db.sm_invoice_head.regular_disc_tp,db.sm_invoice_head.flat_disc_tp,db.sm_invoice_head.approved_disc_tp,db.sm_invoice_head.others_disc_tp,db.sm_invoice_head.sp_flat,db.sm_invoice_head.sp_approved,db.sm_invoice_head.sp_others,db.sm_invoice_head.ret_actual_total_tp,db.sm_invoice_head.ret_regular_disc_tp,db.sm_invoice_head.ret_flat_disc_tp,db.sm_invoice_head.ret_approved_disc_tp,db.sm_invoice_head.ret_others_disc_tp,db.sm_invoice_head.ret_sp_flat,db.sm_invoice_head.ret_sp_approved,db.sm_invoice_head.ret_sp_others,limitby=(0,1))
                            if invHRow:
                                inv_rowid = invHRow[0].id
                                return_tp=float(invHRow[0].return_tp)+round(total_tp_amount,2)
                                return_vat=float(invHRow[0].return_vat)+total_vat_amount
                                return_discount=float(invHRow[0].return_discount)+discount
                                return_sp_discount=float(invHRow[0].return_sp_discount)+total_ret_sp_amount  
                                
                                invReturn_vat=float(invHRow[0].vat_total_amount)                   
                                invDiscount=float(invHRow[0].discount)
                                invSpDiscount=float(invHRow[0].sp_discount)
                                return_count=int(invHRow[0].return_count)
                                return_countTotal=return_count+1
                                
                                ret_actual_total_tp=float(invHRow[0].ret_actual_total_tp)+ret_actual_total_tp
                                ret_regular_disc_tp=float(invHRow[0].ret_regular_disc_tp)+ret_regular_disc_tp
                                ret_flat_disc_tp=float(invHRow[0].ret_flat_disc_tp)+ret_flat_disc_tp
                                ret_approved_disc_tp=float(invHRow[0].ret_approved_disc_tp)+ret_approved_disc_tp
                                ret_others_disc_tp=float(invHRow[0].ret_others_disc_tp)+ret_others_disc_tp                                
                                ret_sp_flat=float(invHRow[0].ret_sp_flat)+ret_sp_flat
                                ret_sp_approved=float(invHRow[0].ret_sp_approved)+ret_sp_approved
                                ret_sp_others=float(invHRow[0].ret_sp_others)+ret_sp_others
                                
                                inv_actual_total_tp=float(invHRow[0].actual_total_tp)
                                inv_regular_disc_tp=float(invHRow[0].regular_disc_tp)
                                inv_flat_disc_tp=float(invHRow[0].flat_disc_tp)
                                inv_approved_disc_tp=float(invHRow[0].approved_disc_tp)
                                inv_others_disc_tp=float(invHRow[0].others_disc_tp)
                                inv_sp_flat=float(invHRow[0].sp_flat)
                                inv_sp_approved=float(invHRow[0].sp_approved)
                                inv_sp_others=float(invHRow[0].sp_others)
                                
                                if ret_actual_total_tp>inv_actual_total_tp:
                                    ret_actual_total_tp=inv_actual_total_tp
                                    
                                if ret_regular_disc_tp>inv_regular_disc_tp:
                                    ret_regular_disc_tp=inv_regular_disc_tp
                                    
                                if ret_flat_disc_tp>inv_flat_disc_tp:
                                    ret_flat_disc_tp=inv_flat_disc_tp
                                    
                                if ret_approved_disc_tp>inv_approved_disc_tp:
                                    ret_approved_disc_tp=inv_approved_disc_tp
                                    
                                if ret_others_disc_tp>inv_others_disc_tp:
                                    ret_others_disc_tp=inv_others_disc_tp
                                    
                                if ret_sp_flat>inv_sp_flat:
                                    ret_sp_flat=inv_sp_flat
                                    
                                if ret_sp_approved>inv_sp_approved:
                                    ret_sp_approved=inv_sp_approved
                                    
                                if ret_sp_others>inv_sp_others:
                                    ret_sp_others=inv_sp_others
                                
                                if return_vat>invReturn_vat:
                                    return_vat=invReturn_vat
                                    
                                if return_discount>invDiscount:
                                    return_discount=invDiscount
                                    
                                if return_sp_discount>invSpDiscount:
                                    return_sp_discount=invSpDiscount
                                    
                                invHRow[0].update_record(ret_actual_total_tp=round(ret_actual_total_tp,2),ret_regular_disc_tp=round(ret_regular_disc_tp,2),ret_flat_disc_tp=round(ret_flat_disc_tp,2),ret_approved_disc_tp=round(ret_approved_disc_tp,2),ret_others_disc_tp=round(ret_others_disc_tp,2),ret_sp_flat=round(ret_sp_flat,2),ret_sp_approved=round(ret_sp_approved,2),ret_sp_others=round(ret_sp_others,2),return_tp=round(return_tp,2),return_vat=round(return_vat,2),return_discount=round(return_discount,2),return_sp_discount=round(return_sp_discount,2),return_count=return_countTotal,ret_dist_discount=round(dist_discount, 2))
                                
                            #-------------------
                            for row in rows:
                                store_id=row.store_id       
                                item_id=row.item_id
                                batch_id=row.batch_id
                                invdet_rowid=row.invdet_rowid
                                
                                quantity=int(row.quantity)
                                bonus_qty=int(row.bonus_qty)  
                                actual_tp=float(row.actual_tp)                              
                                price=float(row.price)
                                
                                prev_return_qty=int(row.prev_return_qty)
                                short_note=str(row.short_note).strip().upper()
                                
                                totalQty=quantity+bonus_qty
                                
                                discount_type=str(row.discount_type).strip().upper()
                                item_discount=float(row.item_discount)
                                return_item_discount=0
                                ret_discount_type_quantity=0
                                
                                inv_quantity=int(row.inv_quantity)
                                inv_price=int(row.inv_price)
                                inv_dist_discount_item = row.inv_dist_discount_item
                                
                                if discount_type=='RD':
                                    rdQuantity=0
                                    #----
                                    rdQtyindex1=short_note.find('REGULAR DISCOUNT ON')
                                    if (rdQtyindex1!=-1):
                                        rdQtyindex2=short_note.find('QUANTITY')
                                        try:
                                            disQty=int(short_note[(rdQtyindex1+19):rdQtyindex2])
                                        except:
                                            disQty=0
                                            
                                        if disQty>0:
                                            regQty=disQty-prev_return_qty
                                            if regQty>0:
                                                if regQty<=quantity:
                                                    rdQuantity=regQty
                                                elif regQty>quantity:
                                                    rdQuantity=quantity
                                    else:
                                        rdQuantity=quantity
                                    #---------------
                                    ret_discount_type_quantity=rdQuantity
                                    
                                    retRegTp=round(rdQuantity*price,2)
                                    if retRegTp>0 and retRegTpAmt>0:                                        
                                        return_item_discount=round((discount_adjustment*retRegTp)/retRegTpAmt,2)
                                        
                                elif (discount_type=='FLAT' or discount_type=='APPROVED' or discount_type=='OTHERS'): 
                                    actualInvTpAmt=round(actual_tp*inv_quantity,2)
                                    actualRetTpAmt=round(actual_tp*quantity,2)                                    
                                    ret_discount_type_quantity=quantity
                                    
                                    if actualInvTpAmt>0 and actualRetTpAmt>0:
                                       return_item_discount=round((item_discount*actualRetTpAmt)/actualInvTpAmt,2)
                                       
                                       
                                #--------- invoice details update
                                invDetRow=db((db.sm_invoice.cid==c_id) & (db.sm_invoice.depot_id==req_depot) &(db.sm_invoice.sl==invoiceSl)&(db.sm_invoice.item_id==item_id)&(db.sm_invoice.batch_id==batch_id)&(db.sm_invoice.id==invdet_rowid)).select(db.sm_invoice.id,db.sm_invoice.return_qty,db.sm_invoice.return_bonus_qty,db.sm_invoice.ret_discount_type_quantity,limitby=(0,1))
                                if invDetRow:
                                    return_qty=int(invDetRow[0].return_qty)+quantity
                                    return_bonus_qty=int(invDetRow[0].return_bonus_qty)+bonus_qty
                                    
                                    return_disc_typeQty=int(invDetRow[0].ret_discount_type_quantity)+ret_discount_type_quantity
                                    
                                    invDetRow[0].update_record(return_qty=return_qty,return_bonus_qty=return_bonus_qty,return_rate=price,ret_discount_type_quantity=return_disc_typeQty,ret_dist_discount_item=inv_dist_discount_item)
                                    
                                #--------- stock balance update
                                balanceRecords=db((db.sm_depot_stock_balance.cid==c_id)&(db.sm_depot_stock_balance.depot_id==req_depot)&(db.sm_depot_stock_balance.store_id==store_id)&(db.sm_depot_stock_balance.item_id==item_id)&(db.sm_depot_stock_balance.batch_id==batch_id)).select(db.sm_depot_stock_balance.id,db.sm_depot_stock_balance.quantity,limitby=(0,1))
                                if balanceRecords:
                                    balance_Qty=balanceRecords[0].quantity+totalQty
                                    balanceRecords[0].update_record(quantity=balance_Qty)
                                    
                                #--------- return detials update
                                if return_item_discount>0 or ret_discount_type_quantity>0:                                    
                                    row.update_record(ret_discount_type_quantity=ret_discount_type_quantity,return_item_discount=return_item_discount)

                                # distributor discount distribute return
                                row.update_record(dist_discount_item=inv_dist_discount_item)

                                dist_discount_distribute_inv(inv_rowid)

                            session.flash='Returned successfully'       
                else:
                    session.flash='Date format error'
            
            #---------------------
            autDelCronRows[0].update_record(auto_del_cron_flag=0)
            db.commit()
            #--------------
            
        redirect(URL(c='order_invoice',f='return_add',vars=dict(req_sl=req_sl,dptid=req_depot)))
        
    #---------- CANCELLED
    elif btn_cancel:
        countRecords=db((db.sm_return.cid==c_id)& (db.sm_return.depot_id==req_depot) & (db.sm_return.sl==req_sl)).count()
        if int(countRecords)==0:
            session.flash='At least one item needs in a return!'
        else:
            db((db.sm_return.cid==c_id)& (db.sm_return.depot_id==req_depot) & (db.sm_return.sl==req_sl)).update(status='Cancelled')
            db((db.sm_return_head.cid==c_id)& (db.sm_return_head.depot_id==req_depot) & (db.sm_return_head.sl==req_sl)).update(status='Cancelled')
            
        redirect(URL(c='order_invoice',f='return_add',vars=dict(req_sl=req_sl,dptid=req_depot)))
    
    #---------- Part_return/ Reset qty
    elif btn_part_return:
        countRecords=db((db.sm_return.cid==c_id)& (db.sm_return.depot_id==req_depot) & (db.sm_return.sl==req_sl)).count()
        if int(countRecords)==0:
            session.flash='At least one item needs in a return!'
        else:
            session.flash='Qty reset successfully'
            db((db.sm_return.cid==c_id)& (db.sm_return.depot_id==req_depot) & (db.sm_return.sl==req_sl)).update(quantity=0,bonus_qty=0)
            
        redirect(URL(c='order_invoice',f='return_add',vars=dict(req_sl=req_sl,dptid=req_depot)))
    
    #---------- Full_return/ Set available qty
    elif btn_full_return:
        countRecords=db((db.sm_return.cid==c_id)& (db.sm_return.depot_id==req_depot) & (db.sm_return.sl==req_sl)).count()
        if int(countRecords)==0:
            session.flash='At least one item needs in a return!'
        else:            
            retRows=db((db.sm_return.cid==c_id)& (db.sm_return.depot_id==req_depot) & (db.sm_return.sl==req_sl)).select(db.sm_return.id,db.sm_return.inv_quantity,db.sm_return.inv_bonus_qty,db.sm_return.prev_return_qty,db.sm_return.prev_return_bonus_qty,orderby=db.sm_return.id)
            for retRow in retRows:
                inv_quantity=retRow.inv_quantity
                inv_bonus_qty=retRow.inv_bonus_qty
                prev_return_qty=retRow.prev_return_qty
                prev_return_bonus_qty=retRow.prev_return_bonus_qty
                
                quantity=inv_quantity-prev_return_qty
                bonus_qty=inv_bonus_qty-prev_return_bonus_qty
                
                retRow.update_record(quantity=quantity,bonus_qty=bonus_qty)
            
            session.flash='Available Qty Set successfully'
        
        redirect(URL(c='order_invoice',f='return_add',vars=dict(req_sl=req_sl,dptid=req_depot)))
    
    #---------- return with rules
    elif btn_return_apply_rules:#not used
        countRecords=db((db.sm_return.cid==c_id)& (db.sm_return.depot_id==req_depot) & (db.sm_return.sl==req_sl) & (db.sm_return.quantity>0)).count()
        if int(countRecords)==0:
            session.flash='At least one item`s quantity needs in a return'
        else:            
            retHeadRecords=db((db.sm_return_head.cid==c_id)&(db.sm_return_head.depot_id==req_depot)&(db.sm_return_head.sl==req_sl)&(db.sm_return_head.status=='Draft')).select(db.sm_return_head.ALL,limitby=(0,1))
            if not retHeadRecords:
                session.flash='Invalid request'
            else:
                depot_id=retHeadRecords[0].depot_id       
                invoice_sl=retHeadRecords[0].invoice_sl         
                store_id=retHeadRecords[0].store_id                
                client_id=retHeadRecords[0].client_id                
                inv_discount=retHeadRecords[0].inv_discount
                prev_return_discount=retHeadRecords[0].prev_return_discount
                
                promo_ref=0
                invhRows=db((db.sm_invoice_head.cid==c_id)& (db.sm_invoice_head.depot_id==req_depot) & (db.sm_invoice_head.sl==invoice_sl)).select(db.sm_invoice_head.promo_ref,db.sm_invoice_head.order_datetime,db.sm_invoice_head.delivery_date,db.sm_invoice_head.payment_mode,limitby=(0,1))
                if not invhRows:
                    session.flash='Invoice Sl not available'
                else:
                    promo_ref=invhRows[0].promo_ref
                    order_date=invhRows[0].order_datetime#order_date                
                    delivery_date=invhRows[0].delivery_date 
                    payment_mode=invhRows[0].payment_mode
                    if promo_ref!=0:
                        promo_ref=1
                    
                    retRows=db((db.sm_return.cid==c_id) & (db.sm_return.depot_id==req_depot)&(db.sm_return.sl==req_sl)).select(db.sm_return.ALL,orderby=db.sm_return.item_id)
                    detailList=[]
                    for retRow in retRows:
                        ret_rowid=str(retRow.id).strip()
                        item_id=str(retRow.item_id).strip().upper()
                        actual_tp=retRow.actual_tp                    
                        actual_vat=retRow.actual_vat
                        
                        inv_quantity=retRow.inv_quantity                    
                        prev_return_qty=retRow.prev_return_qty                    
                        quantity=retRow.quantity
                        availableQty=inv_quantity-(prev_return_qty+quantity)
                        
                        inv_price=retRow.inv_price
                        inv_item_vat=retRow.inv_item_vat                        
                        ret_price=retRow.price
                        ret_item_vat=retRow.item_vat
                        
                        if availableQty>0:                        
                            detailDict={'cid':c_id,'depot_id':req_depot,'return_sl':req_sl,'invoice_sl':invoice_sl,'ret_rowid':ret_rowid,'store_id':store_id,'client_id':client_id,'order_date':order_date,'delivery_date':delivery_date,
                                        'payment_mode':payment_mode,'inv_discount':inv_discount,'prev_return_discount':prev_return_discount,'promo_ref':promo_ref,'item_id':item_id,'actual_tp':actual_tp,'actual_vat':actual_vat,'quantity':availableQty,'ret_price':ret_price,'ret_item_vat':ret_item_vat,'inv_price':inv_price,'inv_item_vat':inv_item_vat}
                            detailList.append(detailDict)
                    
                    if len(detailList)>0:
                        #delete temp
                        db((db.sm_tp_rules_temp_return.cid==c_id) & (db.sm_tp_rules_temp_return.depot_id==req_depot)& (db.sm_tp_rules_temp_return.return_sl==req_sl)).delete()
                        
                        #insert temp
                        db.sm_tp_rules_temp_return.bulk_insert(detailList)
                        
                        return_sl=req_sl
                        retRes=get_rules_return(c_id,req_depot,return_sl,invoice_sl,client_id,order_date)
                        
                        #we get new invoice discount and bonus, after processing - return discount and return bonus qty will set
                        
                        #-------discount part                        
                        invPrevDiscount=inv_discount-prev_return_discount                        
                        newRetDiscount=0
                        restInvRows=db((db.sm_tp_rules_temp_return_invoice.cid==c_id) & (db.sm_tp_rules_temp_return_invoice.depot_id==req_depot) &(db.sm_tp_rules_temp_return_invoice.return_sl==req_sl)).select(db.sm_tp_rules_temp_return_invoice.discount,limitby=(0,1))
                        if restInvRows:
                            newInvDiscount=restInvRows[0].discount
                        newRetDiscount=round(invPrevDiscount-newInvDiscount,2)
                        
                        db((db.sm_return_head.cid==c_id)& (db.sm_return_head.depot_id==req_depot) & (db.sm_return_head.sl==req_sl)).update(discount=newRetDiscount)
                        db((db.sm_return.cid==c_id)& (db.sm_return.depot_id==req_depot) & (db.sm_return.sl==req_sl)).update(discount=newRetDiscount,bonus_qty=0)
                        
                        #-------
                        retRows1=db((db.sm_return.cid==c_id) & (db.sm_return.depot_id==req_depot)&(db.sm_return.sl==req_sl)&(db.sm_return.inv_quantity==0)).select(db.sm_return.id,db.sm_return.inv_bonus_qty,db.sm_return.prev_return_bonus_qty,orderby=db.sm_return.item_id)
                        for retRow1 in retRows1:
                            inv_bonus_available_qty=retRow1.inv_bonus_qty-retRow1.prev_return_bonus_qty 
                            retRow1.update_record(bonus_qty=inv_bonus_available_qty)
                            
                        #------------ bonus qty
                        restInvRows2=db((db.sm_tp_rules_temp_return_invoice.cid==c_id) & (db.sm_tp_rules_temp_return_invoice.depot_id==req_depot)&(db.sm_tp_rules_temp_return_invoice.return_sl==req_sl)).select(db.sm_tp_rules_temp_return_invoice.item_id,db.sm_tp_rules_temp_return_invoice.bonus_qty.sum(),orderby=db.sm_tp_rules_temp_return_invoice.item_id,groupby=db.sm_tp_rules_temp_return_invoice.item_id)
                        for restInvRow2 in restInvRows2:
                            newInv_item_id=restInvRow2.sm_tp_rules_temp_return_invoice.item_id
                            newInv_bonus_qty=restInvRow2[db.sm_tp_rules_temp_return_invoice.bonus_qty.sum()]
                            
                            retRows2=db((db.sm_return.cid==c_id) & (db.sm_return.depot_id==req_depot)&(db.sm_return.sl==req_sl)&(db.sm_return.item_id==newInv_item_id)&(db.sm_return.inv_bonus_qty>0)).select(db.sm_return.id,db.sm_return.inv_bonus_qty,db.sm_return.prev_return_bonus_qty,orderby=db.sm_return.item_id)
                            for retRow2 in retRows2:
                                inv_bonus_qty_available=retRow2.inv_bonus_qty-retRow2.prev_return_bonus_qty   
                                
                                newRetBQty=inv_bonus_qty_available-newInv_bonus_qty
                                
                                if newRetBQty<0:
                                    retRow2.update_record(bonus_qty=inv_bonus_qty_available)
                                    newInv_bonus_qty=newInv_bonus_qty-inv_bonus_qty_available                                    
                                else:
                                    retRow2.update_record(bonus_qty=newRetBQty)
                                    break
                        
                        #------------ return rate
#                         restInvRows3=db((db.sm_tp_rules_temp_return_invoice.cid==c_id) & (db.sm_tp_rules_temp_return_invoice.depot_id==req_depot)&(db.sm_tp_rules_temp_return_invoice.return_sl==req_sl)&(db.sm_tp_rules_temp_return_invoice.quantity>0)).select(db.sm_tp_rules_temp_return_invoice.item_id,db.sm_tp_rules_temp_return_invoice.quantity,db.sm_tp_rules_temp_return_invoice.price,db.sm_tp_rules_temp_return_invoice.item_vat,db.sm_tp_rules_temp_return_invoice.ret_rowid,orderby=db.sm_tp_rules_temp_return_invoice.item_id|db.sm_tp_rules_temp_return_invoice.ret_rowid)
#                         for restInvRow3 in restInvRows3:
#                             newInv_itemId=restInvRow3.item_id
#                             newInv_ret_rowid=restInvRow3.ret_rowid
#                             newInv_quantity=restInvRow3.quantity
#                             newInv_price=restInvRow3.price
#                             newInv_item_vat=restInvRow3.item_vat
#                             
#                             retRows2=db((db.sm_return.cid==c_id) & (db.sm_return.depot_id==req_depot)&(db.sm_return.sl==req_sl)&(db.sm_return.item_id==newInv_itemId)&(db.sm_return.id==newInv_ret_rowid)).select(db.sm_return.id,db.sm_return.price,db.sm_return.item_vat,db.sm_return.price,db.sm_return.inv_price,db.sm_return.price,db.sm_return.inv_item_vat,orderby=db.sm_return.item_id)
#                             for retRow2 in retRows2:                                
#                                 retPrice=retRow2.price
#                                 retVat=retRow2.item_vat                                                                    
#                                 retInvPrice=retRow2.inv_price
#                                 retInvVatPrice=retRow2.inv_item_vat                                
#                                 if newInv_price!=retInvPrice:
#                                     continue
                                    #retRow2.update_record(price=newInv_price,item_vat=newInv_item_vat)
                        
                        session.flash=retRes
                    else:
                        session.flash='Partial return not available, Full return ready'
                        
        redirect(URL(c='order_invoice',f='return_add',vars=dict(req_sl=req_sl,dptid=req_depot)))
    
    #---------- Returned - CANCELLED
    elif btn_return_cancel:
        countRecords=db((db.sm_return.cid==c_id)& (db.sm_return.depot_id==req_depot) & (db.sm_return.sl==req_sl)).count()
        if int(countRecords)==0:
            session.flash='At least one item needs in a return!'
        else:
            if check_return!='YES':
                session.flash='Required checked confirmation'
            else:
                #----------------- check stock cron flag
                autDelCronRows=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==req_depot)&(db.sm_depot.auto_del_cron_flag==0)).select(db.sm_depot.id,db.sm_depot.cid,limitby=(0,1))
                if not autDelCronRows:
                    session.flash='One process running, please try again'
                else:
                    autDelCronRows[0].update_record(auto_del_cron_flag=1)
                    #-------------
                    
                    totalAmount=0
                    total_tp_amount=0
                    total_vat_amount=0
                    discount=0
                    
                    ret_actual_total_tp=0
                    ret_regular_disc_tp=0
                    ret_flat_disc_tp=0
                    ret_approved_disc_tp=0
                    ret_others_disc_tp=0                    
                    ret_sp_flat=0
                    ret_sp_approved=0
                    ret_sp_others=0
                    
                    headRow=db((db.sm_return_head.cid==c_id)& (db.sm_return_head.depot_id==req_depot) & (db.sm_return_head.sl==req_sl)).select(db.sm_return_head.ALL,limitby=(0,1))
                    if not headRow:
                        session.flash='Invalid request'
                    else:
                        client_id=str(headRow[0].client_id)
                        invoiceSl=headRow[0].invoice_sl
                        
                        totalAmount=float(headRow[0].total_amount)
                        total_vat_amount=float(headRow[0].vat_total_amount)
                        discount=float(headRow[0].discount)
                        sp_discount=float(headRow[0].sp_discount)
                        
                        total_tp_amount=round(totalAmount+discount-total_vat_amount,2)
                        
                        #-----------------
                        ret_actual_total_tp=float(headRow[0].ret_actual_total_tp)
                        ret_regular_disc_tp=float(headRow[0].ret_regular_disc_tp)
                        ret_flat_disc_tp=float(headRow[0].ret_flat_disc_tp)
                        ret_approved_disc_tp=float(headRow[0].ret_approved_disc_tp)
                        ret_others_disc_tp=float(headRow[0].ret_others_disc_tp)                           
                        ret_sp_flat=float(headRow[0].ret_sp_flat)
                        ret_sp_approved=float(headRow[0].ret_sp_approved)
                        ret_sp_others=float(headRow[0].ret_sp_others)
                        #------------------
                        
                        rows=db((db.sm_return.cid==c_id)& (db.sm_return.depot_id==req_depot) & (db.sm_return.sl==req_sl) & ((db.sm_return.quantity>0)|(db.sm_return.bonus_qty>0))).select(db.sm_return.ALL,orderby=db.sm_return.item_id)
                        if not rows:
                            session.flash='Required Qty/Bonus Qty' 
                        else:
                            resStr=''
                            
                            if session.ledgerCreate=='YES':                                
                                #-------------
                #                strData=strData+rep_id+'<fdfd>'+client_id+'<fdfd>'+str(totalAmount)
                                
                                #strData=str(c_id)+'<fdfd>PAYMENTCLT<fdfd>'+str(slNo)+'<fdfd>'+str(datetime_fixed)+'<fdfd>'+str(depotId)+'-'+str(slNo)+'<fdfd>DPT-'+str(depotId)+'<fdfd>CLT-'+str(clientID)+'<fdfd>'+str(amount)
                                
                                strData=str(c_id)+'<fdfd>RETURNCANCEL<fdfd>'+str(req_sl)+'<fdfd>'+str(datetime_fixed)+'<fdfd>'+str(req_depot)+'-'+str(req_sl)+'<fdfd>DPT-'+str(req_depot)+'<fdfd>CLT-'+str(client_id)+'<fdfd>'+str(totalAmount)
                                resStr=set_balance_transaction(strData)
                                resStrList=resStr.split('<sep>',resStr.count('<sep>'))
                                flag=resStrList[0]
                                msg=resStrList[1]                        
                            else:
                                flag='True'
                                msg='Success'
                                
                            if flag=='True':
                                db((db.sm_return.cid==c_id)& (db.sm_return.depot_id==req_depot) & (db.sm_return.sl==req_sl)).update(status='Cancelled')
                                db((db.sm_return_head.cid==c_id)& (db.sm_return_head.depot_id==req_depot) & (db.sm_return_head.sl==req_sl)).update(status='Cancelled')
                                
                                db((db.sm_invoice.cid==c_id) & (db.sm_invoice.depot_id==req_depot) &(db.sm_invoice.sl==invoiceSl)).update(note='')
                                invHRow=db((db.sm_invoice_head.cid==c_id) & (db.sm_invoice_head.depot_id==req_depot) &(db.sm_invoice_head.sl==invoiceSl)).select(db.sm_invoice_head.id,db.sm_invoice_head.return_tp,db.sm_invoice_head.return_vat,db.sm_invoice_head.return_discount,db.sm_invoice_head.return_sp_discount,db.sm_invoice_head.return_count,db.sm_invoice_head.actual_total_tp,db.sm_invoice_head.regular_disc_tp,db.sm_invoice_head.flat_disc_tp,db.sm_invoice_head.approved_disc_tp,db.sm_invoice_head.others_disc_tp,db.sm_invoice_head.sp_flat,db.sm_invoice_head.sp_approved,db.sm_invoice_head.sp_others,db.sm_invoice_head.ret_actual_total_tp,db.sm_invoice_head.ret_regular_disc_tp,db.sm_invoice_head.ret_flat_disc_tp,db.sm_invoice_head.ret_approved_disc_tp,db.sm_invoice_head.ret_others_disc_tp,db.sm_invoice_head.ret_sp_flat,db.sm_invoice_head.ret_sp_approved,db.sm_invoice_head.ret_sp_others,limitby=(0,1))
                                if invHRow:
                                    return_tp=float(invHRow[0].return_tp)-round(total_tp_amount,2)
                                    return_vat=float(invHRow[0].return_vat)-total_vat_amount
                                    return_discount=float(invHRow[0].return_discount)-discount
                                    return_sp_discount=float(invHRow[0].return_sp_discount)-sp_discount
                                    return_count=int(invHRow[0].return_count)
                                    return_countTotal=return_count-1
                                    
                                    if return_tp==0:
                                        discount=0
                                        
                                    #-------------------                                    
                                    ret_actual_total_tp=float(invHRow[0].ret_actual_total_tp)-ret_actual_total_tp
                                    ret_regular_disc_tp=float(invHRow[0].ret_regular_disc_tp)-ret_regular_disc_tp
                                    ret_flat_disc_tp=float(invHRow[0].ret_flat_disc_tp)-ret_flat_disc_tp
                                    ret_approved_disc_tp=float(invHRow[0].ret_approved_disc_tp)-ret_approved_disc_tp
                                    ret_others_disc_tp=float(invHRow[0].ret_others_disc_tp)-ret_others_disc_tp                                
                                    ret_sp_flat=float(invHRow[0].ret_sp_flat)-ret_sp_flat
                                    ret_sp_approved=float(invHRow[0].ret_sp_approved)-ret_sp_approved
                                    ret_sp_others=float(invHRow[0].ret_sp_others)-ret_sp_others
                                    if ret_flat_disc_tp==0:
                                        ret_sp_flat=0
                                    if ret_approved_disc_tp==0:
                                        ret_sp_approved=0
                                    if ret_others_disc_tp==0:
                                        ret_sp_others=0
                                        
                                    #------------------                                    
                                    invHRow[0].update_record(ret_actual_total_tp=round(ret_actual_total_tp,2),ret_regular_disc_tp=round(ret_regular_disc_tp,2),ret_flat_disc_tp=round(ret_flat_disc_tp,2),ret_approved_disc_tp=round(ret_approved_disc_tp,2),ret_others_disc_tp=round(ret_others_disc_tp,2),ret_sp_flat=round(ret_sp_flat,2),ret_sp_approved=round(ret_sp_approved,2),ret_sp_others=round(ret_sp_others,2),note='',return_tp=round(return_tp,2),return_vat=round(return_vat,2),return_discount=round(return_discount,2),return_sp_discount=round(return_sp_discount,2),return_count=return_countTotal)
                                
                                cancelList=[]
                                #-------------------
                                for row in rows:
                                    store_id=row.store_id       
                                    item_id=row.item_id
                                    batch_id=row.batch_id
                                    invdet_rowid=row.invdet_rowid
                                    
                                    quantity=int(row.quantity)
                                    bonus_qty=int(row.bonus_qty)
                                    actual_tp=float(row.actual_tp)                                
                                    price=float(row.price)
                                    #item_vat=float(row.item_vat)
                                    
                                    totalQty=quantity+bonus_qty
                                    
                                    ret_discount_type_quantity=int(row.ret_discount_type_quantity)
                                    
                                    #---------------------- for cancel table                                    
                                    cancelList.append({'cid':row.cid,'depot_id':row.depot_id,'depot_name':row.depot_name,'sl':row.sl,'store_id':row.store_id,'store_name':row.store_name,'client_id':row.client_id,'client_name':row.client_name,'rep_id':row.rep_id,'rep_name':row.rep_name,'market_id':row.market_id,'market_name':row.market_name,'d_man_id':row.d_man_id,'d_man_name':row.d_man_name,'shipment_no':row.shipment_no,'invoice_date':row.invoice_date,'invoice_ym_date':row.invoice_ym_date,
                                                       'return_date':row.return_date,'ret_reason':row.ret_reason,'order_sl':row.order_sl,'invoice_sl':row.invoice_sl,'area_id':row.area_id,'area_name':row.area_name,'level0_id':row.level0_id,'level0_name':row.level0_name,'level1_id':row.level1_id,'level1_name':row.level1_name,'level2_id':row.level2_id,'level2_name':row.level2_name,'level3_id':row.level3_id,'level3_name':row.level3_name,'cl_category_id':row.cl_category_id,'cl_category_name':row.cl_category_name,
                                                       'cl_sub_category_id':row.cl_sub_category_id,'cl_sub_category_name':row.cl_sub_category_name,'special_territory_code':row.special_territory_code,'status':'Cancelled','order_media':row.order_media,'device_user_agent':row.device_user_agent,'ip_ref':row.ip_ref,'discount':row.discount,'item_id':row.item_id,'item_name':row.item_name,'batch_id':row.batch_id,'category_id':row.category_id,
                                                       'actual_tp':row.actual_tp,'actual_vat':row.actual_vat,'quantity':row.quantity,'bonus_qty':row.bonus_qty,'price':row.price,'item_vat':row.item_vat,'item_unit':row.item_unit,'item_carton':row.item_carton,'inv_promotion_type':row.inv_promotion_type,'inv_bonus_applied_on_qty':row.inv_bonus_applied_on_qty,'inv_circular_no':row.inv_circular_no,'discount_type':row.discount_type,'item_discount':row.item_discount,'inv_item_discount_percent':row.inv_item_discount_percent,'inv_discount_type_quantity':row.inv_discount_type_quantity,'return_item_discount':row.return_item_discount,'ret_discount_type_quantity':row.ret_discount_type_quantity,'short_note':row.short_note,
                                                       'inv_quantity':row.inv_quantity,'inv_bonus_qty':row.inv_bonus_qty,'inv_price':row.inv_price,'inv_item_vat':row.inv_item_vat,'prev_return_qty':row.prev_return_qty,'prev_return_bonus_qty':row.prev_return_bonus_qty,'inv_discount':row.inv_discount,'prev_return_discount':row.prev_return_discount,'invdet_rowid':row.invdet_rowid,'sp_discount_item':row.sp_discount_item,'inv_sp_discount_item':row.inv_sp_discount_item,'prev_return_sp_discount_item':row.prev_return_sp_discount_item,'ym_date':row.ym_date,
                                                       'depot_status':row.depot_status,'ho_status':row.ho_status,'flag_depot_stock':row.flag_depot_stock,'flag_depot_stock_balance':row.flag_depot_stock_balance,'flag_data':row.flag_data,'returned_on':row.returned_on,'returned_by':row.returned_by,'field1':row.field1,'field2':row.field2,'note':row.note})
                                    
                                    #--------- invoice details update
                                    invDetRow=db((db.sm_invoice.cid==c_id) & (db.sm_invoice.depot_id==req_depot) &(db.sm_invoice.sl==invoiceSl)&(db.sm_invoice.item_id==item_id)&(db.sm_invoice.batch_id==batch_id)&(db.sm_invoice.id==invdet_rowid)).select(db.sm_invoice.id,db.sm_invoice.return_qty,db.sm_invoice.return_bonus_qty,db.sm_invoice.ret_discount_type_quantity,limitby=(0,1))
                                    if invDetRow:
                                        return_qty=int(invDetRow[0].return_qty)-quantity
                                        return_bonus_qty=int(invDetRow[0].return_bonus_qty)-bonus_qty
                                        
                                        return_disc_typeQty=int(invDetRow[0].ret_discount_type_quantity)-ret_discount_type_quantity
                                        
                                        invDetRow[0].update_record(return_qty=return_qty,return_bonus_qty=return_bonus_qty,return_rate=price,ret_discount_type_quantity=return_disc_typeQty)
                                        
                                    #---------
                                    balanceRecords=db((db.sm_depot_stock_balance.cid==c_id)&(db.sm_depot_stock_balance.depot_id==req_depot)&(db.sm_depot_stock_balance.store_id==store_id)&(db.sm_depot_stock_balance.item_id==item_id)&(db.sm_depot_stock_balance.batch_id==batch_id)).select(db.sm_depot_stock_balance.id,db.sm_depot_stock_balance.quantity,limitby=(0,1))
                                    if balanceRecords:
                                        balance_Qty=balanceRecords[0].quantity-totalQty
                                        balanceRecords[0].update_record(quantity=balance_Qty)
                                    else:
                                        continue
                                
                                if len(cancelList)>0:
                                    db.sm_return_cancel.bulk_insert(cancelList)
                                    
                                session.flash='Cancelled successfully'   
                         
                    #---------------------
                    autDelCronRows[0].update_record(auto_del_cron_flag=0)
                    db.commit()
                    #--------------
                    
        redirect(URL(c='order_invoice',f='return_add',vars=dict(req_sl=req_sl,dptid=req_depot)))
        
    return dict()

# ret db discount distribute
def dist_discount_distribute_inv(inv_rowid):
    inv_rowid=str(inv_rowid)

    invHeadRows = "select id,cid,depot_id,sl,actual_total_tp,ret_dist_discount from sm_invoice_head where id='"+inv_rowid+"';"
    invHeadRows = db.executesql(invHeadRows, as_dict=True)

    for i in range(len(invHeadRows)):
        invHeadRowsS = invHeadRows[i]

        row_id = invHeadRowsS['id']
        c_id = invHeadRowsS['cid']
        req_depot = invHeadRowsS['depot_id']
        req_sl = invHeadRowsS['sl']
        actual_total_tp = invHeadRowsS['actual_total_tp']
        dist_discount = invHeadRowsS['ret_dist_discount']

        invRows = db((db.sm_invoice.cid == c_id) & (db.sm_invoice.depot_id == req_depot) & (db.sm_invoice.sl == req_sl) & (db.sm_invoice.status == 'Invoiced') & (db.sm_invoice.quantity > 0)).select(db.sm_invoice.id, db.sm_invoice.actual_tp, db.sm_invoice.quantity)

        for row in invRows:
            actual_tp = float(row.actual_tp)
            quantity = int(row.quantity)

            total_tp=float(actual_tp*quantity)

            dist_discount_item=round((float(dist_discount)/float(actual_total_tp))*float(total_tp),6)

            row.update_record(ret_dist_discount_item=dist_discount_item)

    return 'Done'

#========================= Show Invoice
def show_invoice():
    c_id=session.cid
    req_depot=request.args(0)
    req_sl=request.args(1)

    #--------------- Title
    response.title='Preview Invoice'
    #-------------
    
    #----------- 
    depot_id=''
    depotName=''
    sl=0
    order_sl=0
    order_datetime=''
    delivery_date=''
    client_id=''
    client_name=''
    rep_id=''
    rep_name=''
    d_man_id=''
    d_man_name=''
    area_id=''
    area_name=''
    payment_mode=''
    discount=0
    req_note=''
    status=''
    store_id=''
    store_name=''
    
    headRecords=db((db.sm_invoice_head.cid==c_id)& (db.sm_invoice_head.depot_id==req_depot) & (db.sm_invoice_head.sl==req_sl)).select(db.sm_invoice_head.ALL,limitby=(0,1))
    if headRecords:        
        depot_id=headRecords[0].depot_id
        depotName=headRecords[0].depot_name
        sl=headRecords[0].sl
        
        order_sl=headRecords[0].order_sl
        order_datetime=headRecords[0].order_datetime
        delivery_date=headRecords[0].delivery_date
        
        client_id=headRecords[0].client_id
        client_name=headRecords[0].client_name
        rep_id=headRecords[0].rep_id      
        rep_name=headRecords[0].rep_name
        d_man_id=headRecords[0].d_man_id      
        d_man_name=headRecords[0].d_man_name
        area_id=headRecords[0].area_id      
        area_name=headRecords[0].area_name 
        
        payment_mode=headRecords[0].payment_mode    
        discount=headRecords[0].discount                     
        req_note=headRecords[0].note
        status=headRecords[0].status
        store_id=headRecords[0].store_id
        store_name=headRecords[0].store_name
    
    #----------- 
    showList=[]
    detailRecords=db((db.sm_invoice.cid==c_id)& (db.sm_invoice.depot_id==req_depot) & (db.sm_invoice.sl==req_sl)).select(db.sm_invoice.item_id,db.sm_invoice.item_name,db.sm_invoice.batch_id,db.sm_invoice.category_id,db.sm_invoice.quantity,db.sm_invoice.bonus_qty,db.sm_invoice.price,db.sm_invoice.item_vat,db.sm_invoice.short_note,orderby=db.sm_invoice.item_name)
    showList=detailRecords.as_list()
    
    #------------------- print status (field2) update
    db((db.sm_invoice_head.cid==c_id)& (db.sm_invoice_head.depot_id==depot_id) & (db.sm_invoice_head.sl==req_sl)).update(field2=1)      
    
    return dict(showList=showList,depot_id=depot_id,depotName=depotName,sl=sl,store_id=store_id,store_name=store_name,order_sl=order_sl,order_datetime=order_datetime,delivery_date=delivery_date,
                client_id=client_id,client_name=client_name,rep_id=rep_id,rep_name=rep_name,d_man_id=d_man_id,d_man_name=d_man_name,area_id=area_id,area_name=area_name,payment_mode=payment_mode,discount=discount,req_note=req_note,status=status)


#Preview order
def show_order():
    c_id=session.cid
    req_depot=request.args(0)
    req_sl=request.args(1)
    
    #--------------- Title
    response.title='Preview Order'
    #-------------

    #----------- 
    depot_id=''
    depotName=''
    sl=0
    order_datetime=''
    delivery_date=''
    client_id=''
    client_name=''
    rep_id=''
    rep_name=''
    payment_mode=''
    req_note=''
    status=''
    level0_id=''
    level0_name=''
    level1_id=''
    level1_name=''
    level2_id=''
    level2_name=''
    level3_id=''
    level3_name=''
    #Get head record
    headRecords=db((db.sm_order_head.cid==c_id)& (db.sm_order_head.depot_id==req_depot) & (db.sm_order_head.sl==req_sl)).select(db.sm_order_head.ALL,limitby=(0,1))
    for row in headRecords:        
        depot_id=row.depot_id
        depotName=row.depot_name
        sl=row.sl

        order_datetime=row.order_datetime
        delivery_date=row.delivery_date
        
        client_id=row.client_id
        client_name=row.client_name
        rep_id=row.rep_id
        rep_name=row.rep_name  
        payment_mode=row.payment_mode                      
        req_note=row.note
        status=row.status      
        level0_id=row.level0_id
        level0_name=row.level0_name
        level1_id=row.level1_id
        level1_name=row.level1_name
        level2_id=row.level2_id
        level2_name=row.level2_name
        level3_id=row.level3_id
        level3_name=row.level3_name  
        break    
    
    #Get record for detail and treat as list
    showList=[]
    detailRecords=db((db.sm_order.cid==c_id)& (db.sm_order.depot_id==req_depot) & (db.sm_order.sl==req_sl)
                     ).select(db.sm_order.item_id,db.sm_order.item_name,db.sm_order.category_id,db.sm_order.quantity,db.sm_order.price,db.sm_order.item_vat)
    showList=detailRecords.as_list()
    #-----
    
#    depotRows=db((db.sm_depot.cid==c_id) & (db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
#    if depotRows:
#        depotName=depotRows[0].name
    
    return dict(showList=showList,depot_id=depot_id,depotName=depotName,sl=sl,order_datetime=order_datetime,delivery_date=delivery_date,
                client_id=client_id,client_name=client_name,rep_id=rep_id,rep_name=rep_name,payment_mode=payment_mode,req_note=req_note,level0_id=level0_id,level0_name=level0_name,level1_id=level1_id,level1_name=level1_name,level2_id=level2_id,level2_name=level2_name,level3_id=level3_id,level3_name=level3_name,status=status)


#========================= Show Return
def show_return():
    c_id=session.cid
    req_depot=request.args(0)
    req_sl=request.args(1)
    
    #--------------- Title
    response.title='Preview Return'
    #-------------
    
    #----------- 
    depot_id=''
    depotName=''
    sl=0
    order_sl=0
    invoice_sl=0
    return_date=''
    client_id=''
    rep_id=''
    client_name=''
    rep_name=''
    req_note=''
    status=''
    discount=0
    cause=0
    updatedBy=''
    #Get head record
    headRecords=db((db.sm_return.cid==c_id)& (db.sm_return.depot_id==req_depot) & (db.sm_return.sl==req_sl)).select(db.sm_return.ALL,limitby=(0,1))
    for row in headRecords:
        depot_id=row.depot_id
        depotName=row.depot_name
        sl=row.sl
        
        order_sl=row.order_sl
        invoice_sl=row.invoice_sl
        return_date=row.return_date
        
        client_id=row.client_id
        client_name=row.client_name
        rep_id=row.rep_id
        rep_name=row.rep_name
        discount=row.discount
        req_note=row.note
        status=row.status
        cause=row.ret_reason
        updatedBy=row.updated_by
        
        break
    
    #Get record for detail and treat as list
    showList=[]
    detailRecords=db((db.sm_return.cid==c_id)& (db.sm_return.depot_id==req_depot) & (db.sm_return.sl==req_sl)).select(db.sm_return.ALL,orderby=db.sm_return.item_id)
    showList=detailRecords.as_list()
    
    #-----
    
#    depotRows=db((db.sm_depot.cid==c_id) & (db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
#    if depotRows:
#        depotName=depotRows[0].name
        
    return dict(showList=showList,depot_id=depot_id,depotName=depotName,sl=sl,order_sl=order_sl,invoice_sl=invoice_sl,return_date=return_date,
                client_id=client_id,rep_id=rep_id,client_name=client_name,rep_name=rep_name,req_note=req_note,status=status,discount=discount,cause=cause,updatedBy=updatedBy)
    

#========================= Show Return Note
def show_return_note():
    c_id=session.cid
    req_depot=request.args(0)
    req_sl=request.args(1)
    
    #--------------- Title
    response.title='Return Note'
    #-------------
    
    #----------- 
    depot_id=''
    depotName=''
    sl=0
    order_sl=0
    invoice_sl=0
    return_date=''
    client_id=''
    rep_id=''
    client_name=''
    rep_name=''
    req_note=''
    status=''
    discount=0
    cause=0
    updatedBy=''
    
    d_man_id=''
    d_man_name=''
    payment_mode=''
    inv_discount=0
    discount_precent=0
    prev_return_discount=0
    
    level0_name=''
    address=''
    category_name=''
    market_name=''
    contact_no1=''
    district=''
    area_name=''
    store_id=''
    store_name=''
    invoice_date=''
    order_date=''
    #Get head record
    headRecords=db((db.sm_return.cid==c_id)& (db.sm_return.depot_id==req_depot) & (db.sm_return.sl==req_sl)).select(db.sm_return.ALL,limitby=(0,1))
    for row in headRecords:
        depot_id=row.depot_id
        depotName=row.depot_name
        store_id=row.store_id
        store_name=row.store_name
        
        sl=row.sl        
        order_sl=row.order_sl
        invoice_sl=row.invoice_sl
        return_date=row.return_date
        
        client_id=row.client_id
        client_name=row.client_name
        rep_id=row.rep_id
        rep_name=row.rep_name
        level0_name=row.level0_name
        level2_name=row.level2_name
        area_name=row.area_name
        
        discount=row.discount
        req_note=row.note
        status=row.status
        cause=row.ret_reason
        updatedBy=row.updated_by
        inv_discount=row.inv_discount
        prev_return_discount=row.prev_return_discount
        
        invRecords=db((db.sm_invoice_head.cid==c_id)& (db.sm_invoice_head.depot_id==depot_id) & (db.sm_invoice_head.sl==invoice_sl)).select(db.sm_invoice_head.ALL,limitby=(0,1))
        if invRecords:
            d_man_id=invRecords[0].d_man_id      
            d_man_name=invRecords[0].d_man_name
            payment_mode=invRecords[0].payment_mode
            discount_precent=invRecords[0].discount_precent
            invoice_date=invRecords[0].invoice_date.strftime('%d-%b-%Y')
            order_date=invRecords[0].order_datetime.strftime('%d-%b-%Y')
        #-------------
        clientRows=db((db.sm_client.cid==c_id)& (db.sm_client.depot_id==depot_id) & (db.sm_client.client_id==client_id)).select(db.sm_client.ALL,limitby=(0,1))
        if clientRows:
            address=clientRows[0].address
            category_name=clientRows[0].category_name
            market_name=clientRows[0].market_name
            contact_no1=clientRows[0].contact_no1
            district=clientRows[0].district            
        break
        
    #Get record for detail and treat as list
    showList=[]
    detailRecords=db((db.sm_return.cid==c_id)& (db.sm_return.depot_id==req_depot) & (db.sm_return.sl==req_sl)).select(db.sm_return.ALL,orderby=db.sm_return.item_name)
    showList=detailRecords.as_list()
    
    #-----
    
    return dict(showList=showList,depot_id=depot_id,depotName=depotName,sl=sl,order_sl=order_sl,invoice_sl=invoice_sl,return_date=return_date,client_id=client_id,rep_id=rep_id,client_name=client_name,rep_name=rep_name,d_man_id=d_man_id,d_man_name=d_man_name,area_name=area_name,store_id=store_id,store_name=store_name,invoice_date=invoice_date,order_date=order_date,
                level2_name=level2_name,payment_mode=payment_mode,req_note=req_note,status=status,discount=discount,cause=cause,updatedBy=updatedBy,inv_discount=inv_discount,prev_return_discount=prev_return_discount,discount_precent=discount_precent,level0_name=level0_name,address=address,category_name=category_name,market_name=market_name,contact_no1=contact_no1,district=district)
    

#========================= Client Payment
#validation for client payment
#field1=payment category


def client_payment_validation(form):
    c_id=session.cid
    amount=0
    
    depot_id=str(request.vars.depot_id).strip()
    rep_id=str(request.vars.rep_id).strip().upper()
    client_id=str(request.vars.client_id).strip().upper()
    amount=float(request.vars.amount)
    confirmAmt=request.vars.confirmAmt
    
    try:
        confirmAmt=float(confirmAmt)
    except:
        confirmAmt=0
        
    if amount<=0:
        form.errors.amount=''
        response.flash = 'need valid amount!'
    else:
        if (amount!=confirmAmt):
            form.errors.amount=''
            response.flash = 'invalid confirm amount'
        else:
            amount=((amount*100)//1)/100
            form.vars.amount=amount
            
            if depot_id=='' or depot_id==None:
                form.errors.rep_id=''
                response.flash = 'invalid depot!'
            else:
                repRows=db((db.sm_rep.cid==c_id)& (db.sm_rep.user_type=='rep')& (db.sm_rep.depot_id==depot_id) & (db.sm_rep.rep_id==rep_id)).select(db.sm_rep.name,limitby=(0,1))
                if not repRows:
                    form.errors.rep_id='invalid rep for this depot'
                else:
                    clientRows=db((db.sm_client.cid==c_id)& (db.sm_client.depot_id==depot_id) & (db.sm_client.client_id==client_id)).select(db.sm_client.area_id,db.sm_client.name,orderby=db.sm_client.name,limitby=(0,1))
                    if not clientRows:
                        form.errors.client_id='invalid client for this depot'
                    else:
                        area_id=''
                        client_name=''
                        for row in clientRows:
                            area_id=row.area_id
                            client_name=row.name
                            break
                        
                        #----------
                        rep_name=''
                        rep_name=repRows[0].name
                        #Get max sl
                        maxSl=0
                        records=db((db.sm_depot.cid==c_id) & (db.sm_depot.depot_id==depot_id)).select(db.sm_depot.id,db.sm_depot.client_payment_sl,limitby=(0,1))
                        if records:
                            sl=records[0].client_payment_sl
                            if sl==None or sl=='':
                                sl=0                            
                            maxSl=int(sl)+1                        
                        else:
                            maxSl=1
                        
                        # sl update in depot
                        records[0].update_record(client_payment_sl=maxSl)
                        
                        form.vars.sl=maxSl
                        
                        form.vars.depot_id=depot_id
                        form.vars.rep_id=rep_id
                        form.vars.rep_name=rep_name
                        form.vars.client_id=client_id
                        form.vars.client_name=client_name
                        form.vars.area_id=area_id


def client_payment():
    response.title='Client-Payment'
    #Check access permission
    #----------Task assaign----------
    task_id='rm_client_payment_manage'
    task_id_view='rm_client_payment_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL(c='default', f='home'))      
#   ---------------------    
    c_id=session.cid
    depot_id=session.depot_id

    form =SQLFORM(db.sm_client_payment,
                  fields=['rep_id','client_id','area_id','paytype','pay_date','amount','narration'],
                  submit_button='Post'       
                  )
    
    form.vars.cid=session.cid
    form.vars.depot_id=depot_id
    form.vars.field1='CP'   # field1 =payment Category, CP=Client Payment, PTC= Payment To Client
    
    #Insert after validation 
    if form.accepts(request.vars,session,onvalidation=client_payment_validation):
        depotId=form.vars.depot_id
        clientID=form.vars.client_id  
        pay_date=form.vars.pay_date
        amount=form.vars.amount 
        slNo=form.vars.sl
       
       #Create string for client_payment_balance
#       strData=str(c_id)+'<fdfd>'+str(depotId)+'<fdfd>'+str(clientID)+'<fdfd>'+str(amount)
       #format:cid<fdfd>tx_type<fdfd>sl<fdfd>datetime<fdfd>reference<fdfd>1st account with prefix (cr)<fdfd>2nd account with prefix (dr)<fdfd>tx_amount
        
        if session.ledgerCreate=='YES':
            strData=str(c_id)+'<fdfd>CLTPAYMENT<fdfd>'+str(slNo)+'<fdfd>'+str(datetime_fixed)+'<fdfd>'+str(depotId)+'-'+str(slNo)+'<fdfd>CLT-'+str(clientID)+'<fdfd>DPT-'+str(depotId)+'<fdfd>'+str(amount)
            resStr=set_balance_transaction(strData) 
            resStrList=resStr.split('<sep>',resStr.count('<sep>'))
            flag=resStrList[0]
            msg=resStrList[1]
        else:
            flag='True'
            msg='Success'
            
        
        if flag=='True':
            response.flash = msg
        else:
            db.rollback()
            response.flash = msg
        
    
    #   --------------------------- filter--------------------------
    btn_filter_clientpay=request.vars.btn_filter
    btn_filter_all=request.vars.btn_filter_all
    reqPage=len(request.args)
    if btn_filter_clientpay:
        client_id_value=request.vars.client_id_value
        
        session.btn_filter_clientpay=btn_filter_clientpay
        session.client_id_value_clientpay=client_id_value.upper()
        reqPage==0
        
    elif btn_filter_all:
        session.btn_filter_clientpay=None
        session.client_id_value_clientpay=None
        
        reqPage=0
    
    #--------paging
    if reqPage:
        page=int(reqPage)
    else:
        page=0
    items_per_page=session.items_per_page
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #--------end paging
    
    qset=db()
    qset=qset(db.sm_client_payment.cid==c_id)
    qset=qset(db.sm_client_payment.field1=='CP')
    
    if session.user_type=='Depot':
        qset=qset(db.sm_client_payment.depot_id==session.depot_id)
    
    if (session.btn_filter_clientpay):
        searchValue=str(session.client_id_value_clientpay).split('|')[0]
        qset=qset(db.sm_client_payment.client_id==searchValue)
    
    records=qset.select(db.sm_client_payment.ALL,orderby=~db.sm_client_payment.id,limitby=limitby)
    
    return dict(form=form,depot_id=depot_id,records=records,page=page,items_per_page=items_per_page,access_permission=access_permission,access_permission_view=access_permission_view)
    

def preview_client_payment():
    #----------Task assaign----------
    task_id='rm_client_payment_manage'
    task_id_view='rm_client_payment_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL(c='default', f='home'))
    
    #------------------------
    c_id=session.cid
    depot_id=request.vars.depotId
    sl=request.vars.sl

    #--------------- Title
    response.title='Preview Client Payment'
    
    depotList=[]    
    depotRows=db(db.sm_depot.cid==c_id).select(db.sm_depot.depot_id,db.sm_depot.name)
    if depotRows:
        depotList=depotRows.as_list()
    
    records=db((db.sm_client_payment.cid==c_id)&(db.sm_client_payment.field1=='CP') & (db.sm_client_payment.depot_id==depot_id)& (db.sm_client_payment.sl==sl)).select(db.sm_client_payment.ALL,limitby=(0,1))
    
    sl=0
    to_depot=''
    to_depot_name=''
    rep_id=''
    rep_name=''
    client_id=''
    client_name=''
    area_id=''
    area_name=''
    pay_date=''
    paytype=''
    amount=0
    narration=''
    
    for row in records:
        sl=row.sl
        to_depot=row.depot_id
        rep_id=row.rep_id
        rep_name=row.rep_name
        client_id=row.client_id
        client_name=row.client_name
        area_id=row.area_id
        pay_date=row.pay_date
        paytype=row.paytype
        amount=row.amount
        narration=row.narration
        
        for i in range(len(depotList)):
            myRowData=depotList[i]                                
            depot_id=myRowData['depot_id']
            name=myRowData['name']
            if (str(to_depot).strip()==str(depot_id).strip()):
                to_depot_name=name
                break
        
        levelRow=db((db.sm_level.cid==c_id) & (db.sm_level.level_id==area_id)).select(db.sm_level.level_name,limitby=(0,1))
        if levelRow:
            area_name=levelRow[0].level_name        
        break
        
    #-----------  
    return dict(message=T('Show Client Payment'),sl=sl,to_depot=to_depot,to_depot_name=to_depot_name,rep_id=rep_id,rep_name=rep_name,
                pay_date=pay_date,client_id=client_id,client_name=client_name,area_id=area_id,area_name=area_name,paytype=paytype,amount=amount,narration=narration)


#validation for client payment
# used field1=payment category, stock_in_sl=payment_to_client_sl

def payment_to_client_validation(form):
    c_id=session.cid
    amount=0
    
    depot_id=str(request.vars.depot_id).strip()
    rep_id=request.vars.rep_id
    client_id=request.vars.client_id
    amount=float(request.vars.amount)
    confirmAmt=request.vars.confirmAmt
    
    try:
        confirmAmt=float(confirmAmt)
    except:
        confirmAmt=0
        
    if amount<=0:
        form.errors.amount=''
        response.flash = 'need valid amount!'
    else:
        if (amount!=confirmAmt):
            form.errors.amount=''
            response.flash = 'invalid confirm amount'
        else:
            amount=((amount*100)//1)/100
            form.vars.amount=amount
            
            if depot_id=='' or depot_id==None:
                form.errors.rep_id=''
                response.flash = 'invalid depot!'
            else:
                repRows=db((db.sm_rep.cid==c_id)& (db.sm_rep.user_type=='rep')& (db.sm_rep.depot_id==depot_id)  & (db.sm_rep.rep_id==rep_id.upper())).select(db.sm_rep.name,limitby=(0,1))
                if not repRows:
                    form.errors.rep_id='invalid rep for this depot'
                else:
                    clientRows=db((db.sm_client.cid==c_id)& (db.sm_client.depot_id==depot_id) & (db.sm_client.client_id==client_id)).select(db.sm_client.area_id,db.sm_client.name,
        orderby=db.sm_client.name,limitby=(0,1))
                    if not clientRows:
                        form.errors.client_id='invalid client for this depot'
                    else:
                        area_id=''
                        client_name=''
                        for row in clientRows:
                            area_id=row.area_id
                            client_name=row.name
                            break
                        
                        #----------
                        rep_name=''
                        rep_name=repRows[0].name
                        #Get max sl
                        maxSl=0
                        records=db((db.sm_depot.cid==c_id) & (db.sm_depot.depot_id==depot_id)).select(db.sm_depot.id,db.sm_depot.stock_in_sl,limitby=(0,1))
                        if records:
                            sl=records[0].stock_in_sl   # used for payment to client sl
                            if sl==None or sl=='':
                                sl=0                            
                            maxSl=int(sl)+1                        
                        else:
                            maxSl=1
                        
                        # sl update in depot
                        records[0].update_record(stock_in_sl=maxSl)
                        
                        form.vars.sl=maxSl
                        
                        form.vars.depot_id=depot_id
                        form.vars.rep_id=rep_id.upper()
                        form.vars.rep_name=rep_name
                        form.vars.client_id=client_id.upper()
                        form.vars.client_name=client_name
                        form.vars.area_id=area_id


def payment_to_client():
    response.title='Payment To Client'
    #Check access permission
    #----------Task assaign----------
    task_id='rm_client_payment_manage'
    task_id_view='rm_client_payment_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL(c='default', f='home'))        


#   ---------------------    
    c_id=session.cid
    depot_id=session.depot_id

    form =SQLFORM(db.sm_client_payment,
                  fields=['rep_id','client_id','area_id','paytype','pay_date','amount','narration'],
                  submit_button='Post'       
                  )
    
    form.vars.cid=session.cid
    form.vars.depot_id=depot_id
    form.vars.field1='PTC'   # field1=payment Category, CP=Client Payment, PTC= Payment To Client
    
    #Insert after validation 
    if form.accepts(request.vars,session,onvalidation=payment_to_client_validation):
        depotId=form.vars.depot_id
        clientID=form.vars.client_id  
        pay_date=form.vars.pay_date
        amount=form.vars.amount 
        slNo=form.vars.sl
       
       #Create string for client_payment_balance
#       strData=str(c_id)+'<fdfd>'+str(depotId)+'<fdfd>'+str(clientID)+'<fdfd>'+str(amount)
       #format:cid<fdfd>tx_type<fdfd>sl<fdfd>datetime<fdfd>reference<fdfd>1st account with prefix (cr)<fdfd>2nd account with prefix (dr)<fdfd>tx_amount
        
        if session.ledgerCreate=='YES':
            strData=str(c_id)+'<fdfd>PAYMENTCLT<fdfd>'+str(slNo)+'<fdfd>'+str(datetime_fixed)+'<fdfd>'+str(depotId)+'-'+str(slNo)+'<fdfd>DPT-'+str(depotId)+'<fdfd>CLT-'+str(clientID)+'<fdfd>'+str(amount)
            resStr=set_balance_transaction(strData) 
            resStrList=resStr.split('<sep>',resStr.count('<sep>'))
            flag=resStrList[0]
            msg=resStrList[1]
        else:
            flag='True'
            msg='Success'
            
        if flag=='True':
            response.flash = msg
        else:
            db.rollback()
            response.flash = msg
    
    # ------------- filter-------
    btn_filter=request.vars.btn_filter
    btn_filter_all=request.vars.btn_filter_all
    reqPage=len(request.args)
    if btn_filter:
        client_id_value=request.vars.client_id_value
        
        session.btn_filter_payclient=btn_filter
        session.client_id_value_payclient=client_id_value.upper()
        reqPage==0
        
    elif btn_filter_all:
        session.btn_filter_payclient=None
        session.client_id_value_payclient=None
        
        reqPage=0
        
    #--------paging
    if reqPage:
        page=int(reqPage)
    else:
        page=0
    items_per_page=session.items_per_page
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #--------end paging    
    
    qset=db()
    qset=qset(db.sm_client_payment.cid==c_id)
    qset=qset(db.sm_client_payment.field1=='PTC')
    
    if session.user_type=='Depot':
        qset=qset(db.sm_client_payment.depot_id==session.depot_id)
    
    if (session.btn_filter_payclient):
        searchValue=str(session.client_id_value_payclient).split('|')[0]
        qset=qset(db.sm_client_payment.client_id==searchValue)
    
    records=qset.select(db.sm_client_payment.ALL,orderby=~db.sm_client_payment.id,limitby=limitby)
    
    return dict(form=form,depot_id=depot_id,records=records,page=page,items_per_page=items_per_page,access_permission=access_permission,access_permission_view=access_permission_view)


def preview_payment_to_client():
    #----------Task assaign----------
    task_id='rm_client_payment_manage'
    task_id_view='rm_client_payment_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL(c='default', f='home'))  
    
    #------------------------
    c_id=session.cid
    depot_id=request.vars.depotId
    sl=request.vars.sl

    #--------------- Title
    response.title='Preview Payment To Client'
    
    depotList=[]    
    depotRows=db(db.sm_depot.cid==c_id).select(db.sm_depot.depot_id,db.sm_depot.name)
    if depotRows:
        depotList=depotRows.as_list()
    
    records=db((db.sm_client_payment.cid==c_id)&(db.sm_client_payment.field1=='PTC') & (db.sm_client_payment.depot_id==depot_id)& (db.sm_client_payment.sl==sl)).select(db.sm_client_payment.ALL,limitby=(0,1))
    
    sl=0
    to_depot=''
    to_depot_name=''
    rep_id=''
    rep_name=''
    client_id=''
    client_name=''
    area_id=''
    area_name=''
    pay_date=''
    paytype=''
    amount=0
    narration=''
    
    for row in records:
        sl=row.sl
        to_depot=row.depot_id
        rep_id=row.rep_id
        rep_name=row.rep_name
        client_id=row.client_id
        client_name=row.client_name
        area_id=row.area_id
        pay_date=row.pay_date
        paytype=row.paytype
        amount=row.amount
        narration=row.narration
        
        for i in range(len(depotList)):
            myRowData=depotList[i]                                
            depot_id=myRowData['depot_id']
            name=myRowData['name']
            if (str(to_depot).strip()==str(depot_id).strip()):
                to_depot_name=name
                break
        
        levelRow=db((db.sm_level.cid==c_id) & (db.sm_level.level_id==area_id)).select(db.sm_level.level_name,limitby=(0,1))
        if levelRow:
            area_name=levelRow[0].level_name        
        break
        
    #-----------  
    return dict(message=T('Show Client Payment'),sl=sl,to_depot=to_depot,to_depot_name=to_depot_name,rep_id=rep_id,rep_name=rep_name,
                pay_date=pay_date,client_id=client_id,client_name=client_name,area_id=area_id,area_name=area_name,paytype=paytype,amount=amount,narration=narration)


#====================Not used================
##Delete item from order if more than one item in sl
def delete_order_item():
    c_id=session.cid
    
    btn_delete=request.vars.btn_delete
    
    req_depot=request.args(0)
    req_sl=request.args(1)    
    req_item=request.args(2)
    
    if btn_delete:
        countRecords=db((db.sm_order.cid==c_id)& (db.sm_order.depot_id==req_depot) & (db.sm_order.sl==req_sl)).count()
        if int(countRecords)==1:
            session.flash='At least one item needs in an order, You can cancel if required!'
        else:
            db((db.sm_order.cid==c_id) & (db.sm_order.sl==req_sl)& (db.sm_order.depot_id==req_depot)& (db.sm_order.item_id==req_item)).delete()

        redirect(URL('order_add',vars=dict(req_sl=req_sl,dptid=req_depot)))
    #  ---------------------
    return dict()

##Update order status as Post or Cancel
#def post_cancel_order():
#    c_id=session.cid
#    
#    btn_cancel=request.vars.btn_cancel
#    btn_submitted=request.vars.btn_submitted
#    
#    req_depot=request.args(0)
#    req_sl=request.args(1) 
#    req_date=request.args(2)    
#    ym_date=str(req_date)[0:7]+'-01'
#    
#    
#  
#    # SUBMITTED
#    if btn_submitted:
#        countRecords=db((db.sm_order.cid==c_id)& (db.sm_order.depot_id==req_depot) & (db.sm_order.sl==req_sl)).count()
#        if int(countRecords)==0:
#            session.flash='At least one item needs in an order!'
#        else:
#            db((db.sm_order_head.cid==c_id)& (db.sm_order_head.depot_id==req_depot) & (db.sm_order_head.sl==req_sl)).update(status='Submitted')
#            db((db.sm_order.cid==c_id)& (db.sm_order.depot_id==req_depot) & (db.sm_order.sl==req_sl)).update(status='Submitted')
#            session.flash='Submitted successfully'
#            
#        redirect(URL(c='order_invoice',f='order_add',vars=dict(req_sl=req_sl)))
#    
#    elif btn_cancel:
#        countRecords=db((db.sm_order.cid==c_id)& (db.sm_order.depot_id==req_depot) & (db.sm_order.sl==req_sl)).count()
#        if int(countRecords)==0:
#            session.flash='At least one item needs in an order!'
#        else:
#            records=db((db.sm_order.cid==c_id)& (db.sm_order.depot_id==req_depot) & (db.sm_order.sl==req_sl)& (db.sm_order.status=='Draft')).count(db.sm_order.status)
#            if records:
#                db((db.sm_order_head.cid==c_id)& (db.sm_order_head.depot_id==req_depot) & (db.sm_order_head.sl==req_sl)).update(status='Cancelled')
#                db((db.sm_order.cid==c_id)& (db.sm_order.depot_id==req_depot) & (db.sm_order.sl==req_sl)).update(status='Cancelled')
#                session.flash='Cancelled successfully'
#            else:
#                session.flash='Invalid Order!'
#                
#        redirect(URL(c='order_invoice',f='order_add',vars=dict(req_sl=req_sl)))
#    
#    return dict()
##==============================Not used
#def order_item_selector():
#    c_id=session.cid
#    txt_item= str(request.vars.txt_item).upper()
#
#    selected=[]
#    
#    #--------------------------
#    rows=db(db.sm_item.cid==c_id).select(db.sm_item.item_id,db.sm_item.name,db.sm_item.category_id,db.sm_item.price,orderby=db.sm_item.name)
#    for row in rows:
#        item_id=str(row.item_id).replace('|', ' ')
#        name=str(row.name).replace('|', ' ')
#        category_id=str(row.category_id).replace('|', ' ')
#        price=row.price
#
#        temp=name+item_id
#        temp=temp.upper()
#        
#    
#        if (temp.find(txt_item)== (-1)):
#            continue
#        else:
#            data=name+'|'+item_id+'|'+str(category_id)+'|'+str(price)
#            selected.append(data)
#            if len(selected)>=100:
#                break
#            
#   #----------------       
#
#    return ''.join([DIV(k,
#                 _onclick="jQuery('#txt_item').val('%s')" % k ,
#                 _onmouseover="this.style.backgroundColor='yellow'",
#                 _onmouseout="this.style.backgroundColor='white'"
#                 ).xml() for k in selected])
#
#
#
##========================invoice_generate
#
##==============================Not used
#
#def invoice_item_selector():
#    c_id=session.cid
#    txt_item= str(request.vars.txt_item).upper()
#
#    selected=[]
#            #--------------------------
#    rows=db(db.sm_item.cid==c_id).select(db.sm_item.item_id,db.sm_item.name,db.sm_item.category_id,db.sm_item.price,orderby=db.sm_item.name)
#    for row in rows:
#        item_id=str(row.item_id).replace('|', ' ')
#        name=str(row.name).replace('|', ' ')
#        category_id=row.category_id
#        price=row.price
#        
#        temp=name+item_id
#        temp=temp.upper()
#        
#        if (temp.find(txt_item)== (-1)):
#            continue
#        else:
#            data=name+'|'+item_id+'|'+str(category_id)+'|'+str(price)
#            selected.append(data)
#            if len(selected)>=100:
#                break
#            
#    #----------------
#    return ''.join([DIV(k,
#                 _onclick="jQuery('#txt_item').val('%s')" % k ,
#                 _onmouseover="this.style.backgroundColor='yellow'",
#                 _onmouseout="this.style.backgroundColor='white'"
#                 ).xml() for k in selected])
#
#
#
##============================ Invoice Rules settings


#====================================== CLIENT Opening BATCH UPLOAD
def client_invoice_opening_batch_upload():
    task_id='rm_invoice_manage'
    access_permission=check_role(task_id)
    if access_permission==False:
        session.flash='Access is Denied !'
        redirect (URL('invoice_list'))
    
    if session.user_type!='Depot':
        session.flash='Access is Denied, Depot user can access only'
        redirect (URL(''))
        
    depotID=session.depot_id
    depotName=session.user_depot_name
    
    response.title='Client Opening Batch Upload'
    
    c_id=session.cid
    
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
        
        client_list_excel=[]
        rep_list_excel=[]        
        area_list_excel=[]
        dp_list_excel=[]
        
        client_exist=[]
        rep_exist=[]
        existLevel_list=[]
        dp_exist=[]
                
        ins_list=[]
        ins_dict={}
        
        for i in range(total_row):
            if i>=500:
                break
            else:
                row_data=row_list[i]                    
                coloum_list=row_data.split( '\t')
                if len(coloum_list)==12:
                    client_excel=str(coloum_list[2]).strip().upper()
                    if len(client_excel)<10:
                        client_excel=str(depotID)+str(client_excel)                        
                    if client_excel not in client_list_excel:
                        client_list_excel.append(client_excel)
                    
                    rep_excel=str(coloum_list[8]).strip().upper()
                    if rep_excel not in rep_list_excel:
                        rep_list_excel.append(rep_excel)
                    
                    area_excel=str(coloum_list[9]).strip().upper()
                    if area_excel not in area_list_excel:
                        area_list_excel.append(area_excel)
                    
                    dp_excel=str(coloum_list[10]).strip().upper()
                    if dp_excel not in dp_list_excel:
                        dp_list_excel.append(dp_excel)
                        
        clRows=db((db.sm_client.cid==c_id)&(db.sm_client.depot_id==depotID)&(db.sm_client.client_id.belongs(client_list_excel))).select(db.sm_client.client_id,db.sm_client.name,db.sm_client.area_id,db.sm_client.store_id,db.sm_client.store_name,db.sm_client.market_id,db.sm_client.market_name,db.sm_client.category_id,db.sm_client.category_name,db.sm_client.sub_category_id,db.sm_client.sub_category_name,orderby=db.sm_client.client_id)
        client_exist=clRows.as_list()
        
        repRows=db((db.sm_rep.cid==c_id)&(db.sm_rep.rep_id.belongs(rep_list_excel))).select(db.sm_rep.rep_id,db.sm_rep.name,orderby=db.sm_rep.rep_id)
        rep_exist=repRows.as_list()
        
        existLevelRows=db((db.sm_level.cid==c_id)&(db.sm_level.is_leaf=='1')&(db.sm_level.level_name.belongs(area_list_excel))).select(db.sm_level.ALL,orderby=db.sm_level.level_id)
        existLevel_list=existLevelRows.as_list()
        
        dpRows=db((db.sm_delivery_man.cid==c_id)&(db.sm_delivery_man.depot_id==depotID)&(db.sm_delivery_man.d_man_id.belongs(dp_list_excel))).select(db.sm_delivery_man.d_man_id,db.sm_delivery_man.name,orderby=db.sm_delivery_man.d_man_id)
        dp_exist=dpRows.as_list()
        
        #   --------------------
        for i in range(total_row):
            if i>=500:
                break
            else:
                row_data=row_list[i]
            coloum_list=row_data.split( '\t')
            
            if len(coloum_list)!=12:
                error_data=row_data+'(12 columns need in a row)\n'
                error_str=error_str+error_data
                count_error+=1
                continue
            else:
                invNo_ex=str(coloum_list[0]).strip().upper()
                invDate_ex=str(coloum_list[1]).strip()
                clientId_ex=str(coloum_list[2]).strip().upper()
                tp_ex=coloum_list[3]
                vat_ex=coloum_list[4]
                discount_ex=coloum_list[5]
                sp_discount_ex=coloum_list[6]
                terms_ex=str(coloum_list[7]).strip().upper()
                emp_ex=str(coloum_list[8]).strip().upper()
                territory_ex=str(coloum_list[9]).strip().upper()
                dp_ex=str(coloum_list[10]).strip().upper()                
                shipmentNo_ex=str(coloum_list[11]).strip().upper()
                
                try:
                    invDate=datetime.datetime.strptime(invDate_ex,'%Y-%m-%d')
                except:
                    error_data=row_data+'(Invalid Invoice Date)\n'
                    error_str=error_str+error_data
                    count_error+=1
                    continue
                    
                try:
                    tp_ex=float(tp_ex)
                    if tp_ex<=0:
                        error_data=row_data+'(Invalid TP)\n'
                        error_str=error_str+error_data
                        count_error+=1
                        continue                                   
                except:
                    error_data=row_data+'(Invalid TP)\n'
                    error_str=error_str+error_data
                    count_error+=1
                    continue
                
                try:
                    vat_ex=float(vat_ex)
                    if vat_ex<0:
                        error_data=row_data+'(Invalid Vat)\n'
                        error_str=error_str+error_data
                        count_error+=1
                        continue
                except:
                    error_data=row_data+'(Invalid Vat)\n'
                    error_str=error_str+error_data
                    count_error+=1
                    continue
                    
                try:
                    discount_ex=float(discount_ex)    
                    if discount_ex<0:
                        error_data=row_data+'(Invalid Discount)\n'
                        error_str=error_str+error_data
                        count_error+=1
                        continue
                except:
                    error_data=row_data+'(Invalid Discount)\n'
                    error_str=error_str+error_data
                    count_error+=1
                    continue
                
                try:
                    sp_discount_ex=float(sp_discount_ex)    
                    if sp_discount_ex<0:
                        error_data=row_data+'(Invalid Sp Discount)\n'
                        error_str=error_str+error_data
                        count_error+=1
                        continue
                except:
                    error_data=row_data+'(Invalid Sp Discount)\n'
                    error_str=error_str+error_data
                    count_error+=1
                    continue
                
                
                if clientId_ex=='':
                    error_data=row_data+'(Required Client)\n'
                    error_str=error_str+error_data
                    count_error+=1
                    continue
                
                if terms_ex=='':
                    error_data=row_data+'(Required Terms)\n'
                    error_str=error_str+error_data
                    count_error+=1
                    continue
                
                if emp_ex=='':
                    error_data=row_data+'(Required MSO)\n'
                    error_str=error_str+error_data
                    count_error+=1
                    continue
                
                if territory_ex=='':
                    error_data=row_data+'(Required Territory)\n'
                    error_str=error_str+error_data
                    count_error+=1
                    continue
                
                if dp_ex=='':
                    error_data=row_data+'(Required DP)\n'
                    error_str=error_str+error_data
                    count_error+=1
                    continue
                
                #----------
                if len(clientId_ex)<10:
                    clientId_ex=str(depotID)+str(clientId_ex)
                
                #-----------------------                
                valid_client=False
                valid_rep=False
                valid_dp=False
                
                clientName=''                
                clientStoreID=''
                clientStoreName=''
                
                level_name=''
                level0_id=''
                level0_name=''
                level1_id=''
                level1_name=''
                level2_id=''
                level2_name=''
                level3_id=''
                level3_name=''
                
                depot_name=depotName
                
                repName=''
                dpName=''
                client_market_id=''
                client_market_name=''
                cl_category_id=''
                cl_category_name=''
                cl_sub_category_id=''
                cl_sub_category_name=''
                special_territory_code=''
                
                #----------- 
                for i in range(len(client_exist)):
                    myRowData=client_exist[i]                        
                    client_id=myRowData['client_id']                            
                    if (str(client_id).strip()==str(clientId_ex).strip()):                                
                        valid_client=True
                        clientName=myRowData['name']
                        clientStoreID=myRowData['store_id']
                        clientStoreName=myRowData['store_name'] 
                        client_market_id=myRowData['market_id']
                        client_market_name=myRowData['market_name']                        
                        cl_category_id=myRowData['category_id']
                        cl_category_name=myRowData['category_name']
                        cl_sub_category_id=myRowData['sub_category_id']
                        cl_sub_category_name=myRowData['sub_category_name']
                        break
                        
                valid_client=True
                
                if valid_client==False:
                    error_data=row_data+'(Invalid Client/Customer)\n'
                    error_str=error_str+error_data
                    count_error+=1
                    continue
                else:
                    for i in range(len(existLevel_list)):
                        myRowData=existLevel_list[i]                        
                        territory_id=myRowData['level_id']                            
                        if (str(territory_id).strip()==str(territory_ex).strip()):                                
                            valid_area=True
                            level_name=myRowData['level_name']
                            level0_id=myRowData['level0']
                            level0_name=myRowData['level0_name']
                            level1_id=myRowData['level1']
                            level1_name=myRowData['level1_name']
                            level2_id=myRowData['level2']
                            level2_name=myRowData['level2_name']
                            level3_id=myRowData['level3']
                            level3_name=myRowData['level3_name']    
                            special_territory_code=myRowData['special_territory_code']                         
                            break
                    
                    for i in range(len(rep_exist)):
                        myRowData=rep_exist[i]                        
                        rep_ID=myRowData['rep_id']                    
                        if str(rep_ID).strip()==str(emp_ex).strip():                                
                            valid_rep=True
                            repName=myRowData['name']
                            break
                    
                    valid_rep=True
                                        
                    if valid_rep==False:
                        error_data=row_data+'(Invalid MSO)\n'
                        error_str=error_str+error_data
                        count_error+=1
                        continue
                    else:
                        for i in range(len(dp_exist)):
                            myRowData=dp_exist[i]                        
                            d_man_ID=myRowData['d_man_id']                    
                            if str(d_man_ID).strip()==str(dp_ex).strip():                                
                                valid_dp=True
                                dpName=myRowData['name']
                                break
                                
                        if valid_dp==False:
                            error_data=row_data+'(Invalid DP)\n'
                            error_str=error_str+error_data
                            count_error+=1
                            continue
                        else:                         
                            #-----------------                                
                            invRow=db((db.sm_invoice_head.cid==c_id) & (db.sm_invoice_head.depot_id==depotID) & (db.sm_invoice_head.sl==0) & (db.sm_invoice_head.order_sl==0) & (db.sm_invoice_head.delivery_date==invDate) & (db.sm_invoice_head.client_id==clientId_ex) & (db.sm_invoice_head.note==invNo_ex)).select(db.sm_invoice_head.id,limitby=(0,1))
                            if invRow:                                                    
                                error_data=row_data+'(Already exist)\n'
                                error_str=error_str+error_data
                                count_error+=1
                                continue                                                    
                            else:
                                invoiceTerm=''
                                creditType=''
                                if terms_ex=='CASH':
                                    invoiceTerm=terms_ex
                                else:
                                    invoiceTerm='CREDIT'
                                    creditType=terms_ex
                                    
                                try:
                                    #------------
                                    total_amount=tp_ex+vat_ex-discount_ex-sp_discount_ex
                                    actual_total_tp=tp_ex+sp_discount_ex
                                    db.sm_invoice_head.insert(cid=c_id,depot_id=depotID,depot_name=depot_name,sl=0,store_id=clientStoreID,store_name=clientStoreName,order_sl=0,delivery_date=invDate,payment_mode=invoiceTerm,credit_note=creditType,client_id=clientId_ex,client_name=clientName,rep_id=emp_ex,rep_name=repName,market_id=client_market_id,market_name=client_market_name,d_man_id=dp_ex,d_man_name=dpName,
                                                              area_id=territory_ex,area_name=level_name,level0_id=level0_id,level0_name=level0_name,level1_id=level1_id,level1_name=level1_name,level2_id=level2_id,level2_name=level2_name,level3_id=level3_id,level3_name=level3_name,cl_category_id=cl_category_id,cl_category_name=cl_category_name,cl_sub_category_id=cl_sub_category_id,cl_sub_category_name=cl_sub_category_name,special_territory_code=special_territory_code,status='Submitted',invoice_media='OPENING',actual_total_tp=round(actual_total_tp,2),total_amount=round(total_amount,2),vat_total_amount=round(vat_ex,2),discount=round(discount_ex,2),sp_discount=round(sp_discount_ex,2),ym_date=str(invDate)[0:7]+'-01',invoice_date=invDate,invoice_ym_date=str(invDate)[0:7]+'-01',note=invNo_ex,shipment_no=shipmentNo_ex)
                                    count_inserted+=1                                                    
                                    #-------------
                                except:
                                    error_data=row_data+'(error in process!)\n'
                                    error_str=error_str+error_data
                                    count_error+=1
                                    continue
        
        if error_str=='':
            error_str='No error'
    
    return dict(count_inserted=count_inserted,count_error=count_error,error_str=error_str,total_row=total_row)

#http://c003.cloudapp.net/skf/order_invoice/set_client_invoice_opening
#http://127.0.0.1:8000/skf/order_invoice/set_client_invoice_opening
def set_client_invoice_opening():
    
    resStr=''                    
    
    hRows=db((db.sm_invoice_head.sl==0) & (db.sm_invoice_head.status=='Submitted') & (db.sm_invoice_head.invoice_media=='OPENING')).select(db.sm_invoice_head.ALL,orderby=db.sm_invoice_head.id,limitby=(0,20))
    for row in hRows:
        c_id=row.cid
        req_depot=row.depot_id
        req_sl=row.sl
        client_id=row.client_id
        delivery_date=row.delivery_date
        ym_date=str(delivery_date)[0:7]+'-01'
        
        totalAmount=float(row.total_amount)
        
        #-------------        
        if session.ledgerCreate=='YES':
            strData=str(c_id)+'<fdfd>DELIVERY<fdfd>'+str(req_sl)+'<fdfd>'+str(datetime_fixed)+'<fdfd>'+str(req_depot)+'-'+str(req_sl)+'<fdfd>DPT-'+str(req_depot)+'<fdfd>CLT-'+str(client_id)+'<fdfd>'+str(totalAmount)
            resStr=set_balance_transaction(strData)
            
            resStrList=resStr.split('<sep>',resStr.count('<sep>'))
            flag=resStrList[0]
            msg=resStrList[1]
        else:
            flag='True'
            
        if flag=='True':
            #Update status of head and detail
            row.update_record(status='Invoiced',invoice_date=delivery_date,invoice_ym_date=ym_date)
            
    return 'Done'


