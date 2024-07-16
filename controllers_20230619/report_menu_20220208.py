
#======================= Report Home
def report_home():
    task_id='rm_analysis_view'
    access_permission=check_role(task_id)
    if (access_permission==False ):
        session.flash='Access is Denied'
        redirect (URL('default','home'))
    
    c_id=session.cid
    
    response.title='Stock Reports'
    
    search_date=SQLFORM(db.sm_search_date,
                  fields=['from_dt','to_dt']           
                  )
    
    btn_depot_wise_stock=request.vars.btn_depot_wise_stock
    btn_item_wise_stock=request.vars.btn_item_wise_stock
    
    depotStr=''
    if (session.user_type=='Depot' and session.user_depot_category=='DEPOT'):
        #records=db(db.sm_depot.cid==c_id).select(db.sm_depot.depot_id,db.sm_depot.name,orderby=db.sm_depot.name)
        
        depotStr=str(session.depot_id)+'|'+str(session.user_depot_name).replace('|', ' ')
        
#         subDepotRows=db((db.sm_depot_settings.cid==c_id) & (db.sm_depot_settings.depot_id_from_to==session.depot_id)& (db.sm_depot_settings.from_to_type=='Receive')& (db.sm_depot.cid==c_id)& (db.sm_depot_settings.depot_id==db.sm_depot.depot_id)).select(db.sm_depot_settings.depot_id,db.sm_depot.name,orderby=db.sm_depot_settings.depot_id)
#         for subRow in subDepotRows:
#             depot_id=str(subRow.sm_depot_settings.depot_id).strip()
#             depotName=str(subRow.sm_depot.name).strip().replace('|', ' ')
#             
#             depotIdName=depot_id+'|'+depotName            
#             depotStr+=','+depotIdName
    else:
#         if session.user_type=='Supervisor':
#             depotRows = db(db.sm_depot.cid == c_id).select(db.sm_depot.depot_id,db.sm_depot.name,orderby=db.sm_depot.name)
#         else:
        
        depotRows=db(db.sm_depot.cid==c_id).select(db.sm_depot.depot_id,db.sm_depot.name,orderby=db.sm_depot.name)
        for dptRow in depotRows:
            depot_id=str(dptRow.depot_id).strip()
            name=str(dptRow.name).strip().replace('|', ' ')
            depotIdName=depot_id+'|'+name
            
            if depotStr=='':
                depotStr=depotIdName
            else:
                depotStr+=','+depotIdName
                
    #-------------------------
    if btn_depot_wise_stock:
        depot_id_nameList=str(request.vars.depot_id_name).split('|')
        if len(depot_id_nameList) < 2:
            response.flash='Select Depot'   
        else:
            depotId=depot_id_nameList[0]
            depotName=depot_id_nameList[1]
            
            if depotId=='' or depotName=='':
                response.flash='Select depot for this report'            
            else:
                if (session.user_type=='Depot' and session.user_depot_category=='DEPOT'):
                    depotId=session.depot_id
                    depotName=session.user_depot_name
                    
                redirect(URL(c='report_menu',f='depot_wise_stock_report',vars=dict(page=0,depot_id=depotId,depot_name=depotName)))
                
    elif btn_item_wise_stock:
        item_id_nameList=str(request.vars.item_id_name).split('|')
        if len(item_id_nameList) < 2:
            response.flash='Select Item'   
        else:
            item_id=item_id_nameList[0]
            item_name=item_id_nameList[1]
            
            if item_id=='' or item_name=='':
                response.flash='Select item for this report !'            
            else:
                
                redirect(URL(c='report_menu',f='item_wise_stock_report',vars=dict(page=0,item_name=item_name,item_id=item_id)))
                
    return dict(message='Reports',depotStr=depotStr,search_date=search_date)

