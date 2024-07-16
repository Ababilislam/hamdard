
def home():
#    task_id='rm_analysis_view'
#    access_permission=check_role(task_id)
#    if (access_permission==False ):
#        session.flash='Access is Denied'
#        redirect (URL('default','home'))
    
    response.title='Report'
    
    c_id=session.cid
    
    search_form =SQLFORM(db.sm_search_date)
    
    #-----
    btn_mso_wise_81=request.vars.btn_mso_wise_81
    btn_mso_wise_82=request.vars.btn_mso_wise_82    
    btn_fm_mso_wise_83=request.vars.btn_fm_mso_wise_83
    btn_rsm_fm_wise_84=request.vars.btn_rsm_fm_wise_84    
    btn_rsm_fm_mso_wise_85=request.vars.btn_rsm_fm_mso_wise_85
    btn_mso_market_wise_86=request.vars.btn_mso_market_wise_86
    btn_mso_wise_87=request.vars.btn_mso_wise_87    
    btn_mso_wise_88=request.vars.btn_mso_wise_88
    btn_fm_mso_wise_89=request.vars.btn_fm_mso_wise_89
    btn_rsm_fm_wise_810=request.vars.btn_rsm_fm_wise_810
    btn_rsm_fm_mso_wise_811=request.vars.btn_rsm_fm_mso_wise_811
    btn_mso_market_wise_812=request.vars.btn_mso_market_wise_812
    
    #--------    
    if btn_mso_wise_81:
        from_dt=request.vars.from_dt_4
        to_dt=request.vars.to_dt_4
        
        depot=str(request.vars.depot_id)
        store=str(request.vars.store_id)
         
        level1_idName=str(request.vars.level1_id)
        level2_idName=str(request.vars.level2_id)
        level3_idName=str(request.vars.level3_id)
        mso_id=str(request.vars.mso_id).split('|')[0]
        
        dateFlag=True
        try:
            from_dt2=datetime.datetime.strptime(str(from_dt),'%Y-%m-%d')
            to_dt2=datetime.datetime.strptime(str(to_dt),'%Y-%m-%d')            
            if from_dt2>to_dt2:
                dateFlag=False
        except:
            dateFlag=False
            
        if dateFlag==False:
            response.flash="Invalid Date Range"
        else:
            dateDiff=(to_dt2-from_dt2).days
            if dateDiff>31:
                response.flash="Maximum 31 days allowed between Date Range"
            else:                
                if depot=='' or store=='':
                    response.flash='Required Branch and Store'
                else:      
                    if len(depot.split('|'))>1: 
                        depot_id=depot.split('|')[0]
                        depot_name=depot.split('|')[1]
                    else:
                        depot_id=depot
                        depot_name=''
                    
                    if len(store.split('|'))>1:
                        store_id=store.split('|')[0]
                        store_name=store.split('|')[1]
                    else:
                        store_id=store
                        store_name=''
                        
                    #------      
                    level1_id=''
                    level1_name=''
                    if len(level1_idName.split('|'))>1:
                        level1_id=level1_idName.split('|')[0]
                        level1_name=level1_idName.split('|')[1]
                    else:
                        level1_id=level1_idName
                    
                    #------ 
                    level2_id=''
                    level2_name=''
                    if len(level2_idName.split('|'))>1:
                        level2_id=level2_idName.split('|')[0]
                        level2_name=level2_idName.split('|')[1]
                    else:
                        level2_id=level2_idName
                    #------ 
                    level3_id=''
                    level3_name=''
                    if len(level3_idName.split('|'))>1:
                        level3_id=level3_idName.split('|')[0]
                        level3_name=level3_idName.split('|')[1]
                    else:
                        level3_id=level3_idName
                    
                    
                    mso_Name=''
                    if mso_id!='':
                        rep_check=db((db.sm_rep.cid==c_id) & (db.sm_rep.rep_id==mso_id)).select(db.sm_rep.name,limitby=(0,1))
                        if rep_check:
                            mso_Name=rep_check[0].name
                    
                    if session.user_type=='Depot': 
                        depot_id=session.depot_id
                        depot_name=session.user_depot_name
                        
                    if session.user_type!='Depot':            
                        depotRows = db((db.sm_depot.cid == session.cid) & (db.sm_depot.depot_id == depot_id)).select(db.sm_depot.name,db.sm_depot.depot_category,db.sm_depot.field1,db.sm_depot.short_name, limitby=(0, 1))
                        if depotRows:                                       
                            session.user_depot_address=depotRows[0].field1
                            session.depot_short_name=depotRows[0].short_name
                            
                    #---------------                    
                    if btn_mso_wise_81:
                        if mso_id=='':
                            response.flash='Required MSO'
                        else:                        
                            #redirect (URL('mso_wise_81',vars=dict(fromDate=from_dt,toDate=to_dt,depotID=depot_id,depotName=depot_name,storeID=store_id,storeName=store_name,mso_id=mso_id,mso_Name=mso_Name)))
                            pass
                    
