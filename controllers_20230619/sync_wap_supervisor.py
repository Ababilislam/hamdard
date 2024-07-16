#Billal

import urllib2
#http://127.0.0.1:8000/mreporting/sync_wap_supervisor/check_user?cid=DEMO&uid=ADMIN&password=123
def check_user(): 
    cid=str(urllib2.unquote(request.vars.cid))
    uid=str(urllib2.unquote(request.vars.uid))
    password=str(urllib2.unquote(request.vars.password))
    
    #if cid,userid,pass blank    
    if (cid=='' or uid=='' or password==''):
        retMsg='failed<rdrd>CID,User ID and Password required'
        return retMsg
    else:
        #Check valid company
        
        comp_check_row=db((db.sm_company_settings.cid==cid) & (db.sm_company_settings.status=='ACTIVE')).select(db.sm_company_settings.status,limitby=(0,1))
        if not comp_check_row:
            retMsg='failed<rdrd>Invalid CID'
            return retMsg
        else:
            sup_check_row=db((db.sm_rep.cid==cid) & (db.sm_rep.rep_id==uid) & (db.sm_rep.password==password) & (db.sm_rep.user_type=='sup')  & (db.sm_rep.status=='ACTIVE')).select(db.sm_rep.level_id,db.sm_rep.field1,db.sm_rep.field2,db.sm_rep.note,limitby=(0,1))
            if not sup_check_row:
                retMsg='failed<rdrd>Invalid Authorization'
                return retMsg
            else:
                level_id=str(sup_check_row[0].level_id).strip()
                levelDepth=str(sup_check_row[0].field2).strip()     #level Depth
                
                colName='level'+str(levelDepth)
                
                sup_areaDepotRows=db((db.sm_level.cid==cid) & (db.sm_level.is_leaf=='1')& (db.sm_level[colName]==level_id)&(db.sm_depot.cid==cid) & (db.sm_depot.depot_category!='SUPER')&(db.sm_depot.depot_id==db.sm_level.depot_id)).select(db.sm_level.depot_id,db.sm_depot.name,orderby=db.sm_level.depot_id,groupby=db.sm_level.depot_id)       
#                return db._lastsql
                if not sup_areaDepotRows:
                    retMsg='failed<rdrd>Depot not available'
                    return retMsg
                else:
                    depotStr=''                    
                    for sup_areaDepotRow in sup_areaDepotRows:
                        depot_id=str(sup_areaDepotRow.sm_level.depot_id).strip().replace('-', ' ')
                        name=str(sup_areaDepotRow.sm_depot.name).strip().replace('-', ' ')                        
                        if depotStr=='':
                            depotStr=name+'-'+depot_id
                        else:
                            depotStr+='<fd>'+name+'-'+depot_id
                    
                    #----------------------------
                    itemStr=''
                    records=db(db.sm_item.cid==cid).select(db.sm_item.item_id,db.sm_item.name,db.sm_item.category_id,db.sm_item.price,db.sm_item.dist_price,orderby=db.sm_item.name)
                    for rec in records:
                        item_id=str(rec.item_id).replace(',', ' ')
                        name=str(rec.name).replace(',', ' ')
                        category_id=str(rec.category_id).replace(',', ' ')
                        price=str(rec.price)
                        dist_price=str(rec.dist_price)
                        
                        if itemStr=='':
                            itemStr=item_id+','+name+','+category_id+','+price+','+dist_price
                        else:
                            itemStr+='<fd>'+item_id+','+name+','+category_id+','+price+','+dist_price
                    
                    if itemStr=='':
                        retMsg='failed<rdrd>Item not available'
                        return retMsg
                    else:
                        retMsg='success<rdrd>'+depotStr+'<fdrd>'+itemStr
                        return retMsg