#==================================depot wise stock report
def depot_wise_stock_report():
    task_id='rm_analysis_view'
    access_permission=check_role(task_id)
    if (access_permission==False ):
        session.flash='Access is Denied'
        redirect (URL('default','home'))
    
    c_id=session.cid
    response.title='Report-Depot wise stock'
    
    depot_id=request.vars.depot_id
    depot_name=request.vars.depot_name
    
    btn_filter_rpt=request.vars.btn_filter
    btn_all=request.vars.btn_all
    
    store_idname=request.vars.store_idname
    itemIdName=request.vars.item_details
    without_zero=request.vars.without_zero
    reqPage=len(request.args)
    if btn_filter_rpt:
        session.btn_filter_rpt=btn_filter_rpt
        session.store_idname=store_idname
        session.itemIdName=itemIdName
        session.without_zero=without_zero
        reqPage=0
    elif btn_all:
        session.btn_filter_rpt=None
        session.store_idname=None
        session.itemIdName=None
        session.without_zero=None
        reqPage=0
    
    
    #--------paging
    if reqPage:
        page=int(request.args[0])
    else:
        page=0
    items_per_page=session.items_per_page
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #--------end paging    
    
    #---------------- Item List
    
    qset=db()
    qset=qset(db.sm_depot_stock_balance.cid==c_id)
    if (session.user_type=='Depot' and session.user_depot_category=='DEPOT'):
        qset=qset(db.sm_depot_stock_balance.depot_id==session.depot_id)
    else:
        qset=qset(db.sm_depot_stock_balance.depot_id==depot_id)
        
    if session.btn_filter_rpt:        
        if not(session.store_idname=='' or session.store_idname==None):
            storeId=str(session.store_idname).split('|')[0]            
            qset=qset(db.sm_depot_stock_balance.store_id==storeId)
        
        if not(session.itemIdName=='' or session.itemIdName==None):
            itemId=str(session.itemIdName).split('|')[0]
            qset=qset(db.sm_depot_stock_balance.item_id==itemId)
            
        if not(session.without_zero=='' or session.without_zero==None):            
            qset=qset(db.sm_depot_stock_balance.quantity!=0)    
    
    
    qset=qset((db.sm_item.cid==c_id)&(db.sm_depot_stock_balance.item_id==db.sm_item.item_id))
    
    stockBalanceRecords=qset.select(db.sm_depot_stock_balance.ALL,db.sm_item.name,db.sm_item.unit_type,orderby=db.sm_depot_stock_balance.store_id|db.sm_item.name|db.sm_depot_stock_balance.expiary_date,limitby=limitby)
    
    
    return dict(stockBalanceRecords=stockBalanceRecords,depot_id=depot_id,depot_name=depot_name,store_idname=store_idname,itemIdName=itemIdName,page=page,items_per_page=items_per_page)
    
#------------- Download depot wise stock
def download_depot_wise_stock():
    task_id='rm_analysis_view'
    access_permission=check_role(task_id)
    if (access_permission==False ):
        session.flash='Access is Denied'
        redirect (URL('default','home'))
    
    c_id=session.cid
    
    depot_id=request.vars.depot_id
    depot_name=str(request.vars.depot_name).replace(',', ' ')
    
    #---------------- Item List
    itemList=[]
    itemRows=db(db.sm_item.cid==c_id).select(db.sm_item.item_id,db.sm_item.name,db.sm_item.unit_type,orderby=db.sm_item.item_id)
    itemList=itemRows.as_list()
    
    
    qset=db()
    qset=qset(db.sm_depot_stock_balance.cid==c_id)
    if (session.user_type=='Depot' and session.user_depot_category=='DEPOT'):
        qset=qset(db.sm_depot_stock_balance.depot_id==session.depot_id)
    else:
        qset=qset(db.sm_depot_stock_balance.depot_id==depot_id)
        
    if session.btn_filter_rpt:        
        if not(session.store_idname=='' or session.store_idname==None):
            storeId=str(session.store_idname).split('|')[0]            
            qset=qset(db.sm_depot_stock_balance.store_id==storeId)
        
        if not(session.itemIdName=='' or session.itemIdName==None):
            itemId=str(session.itemIdName).split('|')[0]
            qset=qset(db.sm_depot_stock_balance.item_id==itemId)
        
        if not(session.without_zero=='' or session.without_zero==None):            
            qset=qset(db.sm_depot_stock_balance.quantity!=0)    
            
    stockBalanceRecords=qset.select(db.sm_depot_stock_balance.ALL,orderby=db.sm_depot_stock_balance.store_id|db.sm_depot_stock_balance.item_id|db.sm_depot_stock_balance.expiary_date)
    
    #--------------
