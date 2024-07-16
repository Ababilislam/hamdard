
#http://127.0.0.1:8000/skf/update_depot_transaction/update_transaction
#http://c003.businesssolutionapps.com/skf/update_depot_transaction/update_transaction

#======================= Cron Transaction Function
def update_transaction():    
    stockCronRows=db((db.sm_settings.cid=='SYS')&(db.sm_settings.s_key=='STOCK_CRON_FLAG')).select(db.sm_settings.id,db.sm_settings.s_value,limitby=(0,1))
    if stockCronRows:
        cronFlag=stockCronRows[0].s_value        
        
        if str(cronFlag)=='0':
            stockCronRows[0].update_record(s_value='1')
            
            settCompRows=db((db.sm_settings.s_key=='STOCK_CRON')&(db.sm_settings.s_value=='YES')).select(db.sm_settings.cid)
            if settCompRows:
                for row in settCompRows:
                    c_id=str(row.cid).strip().upper()
                    
                    #----------- record range
                    maxRecord=100
                    limitby=(0,maxRecord)
                    
                    #========================== ISSUE (Update-sm_depot_stock_balance (current stock))
                    issueRecords=db((db.sm_issue.cid==c_id)&(db.sm_issue.status=='Posted')&(db.sm_issue.flag_depot_stock_balance==0)).select(db.sm_issue.id,db.sm_issue.cid,db.sm_issue.depot_id,db.sm_issue.store_id,db.sm_issue.store_name,db.sm_issue.item_id,db.sm_issue.batch_id,db.sm_issue.quantity,db.sm_issue.bonus_qty,limitby=limitby)
                    for issRec in issueRecords:
                        depot_id=issRec.depot_id
                        store_id=issRec.store_id
                        store_name=issRec.store_name                
                        item_id=issRec.item_id
                        batch_id=issRec.batch_id
                        itemQty=issRec.quantity
                        bonus_qty=issRec.bonus_qty
                        
                        totalQty=itemQty+bonus_qty
                        try:
                            #---------------------- depot stock balance part
                            
                            balanceRecords=db((db.sm_depot_stock_balance.cid==c_id)&(db.sm_depot_stock_balance.depot_id==depot_id)&(db.sm_depot_stock_balance.store_id==store_id)&(db.sm_depot_stock_balance.item_id==item_id)&(db.sm_depot_stock_balance.batch_id==batch_id)).select(db.sm_depot_stock_balance.id,db.sm_depot_stock_balance.quantity,limitby=(0,1))
                            if balanceRecords:
                                balance_Qty=balanceRecords[0].quantity-totalQty
                                balanceRecords[0].update_record(quantity=balance_Qty)
                            else:
                                expiary_date=''
                                itemBatchRow=db((db.sm_item_batch.cid==c_id)&(db.sm_item_batch.item_id==item_id)&(db.sm_item_batch.batch_id==batch_id)).select(db.sm_item_batch.expiary_date,limitby=(0,1))
                                if itemBatchRow:
                                    expiary_date=itemBatchRow[0].expiary_date
                                
                                balance_Qty=totalQty*(-1)
                                insert_rows=db.sm_depot_stock_balance.insert(cid=c_id,depot_id=depot_id,store_id=store_id,store_name=store_name,item_id=item_id,batch_id=batch_id,expiary_date=expiary_date,quantity=balance_Qty) #insert
                            
                            #-------------- Update issue flag
                            
                            reqUpdate=issRec.update_record(flag_depot_stock_balance=1)
                        except:
                            return 'Process error in Issue.Error:102'
                    
                    issueRecords=''
                    #-------------- end issue
                    
                    
                    #========================== RECEIVE (Update-sm_depot_stock_balance)
                    receiveRecords=db((db.sm_receive.cid==c_id)&(db.sm_receive.status=='Posted')&(db.sm_receive.flag_depot_stock_balance==0)).select(db.sm_receive.id,db.sm_receive.cid,db.sm_receive.depot_id,db.sm_receive.store_id,db.sm_receive.store_name,db.sm_receive.item_id,db.sm_receive.batch_id,db.sm_receive.quantity,db.sm_receive.bonus_qty,limitby=limitby)
                    for recRec in receiveRecords:
                        depot_id=recRec.depot_id
                        store_id=recRec.store_id
                        store_name=recRec.store_name                     
                        item_id=recRec.item_id
                        batch_id=recRec.batch_id
                        itemQty=recRec.quantity
                        bonus_qty=recRec.bonus_qty        
                        
                        totalQty=itemQty+bonus_qty        
                        try:
                            #---------------------- depot stock balance part   (current stock )
                            
                            balanceRecords=db((db.sm_depot_stock_balance.cid==c_id)&(db.sm_depot_stock_balance.depot_id==depot_id)&(db.sm_depot_stock_balance.store_id==store_id)&(db.sm_depot_stock_balance.item_id==item_id)&(db.sm_depot_stock_balance.batch_id==batch_id)).select(db.sm_depot_stock_balance.id,db.sm_depot_stock_balance.quantity,limitby=(0,1))
                            if balanceRecords:
                                balance_Qty=balanceRecords[0].quantity+totalQty
                                balanceRecords[0].update_record(quantity=balance_Qty)
                            else:
                                expiary_date=''
                                itemBatchRow=db((db.sm_item_batch.cid==c_id)&(db.sm_item_batch.item_id==item_id)&(db.sm_item_batch.batch_id==batch_id)).select(db.sm_item_batch.expiary_date,limitby=(0,1))
                                if itemBatchRow:
                                    expiary_date=itemBatchRow[0].expiary_date
                                
                                insert_rows=db.sm_depot_stock_balance.insert(cid=c_id,depot_id=depot_id,store_id=store_id,store_name=store_name,item_id=item_id,batch_id=batch_id,expiary_date=expiary_date,quantity=totalQty) #insert
                                
                            #-------------- Update receive flag
                            
                            reqUpdate=recRec.update_record(flag_depot_stock_balance=1)
                        except:
                            return 'Process error in Receive.Error:103'
                            
                    receiveRecords=''
                    #-------------- end receive
                    
                    #========================== DAMAGE (Update-sm_depot_stock,sm_depot_stock_balance)
                    damageRecords=db((db.sm_damage.cid==c_id)&(db.sm_damage.status=='Posted')&(db.sm_damage.flag_depot_stock_balance==0)).select(db.sm_damage.ALL,limitby=limitby)
                    for damRec in damageRecords:
                        depot_id=damRec.depot_id
                        store_id=damRec.store_id
                        store_name=damRec.store_name
                        item_id=damRec.item_id
                        batch_id=damRec.batch_id
                        itemQty=damRec.quantity
                        damageType=str(damRec.adjustment_type)    #Positive, Negetive
                        
                        try:
                            #---------------------- depot stock balance part    -current stock
                            balanceRecords=db((db.sm_depot_stock_balance.cid==c_id)&(db.sm_depot_stock_balance.depot_id==depot_id)&(db.sm_depot_stock_balance.store_id==store_id)&(db.sm_depot_stock_balance.item_id==item_id)&(db.sm_depot_stock_balance.batch_id==batch_id)).select(db.sm_depot_stock_balance.id,db.sm_depot_stock_balance.quantity,limitby=(0,1))
                            if balanceRecords:
                                if damageType=='Positive':
                                    balance_Qty=balanceRecords[0].quantity+itemQty
                                else:
                                    balance_Qty=balanceRecords[0].quantity-itemQty
                                    
                                balanceRecords[0].update_record(quantity=balance_Qty)
                            else:
                                expiary_date=''
                                itemBatchRow=db((db.sm_item_batch.cid==c_id)&(db.sm_item_batch.item_id==item_id)&(db.sm_item_batch.batch_id==batch_id)).select(db.sm_item_batch.expiary_date,limitby=(0,1))
                                if itemBatchRow:
                                    expiary_date=itemBatchRow[0].expiary_date
                                    
                                if damageType=='Positive':
                                    balance_Qty=itemQty
                                else:
                                    balance_Qty=itemQty*(-1) 
                                    
                                insert_rows=db.sm_depot_stock_balance.insert(cid=c_id,depot_id=depot_id,store_id=store_id,store_name=store_name,item_id=item_id,batch_id=batch_id,expiary_date=expiary_date,quantity=balance_Qty) #insert
                                
                            #-------------- Update damage flag
                            reqUpdate=damRec.update_record(flag_depot_stock_balance=1)
                            
                        except:
                            return 'Process error in Damage.Error:104'
                    damageRecords=''
                    #-------------- end damage
                    
                    #========================== INVOICE (sm_depot_stock_balance)
                    invoiceRecords=''
                    invoiceRecords=db((db.sm_invoice.cid==c_id)&(db.sm_invoice.status=='Invoiced')&(db.sm_invoice.flag_depot_stock_balance==0)).select(db.sm_invoice.ALL,limitby=limitby)
                    for invRec in invoiceRecords:                                             
                        depot_id=invRec.depot_id
                        store_id=invRec.store_id
                        store_name=invRec.store_name
                        item_id=invRec.item_id
                        batch_id=invRec.batch_id
                        itemQty=invRec.quantity
                        bonus_qty=invRec.bonus_qty
                        
                        totalQty=itemQty+bonus_qty
                        try:
                            #---------------------- depot stock balance part
                            
                            balanceRecords=db((db.sm_depot_stock_balance.cid==c_id)&(db.sm_depot_stock_balance.depot_id==depot_id)&(db.sm_depot_stock_balance.store_id==store_id)&(db.sm_depot_stock_balance.item_id==item_id)&(db.sm_depot_stock_balance.batch_id==batch_id)).select(db.sm_depot_stock_balance.id,db.sm_depot_stock_balance.quantity,limitby=(0,1))
                            if balanceRecords:
                                balance_Qty=balanceRecords[0].quantity-totalQty
                                balanceRecords[0].update_record(quantity=balance_Qty)
                            else:
                                expiary_date=''
                                itemBatchRow=db((db.sm_item_batch.cid==c_id)&(db.sm_item_batch.item_id==item_id)&(db.sm_item_batch.batch_id==batch_id)).select(db.sm_item_batch.expiary_date,limitby=(0,1))
                                if itemBatchRow:
                                    expiary_date=itemBatchRow[0].expiary_date
                                
                                balance_Qty=totalQty*(-1)
                                insert_rows=db.sm_depot_stock_balance.insert(cid=c_id,depot_id=depot_id,store_id=store_id,store_name=store_name,item_id=item_id,batch_id=batch_id,expiary_date=expiary_date,quantity=balance_Qty) #insert
                            
                            #-------------- Update issue flag
                            
                            reqUpdate=invRec.update_record(flag_depot_stock_balance=1)
                        except:
                            return 'Process error in Invoice.Error:106'
                    invoiceRecords=''
                    #-------------- end invoice
                    
                    #========================== RETURN (Update-sm_depot_stock,sm_depot_stock_balance,sm_target)
                    returnRecords=''
                    #returnRecords=db((db.sm_return.cid==c_id)&(db.sm_return.status=='Returned')&(db.sm_return.flag_depot_stock==0)&(db.sm_return.flag_depot_stock_balance==0)).select(db.sm_return.ALL,limitby=limitby)
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
                            #---------------------- depot stock balance part
                            
                            balanceRecords=''
                            qry2=db((db.sm_depot_stock_balance.cid==cid)&(db.sm_depot_stock_balance.depot_id==depot_id)&(db.sm_depot_stock_balance.item_id==item_id))
                            
                            balanceRecords =qry2.select(db.sm_depot_stock_balance.id,db.sm_depot_stock_balance.quantity,limitby=(0,1))
                            if balanceRecords:
                                balance_Qty=balanceRecords[0].quantity+totalQty
                                balanceRecords[0].update_record(quantity=balance_Qty)
                            else:
                                insert_rows=db.sm_depot_stock_balance.insert(cid=cid,depot_id=depot_id,item_id=item_id,quantity=totalQty) #insert
                                
                            #-------------- Update issue flag   
                            
                            query4=db((db.sm_return.id==rowId)&(db.sm_return.cid==cid)&(db.sm_return.depot_id==depot_id))
                                   
                            reqUpdate=query4.update(flag_depot_stock_balance=1)
                        except:
                            return 'Process error in Return.Error:107'
                    returnRecords=''
                    #----------------------- 
            settCompRows=''
            stockCronRows[0].update_record(s_value='0')
            db.commit()
    
    return 'Done'
    #-------------- end return


    