#def getItem():
#    cid=str(urllib2.unquote(request.vars.cid))
#    
#    itemStr=''
#    records=db(db.sm_item.cid==cid).select(db.sm_item.item_id,db.sm_item.name,db.sm_item.category_id,db.sm_item.price,orderby=db.sm_item.name)
#    for rec in records:
#        item_id=str(rec.item_id).replace(',', ' ')
#        name=str(rec.name).replace(',', ' ')
#        category_id=str(rec.category_id).replace(',', ' ')
#        price=str(rec.price)
#        
#        if itemStr=='':
#            itemStr=item_id+','+name+','+category_id+','+price
#        else:
#            itemStr+='<fd>'+item_id+','+name+','+category_id+','+price
#    
#    if itemStr=='':
#        retMsg='failed<rdrd>Item not available'
#        return retMsg
#    else:
#        retMsg='success<rdrd>'+itemStr
#        return retMsg


#Receive from Central Depot by supervisor for under depot
def primarySaleSubmit():
    cid=str(urllib2.unquote(request.vars.cid))
    uid=str(urllib2.unquote(request.vars.uid))
    depot_id=str(urllib2.unquote(request.vars.depot_id))
    submit_string=str(urllib2.unquote(request.vars.submit_string))
    
    itemStr=''
    comp_check_row=db((db.sm_company_settings.cid==cid) & (db.sm_company_settings.status=='ACTIVE')).select(db.sm_company_settings.status,limitby=(0,1))
    if not comp_check_row:
        retMsg='failed<rdrd>Invalid CID'
        return retMsg
    else:
        sup_check_row=db((db.sm_rep.cid==cid) & (db.sm_rep.rep_id==uid) & (db.sm_rep.user_type=='sup')  & (db.sm_rep.status=='ACTIVE')).select(db.sm_rep.name,db.sm_rep.level_id,db.sm_rep.field1,db.sm_rep.field2,db.sm_rep.note,limitby=(0,1))
        if not sup_check_row:
            retMsg='failed<rdrd>Invalid Authorization'
            return retMsg
        else:
            rep_name=str(sup_check_row[0].name).strip()
            level_id=str(sup_check_row[0].level_id).strip()
            levelDepth=str(sup_check_row[0].field2).strip()     #level Depth
            
            colName='level'+str(levelDepth)
            
            sup_areaDepotRows=db((db.sm_level.cid==cid) & (db.sm_level.is_leaf=='1')& (db.sm_level[colName]==level_id)&(db.sm_level.depot_id==depot_id)).select(db.sm_level.level_id,db.sm_level.level_name,orderby=db.sm_level.level_id,limitby=(0,1))       
            if not sup_areaDepotRows:
                retMsg='failed<rdrd>Depot not available. Please Check Your Valid Depot.'
                return retMsg
            else:
                depot_Rows=db((db.sm_depot.cid==cid) & (db.sm_depot.depot_id==depot_id)).select(db.sm_depot.id,db.sm_depot.name,db.sm_depot.receive_sl,limitby=(0,1)) 
                if not depot_Rows:
                    retMsg='failed<rdrd>Invalid Depot.'
                    return retMsg
                else:
                    depot_name=depot_Rows[0].name 
                    receive_sl=int(depot_Rows[0].receive_sl)+1
                      
                    superDepotRows=db((db.sm_depot.cid==cid) & (db.sm_depot.depot_category=='SUPER') & (db.sm_depot.status=='ACTIVE')).select(db.sm_depot.id,db.sm_depot.depot_id,db.sm_depot.name,db.sm_depot.issue_sl,limitby=(0,1))
                    if not superDepotRows:
                        retMsg='failed<rdrd>Invalid Client.Please Check Your Valid Client'
                        return retMsg
                    else:
                        suprer_depot_id=superDepotRows[0].depot_id
                        suprer_depot_name=superDepotRows[0].name
                        issue_sl=int(superDepotRows[0].issue_sl)+1
                        
                        #-- Update new sl
                        superDepotRows[0].update_record(issue_sl=issue_sl)
                        depot_Rows[0].update_record(receive_sl=receive_sl)
                        
                        #===================================
                        receive_depot_id=depot_id
                        
                        req_date=date_fixed
                        ym_date=str(req_date)[0:7]+'-01'
                        
                        #------------- Insert Issue and Receive
                        ins_list_Issue=[]
                        ins_list_Receive=[]
                        totalAmount=0
                        
                        itemList=submit_string.split('<rd>')        
                        for i in range(len(itemList)):
                            
                            itemDetList=str(itemList[i]).split('<fd>');
                            
                            if len(itemDetList)==6:
                                itemId = itemDetList[0];
                                itemName = itemDetList[1];
                                categoryId = itemDetList[2];
                                itemPrice = itemDetList[3];
                                itemPriceDist = itemDetList[4];
                                itemQty = itemDetList[5];
                                
                                temp_amount=float(itemPriceDist)*int(itemQty)                                        
                                totalAmount=totalAmount+temp_amount
                                
                                ins_list_Issue.append({'cid':cid,'depot_id':suprer_depot_id,'sl':issue_sl,'issued_to':receive_depot_id,'issue_date':req_date,'ym_date':ym_date,'note':'','item_id':itemId,'item_name':itemName,'quantity':itemQty,'dist_rate':itemPriceDist,'status':'Posted','issue_process_status':'Received'})
                                ins_list_Receive.append({'cid':cid,'depot_id':receive_depot_id,'sl':receive_sl,'receive_from':suprer_depot_id,'receive_date':req_date,'ref_sl':issue_sl,'item_id':itemId,'item_name':itemName,'quantity':itemQty,'dist_rate':itemPriceDist,'short_note':'','ym_date':ym_date,'note':'','status':'Posted'})  
                            
                        if len(ins_list_Issue) > 0:
                            try:
                                db.sm_issue_head.insert(cid=cid,depot_id=suprer_depot_id,sl=issue_sl,issued_to=receive_depot_id,issue_date=req_date,ym_date=ym_date,status='Posted',issue_process_status='Received')
                                db.sm_issue.bulk_insert(ins_list_Issue)
                                
                                db.sm_receive_head.insert(cid=cid,depot_id=receive_depot_id,sl=receive_sl,receive_from=suprer_depot_id,receive_date=req_date,ref_sl=issue_sl,ym_date=ym_date,note='',status='Posted')
                                db.sm_receive.bulk_insert(ins_list_Receive)
                            except:
                                db.rollback()
                                retMsg='failed<rdrd>Failed to process data'
                                return retMsg
                        
                        #=============                     
                        
                        #--------------------- depot balance
                        #format:cid<fdfd>tx_type<fdfd>sl<fdfd>datetime<fdfd>reference<fdfd>1st account with prefix<fdfd>2nd account with prefix<fdfd>tx_amount
                        
                        #------- condition used for IMPORT/FACTORY/OPENING
                        
                        strData2=str(cid)+'<fdfd>ISSUERECEIVE<fdfd>'+str(issue_sl)+'<fdfd>'+str(datetime_fixed)+'<fdfd>'+str(suprer_depot_id)+'-'+str(issue_sl)+':'+str(receive_depot_id)+'-'+str(receive_sl)+'<fdfd>DPT-'+str(suprer_depot_id)+'<fdfd>DPT-'+str(receive_depot_id)+'<fdfd>'+str(totalAmount)
                        
                        resStr2=set_balance_transaction(strData2)
                        
                        resStrList2=resStr2.split('<sep>',resStr2.count('<sep>'))
                        flag2=resStrList2[0]
                        msg2=resStrList2[1]
                        if flag2!='True':
                            db.rollback()
                            retMsg='failed<rdrd>Failed to process data'
                            return retMsg
                            
                        else:
                            retMsg='success<rdrd>'+str(receive_sl)
                            return retMsg
                            

