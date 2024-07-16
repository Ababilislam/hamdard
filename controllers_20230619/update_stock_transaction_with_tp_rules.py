
#=======================Stock Transaction WITH Cron Function

# Not used

def update_transaction_old():
    
    stockCronRows=db((db.sm_settings.cid=='SYS')&(db.sm_settings.s_key=='STOCK_CRON_FLAG')).select(db.sm_settings.id,db.sm_settings.s_value,limitby=(0,1))
    if stockCronRows:
        cronFlag=stockCronRows[0].s_value        

        if str(cronFlag)=='0':
            stockCronRows[0].update_record(s_value='1')
            
            settCompRows=db((db.sm_settings.s_key=='STOCK_CRON')&(db.sm_settings.s_value=='YES')).select(db.sm_settings.cid)
            if settCompRows:
                # get all settings
                compSttRows=db().select(db.sm_settings.cid,db.sm_settings.s_key,db.sm_settings.s_value)
                for row in settCompRows:
                    c_id=str(row.cid).strip().upper()
                    
                    #----------------------get settings data flag
                    autoDelivery=False
                    invoiceRulesFlag=False                    
                    partigalStockFlag=False
                    negativeStockFlag=False
                    restrictedStockFlag=False 
                    achieveRowsFlag=False
                    
                    for sttRow in compSttRows:
                        cid=str(sttRow.cid).strip().upper()
                        s_key=str(sttRow.s_key).strip().upper()
                        s_value=str(sttRow.s_value).strip()
                        
                        if (cid==c_id and s_key=='AUTO_DELIVERY' and s_value=='YES'):
                            autoDelivery=True
                        elif (cid==c_id and s_key=='INVOICE_RULES' and s_value=='YES'):
                            invoiceRulesFlag=True                     
                        elif (cid==c_id and s_key=='PARTIAL_DELIVERY' and s_value=='YES'):
                            partigalStockFlag=True
                        elif (cid==c_id and s_key=='NEGETIVE_STOCK' and s_value=='YES'):
                            negativeStockFlag=True
                        elif (cid==c_id and s_key=='RESTRICTED_STOCK' and s_value=='YES'):
                            restrictedStockFlag=True
                        elif (cid==c_id and s_key=='ACHIEVEMENT_FLAG' and s_value=='YES'):
                            achieveRowsFlag=True
                    
                    #---------------------- to update achievement in target table
                    if achieveRowsFlag==True:
                        depotList=[]
                        depotRows=db(db.sm_depot.cid==c_id).select(db.sm_depot.cid,db.sm_depot.depot_id,db.sm_depot.reporting_level_id,db.sm_depot.reporting_level_name)
                        depotList=depotRows.as_list()
                    
                    #----------- record range
                    maxRecord=100
                    limitby=(0,maxRecord)
                    #--------------------
                    
                    #======================================= ORDER TO DELIVERY USING PROCESSING RULES
                    #===========================Note: status have 'Draft,Submitted,Invoiced,Cancelled'
                    if autoDelivery==True:                        
                        #-------------------------- if invoice rules needed to apply
                        specificItemFlag=False
                        anyItemFlag=False  
                        if invoiceRulesFlag==True:
                            #---------- check invoice rules category and status                                                  
                            invRulesRows=db((db.uni_middle.table_name=='INVOICE_RULES')&(db.uni_middle.cid==c_id)).select(db.uni_middle.cid,db.uni_middle.str1,db.uni_middle.dt1,db.uni_middle.dt2,db.uni_middle.str2,db.uni_middle.num1,db.uni_middle.num2,db.uni_middle.str3,db.uni_middle.str4,db.uni_middle.dbl1,db.uni_middle.str5,orderby=~db.uni_middle.sl)
                            for invRow in invRulesRows:
                                itemFor=str(invRow.str2).strip().upper()
                                itemRulesStatus=invRow.str5                            
                                if (itemFor=='ANY' and itemRulesStatus=='ACTIVE'):
                                    anyItemFlag=True
                                elif (itemFor!='ANY' and itemRulesStatus=='ACTIVE'):
                                    specificItemFlag=True
                            
                            #------------ restricted stock records
                            restItemRows=db((db.uni_middle.table_name=='RESTRICTED_STOCK_ITEM')&(db.uni_middle.cid==c_id)).select(db.uni_middle.cid,db.uni_middle.str1,db.uni_middle.num1,db.uni_middle.str4,orderby=~db.uni_middle.sl)
                            
                            #---------------- client records for category
                            clientList=[]
                            clientRecords=db(db.sm_client.cid==c_id).select(db.sm_client.client_id,db.sm_client.credit_limit,db.sm_client.depot_id,db.sm_client.category_id,orderby=db.sm_client.name,limitby=limitby)
                            clientList=clientRecords.as_list()
                        #-------------------------------------------------------------
                        
                        #----------------- order head records
                        orderHeadRecords=db((db.sm_order_head.cid==c_id)&(db.sm_order_head.status=='Submitted')&(db.sm_order_head.flag_data=='0')).select(db.sm_order_head.id,db.sm_order_head.depot_id,db.sm_order_head.sl,db.sm_order_head.client_id,db.sm_order_head.order_date,limitby=(0,20))
                        for ordHeadRow in orderHeadRecords:
                            depot_id=ordHeadRow.depot_id
                            sl=ordHeadRow.sl
                            clientId=ordHeadRow.client_id
                            orderDate=ordHeadRow.order_date
                            
                            #---------- get client category for invoice rules (Note: alternative way direct select statemet with condition cid,depotid,clientid)
                            clientCategory=''
                            creditLimit=0
                            if (invoiceRulesFlag==True and (anyItemFlag==True or specificItemFlag==True)):
                                for i in range(len(clientList)):
                                    clientDict=clientList[i]
                                    clientID=clientDict['client_id']
                                    creditLimit=clientDict['credit_limit']
                                    depotID=clientDict['depot_id']
                                    categoryID=clientDict['category_id']
                                    if (str(clientID).strip()==str(clientId).strip() and str(depotID).strip()==str(depot_id).strip()):
                                        clientCategory=categoryID
                                        break
                            
                            #-------------------- get current stock records
                            qry2 = db.sm_depot_stock_balance.cid==c_id 
                            qry2 &= db.sm_depot_stock_balance.depot_id==depot_id
                            balanceRecords =db(qry2).select(db.sm_depot_stock_balance.id,db.sm_depot_stock_balance.item_id,db.sm_depot_stock_balance.quantity)
                            
                            #----------- get delivery max sl from depot
                            records=db((db.sm_depot.cid==c_id) & (db.sm_depot.depot_id==depot_id)).select(db.sm_depot.id,db.sm_depot.del_sl,limitby=(0,1))
                            if records:
                                dsl=records[0].del_sl
                                maxSl=int(dsl)+1
                            else:
                                maxSl=1                        
                            #--- sl update in depot
                            records[0].update_record(del_sl=maxSl)
                            
                            #---------------   order detail records
                            depot_name=''
                            client_id=''
                            client_name=''
                            rep_id=''
                            rep_name=''
                            area_id=''
                            area_name=''
                            order_datetime=''
                            payment_mode=''
                            req_note=''
                            ym_date=''
                            req_delivery_date=''
                            
                            #----------------
                            headDict={}   
                            headList=[]                                               
                            detailDict={}
                            detailList=[]                            
                            headFlag=False
                                                      
                            totalAmount=0
                            discount=0                            
                            orderRecords=db((db.sm_order.cid==c_id) & (db.sm_order.depot_id==depot_id) &(db.sm_order.sl==sl)&(db.sm_order.status=='Submitted')).select(db.sm_order.ALL,orderby=db.sm_order.item_name)
                            for row in orderRecords:                                
                                rowId=row.id     
                                depot_id=row.depot_id
                                depot_name=row.depot_name
                                client_id=row.client_id
                                client_name=row.client_name
                                rep_id=row.rep_id
                                rep_name=row.rep_name
                                area_id=row.area_id
                                area_name=row.area_name                                
                                order_datetime=row.order_datetime
                                payment_mode=row.payment_mode                            
                                req_note=row.note                                
                                item_id=str(row.item_id).strip().upper()
                                item_name=row.item_name
                                category_id=row.category_id
                                item_qty_value=int(row.quantity)
                                price=float(row.price)                                
                                #----- delivery date get from order date
                                ym_date=str(order_datetime)[0:7]+'-01'
                                req_delivery_date=str(order_datetime)[0:10]
                                
                                bonus_qty=0
                                itemTotal=price*item_qty_value                                
                                totalAmount+=itemTotal
                                
                                short_note=''
                                
                                #--------------- invoice rules apply ; bonus qty no problem, discout+=discount, how to update discount?
                                if (invoiceRulesFlag==True and anyItemFlag==False and specificItemFlag==True):                                
                                    for invRow in invRulesRows:
                                        client_category=str(invRow.str1).strip()
                                        dateFrom=invRow.dt1
                                        dateTo=invRow.dt2
                                        itemFor=str(invRow.str2).strip().upper()
                                        limitFrom=invRow.num1
                                        limitTo=invRow.num2
                                        bonusType=invRow.str3
                                        bonus_item=invRow.str4
                                        bonus_disc_qty_amt_per=float(invRow.dbl1)
                                        itemRulesStatus=invRow.str5
                                        
                                        #--------- bonus qty for per limited qty
                                        if  (client_category==clientCategory and (orderDate>=dateFrom and orderDate<=dateTo) and itemFor==item_id and limitFrom==limitTo and itemRulesStatus=='ACTIVE'):
                                            if (bonusType=='Item' and bonus_item==item_id):
                                                qtySlap=int(item_qty_value)/int(limitFrom)
                                                qtySlap=int(qtySlap)
                                                bonus_qty=qtySlap*int(bonus_disc_qty_amt_per)
                                                short_note='bonus %s'%(bonus_qty)
                                                break
                                            elif bonusType=='Item' and bonus_item!=item_id:
                                                    itemId=''
                                                    itemName=''
                                                    categoryId=''
                                                    itemRows=db((db.sm_item.cid==c_id) & (db.sm_item.item_id==bonus_item)).select(db.sm_item.item_id,db.sm_item.name,db.sm_item.category_id,limitby=(0,1))
                                                    if itemRows:
                                                        itemId=itemRows[0].item_id
                                                        itemName=itemRows[0].name
                                                        categoryId=itemRows[0].category_id
                                                    
                                                    qtySlap=int(item_qty_value)/int(limitFrom)
                                                    qtySlap=int(qtySlap)
                                                    bonusQty=qtySlap*int(bonus_disc_qty_amt_per)
                                                    
                                                    short_note='bonus item %s (%s)'%(itemId,bonusQty)
                                                    shortNote='bonus for %s'%(item_id)
                                                    #------------
                                                    detailDict={'cid':c_id,'depot_id':depot_id,'depot_name':depot_name,'sl':maxSl,'order_sl':sl,'client_id':client_id,'client_name':client_name,'rep_id':rep_id,'rep_name':rep_name,'order_datetime':order_datetime,'delivery_date':req_delivery_date,'payment_mode':payment_mode,'note':req_note,
                                                                   'area_id':area_id,'area_name':area_name,'status':'Invoiced','item_id':itemId,'item_name':itemName,'category_id':categoryId,'quantity':0,'bonus_qty':bonusQty,'price':0,'ym_date':ym_date,'short_note':shortNote}
                                                    detailList.append(detailDict)                                            
                                                    break
                                                
                                        #--------------- bonus qty,discout amt,discount percent
                                        else:                   
                                            if (client_category==clientCategory and (orderDate>=dateFrom and orderDate<=dateTo) and itemFor==item_id and (item_qty_value>=limitFrom and item_qty_value<=limitTo) and itemRulesStatus=='ACTIVE'): 
                                                if bonusType=='DiscPer':
                                                    disAmt=(itemTotal*bonus_disc_qty_amt_per)/100
                                                    discount+=disAmt
                                                    short_note='discount %s'%(disAmt)
                                                    break                                          
                                                elif bonusType=='DiscAmt':
                                                    disAmt=bonus_disc_qty_amt_per
                                                    discount+=disAmt
                                                    short_note='discount %s'%(disAmt)
                                                    break
                                                elif (bonusType=='Item' and bonus_item==item_id):
                                                    bonus_qty=int(bonus_disc_qty_amt_per)
                                                    short_note='bonus %s'%(bonus_qty)
                                                    break
                                                elif bonusType=='Item' and bonus_item!=item_id:
                                                    itemId=''
                                                    itemName=''
                                                    categoryId=''
                                                    itemRows=db((db.sm_item.cid==c_id) & (db.sm_item.item_id==bonus_item)).select(db.sm_item.item_id,db.sm_item.name,db.sm_item.category_id,limitby=(0,1))
                                                    if itemRows:
                                                        itemId=itemRows[0].item_id
                                                        itemName=itemRows[0].name
                                                        categoryId=itemRows[0].category_id
                                                    
                                                    bonusQty=int(bonus_disc_qty_amt_per)
                                                    
                                                    short_note='bonus item %s (%s)'%(itemId,bonusQty)
                                                    shortNote='bonus for %s'%(item_id)
                                                    #------------
                                                    detailDict={'cid':c_id,'depot_id':depot_id,'depot_name':depot_name,'sl':maxSl,'order_sl':sl,'client_id':client_id,'client_name':client_name,'rep_id':rep_id,'rep_name':rep_name,'order_datetime':order_datetime,'delivery_date':req_delivery_date,'payment_mode':payment_mode,'note':req_note,
                                                                   'area_id':area_id,'area_name':area_name,'status':'Invoiced','item_id':itemId,'item_name':itemName,'category_id':categoryId,'quantity':0,'bonus_qty':bonusQty,'price':0,'ym_date':ym_date,'short_note':shortNote}
                                                    detailList.append(detailDict)                                            
                                                    break
                                
                                #-------------------- get current stock balance for a specific item
                                totalReqQty=item_qty_value+bonus_qty
                                current_stock_Qty=0
                                for balRow in balanceRecords:
                                    bal_item_id=balRow.item_id
                                    bal_quantity=balRow.quantity
                                    if bal_item_id==item_id:
                                        current_stock_Qty=bal_quantity
                                        break
                                
                                #------------ check current stock with requet stock
                                stockFlag=True
                                if (current_stock_Qty < totalReqQty):
                                    stockFlag=False
                                
                                #------------
                                detailDict={'cid':c_id,'depot_id':depot_id,'depot_name':depot_name,'sl':maxSl,'order_sl':sl,'client_id':client_id,'client_name':client_name,'rep_id':rep_id,'rep_name':rep_name,'order_datetime':order_datetime,'delivery_date':req_delivery_date,'payment_mode':payment_mode,'note':req_note,
                                               'area_id':area_id,'area_name':area_name,'status':'Invoiced','item_id':item_id,'item_name':item_name,'category_id':category_id,'quantity':item_qty_value,'bonus_qty':bonus_qty,'price':price,'ym_date':ym_date,'short_note':short_note}
                                detailList.append(detailDict)
                                if headFlag==False:
                                    headDict={'cid':c_id,'depot_id':depot_id,'depot_name':depot_name,'sl':maxSl,'order_sl':sl,'client_id':client_id,'client_name':client_name,'rep_id':rep_id,'rep_name':rep_name,'order_datetime':order_datetime,'delivery_date':req_delivery_date,'payment_mode':payment_mode,'note':req_note,
                                               'area_id':area_id,'area_name':area_name,'status':'Invoiced','ym_date':ym_date}
                                    headList.append(headDict)
                                    headFlag=True
                            
                            #------------ rules for total amount
                            if (invoiceRulesFlag==True and anyItemFlag==True and specificItemFlag==False):                                
                                for invRow in invRulesRows:
                                    client_category=str(invRow.str1).strip()
                                    dateFrom=invRow.dt1
                                    dateTo=invRow.dt2
                                    itemFor=str(invRow.str2).strip().upper()
                                    limitFrom=invRow.num1
                                    limitTo=invRow.num2
                                    bonusType=invRow.str3
                                    bonus_item=invRow.str4
                                    bonus_disc_qty_amt_per=float(invRow.dbl1)
                                    itemRulesStatus=invRow.str5                                    
                                    if (client_category==clientCategory and (orderDate>=dateFrom and orderDate<=dateTo) and itemFor=='ANY' and (totalAmount>=limitFrom and totalAmount<=limitTo) and itemRulesStatus=='ACTIVE'): 
                                        if bonusType=='DiscPer':
                                            discount=(totalAmount*bonus_disc_qty_amt_per)/100
                                            break                                          
                                        elif bonusType=='DiscAmt':
                                            discount=bonus_disc_qty_amt_per
                                            break
                                        elif bonusType=='Item':
                                            itemId=''
                                            itemName=''
                                            categoryId=''
                                            itemRows=db((db.sm_item.cid==c_id) & (db.sm_item.item_id==bonus_item)).select(db.sm_item.item_id,db.sm_item.name,db.sm_item.category_id,limitby=(0,1))
                                            if itemRows:
                                                itemId=itemRows[0].item_id
                                                itemName=itemRows[0].name
                                                categoryId=itemRows[0].category_id
                                            
                                            bonusQty=bonus_disc_qty_amt_per
                                            shortNote='bonus for total amount'
                                            #------------
                                            detailDict={'cid':c_id,'depot_id':depot_id,'depot_name':depot_name,'sl':maxSl,'order_sl':sl,'client_id':client_id,'client_name':client_name,'rep_id':rep_id,'rep_name':rep_name,'order_datetime':order_datetime,'delivery_date':req_delivery_date,'payment_mode':payment_mode,'note':req_note,
                                                           'area_id':area_id,'area_name':area_name,'status':'Invoiced','item_id':itemId,'item_name':itemName,'category_id':categoryId,'quantity':0,'bonus_qty':bonusQty,'price':0,'ym_date':ym_date,'short_note':shortNote}
                                            detailList.append(detailDict)                                            
                                            break
                            #-----------------
                            totalAmount=totalAmount-discount                            
                            
                            #--------------
                            if (len(headList)> 0 and len(detailList) > 0):
                                #---------- dicount amount assigned
                                for i in range(len(headList)):
                                    headDictData=headList[i]
                                    headDictData['discount']=discount
                                    
                                for j in range(len(detailList)):
                                    detailDictData=detailList[j]
                                    detailDictData['discount']=discount
                                
                                #------------- call balance update function
                                strData=str(c_id)+'<fdfd>DELIVERY<fdfd>'+str(maxSl)+'<fdfd>'+str(datetime_fixed)+'<fdfd>'+str(depot_id)+'-'+str(maxSl)+'<fdfd>DPT-'+str(depot_id)+'<fdfd>CLT-'+str(client_id)+'<fdfd>'+str(totalAmount)
                                
                                if strData!='':
                                    resStr=set_balance_transaction(strData)
                                    
                                    resStrList=resStr.split('<sep>',resStr.count('<sep>'))
                                    flag=resStrList[0]
                                    msg=resStrList[1]
                                    if flag=='True':
                                        #Update status of head and detail
                                        
                                        rows=db.sm_invoice.bulk_insert(detailList)
                                        rows=db.sm_invoice_head.bulk_insert(headList)                        
                                        db((db.sm_order_head.cid==c_id) & (db.sm_order_head.depot_id==depot_id) & (db.sm_order_head.client_id==client_id)&(db.sm_order_head.sl==sl)).update(status='Invoiced',delivery_date=req_delivery_date,invoice_ref=maxSl)
                                        db((db.sm_order.cid==c_id) & (db.sm_order.depot_id==depot_id) & (db.sm_order.client_id==client_id)&(db.sm_order.sl==sl)).update(status='Invoiced',delivery_date=req_delivery_date,invoice_ref=maxSl)
                                        db.commit()
                                        
                            #-------------- end order
                            
                    
                    #===========================REQUISITION (Update-sm_depot_stock)
                    reqRecords=db((db.sm_requisition.cid==c_id)&(db.sm_requisition.status=='Posted')&(db.sm_requisition.flag_depot_stock==0)).select(db.sm_requisition.id,db.sm_requisition.cid,
                           db.sm_requisition.depot_id,db.sm_requisition.ym_date,db.sm_requisition.item_id,db.sm_requisition.quantity,limitby=limitby)
                    for reqRec in reqRecords:
                        rowId=reqRec.id
                        cid=reqRec.cid
                        depot_id=reqRec.depot_id
                        ym_date=reqRec.ym_date
                        item_id=reqRec.item_id
                        itemQty=reqRec.quantity
                        
                        try:
                            #------------------ depot stock part
                            query1 = db.sm_depot_stock.cid==cid 
                            query1 &= db.sm_depot_stock.depot_id==depot_id
                            query1 &= db.sm_depot_stock.ym_date==ym_date
                            query1 &= db.sm_depot_stock.item_id==item_id
                            records=db(query1).select(db.sm_depot_stock.id,db.sm_depot_stock.req_qty)
                            if records:                 
                                records[0].update_record(req_qty=(records[0].req_qty+itemQty))
                            else: 
                                db.sm_depot_stock.insert(cid=cid,depot_id=depot_id,ym_date=ym_date,item_id=item_id,req_qty=itemQty) #insert
                            
                            #------------ Update requisition flag
                            query2 = db.sm_requisition.id==rowId 
                            query2 &= db.sm_requisition.cid==cid
                            query2 &= db.sm_requisition.depot_id==depot_id
                            
                            reqUpdate=db(query2).update(flag_depot_stock=1)
                        except:
                            return 'Process error in Requisition.Error:101'
                    #-------------- end Requisition
                
                
                    #========================== ISSUE (Update-sm_depot_stock,sm_depot_stock_balance)
                    issueRecords=db((db.sm_issue.cid==c_id)&(db.sm_issue.status=='Posted')&(db.sm_issue.flag_depot_stock==0)&(db.sm_issue.flag_depot_stock_balance==0)).select(db.sm_issue.ALL,limitby=limitby)
                    for issRec in issueRecords:
                        rowId=issRec.id
                        cid=issRec.cid
                        depot_id=issRec.depot_id
                        ym_date=issRec.ym_date
                        item_id=issRec.item_id
                        itemQty=issRec.quantity
                        bonus_qty=issRec.bonus_qty        
                        
                        totalQty=itemQty+bonus_qty        
                        try:
                            #------------------ depot stock part
                            query1 = db.sm_depot_stock.cid==cid 
                            query1 &= db.sm_depot_stock.depot_id==depot_id
                            query1 &= db.sm_depot_stock.ym_date==ym_date  
                            query1 &= db.sm_depot_stock.item_id==item_id      
                            records=db(query1).select(db.sm_depot_stock.id,db.sm_depot_stock.quantity,db.sm_depot_stock.iss_qty)
                            if records:
                                balanceQty=records[0].quantity-totalQty
                                issueQty=records[0].iss_qty+totalQty      
                                records[0].update_record(quantity=balanceQty,iss_qty=issueQty)
                            else: 
                                balanceQty=totalQty*(-1)
                                insert_rows=db.sm_depot_stock.insert(cid=cid,depot_id=depot_id,ym_date=ym_date,item_id=item_id,quantity=balanceQty,iss_qty=totalQty) #insert
                            
                            #---------------------- depot stock balance part    
                            qry2 = db.sm_depot_stock_balance.cid==cid 
                            qry2 &= db.sm_depot_stock_balance.depot_id==depot_id    
                            qry2 &= db.sm_depot_stock_balance.item_id==item_id
                            balanceRecords =db(qry2).select(db.sm_depot_stock_balance.id,db.sm_depot_stock_balance.quantity)
                            if balanceRecords:
                                balance_Qty=balanceRecords[0].quantity-totalQty
                                balanceRecords[0].update_record(quantity=balance_Qty)
                            else:
                                balance_Qty=totalQty*(-1) 
                                insert_rows=db.sm_depot_stock_balance.insert(cid=cid,depot_id=depot_id,item_id=item_id,quantity=balance_Qty) #insert
                            
                            #-------------- Update issue flag
                            query3 = db.sm_issue.id==rowId 
                            query3 &= db.sm_issue.cid==cid
                            query3 &= db.sm_issue.depot_id==depot_id            
                            reqUpdate=db(query3).update(flag_depot_stock=1,flag_depot_stock_balance=1)
                        except:
                            return 'Process error in Issue.Error:102'
                    #-------------- end issue
                    
                    
                    #========================== RECEIVE (Update-sm_depot_stock,sm_depot_stock_balance)
                    receiveRecords=db((db.sm_receive.cid==c_id)&(db.sm_receive.status=='Posted')&(db.sm_receive.flag_depot_stock==0)&(db.sm_receive.flag_depot_stock_balance==0)).select(db.sm_receive.ALL,limitby=limitby)
                    for recRec in receiveRecords:
                        rowId=recRec.id
                        cid=recRec.cid
                        depot_id=recRec.depot_id
                        ym_date=recRec.ym_date
                        item_id=recRec.item_id
                        itemQty=recRec.quantity
                        bonus_qty=recRec.bonus_qty        
                        
                        totalQty=itemQty+bonus_qty        
                        try:
                            #------------------ depot stock part
                            query1 = db.sm_depot_stock.cid==cid 
                            query1 &= db.sm_depot_stock.depot_id==depot_id
                            query1 &= db.sm_depot_stock.ym_date==ym_date  
                            query1 &= db.sm_depot_stock.item_id==item_id      
                            records=db(query1).select(db.sm_depot_stock.id,db.sm_depot_stock.quantity,db.sm_depot_stock.rec_qty)
                            if records:
                                balanceQty=records[0].quantity+totalQty
                                receiveQty=records[0].rec_qty+totalQty      
                                records[0].update_record(quantity=balanceQty,rec_qty=receiveQty)
                            else:
                                insert_rows=db.sm_depot_stock.insert(cid=cid,depot_id=depot_id,ym_date=ym_date,item_id=item_id,quantity=totalQty,rec_qty=totalQty) #insert
                            
                            #---------------------- depot stock balance part    
                            qry2 = db.sm_depot_stock_balance.cid==cid 
                            qry2 &= db.sm_depot_stock_balance.depot_id==depot_id    
                            qry2 &= db.sm_depot_stock_balance.item_id==item_id
                            balanceRecords =db(qry2).select(db.sm_depot_stock_balance.id,db.sm_depot_stock_balance.quantity)
                            if balanceRecords:
                                balance_Qty=balanceRecords[0].quantity+totalQty
                                balanceRecords[0].update_record(quantity=balance_Qty)
                            else:
                                insert_rows=db.sm_depot_stock_balance.insert(cid=cid,depot_id=depot_id,item_id=item_id,quantity=totalQty) #insert
                            
                            #-------------- Update receive flag
                            query3 = db.sm_receive.id==rowId 
                            query3 &= db.sm_receive.cid==cid
                            query3 &= db.sm_receive.depot_id==depot_id            
                            reqUpdate=db(query3).update(flag_depot_stock=1,flag_depot_stock_balance=1)
                        except:
                            return 'Process error in Receive.Error:103'
                    #-------------- end receive
                    
                    #========================== DAMAGE (Update-sm_depot_stock,sm_depot_stock_balance)
                    damageRecords=db((db.sm_damage.cid==c_id)&(db.sm_damage.status=='Posted')&(db.sm_damage.flag_depot_stock==0)&(db.sm_damage.flag_depot_stock_balance==0)).select(db.sm_damage.ALL,limitby=limitby)
                    for damRec in damageRecords:
                        rowId=damRec.id
                        cid=damRec.cid
                        depot_id=damRec.depot_id
                        ym_date=damRec.ym_date
                        item_id=damRec.item_id
                        itemQty=damRec.quantity
                        
                        try:
                            #------------------ depot stock part
                            query1 = db.sm_depot_stock.cid==cid 
                            query1 &= db.sm_depot_stock.depot_id==depot_id
                            query1 &= db.sm_depot_stock.ym_date==ym_date  
                            query1 &= db.sm_depot_stock.item_id==item_id      
                            records=db(query1).select(db.sm_depot_stock.id,db.sm_depot_stock.quantity,db.sm_depot_stock.dam_qty)
                            if records:
                                balanceQty=records[0].quantity-itemQty
                                damageQty=records[0].dam_qty+itemQty      
                                records[0].update_record(quantity=balanceQty,dam_qty=damageQty)
                            else: 
                                balanceQty=itemQty*(-1)
                                insert_rows=db.sm_depot_stock.insert(cid=cid,depot_id=depot_id,ym_date=ym_date,item_id=item_id,quantity=balanceQty,dam_qty=itemQty) #insert
                            
                            #---------------------- depot stock balance part    
                            qry2 = db.sm_depot_stock_balance.cid==cid 
                            qry2 &= db.sm_depot_stock_balance.depot_id==depot_id    
                            qry2 &= db.sm_depot_stock_balance.item_id==item_id
                            balanceRecords =db(qry2).select(db.sm_depot_stock_balance.id,db.sm_depot_stock_balance.quantity)
                            if balanceRecords:
                                balance_Qty=balanceRecords[0].quantity-itemQty
                                balanceRecords[0].update_record(quantity=balance_Qty)
                            else:
                                balance_Qty=itemQty*(-1) 
                                insert_rows=db.sm_depot_stock_balance.insert(cid=cid,depot_id=depot_id,item_id=item_id,quantity=balance_Qty) #insert
                            
                            #-------------- Update damage flag
                            query3 = db.sm_damage.id==rowId 
                            query3 &= db.sm_damage.cid==cid
                            query3 &= db.sm_damage.depot_id==depot_id            
                            reqUpdate=db(query3).update(flag_depot_stock=1,flag_depot_stock_balance=1)
                        except:
                            return 'Process error in Damage.Error:104'
                    #-------------- end damage
                    
                    #===========================ORDER (Update-sm_depot_stock) Note: status have 'Draft,Submitted,Invoiced,Cancelled'
                    orderRecords=db((db.sm_order.cid==c_id)&(db.sm_order.status=='Submitted')&(db.sm_order.status=='Invoiced')&(db.sm_order.flag_depot_stock==0)).select(db.sm_order.ALL,limitby=limitby)
                    for ordRec in orderRecords:
                        rowId=ordRec.id
                        cid=ordRec.cid
                        depot_id=ordRec.depot_id
                        ym_date=ordRec.ym_date
                        item_id=ordRec.item_id
                        itemQty=ordRec.quantity
                        
                        try:
                            #------------------ depot stock part
                            query1 = db.sm_depot_stock.cid==cid 
                            query1 &= db.sm_depot_stock.depot_id==depot_id
                            query1 &= db.sm_depot_stock.ym_date==ym_date
                            query1 &= db.sm_depot_stock.item_id==item_id
                            records=db(query1).select(db.sm_depot_stock.id,db.sm_depot_stock.ord_qty)
                            if records:                 
                                records[0].update_record(ord_qty=(records[0].ord_qty+itemQty))
                            else: 
                                db.sm_depot_stock.insert(cid=cid,depot_id=depot_id,ym_date=ym_date,item_id=item_id,ord_qty=itemQty) #insert
                            
                            #------------ Update order flag
                            query2 = db.sm_order.id==rowId 
                            query2 &= db.sm_order.cid==cid
                            query2 &= db.sm_order.depot_id==depot_id
                            
                            reqUpdate=db(query2).update(flag_depot_stock=1)
                        except:
                            return 'Process error in Order.Error:105'
                    #-------------- end order
                    
                    
                    #========================== INVOICE (Update-sm_depot_stock,sm_depot_stock_balance,sm_target)
                    invoiceRecords=db((db.sm_invoice.cid==c_id)&(db.sm_invoice.status=='Invoiced')&(db.sm_invoice.flag_depot_stock==0)&(db.sm_invoice.flag_depot_stock_balance==0)).select(db.sm_invoice.ALL,limitby=limitby)
                    for invRec in invoiceRecords:
                        rowId=invRec.id
                        cid=invRec.cid
                        depot_id=invRec.depot_id
                        rep_id=invRec.rep_id
                        ym_date=invRec.ym_date
                        item_id=invRec.item_id
                        itemQty=invRec.quantity 
                        itemPrice=invRec.price
                        bonus_qty=invRec.bonus_qty
                        
                        totalQty=itemQty+bonus_qty 
                        try:
                            #------------------ depot stock part
                            query1 = db.sm_depot_stock.cid==cid 
                            query1 &= db.sm_depot_stock.depot_id==depot_id
                            query1 &= db.sm_depot_stock.ym_date==ym_date  
                            query1 &= db.sm_depot_stock.item_id==item_id      
                            records=db(query1).select(db.sm_depot_stock.id,db.sm_depot_stock.quantity,db.sm_depot_stock.del_qty)
                            if records:
                                balanceQty=records[0].quantity-totalQty
                                deliveryQty=records[0].del_qty+totalQty      
                                records[0].update_record(quantity=balanceQty,del_qty=deliveryQty)
                            else: 
                                balanceQty=totalQty*(-1)
                                insert_rows=db.sm_depot_stock.insert(cid=cid,depot_id=depot_id,ym_date=ym_date,item_id=item_id,quantity=balanceQty,del_qty=totalQty) #insert
                            
                            #---------------------- depot stock balance part    
                            qry2 = db.sm_depot_stock_balance.cid==cid 
                            qry2 &= db.sm_depot_stock_balance.depot_id==depot_id    
                            qry2 &= db.sm_depot_stock_balance.item_id==item_id
                            balanceRecords =db(qry2).select(db.sm_depot_stock_balance.id,db.sm_depot_stock_balance.quantity)
                            if balanceRecords:
                                balance_Qty=balanceRecords[0].quantity-totalQty
                                balanceRecords[0].update_record(quantity=balance_Qty)
                            else:
                                balance_Qty=totalQty*(-1) 
                                insert_rows=db.sm_depot_stock_balance.insert(cid=cid,depot_id=depot_id,item_id=item_id,quantity=balance_Qty) #insert
                            
                            #---------------------- to update achievement in target table  
                            # sm_target: cid, depotID, reporting level_id, reporting level name, rep id, rep name, item id, item name, targetQty,targetAmt, achievementQty, achivementAmt
                            
                            if achieveRowsFlag:
                                levelID=''
                                levelName=''
                                for j in range(len(depotList)):
                                    depotData=depotList[j]
                                    c_id=depotData['cid']
                                    depotID=str(depotData['depot_id'])
                                    level_ID=str(depotData['reporting_level_id'])
                                    level_Name=str(depotData['reporting_level_name'])
                                    if (str(c_id)==str(cid) and depotID==str(depot_id)):
                                        levelID=level_ID
                                        levelName=level_Name
                                        break
                                
                                qry3 = db.sm_target.cid==cid 
                                qry3 &= db.sm_target.depot_id==depot_id   
                                qry3 &= db.sm_target.ym_date==ym_date 
                                qry3 &= db.sm_target.rep_id==rep_id 
                                qry3 &= db.sm_target.item_id==item_id
                                targetRecords =db(qry3).select(db.sm_target.id,db.sm_target.achievement_qty,db.sm_target.achievement_amount)
                                if targetRecords:
                                    achieveQty=targetRecords[0].achievement_qty+itemQty 
                                    achieveAmt=targetRecords[0].achievement_amount+(itemPrice*itemQty)
                                    targetRecords[0].update_record(achievement_qty=achieveQty,achievement_amount=achieveAmt)
                                else:
                                    achieveQty=itemQty
                                    achieveAmt=itemPrice*itemQty
                                    insert_rows=db.sm_target.insert(cid=cid,depot_id=depot_id,reporting_level_id=levelID,reporting_level_name=levelName,ym_date=ym_date,rep_id=rep_id,item_id=item_id,achievement_qty=achieveQty,achievement_amount=achieveAmt) #insert
                                
                            #---------------------
                            
                            #-------------- Update issue flag
                            query4 = db.sm_invoice.id==rowId 
                            query4 &= db.sm_invoice.cid==cid
                            query4 &= db.sm_invoice.depot_id==depot_id            
                            reqUpdate=db(query4).update(flag_depot_stock=1,flag_depot_stock_balance=1)
                        except:
                            return 'Process error in Invoice.Error:106'
                    #-------------- end invoice
                    
                    #========================== RETURN (Update-sm_depot_stock,sm_depot_stock_balance,sm_target)
                    returnRecords=db((db.sm_return.cid==c_id)&(db.sm_return.status=='Returned')&(db.sm_return.flag_depot_stock==0)&(db.sm_return.flag_depot_stock_balance==0)).select(db.sm_return.ALL,limitby=limitby)
                    for retRec in returnRecords:
                        rowId=retRec.id
                        cid=retRec.cid
                        depot_id=retRec.depot_id
                        rep_id=retRec.rep_id
                        ym_date=retRec.ym_date
                        item_id=retRec.item_id
                        itemQty=retRec.quantity 
                        itemPrice=retRec.price
                        bonus_qty=retRec.bonus_qty
                        
                        totalQty=itemQty+bonus_qty
                        
                        try:
                            #------------------ depot stock part
                            query1 = db.sm_depot_stock.cid==cid 
                            query1 &= db.sm_depot_stock.depot_id==depot_id
                            query1 &= db.sm_depot_stock.ym_date==ym_date  
                            query1 &= db.sm_depot_stock.item_id==item_id      
                            records=db(query1).select(db.sm_depot_stock.id,db.sm_depot_stock.quantity,db.sm_depot_stock.retn_qty)
                            if records:
                                balanceQty=records[0].quantity+totalQty
                                retnQty=records[0].retn_qty+totalQty      
                                records[0].update_record(quantity=balanceQty,retn_qty=retnQty)
                            else:
                                insert_rows=db.sm_depot_stock.insert(cid=cid,depot_id=depot_id,ym_date=ym_date,item_id=item_id,quantity=totalQty,retn_qty=totalQty) #insert
                            
                            #---------------------- depot stock balance part    
                            qry2 = db.sm_depot_stock_balance.cid==cid 
                            qry2 &= db.sm_depot_stock_balance.depot_id==depot_id    
                            qry2 &= db.sm_depot_stock_balance.item_id==item_id
                            balanceRecords =db(qry2).select(db.sm_depot_stock_balance.id,db.sm_depot_stock_balance.quantity)
                            if balanceRecords:
                                balance_Qty=balanceRecords[0].quantity+totalQty
                                balanceRecords[0].update_record(quantity=balance_Qty)
                            else:
                                insert_rows=db.sm_depot_stock_balance.insert(cid=cid,depot_id=depot_id,item_id=item_id,quantity=totalQty) #insert
                    
                            #---------------------- to update achievement in target table  
                            # sm_target: cid, depotID, reporting level_id, reporting level name, rep id, rep name, item id, item name, targetQty,targetAmt, achievementQty, achivementAmt
                            if achieveRowsFlag:
                                levelID=''
                                levelName=''
                                for j in range(len(depotList)):
                                    depotData=depotList[j]
                                    c_id=depotData['cid']
                                    depotID=str(depotData['depot_id'])
                                    level_ID=str(depotData['reporting_level_id'])
                                    level_Name=str(depotData['reporting_level_name'])
                                    if (str(c_id)==str(cid) and depotID==str(depot_id)):
                                        levelID=level_ID
                                        levelName=level_Name
                                        break    
                                
                                qry3 = db.sm_target.cid==cid 
                                qry3 &= db.sm_target.depot_id==depot_id   
                                qry3 &= db.sm_target.ym_date==ym_date 
                                qry3 &= db.sm_target.rep_id==rep_id 
                                qry3 &= db.sm_target.item_id==item_id
                                targetRecords =db(qry3).select(db.sm_target.id,db.sm_target.achievement_qty,db.sm_target.achievement_amount)
                                if targetRecords:
                                    achieveQty=targetRecords[0].achievement_qty-itemQty 
                                    achieveAmt=targetRecords[0].achievement_amount-(itemPrice*itemQty)
                                    targetRecords[0].update_record(achievement_qty=achieveQty,achievement_amount=achieveAmt)
                                else:
                                    achieveQty=itemQty*(-1)
                                    achieveAmt=itemPrice*itemQty*(-1)
                                    insert_rows=db.sm_target.insert(cid=cid,depot_id=depot_id,reporting_level_id=levelID,reporting_level_name=levelName,ym_date=ym_date,rep_id=rep_id,item_id=item_id,achievement_qty=achieveQty,achievement_amount=achieveAmt) #insert
                            
                            #-------------- Update issue flag
                            query4 = db.sm_return.id==rowId 
                            query4 &= db.sm_return.cid==cid
                            query4 &= db.sm_return.depot_id==depot_id            
                            reqUpdate=db(query4).update(flag_depot_stock=1,flag_depot_stock_balance=1)
                        except:
                            return 'Process error in Return.Error:107'
            
            stockCronRows[0].update_record(s_value='0')
            db.commit()
            
    return dict(message='done')      
            #-------------- end return


    