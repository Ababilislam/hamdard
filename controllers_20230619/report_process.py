
#http://127.0.0.1:8000/skf/report_process/set_invoice_wise_outstanding_as_of_date?cid=SKF&depotid=170

def set_invoice_wise_outstanding_as_of_date():    
    c_id=str(request.vars.cid).strip()
    depotID=str(request.vars.depotid).strip()
    toDate=current_date
    
    try:
        endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d').strftime('%Y-%m-%d')
    except:
        endDt=''
    
    if c_id=='' or c_id=='None' or depotID=='' or depotID=='None' or endDt=='' or endDt==None:
        return 'Required CID,DepotID and As of Date'   
        
    depot_name=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depotID)).select(db.sm_depot.name,limitby=(0,1))
    if not depotRow:
        return 'Invalid Depot'
    else:
        depot_name=depotRow[0].name
    
    
    existDelete=db((db.sm_report_as_of_date.cid==c_id)&(db.sm_report_as_of_date.depot_id==depotID)&(db.sm_report_as_of_date.report_date==endDt)).delete()
    
    #------------- Invoice
    
    condStr=" (sm_invoice_head.cid = '"+c_id+"') AND (sm_invoice_head.depot_id='"+depotID+"') AND (sm_invoice_head.invoice_date <= '"+str(endDt)+"') AND (sm_invoice_head.status='Invoiced') AND (round(sm_invoice_head.total_amount-(sm_invoice_head.return_tp+sm_invoice_head.return_vat-sm_invoice_head.return_discount)-sm_invoice_head.collection_amount,2)!=0)"
    
    selectRecords="SELECT cid,depot_id,depot_name,sl,store_id,store_name,'"+str(endDt)+"' as report_date,'"+str(datetime_fixed)+"' as process_date,invoice_date,order_sl,order_datetime,delivery_date,payment_mode,credit_note,client_id,client_name,cl_category_id,cl_category_name,cl_sub_category_id,cl_sub_category_name,client_limit_amt,rep_id,rep_name,market_id,market_name,d_man_id,d_man_name,level0_id,level0_name,level1_id,level1_name,level2_id,level2_name,area_id,area_name,shipment_no,actual_total_tp,vat_total_amount,discount,sp_discount,total_amount,ret_actual_total_tp,return_tp,return_vat,return_discount,return_sp_discount,collection_amount,adjust_amount,note FROM sm_invoice_head WHERE ("+str(condStr)+") ORDER BY id"
    
    insertSql="Insert into sm_report_as_of_date(cid,depot_id,depot_name,sl,store_id,store_name,report_date,process_date,invoice_date,order_sl,order_datetime,delivery_date,payment_mode,credit_note,client_id,client_name,cl_category_id,cl_category_name,cl_sub_category_id,cl_sub_category_name,client_limit_amt,rep_id,rep_name,market_id,market_name,d_man_id,d_man_name,level0_id,level0_name,level1_id,level1_name,level2_id,level2_name,area_id,area_name,shipment_no,actual_total_tp,vat_total_amount,discount,sp_discount,total_amount,ret_actual_total_tp,return_tp,return_vat,return_discount,return_sp_discount,collection_amount,adjust_amount,note) "+selectRecords
    
    db.executesql(insertSql)
    
    return 'Completed'