#     if (session.user_type=='Depot' and session.user_depot_category=='DEPOT'):
#         stockBalanceRecords=db((db.sm_depot_stock_balance.cid==c_id)&(db.sm_depot_stock_balance.depot_id==session.depot_id)).select(db.sm_depot_stock_balance.ALL,orderby=db.sm_depot_stock_balance.store_id|db.sm_depot_stock_balance.item_id)
#     else:
#         stockBalanceRecords=db((db.sm_depot_stock_balance.cid==c_id)&(db.sm_depot_stock_balance.depot_id==depot_id)).select(db.sm_depot_stock_balance.ALL,orderby=db.sm_depot_stock_balance.store_id|db.sm_depot_stock_balance.item_id)
    
    myString='Depot Wise Stock Report\n'
    myString+='Depot ID:,'+str(depot_id)+'\n'
    myString+='Depot Name'+','+str(depot_name)+'\n\n'
    
    myString+='Store ID,Store Name,Item ID,Name,Unit Type,Batch ID,Expiary Date,Stock Quantity,Blocked Quantity,Available Quantity'+'\n'
    for row in stockBalanceRecords:
        store_id=row.store_id
        store_name=row.store_name
        item_id=row.item_id
        batch_id=row.batch_id
        expiary_date=row.expiary_date
        quantity=row.quantity
        block_qty=row.block_qty
        
        #-------------------------- getting name
        item_name=''
        unit_type=''
        for i in range(len(itemList)):
            itemDict=itemList[i]
            itemId=itemDict['item_id']
            itemName=itemDict['name']
            unitType=itemDict['unit_type']
            if (itemId==item_id):
                item_name=str(itemName).replace(',', ' ')
                unit_type=unitType
                break
        
        #------------------------        
        myString+=str(store_id)+','+str(store_name)+','+str(item_id)+','+str(item_name)+','+str(unit_type)+','+str(batch_id)+','+str(expiary_date)+','+str(quantity)+','+str(block_qty)+','+str(quantity-block_qty)+'\n'

    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_depot_wise_stock.csv'   
    return str(myString)


#==================================Item wise stock report
def item_wise_stock_report():
    task_id='rm_analysis_view'
    access_permission=check_role(task_id)
    if (access_permission==False ):
        session.flash='Access is Denied'
        redirect (URL('default','home'))
    
    c_id=session.cid
    
    response.title='Report-Item wise stock'
    
    
    item_name=request.vars.item_name
    item_id=request.vars.item_id
    
    page=int(request.vars.page)
    #----------paging
    if (page > 0):
        page=page
    else:
        page=0
    items_per_page=session.items_per_page
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #----------end paging
    
    #----------------
    depotList=[]    
    if (session.user_type=='Depot' and session.user_depot_category=='DEPOT'):
        depotRows=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==session.depot_id)).select(db.sm_depot.depot_id,db.sm_depot.name,orderby=db.sm_depot.depot_id)
        
        stockBalanceRecords=db((db.sm_depot_stock_balance.cid==c_id)&(db.sm_depot_stock_balance.depot_id==session.depot_id)&(db.sm_depot_stock_balance.item_id==item_id)&(db.sm_depot_stock_balance.quantity!=0)).select(db.sm_depot_stock_balance.ALL,orderby=db.sm_depot_stock_balance.depot_id|db.sm_depot_stock_balance.store_id|db.sm_depot_stock_balance.expiary_date,limitby=limitby)
        depotList=depotRows.as_list()
    
    else:
#         if session.user_type=='Supervisor':
#             depotRows = db((db.sm_depot.cid == c_id)&(db.sm_depot.depot_id.belongs(session.distributorList))).select(db.sm_depot.depot_id,db.sm_depot.name,orderby=db.sm_depot.depot_id)
#             stockBalanceRecords=db((db.sm_depot_stock_balance.cid==c_id)&(db.sm_depot_stock_balance.depot_id.belongs(session.distributorList))&(db.sm_depot_stock_balance.item_id==item_id)).select(db.sm_depot_stock_balance.ALL,orderby=db.sm_depot_stock_balance.depot_id|db.sm_depot_stock_balance.expiary_date,limitby=limitby)
#         else:        
        depotRows=db(db.sm_depot.cid==c_id).select(db.sm_depot.depot_id,db.sm_depot.name,orderby=db.sm_depot.depot_id)
        stockBalanceRecords=db((db.sm_depot_stock_balance.cid==c_id)&(db.sm_depot_stock_balance.item_id==item_id)&(db.sm_depot_stock_balance.quantity!=0)).select(db.sm_depot_stock_balance.ALL,orderby=db.sm_depot_stock_balance.depot_id|db.sm_depot_stock_balance.store_id|db.sm_depot_stock_balance.expiary_date,limitby=limitby)
        
        depotList=depotRows.as_list()
    
    #----------
    return dict(stockBalanceRecords=stockBalanceRecords,depotList=depotList,item_id=item_id,item_name=item_name,page=page,items_per_page=items_per_page)


#------------- Download item wise stock
def download_item_wise_stock():
    task_id='rm_analysis_view'
    access_permission=check_role(task_id)
    if (access_permission==False ):
        session.flash='Access is Denied'
        redirect (URL('default','home'))
        
    c_id=session.cid 
    
    item_name=str(request.vars.item_name).replace(',', ' ')
    item_id=request.vars.item_id
    
    #----------------
    depotList=[]
    if (session.user_type=='Depot' and session.user_depot_category=='DEPOT'):
        depotRows=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==session.depot_id)).select(db.sm_depot.depot_id,db.sm_depot.name,orderby=db.sm_depot.depot_id)
        
        stockBalanceRecords=db((db.sm_depot_stock_balance.cid==c_id)&(db.sm_depot_stock_balance.depot_id==session.depot_id)&(db.sm_depot_stock_balance.item_id==item_id)&(db.sm_depot_stock_balance.quantity!=0)).select(db.sm_depot_stock_balance.ALL,orderby=db.sm_depot_stock_balance.depot_id|db.sm_depot_stock_balance.store_id|db.sm_depot_stock_balance.expiary_date)
        depotList=depotRows.as_list()
    else:
#         if session.user_type=='Supervisor':
#             depotRows = db((db.sm_depot.cid == c_id)&(db.sm_depot.depot_id.belongs(session.distributorList))).select(db.sm_depot.depot_id,db.sm_depot.name,orderby=db.sm_depot.depot_id)
#             stockBalanceRecords=db((db.sm_depot_stock_balance.cid==c_id)&(db.sm_depot_stock_balance.depot_id.belongs(session.distributorList))&(db.sm_depot_stock_balance.item_id==item_id)).select(db.sm_depot_stock_balance.ALL,orderby=db.sm_depot_stock_balance.depot_id|db.sm_depot_stock_balance.expiary_date)
#         else:        
        depotRows=db(db.sm_depot.cid==c_id).select(db.sm_depot.depot_id,db.sm_depot.name,orderby=db.sm_depot.depot_id)
        stockBalanceRecords=db((db.sm_depot_stock_balance.cid==c_id)&(db.sm_depot_stock_balance.item_id==item_id)&(db.sm_depot_stock_balance.quantity!=0)).select(db.sm_depot_stock_balance.ALL,orderby=db.sm_depot_stock_balance.depot_id|db.sm_depot_stock_balance.store_id|db.sm_depot_stock_balance.expiary_date)
        
        depotList=depotRows.as_list()
    #----------

    myString='Item Wise Stock Report\n'
    myString+='Item ID:,'+str(item_id)+'\n'
    myString+='Item Name'+','+str(item_name)+'\n\n'
    
    myString+='Depot ID,Name,Store ID,Store Name,Batch ID,Expiary Date,Stock Quantity,Blocked Quantity,Available Quantity'+'\n'
    
    for row in stockBalanceRecords:
        depot_id=row.depot_id
        store_id=row.store_id
        store_name=row.store_name
        batch_id=row.batch_id
        expiary_date=row.expiary_date
        quantity=row.quantity
        block_qty=row.block_qty
        
        #-------------------------- getting name
        depot_name=''
        for i in range(len(depotList)):
            dictData=depotList[i]
            depotId=dictData['depot_id']
            depotName=dictData['name']
            if (depotId==depot_id):
                depot_name=str(depotName).replace(',', ' ')
                break

        #------------------------        
        myString+=str(depot_id)+','+str(depot_name)+','+str(store_id)+','+str(store_name)+','+str(batch_id)+','+str(expiary_date)+','+str(quantity)+','+str(block_qty)+','+str(quantity-block_qty)+'\n'

    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_item_wise_stock.csv'   
    return str(myString)


#======================= Stock Movement Report ( Not used)
# Not used
def stock_movement_report_notused():
    if (session.cid=='' or session.cid==None):
        redirect (URL('default','home'))
        
    c_id=session.cid     
    response.title='Report-Stock Movement'
    
    year=request.vars.year
    month=request.vars.month
    ym_date=str(year)+'-'+str(month)+'-01'
    
    month_name=request.vars.month_name
    
    depot_id=request.vars.depot_id
    depot_name=request.vars.depot_name
    

    page=int(request.vars.page)
    #----------paging
    if (page > 0):
        page=page
    else:
        page=0
    items_per_page=session.items_per_page
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #----------end paging
    
    
    #---------------- Item List
    itemList=[]
    itemRows=db(db.sm_item.cid==c_id).select(db.sm_item.item_id,db.sm_item.name,db.sm_item.unit_type,orderby=db.sm_item.item_id)
    itemList=itemRows.as_list()    
    
    #-----------------------    
    if (session.user_type=='Depot'):
        depot_id=session.depot_id        
        depotStockRecords=db((db.sm_depot_stock.cid==c_id)&(db.sm_depot_stock.depot_id==depot_id)&(db.sm_depot_stock.ym_date==ym_date)).select(db.sm_depot_stock.ALL,orderby=~db.sm_depot_stock.ym_date,limitby=limitby)
        depotStockOpening=db((db.sm_depot_stock.cid==c_id)&(db.sm_depot_stock.depot_id==depot_id)&(db.sm_depot_stock.ym_date < ym_date)).select(db.sm_depot_stock.item_id,db.sm_depot_stock.quantity,orderby=~db.sm_depot_stock.ym_date)
        
    else:
        depotStockRecords=db((db.sm_depot_stock.cid==c_id)&(db.sm_depot_stock.depot_id==depot_id)&(db.sm_depot_stock.ym_date==ym_date)).select(db.sm_depot_stock.ALL,orderby=~db.sm_depot_stock.ym_date,limitby=limitby)
        depotStockOpening=db((db.sm_depot_stock.cid==c_id)&(db.sm_depot_stock.depot_id==depot_id)&(db.sm_depot_stock.ym_date < ym_date)).select(db.sm_depot_stock.item_id,db.sm_depot_stock.quantity,orderby=~db.sm_depot_stock.ym_date)
        
    return dict(depotStockRecords=depotStockRecords,depotStockOpening=depotStockOpening,itemList=itemList,year=year,month=month,month_name=month_name,depot_id=depot_id,depot_name=depot_name,page=page,items_per_page=items_per_page)