#                     elif btn_stp_item_wise_sales_distribution:
#                         redirect (URL('stp_item_wise_sales_distribution',vars=dict(fromDate=from_dt,toDate=to_dt,depotID=depot_id,depotName=depot_name,storeID=store_id,storeName=store_name,msoID=coll_mso_id,msoName=coll_mso_name)))
                        
    return dict(search_form=search_form)

#------------------------- Collection
def mso_wise_81():
    c_id=session.cid
    
    response.title='8.1 MSO wise sales comparison'
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate    
    
    depot_id=str(request.vars.depotID).strip()    
    depot_name=str(request.vars.depotName).strip()
    
    store_id=str(request.vars.storeID).strip()
    storeName=str(request.vars.storeName).strip()
    
    level1_id=str(request.vars.level1_id).strip()
    level1_name=str(request.vars.level1_name).strip()
    
    level2_id=str(request.vars.level2_id).strip()
    level2_name=str(request.vars.level2_name).strip()
    
    level3_id=str(request.vars.level3_id).strip()
    level3_name=str(request.vars.level3_name).strip()
    
    mso_id=str(request.vars.mso_id).strip()
    mso_Name=str(request.vars.mso_Name).strip()
    
    startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d').strftime('%Y-%m-%d')
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d').strftime('%Y-%m-%d')
    
    
    #---------------
    qset=db()
    qset=qset(db.sm_invoice_head.cid==c_id)
    qset=qset((db.sm_invoice_head.invoice_date>=startDt)&(db.sm_invoice_head.invoice_date<=endDt))
    qset=qset(db.sm_invoice_head.depot_id==depot_id)
    qset=qset(db.sm_invoice_head.store_id==store_id)
    qset=qset(db.sm_invoice_head.status=='Invoiced')
    
    qset=qset(db.sm_client.cid==c_id)
    qset=qset(db.sm_invoice_head.client_id==db.sm_client.client_id)
    
    dateRecords="SELECT a.invoice_date,a.sl, a.client_id, a.client_name, a.area_id, a.discount, a.vat_total_amount, a.total_amount,b.collection_amount,b.collection_date FROM sm_invoice_head a LEFT OUTER JOIN sm_payment_collection b ON a.client_id=b.client_id where a.cid = '"+c_id+"' and a.invoice_date >= '"+str(startDt)+"' and a.invoice_date < '"+str(endDt)+"' and a.depot_id = '"+depot_id+"' and a.store_id = '"+store_id+"' and a.status = 'Invoiced' ORDER BY a.client_id"
        
    records=db.executesql(dateRecords,as_dict = True) 
    
    
    
    return dict(records=records,fromDate=fromDate,toDate=toDate,depotID=depot_id,depotName=depot_name,storeID=store_id,storeName=store_name,deliveryManID=delivery_man_id,deliveryManName=delivery_man_name,territoryID=territory_id,territoryName=territory_name,msoID=mso_id,msoName=mso_name,page=page,items_per_page=items_per_page)    


