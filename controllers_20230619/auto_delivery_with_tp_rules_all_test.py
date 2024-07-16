#================= ORDER TO DELIVERY USING PROCESSING RULES (order status have 'Draft,Submitted,Invoiced,Cancelled'; allowed:'Submitted')

#http://127.0.0.1:8000/skf/auto_delivery_with_tp_rules_all/test
def test():    
    return 15%5
    
#http://127.0.0.1:8000/skf/auto_delivery_with_tp_rules_all/auto_delivery_start?depotid=170
#http://c003.cloudapp.net/skf/auto_delivery_with_tp_rules_all/auto_delivery_start?depotid=170

#======================= auto delivery WITH Cron Function
def auto_delivery_start():
    ret=''
    
    depotID=request.vars.depotid
    if depotID=='' or depotID==None:
        orderHeadRecords = db((db.sm_order_head.status == 'Submitted') & (db.sm_order_head.flag_data == '0') & (db.sm_order_head.field1 == 'ORDER') & ((db.sm_order_head.delivery_date <= current_date) | (db.sm_order_head.field2 == 1))).select(db.sm_order_head.depot_id,orderby=db.sm_order_head.id,limitby=(0,1))
        if not orderHeadRecords:
            return 'Data Not found'
        else:
            depot_id = orderHeadRecords[0].depot_id
            depotID=depot_id


    autDelCronRows=db((db.sm_depot.depot_id==depotID)&(db.sm_depot.auto_del_cron_flag==0)).select(db.sm_depot.id,db.sm_depot.cid,limitby=(0,1))
    # return autDelCronRows
    if autDelCronRows:
        c_id=str(autDelCronRows[0].cid)
        
        autDelCronRows[0].update_record(auto_del_cron_flag=1)
        
        settCompRows=db((db.sm_settings.cid==c_id)&(db.sm_settings.s_key=='AUTO_DELIVERY')&(db.sm_settings.s_value=='YES')).select(db.sm_settings.cid,limitby=(0,1))
        # return settCompRows
        if settCompRows:
            #----------- order head record range
            maxRecord=5
            limitby=(0,maxRecord)
            
            #Order Head Loop
            orderHeadRecords=db((db.sm_order_head.cid==c_id)&(db.sm_order_head.depot_id==depotID)&(db.sm_order_head.status=='Submitted')&(db.sm_order_head.flag_data=='0')&(db.sm_order_head.field1=='ORDER')&((db.sm_order_head.delivery_date<=current_date)|(db.sm_order_head.field2==1))).select(db.sm_order_head.ALL,orderby=db.sm_order_head.id,limitby=limitby)
            return db._lastsql
            for ordHRow in orderHeadRecords:
                depot_id=ordHRow.depot_id
                depot_name=ordHRow.depot_name
                store_id=ordHRow.store_id
                store_name=ordHRow.store_name
                order_sl=ordHRow.sl
                client_id=ordHRow.client_id                
                client_name=ordHRow.client_name
                rep_id=ordHRow.rep_id
                rep_name=ordHRow.rep_name
                order_date=ordHRow.order_date
                order_datetime=ordHRow.order_datetime
                delivery_date=ordHRow.delivery_date
                payment_mode=ordHRow.payment_mode
                area_id=ordHRow.area_id
                area_name=ordHRow.area_name
                order_media=ordHRow.order_media
                ym_date=ordHRow.ym_date
                client_cat=ordHRow.client_cat
                note=ordHRow.note
                market_id=ordHRow.market_id
                market_name=ordHRow.market_name
                
                orderRows=db((db.sm_order.cid==c_id) & (db.sm_order.depot_id==depot_id)&(db.sm_order.sl==order_sl)).select(db.sm_order.ALL,orderby=db.sm_order.item_id)
                if not orderRows:
                    ordHRow.update_record(status='Invoiced',flag_data='1',field2=1)
                else:
                    detailList=[]
                    for ordRow in orderRows:
                        item_id=str(ordRow.item_id).strip().upper()
                        item_name=ordRow.item_name
                        category_id=ordRow.category_id
                        quantity=ordRow.quantity
                        price=ordRow.price
                        item_vat=ordRow.item_vat
                        item_unit=ordRow.item_unit
                        item_carton=ordRow.item_carton
                        
                        detailDict={'cid':c_id,'depot_id':depot_id,'depot_name':depot_name,'sl':order_sl,'store_id':store_id,'store_name':store_name,'client_id':client_id,'client_name':client_name,'rep_id':rep_id,'rep_name':rep_name,'market_id':market_id,'market_name':market_name,'order_date':order_date,'order_datetime':order_datetime,'delivery_date':delivery_date,
                                    'payment_mode':payment_mode,'area_id':area_id,'area_name':area_name,'order_media':order_media,'ym_date':ym_date,'client_cat':client_cat,'note':note,'item_id':item_id,'item_name':item_name,'category_id':category_id,'quantity':quantity,'price':price,'item_vat':item_vat,'item_unit':item_unit,'item_carton':item_carton}
                        detailList.append(detailDict)
                        
                    #delete temp
                    db((db.sm_tp_rules_temp_process.cid==c_id) & (db.sm_tp_rules_temp_process.depot_id==depot_id)).delete()
                    
                    #insert temp
                    db.sm_tp_rules_temp_process.bulk_insert(detailList)
                    
                    #----- call function to create invoice with tp rules
                    ret=get_order_to_delivery_detail_rules(c_id,depot_id,order_sl,client_id,order_date)
                    
            orderHeadRecords=''
            
            #-------------- end settings
            settCompRows=''
            
        autDelCronRows[0].update_record(auto_del_cron_flag=0)
        db.commit()
        #return ret
        
    return 'Done'     

    