#------------- Download stock movement
# Not used
def download_depot_stock_movement_notused():
    if (session.cid=='' or session.cid==None):
        redirect (URL('default','home'))
        
    c_id=session.cid 
    
    year=request.vars.year
    month=request.vars.month
    ym_date=str(year)+'-'+str(month)+'-01'
    
    month_name=request.vars.month_name
    
    depot_id=request.vars.depot_id
    depot_name=request.vars.depot_name
    
    #---------------- Item List
    itemList=[]
    itemRows=db(db.sm_item.cid==c_id).select(db.sm_item.item_id,db.sm_item.name,db.sm_item.unit_type,orderby=db.sm_item.item_id)
    itemList=itemRows.as_list() 
    
    #-----------------------
    
    if (session.user_type=='Depot'):
        depot_id=session.depot_id        
        depotStockRecords=db((db.sm_depot_stock.cid==c_id)&(db.sm_depot_stock.depot_id==depot_id)&(db.sm_depot_stock.ym_date==ym_date)).select(db.sm_depot_stock.ALL,orderby=~db.sm_depot_stock.ym_date.item_id)
        depotStockOpening=db((db.sm_depot_stock.cid==c_id)&(db.sm_depot_stock.depot_id==depot_id)&(db.sm_depot_stock.ym_date < ym_date)).select(db.sm_depot_stock.item_id,db.sm_depot_stock.quantity,orderby=~db.sm_depot_stock.ym_date)
    else:
        depotStockRecords=db((db.sm_depot_stock.cid==c_id)&(db.sm_depot_stock.depot_id==depot_id)&(db.sm_depot_stock.ym_date==ym_date)).select(db.sm_depot_stock.ALL,orderby=~db.sm_depot_stock.ym_date)
        depotStockOpening=db((db.sm_depot_stock.cid==c_id)&(db.sm_depot_stock.depot_id==depot_id)&(db.sm_depot_stock.ym_date < ym_date)).select(db.sm_depot_stock.item_id,db.sm_depot_stock.quantity,orderby=~db.sm_depot_stock.ym_date)
        
    myString='Depot Stock Movement\n'
    myString+='Year:,'+str(year)+'-'+str(month_name)+'\n'
    myString+='Depot ID:'+','+str(depot_name)+'-'+str(depot_id)+'\n\n'
    
    myString+='Item ID,Name,Unit Type,Opening,Receive,Issue,Damage,Delivery,Return,Total,Closing'+'\n'    
    for row in depotStockRecords:
        item_id=row.item_id  
        rec_qty=row.rec_qty 
        iss_qty=row.iss_qty 
        dam_qty=row.dam_qty 
        del_qty=row.del_qty 
        retn_qty=row.retn_qty 
        
        balanceQty=rec_qty-iss_qty-dam_qty-del_qty+retn_qty
        
        #-------------------------- 
        item_name=''
        unit_type=''
        for i in range(len(itemList)):
            itemDict=itemList[i]
            itemId=itemDict['item_id']
            itemName=itemDict['name']
            unitType=itemDict['unit_type']
            if (itemId==item_id):
                item_name=str(itemName).replace(',', ' ')
                unit_type=unitType
                break
        
        totalQty=0
        for row in depotStockOpening:
            itemID=row.item_id
            itemQty=row.quantity            
            if item_id==itemID:
                totalQty+=int(itemQty)
        
        closingBalance=totalQty+balanceQty
        
        
        #------------------------        
        myString+=str(item_id)+','+str(item_name)+','+str(unit_type)+','+str(totalQty)+','+str(rec_qty)+','+str(iss_qty)+','+str(dam_qty)+','+str(del_qty)+','+str(retn_qty)+','+str(balanceQty)+','+str(closingBalance)+'\n'

    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_depot_stock_movement.csv'   
    return str(myString)


    
