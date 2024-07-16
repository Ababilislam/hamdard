#================= ORDER TO DELIVERY USING PROCESSING RULES (order status have 'Draft,Submitted,Invoiced,Cancelled'; allowed:'Submitted')

#http://127.0.0.1:8000/mrepskf/auto_delivery_with_tp_rules/auto_delivery_start

#======================= auto delivery WITH Cron Function

def auto_delivery_start():
    ret=''
    autDelCronRows=db((db.sm_settings.cid=='SYS')&(db.sm_settings.s_key=='AUTO_DEL_CRON_FLAG')).select(db.sm_settings.id,db.sm_settings.s_value,limitby=(0,1))
    if autDelCronRows:
        cronFlag=autDelCronRows[0].s_value
        if str(cronFlag)=='0':
            autDelCronRows[0].update_record(s_value='1')
            
            settCompRows=db((db.sm_settings.s_key=='AUTO_DELIVERY')&(db.sm_settings.s_value=='YES')).select(db.sm_settings.cid)
            if settCompRows:
                #----------- order head record range
                maxRecord=20
                limitby=(0,maxRecord)
                
                for row in settCompRows:
                    c_id=str(row.cid).strip().upper()
                    
                    #Order Head Loop
                    orderHeadRecords=db((db.sm_order_head.cid==c_id)&(db.sm_order_head.status=='Submitted')&(db.sm_order_head.flag_data=='0')&(db.sm_order_head.field1=='ORDER')).select(db.sm_order_head.id,db.sm_order_head.depot_id,db.sm_order_head.sl,db.sm_order_head.client_id,db.sm_order_head.order_date,limitby=limitby)
                    for ordHeadRow in orderHeadRecords:
                        depot_id=ordHeadRow.depot_id
                        order_sl=ordHeadRow.sl
                        clientId=ordHeadRow.client_id
                        orderDate=ordHeadRow.order_date
                        
                        
                        orderRow=db((db.sm_order.cid==c_id) & (db.sm_order.depot_id==depot_id) & (db.sm_order.client_id==clientId)&(db.sm_order.sl==order_sl)).select(db.sm_order.sl,limitby=(0,1))
                        if not orderRow:
                            ordHeadRow.update_record(status='Invoiced',flag_data='1')
                            
                        else:
                            #----- call function to create invoice with Invoiced Status from order
                            #ret=get_order_to_delivery(c_id,depot_id,order_sl,clientId,orderDate)
                            
                            #----- call function to create invoice with Submitted Status from order
                            ret=get_order_to_delivery_submit(c_id,depot_id,order_sl,clientId,orderDate)
                            
                            
                    orderHeadRecords=''
                
                #-------------- end settings
                settCompRows=''
                
            autDelCronRows[0].update_record(s_value='0')
            db.commit()
            #return ret
        
    return 'Done'     

    