def orderSubmit():
    cid=str(urllib2.unquote(request.vars.cid))
    uid=str(urllib2.unquote(request.vars.uid))
    depot_id=str(urllib2.unquote(request.vars.depot_id))
    submit_string=str(urllib2.unquote(request.vars.submit_string))
    
    itemStr=''
    comp_check_row=db((db.sm_company_settings.cid==cid) & (db.sm_company_settings.status=='ACTIVE')).select(db.sm_company_settings.status,limitby=(0,1))
    if not comp_check_row:
        retMsg='failed<rdrd>Invalid CID'
        return retMsg
    else:
        sup_check_row=db((db.sm_rep.cid==cid) & (db.sm_rep.rep_id==uid) & (db.sm_rep.user_type=='sup')  & (db.sm_rep.status=='ACTIVE')).select(db.sm_rep.name,db.sm_rep.level_id,db.sm_rep.field1,db.sm_rep.field2,db.sm_rep.note,limitby=(0,1))
        if not sup_check_row:
            retMsg='failed<rdrd>Invalid Authorization'
            return retMsg
        else:
            rep_name=str(sup_check_row[0].name).strip()
            level_id=str(sup_check_row[0].level_id).strip()
            levelDepth=str(sup_check_row[0].field2).strip()     #level Depth
            
            colName='level'+str(levelDepth)
            
            sup_areaDepotRows=db((db.sm_level.cid==cid) & (db.sm_level.is_leaf=='1')& (db.sm_level[colName]==level_id)&(db.sm_level.depot_id==depot_id)).select(db.sm_level.level_id,db.sm_level.level_name,orderby=db.sm_level.level_id,limitby=(0,1))       
            if not sup_areaDepotRows:
                retMsg='failed<rdrd>Depot Route not available'
                return retMsg
            else:
                route_id=str(sup_areaDepotRows[0].level_id).strip()
                route_name=str(sup_areaDepotRows[0].level_name).strip()
                
                depot_name_check=db((db.sm_depot.cid==cid) & (db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1)) 
                if not depot_name_check:
                    retMsg='failed<rdrd>Invalid Depot.Please Check Your Valid Depot'
                    return retMsg
                else:
                    depot_name=depot_name_check[0].name 
                    
                    row_client=db((db.sm_client.cid==cid)& (db.sm_client.depot_id==depot_id) & (db.sm_client.area_id==route_id) & (db.sm_client.status=='ACTIVE') ).select(db.sm_client.client_id,db.sm_client.name,limitby=(0,1))
                    if not row_client:
                        retMsg='failed<rdrd>Invalid Client.Please Check Your Valid Client'
                        return retMsg
                    else:
                        client_name=row_client[0].name
                        client_id=row_client[0].client_id
                        
                        #=============
                        #Get sl from sm_depot
                        sl=1
                        query_sl=db((db.sm_depot.cid==cid) & (db.sm_depot.depot_id==depot_id)).select(db.sm_depot.id,db.sm_depot.order_sl,limitby=(0,1))
                        if query_sl:
                            sl=int(query_sl[0].order_sl)+1
                        query_sl[0].update_record(order_sl=sl)
                        
                        order_date=str(date_fixed)[0:10]
                        delivery_date=date_fixed
                        ym_date=str(delivery_date)[0:7]+'-01'
                        
                        ins_list=[]
                        ins_dict={}
                        
                        itemList=submit_string.split('<rd>')        
                        for i in range(len(itemList)):
                            itemDetList=str(itemList[i]).split('<fd>');
                            itemId = itemDetList[0];
                            itemName = itemDetList[1];
                            categoryId = itemDetList[2];
                            itemPrice = itemDetList[3];
                            itemPriceDist = itemDetList[4];
                            itemQty = itemDetList[5];
                            
                            ins_dict= {'cid':cid,'depot_id':depot_id,'depot_name':depot_name,'sl':sl,'client_id':client_id,'client_name':client_name,'rep_id':uid,'rep_name':rep_name,'order_date':order_date,'delivery_date':delivery_date,'area_id':route_id,'area_name':route_name,'item_id':itemId,'item_name':itemName,'category_id':categoryId,'price':itemPrice,'quantity':itemQty,'order_media':'WAP','status':'Submitted','ym_date':ym_date}
                            ins_list.append(ins_dict)  
                        
                        if len(ins_list) > 0:
                            try:
                                db.sm_order_head.insert(cid=cid,depot_id=depot_id,depot_name=depot_name,sl=sl,client_id=client_id,client_name=client_name,rep_id=uid,rep_name=rep_name,order_date=order_date,delivery_date=delivery_date,area_id=route_id,area_name=route_name,order_media='WAP',status='Submitted',ym_date=ym_date)
                                db.sm_order.bulk_insert(ins_list)
                            except:
                                retMsg='failed<rdrd>Failed to process data'
                                return retMsg
                            
                            retMsg='success<rdrd>'+str(sl)
                            return retMsg
                        else:
                            retMsg='failed<rdrd>Item not available'
                            return retMsg
                            
def deliverySubmit():
    cid=str(urllib2.unquote(request.vars.cid))
    uid=str(urllib2.unquote(request.vars.uid))
    depot_id=str(urllib2.unquote(request.vars.depot_id))
    submit_string=str(urllib2.unquote(request.vars.submit_string))
    
    itemStr=''
    comp_check_row=db((db.sm_company_settings.cid==cid) & (db.sm_company_settings.status=='ACTIVE')).select(db.sm_company_settings.status,limitby=(0,1))
    if not comp_check_row:
        retMsg='failed<rdrd>Invalid CID'
        return retMsg
    else:
        sup_check_row=db((db.sm_rep.cid==cid) & (db.sm_rep.rep_id==uid) & (db.sm_rep.user_type=='sup')  & (db.sm_rep.status=='ACTIVE')).select(db.sm_rep.name,db.sm_rep.level_id,db.sm_rep.field1,db.sm_rep.field2,db.sm_rep.note,limitby=(0,1))
        if not sup_check_row:
            retMsg='failed<rdrd>Invalid Authorization'
            return retMsg
        else:
            rep_name=str(sup_check_row[0].name).strip()
            level_id=str(sup_check_row[0].level_id).strip()
            levelDepth=str(sup_check_row[0].field2).strip()     #level Depth
            
            colName='level'+str(levelDepth)
            
            sup_areaDepotRows=db((db.sm_level.cid==cid) & (db.sm_level.is_leaf=='1')& (db.sm_level[colName]==level_id)&(db.sm_level.depot_id==depot_id)).select(db.sm_level.level_id,db.sm_level.level_name,orderby=db.sm_level.level_id,limitby=(0,1))       
            if not sup_areaDepotRows:
                retMsg='failed<rdrd>Depot Route not available'
                return retMsg
            else:
                route_id=str(sup_areaDepotRows[0].level_id).strip()
                route_name=str(sup_areaDepotRows[0].level_name).strip()
                
                depot_name_check=db((db.sm_depot.cid==cid) & (db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1)) 
                if not depot_name_check:
                    retMsg='failed<rdrd>Invalid Depot.Please Check Your Valid Depot'
                    return retMsg
                else:
                    depot_name=depot_name_check[0].name 
                    
                    row_client=db((db.sm_client.cid==cid)& (db.sm_client.depot_id==depot_id) & (db.sm_client.area_id==route_id) & (db.sm_client.status=='ACTIVE') ).select(db.sm_client.client_id,db.sm_client.name,limitby=(0,1))
                    if not row_client:
                        retMsg='failed<rdrd>Invalid Client.Please Check Your Valid Client'
                        return retMsg
                    else:
                        client_name=row_client[0].name
                        client_id=row_client[0].client_id
                        
                        order_datetime=date_fixed
                        delivery_date=date_fixed
                        ym_date=str(delivery_date)[0:7]+'-01'
                        
                        #----------------------Process product list
                        rec_duplicate_check=db((db.sm_settings.cid==cid) & (db.sm_settings.s_key=="D_DUPLICATE_CHECK")& (db.sm_settings.s_value=="YES")).select(db.sm_settings.s_value,limitby=(0,1))
                        if rec_duplicate_check:
                            result=duplicate_return(cid,depot_id,uid,route_id,client_id,delivery_date)
                            if (result=="Success"):
                                pass
                            else:
                                retMsg='failed<rdrd>Failed to process Auto-return'
                                return retMsg
                        
                        #=============
                        #Get sl from sm_depot
                        sl=1
                        query_sl=db((db.sm_depot.cid==cid) & (db.sm_depot.depot_id==depot_id)).select(db.sm_depot.id,db.sm_depot.del_sl,limitby=(0,1))
                        if query_sl:
                            sl=int(query_sl[0].del_sl)+1
                        query_sl[0].update_record(del_sl=sl)
                        #-----------
                        
                        ins_list=[]
                        ins_dict={}
                        
                        totalAmount=0
                        
                        itemList=submit_string.split('<rd>')        
                        for i in range(len(itemList)):
                            itemDetList=str(itemList[i]).split('<fd>');
                            itemId = itemDetList[0];
                            itemName = itemDetList[1];
                            categoryId = itemDetList[2];
                            itemPrice = itemDetList[3];
                            itemPriceDist = itemDetList[4];
                            itemQty = itemDetList[5];
                            
                            temp_amount=float(itemPrice)*int(itemQty)                                        
                            totalAmount=totalAmount+temp_amount
                            
                            ins_dict={'cid':cid,'depot_id':depot_id,'depot_name':depot_name,'sl':sl,'client_id':client_id,'client_name':client_name,'rep_id':uid,'rep_name':rep_name,'order_datetime':order_datetime,'delivery_date':delivery_date,'area_id':route_id,'area_name':route_name,'item_id':itemId,'item_name':itemName,'category_id':categoryId,'price':itemPrice,'quantity':itemQty,'invoice_media':'WAP','status':'Invoiced','ym_date':ym_date}
                            ins_list.append(ins_dict)  
                            
                        if len(ins_list) > 0:
                            try:
                                db.sm_invoice_head.insert(cid=cid,depot_id=depot_id,depot_name=depot_name,sl=sl,client_id=client_id,client_name=client_name,rep_id=uid,rep_name=rep_name,order_datetime=order_datetime,delivery_date=delivery_date,area_id=route_id,area_name=route_name,invoice_media='WAP',status='Invoiced',ym_date=ym_date)
                                db.sm_invoice.bulk_insert(ins_list)
                            except:
                                retMsg='failed<rdrd>Failed to process data'
                                return retMsg
                            
                            #-----------
                            #Update client depot balance
                            data_for_balance_update=str(cid)+'<fdfd>DELIVERY<fdfd>'+str(sl)+'<fdfd>'+str(datetime_fixed)+'<fdfd>'+str(depot_id)+'-'+str(sl)+'<fdfd>DPT-'+str(depot_id)+'<fdfd>CLT-'+str(client_id)+'<fdfd>'+str(totalAmount)
                            resStr=set_balance_transaction(data_for_balance_update)
                            
                            resStrList=resStr.split('<sep>')
                            flag=resStrList[0]
                            msg=resStrList[1]
                            
                            returnStr=''
                            if flag=='True':
                                retMsg='success<rdrd>'+str(sl)
                                return retMsg
                            else:
                                db.rollback()
                                retMsg='failed<rdrd>Failed to process balance'
                                return retMsg                            
                            #------------                            
                            
                        else:
                            retMsg='failed<rdrd>Item not available'
                            return retMsg


def duplicate_return(cid,depot_id,rep_id,route_id,client_id,delivery_date):
    req_depot_id=depot_id    
    client_id=client_id
    return_date=delivery_date
    ym_date=str(return_date)[0:7]+'-01'
    
    #Get records from invoice
    #Insert head in loop
    #Create list for bulk insert
   
    #------------------- requisition items
    invoice_sl=0
    reqhead=db((db.sm_invoice_head.cid==cid) & (db.sm_invoice_head.depot_id==req_depot_id) &(db.sm_invoice_head.rep_id==rep_id) &(db.sm_invoice_head.client_id==client_id) &(db.sm_invoice_head.delivery_date==delivery_date) &(db.sm_invoice_head.status=='Invoiced')).select(db.sm_invoice_head.sl,orderby=~db.sm_invoice_head.sl, limitby=(0,1))
    if reqhead:
        invoice_sl=reqhead[0].sl
    
    reqRecords=db((db.sm_invoice.cid==cid) & (db.sm_invoice.depot_id==req_depot_id) &(db.sm_invoice.sl==invoice_sl)&(db.sm_invoice.status=='Invoiced')).select(db.sm_invoice.ALL,orderby=db.sm_invoice.item_name)
    if not reqRecords:
        return "Success"
    else:  
        maxSl=1
        records=db((db.sm_depot.cid==cid) & (db.sm_depot.depot_id==req_depot_id)).select(db.sm_depot.id,db.sm_depot.return_sl,limitby=(0,1))
        if records:
            maxSl=int(records[0].return_sl)+1
        # sl update in depot
        records[0].update_record(return_sl=maxSl)
        
        reqDict={}
        insList=[]
        invoice_sl=0
        headFlag=False
        totalAmount=0
        discount=0
        for row in reqRecords:
            depot_id=row.depot_id
            invoice_sl=row.sl
            order_sl=row.order_sl
            client_id=row.client_id
            rep_id=row.rep_id        
            req_note=row.note
            area_id=row.area_id 
            discount=row.discount
            
            item_id=row.item_id
            item_name=row.item_name
            category_id=row.category_id
            item_qty_value=row.quantity
            bonus_qty=row.bonus_qty
            price=row.price
            
            totalAmount+=price*item_qty_value 
            
            reqDict={'cid':cid,'depot_id':depot_id,'sl':maxSl,'order_sl':order_sl,'invoice_sl':invoice_sl,'client_id':client_id,'rep_id':rep_id,'area_id':area_id,'return_date':return_date,'discount':discount,'note':req_note,
                           'item_id':item_id,'item_name':item_name,'category_id':category_id,'quantity':item_qty_value,'bonus_qty':bonus_qty,'price':price,'ym_date':ym_date}
            insList.append(reqDict)
            if headFlag==False:
                db.sm_return_head.insert(cid=cid,depot_id=depot_id,sl=maxSl,order_sl=order_sl,invoice_sl=invoice_sl,client_id=client_id,rep_id=rep_id,area_id=area_id,return_date=return_date,discount=discount,note=req_note,ym_date=ym_date)
                headFlag=True
        totalAmount=totalAmount-discount
                            
        rows=db.sm_return.bulk_insert(insList)
        #update in invoice
        
        db((db.sm_invoice.cid==cid) & (db.sm_invoice.depot_id==req_depot_id) & (db.sm_invoice.client_id==client_id)&(db.sm_invoice.sl==invoice_sl)).update(note='Returned')
        db((db.sm_invoice_head.cid==cid) & (db.sm_invoice_head.depot_id==req_depot_id) & (db.sm_invoice_head.client_id==client_id)&(db.sm_invoice_head.sl==invoice_sl)).update(note='Returned')
        
        #    Create string for client_balance_for_del_return to maintain client balance 
        
        strData=str(cid)+'<fdfd>RETURN<fdfd>'+str(maxSl)+'<fdfd>'+str(datetime_fixed)+'<fdfd>'+str(depot_id)+'-'+str(maxSl)+'<fdfd>CLT-'+str(client_id)+'<fdfd>DPT-'+str(depot_id)+'<fdfd>'+str(totalAmount)
        resStr=set_balance_transaction(strData)
        
        resStrList=resStr.split('<sep>')
        flag=resStrList[0]
        msg=resStrList[1]
        if flag=='True':
            db((db.sm_return.cid==cid)& (db.sm_return.depot_id==depot_id) & (db.sm_return.sl==maxSl)).update(status='Returned')
            db((db.sm_return_head.cid==cid)& (db.sm_return_head.depot_id==depot_id) & (db.sm_return_head.sl==maxSl)).update(status='Returned')
            return "Success"
        else:
            db.rollback()
            return "Failed"


               
