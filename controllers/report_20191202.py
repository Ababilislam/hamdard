import math
import os
import calendar
import urllib2

def sub_months(sourcedate, months):    
    month = sourcedate.month - 1 - months
    year = sourcedate.year + month / 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year, month)[1])
    return datetime.date(year, month, day)
    
#======================= Report Home
def reports_home():
    if (session.cid=='' or session.cid==None):
        redirect (URL('default','home'))
    if int(session.setting_repot)!=1:
        session.flash='Access is Denied !'
        redirect (URL('default','home'))
        
    response.title='Reports'
    #------------
    
    btn_ledger_report=request.vars.btn_ledger_report
    btn_stock_report=request.vars.btn_stock_report
    btn_show_subdepot=request.vars.btn_show_subdepot
    
    #---------------------
    if btn_ledger_report:
        redirect(URL(c='utility',f='reports_home'))                
    elif btn_stock_report:
        redirect(URL(c='report_menu',f='report_home'))  
    elif btn_show_subdepot:
        redirect(URL(c='depot',f='sub_depot_list')) 
    else:
        return dict()
    #--------------
    
def home():
    task_id='rm_analysis_view'
    access_permission=check_role(task_id)
    if (access_permission==False ):
        session.flash='Access is Denied'
        redirect (URL('default','home'))
        
    response.title='Report'
    
    c_id=session.cid
    
    search_form =SQLFORM(db.sm_search_date)
    
    #-----
    btn_stock_status_batch=request.vars.btn_stock_status_batch
    btn_stock_status_without_batch=request.vars.btn_stock_status_without_batch
    
    #Stock movement
    btn_in_transit=request.vars.btn_in_transit
    
    btn_issue=request.vars.btn_issue
    btn_issue_item_wise=request.vars.btn_issue_item_wise
    
    btn_adj_sum_and_details=request.vars.btn_adj_sum_and_details
    btn_adj_sum=request.vars.btn_adj_sum
    btn_adj_details=request.vars.btn_adj_details
    btn_adj_summery_itemwise=request.vars.btn_adj_summery_itemwise
    btn_adjustment_preview=request.vars.btn_adjustment_preview
    
    btn_receipt_summery=request.vars.btn_receipt_summery
    btn_receipt_details=request.vars.btn_receipt_details
    btn_receipt_summery_itemwise=request.vars.btn_receipt_summery_itemwise
    btn_receipt_summery_and_details=request.vars.btn_receipt_summery_and_details
    btn_gr_note_preview=request.vars.btn_gr_note_preview
    
    btn_transfer_summery=request.vars.btn_transfer_summery
    btn_transfer_summery_and_details=request.vars.btn_transfer_summery_and_details
    btn_transfer_summery_item_wise=request.vars.btn_transfer_summery_item_wise
    btn_transfer_details=request.vars.btn_transfer_details
    
    btn_gr_transfer_b2b_preview=request.vars.btn_gr_transfer_b2b_preview
    btn_gr_transfer_internal_preview=request.vars.btn_gr_transfer_internal_preview
    
    btn_transit_dispute=request.vars.btn_transit_dispute
    btn_transit_dispute_item_wise=request.vars.btn_transit_dispute_item_wise
    
    #outstanding
    btn_invoice_wise=request.vars.btn_invoice_wise
    btn_customer_wise=request.vars.btn_customer_wise
    btn_customer_wise_details=request.vars.btn_customer_wise_details    
    btn_customer_wise_details_print=request.vars.btn_customer_wise_details_print  
    btn_customer_wise_details_print2=request.vars.btn_customer_wise_details_print2
    btn_delivery_man_wise=request.vars.btn_delivery_man_wise    
    btn_delivery_man_details=request.vars.btn_delivery_man_details
    btn_delivery_man_details_print=request.vars.btn_delivery_man_details_print
    btn_territory_wise=request.vars.btn_territory_wise    
    btn_territory_details=request.vars.btn_territory_details
    btn_negative_balance=request.vars.btn_negative_balance
    btn_rsm_fm_mso_wise=request.vars.btn_rsm_fm_mso_wise
    btn_rsm_fm_mso_wise_summary=request.vars.btn_rsm_fm_mso_wise_summary
    
    btn_customer_wise_details2=request.vars.btn_customer_wise_details2
    btn_customer_wise_details3=request.vars.btn_customer_wise_details3  #A/R Outstanding
    
    btn_invoice_wise_before_ret=request.vars.btn_invoice_wise_before_ret
    btn_invoice_wise_AsOfDate=request.vars.btn_invoice_wise_AsOfDate
    
    
    btn_ost_summary_asOfDate_tr=request.vars.btn_ost_summary_asOfDate_tr
    btn_sales_AsOfDate=request.vars.btn_sales_AsOfDate
    btn_received_AsOfDate=request.vars.btn_received_AsOfDate
    btn_invoice_wise_AsOfDate_tr=request.vars.btn_invoice_wise_AsOfDate_tr
    
    
    
    
    
    #collection and ledger
    btn_collection_invoice_wise=request.vars.btn_collection_invoice_wise
    btn_collection_customer_wise=request.vars.btn_collection_customer_wise
    btn_collection_transaction_wise=request.vars.btn_collection_transaction_wise
    btn_ledger_wise=request.vars.btn_ledger_wise
    
    btn_money_receipt=request.vars.btn_money_receipt
    btn_money_receipt_2=request.vars.btn_money_receipt_2
    btn_money_receipt_adjustment=request.vars.btn_money_receipt_adjustment
    
    btn_inv_and_receipt=request.vars.btn_inv_and_receipt
    btn_inv_details=request.vars.btn_inv_details
    
#    ============= STP Generator===========
    btn_stp_generator=request.vars.btn_stp_generator
    btn_stp_item_wise_sales_distribution=request.vars.btn_stp_item_wise_sales_distribution
    #--------
    
    if (btn_stock_status_batch or btn_stock_status_without_batch):        
        depot=str(request.vars.depot_id)
        store=str(request.vars.store_id)
        
        if depot=='':
            response.flash='Required Branch'
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
                
            user_depot_address=''
            if session.user_type!='Depot':            
                depotRows = db((db.sm_depot.cid == session.cid) & (db.sm_depot.depot_id == depot_id)).select(db.sm_depot.name,db.sm_depot.depot_category,db.sm_depot.field1, limitby=(0, 1))
                if depotRows:
                    user_depot_address=depotRows[0].field1
                                 
                    session.user_depot_address=user_depot_address
            
            if btn_stock_status_batch:
                if store_id!='':
                    redirect (URL('stockStatusWithBatch',vars=dict(depotID=depot_id,storeID=store_id)))
                else:
                    redirect (URL('stockStatusWithBatchall',vars=dict(depotID=depot_id,storeID=store_id)))
                    
            elif btn_stock_status_without_batch:
                if store_id!='':
                    redirect (URL('stockStatusWithoutBatch',vars=dict(depotID=depot_id,storeID=store_id))) 
                else:
                    redirect (URL('stockStatusWithoutBatchStoreall',vars=dict(depotID=depot_id))) 
                
    elif (btn_transfer_details or btn_transfer_summery_item_wise or btn_transfer_summery or btn_transfer_summery_and_details or btn_adj_sum or btn_adj_details or btn_adj_summery_itemwise or btn_receipt_details or btn_receipt_summery or btn_gr_note_preview or btn_receipt_summery_itemwise or btn_receipt_summery_and_details or btn_adj_sum_and_details or btn_transit_dispute_item_wise or btn_transit_dispute or btn_issue_item_wise or btn_issue or btn_gr_transfer_b2b_preview or btn_gr_transfer_internal_preview or btn_adjustment_preview):
        from_dt=request.vars.from_dt
        to_dt=request.vars.to_dt
        depot=str(request.vars.pri_depot_id)
        store=str(request.vars.pri_store_id)
        pri_depot_id_from=str(request.vars.pri_depot_id_from)
        pri_adjustment_cause=str(request.vars.pri_adjustment_cause)        
        pri_depot_id_to=str(request.vars.pri_depot_id_to)
        
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
            if dateDiff>90:
                response.flash="Maximum 90 days allowed between Date Range"
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
                    
                    if len(pri_depot_id_from.split('|'))>1: 
                        from_depot_id=pri_depot_id_from.split('|')[0]
                        from_depot_name=pri_depot_id_from.split('|')[1]
                    else:
                        from_depot_id=pri_depot_id_from
                        from_depot_name=''
                        
                    if len(pri_depot_id_to.split('|'))>1: 
                        to_depot_id=pri_depot_id_to.split('|')[0]
                        to_depot_name=pri_depot_id_to.split('|')[1]
                    else:
                        to_depot_id=pri_depot_id_to
                        to_depot_name=''
                        
                    
                    user_depot_address=''
                    if session.user_type!='Depot':            
                        depotRows = db((db.sm_depot.cid == c_id) & (db.sm_depot.depot_id == depot_id)).select(db.sm_depot.name,db.sm_depot.depot_category,db.sm_depot.field1, limitby=(0, 1))
                        if depotRows:
                            user_depot_address=depotRows[0].field1                            
                            session.user_depot_address=user_depot_address
                    
                    #-------------------
                    if btn_adj_sum_and_details:
                        redirect (URL('adjustmentSumDetails',vars=dict(fromDate=from_dt,toDate=to_dt,depotID=depot_id,storeID=store_id))) 
                    elif btn_adj_sum:
                        redirect (URL('adjustmentSummery',vars=dict(fromDate=from_dt,toDate=to_dt,depotID=depot_id,storeID=store_id,adjustment_cause=pri_adjustment_cause))) 
                    elif btn_adj_details:
                        redirect (URL('adjustmentDetails',vars=dict(fromDate=from_dt,toDate=to_dt,depotID=depot_id,storeID=store_id))) 
                    elif btn_adj_summery_itemwise:
                        redirect (URL('adjustmentSummeryItemWise',vars=dict(fromDate=from_dt,toDate=to_dt,depotID=depot_id,storeID=store_id))) 
                    
                    
                    elif btn_receipt_summery:
                        redirect (URL('receiptSummery',vars=dict(fromDate=from_dt,toDate=to_dt,depotID=depot_id,storeID=store_id,fromDepotID=from_depot_id))) 
                    elif btn_receipt_details:
                        redirect (URL('receiptDetails',vars=dict(fromDate=from_dt,toDate=to_dt,depotID=depot_id,storeID=store_id,fromDepotID=from_depot_id))) 
                    elif btn_receipt_summery_itemwise:
                        redirect (URL('receiveSummeryItemWise',vars=dict(fromDate=from_dt,toDate=to_dt,depotID=depot_id,storeID=store_id,fromDepotID=from_depot_id))) 
                    elif btn_receipt_summery_and_details:
                        redirect (URL('receiptSumDetails',vars=dict(fromDate=from_dt,toDate=to_dt,depotID=depot_id,storeID=store_id,fromDepotID=from_depot_id))) 
                    elif btn_gr_note_preview:
                        redirect (URL('grNotePreview',vars=dict(fromDate=from_dt,toDate=to_dt,depotID=depot_id,storeID=store_id,fromDepotID=from_depot_id))) 
                        
                        
                    elif btn_transfer_summery:
                        redirect (URL('transferSummery',vars=dict(fromDate=from_dt,toDate=to_dt,depotID=depot_id,storeID=store_id,to_depot_id=to_depot_id))) 
                    elif btn_transfer_summery_item_wise:
                        redirect (URL('transferSummeryItemWise',vars=dict(fromDate=from_dt,toDate=to_dt,depotID=depot_id,storeID=store_id,to_depot_id=to_depot_id))) 
                    elif btn_transfer_details:
                        redirect (URL('transferDetails',vars=dict(fromDate=from_dt,toDate=to_dt,depotID=depot_id,storeID=store_id,to_depot_id=to_depot_id))) 
                    elif btn_transfer_summery_and_details:
                        redirect (URL('transferSumDetails',vars=dict(fromDate=from_dt,toDate=to_dt,depotID=depot_id,storeID=store_id,to_depot_id=to_depot_id))) 
                    
                    elif btn_gr_transfer_b2b_preview:
                        redirect (URL('transferBranchToBranchPreview',vars=dict(fromDate=from_dt,toDate=to_dt,depotID=depot_id,storeID=store_id))) 
                    elif btn_gr_transfer_internal_preview:
                        redirect (URL('transferInternalPreview',vars=dict(fromDate=from_dt,toDate=to_dt,depotID=depot_id,storeID=store_id))) 
                    elif btn_adjustment_preview:
                        redirect (URL('adjustmentPreview',vars=dict(fromDate=from_dt,toDate=to_dt,depotID=depot_id,storeID=store_id))) 
                        
                    elif btn_issue:
                        redirect (URL('issueList',vars=dict(fromDate=from_dt,toDate=to_dt,depotID=depot_id,depotName=depot_name,storeID=store_id,storeName=store_name))) 
                    elif btn_issue_item_wise:
                        redirect (URL('issueItemWise',vars=dict(fromDate=from_dt,toDate=to_dt,depotID=depot_id,depotName=depot_name,storeID=store_id,storeName=store_name))) 
                        
                    elif btn_transit_dispute:
                        redirect (URL('tansitDisputeList',vars=dict(fromDate=from_dt,toDate=to_dt,depotID=depot_id,depotName=depot_name,storeID=store_id,storeName=store_name))) 
                    elif btn_transit_dispute_item_wise:
                        redirect (URL('tansitDisputeItemWise',vars=dict(fromDate=from_dt,toDate=to_dt,depotID=depot_id,depotName=depot_name,storeID=store_id,storeName=store_name))) 
                    
                    
                    
    elif (btn_rsm_fm_mso_wise or btn_negative_balance or btn_territory_details or btn_territory_wise or btn_delivery_man_details or btn_delivery_man_details_print or btn_delivery_man_wise or btn_customer_wise or btn_customer_wise_details2 or btn_customer_wise_details3 or btn_customer_wise_details or btn_customer_wise_details_print or btn_customer_wise_details_print2 or btn_invoice_wise or btn_invoice_wise_before_ret or btn_rsm_fm_mso_wise_summary or btn_invoice_wise_AsOfDate or btn_invoice_wise_AsOfDate_tr or btn_ost_summary_asOfDate_tr or btn_received_AsOfDate or btn_sales_AsOfDate):
        from_dt=request.vars.from_dt_2
        to_dt=request.vars.to_dt_2
        
        depot=str(request.vars.out_st_depot_id)
        store=str(request.vars.out_st_store_id)
        
        out_st_delivery_man=str(request.vars.out_st_delivery_man)
        out_st_territory=str(request.vars.out_st_territory)
        out_st_rsm_fm=str(request.vars.out_st_rsm_fm)
        out_st_mso=str(request.vars.out_st_mso)
        customerIdName=request.vars.out_st_customer
        
        invoice_term=str(request.vars.invoice_term)
        credit_type=str(request.vars.credit_type)
        customer_cat=str(request.vars.customer_cat)
        customer_sub_cat=str(request.vars.customer_sub_cat)
        
        out_st_level1=str(request.vars.out_st_level1)
        out_st_level2=str(request.vars.out_st_level2)
        
        dateFlag=True
        try:
            from_dt2=datetime.datetime.strptime(str(from_dt),'%Y-%m-%d')            
        except:
            from_dt2=''
        
        try:
            to_dt2=datetime.datetime.strptime(str(to_dt),'%Y-%m-%d')            
            if from_dt2!='' and from_dt2>to_dt2:
                dateFlag=False
        except:
            dateFlag=False
            
        if dateFlag==False:
            response.flash="Invalid Date"
        else:
            if depot=='' or store=='':
                response.flash='Required Branch and Store'
            else:
                if len(depot.split('|'))>1: 
                    depot_id=depot.split('|')[0]                    
                else:
                    depot_id=depot
                                    
                if len(store.split('|'))>1:
                    store_id=store.split('|')[0]
                    store_name=store.split('|')[1]
                else:
                    store_id=store
                    store_name=''
                    
                user_depot_address=''
                if session.user_type!='Depot':            
                    depotRows = db((db.sm_depot.cid == c_id) & (db.sm_depot.depot_id == depot_id)).select(db.sm_depot.name,db.sm_depot.depot_category,db.sm_depot.field1, limitby=(0, 1))
                    if depotRows:
                        user_depot_address=depotRows[0].field1                                     
                        session.user_depot_address=user_depot_address
                    
                
                out_st_delivery_man_id=''                
                if out_st_delivery_man!='':
                    out_st_delivery_man_id=out_st_delivery_man.split('|')[0]
                    
                out_st_territory_id=''                
                if out_st_territory!='':
                    out_st_territory_id=out_st_territory.split('|')[0]
                                    
                out_st_mso_id=''                
                if out_st_mso!='':
                    out_st_mso_id=out_st_mso.split('|')[0]
                                  
                customerId=''
                if customerIdName!='':
                    customerId=str(customerIdName).split('|')[0]
                    
                out_st_level1_id=''                
                if out_st_level1!='':
                    out_st_level1_id=out_st_level1.split('|')[0]
                    
                out_st_level2_id=''                
                if out_st_level2!='':
                    out_st_level2_id=out_st_level2.split('|')[0]
                    
                if btn_invoice_wise:
                    redirect (URL('outStInvoiceWise',vars=dict(fromDate=from_dt,toDate=to_dt,depotID=depot_id,storeID=store_id,deliveryManID=out_st_delivery_man_id,territoryID=out_st_territory_id,msoID=out_st_mso_id,invoice_term=invoice_term,customerId=customerId,credit_type=credit_type,customer_cat=customer_cat,customer_sub_cat=customer_sub_cat,out_st_level1_id=out_st_level1_id,out_st_level2_id=out_st_level2_id)))
                elif btn_invoice_wise_before_ret:#Not used
                    redirect (URL('outStInvoiceWise1',vars=dict(fromDate=from_dt,toDate=to_dt,depotID=depot_id,storeID=store_id,deliveryManID=out_st_delivery_man_id,territoryID=out_st_territory_id,msoID=out_st_mso_id,invoice_term=invoice_term,customerId=customerId,credit_type=credit_type,customer_cat=customer_cat,customer_sub_cat=customer_sub_cat)))
                elif btn_customer_wise:
                    redirect (URL('outStCustomerWise',vars=dict(fromDate=from_dt,toDate=to_dt,depotID=depot_id,storeID=store_id,deliveryManID=out_st_delivery_man_id,territoryID=out_st_territory_id,msoID=out_st_mso_id,invoice_term=invoice_term,customerId=customerId,credit_type=credit_type,customer_cat=customer_cat,customer_sub_cat=customer_sub_cat,out_st_level1_id=out_st_level1_id,out_st_level2_id=out_st_level2_id))) 
                elif btn_customer_wise_details:
                    redirect (URL('outStCustomerWiseDetails',vars=dict(fromDate=from_dt,toDate=to_dt,depotID=depot_id,storeID=store_id,deliveryManID=out_st_delivery_man_id,territoryID=out_st_territory_id,msoID=out_st_mso_id,invoice_term=invoice_term,customerId=customerId,credit_type=credit_type,customer_cat=customer_cat,customer_sub_cat=customer_sub_cat,out_st_level1_id=out_st_level1_id,out_st_level2_id=out_st_level2_id)))
                elif btn_customer_wise_details_print:
                    redirect (URL('outStCustomerWiseDetails_print',vars=dict(fromDate=from_dt,toDate=to_dt,depotID=depot_id,storeID=store_id,deliveryManID=out_st_delivery_man_id,territoryID=out_st_territory_id,msoID=out_st_mso_id,invoice_term=invoice_term,customerId=customerId,credit_type=credit_type,customer_cat=customer_cat,customer_sub_cat=customer_sub_cat,out_st_level1_id=out_st_level1_id,out_st_level2_id=out_st_level2_id)))
                elif btn_customer_wise_details_print2:
                    redirect (URL('outStCustomerWiseDetails_print2',vars=dict(fromDate=from_dt,toDate=to_dt,depotID=depot_id,storeID=store_id,deliveryManID=out_st_delivery_man_id,territoryID=out_st_territory_id,msoID=out_st_mso_id,invoice_term=invoice_term,customerId=customerId,credit_type=credit_type,customer_cat=customer_cat,customer_sub_cat=customer_sub_cat,out_st_level1_id=out_st_level1_id,out_st_level2_id=out_st_level2_id)))
                
                elif btn_delivery_man_wise:
                    redirect (URL('outStDeliveryPersonWise',vars=dict(fromDate=from_dt,toDate=to_dt,depotID=depot_id,storeID=store_id,deliveryManID=out_st_delivery_man_id,territoryID=out_st_territory_id,msoID=out_st_mso_id,invoice_term=invoice_term,customerId=customerId,credit_type=credit_type,customer_cat=customer_cat,customer_sub_cat=customer_sub_cat,out_st_level1_id=out_st_level1_id,out_st_level2_id=out_st_level2_id))) 
                elif btn_delivery_man_details:
                    redirect (URL('outStDeliveryPersonWiseDetails',vars=dict(fromDate=from_dt,toDate=to_dt,depotID=depot_id,storeID=store_id,deliveryManID=out_st_delivery_man_id,territoryID=out_st_territory_id,msoID=out_st_mso_id,invoice_term=invoice_term,customerId=customerId,credit_type=credit_type,customer_cat=customer_cat,customer_sub_cat=customer_sub_cat,out_st_level1_id=out_st_level1_id,out_st_level2_id=out_st_level2_id))) 
                elif btn_delivery_man_details_print:
                    redirect (URL('outStDeliveryPersonWiseDetails_print',vars=dict(fromDate=from_dt,toDate=to_dt,depotID=depot_id,storeID=store_id,deliveryManID=out_st_delivery_man_id,territoryID=out_st_territory_id,msoID=out_st_mso_id,invoice_term=invoice_term,customerId=customerId,credit_type=credit_type,customer_cat=customer_cat,customer_sub_cat=customer_sub_cat,out_st_level1_id=out_st_level1_id,out_st_level2_id=out_st_level2_id))) 
                elif btn_territory_wise:
                    redirect (URL('outStTerritoryWise',vars=dict(fromDate=from_dt,toDate=to_dt,depotID=depot_id,storeID=store_id,deliveryManID=out_st_delivery_man_id,territoryID=out_st_territory_id,msoID=out_st_mso_id,invoice_term=invoice_term,customerId=customerId,credit_type=credit_type,customer_cat=customer_cat,customer_sub_cat=customer_sub_cat,out_st_level1_id=out_st_level1_id,out_st_level2_id=out_st_level2_id))) 
                elif btn_territory_details:
                    redirect (URL('outStTerritoryWiseDetails',vars=dict(fromDate=from_dt,toDate=to_dt,depotID=depot_id,storeID=store_id,deliveryManID=out_st_delivery_man_id,territoryID=out_st_territory_id,msoID=out_st_mso_id,invoice_term=invoice_term,customerId=customerId,credit_type=credit_type,customer_cat=customer_cat,customer_sub_cat=customer_sub_cat,out_st_level1_id=out_st_level1_id,out_st_level2_id=out_st_level2_id)))
                elif btn_negative_balance:
                    redirect (URL('negativeBanaceInvoiceWise',vars=dict(fromDate=from_dt,toDate=to_dt,depotID=depot_id,storeID=store_id,deliveryManID=out_st_delivery_man_id,territoryID=out_st_territory_id,msoID=out_st_mso_id,invoice_term=invoice_term,customerId=customerId,credit_type=credit_type,customer_cat=customer_cat,customer_sub_cat=customer_sub_cat,out_st_level1_id=out_st_level1_id,out_st_level2_id=out_st_level2_id)))
                elif btn_rsm_fm_mso_wise:
                    redirect (URL('outStRsmFmMsoWise',vars=dict(fromDate=from_dt,toDate=to_dt,depotID=depot_id,storeID=store_id,deliveryManID=out_st_delivery_man_id,territoryID=out_st_territory_id,msoID=out_st_mso_id,invoice_term=invoice_term,customerId=customerId,credit_type=credit_type,customer_cat=customer_cat,customer_sub_cat=customer_sub_cat,out_st_level1_id=out_st_level1_id,out_st_level2_id=out_st_level2_id)))
                elif btn_rsm_fm_mso_wise_summary:
                    redirect (URL('outStRsmFmMsoWiseSummary',vars=dict(fromDate=from_dt,toDate=to_dt,depotID=depot_id,storeID=store_id,deliveryManID=out_st_delivery_man_id,territoryID=out_st_territory_id,msoID=out_st_mso_id,invoice_term=invoice_term,customerId=customerId,credit_type=credit_type,customer_cat=customer_cat,customer_sub_cat=customer_sub_cat,out_st_level1_id=out_st_level1_id,out_st_level2_id=out_st_level2_id))) 
                elif btn_customer_wise_details2:
                    redirect (URL('outStCustomerWiseDetails2',vars=dict(fromDate=from_dt,toDate=to_dt,depotID=depot_id,storeID=store_id,deliveryManID=out_st_delivery_man_id,territoryID=out_st_territory_id,msoID=out_st_mso_id,invoice_term=invoice_term,customerId=customerId,credit_type=credit_type,customer_cat=customer_cat,customer_sub_cat=customer_sub_cat,out_st_level1_id=out_st_level1_id,out_st_level2_id=out_st_level2_id))) 
                elif btn_customer_wise_details3:
                    redirect (URL('outStCustomerWiseDetails3',vars=dict(fromDate=from_dt,toDate=to_dt,depotID=depot_id,storeID=store_id,deliveryManID=out_st_delivery_man_id,territoryID=out_st_territory_id,msoID=out_st_mso_id,invoice_term=invoice_term,customerId=customerId,credit_type=credit_type,customer_cat=customer_cat,customer_sub_cat=customer_sub_cat,out_st_level1_id=out_st_level1_id,out_st_level2_id=out_st_level2_id))) 
                    
                elif btn_invoice_wise_AsOfDate:
                    redirect (URL('outStInvoiceWise_AsOfDate',vars=dict(fromDate=from_dt,toDate=to_dt,depotID=depot_id,storeID=store_id,deliveryManID=out_st_delivery_man_id,territoryID=out_st_territory_id,msoID=out_st_mso_id,invoice_term=invoice_term,customerId=customerId,credit_type=credit_type,customer_cat=customer_cat,customer_sub_cat=customer_sub_cat,out_st_level1_id=out_st_level1_id,out_st_level2_id=out_st_level2_id)))
                    
                elif btn_invoice_wise_AsOfDate_tr:
                    redirect (URL('outStInvoiceWise_AsOfDate_tr',vars=dict(toDate=to_dt,depotID=depot_id,storeID=store_id,deliveryManID=out_st_delivery_man_id,territoryID=out_st_territory_id,msoID=out_st_mso_id,invoice_term=invoice_term,customerId=customerId,credit_type=credit_type,customer_cat=customer_cat,customer_sub_cat=customer_sub_cat,out_st_level1_id=out_st_level1_id,out_st_level2_id=out_st_level2_id)))
                elif btn_ost_summary_asOfDate_tr:
                    redirect (URL('outSt_summary_asOfDate_tr',vars=dict(toDate=to_dt,depotID=depot_id,storeID=store_id,deliveryManID=out_st_delivery_man_id,territoryID=out_st_territory_id,msoID=out_st_mso_id,invoice_term=invoice_term,customerId=customerId,credit_type=credit_type,customer_cat=customer_cat,customer_sub_cat=customer_sub_cat,out_st_level1_id=out_st_level1_id,out_st_level2_id=out_st_level2_id)))
                
                elif btn_sales_AsOfDate:
                    redirect (URL('sales_summary_asOfDate',vars=dict(toDate=to_dt,depotID=depot_id,storeID=store_id,deliveryManID=out_st_delivery_man_id,territoryID=out_st_territory_id,msoID=out_st_mso_id,invoice_term=invoice_term,customerId=customerId,credit_type=credit_type,customer_cat=customer_cat,customer_sub_cat=customer_sub_cat,out_st_level1_id=out_st_level1_id,out_st_level2_id=out_st_level2_id)))
                  
                elif btn_received_AsOfDate:
                    redirect (URL('collInvAndReceipt_asOfDate',vars=dict(toDate=to_dt,depotID=depot_id,storeID=store_id,deliveryManID=out_st_delivery_man_id,territoryID=out_st_territory_id,msoID=out_st_mso_id,invoice_term=invoice_term,customerId=customerId,credit_type=credit_type,customer_cat=customer_cat,customer_sub_cat=customer_sub_cat,out_st_level1_id=out_st_level1_id,out_st_level2_id=out_st_level2_id)))
                    
                
                
                
    elif (btn_inv_details or btn_inv_and_receipt or btn_money_receipt_2 or btn_money_receipt or btn_money_receipt_adjustment or btn_collection_transaction_wise or btn_collection_customer_wise or btn_collection_invoice_wise):
        from_dt=request.vars.from_dt_3
        to_dt=request.vars.to_dt_3
        depot=str(request.vars.coll_depot_id)
        store=str(request.vars.coll_store_id)
        
        coll_delivery_man=str(request.vars.coll_delivery_man)
        coll_territory=str(request.vars.coll_territory)
        coll_rsm_fm=str(request.vars.coll_rsm_fm)
        coll_mso=str(request.vars.coll_mso)
        collection_customer=str(request.vars.collection_customer)
        
        coll_inv_term=str(request.vars.coll_inv_term)
        coll_credit_type=str(request.vars.coll_credit_type)
        coll_payment_mode=str(request.vars.coll_payment_mode)
        
        coll_customer_cat=str(request.vars.coll_customer_cat)
        coll_customer_sub_cat=str(request.vars.coll_customer_sub_cat)        
        
        coll_mrno=str(request.vars.coll_mrno)
        coll_inv_sl_from=str(request.vars.coll_inv_sl_from)
        coll_inv_sl_to=str(request.vars.coll_inv_sl_to)
        coll_batchno=str(request.vars.coll_batchno)
        coll_adjustment_cause=str(request.vars.coll_adjustment_cause)
        
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
            if dateDiff>90:
                response.flash="Maximum 90 days allowed between Date Range"
            else:
                if depot=='' or store=='':
                    response.flash='Required Branch and Store'
                else:
                    filterFlag=True
                    if coll_mrno!='':
                        try:
                            coll_mrno=int(coll_mrno)
                            if coll_mrno<1:
                                filterFlag=False
                                response.flash='Required valid MR.No'
                        except:
                            filterFlag=False
                            response.flash='Required valid MR.No'
                    
                    if coll_batchno!='':
                        try:
                            coll_batchno=int(coll_batchno)
                            if coll_batchno<1:
                                filterFlag=False
                                response.flash='Required valid Batch Number'
                        except:
                            filterFlag=False
                            response.flash='Required valid Batch Number'
                            
                    if filterFlag==True and (coll_inv_sl_from!='' or coll_inv_sl_to!=''):
                        try:
                            coll_inv_sl_from=int(coll_inv_sl_from)
                            coll_inv_sl_to=int(coll_inv_sl_to)
                            if coll_inv_sl_from>coll_inv_sl_to:
                                filterFlag=False
                                response.flash='Required valid Invoice From and To'    
                        except:
                            filterFlag=False
                            response.flash='Required valid Invoice From and To'
                            
                    if filterFlag==False:
                        pass
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
                        
                        
                        user_depot_address=''
                        if session.user_type!='Depot':            
                            depotRows = db((db.sm_depot.cid == c_id) & (db.sm_depot.depot_id == depot_id)).select(db.sm_depot.name,db.sm_depot.depot_category,db.sm_depot.field1, limitby=(0, 1))
                            if depotRows:
                                user_depot_address=depotRows[0].field1
                                             
                                session.user_depot_address=user_depot_address
                                
                        coll_delivery_man_id=''
                        coll_delivery_man_name=''
                        if coll_delivery_man!='':
                            coll_delivery_man_id=coll_delivery_man.split('|')[0]
                            coll_delivery_man_name=coll_delivery_man.split('|')[1]
                        
                        coll_territory_id=''
                        coll_territory_name=''
                        if coll_territory!='':
                            coll_territory_id=coll_territory.split('|')[0]
                            coll_territory_name=coll_territory.split('|')[1]
                        
            #            if out_st_rsm_fm!='':
            #                out_st_rsm_fm=out_st_rsm_fm.split('|')[0]
                        coll_mso_id=''
                        coll_mso_name=''
                        if coll_mso!='':
                            coll_mso_id=coll_mso.split('|')[0]
                            coll_mso_name=coll_mso.split('|')[1]
                        
                        customerID=''                    
                        if collection_customer!='':
                            customerID=collection_customer.split('|')[0]
                        
                        if btn_collection_invoice_wise:
                            redirect (URL('collInvoiceWise',vars=dict(fromDate=from_dt,toDate=to_dt,depotID=depot_id,depotName=depot_name,storeID=store_id,storeName=store_name,deliveryManID=coll_delivery_man_id,deliveryManName=coll_delivery_man_name,territoryID=coll_territory_id,territoryName=coll_territory_name,msoID=coll_mso_id,msoName=coll_mso_name)))
                        elif btn_collection_customer_wise:
                            redirect (URL('collCustomerWise',vars=dict(fromDate=from_dt,toDate=to_dt,depotID=depot_id,depotName=depot_name,storeID=store_id,storeName=store_name,deliveryManID=coll_delivery_man_id,deliveryManName=coll_delivery_man_name,territoryID=coll_territory_id,territoryName=coll_territory_name,msoID=coll_mso_id,msoName=coll_mso_name)))
                        elif btn_collection_transaction_wise:
                            redirect (URL('collTransactionWise',vars=dict(fromDate=from_dt,toDate=to_dt,depotID=depot_id,depotName=depot_name,storeID=store_id,storeName=store_name,deliveryManID=coll_delivery_man_id,deliveryManName=coll_delivery_man_name,territoryID=coll_territory_id,territoryName=coll_territory_name,msoID=coll_mso_id,msoName=coll_mso_name)))
                        
                        elif btn_money_receipt:
                            redirect (URL('collMoneyReceipt',vars=dict(fromDate=from_dt,toDate=to_dt,depotID=depot_id,storeID=store_id,deliveryManID=coll_delivery_man_id,territoryID=coll_territory_id,msoID=coll_mso_id,coll_mrno=coll_mrno,coll_inv_sl_from=coll_inv_sl_from,coll_inv_sl_to=coll_inv_sl_to,coll_inv_term=coll_inv_term,coll_credit_type=coll_credit_type,coll_payment_mode=coll_payment_mode,coll_batchno=coll_batchno)))
                        elif btn_money_receipt_2:
                            redirect (URL('collMoneyReceipt2',vars=dict(fromDate=from_dt,toDate=to_dt,depotID=depot_id,storeID=store_id,deliveryManID=coll_delivery_man_id,territoryID=coll_territory_id,msoID=coll_mso_id,customerID=customerID,coll_mrno=coll_mrno,coll_inv_sl_from=coll_inv_sl_from,coll_inv_sl_to=coll_inv_sl_to,coll_inv_term=coll_inv_term,coll_credit_type=coll_credit_type,coll_payment_mode=coll_payment_mode)))
                        
                        elif btn_money_receipt_adjustment:
                            redirect (URL('collMoneyReceiptAdjustment',vars=dict(fromDate=from_dt,toDate=to_dt,depotID=depot_id,storeID=store_id,deliveryManID=coll_delivery_man_id,territoryID=coll_territory_id,msoID=coll_mso_id,coll_mrno=coll_mrno,coll_inv_sl_from=coll_inv_sl_from,coll_inv_sl_to=coll_inv_sl_to,coll_inv_term=coll_inv_term,coll_credit_type=coll_credit_type,coll_payment_mode=coll_payment_mode,coll_adjustment_cause=coll_adjustment_cause)))
                        
                        elif btn_inv_and_receipt:
                            redirect (URL('collInvAndReceipt',vars=dict(fromDate=from_dt,toDate=to_dt,depotID=depot_id,storeID=store_id,deliveryManID=coll_delivery_man_id,territoryID=coll_territory_id,msoID=coll_mso_id,coll_inv_sl_from=coll_inv_sl_from,coll_inv_sl_to=coll_inv_sl_to,coll_inv_term=coll_inv_term,coll_credit_type=coll_credit_type,coll_payment_mode=coll_payment_mode,coll_customer_cat=coll_customer_cat,coll_customer_sub_cat=coll_customer_sub_cat,coll_batchno=coll_batchno)))
                            
                        elif btn_inv_details:
                            redirect (URL('collInvDetails',vars=dict(fromDate=from_dt,toDate=to_dt,depotID=depot_id,storeID=store_id,deliveryManID=coll_delivery_man_id,territoryID=coll_territory_id,msoID=coll_mso_id,coll_inv_sl_from=coll_inv_sl_from,coll_inv_sl_to=coll_inv_sl_to,coll_inv_term=coll_inv_term,coll_credit_type=coll_credit_type,coll_payment_mode=coll_payment_mode,coll_customer_cat=coll_customer_cat,coll_customer_sub_cat=coll_customer_sub_cat,coll_batchno=coll_batchno)))
    
    elif btn_ledger_wise:
        redirect (URL('utility','reports_home'))
    
    elif btn_in_transit:
        redirect (URL('depot','show_pending_issue'))
        
    elif btn_stp_generator or btn_stp_item_wise_sales_distribution:
        from_dt=request.vars.from_dt_4
        to_dt=request.vars.to_dt_4
        depot=str(request.vars.stp_depot_id)
        store=str(request.vars.stp_store_id)
        
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
            if dateDiff>90:
                response.flash="Maximum 90 days allowed between Date Range"
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
                        
                    if session.user_type=='Depot': 
                        depot_id=session.depot_id
                        depot_name=session.user_depot_name
                        
                    
                    if session.user_type!='Depot':            
                        depotRows = db((db.sm_depot.cid == c_id) & (db.sm_depot.depot_id == depot_id)).select(db.sm_depot.name,db.sm_depot.depot_category,db.sm_depot.field1,db.sm_depot.short_name, limitby=(0, 1))
                        if depotRows:                                       
                            session.user_depot_address=depotRows[0].field1
                            session.depot_short_name=depotRows[0].short_name
                            
                    if btn_stp_generator:
                        redirect (URL('stp_generator',vars=dict(fromDate=from_dt,toDate=to_dt,depotID=depot_id,storeID=store_id)))
                    
                    elif btn_stp_item_wise_sales_distribution:
                        redirect (URL('stp_item_wise_sales_distribution',vars=dict(fromDate=from_dt,toDate=to_dt,depotID=depot_id,storeID=store_id)))
                    
    
    #-------------------
    invTermRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='PAYMENT_MODE')).select(db.sm_category_type.cat_type_id,orderby=db.sm_category_type.cat_type_id)
    paymentTypeRows=db((db.sm_category_type.cid==c_id) & (db.sm_category_type.type_name=='PAYMENT_TYPE')).select(db.sm_category_type.cat_type_id,orderby=db.sm_category_type.cat_type_id)
    custSubCatRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_SUB_CATEGORY')).select(db.sm_category_type.cat_type_id,db.sm_category_type.cat_type_name,orderby=db.sm_category_type.cat_type_name)
    custCatRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_CATEGORY')).select(db.sm_category_type.cat_type_id,db.sm_category_type.cat_type_name,orderby=db.sm_category_type.cat_type_name)
    creditTypeRows=db((db.sm_category_type.cid==c_id) & (db.sm_category_type.type_name=='CREDIT_NOTE')).select(db.sm_category_type.cat_type_id,orderby=db.sm_category_type.cat_type_id)
    
    causeRows=db((db.sm_category_type.cid==c_id)&(db.sm_category_type.type_name=='PAYMENT_ADJUSTMENT_TYPE')).select(db.sm_category_type.ALL,orderby=db.sm_category_type.id)
    pri_causeRows=db((db.sm_category_type.cid==c_id) & (db.sm_category_type.type_name=='ADJUSTMENT_TYPE')).select(db.sm_category_type.cat_type_id,db.sm_category_type.field1,orderby=db.sm_category_type.cat_type_id)
    
    return dict(search_form=search_form,invTermRows=invTermRows,paymentTypeRows=paymentTypeRows,custCatRows=custCatRows,custSubCatRows=custSubCatRows,creditTypeRows=creditTypeRows,pri_causeRows=pri_causeRows,causeRows=causeRows)

#------------------------- Collection


def collInvDetails():
    c_id=session.cid
    
    response.title='7.02 Invoice details'
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate    
    
    depot_id=str(request.vars.depotID).strip()
    store_id=str(request.vars.storeID).strip()    
    delivery_man_id=str(request.vars.deliveryManID).strip()  
    territory_id=str(request.vars.territoryID).strip()    
    mso_id=str(request.vars.msoID).strip()
        
    coll_inv_term=str(request.vars.coll_inv_term).strip()  
    coll_credit_type=str(request.vars.coll_credit_type).strip()  
    coll_payment_mode=str(request.vars.coll_payment_mode).strip()  
    
    try:
        coll_inv_sl_from=int(request.vars.coll_inv_sl_from)
        coll_inv_sl_to=int(request.vars.coll_inv_sl_to)
    except:
        coll_inv_sl_from=''
        coll_inv_sl_to=''
    
    try:
        coll_batchno=int(request.vars.coll_batchno)
    except:
        coll_batchno=''
        
    coll_customer_cat=str(request.vars.coll_customer_cat).strip() 
    coll_customer_sub_cat=str(request.vars.coll_customer_sub_cat).strip()    
    catName=''
    custCatRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_CATEGORY')&(db.sm_category_type.cat_type_id==coll_customer_cat)).select(db.sm_category_type.cat_type_name, limitby=(0,1))
    if custCatRows:
        catName=custCatRows[0].cat_type_name        
    subCatName=''
    custSubCatRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_SUB_CATEGORY')&(db.sm_category_type.cat_type_id==coll_customer_sub_cat)).select(db.sm_category_type.cat_type_name, limitby=(0,1))
    if custSubCatRows:
        subCatName=custSubCatRows[0].cat_type_name
    
    depot_name=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depot_name=depotRow[0].name
    
    store_name=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        store_name=storeRow[0].store_name
        
    delivery_man_name=''
    dpRow=db((db.sm_delivery_man.cid==c_id)&(db.sm_delivery_man.depot_id==depot_id)&(db.sm_delivery_man.d_man_id==delivery_man_id)).select(db.sm_delivery_man.name,limitby=(0,1))
    if dpRow:
        delivery_man_name=dpRow[0].name
        
    territory_name=''
    levelRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==territory_id)).select(db.sm_level.level_name,limitby=(0,1))
    if levelRow:
        territory_name=levelRow[0].level_name
         
    mso_name=''
    repRow=db((db.sm_rep.cid==c_id)&(db.sm_rep.rep_id==mso_id)).select(db.sm_rep.name,limitby=(0,1))
    if repRow:
        mso_name=repRow[0].name
        
    startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d').strftime('%Y-%m-%d')    
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d').strftime('%Y-%m-%d')
    
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    
    transactionCause=['','COLLECTION ERROR','ENTRY ERROR']
    
    qset=db()
    qset=qset(db.sm_payment_collection.cid==c_id)
    qset=qset(db.sm_payment_collection.depot_id==depot_id)
    qset=qset(db.sm_payment_collection.store_id==store_id)
    if coll_inv_sl_from!='' and coll_inv_sl_to!='':
        qset=qset((db.sm_payment_collection.sl>=coll_inv_sl_from)&(db.sm_payment_collection.sl<=coll_inv_sl_to))
    else:        
        #qset=qset((db.sm_payment_collection.payment_collection_date>=startDt)&(db.sm_payment_collection.payment_collection_date<=endDt))
        qset=qset((db.sm_payment_collection.collection_date>=startDt)&(db.sm_payment_collection.collection_date<=endDt))
        
    qset=qset(db.sm_payment_collection.status=='Posted')
    #qset=qset(db.sm_payment_collection.transaction_type=='Payment')
    qset=qset(db.sm_payment_collection.transaction_cause.belongs(transactionCause))
    
    if delivery_man_id!='':
        qset=qset(db.sm_payment_collection.d_man_id==delivery_man_id)
    if territory_id!='':
        qset=qset(db.sm_payment_collection.area_id==territory_id)
    if mso_id!='':
        qset=qset(db.sm_payment_collection.rep_id==mso_id)
        
    if coll_inv_term!='':
        qset=qset(db.sm_payment_collection.payment_mode==coll_inv_term)
    if coll_credit_type!='':
        qset=qset(db.sm_payment_collection.credit_note==coll_credit_type)
    if coll_payment_mode!='':
        qset=qset(db.sm_payment_collection.payment_type==coll_payment_mode)
    if coll_customer_cat!='':
        qset=qset(db.sm_payment_collection.cl_category_id==coll_customer_cat)
    if coll_customer_sub_cat!='':
        qset=qset(db.sm_payment_collection.cl_sub_category_id==coll_customer_sub_cat)
        
    if coll_batchno!='':
        qset=qset(db.sm_payment_collection.collection_batch==coll_batchno)
        
    qset=qset(db.sm_invoice_head.cid==c_id)
    qset=qset(db.sm_invoice_head.depot_id==depot_id)
    qset=qset(db.sm_payment_collection.head_rowid==db.sm_invoice_head.id)
    
    records=qset.select(db.sm_invoice_head.id,db.sm_invoice_head.depot_id,db.sm_invoice_head.sl,db.sm_invoice_head.invoice_date.max(),db.sm_invoice_head.shipment_no.max(),db.sm_invoice_head.payment_mode.max(),db.sm_invoice_head.credit_note.max(),db.sm_invoice_head.client_id.max(),db.sm_invoice_head.client_name.max(),db.sm_invoice_head.area_id.max(),db.sm_invoice_head.market_name.max(),db.sm_invoice_head.rep_id.max(),db.sm_invoice_head.rep_name.max(),db.sm_invoice_head.d_man_id.max(),db.sm_invoice_head.d_man_name.max(),db.sm_invoice_head.adjust_amount.max(),db.sm_invoice_head.actual_total_tp.max(),db.sm_invoice_head.vat_total_amount.max(),db.sm_invoice_head.discount.max(),db.sm_invoice_head.sp_discount.max(),db.sm_invoice_head.return_tp.max(),db.sm_invoice_head.return_vat.max(),db.sm_invoice_head.return_discount.max(),db.sm_invoice_head.return_sp_discount.max(),db.sm_payment_collection.payment_collection_date,db.sm_payment_collection.collection_date,db.sm_payment_collection.collection_batch,db.sm_payment_collection.collection_amount.sum(),orderby=db.sm_invoice_head.id|db.sm_payment_collection.collection_date,groupby=db.sm_invoice_head.id|db.sm_invoice_head.depot_id|db.sm_invoice_head.sl|db.sm_payment_collection.collection_date|db.sm_payment_collection.collection_batch)
    
    recTotal=0
    recRows=qset.select(db.sm_payment_collection.cid,db.sm_payment_collection.collection_amount.sum(),groupby=db.sm_payment_collection.cid)
    for recRow in recRows:
        recTotal=recRow[db.sm_payment_collection.collection_amount.sum()]
        
    InvTotalTp=0
    InvTotalVat=0
    InvTotalDisc=0
    InvTotalSp=0
    InvTotalNet=0
    InvTotalAdjust=0
    
    retTotalTp=0
    retTotalVat=0
    retTotalDisc=0
    retTotalSpDisc=0
    retTotal=0
    
    invRows=qset.select(db.sm_invoice_head.id,db.sm_invoice_head.actual_total_tp.max(),db.sm_invoice_head.total_amount.max(),db.sm_invoice_head.vat_total_amount.max(),db.sm_invoice_head.discount.max(),db.sm_invoice_head.sp_discount.max(),db.sm_invoice_head.return_tp.max(),db.sm_invoice_head.return_vat.max(),db.sm_invoice_head.return_discount.max(),db.sm_invoice_head.return_sp_discount.max(),db.sm_invoice_head.adjust_amount.max(),groupby=db.sm_invoice_head.id)
    for invRow in invRows:
        actual_total_tp=invRow[db.sm_invoice_head.actual_total_tp.max()]       
        #total_amount=invRow.total_amount
        vat_total_amount=invRow[db.sm_invoice_head.vat_total_amount.max()]
        total_discount=invRow[db.sm_invoice_head.discount.max()]
        total_sp_discount=invRow[db.sm_invoice_head.sp_discount.max()]
        
        return_tp=invRow[db.sm_invoice_head.return_tp.max()]
        return_vat=invRow[db.sm_invoice_head.return_vat.max()]
        return_discount=invRow[db.sm_invoice_head.return_discount.max()]
        return_sp_discount=invRow[db.sm_invoice_head.return_sp_discount.max()]
        
        adjust_amount=invRow[db.sm_invoice_head.adjust_amount.max()]
        
        return_amt=return_tp+return_vat-return_discount
        
        retTotalTp+=return_tp+return_sp_discount
        retTotalVat+=return_vat
        retTotalDisc+=return_discount
        retTotalSpDisc+=return_sp_discount
        
        #retTotal+=return_amt
        
        #InvTotalTp+=total_amount-vat_total_amount+total_discount
        InvTotalTp+=actual_total_tp        
        InvTotalVat+=vat_total_amount
        InvTotalDisc+=total_discount
        InvTotalSp+=total_sp_discount
        
        #InvTotalNet+=total_amount
        
        InvTotalAdjust+=adjust_amount
        
    InvTotalTpAmt=InvTotalTp-retTotalTp
    InvTotalVatAmt=InvTotalVat-retTotalVat
    InvTotalDiscAmt=InvTotalDisc-retTotalDisc
    InvTotalSpDiscAmt=InvTotalSp-retTotalSpDisc
    
    InvTotalNetAmt=InvTotalTpAmt+InvTotalVatAmt-(InvTotalDiscAmt+InvTotalSpDiscAmt)
    
    if InvTotalNetAmt>0:
        recTpAmt=(InvTotalTpAmt*recTotal)/InvTotalNetAmt
        recVatAmt=(InvTotalVatAmt*recTotal)/InvTotalNetAmt
        recDiscAmt=(InvTotalDiscAmt*recTotal)/InvTotalNetAmt
        recSpDiscAmt=(InvTotalSpDiscAmt*recTotal)/InvTotalNetAmt
    else:
        recTpAmt=0
        recVatAmt=0
        recDiscAmt=0
        recSpDiscAmt=0
    
    #=============================
#     p_totalInvTP=InvTotalTpAmt
#     p_totalInvVat=InvTotalVatAmt
#     p_totalInvDisc=InvTotalDiscAmt
#     p_totalInvSp=InvTotalSpDiscAmt
#     p_totalInvAmt=InvTotalNetAmt
#     
#     percentTp=0
#     percentVat=0
#     percentDisc=0
#     percentSpDisc=0
#     try:
#         percentTp=p_totalInvTP/p_totalInvAmt*100
#         percentVat=p_totalInvVat/p_totalInvAmt*100
#         percentDisc=p_totalInvDisc/p_totalInvAmt*100
#         percentSpDisc=p_totalInvSp/p_totalInvAmt*100
#     except:
#         percentTp=0
#         percentVat=0
#         percentDisc=0
#         percentSpDisc=0
    #========================
    #percentTp=percentTp,percentVat=percentVat,percentDisc=percentDisc,percentSpDisc=percentSpDisc,
    
    return dict(records=records,fromDate=fromDate,toDate=toDate,depotID=depot_id,depotName=depot_name,storeID=store_id,storeName=store_name,deliveryManID=delivery_man_id,deliveryManName=delivery_man_name,territoryID=territory_id,territoryName=territory_name,msoID=mso_id,msoName=mso_name,InvTotalNetAmt=InvTotalNetAmt,InvTotalDiscAmt=InvTotalDiscAmt,InvTotalVatAmt=InvTotalVatAmt,InvTotalTpAmt=InvTotalTpAmt,InvTotalSp=InvTotalSp,recTotal=recTotal,recTpAmt=recTpAmt,recVatAmt=recVatAmt,recDiscAmt=recDiscAmt,recSpDiscAmt=recSpDiscAmt,InvTotalSpDiscAmt=InvTotalSpDiscAmt,InvTotalAdjust=InvTotalAdjust,coll_inv_sl_from=coll_inv_sl_from,coll_inv_sl_to=coll_inv_sl_to,coll_inv_term=coll_inv_term,coll_credit_type=coll_credit_type,coll_payment_mode=coll_payment_mode,coll_customer_cat=coll_customer_cat,coll_customer_sub_cat=coll_customer_sub_cat,catName=catName,subCatName=subCatName,coll_batchno=coll_batchno,page=page,items_per_page=items_per_page)    
    
def collInvDetails_download():
    c_id=session.cid
    
    response.title='Downlaod - Invoice Details'
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    depot_id=str(request.vars.depotID).strip()
    store_id=str(request.vars.storeID).strip()    
    delivery_man_id=str(request.vars.deliveryManID).strip()  
    territory_id=str(request.vars.territoryID).strip()    
    mso_id=str(request.vars.msoID).strip()
        
    coll_inv_term=str(request.vars.coll_inv_term).strip()  
    coll_credit_type=str(request.vars.coll_credit_type).strip()  
    coll_payment_mode=str(request.vars.coll_payment_mode).strip()  
    
    try:
        coll_inv_sl_from=int(request.vars.coll_inv_sl_from)
        coll_inv_sl_to=int(request.vars.coll_inv_sl_to)
    except:
        coll_inv_sl_from=''
        coll_inv_sl_to=''
    
    try:
        coll_batchno=int(request.vars.coll_batchno)
    except:
        coll_batchno=''
        
    coll_customer_cat=str(request.vars.coll_customer_cat).strip() 
    coll_customer_sub_cat=str(request.vars.coll_customer_sub_cat).strip()    
    catName=''
    custCatRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_CATEGORY')&(db.sm_category_type.cat_type_id==coll_customer_cat)).select(db.sm_category_type.cat_type_name, limitby=(0,1))
    if custCatRows:
        catName=custCatRows[0].cat_type_name        
    subCatName=''
    custSubCatRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_SUB_CATEGORY')&(db.sm_category_type.cat_type_id==coll_customer_sub_cat)).select(db.sm_category_type.cat_type_name, limitby=(0,1))
    if custSubCatRows:
        subCatName=custSubCatRows[0].cat_type_name
    
    depot_name=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depot_name=depotRow[0].name
    
    store_name=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        store_name=storeRow[0].store_name
        
    delivery_man_name=''
    dpRow=db((db.sm_delivery_man.cid==c_id)&(db.sm_delivery_man.depot_id==depot_id)&(db.sm_delivery_man.d_man_id==delivery_man_id)).select(db.sm_delivery_man.name,limitby=(0,1))
    if dpRow:
        delivery_man_name=dpRow[0].name
        
    territory_name=''
    levelRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==territory_id)).select(db.sm_level.level_name,limitby=(0,1))
    if levelRow:
        territory_name=levelRow[0].level_name
         
    mso_name=''
    repRow=db((db.sm_rep.cid==c_id)&(db.sm_rep.rep_id==mso_id)).select(db.sm_rep.name,limitby=(0,1))
    if repRow:
        mso_name=repRow[0].name
        
    startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d').strftime('%Y-%m-%d')    
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d').strftime('%Y-%m-%d')
    
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    
    #dateRecords="SELECT a.invoice_date,a.sl, a.client_id, a.client_name, a.area_id,a.market_name, a.discount, a.vat_total_amount, a.total_amount,a.adjust_amount,b.collection_amount,b.collection_date FROM sm_invoice_head a LEFT OUTER JOIN sm_payment_collection b ON a.sl=b.sl where a.cid = '"+c_id+"' and a.invoice_date >= '"+str(startDt)+"' and a.invoice_date <= '"+str(endDt)+"' and a.depot_id = '"+depot_id+"' and a.store_id = '"+store_id+"' and a.status = 'Invoiced' and a.sl !=0 ORDER BY a.sl"
    #records=db.executesql(dateRecords,as_dict = True)    
    
    transactionCause=['','COLLECTION ERROR','ENTRY ERROR']
    
    qset=db()
    qset=qset(db.sm_payment_collection.cid==c_id)
    qset=qset(db.sm_payment_collection.depot_id==depot_id)
    qset=qset(db.sm_payment_collection.store_id==store_id)
    if coll_inv_sl_from!='' and coll_inv_sl_to!='':
        qset=qset((db.sm_payment_collection.sl>=coll_inv_sl_from)&(db.sm_payment_collection.sl<=coll_inv_sl_to))
    else:
        #qset=qset((db.sm_payment_collection.payment_collection_date>=startDt)&(db.sm_payment_collection.payment_collection_date<=endDt))
        qset=qset((db.sm_payment_collection.collection_date>=startDt)&(db.sm_payment_collection.collection_date<=endDt))
        
    qset=qset(db.sm_payment_collection.status=='Posted')
    qset=qset(db.sm_payment_collection.transaction_cause.belongs(transactionCause))
    
    if delivery_man_id!='':
        qset=qset(db.sm_payment_collection.d_man_id==delivery_man_id)
    if territory_id!='':
        qset=qset(db.sm_payment_collection.area_id==territory_id)
    if mso_id!='':
        qset=qset(db.sm_payment_collection.rep_id==mso_id)
         
    if coll_inv_term!='':
        qset=qset(db.sm_payment_collection.payment_mode==coll_inv_term)
    if coll_credit_type!='':
        qset=qset(db.sm_payment_collection.credit_note==coll_credit_type)
    if coll_payment_mode!='':
        qset=qset(db.sm_payment_collection.payment_type==coll_payment_mode)
    if coll_customer_cat!='':
        qset=qset(db.sm_payment_collection.cl_category_id==coll_customer_cat)
    if coll_customer_sub_cat!='':
        qset=qset(db.sm_payment_collection.cl_sub_category_id==coll_customer_sub_cat)
    
    if coll_batchno!='':
        qset=qset(db.sm_payment_collection.collection_batch==coll_batchno)
        
    qset=qset(db.sm_invoice_head.cid==c_id)
    qset=qset(db.sm_invoice_head.depot_id==depot_id)
    qset=qset(db.sm_payment_collection.head_rowid==db.sm_invoice_head.id)
    
    records=qset.select(db.sm_invoice_head.id,db.sm_invoice_head.depot_id,db.sm_invoice_head.sl,db.sm_invoice_head.invoice_date.max(),db.sm_invoice_head.shipment_no.max(),db.sm_invoice_head.payment_mode.max(),db.sm_invoice_head.credit_note.max(),db.sm_invoice_head.client_id.max(),db.sm_invoice_head.client_name.max(),db.sm_invoice_head.area_id.max(),db.sm_invoice_head.market_name.max(),db.sm_invoice_head.rep_id.max(),db.sm_invoice_head.rep_name.max(),db.sm_invoice_head.d_man_id.max(),db.sm_invoice_head.d_man_name.max(),db.sm_invoice_head.adjust_amount.max(),db.sm_invoice_head.actual_total_tp.max(),db.sm_invoice_head.vat_total_amount.max(),db.sm_invoice_head.discount.max(),db.sm_invoice_head.sp_discount.max(),db.sm_invoice_head.return_tp.max(),db.sm_invoice_head.return_vat.max(),db.sm_invoice_head.return_discount.max(),db.sm_invoice_head.return_sp_discount.max(),db.sm_payment_collection.payment_collection_date,db.sm_payment_collection.collection_date,db.sm_payment_collection.collection_batch,db.sm_payment_collection.collection_amount.sum(),orderby=db.sm_invoice_head.id|db.sm_payment_collection.collection_date,groupby=db.sm_invoice_head.id|db.sm_invoice_head.depot_id|db.sm_invoice_head.sl|db.sm_payment_collection.collection_date|db.sm_payment_collection.collection_batch)
    
    recTotal=0
    recRows=qset.select(db.sm_payment_collection.cid,db.sm_payment_collection.collection_amount.sum(),groupby=db.sm_payment_collection.cid)
    for recRow in recRows:
        recTotal=recRow[db.sm_payment_collection.collection_amount.sum()]
        
    InvTotalTp=0
    InvTotalVat=0
    InvTotalDisc=0
    InvTotalSp=0
    InvTotalNet=0
    InvTotalAdjust=0
    
    retTotalTp=0
    retTotalVat=0
    retTotalDisc=0
    retTotalSpDisc=0
    retTotal=0
    
    invRows=qset.select(db.sm_invoice_head.id,db.sm_invoice_head.actual_total_tp.max(),db.sm_invoice_head.total_amount.max(),db.sm_invoice_head.vat_total_amount.max(),db.sm_invoice_head.discount.max(),db.sm_invoice_head.sp_discount.max(),db.sm_invoice_head.return_tp.max(),db.sm_invoice_head.return_vat.max(),db.sm_invoice_head.return_discount.max(),db.sm_invoice_head.return_sp_discount.max(),db.sm_invoice_head.adjust_amount.max(),groupby=db.sm_invoice_head.id)
    for invRow in invRows:
        actual_total_tp=invRow[db.sm_invoice_head.actual_total_tp.max()]       
        #total_amount=invRow.total_amount
        vat_total_amount=invRow[db.sm_invoice_head.vat_total_amount.max()]
        total_discount=invRow[db.sm_invoice_head.discount.max()]
        total_sp_discount=invRow[db.sm_invoice_head.sp_discount.max()]
        
        return_tp=invRow[db.sm_invoice_head.return_tp.max()]
        return_vat=invRow[db.sm_invoice_head.return_vat.max()]
        return_discount=invRow[db.sm_invoice_head.return_discount.max()]
        return_sp_discount=invRow[db.sm_invoice_head.return_sp_discount.max()]
        
        adjust_amount=invRow[db.sm_invoice_head.adjust_amount.max()]
        
        return_amt=return_tp+return_vat-return_discount
        
        retTotalTp+=return_tp+return_sp_discount
        retTotalVat+=return_vat
        retTotalDisc+=return_discount
        retTotalSpDisc+=return_sp_discount
        
        #retTotal+=return_amt
        
        #InvTotalTp+=total_amount-vat_total_amount+total_discount
        InvTotalTp+=actual_total_tp        
        InvTotalVat+=vat_total_amount
        InvTotalDisc+=total_discount
        InvTotalSp+=total_sp_discount
        
        #InvTotalNet+=total_amount
        
        InvTotalAdjust+=adjust_amount
        
    InvTotalTpAmt=InvTotalTp-retTotalTp
    InvTotalVatAmt=InvTotalVat-retTotalVat
    InvTotalDiscAmt=InvTotalDisc-retTotalDisc
    InvTotalSpDiscAmt=InvTotalSp-retTotalSpDisc    
    InvTotalNetAmt=InvTotalTpAmt+InvTotalVatAmt-(InvTotalDiscAmt+InvTotalSpDiscAmt)
    
        
    recTpAmt=0
    recVatAmt=0
    recDiscAmt=0
    recSpDiscAmt=0
    
    #=============================
#     p_totalInvTP=InvTotalTpAmt
#     p_totalInvVat=InvTotalVatAmt
#     p_totalInvDisc=InvTotalDiscAmt
#     p_totalInvSp=InvTotalSpDiscAmt
#     p_totalInvAmt=InvTotalNetAmt
#     
#     percentTp=0
#     percentVat=0
#     percentDisc=0
#     percentSpDisc=0
#     try:
#         percentTp=p_totalInvTP/p_totalInvAmt*100
#         percentVat=p_totalInvVat/p_totalInvAmt*100
#         percentDisc=p_totalInvDisc/p_totalInvAmt*100
#         percentSpDisc=p_totalInvSp/p_totalInvAmt*100
#     except:
#         percentTp=0
#         percentVat=0
#         percentDisc=0
#         percentSpDisc=0
    #========================
    
    #-------------    
    myString='7.2 Invoice Wise Cash Collection: Invoice Details\n'
    
    if coll_inv_sl_from!='' and coll_inv_sl_to!='':
        myString+='INV.No,From:'+str(coll_inv_sl_from)+',To:'+str(coll_inv_sl_to)+'\n'
    else:
        myString+='Received Date From:,'+str(startDt)+'\n'            
        myString+='To Date:'+','+str(endDt)+'\n'
        
    myString+='Branch ID:,'+str(depot_id)+'\n'
    myString+='Branch Name'+','+str(depot_name)+'\n'
    myString+='Store ID:,'+str(store_id)+'\n'
    myString+='Store Name'+','+str(store_name)+'\n'
    myString+='DP ID:,'+str(delivery_man_id)+'\n'
    myString+='DP Name'+','+str(delivery_man_name)+'\n'
    myString+='Territory ID:,'+str(territory_id)+'\n'
    myString+='Territory Name'+','+str(territory_name)+'\n'
    myString+='MSO ID:,'+str(mso_id)+'\n'
    myString+='MSO Name'+','+str(mso_name)+'\n'
    
    if coll_inv_term=='':
        coll_inv_term='ALL'
    else:
        if coll_inv_term=='CREDIT':
            if coll_credit_type=='':
                coll_credit_type='ALL'
    if coll_payment_mode=='':
        coll_payment_mode='ALL'    
    
    myString+='Invoice Term:,'+str(coll_inv_term)+'\n'
    myString+='Credit Type:,'+str(coll_credit_type)+'\n'
    myString+='Payment Type:,'+str(coll_payment_mode)+'\n'
    
    if catName=='':
        catName='ALL'
    if subCatName=='':
        subCatName='ALL'        
    myString+='Customer Category'+','+str(catName)+'\n'
    myString+='Customer Sub-Category'+','+str(subCatName)+'\n'
    
    if coll_batchno!='':
        myString+='Batch Number'+',`'+str(coll_batchno)+'\n'
    
    sl=0
    myString+='SL,Inv.Date,ShipNo,Invoice No,InvoiceTerm,CreditType,Cust. ID,Cust. Name,Tr. Code,Market,SPID,SPName,DPID,DPName,Adjusted,RECEIVED-TP,RECEIVED-Vat,RECEIVED-Disc,RECEIVED-SP,RECEIVED-Net,Received Date,BatchNumber,Transaction Date'+'\n'
    for row in records:
        sl+=1
        
        invoice_date=row[db.sm_invoice_head.invoice_date.max()] 
        if row.sm_invoice_head.sl==0:
            shipment_no=row[db.sm_invoice_head.shipment_no.max()]
        else:
            shipment_no=str(session.prefix_invoice)+'SH-'+str(row[db.sm_invoice_head.shipment_no.max()])        
        invSl=str(session.prefix_invoice)+'INV'+str(row.sm_invoice_head.depot_id)+'-'+str(row.sm_invoice_head.sl)        
        payment_mode=row[db.sm_invoice_head.payment_mode.max()]
        credit_note=row[db.sm_invoice_head.credit_note.max()]
#         invTermAndCreditType=''
#         if str(payment_mode).upper()=='CASH':
#             invTermAndCreditType=payment_mode
#         else:
#             invTermAndCreditType=credit_note
            
        client_id=row[db.sm_invoice_head.client_id.max()]
        client_name=row[db.sm_invoice_head.client_name.max()]
        area_id=row[db.sm_invoice_head.area_id.max()]
        market_name=row[db.sm_invoice_head.market_name.max()]
        rep_id=row[db.sm_invoice_head.rep_id.max()]
        rep_name=row[db.sm_invoice_head.rep_name.max()]
        d_man_id=row[db.sm_invoice_head.d_man_id.max()]
        d_man_name=row[db.sm_invoice_head.d_man_name.max()]
        
        invTpAmt=round(row[db.sm_invoice_head.actual_total_tp.max()]-(row[db.sm_invoice_head.return_tp.max()]+row[db.sm_invoice_head.return_sp_discount.max()]),2)
        invVatAmt=round(row[db.sm_invoice_head.vat_total_amount.max()]-row[db.sm_invoice_head.return_vat.max()],2)
        invDiscAmt=round(row[db.sm_invoice_head.discount.max()]-row[db.sm_invoice_head.return_discount.max()],2)
        invSpDiscAmt=round(row[db.sm_invoice_head.sp_discount.max()]-row[db.sm_invoice_head.return_sp_discount.max()],2)
        invTotal=invTpAmt+invVatAmt-(invDiscAmt+invSpDiscAmt)
        
        invNet=row[db.sm_invoice_head.actual_total_tp.max()]+row[db.sm_invoice_head.vat_total_amount.max()]-(row[db.sm_invoice_head.discount.max()]+row[db.sm_invoice_head.sp_discount.max()])
        
        adjust_amount=round(row[db.sm_invoice_head.adjust_amount.max()],2)
        
        collectAmt=round(row[db.sm_payment_collection.collection_amount.sum()],2)
        
        if invNet>0:
            recTp=round((row[db.sm_invoice_head.actual_total_tp.max()]/invNet*collectAmt),2)
            recVat=round((row[db.sm_invoice_head.vat_total_amount.max()]/invNet*collectAmt),2)
            recDisc=round((row[db.sm_invoice_head.discount.max()]/invNet*collectAmt),2)
            recSpDisc=round((row[db.sm_invoice_head.sp_discount.max()]/invNet*collectAmt),2)
            
#             recTp=round((invTpAmt*collectAmt)/invTotal,2)
#             recVat=round((invVatAmt*collectAmt)/invTotal,2)
#             recDisc=round((invDiscAmt*collectAmt)/invTotal,2)
#             recSpDisc=round((invSpDiscAmt*collectAmt)/invTotal,2)
            
#             recTp=round(collectAmt*(percentTp/100),2)
#             recVat=round(collectAmt*(percentVat/100),2)
#             recDisc=round(collectAmt*(percentDisc/100),2)
#             recSpDisc=round(collectAmt*(percentSpDisc/100),2)
            
        else:
            recTp=0
            recVat=0
            recDisc=0
            recSpDisc=0
            
        recTpAmt+=recTp
        recVatAmt+=recVat
        recDiscAmt+=recDisc
        recSpDiscAmt+=recSpDisc
        
        collection_date=row.sm_payment_collection.collection_date
        payment_collection_date=row.sm_payment_collection.payment_collection_date
        collection_batch=row.sm_payment_collection.collection_batch
        
        #------------------------        
        myString+=str(sl)+','+str(invoice_date)+','+str(shipment_no)+','+str(invSl)+','+str(payment_mode)+','+str(credit_note)+','+str(client_id)+','+str(client_name)+','+str(area_id)+','+str(market_name)+','+str(rep_id)+','+str(rep_name)+','+str(d_man_id)+','+str(d_man_name)+','+\
        str(adjust_amount)+','+str(recTp)+','+str(recVat)+','+str(recDisc)+','+str(recSpDisc)+','+str(collectAmt)+','+\
        str(collection_date)+','+str(collection_batch)+','+str(payment_collection_date)+'\n'
        
    myString+='\n\nSummary,,,,,,,,,,,,,,,,,,,,\n'    
    myString+='Invoice TP,'+str(round(InvTotalTpAmt,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Invoice VAT,'+str(round(InvTotalVatAmt,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Invoice Discount,'+str(round(InvTotalDiscAmt,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Invoice SP.Disc,'+str(round(InvTotalSpDiscAmt,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Invoice Net,'+str(round(InvTotalNetAmt,2))+',,,,,,,,,,,,,,,,,,,\n\n'
    
    myString+='Received TP,'+str(round(recTpAmt,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Received VAT,'+str(round(recVatAmt,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Received Discount,'+str(round(recDiscAmt,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Received SP.Disc,'+str(round(recSpDiscAmt,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Received Net,'+str(round(recTotal,2))+',,,,,,,,,,,,,,,,,,,\n\n'
    
    myString+='Outstanding Net,'+str(round(InvTotalNetAmt-recTotal,2))+',,,,,,,,,,,,,,,,,,,\n\n'
    
    myString+='After Adjusted,-,,,,,,,,,,,,,,,,,,,\n'
    
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_collInvDetails.csv'   
    return str(myString)
    
def collInvDetails_bak():
    c_id=session.cid
    
    response.title='7.02 Invoice details'
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate    
    
    depot_id=str(request.vars.depotID).strip()
    store_id=str(request.vars.storeID).strip()    
    delivery_man_id=str(request.vars.deliveryManID).strip()  
    territory_id=str(request.vars.territoryID).strip()    
    mso_id=str(request.vars.msoID).strip()
        
    coll_inv_term=str(request.vars.coll_inv_term).strip()  
    coll_credit_type=str(request.vars.coll_credit_type).strip()  
    coll_payment_mode=str(request.vars.coll_payment_mode).strip()  
    
    try:
        coll_inv_sl_from=int(request.vars.coll_inv_sl_from)
        coll_inv_sl_to=int(request.vars.coll_inv_sl_to)
    except:
        coll_inv_sl_from=''
        coll_inv_sl_to=''
    
    try:
        coll_batchno=int(request.vars.coll_batchno)
    except:
        coll_batchno=''
        
    coll_customer_cat=str(request.vars.coll_customer_cat).strip() 
    coll_customer_sub_cat=str(request.vars.coll_customer_sub_cat).strip()    
    catName=''
    custCatRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_CATEGORY')&(db.sm_category_type.cat_type_id==coll_customer_cat)).select(db.sm_category_type.cat_type_name, limitby=(0,1))
    if custCatRows:
        catName=custCatRows[0].cat_type_name        
    subCatName=''
    custSubCatRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_SUB_CATEGORY')&(db.sm_category_type.cat_type_id==coll_customer_sub_cat)).select(db.sm_category_type.cat_type_name, limitby=(0,1))
    if custSubCatRows:
        subCatName=custSubCatRows[0].cat_type_name
    
    depot_name=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depot_name=depotRow[0].name
    
    store_name=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        store_name=storeRow[0].store_name
        
    delivery_man_name=''
    dpRow=db((db.sm_delivery_man.cid==c_id)&(db.sm_delivery_man.depot_id==depot_id)&(db.sm_delivery_man.d_man_id==delivery_man_id)).select(db.sm_delivery_man.name,limitby=(0,1))
    if dpRow:
        delivery_man_name=dpRow[0].name
        
    territory_name=''
    levelRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==territory_id)).select(db.sm_level.level_name,limitby=(0,1))
    if levelRow:
        territory_name=levelRow[0].level_name
         
    mso_name=''
    repRow=db((db.sm_rep.cid==c_id)&(db.sm_rep.rep_id==mso_id)).select(db.sm_rep.name,limitby=(0,1))
    if repRow:
        mso_name=repRow[0].name
        
    startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d').strftime('%Y-%m-%d')    
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d').strftime('%Y-%m-%d')
    
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    
    transactionCause=['','COLLECTION ERROR','ENTRY ERROR']
    
    qset=db()
    qset=qset(db.sm_payment_collection.cid==c_id)
    qset=qset(db.sm_payment_collection.depot_id==depot_id)
    qset=qset(db.sm_payment_collection.store_id==store_id)
    if coll_inv_sl_from!='' and coll_inv_sl_to!='':
        qset=qset((db.sm_payment_collection.sl>=coll_inv_sl_from)&(db.sm_payment_collection.sl<=coll_inv_sl_to))
    else:        
        qset=qset((db.sm_payment_collection.payment_collection_date>=startDt)&(db.sm_payment_collection.payment_collection_date<=endDt))
    
    qset=qset(db.sm_payment_collection.status=='Posted')
    #qset=qset(db.sm_payment_collection.transaction_type=='Payment')
    qset=qset(db.sm_payment_collection.transaction_cause.belongs(transactionCause))
    
    if delivery_man_id!='':
        qset=qset(db.sm_payment_collection.d_man_id==delivery_man_id)
    if territory_id!='':
        qset=qset(db.sm_payment_collection.area_id==territory_id)
    if mso_id!='':
        qset=qset(db.sm_payment_collection.rep_id==mso_id)
        
    if coll_inv_term!='':
        qset=qset(db.sm_payment_collection.payment_mode==coll_inv_term)
    if coll_credit_type!='':
        qset=qset(db.sm_payment_collection.credit_note==coll_credit_type)
    if coll_payment_mode!='':
        qset=qset(db.sm_payment_collection.payment_type==coll_payment_mode)
    if coll_customer_cat!='':
        qset=qset(db.sm_payment_collection.cl_category_id==coll_customer_cat)
    if coll_customer_sub_cat!='':
        qset=qset(db.sm_payment_collection.cl_sub_category_id==coll_customer_sub_cat)
        
    if coll_batchno!='':
        qset=qset(db.sm_payment_collection.collection_batch==coll_batchno)
        
    qset=qset(db.sm_invoice_head.cid==c_id)
    qset=qset(db.sm_invoice_head.depot_id==depot_id)
    qset=qset(db.sm_payment_collection.head_rowid==db.sm_invoice_head.id)
    
    records=qset.select(db.sm_invoice_head.id,db.sm_invoice_head.depot_id,db.sm_invoice_head.sl,db.sm_invoice_head.invoice_date.max(),db.sm_invoice_head.shipment_no.max(),db.sm_invoice_head.payment_mode.max(),db.sm_invoice_head.credit_note.max(),db.sm_invoice_head.client_id.max(),db.sm_invoice_head.client_name.max(),db.sm_invoice_head.area_id.max(),db.sm_invoice_head.market_name.max(),db.sm_invoice_head.rep_id.max(),db.sm_invoice_head.rep_name.max(),db.sm_invoice_head.d_man_id.max(),db.sm_invoice_head.d_man_name.max(),db.sm_invoice_head.adjust_amount.max(),db.sm_invoice_head.actual_total_tp.max(),db.sm_invoice_head.vat_total_amount.max(),db.sm_invoice_head.discount.max(),db.sm_invoice_head.sp_discount.max(),db.sm_invoice_head.return_tp.max(),db.sm_invoice_head.return_vat.max(),db.sm_invoice_head.return_discount.max(),db.sm_invoice_head.return_sp_discount.max(),db.sm_payment_collection.payment_collection_date,db.sm_payment_collection.collection_batch,db.sm_payment_collection.collection_amount.sum(),orderby=db.sm_invoice_head.id|db.sm_payment_collection.payment_collection_date,groupby=db.sm_invoice_head.id|db.sm_invoice_head.depot_id|db.sm_invoice_head.sl|db.sm_payment_collection.payment_collection_date|db.sm_payment_collection.collection_batch)
    
    recTotal=0
    recRows=qset.select(db.sm_payment_collection.cid,db.sm_payment_collection.collection_amount.sum(),groupby=db.sm_payment_collection.cid)
    for recRow in recRows:
        recTotal=recRow[db.sm_payment_collection.collection_amount.sum()]
        
    InvTotalTp=0
    InvTotalVat=0
    InvTotalDisc=0
    InvTotalSp=0
    InvTotalNet=0
    InvTotalAdjust=0
    
    retTotalTp=0
    retTotalVat=0
    retTotalDisc=0
    retTotalSpDisc=0
    retTotal=0
    
    invRows=qset.select(db.sm_invoice_head.id,db.sm_invoice_head.actual_total_tp.max(),db.sm_invoice_head.total_amount.max(),db.sm_invoice_head.vat_total_amount.max(),db.sm_invoice_head.discount.max(),db.sm_invoice_head.sp_discount.max(),db.sm_invoice_head.return_tp.max(),db.sm_invoice_head.return_vat.max(),db.sm_invoice_head.return_discount.max(),db.sm_invoice_head.return_sp_discount.max(),db.sm_invoice_head.adjust_amount.max(),groupby=db.sm_invoice_head.id)
    for invRow in invRows:
        actual_total_tp=invRow[db.sm_invoice_head.actual_total_tp.max()]       
        #total_amount=invRow.total_amount
        vat_total_amount=invRow[db.sm_invoice_head.vat_total_amount.max()]
        total_discount=invRow[db.sm_invoice_head.discount.max()]
        total_sp_discount=invRow[db.sm_invoice_head.sp_discount.max()]
        
        return_tp=invRow[db.sm_invoice_head.return_tp.max()]
        return_vat=invRow[db.sm_invoice_head.return_vat.max()]
        return_discount=invRow[db.sm_invoice_head.return_discount.max()]
        return_sp_discount=invRow[db.sm_invoice_head.return_sp_discount.max()]
        
        adjust_amount=invRow[db.sm_invoice_head.adjust_amount.max()]
        
        return_amt=return_tp+return_vat-return_discount
        
        retTotalTp+=return_tp+return_sp_discount
        retTotalVat+=return_vat
        retTotalDisc+=return_discount
        retTotalSpDisc+=return_sp_discount
        
        #retTotal+=return_amt
        
        #InvTotalTp+=total_amount-vat_total_amount+total_discount
        InvTotalTp+=actual_total_tp        
        InvTotalVat+=vat_total_amount
        InvTotalDisc+=total_discount
        InvTotalSp+=total_sp_discount
        
        #InvTotalNet+=total_amount
        
        InvTotalAdjust+=adjust_amount
        
    InvTotalTpAmt=InvTotalTp-retTotalTp
    InvTotalVatAmt=InvTotalVat-retTotalVat
    InvTotalDiscAmt=InvTotalDisc-retTotalDisc
    InvTotalSpDiscAmt=InvTotalSp-retTotalSpDisc
    
    InvTotalNetAmt=InvTotalTpAmt+InvTotalVatAmt-(InvTotalDiscAmt+InvTotalSpDiscAmt)
    
    if InvTotalNetAmt>0:
        recTpAmt=(InvTotalTpAmt*recTotal)/InvTotalNetAmt
        recVatAmt=(InvTotalVatAmt*recTotal)/InvTotalNetAmt
        recDiscAmt=(InvTotalDiscAmt*recTotal)/InvTotalNetAmt
        recSpDiscAmt=(InvTotalSpDiscAmt*recTotal)/InvTotalNetAmt
    else:
        recTpAmt=0
        recVatAmt=0
        recDiscAmt=0
        recSpDiscAmt=0
        
    return dict(records=records,fromDate=fromDate,toDate=toDate,depotID=depot_id,depotName=depot_name,storeID=store_id,storeName=store_name,deliveryManID=delivery_man_id,deliveryManName=delivery_man_name,territoryID=territory_id,territoryName=territory_name,msoID=mso_id,msoName=mso_name,InvTotalNetAmt=InvTotalNetAmt,InvTotalDiscAmt=InvTotalDiscAmt,InvTotalVatAmt=InvTotalVatAmt,InvTotalTpAmt=InvTotalTpAmt,InvTotalSp=InvTotalSp,recTotal=recTotal,recTpAmt=recTpAmt,recVatAmt=recVatAmt,recDiscAmt=recDiscAmt,recSpDiscAmt=recSpDiscAmt,InvTotalSpDiscAmt=InvTotalSpDiscAmt,InvTotalAdjust=InvTotalAdjust,coll_inv_sl_from=coll_inv_sl_from,coll_inv_sl_to=coll_inv_sl_to,coll_inv_term=coll_inv_term,coll_credit_type=coll_credit_type,coll_payment_mode=coll_payment_mode,coll_customer_cat=coll_customer_cat,coll_customer_sub_cat=coll_customer_sub_cat,catName=catName,subCatName=subCatName,coll_batchno=coll_batchno,page=page,items_per_page=items_per_page)    
    
def collInvDetails_download_bak():
    c_id=session.cid
    
    response.title='Downlaod - Invoice Details'
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    depot_id=str(request.vars.depotID).strip()
    store_id=str(request.vars.storeID).strip()    
    delivery_man_id=str(request.vars.deliveryManID).strip()  
    territory_id=str(request.vars.territoryID).strip()    
    mso_id=str(request.vars.msoID).strip()
        
    coll_inv_term=str(request.vars.coll_inv_term).strip()  
    coll_credit_type=str(request.vars.coll_credit_type).strip()  
    coll_payment_mode=str(request.vars.coll_payment_mode).strip()  
    
    try:
        coll_inv_sl_from=int(request.vars.coll_inv_sl_from)
        coll_inv_sl_to=int(request.vars.coll_inv_sl_to)
    except:
        coll_inv_sl_from=''
        coll_inv_sl_to=''
    
    try:
        coll_batchno=int(request.vars.coll_batchno)
    except:
        coll_batchno=''
        
    coll_customer_cat=str(request.vars.coll_customer_cat).strip() 
    coll_customer_sub_cat=str(request.vars.coll_customer_sub_cat).strip()    
    catName=''
    custCatRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_CATEGORY')&(db.sm_category_type.cat_type_id==coll_customer_cat)).select(db.sm_category_type.cat_type_name, limitby=(0,1))
    if custCatRows:
        catName=custCatRows[0].cat_type_name        
    subCatName=''
    custSubCatRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_SUB_CATEGORY')&(db.sm_category_type.cat_type_id==coll_customer_sub_cat)).select(db.sm_category_type.cat_type_name, limitby=(0,1))
    if custSubCatRows:
        subCatName=custSubCatRows[0].cat_type_name
    
    depot_name=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depot_name=depotRow[0].name
    
    store_name=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        store_name=storeRow[0].store_name
        
    delivery_man_name=''
    dpRow=db((db.sm_delivery_man.cid==c_id)&(db.sm_delivery_man.depot_id==depot_id)&(db.sm_delivery_man.d_man_id==delivery_man_id)).select(db.sm_delivery_man.name,limitby=(0,1))
    if dpRow:
        delivery_man_name=dpRow[0].name
        
    territory_name=''
    levelRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==territory_id)).select(db.sm_level.level_name,limitby=(0,1))
    if levelRow:
        territory_name=levelRow[0].level_name
         
    mso_name=''
    repRow=db((db.sm_rep.cid==c_id)&(db.sm_rep.rep_id==mso_id)).select(db.sm_rep.name,limitby=(0,1))
    if repRow:
        mso_name=repRow[0].name
        
    startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d').strftime('%Y-%m-%d')    
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d').strftime('%Y-%m-%d')
    
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    
    #dateRecords="SELECT a.invoice_date,a.sl, a.client_id, a.client_name, a.area_id,a.market_name, a.discount, a.vat_total_amount, a.total_amount,a.adjust_amount,b.collection_amount,b.collection_date FROM sm_invoice_head a LEFT OUTER JOIN sm_payment_collection b ON a.sl=b.sl where a.cid = '"+c_id+"' and a.invoice_date >= '"+str(startDt)+"' and a.invoice_date <= '"+str(endDt)+"' and a.depot_id = '"+depot_id+"' and a.store_id = '"+store_id+"' and a.status = 'Invoiced' and a.sl !=0 ORDER BY a.sl"
    #records=db.executesql(dateRecords,as_dict = True)    
    
    transactionCause=['','COLLECTION ERROR','ENTRY ERROR']
    
    qset=db()
    qset=qset(db.sm_payment_collection.cid==c_id)
    qset=qset(db.sm_payment_collection.depot_id==depot_id)
    qset=qset(db.sm_payment_collection.store_id==store_id)
    if coll_inv_sl_from!='' and coll_inv_sl_to!='':
        qset=qset((db.sm_payment_collection.sl>=coll_inv_sl_from)&(db.sm_payment_collection.sl<=coll_inv_sl_to))
    else:        
        qset=qset((db.sm_payment_collection.payment_collection_date>=startDt)&(db.sm_payment_collection.payment_collection_date<=endDt))
    
    qset=qset(db.sm_payment_collection.status=='Posted')
    #qset=qset(db.sm_payment_collection.transaction_type=='Payment')
    qset=qset(db.sm_payment_collection.transaction_cause.belongs(transactionCause))
    
    if delivery_man_id!='':
        qset=qset(db.sm_payment_collection.d_man_id==delivery_man_id)
    if territory_id!='':
        qset=qset(db.sm_payment_collection.area_id==territory_id)
    if mso_id!='':
        qset=qset(db.sm_payment_collection.rep_id==mso_id)
         
    if coll_inv_term!='':
        qset=qset(db.sm_payment_collection.payment_mode==coll_inv_term)
    if coll_credit_type!='':
        qset=qset(db.sm_payment_collection.credit_note==coll_credit_type)
    if coll_payment_mode!='':
        qset=qset(db.sm_payment_collection.payment_type==coll_payment_mode)
    if coll_customer_cat!='':
        qset=qset(db.sm_payment_collection.cl_category_id==coll_customer_cat)
    if coll_customer_sub_cat!='':
        qset=qset(db.sm_payment_collection.cl_sub_category_id==coll_customer_sub_cat)
    
    if coll_batchno!='':
        qset=qset(db.sm_payment_collection.collection_batch==coll_batchno)
        
    qset=qset(db.sm_invoice_head.cid==c_id)
    qset=qset(db.sm_invoice_head.depot_id==depot_id)
    qset=qset(db.sm_payment_collection.head_rowid==db.sm_invoice_head.id)
    
    records=qset.select(db.sm_invoice_head.id,db.sm_invoice_head.depot_id,db.sm_invoice_head.sl,db.sm_invoice_head.invoice_date.max(),db.sm_invoice_head.shipment_no.max(),db.sm_invoice_head.payment_mode.max(),db.sm_invoice_head.credit_note.max(),db.sm_invoice_head.client_id.max(),db.sm_invoice_head.client_name.max(),db.sm_invoice_head.area_id.max(),db.sm_invoice_head.market_name.max(),db.sm_invoice_head.rep_id.max(),db.sm_invoice_head.rep_name.max(),db.sm_invoice_head.d_man_id.max(),db.sm_invoice_head.d_man_name.max(),db.sm_invoice_head.adjust_amount.max(),db.sm_invoice_head.actual_total_tp.max(),db.sm_invoice_head.vat_total_amount.max(),db.sm_invoice_head.discount.max(),db.sm_invoice_head.sp_discount.max(),db.sm_invoice_head.return_tp.max(),db.sm_invoice_head.return_vat.max(),db.sm_invoice_head.return_discount.max(),db.sm_invoice_head.return_sp_discount.max(),db.sm_payment_collection.payment_collection_date,db.sm_payment_collection.collection_batch,db.sm_payment_collection.collection_amount.sum(),orderby=db.sm_invoice_head.id|db.sm_payment_collection.payment_collection_date,groupby=db.sm_invoice_head.id|db.sm_invoice_head.depot_id|db.sm_invoice_head.sl|db.sm_payment_collection.payment_collection_date|db.sm_payment_collection.collection_batch)
    
    recTotal=0
    recRows=qset.select(db.sm_payment_collection.cid,db.sm_payment_collection.collection_amount.sum(),groupby=db.sm_payment_collection.cid)
    for recRow in recRows:
        recTotal=recRow[db.sm_payment_collection.collection_amount.sum()]
        
    InvTotalTp=0
    InvTotalVat=0
    InvTotalDisc=0
    InvTotalSp=0
    InvTotalNet=0
    InvTotalAdjust=0
    
    retTotalTp=0
    retTotalVat=0
    retTotalDisc=0
    retTotalSpDisc=0
    retTotal=0
    
    invRows=qset.select(db.sm_invoice_head.id,db.sm_invoice_head.actual_total_tp.max(),db.sm_invoice_head.total_amount.max(),db.sm_invoice_head.vat_total_amount.max(),db.sm_invoice_head.discount.max(),db.sm_invoice_head.sp_discount.max(),db.sm_invoice_head.return_tp.max(),db.sm_invoice_head.return_vat.max(),db.sm_invoice_head.return_discount.max(),db.sm_invoice_head.return_sp_discount.max(),db.sm_invoice_head.adjust_amount.max(),groupby=db.sm_invoice_head.id)
    for invRow in invRows:
        actual_total_tp=invRow[db.sm_invoice_head.actual_total_tp.max()]       
        #total_amount=invRow.total_amount
        vat_total_amount=invRow[db.sm_invoice_head.vat_total_amount.max()]
        total_discount=invRow[db.sm_invoice_head.discount.max()]
        total_sp_discount=invRow[db.sm_invoice_head.sp_discount.max()]
        
        return_tp=invRow[db.sm_invoice_head.return_tp.max()]
        return_vat=invRow[db.sm_invoice_head.return_vat.max()]
        return_discount=invRow[db.sm_invoice_head.return_discount.max()]
        return_sp_discount=invRow[db.sm_invoice_head.return_sp_discount.max()]
        
        adjust_amount=invRow[db.sm_invoice_head.adjust_amount.max()]
        
        return_amt=return_tp+return_vat-return_discount
        
        retTotalTp+=return_tp+return_sp_discount
        retTotalVat+=return_vat
        retTotalDisc+=return_discount
        retTotalSpDisc+=return_sp_discount
        
        #retTotal+=return_amt
        
        #InvTotalTp+=total_amount-vat_total_amount+total_discount
        InvTotalTp+=actual_total_tp        
        InvTotalVat+=vat_total_amount
        InvTotalDisc+=total_discount
        InvTotalSp+=total_sp_discount
        
        #InvTotalNet+=total_amount
        
        InvTotalAdjust+=adjust_amount
        
    InvTotalTpAmt=InvTotalTp-retTotalTp
    InvTotalVatAmt=InvTotalVat-retTotalVat
    InvTotalDiscAmt=InvTotalDisc-retTotalDisc
    InvTotalSpDiscAmt=InvTotalSp-retTotalSpDisc    
    InvTotalNetAmt=InvTotalTpAmt+InvTotalVatAmt-(InvTotalDiscAmt+InvTotalSpDiscAmt)
    
        
    recTpAmt=0
    recVatAmt=0
    recDiscAmt=0
    recSpDiscAmt=0
    
    #-------------    
    myString='7.2 Invoice Wise Cash Collection: Invoice Details\n'
    
    if coll_inv_sl_from!='' and coll_inv_sl_to!='':
        myString+='INV.No,From:'+str(coll_inv_sl_from)+',To:'+str(coll_inv_sl_to)+'\n'
    else:
        myString+='Rec. Date From:,'+str(startDt)+'\n'            
        myString+='To Date:'+','+str(endDt)+'\n'
        
    myString+='Branch ID:,'+str(depot_id)+'\n'
    myString+='Branch Name'+','+str(depot_name)+'\n'
    myString+='Store ID:,'+str(store_id)+'\n'
    myString+='Store Name'+','+str(store_name)+'\n'
    myString+='DP ID:,'+str(delivery_man_id)+'\n'
    myString+='DP Name'+','+str(delivery_man_name)+'\n'
    myString+='Territory ID:,'+str(territory_id)+'\n'
    myString+='Territory Name'+','+str(territory_name)+'\n'
    myString+='MSO ID:,'+str(mso_id)+'\n'
    myString+='MSO Name'+','+str(mso_name)+'\n'
    
    if coll_inv_term=='':
        coll_inv_term='ALL'
    else:
        if coll_inv_term=='CREDIT':
            if coll_credit_type=='':
                coll_credit_type='ALL'
    if coll_payment_mode=='':
        coll_payment_mode='ALL'    
    
    myString+='Invoice Term:,'+str(coll_inv_term)+'\n'
    myString+='Credit Type:,'+str(coll_credit_type)+'\n'
    myString+='Payment Type:,'+str(coll_payment_mode)+'\n'
    
    if catName=='':
        catName='ALL'
    if subCatName=='':
        subCatName='ALL'        
    myString+='Customer Category'+','+str(catName)+'\n'
    myString+='Customer Sub-Category'+','+str(subCatName)+'\n'
    
    if coll_batchno!='':
        myString+='Batch Number'+',`'+str(coll_batchno)+'\n'
    
    sl=0
    myString+='SL,Inv.Date,ShipNo,Invoice No,InvoiceTerm,CreditType,Cust. ID,Cust. Name,Tr. Code,Market,SPID,SPName,DPID,DPName,Adjusted,RECEIVED-TP,RECEIVED-Vat,RECEIVED-Disc,RECEIVED-SP,RECEIVED-Net,Rec.Date,BatchNumber'+'\n'
    for row in records:
        sl+=1
        
        invoice_date=row[db.sm_invoice_head.invoice_date.max()] 
        if row.sm_invoice_head.sl==0:
            shipment_no=row[db.sm_invoice_head.shipment_no.max()]
        else:
            shipment_no=str(session.prefix_invoice)+'SH-'+str(row[db.sm_invoice_head.shipment_no.max()])        
        invSl=str(session.prefix_invoice)+'INV'+str(row.sm_invoice_head.depot_id)+'-'+str(row.sm_invoice_head.sl)        
        payment_mode=row[db.sm_invoice_head.payment_mode.max()]
        credit_note=row[db.sm_invoice_head.credit_note.max()]
#         invTermAndCreditType=''
#         if str(payment_mode).upper()=='CASH':
#             invTermAndCreditType=payment_mode
#         else:
#             invTermAndCreditType=credit_note
            
        client_id=row[db.sm_invoice_head.client_id.max()]
        client_name=row[db.sm_invoice_head.client_name.max()]
        area_id=row[db.sm_invoice_head.area_id.max()]
        market_name=row[db.sm_invoice_head.market_name.max()]
        rep_id=row[db.sm_invoice_head.rep_id.max()]
        rep_name=row[db.sm_invoice_head.rep_name.max()]
        d_man_id=row[db.sm_invoice_head.d_man_id.max()]
        d_man_name=row[db.sm_invoice_head.d_man_name.max()]
        
        invTpAmt=round(row[db.sm_invoice_head.actual_total_tp.max()]-(row[db.sm_invoice_head.return_tp.max()]+row[db.sm_invoice_head.return_sp_discount.max()]),2)
        invVatAmt=round(row[db.sm_invoice_head.vat_total_amount.max()]-row[db.sm_invoice_head.return_vat.max()],2)
        invDiscAmt=round(row[db.sm_invoice_head.discount.max()]-row[db.sm_invoice_head.return_discount.max()],2)
        invSpDiscAmt=round(row[db.sm_invoice_head.sp_discount.max()]-row[db.sm_invoice_head.return_sp_discount.max()],2)
        invTotal=invTpAmt+invVatAmt-(invDiscAmt+invSpDiscAmt)
        
        adjust_amount=round(row[db.sm_invoice_head.adjust_amount.max()],2)
        
        collectAmt=round(row[db.sm_payment_collection.collection_amount.sum()],2)
        
        if invTotal>0:
            recTp=round((invTpAmt*collectAmt)/invTotal,2)
            recVat=round((invVatAmt*collectAmt)/invTotal,2)
            recDisc=round((invDiscAmt*collectAmt)/invTotal,2)
            recSpDisc=round((invSpDiscAmt*collectAmt)/invTotal,2)
        else:
            recTp=0
            recVat=0
            recDisc=0
            recSpDisc=0
            
        recTpAmt+=recTp
        recVatAmt+=recVat
        recDiscAmt+=recDisc
        recSpDiscAmt+=recSpDisc
        
        payment_collection_date=row.sm_payment_collection.payment_collection_date        
        collection_batch=row.sm_payment_collection.collection_batch
        
        #------------------------        
        myString+=str(sl)+','+str(invoice_date)+','+str(shipment_no)+','+str(invSl)+','+str(payment_mode)+','+str(credit_note)+','+str(client_id)+','+str(client_name)+','+str(area_id)+','+str(market_name)+','+str(rep_id)+','+str(rep_name)+','+str(d_man_id)+','+str(d_man_name)+','+\
        str(adjust_amount)+','+str(recTp)+','+str(recVat)+','+str(recDisc)+','+str(recSpDisc)+','+str(collectAmt)+','+\
        str(payment_collection_date)+','+str(collection_batch)+'\n'
    
    
    myString+='\n\nSummary,,,,,,,,,,,,,,,,,,,,\n'    
    myString+='Invoice TP,'+str(round(InvTotalTpAmt,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Invoice VAT,'+str(round(InvTotalVatAmt,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Invoice Discount,'+str(round(InvTotalDiscAmt,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Invoice SP.Disc,'+str(round(InvTotalSpDiscAmt,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Invoice Net,'+str(round(InvTotalNetAmt,2))+',,,,,,,,,,,,,,,,,,,\n\n'
    
    myString+='Received TP,'+str(round(recTpAmt,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Received VAT,'+str(round(recVatAmt,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Received Discount,'+str(round(recDiscAmt,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Received SP.Disc,'+str(round(recSpDiscAmt,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Received Net,'+str(round(recTotal,2))+',,,,,,,,,,,,,,,,,,,\n\n'
    
    myString+='Outstanding Net,'+str(round(InvTotalNetAmt-recTotal,2))+',,,,,,,,,,,,,,,,,,,\n\n'
    
    myString+='After Adjusted,-,,,,,,,,,,,,,,,,,,,\n'
    
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_collInvDetails.csv'   
    return str(myString)
    



def collInvAndReceipt():
    c_id=session.cid
    
    response.title='7.01 Invoice and Receipt'
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate    
    
    depot_id=str(request.vars.depotID).strip()
    store_id=str(request.vars.storeID).strip()    
    delivery_man_id=str(request.vars.deliveryManID).strip()  
    territory_id=str(request.vars.territoryID).strip()    
    mso_id=str(request.vars.msoID).strip()
    
    coll_inv_term=str(request.vars.coll_inv_term).strip()  
    coll_credit_type=str(request.vars.coll_credit_type).strip()  
    coll_payment_mode=str(request.vars.coll_payment_mode).strip()  
    
    try:
        coll_inv_sl_from=int(request.vars.coll_inv_sl_from)
        coll_inv_sl_to=int(request.vars.coll_inv_sl_to)
    except:
        coll_inv_sl_from=''
        coll_inv_sl_to=''
    
    try:
        coll_batchno=int(request.vars.coll_batchno)
    except:
        coll_batchno=''
        
    coll_customer_cat=str(request.vars.coll_customer_cat).strip() 
    coll_customer_sub_cat=str(request.vars.coll_customer_sub_cat).strip()    
    catName=''
    custCatRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_CATEGORY')&(db.sm_category_type.cat_type_id==coll_customer_cat)).select(db.sm_category_type.cat_type_name, limitby=(0,1))
    if custCatRows:
        catName=custCatRows[0].cat_type_name        
    subCatName=''
    custSubCatRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_SUB_CATEGORY')&(db.sm_category_type.cat_type_id==coll_customer_sub_cat)).select(db.sm_category_type.cat_type_name, limitby=(0,1))
    if custSubCatRows:
        subCatName=custSubCatRows[0].cat_type_name
        
    depot_name=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depot_name=depotRow[0].name
        
    store_name=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        store_name=storeRow[0].store_name
        
    delivery_man_name=''
    dpRow=db((db.sm_delivery_man.cid==c_id)&(db.sm_delivery_man.depot_id==depot_id)&(db.sm_delivery_man.d_man_id==delivery_man_id)).select(db.sm_delivery_man.name,limitby=(0,1))
    if dpRow:
        delivery_man_name=dpRow[0].name
        
    territory_name=''
    levelRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==territory_id)).select(db.sm_level.level_name,limitby=(0,1))
    if levelRow:
        territory_name=levelRow[0].level_name
        
    mso_name=''
    repRow=db((db.sm_rep.cid==c_id)&(db.sm_rep.rep_id==mso_id)).select(db.sm_rep.name,limitby=(0,1))
    if repRow:
        mso_name=repRow[0].name
        
    startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d').strftime('%Y-%m-%d')    
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d').strftime('%Y-%m-%d')
    
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    
    transactionCause=['','COLLECTION ERROR','ENTRY ERROR']
    
    qset=db()
    qset=qset(db.sm_payment_collection.cid==c_id)
    qset=qset(db.sm_payment_collection.depot_id==depot_id)
    qset=qset(db.sm_payment_collection.store_id==store_id)
    if coll_inv_sl_from!='' and coll_inv_sl_to!='':
        qset=qset((db.sm_payment_collection.sl>=coll_inv_sl_from)&(db.sm_payment_collection.sl<=coll_inv_sl_to))
    else:        
        #qset=qset((db.sm_payment_collection.payment_collection_date>=startDt)&(db.sm_payment_collection.payment_collection_date<=endDt))
        qset=qset((db.sm_payment_collection.collection_date>=startDt)&(db.sm_payment_collection.collection_date<=endDt))
        
    qset=qset(db.sm_payment_collection.status=='Posted')
    qset=qset(db.sm_payment_collection.transaction_cause.belongs(transactionCause))
    
    if delivery_man_id!='':
        qset=qset(db.sm_payment_collection.d_man_id==delivery_man_id)
    if territory_id!='':
        qset=qset(db.sm_payment_collection.area_id==territory_id)
    if mso_id!='':
        qset=qset(db.sm_payment_collection.rep_id==mso_id)
         
    if coll_inv_term!='':
        qset=qset(db.sm_payment_collection.payment_mode==coll_inv_term)
    if coll_credit_type!='':
        qset=qset(db.sm_payment_collection.credit_note==coll_credit_type)
    if coll_payment_mode!='':
        qset=qset(db.sm_payment_collection.payment_type==coll_payment_mode)
    if coll_customer_cat!='':
        qset=qset(db.sm_payment_collection.cl_category_id==coll_customer_cat)
    if coll_customer_sub_cat!='':
        qset=qset(db.sm_payment_collection.cl_sub_category_id==coll_customer_sub_cat)
        
    if coll_batchno!='':
        qset=qset(db.sm_payment_collection.collection_batch==coll_batchno)
    
    qset=qset(db.sm_invoice_head.cid==c_id)
    qset=qset(db.sm_invoice_head.depot_id==depot_id)
    qset=qset(db.sm_payment_collection.head_rowid==db.sm_invoice_head.id)
    
    records=qset.select(db.sm_invoice_head.id,db.sm_invoice_head.depot_id,db.sm_invoice_head.sl,db.sm_invoice_head.invoice_date.max(),db.sm_invoice_head.shipment_no.max(),db.sm_invoice_head.payment_mode.max(),db.sm_invoice_head.credit_note.max(),db.sm_invoice_head.client_id.max(),db.sm_invoice_head.client_name.max(),db.sm_invoice_head.area_id.max(),db.sm_invoice_head.market_name.max(),db.sm_invoice_head.rep_id.max(),db.sm_invoice_head.rep_name.max(),db.sm_invoice_head.d_man_id.max(),db.sm_invoice_head.d_man_name.max(),db.sm_invoice_head.adjust_amount.max(),db.sm_invoice_head.actual_total_tp.max(),db.sm_invoice_head.vat_total_amount.max(),db.sm_invoice_head.discount.max(),db.sm_invoice_head.sp_discount.max(),db.sm_invoice_head.return_tp.max(),db.sm_invoice_head.return_vat.max(),db.sm_invoice_head.return_discount.max(),db.sm_invoice_head.return_sp_discount.max(),db.sm_payment_collection.payment_collection_date,db.sm_payment_collection.collection_date,db.sm_payment_collection.collection_batch,db.sm_payment_collection.collection_amount.sum(),orderby=db.sm_invoice_head.id|db.sm_payment_collection.collection_date,groupby=db.sm_invoice_head.id|db.sm_invoice_head.depot_id|db.sm_invoice_head.sl|db.sm_payment_collection.collection_date|db.sm_payment_collection.collection_batch)
    
    recTotal=0
    recRows=qset.select(db.sm_payment_collection.cid,db.sm_payment_collection.collection_amount.sum(),groupby=db.sm_payment_collection.cid)
    for recRow in recRows:
        recTotal=recRow[db.sm_payment_collection.collection_amount.sum()]
        
    InvTotalTp=0
    InvTotalVat=0
    InvTotalDisc=0
    InvTotalSp=0
    InvTotalNet=0
    InvTotalAdjust=0
    
    retTotalTp=0
    retTotalVat=0
    retTotalDisc=0
    retTotalSpDisc=0
    retTotal=0
    
    invRows=qset.select(db.sm_invoice_head.id,db.sm_invoice_head.actual_total_tp.max(),db.sm_invoice_head.total_amount.max(),db.sm_invoice_head.vat_total_amount.max(),db.sm_invoice_head.discount.max(),db.sm_invoice_head.sp_discount.max(),db.sm_invoice_head.return_tp.max(),db.sm_invoice_head.return_vat.max(),db.sm_invoice_head.return_discount.max(),db.sm_invoice_head.return_sp_discount.max(),db.sm_invoice_head.adjust_amount.max(),groupby=db.sm_invoice_head.id)
    for invRow in invRows:
        actual_total_tp=invRow[db.sm_invoice_head.actual_total_tp.max()]       
        #total_amount=invRow.total_amount
        vat_total_amount=invRow[db.sm_invoice_head.vat_total_amount.max()]
        total_discount=invRow[db.sm_invoice_head.discount.max()]
        total_sp_discount=invRow[db.sm_invoice_head.sp_discount.max()]
        
        return_tp=invRow[db.sm_invoice_head.return_tp.max()]
        return_vat=invRow[db.sm_invoice_head.return_vat.max()]
        return_discount=invRow[db.sm_invoice_head.return_discount.max()]
        return_sp_discount=invRow[db.sm_invoice_head.return_sp_discount.max()]
        
        adjust_amount=invRow[db.sm_invoice_head.adjust_amount.max()]
        
        return_amt=return_tp+return_vat-return_discount
        
        retTotalTp+=return_tp+return_sp_discount
        retTotalVat+=return_vat
        retTotalDisc+=return_discount
        retTotalSpDisc+=return_sp_discount
        
        #retTotal+=return_amt
        
        #InvTotalTp+=total_amount-vat_total_amount+total_discount
        InvTotalTp+=actual_total_tp        
        InvTotalVat+=vat_total_amount
        InvTotalDisc+=total_discount
        InvTotalSp+=total_sp_discount
        
        #InvTotalNet+=total_amount
        
        InvTotalAdjust+=adjust_amount
        
    InvTotalTpAmt=InvTotalTp-retTotalTp
    InvTotalVatAmt=InvTotalVat-retTotalVat
    InvTotalDiscAmt=InvTotalDisc-retTotalDisc
    InvTotalSpDiscAmt=InvTotalSp-retTotalSpDisc
    
    InvTotalNetAmt=InvTotalTpAmt+InvTotalVatAmt-(InvTotalDiscAmt+InvTotalSpDiscAmt)
    
    if InvTotalNetAmt>0:
        recTpAmt=(InvTotalTpAmt*recTotal)/InvTotalNetAmt
        recVatAmt=(InvTotalVatAmt*recTotal)/InvTotalNetAmt
        recDiscAmt=(InvTotalDiscAmt*recTotal)/InvTotalNetAmt
        recSpDiscAmt=(InvTotalSpDiscAmt*recTotal)/InvTotalNetAmt
    else:
        recTpAmt=0
        recVatAmt=0
        recDiscAmt=0
        recSpDiscAmt=0
        
    #=============================
#     p_totalInvTP=InvTotalTpAmt
#     p_totalInvVat=InvTotalVatAmt
#     p_totalInvDisc=InvTotalDiscAmt
#     p_totalInvSp=InvTotalSpDiscAmt
#     p_totalInvAmt=InvTotalNetAmt
#     
#     percentTp=0
#     percentVat=0
#     percentDisc=0
#     percentSpDisc=0
#     try:
#         percentTp=p_totalInvTP/p_totalInvAmt*100
#         percentVat=p_totalInvVat/p_totalInvAmt*100
#         percentDisc=p_totalInvDisc/p_totalInvAmt*100
#         percentSpDisc=p_totalInvSp/p_totalInvAmt*100
#     except:
#         percentTp=0
#         percentVat=0
#         percentDisc=0
#         percentSpDisc=0
    #========================
    #percentTp=percentTp,percentVat=percentVat,percentDisc=percentDisc,percentSpDisc=percentSpDisc,
    
    return dict(records=records,fromDate=fromDate,toDate=toDate,depotID=depot_id,depotName=depot_name,storeID=store_id,storeName=store_name,deliveryManID=delivery_man_id,deliveryManName=delivery_man_name,territoryID=territory_id,territoryName=territory_name,msoID=mso_id,msoName=mso_name,InvTotalNetAmt=InvTotalNetAmt,InvTotalDiscAmt=InvTotalDiscAmt,InvTotalVatAmt=InvTotalVatAmt,InvTotalTpAmt=InvTotalTpAmt,InvTotalSp=InvTotalSp,recTotal=recTotal,recTpAmt=recTpAmt,recVatAmt=recVatAmt,recDiscAmt=recDiscAmt,recSpDiscAmt=recSpDiscAmt,InvTotalSpDiscAmt=InvTotalSpDiscAmt,InvTotalAdjust=InvTotalAdjust,coll_inv_sl_from=coll_inv_sl_from,coll_inv_sl_to=coll_inv_sl_to,coll_inv_term=coll_inv_term,coll_credit_type=coll_credit_type,coll_payment_mode=coll_payment_mode,coll_customer_cat=coll_customer_cat,coll_customer_sub_cat=coll_customer_sub_cat,catName=catName,subCatName=subCatName,coll_batchno=coll_batchno,page=page,items_per_page=items_per_page)    
    
def collInvAndReceipt_download():
    c_id=session.cid
    
    response.title='7.01 Downlaod - Invoice and Receipt'
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate    
    
    depot_id=str(request.vars.depotID).strip()
    store_id=str(request.vars.storeID).strip()    
    delivery_man_id=str(request.vars.deliveryManID).strip()  
    territory_id=str(request.vars.territoryID).strip()    
    mso_id=str(request.vars.msoID).strip()
    
    coll_inv_term=str(request.vars.coll_inv_term).strip()  
    coll_credit_type=str(request.vars.coll_credit_type).strip()  
    coll_payment_mode=str(request.vars.coll_payment_mode).strip()  
    
    try:
        coll_inv_sl_from=int(request.vars.coll_inv_sl_from)
        coll_inv_sl_to=int(request.vars.coll_inv_sl_to)
    except:
        coll_inv_sl_from=''
        coll_inv_sl_to=''
        
    try:
        coll_batchno=int(request.vars.coll_batchno)
    except:
        coll_batchno=''
        
    coll_customer_cat=str(request.vars.coll_customer_cat).strip() 
    coll_customer_sub_cat=str(request.vars.coll_customer_sub_cat).strip()    
    catName=''
    custCatRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_CATEGORY')&(db.sm_category_type.cat_type_id==coll_customer_cat)).select(db.sm_category_type.cat_type_name, limitby=(0,1))
    if custCatRows:
        catName=custCatRows[0].cat_type_name        
    subCatName=''
    custSubCatRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_SUB_CATEGORY')&(db.sm_category_type.cat_type_id==coll_customer_sub_cat)).select(db.sm_category_type.cat_type_name, limitby=(0,1))
    if custSubCatRows:
        subCatName=custSubCatRows[0].cat_type_name
    
    depot_name=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depot_name=depotRow[0].name
    
    store_name=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        store_name=storeRow[0].store_name
        
    delivery_man_name=''
    dpRow=db((db.sm_delivery_man.cid==c_id)&(db.sm_delivery_man.depot_id==depot_id)&(db.sm_delivery_man.d_man_id==delivery_man_id)).select(db.sm_delivery_man.name,limitby=(0,1))
    if dpRow:
        delivery_man_name=dpRow[0].name
        
    territory_name=''
    levelRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==territory_id)).select(db.sm_level.level_name,limitby=(0,1))
    if levelRow:
        territory_name=levelRow[0].level_name
         
    mso_name=''
    repRow=db((db.sm_rep.cid==c_id)&(db.sm_rep.rep_id==mso_id)).select(db.sm_rep.name,limitby=(0,1))
    if repRow:
        mso_name=repRow[0].name
        
    startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d').strftime('%Y-%m-%d')    
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d').strftime('%Y-%m-%d')
    
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    
    #dateRecords="SELECT a.invoice_date,a.sl, a.client_id, a.client_name, a.area_id,a.market_name, a.discount, a.vat_total_amount, a.total_amount,a.adjust_amount,b.collection_amount,b.collection_date FROM sm_invoice_head a LEFT OUTER JOIN sm_payment_collection b ON a.sl=b.sl where a.cid = '"+c_id+"' and a.invoice_date >= '"+str(startDt)+"' and a.invoice_date <= '"+str(endDt)+"' and a.depot_id = '"+depot_id+"' and a.store_id = '"+store_id+"' and a.status = 'Invoiced' and a.sl !=0 ORDER BY a.sl"
    #records=db.executesql(dateRecords,as_dict = True)    
    
    transactionCause=['','COLLECTION ERROR','ENTRY ERROR']
    
    qset=db()
    qset=qset(db.sm_payment_collection.cid==c_id)
    qset=qset(db.sm_payment_collection.depot_id==depot_id)
    qset=qset(db.sm_payment_collection.store_id==store_id)
    if coll_inv_sl_from!='' and coll_inv_sl_to!='':
        qset=qset((db.sm_payment_collection.sl>=coll_inv_sl_from)&(db.sm_payment_collection.sl<=coll_inv_sl_to))
    else:        
        #qset=qset((db.sm_payment_collection.payment_collection_date>=startDt)&(db.sm_payment_collection.payment_collection_date<=endDt))
        qset=qset((db.sm_payment_collection.collection_date>=startDt)&(db.sm_payment_collection.collection_date<=endDt))
        
    qset=qset(db.sm_payment_collection.status=='Posted')    
    qset=qset(db.sm_payment_collection.transaction_cause.belongs(transactionCause))
    
    if delivery_man_id!='':
        qset=qset(db.sm_payment_collection.d_man_id==delivery_man_id)
    if territory_id!='':
        qset=qset(db.sm_payment_collection.area_id==territory_id)
    if mso_id!='':
        qset=qset(db.sm_payment_collection.rep_id==mso_id)
        
    if coll_inv_term!='':
        qset=qset(db.sm_payment_collection.payment_mode==coll_inv_term)
    if coll_credit_type!='':
        qset=qset(db.sm_payment_collection.credit_note==coll_credit_type)
    if coll_payment_mode!='':
        qset=qset(db.sm_payment_collection.payment_type==coll_payment_mode)
    if coll_customer_cat!='':
        qset=qset(db.sm_payment_collection.cl_category_id==coll_customer_cat)
    if coll_customer_sub_cat!='':
        qset=qset(db.sm_payment_collection.cl_sub_category_id==coll_customer_sub_cat)
    
    if coll_batchno!='':
        qset=qset(db.sm_payment_collection.collection_batch==coll_batchno)
    
    qset=qset(db.sm_invoice_head.cid==c_id)
    qset=qset(db.sm_invoice_head.depot_id==depot_id)
    qset=qset(db.sm_payment_collection.head_rowid==db.sm_invoice_head.id)
    
    records=qset.select(db.sm_invoice_head.id,db.sm_invoice_head.depot_id,db.sm_invoice_head.sl,db.sm_invoice_head.invoice_date.max(),db.sm_invoice_head.shipment_no.max(),db.sm_invoice_head.payment_mode.max(),db.sm_invoice_head.credit_note.max(),db.sm_invoice_head.client_id.max(),db.sm_invoice_head.client_name.max(),db.sm_invoice_head.area_id.max(),db.sm_invoice_head.market_name.max(),db.sm_invoice_head.rep_id.max(),db.sm_invoice_head.rep_name.max(),db.sm_invoice_head.d_man_id.max(),db.sm_invoice_head.d_man_name.max(),db.sm_invoice_head.adjust_amount.max(),db.sm_invoice_head.actual_total_tp.max(),db.sm_invoice_head.vat_total_amount.max(),db.sm_invoice_head.discount.max(),db.sm_invoice_head.sp_discount.max(),db.sm_invoice_head.return_tp.max(),db.sm_invoice_head.return_vat.max(),db.sm_invoice_head.return_discount.max(),db.sm_invoice_head.return_sp_discount.max(),db.sm_payment_collection.payment_collection_date,db.sm_payment_collection.collection_date,db.sm_payment_collection.collection_batch,db.sm_payment_collection.collection_amount.sum(),orderby=db.sm_invoice_head.id|db.sm_payment_collection.collection_date,groupby=db.sm_invoice_head.id|db.sm_invoice_head.depot_id|db.sm_invoice_head.sl|db.sm_payment_collection.collection_date|db.sm_payment_collection.collection_batch)
    
    recTotal=0
    recRows=qset.select(db.sm_payment_collection.cid,db.sm_payment_collection.collection_amount.sum(),groupby=db.sm_payment_collection.cid)
    for recRow in recRows:
        recTotal=recRow[db.sm_payment_collection.collection_amount.sum()]
        
    InvTotalTp=0
    InvTotalVat=0
    InvTotalDisc=0
    InvTotalSp=0
    InvTotalNet=0
    InvTotalAdjust=0
    
    retTotalTp=0
    retTotalVat=0
    retTotalDisc=0
    retTotalSpDisc=0
    retTotal=0
    
    invRows=qset.select(db.sm_invoice_head.id,db.sm_invoice_head.actual_total_tp.max(),db.sm_invoice_head.total_amount.max(),db.sm_invoice_head.vat_total_amount.max(),db.sm_invoice_head.discount.max(),db.sm_invoice_head.sp_discount.max(),db.sm_invoice_head.return_tp.max(),db.sm_invoice_head.return_vat.max(),db.sm_invoice_head.return_discount.max(),db.sm_invoice_head.return_sp_discount.max(),db.sm_invoice_head.adjust_amount.max(),groupby=db.sm_invoice_head.id)
    for invRow in invRows:
        actual_total_tp=invRow[db.sm_invoice_head.actual_total_tp.max()]       
        #total_amount=invRow.total_amount
        vat_total_amount=invRow[db.sm_invoice_head.vat_total_amount.max()]
        total_discount=invRow[db.sm_invoice_head.discount.max()]
        total_sp_discount=invRow[db.sm_invoice_head.sp_discount.max()]
        
        return_tp=invRow[db.sm_invoice_head.return_tp.max()]
        return_vat=invRow[db.sm_invoice_head.return_vat.max()]
        return_discount=invRow[db.sm_invoice_head.return_discount.max()]
        return_sp_discount=invRow[db.sm_invoice_head.return_sp_discount.max()]
        
        adjust_amount=invRow[db.sm_invoice_head.adjust_amount.max()]
        
        return_amt=return_tp+return_vat-return_discount
        
        retTotalTp+=return_tp+return_sp_discount
        retTotalVat+=return_vat
        retTotalDisc+=return_discount
        retTotalSpDisc+=return_sp_discount
        
        #retTotal+=return_amt
        
        #InvTotalTp+=total_amount-vat_total_amount+total_discount
        InvTotalTp+=actual_total_tp        
        InvTotalVat+=vat_total_amount
        InvTotalDisc+=total_discount
        InvTotalSp+=total_sp_discount
        
        #InvTotalNet+=total_amount
        
        InvTotalAdjust+=adjust_amount
        
    InvTotalTpAmt=InvTotalTp-retTotalTp
    InvTotalVatAmt=InvTotalVat-retTotalVat
    InvTotalDiscAmt=InvTotalDisc-retTotalDisc
    InvTotalSpDiscAmt=InvTotalSp-retTotalSpDisc
    
    InvTotalNetAmt=InvTotalTpAmt+InvTotalVatAmt-(InvTotalDiscAmt+InvTotalSpDiscAmt)
    
    recTpAmt=0
    recVatAmt=0
    recDiscAmt=0
    recSpDiscAmt=0
    
    #=============================
#     p_totalInvTP=InvTotalTpAmt
#     p_totalInvVat=InvTotalVatAmt
#     p_totalInvDisc=InvTotalDiscAmt
#     p_totalInvSp=InvTotalSpDiscAmt
#     p_totalInvAmt=InvTotalNetAmt
#     
#     percentTp=0
#     percentVat=0
#     percentDisc=0
#     percentSpDisc=0
#     try:
#         percentTp=p_totalInvTP/p_totalInvAmt*100
#         percentVat=p_totalInvVat/p_totalInvAmt*100
#         percentDisc=p_totalInvDisc/p_totalInvAmt*100
#         percentSpDisc=p_totalInvSp/p_totalInvAmt*100
#     except:
#         percentTp=0
#         percentVat=0
#         percentDisc=0
#         percentSpDisc=0
    #========================
    
    #-------------
    myString='7.1 Invoice Wise Cash Collection: With Invoice & Receipt Details\n'
    
    if coll_inv_sl_from!='' and coll_inv_sl_to!='':
        myString+='INV.No '+',From:'+str(coll_inv_sl_from)+',To:'+str(coll_inv_sl_to)+'\n'
    else:
        myString+='Received Date From:,'+str(startDt)+'\n'            
        myString+='To Date:'+','+str(endDt)+'\n'
        
    myString+='Branch ID:,'+str(depot_id)+'\n'
    myString+='Branch Name'+','+str(depot_name)+'\n'
    myString+='Store ID:,'+str(store_id)+'\n'
    myString+='Store Name'+','+str(store_name)+'\n'
    myString+='DP ID:,'+str(delivery_man_id)+'\n'
    myString+='DP Name'+','+str(delivery_man_name)+'\n'
    myString+='Territory ID:,'+str(territory_id)+'\n'
    myString+='Territory Name'+','+str(territory_name)+'\n'
    myString+='MSO ID:,'+str(mso_id)+'\n'
    myString+='MSO Name'+','+str(mso_name)+'\n'
    
    if coll_inv_term=='':
        coll_inv_term='ALL'
    else:
        if coll_inv_term=='CREDIT':
            if coll_credit_type=='':
                coll_credit_type='ALL'
    if coll_payment_mode=='':
        coll_payment_mode='ALL'    
        
    myString+='Invoice Term:,'+str(coll_inv_term)+'\n'
    myString+='Credit Type:,'+str(coll_credit_type)+'\n'
    myString+='Payment Type:,'+str(coll_payment_mode)+'\n'
    
    if catName=='':
        catName='ALL'
    if subCatName=='':
        subCatName='ALL'        
    myString+='Customer Category'+','+str(catName)+'\n'
    myString+='Customer Sub-Category'+','+str(subCatName)+'\n'
    
    if coll_batchno!='':
        myString+='Batch Number'+',`'+str(coll_batchno)+'\n'
        
    sl=0
    myString+='SL,Inv.Date,ShipNo,Invoice No,InvoiceTerm,CreditType,Cust. ID,Cust. Name,Tr. Code,Market,SPID,SPName,DPID,DPName,INVOICE-TP,INVOICE-Vat,INVOICE-Disc,INVOICE-SP,INVOICE-Net,Adjusted,RECEIVED-TP,RECEIVED-Vat,RECEIVED-Disc,RECEIVED-SP,RECEIVED-Net,Received Date,BatchNo,Transaction Date'+'\n'
    for row in records:
        sl+=1
        
        invoice_date=row[db.sm_invoice_head.invoice_date.max()] 
        if row.sm_invoice_head.sl==0:
            shipment_no=row[db.sm_invoice_head.shipment_no.max()]
        else:
            shipment_no=str(session.prefix_invoice)+'SH-'+str(row[db.sm_invoice_head.shipment_no.max()])        
        invSl=str(session.prefix_invoice)+'INV'+str(row.sm_invoice_head.depot_id)+'-'+str(row.sm_invoice_head.sl)        
        payment_mode=row[db.sm_invoice_head.payment_mode.max()]
        credit_note=row[db.sm_invoice_head.credit_note.max()]
#         invTermAndCreditType=''
#         if str(payment_mode).upper()=='CASH':
#             invTermAndCreditType=payment_mode
#         else:
#             invTermAndCreditType=credit_note
            
        client_id=row[db.sm_invoice_head.client_id.max()]
        client_name=row[db.sm_invoice_head.client_name.max()]
        area_id=row[db.sm_invoice_head.area_id.max()]
        market_name=row[db.sm_invoice_head.market_name.max()]
        rep_id=row[db.sm_invoice_head.rep_id.max()]
        rep_name=row[db.sm_invoice_head.rep_name.max()]
        d_man_id=row[db.sm_invoice_head.d_man_id.max()]
        d_man_name=row[db.sm_invoice_head.d_man_name.max()]
        
        invTpAmt=round(row[db.sm_invoice_head.actual_total_tp.max()]-(row[db.sm_invoice_head.return_tp.max()]+row[db.sm_invoice_head.return_sp_discount.max()]),2)
        invVatAmt=round(row[db.sm_invoice_head.vat_total_amount.max()]-row[db.sm_invoice_head.return_vat.max()],2)
        invDiscAmt=round(row[db.sm_invoice_head.discount.max()]-row[db.sm_invoice_head.return_discount.max()],2)
        invSpDiscAmt=round(row[db.sm_invoice_head.sp_discount.max()]-row[db.sm_invoice_head.return_sp_discount.max()],2)
        invTotal=invTpAmt+invVatAmt-(invDiscAmt+invSpDiscAmt)
        
        invNet=row[db.sm_invoice_head.actual_total_tp.max()]+row[db.sm_invoice_head.vat_total_amount.max()]-(row[db.sm_invoice_head.discount.max()]+row[db.sm_invoice_head.sp_discount.max()])
        
        adjust_amount=round(row[db.sm_invoice_head.adjust_amount.max()],2)
        
        collectAmt=round(row[db.sm_payment_collection.collection_amount.sum()],2)
        
        if invNet>0:            
            recTp=round((row[db.sm_invoice_head.actual_total_tp.max()]/invNet*collectAmt),2)
            recVat=round((row[db.sm_invoice_head.vat_total_amount.max()]/invNet*collectAmt),2)
            recDisc=round((row[db.sm_invoice_head.discount.max()]/invNet*collectAmt),2)
            recSpDisc=round((row[db.sm_invoice_head.sp_discount.max()]/invNet*collectAmt),2)
            
#             recTp=round((invTpAmt*collectAmt)/invTotal,2)
#             recVat=round((invVatAmt*collectAmt)/invTotal,2)
#             recDisc=round((invDiscAmt*collectAmt)/invTotal,2)
#             recSpDisc=round((invSpDiscAmt*collectAmt)/invTotal,2)
            
#             recTp=round(collectAmt*(percentTp/100),2)
#             recVat=round(collectAmt*(percentVat/100),2)
#             recDisc=round(collectAmt*(percentDisc/100),2)
#             recSpDisc=round(collectAmt*(percentSpDisc/100),2)
            
        else:
            recTp=0
            recVat=0
            recDisc=0
            recSpDisc=0
            
        recTpAmt+=recTp
        recVatAmt+=recVat
        recDiscAmt+=recDisc
        recSpDiscAmt+=recSpDisc
        
        collection_date=row.sm_payment_collection.collection_date
        payment_collection_date=row.sm_payment_collection.payment_collection_date
        collection_batch=row.sm_payment_collection.collection_batch
        
        #------------------------        
        myString+=str(sl)+','+str(invoice_date)+','+str(shipment_no)+','+str(invSl)+','+str(payment_mode)+','+str(credit_note)+','+str(client_id)+','+str(client_name)+','+str(area_id)+','+str(market_name)+','+str(rep_id)+','+str(rep_name)+','+str(d_man_id)+','+str(d_man_name)+','+str(invTpAmt)+','+\
        str(invVatAmt)+','+str(invDiscAmt)+','+str(invSpDiscAmt)+','+str(invTotal)+','+str(adjust_amount)+','+str(recTp)+','+str(recVat)+','+str(recDisc)+','+str(recSpDisc)+','+str(collectAmt)+','+\
        str(collection_date)+','+str(collection_batch)+','+str(payment_collection_date)+'\n'
        
    myString+='\n\nSummary,,,,,,,,,,,,,,,,,,,,\n'    
    myString+='Invoice TP,'+str(round(InvTotalTpAmt,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Invoice VAT,'+str(round(InvTotalVatAmt,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Invoice Discount,'+str(round(InvTotalDiscAmt,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Invoice SP.Disc,'+str(round(InvTotalSpDiscAmt,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Invoice Net,'+str(round(InvTotalNetAmt,2))+',,,,,,,,,,,,,,,,,,,\n\n'
    
    myString+='Received TP,'+str(round(recTpAmt,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Received VAT,'+str(round(recVatAmt,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Received Discount,'+str(round(recDiscAmt,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Received SP.Disc,'+str(round(recSpDiscAmt,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Received Net,'+str(round(recTotal,2))+',,,,,,,,,,,,,,,,,,,\n\n'
    
    myString+='Adjustment,'+str(round(InvTotalAdjust,2))+',,,,,,,,,,,,,,,,,,,\n'
    
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_collInvAndReceipt.csv'   
    return str(myString)


def collInvAndReceipt_asOfDate():
    c_id=session.cid
    
    response.title='Received Summary (As Of Date)'
    
    toDate=request.vars.toDate
    
    depot_id=str(request.vars.depotID).strip()
    store_id=str(request.vars.storeID).strip()
    out_st_delivery_man_id=str(request.vars.deliveryManID).strip()
    out_st_territory_id=str(request.vars.territoryID).strip()
    out_st_mso_id=str(request.vars.msoID).strip()
    invoice_term=str(request.vars.invoice_term).strip()
    customerId=str(request.vars.customerId).strip()
    
    credit_type=str(request.vars.credit_type).strip()
    customer_cat=str(request.vars.customer_cat).strip() 
    customer_sub_cat=str(request.vars.customer_sub_cat).strip()  
    
    out_st_level1_id=str(request.vars.out_st_level1_id).strip()  
    out_st_level2_id=str(request.vars.out_st_level2_id).strip()  
    
    catName=''
    custCatRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_CATEGORY')&(db.sm_category_type.cat_type_id==customer_cat)).select(db.sm_category_type.cat_type_name, limitby=(0,1))
    if custCatRows:
        catName=custCatRows[0].cat_type_name        
    subCatName=''
    custSubCatRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_SUB_CATEGORY')&(db.sm_category_type.cat_type_id==customer_sub_cat)).select(db.sm_category_type.cat_type_name, limitby=(0,1))
    if custSubCatRows:
        subCatName=custSubCatRows[0].cat_type_name
        
    depot_name=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depot_name=depotRow[0].name
        
    store_name=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        store_name=storeRow[0].store_name
        
    out_st_delivery_man_name=''
    dpRow=db((db.sm_delivery_man.cid==c_id)&(db.sm_delivery_man.depot_id==depot_id)&(db.sm_delivery_man.d_man_id==out_st_delivery_man_id)).select(db.sm_delivery_man.name,limitby=(0,1))
    if dpRow:
        out_st_delivery_man_name=dpRow[0].name
        
    out_st_territory_name=''
    levelRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==out_st_territory_id)).select(db.sm_level.level_name,limitby=(0,1))
    if levelRow:
        out_st_territory_name=levelRow[0].level_name
        
    out_st_mso_name=''
    repRow=db((db.sm_rep.cid==c_id)&(db.sm_rep.rep_id==out_st_mso_id)).select(db.sm_rep.name,limitby=(0,1))
    if repRow:
        out_st_mso_name=repRow[0].name
        
    customerName=''
    clientRow=db((db.sm_client.cid==c_id)&(db.sm_client.depot_id==depot_id)&(db.sm_client.client_id==customerId)).select(db.sm_client.name,limitby=(0,1))
    if clientRow:
        customerName=clientRow[0].name
    
    startDt=''
    try:        
        endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d').strftime('%Y-%m-%d')
    except:
        endDt=''
        
    #--------------    
    condStr="(a.cid = '"+c_id+"') AND (a.depot_id='"+depot_id+"') AND (a.store_id='"+store_id+"') AND (a.collection_date <= '"+str(endDt)+"')"
    
    if out_st_delivery_man_id!='':
        condStr+=" AND (a.d_man_id='"+out_st_delivery_man_id+"')"        
    if out_st_territory_id!='':
        condStr+=" AND (a.area_id='"+out_st_territory_id+"')"        
    if out_st_mso_id!='':
        condStr+=" AND (a.rep_id='"+out_st_mso_id+"')"        
    if invoice_term!='':
        condStr+=" AND (a.payment_mode='"+invoice_term+"')"
    if customerId!='':
        condStr+=" AND (a.client_id='"+customerId+"')"
        
    if credit_type!='':
        condStr+=" AND (a.credit_note='"+credit_type+"')"
    if customer_cat!='':
        condStr+=" AND (a.cl_category_id='"+customer_cat+"')"
    if customer_sub_cat!='':
        condStr+=" AND (a.cl_sub_category_id='"+customer_sub_cat+"')"
        
    if out_st_level1_id!='':
        condStr+=" AND (a.level1_id='"+out_st_level1_id+"')"        
    if out_st_level2_id!='':
        condStr+=" AND (a.level2_id='"+out_st_level2_id+"')"
        
    condStr+=" AND (b.cid = '"+c_id+"')"
    condStr+=" AND (b.depot_id='"+depot_id+"')"
    condStr+=" AND (b.id=a.head_rowid)"
    
    paymentRecords="SELECT a.depot_id,a.store_id,ROUND(SUM(b.actual_total_tp/b.total_amount*a.collection_amount),2) as tp_amt,ROUND(SUM(b.vat_total_amount/b.total_amount*a.collection_amount),2) as vat_amt,ROUND(SUM(b.discount/b.total_amount*a.collection_amount),2) as disc_amt,ROUND(SUM(b.sp_discount/b.total_amount*a.collection_amount),2) as spdisc_amt, ROUND(SUM(a.collection_amount),2) as collection_amount from sm_payment_collection a,sm_invoice_head b WHERE ("+str(condStr)+") GROUP BY a.store_id"
    paymentRecordList=db.executesql(paymentRecords,as_dict = True)
    
    
    #====================
    payNet=0
    payTp=0
    payVat=0
    payDisc=0
    paySpDisc=0
    payAdjust=0
    
    for k in range(len(paymentRecordList)):        
        payNet=paymentRecordList[k]['collection_amount']
        payTp=paymentRecordList[k]['tp_amt']
        payVat=paymentRecordList[k]['vat_amt']
        payDisc=paymentRecordList[k]['disc_amt']
        paySpDisc=paymentRecordList[k]['spdisc_amt']
#         payAdjust=paymentRecordList[k]['adjust_amount']
        break
        
    return dict(payNet=payNet,payTp=payTp,payVat=payVat,payDisc=payDisc,paySpDisc=paySpDisc,payAdjust=payAdjust,toDate=endDt,depotID=depot_id,depotName=depot_name,storeID=store_id,storeName=store_name,deliveryManID=out_st_delivery_man_id,deliveryManName=out_st_delivery_man_name,territoryID=out_st_territory_id,territoryName=out_st_territory_name,msoID=out_st_mso_id,msoName=out_st_mso_name,invoice_term=invoice_term,customerId=customerId,customerName=customerName,credit_type=credit_type,customer_cat=customer_cat,customer_sub_cat=customer_sub_cat,catName=catName,subCatName=subCatName,out_st_level1_id=out_st_level1_id,out_st_level2_id=out_st_level2_id)    
    
def sales_summary_asOfDate():
    c_id=session.cid
    
    response.title='Sales Summary (As Of Date)'
    
    toDate=request.vars.toDate
    
    depot_id=str(request.vars.depotID).strip()
    store_id=str(request.vars.storeID).strip()
    out_st_delivery_man_id=str(request.vars.deliveryManID).strip()
    out_st_territory_id=str(request.vars.territoryID).strip()
    out_st_mso_id=str(request.vars.msoID).strip()
    invoice_term=str(request.vars.invoice_term).strip()
    customerId=str(request.vars.customerId).strip()
    
    credit_type=str(request.vars.credit_type).strip()
    customer_cat=str(request.vars.customer_cat).strip() 
    customer_sub_cat=str(request.vars.customer_sub_cat).strip()  
    
    out_st_level1_id=str(request.vars.out_st_level1_id).strip()  
    out_st_level2_id=str(request.vars.out_st_level2_id).strip()  
    
    catName=''
    custCatRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_CATEGORY')&(db.sm_category_type.cat_type_id==customer_cat)).select(db.sm_category_type.cat_type_name, limitby=(0,1))
    if custCatRows:
        catName=custCatRows[0].cat_type_name        
    subCatName=''
    custSubCatRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_SUB_CATEGORY')&(db.sm_category_type.cat_type_id==customer_sub_cat)).select(db.sm_category_type.cat_type_name, limitby=(0,1))
    if custSubCatRows:
        subCatName=custSubCatRows[0].cat_type_name
        
    depot_name=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depot_name=depotRow[0].name
        
    store_name=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        store_name=storeRow[0].store_name
        
    out_st_delivery_man_name=''
    dpRow=db((db.sm_delivery_man.cid==c_id)&(db.sm_delivery_man.depot_id==depot_id)&(db.sm_delivery_man.d_man_id==out_st_delivery_man_id)).select(db.sm_delivery_man.name,limitby=(0,1))
    if dpRow:
        out_st_delivery_man_name=dpRow[0].name
        
    out_st_territory_name=''
    levelRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==out_st_territory_id)).select(db.sm_level.level_name,limitby=(0,1))
    if levelRow:
        out_st_territory_name=levelRow[0].level_name
        
    out_st_mso_name=''
    repRow=db((db.sm_rep.cid==c_id)&(db.sm_rep.rep_id==out_st_mso_id)).select(db.sm_rep.name,limitby=(0,1))
    if repRow:
        out_st_mso_name=repRow[0].name
        
    customerName=''
    clientRow=db((db.sm_client.cid==c_id)&(db.sm_client.depot_id==depot_id)&(db.sm_client.client_id==customerId)).select(db.sm_client.name,limitby=(0,1))
    if clientRow:
        customerName=clientRow[0].name
    
    startDt=''
    try:        
        endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d').strftime('%Y-%m-%d')
    except:
        endDt=''
        
    #--------------
    
    condStr="(cid = '"+c_id+"') AND (depot_id='"+depot_id+"') AND (store_id='"+store_id+"') AND (transaction_date <= '"+str(endDt)+"')"
    
    if out_st_delivery_man_id!='':
        condStr+=" AND (d_man_id='"+out_st_delivery_man_id+"')"        
    if out_st_territory_id!='':
        condStr+=" AND (area_id='"+out_st_territory_id+"')"        
    if out_st_mso_id!='':
        condStr+=" AND (rep_id='"+out_st_mso_id+"')"        
    if invoice_term!='':
        condStr+=" AND (payment_mode='"+invoice_term+"')"
    if customerId!='':
        condStr+=" AND (client_id='"+customerId+"')"
        
    if credit_type!='':
        condStr+=" AND (credit_note='"+credit_type+"')"
    if customer_cat!='':
        condStr+=" AND (cl_category_id='"+customer_cat+"')"
    if customer_sub_cat!='':
        condStr+=" AND (cl_sub_category_id='"+customer_sub_cat+"')"
        
    if out_st_level1_id!='':
        condStr+=" AND (level1_id='"+out_st_level1_id+"')"        
    if out_st_level2_id!='':
        condStr+=" AND (level2_id='"+out_st_level2_id+"')"
        
    invoiceRecords="SELECT depot_id,store_id,ROUND(SUM(trans_net_amt),2) as trans_net_amt, ROUND(SUM( tp_amt ),2) as tp_amt , ROUND(SUM( vat_amt ),2) as vat_amt , ROUND(SUM( disc_amt ),2) as disc_amt , ROUND(SUM( spdisc_amt ),2) as spdisc_amt , ROUND(SUM( adjust_amount ),2) as adjust_amount from sm_rpt_transaction WHERE ("+str(condStr)+" AND transaction_type ='INV') GROUP BY depot_id"
    invoiceRecordList=db.executesql(invoiceRecords,as_dict = True)
    
    returnRecords="SELECT depot_id,store_id,ROUND(SUM(trans_net_amt),2) as trans_net_amt, ROUND(SUM( tp_amt ),2) as tp_amt , ROUND(SUM( vat_amt ),2) as vat_amt , ROUND(SUM( disc_amt ),2) as disc_amt , ROUND(SUM( spdisc_amt ),2) as spdisc_amt , ROUND(SUM( adjust_amount ),2) as adjust_amount from sm_rpt_transaction WHERE ("+str(condStr)+" AND transaction_type like('RE%')) GROUP BY depot_id"
    returnRecordList=db.executesql(returnRecords,as_dict = True)
    
    #====================
    invoiceNet=0
    invoiceTp=0
    invoiceVat=0
    invoiceDisc=0
    invoiceSpDisc=0
    
    retNet=0
    retTp=0
    retVat=0
    retDisc=0
    retSpDisc=0
    
    for i in range(len(invoiceRecordList)):        
        invoiceNet=invoiceRecordList[i]['trans_net_amt']
        invoiceTp=invoiceRecordList[i]['tp_amt']
        invoiceVat=invoiceRecordList[i]['vat_amt']
        invoiceDisc=invoiceRecordList[i]['disc_amt']
        invoiceSpDisc=invoiceRecordList[i]['spdisc_amt']
        break
    
    for j in range(len(returnRecordList)):        
        retNet=returnRecordList[j]['trans_net_amt']
        retTp=returnRecordList[j]['tp_amt']
        retVat=returnRecordList[j]['vat_amt']
        retDisc=returnRecordList[j]['disc_amt']
        retSpDisc=returnRecordList[j]['spdisc_amt']
        break
        
    return dict(invoiceNet=invoiceNet,invoiceTp=invoiceTp,invoiceVat=invoiceVat,invoiceDisc=invoiceDisc,invoiceSpDisc=invoiceSpDisc,retNet=retNet,retTp=retTp,retVat=retVat,retDisc=retDisc,retSpDisc=retSpDisc,toDate=endDt,depotID=depot_id,depotName=depot_name,storeID=store_id,storeName=store_name,deliveryManID=out_st_delivery_man_id,deliveryManName=out_st_delivery_man_name,territoryID=out_st_territory_id,territoryName=out_st_territory_name,msoID=out_st_mso_id,msoName=out_st_mso_name,invoice_term=invoice_term,customerId=customerId,customerName=customerName,credit_type=credit_type,customer_cat=customer_cat,customer_sub_cat=customer_sub_cat,catName=catName,subCatName=subCatName,out_st_level1_id=out_st_level1_id,out_st_level2_id=out_st_level2_id)    
    
def collInvAndReceipt_backPercent():
    c_id=session.cid
    
    response.title='7.01 Invoice and Receipt'
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate    
    
    depot_id=str(request.vars.depotID).strip()
    store_id=str(request.vars.storeID).strip()    
    delivery_man_id=str(request.vars.deliveryManID).strip()  
    territory_id=str(request.vars.territoryID).strip()    
    mso_id=str(request.vars.msoID).strip()
    
    coll_inv_term=str(request.vars.coll_inv_term).strip()  
    coll_credit_type=str(request.vars.coll_credit_type).strip()  
    coll_payment_mode=str(request.vars.coll_payment_mode).strip()  
    
    try:
        coll_inv_sl_from=int(request.vars.coll_inv_sl_from)
        coll_inv_sl_to=int(request.vars.coll_inv_sl_to)
    except:
        coll_inv_sl_from=''
        coll_inv_sl_to=''
    
    try:
        coll_batchno=int(request.vars.coll_batchno)
    except:
        coll_batchno=''
        
    coll_customer_cat=str(request.vars.coll_customer_cat).strip() 
    coll_customer_sub_cat=str(request.vars.coll_customer_sub_cat).strip()    
    catName=''
    custCatRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_CATEGORY')&(db.sm_category_type.cat_type_id==coll_customer_cat)).select(db.sm_category_type.cat_type_name, limitby=(0,1))
    if custCatRows:
        catName=custCatRows[0].cat_type_name        
    subCatName=''
    custSubCatRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_SUB_CATEGORY')&(db.sm_category_type.cat_type_id==coll_customer_sub_cat)).select(db.sm_category_type.cat_type_name, limitby=(0,1))
    if custSubCatRows:
        subCatName=custSubCatRows[0].cat_type_name
        
    depot_name=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depot_name=depotRow[0].name
        
    store_name=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        store_name=storeRow[0].store_name
        
    delivery_man_name=''
    dpRow=db((db.sm_delivery_man.cid==c_id)&(db.sm_delivery_man.depot_id==depot_id)&(db.sm_delivery_man.d_man_id==delivery_man_id)).select(db.sm_delivery_man.name,limitby=(0,1))
    if dpRow:
        delivery_man_name=dpRow[0].name
        
    territory_name=''
    levelRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==territory_id)).select(db.sm_level.level_name,limitby=(0,1))
    if levelRow:
        territory_name=levelRow[0].level_name
        
    mso_name=''
    repRow=db((db.sm_rep.cid==c_id)&(db.sm_rep.rep_id==mso_id)).select(db.sm_rep.name,limitby=(0,1))
    if repRow:
        mso_name=repRow[0].name
        
    startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d').strftime('%Y-%m-%d')    
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d').strftime('%Y-%m-%d')
    
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    
    transactionCause=['','COLLECTION ERROR','ENTRY ERROR']
    
    qset=db()
    qset=qset(db.sm_payment_collection.cid==c_id)
    qset=qset(db.sm_payment_collection.depot_id==depot_id)
    qset=qset(db.sm_payment_collection.store_id==store_id)
    if coll_inv_sl_from!='' and coll_inv_sl_to!='':
        qset=qset((db.sm_payment_collection.sl>=coll_inv_sl_from)&(db.sm_payment_collection.sl<=coll_inv_sl_to))
    else:        
        #qset=qset((db.sm_payment_collection.payment_collection_date>=startDt)&(db.sm_payment_collection.payment_collection_date<=endDt))
        qset=qset((db.sm_payment_collection.collection_date>=startDt)&(db.sm_payment_collection.collection_date<=endDt))
    qset=qset(db.sm_payment_collection.status=='Posted')
    qset=qset(db.sm_payment_collection.transaction_cause.belongs(transactionCause))
    
    if delivery_man_id!='':
        qset=qset(db.sm_payment_collection.d_man_id==delivery_man_id)
    if territory_id!='':
        qset=qset(db.sm_payment_collection.area_id==territory_id)
    if mso_id!='':
        qset=qset(db.sm_payment_collection.rep_id==mso_id)
         
    if coll_inv_term!='':
        qset=qset(db.sm_payment_collection.payment_mode==coll_inv_term)
    if coll_credit_type!='':
        qset=qset(db.sm_payment_collection.credit_note==coll_credit_type)
    if coll_payment_mode!='':
        qset=qset(db.sm_payment_collection.payment_type==coll_payment_mode)
    if coll_customer_cat!='':
        qset=qset(db.sm_payment_collection.cl_category_id==coll_customer_cat)
    if coll_customer_sub_cat!='':
        qset=qset(db.sm_payment_collection.cl_sub_category_id==coll_customer_sub_cat)
        
    if coll_batchno!='':
        qset=qset(db.sm_payment_collection.collection_batch==coll_batchno)
    
    qset=qset(db.sm_invoice_head.cid==c_id)
    qset=qset(db.sm_invoice_head.depot_id==depot_id)
    qset=qset(db.sm_payment_collection.head_rowid==db.sm_invoice_head.id)
    
    records=qset.select(db.sm_invoice_head.id,db.sm_invoice_head.depot_id,db.sm_invoice_head.sl,db.sm_invoice_head.invoice_date.max(),db.sm_invoice_head.shipment_no.max(),db.sm_invoice_head.payment_mode.max(),db.sm_invoice_head.credit_note.max(),db.sm_invoice_head.client_id.max(),db.sm_invoice_head.client_name.max(),db.sm_invoice_head.area_id.max(),db.sm_invoice_head.market_name.max(),db.sm_invoice_head.rep_id.max(),db.sm_invoice_head.rep_name.max(),db.sm_invoice_head.d_man_id.max(),db.sm_invoice_head.d_man_name.max(),db.sm_invoice_head.adjust_amount.max(),db.sm_invoice_head.actual_total_tp.max(),db.sm_invoice_head.vat_total_amount.max(),db.sm_invoice_head.discount.max(),db.sm_invoice_head.sp_discount.max(),db.sm_invoice_head.return_tp.max(),db.sm_invoice_head.return_vat.max(),db.sm_invoice_head.return_discount.max(),db.sm_invoice_head.return_sp_discount.max(),db.sm_payment_collection.payment_collection_date,db.sm_payment_collection.collection_batch,db.sm_payment_collection.collection_amount.sum(),orderby=db.sm_invoice_head.id|db.sm_payment_collection.payment_collection_date,groupby=db.sm_invoice_head.id|db.sm_invoice_head.depot_id|db.sm_invoice_head.sl|db.sm_payment_collection.payment_collection_date|db.sm_payment_collection.collection_batch)
    
    recTotal=0
    recRows=qset.select(db.sm_payment_collection.cid,db.sm_payment_collection.collection_amount.sum(),groupby=db.sm_payment_collection.cid)
    for recRow in recRows:
        recTotal=recRow[db.sm_payment_collection.collection_amount.sum()]
        
    InvTotalTp=0
    InvTotalVat=0
    InvTotalDisc=0
    InvTotalSp=0
    InvTotalNet=0
    InvTotalAdjust=0
    
    retTotalTp=0
    retTotalVat=0
    retTotalDisc=0
    retTotalSpDisc=0
    retTotal=0
    
    invRows=qset.select(db.sm_invoice_head.id,db.sm_invoice_head.actual_total_tp.max(),db.sm_invoice_head.total_amount.max(),db.sm_invoice_head.vat_total_amount.max(),db.sm_invoice_head.discount.max(),db.sm_invoice_head.sp_discount.max(),db.sm_invoice_head.return_tp.max(),db.sm_invoice_head.return_vat.max(),db.sm_invoice_head.return_discount.max(),db.sm_invoice_head.return_sp_discount.max(),db.sm_invoice_head.adjust_amount.max(),groupby=db.sm_invoice_head.id)
    for invRow in invRows:
        actual_total_tp=invRow[db.sm_invoice_head.actual_total_tp.max()]       
        #total_amount=invRow.total_amount
        vat_total_amount=invRow[db.sm_invoice_head.vat_total_amount.max()]
        total_discount=invRow[db.sm_invoice_head.discount.max()]
        total_sp_discount=invRow[db.sm_invoice_head.sp_discount.max()]
        
        return_tp=invRow[db.sm_invoice_head.return_tp.max()]
        return_vat=invRow[db.sm_invoice_head.return_vat.max()]
        return_discount=invRow[db.sm_invoice_head.return_discount.max()]
        return_sp_discount=invRow[db.sm_invoice_head.return_sp_discount.max()]
        
        adjust_amount=invRow[db.sm_invoice_head.adjust_amount.max()]
        
        return_amt=return_tp+return_vat-return_discount
        
        retTotalTp+=return_tp+return_sp_discount
        retTotalVat+=return_vat
        retTotalDisc+=return_discount
        retTotalSpDisc+=return_sp_discount
        
        #retTotal+=return_amt
        
        #InvTotalTp+=total_amount-vat_total_amount+total_discount
        InvTotalTp+=actual_total_tp        
        InvTotalVat+=vat_total_amount
        InvTotalDisc+=total_discount
        InvTotalSp+=total_sp_discount
        
        #InvTotalNet+=total_amount
        
        InvTotalAdjust+=adjust_amount
        
    InvTotalTpAmt=InvTotalTp-retTotalTp
    InvTotalVatAmt=InvTotalVat-retTotalVat
    InvTotalDiscAmt=InvTotalDisc-retTotalDisc
    InvTotalSpDiscAmt=InvTotalSp-retTotalSpDisc
    
    InvTotalNetAmt=InvTotalTpAmt+InvTotalVatAmt-(InvTotalDiscAmt+InvTotalSpDiscAmt)
    
    if InvTotalNetAmt>0:
        recTpAmt=(InvTotalTpAmt*recTotal)/InvTotalNetAmt
        recVatAmt=(InvTotalVatAmt*recTotal)/InvTotalNetAmt
        recDiscAmt=(InvTotalDiscAmt*recTotal)/InvTotalNetAmt
        recSpDiscAmt=(InvTotalSpDiscAmt*recTotal)/InvTotalNetAmt
    else:
        recTpAmt=0
        recVatAmt=0
        recDiscAmt=0
        recSpDiscAmt=0
        
    #=============================
    p_totalInvTP=InvTotalTpAmt
    p_totalInvVat=InvTotalVatAmt
    p_totalInvDisc=InvTotalDiscAmt
    p_totalInvSp=InvTotalSpDiscAmt
    p_totalInvAmt=InvTotalNetAmt
    
    percentTp=0
    percentVat=0
    percentDisc=0
    percentSpDisc=0
    try:
        percentTp=p_totalInvTP/p_totalInvAmt*100
        percentVat=p_totalInvVat/p_totalInvAmt*100
        percentDisc=p_totalInvDisc/p_totalInvAmt*100
        percentSpDisc=p_totalInvSp/p_totalInvAmt*100
    except:
        percentTp=0
        percentVat=0
        percentDisc=0
        percentSpDisc=0
    #========================
    
    return dict(percentTp=percentTp,percentVat=percentVat,percentDisc=percentDisc,percentSpDisc=percentSpDisc,records=records,fromDate=fromDate,toDate=toDate,depotID=depot_id,depotName=depot_name,storeID=store_id,storeName=store_name,deliveryManID=delivery_man_id,deliveryManName=delivery_man_name,territoryID=territory_id,territoryName=territory_name,msoID=mso_id,msoName=mso_name,InvTotalNetAmt=InvTotalNetAmt,InvTotalDiscAmt=InvTotalDiscAmt,InvTotalVatAmt=InvTotalVatAmt,InvTotalTpAmt=InvTotalTpAmt,InvTotalSp=InvTotalSp,recTotal=recTotal,recTpAmt=recTpAmt,recVatAmt=recVatAmt,recDiscAmt=recDiscAmt,recSpDiscAmt=recSpDiscAmt,InvTotalSpDiscAmt=InvTotalSpDiscAmt,InvTotalAdjust=InvTotalAdjust,coll_inv_sl_from=coll_inv_sl_from,coll_inv_sl_to=coll_inv_sl_to,coll_inv_term=coll_inv_term,coll_credit_type=coll_credit_type,coll_payment_mode=coll_payment_mode,coll_customer_cat=coll_customer_cat,coll_customer_sub_cat=coll_customer_sub_cat,catName=catName,subCatName=subCatName,coll_batchno=coll_batchno,page=page,items_per_page=items_per_page)    
    
def collInvAndReceipt_download_backPercent():
    c_id=session.cid
    
    response.title='7.01 Downlaod - Invoice and Receipt'
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate    
    
    depot_id=str(request.vars.depotID).strip()
    store_id=str(request.vars.storeID).strip()    
    delivery_man_id=str(request.vars.deliveryManID).strip()  
    territory_id=str(request.vars.territoryID).strip()    
    mso_id=str(request.vars.msoID).strip()
    
    coll_inv_term=str(request.vars.coll_inv_term).strip()  
    coll_credit_type=str(request.vars.coll_credit_type).strip()  
    coll_payment_mode=str(request.vars.coll_payment_mode).strip()  
    
    try:
        coll_inv_sl_from=int(request.vars.coll_inv_sl_from)
        coll_inv_sl_to=int(request.vars.coll_inv_sl_to)
    except:
        coll_inv_sl_from=''
        coll_inv_sl_to=''
        
    try:
        coll_batchno=int(request.vars.coll_batchno)
    except:
        coll_batchno=''
        
    coll_customer_cat=str(request.vars.coll_customer_cat).strip() 
    coll_customer_sub_cat=str(request.vars.coll_customer_sub_cat).strip()    
    catName=''
    custCatRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_CATEGORY')&(db.sm_category_type.cat_type_id==coll_customer_cat)).select(db.sm_category_type.cat_type_name, limitby=(0,1))
    if custCatRows:
        catName=custCatRows[0].cat_type_name        
    subCatName=''
    custSubCatRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_SUB_CATEGORY')&(db.sm_category_type.cat_type_id==coll_customer_sub_cat)).select(db.sm_category_type.cat_type_name, limitby=(0,1))
    if custSubCatRows:
        subCatName=custSubCatRows[0].cat_type_name
    
    depot_name=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depot_name=depotRow[0].name
    
    store_name=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        store_name=storeRow[0].store_name
        
    delivery_man_name=''
    dpRow=db((db.sm_delivery_man.cid==c_id)&(db.sm_delivery_man.depot_id==depot_id)&(db.sm_delivery_man.d_man_id==delivery_man_id)).select(db.sm_delivery_man.name,limitby=(0,1))
    if dpRow:
        delivery_man_name=dpRow[0].name
        
    territory_name=''
    levelRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==territory_id)).select(db.sm_level.level_name,limitby=(0,1))
    if levelRow:
        territory_name=levelRow[0].level_name
         
    mso_name=''
    repRow=db((db.sm_rep.cid==c_id)&(db.sm_rep.rep_id==mso_id)).select(db.sm_rep.name,limitby=(0,1))
    if repRow:
        mso_name=repRow[0].name
        
    startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d').strftime('%Y-%m-%d')    
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d').strftime('%Y-%m-%d')
    
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    
    #dateRecords="SELECT a.invoice_date,a.sl, a.client_id, a.client_name, a.area_id,a.market_name, a.discount, a.vat_total_amount, a.total_amount,a.adjust_amount,b.collection_amount,b.collection_date FROM sm_invoice_head a LEFT OUTER JOIN sm_payment_collection b ON a.sl=b.sl where a.cid = '"+c_id+"' and a.invoice_date >= '"+str(startDt)+"' and a.invoice_date <= '"+str(endDt)+"' and a.depot_id = '"+depot_id+"' and a.store_id = '"+store_id+"' and a.status = 'Invoiced' and a.sl !=0 ORDER BY a.sl"
    #records=db.executesql(dateRecords,as_dict = True)    
    
    transactionCause=['','COLLECTION ERROR','ENTRY ERROR']
    
    qset=db()
    qset=qset(db.sm_payment_collection.cid==c_id)
    qset=qset(db.sm_payment_collection.depot_id==depot_id)
    qset=qset(db.sm_payment_collection.store_id==store_id)
    if coll_inv_sl_from!='' and coll_inv_sl_to!='':
        qset=qset((db.sm_payment_collection.sl>=coll_inv_sl_from)&(db.sm_payment_collection.sl<=coll_inv_sl_to))
    else:        
        qset=qset((db.sm_payment_collection.payment_collection_date>=startDt)&(db.sm_payment_collection.payment_collection_date<=endDt))
        
    qset=qset(db.sm_payment_collection.status=='Posted')
    #qset=qset(db.sm_payment_collection.transaction_type=='Payment')
    qset=qset(db.sm_payment_collection.transaction_cause.belongs(transactionCause))
    
    if delivery_man_id!='':
        qset=qset(db.sm_payment_collection.d_man_id==delivery_man_id)
    if territory_id!='':
        qset=qset(db.sm_payment_collection.area_id==territory_id)
    if mso_id!='':
        qset=qset(db.sm_payment_collection.rep_id==mso_id)
        
    if coll_inv_term!='':
        qset=qset(db.sm_payment_collection.payment_mode==coll_inv_term)
    if coll_credit_type!='':
        qset=qset(db.sm_payment_collection.credit_note==coll_credit_type)
    if coll_payment_mode!='':
        qset=qset(db.sm_payment_collection.payment_type==coll_payment_mode)
    if coll_customer_cat!='':
        qset=qset(db.sm_payment_collection.cl_category_id==coll_customer_cat)
    if coll_customer_sub_cat!='':
        qset=qset(db.sm_payment_collection.cl_sub_category_id==coll_customer_sub_cat)
    
    if coll_batchno!='':
        qset=qset(db.sm_payment_collection.collection_batch==coll_batchno)
    
    qset=qset(db.sm_invoice_head.cid==c_id)
    qset=qset(db.sm_invoice_head.depot_id==depot_id)
    qset=qset(db.sm_payment_collection.head_rowid==db.sm_invoice_head.id)
    
    records=qset.select(db.sm_invoice_head.id,db.sm_invoice_head.depot_id,db.sm_invoice_head.sl,db.sm_invoice_head.invoice_date.max(),db.sm_invoice_head.shipment_no.max(),db.sm_invoice_head.payment_mode.max(),db.sm_invoice_head.credit_note.max(),db.sm_invoice_head.client_id.max(),db.sm_invoice_head.client_name.max(),db.sm_invoice_head.area_id.max(),db.sm_invoice_head.market_name.max(),db.sm_invoice_head.rep_id.max(),db.sm_invoice_head.rep_name.max(),db.sm_invoice_head.d_man_id.max(),db.sm_invoice_head.d_man_name.max(),db.sm_invoice_head.adjust_amount.max(),db.sm_invoice_head.actual_total_tp.max(),db.sm_invoice_head.vat_total_amount.max(),db.sm_invoice_head.discount.max(),db.sm_invoice_head.sp_discount.max(),db.sm_invoice_head.return_tp.max(),db.sm_invoice_head.return_vat.max(),db.sm_invoice_head.return_discount.max(),db.sm_invoice_head.return_sp_discount.max(),db.sm_payment_collection.payment_collection_date,db.sm_payment_collection.collection_batch,db.sm_payment_collection.collection_amount.sum(),orderby=db.sm_invoice_head.id|db.sm_payment_collection.payment_collection_date,groupby=db.sm_invoice_head.id|db.sm_invoice_head.depot_id|db.sm_invoice_head.sl|db.sm_payment_collection.payment_collection_date|db.sm_payment_collection.collection_batch)
    
    recTotal=0
    recRows=qset.select(db.sm_payment_collection.cid,db.sm_payment_collection.collection_amount.sum(),groupby=db.sm_payment_collection.cid)
    for recRow in recRows:
        recTotal=recRow[db.sm_payment_collection.collection_amount.sum()]
        
    InvTotalTp=0
    InvTotalVat=0
    InvTotalDisc=0
    InvTotalSp=0
    InvTotalNet=0
    InvTotalAdjust=0
    
    retTotalTp=0
    retTotalVat=0
    retTotalDisc=0
    retTotalSpDisc=0
    retTotal=0
    
    invRows=qset.select(db.sm_invoice_head.id,db.sm_invoice_head.actual_total_tp.max(),db.sm_invoice_head.total_amount.max(),db.sm_invoice_head.vat_total_amount.max(),db.sm_invoice_head.discount.max(),db.sm_invoice_head.sp_discount.max(),db.sm_invoice_head.return_tp.max(),db.sm_invoice_head.return_vat.max(),db.sm_invoice_head.return_discount.max(),db.sm_invoice_head.return_sp_discount.max(),db.sm_invoice_head.adjust_amount.max(),groupby=db.sm_invoice_head.id)
    for invRow in invRows:
        actual_total_tp=invRow[db.sm_invoice_head.actual_total_tp.max()]       
        #total_amount=invRow.total_amount
        vat_total_amount=invRow[db.sm_invoice_head.vat_total_amount.max()]
        total_discount=invRow[db.sm_invoice_head.discount.max()]
        total_sp_discount=invRow[db.sm_invoice_head.sp_discount.max()]
        
        return_tp=invRow[db.sm_invoice_head.return_tp.max()]
        return_vat=invRow[db.sm_invoice_head.return_vat.max()]
        return_discount=invRow[db.sm_invoice_head.return_discount.max()]
        return_sp_discount=invRow[db.sm_invoice_head.return_sp_discount.max()]
        
        adjust_amount=invRow[db.sm_invoice_head.adjust_amount.max()]
        
        return_amt=return_tp+return_vat-return_discount
        
        retTotalTp+=return_tp+return_sp_discount
        retTotalVat+=return_vat
        retTotalDisc+=return_discount
        retTotalSpDisc+=return_sp_discount
        
        #retTotal+=return_amt
        
        #InvTotalTp+=total_amount-vat_total_amount+total_discount
        InvTotalTp+=actual_total_tp        
        InvTotalVat+=vat_total_amount
        InvTotalDisc+=total_discount
        InvTotalSp+=total_sp_discount
        
        #InvTotalNet+=total_amount
        
        InvTotalAdjust+=adjust_amount
        
    InvTotalTpAmt=InvTotalTp-retTotalTp
    InvTotalVatAmt=InvTotalVat-retTotalVat
    InvTotalDiscAmt=InvTotalDisc-retTotalDisc
    InvTotalSpDiscAmt=InvTotalSp-retTotalSpDisc
    
    InvTotalNetAmt=InvTotalTpAmt+InvTotalVatAmt-(InvTotalDiscAmt+InvTotalSpDiscAmt)
    
    recTpAmt=0
    recVatAmt=0
    recDiscAmt=0
    recSpDiscAmt=0
    
    #=============================
    p_totalInvTP=InvTotalTpAmt
    p_totalInvVat=InvTotalVatAmt
    p_totalInvDisc=InvTotalDiscAmt
    p_totalInvSp=InvTotalSpDiscAmt
    p_totalInvAmt=InvTotalNetAmt
    
    percentTp=0
    percentVat=0
    percentDisc=0
    percentSpDisc=0
    try:
        percentTp=p_totalInvTP/p_totalInvAmt*100
        percentVat=p_totalInvVat/p_totalInvAmt*100
        percentDisc=p_totalInvDisc/p_totalInvAmt*100
        percentSpDisc=p_totalInvSp/p_totalInvAmt*100
    except:
        percentTp=0
        percentVat=0
        percentDisc=0
        percentSpDisc=0
    #========================
    
    #-------------
    myString='7.1 Invoice Wise Cash Collection: With Invoice & Receipt Details\n'
    
    if coll_inv_sl_from!='' and coll_inv_sl_to!='':
        myString+='INV.No '+',From:'+str(coll_inv_sl_from)+',To:'+str(coll_inv_sl_to)+'\n'
    else:
        myString+='Rec. Date From:,'+str(startDt)+'\n'            
        myString+='To Date:'+','+str(endDt)+'\n'
    
    myString+='Branch ID:,'+str(depot_id)+'\n'
    myString+='Branch Name'+','+str(depot_name)+'\n'
    myString+='Store ID:,'+str(store_id)+'\n'
    myString+='Store Name'+','+str(store_name)+'\n'
    myString+='DP ID:,'+str(delivery_man_id)+'\n'
    myString+='DP Name'+','+str(delivery_man_name)+'\n'
    myString+='Territory ID:,'+str(territory_id)+'\n'
    myString+='Territory Name'+','+str(territory_name)+'\n'
    myString+='MSO ID:,'+str(mso_id)+'\n'
    myString+='MSO Name'+','+str(mso_name)+'\n'
    
    if coll_inv_term=='':
        coll_inv_term='ALL'
    else:
        if coll_inv_term=='CREDIT':
            if coll_credit_type=='':
                coll_credit_type='ALL'
    if coll_payment_mode=='':
        coll_payment_mode='ALL'    
        
    myString+='Invoice Term:,'+str(coll_inv_term)+'\n'
    myString+='Credit Type:,'+str(coll_credit_type)+'\n'
    myString+='Payment Type:,'+str(coll_payment_mode)+'\n'
    
    if catName=='':
        catName='ALL'
    if subCatName=='':
        subCatName='ALL'        
    myString+='Customer Category'+','+str(catName)+'\n'
    myString+='Customer Sub-Category'+','+str(subCatName)+'\n'
    
    if coll_batchno!='':
        myString+='Batch Number'+',`'+str(coll_batchno)+'\n'
        
    sl=0
    myString+='SL,Inv.Date,ShipNo,Invoice No,InvoiceTerm,CreditType,Cust. ID,Cust. Name,Tr. Code,Market,SPID,SPName,DPID,DPName,INVOICE-TP,INVOICE-Vat,INVOICE-Disc,INVOICE-SP,INVOICE-Net,Adjusted,RECEIVED-TP,RECEIVED-Vat,RECEIVED-Disc,RECEIVED-SP,RECEIVED-Net,Rec.Date,BatchNo'+'\n'
    for row in records:
        sl+=1
        
        invoice_date=row[db.sm_invoice_head.invoice_date.max()] 
        if row.sm_invoice_head.sl==0:
            shipment_no=row[db.sm_invoice_head.shipment_no.max()]
        else:
            shipment_no=str(session.prefix_invoice)+'SH-'+str(row[db.sm_invoice_head.shipment_no.max()])        
        invSl=str(session.prefix_invoice)+'INV'+str(row.sm_invoice_head.depot_id)+'-'+str(row.sm_invoice_head.sl)        
        payment_mode=row[db.sm_invoice_head.payment_mode.max()]
        credit_note=row[db.sm_invoice_head.credit_note.max()]
#         invTermAndCreditType=''
#         if str(payment_mode).upper()=='CASH':
#             invTermAndCreditType=payment_mode
#         else:
#             invTermAndCreditType=credit_note
            
        client_id=row[db.sm_invoice_head.client_id.max()]
        client_name=row[db.sm_invoice_head.client_name.max()]
        area_id=row[db.sm_invoice_head.area_id.max()]
        market_name=row[db.sm_invoice_head.market_name.max()]
        rep_id=row[db.sm_invoice_head.rep_id.max()]
        rep_name=row[db.sm_invoice_head.rep_name.max()]
        d_man_id=row[db.sm_invoice_head.d_man_id.max()]
        d_man_name=row[db.sm_invoice_head.d_man_name.max()]
        
        invTpAmt=round(row[db.sm_invoice_head.actual_total_tp.max()]-(row[db.sm_invoice_head.return_tp.max()]+row[db.sm_invoice_head.return_sp_discount.max()]),2)
        invVatAmt=round(row[db.sm_invoice_head.vat_total_amount.max()]-row[db.sm_invoice_head.return_vat.max()],2)
        invDiscAmt=round(row[db.sm_invoice_head.discount.max()]-row[db.sm_invoice_head.return_discount.max()],2)
        invSpDiscAmt=round(row[db.sm_invoice_head.sp_discount.max()]-row[db.sm_invoice_head.return_sp_discount.max()],2)
        invTotal=invTpAmt+invVatAmt-(invDiscAmt+invSpDiscAmt)
        
        adjust_amount=round(row[db.sm_invoice_head.adjust_amount.max()],2)
        
        collectAmt=round(row[db.sm_payment_collection.collection_amount.sum()],2)
        
        if invTotal>0:
#             recTp=round((invTpAmt*collectAmt)/invTotal,2)
#             recVat=round((invVatAmt*collectAmt)/invTotal,2)
#             recDisc=round((invDiscAmt*collectAmt)/invTotal,2)
#             recSpDisc=round((invSpDiscAmt*collectAmt)/invTotal,2)
            
            recTp=round(collectAmt*(percentTp/100),2)
            recVat=round(collectAmt*(percentVat/100),2)
            recDisc=round(collectAmt*(percentDisc/100),2)
            recSpDisc=round(collectAmt*(percentSpDisc/100),2)
            
        else:
            recTp=0
            recVat=0
            recDisc=0
            recSpDisc=0
            
        recTpAmt+=recTp
        recVatAmt+=recVat
        recDiscAmt+=recDisc
        recSpDiscAmt+=recSpDisc
        
        payment_collection_date=row.sm_payment_collection.payment_collection_date        
        collection_batch=row.sm_payment_collection.collection_batch
        
        #------------------------        
        myString+=str(sl)+','+str(invoice_date)+','+str(shipment_no)+','+str(invSl)+','+str(payment_mode)+','+str(credit_note)+','+str(client_id)+','+str(client_name)+','+str(area_id)+','+str(market_name)+','+str(rep_id)+','+str(rep_name)+','+str(d_man_id)+','+str(d_man_name)+','+str(invTpAmt)+','+\
        str(invVatAmt)+','+str(invDiscAmt)+','+str(invSpDiscAmt)+','+str(invTotal)+','+str(adjust_amount)+','+str(recTp)+','+str(recVat)+','+str(recDisc)+','+str(recSpDisc)+','+str(collectAmt)+','+\
        str(payment_collection_date)+','+str(collection_batch)+'\n'
        
    myString+='\n\nSummary,,,,,,,,,,,,,,,,,,,,\n'    
    myString+='Invoice TP,'+str(round(InvTotalTpAmt,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Invoice VAT,'+str(round(InvTotalVatAmt,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Invoice Discount,'+str(round(InvTotalDiscAmt,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Invoice SP.Disc,'+str(round(InvTotalSpDiscAmt,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Invoice Net,'+str(round(InvTotalNetAmt,2))+',,,,,,,,,,,,,,,,,,,\n\n'
    
    myString+='Received TP,'+str(round(recTpAmt,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Received VAT,'+str(round(recVatAmt,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Received Discount,'+str(round(recDiscAmt,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Received SP.Disc,'+str(round(recSpDiscAmt,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Received Net,'+str(round(recTotal,2))+',,,,,,,,,,,,,,,,,,,\n\n'
    
    myString+='Adjustment,'+str(round(InvTotalAdjust,2))+',,,,,,,,,,,,,,,,,,,\n'
    
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_collInvAndReceipt.csv'   
    return str(myString)


def collInvAndReceipt_bak():
    c_id=session.cid
    
    response.title='7.01 Invoice and Receipt'
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate    
    
    depot_id=str(request.vars.depotID).strip()
    store_id=str(request.vars.storeID).strip()    
    delivery_man_id=str(request.vars.deliveryManID).strip()  
    territory_id=str(request.vars.territoryID).strip()    
    mso_id=str(request.vars.msoID).strip()
    
    coll_inv_term=str(request.vars.coll_inv_term).strip()  
    coll_credit_type=str(request.vars.coll_credit_type).strip()  
    coll_payment_mode=str(request.vars.coll_payment_mode).strip()  
    
    try:
        coll_inv_sl_from=int(request.vars.coll_inv_sl_from)
        coll_inv_sl_to=int(request.vars.coll_inv_sl_to)
    except:
        coll_inv_sl_from=''
        coll_inv_sl_to=''
    
    try:
        coll_batchno=int(request.vars.coll_batchno)
    except:
        coll_batchno=''
        
    coll_customer_cat=str(request.vars.coll_customer_cat).strip() 
    coll_customer_sub_cat=str(request.vars.coll_customer_sub_cat).strip()    
    catName=''
    custCatRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_CATEGORY')&(db.sm_category_type.cat_type_id==coll_customer_cat)).select(db.sm_category_type.cat_type_name, limitby=(0,1))
    if custCatRows:
        catName=custCatRows[0].cat_type_name        
    subCatName=''
    custSubCatRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_SUB_CATEGORY')&(db.sm_category_type.cat_type_id==coll_customer_sub_cat)).select(db.sm_category_type.cat_type_name, limitby=(0,1))
    if custSubCatRows:
        subCatName=custSubCatRows[0].cat_type_name
        
    depot_name=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depot_name=depotRow[0].name
        
    store_name=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        store_name=storeRow[0].store_name
        
    delivery_man_name=''
    dpRow=db((db.sm_delivery_man.cid==c_id)&(db.sm_delivery_man.depot_id==depot_id)&(db.sm_delivery_man.d_man_id==delivery_man_id)).select(db.sm_delivery_man.name,limitby=(0,1))
    if dpRow:
        delivery_man_name=dpRow[0].name
        
    territory_name=''
    levelRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==territory_id)).select(db.sm_level.level_name,limitby=(0,1))
    if levelRow:
        territory_name=levelRow[0].level_name
        
    mso_name=''
    repRow=db((db.sm_rep.cid==c_id)&(db.sm_rep.rep_id==mso_id)).select(db.sm_rep.name,limitby=(0,1))
    if repRow:
        mso_name=repRow[0].name
        
    startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d').strftime('%Y-%m-%d')    
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d').strftime('%Y-%m-%d')
    
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    
    transactionCause=['','COLLECTION ERROR','ENTRY ERROR']
    
    qset=db()
    qset=qset(db.sm_payment_collection.cid==c_id)
    qset=qset(db.sm_payment_collection.depot_id==depot_id)
    qset=qset(db.sm_payment_collection.store_id==store_id)
    if coll_inv_sl_from!='' and coll_inv_sl_to!='':
        qset=qset((db.sm_payment_collection.sl>=coll_inv_sl_from)&(db.sm_payment_collection.sl<=coll_inv_sl_to))
    else:        
        qset=qset((db.sm_payment_collection.payment_collection_date>=startDt)&(db.sm_payment_collection.payment_collection_date<=endDt))
    qset=qset(db.sm_payment_collection.status=='Posted')
    qset=qset(db.sm_payment_collection.transaction_cause.belongs(transactionCause))
    
    if delivery_man_id!='':
        qset=qset(db.sm_payment_collection.d_man_id==delivery_man_id)
    if territory_id!='':
        qset=qset(db.sm_payment_collection.area_id==territory_id)
    if mso_id!='':
        qset=qset(db.sm_payment_collection.rep_id==mso_id)
         
    if coll_inv_term!='':
        qset=qset(db.sm_payment_collection.payment_mode==coll_inv_term)
    if coll_credit_type!='':
        qset=qset(db.sm_payment_collection.credit_note==coll_credit_type)
    if coll_payment_mode!='':
        qset=qset(db.sm_payment_collection.payment_type==coll_payment_mode)
    if coll_customer_cat!='':
        qset=qset(db.sm_payment_collection.cl_category_id==coll_customer_cat)
    if coll_customer_sub_cat!='':
        qset=qset(db.sm_payment_collection.cl_sub_category_id==coll_customer_sub_cat)
        
    if coll_batchno!='':
        qset=qset(db.sm_payment_collection.collection_batch==coll_batchno)
    
    qset=qset(db.sm_invoice_head.cid==c_id)
    qset=qset(db.sm_invoice_head.depot_id==depot_id)
    qset=qset(db.sm_payment_collection.head_rowid==db.sm_invoice_head.id)
    
    records=qset.select(db.sm_invoice_head.id,db.sm_invoice_head.depot_id,db.sm_invoice_head.sl,db.sm_invoice_head.invoice_date.max(),db.sm_invoice_head.shipment_no.max(),db.sm_invoice_head.payment_mode.max(),db.sm_invoice_head.credit_note.max(),db.sm_invoice_head.client_id.max(),db.sm_invoice_head.client_name.max(),db.sm_invoice_head.area_id.max(),db.sm_invoice_head.market_name.max(),db.sm_invoice_head.rep_id.max(),db.sm_invoice_head.rep_name.max(),db.sm_invoice_head.d_man_id.max(),db.sm_invoice_head.d_man_name.max(),db.sm_invoice_head.adjust_amount.max(),db.sm_invoice_head.actual_total_tp.max(),db.sm_invoice_head.vat_total_amount.max(),db.sm_invoice_head.discount.max(),db.sm_invoice_head.sp_discount.max(),db.sm_invoice_head.return_tp.max(),db.sm_invoice_head.return_vat.max(),db.sm_invoice_head.return_discount.max(),db.sm_invoice_head.return_sp_discount.max(),db.sm_payment_collection.payment_collection_date,db.sm_payment_collection.collection_batch,db.sm_payment_collection.collection_amount.sum(),orderby=db.sm_invoice_head.id|db.sm_payment_collection.payment_collection_date,groupby=db.sm_invoice_head.id|db.sm_invoice_head.depot_id|db.sm_invoice_head.sl|db.sm_payment_collection.payment_collection_date|db.sm_payment_collection.collection_batch)
    
    recTotal=0
    recRows=qset.select(db.sm_payment_collection.cid,db.sm_payment_collection.collection_amount.sum(),groupby=db.sm_payment_collection.cid)
    for recRow in recRows:
        recTotal=recRow[db.sm_payment_collection.collection_amount.sum()]
        
    InvTotalTp=0
    InvTotalVat=0
    InvTotalDisc=0
    InvTotalSp=0
    InvTotalNet=0
    InvTotalAdjust=0
    
    retTotalTp=0
    retTotalVat=0
    retTotalDisc=0
    retTotalSpDisc=0
    retTotal=0
    
    invRows=qset.select(db.sm_invoice_head.id,db.sm_invoice_head.actual_total_tp.max(),db.sm_invoice_head.total_amount.max(),db.sm_invoice_head.vat_total_amount.max(),db.sm_invoice_head.discount.max(),db.sm_invoice_head.sp_discount.max(),db.sm_invoice_head.return_tp.max(),db.sm_invoice_head.return_vat.max(),db.sm_invoice_head.return_discount.max(),db.sm_invoice_head.return_sp_discount.max(),db.sm_invoice_head.adjust_amount.max(),groupby=db.sm_invoice_head.id)
    for invRow in invRows:
        actual_total_tp=invRow[db.sm_invoice_head.actual_total_tp.max()]       
        #total_amount=invRow.total_amount
        vat_total_amount=invRow[db.sm_invoice_head.vat_total_amount.max()]
        total_discount=invRow[db.sm_invoice_head.discount.max()]
        total_sp_discount=invRow[db.sm_invoice_head.sp_discount.max()]
        
        return_tp=invRow[db.sm_invoice_head.return_tp.max()]
        return_vat=invRow[db.sm_invoice_head.return_vat.max()]
        return_discount=invRow[db.sm_invoice_head.return_discount.max()]
        return_sp_discount=invRow[db.sm_invoice_head.return_sp_discount.max()]
        
        adjust_amount=invRow[db.sm_invoice_head.adjust_amount.max()]
        
        return_amt=return_tp+return_vat-return_discount
        
        retTotalTp+=return_tp+return_sp_discount
        retTotalVat+=return_vat
        retTotalDisc+=return_discount
        retTotalSpDisc+=return_sp_discount
        
        #retTotal+=return_amt
        
        #InvTotalTp+=total_amount-vat_total_amount+total_discount
        InvTotalTp+=actual_total_tp        
        InvTotalVat+=vat_total_amount
        InvTotalDisc+=total_discount
        InvTotalSp+=total_sp_discount
        
        #InvTotalNet+=total_amount
        
        InvTotalAdjust+=adjust_amount
        
    InvTotalTpAmt=InvTotalTp-retTotalTp
    InvTotalVatAmt=InvTotalVat-retTotalVat
    InvTotalDiscAmt=InvTotalDisc-retTotalDisc
    InvTotalSpDiscAmt=InvTotalSp-retTotalSpDisc
    
    InvTotalNetAmt=InvTotalTpAmt+InvTotalVatAmt-(InvTotalDiscAmt+InvTotalSpDiscAmt)
    
    if InvTotalNetAmt>0:
        recTpAmt=(InvTotalTpAmt*recTotal)/InvTotalNetAmt
        recVatAmt=(InvTotalVatAmt*recTotal)/InvTotalNetAmt
        recDiscAmt=(InvTotalDiscAmt*recTotal)/InvTotalNetAmt
        recSpDiscAmt=(InvTotalSpDiscAmt*recTotal)/InvTotalNetAmt
    else:
        recTpAmt=0
        recVatAmt=0
        recDiscAmt=0
        recSpDiscAmt=0
    
    #=============================
#     p_totalInvTP=InvTotalTpAmt
#     p_totalInvVat=InvTotalVatAmt
#     p_totalInvDisc=InvTotalDiscAmt
#     p_totalInvSp=InvTotalSpDiscAmt
#     p_totalInvAmt=InvTotalNetAmt
#     
#     percentTp=0
#     percentVat=0
#     percentDisc=0
#     percentSpDisc=0  
#     try:
#         percentTp=p_totalInvTP/p_totalInvAmt*100
#         percentVat=p_totalInvVat/p_totalInvAmt*100
#         percentDisc=p_totalInvDisc/p_totalInvAmt*100
#         percentSpDisc=p_totalInvSp/p_totalInvAmt*100
#     except:
#         percentTp=0
#         percentVat=0
#         percentDisc=0
#         percentSpDisc=0
    #========================
    #percentTp=percentTp,percentVat=percentVat,percentDisc=percentDisc,percentSpDisc=percentSpDisc,
    
    return dict(records=records,fromDate=fromDate,toDate=toDate,depotID=depot_id,depotName=depot_name,storeID=store_id,storeName=store_name,deliveryManID=delivery_man_id,deliveryManName=delivery_man_name,territoryID=territory_id,territoryName=territory_name,msoID=mso_id,msoName=mso_name,InvTotalNetAmt=InvTotalNetAmt,InvTotalDiscAmt=InvTotalDiscAmt,InvTotalVatAmt=InvTotalVatAmt,InvTotalTpAmt=InvTotalTpAmt,InvTotalSp=InvTotalSp,recTotal=recTotal,recTpAmt=recTpAmt,recVatAmt=recVatAmt,recDiscAmt=recDiscAmt,recSpDiscAmt=recSpDiscAmt,InvTotalSpDiscAmt=InvTotalSpDiscAmt,InvTotalAdjust=InvTotalAdjust,coll_inv_sl_from=coll_inv_sl_from,coll_inv_sl_to=coll_inv_sl_to,coll_inv_term=coll_inv_term,coll_credit_type=coll_credit_type,coll_payment_mode=coll_payment_mode,coll_customer_cat=coll_customer_cat,coll_customer_sub_cat=coll_customer_sub_cat,catName=catName,subCatName=subCatName,coll_batchno=coll_batchno,page=page,items_per_page=items_per_page)    
    
def collInvAndReceipt_download_bak():
    c_id=session.cid
    
    response.title='7.01 Downlaod - Invoice and Receipt'
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate    
    
    depot_id=str(request.vars.depotID).strip()
    store_id=str(request.vars.storeID).strip()    
    delivery_man_id=str(request.vars.deliveryManID).strip()  
    territory_id=str(request.vars.territoryID).strip()    
    mso_id=str(request.vars.msoID).strip()
    
    coll_inv_term=str(request.vars.coll_inv_term).strip()  
    coll_credit_type=str(request.vars.coll_credit_type).strip()  
    coll_payment_mode=str(request.vars.coll_payment_mode).strip()  
    
    try:
        coll_inv_sl_from=int(request.vars.coll_inv_sl_from)
        coll_inv_sl_to=int(request.vars.coll_inv_sl_to)
    except:
        coll_inv_sl_from=''
        coll_inv_sl_to=''
        
    try:
        coll_batchno=int(request.vars.coll_batchno)
    except:
        coll_batchno=''
        
    coll_customer_cat=str(request.vars.coll_customer_cat).strip() 
    coll_customer_sub_cat=str(request.vars.coll_customer_sub_cat).strip()    
    catName=''
    custCatRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_CATEGORY')&(db.sm_category_type.cat_type_id==coll_customer_cat)).select(db.sm_category_type.cat_type_name, limitby=(0,1))
    if custCatRows:
        catName=custCatRows[0].cat_type_name        
    subCatName=''
    custSubCatRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_SUB_CATEGORY')&(db.sm_category_type.cat_type_id==coll_customer_sub_cat)).select(db.sm_category_type.cat_type_name, limitby=(0,1))
    if custSubCatRows:
        subCatName=custSubCatRows[0].cat_type_name
    
    depot_name=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depot_name=depotRow[0].name
    
    store_name=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        store_name=storeRow[0].store_name
        
    delivery_man_name=''
    dpRow=db((db.sm_delivery_man.cid==c_id)&(db.sm_delivery_man.depot_id==depot_id)&(db.sm_delivery_man.d_man_id==delivery_man_id)).select(db.sm_delivery_man.name,limitby=(0,1))
    if dpRow:
        delivery_man_name=dpRow[0].name
        
    territory_name=''
    levelRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==territory_id)).select(db.sm_level.level_name,limitby=(0,1))
    if levelRow:
        territory_name=levelRow[0].level_name
         
    mso_name=''
    repRow=db((db.sm_rep.cid==c_id)&(db.sm_rep.rep_id==mso_id)).select(db.sm_rep.name,limitby=(0,1))
    if repRow:
        mso_name=repRow[0].name
        
    startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d').strftime('%Y-%m-%d')    
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d').strftime('%Y-%m-%d')
    
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    
    #dateRecords="SELECT a.invoice_date,a.sl, a.client_id, a.client_name, a.area_id,a.market_name, a.discount, a.vat_total_amount, a.total_amount,a.adjust_amount,b.collection_amount,b.collection_date FROM sm_invoice_head a LEFT OUTER JOIN sm_payment_collection b ON a.sl=b.sl where a.cid = '"+c_id+"' and a.invoice_date >= '"+str(startDt)+"' and a.invoice_date <= '"+str(endDt)+"' and a.depot_id = '"+depot_id+"' and a.store_id = '"+store_id+"' and a.status = 'Invoiced' and a.sl !=0 ORDER BY a.sl"
    #records=db.executesql(dateRecords,as_dict = True)    
    
    transactionCause=['','COLLECTION ERROR','ENTRY ERROR']
    
    qset=db()
    qset=qset(db.sm_payment_collection.cid==c_id)
    qset=qset(db.sm_payment_collection.depot_id==depot_id)
    qset=qset(db.sm_payment_collection.store_id==store_id)
    if coll_inv_sl_from!='' and coll_inv_sl_to!='':
        qset=qset((db.sm_payment_collection.sl>=coll_inv_sl_from)&(db.sm_payment_collection.sl<=coll_inv_sl_to))
    else:        
        qset=qset((db.sm_payment_collection.payment_collection_date>=startDt)&(db.sm_payment_collection.payment_collection_date<=endDt))
        
    qset=qset(db.sm_payment_collection.status=='Posted')
    #qset=qset(db.sm_payment_collection.transaction_type=='Payment')
    qset=qset(db.sm_payment_collection.transaction_cause.belongs(transactionCause))
    
    if delivery_man_id!='':
        qset=qset(db.sm_payment_collection.d_man_id==delivery_man_id)
    if territory_id!='':
        qset=qset(db.sm_payment_collection.area_id==territory_id)
    if mso_id!='':
        qset=qset(db.sm_payment_collection.rep_id==mso_id)
        
    if coll_inv_term!='':
        qset=qset(db.sm_payment_collection.payment_mode==coll_inv_term)
    if coll_credit_type!='':
        qset=qset(db.sm_payment_collection.credit_note==coll_credit_type)
    if coll_payment_mode!='':
        qset=qset(db.sm_payment_collection.payment_type==coll_payment_mode)
    if coll_customer_cat!='':
        qset=qset(db.sm_payment_collection.cl_category_id==coll_customer_cat)
    if coll_customer_sub_cat!='':
        qset=qset(db.sm_payment_collection.cl_sub_category_id==coll_customer_sub_cat)
    
    if coll_batchno!='':
        qset=qset(db.sm_payment_collection.collection_batch==coll_batchno)
    
    qset=qset(db.sm_invoice_head.cid==c_id)
    qset=qset(db.sm_invoice_head.depot_id==depot_id)
    qset=qset(db.sm_payment_collection.head_rowid==db.sm_invoice_head.id)
    
    records=qset.select(db.sm_invoice_head.id,db.sm_invoice_head.depot_id,db.sm_invoice_head.sl,db.sm_invoice_head.invoice_date.max(),db.sm_invoice_head.shipment_no.max(),db.sm_invoice_head.payment_mode.max(),db.sm_invoice_head.credit_note.max(),db.sm_invoice_head.client_id.max(),db.sm_invoice_head.client_name.max(),db.sm_invoice_head.area_id.max(),db.sm_invoice_head.market_name.max(),db.sm_invoice_head.rep_id.max(),db.sm_invoice_head.rep_name.max(),db.sm_invoice_head.d_man_id.max(),db.sm_invoice_head.d_man_name.max(),db.sm_invoice_head.adjust_amount.max(),db.sm_invoice_head.actual_total_tp.max(),db.sm_invoice_head.vat_total_amount.max(),db.sm_invoice_head.discount.max(),db.sm_invoice_head.sp_discount.max(),db.sm_invoice_head.return_tp.max(),db.sm_invoice_head.return_vat.max(),db.sm_invoice_head.return_discount.max(),db.sm_invoice_head.return_sp_discount.max(),db.sm_payment_collection.payment_collection_date,db.sm_payment_collection.collection_batch,db.sm_payment_collection.collection_amount.sum(),orderby=db.sm_invoice_head.id|db.sm_payment_collection.payment_collection_date,groupby=db.sm_invoice_head.id|db.sm_invoice_head.depot_id|db.sm_invoice_head.sl|db.sm_payment_collection.payment_collection_date|db.sm_payment_collection.collection_batch)
    
    recTotal=0
    recRows=qset.select(db.sm_payment_collection.cid,db.sm_payment_collection.collection_amount.sum(),groupby=db.sm_payment_collection.cid)
    for recRow in recRows:
        recTotal=recRow[db.sm_payment_collection.collection_amount.sum()]
        
    InvTotalTp=0
    InvTotalVat=0
    InvTotalDisc=0
    InvTotalSp=0
    InvTotalNet=0
    InvTotalAdjust=0
    
    retTotalTp=0
    retTotalVat=0
    retTotalDisc=0
    retTotalSpDisc=0
    retTotal=0
    
    invRows=qset.select(db.sm_invoice_head.id,db.sm_invoice_head.actual_total_tp.max(),db.sm_invoice_head.total_amount.max(),db.sm_invoice_head.vat_total_amount.max(),db.sm_invoice_head.discount.max(),db.sm_invoice_head.sp_discount.max(),db.sm_invoice_head.return_tp.max(),db.sm_invoice_head.return_vat.max(),db.sm_invoice_head.return_discount.max(),db.sm_invoice_head.return_sp_discount.max(),db.sm_invoice_head.adjust_amount.max(),groupby=db.sm_invoice_head.id)
    for invRow in invRows:
        actual_total_tp=invRow[db.sm_invoice_head.actual_total_tp.max()]       
        #total_amount=invRow.total_amount
        vat_total_amount=invRow[db.sm_invoice_head.vat_total_amount.max()]
        total_discount=invRow[db.sm_invoice_head.discount.max()]
        total_sp_discount=invRow[db.sm_invoice_head.sp_discount.max()]
        
        return_tp=invRow[db.sm_invoice_head.return_tp.max()]
        return_vat=invRow[db.sm_invoice_head.return_vat.max()]
        return_discount=invRow[db.sm_invoice_head.return_discount.max()]
        return_sp_discount=invRow[db.sm_invoice_head.return_sp_discount.max()]
        
        adjust_amount=invRow[db.sm_invoice_head.adjust_amount.max()]
        
        return_amt=return_tp+return_vat-return_discount
        
        retTotalTp+=return_tp+return_sp_discount
        retTotalVat+=return_vat
        retTotalDisc+=return_discount
        retTotalSpDisc+=return_sp_discount
        
        #retTotal+=return_amt
        
        #InvTotalTp+=total_amount-vat_total_amount+total_discount
        InvTotalTp+=actual_total_tp        
        InvTotalVat+=vat_total_amount
        InvTotalDisc+=total_discount
        InvTotalSp+=total_sp_discount
        
        #InvTotalNet+=total_amount
        
        InvTotalAdjust+=adjust_amount
        
    InvTotalTpAmt=InvTotalTp-retTotalTp
    InvTotalVatAmt=InvTotalVat-retTotalVat
    InvTotalDiscAmt=InvTotalDisc-retTotalDisc
    InvTotalSpDiscAmt=InvTotalSp-retTotalSpDisc
    
    InvTotalNetAmt=InvTotalTpAmt+InvTotalVatAmt-(InvTotalDiscAmt+InvTotalSpDiscAmt)
    
    recTpAmt=0
    recVatAmt=0
    recDiscAmt=0
    recSpDiscAmt=0
    
    #-------------
    
    myString='7.1 Invoice Wise Cash Collection: With Invoice & Receipt Details\n'
    
    if coll_inv_sl_from!='' and coll_inv_sl_to!='':
        myString+='INV.No '+',From:'+str(coll_inv_sl_from)+',To:'+str(coll_inv_sl_to)+'\n'
    else:
        myString+='Rec. Date From:,'+str(startDt)+'\n'            
        myString+='To Date:'+','+str(endDt)+'\n'
    
    myString+='Branch ID:,'+str(depot_id)+'\n'
    myString+='Branch Name'+','+str(depot_name)+'\n'
    myString+='Store ID:,'+str(store_id)+'\n'
    myString+='Store Name'+','+str(store_name)+'\n'
    myString+='DP ID:,'+str(delivery_man_id)+'\n'
    myString+='DP Name'+','+str(delivery_man_name)+'\n'
    myString+='Territory ID:,'+str(territory_id)+'\n'
    myString+='Territory Name'+','+str(territory_name)+'\n'
    myString+='MSO ID:,'+str(mso_id)+'\n'
    myString+='MSO Name'+','+str(mso_name)+'\n'
    
    if coll_inv_term=='':
        coll_inv_term='ALL'
    else:
        if coll_inv_term=='CREDIT':
            if coll_credit_type=='':
                coll_credit_type='ALL'
    if coll_payment_mode=='':
        coll_payment_mode='ALL'    
        
    myString+='Invoice Term:,'+str(coll_inv_term)+'\n'
    myString+='Credit Type:,'+str(coll_credit_type)+'\n'
    myString+='Payment Type:,'+str(coll_payment_mode)+'\n'
    
    if catName=='':
        catName='ALL'
    if subCatName=='':
        subCatName='ALL'        
    myString+='Customer Category'+','+str(catName)+'\n'
    myString+='Customer Sub-Category'+','+str(subCatName)+'\n'
    
    if coll_batchno!='':
        myString+='Batch Number'+',`'+str(coll_batchno)+'\n'
        
    sl=0
    myString+='SL,Inv.Date,ShipNo,Invoice No,InvoiceTerm,CreditType,Cust. ID,Cust. Name,Tr. Code,Market,SPID,SPName,DPID,DPName,INVOICE-TP,INVOICE-Vat,INVOICE-Disc,INVOICE-SP,INVOICE-Net,Adjusted,RECEIVED-TP,RECEIVED-Vat,RECEIVED-Disc,RECEIVED-SP,RECEIVED-Net,Rec.Date,BatchNo'+'\n'
    for row in records:
        sl+=1
        
        invoice_date=row[db.sm_invoice_head.invoice_date.max()] 
        if row.sm_invoice_head.sl==0:
            shipment_no=row[db.sm_invoice_head.shipment_no.max()]
        else:
            shipment_no=str(session.prefix_invoice)+'SH-'+str(row[db.sm_invoice_head.shipment_no.max()])        
        invSl=str(session.prefix_invoice)+'INV'+str(row.sm_invoice_head.depot_id)+'-'+str(row.sm_invoice_head.sl)        
        payment_mode=row[db.sm_invoice_head.payment_mode.max()]
        credit_note=row[db.sm_invoice_head.credit_note.max()]
#         invTermAndCreditType=''
#         if str(payment_mode).upper()=='CASH':
#             invTermAndCreditType=payment_mode
#         else:
#             invTermAndCreditType=credit_note
            
        client_id=row[db.sm_invoice_head.client_id.max()]
        client_name=row[db.sm_invoice_head.client_name.max()]
        area_id=row[db.sm_invoice_head.area_id.max()]
        market_name=row[db.sm_invoice_head.market_name.max()]
        rep_id=row[db.sm_invoice_head.rep_id.max()]
        rep_name=row[db.sm_invoice_head.rep_name.max()]
        d_man_id=row[db.sm_invoice_head.d_man_id.max()]
        d_man_name=row[db.sm_invoice_head.d_man_name.max()]
        
        invTpAmt=round(row[db.sm_invoice_head.actual_total_tp.max()]-(row[db.sm_invoice_head.return_tp.max()]+row[db.sm_invoice_head.return_sp_discount.max()]),2)
        invVatAmt=round(row[db.sm_invoice_head.vat_total_amount.max()]-row[db.sm_invoice_head.return_vat.max()],2)
        invDiscAmt=round(row[db.sm_invoice_head.discount.max()]-row[db.sm_invoice_head.return_discount.max()],2)
        invSpDiscAmt=round(row[db.sm_invoice_head.sp_discount.max()]-row[db.sm_invoice_head.return_sp_discount.max()],2)
        invTotal=invTpAmt+invVatAmt-(invDiscAmt+invSpDiscAmt)
        
        adjust_amount=round(row[db.sm_invoice_head.adjust_amount.max()],2)
        
        collectAmt=round(row[db.sm_payment_collection.collection_amount.sum()],2)
        
        if invTotal>0:
            recTp=round((invTpAmt*collectAmt)/invTotal,2)
            recVat=round((invVatAmt*collectAmt)/invTotal,2)
            recDisc=round((invDiscAmt*collectAmt)/invTotal,2)
            recSpDisc=round((invSpDiscAmt*collectAmt)/invTotal,2)
        else:
            recTp=0
            recVat=0
            recDisc=0
            recSpDisc=0
            
        recTpAmt+=recTp
        recVatAmt+=recVat
        recDiscAmt+=recDisc
        recSpDiscAmt+=recSpDisc
        
        payment_collection_date=row.sm_payment_collection.payment_collection_date        
        collection_batch=row.sm_payment_collection.collection_batch
        
        #------------------------        
        myString+=str(sl)+','+str(invoice_date)+','+str(shipment_no)+','+str(invSl)+','+str(payment_mode)+','+str(credit_note)+','+str(client_id)+','+str(client_name)+','+str(area_id)+','+str(market_name)+','+str(rep_id)+','+str(rep_name)+','+str(d_man_id)+','+str(d_man_name)+','+str(invTpAmt)+','+\
        str(invVatAmt)+','+str(invDiscAmt)+','+str(invSpDiscAmt)+','+str(invTotal)+','+str(adjust_amount)+','+str(recTp)+','+str(recVat)+','+str(recDisc)+','+str(recSpDisc)+','+str(collectAmt)+','+\
        str(payment_collection_date)+','+str(collection_batch)+'\n'
        
    myString+='\n\nSummary,,,,,,,,,,,,,,,,,,,,\n'    
    myString+='Invoice TP,'+str(round(InvTotalTpAmt,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Invoice VAT,'+str(round(InvTotalVatAmt,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Invoice Discount,'+str(round(InvTotalDiscAmt,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Invoice SP.Disc,'+str(round(InvTotalSpDiscAmt,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Invoice Net,'+str(round(InvTotalNetAmt,2))+',,,,,,,,,,,,,,,,,,,\n\n'
    
    myString+='Received TP,'+str(round(recTpAmt,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Received VAT,'+str(round(recVatAmt,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Received Discount,'+str(round(recDiscAmt,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Received SP.Disc,'+str(round(recSpDiscAmt,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Received Net,'+str(round(recTotal,2))+',,,,,,,,,,,,,,,,,,,\n\n'
    
    myString+='Adjustment,'+str(round(InvTotalAdjust,2))+',,,,,,,,,,,,,,,,,,,\n'
    
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_collInvAndReceipt.csv'   
    return str(myString)

    
def collMoneyReceipt2():
    c_id=session.cid
    
    response.title='3.02 Money Receipt'
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate    
    
    depot_id=str(request.vars.depotID).strip()
    store_id=str(request.vars.storeID).strip()    
    delivery_man_id=str(request.vars.deliveryManID).strip()    
    territory_id=str(request.vars.territoryID).strip()    
    mso_id=str(request.vars.msoID).strip()    
    customerID=str(request.vars.customerID).strip() 
        
    coll_inv_term=str(request.vars.coll_inv_term).strip()  
    coll_credit_type=str(request.vars.coll_credit_type).strip()  
    coll_payment_mode=str(request.vars.coll_payment_mode).strip()  
    
    try:
        coll_mrno=int(request.vars.coll_mrno)
    except:
        coll_mrno=''
    
    try:
        coll_inv_sl_from=int(request.vars.coll_inv_sl_from)
        coll_inv_sl_to=int(request.vars.coll_inv_sl_to)
    except:
        coll_inv_sl_from=''
        coll_inv_sl_to=''
        
    depot_name=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depot_name=depotRow[0].name
    
    store_name=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        store_name=storeRow[0].store_name
        
    delivery_man_name=''
    dpRow=db((db.sm_delivery_man.cid==c_id)&(db.sm_delivery_man.depot_id==depot_id)&(db.sm_delivery_man.d_man_id==delivery_man_id)).select(db.sm_delivery_man.name,limitby=(0,1))
    if dpRow:
        delivery_man_name=dpRow[0].name
        
    territory_name=''
    levelRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==territory_id)).select(db.sm_level.level_name,limitby=(0,1))
    if levelRow:
        territory_name=levelRow[0].level_name
        
    mso_name=''
    repRow=db((db.sm_rep.cid==c_id)&(db.sm_rep.rep_id==mso_id)).select(db.sm_rep.name,limitby=(0,1))
    if repRow:
        mso_name=repRow[0].name
        
    customerName=''
    clientRow=db((db.sm_client.cid==c_id)&(db.sm_client.depot_id==depot_id)&(db.sm_client.client_id==customerID)).select(db.sm_client.name,limitby=(0,1))
    if clientRow:
        customerName=clientRow[0].name
        
    startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d')    
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d')
    
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    transactionCause=['','COLLECTION ERROR','ENTRY ERROR']#blank for payment
    
    qset=db()
    qset=qset(db.sm_payment_collection.cid==c_id)
    #qset=qset((db.sm_payment_collection.collection_date>=startDt)&(db.sm_payment_collection.collection_date<=endDt))
    qset=qset(db.sm_payment_collection.depot_id==depot_id)
    qset=qset(db.sm_payment_collection.store_id==store_id)
    
    if coll_mrno!='':
        qset=qset(db.sm_payment_collection.id==coll_mrno)
    else:
        if coll_inv_sl_from!='' and coll_inv_sl_to!='':
            qset=qset((db.sm_payment_collection.sl>=coll_inv_sl_from)&(db.sm_payment_collection.sl<=coll_inv_sl_to))
        else:
            qset=qset((db.sm_payment_collection.payment_collection_date>=startDt)&(db.sm_payment_collection.payment_collection_date<=endDt))
         
    qset=qset(db.sm_payment_collection.status=='Posted')
    #qset=qset(db.sm_payment_collection.transaction_type=='Payment')
    qset=qset(db.sm_payment_collection.transaction_cause.belongs(transactionCause))
    
    #qset=qset(db.sm_client.cid==c_id)
    #qset=qset(db.sm_payment_collection.client_id==db.sm_client.client_id)
    
    if delivery_man_id!='':
        qset=qset(db.sm_payment_collection.d_man_id==delivery_man_id)
    if territory_id!='':
        qset=qset(db.sm_payment_collection.area_id==territory_id)
    if mso_id!='':
        qset=qset(db.sm_payment_collection.rep_id==mso_id)
    if customerID!='':
        qset=qset(db.sm_payment_collection.client_id==customerID)
     
    if coll_inv_term!='':
        qset=qset(db.sm_payment_collection.payment_mode==coll_inv_term)
    if coll_credit_type!='':
        qset=qset(db.sm_payment_collection.credit_note==coll_credit_type)
    if coll_payment_mode!='':
        qset=qset(db.sm_payment_collection.payment_type==coll_payment_mode)
        
    records=qset.select(db.sm_payment_collection.head_rowid,db.sm_payment_collection.payment_collection_date,db.sm_payment_collection.id.max(),db.sm_payment_collection.market_name.max(),db.sm_payment_collection.depot_id.max(),db.sm_payment_collection.collection_batch.max(),db.sm_payment_collection.client_id.max(),db.sm_payment_collection.client_name.max(),db.sm_payment_collection.depot_name.max(),db.sm_payment_collection.payment_type.max(),db.sm_payment_collection.sl.max(),db.sm_payment_collection.invoice_date.max(),db.sm_payment_collection.d_man_name.max(),db.sm_payment_collection.collection_note.max(),db.sm_payment_collection.collection_amount.sum(),orderby=db.sm_payment_collection.id,groupby=db.sm_payment_collection.head_rowid|db.sm_payment_collection.payment_collection_date)
    
    return dict(records=records,fromDate=fromDate,toDate=toDate,depotID=depot_id,depotName=depot_name,storeID=store_id,storeName=store_name,deliveryManID=delivery_man_id,deliveryManName=delivery_man_name,territoryID=territory_id,territoryName=territory_name,msoID=mso_id,msoName=mso_name,customerID=customerID,customerName=customerName,coll_mrno=coll_mrno,coll_inv_sl_from=coll_inv_sl_from,coll_inv_sl_to=coll_inv_sl_to,page=page,items_per_page=items_per_page)    
    
def collMoneyReceipt():
    c_id=session.cid
    
    response.title='3.1A Money Receipt'
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate    
    
    depot_id=str(request.vars.depotID).strip()
    store_id=str(request.vars.storeID).strip()    
    delivery_man_id=str(request.vars.deliveryManID).strip()    
    territory_id=str(request.vars.territoryID).strip()    
    mso_id=str(request.vars.msoID).strip()
        
    coll_inv_term=str(request.vars.coll_inv_term).strip()  
    coll_credit_type=str(request.vars.coll_credit_type).strip()  
    coll_payment_mode=str(request.vars.coll_payment_mode).strip()  
    
    try:
        coll_mrno=int(request.vars.coll_mrno)
    except:
        coll_mrno=''
    
    try:
        coll_inv_sl_from=int(request.vars.coll_inv_sl_from)
        coll_inv_sl_to=int(request.vars.coll_inv_sl_to)
    except:
        coll_inv_sl_from=''
        coll_inv_sl_to=''
    
    try:
        coll_batchno=int(request.vars.coll_batchno)
    except:
        coll_batchno=''
    
    depot_name=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depot_name=depotRow[0].name
    
    store_name=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        store_name=storeRow[0].store_name
        
    delivery_man_name=''
    dpRow=db((db.sm_delivery_man.cid==c_id)&(db.sm_delivery_man.depot_id==depot_id)&(db.sm_delivery_man.d_man_id==delivery_man_id)).select(db.sm_delivery_man.name,limitby=(0,1))
    if dpRow:
        delivery_man_name=dpRow[0].name
        
    territory_name=''
    levelRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==territory_id)).select(db.sm_level.level_name,limitby=(0,1))
    if levelRow:
        territory_name=levelRow[0].level_name
         
    mso_name=''
    repRow=db((db.sm_rep.cid==c_id)&(db.sm_rep.rep_id==mso_id)).select(db.sm_rep.name,limitby=(0,1))
    if repRow:
        mso_name=repRow[0].name
        
    
    startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d')    
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d')
    
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    transactionCause=['','COLLECTION ERROR','ENTRY ERROR']#blank for payment
    
    qset=db()
    qset=qset(db.sm_payment_collection.cid==c_id)
    #qset=qset((db.sm_payment_collection.collection_date>=startDt)&(db.sm_payment_collection.collection_date<=endDt))
    qset=qset(db.sm_payment_collection.depot_id==depot_id)
    qset=qset(db.sm_payment_collection.store_id==store_id)
    if coll_mrno!='':
        qset=qset(db.sm_payment_collection.id==coll_mrno)
    else:
        if coll_inv_sl_from!='' and coll_inv_sl_to!='':
            qset=qset((db.sm_payment_collection.sl>=coll_inv_sl_from)&(db.sm_payment_collection.sl<=coll_inv_sl_to))
        else:            
            qset=qset((db.sm_payment_collection.payment_collection_date>=startDt)&(db.sm_payment_collection.payment_collection_date<=endDt))
    
    qset=qset(db.sm_payment_collection.status=='Posted')
    qset=qset(db.sm_payment_collection.transaction_cause.belongs(transactionCause))
    
    if delivery_man_id!='':
        qset=qset(db.sm_payment_collection.d_man_id==delivery_man_id)
    if territory_id!='':
        qset=qset(db.sm_payment_collection.area_id==territory_id)
    if mso_id!='':
        qset=qset(db.sm_payment_collection.rep_id==mso_id)
        
    if coll_inv_term!='':
        qset=qset(db.sm_payment_collection.payment_mode==coll_inv_term)
    if coll_credit_type!='':
        qset=qset(db.sm_payment_collection.credit_note==coll_credit_type)
    if coll_payment_mode!='':
        qset=qset(db.sm_payment_collection.payment_type==coll_payment_mode)
    
    if coll_batchno!='':
        qset=qset(db.sm_payment_collection.collection_batch==coll_batchno)
        
    records=qset.select(db.sm_payment_collection.sl,db.sm_payment_collection.id,db.sm_payment_collection.depot_id,db.sm_payment_collection.order_sl,db.sm_payment_collection.collection_date,db.sm_payment_collection.payment_collection_date,db.sm_payment_collection.client_id,db.sm_payment_collection.client_name,db.sm_payment_collection.total_inv_amount,db.sm_payment_collection.collection_amount,db.sm_payment_collection.payment_mode,db.sm_payment_collection.d_man_name,db.sm_payment_collection.payment_type,db.sm_payment_collection.transaction_type,db.sm_payment_collection.transaction_cause,db.sm_payment_collection.collection_batch,db.sm_payment_collection.collection_note,orderby=~db.sm_payment_collection.payment_collection_date|~db.sm_payment_collection.id)
    
    return dict(records=records,fromDate=fromDate,toDate=toDate,depotID=depot_id,depotName=depot_name,storeID=store_id,storeName=store_name,deliveryManID=delivery_man_id,deliveryManName=delivery_man_name,territoryID=territory_id,territoryName=territory_name,msoID=mso_id,msoName=mso_name,coll_mrno=coll_mrno,coll_inv_sl_from=coll_inv_sl_from,coll_inv_sl_to=coll_inv_sl_to,coll_inv_term=coll_inv_term,coll_credit_type=coll_credit_type,coll_payment_mode=coll_payment_mode,coll_batchno=coll_batchno,page=page,items_per_page=items_per_page)    
    
def collMoneyReceipt_download():
    c_id=session.cid
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate    
    
    depot_id=str(request.vars.depotID).strip()
    store_id=str(request.vars.storeID).strip()    
    delivery_man_id=str(request.vars.deliveryManID).strip()    
    territory_id=str(request.vars.territoryID).strip()    
    mso_id=str(request.vars.msoID).strip()    
        
    coll_inv_term=str(request.vars.coll_inv_term).strip()  
    coll_credit_type=str(request.vars.coll_credit_type).strip()  
    coll_payment_mode=str(request.vars.coll_payment_mode).strip()  
    
    try:
        coll_mrno=int(request.vars.coll_mrno)
    except:
        coll_mrno=''
    
    try:
        coll_inv_sl_from=int(request.vars.coll_inv_sl_from)
        coll_inv_sl_to=int(request.vars.coll_inv_sl_to)
    except:
        coll_inv_sl_from=''
        coll_inv_sl_to=''
    
    try:
        coll_batchno=int(request.vars.coll_batchno)
    except:
        coll_batchno=''
    
    depot_name=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depot_name=depotRow[0].name
    
    store_name=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        store_name=storeRow[0].store_name
        
    delivery_man_name=''
    dpRow=db((db.sm_delivery_man.cid==c_id)&(db.sm_delivery_man.depot_id==depot_id)&(db.sm_delivery_man.d_man_id==delivery_man_id)).select(db.sm_delivery_man.name,limitby=(0,1))
    if dpRow:
        delivery_man_name=dpRow[0].name
        
    territory_name=''
    levelRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==territory_id)).select(db.sm_level.level_name,limitby=(0,1))
    if levelRow:
        territory_name=levelRow[0].level_name
         
    mso_name=''
    repRow=db((db.sm_rep.cid==c_id)&(db.sm_rep.rep_id==mso_id)).select(db.sm_rep.name,limitby=(0,1))
    if repRow:
        mso_name=repRow[0].name
        
    startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d')    
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d')
    
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    transactionCause=['','COLLECTION ERROR','ENTRY ERROR']#blank for payment
    
    qset=db()
    qset=qset(db.sm_payment_collection.cid==c_id)
    qset=qset(db.sm_payment_collection.depot_id==depot_id)
    qset=qset(db.sm_payment_collection.store_id==store_id)
    if coll_mrno!='':
        qset=qset(db.sm_payment_collection.id==coll_mrno)
    else:
        if coll_inv_sl_from!='' and coll_inv_sl_to!='':
            qset=qset((db.sm_payment_collection.sl>=coll_inv_sl_from)&(db.sm_payment_collection.sl<=coll_inv_sl_to))
        else:            
            qset=qset((db.sm_payment_collection.payment_collection_date>=startDt)&(db.sm_payment_collection.payment_collection_date<=endDt))
    
    qset=qset(db.sm_payment_collection.status=='Posted')
    qset=qset(db.sm_payment_collection.transaction_cause.belongs(transactionCause))
    
    if delivery_man_id!='':
        qset=qset(db.sm_payment_collection.d_man_id==delivery_man_id)
    if territory_id!='':
        qset=qset(db.sm_payment_collection.area_id==territory_id)
    if mso_id!='':
        qset=qset(db.sm_payment_collection.rep_id==mso_id)
         
    if coll_inv_term!='':
        qset=qset(db.sm_payment_collection.payment_mode==coll_inv_term)
    if coll_credit_type!='':
        qset=qset(db.sm_payment_collection.credit_note==coll_credit_type)
    if coll_payment_mode!='':
        qset=qset(db.sm_payment_collection.payment_type==coll_payment_mode)
        
    if coll_batchno!='':
        qset=qset(db.sm_payment_collection.collection_batch==coll_batchno)
        
    records=qset.select(db.sm_payment_collection.sl,db.sm_payment_collection.id,db.sm_payment_collection.depot_id,db.sm_payment_collection.order_sl,db.sm_payment_collection.collection_date,db.sm_payment_collection.payment_collection_date,db.sm_payment_collection.client_id,db.sm_payment_collection.client_name,db.sm_payment_collection.total_inv_amount,db.sm_payment_collection.collection_amount,db.sm_payment_collection.payment_mode,db.sm_payment_collection.d_man_name,db.sm_payment_collection.payment_type,db.sm_payment_collection.transaction_type,db.sm_payment_collection.transaction_cause,db.sm_payment_collection.collection_batch,db.sm_payment_collection.collection_note,orderby=~db.sm_payment_collection.payment_collection_date|~db.sm_payment_collection.id)
    
    #-------------    
    myString='3.1-A Money Receipt\n'
    if coll_mrno!='':
        myString+='MR. No'+','+str(coll_mrno)+'\n'
    else:
        if coll_inv_sl_from!='' and coll_inv_sl_to!='':
            myString+='INV.No '+',From:'+str(coll_inv_sl_from)+',To:'+str(coll_inv_sl_to)+'\n'
        else:
            myString+='Rec. Date From:,'+str(startDt)+'\n'            
            myString+='To Date:'+','+str(endDt)+'\n'
    
    myString+='Branch ID:,'+str(depot_id)+'\n'
    myString+='Branch Name'+','+str(depot_name)+'\n'
    myString+='Store ID:,'+str(store_id)+'\n'
    myString+='Store Name'+','+str(store_name)+'\n'
    myString+='DP ID:,'+str(delivery_man_id)+'\n'
    myString+='DP Name'+','+str(delivery_man_name)+'\n'
    myString+='Territory ID:,'+str(territory_id)+'\n'
    myString+='Territory Name'+','+str(territory_name)+'\n'
    myString+='MSO ID:,'+str(mso_id)+'\n'
    myString+='MSO Name'+','+str(mso_name)+'\n'
        
    if coll_inv_term=='':
        coll_inv_term='ALL'
    else:
        if coll_inv_term=='CREDIT':
            if coll_credit_type=='':
                coll_credit_type='ALL'
                
    if coll_payment_mode=='':
        coll_payment_mode='ALL'    
        
    myString+='Invoice Term:,'+str(coll_inv_term)+'\n'
    myString+='Credit Type:,'+str(coll_credit_type)+'\n'
    myString+='Payment Type:,'+str(coll_payment_mode)+'\n'
    
    if coll_batchno!='':
        myString+='Batch Number'+',`'+str(coll_batchno)+'\n'
        
    totalApAmount=0
    sl=0
    myString+='Sl.No,MR.No,Batch Number,Inv.SL/Ref.No,Doc Date,Cust. Name,Inv Amount,Applied Amt,Invoice Term,Payment Mode,Payment Description,Deliveryman Name'+'\n'
    for row in records:
        sl+=1        
        mrNo=row.id
        collection_batch=row.collection_batch
        invSl=str(session.prefix_invoice)+'INV'+str(row.depot_id)+'-'+str(row.sl)
        payment_collection_date=row.payment_collection_date        
        client_name=row.client_name
        total_inv_amount=row.total_inv_amount
        collection_amount=row.collection_amount
        totalApAmount+=collection_amount
        
        payment_mode=row.payment_mode                                                  
        payment_type=row.payment_type
        
        if row.transaction_cause=='':
            transaction_type=row.transaction_type
        else:
            transaction_type=str(row.transaction_type)+';'+str(row.transaction_cause)
        
        collection_note=row.collection_note
        d_man_name=row.d_man_name
            
        #------------------------        
        myString+=str(sl)+','+str(mrNo)+','+str(collection_batch)+','+str(invSl)+','+str(payment_collection_date)+','+str(client_name)+','+str(total_inv_amount)+','+str(collection_amount)+','+\
        str(payment_mode)+','+str(payment_type)+','+str(collection_note)+','+str(d_man_name)+'\n'
        
    myString+='Total,,,,,,,'+str(round(totalApAmount,2))+'\n\n\n'
    
    myString+='TAKA,'+str(round(totalApAmount,2))+'\n'
    
    try:
        inword=num2word(str(totalApAmount))
    except:
        inword='-'
    
    myString+='Taka in Words:,'+str(inword)+'\n'
    
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_moneyReceipt.csv'   
    return str(myString)


def collMoneyReceiptAdjustment():
    c_id=session.cid
    
    response.title='3.1B Money Receipt Adjustment'
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate    
    
    depot_id=str(request.vars.depotID).strip()
    store_id=str(request.vars.storeID).strip()    
    delivery_man_id=str(request.vars.deliveryManID).strip()    
    territory_id=str(request.vars.territoryID).strip()    
    mso_id=str(request.vars.msoID).strip()    
        
    coll_inv_term=str(request.vars.coll_inv_term).strip()  
    coll_credit_type=str(request.vars.coll_credit_type).strip()  
    coll_payment_mode=str(request.vars.coll_payment_mode).strip()  
    
    try:
        coll_mrno=int(request.vars.coll_mrno)
    except:
        coll_mrno=''
    
    try:
        coll_inv_sl_from=int(request.vars.coll_inv_sl_from)
        coll_inv_sl_to=int(request.vars.coll_inv_sl_to)
    except:
        coll_inv_sl_from=''
        coll_inv_sl_to=''
    
    coll_adjustment_cause=str(request.vars.coll_adjustment_cause).strip()  
    
    depot_name=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depot_name=depotRow[0].name
    
    store_name=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        store_name=storeRow[0].store_name
        
    delivery_man_name=''
    dpRow=db((db.sm_delivery_man.cid==c_id)&(db.sm_delivery_man.depot_id==depot_id)&(db.sm_delivery_man.d_man_id==delivery_man_id)).select(db.sm_delivery_man.name,limitby=(0,1))
    if dpRow:
        delivery_man_name=dpRow[0].name
        
    territory_name=''
    levelRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==territory_id)).select(db.sm_level.level_name,limitby=(0,1))
    if levelRow:
        territory_name=levelRow[0].level_name
         
    mso_name=''
    repRow=db((db.sm_rep.cid==c_id)&(db.sm_rep.rep_id==mso_id)).select(db.sm_rep.name,limitby=(0,1))
    if repRow:
        mso_name=repRow[0].name
        
    startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d')    
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d')
    
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    transactionCause=['VAT AIT','RETURN GOODS','BAD DEBTS']#blank for payment
    
    qset=db()
    qset=qset(db.sm_payment_collection.cid==c_id)
    #qset=qset((db.sm_payment_collection.collection_date>=startDt)&(db.sm_payment_collection.collection_date<=endDt))
    qset=qset(db.sm_payment_collection.depot_id==depot_id)
    qset=qset(db.sm_payment_collection.store_id==store_id)
    if coll_mrno!='':
        qset=qset(db.sm_payment_collection.id==coll_mrno)
    else:
        if coll_inv_sl_from!='' and coll_inv_sl_to!='':
            qset=qset((db.sm_payment_collection.sl>=coll_inv_sl_from)&(db.sm_payment_collection.sl<=coll_inv_sl_to))
        else:
            qset=qset((db.sm_payment_collection.payment_collection_date>=startDt)&(db.sm_payment_collection.payment_collection_date<=endDt))
            
    qset=qset(db.sm_payment_collection.status=='Posted')
    qset=qset(db.sm_payment_collection.transaction_cause.belongs(transactionCause))
    
    if delivery_man_id!='':
        qset=qset(db.sm_payment_collection.d_man_id==delivery_man_id)
    if territory_id!='':
        qset=qset(db.sm_payment_collection.area_id==territory_id)
    if mso_id!='':
        qset=qset(db.sm_payment_collection.rep_id==mso_id)
         
    if coll_inv_term!='':
        qset=qset(db.sm_payment_collection.payment_mode==coll_inv_term)
    if coll_credit_type!='':
        qset=qset(db.sm_payment_collection.credit_note==coll_credit_type)
    if coll_payment_mode!='':
        qset=qset(db.sm_payment_collection.payment_type==coll_payment_mode)    
    if coll_adjustment_cause!='':
        qset=qset(db.sm_payment_collection.transaction_cause==coll_adjustment_cause)
    
    records=qset.select(db.sm_payment_collection.sl,db.sm_payment_collection.id,db.sm_payment_collection.depot_id,db.sm_payment_collection.order_sl,db.sm_payment_collection.collection_date,db.sm_payment_collection.payment_collection_date,db.sm_payment_collection.client_id,db.sm_payment_collection.client_name,db.sm_payment_collection.total_inv_amount,db.sm_payment_collection.collection_amount,db.sm_payment_collection.payment_type,db.sm_payment_collection.d_man_name,db.sm_payment_collection.transaction_type,db.sm_payment_collection.transaction_cause,db.sm_payment_collection.collection_note,orderby=~db.sm_payment_collection.payment_collection_date|~db.sm_payment_collection.id)
    
    return dict(records=records,fromDate=fromDate,toDate=toDate,depotID=depot_id,depotName=depot_name,storeID=store_id,storeName=store_name,deliveryManID=delivery_man_id,deliveryManName=delivery_man_name,territoryID=territory_id,territoryName=territory_name,msoID=mso_id,msoName=mso_name,coll_mrno=coll_mrno,coll_inv_sl_from=coll_inv_sl_from,coll_inv_sl_to=coll_inv_sl_to,coll_inv_term=coll_inv_term,coll_credit_type=coll_credit_type,coll_payment_mode=coll_payment_mode,coll_adjustment_cause=coll_adjustment_cause,page=page,items_per_page=items_per_page)    
    
def collMoneyReceiptAdjustment_download():
    c_id=session.cid
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate    
    
    depot_id=str(request.vars.depotID).strip()
    store_id=str(request.vars.storeID).strip()    
    delivery_man_id=str(request.vars.deliveryManID).strip()    
    territory_id=str(request.vars.territoryID).strip()    
    mso_id=str(request.vars.msoID).strip()    
        
    coll_inv_term=str(request.vars.coll_inv_term).strip()  
    coll_credit_type=str(request.vars.coll_credit_type).strip()  
    coll_payment_mode=str(request.vars.coll_payment_mode).strip()  
    
    try:
        coll_mrno=int(request.vars.coll_mrno)
    except:
        coll_mrno=''
    
    try:
        coll_inv_sl_from=int(request.vars.coll_inv_sl_from)
        coll_inv_sl_to=int(request.vars.coll_inv_sl_to)
    except:
        coll_inv_sl_from=''
        coll_inv_sl_to=''
    
    coll_adjustment_cause=str(request.vars.coll_adjustment_cause).strip()  
    
    depot_name=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depot_name=depotRow[0].name
    
    store_name=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        store_name=storeRow[0].store_name
        
    delivery_man_name=''
    dpRow=db((db.sm_delivery_man.cid==c_id)&(db.sm_delivery_man.depot_id==depot_id)&(db.sm_delivery_man.d_man_id==delivery_man_id)).select(db.sm_delivery_man.name,limitby=(0,1))
    if dpRow:
        delivery_man_name=dpRow[0].name
        
    territory_name=''
    levelRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==territory_id)).select(db.sm_level.level_name,limitby=(0,1))
    if levelRow:
        territory_name=levelRow[0].level_name
         
    mso_name=''
    repRow=db((db.sm_rep.cid==c_id)&(db.sm_rep.rep_id==mso_id)).select(db.sm_rep.name,limitby=(0,1))
    if repRow:
        mso_name=repRow[0].name
        
    startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d')    
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d')
    
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    transactionCause=['VAT AIT','RETURN GOODS','BAD DEBTS']#blank for payment
    
    qset=db()
    qset=qset(db.sm_payment_collection.cid==c_id)
    #qset=qset((db.sm_payment_collection.collection_date>=startDt)&(db.sm_payment_collection.collection_date<=endDt))
    qset=qset(db.sm_payment_collection.depot_id==depot_id)
    qset=qset(db.sm_payment_collection.store_id==store_id)
    if coll_mrno!='':
        qset=qset(db.sm_payment_collection.id==coll_mrno)
    else:
        if coll_inv_sl_from!='' and coll_inv_sl_to!='':
            qset=qset((db.sm_payment_collection.sl>=coll_inv_sl_from)&(db.sm_payment_collection.sl<=coll_inv_sl_to))
        else:            
            qset=qset((db.sm_payment_collection.payment_collection_date>=startDt)&(db.sm_payment_collection.payment_collection_date<=endDt))
            
    qset=qset(db.sm_payment_collection.status=='Posted')
    qset=qset(db.sm_payment_collection.transaction_cause.belongs(transactionCause))    
    if delivery_man_id!='':
        qset=qset(db.sm_payment_collection.d_man_id==delivery_man_id)
    if territory_id!='':
        qset=qset(db.sm_payment_collection.area_id==territory_id)
    if mso_id!='':
        qset=qset(db.sm_payment_collection.rep_id==mso_id)
    if coll_mrno!='':
        qset=qset(db.sm_payment_collection.id==coll_mrno)
     
    if coll_inv_term!='':
        qset=qset(db.sm_payment_collection.payment_mode==coll_inv_term)
    if coll_credit_type!='':
        qset=qset(db.sm_payment_collection.credit_note==coll_credit_type)
    if coll_payment_mode!='':
        qset=qset(db.sm_payment_collection.payment_type==coll_payment_mode)
    if coll_adjustment_cause!='':
        qset=qset(db.sm_payment_collection.transaction_cause==coll_adjustment_cause)
        
    records=qset.select(db.sm_payment_collection.sl,db.sm_payment_collection.id,db.sm_payment_collection.depot_id,db.sm_payment_collection.order_sl,db.sm_payment_collection.collection_date,db.sm_payment_collection.payment_collection_date,db.sm_payment_collection.client_id,db.sm_payment_collection.client_name,db.sm_payment_collection.total_inv_amount,db.sm_payment_collection.collection_amount,db.sm_payment_collection.payment_type,db.sm_payment_collection.d_man_name,db.sm_payment_collection.transaction_type,db.sm_payment_collection.transaction_cause,db.sm_payment_collection.collection_note,orderby=~db.sm_payment_collection.payment_collection_date|~db.sm_payment_collection.id)
    
    
    #-------------    
    myString='3.1-B AR-Adjustment\n'
    if coll_mrno!='':
        myString+='MR. No'+','+str(coll_mrno)+'\n'
    else:
        if coll_inv_sl_from!='' and coll_inv_sl_to!='':
            myString+='INV.No '+',From:'+str(coll_inv_sl_from)+',To:'+str(coll_inv_sl_to)+'\n'
        else:
            myString+='Rec. Date From:,'+str(startDt)+'\n'            
            myString+='To Date:'+','+str(endDt)+'\n'
            
    myString+='Branch ID:,'+str(depot_id)+'\n'
    myString+='Branch Name'+','+str(depot_name)+'\n'
    myString+='Store ID:,'+str(store_id)+'\n'
    myString+='Store Name'+','+str(store_name)+'\n'
    myString+='DP ID:,'+str(delivery_man_id)+'\n'
    myString+='DP Name'+','+str(delivery_man_name)+'\n'
    myString+='Territory ID:,'+str(territory_id)+'\n'
    myString+='Territory Name'+','+str(territory_name)+'\n'
    myString+='MSO ID:,'+str(mso_id)+'\n'
    myString+='MSO Name'+','+str(mso_name)+'\n'
    
    if coll_inv_term=='':
        coll_inv_term='ALL'
    else:
        if coll_inv_term=='CREDIT':
            if coll_credit_type=='':
                coll_credit_type='ALL'
    if coll_payment_mode=='':
        coll_payment_mode='ALL'    
    
    myString+='Invoice Term:,'+str(coll_inv_term)+'\n'
    myString+='Credit Type:,'+str(coll_credit_type)+'\n'
    myString+='Payment Type:,'+str(coll_payment_mode)+'\n'
    myString+='Cause:,'+str(coll_adjustment_cause)+'\n'
    
    
    totalApAmount=0
    sl=0
    myString+='Sl.No,MR.No,Inv.SL/Ref.No,Doc Date,Cust. Name,Inv Amount,Applied Amt,Pay Type,Cause,Payment Description,Deliveryman Name'+'\n'
    for row in records:
        sl+=1        
        mrNo=row.id
        invSl=str(session.prefix_invoice)+'INV'+str(row.depot_id)+'-'+str(row.sl)
        payment_collection_date=row.payment_collection_date        
        client_name=row.client_name
        total_inv_amount=row.total_inv_amount
        collection_amount=row.collection_amount
        totalApAmount+=collection_amount
                                                          
        payment_type=row.payment_type
        
        if row.transaction_cause=='':
            transaction_type=row.transaction_type
        else:
            transaction_type=str(row.transaction_type)+';'+str(row.transaction_cause)
        
        collection_note=row.collection_note
        d_man_name=row.d_man_name
            
        #------------------------        
        myString+=str(sl)+','+str(mrNo)+','+str(invSl)+','+str(payment_collection_date)+','+str(client_name)+','+str(total_inv_amount)+','+str(collection_amount)+','+\
        str(payment_type)+','+str(transaction_type)+','+str(collection_note)+','+str(d_man_name)+'\n'
     
    myString+='Total,,,,,,'+str(round(totalApAmount,2))+'\n\n\n'
    
    myString+='TAKA,'+str(round(totalApAmount,2))+'\n'
    
    try:
        inword=num2word(str(totalApAmount))
    except:
        inword='-'
    
    myString+='Taka in Words:,'+str(inword)+'\n'
    
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_ARAdjustment.csv'   
    return str(myString)

    
    

def collTransactionWise():
    c_id=session.cid
    
    response.title='Collection Invoice Wise'

    fromDate=request.vars.fromDate
    toDate=request.vars.toDate    
    
    depot_id=str(request.vars.depotID).strip()
    store_id=str(request.vars.storeID).strip()
    
    depot_name=str(request.vars.depotName).strip()
    store_name=str(request.vars.storeName).strip()
    
    
    delivery_man_id=str(request.vars.deliveryManID).strip()
    delivery_man_name=str(request.vars.deliveryManName).strip()
    
    territory_id=str(request.vars.territoryID).strip()
    territory_name=str(request.vars.territoryName).strip()
    
    mso_id=str(request.vars.msoID).strip()
    mso_name=str(request.vars.msoName).strip()

    
    startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d')    
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d')+datetime.timedelta(days=1)
    
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    qset=db()
    qset=qset(db.sm_payment_collection.cid==c_id)
    qset=qset(db.sm_payment_collection.depot_id==depot_id)
    qset=qset(db.sm_payment_collection.store_id==store_id)
    qset=qset((db.sm_payment_collection.collection_date>=startDt)&(db.sm_payment_collection.collection_date<endDt))    
    qset=qset(db.sm_payment_collection.status=='Posted')
    
    if delivery_man_id!='':
        qset=qset(db.sm_payment_collection.d_man_id==delivery_man_id)
    if territory_id!='':
        qset=qset(db.sm_payment_collection.area_id==territory_id)
    if mso_id!='':
        qset=qset(db.sm_payment_collection.rep_id==mso_id)
        
    records=qset.select(db.sm_payment_collection.collection_date,db.sm_payment_collection.invoice_date,db.sm_payment_collection.sl,db.sm_payment_collection.client_id,db.sm_payment_collection.client_name,db.sm_payment_collection.area_id,db.sm_payment_collection.rep_name,db.sm_payment_collection.d_man_name,db.sm_payment_collection.total_inv_amount,db.sm_payment_collection.receivable_amount,db.sm_payment_collection.collection_amount,orderby=~db.sm_payment_collection.collection_date,limitby=limitby)
    
    recordsTotal=qset.select(db.sm_payment_collection.cid,db.sm_payment_collection.total_inv_amount.sum(),db.sm_payment_collection.receivable_amount.sum(),db.sm_payment_collection.collection_amount.sum(),groupby=db.sm_payment_collection.cid)
    
    return dict(recordsTotal=recordsTotal,records=records,fromDate=fromDate,toDate=toDate,depotID=depot_id,depotName=depot_name,storeID=store_id,storeName=store_name,deliveryManID=delivery_man_id,deliveryManName=delivery_man_name,territoryID=territory_id,territoryName=territory_name,msoID=mso_id,msoName=mso_name,page=page,items_per_page=items_per_page)    
    
def collCustomerWise():
    c_id=session.cid
    
    response.title='Collection Customer Wise'

    fromDate=request.vars.fromDate
    toDate=request.vars.toDate    
    
    depot_id=str(request.vars.depotID).strip()
    store_id=str(request.vars.storeID).strip()
    
    depot_name=str(request.vars.depotName).strip()
    store_name=str(request.vars.storeName).strip()
    
    delivery_man_id=str(request.vars.deliveryManID).strip()
    delivery_man_name=str(request.vars.deliveryManName).strip()
    
    territory_id=str(request.vars.territoryID).strip()
    territory_name=str(request.vars.territoryName).strip()
    
    mso_id=str(request.vars.msoID).strip()
    mso_name=str(request.vars.msoName).strip()
    
    startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d')    
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d')+datetime.timedelta(days=1)
    
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    qset=db()
    qset=qset(db.sm_payment_collection.cid==c_id)
    qset=qset(db.sm_payment_collection.depot_id==depot_id)
    qset=qset(db.sm_payment_collection.store_id==store_id)
    qset=qset((db.sm_payment_collection.collection_date>=startDt)&(db.sm_payment_collection.collection_date<endDt))    
    qset=qset(db.sm_payment_collection.status=='Posted')
    
    if delivery_man_id!='':
        qset=qset(db.sm_payment_collection.d_man_id==delivery_man_id)
    if territory_id!='':
        qset=qset(db.sm_payment_collection.area_id==territory_id)
    if mso_id!='':
        qset=qset(db.sm_payment_collection.rep_id==mso_id)
    
    records=qset.select(db.sm_payment_collection.client_id,db.sm_payment_collection.client_name,db.sm_payment_collection.area_id,db.sm_payment_collection.rep_name,db.sm_payment_collection.d_man_name,db.sm_payment_collection.total_inv_amount,db.sm_payment_collection.receivable_amount,db.sm_payment_collection.collection_amount,orderby=db.sm_payment_collection.client_id,limitby=limitby)
    
    recordsTotal=qset.select(db.sm_payment_collection.cid,db.sm_payment_collection.total_inv_amount.sum(),db.sm_payment_collection.receivable_amount.sum(),db.sm_payment_collection.collection_amount.sum(),groupby=db.sm_payment_collection.cid)
    
    return dict(recordsTotal=recordsTotal,records=records,fromDate=fromDate,toDate=toDate,depotID=depot_id,depotName=depot_name,storeID=store_id,storeName=store_name,deliveryManID=delivery_man_id,deliveryManName=delivery_man_name,territoryID=territory_id,territoryName=territory_name,msoID=mso_id,msoName=mso_name,page=page,items_per_page=items_per_page)    


def collInvoiceWise():
    c_id=session.cid
    
    response.title='Collection Invoice Wise'

    fromDate=request.vars.fromDate
    toDate=request.vars.toDate    
    
    depot_id=str(request.vars.depotID).strip()
    store_id=str(request.vars.storeID).strip()
    
    depot_name=str(request.vars.depotName).strip()
    store_name=str(request.vars.storeName).strip()
    
    
    delivery_man_id=str(request.vars.deliveryManID).strip()
    delivery_man_name=str(request.vars.deliveryManName).strip()
    
    territory_id=str(request.vars.territoryID).strip()
    territory_name=str(request.vars.territoryName).strip()
    
    mso_id=str(request.vars.msoID).strip()
    mso_name=str(request.vars.msoName).strip()

    
    startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d')    
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d')+datetime.timedelta(days=1)
       
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    qset=db()
    qset=qset(db.sm_payment_collection.cid==c_id)
    qset=qset(db.sm_payment_collection.depot_id==depot_id)
    qset=qset(db.sm_payment_collection.store_id==store_id)
    qset=qset((db.sm_payment_collection.collection_date>=startDt)&(db.sm_payment_collection.collection_date<endDt))    
    qset=qset(db.sm_payment_collection.status=='Posted')
    
    if delivery_man_id!='':
        qset=qset(db.sm_payment_collection.d_man_id==delivery_man_id)
    if territory_id!='':
        qset=qset(db.sm_payment_collection.area_id==territory_id)
    if mso_id!='':
        qset=qset(db.sm_payment_collection.rep_id==mso_id)
    
    records=qset.select(db.sm_payment_collection.collection_date,db.sm_payment_collection.head_rowid,db.sm_payment_collection.invoice_date.max(),db.sm_payment_collection.sl.max(),db.sm_payment_collection.client_id.max(),db.sm_payment_collection.client_name.max(),db.sm_payment_collection.area_id.max(),db.sm_payment_collection.rep_name.max(),db.sm_payment_collection.d_man_name.max(),db.sm_payment_collection.total_inv_amount.sum(),db.sm_payment_collection.receivable_amount.sum(),db.sm_payment_collection.collection_amount.sum(),groupby=db.sm_payment_collection.collection_date|db.sm_payment_collection.head_rowid,orderby=~db.sm_payment_collection.collection_date,limitby=limitby)
    
    recordsTotal=qset.select(db.sm_payment_collection.cid,db.sm_payment_collection.total_inv_amount.sum(),db.sm_payment_collection.receivable_amount.sum(),db.sm_payment_collection.collection_amount.sum(),groupby=db.sm_payment_collection.cid)
    
    return dict(recordsTotal=recordsTotal,records=records,fromDate=fromDate,toDate=toDate,depotID=depot_id,depotName=depot_name,storeID=store_id,storeName=store_name,deliveryManID=delivery_man_id,deliveryManName=delivery_man_name,territoryID=territory_id,territoryName=territory_name,msoID=mso_id,msoName=mso_name,page=page,items_per_page=items_per_page)    


def outStRsmFmMsoWise():
    c_id=session.cid
    
    response.title='6.9A Outstanding RSM/FM/MSO Wise'
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    depot_id=str(request.vars.depotID).strip()
    store_id=str(request.vars.storeID).strip()    
    out_st_delivery_man_id=str(request.vars.deliveryManID).strip()    
    out_st_territory_id=str(request.vars.territoryID).strip()    
    out_st_mso_id=str(request.vars.msoID).strip()
    invoice_term=str(request.vars.invoice_term).strip()
    customerId=str(request.vars.customerId).strip()
    
    credit_type=str(request.vars.credit_type).strip()
    customer_cat=str(request.vars.customer_cat).strip() 
    customer_sub_cat=str(request.vars.customer_sub_cat).strip()    
    
    out_st_level1_id=str(request.vars.out_st_level1_id).strip()  
    out_st_level2_id=str(request.vars.out_st_level2_id).strip()  
    
    catName=''
    custCatRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_CATEGORY')&(db.sm_category_type.cat_type_id==customer_cat)).select(db.sm_category_type.cat_type_name, limitby=(0,1))
    if custCatRows:
        catName=custCatRows[0].cat_type_name        
    subCatName=''
    custSubCatRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_SUB_CATEGORY')&(db.sm_category_type.cat_type_id==customer_sub_cat)).select(db.sm_category_type.cat_type_name, limitby=(0,1))
    if custSubCatRows:
        subCatName=custSubCatRows[0].cat_type_name
    
    depot_name=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depot_name=depotRow[0].name
    
    store_name=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        store_name=storeRow[0].store_name
        
    out_st_delivery_man_name=''
    dpRow=db((db.sm_delivery_man.cid==c_id)&(db.sm_delivery_man.depot_id==depot_id)&(db.sm_delivery_man.d_man_id==out_st_delivery_man_id)).select(db.sm_delivery_man.name,limitby=(0,1))
    if dpRow:
        out_st_delivery_man_name=dpRow[0].name
        
    out_st_territory_name=''
    levelRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==out_st_territory_id)).select(db.sm_level.level_name,limitby=(0,1))
    if levelRow:
        out_st_territory_name=levelRow[0].level_name
        
    out_st_mso_name=''
    repRow=db((db.sm_rep.cid==c_id)&(db.sm_rep.rep_id==out_st_mso_id)).select(db.sm_rep.name,limitby=(0,1))
    if repRow:
        out_st_mso_name=repRow[0].name
    
    customerName=''
    clientRow=db((db.sm_client.cid==c_id)&(db.sm_client.depot_id==depot_id)&(db.sm_client.client_id==customerId)).select(db.sm_client.name,limitby=(0,1))
    if clientRow:
        customerName=clientRow[0].name
       
    try:        
        startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d').strftime('%Y-%m-%d')
    except:
        startDt=''                
        
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d').strftime('%Y-%m-%d')
    
    currentMonth=str(toDate)[0:7] + '-01'
    currentMonthFDate = datetime.datetime.strptime(str(currentMonth), '%Y-%m-%d')
    last_1_month = sub_months(currentMonthFDate, 1)
    last_2_month = sub_months(currentMonthFDate, 2)
    last_3_month = sub_months(currentMonthFDate, 3)
    last_4_month = sub_months(currentMonthFDate, 4)
    last_5_month = sub_months(currentMonthFDate, 5)
    last_6_month = sub_months(currentMonthFDate, 6) 
    
    
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    
    condStr=" AND (round(total_amount-(return_tp+return_vat-return_discount)-collection_amount,2)!=0)"
    
    if out_st_delivery_man_id!='':
        condStr+=" AND (d_man_id='"+out_st_delivery_man_id+"')"        
    if out_st_territory_id!='':
        condStr+=" AND (area_id='"+out_st_territory_id+"')"        
    if out_st_mso_id!='':
        condStr+=" AND (rep_id='"+out_st_mso_id+"')"        
    if invoice_term!='':
        condStr+=" AND (payment_mode='"+invoice_term+"')"
    if customerId!='':
        condStr+=" AND (client_id='"+customerId+"')"
        
    if credit_type!='':
        condStr+=" AND (credit_note='"+credit_type+"')"
    if customer_cat!='':
        condStr+=" AND (cl_category_id='"+customer_cat+"')"
    if customer_sub_cat!='':
        condStr+=" AND (cl_sub_category_id='"+customer_sub_cat+"')"
        
    if out_st_level1_id!='':
        condStr+=" AND (level1_id='"+out_st_level1_id+"')"        
    if out_st_level2_id!='':
        condStr+=" AND (level2_id='"+out_st_level2_id+"')"
        
    if currentMonthFDate!='':
        sqlRecordsHead="SELECT level1_id,level2_id,level3_id,client_id,MAX(client_name) as client_name,concat(level3_id,'-',client_id) as headID,0 as 'monthL0',0 as 'monthL1',0 as 'monthL2',0 as 'monthL3',0 as 'monthL4',0 as 'monthL5',0 as 'monthL6',0 as 'monthLE' FROM sm_invoice_head WHERE ((cid = '"+c_id+"') AND (depot_id='"+depot_id+"') AND (store_id='"+store_id+"') AND (invoice_ym_date <= '"+str(currentMonthFDate)+"') AND (status='Invoiced') "+str(condStr)+") GROUP BY level1_id,level2_id,level3_id,client_id ORDER BY level1_id,level2_id,level3_id,client_id"
        sqlRecords_0="SELECT concat(level3_id,'-',client_id) as detailID,round(SUM(actual_total_tp-(return_tp+return_sp_discount)+(vat_total_amount-return_vat)-(discount-return_discount)-(sp_discount-return_sp_discount)-collection_amount),2) as ost0Amt FROM sm_invoice_head WHERE ((cid = '"+c_id+"') AND (depot_id='"+depot_id+"') AND (store_id='"+store_id+"') AND (invoice_ym_date = '"+str(currentMonthFDate)+"') AND (status='Invoiced') "+str(condStr)+") GROUP BY level1_id,level2_id,level3_id,client_id ORDER BY level1_id,level2_id,level3_id,client_id"
        sqlRecords_1="SELECT concat(level3_id,'-',client_id) as detailID,round(SUM(actual_total_tp-(return_tp+return_sp_discount)+(vat_total_amount-return_vat)-(discount-return_discount)-(sp_discount-return_sp_discount)-collection_amount),2) as ost1Amt FROM sm_invoice_head WHERE ((cid = '"+c_id+"') AND (depot_id='"+depot_id+"') AND (store_id='"+store_id+"') AND (invoice_ym_date = '"+str(last_1_month)+"') AND (status='Invoiced') "+str(condStr)+") GROUP BY level1_id,level2_id,level3_id,client_id ORDER BY level1_id,level2_id,level3_id,client_id"
        sqlRecords_2="SELECT concat(level3_id,'-',client_id) as detailID,round(SUM(actual_total_tp-(return_tp+return_sp_discount)+(vat_total_amount-return_vat)-(discount-return_discount)-(sp_discount-return_sp_discount)-collection_amount),2) as ost2Amt FROM sm_invoice_head WHERE ((cid = '"+c_id+"') AND (depot_id='"+depot_id+"') AND (store_id='"+store_id+"') AND (invoice_ym_date = '"+str(last_2_month)+"') AND (status='Invoiced') "+str(condStr)+") GROUP BY level1_id,level2_id,level3_id,client_id ORDER BY level1_id,level2_id,level3_id,client_id"
        sqlRecords_3="SELECT concat(level3_id,'-',client_id) as detailID,round(SUM(actual_total_tp-(return_tp+return_sp_discount)+(vat_total_amount-return_vat)-(discount-return_discount)-(sp_discount-return_sp_discount)-collection_amount),2) as ost3Amt FROM sm_invoice_head WHERE ((cid = '"+c_id+"') AND (depot_id='"+depot_id+"') AND (store_id='"+store_id+"') AND (invoice_ym_date = '"+str(last_3_month)+"') AND (status='Invoiced') "+str(condStr)+") GROUP BY level1_id,level2_id,level3_id,client_id ORDER BY level1_id,level2_id,level3_id,client_id"
        sqlRecords_4="SELECT concat(level3_id,'-',client_id) as detailID,round(SUM(actual_total_tp-(return_tp+return_sp_discount)+(vat_total_amount-return_vat)-(discount-return_discount)-(sp_discount-return_sp_discount)-collection_amount),2) as ost4Amt FROM sm_invoice_head WHERE ((cid = '"+c_id+"') AND (depot_id='"+depot_id+"') AND (store_id='"+store_id+"') AND (invoice_ym_date = '"+str(last_4_month)+"') AND (status='Invoiced') "+str(condStr)+") GROUP BY level1_id,level2_id,level3_id,client_id ORDER BY level1_id,level2_id,level3_id,client_id"
        sqlRecords_5="SELECT concat(level3_id,'-',client_id) as detailID,round(SUM(actual_total_tp-(return_tp+return_sp_discount)+(vat_total_amount-return_vat)-(discount-return_discount)-(sp_discount-return_sp_discount)-collection_amount),2) as ost5Amt FROM sm_invoice_head WHERE ((cid = '"+c_id+"') AND (depot_id='"+depot_id+"') AND (store_id='"+store_id+"') AND (invoice_ym_date = '"+str(last_5_month)+"') AND (status='Invoiced') "+str(condStr)+") GROUP BY level1_id,level2_id,level3_id,client_id ORDER BY level1_id,level2_id,level3_id,client_id"
        sqlRecords_6="SELECT concat(level3_id,'-',client_id) as detailID,round(SUM(actual_total_tp-(return_tp+return_sp_discount)+(vat_total_amount-return_vat)-(discount-return_discount)-(sp_discount-return_sp_discount)-collection_amount),2) as ost6Amt FROM sm_invoice_head WHERE ((cid = '"+c_id+"') AND (depot_id='"+depot_id+"') AND (store_id='"+store_id+"') AND (invoice_ym_date = '"+str(last_6_month)+"') AND (status='Invoiced') "+str(condStr)+") GROUP BY level1_id,level2_id,level3_id,client_id ORDER BY level1_id,level2_id,level3_id,client_id"
        sqlRecords_e="SELECT concat(level3_id,'-',client_id) as detailID,round(SUM(actual_total_tp-(return_tp+return_sp_discount)+(vat_total_amount-return_vat)-(discount-return_discount)-(sp_discount-return_sp_discount)-collection_amount),2) as ostEAmt FROM sm_invoice_head WHERE ((cid = '"+c_id+"') AND (depot_id='"+depot_id+"') AND (store_id='"+store_id+"') AND (invoice_ym_date < '"+str(last_6_month)+"') AND (status='Invoiced') "+str(condStr)+") GROUP BY level1_id,level2_id,level3_id,client_id ORDER BY level1_id,level2_id,level3_id,client_id"
    else:
        sqlRecords_0=""
        sqlRecords_1=""
        sqlRecords_2=""
        sqlRecords_3=""
        sqlRecords_4=""
        sqlRecords_5=""
        sqlRecords_6=""
        sqlRecords_e=""
        
    recordsHeadList=db.executesql(sqlRecordsHead,as_dict = True)
    #recordsHeadList.sort(key=itemgetter('headID'), reverse=False)
    
    #month-0
    recordsList_0=db.executesql(sqlRecords_0,as_dict = True)
    #recordsList_0.sort(key=itemgetter('detailID'), reverse=False)    
    for i in range(len(recordsList_0)):
        detDictData_0=recordsList_0[i]
        detailID=detDictData_0['detailID']
        
        for j in range(len(recordsHeadList)):
            headDictData=recordsHeadList[j]
            headID=headDictData['headID']
            if headID==detailID:
                headDictData['monthL0']=detDictData_0['ost0Amt']
                break
                
    #month-1
    recordsList_1=db.executesql(sqlRecords_1,as_dict = True)
    #recordsList_1.sort(key=itemgetter('detailID'), reverse=False)    
    for i in range(len(recordsList_1)):
        detDictData_1=recordsList_1[i]
        detailID=detDictData_1['detailID']
        
        for j in range(len(recordsHeadList)):
            headDictData=recordsHeadList[j]
            headID=headDictData['headID']
            if headID==detailID:
                headDictData['monthL1']=detDictData_1['ost1Amt']
                break
    
    #month-2
    recordsList_2=db.executesql(sqlRecords_2,as_dict = True)
    #recordsList_2.sort(key=itemgetter('detailID'), reverse=False)    
    for i in range(len(recordsList_2)):
        detDictData_2=recordsList_2[i]
        detailID=detDictData_2['detailID']
        
        for j in range(len(recordsHeadList)):
            headDictData=recordsHeadList[j]
            headID=headDictData['headID']
            if headID==detailID:
                headDictData['monthL2']=detDictData_2['ost2Amt']
                break
    
    #month-3
    recordsList_3=db.executesql(sqlRecords_3,as_dict = True)
    #recordsList_3.sort(key=itemgetter('detailID'), reverse=False)    
    for i in range(len(recordsList_3)):
        detDictData_3=recordsList_3[i]
        detailID=detDictData_3['detailID']
        
        for j in range(len(recordsHeadList)):
            headDictData=recordsHeadList[j]
            headID=headDictData['headID']
            if headID==detailID:
                headDictData['monthL3']=detDictData_3['ost3Amt']
                break
    
    #month-4
    recordsList_4=db.executesql(sqlRecords_4,as_dict = True)
    #recordsList_4.sort(key=itemgetter('detailID'), reverse=False)    
    for i in range(len(recordsList_4)):
        detDictData_4=recordsList_4[i]
        detailID=detDictData_4['detailID']
        
        for j in range(len(recordsHeadList)):
            headDictData=recordsHeadList[j]
            headID=headDictData['headID']
            if headID==detailID:
                headDictData['monthL4']=detDictData_4['ost4Amt']
                break
    
    #month-5
    recordsList_5=db.executesql(sqlRecords_5,as_dict = True)
    #recordsList_5.sort(key=itemgetter('detailID'), reverse=False)    
    for i in range(len(recordsList_5)):
        detDictData_5=recordsList_5[i]
        detailID=detDictData_5['detailID']
        
        for j in range(len(recordsHeadList)):
            headDictData=recordsHeadList[j]
            headID=headDictData['headID']
            if headID==detailID:
                headDictData['monthL5']=detDictData_5['ost5Amt']
                break
    
    #month-6
    recordsList_6=db.executesql(sqlRecords_6,as_dict = True)
    #recordsList_6.sort(key=itemgetter('detailID'), reverse=False)    
    for i in range(len(recordsList_6)):
        detDictData_6=recordsList_6[i]
        detailID=detDictData_6['detailID']
        
        for j in range(len(recordsHeadList)):
            headDictData=recordsHeadList[j]
            headID=headDictData['headID']
            if headID==detailID:
                headDictData['monthL6']=detDictData_6['ost6Amt']
                break
    #month-e
    recordsList_e=db.executesql(sqlRecords_e,as_dict = True)
    #recordsList_e.sort(key=itemgetter('detailID'), reverse=False)    
    for i in range(len(recordsList_e)):
        detDictData_e=recordsList_e[i]
        detailID=detDictData_e['detailID']
        
        for j in range(len(recordsHeadList)):
            headDictData=recordsHeadList[j]
            headID=headDictData['headID']
            if headID==detailID:
                headDictData['monthLE']=detDictData_e['ostEAmt']
                break
            
    return dict(recordsHeadList=recordsHeadList,fromDate=startDt,toDate=endDt,depotID=depot_id,depotName=depot_name,storeID=store_id,storeName=store_name,deliveryManID=out_st_delivery_man_id,deliveryManName=out_st_delivery_man_name,territoryID=out_st_territory_id,territoryName=out_st_territory_name,msoID=out_st_mso_id,msoName=out_st_mso_name,invoice_term=invoice_term,customerId=customerId,customerName=customerName,credit_type=credit_type,customer_cat=customer_cat,customer_sub_cat=customer_sub_cat,catName=catName,subCatName=subCatName,out_st_level1_id=out_st_level1_id,out_st_level2_id=out_st_level2_id,page=page,items_per_page=items_per_page)    

def outStRsmFmMsoWise_download():
    c_id=session.cid
    
    response.title='6.9A Download-Outstanding RSM/FM/MSO Wise'
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    depot_id=str(request.vars.depotID).strip()
    store_id=str(request.vars.storeID).strip()    
    out_st_delivery_man_id=str(request.vars.deliveryManID).strip()    
    out_st_territory_id=str(request.vars.territoryID).strip()    
    out_st_mso_id=str(request.vars.msoID).strip()
    invoice_term=str(request.vars.invoice_term).strip()
    customerId=str(request.vars.customerId).strip()
    
    credit_type=str(request.vars.credit_type).strip()
    customer_cat=str(request.vars.customer_cat).strip() 
    customer_sub_cat=str(request.vars.customer_sub_cat).strip()    
    
    out_st_level1_id=str(request.vars.out_st_level1_id).strip()  
    out_st_level2_id=str(request.vars.out_st_level2_id).strip()  
    
    catName=''
    custCatRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_CATEGORY')&(db.sm_category_type.cat_type_id==customer_cat)).select(db.sm_category_type.cat_type_name, limitby=(0,1))
    if custCatRows:
        catName=custCatRows[0].cat_type_name        
    subCatName=''
    custSubCatRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_SUB_CATEGORY')&(db.sm_category_type.cat_type_id==customer_sub_cat)).select(db.sm_category_type.cat_type_name, limitby=(0,1))
    if custSubCatRows:
        subCatName=custSubCatRows[0].cat_type_name
    
    depot_name=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depot_name=depotRow[0].name
    
    store_name=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        store_name=storeRow[0].store_name
        
    out_st_delivery_man_name=''
    dpRow=db((db.sm_delivery_man.cid==c_id)&(db.sm_delivery_man.depot_id==depot_id)&(db.sm_delivery_man.d_man_id==out_st_delivery_man_id)).select(db.sm_delivery_man.name,limitby=(0,1))
    if dpRow:
        out_st_delivery_man_name=dpRow[0].name
        
    out_st_territory_name=''
    levelRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==out_st_territory_id)).select(db.sm_level.level_name,limitby=(0,1))
    if levelRow:
        out_st_territory_name=levelRow[0].level_name
        
    out_st_mso_name=''
    repRow=db((db.sm_rep.cid==c_id)&(db.sm_rep.rep_id==out_st_mso_id)).select(db.sm_rep.name,limitby=(0,1))
    if repRow:
        out_st_mso_name=repRow[0].name
        
    customerName=''
    clientRow=db((db.sm_client.cid==c_id)&(db.sm_client.depot_id==depot_id)&(db.sm_client.client_id==customerId)).select(db.sm_client.name,limitby=(0,1))
    if clientRow:
        customerName=clientRow[0].name
       
    try:        
        startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d').strftime('%Y-%m-%d')
    except:
        startDt=''                
        
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d').strftime('%Y-%m-%d')
    
    currentMonth=str(toDate)[0:7] + '-01'
    currentMonthFDate = datetime.datetime.strptime(str(currentMonth), '%Y-%m-%d')
    last_1_month = sub_months(currentMonthFDate, 1)
    last_2_month = sub_months(currentMonthFDate, 2)
    last_3_month = sub_months(currentMonthFDate, 3)
    last_4_month = sub_months(currentMonthFDate, 4)
    last_5_month = sub_months(currentMonthFDate, 5)
    last_6_month = sub_months(currentMonthFDate, 6) 
    
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    
    condStr=" AND (round(total_amount-(return_tp+return_vat-return_discount)-collection_amount,2)!=0)"
    
    if out_st_delivery_man_id!='':
        condStr+=" AND (d_man_id='"+out_st_delivery_man_id+"')"        
    if out_st_territory_id!='':
        condStr+=" AND (area_id='"+out_st_territory_id+"')"        
    if out_st_mso_id!='':
        condStr+=" AND (rep_id='"+out_st_mso_id+"')"        
    if invoice_term!='':
        condStr+=" AND (payment_mode='"+invoice_term+"')"
    if customerId!='':
        condStr+=" AND (client_id='"+customerId+"')"
        
    if credit_type!='':
        condStr+=" AND (credit_note='"+credit_type+"')"
    if customer_cat!='':
        condStr+=" AND (cl_category_id='"+customer_cat+"')"
    if customer_sub_cat!='':
        condStr+=" AND (cl_sub_category_id='"+customer_sub_cat+"')"
        
    if out_st_level1_id!='':
        condStr+=" AND (level1_id='"+out_st_level1_id+"')"        
    if out_st_level2_id!='':
        condStr+=" AND (level2_id='"+out_st_level2_id+"')"
        
    if currentMonthFDate!='':
        sqlRecordsHead="SELECT level1_id,level2_id,level3_id,client_id,MAX(client_name) as client_name,concat(level3_id,'-',client_id) as headID,0 as 'monthL0',0 as 'monthL1',0 as 'monthL2',0 as 'monthL3',0 as 'monthL4',0 as 'monthL5',0 as 'monthL6',0 as 'monthLE' FROM sm_invoice_head WHERE ((cid = '"+c_id+"') AND (depot_id='"+depot_id+"') AND (store_id='"+store_id+"') AND (invoice_ym_date <= '"+str(currentMonthFDate)+"') AND (status='Invoiced') "+str(condStr)+") GROUP BY level1_id,level2_id,level3_id,client_id ORDER BY level1_id,level2_id,level3_id,client_id"
        sqlRecords_0="SELECT concat(level3_id,'-',client_id) as detailID,round(SUM(actual_total_tp-(return_tp+return_sp_discount)+(vat_total_amount-return_vat)-(discount-return_discount)-(sp_discount-return_sp_discount)-collection_amount),2) as ost0Amt FROM sm_invoice_head WHERE ((cid = '"+c_id+"') AND (depot_id='"+depot_id+"') AND (store_id='"+store_id+"') AND (invoice_ym_date = '"+str(currentMonthFDate)+"') AND (status='Invoiced') "+str(condStr)+") GROUP BY level1_id,level2_id,level3_id,client_id ORDER BY level1_id,level2_id,level3_id,client_id"
        sqlRecords_1="SELECT concat(level3_id,'-',client_id) as detailID,round(SUM(actual_total_tp-(return_tp+return_sp_discount)+(vat_total_amount-return_vat)-(discount-return_discount)-(sp_discount-return_sp_discount)-collection_amount),2) as ost1Amt FROM sm_invoice_head WHERE ((cid = '"+c_id+"') AND (depot_id='"+depot_id+"') AND (store_id='"+store_id+"') AND (invoice_ym_date = '"+str(last_1_month)+"') AND (status='Invoiced') "+str(condStr)+") GROUP BY level1_id,level2_id,level3_id,client_id ORDER BY level1_id,level2_id,level3_id,client_id"
        sqlRecords_2="SELECT concat(level3_id,'-',client_id) as detailID,round(SUM(actual_total_tp-(return_tp+return_sp_discount)+(vat_total_amount-return_vat)-(discount-return_discount)-(sp_discount-return_sp_discount)-collection_amount),2) as ost2Amt FROM sm_invoice_head WHERE ((cid = '"+c_id+"') AND (depot_id='"+depot_id+"') AND (store_id='"+store_id+"') AND (invoice_ym_date = '"+str(last_2_month)+"') AND (status='Invoiced') "+str(condStr)+") GROUP BY level1_id,level2_id,level3_id,client_id ORDER BY level1_id,level2_id,level3_id,client_id"
        sqlRecords_3="SELECT concat(level3_id,'-',client_id) as detailID,round(SUM(actual_total_tp-(return_tp+return_sp_discount)+(vat_total_amount-return_vat)-(discount-return_discount)-(sp_discount-return_sp_discount)-collection_amount),2) as ost3Amt FROM sm_invoice_head WHERE ((cid = '"+c_id+"') AND (depot_id='"+depot_id+"') AND (store_id='"+store_id+"') AND (invoice_ym_date = '"+str(last_3_month)+"') AND (status='Invoiced') "+str(condStr)+") GROUP BY level1_id,level2_id,level3_id,client_id ORDER BY level1_id,level2_id,level3_id,client_id"
        sqlRecords_4="SELECT concat(level3_id,'-',client_id) as detailID,round(SUM(actual_total_tp-(return_tp+return_sp_discount)+(vat_total_amount-return_vat)-(discount-return_discount)-(sp_discount-return_sp_discount)-collection_amount),2) as ost4Amt FROM sm_invoice_head WHERE ((cid = '"+c_id+"') AND (depot_id='"+depot_id+"') AND (store_id='"+store_id+"') AND (invoice_ym_date = '"+str(last_4_month)+"') AND (status='Invoiced') "+str(condStr)+") GROUP BY level1_id,level2_id,level3_id,client_id ORDER BY level1_id,level2_id,level3_id,client_id"
        sqlRecords_5="SELECT concat(level3_id,'-',client_id) as detailID,round(SUM(actual_total_tp-(return_tp+return_sp_discount)+(vat_total_amount-return_vat)-(discount-return_discount)-(sp_discount-return_sp_discount)-collection_amount),2) as ost5Amt FROM sm_invoice_head WHERE ((cid = '"+c_id+"') AND (depot_id='"+depot_id+"') AND (store_id='"+store_id+"') AND (invoice_ym_date = '"+str(last_5_month)+"') AND (status='Invoiced') "+str(condStr)+") GROUP BY level1_id,level2_id,level3_id,client_id ORDER BY level1_id,level2_id,level3_id,client_id"
        sqlRecords_6="SELECT concat(level3_id,'-',client_id) as detailID,round(SUM(actual_total_tp-(return_tp+return_sp_discount)+(vat_total_amount-return_vat)-(discount-return_discount)-(sp_discount-return_sp_discount)-collection_amount),2) as ost6Amt FROM sm_invoice_head WHERE ((cid = '"+c_id+"') AND (depot_id='"+depot_id+"') AND (store_id='"+store_id+"') AND (invoice_ym_date = '"+str(last_6_month)+"') AND (status='Invoiced') "+str(condStr)+") GROUP BY level1_id,level2_id,level3_id,client_id ORDER BY level1_id,level2_id,level3_id,client_id"
        sqlRecords_e="SELECT concat(level3_id,'-',client_id) as detailID,round(SUM(actual_total_tp-(return_tp+return_sp_discount)+(vat_total_amount-return_vat)-(discount-return_discount)-(sp_discount-return_sp_discount)-collection_amount),2) as ostEAmt FROM sm_invoice_head WHERE ((cid = '"+c_id+"') AND (depot_id='"+depot_id+"') AND (store_id='"+store_id+"') AND (invoice_ym_date < '"+str(last_6_month)+"') AND (status='Invoiced') "+str(condStr)+") GROUP BY level1_id,level2_id,level3_id,client_id ORDER BY level1_id,level2_id,level3_id,client_id"
    else:
        sqlRecords_0=""
        sqlRecords_1=""
        sqlRecords_2=""
        sqlRecords_3=""
        sqlRecords_4=""
        sqlRecords_5=""
        sqlRecords_6=""
        sqlRecords_e=""
        
    recordsHeadList=db.executesql(sqlRecordsHead,as_dict = True)
    #recordsHeadList.sort(key=itemgetter('headID'), reverse=False)
    
    #month-0
    recordsList_0=db.executesql(sqlRecords_0,as_dict = True)
    #recordsList_0.sort(key=itemgetter('detailID'), reverse=False)    
    for i in range(len(recordsList_0)):
        detDictData_0=recordsList_0[i]
        detailID=detDictData_0['detailID']
        
        for j in range(len(recordsHeadList)):
            headDictData=recordsHeadList[j]
            headID=headDictData['headID']
            if headID==detailID:
                headDictData['monthL0']=detDictData_0['ost0Amt']
                break
                
    #month-1
    recordsList_1=db.executesql(sqlRecords_1,as_dict = True)
    #recordsList_1.sort(key=itemgetter('detailID'), reverse=False)    
    for i in range(len(recordsList_1)):
        detDictData_1=recordsList_1[i]
        detailID=detDictData_1['detailID']
        
        for j in range(len(recordsHeadList)):
            headDictData=recordsHeadList[j]
            headID=headDictData['headID']
            if headID==detailID:
                headDictData['monthL1']=detDictData_1['ost1Amt']
                break
    
    #month-2
    recordsList_2=db.executesql(sqlRecords_2,as_dict = True)
    #recordsList_2.sort(key=itemgetter('detailID'), reverse=False)    
    for i in range(len(recordsList_2)):
        detDictData_2=recordsList_2[i]
        detailID=detDictData_2['detailID']
        
        for j in range(len(recordsHeadList)):
            headDictData=recordsHeadList[j]
            headID=headDictData['headID']
            if headID==detailID:
                headDictData['monthL2']=detDictData_2['ost2Amt']
                break
    
    #month-3
    recordsList_3=db.executesql(sqlRecords_3,as_dict = True)
    #recordsList_3.sort(key=itemgetter('detailID'), reverse=False)    
    for i in range(len(recordsList_3)):
        detDictData_3=recordsList_3[i]
        detailID=detDictData_3['detailID']
        
        for j in range(len(recordsHeadList)):
            headDictData=recordsHeadList[j]
            headID=headDictData['headID']
            if headID==detailID:
                headDictData['monthL3']=detDictData_3['ost3Amt']
                break
    
    #month-4
    recordsList_4=db.executesql(sqlRecords_4,as_dict = True)
    #recordsList_4.sort(key=itemgetter('detailID'), reverse=False)    
    for i in range(len(recordsList_4)):
        detDictData_4=recordsList_4[i]
        detailID=detDictData_4['detailID']
        
        for j in range(len(recordsHeadList)):
            headDictData=recordsHeadList[j]
            headID=headDictData['headID']
            if headID==detailID:
                headDictData['monthL4']=detDictData_4['ost4Amt']
                break
    
    #month-5
    recordsList_5=db.executesql(sqlRecords_5,as_dict = True)
    #recordsList_5.sort(key=itemgetter('detailID'), reverse=False)    
    for i in range(len(recordsList_5)):
        detDictData_5=recordsList_5[i]
        detailID=detDictData_5['detailID']
        
        for j in range(len(recordsHeadList)):
            headDictData=recordsHeadList[j]
            headID=headDictData['headID']
            if headID==detailID:
                headDictData['monthL5']=detDictData_5['ost5Amt']
                break
    
    #month-6
    recordsList_6=db.executesql(sqlRecords_6,as_dict = True)
    #recordsList_6.sort(key=itemgetter('detailID'), reverse=False)    
    for i in range(len(recordsList_6)):
        detDictData_6=recordsList_6[i]
        detailID=detDictData_6['detailID']
        
        for j in range(len(recordsHeadList)):
            headDictData=recordsHeadList[j]
            headID=headDictData['headID']
            if headID==detailID:
                headDictData['monthL6']=detDictData_6['ost6Amt']
                break
    #month-e
    recordsList_e=db.executesql(sqlRecords_e,as_dict = True)
    #recordsList_e.sort(key=itemgetter('detailID'), reverse=False)    
    for i in range(len(recordsList_e)):
        detDictData_e=recordsList_e[i]
        detailID=detDictData_e['detailID']
        
        for j in range(len(recordsHeadList)):
            headDictData=recordsHeadList[j]
            headID=headDictData['headID']
            if headID==detailID:
                headDictData['monthLE']=detDictData_e['ostEAmt']
                break
    
    #==================================
    myString='6.09A Outstanding List: RSM FM MSO Wise Summary & Details\n'
    myString+='Inv Date From:,'+str(startDt)+'\n'
    myString+='To/ as of Date:'+','+str(endDt)+'\n'
    myString+='Inv Term:,'+str(invoice_term)+'\n'
    myString+='Branch ID:,'+str(depot_id)+'\n'
    myString+='Branch Name'+','+str(depot_name)+'\n'
    myString+='Store ID:,'+str(store_id)+'\n'
    myString+='Store Name'+','+str(store_name)+'\n'
    myString+='DP ID:,'+str(out_st_delivery_man_id)+'\n'
    myString+='DP Name'+','+str(out_st_delivery_man_name)+'\n'
    myString+='Territory ID:,'+str(out_st_territory_id)+'\n'
    myString+='Territory Name'+','+str(out_st_territory_name)+'\n'
    myString+='MSO ID:,'+str(out_st_mso_id)+'\n'
    myString+='MSO Name'+','+str(out_st_mso_name)+'\n'
    myString+='Customer ID:,'+str(customerId)+'\n'
    myString+='Customer Name'+','+str(customerName)+'\n'
    
    myString+='Credit Type:,'+str(credit_type)+'\n'
    if catName=='':
        catName='ALL'
    if subCatName=='':
        subCatName='ALL'
    myString+='Customer Category'+','+str(catName)+'\n'
    myString+='Customer Sub-Category'+','+str(subCatName)+'\n'
    
    myString+=str(session.level1Name)+','+str(out_st_level1_id)+'\n'
    myString+=str(session.level2Name)+','+str(out_st_level2_id)+'\n'
    
    #==================================RSM Wise    
        
    rowSL=0
    
    myString='SL,RSM Tr. Code,FM Tr. Code,MSO Tr. Code,Customer ID,Customer Name,Current Month,Last One Month,Last Two Month,Last Three Month,Last Four Month,Last Five Month,Last six Month,Earlier,OutStanding Net Amt,Remarks'+'\n'
    for i in range(len(recordsHeadList)):
                
        recData=recordsHeadList[i]
        rowSL+=1
        
        #----------
        level1_id=recData['level1_id']
        level2_id=recData['level2_id']
        level3_id=recData['level3_id']
         
        client_id=recData['client_id']
        client_name=recData['client_name']
        
        ostAmt_0=round(float(recData['monthL0']),2)
                
        ostAmt_1=round(float(recData['monthL1']),2)
        
        ostAmt_2=round(float(recData['monthL2']),2)
        
        ostAmt_3=round(float(recData['monthL3']),2)
        
        ostAmt_4=round(float(recData['monthL4']),2)
        
        ostAmt_5=round(float(recData['monthL5']),2)
        
        ostAmt_6=round(float(recData['monthL6']),2)
        
        ostAmt_e=round(float(recData['monthLE']),2)
        
        netAmt=(ostAmt_0+ostAmt_1+ostAmt_2+ostAmt_3+ostAmt_4+ostAmt_5+ostAmt_6+ostAmt_e)
        
        #------------------------        
        myString+=str(rowSL)+','+str(level1_id)+','+str(level2_id)+','+str(level3_id)+','+str(client_id)+','+str(client_name)+','+str(ostAmt_0)+','+str(ostAmt_1)+','+\
        str(ostAmt_2)+','+str(ostAmt_3)+','+str(ostAmt_4)+','+str(ostAmt_5)+','+str(ostAmt_6)+','+str(ostAmt_e)+','+str(netAmt)+'\n'
        
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_RSM_FM_MSOWiseOutstanding.csv'   
    return str(myString)
    

def outStRsmFmMsoWiseSummary():
    c_id=session.cid
    
    response.title='6.9B Outstanding RSM/FM/MSO Wise'
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    depot_id=str(request.vars.depotID).strip()
    store_id=str(request.vars.storeID).strip()    
    out_st_delivery_man_id=str(request.vars.deliveryManID).strip()    
    out_st_territory_id=str(request.vars.territoryID).strip()    
    out_st_mso_id=str(request.vars.msoID).strip()
    invoice_term=str(request.vars.invoice_term).strip()
    customerId=str(request.vars.customerId).strip()
    
    credit_type=str(request.vars.credit_type).strip()
    customer_cat=str(request.vars.customer_cat).strip() 
    customer_sub_cat=str(request.vars.customer_sub_cat).strip()    
    
    out_st_level1_id=str(request.vars.out_st_level1_id).strip()  
    out_st_level2_id=str(request.vars.out_st_level2_id).strip()  
    
    catName=''
    custCatRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_CATEGORY')&(db.sm_category_type.cat_type_id==customer_cat)).select(db.sm_category_type.cat_type_name, limitby=(0,1))
    if custCatRows:
        catName=custCatRows[0].cat_type_name        
    subCatName=''
    custSubCatRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_SUB_CATEGORY')&(db.sm_category_type.cat_type_id==customer_sub_cat)).select(db.sm_category_type.cat_type_name, limitby=(0,1))
    if custSubCatRows:
        subCatName=custSubCatRows[0].cat_type_name
    
    depot_name=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depot_name=depotRow[0].name
    
    store_name=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        store_name=storeRow[0].store_name
        
    out_st_delivery_man_name=''
    dpRow=db((db.sm_delivery_man.cid==c_id)&(db.sm_delivery_man.depot_id==depot_id)&(db.sm_delivery_man.d_man_id==out_st_delivery_man_id)).select(db.sm_delivery_man.name,limitby=(0,1))
    if dpRow:
        out_st_delivery_man_name=dpRow[0].name
        
    out_st_territory_name=''
    levelRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==out_st_territory_id)).select(db.sm_level.level_name,limitby=(0,1))
    if levelRow:
        out_st_territory_name=levelRow[0].level_name
        
    out_st_mso_name=''
    repRow=db((db.sm_rep.cid==c_id)&(db.sm_rep.rep_id==out_st_mso_id)).select(db.sm_rep.name,limitby=(0,1))
    if repRow:
        out_st_mso_name=repRow[0].name
    
    customerName=''
    clientRow=db((db.sm_client.cid==c_id)&(db.sm_client.depot_id==depot_id)&(db.sm_client.client_id==customerId)).select(db.sm_client.name,limitby=(0,1))
    if clientRow:
        customerName=clientRow[0].name
       
    try:        
        startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d').strftime('%Y-%m-%d')
    except:
        startDt=''                
        
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d').strftime('%Y-%m-%d')
    
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    
    rsmRows=db((db.sm_supervisor_level.cid==c_id) & (db.sm_supervisor_level.level_depth_no==1)).select(db.sm_supervisor_level.sup_id,db.sm_supervisor_level.sup_name,db.sm_supervisor_level.level_id)
    fmRows=db((db.sm_supervisor_level.cid==c_id) & (db.sm_supervisor_level.level_depth_no==2)).select(db.sm_supervisor_level.sup_id,db.sm_supervisor_level.sup_name,db.sm_supervisor_level.level_id)
    
    condStr=" AND (round(sm_invoice_head.total_amount-(sm_invoice_head.return_tp+sm_invoice_head.return_vat-sm_invoice_head.return_discount)-sm_invoice_head.collection_amount,2)!=0)"
    
    if out_st_delivery_man_id!='':
        condStr+=" AND (sm_invoice_head.d_man_id='"+out_st_delivery_man_id+"')"        
    if out_st_territory_id!='':
        condStr+=" AND (sm_invoice_head.area_id='"+out_st_territory_id+"')"        
    if out_st_mso_id!='':
        condStr+=" AND (sm_invoice_head.rep_id='"+out_st_mso_id+"')"        
    if invoice_term!='':
        condStr+=" AND (sm_invoice_head.payment_mode='"+invoice_term+"')"
    if customerId!='':
        condStr+=" AND (sm_invoice_head.client_id='"+customerId+"')"
        
    if credit_type!='':
        condStr+=" AND (sm_invoice_head.credit_note='"+credit_type+"')"
    if customer_cat!='':
        condStr+=" AND (sm_invoice_head.cl_category_id='"+customer_cat+"')"
    if customer_sub_cat!='':
        condStr+=" AND (sm_invoice_head.cl_sub_category_id='"+customer_sub_cat+"')"
    
    if out_st_level1_id!='':
        condStr+=" AND (sm_invoice_head.level1_id='"+out_st_level1_id+"')"        
    if out_st_level2_id!='':
        condStr+=" AND (sm_invoice_head.level2_id='"+out_st_level2_id+"')"
        
    if startDt!='' and endDt!='':
        rsmRecords="SELECT sm_invoice_head.level1_id as level1_id,COUNT(distinct(sm_invoice_head.client_id)) as cusCount,COUNT(distinct(sm_invoice_head.market_id)) as marCount,COUNT(sm_invoice_head.id) as invCount,MAX(sm_invoice_head.sl) as maxSl,MAX(sm_invoice_head.invoice_date) as maxInvDate,SUM(sm_invoice_head.actual_total_tp) as actualTpAmt,SUM(sm_invoice_head.total_amount) as totalAmt,SUM(sm_invoice_head.vat_total_amount) as vatTotalAmt,SUM(sm_invoice_head.discount) as discAmt,SUM(sm_invoice_head.adjust_amount) as adjustAmt,SUM(sm_invoice_head.return_tp) as retTpAmt,SUM(sm_invoice_head.return_vat) as retVatAmt,SUM(sm_invoice_head.return_discount) as retDiscAmt,SUM(sm_invoice_head.return_sp_discount) as retSpDiscAmt,SUM(sm_invoice_head.collection_amount) as collAmt,SUM(sm_invoice_head.sp_discount) as spDiscAmt FROM sm_invoice_head WHERE ((sm_invoice_head.cid = '"+c_id+"') AND ((sm_invoice_head.invoice_date >= '"+str(startDt)+"') AND (sm_invoice_head.invoice_date <= '"+str(endDt)+"')) AND (sm_invoice_head.depot_id='"+depot_id+"') AND (sm_invoice_head.store_id='"+store_id+"') AND (sm_invoice_head.status='Invoiced') "+str(condStr)+") GROUP BY sm_invoice_head.level1_id ORDER BY sm_invoice_head.level1_id"
        fmRecords="SELECT sm_invoice_head.level1_id as level1_id,sm_invoice_head.level2_id as level2_id,COUNT(distinct(sm_invoice_head.client_id)) as cusCount,COUNT(distinct(sm_invoice_head.market_id)) as marCount,COUNT(sm_invoice_head.id) as invCount,MAX(sm_invoice_head.sl) as maxSl,MAX(sm_invoice_head.invoice_date) as maxInvDate,SUM(sm_invoice_head.actual_total_tp) as actualTpAmt,SUM(sm_invoice_head.total_amount) as totalAmt,SUM(sm_invoice_head.vat_total_amount) as vatTotalAmt,SUM(sm_invoice_head.discount) as discAmt,SUM(sm_invoice_head.adjust_amount) as adjustAmt,SUM(sm_invoice_head.return_tp) as retTpAmt,SUM(sm_invoice_head.return_vat) as retVatAmt,SUM(sm_invoice_head.return_discount) as retDiscAmt,SUM(sm_invoice_head.return_sp_discount) as retSpDiscAmt,SUM(sm_invoice_head.collection_amount) as collAmt,SUM(sm_invoice_head.sp_discount) as spDiscAmt FROM sm_invoice_head WHERE ((sm_invoice_head.cid = '"+c_id+"') AND ((sm_invoice_head.invoice_date >= '"+str(startDt)+"') AND (sm_invoice_head.invoice_date <= '"+str(endDt)+"')) AND (sm_invoice_head.depot_id='"+depot_id+"') AND (sm_invoice_head.store_id='"+store_id+"') AND (sm_invoice_head.status='Invoiced') "+str(condStr)+") GROUP BY sm_invoice_head.level1_id,sm_invoice_head.level2_id ORDER BY sm_invoice_head.level1_id,sm_invoice_head.level2_id"
        msoRecords="SELECT sm_invoice_head.level1_id as level1_id,sm_invoice_head.level2_id as level2_id,sm_invoice_head.rep_id as rep_id,MAX(sm_invoice_head.rep_name) as rep_name,COUNT(distinct(sm_invoice_head.client_id)) as cusCount,COUNT(distinct(sm_invoice_head.market_id)) as marCount,COUNT(sm_invoice_head.id) as invCount,MAX(sm_invoice_head.sl) as maxSl,MAX(sm_invoice_head.invoice_date) as maxInvDate,SUM(sm_invoice_head.actual_total_tp) as actualTpAmt,SUM(sm_invoice_head.total_amount) as totalAmt,SUM(sm_invoice_head.vat_total_amount) as vatTotalAmt,SUM(sm_invoice_head.discount) as discAmt,SUM(sm_invoice_head.adjust_amount) as adjustAmt,SUM(sm_invoice_head.return_tp) as retTpAmt,SUM(sm_invoice_head.return_vat) as retVatAmt,SUM(sm_invoice_head.return_discount) as retDiscAmt,SUM(sm_invoice_head.return_sp_discount) as retSpDiscAmt,SUM(sm_invoice_head.collection_amount) as collAmt,SUM(sm_invoice_head.sp_discount) as spDiscAmt FROM sm_invoice_head WHERE ((sm_invoice_head.cid = '"+c_id+"') AND ((sm_invoice_head.invoice_date >= '"+str(startDt)+"') AND (sm_invoice_head.invoice_date <= '"+str(endDt)+"')) AND (sm_invoice_head.depot_id='"+depot_id+"') AND (sm_invoice_head.store_id='"+store_id+"') AND (sm_invoice_head.status='Invoiced') "+str(condStr)+") GROUP BY sm_invoice_head.level1_id,sm_invoice_head.level2_id,sm_invoice_head.rep_id ORDER BY sm_invoice_head.level1_id,sm_invoice_head.level2_id,sm_invoice_head.rep_id"
    else:
        rsmRecords="SELECT sm_invoice_head.level1_id as level1_id,COUNT(distinct(sm_invoice_head.client_id)) as cusCount,COUNT(distinct(sm_invoice_head.market_id)) as marCount,COUNT(sm_invoice_head.id) as invCount,MAX(sm_invoice_head.sl) as maxSl,MAX(sm_invoice_head.invoice_date) as maxInvDate,SUM(sm_invoice_head.actual_total_tp) as actualTpAmt,SUM(sm_invoice_head.total_amount) as totalAmt,SUM(sm_invoice_head.vat_total_amount) as vatTotalAmt,SUM(sm_invoice_head.discount) as discAmt,SUM(sm_invoice_head.adjust_amount) as adjustAmt,SUM(sm_invoice_head.return_tp) as retTpAmt,SUM(sm_invoice_head.return_vat) as retVatAmt,SUM(sm_invoice_head.return_discount) as retDiscAmt,SUM(sm_invoice_head.return_sp_discount) as retSpDiscAmt,SUM(sm_invoice_head.collection_amount) as collAmt,SUM(sm_invoice_head.sp_discount) as spDiscAmt FROM sm_invoice_head WHERE ((sm_invoice_head.cid = '"+c_id+"') AND ((sm_invoice_head.invoice_date >= '"+str(startDt)+"') AND (sm_invoice_head.invoice_date <= '"+str(endDt)+"')) AND (sm_invoice_head.depot_id='"+depot_id+"') AND (sm_invoice_head.store_id='"+store_id+"') AND (sm_invoice_head.status='Invoiced') "+str(condStr)+") GROUP BY sm_invoice_head.level1_id ORDER BY sm_invoice_head.level1_id"
        fmRecords="SELECT sm_invoice_head.level1_id as level1_id,sm_invoice_head.level2_id as level2_id,COUNT(distinct(sm_invoice_head.client_id)) as cusCount,COUNT(distinct(sm_invoice_head.market_id)) as marCount,COUNT(sm_invoice_head.id) as invCount,MAX(sm_invoice_head.sl) as maxSl,MAX(sm_invoice_head.invoice_date) as maxInvDate,SUM(sm_invoice_head.actual_total_tp) as actualTpAmt,SUM(sm_invoice_head.total_amount) as totalAmt,SUM(sm_invoice_head.vat_total_amount) as vatTotalAmt,SUM(sm_invoice_head.discount) as discAmt,SUM(sm_invoice_head.adjust_amount) as adjustAmt,SUM(sm_invoice_head.return_tp) as retTpAmt,SUM(sm_invoice_head.return_vat) as retVatAmt,SUM(sm_invoice_head.return_discount) as retDiscAmt,SUM(sm_invoice_head.return_sp_discount) as retSpDiscAmt,SUM(sm_invoice_head.collection_amount) as collAmt,SUM(sm_invoice_head.sp_discount) as spDiscAmt FROM sm_invoice_head WHERE ((sm_invoice_head.cid = '"+c_id+"') AND ((sm_invoice_head.invoice_date >= '"+str(startDt)+"') AND (sm_invoice_head.invoice_date <= '"+str(endDt)+"')) AND (sm_invoice_head.depot_id='"+depot_id+"') AND (sm_invoice_head.store_id='"+store_id+"') AND (sm_invoice_head.status='Invoiced') "+str(condStr)+") GROUP BY sm_invoice_head.level1_id,sm_invoice_head.level2_id ORDER BY sm_invoice_head.level1_id,sm_invoice_head.level2_id"
        msoRecords="SELECT sm_invoice_head.level1_id as level1_id,sm_invoice_head.level2_id as level2_id,sm_invoice_head.rep_id as rep_id,MAX(sm_invoice_head.rep_name) as rep_name,COUNT(distinct(sm_invoice_head.client_id)) as cusCount,COUNT(distinct(sm_invoice_head.market_id)) as marCount,COUNT(sm_invoice_head.id) as invCount,MAX(sm_invoice_head.sl) as maxSl,MAX(sm_invoice_head.invoice_date) as maxInvDate,SUM(sm_invoice_head.actual_total_tp) as actualTpAmt,SUM(sm_invoice_head.total_amount) as totalAmt,SUM(sm_invoice_head.vat_total_amount) as vatTotalAmt,SUM(sm_invoice_head.discount) as discAmt,SUM(sm_invoice_head.adjust_amount) as adjustAmt,SUM(sm_invoice_head.return_tp) as retTpAmt,SUM(sm_invoice_head.return_vat) as retVatAmt,SUM(sm_invoice_head.return_discount) as retDiscAmt,SUM(sm_invoice_head.return_sp_discount) as retSpDiscAmt,SUM(sm_invoice_head.collection_amount) as collAmt,SUM(sm_invoice_head.sp_discount) as spDiscAmt FROM sm_invoice_head WHERE ((sm_invoice_head.cid = '"+c_id+"') AND (sm_invoice_head.invoice_date <= '"+str(endDt)+"') AND (sm_invoice_head.depot_id='"+depot_id+"') AND (sm_invoice_head.store_id='"+store_id+"') AND (sm_invoice_head.status='Invoiced') "+str(condStr)+") GROUP BY sm_invoice_head.level1_id,sm_invoice_head.level2_id,sm_invoice_head.rep_id ORDER BY sm_invoice_head.level1_id,sm_invoice_head.level2_id,sm_invoice_head.rep_id"
        
    rsmRecordsList=db.executesql(rsmRecords,as_dict = True)    
    #rsmRecordsList.sort(key=itemgetter('level1_id'), reverse=False)
    
    fmRecordsList=db.executesql(fmRecords,as_dict = True)    
    #fmRecordsList.sort(key=itemgetter('level2_id'), reverse=False)
    
    msoRecordsList=db.executesql(msoRecords,as_dict = True)    
    #msoRecordsList.sort(key=itemgetter('level2_id','rep_id'), reverse=False)
    
    #====================
    p_totalInvTP_rsm=0
    p_totalInvVat_rsm=0
    p_totalInvDisc_rsm=0
    p_totalInvSp_rsm=0
    p_totalInvAmt_rsm=0
    percentTp_rsm=0
    percentVat_rsm=0
    percentDisc_rsm=0
    percentSpDisc_rsm=0
    
    for i in range(len(rsmRecordsList)):                
        recData=rsmRecordsList[i]
        
        p_invTp_rsm=recData['actualTpAmt']-(recData['retTpAmt']+recData['retSpDiscAmt'])   
        p_invVat_rsm=recData['vatTotalAmt']-recData['retVatAmt']
        p_invDiscount_rsm=recData['discAmt']-recData['retDiscAmt']
        p_invSpDisc_rsm=recData['spDiscAmt']-recData['retSpDiscAmt']
        p_invNetAmt_rsm=p_invTp_rsm+p_invVat_rsm-(p_invDiscount_rsm+p_invSpDisc_rsm)
    
        p_outstanding_rsm=round(p_invNetAmt_rsm-recData['collAmt'],2)
        
        if p_outstanding_rsm==0:
            continue
            
        p_totalInvTP_rsm+=p_invTp_rsm
        p_totalInvVat_rsm+=p_invVat_rsm
        p_totalInvDisc_rsm+=p_invDiscount_rsm
        p_totalInvSp_rsm+=p_invSpDisc_rsm
        p_totalInvAmt_rsm+=p_invNetAmt_rsm
        
    try:
        percentTp_rsm=p_totalInvTP_rsm/p_totalInvAmt_rsm*100
        percentVat_rsm=p_totalInvVat_rsm/p_totalInvAmt_rsm*100
        percentDisc_rsm=p_totalInvDisc_rsm/p_totalInvAmt_rsm*100
        percentSpDisc_rsm=p_totalInvSp_rsm/p_totalInvAmt_rsm*100
    except:
        percentTp_rsm=0
        percentVat_rsm=0
        percentDisc_rsm=0
        percentSpDisc_rsm=0
    #======================
    #====================
    p_totalInvTP_fm=0
    p_totalInvVat_fm=0
    p_totalInvDisc_fm=0
    p_totalInvSp_fm=0
    p_totalInvAmt_fm=0
    percentTp_fm=0
    percentVat_fm=0
    percentDisc_fm=0
    percentSpDisc_fm=0
    
    for i in range(len(fmRecordsList)):                
        recData=fmRecordsList[i]
        
        p_invTp_fm=recData['actualTpAmt']-(recData['retTpAmt']+recData['retSpDiscAmt'])   
        p_invVat_fm=recData['vatTotalAmt']-recData['retVatAmt']
        p_invDiscount_fm=recData['discAmt']-recData['retDiscAmt']
        p_invSpDisc_fm=recData['spDiscAmt']-recData['retSpDiscAmt']
        p_invNetAmt_fm=p_invTp_fm+p_invVat_fm-(p_invDiscount_fm+p_invSpDisc_fm)
    
        p_outstanding_fm=round(p_invNetAmt_fm-recData['collAmt'],2)
        
        if p_outstanding_fm==0:
            continue
            
        p_totalInvTP_fm+=p_invTp_fm
        p_totalInvVat_fm+=p_invVat_fm
        p_totalInvDisc_fm+=p_invDiscount_fm
        p_totalInvSp_fm+=p_invSpDisc_fm
        p_totalInvAmt_fm+=p_invNetAmt_fm
        
    try:
        percentTp_fm=p_totalInvTP_fm/p_totalInvAmt_fm*100
        percentVat_fm=p_totalInvVat_fm/p_totalInvAmt_fm*100
        percentDisc_fm=p_totalInvDisc_fm/p_totalInvAmt_fm*100
        percentSpDisc_fm=p_totalInvSp_fm/p_totalInvAmt_fm*100
    except:
        percentTp_fm=0
        percentVat_fm=0
        percentDisc_fm=0
        percentSpDisc_fm=0
    #======================
    #====================
    p_totalInvTP=0
    p_totalInvVat=0
    p_totalInvDisc=0
    p_totalInvSp=0
    p_totalInvAmt=0
    percentTp=0
    percentVat=0
    percentDisc=0
    percentSpDisc=0
    
    for i in range(len(msoRecordsList)):                
        recData=msoRecordsList[i]
        
        p_invTp=recData['actualTpAmt']-(recData['retTpAmt']+recData['retSpDiscAmt'])   
        p_invVat=recData['vatTotalAmt']-recData['retVatAmt']
        p_invDiscount=recData['discAmt']-recData['retDiscAmt']
        p_invSpDisc=recData['spDiscAmt']-recData['retSpDiscAmt']
        p_invNetAmt=p_invTp+p_invVat-(p_invDiscount+p_invSpDisc)
    
        p_outstanding=round(p_invNetAmt-recData['collAmt'],2)
        
        if p_outstanding==0:
            continue
            
        p_totalInvTP+=p_invTp
        p_totalInvVat+=p_invVat
        p_totalInvDisc+=p_invDiscount
        p_totalInvSp+=p_invSpDisc
        p_totalInvAmt+=p_invNetAmt
        
    try:
        percentTp=p_totalInvTP/p_totalInvAmt*100
        percentVat=p_totalInvVat/p_totalInvAmt*100
        percentDisc=p_totalInvDisc/p_totalInvAmt*100
        percentSpDisc=p_totalInvSp/p_totalInvAmt*100
    except:
        percentTp=0
        percentVat=0
        percentDisc=0
        percentSpDisc=0
    #======================
    
    return dict(percentTp_rsm=percentTp_rsm,percentVat_rsm=percentVat_rsm,percentDisc_rsm=percentDisc_rsm,percentSpDisc_rsm=percentSpDisc_rsm,percentTp_fm=percentTp_fm,percentVat_fm=percentVat_fm,percentDisc_fm=percentDisc_fm,percentSpDisc_fm=percentSpDisc_fm,percentTp=percentTp,percentVat=percentVat,percentDisc=percentDisc,percentSpDisc=percentSpDisc,msoRecordsList=msoRecordsList,rsmRecordsList=rsmRecordsList,rsmRows=rsmRows,fmRecordsList=fmRecordsList,fmRows=fmRows,fromDate=startDt,toDate=endDt,depotID=depot_id,depotName=depot_name,storeID=store_id,storeName=store_name,deliveryManID=out_st_delivery_man_id,deliveryManName=out_st_delivery_man_name,territoryID=out_st_territory_id,territoryName=out_st_territory_name,msoID=out_st_mso_id,msoName=out_st_mso_name,invoice_term=invoice_term,customerId=customerId,customerName=customerName,credit_type=credit_type,customer_cat=customer_cat,customer_sub_cat=customer_sub_cat,catName=catName,subCatName=subCatName,out_st_level1_id=out_st_level1_id,out_st_level2_id=out_st_level2_id,page=page,items_per_page=items_per_page)    
    
def outStRsmFmMsoWiseSummary_download():
    c_id=session.cid
    
    currentDate=datetime.datetime.strptime(str(current_date),'%Y-%m-%d')
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    depot_id=str(request.vars.depotID).strip()
    store_id=str(request.vars.storeID).strip()    
    out_st_delivery_man_id=str(request.vars.deliveryManID).strip()    
    out_st_territory_id=str(request.vars.territoryID).strip()    
    out_st_mso_id=str(request.vars.msoID).strip()
    invoice_term=str(request.vars.invoice_term).strip()
    customerId=str(request.vars.customerId).strip()
    
    credit_type=str(request.vars.credit_type).strip()
    customer_cat=str(request.vars.customer_cat).strip() 
    customer_sub_cat=str(request.vars.customer_sub_cat).strip()    
    
    out_st_level1_id=str(request.vars.out_st_level1_id).strip()  
    out_st_level2_id=str(request.vars.out_st_level2_id).strip()  
    
    catName=''
    custCatRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_CATEGORY')&(db.sm_category_type.cat_type_id==customer_cat)).select(db.sm_category_type.cat_type_name, limitby=(0,1))
    if custCatRows:
        catName=custCatRows[0].cat_type_name        
    subCatName=''
    custSubCatRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_SUB_CATEGORY')&(db.sm_category_type.cat_type_id==customer_sub_cat)).select(db.sm_category_type.cat_type_name, limitby=(0,1))
    if custSubCatRows:
        subCatName=custSubCatRows[0].cat_type_name
    
    depot_name=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depot_name=depotRow[0].name
    
    store_name=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        store_name=storeRow[0].store_name
        
    out_st_delivery_man_name=''
    dpRow=db((db.sm_delivery_man.cid==c_id)&(db.sm_delivery_man.depot_id==depot_id)&(db.sm_delivery_man.d_man_id==out_st_delivery_man_id)).select(db.sm_delivery_man.name,limitby=(0,1))
    if dpRow:
        out_st_delivery_man_name=dpRow[0].name
        
    out_st_territory_name=''
    levelRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==out_st_territory_id)).select(db.sm_level.level_name,limitby=(0,1))
    if levelRow:
        out_st_territory_name=levelRow[0].level_name
        
    out_st_mso_name=''
    repRow=db((db.sm_rep.cid==c_id)&(db.sm_rep.rep_id==out_st_mso_id)).select(db.sm_rep.name,limitby=(0,1))
    if repRow:
        out_st_mso_name=repRow[0].name
    
    customerName=''
    clientRow=db((db.sm_client.cid==c_id)&(db.sm_client.depot_id==depot_id)&(db.sm_client.client_id==customerId)).select(db.sm_client.name,limitby=(0,1))
    if clientRow:
        customerName=clientRow[0].name
       
    try:        
        startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d').strftime('%Y-%m-%d')
    except:
        startDt=''                
        
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d').strftime('%Y-%m-%d')
    
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    
    rsmRows=db((db.sm_supervisor_level.cid==c_id) & (db.sm_supervisor_level.level_depth_no==1)).select(db.sm_supervisor_level.sup_id,db.sm_supervisor_level.sup_name,db.sm_supervisor_level.level_id)
    fmRows=db((db.sm_supervisor_level.cid==c_id) & (db.sm_supervisor_level.level_depth_no==2)).select(db.sm_supervisor_level.sup_id,db.sm_supervisor_level.sup_name,db.sm_supervisor_level.level_id)
    
    condStr=" AND (round(sm_invoice_head.total_amount-(sm_invoice_head.return_tp+sm_invoice_head.return_vat-sm_invoice_head.return_discount)-sm_invoice_head.collection_amount,2)!=0)"
    
    if out_st_delivery_man_id!='':
        condStr+=" AND (sm_invoice_head.d_man_id='"+out_st_delivery_man_id+"')"        
    if out_st_territory_id!='':
        condStr+=" AND (sm_invoice_head.area_id='"+out_st_territory_id+"')"        
    if out_st_mso_id!='':
        condStr+=" AND (sm_invoice_head.rep_id='"+out_st_mso_id+"')"        
    if invoice_term!='':
        condStr+=" AND (sm_invoice_head.payment_mode='"+invoice_term+"')"
    if customerId!='':
        condStr+=" AND (sm_invoice_head.client_id='"+customerId+"')"
        
    if credit_type!='':
        condStr+=" AND (sm_invoice_head.credit_note='"+credit_type+"')"
    if customer_cat!='':
        condStr+=" AND (sm_invoice_head.cl_category_id='"+customer_cat+"')"
    if customer_sub_cat!='':
        condStr+=" AND (sm_invoice_head.cl_sub_category_id='"+customer_sub_cat+"')"
    
    if out_st_level1_id!='':
        condStr+=" AND (sm_invoice_head.level1_id='"+out_st_level1_id+"')"        
    if out_st_level2_id!='':
        condStr+=" AND (sm_invoice_head.level2_id='"+out_st_level2_id+"')"
        
    if startDt!='' and endDt!='':
        rsmRecords="SELECT sm_invoice_head.level1_id as level1_id,COUNT(distinct(sm_invoice_head.client_id)) as cusCount,COUNT(distinct(sm_invoice_head.market_id)) as marCount,COUNT(sm_invoice_head.id) as invCount,MAX(sm_invoice_head.sl) as maxSl,MAX(sm_invoice_head.invoice_date) as maxInvDate,SUM(sm_invoice_head.actual_total_tp) as actualTpAmt,SUM(sm_invoice_head.total_amount) as totalAmt,SUM(sm_invoice_head.vat_total_amount) as vatTotalAmt,SUM(sm_invoice_head.discount) as discAmt,SUM(sm_invoice_head.adjust_amount) as adjustAmt,SUM(sm_invoice_head.return_tp) as retTpAmt,SUM(sm_invoice_head.return_vat) as retVatAmt,SUM(sm_invoice_head.return_discount) as retDiscAmt,SUM(sm_invoice_head.return_sp_discount) as retSpDiscAmt,SUM(sm_invoice_head.collection_amount) as collAmt,SUM(sm_invoice_head.sp_discount) as spDiscAmt FROM sm_invoice_head WHERE ((sm_invoice_head.cid = '"+c_id+"') AND ((sm_invoice_head.invoice_date >= '"+str(startDt)+"') AND (sm_invoice_head.invoice_date <= '"+str(endDt)+"')) AND (sm_invoice_head.depot_id='"+depot_id+"') AND (sm_invoice_head.store_id='"+store_id+"') AND (sm_invoice_head.status='Invoiced') "+str(condStr)+") GROUP BY sm_invoice_head.level1_id ORDER BY sm_invoice_head.level1_id"
        fmRecords="SELECT sm_invoice_head.level1_id as level1_id,sm_invoice_head.level2_id as level2_id,COUNT(distinct(sm_invoice_head.client_id)) as cusCount,COUNT(distinct(sm_invoice_head.market_id)) as marCount,COUNT(sm_invoice_head.id) as invCount,MAX(sm_invoice_head.sl) as maxSl,MAX(sm_invoice_head.invoice_date) as maxInvDate,SUM(sm_invoice_head.actual_total_tp) as actualTpAmt,SUM(sm_invoice_head.total_amount) as totalAmt,SUM(sm_invoice_head.vat_total_amount) as vatTotalAmt,SUM(sm_invoice_head.discount) as discAmt,SUM(sm_invoice_head.adjust_amount) as adjustAmt,SUM(sm_invoice_head.return_tp) as retTpAmt,SUM(sm_invoice_head.return_vat) as retVatAmt,SUM(sm_invoice_head.return_discount) as retDiscAmt,SUM(sm_invoice_head.return_sp_discount) as retSpDiscAmt,SUM(sm_invoice_head.collection_amount) as collAmt,SUM(sm_invoice_head.sp_discount) as spDiscAmt FROM sm_invoice_head WHERE ((sm_invoice_head.cid = '"+c_id+"') AND ((sm_invoice_head.invoice_date >= '"+str(startDt)+"') AND (sm_invoice_head.invoice_date <= '"+str(endDt)+"')) AND (sm_invoice_head.depot_id='"+depot_id+"') AND (sm_invoice_head.store_id='"+store_id+"') AND (sm_invoice_head.status='Invoiced') "+str(condStr)+") GROUP BY sm_invoice_head.level1_id,sm_invoice_head.level2_id ORDER BY sm_invoice_head.level1_id,sm_invoice_head.level2_id"
        msoRecords="SELECT sm_invoice_head.level1_id as level1_id,sm_invoice_head.level2_id as level2_id,sm_invoice_head.rep_id as rep_id,MAX(sm_invoice_head.rep_name) as rep_name,COUNT(distinct(sm_invoice_head.client_id)) as cusCount,COUNT(distinct(sm_invoice_head.market_id)) as marCount,COUNT(sm_invoice_head.id) as invCount,MAX(sm_invoice_head.sl) as maxSl,MAX(sm_invoice_head.invoice_date) as maxInvDate,SUM(sm_invoice_head.actual_total_tp) as actualTpAmt,SUM(sm_invoice_head.total_amount) as totalAmt,SUM(sm_invoice_head.vat_total_amount) as vatTotalAmt,SUM(sm_invoice_head.discount) as discAmt,SUM(sm_invoice_head.adjust_amount) as adjustAmt,SUM(sm_invoice_head.return_tp) as retTpAmt,SUM(sm_invoice_head.return_vat) as retVatAmt,SUM(sm_invoice_head.return_discount) as retDiscAmt,SUM(sm_invoice_head.return_sp_discount) as retSpDiscAmt,SUM(sm_invoice_head.collection_amount) as collAmt,SUM(sm_invoice_head.sp_discount) as spDiscAmt FROM sm_invoice_head WHERE ((sm_invoice_head.cid = '"+c_id+"') AND ((sm_invoice_head.invoice_date >= '"+str(startDt)+"') AND (sm_invoice_head.invoice_date <= '"+str(endDt)+"')) AND (sm_invoice_head.depot_id='"+depot_id+"') AND (sm_invoice_head.store_id='"+store_id+"') AND (sm_invoice_head.status='Invoiced') "+str(condStr)+") GROUP BY sm_invoice_head.level1_id,sm_invoice_head.level2_id,sm_invoice_head.rep_id ORDER BY sm_invoice_head.level1_id,sm_invoice_head.level2_id,sm_invoice_head.rep_id"
    else:
        rsmRecords="SELECT sm_invoice_head.level1_id as level1_id,COUNT(distinct(sm_invoice_head.client_id)) as cusCount,COUNT(distinct(sm_invoice_head.market_id)) as marCount,COUNT(sm_invoice_head.id) as invCount,MAX(sm_invoice_head.sl) as maxSl,MAX(sm_invoice_head.invoice_date) as maxInvDate,SUM(sm_invoice_head.actual_total_tp) as actualTpAmt,SUM(sm_invoice_head.total_amount) as totalAmt,SUM(sm_invoice_head.vat_total_amount) as vatTotalAmt,SUM(sm_invoice_head.discount) as discAmt,SUM(sm_invoice_head.adjust_amount) as adjustAmt,SUM(sm_invoice_head.return_tp) as retTpAmt,SUM(sm_invoice_head.return_vat) as retVatAmt,SUM(sm_invoice_head.return_discount) as retDiscAmt,SUM(sm_invoice_head.return_sp_discount) as retSpDiscAmt,SUM(sm_invoice_head.collection_amount) as collAmt,SUM(sm_invoice_head.sp_discount) as spDiscAmt FROM sm_invoice_head WHERE ((sm_invoice_head.cid = '"+c_id+"') AND ((sm_invoice_head.invoice_date >= '"+str(startDt)+"') AND (sm_invoice_head.invoice_date <= '"+str(endDt)+"')) AND (sm_invoice_head.depot_id='"+depot_id+"') AND (sm_invoice_head.store_id='"+store_id+"') AND (sm_invoice_head.status='Invoiced') "+str(condStr)+") GROUP BY sm_invoice_head.level1_id ORDER BY sm_invoice_head.level1_id"
        fmRecords="SELECT sm_invoice_head.level1_id as level1_id,sm_invoice_head.level2_id as level2_id,COUNT(distinct(sm_invoice_head.client_id)) as cusCount,COUNT(distinct(sm_invoice_head.market_id)) as marCount,COUNT(sm_invoice_head.id) as invCount,MAX(sm_invoice_head.sl) as maxSl,MAX(sm_invoice_head.invoice_date) as maxInvDate,SUM(sm_invoice_head.actual_total_tp) as actualTpAmt,SUM(sm_invoice_head.total_amount) as totalAmt,SUM(sm_invoice_head.vat_total_amount) as vatTotalAmt,SUM(sm_invoice_head.discount) as discAmt,SUM(sm_invoice_head.adjust_amount) as adjustAmt,SUM(sm_invoice_head.return_tp) as retTpAmt,SUM(sm_invoice_head.return_vat) as retVatAmt,SUM(sm_invoice_head.return_discount) as retDiscAmt,SUM(sm_invoice_head.return_sp_discount) as retSpDiscAmt,SUM(sm_invoice_head.collection_amount) as collAmt,SUM(sm_invoice_head.sp_discount) as spDiscAmt FROM sm_invoice_head WHERE ((sm_invoice_head.cid = '"+c_id+"') AND ((sm_invoice_head.invoice_date >= '"+str(startDt)+"') AND (sm_invoice_head.invoice_date <= '"+str(endDt)+"')) AND (sm_invoice_head.depot_id='"+depot_id+"') AND (sm_invoice_head.store_id='"+store_id+"') AND (sm_invoice_head.status='Invoiced') "+str(condStr)+") GROUP BY sm_invoice_head.level1_id,sm_invoice_head.level2_id ORDER BY sm_invoice_head.level1_id,sm_invoice_head.level2_id"
        msoRecords="SELECT sm_invoice_head.level1_id as level1_id,sm_invoice_head.level2_id as level2_id,sm_invoice_head.rep_id as rep_id,MAX(sm_invoice_head.rep_name) as rep_name,COUNT(distinct(sm_invoice_head.client_id)) as cusCount,COUNT(distinct(sm_invoice_head.market_id)) as marCount,COUNT(sm_invoice_head.id) as invCount,MAX(sm_invoice_head.sl) as maxSl,MAX(sm_invoice_head.invoice_date) as maxInvDate,SUM(sm_invoice_head.actual_total_tp) as actualTpAmt,SUM(sm_invoice_head.total_amount) as totalAmt,SUM(sm_invoice_head.vat_total_amount) as vatTotalAmt,SUM(sm_invoice_head.discount) as discAmt,SUM(sm_invoice_head.adjust_amount) as adjustAmt,SUM(sm_invoice_head.return_tp) as retTpAmt,SUM(sm_invoice_head.return_vat) as retVatAmt,SUM(sm_invoice_head.return_discount) as retDiscAmt,SUM(sm_invoice_head.return_sp_discount) as retSpDiscAmt,SUM(sm_invoice_head.collection_amount) as collAmt,SUM(sm_invoice_head.sp_discount) as spDiscAmt FROM sm_invoice_head WHERE ((sm_invoice_head.cid = '"+c_id+"') AND (sm_invoice_head.invoice_date <= '"+str(endDt)+"') AND (sm_invoice_head.depot_id='"+depot_id+"') AND (sm_invoice_head.store_id='"+store_id+"') AND (sm_invoice_head.status='Invoiced') "+str(condStr)+") GROUP BY sm_invoice_head.level1_id,sm_invoice_head.level2_id,sm_invoice_head.rep_id ORDER BY sm_invoice_head.level1_id,sm_invoice_head.level2_id,sm_invoice_head.rep_id"
        
    rsmRecordsList=db.executesql(rsmRecords,as_dict = True)    
    #rsmRecordsList.sort(key=itemgetter('level1_id'), reverse=False)
    
    fmRecordsList=db.executesql(fmRecords,as_dict = True)    
    #fmRecordsList.sort(key=itemgetter('level2_id'), reverse=False)
    
    msoRecordsList=db.executesql(msoRecords,as_dict = True)    
    #msoRecordsList.sort(key=itemgetter('level2_id','rep_id'), reverse=False)
    
    #====================
    p_totalInvTP_rsm=0
    p_totalInvVat_rsm=0
    p_totalInvDisc_rsm=0
    p_totalInvSp_rsm=0
    p_totalInvAmt_rsm=0
    percentTp_rsm=0
    percentVat_rsm=0
    percentDisc_rsm=0
    percentSpDisc_rsm=0
    
    for i in range(len(rsmRecordsList)):                
        recData=rsmRecordsList[i]
        
        p_invTp_rsm=recData['actualTpAmt']-(recData['retTpAmt']+recData['retSpDiscAmt'])   
        p_invVat_rsm=recData['vatTotalAmt']-recData['retVatAmt']
        p_invDiscount_rsm=recData['discAmt']-recData['retDiscAmt']
        p_invSpDisc_rsm=recData['spDiscAmt']-recData['retSpDiscAmt']
        p_invNetAmt_rsm=p_invTp_rsm+p_invVat_rsm-(p_invDiscount_rsm+p_invSpDisc_rsm)
    
        p_outstanding_rsm=round(p_invNetAmt_rsm-recData['collAmt'],2)
        
        if p_outstanding_rsm==0:
            continue
            
        p_totalInvTP_rsm+=p_invTp_rsm
        p_totalInvVat_rsm+=p_invVat_rsm
        p_totalInvDisc_rsm+=p_invDiscount_rsm
        p_totalInvSp_rsm+=p_invSpDisc_rsm
        p_totalInvAmt_rsm+=p_invNetAmt_rsm
        
    try:
        percentTp_rsm=p_totalInvTP_rsm/p_totalInvAmt_rsm*100
        percentVat_rsm=p_totalInvVat_rsm/p_totalInvAmt_rsm*100
        percentDisc_rsm=p_totalInvDisc_rsm/p_totalInvAmt_rsm*100
        percentSpDisc_rsm=p_totalInvSp_rsm/p_totalInvAmt_rsm*100
    except:
        percentTp_rsm=0
        percentVat_rsm=0
        percentDisc_rsm=0
        percentSpDisc_rsm=0
    #======================
    #====================
    p_totalInvTP_fm=0
    p_totalInvVat_fm=0
    p_totalInvDisc_fm=0
    p_totalInvSp_fm=0
    p_totalInvAmt_fm=0
    percentTp_fm=0
    percentVat_fm=0
    percentDisc_fm=0
    percentSpDisc_fm=0
    
    for i in range(len(fmRecordsList)):                
        recData=fmRecordsList[i]
        
        p_invTp_fm=recData['actualTpAmt']-(recData['retTpAmt']+recData['retSpDiscAmt'])   
        p_invVat_fm=recData['vatTotalAmt']-recData['retVatAmt']
        p_invDiscount_fm=recData['discAmt']-recData['retDiscAmt']
        p_invSpDisc_fm=recData['spDiscAmt']-recData['retSpDiscAmt']
        p_invNetAmt_fm=p_invTp_fm+p_invVat_fm-(p_invDiscount_fm+p_invSpDisc_fm)
    
        p_outstanding_fm=round(p_invNetAmt_fm-recData['collAmt'],2)
        
        if p_outstanding_fm==0:
            continue
            
        p_totalInvTP_fm+=p_invTp_fm
        p_totalInvVat_fm+=p_invVat_fm
        p_totalInvDisc_fm+=p_invDiscount_fm
        p_totalInvSp_fm+=p_invSpDisc_fm
        p_totalInvAmt_fm+=p_invNetAmt_fm
        
    try:
        percentTp_fm=p_totalInvTP_fm/p_totalInvAmt_fm*100
        percentVat_fm=p_totalInvVat_fm/p_totalInvAmt_fm*100
        percentDisc_fm=p_totalInvDisc_fm/p_totalInvAmt_fm*100
        percentSpDisc_fm=p_totalInvSp_fm/p_totalInvAmt_fm*100
    except:
        percentTp_fm=0
        percentVat_fm=0
        percentDisc_fm=0
        percentSpDisc_fm=0
    #======================
    #====================
    p_totalInvTP=0
    p_totalInvVat=0
    p_totalInvDisc=0
    p_totalInvSp=0
    p_totalInvAmt=0
    percentTp=0
    percentVat=0
    percentDisc=0
    percentSpDisc=0
    
    for i in range(len(msoRecordsList)):                
        recData=msoRecordsList[i]
        
        p_invTp=recData['actualTpAmt']-(recData['retTpAmt']+recData['retSpDiscAmt'])   
        p_invVat=recData['vatTotalAmt']-recData['retVatAmt']
        p_invDiscount=recData['discAmt']-recData['retDiscAmt']
        p_invSpDisc=recData['spDiscAmt']-recData['retSpDiscAmt']
        p_invNetAmt=p_invTp+p_invVat-(p_invDiscount+p_invSpDisc)
    
        p_outstanding=round(p_invNetAmt-recData['collAmt'],2)
        
        if p_outstanding==0:
            continue
            
        p_totalInvTP+=p_invTp
        p_totalInvVat+=p_invVat
        p_totalInvDisc+=p_invDiscount
        p_totalInvSp+=p_invSpDisc
        p_totalInvAmt+=p_invNetAmt
        
    try:
        percentTp=p_totalInvTP/p_totalInvAmt*100
        percentVat=p_totalInvVat/p_totalInvAmt*100
        percentDisc=p_totalInvDisc/p_totalInvAmt*100
        percentSpDisc=p_totalInvSp/p_totalInvAmt*100
    except:
        percentTp=0
        percentVat=0
        percentDisc=0
        percentSpDisc=0
    #======================
    
    myString='6.09B Outstanding List: RSM/FM/MSO Wise\n'
    myString+='Inv Date From:,'+str(startDt)+'\n'
    myString+='To/ as of Date:'+','+str(endDt)+'\n'
    myString+='Inv Term:,'+str(invoice_term)+'\n'
    myString+='Branch ID:,'+str(depot_id)+'\n'
    myString+='Branch Name'+','+str(depot_name)+'\n'
    myString+='Store ID:,'+str(store_id)+'\n'
    myString+='Store Name'+','+str(store_name)+'\n'
    myString+='DP ID:,'+str(out_st_delivery_man_id)+'\n'
    myString+='DP Name'+','+str(out_st_delivery_man_name)+'\n'
    myString+='Territory ID:,'+str(out_st_territory_id)+'\n'
    myString+='Territory Name'+','+str(out_st_territory_name)+'\n'
    myString+='MSO ID:,'+str(out_st_mso_id)+'\n'
    myString+='MSO Name'+','+str(out_st_mso_name)+'\n'
    myString+='Customer ID:,'+str(customerId)+'\n'
    myString+='Customer Name'+','+str(customerName)+'\n'
    
    myString+='Credit Type:,'+str(credit_type)+'\n'
    if catName=='':
        catName='ALL'
    if subCatName=='':
        subCatName='ALL'
    myString+='Customer Category'+','+str(catName)+'\n'
    myString+='Customer Sub-Category'+','+str(subCatName)+'\n'
    
    myString+=str(session.level1Name)+','+str(out_st_level1_id)+'\n'
    myString+=str(session.level2Name)+','+str(out_st_level2_id)+'\n'
    
    #==================================RSM Wise    
    totalInvTP=0
    totalInvVat=0
    totalInvDisc=0
    totalInvAmt=0
    totalInvSp=0
    totalOutsTP=0
    totalOutsVat=0
    totalOutsDisc=0
    totalOutST=0
    totalOutSp=0
    
    sl=0
    myString+='RSM Wise:\n'
    myString+='SL,'+str(session.level1Name)+',RSMID,RSMName,Inv Count,Last Inv,LastDate,Invoice-TP,Invoice-Vat,Invoice-Disc,Invoice-SP,Invoice-Net,Adjusted,Outstanding-TP,Outstanding-Vat,Outstanding-Disc,Outstanding-SP,Outstanding-Net,Aging,Oustanding%'+'\n'
    for i in range(len(rsmRecordsList)):
        
        recData=rsmRecordsList[i]
        
        #----------
        invTp=recData['actualTpAmt']-(recData['retTpAmt']+recData['retSpDiscAmt'])
        invVat=recData['vatTotalAmt']-recData['retVatAmt']
        invDiscount=recData['discAmt']-recData['retDiscAmt']
        invSpDisc=recData['spDiscAmt']-recData['retSpDiscAmt']
        invNetAmt=invTp+invVat-(invDiscount+invSpDisc)
        
        outstanding=round(invNetAmt-recData['collAmt'],2)
        if outstanding==0:
            continue
            
        sl+=1
        
        try:
#             outTp=(invTp*outstanding)/invNetAmt
#             outVat=(invVat*outstanding)/invNetAmt
#             outDisc=(invDiscount*outstanding)/invNetAmt
#             outSp=(invSpDisc*outstanding)/invNetAmt
            outTp=outstanding*(percentTp_rsm/100)
            outVat=outstanding*(percentVat_rsm/100)
            outDisc=outstanding*(percentDisc_rsm/100)
            outSp=outstanding*(percentSpDisc_rsm/100)
            
        except:
            outTp=0
            outVat=0
            outDisc=0
            outSp=0
            
        #-------
        lastInv=str(session.prefix_invoice)+'INV-'+str(recData['maxSl'])                                              
        lastDate=recData['maxInvDate'].strftime('%d-%b-%y')
        
        adjust_amount=recData['adjustAmt']
        
        totalInvTP+=invTp
        totalInvVat+=invVat
        totalInvDisc+=invDiscount
        totalInvSp+=invSpDisc
        totalInvAmt+=invNetAmt
        
        #totalOutsTP+=outTp
        #totalOutsVat+=outVat
        #totalOutsDisc+=outDisc
        #totalOutSp+=outSp
        totalOutST+=outstanding
        
        
        try:            
            invoice_date=datetime.datetime.strptime(str(recData['maxInvDate']),'%Y-%m-%d')
            agingDay=(currentDate-invoice_date).days
        except:
            agingDay=''
        
        outstandingPercent=0
        if invNetAmt!=0:
            try:
                outstandingPercent=round((outstanding/invNetAmt*100),2)
            except:
                outstandingPercent=0
                
        sup_id1=''
        sup_name1=''
        for rsmRow in rsmRows:
            level_id1=rsmRow.level_id
            if level_id1==recData['level1_id']:
                sup_id1=rsmRow.sup_id
                sup_name1=rsmRow.sup_name
                break
        
        
        #------------------------        
        myString+=str(sl)+','+str(recData['level1_id'])+','+str(sup_id1)+','+str(sup_name1)+','+str(recData['invCount'])+','+str(lastInv)+','+str(lastDate)+','+str(invTp)+','+str(invVat)+','+str(invDiscount)+','+str(invSpDisc)+','+str(invNetAmt)+','+str(adjust_amount)+','+str(outTp)+','+str(outVat)+','+str(outDisc)+','+str(outSp)+','+str(outstanding)+','+str(agingDay)+','+str(outstandingPercent)+'\n'
    
    myString+='\n\n\n'
    
    #================================== FM Wise    
    totalInvTP=0
    totalInvVat=0
    totalInvDisc=0
    totalInvAmt=0
    totalInvSp=0
    totalOutsTP=0
    totalOutsVat=0
    totalOutsDisc=0
    totalOutST=0
    totalOutSp=0
    
    sl=0
    myString+='FM Wise:\n'
    myString+='SL,'+str(session.level1Name)+','+str(session.level2Name)+',FMID,FMName,Inv Count,Last Inv,LastDate,Invoice-TP,Invoice-Vat,Invoice-Disc,Invoice-SP,Invoice-Net,Adjusted,Outstanding-TP,Outstanding-Vat,Outstanding-Disc,Outstanding-SP,Outstanding-Net,Aging,Oustanding%'+'\n'
    for i in range(len(fmRecordsList)):
        
        recData=fmRecordsList[i]
        
        #----------
        invTp=recData['actualTpAmt']-(recData['retTpAmt']+recData['retSpDiscAmt'])
        invVat=recData['vatTotalAmt']-recData['retVatAmt']
        invDiscount=recData['discAmt']-recData['retDiscAmt']
        invSpDisc=recData['spDiscAmt']-recData['retSpDiscAmt']
        invNetAmt=invTp+invVat-(invDiscount+invSpDisc)
        
        outstanding=round(invNetAmt-recData['collAmt'],2)
        if outstanding==0:
            continue
        
        sl+=1
        
        try:
#             outTp=(invTp*outstanding)/invNetAmt
#             outVat=(invVat*outstanding)/invNetAmt
#             outDisc=(invDiscount*outstanding)/invNetAmt
#             outSp=(invSpDisc*outstanding)/invNetAmt
            outTp=outstanding*(percentTp_fm/100)
            outVat=outstanding*(percentVat_fm/100)
            outDisc=outstanding*(percentDisc_fm/100)
            outSp=outstanding*(percentSpDisc_fm/100)
        except:
            outTp=0
            outVat=0
            outDisc=0
            outSp=0
            
        #-------
        
        lastInv=str(session.prefix_invoice)+'INV-'+str(recData['maxSl'])                                              
        lastDate=recData['maxInvDate'].strftime('%d-%b-%y')
        
        adjust_amount=recData['adjustAmt']
        
        totalInvTP+=invTp
        totalInvVat+=invVat
        totalInvDisc+=invDiscount
        totalInvSp+=invSpDisc
        totalInvAmt+=invNetAmt
        
        #totalOutsTP+=outTp
        #totalOutsVat+=outVat
        #totalOutsDisc+=outDisc
        #totalOutSp+=outSp
        totalOutST+=outstanding
                
        
        try:            
            invoice_date=datetime.datetime.strptime(str(recData['maxInvDate']),'%Y-%m-%d')        
            agingDay=(currentDate-invoice_date).days
        except:
            agingDay=''
            
        outstandingPercent=0
        if invNetAmt!=0:
            try:
                outstandingPercent=round((outstanding/invNetAmt*100),2)
            except:
                outstandingPercent=0
        
        sup_id2=''
        sup_name2=''
        for fmRow in fmRows:
            level_id2=fmRow.level_id
            if level_id2==recData['level2_id']:
                sup_id2=fmRow.sup_id
                sup_name2=fmRow.sup_name
                break
        
        #------------------------        
        myString+=str(sl)+','+str(recData['level1_id'])+','+str(recData['level2_id'])+','+str(sup_id2)+','+str(sup_name2)+','+str(recData['invCount'])+','+str(lastInv)+','+str(lastDate)+','+str(invTp)+','+str(invVat)+','+str(invDiscount)+','+str(invSpDisc)+','+str(invNetAmt)+','+str(adjust_amount)+','+str(outTp)+','+str(outVat)+','+str(outDisc)+','+str(outSp)+','+str(outstanding)+','+str(agingDay)+','+str(outstandingPercent)+'\n'
    
    myString+='\n\n\n'
        
    #===================================
    totalInvTP=0
    totalInvVat=0
    totalInvDisc=0
    totalInvAmt=0
    totalInvSp=0
    totalOutsTP=0
    totalOutsVat=0
    totalOutsDisc=0
    totalOutST=0
    totalOutSp=0
    
    sl=0
    myString+='MSO Wise:\n'
    myString+='SL,'+str(session.level1Name)+','+str(session.level2Name)+',MSOID,MSOName,Inv Count,Last Inv,LastDate,Invoice-TP,Invoice-Vat,Invoice-Disc,Invoice-SP,Invoice-Net,Adjusted,Outstanding-TP,Outstanding-Vat,Outstanding-Disc,Outstanding-SP,Outstanding-Net,Aging,Oustanding%'+'\n'
    for i in range(len(msoRecordsList)):
                
        recData=msoRecordsList[i]
        
        #----------
        invTp=recData['actualTpAmt']-(recData['retTpAmt']+recData['retSpDiscAmt'])
        invVat=recData['vatTotalAmt']-recData['retVatAmt']
        invDiscount=recData['discAmt']-recData['retDiscAmt']
        invSpDisc=recData['spDiscAmt']-recData['retSpDiscAmt']
        invNetAmt=invTp+invVat-(invDiscount+invSpDisc)
        
        outstanding=round(invNetAmt-recData['collAmt'],2)
        if outstanding==0:
            continue
            
        sl+=1
        
        try:
#             outTp=(invTp*outstanding)/invNetAmt
#             outVat=(invVat*outstanding)/invNetAmt
#             outDisc=(invDiscount*outstanding)/invNetAmt
#             outSp=(invSpDisc*outstanding)/invNetAmt
            outTp=outstanding*(percentTp/100)
            outVat=outstanding*(percentVat/100)
            outDisc=outstanding*(percentDisc/100)
            outSp=outstanding*(percentSpDisc/100)
        except:
            outTp=0
            outVat=0
            outDisc=0
            outSp=0
            
        #-------
        
        lastInv=str(session.prefix_invoice)+'INV-'+str(recData['maxSl'])                                              
        lastDate=recData['maxInvDate'].strftime('%d-%b-%y')
        
        adjust_amount=recData['adjustAmt']
        
        totalInvTP+=invTp
        totalInvVat+=invVat
        totalInvDisc+=invDiscount
        totalInvSp+=invSpDisc
        totalInvAmt+=invNetAmt
        
        #totalOutsTP+=outTp
        #totalOutsVat+=outVat
        #totalOutsDisc+=outDisc
        #totalOutSp+=outSp
        totalOutST+=outstanding
        
        try:            
            invoice_date=datetime.datetime.strptime(str(recData['maxInvDate']),'%Y-%m-%d')        
            agingDay=(currentDate-invoice_date).days
        except:
            agingDay=''
            
        outstandingPercent=0
        if invNetAmt!=0:
            try:
                outstandingPercent=round((outstanding/invNetAmt*100),2)
            except:
                outstandingPercent=0
                
        try:
            rep_id=str(recData['rep_id']).strip()
        except:
            rep_id=rep_id.replace('xa0', '')
            
        try:
            rep_name=str(recData['rep_name']).strip()
        except:
            rep_name=rep_name.replace('xa0', '')
            
        #------------------------        
        myString+=str(sl)+','+str(recData['level1_id'])+','+str(recData['level2_id'])+','+str(rep_id)+','+str(rep_name)+','+str(recData['invCount'])+','+str(lastInv)+','+str(lastDate)+','+str(invTp)+','+str(invVat)+','+str(invDiscount)+','+str(invSpDisc)+','+str(invNetAmt)+','+str(adjust_amount)+','+str(outTp)+','+str(outVat)+','+str(outDisc)+','+str(outSp)+','+str(outstanding)+','+str(agingDay)+','+str(outstandingPercent)+'\n'
    
    
    myString+='\n\nSummary\n'
    
    myString+='Invoice TP,'+str(round(totalInvTP,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Invoice VAT,'+str(round(totalInvVat,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Invoice Discount,'+str(round(totalInvDisc,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Invoice SP.Disc,'+str(round(totalInvSp,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Invoice Net,'+str(round(totalInvAmt,2))+',,,,,,,,,,,,,,,,,,,\n\n'
    
    
    try:
        totalOutsTP=(totalInvTP*totalOutST)/totalInvAmt
        totalOutsVat=(totalInvVat*totalOutST)/totalInvAmt
        totalOutsDisc=(totalInvDisc*totalOutST)/totalInvAmt
        totalOutSp=(totalInvSp*totalOutST)/totalInvAmt
    except:
        totalOutsTP=0
        totalOutsVat=0
        totalOutsDisc=0
        totalOutSp=0
    
    myString+='Outstanding TP,'+str(round(totalOutsTP,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Outstanding VAT,'+str(round(totalOutsVat,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Outstanding Discount,'+str(round(totalOutsDisc,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Outstanding SP.Disc,'+str(round(totalOutSp,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Outstanding Net,'+str(round(totalOutST,2))+',,,,,,,,,,,,,,,,,,,\n'
    
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_RSM_FM_MSOWiseOutstandingSummary.csv'   
    return str(myString)


def negativeBanaceInvoiceWise():
    c_id=session.cid
    
    response.title='6.8 Negative Balance: Invoice Wise'
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    depot_id=str(request.vars.depotID).strip()
    store_id=str(request.vars.storeID).strip()    
    out_st_delivery_man_id=str(request.vars.deliveryManID).strip()    
    out_st_territory_id=str(request.vars.territoryID).strip()    
    out_st_mso_id=str(request.vars.msoID).strip()
    invoice_term=str(request.vars.invoice_term).strip()
    customerId=str(request.vars.customerId).strip()
    
    credit_type=str(request.vars.credit_type).strip()
    customer_cat=str(request.vars.customer_cat).strip() 
    customer_sub_cat=str(request.vars.customer_sub_cat).strip()    
    
    out_st_level1_id=str(request.vars.out_st_level1_id).strip()  
    out_st_level2_id=str(request.vars.out_st_level2_id).strip()  
    
    catName=''
    custCatRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_CATEGORY')&(db.sm_category_type.cat_type_id==customer_cat)).select(db.sm_category_type.cat_type_name, limitby=(0,1))
    if custCatRows:
        catName=custCatRows[0].cat_type_name        
    subCatName=''
    custSubCatRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_SUB_CATEGORY')&(db.sm_category_type.cat_type_id==customer_sub_cat)).select(db.sm_category_type.cat_type_name, limitby=(0,1))
    if custSubCatRows:
        subCatName=custSubCatRows[0].cat_type_name
    
    depot_name=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depot_name=depotRow[0].name
    
    store_name=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        store_name=storeRow[0].store_name
        
    out_st_delivery_man_name=''
    dpRow=db((db.sm_delivery_man.cid==c_id)&(db.sm_delivery_man.depot_id==depot_id)&(db.sm_delivery_man.d_man_id==out_st_delivery_man_id)).select(db.sm_delivery_man.name,limitby=(0,1))
    if dpRow:
        out_st_delivery_man_name=dpRow[0].name
        
    out_st_territory_name=''
    levelRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==out_st_territory_id)).select(db.sm_level.level_name,limitby=(0,1))
    if levelRow:
        out_st_territory_name=levelRow[0].level_name
        
    out_st_mso_name=''
    repRow=db((db.sm_rep.cid==c_id)&(db.sm_rep.rep_id==out_st_mso_id)).select(db.sm_rep.name,limitby=(0,1))
    if repRow:
        out_st_mso_name=repRow[0].name
        
    customerName=''
    clientRow=db((db.sm_client.cid==c_id)&(db.sm_client.depot_id==depot_id)&(db.sm_client.client_id==customerId)).select(db.sm_client.name,limitby=(0,1))
    if clientRow:
        customerName=clientRow[0].name
        
    try:        
        startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d').strftime('%Y-%m-%d')
    except:
        startDt=''                
    
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d').strftime('%Y-%m-%d')
   
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    
    qset=db()
    qset=qset(db.sm_invoice_head.cid==c_id)
    qset=qset(db.sm_invoice_head.depot_id==depot_id)
    qset=qset(db.sm_invoice_head.store_id==store_id)
    
    if startDt!='' and endDt!='':        
        qset=qset((db.sm_invoice_head.invoice_date>=startDt)&(db.sm_invoice_head.invoice_date<=endDt))
    else:
        qset=qset(db.sm_invoice_head.invoice_date<=endDt)
        
    qset=qset(db.sm_invoice_head.status=='Invoiced')
    qset=qset(db.sm_invoice_head.total_amount-(db.sm_invoice_head.return_tp+db.sm_invoice_head.return_vat-db.sm_invoice_head.return_discount) < db.sm_invoice_head.collection_amount)
    
    if out_st_delivery_man_id!='':
        qset=qset(db.sm_invoice_head.d_man_id==out_st_delivery_man_id)
    if out_st_territory_id!='':
        qset=qset(db.sm_invoice_head.area_id==out_st_territory_id)
    if out_st_mso_id!='':
        qset=qset(db.sm_invoice_head.rep_id==out_st_mso_id)
    if invoice_term!='':
        qset=qset(db.sm_invoice_head.payment_mode==invoice_term)
    if customerId!='':
        qset=qset(db.sm_invoice_head.client_id==customerId)
        
    if credit_type!='':
        qset=qset(db.sm_invoice_head.credit_note==credit_type)
    if customer_cat!='':
        qset=qset(db.sm_invoice_head.cl_category_id==customer_cat)
    if customer_sub_cat!='':
        qset=qset(db.sm_invoice_head.cl_sub_category_id==customer_sub_cat)
        
    if out_st_level1_id!='':
        qset=qset(db.sm_invoice_head.level1_id==out_st_level1_id)
    if out_st_level2_id!='':
        qset=qset(db.sm_invoice_head.level2_id==out_st_level2_id)
        
    records=qset.select(db.sm_invoice_head.ALL,orderby=db.sm_invoice_head.area_id|db.sm_invoice_head.sl)
    
    #====================
    p_totalInvTP=0
    p_totalInvVat=0
    p_totalInvDisc=0
    p_totalInvSp=0
    p_totalInvAmt=0
    percentTp=0
    percentVat=0
    percentDisc=0
    percentSpDisc=0
    
    for record in records:        
        p_invTp=record.actual_total_tp-(record.return_tp+record.return_sp_discount)
        p_invVat=record.vat_total_amount-record.return_vat
        p_invDiscount=record.discount-record.return_discount
        p_invSpDisc=record.sp_discount-record.return_sp_discount
        p_invNetAmt=p_invTp+p_invVat-(p_invDiscount+p_invSpDisc)
        
        p_outstanding=round(p_invNetAmt-record.collection_amount,2)
        if p_outstanding==0:
            continue
            
        p_totalInvTP+=p_invTp
        p_totalInvVat+=p_invVat
        p_totalInvDisc+=p_invDiscount
        p_totalInvSp+=p_invSpDisc
        p_totalInvAmt+=p_invNetAmt
        
    try:
        percentTp=p_totalInvTP/p_totalInvAmt*100
        percentVat=p_totalInvVat/p_totalInvAmt*100
        percentDisc=p_totalInvDisc/p_totalInvAmt*100
        percentSpDisc=p_totalInvSp/p_totalInvAmt*100
    except:
        percentTp=0
        percentVat=0
        percentDisc=0
        percentSpDisc=0
    #======================
    
    return dict(percentTp=percentTp,percentVat=percentVat,percentDisc=percentDisc,percentSpDisc=percentSpDisc,records=records,fromDate=fromDate,toDate=toDate,depotID=depot_id,depotName=depot_name,storeID=store_id,storeName=store_name,deliveryManID=out_st_delivery_man_id,deliveryManName=out_st_delivery_man_name,territoryID=out_st_territory_id,territoryName=out_st_territory_name,msoID=out_st_mso_id,msoName=out_st_mso_name,invoice_term=invoice_term,customerId=customerId,customerName=customerName,credit_type=credit_type,customer_cat=customer_cat,customer_sub_cat=customer_sub_cat,catName=catName,subCatName=subCatName,out_st_level1_id=out_st_level1_id,out_st_level2_id=out_st_level2_id,page=page,items_per_page=items_per_page)    
    

def negativeBanaceInvoiceWise_download():
    c_id=session.cid
    
    currentDate=datetime.datetime.strptime(str(current_date),'%Y-%m-%d')
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    depot_id=str(request.vars.depotID).strip()
    store_id=str(request.vars.storeID).strip()    
    out_st_delivery_man_id=str(request.vars.deliveryManID).strip()    
    out_st_territory_id=str(request.vars.territoryID).strip()    
    out_st_mso_id=str(request.vars.msoID).strip()
    invoice_term=str(request.vars.invoice_term).strip()
    customerId=str(request.vars.customerId).strip()
    
    credit_type=str(request.vars.credit_type).strip()
    customer_cat=str(request.vars.customer_cat).strip() 
    customer_sub_cat=str(request.vars.customer_sub_cat).strip()    
    
    out_st_level1_id=str(request.vars.out_st_level1_id).strip()  
    out_st_level2_id=str(request.vars.out_st_level2_id).strip()  
    
    catName=''
    custCatRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_CATEGORY')&(db.sm_category_type.cat_type_id==customer_cat)).select(db.sm_category_type.cat_type_name, limitby=(0,1))
    if custCatRows:
        catName=custCatRows[0].cat_type_name        
    subCatName=''
    custSubCatRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_SUB_CATEGORY')&(db.sm_category_type.cat_type_id==customer_sub_cat)).select(db.sm_category_type.cat_type_name, limitby=(0,1))
    if custSubCatRows:
        subCatName=custSubCatRows[0].cat_type_name
    
    depot_name=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depot_name=depotRow[0].name
    
    store_name=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        store_name=storeRow[0].store_name
        
    out_st_delivery_man_name=''
    dpRow=db((db.sm_delivery_man.cid==c_id)&(db.sm_delivery_man.depot_id==depot_id)&(db.sm_delivery_man.d_man_id==out_st_delivery_man_id)).select(db.sm_delivery_man.name,limitby=(0,1))
    if dpRow:
        out_st_delivery_man_name=dpRow[0].name
        
    out_st_territory_name=''
    levelRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==out_st_territory_id)).select(db.sm_level.level_name,limitby=(0,1))
    if levelRow:
        out_st_territory_name=levelRow[0].level_name
        
    out_st_mso_name=''
    repRow=db((db.sm_rep.cid==c_id)&(db.sm_rep.rep_id==out_st_mso_id)).select(db.sm_rep.name,limitby=(0,1))
    if repRow:
        out_st_mso_name=repRow[0].name
        
    customerName=''
    clientRow=db((db.sm_client.cid==c_id)&(db.sm_client.depot_id==depot_id)&(db.sm_client.client_id==customerId)).select(db.sm_client.name,limitby=(0,1))
    if clientRow:
        customerName=clientRow[0].name
        
    try:        
        startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d').strftime('%Y-%m-%d')
    except:
        startDt=''                
    
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d').strftime('%Y-%m-%d')
   
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    
    qset=db()
    qset=qset(db.sm_invoice_head.cid==c_id)
    qset=qset(db.sm_invoice_head.depot_id==depot_id)
    qset=qset(db.sm_invoice_head.store_id==store_id)
    
    if startDt!='' and endDt!='':        
        qset=qset((db.sm_invoice_head.invoice_date>=startDt)&(db.sm_invoice_head.invoice_date<=endDt))
    else:
        qset=qset(db.sm_invoice_head.invoice_date<=endDt)
        
    qset=qset(db.sm_invoice_head.status=='Invoiced')
    qset=qset(db.sm_invoice_head.total_amount-(db.sm_invoice_head.return_tp+db.sm_invoice_head.return_vat-db.sm_invoice_head.return_discount) < db.sm_invoice_head.collection_amount)
    
    if out_st_delivery_man_id!='':
        qset=qset(db.sm_invoice_head.d_man_id==out_st_delivery_man_id)
    if out_st_territory_id!='':
        qset=qset(db.sm_invoice_head.area_id==out_st_territory_id)
    if out_st_mso_id!='':
        qset=qset(db.sm_invoice_head.rep_id==out_st_mso_id)
    if invoice_term!='':
        qset=qset(db.sm_invoice_head.payment_mode==invoice_term)
    if customerId!='':
        qset=qset(db.sm_invoice_head.client_id==customerId)
        
    if credit_type!='':
        qset=qset(db.sm_invoice_head.credit_note==credit_type)
    if customer_cat!='':
        qset=qset(db.sm_invoice_head.cl_category_id==customer_cat)
    if customer_sub_cat!='':
        qset=qset(db.sm_invoice_head.cl_sub_category_id==customer_sub_cat)
      
    if out_st_level1_id!='':
        qset=qset(db.sm_invoice_head.level1_id==out_st_level1_id)
    if out_st_level2_id!='':
        qset=qset(db.sm_invoice_head.level2_id==out_st_level2_id)
        
    records=qset.select(db.sm_invoice_head.ALL,orderby=db.sm_invoice_head.area_id|db.sm_invoice_head.sl)
    
    #====================
    p_totalInvTP=0
    p_totalInvVat=0
    p_totalInvDisc=0
    p_totalInvSp=0
    p_totalInvAmt=0
    percentTp=0
    percentVat=0
    percentDisc=0
    percentSpDisc=0
    
    for record in records:        
        p_invTp=record.actual_total_tp-(record.return_tp+record.return_sp_discount)
        p_invVat=record.vat_total_amount-record.return_vat
        p_invDiscount=record.discount-record.return_discount
        p_invSpDisc=record.sp_discount-record.return_sp_discount
        p_invNetAmt=p_invTp+p_invVat-(p_invDiscount+p_invSpDisc)
        
        p_outstanding=round(p_invNetAmt-record.collection_amount,2)
        if p_outstanding==0:
            continue
            
        p_totalInvTP+=p_invTp
        p_totalInvVat+=p_invVat
        p_totalInvDisc+=p_invDiscount
        p_totalInvSp+=p_invSpDisc
        p_totalInvAmt+=p_invNetAmt
        
    try:
        percentTp=p_totalInvTP/p_totalInvAmt*100
        percentVat=p_totalInvVat/p_totalInvAmt*100
        percentDisc=p_totalInvDisc/p_totalInvAmt*100
        percentSpDisc=p_totalInvSp/p_totalInvAmt*100
    except:
        percentTp=0
        percentVat=0
        percentDisc=0
        percentSpDisc=0
    #======================
    
    myString='6.8 Negative Balance: Invoice Wise\n'
    myString+='Inv Date From:,'+str(startDt)+'\n'
    myString+='To/ as of Date:'+','+str(endDt)+'\n'
    myString+='Inv Term:,'+str(invoice_term)+'\n'
    myString+='Branch ID:,'+str(depot_id)+'\n'
    myString+='Branch Name'+','+str(depot_name)+'\n'
    myString+='Store ID:,'+str(store_id)+'\n'
    myString+='Store Name'+','+str(store_name)+'\n'
    myString+='DP ID:,'+str(out_st_delivery_man_id)+'\n'
    myString+='DP Name'+','+str(out_st_delivery_man_name)+'\n'
    myString+='Territory ID:,'+str(out_st_territory_id)+'\n'
    myString+='Territory Name'+','+str(out_st_territory_name)+'\n'
    myString+='MSO ID:,'+str(out_st_mso_id)+'\n'
    myString+='MSO Name'+','+str(out_st_mso_name)+'\n'
    myString+='Customer ID:,'+str(customerId)+'\n'
    myString+='Customer Name'+','+str(customerName)+'\n'
    
    myString+='Credit Type:,'+str(credit_type)+'\n'    
    if catName=='':
        catName='ALL'
    if subCatName=='':
        subCatName='ALL'        
    myString+='Customer Category'+','+str(catName)+'\n'
    myString+='Customer Sub-Category'+','+str(subCatName)+'\n'
    
    myString+=str(session.level1Name)+','+str(out_st_level1_id)+'\n'
    myString+=str(session.level2Name)+','+str(out_st_level2_id)+'\n'
    
    totalInvTP=0
    totalInvVat=0
    totalInvDisc=0
    totalInvAmt=0
    totalInvSp=0
    totalOutsTP=0
    totalOutsVat=0
    totalOutsDisc=0
    totalOutST=0
    totalOutSp=0
    
    sl=0
    myString+='SL,Date,Inv.No,Cust.ID,Cust.Name,MSO ID,MSO Name,DP ID,DP Name,Terms,Tr.Code,Market,Invoice-TP,Invoice-Vat,Invoice-Disc,Invoice-SP,Invoice-Net,Adjusted,Outstanding-TP,Outstanding-Vat,Outstanding-Disc,Outstanding-SP,Outstanding-Net,Aging,Oustanding%'+'\n'
    for row in records:
        sl+=1
        depot_id=row.depot_id
        invoice_date=row.invoice_date
        invNo=str(session.prefix_invoice)+'INV'+str(depot_id)+'-'+str(row.sl)
        client_id=row.client_id
        client_name=str(row.client_name).replace(',', ' ')
        rep_id=row.rep_id
        rep_name=str(row.rep_name).replace(',', ' ')
        d_man_id=row.d_man_id
        d_man_name=str(row.d_man_name).replace(',', ' ')
        payment_mode=row.payment_mode
        area_id=row.area_id
        market_name=str(row.market_name).replace(',', ' ')
        
        invTp=row.actual_total_tp-(row.return_tp+row.return_sp_discount)
        invVat=row.vat_total_amount-row.return_vat
        invDiscount=row.discount-row.return_discount
        invSpDisc=row.sp_discount-row.return_sp_discount
        invNetAmt=invTp+invVat-(invDiscount+invSpDisc)
        
        adjust_amount=row.adjust_amount
        
        outstanding=round(invNetAmt-row.collection_amount,2)      
        if outstanding==0:
            continue
            
        try:
#             outTp=(invTp*outstanding)/invNetAmt
#             outVat=(invVat*outstanding)/invNetAmt
#             outDisc=(invDiscount*outstanding)/invNetAmt
#             outSp=(invSpDisc*outstanding)/invNetAmt
            outTp=outstanding*(percentTp/100)
            outVat=outstanding*(percentVat/100)
            outDisc=outstanding*(percentDisc/100)
            outSp=outstanding*(percentSpDisc/100)
        except:
            outTp=0
            outVat=0
            outDisc=0
            outSp=0
        
        totalInvTP+=invTp
        totalInvVat+=invVat
        totalInvDisc+=invDiscount
        totalInvSp+=invSpDisc
        totalInvAmt+=invNetAmt
        
        #totalOutsTP+=outTp
        #totalOutsVat+=outVat
        #totalOutsDisc+=outDisc
        #totalOutSp+=outSp
        totalOutST+=outstanding
        
        invoice_date=datetime.datetime.strptime(str(row.invoice_date),'%Y-%m-%d')
        agingDay=(currentDate-invoice_date).days
        
        if invNetAmt!=0:
            outstandingPercent=round((outstanding/invNetAmt*100),2)
        else:
            outstandingPercent=0
            
        #------------------------        
        myString+=str(sl)+','+str(invoice_date)+','+str(invNo)+','+str(client_id)+','+str(client_name)+','+str(rep_id)+','+str(rep_name)+','+str(d_man_id)+','+str(d_man_name)+','+str(payment_mode)+','+str(area_id)+','+str(market_name)+','+str(invTp)+','+\
        str(invVat)+','+str(invDiscount)+','+str(invSpDisc)+','+str(invNetAmt)+','+str(adjust_amount)+','+str(outTp)+','+str(outVat)+','+str(outDisc)+','+str(outSp)+','+str(outstanding)+','+\
        str(agingDay)+','+str(outstandingPercent)+'\n'
    
    myString+='\n\nSummary,,,,,,,,,,,,,,,,,,,,\n'
    
    myString+='Invoice TP,'+str(round(totalInvTP,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Invoice VAT,'+str(round(totalInvVat,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Invoice Discount,'+str(round(totalInvDisc,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Invoice SP.Disc,'+str(round(totalInvSp,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Invoice Net,'+str(round(totalInvAmt,2))+',,,,,,,,,,,,,,,,,,,\n\n'
    
    try:
        totalOutsTP=(totalInvTP*totalOutST)/totalInvAmt
        totalOutsVat=(totalInvVat*totalOutST)/totalInvAmt
        totalOutsDisc=(totalInvDisc*totalOutST)/totalInvAmt
        totalOutSp=(totalInvSp*totalOutST)/totalInvAmt
    except:
        totalOutsTP=0
        totalOutsVat=0
        totalOutsDisc=0
        totalOutSp=0
        
    myString+='Outstanding TP,'+str(round(totalOutsTP,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Outstanding VAT,'+str(round(totalOutsVat,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Outstanding Discount,'+str(round(totalOutsDisc,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Outstanding SP.Disc,'+str(round(totalOutSp,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Outstanding Net,'+str(round(totalOutST,2))+',,,,,,,,,,,,,,,,,,,\n'
    
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_negativeBanaceInvWiseOutstanding.csv'   
    return str(myString)

def outStTerritoryWiseDetails():
    c_id=session.cid
    
    response.title='6.7 Outstanding Territory Wise Details'
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    depot_id=str(request.vars.depotID).strip()
    store_id=str(request.vars.storeID).strip()    
    out_st_delivery_man_id=str(request.vars.deliveryManID).strip()    
    out_st_territory_id=str(request.vars.territoryID).strip()    
    out_st_mso_id=str(request.vars.msoID).strip()
    invoice_term=str(request.vars.invoice_term).strip()
    customerId=str(request.vars.customerId).strip()
    
    credit_type=str(request.vars.credit_type).strip()
    customer_cat=str(request.vars.customer_cat).strip() 
    customer_sub_cat=str(request.vars.customer_sub_cat).strip()    
    
    out_st_level1_id=str(request.vars.out_st_level1_id).strip()  
    out_st_level2_id=str(request.vars.out_st_level2_id).strip()  
    
    catName=''
    custCatRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_CATEGORY')&(db.sm_category_type.cat_type_id==customer_cat)).select(db.sm_category_type.cat_type_name, limitby=(0,1))
    if custCatRows:
        catName=custCatRows[0].cat_type_name        
    subCatName=''
    custSubCatRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_SUB_CATEGORY')&(db.sm_category_type.cat_type_id==customer_sub_cat)).select(db.sm_category_type.cat_type_name, limitby=(0,1))
    if custSubCatRows:
        subCatName=custSubCatRows[0].cat_type_name
    
    depot_name=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depot_name=depotRow[0].name
    
    store_name=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        store_name=storeRow[0].store_name
        
    out_st_delivery_man_name=''
    dpRow=db((db.sm_delivery_man.cid==c_id)&(db.sm_delivery_man.depot_id==depot_id)&(db.sm_delivery_man.d_man_id==out_st_delivery_man_id)).select(db.sm_delivery_man.name,limitby=(0,1))
    if dpRow:
        out_st_delivery_man_name=dpRow[0].name
        
    out_st_territory_name=''
    levelRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==out_st_territory_id)).select(db.sm_level.level_name,limitby=(0,1))
    if levelRow:
        out_st_territory_name=levelRow[0].level_name
        
    out_st_mso_name=''
    repRow=db((db.sm_rep.cid==c_id)&(db.sm_rep.rep_id==out_st_mso_id)).select(db.sm_rep.name,limitby=(0,1))
    if repRow:
        out_st_mso_name=repRow[0].name
        
    customerName=''
    clientRow=db((db.sm_client.cid==c_id)&(db.sm_client.depot_id==depot_id)&(db.sm_client.client_id==customerId)).select(db.sm_client.name,limitby=(0,1))
    if clientRow:
        customerName=clientRow[0].name
       
    try:        
        startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d').strftime('%Y-%m-%d')     
    except:
        startDt=''
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d').strftime('%Y-%m-%d')
   
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    qset=db()
    qset=qset(db.sm_invoice_head.cid==c_id)
    qset=qset(db.sm_invoice_head.depot_id==depot_id)
    qset=qset(db.sm_invoice_head.store_id==store_id)
    
    if startDt!='' and endDt!='':        
        qset=qset((db.sm_invoice_head.invoice_date>=startDt)&(db.sm_invoice_head.invoice_date<=endDt))
    else:
        qset=qset(db.sm_invoice_head.invoice_date<=endDt)
        
    qset=qset(db.sm_invoice_head.status=='Invoiced')
    qset=qset(db.sm_invoice_head.total_amount-(db.sm_invoice_head.return_tp+db.sm_invoice_head.return_vat-db.sm_invoice_head.return_discount)-db.sm_invoice_head.collection_amount!=0)
    
    if out_st_delivery_man_id!='':
        qset=qset(db.sm_invoice_head.d_man_id==out_st_delivery_man_id)
    if out_st_territory_id!='':
        qset=qset(db.sm_invoice_head.area_id==out_st_territory_id)
    if out_st_mso_id!='':
        qset=qset(db.sm_invoice_head.rep_id==out_st_mso_id)
    if invoice_term!='':
        qset=qset(db.sm_invoice_head.payment_mode==invoice_term)
    if customerId!='':
        qset=qset(db.sm_invoice_head.client_id==customerId)
        
    if credit_type!='':
        qset=qset(db.sm_invoice_head.credit_note==credit_type)
    if customer_cat!='':
        qset=qset(db.sm_invoice_head.cl_category_id==customer_cat)
    if customer_sub_cat!='':
        qset=qset(db.sm_invoice_head.cl_sub_category_id==customer_sub_cat)
      
    if out_st_level1_id!='':
        qset=qset(db.sm_invoice_head.level1_id==out_st_level1_id)
    if out_st_level2_id!='':
        qset=qset(db.sm_invoice_head.level2_id==out_st_level2_id)
        
    records=qset.select(db.sm_invoice_head.sl,db.sm_invoice_head.invoice_date,db.sm_invoice_head.client_id,db.sm_invoice_head.client_name,db.sm_invoice_head.market_name,db.sm_invoice_head.adjust_amount,db.sm_invoice_head.payment_mode,db.sm_invoice_head.area_id,db.sm_invoice_head.actual_total_tp,db.sm_invoice_head.total_amount,db.sm_invoice_head.vat_total_amount,db.sm_invoice_head.discount,db.sm_invoice_head.sp_discount,db.sm_invoice_head.return_tp,db.sm_invoice_head.return_vat,db.sm_invoice_head.return_discount,db.sm_invoice_head.return_sp_discount,db.sm_invoice_head.collection_amount,orderby=db.sm_invoice_head.area_id|db.sm_invoice_head.client_name)
    
    #====================
    p_totalInvTP=0
    p_totalInvVat=0
    p_totalInvDisc=0
    p_totalInvSp=0
    p_totalInvAmt=0
    percentTp=0
    percentVat=0
    percentDisc=0
    percentSpDisc=0
    
    for record in records:        
        p_invTp=record.actual_total_tp-(record.return_tp+record.return_sp_discount)
        p_invVat=record.vat_total_amount-record.return_vat
        p_invDiscount=record.discount-record.return_discount
        p_invSpDisc=record.sp_discount-record.return_sp_discount
        p_invNetAmt=p_invTp+p_invVat-(p_invDiscount+p_invSpDisc)
        
        p_outstanding=round(p_invNetAmt-record.collection_amount,2)
        if p_outstanding==0:
            continue
            
        p_totalInvTP+=p_invTp
        p_totalInvVat+=p_invVat
        p_totalInvDisc+=p_invDiscount
        p_totalInvSp+=p_invSpDisc
        p_totalInvAmt+=p_invNetAmt
        
    try:
        percentTp=p_totalInvTP/p_totalInvAmt*100
        percentVat=p_totalInvVat/p_totalInvAmt*100
        percentDisc=p_totalInvDisc/p_totalInvAmt*100
        percentSpDisc=p_totalInvSp/p_totalInvAmt*100
    except:
        percentTp=0
        percentVat=0
        percentDisc=0
        percentSpDisc=0
    #======================
    
    return dict(percentTp=percentTp,percentVat=percentVat,percentDisc=percentDisc,percentSpDisc=percentSpDisc,records=records,fromDate=fromDate,toDate=toDate,depotID=depot_id,depotName=depot_name,storeID=store_id,storeName=store_name,deliveryManID=out_st_delivery_man_id,deliveryManName=out_st_delivery_man_name,territoryID=out_st_territory_id,territoryName=out_st_territory_name,msoID=out_st_mso_id,msoName=out_st_mso_name,invoice_term=invoice_term,customerId=customerId,customerName=customerName,credit_type=credit_type,customer_cat=customer_cat,customer_sub_cat=customer_sub_cat,catName=catName,subCatName=subCatName,out_st_level1_id=out_st_level1_id,out_st_level2_id=out_st_level2_id,page=page,items_per_page=items_per_page)    


def outStTerritoryWiseDetails_download():
    c_id=session.cid
    
    currentDate=datetime.datetime.strptime(str(current_date),'%Y-%m-%d')
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    depot_id=str(request.vars.depotID).strip()
    store_id=str(request.vars.storeID).strip()    
    out_st_delivery_man_id=str(request.vars.deliveryManID).strip()    
    out_st_territory_id=str(request.vars.territoryID).strip()    
    out_st_mso_id=str(request.vars.msoID).strip()
    invoice_term=str(request.vars.invoice_term).strip()
    customerId=str(request.vars.customerId).strip()
    
    credit_type=str(request.vars.credit_type).strip()
    customer_cat=str(request.vars.customer_cat).strip() 
    customer_sub_cat=str(request.vars.customer_sub_cat).strip()    
    
    out_st_level1_id=str(request.vars.out_st_level1_id).strip()  
    out_st_level2_id=str(request.vars.out_st_level2_id).strip()  
    
    catName=''
    custCatRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_CATEGORY')&(db.sm_category_type.cat_type_id==customer_cat)).select(db.sm_category_type.cat_type_name, limitby=(0,1))
    if custCatRows:
        catName=custCatRows[0].cat_type_name        
    subCatName=''
    custSubCatRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_SUB_CATEGORY')&(db.sm_category_type.cat_type_id==customer_sub_cat)).select(db.sm_category_type.cat_type_name, limitby=(0,1))
    if custSubCatRows:
        subCatName=custSubCatRows[0].cat_type_name
    
    depot_name=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depot_name=depotRow[0].name
    
    store_name=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        store_name=storeRow[0].store_name
        
    out_st_delivery_man_name=''
    dpRow=db((db.sm_delivery_man.cid==c_id)&(db.sm_delivery_man.depot_id==depot_id)&(db.sm_delivery_man.d_man_id==out_st_delivery_man_id)).select(db.sm_delivery_man.name,limitby=(0,1))
    if dpRow:
        out_st_delivery_man_name=dpRow[0].name
        
    out_st_territory_name=''
    levelRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==out_st_territory_id)).select(db.sm_level.level_name,limitby=(0,1))
    if levelRow:
        out_st_territory_name=levelRow[0].level_name
        
    out_st_mso_name=''
    repRow=db((db.sm_rep.cid==c_id)&(db.sm_rep.rep_id==out_st_mso_id)).select(db.sm_rep.name,limitby=(0,1))
    if repRow:
        out_st_mso_name=repRow[0].name
        
    customerName=''
    clientRow=db((db.sm_client.cid==c_id)&(db.sm_client.depot_id==depot_id)&(db.sm_client.client_id==customerId)).select(db.sm_client.name,limitby=(0,1))
    if clientRow:
        customerName=clientRow[0].name
       
    try:        
        startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d').strftime('%Y-%m-%d')     
    except:
        startDt=''
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d').strftime('%Y-%m-%d')
   
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    qset=db()
    qset=qset(db.sm_invoice_head.cid==c_id)
    qset=qset(db.sm_invoice_head.depot_id==depot_id)
    qset=qset(db.sm_invoice_head.store_id==store_id)
    
    if startDt!='' and endDt!='':        
        qset=qset((db.sm_invoice_head.invoice_date>=startDt)&(db.sm_invoice_head.invoice_date<=endDt))
    else:
        qset=qset(db.sm_invoice_head.invoice_date<=endDt)
    
    qset=qset(db.sm_invoice_head.status=='Invoiced')
    qset=qset(db.sm_invoice_head.total_amount-(db.sm_invoice_head.return_tp+db.sm_invoice_head.return_vat-db.sm_invoice_head.return_discount)-db.sm_invoice_head.collection_amount!=0)
    
    if out_st_delivery_man_id!='':
        qset=qset(db.sm_invoice_head.d_man_id==out_st_delivery_man_id)
    if out_st_territory_id!='':
        qset=qset(db.sm_invoice_head.area_id==out_st_territory_id)
    if out_st_mso_id!='':
        qset=qset(db.sm_invoice_head.rep_id==out_st_mso_id)
    if invoice_term!='':
        qset=qset(db.sm_invoice_head.payment_mode==invoice_term)
    if customerId!='':
        qset=qset(db.sm_invoice_head.client_id==customerId)
        
    if credit_type!='':
        qset=qset(db.sm_invoice_head.credit_note==credit_type)
    if customer_cat!='':
        qset=qset(db.sm_invoice_head.cl_category_id==customer_cat)
    if customer_sub_cat!='':
        qset=qset(db.sm_invoice_head.cl_sub_category_id==customer_sub_cat)
      
    if out_st_level1_id!='':
        qset=qset(db.sm_invoice_head.level1_id==out_st_level1_id)
    if out_st_level2_id!='':
        qset=qset(db.sm_invoice_head.level2_id==out_st_level2_id)
        
    records=qset.select(db.sm_invoice_head.sl,db.sm_invoice_head.invoice_date,db.sm_invoice_head.client_id,db.sm_invoice_head.client_name,db.sm_invoice_head.market_name,db.sm_invoice_head.adjust_amount,db.sm_invoice_head.payment_mode,db.sm_invoice_head.area_id,db.sm_invoice_head.actual_total_tp,db.sm_invoice_head.total_amount,db.sm_invoice_head.vat_total_amount,db.sm_invoice_head.discount,db.sm_invoice_head.sp_discount,db.sm_invoice_head.return_tp,db.sm_invoice_head.return_vat,db.sm_invoice_head.return_discount,db.sm_invoice_head.return_sp_discount,db.sm_invoice_head.collection_amount,orderby=db.sm_invoice_head.area_id|db.sm_invoice_head.client_name)
    
    #====================
    p_totalInvTP=0
    p_totalInvVat=0
    p_totalInvDisc=0
    p_totalInvSp=0
    p_totalInvAmt=0
    percentTp=0
    percentVat=0
    percentDisc=0
    percentSpDisc=0
    
    for record in records:        
        p_invTp=record.actual_total_tp-(record.return_tp+record.return_sp_discount)
        p_invVat=record.vat_total_amount-record.return_vat
        p_invDiscount=record.discount-record.return_discount
        p_invSpDisc=record.sp_discount-record.return_sp_discount
        p_invNetAmt=p_invTp+p_invVat-(p_invDiscount+p_invSpDisc)
        
        p_outstanding=round(p_invNetAmt-record.collection_amount,2)
        if p_outstanding==0:
            continue
            
        p_totalInvTP+=p_invTp
        p_totalInvVat+=p_invVat
        p_totalInvDisc+=p_invDiscount
        p_totalInvSp+=p_invSpDisc
        p_totalInvAmt+=p_invNetAmt
        
    try:
        percentTp=p_totalInvTP/p_totalInvAmt*100
        percentVat=p_totalInvVat/p_totalInvAmt*100
        percentDisc=p_totalInvDisc/p_totalInvAmt*100
        percentSpDisc=p_totalInvSp/p_totalInvAmt*100
    except:
        percentTp=0
        percentVat=0
        percentDisc=0
        percentSpDisc=0
    #======================
    
    myString='6.7 Territory Wise Details Outstanding\n'
    myString+='Inv Date From:,'+str(startDt)+'\n'
    myString+='To/ as of Date:'+','+str(endDt)+'\n'
    myString+='Inv Term:,'+str(invoice_term)+'\n'
    myString+='Branch ID:,'+str(depot_id)+'\n'
    myString+='Branch Name'+','+str(depot_name)+'\n'
    myString+='Store ID:,'+str(store_id)+'\n'
    myString+='Store Name'+','+str(store_name)+'\n'
    myString+='DP ID:,'+str(out_st_delivery_man_id)+'\n'
    myString+='DP Name'+','+str(out_st_delivery_man_name)+'\n'
    myString+='Territory ID:,'+str(out_st_territory_id)+'\n'
    myString+='Territory Name'+','+str(out_st_territory_name)+'\n'
    myString+='MSO ID:,'+str(out_st_mso_id)+'\n'
    myString+='MSO Name'+','+str(out_st_mso_name)+'\n'
    myString+='Customer ID:,'+str(customerId)+'\n'
    myString+='Customer Name'+','+str(customerName)+'\n'
    
    myString+='Credit Type:,'+str(credit_type)+'\n'    
    if catName=='':
        catName='ALL'
    if subCatName=='':
        subCatName='ALL'        
    myString+='Customer Category'+','+str(catName)+'\n'
    myString+='Customer Sub-Category'+','+str(subCatName)+'\n'
    
    myString+=str(session.level1Name)+','+str(out_st_level1_id)+'\n'
    myString+=str(session.level2Name)+','+str(out_st_level2_id)+'\n'
    
    totalInvTP=0
    totalInvVat=0
    totalInvDisc=0
    totalInvAmt=0
    totalInvSp=0
    totalOutsTP=0
    totalOutsVat=0
    totalOutsDisc=0
    totalOutST=0
    totalOutSp=0
    
    sl=0
    myString+='SL,Date,Inv.No,Cust.ID,Cust.Name,Tr.Code,Market,Invoice-TP,Invoice-Vat,Invoice-Disc,Invoice-SP,Invoice-Net,Adjusted,Outstanding-TP,Outstanding-Vat,Outstanding-Disc,Outstanding-SP,Outstanding-Net,Aging,Oustanding%'+'\n'
    for row in records:
        
        invoice_date=row.invoice_date
        invNo=str(session.prefix_invoice)+'INV-'+str(row.sl)
        client_id=row.client_id
        client_name=str(row.client_name).replace(',', ' ')
        payment_mode=row.payment_mode
        area_id=row.area_id
        market_name=str(row.market_name).replace(',', ' ')
        
        #-------------
        invTp=row.actual_total_tp-(row.return_tp+row.return_sp_discount)
        invVat=row.vat_total_amount-row.return_vat
        invDiscount=row.discount-row.return_discount
        invSpDisc=row.sp_discount-row.return_sp_discount
        invNetAmt=invTp+invVat-(invDiscount+invSpDisc)
        
        adjust_amount=row.adjust_amount
        
        outstanding=round(invNetAmt-row.collection_amount,2)
        if outstanding==0:
            continue
        sl+=1
        
        try:
#             outTp=(invTp*outstanding)/invNetAmt
#             outVat=(invVat*outstanding)/invNetAmt
#             outDisc=(invDiscount*outstanding)/invNetAmt
#             outSp=(invSpDisc*outstanding)/invNetAmt
            outTp=outstanding*(percentTp/100)
            outVat=outstanding*(percentVat/100)
            outDisc=outstanding*(percentDisc/100)
            outSp=outstanding*(percentSpDisc/100)
        except:
            outTp=0
            outVat=0
            outDisc=0
            outSp=0
        
        totalInvTP+=invTp
        totalInvVat+=invVat
        totalInvDisc+=invDiscount
        totalInvSp+=invSpDisc
        totalInvAmt+=invNetAmt
        
        
        #totalOutsTP+=outTp
        #totalOutsVat+=outVat
        #totalOutsDisc+=outDisc
        #totalOutSp+=outSp
        
        totalOutST+=outstanding
        
        invoice_date=datetime.datetime.strptime(str(row.invoice_date),'%Y-%m-%d')
        agingDay=(currentDate-invoice_date).days
        
        if invNetAmt!=0:
            outstandingPercent=round((outstanding/invNetAmt*100),2)
        else:
            outstandingPercent=0
            
        #-----------------------
        
        myString+=str(sl)+','+str(invoice_date)+','+str(invNo)+','+str(client_id)+','+str(client_name)+','+str(area_id)+','+str(market_name)+','+str(invTp)+','+\
        str(invVat)+','+str(invDiscount)+','+str(invSpDisc)+','+str(invNetAmt)+','+str(adjust_amount)+','+str(outTp)+','+str(outVat)+','+str(outDisc)+','+str(outSp)+','+str(outstanding)+','+\
        str(agingDay)+','+str(outstandingPercent)+'\n'
    
    myString+='\n\nSummary,,,,,,,,,,,,,,,,,,,,\n'
    
    myString+='Invoice TP,'+str(round(totalInvTP,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Invoice VAT,'+str(round(totalInvVat,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Invoice Discount,'+str(round(totalInvDisc,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Invoice SP.Disc,'+str(round(totalInvSp,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Invoice Net,'+str(round(totalInvAmt,2))+',,,,,,,,,,,,,,,,,,,\n\n'
    
    try:
        totalOutsTP=(totalInvTP*totalOutST)/totalInvAmt
        totalOutsVat=(totalInvVat*totalOutST)/totalInvAmt
        totalOutsDisc=(totalInvDisc*totalOutST)/totalInvAmt
        totalOutSp=(totalInvSp*totalOutST)/totalInvAmt
    except:
        totalOutsTP=0
        totalOutsVat=0
        totalOutsDisc=0
        totalOutSp=0
        
    myString+='Outstanding TP,'+str(round(totalOutsTP,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Outstanding VAT,'+str(round(totalOutsVat,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Outstanding Discount,'+str(round(totalOutsDisc,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Outstanding SP.Disc,'+str(round(totalOutSp,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Outstanding Net,'+str(round(totalOutST,2))+',,,,,,,,,,,,,,,,,,,\n'
    
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_TerritoryWiseDetailsOutstanding.csv'   
    return str(myString)



def outStTerritoryWise():
    c_id=session.cid
    
    response.title='6.6 Outstanding Territory Wise'
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    depot_id=str(request.vars.depotID).strip()
    store_id=str(request.vars.storeID).strip()    
    out_st_delivery_man_id=str(request.vars.deliveryManID).strip()    
    out_st_territory_id=str(request.vars.territoryID).strip()    
    out_st_mso_id=str(request.vars.msoID).strip()
    invoice_term=str(request.vars.invoice_term).strip()
    customerId=str(request.vars.customerId).strip()
    
    credit_type=str(request.vars.credit_type).strip()
    customer_cat=str(request.vars.customer_cat).strip() 
    customer_sub_cat=str(request.vars.customer_sub_cat).strip()    
    
    out_st_level1_id=str(request.vars.out_st_level1_id).strip()  
    out_st_level2_id=str(request.vars.out_st_level2_id).strip()  
    
    catName=''
    custCatRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_CATEGORY')&(db.sm_category_type.cat_type_id==customer_cat)).select(db.sm_category_type.cat_type_name, limitby=(0,1))
    if custCatRows:
        catName=custCatRows[0].cat_type_name        
    subCatName=''
    custSubCatRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_SUB_CATEGORY')&(db.sm_category_type.cat_type_id==customer_sub_cat)).select(db.sm_category_type.cat_type_name, limitby=(0,1))
    if custSubCatRows:
        subCatName=custSubCatRows[0].cat_type_name
    
    depot_name=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depot_name=depotRow[0].name
    
    store_name=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        store_name=storeRow[0].store_name
        
    out_st_delivery_man_name=''
    dpRow=db((db.sm_delivery_man.cid==c_id)&(db.sm_delivery_man.depot_id==depot_id)&(db.sm_delivery_man.d_man_id==out_st_delivery_man_id)).select(db.sm_delivery_man.name,limitby=(0,1))
    if dpRow:
        out_st_delivery_man_name=dpRow[0].name
        
    out_st_territory_name=''
    levelRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==out_st_territory_id)).select(db.sm_level.level_name,limitby=(0,1))
    if levelRow:
        out_st_territory_name=levelRow[0].level_name
        
    out_st_mso_name=''
    repRow=db((db.sm_rep.cid==c_id)&(db.sm_rep.rep_id==out_st_mso_id)).select(db.sm_rep.name,limitby=(0,1))
    if repRow:
        out_st_mso_name=repRow[0].name
    
    customerName=''
    clientRow=db((db.sm_client.cid==c_id)&(db.sm_client.depot_id==depot_id)&(db.sm_client.client_id==customerId)).select(db.sm_client.name,limitby=(0,1))
    if clientRow:
        customerName=clientRow[0].name
       
    try:        
        startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d').strftime('%Y-%m-%d')
    except:
        startDt=''                
        
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d').strftime('%Y-%m-%d')
    
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    
    condStr=" AND (round(sm_invoice_head.total_amount-(sm_invoice_head.return_tp+sm_invoice_head.return_vat-sm_invoice_head.return_discount)-sm_invoice_head.collection_amount,2)!=0)"
    
    if out_st_delivery_man_id!='':
        condStr+=" AND (sm_invoice_head.d_man_id='"+out_st_delivery_man_id+"')"        
    if out_st_territory_id!='':
        condStr+=" AND (sm_invoice_head.area_id='"+out_st_territory_id+"')"        
    if out_st_mso_id!='':
        condStr+=" AND (sm_invoice_head.rep_id='"+out_st_mso_id+"')"        
    if invoice_term!='':
        condStr+=" AND (sm_invoice_head.payment_mode='"+invoice_term+"')"
    if customerId!='':
        condStr+=" AND (sm_invoice_head.client_id='"+customerId+"')"
        
    if credit_type!='':
        condStr+=" AND (sm_invoice_head.credit_note='"+credit_type+"')"
    if customer_cat!='':
        condStr+=" AND (sm_invoice_head.cl_category_id='"+customer_cat+"')"
    if customer_sub_cat!='':
        condStr+=" AND (sm_invoice_head.cl_sub_category_id='"+customer_sub_cat+"')"
        
    if out_st_level1_id!='':
        condStr+=" AND (sm_invoice_head.level1_id='"+out_st_level1_id+"')"        
    if out_st_level2_id!='':
        condStr+=" AND (sm_invoice_head.level2_id='"+out_st_level2_id+"')"
        
    if startDt!='' and endDt!='': 
        dateRecords="SELECT sm_invoice_head.area_id as area_id,COUNT(distinct(sm_invoice_head.client_id)) as cusCount,COUNT(distinct(sm_invoice_head.market_id)) as marCount,COUNT(sm_invoice_head.id) as invCount,MAX(sm_invoice_head.sl) as maxSl,MAX(sm_invoice_head.invoice_date) as maxInvDate,SUM(sm_invoice_head.actual_total_tp) as actTpAmt,SUM(sm_invoice_head.total_amount) as totalAmt,SUM(sm_invoice_head.vat_total_amount) as vatTotalAmt,SUM(sm_invoice_head.discount) as discAmt,SUM(sm_invoice_head.adjust_amount) as adjustAmt,SUM(sm_invoice_head.return_tp) as retTpAmt,SUM(sm_invoice_head.return_vat) as retVatAmt,SUM(sm_invoice_head.return_discount) as retDiscAmt,SUM(sm_invoice_head.return_sp_discount) as retSpDiscAmt,SUM(sm_invoice_head.collection_amount) as collAmt,SUM(sm_invoice_head.sp_discount) as spDiscAmt FROM sm_invoice_head WHERE ((sm_invoice_head.cid = '"+c_id+"') AND ((sm_invoice_head.invoice_date >= '"+str(startDt)+"') AND (sm_invoice_head.invoice_date <= '"+str(endDt)+"')) AND (sm_invoice_head.depot_id='"+depot_id+"') AND (sm_invoice_head.store_id='"+store_id+"') AND (sm_invoice_head.status='Invoiced') "+str(condStr)+") GROUP BY sm_invoice_head.area_id ORDER BY sm_invoice_head.area_id"
    else:
        dateRecords="SELECT sm_invoice_head.area_id as area_id,COUNT(distinct(sm_invoice_head.client_id)) as cusCount,COUNT(distinct(sm_invoice_head.market_id)) as marCount,COUNT(sm_invoice_head.id) as invCount,MAX(sm_invoice_head.sl) as maxSl,MAX(sm_invoice_head.invoice_date) as maxInvDate,SUM(sm_invoice_head.actual_total_tp) as actTpAmt,SUM(sm_invoice_head.total_amount) as totalAmt,SUM(sm_invoice_head.vat_total_amount) as vatTotalAmt,SUM(sm_invoice_head.discount) as discAmt,SUM(sm_invoice_head.adjust_amount) as adjustAmt,SUM(sm_invoice_head.return_tp) as retTpAmt,SUM(sm_invoice_head.return_vat) as retVatAmt,SUM(sm_invoice_head.return_discount) as retDiscAmt,SUM(sm_invoice_head.return_sp_discount) as retSpDiscAmt,SUM(sm_invoice_head.collection_amount) as collAmt,SUM(sm_invoice_head.sp_discount) as spDiscAmt FROM sm_invoice_head WHERE ((sm_invoice_head.cid = '"+c_id+"') AND (sm_invoice_head.invoice_date <= '"+str(endDt)+"') AND (sm_invoice_head.depot_id='"+depot_id+"') AND (sm_invoice_head.store_id='"+store_id+"') AND (sm_invoice_head.status='Invoiced') "+str(condStr)+") GROUP BY sm_invoice_head.area_id ORDER BY sm_invoice_head.area_id"
        
    recordList=db.executesql(dateRecords,as_dict = True)
    
    #====================
    p_totalInvTP=0
    p_totalInvVat=0
    p_totalInvDisc=0
    p_totalInvSp=0
    p_totalInvAmt=0
    percentTp=0
    percentVat=0
    percentDisc=0
    percentSpDisc=0
    
    for i in range(len(recordList)):                
        recData=recordList[i]
        
        p_invTp=recData['actTpAmt']-(recData['retTpAmt']+recData['retSpDiscAmt'])   
        p_invVat=recData['vatTotalAmt']-recData['retVatAmt']
        p_invDiscount=recData['discAmt']-recData['retDiscAmt']
        p_invSpDisc=recData['spDiscAmt']-recData['retSpDiscAmt']
        p_invNetAmt=p_invTp+p_invVat-(p_invDiscount+p_invSpDisc)
    
        p_outstanding=round(p_invNetAmt-recData['collAmt'],2)
        
        if p_outstanding==0:
            continue
            
        p_totalInvTP+=p_invTp
        p_totalInvVat+=p_invVat
        p_totalInvDisc+=p_invDiscount
        p_totalInvSp+=p_invSpDisc
        p_totalInvAmt+=p_invNetAmt
        
    try:
        percentTp=p_totalInvTP/p_totalInvAmt*100
        percentVat=p_totalInvVat/p_totalInvAmt*100
        percentDisc=p_totalInvDisc/p_totalInvAmt*100
        percentSpDisc=p_totalInvSp/p_totalInvAmt*100
    except:
        percentTp=0
        percentVat=0
        percentDisc=0
        percentSpDisc=0
    #======================
    
    return dict(percentTp=percentTp,percentVat=percentVat,percentDisc=percentDisc,percentSpDisc=percentSpDisc,recordList=recordList,fromDate=startDt,toDate=endDt,depotID=depot_id,depotName=depot_name,storeID=store_id,storeName=store_name,deliveryManID=out_st_delivery_man_id,deliveryManName=out_st_delivery_man_name,territoryID=out_st_territory_id,territoryName=out_st_territory_name,msoID=out_st_mso_id,msoName=out_st_mso_name,invoice_term=invoice_term,customerId=customerId,customerName=customerName,credit_type=credit_type,customer_cat=customer_cat,customer_sub_cat=customer_sub_cat,catName=catName,subCatName=subCatName,out_st_level1_id=out_st_level1_id,out_st_level2_id=out_st_level2_id,page=page,items_per_page=items_per_page)    

def outStTerritoryWise_download():
    c_id=session.cid
    
    currentDate=datetime.datetime.strptime(str(current_date),'%Y-%m-%d')
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    depot_id=str(request.vars.depotID).strip()
    store_id=str(request.vars.storeID).strip()    
    out_st_delivery_man_id=str(request.vars.deliveryManID).strip()    
    out_st_territory_id=str(request.vars.territoryID).strip()    
    out_st_mso_id=str(request.vars.msoID).strip()
    invoice_term=str(request.vars.invoice_term).strip()
    customerId=str(request.vars.customerId).strip()
    
    credit_type=str(request.vars.credit_type).strip()
    customer_cat=str(request.vars.customer_cat).strip() 
    customer_sub_cat=str(request.vars.customer_sub_cat).strip()    
    
    out_st_level1_id=str(request.vars.out_st_level1_id).strip()  
    out_st_level2_id=str(request.vars.out_st_level2_id).strip()  
    
    catName=''
    custCatRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_CATEGORY')&(db.sm_category_type.cat_type_id==customer_cat)).select(db.sm_category_type.cat_type_name, limitby=(0,1))
    if custCatRows:
        catName=custCatRows[0].cat_type_name        
    subCatName=''
    custSubCatRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_SUB_CATEGORY')&(db.sm_category_type.cat_type_id==customer_sub_cat)).select(db.sm_category_type.cat_type_name, limitby=(0,1))
    if custSubCatRows:
        subCatName=custSubCatRows[0].cat_type_name
    
    depot_name=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depot_name=depotRow[0].name
    
    store_name=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        store_name=storeRow[0].store_name
        
    out_st_delivery_man_name=''
    dpRow=db((db.sm_delivery_man.cid==c_id)&(db.sm_delivery_man.depot_id==depot_id)&(db.sm_delivery_man.d_man_id==out_st_delivery_man_id)).select(db.sm_delivery_man.name,limitby=(0,1))
    if dpRow:
        out_st_delivery_man_name=dpRow[0].name
        
    out_st_territory_name=''
    levelRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==out_st_territory_id)).select(db.sm_level.level_name,limitby=(0,1))
    if levelRow:
        out_st_territory_name=levelRow[0].level_name
        
    out_st_mso_name=''
    repRow=db((db.sm_rep.cid==c_id)&(db.sm_rep.rep_id==out_st_mso_id)).select(db.sm_rep.name,limitby=(0,1))
    if repRow:
        out_st_mso_name=repRow[0].name
    
    customerName=''
    clientRow=db((db.sm_client.cid==c_id)&(db.sm_client.depot_id==depot_id)&(db.sm_client.client_id==customerId)).select(db.sm_client.name,limitby=(0,1))
    if clientRow:
        customerName=clientRow[0].name
       
    try:        
        startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d').strftime('%Y-%m-%d')
    except:
        startDt=''                
        
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d').strftime('%Y-%m-%d')
    
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    
    condStr=" AND (round(sm_invoice_head.total_amount-(sm_invoice_head.return_tp+sm_invoice_head.return_vat-sm_invoice_head.return_discount)-sm_invoice_head.collection_amount,2)!=0)"
    
    if out_st_delivery_man_id!='':
        condStr+=" AND (sm_invoice_head.d_man_id='"+out_st_delivery_man_id+"')"        
    if out_st_territory_id!='':
        condStr+=" AND (sm_invoice_head.area_id='"+out_st_territory_id+"')"        
    if out_st_mso_id!='':
        condStr+=" AND (sm_invoice_head.rep_id='"+out_st_mso_id+"')"        
    if invoice_term!='':
        condStr+=" AND (sm_invoice_head.payment_mode='"+invoice_term+"')"
    if customerId!='':
        condStr+=" AND (sm_invoice_head.client_id='"+customerId+"')"
        
    if credit_type!='':
        condStr+=" AND (sm_invoice_head.credit_note='"+credit_type+"')"
    if customer_cat!='':
        condStr+=" AND (sm_invoice_head.cl_category_id='"+customer_cat+"')"
    if customer_sub_cat!='':
        condStr+=" AND (sm_invoice_head.cl_sub_category_id='"+customer_sub_cat+"')"
    
    if out_st_level1_id!='':
        condStr+=" AND (sm_invoice_head.level1_id='"+out_st_level1_id+"')"        
    if out_st_level2_id!='':
        condStr+=" AND (sm_invoice_head.level2_id='"+out_st_level2_id+"')"
        
    if startDt!='' and endDt!='': 
        dateRecords="SELECT sm_invoice_head.area_id as area_id,COUNT(distinct(sm_invoice_head.client_id)) as cusCount,COUNT(distinct(sm_invoice_head.market_id)) as marCount,COUNT(sm_invoice_head.id) as invCount,MAX(sm_invoice_head.sl) as maxSl,MAX(sm_invoice_head.invoice_date) as maxInvDate,SUM(sm_invoice_head.actual_total_tp) as actTpAmt,SUM(sm_invoice_head.total_amount) as totalAmt,SUM(sm_invoice_head.vat_total_amount) as vatTotalAmt,SUM(sm_invoice_head.discount) as discAmt,SUM(sm_invoice_head.adjust_amount) as adjustAmt,SUM(sm_invoice_head.return_tp) as retTpAmt,SUM(sm_invoice_head.return_vat) as retVatAmt,SUM(sm_invoice_head.return_discount) as retDiscAmt,SUM(sm_invoice_head.return_sp_discount) as retSpDiscAmt,SUM(sm_invoice_head.collection_amount) as collAmt,SUM(sm_invoice_head.sp_discount) as spDiscAmt FROM sm_invoice_head WHERE ((sm_invoice_head.cid = '"+c_id+"') AND ((sm_invoice_head.invoice_date >= '"+str(startDt)+"') AND (sm_invoice_head.invoice_date <= '"+str(endDt)+"')) AND (sm_invoice_head.depot_id='"+depot_id+"') AND (sm_invoice_head.store_id='"+store_id+"') AND (sm_invoice_head.status='Invoiced') "+str(condStr)+") GROUP BY sm_invoice_head.area_id ORDER BY sm_invoice_head.area_id"
    else:
        dateRecords="SELECT sm_invoice_head.area_id as area_id,COUNT(distinct(sm_invoice_head.client_id)) as cusCount,COUNT(distinct(sm_invoice_head.market_id)) as marCount,COUNT(sm_invoice_head.id) as invCount,MAX(sm_invoice_head.sl) as maxSl,MAX(sm_invoice_head.invoice_date) as maxInvDate,SUM(sm_invoice_head.actual_total_tp) as actTpAmt,SUM(sm_invoice_head.total_amount) as totalAmt,SUM(sm_invoice_head.vat_total_amount) as vatTotalAmt,SUM(sm_invoice_head.discount) as discAmt,SUM(sm_invoice_head.adjust_amount) as adjustAmt,SUM(sm_invoice_head.return_tp) as retTpAmt,SUM(sm_invoice_head.return_vat) as retVatAmt,SUM(sm_invoice_head.return_discount) as retDiscAmt,SUM(sm_invoice_head.return_sp_discount) as retSpDiscAmt,SUM(sm_invoice_head.collection_amount) as collAmt,SUM(sm_invoice_head.sp_discount) as spDiscAmt FROM sm_invoice_head WHERE ((sm_invoice_head.cid = '"+c_id+"') AND (sm_invoice_head.invoice_date <= '"+str(endDt)+"') AND (sm_invoice_head.depot_id='"+depot_id+"') AND (sm_invoice_head.store_id='"+store_id+"') AND (sm_invoice_head.status='Invoiced') "+str(condStr)+") GROUP BY sm_invoice_head.area_id ORDER BY sm_invoice_head.area_id"
        
    recordList=db.executesql(dateRecords,as_dict = True)
    
    #====================
    p_totalInvTP=0
    p_totalInvVat=0
    p_totalInvDisc=0
    p_totalInvSp=0
    p_totalInvAmt=0
    percentTp=0
    percentVat=0
    percentDisc=0
    percentSpDisc=0
    
    for i in range(len(recordList)):                
        recData=recordList[i]
        
        p_invTp=recData['actTpAmt']-(recData['retTpAmt']+recData['retSpDiscAmt'])   
        p_invVat=recData['vatTotalAmt']-recData['retVatAmt']
        p_invDiscount=recData['discAmt']-recData['retDiscAmt']
        p_invSpDisc=recData['spDiscAmt']-recData['retSpDiscAmt']
        p_invNetAmt=p_invTp+p_invVat-(p_invDiscount+p_invSpDisc)
    
        p_outstanding=round(p_invNetAmt-recData['collAmt'],2)
        
        if p_outstanding==0:
            continue
            
        p_totalInvTP+=p_invTp
        p_totalInvVat+=p_invVat
        p_totalInvDisc+=p_invDiscount
        p_totalInvSp+=p_invSpDisc
        p_totalInvAmt+=p_invNetAmt
        
    try:
        percentTp=p_totalInvTP/p_totalInvAmt*100
        percentVat=p_totalInvVat/p_totalInvAmt*100
        percentDisc=p_totalInvDisc/p_totalInvAmt*100
        percentSpDisc=p_totalInvSp/p_totalInvAmt*100
    except:
        percentTp=0
        percentVat=0
        percentDisc=0
        percentSpDisc=0
    #======================
    
    myString='6.6 Outstanding List: Territory Wise\n'
    myString+='Inv Date From:,'+str(startDt)+'\n'
    myString+='To/ as of Date:'+','+str(endDt)+'\n'
    myString+='Inv Term:,'+str(invoice_term)+'\n'
    myString+='Branch ID:,'+str(depot_id)+'\n'
    myString+='Branch Name'+','+str(depot_name)+'\n'
    myString+='Store ID:,'+str(store_id)+'\n'
    myString+='Store Name'+','+str(store_name)+'\n'
    myString+='DP ID:,'+str(out_st_delivery_man_id)+'\n'
    myString+='DP Name'+','+str(out_st_delivery_man_name)+'\n'
    myString+='Territory ID:,'+str(out_st_territory_id)+'\n'
    myString+='Territory Name'+','+str(out_st_territory_name)+'\n'
    myString+='MSO ID:,'+str(out_st_mso_id)+'\n'
    myString+='MSO Name'+','+str(out_st_mso_name)+'\n'
    myString+='Customer ID:,'+str(customerId)+'\n'
    myString+='Customer Name'+','+str(customerName)+'\n'
    
    myString+='Credit Type:,'+str(credit_type)+'\n'    
    if catName=='':
        catName='ALL'
    if subCatName=='':
        subCatName='ALL'        
    myString+='Customer Category'+','+str(catName)+'\n'
    myString+='Customer Sub-Category'+','+str(subCatName)+'\n'
    
    myString+=str(session.level1Name)+','+str(out_st_level1_id)+'\n'
    myString+=str(session.level2Name)+','+str(out_st_level2_id)+'\n'
    
    totalInvTP=0
    totalInvVat=0
    totalInvDisc=0
    totalInvAmt=0
    totalInvSp=0
    totalOutsTP=0
    totalOutsVat=0
    totalOutsDisc=0
    totalOutST=0
    totalOutSp=0
    
    sl=0
    myString+='SL,Tr. Code,Customer Count,Market Count,Inv Count,Last Inv,LastDate,Invoice-TP,Invoice-Vat,Invoice-Disc,Invoice-SP,Invoice-Net,Adjusted,Outstanding-TP,Outstanding-Vat,Outstanding-Disc,Outstanding-SP,Outstanding-Net,Aging,Oustanding%'+'\n'
    for i in range(len(recordList)):
                
        recData=recordList[i]
        
        #----------
        invTp=recData['actTpAmt']-(recData['retTpAmt']+recData['retSpDiscAmt'])
        invVat=recData['vatTotalAmt']-recData['retVatAmt']
        invDiscount=recData['discAmt']-recData['retDiscAmt']
        invSpDisc=recData['spDiscAmt']-recData['retSpDiscAmt']
        invNetAmt=invTp+invVat-(invDiscount+invSpDisc)
        
        outstanding=round(invNetAmt-recData['collAmt'],2)
        if outstanding==0:
            continue
        
        sl+=1
        
        try:
#             outTp=(invTp*outstanding)/invNetAmt
#             outVat=(invVat*outstanding)/invNetAmt
#             outDisc=(invDiscount*outstanding)/invNetAmt
#             outSp=(invSpDisc*outstanding)/invNetAmt
            outTp=outstanding*(percentTp/100)
            outVat=outstanding*(percentVat/100)
            outDisc=outstanding*(percentDisc/100)
            outSp=outstanding*(percentSpDisc/100)
        except:
            outTp=0
            outVat=0
            outDisc=0
            outSp=0
            
        #-------
                
        #if outstanding < 0:
            #continue
        
        lastInv=str(session.prefix_invoice)+'INV-'+str(recData['maxSl'])                                              
        lastDate=recData['maxInvDate'].strftime('%d-%b-%y')
        
        adjust_amount=recData['adjustAmt']
        
        totalInvTP+=invTp
        totalInvVat+=invVat
        totalInvDisc+=invDiscount
        totalInvSp+=invSpDisc
        totalInvAmt+=invNetAmt
        
        #totalOutsTP+=outTp
        #totalOutsVat+=outVat
        #totalOutsDisc+=outDisc
        #totalOutSp+=outSp
        totalOutST+=outstanding
                
        invoice_date=datetime.datetime.strptime(str(recData['maxInvDate']),'%Y-%m-%d')
        
        agingDay=(currentDate-invoice_date).days
        
        outstandingPercent=0
        if invNetAmt!=0:
            outstandingPercent=round((outstanding/invNetAmt*100),2)
        
        #------------------------        
        myString+=str(sl)+','+str(recData['area_id'])+','+str(recData['cusCount'])+','+str(recData['marCount'])+','+str(recData['invCount'])+','+str(lastInv)+','+str(lastDate)+','+str(invTp)+','+\
        str(invVat)+','+str(invDiscount)+','+str(invSpDisc)+','+str(invNetAmt)+','+str(adjust_amount)+','+str(outTp)+','+str(outVat)+','+str(outDisc)+','+str(outSp)+','+str(outstanding)+','+\
        str(agingDay)+','+str(outstandingPercent)+'\n'
    
    
    myString+='\n\nSummary,,,,,,,,,,,,,,,,,,,,\n'
    
    myString+='Invoice TP,'+str(round(totalInvTP,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Invoice VAT,'+str(round(totalInvVat,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Invoice Discount,'+str(round(totalInvDisc,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Invoice SP.Disc,'+str(round(totalInvSp,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Invoice Net,'+str(round(totalInvAmt,2))+',,,,,,,,,,,,,,,,,,,\n\n'
    
    
    try:
        totalOutsTP=(totalInvTP*totalOutST)/totalInvAmt
        totalOutsVat=(totalInvVat*totalOutST)/totalInvAmt
        totalOutsDisc=(totalInvDisc*totalOutST)/totalInvAmt
        totalOutSp=(totalInvSp*totalOutST)/totalInvAmt
    except:
        totalOutsTP=0
        totalOutsVat=0
        totalOutsDisc=0
        totalOutSp=0
    
    myString+='Outstanding TP,'+str(round(totalOutsTP,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Outstanding VAT,'+str(round(totalOutsVat,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Outstanding Discount,'+str(round(totalOutsDisc,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Outstanding SP.Disc,'+str(round(totalOutSp,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Outstanding Net,'+str(round(totalOutST,2))+',,,,,,,,,,,,,,,,,,,\n'
    
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_TerritoryWiseOutstanding.csv'   
    return str(myString)
    
def outStDeliveryPersonWiseDetails():
    c_id=session.cid
    
    response.title='6.5 Outstanding Delivery Person Wise Details'
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    depot_id=str(request.vars.depotID).strip()
    store_id=str(request.vars.storeID).strip()
    
    out_st_delivery_man_id=str(request.vars.deliveryManID).strip()
    out_st_territory_id=str(request.vars.territoryID).strip()
    out_st_mso_id=str(request.vars.msoID).strip()
    invoice_term=str(request.vars.invoice_term).strip()
    customerId=str(request.vars.customerId).strip()
    
    credit_type=str(request.vars.credit_type).strip()
    customer_cat=str(request.vars.customer_cat).strip() 
    customer_sub_cat=str(request.vars.customer_sub_cat).strip()    
    
    out_st_level1_id=str(request.vars.out_st_level1_id).strip()  
    out_st_level2_id=str(request.vars.out_st_level2_id).strip()  
    
    catName=''
    custCatRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_CATEGORY')&(db.sm_category_type.cat_type_id==customer_cat)).select(db.sm_category_type.cat_type_name, limitby=(0,1))
    if custCatRows:
        catName=custCatRows[0].cat_type_name        
    subCatName=''
    custSubCatRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_SUB_CATEGORY')&(db.sm_category_type.cat_type_id==customer_sub_cat)).select(db.sm_category_type.cat_type_name, limitby=(0,1))
    if custSubCatRows:
        subCatName=custSubCatRows[0].cat_type_name
    
    depot_name=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depot_name=depotRow[0].name
    
    store_name=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        store_name=storeRow[0].store_name
        
    out_st_delivery_man_name=''
    dpRow=db((db.sm_delivery_man.cid==c_id)&(db.sm_delivery_man.depot_id==depot_id)&(db.sm_delivery_man.d_man_id==out_st_delivery_man_id)).select(db.sm_delivery_man.name,limitby=(0,1))
    if dpRow:
        out_st_delivery_man_name=dpRow[0].name
        
    out_st_territory_name=''
    levelRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==out_st_territory_id)).select(db.sm_level.level_name,limitby=(0,1))
    if levelRow:
        out_st_territory_name=levelRow[0].level_name
        
    out_st_mso_name=''
    repRow=db((db.sm_rep.cid==c_id)&(db.sm_rep.rep_id==out_st_mso_id)).select(db.sm_rep.name,limitby=(0,1))
    if repRow:
        out_st_mso_name=repRow[0].name
        
    customerName=''
    clientRow=db((db.sm_client.cid==c_id)&(db.sm_client.depot_id==depot_id)&(db.sm_client.client_id==customerId)).select(db.sm_client.name,limitby=(0,1))
    if clientRow:
        customerName=clientRow[0].name
        
    try:        
        startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d').strftime('%Y-%m-%d')   
    except:
        startDt=''                
    
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d').strftime('%Y-%m-%d')
    
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    
    qset=db()
    qset=qset(db.sm_invoice_head.cid==c_id)
    qset=qset(db.sm_invoice_head.depot_id==depot_id)
    qset=qset(db.sm_invoice_head.store_id==store_id)
    
    if startDt!='' and endDt!='':        
        qset=qset((db.sm_invoice_head.invoice_date>=startDt)&(db.sm_invoice_head.invoice_date<=endDt))
    else:
        qset=qset(db.sm_invoice_head.invoice_date<=endDt)
        
    qset=qset(db.sm_invoice_head.status=='Invoiced')
    qset=qset(db.sm_invoice_head.total_amount-(db.sm_invoice_head.return_tp+db.sm_invoice_head.return_vat-db.sm_invoice_head.return_discount)-db.sm_invoice_head.collection_amount!=0)
    
    if out_st_delivery_man_id!='':
        qset=qset(db.sm_invoice_head.d_man_id==out_st_delivery_man_id)
    if out_st_territory_id!='':
        qset=qset(db.sm_invoice_head.area_id==out_st_territory_id)
    if out_st_mso_id!='':
        qset=qset(db.sm_invoice_head.rep_id==out_st_mso_id)
    if invoice_term!='':
        qset=qset(db.sm_invoice_head.payment_mode==invoice_term)
    if customerId!='':
        qset=qset(db.sm_invoice_head.client_id==customerId)
        
    if credit_type!='':
        qset=qset(db.sm_invoice_head.credit_note==credit_type)
    if customer_cat!='':
        qset=qset(db.sm_invoice_head.cl_category_id==customer_cat)
    if customer_sub_cat!='':
        qset=qset(db.sm_invoice_head.cl_sub_category_id==customer_sub_cat)
      
    if out_st_level1_id!='':
        qset=qset(db.sm_invoice_head.level1_id==out_st_level1_id)
    if out_st_level2_id!='':
        qset=qset(db.sm_invoice_head.level2_id==out_st_level2_id)
        
    records=qset.select(db.sm_invoice_head.d_man_id,db.sm_invoice_head.d_man_name,db.sm_invoice_head.sl,db.sm_invoice_head.shipment_no,db.sm_invoice_head.invoice_date,db.sm_invoice_head.client_id,db.sm_invoice_head.client_name,db.sm_invoice_head.market_name,db.sm_invoice_head.adjust_amount,db.sm_invoice_head.payment_mode,db.sm_invoice_head.area_id,db.sm_invoice_head.actual_total_tp,db.sm_invoice_head.total_amount,db.sm_invoice_head.vat_total_amount,db.sm_invoice_head.discount,db.sm_invoice_head.sp_discount,db.sm_invoice_head.return_tp,db.sm_invoice_head.return_vat,db.sm_invoice_head.return_discount,db.sm_invoice_head.return_sp_discount,db.sm_invoice_head.collection_amount,orderby=db.sm_invoice_head.d_man_name|db.sm_invoice_head.client_name)
    
    #====================
    p_totalInvTP=0
    p_totalInvVat=0
    p_totalInvDisc=0
    p_totalInvSp=0
    p_totalInvAmt=0
    percentTp=0
    percentVat=0
    percentDisc=0
    percentSpDisc=0
    
    for record in records:        
        p_invTp=record.actual_total_tp-(record.return_tp+record.return_sp_discount)
        p_invVat=record.vat_total_amount-record.return_vat
        p_invDiscount=record.discount-record.return_discount
        p_invSpDisc=record.sp_discount-record.return_sp_discount
        p_invNetAmt=p_invTp+p_invVat-(p_invDiscount+p_invSpDisc)
        
        p_outstanding=round(p_invNetAmt-record.collection_amount,2)
        if p_outstanding==0:
            continue
            
        p_totalInvTP+=p_invTp
        p_totalInvVat+=p_invVat
        p_totalInvDisc+=p_invDiscount
        p_totalInvSp+=p_invSpDisc
        p_totalInvAmt+=p_invNetAmt
        
    try:
        percentTp=p_totalInvTP/p_totalInvAmt*100
        percentVat=p_totalInvVat/p_totalInvAmt*100
        percentDisc=p_totalInvDisc/p_totalInvAmt*100
        percentSpDisc=p_totalInvSp/p_totalInvAmt*100
    except:
        percentTp=0
        percentVat=0
        percentDisc=0
        percentSpDisc=0
    #======================
    
    return dict(percentTp=percentTp,percentVat=percentVat,percentDisc=percentDisc,percentSpDisc=percentSpDisc,records=records,fromDate=fromDate,toDate=toDate,depotID=depot_id,depotName=depot_name,storeID=store_id,storeName=store_name,deliveryManID=out_st_delivery_man_id,deliveryManName=out_st_delivery_man_name,territoryID=out_st_territory_id,territoryName=out_st_territory_name,msoID=out_st_mso_id,msoName=out_st_mso_name,invoice_term=invoice_term,customerId=customerId,customerName=customerName,credit_type=credit_type,customer_cat=customer_cat,customer_sub_cat=customer_sub_cat,catName=catName,subCatName=subCatName,out_st_level1_id=out_st_level1_id,out_st_level2_id=out_st_level2_id,page=page,items_per_page=items_per_page)    


def outStDeliveryPersonWiseDetails_download():
    c_id=session.cid
    
    currentDate=datetime.datetime.strptime(str(current_date),'%Y-%m-%d')
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    depot_id=str(request.vars.depotID).strip()
    store_id=str(request.vars.storeID).strip()
    
    out_st_delivery_man_id=str(request.vars.deliveryManID).strip()
    out_st_territory_id=str(request.vars.territoryID).strip()
    out_st_mso_id=str(request.vars.msoID).strip()
    invoice_term=str(request.vars.invoice_term).strip()
    customerId=str(request.vars.customerId).strip()
    
    credit_type=str(request.vars.credit_type).strip()
    customer_cat=str(request.vars.customer_cat).strip() 
    customer_sub_cat=str(request.vars.customer_sub_cat).strip()    
    
    out_st_level1_id=str(request.vars.out_st_level1_id).strip()  
    out_st_level2_id=str(request.vars.out_st_level2_id).strip()  
    
    catName=''
    custCatRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_CATEGORY')&(db.sm_category_type.cat_type_id==customer_cat)).select(db.sm_category_type.cat_type_name, limitby=(0,1))
    if custCatRows:
        catName=custCatRows[0].cat_type_name        
    subCatName=''
    custSubCatRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_SUB_CATEGORY')&(db.sm_category_type.cat_type_id==customer_sub_cat)).select(db.sm_category_type.cat_type_name, limitby=(0,1))
    if custSubCatRows:
        subCatName=custSubCatRows[0].cat_type_name
    
    depot_name=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depot_name=depotRow[0].name
    
    store_name=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        store_name=storeRow[0].store_name
        
    out_st_delivery_man_name=''
    dpRow=db((db.sm_delivery_man.cid==c_id)&(db.sm_delivery_man.depot_id==depot_id)&(db.sm_delivery_man.d_man_id==out_st_delivery_man_id)).select(db.sm_delivery_man.name,limitby=(0,1))
    if dpRow:
        out_st_delivery_man_name=dpRow[0].name
        
    out_st_territory_name=''
    levelRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==out_st_territory_id)).select(db.sm_level.level_name,limitby=(0,1))
    if levelRow:
        out_st_territory_name=levelRow[0].level_name
        
    out_st_mso_name=''
    repRow=db((db.sm_rep.cid==c_id)&(db.sm_rep.rep_id==out_st_mso_id)).select(db.sm_rep.name,limitby=(0,1))
    if repRow:
        out_st_mso_name=repRow[0].name
        
    customerName=''
    clientRow=db((db.sm_client.cid==c_id)&(db.sm_client.depot_id==depot_id)&(db.sm_client.client_id==customerId)).select(db.sm_client.name,limitby=(0,1))
    if clientRow:
        customerName=clientRow[0].name
        
    try:        
        startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d').strftime('%Y-%m-%d')   
    except:
        startDt=''                
    
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d').strftime('%Y-%m-%d')
    
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    
    qset=db()
    qset=qset(db.sm_invoice_head.cid==c_id)
    qset=qset(db.sm_invoice_head.depot_id==depot_id)
    qset=qset(db.sm_invoice_head.store_id==store_id)
    
    if startDt!='' and endDt!='':        
        qset=qset((db.sm_invoice_head.invoice_date>=startDt)&(db.sm_invoice_head.invoice_date<=endDt))
    else:
        qset=qset(db.sm_invoice_head.invoice_date<=endDt)
        
    qset=qset(db.sm_invoice_head.status=='Invoiced')
    qset=qset(db.sm_invoice_head.total_amount-(db.sm_invoice_head.return_tp+db.sm_invoice_head.return_vat-db.sm_invoice_head.return_discount)-db.sm_invoice_head.collection_amount!=0)
    
    if out_st_delivery_man_id!='':
        qset=qset(db.sm_invoice_head.d_man_id==out_st_delivery_man_id)
    if out_st_territory_id!='':
        qset=qset(db.sm_invoice_head.area_id==out_st_territory_id)
    if out_st_mso_id!='':
        qset=qset(db.sm_invoice_head.rep_id==out_st_mso_id)
    if invoice_term!='':
        qset=qset(db.sm_invoice_head.payment_mode==invoice_term)
    if customerId!='':
        qset=qset(db.sm_invoice_head.client_id==customerId)
        
    if credit_type!='':
        qset=qset(db.sm_invoice_head.credit_note==credit_type)
    if customer_cat!='':
        qset=qset(db.sm_invoice_head.cl_category_id==customer_cat)
    if customer_sub_cat!='':
        qset=qset(db.sm_invoice_head.cl_sub_category_id==customer_sub_cat)
      
    if out_st_level1_id!='':
        qset=qset(db.sm_invoice_head.level1_id==out_st_level1_id)
    if out_st_level2_id!='':
        qset=qset(db.sm_invoice_head.level2_id==out_st_level2_id)
        
    records=qset.select(db.sm_invoice_head.d_man_id,db.sm_invoice_head.d_man_name,db.sm_invoice_head.sl,db.sm_invoice_head.shipment_no,db.sm_invoice_head.invoice_date,db.sm_invoice_head.client_id,db.sm_invoice_head.client_name,db.sm_invoice_head.market_name,db.sm_invoice_head.adjust_amount,db.sm_invoice_head.payment_mode,db.sm_invoice_head.area_id,db.sm_invoice_head.actual_total_tp,db.sm_invoice_head.total_amount,db.sm_invoice_head.vat_total_amount,db.sm_invoice_head.discount,db.sm_invoice_head.sp_discount,db.sm_invoice_head.return_tp,db.sm_invoice_head.return_vat,db.sm_invoice_head.return_discount,db.sm_invoice_head.return_sp_discount,db.sm_invoice_head.collection_amount,orderby=db.sm_invoice_head.d_man_name|db.sm_invoice_head.client_name)
    
    #====================
    p_totalInvTP=0
    p_totalInvVat=0
    p_totalInvDisc=0
    p_totalInvSp=0
    p_totalInvAmt=0
    percentTp=0
    percentVat=0
    percentDisc=0
    percentSpDisc=0
    
    for record in records:        
        p_invTp=record.actual_total_tp-(record.return_tp+record.return_sp_discount)
        p_invVat=record.vat_total_amount-record.return_vat
        p_invDiscount=record.discount-record.return_discount
        p_invSpDisc=record.sp_discount-record.return_sp_discount
        p_invNetAmt=p_invTp+p_invVat-(p_invDiscount+p_invSpDisc)
        
        p_outstanding=round(p_invNetAmt-record.collection_amount,2)
        if p_outstanding==0:
            continue
            
        p_totalInvTP+=p_invTp
        p_totalInvVat+=p_invVat
        p_totalInvDisc+=p_invDiscount
        p_totalInvSp+=p_invSpDisc
        p_totalInvAmt+=p_invNetAmt
        
    try:
        percentTp=p_totalInvTP/p_totalInvAmt*100
        percentVat=p_totalInvVat/p_totalInvAmt*100
        percentDisc=p_totalInvDisc/p_totalInvAmt*100
        percentSpDisc=p_totalInvSp/p_totalInvAmt*100
    except:
        percentTp=0
        percentVat=0
        percentDisc=0
        percentSpDisc=0
    #======================
    
    myString='6.5 Delivery Person Wise Details Outstanding\n'
    myString+='Inv Date From:,'+str(startDt)+'\n'
    myString+='To/ as of Date:'+','+str(endDt)+'\n'
    myString+='Inv Term:,'+str(invoice_term)+'\n'
    myString+='Branch ID:,'+str(depot_id)+'\n'
    myString+='Branch Name'+','+str(depot_name)+'\n'
    myString+='Store ID:,'+str(store_id)+'\n'
    myString+='Store Name'+','+str(store_name)+'\n'
    myString+='DP ID:,'+str(out_st_delivery_man_id)+'\n'
    myString+='DP Name'+','+str(out_st_delivery_man_name)+'\n'
    myString+='Territory ID:,'+str(out_st_territory_id)+'\n'
    myString+='Territory Name'+','+str(out_st_territory_name)+'\n'
    myString+='MSO ID:,'+str(out_st_mso_id)+'\n'
    myString+='MSO Name'+','+str(out_st_mso_name)+'\n'
    myString+='Customer ID:,'+str(customerId)+'\n'
    myString+='Customer Name'+','+str(customerName)+'\n'
    
    myString+='Credit Type:,'+str(credit_type)+'\n'    
    if catName=='':
        catName='ALL'
    if subCatName=='':
        subCatName='ALL'        
    myString+='Customer Category'+','+str(catName)+'\n'
    myString+='Customer Sub-Category'+','+str(subCatName)+'\n'
    
    myString+=str(session.level1Name)+','+str(out_st_level1_id)+'\n'
    myString+=str(session.level2Name)+','+str(out_st_level2_id)+'\n'
    
    totalInvTP=0
    totalInvVat=0
    totalInvDisc=0
    totalInvAmt=0
    totalInvSp=0
    totalOutsTP=0
    totalOutsVat=0
    totalOutsDisc=0
    totalOutST=0
    totalOutSp=0
    
    sl=0
    myString+='SL,DP ID,DP Name,Date,Ship.No,Inv.No,Cust.ID,Cust.Name,Terms,Tr.Code,Market,Invoice-TP,Invoice-Vat,Invoice-Disc,Invoice-SP,Invoice-Net,Adjusted,Outstanding-TP,Outstanding-Vat,Outstanding-Disc,Outstanding-SP,Outstanding-Net,Aging,Oustanding%'+'\n'
    for row in records:
        d_man_id=row.d_man_id
        d_man_name=row.d_man_name
        invoice_date=row.invoice_date
        shipment_no=row.shipment_no
        invNo=str(session.prefix_invoice)+'INV-'+str(row.sl)
        client_id=row.client_id
        client_name=str(row.client_name).replace(',', ' ')
        payment_mode=row.payment_mode
        area_id=row.area_id
        market_name=str(row.market_name).replace(',', ' ')
        
        #-------------
        invTp=row.actual_total_tp-(row.return_tp+row.return_sp_discount)
        invVat=row.vat_total_amount-row.return_vat
        invDiscount=row.discount-row.return_discount
        invSpDisc=row.sp_discount-row.return_sp_discount
        invNetAmt=invTp+invVat-(invDiscount+invSpDisc)
        
        adjust_amount=row.adjust_amount
        
        outstanding=round(invNetAmt-row.collection_amount,2)
        if outstanding==0:
            continue
        sl+=1
        
        try:
#             outTp=(invTp*outstanding)/invNetAmt
#             outVat=(invVat*outstanding)/invNetAmt
#             outDisc=(invDiscount*outstanding)/invNetAmt
#             outSp=(invSpDisc*outstanding)/invNetAmt
            outTp=outstanding*(percentTp/100)
            outVat=outstanding*(percentVat/100)
            outDisc=outstanding*(percentDisc/100)
            outSp=outstanding*(percentSpDisc/100)
        except:
            outTp=0
            outVat=0
            outDisc=0
            outSp=0
        
        totalInvTP+=invTp
        totalInvVat+=invVat
        totalInvDisc+=invDiscount
        totalInvSp+=invSpDisc
        totalInvAmt+=invNetAmt
        
        #totalOutsTP+=outTp
        #totalOutsVat+=outVat
        #totalOutsDisc+=outDisc
        #totalOutSp+=outSp
        
        totalOutST+=outstanding
        
        invoice_date=datetime.datetime.strptime(str(row.invoice_date),'%Y-%m-%d')
        agingDay=(currentDate-invoice_date).days
        
        if invNetAmt!=0:
            outstandingPercent=round((outstanding/invNetAmt*100),2)
        else:
            outstandingPercent=0
        
        #------------------------        
        myString+=str(sl)+','+str(d_man_id)+','+str(d_man_name)+','+str(invoice_date)+','+str(shipment_no)+','+str(invNo)+','+str(client_id)+','+str(client_name)+','+str(payment_mode)+','+str(area_id)+','+str(market_name)+','+str(invTp)+','+\
        str(invVat)+','+str(invDiscount)+','+str(invSpDisc)+','+str(invNetAmt)+','+str(adjust_amount)+','+str(outTp)+','+str(outVat)+','+str(outDisc)+','+str(outSp)+','+str(outstanding)+','+\
        str(agingDay)+','+str(outstandingPercent)+'\n'
    
    myString+='\n\nSummary,,,,,,,,,,,,,,,,,,,,\n'
    
    myString+='Invoice TP,'+str(round(totalInvTP,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Invoice VAT,'+str(round(totalInvVat,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Invoice Discount,'+str(round(totalInvDisc,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Invoice SP.Disc,'+str(round(totalInvSp,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Invoice Net,'+str(round(totalInvAmt,2))+',,,,,,,,,,,,,,,,,,,\n\n'
    
    try:
        totalOutsTP=(totalInvTP*totalOutST)/totalInvAmt
        totalOutsVat=(totalInvVat*totalOutST)/totalInvAmt
        totalOutsDisc=(totalInvDisc*totalOutST)/totalInvAmt
        totalOutSp=(totalInvSp*totalOutST)/totalInvAmt
    except:
        totalOutsTP=0
        totalOutsVat=0
        totalOutsDisc=0
        totalOutSp=0
        
    myString+='Outstanding TP,'+str(round(totalOutsTP,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Outstanding VAT,'+str(round(totalOutsVat,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Outstanding Discount,'+str(round(totalOutsDisc,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Outstanding SP.Disc,'+str(round(totalOutSp,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Outstanding Net,'+str(round(totalOutST,2))+',,,,,,,,,,,,,,,,,,,\n'
    
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_DpWiseDetailsOutstanding.csv'   
    return str(myString)


def outStDeliveryPersonWiseDetails_print():
    c_id=session.cid
    
    response.title='6.5A Outstanding Delivery Person Wise Details (Print)'
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    depot_id=str(request.vars.depotID).strip()
    store_id=str(request.vars.storeID).strip()
    
    out_st_delivery_man_id=str(request.vars.deliveryManID).strip()
    out_st_territory_id=str(request.vars.territoryID).strip()
    out_st_mso_id=str(request.vars.msoID).strip()
    invoice_term=str(request.vars.invoice_term).strip()
    customerId=str(request.vars.customerId).strip()
    
    credit_type=str(request.vars.credit_type).strip()
    customer_cat=str(request.vars.customer_cat).strip() 
    customer_sub_cat=str(request.vars.customer_sub_cat).strip()    
    
    out_st_level1_id=str(request.vars.out_st_level1_id).strip()  
    out_st_level2_id=str(request.vars.out_st_level2_id).strip()  
    
    catName=''
    custCatRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_CATEGORY')&(db.sm_category_type.cat_type_id==customer_cat)).select(db.sm_category_type.cat_type_name, limitby=(0,1))
    if custCatRows:
        catName=custCatRows[0].cat_type_name        
    subCatName=''
    custSubCatRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_SUB_CATEGORY')&(db.sm_category_type.cat_type_id==customer_sub_cat)).select(db.sm_category_type.cat_type_name, limitby=(0,1))
    if custSubCatRows:
        subCatName=custSubCatRows[0].cat_type_name
    
    depot_name=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depot_name=depotRow[0].name
    
    store_name=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        store_name=storeRow[0].store_name
        
    out_st_delivery_man_name=''
    dpRow=db((db.sm_delivery_man.cid==c_id)&(db.sm_delivery_man.depot_id==depot_id)&(db.sm_delivery_man.d_man_id==out_st_delivery_man_id)).select(db.sm_delivery_man.name,limitby=(0,1))
    if dpRow:
        out_st_delivery_man_name=dpRow[0].name
        
    out_st_territory_name=''
    levelRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==out_st_territory_id)).select(db.sm_level.level_name,limitby=(0,1))
    if levelRow:
        out_st_territory_name=levelRow[0].level_name
        
    out_st_mso_name=''
    repRow=db((db.sm_rep.cid==c_id)&(db.sm_rep.rep_id==out_st_mso_id)).select(db.sm_rep.name,limitby=(0,1))
    if repRow:
        out_st_mso_name=repRow[0].name
        
    customerName=''
    clientRow=db((db.sm_client.cid==c_id)&(db.sm_client.depot_id==depot_id)&(db.sm_client.client_id==customerId)).select(db.sm_client.name,limitby=(0,1))
    if clientRow:
        customerName=clientRow[0].name
        
    try:        
        startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d').strftime('%Y-%m-%d')   
    except:
        startDt=''                
    
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d').strftime('%Y-%m-%d')
    
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    
    qset=db()
    qset=qset(db.sm_invoice_head.cid==c_id)
    qset=qset(db.sm_invoice_head.depot_id==depot_id)
    qset=qset(db.sm_invoice_head.store_id==store_id)
    
    if startDt!='' and endDt!='':        
        qset=qset((db.sm_invoice_head.invoice_date>=startDt)&(db.sm_invoice_head.invoice_date<=endDt))
    else:
        qset=qset(db.sm_invoice_head.invoice_date<=endDt)
        
    qset=qset(db.sm_invoice_head.status=='Invoiced')
    qset=qset(db.sm_invoice_head.total_amount-(db.sm_invoice_head.return_tp+db.sm_invoice_head.return_vat-db.sm_invoice_head.return_discount)-db.sm_invoice_head.collection_amount!=0)
    
    if out_st_delivery_man_id!='':
        qset=qset(db.sm_invoice_head.d_man_id==out_st_delivery_man_id)
    if out_st_territory_id!='':
        qset=qset(db.sm_invoice_head.area_id==out_st_territory_id)
    if out_st_mso_id!='':
        qset=qset(db.sm_invoice_head.rep_id==out_st_mso_id)
    if invoice_term!='':
        qset=qset(db.sm_invoice_head.payment_mode==invoice_term)
    if customerId!='':
        qset=qset(db.sm_invoice_head.client_id==customerId)
        
    if credit_type!='':
        qset=qset(db.sm_invoice_head.credit_note==credit_type)
    if customer_cat!='':
        qset=qset(db.sm_invoice_head.cl_category_id==customer_cat)
    if customer_sub_cat!='':
        qset=qset(db.sm_invoice_head.cl_sub_category_id==customer_sub_cat)
      
    if out_st_level1_id!='':
        qset=qset(db.sm_invoice_head.level1_id==out_st_level1_id)
    if out_st_level2_id!='':
        qset=qset(db.sm_invoice_head.level2_id==out_st_level2_id)
        
    records=qset.select(db.sm_invoice_head.d_man_id,db.sm_invoice_head.d_man_name,db.sm_invoice_head.sl,db.sm_invoice_head.shipment_no,db.sm_invoice_head.invoice_date,db.sm_invoice_head.client_id,db.sm_invoice_head.client_name,db.sm_invoice_head.market_name,db.sm_invoice_head.adjust_amount,db.sm_invoice_head.payment_mode,db.sm_invoice_head.area_id,db.sm_invoice_head.actual_total_tp,db.sm_invoice_head.total_amount,db.sm_invoice_head.vat_total_amount,db.sm_invoice_head.discount,db.sm_invoice_head.sp_discount,db.sm_invoice_head.return_tp,db.sm_invoice_head.return_vat,db.sm_invoice_head.return_discount,db.sm_invoice_head.return_sp_discount,db.sm_invoice_head.collection_amount,orderby=db.sm_invoice_head.d_man_name|db.sm_invoice_head.client_name)
    
    #====================
    p_totalInvTP=0
    p_totalInvVat=0
    p_totalInvDisc=0
    p_totalInvSp=0
    p_totalInvAmt=0
    percentTp=0
    percentVat=0
    percentDisc=0
    percentSpDisc=0
    
    for record in records:        
        p_invTp=record.actual_total_tp-(record.return_tp+record.return_sp_discount)
        p_invVat=record.vat_total_amount-record.return_vat
        p_invDiscount=record.discount-record.return_discount
        p_invSpDisc=record.sp_discount-record.return_sp_discount
        p_invNetAmt=p_invTp+p_invVat-(p_invDiscount+p_invSpDisc)
        
        p_outstanding=round(p_invNetAmt-record.collection_amount,2)
        if p_outstanding==0:
            continue
            
        p_totalInvTP+=p_invTp
        p_totalInvVat+=p_invVat
        p_totalInvDisc+=p_invDiscount
        p_totalInvSp+=p_invSpDisc
        p_totalInvAmt+=p_invNetAmt
        
    try:
        percentTp=p_totalInvTP/p_totalInvAmt*100
        percentVat=p_totalInvVat/p_totalInvAmt*100
        percentDisc=p_totalInvDisc/p_totalInvAmt*100
        percentSpDisc=p_totalInvSp/p_totalInvAmt*100
    except:
        percentTp=0
        percentVat=0
        percentDisc=0
        percentSpDisc=0
    #======================
    
    return dict(percentTp=percentTp,percentVat=percentVat,percentDisc=percentDisc,percentSpDisc=percentSpDisc,records=records,fromDate=fromDate,toDate=toDate,depotID=depot_id,depotName=depot_name,storeID=store_id,storeName=store_name,deliveryManID=out_st_delivery_man_id,deliveryManName=out_st_delivery_man_name,territoryID=out_st_territory_id,territoryName=out_st_territory_name,msoID=out_st_mso_id,msoName=out_st_mso_name,invoice_term=invoice_term,customerId=customerId,customerName=customerName,credit_type=credit_type,customer_cat=customer_cat,customer_sub_cat=customer_sub_cat,catName=catName,subCatName=subCatName,out_st_level1_id=out_st_level1_id,out_st_level2_id=out_st_level2_id,page=page,items_per_page=items_per_page)    


def outStDeliveryPersonWiseDetails_print_download():
    c_id=session.cid
    
    currentDate=datetime.datetime.strptime(str(current_date),'%Y-%m-%d')
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    depot_id=str(request.vars.depotID).strip()
    store_id=str(request.vars.storeID).strip()
    
    out_st_delivery_man_id=str(request.vars.deliveryManID).strip()
    out_st_territory_id=str(request.vars.territoryID).strip()
    out_st_mso_id=str(request.vars.msoID).strip()
    invoice_term=str(request.vars.invoice_term).strip()
    customerId=str(request.vars.customerId).strip()
    
    credit_type=str(request.vars.credit_type).strip()
    customer_cat=str(request.vars.customer_cat).strip() 
    customer_sub_cat=str(request.vars.customer_sub_cat).strip()    
    
    out_st_level1_id=str(request.vars.out_st_level1_id).strip()  
    out_st_level2_id=str(request.vars.out_st_level2_id).strip()  
    
    catName=''
    custCatRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_CATEGORY')&(db.sm_category_type.cat_type_id==customer_cat)).select(db.sm_category_type.cat_type_name, limitby=(0,1))
    if custCatRows:
        catName=custCatRows[0].cat_type_name        
    subCatName=''
    custSubCatRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_SUB_CATEGORY')&(db.sm_category_type.cat_type_id==customer_sub_cat)).select(db.sm_category_type.cat_type_name, limitby=(0,1))
    if custSubCatRows:
        subCatName=custSubCatRows[0].cat_type_name
    
    depot_name=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depot_name=depotRow[0].name
    
    store_name=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        store_name=storeRow[0].store_name
        
    out_st_delivery_man_name=''
    dpRow=db((db.sm_delivery_man.cid==c_id)&(db.sm_delivery_man.depot_id==depot_id)&(db.sm_delivery_man.d_man_id==out_st_delivery_man_id)).select(db.sm_delivery_man.name,limitby=(0,1))
    if dpRow:
        out_st_delivery_man_name=dpRow[0].name
        
    out_st_territory_name=''
    levelRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==out_st_territory_id)).select(db.sm_level.level_name,limitby=(0,1))
    if levelRow:
        out_st_territory_name=levelRow[0].level_name
        
    out_st_mso_name=''
    repRow=db((db.sm_rep.cid==c_id)&(db.sm_rep.rep_id==out_st_mso_id)).select(db.sm_rep.name,limitby=(0,1))
    if repRow:
        out_st_mso_name=repRow[0].name
        
    customerName=''
    clientRow=db((db.sm_client.cid==c_id)&(db.sm_client.depot_id==depot_id)&(db.sm_client.client_id==customerId)).select(db.sm_client.name,limitby=(0,1))
    if clientRow:
        customerName=clientRow[0].name
        
    try:        
        startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d').strftime('%Y-%m-%d')   
    except:
        startDt=''                
    
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d').strftime('%Y-%m-%d')
    
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    
    qset=db()
    qset=qset(db.sm_invoice_head.cid==c_id)
    qset=qset(db.sm_invoice_head.depot_id==depot_id)
    qset=qset(db.sm_invoice_head.store_id==store_id)
    
    if startDt!='' and endDt!='':        
        qset=qset((db.sm_invoice_head.invoice_date>=startDt)&(db.sm_invoice_head.invoice_date<=endDt))
    else:
        qset=qset(db.sm_invoice_head.invoice_date<=endDt)
        
    qset=qset(db.sm_invoice_head.status=='Invoiced')
    qset=qset(db.sm_invoice_head.total_amount-(db.sm_invoice_head.return_tp+db.sm_invoice_head.return_vat-db.sm_invoice_head.return_discount)-db.sm_invoice_head.collection_amount!=0)
    
    if out_st_delivery_man_id!='':
        qset=qset(db.sm_invoice_head.d_man_id==out_st_delivery_man_id)
    if out_st_territory_id!='':
        qset=qset(db.sm_invoice_head.area_id==out_st_territory_id)
    if out_st_mso_id!='':
        qset=qset(db.sm_invoice_head.rep_id==out_st_mso_id)
    if invoice_term!='':
        qset=qset(db.sm_invoice_head.payment_mode==invoice_term)
    if customerId!='':
        qset=qset(db.sm_invoice_head.client_id==customerId)
        
    if credit_type!='':
        qset=qset(db.sm_invoice_head.credit_note==credit_type)
    if customer_cat!='':
        qset=qset(db.sm_invoice_head.cl_category_id==customer_cat)
    if customer_sub_cat!='':
        qset=qset(db.sm_invoice_head.cl_sub_category_id==customer_sub_cat)
      
    if out_st_level1_id!='':
        qset=qset(db.sm_invoice_head.level1_id==out_st_level1_id)
    if out_st_level2_id!='':
        qset=qset(db.sm_invoice_head.level2_id==out_st_level2_id)
        
    records=qset.select(db.sm_invoice_head.d_man_id,db.sm_invoice_head.d_man_name,db.sm_invoice_head.sl,db.sm_invoice_head.shipment_no,db.sm_invoice_head.invoice_date,db.sm_invoice_head.client_id,db.sm_invoice_head.client_name,db.sm_invoice_head.market_name,db.sm_invoice_head.adjust_amount,db.sm_invoice_head.payment_mode,db.sm_invoice_head.area_id,db.sm_invoice_head.actual_total_tp,db.sm_invoice_head.total_amount,db.sm_invoice_head.vat_total_amount,db.sm_invoice_head.discount,db.sm_invoice_head.sp_discount,db.sm_invoice_head.return_tp,db.sm_invoice_head.return_vat,db.sm_invoice_head.return_discount,db.sm_invoice_head.return_sp_discount,db.sm_invoice_head.collection_amount,orderby=db.sm_invoice_head.d_man_name|db.sm_invoice_head.client_name)
    
    #====================
    p_totalInvTP=0
    p_totalInvVat=0
    p_totalInvDisc=0
    p_totalInvSp=0
    p_totalInvAmt=0
    percentTp=0
    percentVat=0
    percentDisc=0
    percentSpDisc=0
    
    for record in records:        
        p_invTp=record.actual_total_tp-(record.return_tp+record.return_sp_discount)
        p_invVat=record.vat_total_amount-record.return_vat
        p_invDiscount=record.discount-record.return_discount
        p_invSpDisc=record.sp_discount-record.return_sp_discount
        p_invNetAmt=p_invTp+p_invVat-(p_invDiscount+p_invSpDisc)
        
        p_outstanding=round(p_invNetAmt-record.collection_amount,2)
        if p_outstanding==0:
            continue
            
        p_totalInvTP+=p_invTp
        p_totalInvVat+=p_invVat
        p_totalInvDisc+=p_invDiscount
        p_totalInvSp+=p_invSpDisc
        p_totalInvAmt+=p_invNetAmt
        
    try:
        percentTp=p_totalInvTP/p_totalInvAmt*100
        percentVat=p_totalInvVat/p_totalInvAmt*100
        percentDisc=p_totalInvDisc/p_totalInvAmt*100
        percentSpDisc=p_totalInvSp/p_totalInvAmt*100
    except:
        percentTp=0
        percentVat=0
        percentDisc=0
        percentSpDisc=0
    #======================
    
    myString='6.5A Delivery Person Wise Details Outstanding (Print)\n'
    myString+='Inv Date From:,'+str(startDt)+'\n'
    myString+='To/ as of Date:'+','+str(endDt)+'\n'
    myString+='Inv Term:,'+str(invoice_term)+'\n'
    myString+='Branch ID:,'+str(depot_id)+'\n'
    myString+='Branch Name'+','+str(depot_name)+'\n'
    myString+='Store ID:,'+str(store_id)+'\n'
    myString+='Store Name'+','+str(store_name)+'\n'
    myString+='DP ID:,'+str(out_st_delivery_man_id)+'\n'
    myString+='DP Name'+','+str(out_st_delivery_man_name)+'\n'
    myString+='Territory ID:,'+str(out_st_territory_id)+'\n'
    myString+='Territory Name'+','+str(out_st_territory_name)+'\n'
    myString+='MSO ID:,'+str(out_st_mso_id)+'\n'
    myString+='MSO Name'+','+str(out_st_mso_name)+'\n'
    myString+='Customer ID:,'+str(customerId)+'\n'
    myString+='Customer Name'+','+str(customerName)+'\n'
    
    myString+='Credit Type:,'+str(credit_type)+'\n'    
    if catName=='':
        catName='ALL'
    if subCatName=='':
        subCatName='ALL'        
    myString+='Customer Category'+','+str(catName)+'\n'
    myString+='Customer Sub-Category'+','+str(subCatName)+'\n'
    
    myString+=str(session.level1Name)+','+str(out_st_level1_id)+'\n'
    myString+=str(session.level2Name)+','+str(out_st_level2_id)+'\n'
    
    totalInvTP=0
    totalInvVat=0
    totalInvDisc=0
    totalInvAmt=0
    totalInvSp=0
    totalOutsTP=0
    totalOutsVat=0
    totalOutsDisc=0
    totalOutST=0
    totalOutSp=0
    
    sl=0
    myString+='SL,DP ID,DP Name,Date,Ship.No,Inv.No,Cust.ID,Cust.Name,Terms,Tr.Code,Market,Outstanding-TP,Outstanding-Vat,Outstanding-Disc,Outstanding-SP,Outstanding-Net,Aging,Oustanding%'+'\n'
    for row in records:
        d_man_id=row.d_man_id
        d_man_name=row.d_man_name
        invoice_date=row.invoice_date
        shipment_no=row.shipment_no
        invNo=str(session.prefix_invoice)+'INV-'+str(row.sl)
        client_id=row.client_id
        client_name=str(row.client_name).replace(',', ' ')
        payment_mode=row.payment_mode
        area_id=row.area_id
        market_name=str(row.market_name).replace(',', ' ')
        
        #-------------
        invTp=row.actual_total_tp-(row.return_tp+row.return_sp_discount)
        invVat=row.vat_total_amount-row.return_vat
        invDiscount=row.discount-row.return_discount
        invSpDisc=row.sp_discount-row.return_sp_discount
        invNetAmt=invTp+invVat-(invDiscount+invSpDisc)
        
        adjust_amount=row.adjust_amount
        
        outstanding=round(invNetAmt-row.collection_amount,2)
        if outstanding==0:
            continue
        sl+=1
        
        try:
#             outTp=(invTp*outstanding)/invNetAmt
#             outVat=(invVat*outstanding)/invNetAmt
#             outDisc=(invDiscount*outstanding)/invNetAmt
#             outSp=(invSpDisc*outstanding)/invNetAmt
            outTp=outstanding*(percentTp/100)
            outVat=outstanding*(percentVat/100)
            outDisc=outstanding*(percentDisc/100)
            outSp=outstanding*(percentSpDisc/100)
        except:
            outTp=0
            outVat=0
            outDisc=0
            outSp=0
        
        totalInvTP+=invTp
        totalInvVat+=invVat
        totalInvDisc+=invDiscount
        totalInvSp+=invSpDisc
        totalInvAmt+=invNetAmt
        
        #totalOutsTP+=outTp
        #totalOutsVat+=outVat
        #totalOutsDisc+=outDisc
        #totalOutSp+=outSp
        
        totalOutST+=outstanding
        
        invoice_date=datetime.datetime.strptime(str(row.invoice_date),'%Y-%m-%d')
        agingDay=(currentDate-invoice_date).days
        
        if invNetAmt!=0:
            outstandingPercent=round((outstanding/invNetAmt*100),2)
        else:
            outstandingPercent=0
        
        #------------------------        
        myString+=str(sl)+','+str(d_man_id)+','+str(d_man_name)+','+str(invoice_date)+','+str(shipment_no)+','+str(invNo)+','+str(client_id)+','+str(client_name)+','+str(payment_mode)+','+str(area_id)+','+str(market_name)+','+\
        str(outTp)+','+str(outVat)+','+str(outDisc)+','+str(outSp)+','+str(outstanding)+','+str(agingDay)+','+str(outstandingPercent)+'\n'
    
    myString+='\n\nSummary,,,,,,,,,,,,,,,,,,,,\n'
    
    myString+='Invoice TP,'+str(round(totalInvTP,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Invoice VAT,'+str(round(totalInvVat,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Invoice Discount,'+str(round(totalInvDisc,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Invoice SP.Disc,'+str(round(totalInvSp,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Invoice Net,'+str(round(totalInvAmt,2))+',,,,,,,,,,,,,,,,,,,\n\n'
    
    try:
        totalOutsTP=(totalInvTP*totalOutST)/totalInvAmt
        totalOutsVat=(totalInvVat*totalOutST)/totalInvAmt
        totalOutsDisc=(totalInvDisc*totalOutST)/totalInvAmt
        totalOutSp=(totalInvSp*totalOutST)/totalInvAmt
    except:
        totalOutsTP=0
        totalOutsVat=0
        totalOutsDisc=0
        totalOutSp=0
        
    myString+='Outstanding TP,'+str(round(totalOutsTP,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Outstanding VAT,'+str(round(totalOutsVat,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Outstanding Discount,'+str(round(totalOutsDisc,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Outstanding SP.Disc,'+str(round(totalOutSp,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Outstanding Net,'+str(round(totalOutST,2))+',,,,,,,,,,,,,,,,,,,\n'
    
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_DpWiseDetailsOutstanding_Print.csv'   
    return str(myString)




def outStDeliveryPersonWise():
    c_id=session.cid
    
    response.title='6.4 Outstanding Delivery Person Wise'
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    depot_id=str(request.vars.depotID).strip()
    store_id=str(request.vars.storeID).strip()
    out_st_delivery_man_id=str(request.vars.deliveryManID).strip()
    out_st_territory_id=str(request.vars.territoryID).strip()
    out_st_mso_id=str(request.vars.msoID).strip()
    invoice_term=str(request.vars.invoice_term).strip()
    customerId=str(request.vars.customerId).strip()
    
    credit_type=str(request.vars.credit_type).strip()
    customer_cat=str(request.vars.customer_cat).strip() 
    customer_sub_cat=str(request.vars.customer_sub_cat).strip()    
    
    out_st_level1_id=str(request.vars.out_st_level1_id).strip()  
    out_st_level2_id=str(request.vars.out_st_level2_id).strip()  
    
    catName=''
    custCatRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_CATEGORY')&(db.sm_category_type.cat_type_id==customer_cat)).select(db.sm_category_type.cat_type_name, limitby=(0,1))
    if custCatRows:
        catName=custCatRows[0].cat_type_name        
    subCatName=''
    custSubCatRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_SUB_CATEGORY')&(db.sm_category_type.cat_type_id==customer_sub_cat)).select(db.sm_category_type.cat_type_name, limitby=(0,1))
    if custSubCatRows:
        subCatName=custSubCatRows[0].cat_type_name
        
    depot_name=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depot_name=depotRow[0].name
        
    store_name=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        store_name=storeRow[0].store_name
        
    out_st_delivery_man_name=''
    dpRow=db((db.sm_delivery_man.cid==c_id)&(db.sm_delivery_man.depot_id==depot_id)&(db.sm_delivery_man.d_man_id==out_st_delivery_man_id)).select(db.sm_delivery_man.name,limitby=(0,1))
    if dpRow:
        out_st_delivery_man_name=dpRow[0].name
        
    out_st_territory_name=''
    levelRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==out_st_territory_id)).select(db.sm_level.level_name,limitby=(0,1))
    if levelRow:
        out_st_territory_name=levelRow[0].level_name
        
    out_st_mso_name=''
    repRow=db((db.sm_rep.cid==c_id)&(db.sm_rep.rep_id==out_st_mso_id)).select(db.sm_rep.name,limitby=(0,1))
    if repRow:
        out_st_mso_name=repRow[0].name
        
    customerName=''
    clientRow=db((db.sm_client.cid==c_id)&(db.sm_client.depot_id==depot_id)&(db.sm_client.client_id==customerId)).select(db.sm_client.name,limitby=(0,1))
    if clientRow:
        customerName=clientRow[0].name
        
    try:        
        startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d').strftime('%Y-%m-%d')
    except:
        startDt=''                
    
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d').strftime('%Y-%m-%d')
    
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    
    condStr=" AND (round(sm_invoice_head.total_amount-(sm_invoice_head.return_tp+sm_invoice_head.return_vat-sm_invoice_head.return_discount)-sm_invoice_head.collection_amount,2)!=0)"
    
    if out_st_delivery_man_id!='':
        condStr+=" AND (sm_invoice_head.d_man_id='"+out_st_delivery_man_id+"')"        
    if out_st_territory_id!='':
        condStr+=" AND (sm_invoice_head.area_id='"+out_st_territory_id+"')"        
    if out_st_mso_id!='':
        condStr+=" AND (sm_invoice_head.rep_id='"+out_st_mso_id+"')"        
    if invoice_term!='':
        condStr+=" AND (sm_invoice_head.payment_mode='"+invoice_term+"')"
    if customerId!='':
        condStr+=" AND (sm_invoice_head.client_id='"+customerId+"')"
        
    if credit_type!='':
        condStr+=" AND (sm_invoice_head.credit_note='"+credit_type+"')"
    if customer_cat!='':
        condStr+=" AND (sm_invoice_head.cl_category_id='"+customer_cat+"')"
    if customer_sub_cat!='':
        condStr+=" AND (sm_invoice_head.cl_sub_category_id='"+customer_sub_cat+"')"
    
    if out_st_level1_id!='':
        condStr+=" AND (sm_invoice_head.level1_id='"+out_st_level1_id+"')"        
    if out_st_level2_id!='':
        condStr+=" AND (sm_invoice_head.level2_id='"+out_st_level2_id+"')"
        
    if startDt!='' and endDt!='': 
        dateRecords="SELECT sm_invoice_head.d_man_id as d_man_id,MAX(sm_invoice_head.d_man_name) as d_man_name,COUNT(sm_invoice_head.id) as invCount,MAX(sm_invoice_head.sl) as maxSl,MAX(sm_invoice_head.invoice_date) as invoice_date,SUM(sm_invoice_head.actual_total_tp) as actTpAmt, SUM(sm_invoice_head.total_amount) as totalAmt,SUM(sm_invoice_head.vat_total_amount) as vatTotalAmt,SUM(sm_invoice_head.discount) as discAmt,SUM(sm_invoice_head.adjust_amount) as adjustAmt,SUM(sm_invoice_head.return_tp) as retTpAmt,SUM(sm_invoice_head.return_vat) as retVatAmt,SUM(sm_invoice_head.return_discount) as retDiscAmt,SUM(sm_invoice_head.return_sp_discount) as retSpDiscAmt,SUM(sm_invoice_head.collection_amount) as collAmt,SUM(sm_invoice_head.sp_discount) as spDiscAmt FROM sm_invoice_head WHERE ((sm_invoice_head.cid = '"+c_id+"') AND ((sm_invoice_head.invoice_date >= '"+str(startDt)+"') AND (sm_invoice_head.invoice_date <= '"+str(endDt)+"')) AND (sm_invoice_head.depot_id='"+depot_id+"') AND (sm_invoice_head.store_id='"+store_id+"') AND (sm_invoice_head.status='Invoiced') "+str(condStr)+") GROUP BY sm_invoice_head.d_man_id ORDER BY sm_invoice_head.d_man_name"
    else:
        dateRecords="SELECT sm_invoice_head.d_man_id as d_man_id,MAX(sm_invoice_head.d_man_name) as d_man_name,COUNT(sm_invoice_head.id) as invCount,MAX(sm_invoice_head.sl) as maxSl,MAX(sm_invoice_head.invoice_date) as invoice_date,SUM(sm_invoice_head.actual_total_tp) as actTpAmt, SUM(sm_invoice_head.total_amount) as totalAmt,SUM(sm_invoice_head.vat_total_amount) as vatTotalAmt,SUM(sm_invoice_head.discount) as discAmt,SUM(sm_invoice_head.adjust_amount) as adjustAmt,SUM(sm_invoice_head.return_tp) as retTpAmt,SUM(sm_invoice_head.return_vat) as retVatAmt,SUM(sm_invoice_head.return_discount) as retDiscAmt,SUM(sm_invoice_head.return_sp_discount) as retSpDiscAmt,SUM(sm_invoice_head.collection_amount) as collAmt,SUM(sm_invoice_head.sp_discount) as spDiscAmt FROM sm_invoice_head WHERE ((sm_invoice_head.cid = '"+c_id+"') AND (sm_invoice_head.invoice_date <= '"+str(endDt)+"') AND (sm_invoice_head.depot_id='"+depot_id+"') AND (sm_invoice_head.store_id='"+store_id+"') AND (sm_invoice_head.status='Invoiced') "+str(condStr)+") GROUP BY sm_invoice_head.d_man_id ORDER BY sm_invoice_head.d_man_name"
        
    recordList=db.executesql(dateRecords,as_dict = True)
    
    #====================
    p_totalInvTP=0
    p_totalInvVat=0
    p_totalInvDisc=0
    p_totalInvSp=0
    p_totalInvAmt=0
    percentTp=0
    percentVat=0
    percentDisc=0
    percentSpDisc=0
    
    for i in range(len(recordList)):                
        recData=recordList[i]
        
        p_invTp=recData['actTpAmt']-(recData['retTpAmt']+recData['retSpDiscAmt'])   
        p_invVat=recData['vatTotalAmt']-recData['retVatAmt']
        p_invDiscount=recData['discAmt']-recData['retDiscAmt']
        p_invSpDisc=recData['spDiscAmt']-recData['retSpDiscAmt']
        p_invNetAmt=p_invTp+p_invVat-(p_invDiscount+p_invSpDisc)
    
        p_outstanding=round(p_invNetAmt-recData['collAmt'],2)
        
        if p_outstanding==0:
            continue
            
        p_totalInvTP+=p_invTp
        p_totalInvVat+=p_invVat
        p_totalInvDisc+=p_invDiscount
        p_totalInvSp+=p_invSpDisc
        p_totalInvAmt+=p_invNetAmt
        
    try:
        percentTp=p_totalInvTP/p_totalInvAmt*100
        percentVat=p_totalInvVat/p_totalInvAmt*100
        percentDisc=p_totalInvDisc/p_totalInvAmt*100
        percentSpDisc=p_totalInvSp/p_totalInvAmt*100
    except:
        percentTp=0
        percentVat=0
        percentDisc=0
        percentSpDisc=0
    #======================
    return dict(percentTp=percentTp,percentVat=percentVat,percentDisc=percentDisc,percentSpDisc=percentSpDisc,recordList=recordList,fromDate=startDt,toDate=endDt,depotID=depot_id,depotName=depot_name,storeID=store_id,storeName=store_name,deliveryManID=out_st_delivery_man_id,deliveryManName=out_st_delivery_man_name,territoryID=out_st_territory_id,territoryName=out_st_territory_name,msoID=out_st_mso_id,msoName=out_st_mso_name,invoice_term=invoice_term,customerId=customerId,customerName=customerName,credit_type=credit_type,customer_cat=customer_cat,customer_sub_cat=customer_sub_cat,catName=catName,subCatName=subCatName,out_st_level1_id=out_st_level1_id,out_st_level2_id=out_st_level2_id,page=page,items_per_page=items_per_page)    


def outStDeliveryPersonWise_download():
    c_id=session.cid
    
    currentDate=datetime.datetime.strptime(str(current_date),'%Y-%m-%d')
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    depot_id=str(request.vars.depotID).strip()
    store_id=str(request.vars.storeID).strip()
    out_st_delivery_man_id=str(request.vars.deliveryManID).strip()
    out_st_territory_id=str(request.vars.territoryID).strip()
    out_st_mso_id=str(request.vars.msoID).strip()
    invoice_term=str(request.vars.invoice_term).strip()
    customerId=str(request.vars.customerId).strip()
    
    credit_type=str(request.vars.credit_type).strip()
    customer_cat=str(request.vars.customer_cat).strip() 
    customer_sub_cat=str(request.vars.customer_sub_cat).strip()    
    
    out_st_level1_id=str(request.vars.out_st_level1_id).strip()  
    out_st_level2_id=str(request.vars.out_st_level2_id).strip()  
    
    catName=''
    custCatRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_CATEGORY')&(db.sm_category_type.cat_type_id==customer_cat)).select(db.sm_category_type.cat_type_name, limitby=(0,1))
    if custCatRows:
        catName=custCatRows[0].cat_type_name        
    subCatName=''
    custSubCatRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_SUB_CATEGORY')&(db.sm_category_type.cat_type_id==customer_sub_cat)).select(db.sm_category_type.cat_type_name, limitby=(0,1))
    if custSubCatRows:
        subCatName=custSubCatRows[0].cat_type_name
    
    depot_name=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depot_name=depotRow[0].name
    
    store_name=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        store_name=storeRow[0].store_name
        
    out_st_delivery_man_name=''
    dpRow=db((db.sm_delivery_man.cid==c_id)&(db.sm_delivery_man.depot_id==depot_id)&(db.sm_delivery_man.d_man_id==out_st_delivery_man_id)).select(db.sm_delivery_man.name,limitby=(0,1))
    if dpRow:
        out_st_delivery_man_name=dpRow[0].name
        
    out_st_territory_name=''
    levelRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==out_st_territory_id)).select(db.sm_level.level_name,limitby=(0,1))
    if levelRow:
        out_st_territory_name=levelRow[0].level_name
        
    out_st_mso_name=''
    repRow=db((db.sm_rep.cid==c_id)&(db.sm_rep.rep_id==out_st_mso_id)).select(db.sm_rep.name,limitby=(0,1))
    if repRow:
        out_st_mso_name=repRow[0].name
         
    customerName=''
    clientRow=db((db.sm_client.cid==c_id)&(db.sm_client.depot_id==depot_id)&(db.sm_client.client_id==customerId)).select(db.sm_client.name,limitby=(0,1))
    if clientRow:
        customerName=clientRow[0].name
        
    try:        
        startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d').strftime('%Y-%m-%d')
    except:
        startDt=''                
    
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d').strftime('%Y-%m-%d')
    
    #--------------    
    condStr=" AND (round(sm_invoice_head.total_amount-(sm_invoice_head.return_tp+sm_invoice_head.return_vat-sm_invoice_head.return_discount)-sm_invoice_head.collection_amount,2)!=0)"
    
    if out_st_delivery_man_id!='':
        condStr+=" AND (sm_invoice_head.d_man_id='"+out_st_delivery_man_id+"')"        
    if out_st_territory_id!='':
        condStr+=" AND (sm_invoice_head.area_id='"+out_st_territory_id+"')"        
    if out_st_mso_id!='':
        condStr+=" AND (sm_invoice_head.rep_id='"+out_st_mso_id+"')"        
    if invoice_term!='':
        condStr+=" AND (sm_invoice_head.payment_mode='"+invoice_term+"')"
    if customerId!='':
        condStr+=" AND (sm_invoice_head.client_id='"+customerId+"')"
         
    if credit_type!='':
        condStr+=" AND (sm_invoice_head.credit_note='"+credit_type+"')"
    if customer_cat!='':
        condStr+=" AND (sm_invoice_head.cl_category_id='"+customer_cat+"')"
    if customer_sub_cat!='':
        condStr+=" AND (sm_invoice_head.cl_sub_category_id='"+customer_sub_cat+"')"
    
    if out_st_level1_id!='':
        condStr+=" AND (sm_invoice_head.level1_id='"+out_st_level1_id+"')"        
    if out_st_level2_id!='':
        condStr+=" AND (sm_invoice_head.level2_id='"+out_st_level2_id+"')"
        
    if startDt!='' and endDt!='': 
        dateRecords="SELECT sm_invoice_head.d_man_id as d_man_id,MAX(sm_invoice_head.d_man_name) as d_man_name,COUNT(sm_invoice_head.id) as invCount,MAX(sm_invoice_head.sl) as maxSl,MAX(sm_invoice_head.invoice_date) as invoice_date,SUM(sm_invoice_head.actual_total_tp) as actTpAmt, SUM(sm_invoice_head.total_amount) as totalAmt,SUM(sm_invoice_head.vat_total_amount) as vatTotalAmt,SUM(sm_invoice_head.discount) as discAmt,SUM(sm_invoice_head.adjust_amount) as adjustAmt,SUM(sm_invoice_head.return_tp) as retTpAmt,SUM(sm_invoice_head.return_vat) as retVatAmt,SUM(sm_invoice_head.return_discount) as retDiscAmt,SUM(sm_invoice_head.return_sp_discount) as retSpDiscAmt,SUM(sm_invoice_head.collection_amount) as collAmt,SUM(sm_invoice_head.sp_discount) as spDiscAmt FROM sm_invoice_head WHERE ((sm_invoice_head.cid = '"+c_id+"') AND ((sm_invoice_head.invoice_date >= '"+str(startDt)+"') AND (sm_invoice_head.invoice_date <= '"+str(endDt)+"')) AND (sm_invoice_head.depot_id='"+depot_id+"') AND (sm_invoice_head.store_id='"+store_id+"') AND (sm_invoice_head.status='Invoiced') "+str(condStr)+") GROUP BY sm_invoice_head.d_man_id ORDER BY sm_invoice_head.d_man_name"
    else:
        dateRecords="SELECT sm_invoice_head.d_man_id as d_man_id,MAX(sm_invoice_head.d_man_name) as d_man_name,COUNT(sm_invoice_head.id) as invCount,MAX(sm_invoice_head.sl) as maxSl,MAX(sm_invoice_head.invoice_date) as invoice_date,SUM(sm_invoice_head.actual_total_tp) as actTpAmt, SUM(sm_invoice_head.total_amount) as totalAmt,SUM(sm_invoice_head.vat_total_amount) as vatTotalAmt,SUM(sm_invoice_head.discount) as discAmt,SUM(sm_invoice_head.adjust_amount) as adjustAmt,SUM(sm_invoice_head.return_tp) as retTpAmt,SUM(sm_invoice_head.return_vat) as retVatAmt,SUM(sm_invoice_head.return_discount) as retDiscAmt,SUM(sm_invoice_head.return_sp_discount) as retSpDiscAmt,SUM(sm_invoice_head.collection_amount) as collAmt,SUM(sm_invoice_head.sp_discount) as spDiscAmt FROM sm_invoice_head WHERE ((sm_invoice_head.cid = '"+c_id+"') AND (sm_invoice_head.invoice_date <= '"+str(endDt)+"') AND (sm_invoice_head.depot_id='"+depot_id+"') AND (sm_invoice_head.store_id='"+store_id+"') AND (sm_invoice_head.status='Invoiced') "+str(condStr)+") GROUP BY sm_invoice_head.d_man_id ORDER BY sm_invoice_head.d_man_name"
        
    recordList=db.executesql(dateRecords,as_dict = True)
    
    
    #====================
    p_totalInvTP=0
    p_totalInvVat=0
    p_totalInvDisc=0
    p_totalInvSp=0
    p_totalInvAmt=0
    percentTp=0
    percentVat=0
    percentDisc=0
    percentSpDisc=0
    
    for i in range(len(recordList)):                
        recData=recordList[i]
        
        p_invTp=recData['actTpAmt']-(recData['retTpAmt']+recData['retSpDiscAmt'])   
        p_invVat=recData['vatTotalAmt']-recData['retVatAmt']
        p_invDiscount=recData['discAmt']-recData['retDiscAmt']
        p_invSpDisc=recData['spDiscAmt']-recData['retSpDiscAmt']
        p_invNetAmt=p_invTp+p_invVat-(p_invDiscount+p_invSpDisc)
    
        p_outstanding=round(p_invNetAmt-recData['collAmt'],2)
        
        if p_outstanding==0:
            continue
            
        p_totalInvTP+=p_invTp
        p_totalInvVat+=p_invVat
        p_totalInvDisc+=p_invDiscount
        p_totalInvSp+=p_invSpDisc
        p_totalInvAmt+=p_invNetAmt
        
    try:
        percentTp=p_totalInvTP/p_totalInvAmt*100
        percentVat=p_totalInvVat/p_totalInvAmt*100
        percentDisc=p_totalInvDisc/p_totalInvAmt*100
        percentSpDisc=p_totalInvSp/p_totalInvAmt*100
    except:
        percentTp=0
        percentVat=0
        percentDisc=0
        percentSpDisc=0
    #======================
    
    myString='6.4 Delivery Person Wise Outstanding\n'
    myString+='Inv Date From:,'+str(startDt)+'\n'
    myString+='To/ as of Date:'+','+str(endDt)+'\n'
    myString+='Inv Term:,'+str(invoice_term)+'\n'
    myString+='Branch ID:,'+str(depot_id)+'\n'
    myString+='Branch Name'+','+str(depot_name)+'\n'
    myString+='Store ID:,'+str(store_id)+'\n'
    myString+='Store Name'+','+str(store_name)+'\n'
    myString+='DP ID:,'+str(out_st_delivery_man_id)+'\n'
    myString+='DP Name'+','+str(out_st_delivery_man_name)+'\n'
    myString+='Territory ID:,'+str(out_st_territory_id)+'\n'
    myString+='Territory Name'+','+str(out_st_territory_name)+'\n'
    myString+='MSO ID:,'+str(out_st_mso_id)+'\n'
    myString+='MSO Name'+','+str(out_st_mso_name)+'\n'
    myString+='Customer ID:,'+str(customerId)+'\n'
    myString+='Customer Name'+','+str(customerName)+'\n'
    
    myString+='Credit Type:,'+str(credit_type)+'\n'    
    if catName=='':
        catName='ALL'
    if subCatName=='':
        subCatName='ALL'        
    myString+='Customer Category'+','+str(catName)+'\n'
    myString+='Customer Sub-Category'+','+str(subCatName)+'\n'
    
    myString+=str(session.level1Name)+','+str(out_st_level1_id)+'\n'
    myString+=str(session.level2Name)+','+str(out_st_level2_id)+'\n'
    
    totalInvTP=0
    totalInvVat=0
    totalInvDisc=0
    totalInvAmt=0
    totalInvSp=0
    totalOutsTP=0
    totalOutsVat=0
    totalOutsDisc=0
    totalOutST=0
    totalOutSp=0
    
    sl=0
    myString+='SL,DP ID,DP Name,InvCount,LastInv,LastDate,Invoice-TP,Invoice-Vat,Invoice-Disc,Invoice-SP,Invoice-Net,Adjusted,Outstanding-TP,Outstanding-Vat,Outstanding-Disc,Outstanding-SP,Outstanding-Net,Aging,Oustanding%'+'\n'
    for i in range(len(recordList)):
                
        recData=recordList[i]
        
        d_man_id=recData['d_man_id']
        d_man_name=recData['d_man_name']
        invCount=recData['invCount']        
        lastInv=str(session.prefix_invoice)+'INV-'+str(recData['maxSl'])
        lastDate=recData['invoice_date']
        
        adjust_amount=recData['adjustAmt']
        
        #----------
        invTp=recData['actTpAmt']-(recData['retTpAmt']+recData['retSpDiscAmt'])
        invVat=recData['vatTotalAmt']-recData['retVatAmt']
        invDiscount=recData['discAmt']-recData['retDiscAmt']
        invSpDisc=recData['spDiscAmt']-recData['retSpDiscAmt']
        invNetAmt=invTp+invVat-(invDiscount+invSpDisc)
        
        outstanding=round(invNetAmt-recData['collAmt'],2)
        if outstanding==0:
            continue        
        sl+=1        
        try:
#             outTp=(invTp*outstanding)/invNetAmt
#             outVat=(invVat*outstanding)/invNetAmt
#             outDisc=(invDiscount*outstanding)/invNetAmt
#             outSp=(invSpDisc*outstanding)/invNetAmt
            
            outTp=outstanding*(percentTp/100)
            outVat=outstanding*(percentVat/100)
            outDisc=outstanding*(percentDisc/100)
            outSp=outstanding*(percentSpDisc/100)
        except:
            outTp=0
            outVat=0
            outDisc=0
            outSp=0
        
        #-------------        
        totalInvTP+=invTp
        totalInvVat+=invVat
        totalInvDisc+=invDiscount
        totalInvSp+=invSpDisc
        totalInvAmt+=invNetAmt
        
        #totalOutsTP+=outTp
        #totalOutsVat+=outVat
        #totalOutsDisc+=outDisc
        #totalOutSp+=outSp
        
        totalOutST+=outstanding
        
        invoice_date=datetime.datetime.strptime(str(lastDate),'%Y-%m-%d')
        agingDay=(currentDate-invoice_date).days
        
        if invNetAmt!=0:
            outstandingPercent=round((outstanding/invNetAmt*100),2)
        else:
            outstandingPercent=0
        
        #------------------------        
        myString+=str(sl)+','+str(d_man_id)+','+str(d_man_name)+','+str(invCount)+','+str(lastInv)+','+str(lastDate)+','+str(invTp)+','+\
        str(invVat)+','+str(invDiscount)+','+str(invSpDisc)+','+str(invNetAmt)+','+str(adjust_amount)+','+str(outTp)+','+str(outVat)+','+str(outDisc)+','+str(outSp)+','+str(outstanding)+','+\
        str(agingDay)+','+str(outstandingPercent)+'\n'
    
    
    myString+='\n\nSummary,,,,,,,,,,,,,,,,,,,,\n'
    
    myString+='Invoice TP,'+str(round(totalInvTP,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Invoice VAT,'+str(round(totalInvVat,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Invoice Discount,'+str(round(totalInvDisc,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Invoice SP.Disc,'+str(round(totalInvSp,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Invoice Net,'+str(round(totalInvAmt,2))+',,,,,,,,,,,,,,,,,,,\n\n'
    
    
    try:
        totalOutsTP=(totalInvTP*totalOutST)/totalInvAmt
        totalOutsVat=(totalInvVat*totalOutST)/totalInvAmt
        totalOutsDisc=(totalInvDisc*totalOutST)/totalInvAmt
        totalOutSp=(totalInvSp*totalOutST)/totalInvAmt
    except:
        totalOutsTP=0
        totalOutsVat=0
        totalOutsDisc=0
        totalOutSp=0
    
    myString+='Outstanding TP,'+str(round(totalOutsTP,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Outstanding VAT,'+str(round(totalOutsVat,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Outstanding Discount,'+str(round(totalOutsDisc,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Outstanding SP.Disc,'+str(round(totalOutSp,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Outstanding Net,'+str(round(totalOutST,2))+',,,,,,,,,,,,,,,,,,,\n'
    
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_DpWiseOutstanding.csv'   
    return str(myString)


def outStCustomerWise():
    c_id=session.cid
    
    response.title='6.2 Outstanding Customer Wise'
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    depot_id=str(request.vars.depotID).strip()
    store_id=str(request.vars.storeID).strip()
    out_st_delivery_man_id=str(request.vars.deliveryManID).strip()
    out_st_territory_id=str(request.vars.territoryID).strip()
    out_st_mso_id=str(request.vars.msoID).strip()
    invoice_term=str(request.vars.invoice_term).strip()
    customerId=str(request.vars.customerId).strip()
    
    credit_type=str(request.vars.credit_type).strip()
    customer_cat=str(request.vars.customer_cat).strip() 
    customer_sub_cat=str(request.vars.customer_sub_cat).strip()    
    
    out_st_level1_id=str(request.vars.out_st_level1_id).strip()  
    out_st_level2_id=str(request.vars.out_st_level2_id).strip()  
    
    catName=''
    custCatRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_CATEGORY')&(db.sm_category_type.cat_type_id==customer_cat)).select(db.sm_category_type.cat_type_name, limitby=(0,1))
    if custCatRows:
        catName=custCatRows[0].cat_type_name        
    subCatName=''
    custSubCatRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_SUB_CATEGORY')&(db.sm_category_type.cat_type_id==customer_sub_cat)).select(db.sm_category_type.cat_type_name, limitby=(0,1))
    if custSubCatRows:
        subCatName=custSubCatRows[0].cat_type_name
    
    depot_name=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depot_name=depotRow[0].name
    
    store_name=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        store_name=storeRow[0].store_name
        
    out_st_delivery_man_name=''
    dpRow=db((db.sm_delivery_man.cid==c_id)&(db.sm_delivery_man.depot_id==depot_id)&(db.sm_delivery_man.d_man_id==out_st_delivery_man_id)).select(db.sm_delivery_man.name,limitby=(0,1))
    if dpRow:
        out_st_delivery_man_name=dpRow[0].name
        
    out_st_territory_name=''
    levelRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==out_st_territory_id)).select(db.sm_level.level_name,limitby=(0,1))
    if levelRow:
        out_st_territory_name=levelRow[0].level_name
        
    out_st_mso_name=''
    repRow=db((db.sm_rep.cid==c_id)&(db.sm_rep.rep_id==out_st_mso_id)).select(db.sm_rep.name,limitby=(0,1))
    if repRow:
        out_st_mso_name=repRow[0].name
    
    customerName=''
    clientRow=db((db.sm_client.cid==c_id)&(db.sm_client.depot_id==depot_id)&(db.sm_client.client_id==customerId)).select(db.sm_client.name,limitby=(0,1))
    if clientRow:
        customerName=clientRow[0].name
        
    try:        
        startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d').strftime('%Y-%m-%d')     
    except:
        startDt=''                
    
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d').strftime('%Y-%m-%d')
    
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    
    condStr=" AND (round(sm_invoice_head.total_amount-(sm_invoice_head.return_tp+sm_invoice_head.return_vat-sm_invoice_head.return_discount)-sm_invoice_head.collection_amount,2)!=0)"
    
    if out_st_delivery_man_id!='':
        condStr+=" AND (sm_invoice_head.d_man_id='"+out_st_delivery_man_id+"')"        
    if out_st_territory_id!='':
        condStr+=" AND (sm_invoice_head.area_id='"+out_st_territory_id+"')"        
    if out_st_mso_id!='':
        condStr+=" AND (sm_invoice_head.rep_id='"+out_st_mso_id+"')"        
    if invoice_term!='':
        condStr+=" AND (sm_invoice_head.payment_mode='"+invoice_term+"')"
    if customerId!='':
        condStr+=" AND (sm_invoice_head.client_id='"+customerId+"')"
        
    if credit_type!='':
        condStr+=" AND (sm_invoice_head.credit_note='"+credit_type+"')"
    if customer_cat!='':
        condStr+=" AND (sm_invoice_head.cl_category_id='"+customer_cat+"')"
    if customer_sub_cat!='':
        condStr+=" AND (sm_invoice_head.cl_sub_category_id='"+customer_sub_cat+"')"
        
    if out_st_level1_id!='':
        condStr+=" AND (sm_invoice_head.level1_id='"+out_st_level1_id+"')"        
    if out_st_level2_id!='':
        condStr+=" AND (sm_invoice_head.level2_id='"+out_st_level2_id+"')"
        
    if startDt!='' and endDt!='': 
        dateRecords="SELECT sm_invoice_head.client_id as client_id,MAX(sm_invoice_head.client_name) as client_name,sm_invoice_head.market_name as market_name,sm_invoice_head.area_id as area_id,COUNT(sm_invoice_head.id) as invCount,MAX(sm_invoice_head.invoice_date) as invoice_date,SUM(sm_invoice_head.actual_total_tp) as actTpAmt,SUM(sm_invoice_head.total_amount) as totalAmt,SUM(sm_invoice_head.vat_total_amount) as vatTotalAmt,SUM(sm_invoice_head.discount) as discAmt,SUM(sm_invoice_head.adjust_amount) as adjustAmt,SUM(sm_invoice_head.return_tp) as retTpAmt,SUM(sm_invoice_head.return_vat) as retVatAmt,SUM(sm_invoice_head.return_discount) as retDiscAmt,SUM(sm_invoice_head.return_sp_discount) as retSpDiscAmt,SUM(sm_invoice_head.collection_amount) as collAmt,SUM(sm_invoice_head.sp_discount) as spDiscAmt FROM sm_invoice_head WHERE ((sm_invoice_head.cid = '"+c_id+"') AND ((sm_invoice_head.invoice_date >= '"+str(startDt)+"') AND (sm_invoice_head.invoice_date <= '"+str(endDt)+"')) AND (sm_invoice_head.depot_id='"+depot_id+"') AND (sm_invoice_head.store_id='"+store_id+"') AND (sm_invoice_head.status='Invoiced') "+str(condStr)+") GROUP BY sm_invoice_head.client_id,sm_invoice_head.market_name,sm_invoice_head.area_id ORDER BY sm_invoice_head.client_name"
    else:
        dateRecords="SELECT sm_invoice_head.client_id as client_id,MAX(sm_invoice_head.client_name) as client_name,sm_invoice_head.market_name as market_name,sm_invoice_head.area_id as area_id,COUNT(sm_invoice_head.id) as invCount,MAX(sm_invoice_head.invoice_date) as invoice_date,SUM(sm_invoice_head.actual_total_tp) as actTpAmt,SUM(sm_invoice_head.total_amount) as totalAmt,SUM(sm_invoice_head.vat_total_amount) as vatTotalAmt,SUM(sm_invoice_head.discount) as discAmt,SUM(sm_invoice_head.adjust_amount) as adjustAmt,SUM(sm_invoice_head.return_tp) as retTpAmt,SUM(sm_invoice_head.return_vat) as retVatAmt,SUM(sm_invoice_head.return_discount) as retDiscAmt,SUM(sm_invoice_head.return_sp_discount) as retSpDiscAmt,SUM(sm_invoice_head.collection_amount) as collAmt,SUM(sm_invoice_head.sp_discount) as spDiscAmt FROM sm_invoice_head WHERE ((sm_invoice_head.cid = '"+c_id+"') AND (sm_invoice_head.invoice_date <= '"+str(endDt)+"') AND (sm_invoice_head.depot_id='"+depot_id+"') AND (sm_invoice_head.store_id='"+store_id+"') AND (sm_invoice_head.status='Invoiced') "+str(condStr)+") GROUP BY sm_invoice_head.client_id,sm_invoice_head.market_name,sm_invoice_head.area_id ORDER BY sm_invoice_head.client_name"
        
    recordList=db.executesql(dateRecords,as_dict = True)
    
    
    #====================
    p_totalInvTP=0
    p_totalInvVat=0
    p_totalInvDisc=0
    p_totalInvSp=0
    p_totalInvAmt=0
    percentTp=0
    percentVat=0
    percentDisc=0
    percentSpDisc=0
    
    for i in range(len(recordList)):                
        recData=recordList[i]
        
        p_invTp=recData['actTpAmt']-(recData['retTpAmt']+recData['retSpDiscAmt'])   
        p_invVat=recData['vatTotalAmt']-recData['retVatAmt']
        p_invDiscount=recData['discAmt']-recData['retDiscAmt']
        p_invSpDisc=recData['spDiscAmt']-recData['retSpDiscAmt']
        p_invNetAmt=p_invTp+p_invVat-(p_invDiscount+p_invSpDisc)
    
        p_outstanding=round(p_invNetAmt-recData['collAmt'],2)
        
        if p_outstanding==0:
            continue
            
        p_totalInvTP+=p_invTp
        p_totalInvVat+=p_invVat
        p_totalInvDisc+=p_invDiscount
        p_totalInvSp+=p_invSpDisc
        p_totalInvAmt+=p_invNetAmt
        
    try:
        percentTp=p_totalInvTP/p_totalInvAmt*100
        percentVat=p_totalInvVat/p_totalInvAmt*100
        percentDisc=p_totalInvDisc/p_totalInvAmt*100
        percentSpDisc=p_totalInvSp/p_totalInvAmt*100
    except:
        percentTp=0
        percentVat=0
        percentDisc=0
        percentSpDisc=0
    #======================
    
    return dict(percentTp=percentTp,percentVat=percentVat,percentDisc=percentDisc,percentSpDisc=percentSpDisc,recordList=recordList,fromDate=startDt,toDate=toDate,depotID=depot_id,depotName=depot_name,storeID=store_id,storeName=store_name,deliveryManID=out_st_delivery_man_id,deliveryManName=out_st_delivery_man_name,territoryID=out_st_territory_id,territoryName=out_st_territory_name,msoID=out_st_mso_id,msoName=out_st_mso_name,invoice_term=invoice_term,customerId=customerId,customerName=customerName,credit_type=credit_type,customer_cat=customer_cat,customer_sub_cat=customer_sub_cat,catName=catName,subCatName=subCatName,out_st_level1_id=out_st_level1_id,out_st_level2_id=out_st_level2_id,page=page,items_per_page=items_per_page)    


def outStCustomerWise_download():
    c_id=session.cid
    
    response.title='Download-Outstanding Customer Wise'
    
    currentDate=datetime.datetime.strptime(str(current_date),'%Y-%m-%d')
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    depot_id=str(request.vars.depotID).strip()
    store_id=str(request.vars.storeID).strip()
    out_st_delivery_man_id=str(request.vars.deliveryManID).strip()
    out_st_territory_id=str(request.vars.territoryID).strip()
    out_st_mso_id=str(request.vars.msoID).strip()
    invoice_term=str(request.vars.invoice_term).strip()
    customerId=str(request.vars.customerId).strip()
    
    credit_type=str(request.vars.credit_type).strip()
    customer_cat=str(request.vars.customer_cat).strip() 
    customer_sub_cat=str(request.vars.customer_sub_cat).strip()    
    
    out_st_level1_id=str(request.vars.out_st_level1_id).strip()  
    out_st_level2_id=str(request.vars.out_st_level2_id).strip()  
    
    catName=''
    custCatRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_CATEGORY')&(db.sm_category_type.cat_type_id==customer_cat)).select(db.sm_category_type.cat_type_name, limitby=(0,1))
    if custCatRows:
        catName=custCatRows[0].cat_type_name        
    subCatName=''
    custSubCatRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_SUB_CATEGORY')&(db.sm_category_type.cat_type_id==customer_sub_cat)).select(db.sm_category_type.cat_type_name, limitby=(0,1))
    if custSubCatRows:
        subCatName=custSubCatRows[0].cat_type_name
    
    depot_name=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depot_name=depotRow[0].name
    
    store_name=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        store_name=storeRow[0].store_name
        
    out_st_delivery_man_name=''
    dpRow=db((db.sm_delivery_man.cid==c_id)&(db.sm_delivery_man.depot_id==depot_id)&(db.sm_delivery_man.d_man_id==out_st_delivery_man_id)).select(db.sm_delivery_man.name,limitby=(0,1))
    if dpRow:
        out_st_delivery_man_name=dpRow[0].name
        
    out_st_territory_name=''
    levelRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==out_st_territory_id)).select(db.sm_level.level_name,limitby=(0,1))
    if levelRow:
        out_st_territory_name=levelRow[0].level_name
        
    out_st_mso_name=''
    repRow=db((db.sm_rep.cid==c_id)&(db.sm_rep.rep_id==out_st_mso_id)).select(db.sm_rep.name,limitby=(0,1))
    if repRow:
        out_st_mso_name=repRow[0].name
    
    customerName=''
    clientRow=db((db.sm_client.cid==c_id)&(db.sm_client.depot_id==depot_id)&(db.sm_client.client_id==customerId)).select(db.sm_client.name,limitby=(0,1))
    if clientRow:
        customerName=clientRow[0].name
        
    try:        
        startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d').strftime('%Y-%m-%d')     
    except:
        startDt=''                
    
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d').strftime('%Y-%m-%d')
    
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    
    condStr=" AND (round(sm_invoice_head.total_amount-(sm_invoice_head.return_tp+sm_invoice_head.return_vat-sm_invoice_head.return_discount)-sm_invoice_head.collection_amount,2)!=0)"
    
    if out_st_delivery_man_id!='':
        condStr+=" AND (sm_invoice_head.d_man_id='"+out_st_delivery_man_id+"')"        
    if out_st_territory_id!='':
        condStr+=" AND (sm_invoice_head.area_id='"+out_st_territory_id+"')"        
    if out_st_mso_id!='':
        condStr+=" AND (sm_invoice_head.rep_id='"+out_st_mso_id+"')"        
    if invoice_term!='':
        condStr+=" AND (sm_invoice_head.payment_mode='"+invoice_term+"')"
    if customerId!='':
        condStr+=" AND (sm_invoice_head.client_id='"+customerId+"')"
        
    if credit_type!='':
        condStr+=" AND (sm_invoice_head.credit_note='"+credit_type+"')"
    if customer_cat!='':
        condStr+=" AND (sm_invoice_head.cl_category_id='"+customer_cat+"')"
    if customer_sub_cat!='':
        condStr+=" AND (sm_invoice_head.cl_sub_category_id='"+customer_sub_cat+"')"
    
    if out_st_level1_id!='':
        condStr+=" AND (sm_invoice_head.level1_id='"+out_st_level1_id+"')"        
    if out_st_level2_id!='':
        condStr+=" AND (sm_invoice_head.level2_id='"+out_st_level2_id+"')"
        
    if startDt!='' and endDt!='': 
        dateRecords="SELECT sm_invoice_head.client_id as client_id,MAX(sm_invoice_head.client_name) as client_name,sm_invoice_head.market_name as market_name,sm_invoice_head.area_id as area_id,COUNT(sm_invoice_head.id) as invCount,MAX(sm_invoice_head.invoice_date) as invoice_date,SUM(sm_invoice_head.actual_total_tp) as actTpAmt,SUM(sm_invoice_head.total_amount) as totalAmt,SUM(sm_invoice_head.vat_total_amount) as vatTotalAmt,SUM(sm_invoice_head.discount) as discAmt,SUM(sm_invoice_head.adjust_amount) as adjustAmt,SUM(sm_invoice_head.return_tp) as retTpAmt,SUM(sm_invoice_head.return_vat) as retVatAmt,SUM(sm_invoice_head.return_discount) as retDiscAmt,SUM(sm_invoice_head.return_sp_discount) as retSpDiscAmt,SUM(sm_invoice_head.collection_amount) as collAmt,SUM(sm_invoice_head.sp_discount) as spDiscAmt FROM sm_invoice_head WHERE ((sm_invoice_head.cid = '"+c_id+"') AND ((sm_invoice_head.invoice_date >= '"+str(startDt)+"') AND (sm_invoice_head.invoice_date <= '"+str(endDt)+"')) AND (sm_invoice_head.depot_id='"+depot_id+"') AND (sm_invoice_head.store_id='"+store_id+"') AND (sm_invoice_head.status='Invoiced') "+str(condStr)+") GROUP BY sm_invoice_head.client_id,sm_invoice_head.market_name,sm_invoice_head.area_id ORDER BY sm_invoice_head.client_name"
    else:
        dateRecords="SELECT sm_invoice_head.client_id as client_id,MAX(sm_invoice_head.client_name) as client_name,sm_invoice_head.market_name as market_name,sm_invoice_head.area_id as area_id,COUNT(sm_invoice_head.id) as invCount,MAX(sm_invoice_head.invoice_date) as invoice_date,SUM(sm_invoice_head.actual_total_tp) as actTpAmt,SUM(sm_invoice_head.total_amount) as totalAmt,SUM(sm_invoice_head.vat_total_amount) as vatTotalAmt,SUM(sm_invoice_head.discount) as discAmt,SUM(sm_invoice_head.adjust_amount) as adjustAmt,SUM(sm_invoice_head.return_tp) as retTpAmt,SUM(sm_invoice_head.return_vat) as retVatAmt,SUM(sm_invoice_head.return_discount) as retDiscAmt,SUM(sm_invoice_head.return_sp_discount) as retSpDiscAmt,SUM(sm_invoice_head.collection_amount) as collAmt,SUM(sm_invoice_head.sp_discount) as spDiscAmt FROM sm_invoice_head WHERE ((sm_invoice_head.cid = '"+c_id+"') AND (sm_invoice_head.invoice_date <= '"+str(endDt)+"') AND (sm_invoice_head.depot_id='"+depot_id+"') AND (sm_invoice_head.store_id='"+store_id+"') AND (sm_invoice_head.status='Invoiced') "+str(condStr)+") GROUP BY sm_invoice_head.client_id,sm_invoice_head.market_name,sm_invoice_head.area_id ORDER BY sm_invoice_head.client_name"
        
    recordList=db.executesql(dateRecords,as_dict = True)
    
    #====================
    p_totalInvTP=0
    p_totalInvVat=0
    p_totalInvDisc=0
    p_totalInvSp=0
    p_totalInvAmt=0
    percentTp=0
    percentVat=0
    percentDisc=0
    percentSpDisc=0
    
    for i in range(len(recordList)):                
        recData=recordList[i]
        
        p_invTp=recData['actTpAmt']-(recData['retTpAmt']+recData['retSpDiscAmt'])   
        p_invVat=recData['vatTotalAmt']-recData['retVatAmt']
        p_invDiscount=recData['discAmt']-recData['retDiscAmt']
        p_invSpDisc=recData['spDiscAmt']-recData['retSpDiscAmt']
        p_invNetAmt=p_invTp+p_invVat-(p_invDiscount+p_invSpDisc)
    
        p_outstanding=round(p_invNetAmt-recData['collAmt'],2)
        
        if p_outstanding==0:
            continue
            
        p_totalInvTP+=p_invTp
        p_totalInvVat+=p_invVat
        p_totalInvDisc+=p_invDiscount
        p_totalInvSp+=p_invSpDisc
        p_totalInvAmt+=p_invNetAmt
        
    try:
        percentTp=p_totalInvTP/p_totalInvAmt*100
        percentVat=p_totalInvVat/p_totalInvAmt*100
        percentDisc=p_totalInvDisc/p_totalInvAmt*100
        percentSpDisc=p_totalInvSp/p_totalInvAmt*100
    except:
        percentTp=0
        percentVat=0
        percentDisc=0
        percentSpDisc=0
    #======================
    
    myString='6.2 Outstanding Customer Wise\n'
    myString+='Inv Date From:,'+str(startDt)+'\n'
    myString+='To/ as of Date:'+','+str(endDt)+'\n'
    myString+='Inv Term:,'+str(invoice_term)+'\n'
    myString+='Branch ID:,'+str(depot_id)+'\n'
    myString+='Branch Name'+','+str(depot_name)+'\n'
    myString+='Store ID:,'+str(store_id)+'\n'
    myString+='Store Name'+','+str(store_name)+'\n'
    myString+='DP ID:,'+str(out_st_delivery_man_id)+'\n'
    myString+='DP Name'+','+str(out_st_delivery_man_name)+'\n'
    myString+='Territory ID:,'+str(out_st_territory_id)+'\n'
    myString+='Territory Name'+','+str(out_st_territory_name)+'\n'
    myString+='MSO ID:,'+str(out_st_mso_id)+'\n'
    myString+='MSO Name'+','+str(out_st_mso_name)+'\n'
    myString+='Customer ID:,'+str(customerId)+'\n'
    myString+='Customer Name'+','+str(customerName)+'\n'
    
    myString+='Credit Type:,'+str(credit_type)+'\n'    
    if catName=='':
        catName='ALL'
    if subCatName=='':
        subCatName='ALL'        
    myString+='Customer Category'+','+str(catName)+'\n'
    myString+='Customer Sub-Category'+','+str(subCatName)+'\n'
    
    myString+=str(session.level1Name)+','+str(out_st_level1_id)+'\n'
    myString+=str(session.level2Name)+','+str(out_st_level2_id)+'\n'
    
    totalInvTP=0
    totalInvVat=0
    totalInvDisc=0
    totalInvAmt=0
    totalInvSp=0
    totalOutsTP=0
    totalOutsVat=0
    totalOutsDisc=0
    totalOutST=0
    totalOutSp=0    
    sl=0
    
    myString+='SL,Cust.ID,Cust.Name,Inv.Count,Tr.Code,Market,Invoice-TP,Invoice-Vat,Invoice-Disc,Invoice-SP,Invoice-Net,Adjusted,Outstanding-TP,Outstanding-Vat,Outstanding-Disc,Outstanding-SP,Outstanding-Net,Aging,Oustanding%'+'\n'
    for i in range(len(recordList)):                
        recData=recordList[i]
        
        client_id=recData['client_id']
        client_name=str(recData['client_name']).replace(',', ' ')        
        invCount=recData['invCount']    
        area_id=recData['area_id']
        market_name=str(recData['market_name']).replace(',', ' ')
        
        adjust_amount=recData['adjustAmt']
        
        #----------
        invTp=recData['actTpAmt']-(recData['retTpAmt']+recData['retSpDiscAmt'])
        invVat=recData['vatTotalAmt']-recData['retVatAmt']
        invDiscount=recData['discAmt']-recData['retDiscAmt']
        invSpDisc=recData['spDiscAmt']-recData['retSpDiscAmt']
        invNetAmt=invTp+invVat-(invDiscount+invSpDisc)
        
        outstanding=round(invNetAmt-recData['collAmt'],2)
        if outstanding==0:
            continue
        
        sl+=1
        
        try:
#             outTp=(invTp*outstanding)/invNetAmt
#             outVat=(invVat*outstanding)/invNetAmt
#             outDisc=(invDiscount*outstanding)/invNetAmt
#             outSp=(invSpDisc*outstanding)/invNetAmt
            
            outTp=outstanding*(percentTp/100)
            outVat=outstanding*(percentVat/100)
            outDisc=outstanding*(percentDisc/100)
            outSp=outstanding*(percentSpDisc/100)
        except:
            outTp=0
            outVat=0
            outDisc=0
            outSp=0
            
        #-------------        
        totalInvTP+=invTp
        totalInvVat+=invVat
        totalInvDisc+=invDiscount
        totalInvSp+=invSpDisc
        totalInvAmt+=invNetAmt
        
        totalOutST+=outstanding
        
        invoice_date=datetime.datetime.strptime(str(recData['invoice_date']),'%Y-%m-%d')
        agingDay=(currentDate-invoice_date).days
        
        if invNetAmt!=0:
            outstandingPercent=round((outstanding/invNetAmt*100),2)
        else:
            outstandingPercent=0
        
        #------------------------        
        myString+=str(sl)+','+str(client_id)+','+str(client_name)+','+str(invCount)+','+str(area_id)+','+str(market_name)+','+str(invTp)+','+\
        str(invVat)+','+str(invDiscount)+','+str(invSpDisc)+','+str(invNetAmt)+','+str(adjust_amount)+','+str(outTp)+','+str(outVat)+','+str(outDisc)+','+str(outSp)+','+str(outstanding)+','+\
        str(agingDay)+','+str(outstandingPercent)+'\n'
    
    
    #------------------------
    
    myString+='\n\nSummary,,,,,,,,,,,,,,,,,,,,\n'
    
    myString+='Invoice TP,'+str(round(totalInvTP,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Invoice VAT,'+str(round(totalInvVat,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Invoice Discount,'+str(round(totalInvDisc,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Invoice SP.Disc,'+str(round(totalInvSp,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Invoice Net,'+str(round(totalInvAmt,2))+',,,,,,,,,,,,,,,,,,,\n\n'
    
    try:
        totalOutsTP=(totalInvTP*totalOutST)/totalInvAmt
        totalOutsVat=(totalInvVat*totalOutST)/totalInvAmt
        totalOutsDisc=(totalInvDisc*totalOutST)/totalInvAmt
        totalOutSp=(totalInvSp*totalOutST)/totalInvAmt
    except:
        totalOutsTP=0
        totalOutsVat=0
        totalOutsDisc=0
        totalOutSp=0
        
    myString+='Outstanding TP,'+str(round(totalOutsTP,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Outstanding VAT,'+str(round(totalOutsVat,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Outstanding Discount,'+str(round(totalOutsDisc,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Outstanding SP.Disc,'+str(round(totalOutSp,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Outstanding Net,'+str(round(totalOutST,2))+',,,,,,,,,,,,,,,,,,,\n'
    
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_custWiseOutstanding.csv'   
    return str(myString)
    

def outStCustomerWiseDetails():
    c_id=session.cid
    
    response.title='6.3 Outstanding Customer Wise Details'
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    depot_id=str(request.vars.depotID).strip()
    store_id=str(request.vars.storeID).strip()    
    out_st_delivery_man_id=str(request.vars.deliveryManID).strip()    
    out_st_territory_id=str(request.vars.territoryID).strip()    
    out_st_mso_id=str(request.vars.msoID).strip()    
    invoice_term=str(request.vars.invoice_term).strip()
    customerId=str(request.vars.customerId).strip()
    
    credit_type=str(request.vars.credit_type).strip()
    customer_cat=str(request.vars.customer_cat).strip() 
    customer_sub_cat=str(request.vars.customer_sub_cat).strip()    
    
    out_st_level1_id=str(request.vars.out_st_level1_id).strip()  
    out_st_level2_id=str(request.vars.out_st_level2_id).strip()  
    
    catName=''
    custCatRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_CATEGORY')&(db.sm_category_type.cat_type_id==customer_cat)).select(db.sm_category_type.cat_type_name, limitby=(0,1))
    if custCatRows:
        catName=custCatRows[0].cat_type_name        
    subCatName=''
    custSubCatRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_SUB_CATEGORY')&(db.sm_category_type.cat_type_id==customer_sub_cat)).select(db.sm_category_type.cat_type_name, limitby=(0,1))
    if custSubCatRows:
        subCatName=custSubCatRows[0].cat_type_name
    
    depot_name=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depot_name=depotRow[0].name
    
    store_name=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        store_name=storeRow[0].store_name
        
    out_st_delivery_man_name=''
    dpRow=db((db.sm_delivery_man.cid==c_id)&(db.sm_delivery_man.depot_id==depot_id)&(db.sm_delivery_man.d_man_id==out_st_delivery_man_id)).select(db.sm_delivery_man.name,limitby=(0,1))
    if dpRow:
        out_st_delivery_man_name=dpRow[0].name
        
    out_st_territory_name=''
    levelRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==out_st_territory_id)).select(db.sm_level.level_name,limitby=(0,1))
    if levelRow:
        out_st_territory_name=levelRow[0].level_name
        
    out_st_mso_name=''
    repRow=db((db.sm_rep.cid==c_id)&(db.sm_rep.rep_id==out_st_mso_id)).select(db.sm_rep.name,limitby=(0,1))
    if repRow:
        out_st_mso_name=repRow[0].name
    
    customerName=''
    clientRow=db((db.sm_client.cid==c_id)&(db.sm_client.depot_id==depot_id)&(db.sm_client.client_id==customerId)).select(db.sm_client.name,limitby=(0,1))
    if clientRow:
        customerName=clientRow[0].name
    
    
    try:        
        startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d').strftime('%Y-%m-%d')
    except:
        startDt=''                
        
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d').strftime('%Y-%m-%d')
    
    clientRows=db((db.sm_cp_approved.cid==c_id)&(db.sm_cp_approved.branch_id==depot_id)&(db.sm_cp_approved.status=='ACTIVE')).select(db.sm_cp_approved.client_id,db.sm_cp_approved.credit_amount)
    
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    qset=db()
    qset=qset(db.sm_invoice_head.cid==c_id)
    qset=qset(db.sm_invoice_head.depot_id==depot_id)
    qset=qset(db.sm_invoice_head.store_id==store_id)
    if startDt!='' and startDt!='':        
        qset=qset((db.sm_invoice_head.invoice_date>=startDt)&(db.sm_invoice_head.invoice_date<=endDt))
    else:
        qset=qset(db.sm_invoice_head.invoice_date<=endDt)
    
    qset=qset(db.sm_invoice_head.status=='Invoiced')
    qset=qset(db.sm_invoice_head.total_amount-(db.sm_invoice_head.return_tp+db.sm_invoice_head.return_vat-db.sm_invoice_head.return_discount)-db.sm_invoice_head.collection_amount!=0)
    
    if out_st_delivery_man_id!='':
        qset=qset(db.sm_invoice_head.d_man_id==out_st_delivery_man_id)
    if out_st_territory_id!='':
        qset=qset(db.sm_invoice_head.area_id==out_st_territory_id)
    if out_st_mso_id!='':
        qset=qset(db.sm_invoice_head.rep_id==out_st_mso_id)
    if invoice_term!='':
        qset=qset(db.sm_invoice_head.payment_mode==invoice_term)
    if customerId!='':
        qset=qset(db.sm_invoice_head.client_id==customerId)
        
    if credit_type!='':
        qset=qset(db.sm_invoice_head.credit_note==credit_type)
    if customer_cat!='':
        qset=qset(db.sm_invoice_head.cl_category_id==customer_cat)
    if customer_sub_cat!='':
        qset=qset(db.sm_invoice_head.cl_sub_category_id==customer_sub_cat)
        
    if out_st_level1_id!='':
        qset=qset(db.sm_invoice_head.level1_id==out_st_level1_id)
    if out_st_level2_id!='':
        qset=qset(db.sm_invoice_head.level2_id==out_st_level2_id)
        
    records=qset.select(db.sm_invoice_head.ALL,orderby=db.sm_invoice_head.client_name|~db.sm_invoice_head.invoice_date)
    
    #====================
    p_totalInvTP=0
    p_totalInvVat=0
    p_totalInvDisc=0
    p_totalInvSp=0
    p_totalInvAmt=0
    percentTp=0
    percentVat=0
    percentDisc=0
    percentSpDisc=0
    
    for record in records:        
        p_invTp=record.actual_total_tp-(record.return_tp+record.return_sp_discount)
        p_invVat=record.vat_total_amount-record.return_vat
        p_invDiscount=record.discount-record.return_discount
        p_invSpDisc=record.sp_discount-record.return_sp_discount
        p_invNetAmt=p_invTp+p_invVat-(p_invDiscount+p_invSpDisc)
        
        p_outstanding=round(p_invNetAmt-record.collection_amount,2)
        if p_outstanding==0:
            continue
            
        p_totalInvTP+=p_invTp
        p_totalInvVat+=p_invVat
        p_totalInvDisc+=p_invDiscount
        p_totalInvSp+=p_invSpDisc
        p_totalInvAmt+=p_invNetAmt
        
    try:
        percentTp=p_totalInvTP/p_totalInvAmt*100
        percentVat=p_totalInvVat/p_totalInvAmt*100
        percentDisc=p_totalInvDisc/p_totalInvAmt*100
        percentSpDisc=p_totalInvSp/p_totalInvAmt*100
    except:
        percentTp=0
        percentVat=0
        percentDisc=0
        percentSpDisc=0
    #======================
    
    return dict(percentTp=percentTp,percentVat=percentVat,percentDisc=percentDisc,percentSpDisc=percentSpDisc,records=records,clientRows=clientRows,fromDate=startDt,toDate=endDt,depotID=depot_id,depotName=depot_name,storeID=store_id,storeName=store_name,deliveryManID=out_st_delivery_man_id,deliveryManName=out_st_delivery_man_name,territoryID=out_st_territory_id,territoryName=out_st_territory_name,msoID=out_st_mso_id,msoName=out_st_mso_name,invoice_term=invoice_term,customerId=customerId,customerName=customerName,credit_type=credit_type,customer_cat=customer_cat,customer_sub_cat=customer_sub_cat,catName=catName,subCatName=subCatName,out_st_level1_id=out_st_level1_id,out_st_level2_id=out_st_level2_id,page=page,items_per_page=items_per_page)    


def outStCustomerWiseDetails_downlaod():
    c_id=session.cid
    
    currentDate=datetime.datetime.strptime(str(current_date),'%Y-%m-%d')
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    depot_id=str(request.vars.depotID).strip()
    store_id=str(request.vars.storeID).strip()    
    out_st_delivery_man_id=str(request.vars.deliveryManID).strip()    
    out_st_territory_id=str(request.vars.territoryID).strip()    
    out_st_mso_id=str(request.vars.msoID).strip()    
    invoice_term=str(request.vars.invoice_term).strip()
    customerId=str(request.vars.customerId).strip()
    
    credit_type=str(request.vars.credit_type).strip()
    customer_cat=str(request.vars.customer_cat).strip() 
    customer_sub_cat=str(request.vars.customer_sub_cat).strip()    
    
    out_st_level1_id=str(request.vars.out_st_level1_id).strip()  
    out_st_level2_id=str(request.vars.out_st_level2_id).strip()  
    
    catName=''
    custCatRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_CATEGORY')&(db.sm_category_type.cat_type_id==customer_cat)).select(db.sm_category_type.cat_type_name, limitby=(0,1))
    if custCatRows:
        catName=custCatRows[0].cat_type_name        
    subCatName=''
    custSubCatRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_SUB_CATEGORY')&(db.sm_category_type.cat_type_id==customer_sub_cat)).select(db.sm_category_type.cat_type_name, limitby=(0,1))
    if custSubCatRows:
        subCatName=custSubCatRows[0].cat_type_name
    
    depot_name=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depot_name=depotRow[0].name
    
    store_name=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        store_name=storeRow[0].store_name
        
    out_st_delivery_man_name=''
    dpRow=db((db.sm_delivery_man.cid==c_id)&(db.sm_delivery_man.depot_id==depot_id)&(db.sm_delivery_man.d_man_id==out_st_delivery_man_id)).select(db.sm_delivery_man.name,limitby=(0,1))
    if dpRow:
        out_st_delivery_man_name=dpRow[0].name
        
    out_st_territory_name=''
    levelRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==out_st_territory_id)).select(db.sm_level.level_name,limitby=(0,1))
    if levelRow:
        out_st_territory_name=levelRow[0].level_name
        
    out_st_mso_name=''
    repRow=db((db.sm_rep.cid==c_id)&(db.sm_rep.rep_id==out_st_mso_id)).select(db.sm_rep.name,limitby=(0,1))
    if repRow:
        out_st_mso_name=repRow[0].name
        
    customerName=''
    clientRow=db((db.sm_client.cid==c_id)&(db.sm_client.depot_id==depot_id)&(db.sm_client.client_id==customerId)).select(db.sm_client.name,limitby=(0,1))
    if clientRow:
        customerName=clientRow[0].name
    
    try:        
        startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d').strftime('%Y-%m-%d')
    except:
        startDt=''                
        
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d').strftime('%Y-%m-%d')
    
    clientRows=db((db.sm_cp_approved.cid==c_id)&(db.sm_cp_approved.branch_id==depot_id)&(db.sm_cp_approved.status=='ACTIVE')).select(db.sm_cp_approved.client_id,db.sm_cp_approved.credit_amount)
    
    #--------------
    qset=db()
    qset=qset(db.sm_invoice_head.cid==c_id)        
    qset=qset(db.sm_invoice_head.depot_id==depot_id)
    qset=qset(db.sm_invoice_head.store_id==store_id)
    
    if startDt!='' and startDt!='':        
        qset=qset((db.sm_invoice_head.invoice_date>=startDt)&(db.sm_invoice_head.invoice_date<=endDt))
    else:
        qset=qset(db.sm_invoice_head.invoice_date<=endDt)
    
    qset=qset(db.sm_invoice_head.status=='Invoiced')
    qset=qset(db.sm_invoice_head.total_amount-(db.sm_invoice_head.return_tp+db.sm_invoice_head.return_vat-db.sm_invoice_head.return_discount)-db.sm_invoice_head.collection_amount!=0)
    
    if out_st_delivery_man_id!='':
        qset=qset(db.sm_invoice_head.d_man_id==out_st_delivery_man_id)
    if out_st_territory_id!='':
        qset=qset(db.sm_invoice_head.area_id==out_st_territory_id)
    if out_st_mso_id!='':
        qset=qset(db.sm_invoice_head.rep_id==out_st_mso_id)
    if invoice_term!='':
        qset=qset(db.sm_invoice_head.payment_mode==invoice_term)
    if customerId!='':
        qset=qset(db.sm_invoice_head.client_id==customerId)
        
    if credit_type!='':
        qset=qset(db.sm_invoice_head.credit_note==credit_type)
    if customer_cat!='':
        qset=qset(db.sm_invoice_head.cl_category_id==customer_cat)
    if customer_sub_cat!='':
        qset=qset(db.sm_invoice_head.cl_sub_category_id==customer_sub_cat)
      
    if out_st_level1_id!='':
        qset=qset(db.sm_invoice_head.level1_id==out_st_level1_id)
    if out_st_level2_id!='':
        qset=qset(db.sm_invoice_head.level2_id==out_st_level2_id)
        
    records=qset.select(db.sm_invoice_head.ALL,orderby=db.sm_invoice_head.client_name|~db.sm_invoice_head.invoice_date)
    
    #====================
    p_totalInvTP=0
    p_totalInvVat=0
    p_totalInvDisc=0
    p_totalInvSp=0
    p_totalInvAmt=0
    percentTp=0
    percentVat=0
    percentDisc=0
    percentSpDisc=0
    
    for record in records:        
        p_invTp=record.actual_total_tp-(record.return_tp+record.return_sp_discount)
        p_invVat=record.vat_total_amount-record.return_vat
        p_invDiscount=record.discount-record.return_discount
        p_invSpDisc=record.sp_discount-record.return_sp_discount
        p_invNetAmt=p_invTp+p_invVat-(p_invDiscount+p_invSpDisc)
        
        p_outstanding=round(p_invNetAmt-record.collection_amount,2)
        if p_outstanding==0:
            continue
            
        p_totalInvTP+=p_invTp
        p_totalInvVat+=p_invVat
        p_totalInvDisc+=p_invDiscount
        p_totalInvSp+=p_invSpDisc
        p_totalInvAmt+=p_invNetAmt
        
    try:
        percentTp=p_totalInvTP/p_totalInvAmt*100
        percentVat=p_totalInvVat/p_totalInvAmt*100
        percentDisc=p_totalInvDisc/p_totalInvAmt*100
        percentSpDisc=p_totalInvSp/p_totalInvAmt*100
    except:
        percentTp=0
        percentVat=0
        percentDisc=0
        percentSpDisc=0
    #======================
    
    myString='6.3 Customer Wise Details\n'
    myString+='Inv Date From:,'+str(startDt)+'\n'
    myString+='To/ as of Date:'+','+str(endDt)+'\n'
    myString+='Inv Term:,'+str(invoice_term)+'\n'
    myString+='Branch ID:,'+str(depot_id)+'\n'
    myString+='Branch Name'+','+str(depot_name)+'\n'
    myString+='Store ID:,'+str(store_id)+'\n'
    myString+='Store Name'+','+str(store_name)+'\n'
    myString+='DP ID:,'+str(out_st_delivery_man_id)+'\n'
    myString+='DP Name'+','+str(out_st_delivery_man_name)+'\n'
    myString+='Territory ID:,'+str(out_st_territory_id)+'\n'
    myString+='Territory Name'+','+str(out_st_territory_name)+'\n'
    myString+='MSO ID:,'+str(out_st_mso_id)+'\n'
    myString+='MSO Name'+','+str(out_st_mso_name)+'\n'
    myString+='Customer ID:,'+str(customerId)+'\n'
    myString+='Customer Name'+','+str(customerName)+'\n'
    
    myString+='Credit Type:,'+str(credit_type)+'\n'    
    if catName=='':
        catName='ALL'
    if subCatName=='':
        subCatName='ALL'        
    myString+='Customer Category'+','+str(catName)+'\n'
    myString+='Customer Sub-Category'+','+str(subCatName)+'\n'
    
    myString+=str(session.level1Name)+','+str(out_st_level1_id)+'\n'
    myString+=str(session.level2Name)+','+str(out_st_level2_id)+'\n'
    
    totalInvTP=0
    totalInvVat=0
    totalInvDisc=0
    totalInvAmt=0
    totalInvSp=0
    totalOutsTP=0
    totalOutsVat=0
    totalOutsDisc=0
    totalOutST=0
    totalOutSp=0    
    sl=0
    
    preRecClient=''
    newRecClient=''
    totalRowFlag=0
    subTotalOutST=0
    newClient=''
    preClient=''
    myString+='SL,Date,Inv.No,Cust.ID,Cust.Name,Tr.Code,Market,Invoice-TP,Invoice-Vat,Invoice-Disc,Invoice-SP,Invoice-Net,Adjusted,Outstanding-TP,Outstanding-Vat,Outstanding-Disc,Outstanding-SP,Outstanding-Net,Aging,Oustanding%'+'\n'
    for row in records:
        
        clientCredit=0
        #------------------- Sub-Total
        newRecClient=str(row.client_id).strip()   
        newClient=str(row.client_id).strip()+'_'+str(row.client_name).strip() 
        if (preClient!='' and newClient!='' and preClient!=newClient):
            totalRowFlag=1            
            for clRow in clientRows:
                if clRow.client_id==preRecClient:
                    clientCredit=clRow.credit_amount
                    break
                                
        preRecClient=newRecClient  
        preClient=newClient
        
        if totalRowFlag==1 and subTotalOutST!=0:#
            myString+=',,,,,,,,,,,,,,Credit Limit,'+str(clientCredit)+',Total Amount,'+str(subTotalOutST)+',,,\n'
            subTotalOutST=0
            totalRowFlag=0   
        #-----------------------
        
        invoice_date=row.invoice_date
        invNo=str(session.prefix_invoice)+'INV-'+str(row.sl)
        client_id=row.client_id
        client_name=str(row.client_name).replace(',', ' ')
        payment_mode=row.payment_mode
        area_id=row.area_id
        market_name=str(row.market_name).replace(',', ' ')
        
        #-------------
        invTp=row.actual_total_tp-(row.return_tp+row.return_sp_discount)
        invVat=row.vat_total_amount-row.return_vat
        invDiscount=row.discount-row.return_discount
        invSpDisc=row.sp_discount-row.return_sp_discount
        invNetAmt=invTp+invVat-(invDiscount+invSpDisc)
        
        adjust_amount=row.adjust_amount
        
        outstanding=round(invNetAmt-row.collection_amount,2)
        if outstanding==0:
            continue
        sl+=1
        
        try:
#             outTp=(invTp*outstanding)/invNetAmt
#             outVat=(invVat*outstanding)/invNetAmt
#             outDisc=(invDiscount*outstanding)/invNetAmt
#             outSp=(invSpDisc*outstanding)/invNetAmt
            outTp=outstanding*(percentTp/100)
            outVat=outstanding*(percentVat/100)
            outDisc=outstanding*(percentDisc/100)
            outSp=outstanding*(percentSpDisc/100)
        except:
            outTp=0
            outVat=0
            outDisc=0
            outSp=0
        
        totalInvTP+=invTp
        totalInvVat+=invVat
        totalInvDisc+=invDiscount
        totalInvSp+=invSpDisc
        totalInvAmt+=invNetAmt
        
        #totalOutsTP+=outTp
        #totalOutsVat+=outVat
        #totalOutsDisc+=outDisc
        #totalOutSp+=outSp
        
        subTotalOutST+=outstanding
        totalOutST+=outstanding
        
        invoice_date=datetime.datetime.strptime(str(row.invoice_date),'%Y-%m-%d')
        agingDay=(currentDate-invoice_date).days
        
        if invNetAmt!=0:
            outstandingPercent=round((outstanding/invNetAmt*100),2)
        else:
            outstandingPercent=0
            
        #------------------------        
        myString+=str(sl)+','+str(invoice_date)+','+str(invNo)+','+str(client_id)+','+str(client_name)+','+str(area_id)+','+str(market_name)+','+str(invTp)+','+\
        str(invVat)+','+str(invDiscount)+','+str(invSpDisc)+','+str(invNetAmt)+','+str(adjust_amount)+','+str(outTp)+','+str(outVat)+','+str(outDisc)+','+str(outSp)+','+str(outstanding)+','+\
        str(agingDay)+','+str(outstandingPercent)+'\n'
        
    #------------------------ Sub-Total
    if totalRowFlag==0 and subTotalOutST!=0:
        clientCredit=0
        for clRow in clientRows:
            if clRow.client_id==newRecClient:
                clientCredit=clRow.credit_amount
                break
                
        myString+=',,,,,,,,,,,,,,Credit Limit,'+str(clientCredit)+',Total Amount,'+str(subTotalOutST)+',,,\n'
        
    #------------------------    
    myString+='\n\nSummary,,,,,,,,,,,,,,,,,,,,\n'
    
    myString+='Invoice TP,'+str(round(totalInvTP,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Invoice VAT,'+str(round(totalInvVat,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Invoice Discount,'+str(round(totalInvDisc,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Invoice SP.Disc,'+str(round(totalInvSp,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Invoice Net,'+str(round(totalInvAmt,2))+',,,,,,,,,,,,,,,,,,,\n\n'
    
    try:
        totalOutsTP=(totalInvTP*totalOutST)/totalInvAmt
        totalOutsVat=(totalInvVat*totalOutST)/totalInvAmt
        totalOutsDisc=(totalInvDisc*totalOutST)/totalInvAmt
        totalOutSp=(totalInvSp*totalOutST)/totalInvAmt
    except:
        totalOutsTP=0
        totalOutsVat=0
        totalOutsDisc=0
        totalOutSp=0
        
    myString+='Outstanding TP,'+str(round(totalOutsTP,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Outstanding VAT,'+str(round(totalOutsVat,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Outstanding Discount,'+str(round(totalOutsDisc,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Outstanding SP.Disc,'+str(round(totalOutSp,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Outstanding Net,'+str(round(totalOutST,2))+',,,,,,,,,,,,,,,,,,,\n'
    
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_custWiseDetailsOutstanding.csv'   
    return str(myString)

def outStCustomerWiseDetails_print():
    c_id=session.cid
    
    response.title='6.3A Outstanding Customer Wise Details (Print)'
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    depot_id=str(request.vars.depotID).strip()
    store_id=str(request.vars.storeID).strip()    
    out_st_delivery_man_id=str(request.vars.deliveryManID).strip()    
    out_st_territory_id=str(request.vars.territoryID).strip()    
    out_st_mso_id=str(request.vars.msoID).strip()    
    invoice_term=str(request.vars.invoice_term).strip()
    customerId=str(request.vars.customerId).strip()
    
    credit_type=str(request.vars.credit_type).strip()
    customer_cat=str(request.vars.customer_cat).strip() 
    customer_sub_cat=str(request.vars.customer_sub_cat).strip()    
    
    out_st_level1_id=str(request.vars.out_st_level1_id).strip()  
    out_st_level2_id=str(request.vars.out_st_level2_id).strip()  
    
    catName=''
    custCatRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_CATEGORY')&(db.sm_category_type.cat_type_id==customer_cat)).select(db.sm_category_type.cat_type_name, limitby=(0,1))
    if custCatRows:
        catName=custCatRows[0].cat_type_name        
    subCatName=''
    custSubCatRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_SUB_CATEGORY')&(db.sm_category_type.cat_type_id==customer_sub_cat)).select(db.sm_category_type.cat_type_name, limitby=(0,1))
    if custSubCatRows:
        subCatName=custSubCatRows[0].cat_type_name
    
    depot_name=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depot_name=depotRow[0].name
    
    store_name=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        store_name=storeRow[0].store_name
        
    out_st_delivery_man_name=''
    dpRow=db((db.sm_delivery_man.cid==c_id)&(db.sm_delivery_man.depot_id==depot_id)&(db.sm_delivery_man.d_man_id==out_st_delivery_man_id)).select(db.sm_delivery_man.name,limitby=(0,1))
    if dpRow:
        out_st_delivery_man_name=dpRow[0].name
        
    out_st_territory_name=''
    levelRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==out_st_territory_id)).select(db.sm_level.level_name,limitby=(0,1))
    if levelRow:
        out_st_territory_name=levelRow[0].level_name
        
    out_st_mso_name=''
    repRow=db((db.sm_rep.cid==c_id)&(db.sm_rep.rep_id==out_st_mso_id)).select(db.sm_rep.name,limitby=(0,1))
    if repRow:
        out_st_mso_name=repRow[0].name
    
    customerName=''
    clientRow=db((db.sm_client.cid==c_id)&(db.sm_client.depot_id==depot_id)&(db.sm_client.client_id==customerId)).select(db.sm_client.name,limitby=(0,1))
    if clientRow:
        customerName=clientRow[0].name
    
    
    try:        
        startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d').strftime('%Y-%m-%d')
    except:
        startDt=''                
        
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d').strftime('%Y-%m-%d')
    
    clientRows=db((db.sm_cp_approved.cid==c_id)&(db.sm_cp_approved.branch_id==depot_id)&(db.sm_cp_approved.status=='ACTIVE')).select(db.sm_cp_approved.client_id,db.sm_cp_approved.credit_amount)
    
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    qset=db()
    qset=qset(db.sm_invoice_head.cid==c_id)
    qset=qset(db.sm_invoice_head.depot_id==depot_id)
    qset=qset(db.sm_invoice_head.store_id==store_id)
    if startDt!='' and startDt!='':        
        qset=qset((db.sm_invoice_head.invoice_date>=startDt)&(db.sm_invoice_head.invoice_date<=endDt))
    else:
        qset=qset(db.sm_invoice_head.invoice_date<=endDt)
    
    qset=qset(db.sm_invoice_head.status=='Invoiced')
    qset=qset(db.sm_invoice_head.total_amount-(db.sm_invoice_head.return_tp+db.sm_invoice_head.return_vat-db.sm_invoice_head.return_discount)-db.sm_invoice_head.collection_amount!=0)
    
    if out_st_delivery_man_id!='':
        qset=qset(db.sm_invoice_head.d_man_id==out_st_delivery_man_id)
    if out_st_territory_id!='':
        qset=qset(db.sm_invoice_head.area_id==out_st_territory_id)
    if out_st_mso_id!='':
        qset=qset(db.sm_invoice_head.rep_id==out_st_mso_id)
    if invoice_term!='':
        qset=qset(db.sm_invoice_head.payment_mode==invoice_term)
    if customerId!='':
        qset=qset(db.sm_invoice_head.client_id==customerId)
        
    if credit_type!='':
        qset=qset(db.sm_invoice_head.credit_note==credit_type)
    if customer_cat!='':
        qset=qset(db.sm_invoice_head.cl_category_id==customer_cat)
    if customer_sub_cat!='':
        qset=qset(db.sm_invoice_head.cl_sub_category_id==customer_sub_cat)
        
    if out_st_level1_id!='':
        qset=qset(db.sm_invoice_head.level1_id==out_st_level1_id)
    if out_st_level2_id!='':
        qset=qset(db.sm_invoice_head.level2_id==out_st_level2_id)
        
    records=qset.select(db.sm_invoice_head.ALL,orderby=db.sm_invoice_head.client_name|~db.sm_invoice_head.invoice_date)
    
    #====================
    p_totalInvTP=0
    p_totalInvVat=0
    p_totalInvDisc=0
    p_totalInvSp=0
    p_totalInvAmt=0
    percentTp=0
    percentVat=0
    percentDisc=0
    percentSpDisc=0
    
    for record in records:        
        p_invTp=record.actual_total_tp-(record.return_tp+record.return_sp_discount)
        p_invVat=record.vat_total_amount-record.return_vat
        p_invDiscount=record.discount-record.return_discount
        p_invSpDisc=record.sp_discount-record.return_sp_discount
        p_invNetAmt=p_invTp+p_invVat-(p_invDiscount+p_invSpDisc)
        
        p_outstanding=round(p_invNetAmt-record.collection_amount,2)
        if p_outstanding==0:
            continue
            
        p_totalInvTP+=p_invTp
        p_totalInvVat+=p_invVat
        p_totalInvDisc+=p_invDiscount
        p_totalInvSp+=p_invSpDisc
        p_totalInvAmt+=p_invNetAmt
        
    try:
        percentTp=p_totalInvTP/p_totalInvAmt*100
        percentVat=p_totalInvVat/p_totalInvAmt*100
        percentDisc=p_totalInvDisc/p_totalInvAmt*100
        percentSpDisc=p_totalInvSp/p_totalInvAmt*100
    except:
        percentTp=0
        percentVat=0
        percentDisc=0
        percentSpDisc=0
    #======================
    
    return dict(percentTp=percentTp,percentVat=percentVat,percentDisc=percentDisc,percentSpDisc=percentSpDisc,records=records,clientRows=clientRows,fromDate=startDt,toDate=endDt,depotID=depot_id,depotName=depot_name,storeID=store_id,storeName=store_name,deliveryManID=out_st_delivery_man_id,deliveryManName=out_st_delivery_man_name,territoryID=out_st_territory_id,territoryName=out_st_territory_name,msoID=out_st_mso_id,msoName=out_st_mso_name,invoice_term=invoice_term,customerId=customerId,customerName=customerName,credit_type=credit_type,customer_cat=customer_cat,customer_sub_cat=customer_sub_cat,catName=catName,subCatName=subCatName,out_st_level1_id=out_st_level1_id,out_st_level2_id=out_st_level2_id,page=page,items_per_page=items_per_page)    


def outStCustomerWiseDetails_print_downlaod():
    c_id=session.cid
    
    currentDate=datetime.datetime.strptime(str(current_date),'%Y-%m-%d')
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    depot_id=str(request.vars.depotID).strip()
    store_id=str(request.vars.storeID).strip()    
    out_st_delivery_man_id=str(request.vars.deliveryManID).strip()    
    out_st_territory_id=str(request.vars.territoryID).strip()    
    out_st_mso_id=str(request.vars.msoID).strip()    
    invoice_term=str(request.vars.invoice_term).strip()
    customerId=str(request.vars.customerId).strip()
    
    credit_type=str(request.vars.credit_type).strip()
    customer_cat=str(request.vars.customer_cat).strip() 
    customer_sub_cat=str(request.vars.customer_sub_cat).strip()    
    
    out_st_level1_id=str(request.vars.out_st_level1_id).strip()  
    out_st_level2_id=str(request.vars.out_st_level2_id).strip()  
    
    catName=''
    custCatRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_CATEGORY')&(db.sm_category_type.cat_type_id==customer_cat)).select(db.sm_category_type.cat_type_name, limitby=(0,1))
    if custCatRows:
        catName=custCatRows[0].cat_type_name        
    subCatName=''
    custSubCatRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_SUB_CATEGORY')&(db.sm_category_type.cat_type_id==customer_sub_cat)).select(db.sm_category_type.cat_type_name, limitby=(0,1))
    if custSubCatRows:
        subCatName=custSubCatRows[0].cat_type_name
    
    depot_name=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depot_name=depotRow[0].name
    
    store_name=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        store_name=storeRow[0].store_name
        
    out_st_delivery_man_name=''
    dpRow=db((db.sm_delivery_man.cid==c_id)&(db.sm_delivery_man.depot_id==depot_id)&(db.sm_delivery_man.d_man_id==out_st_delivery_man_id)).select(db.sm_delivery_man.name,limitby=(0,1))
    if dpRow:
        out_st_delivery_man_name=dpRow[0].name
        
    out_st_territory_name=''
    levelRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==out_st_territory_id)).select(db.sm_level.level_name,limitby=(0,1))
    if levelRow:
        out_st_territory_name=levelRow[0].level_name
        
    out_st_mso_name=''
    repRow=db((db.sm_rep.cid==c_id)&(db.sm_rep.rep_id==out_st_mso_id)).select(db.sm_rep.name,limitby=(0,1))
    if repRow:
        out_st_mso_name=repRow[0].name
        
    customerName=''
    clientRow=db((db.sm_client.cid==c_id)&(db.sm_client.depot_id==depot_id)&(db.sm_client.client_id==customerId)).select(db.sm_client.name,limitby=(0,1))
    if clientRow:
        customerName=clientRow[0].name
    
    try:        
        startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d').strftime('%Y-%m-%d')
    except:
        startDt=''                
        
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d').strftime('%Y-%m-%d')
    
    clientRows=db((db.sm_cp_approved.cid==c_id)&(db.sm_cp_approved.branch_id==depot_id)&(db.sm_cp_approved.status=='ACTIVE')).select(db.sm_cp_approved.client_id,db.sm_cp_approved.credit_amount)
    
    #--------------
    qset=db()
    qset=qset(db.sm_invoice_head.cid==c_id)        
    qset=qset(db.sm_invoice_head.depot_id==depot_id)
    qset=qset(db.sm_invoice_head.store_id==store_id)
    
    if startDt!='' and startDt!='':        
        qset=qset((db.sm_invoice_head.invoice_date>=startDt)&(db.sm_invoice_head.invoice_date<=endDt))
    else:
        qset=qset(db.sm_invoice_head.invoice_date<=endDt)
    
    qset=qset(db.sm_invoice_head.status=='Invoiced')
    qset=qset(db.sm_invoice_head.total_amount-(db.sm_invoice_head.return_tp+db.sm_invoice_head.return_vat-db.sm_invoice_head.return_discount)-db.sm_invoice_head.collection_amount!=0)
    
    if out_st_delivery_man_id!='':
        qset=qset(db.sm_invoice_head.d_man_id==out_st_delivery_man_id)
    if out_st_territory_id!='':
        qset=qset(db.sm_invoice_head.area_id==out_st_territory_id)
    if out_st_mso_id!='':
        qset=qset(db.sm_invoice_head.rep_id==out_st_mso_id)
    if invoice_term!='':
        qset=qset(db.sm_invoice_head.payment_mode==invoice_term)
    if customerId!='':
        qset=qset(db.sm_invoice_head.client_id==customerId)
        
    if credit_type!='':
        qset=qset(db.sm_invoice_head.credit_note==credit_type)
    if customer_cat!='':
        qset=qset(db.sm_invoice_head.cl_category_id==customer_cat)
    if customer_sub_cat!='':
        qset=qset(db.sm_invoice_head.cl_sub_category_id==customer_sub_cat)
      
    if out_st_level1_id!='':
        qset=qset(db.sm_invoice_head.level1_id==out_st_level1_id)
    if out_st_level2_id!='':
        qset=qset(db.sm_invoice_head.level2_id==out_st_level2_id)
        
    records=qset.select(db.sm_invoice_head.ALL,orderby=db.sm_invoice_head.client_name|~db.sm_invoice_head.invoice_date)
    
    #====================
    p_totalInvTP=0
    p_totalInvVat=0
    p_totalInvDisc=0
    p_totalInvSp=0
    p_totalInvAmt=0
    percentTp=0
    percentVat=0
    percentDisc=0
    percentSpDisc=0
    
    for record in records:        
        p_invTp=record.actual_total_tp-(record.return_tp+record.return_sp_discount)
        p_invVat=record.vat_total_amount-record.return_vat
        p_invDiscount=record.discount-record.return_discount
        p_invSpDisc=record.sp_discount-record.return_sp_discount
        p_invNetAmt=p_invTp+p_invVat-(p_invDiscount+p_invSpDisc)
        
        p_outstanding=round(p_invNetAmt-record.collection_amount,2)
        if p_outstanding==0:
            continue
            
        p_totalInvTP+=p_invTp
        p_totalInvVat+=p_invVat
        p_totalInvDisc+=p_invDiscount
        p_totalInvSp+=p_invSpDisc
        p_totalInvAmt+=p_invNetAmt
        
    try:
        percentTp=p_totalInvTP/p_totalInvAmt*100
        percentVat=p_totalInvVat/p_totalInvAmt*100
        percentDisc=p_totalInvDisc/p_totalInvAmt*100
        percentSpDisc=p_totalInvSp/p_totalInvAmt*100
    except:
        percentTp=0
        percentVat=0
        percentDisc=0
        percentSpDisc=0
    #======================
    
    myString='6.3A Customer Wise Details(Print)\n'
    myString+='Inv Date From:,'+str(startDt)+'\n'
    myString+='To/ as of Date:'+','+str(endDt)+'\n'
    myString+='Inv Term:,'+str(invoice_term)+'\n'
    myString+='Branch ID:,'+str(depot_id)+'\n'
    myString+='Branch Name'+','+str(depot_name)+'\n'
    myString+='Store ID:,'+str(store_id)+'\n'
    myString+='Store Name'+','+str(store_name)+'\n'
    myString+='DP ID:,'+str(out_st_delivery_man_id)+'\n'
    myString+='DP Name'+','+str(out_st_delivery_man_name)+'\n'
    myString+='Territory ID:,'+str(out_st_territory_id)+'\n'
    myString+='Territory Name'+','+str(out_st_territory_name)+'\n'
    myString+='MSO ID:,'+str(out_st_mso_id)+'\n'
    myString+='MSO Name'+','+str(out_st_mso_name)+'\n'
    myString+='Customer ID:,'+str(customerId)+'\n'
    myString+='Customer Name'+','+str(customerName)+'\n'
    
    myString+='Credit Type:,'+str(credit_type)+'\n'    
    if catName=='':
        catName='ALL'
    if subCatName=='':
        subCatName='ALL'        
    myString+='Customer Category'+','+str(catName)+'\n'
    myString+='Customer Sub-Category'+','+str(subCatName)+'\n'
    
    myString+=str(session.level1Name)+','+str(out_st_level1_id)+'\n'
    myString+=str(session.level2Name)+','+str(out_st_level2_id)+'\n'
    
    totalInvTP=0
    totalInvVat=0
    totalInvDisc=0
    totalInvAmt=0
    totalInvSp=0
    totalOutsTP=0
    totalOutsVat=0
    totalOutsDisc=0
    totalOutST=0
    totalOutSp=0    
    sl=0
    
    preRecClient=''
    newRecClient=''
    totalRowFlag=0
    subTotalOutST=0
    newClient=''
    preClient=''
    myString+='SL,Date,Inv.No,Cust.ID,Cust.Name,Tr.Code,Market,Outstanding-TP,Outstanding-Vat,Outstanding-Disc,Outstanding-SP,Outstanding-Net,Aging,Oustanding%'+'\n'
    for row in records:
        
        clientCredit=0
        #------------------- Sub-Total
        newRecClient=str(row.client_id).strip()   
        newClient=str(row.client_id).strip()+'_'+str(row.client_name).strip() 
        if (preClient!='' and newClient!='' and preClient!=newClient):
            totalRowFlag=1            
            for clRow in clientRows:
                if clRow.client_id==preRecClient:
                    clientCredit=clRow.credit_amount
                    break
                                
        preRecClient=newRecClient  
        preClient=newClient
        
        if totalRowFlag==1 and subTotalOutST!=0:#
            myString+=',,,,,,,,Credit Limit,'+str(clientCredit)+',Total Amount,'+str(subTotalOutST)+',,,\n'
            subTotalOutST=0
            totalRowFlag=0   
        #-----------------------
        
        invoice_date=row.invoice_date
        invNo=str(session.prefix_invoice)+'INV-'+str(row.sl)
        client_id=row.client_id
        client_name=str(row.client_name).replace(',', ' ')
        payment_mode=row.payment_mode
        area_id=row.area_id
        market_name=str(row.market_name).replace(',', ' ')
        
        #-------------
        invTp=row.actual_total_tp-(row.return_tp+row.return_sp_discount)
        invVat=row.vat_total_amount-row.return_vat
        invDiscount=row.discount-row.return_discount
        invSpDisc=row.sp_discount-row.return_sp_discount
        invNetAmt=invTp+invVat-(invDiscount+invSpDisc)
        
        adjust_amount=row.adjust_amount
        
        outstanding=round(invNetAmt-row.collection_amount,2)
        if outstanding==0:
            continue
        sl+=1
        
        try:
#             outTp=(invTp*outstanding)/invNetAmt
#             outVat=(invVat*outstanding)/invNetAmt
#             outDisc=(invDiscount*outstanding)/invNetAmt
#             outSp=(invSpDisc*outstanding)/invNetAmt
            outTp=outstanding*(percentTp/100)
            outVat=outstanding*(percentVat/100)
            outDisc=outstanding*(percentDisc/100)
            outSp=outstanding*(percentSpDisc/100)
        except:
            outTp=0
            outVat=0
            outDisc=0
            outSp=0
        
        totalInvTP+=invTp
        totalInvVat+=invVat
        totalInvDisc+=invDiscount
        totalInvSp+=invSpDisc
        totalInvAmt+=invNetAmt
        
        #totalOutsTP+=outTp
        #totalOutsVat+=outVat
        #totalOutsDisc+=outDisc
        #totalOutSp+=outSp
        
        subTotalOutST+=outstanding
        totalOutST+=outstanding
        
        invoice_date=datetime.datetime.strptime(str(row.invoice_date),'%Y-%m-%d')
        agingDay=(currentDate-invoice_date).days
        
        if invNetAmt!=0:
            outstandingPercent=round((outstanding/invNetAmt*100),2)
        else:
            outstandingPercent=0
            
        #------------------------        
        myString+=str(sl)+','+str(invoice_date)+','+str(invNo)+','+str(client_id)+','+str(client_name)+','+str(area_id)+','+str(market_name)+','+str(outTp)+','+str(outVat)+','+str(outDisc)+','+str(outSp)+','+str(outstanding)+','+\
        str(agingDay)+','+str(outstandingPercent)+'\n'
        
    #------------------------ Sub-Total
    if totalRowFlag==0 and subTotalOutST!=0:
        clientCredit=0
        for clRow in clientRows:
            if clRow.client_id==newRecClient:
                clientCredit=clRow.credit_amount
                break
                
        myString+=',,,,,,,,Credit Limit,'+str(clientCredit)+',Total Amount,'+str(subTotalOutST)+',,,\n'
        
    #------------------------    
    myString+='\n\nSummary,,,,,,,,,,,,,,,,,,,,\n'
    
    myString+='Invoice TP,'+str(round(totalInvTP,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Invoice VAT,'+str(round(totalInvVat,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Invoice Discount,'+str(round(totalInvDisc,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Invoice SP.Disc,'+str(round(totalInvSp,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Invoice Net,'+str(round(totalInvAmt,2))+',,,,,,,,,,,,,,,,,,,\n\n'
    
    try:
        totalOutsTP=(totalInvTP*totalOutST)/totalInvAmt
        totalOutsVat=(totalInvVat*totalOutST)/totalInvAmt
        totalOutsDisc=(totalInvDisc*totalOutST)/totalInvAmt
        totalOutSp=(totalInvSp*totalOutST)/totalInvAmt
    except:
        totalOutsTP=0
        totalOutsVat=0
        totalOutsDisc=0
        totalOutSp=0
        
    myString+='Outstanding TP,'+str(round(totalOutsTP,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Outstanding VAT,'+str(round(totalOutsVat,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Outstanding Discount,'+str(round(totalOutsDisc,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Outstanding SP.Disc,'+str(round(totalOutSp,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Outstanding Net,'+str(round(totalOutST,2))+',,,,,,,,,,,,,,,,,,,\n'
    
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_custWiseDetailsOutstanding_print.csv'   
    return str(myString)


def outStCustomerWiseDetails_print2():
    c_id=session.cid
    
    response.title='6.3B Outstanding Customer Wise Details (Print-2)'
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    depot_id=str(request.vars.depotID).strip()
    store_id=str(request.vars.storeID).strip()    
    out_st_delivery_man_id=str(request.vars.deliveryManID).strip()    
    out_st_territory_id=str(request.vars.territoryID).strip()    
    out_st_mso_id=str(request.vars.msoID).strip()    
    invoice_term=str(request.vars.invoice_term).strip()
    customerId=str(request.vars.customerId).strip()
    
    credit_type=str(request.vars.credit_type).strip()
    customer_cat=str(request.vars.customer_cat).strip() 
    customer_sub_cat=str(request.vars.customer_sub_cat).strip()    
    
    out_st_level1_id=str(request.vars.out_st_level1_id).strip()  
    out_st_level2_id=str(request.vars.out_st_level2_id).strip()  
    
    catName=''
    custCatRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_CATEGORY')&(db.sm_category_type.cat_type_id==customer_cat)).select(db.sm_category_type.cat_type_name, limitby=(0,1))
    if custCatRows:
        catName=custCatRows[0].cat_type_name        
    subCatName=''
    custSubCatRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_SUB_CATEGORY')&(db.sm_category_type.cat_type_id==customer_sub_cat)).select(db.sm_category_type.cat_type_name, limitby=(0,1))
    if custSubCatRows:
        subCatName=custSubCatRows[0].cat_type_name
    
    depot_name=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depot_name=depotRow[0].name
    
    store_name=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        store_name=storeRow[0].store_name
        
    out_st_delivery_man_name=''
    dpRow=db((db.sm_delivery_man.cid==c_id)&(db.sm_delivery_man.depot_id==depot_id)&(db.sm_delivery_man.d_man_id==out_st_delivery_man_id)).select(db.sm_delivery_man.name,limitby=(0,1))
    if dpRow:
        out_st_delivery_man_name=dpRow[0].name
        
    out_st_territory_name=''
    levelRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==out_st_territory_id)).select(db.sm_level.level_name,limitby=(0,1))
    if levelRow:
        out_st_territory_name=levelRow[0].level_name
        
    out_st_mso_name=''
    repRow=db((db.sm_rep.cid==c_id)&(db.sm_rep.rep_id==out_st_mso_id)).select(db.sm_rep.name,limitby=(0,1))
    if repRow:
        out_st_mso_name=repRow[0].name
    
    customerName=''
    clientRow=db((db.sm_client.cid==c_id)&(db.sm_client.depot_id==depot_id)&(db.sm_client.client_id==customerId)).select(db.sm_client.name,limitby=(0,1))
    if clientRow:
        customerName=clientRow[0].name
    
    
    try:        
        startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d').strftime('%Y-%m-%d')
    except:
        startDt=''                
        
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d').strftime('%Y-%m-%d')
    
    clientRows=db((db.sm_cp_approved.cid==c_id)&(db.sm_cp_approved.branch_id==depot_id)&(db.sm_cp_approved.status=='ACTIVE')).select(db.sm_cp_approved.client_id,db.sm_cp_approved.credit_amount)
    
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    qset=db()
    qset=qset(db.sm_invoice_head.cid==c_id)
    qset=qset(db.sm_invoice_head.depot_id==depot_id)
    qset=qset(db.sm_invoice_head.store_id==store_id)
    if startDt!='' and startDt!='':        
        qset=qset((db.sm_invoice_head.invoice_date>=startDt)&(db.sm_invoice_head.invoice_date<=endDt))
    else:
        qset=qset(db.sm_invoice_head.invoice_date<=endDt)
    
    qset=qset(db.sm_invoice_head.status=='Invoiced')
    qset=qset(db.sm_invoice_head.total_amount-(db.sm_invoice_head.return_tp+db.sm_invoice_head.return_vat-db.sm_invoice_head.return_discount)-db.sm_invoice_head.collection_amount!=0)
    
    if out_st_delivery_man_id!='':
        qset=qset(db.sm_invoice_head.d_man_id==out_st_delivery_man_id)
    if out_st_territory_id!='':
        qset=qset(db.sm_invoice_head.area_id==out_st_territory_id)
    if out_st_mso_id!='':
        qset=qset(db.sm_invoice_head.rep_id==out_st_mso_id)
    if invoice_term!='':
        qset=qset(db.sm_invoice_head.payment_mode==invoice_term)
    if customerId!='':
        qset=qset(db.sm_invoice_head.client_id==customerId)
        
    if credit_type!='':
        qset=qset(db.sm_invoice_head.credit_note==credit_type)
    if customer_cat!='':
        qset=qset(db.sm_invoice_head.cl_category_id==customer_cat)
    if customer_sub_cat!='':
        qset=qset(db.sm_invoice_head.cl_sub_category_id==customer_sub_cat)
        
    if out_st_level1_id!='':
        qset=qset(db.sm_invoice_head.level1_id==out_st_level1_id)
    if out_st_level2_id!='':
        qset=qset(db.sm_invoice_head.level2_id==out_st_level2_id)
        
    records=qset.select(db.sm_invoice_head.ALL,orderby=db.sm_invoice_head.client_name|~db.sm_invoice_head.invoice_date)
    
    #====================
    p_totalInvTP=0
    p_totalInvVat=0
    p_totalInvDisc=0
    p_totalInvSp=0
    p_totalInvAmt=0
    percentTp=0
    percentVat=0
    percentDisc=0
    percentSpDisc=0
    
    for record in records:        
        p_invTp=record.actual_total_tp-(record.return_tp+record.return_sp_discount)
        p_invVat=record.vat_total_amount-record.return_vat
        p_invDiscount=record.discount-record.return_discount
        p_invSpDisc=record.sp_discount-record.return_sp_discount
        p_invNetAmt=p_invTp+p_invVat-(p_invDiscount+p_invSpDisc)
        
        p_outstanding=round(p_invNetAmt-record.collection_amount,2)
        if p_outstanding==0:
            continue
            
        p_totalInvTP+=p_invTp
        p_totalInvVat+=p_invVat
        p_totalInvDisc+=p_invDiscount
        p_totalInvSp+=p_invSpDisc
        p_totalInvAmt+=p_invNetAmt
        
    try:
        percentTp=p_totalInvTP/p_totalInvAmt*100
        percentVat=p_totalInvVat/p_totalInvAmt*100
        percentDisc=p_totalInvDisc/p_totalInvAmt*100
        percentSpDisc=p_totalInvSp/p_totalInvAmt*100
    except:
        percentTp=0
        percentVat=0
        percentDisc=0
        percentSpDisc=0
    #======================
    
    return dict(percentTp=percentTp,percentVat=percentVat,percentDisc=percentDisc,percentSpDisc=percentSpDisc,records=records,clientRows=clientRows,fromDate=startDt,toDate=endDt,depotID=depot_id,depotName=depot_name,storeID=store_id,storeName=store_name,deliveryManID=out_st_delivery_man_id,deliveryManName=out_st_delivery_man_name,territoryID=out_st_territory_id,territoryName=out_st_territory_name,msoID=out_st_mso_id,msoName=out_st_mso_name,invoice_term=invoice_term,customerId=customerId,customerName=customerName,credit_type=credit_type,customer_cat=customer_cat,customer_sub_cat=customer_sub_cat,catName=catName,subCatName=subCatName,out_st_level1_id=out_st_level1_id,out_st_level2_id=out_st_level2_id,page=page,items_per_page=items_per_page)    


def outStCustomerWiseDetails_print2_downlaod():
    c_id=session.cid
    
    currentDate=datetime.datetime.strptime(str(current_date),'%Y-%m-%d')
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    depot_id=str(request.vars.depotID).strip()
    store_id=str(request.vars.storeID).strip()    
    out_st_delivery_man_id=str(request.vars.deliveryManID).strip()    
    out_st_territory_id=str(request.vars.territoryID).strip()    
    out_st_mso_id=str(request.vars.msoID).strip()    
    invoice_term=str(request.vars.invoice_term).strip()
    customerId=str(request.vars.customerId).strip()
    
    credit_type=str(request.vars.credit_type).strip()
    customer_cat=str(request.vars.customer_cat).strip() 
    customer_sub_cat=str(request.vars.customer_sub_cat).strip()    
    
    out_st_level1_id=str(request.vars.out_st_level1_id).strip()  
    out_st_level2_id=str(request.vars.out_st_level2_id).strip()  
    
    catName=''
    custCatRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_CATEGORY')&(db.sm_category_type.cat_type_id==customer_cat)).select(db.sm_category_type.cat_type_name, limitby=(0,1))
    if custCatRows:
        catName=custCatRows[0].cat_type_name        
    subCatName=''
    custSubCatRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_SUB_CATEGORY')&(db.sm_category_type.cat_type_id==customer_sub_cat)).select(db.sm_category_type.cat_type_name, limitby=(0,1))
    if custSubCatRows:
        subCatName=custSubCatRows[0].cat_type_name
    
    depot_name=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depot_name=depotRow[0].name
    
    store_name=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        store_name=storeRow[0].store_name
        
    out_st_delivery_man_name=''
    dpRow=db((db.sm_delivery_man.cid==c_id)&(db.sm_delivery_man.depot_id==depot_id)&(db.sm_delivery_man.d_man_id==out_st_delivery_man_id)).select(db.sm_delivery_man.name,limitby=(0,1))
    if dpRow:
        out_st_delivery_man_name=dpRow[0].name
        
    out_st_territory_name=''
    levelRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==out_st_territory_id)).select(db.sm_level.level_name,limitby=(0,1))
    if levelRow:
        out_st_territory_name=levelRow[0].level_name
        
    out_st_mso_name=''
    repRow=db((db.sm_rep.cid==c_id)&(db.sm_rep.rep_id==out_st_mso_id)).select(db.sm_rep.name,limitby=(0,1))
    if repRow:
        out_st_mso_name=repRow[0].name
        
    customerName=''
    clientRow=db((db.sm_client.cid==c_id)&(db.sm_client.depot_id==depot_id)&(db.sm_client.client_id==customerId)).select(db.sm_client.name,limitby=(0,1))
    if clientRow:
        customerName=clientRow[0].name
    
    try:        
        startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d').strftime('%Y-%m-%d')
    except:
        startDt=''                
        
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d').strftime('%Y-%m-%d')
    
    clientRows=db((db.sm_cp_approved.cid==c_id)&(db.sm_cp_approved.branch_id==depot_id)&(db.sm_cp_approved.status=='ACTIVE')).select(db.sm_cp_approved.client_id,db.sm_cp_approved.credit_amount)
    
    #--------------
    qset=db()
    qset=qset(db.sm_invoice_head.cid==c_id)        
    qset=qset(db.sm_invoice_head.depot_id==depot_id)
    qset=qset(db.sm_invoice_head.store_id==store_id)
    
    if startDt!='' and startDt!='':        
        qset=qset((db.sm_invoice_head.invoice_date>=startDt)&(db.sm_invoice_head.invoice_date<=endDt))
    else:
        qset=qset(db.sm_invoice_head.invoice_date<=endDt)
    
    qset=qset(db.sm_invoice_head.status=='Invoiced')
    qset=qset(db.sm_invoice_head.total_amount-(db.sm_invoice_head.return_tp+db.sm_invoice_head.return_vat-db.sm_invoice_head.return_discount)-db.sm_invoice_head.collection_amount!=0)
    
    if out_st_delivery_man_id!='':
        qset=qset(db.sm_invoice_head.d_man_id==out_st_delivery_man_id)
    if out_st_territory_id!='':
        qset=qset(db.sm_invoice_head.area_id==out_st_territory_id)
    if out_st_mso_id!='':
        qset=qset(db.sm_invoice_head.rep_id==out_st_mso_id)
    if invoice_term!='':
        qset=qset(db.sm_invoice_head.payment_mode==invoice_term)
    if customerId!='':
        qset=qset(db.sm_invoice_head.client_id==customerId)
        
    if credit_type!='':
        qset=qset(db.sm_invoice_head.credit_note==credit_type)
    if customer_cat!='':
        qset=qset(db.sm_invoice_head.cl_category_id==customer_cat)
    if customer_sub_cat!='':
        qset=qset(db.sm_invoice_head.cl_sub_category_id==customer_sub_cat)
      
    if out_st_level1_id!='':
        qset=qset(db.sm_invoice_head.level1_id==out_st_level1_id)
    if out_st_level2_id!='':
        qset=qset(db.sm_invoice_head.level2_id==out_st_level2_id)
        
    records=qset.select(db.sm_invoice_head.ALL,orderby=db.sm_invoice_head.client_name|~db.sm_invoice_head.invoice_date)
    
    #====================
    p_totalInvTP=0
    p_totalInvVat=0
    p_totalInvDisc=0
    p_totalInvSp=0
    p_totalInvAmt=0
    percentTp=0
    percentVat=0
    percentDisc=0
    percentSpDisc=0
    
    for record in records:        
        p_invTp=record.actual_total_tp-(record.return_tp+record.return_sp_discount)
        p_invVat=record.vat_total_amount-record.return_vat
        p_invDiscount=record.discount-record.return_discount
        p_invSpDisc=record.sp_discount-record.return_sp_discount
        p_invNetAmt=p_invTp+p_invVat-(p_invDiscount+p_invSpDisc)
        
        p_outstanding=round(p_invNetAmt-record.collection_amount,2)
        if p_outstanding==0:
            continue
            
        p_totalInvTP+=p_invTp
        p_totalInvVat+=p_invVat
        p_totalInvDisc+=p_invDiscount
        p_totalInvSp+=p_invSpDisc
        p_totalInvAmt+=p_invNetAmt
        
    try:
        percentTp=p_totalInvTP/p_totalInvAmt*100
        percentVat=p_totalInvVat/p_totalInvAmt*100
        percentDisc=p_totalInvDisc/p_totalInvAmt*100
        percentSpDisc=p_totalInvSp/p_totalInvAmt*100
    except:
        percentTp=0
        percentVat=0
        percentDisc=0
        percentSpDisc=0
    #======================
    
    myString='6.3B Customer Wise Details(Print-2)\n'
    myString+='Inv Date From:,'+str(startDt)+'\n'
    myString+='To/ as of Date:'+','+str(endDt)+'\n'
    myString+='Inv Term:,'+str(invoice_term)+'\n'
    myString+='Branch ID:,'+str(depot_id)+'\n'
    myString+='Branch Name'+','+str(depot_name)+'\n'
    myString+='Store ID:,'+str(store_id)+'\n'
    myString+='Store Name'+','+str(store_name)+'\n'
    myString+='DP ID:,'+str(out_st_delivery_man_id)+'\n'
    myString+='DP Name'+','+str(out_st_delivery_man_name)+'\n'
    myString+='Territory ID:,'+str(out_st_territory_id)+'\n'
    myString+='Territory Name'+','+str(out_st_territory_name)+'\n'
    myString+='MSO ID:,'+str(out_st_mso_id)+'\n'
    myString+='MSO Name'+','+str(out_st_mso_name)+'\n'
    myString+='Customer ID:,'+str(customerId)+'\n'
    myString+='Customer Name'+','+str(customerName)+'\n'
    
    myString+='Credit Type:,'+str(credit_type)+'\n'    
    if catName=='':
        catName='ALL'
    if subCatName=='':
        subCatName='ALL'        
    myString+='Customer Category'+','+str(catName)+'\n'
    myString+='Customer Sub-Category'+','+str(subCatName)+'\n'
    
    myString+=str(session.level1Name)+','+str(out_st_level1_id)+'\n'
    myString+=str(session.level2Name)+','+str(out_st_level2_id)+'\n'
    
    totalInvTP=0
    totalInvVat=0
    totalInvDisc=0
    totalInvAmt=0
    totalInvSp=0
    totalOutsTP=0
    totalOutsVat=0
    totalOutsDisc=0
    totalOutST=0
    totalOutSp=0    
    sl=0
    
    preRecClient=''
    newRecClient=''
    totalRowFlag=0
    subTotalOutST=0
    newClient=''
    preClient=''
    myString+='SL,Date,Inv.No,Cust.ID,Cust.Name,Tr.Code,Market,Outstanding-TP,Outstanding-Vat,Outstanding-Disc,Outstanding-SP,Outstanding-Net,Aging,Oustanding%'+'\n'
    for row in records:
        
        
        #-----------------------
        
        invoice_date=row.invoice_date
        invNo=str(session.prefix_invoice)+'INV-'+str(row.sl)
        client_id=row.client_id
        client_name=str(row.client_name).replace(',', ' ')
        payment_mode=row.payment_mode
        area_id=row.area_id
        market_name=str(row.market_name).replace(',', ' ')
        
        #-------------
        invTp=row.actual_total_tp-(row.return_tp+row.return_sp_discount)
        invVat=row.vat_total_amount-row.return_vat
        invDiscount=row.discount-row.return_discount
        invSpDisc=row.sp_discount-row.return_sp_discount
        invNetAmt=invTp+invVat-(invDiscount+invSpDisc)
        
        adjust_amount=row.adjust_amount
        
        outstanding=round(invNetAmt-row.collection_amount,2)
        if outstanding==0:
            continue
        sl+=1
        
        try:
#             outTp=(invTp*outstanding)/invNetAmt
#             outVat=(invVat*outstanding)/invNetAmt
#             outDisc=(invDiscount*outstanding)/invNetAmt
#             outSp=(invSpDisc*outstanding)/invNetAmt
            outTp=outstanding*(percentTp/100)
            outVat=outstanding*(percentVat/100)
            outDisc=outstanding*(percentDisc/100)
            outSp=outstanding*(percentSpDisc/100)
        except:
            outTp=0
            outVat=0
            outDisc=0
            outSp=0
        
        totalInvTP+=invTp
        totalInvVat+=invVat
        totalInvDisc+=invDiscount
        totalInvSp+=invSpDisc
        totalInvAmt+=invNetAmt
        
        #totalOutsTP+=outTp
        #totalOutsVat+=outVat
        #totalOutsDisc+=outDisc
        #totalOutSp+=outSp
        
        subTotalOutST+=outstanding
        totalOutST+=outstanding
        
        invoice_date=datetime.datetime.strptime(str(row.invoice_date),'%Y-%m-%d')
        agingDay=(currentDate-invoice_date).days
        
        if invNetAmt!=0:
            outstandingPercent=round((outstanding/invNetAmt*100),2)
        else:
            outstandingPercent=0
            
        #------------------------        
        myString+=str(sl)+','+str(invoice_date)+','+str(invNo)+','+str(client_id)+','+str(client_name)+','+str(area_id)+','+str(market_name)+','+str(outTp)+','+str(outVat)+','+str(outDisc)+','+str(outSp)+','+str(outstanding)+','+\
        str(agingDay)+','+str(outstandingPercent)+'\n'
        
    #------------------------ Sub-Total
    
    #------------------------    
    myString+='\n\nSummary,,,,,,,,,,,,,,,,,,,,\n'
    
    myString+='Invoice TP,'+str(round(totalInvTP,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Invoice VAT,'+str(round(totalInvVat,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Invoice Discount,'+str(round(totalInvDisc,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Invoice SP.Disc,'+str(round(totalInvSp,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Invoice Net,'+str(round(totalInvAmt,2))+',,,,,,,,,,,,,,,,,,,\n\n'
    
    try:
        totalOutsTP=(totalInvTP*totalOutST)/totalInvAmt
        totalOutsVat=(totalInvVat*totalOutST)/totalInvAmt
        totalOutsDisc=(totalInvDisc*totalOutST)/totalInvAmt
        totalOutSp=(totalInvSp*totalOutST)/totalInvAmt
    except:
        totalOutsTP=0
        totalOutsVat=0
        totalOutsDisc=0
        totalOutSp=0
        
    myString+='Outstanding TP,'+str(round(totalOutsTP,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Outstanding VAT,'+str(round(totalOutsVat,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Outstanding Discount,'+str(round(totalOutsDisc,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Outstanding SP.Disc,'+str(round(totalOutSp,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Outstanding Net,'+str(round(totalOutST,2))+',,,,,,,,,,,,,,,,,,,\n'
    
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_custWiseDetailsOutstanding_print2.csv'   
    return str(myString)

def outStCustomerWiseDetails2():
    c_id=session.cid
    
    response.title='6.11 A/R Outstanding: Cash/Cheque Instant Report'
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    depot_id=str(request.vars.depotID).strip()
    store_id=str(request.vars.storeID).strip()    
    out_st_delivery_man_id=str(request.vars.deliveryManID).strip()    
    out_st_territory_id=str(request.vars.territoryID).strip()    
    out_st_mso_id=str(request.vars.msoID).strip()    
    invoice_term=str(request.vars.invoice_term).strip()
    customerId=str(request.vars.customerId).strip()
    
    credit_type=str(request.vars.credit_type).strip()
    customer_cat=str(request.vars.customer_cat).strip() 
    customer_sub_cat=str(request.vars.customer_sub_cat).strip()    
    
    out_st_level1_id=str(request.vars.out_st_level1_id).strip()  
    out_st_level2_id=str(request.vars.out_st_level2_id).strip()  
    
    catName=''
    custCatRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_CATEGORY')&(db.sm_category_type.cat_type_id==customer_cat)).select(db.sm_category_type.cat_type_name, limitby=(0,1))
    if custCatRows:
        catName=custCatRows[0].cat_type_name        
    subCatName=''
    custSubCatRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_SUB_CATEGORY')&(db.sm_category_type.cat_type_id==customer_sub_cat)).select(db.sm_category_type.cat_type_name, limitby=(0,1))
    if custSubCatRows:
        subCatName=custSubCatRows[0].cat_type_name
    
    depot_name=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depot_name=depotRow[0].name
    
    store_name=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        store_name=storeRow[0].store_name
        
    out_st_delivery_man_name=''
    dpRow=db((db.sm_delivery_man.cid==c_id)&(db.sm_delivery_man.depot_id==depot_id)&(db.sm_delivery_man.d_man_id==out_st_delivery_man_id)).select(db.sm_delivery_man.name,limitby=(0,1))
    if dpRow:
        out_st_delivery_man_name=dpRow[0].name
        
    out_st_territory_name=''
    levelRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==out_st_territory_id)).select(db.sm_level.level_name,limitby=(0,1))
    if levelRow:
        out_st_territory_name=levelRow[0].level_name
        
    out_st_mso_name=''
    repRow=db((db.sm_rep.cid==c_id)&(db.sm_rep.rep_id==out_st_mso_id)).select(db.sm_rep.name,limitby=(0,1))
    if repRow:
        out_st_mso_name=repRow[0].name
    
    customerName=''
    clientRow=db((db.sm_client.cid==c_id)&(db.sm_client.depot_id==depot_id)&(db.sm_client.client_id==customerId)).select(db.sm_client.name,limitby=(0,1))
    if clientRow:
        customerName=clientRow[0].name
    
    
    try:        
        startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d').strftime('%Y-%m-%d')
    except:
        startDt=''                
        
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d').strftime('%Y-%m-%d')
    
    clientRows=db((db.sm_cp_approved.cid==c_id)&(db.sm_cp_approved.branch_id==depot_id)&(db.sm_cp_approved.status=='ACTIVE')).select(db.sm_cp_approved.client_id,db.sm_cp_approved.credit_amount)
    
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    qset=db()
    qset=qset(db.sm_invoice_head.cid==c_id)
    qset=qset(db.sm_invoice_head.depot_id==depot_id)
    qset=qset(db.sm_invoice_head.store_id==store_id)
    if startDt!='' and startDt!='':        
        qset=qset((db.sm_invoice_head.invoice_date>=startDt)&(db.sm_invoice_head.invoice_date<=endDt))
    else:
        qset=qset(db.sm_invoice_head.invoice_date<=endDt)
    
    qset=qset(db.sm_invoice_head.status=='Invoiced')
    qset=qset(db.sm_invoice_head.total_amount-(db.sm_invoice_head.return_tp+db.sm_invoice_head.return_vat-db.sm_invoice_head.return_discount)-db.sm_invoice_head.collection_amount!=0)
    
    if out_st_delivery_man_id!='':
        qset=qset(db.sm_invoice_head.d_man_id==out_st_delivery_man_id)
    if out_st_territory_id!='':
        qset=qset(db.sm_invoice_head.area_id==out_st_territory_id)
    if out_st_mso_id!='':
        qset=qset(db.sm_invoice_head.rep_id==out_st_mso_id)
    if invoice_term!='':
        qset=qset(db.sm_invoice_head.payment_mode==invoice_term)
    if customerId!='':
        qset=qset(db.sm_invoice_head.client_id==customerId)
        
    if credit_type!='':
        qset=qset(db.sm_invoice_head.credit_note==credit_type)
    if customer_cat!='':
        qset=qset(db.sm_invoice_head.cl_category_id==customer_cat)
    if customer_sub_cat!='':
        qset=qset(db.sm_invoice_head.cl_sub_category_id==customer_sub_cat)
      
    if out_st_level1_id!='':
        qset=qset(db.sm_invoice_head.level1_id==out_st_level1_id)
    if out_st_level2_id!='':
        qset=qset(db.sm_invoice_head.level2_id==out_st_level2_id)
        
    records=qset.select(db.sm_invoice_head.ALL,orderby=db.sm_invoice_head.client_name|db.sm_invoice_head.invoice_date)
    
    #====================
    p_totalInvTP=0
    p_totalInvVat=0
    p_totalInvDisc=0
    p_totalInvSp=0
    p_totalInvAmt=0
    percentTp=0
    percentVat=0
    percentDisc=0
    percentSpDisc=0
    
    for record in records:        
        p_invTp=record.actual_total_tp-(record.return_tp+record.return_sp_discount)
        p_invVat=record.vat_total_amount-record.return_vat
        p_invDiscount=record.discount-record.return_discount
        p_invSpDisc=record.sp_discount-record.return_sp_discount
        p_invNetAmt=p_invTp+p_invVat-(p_invDiscount+p_invSpDisc)
        
        p_outstanding=round(p_invNetAmt-record.collection_amount,2)
        if p_outstanding==0:
            continue
            
        p_totalInvTP+=p_invTp
        p_totalInvVat+=p_invVat
        p_totalInvDisc+=p_invDiscount
        p_totalInvSp+=p_invSpDisc
        p_totalInvAmt+=p_invNetAmt
        
    try:
        percentTp=p_totalInvTP/p_totalInvAmt*100
        percentVat=p_totalInvVat/p_totalInvAmt*100
        percentDisc=p_totalInvDisc/p_totalInvAmt*100
        percentSpDisc=p_totalInvSp/p_totalInvAmt*100
    except:
        percentTp=0
        percentVat=0
        percentDisc=0
        percentSpDisc=0
    #======================
    
    return dict(percentTp=percentTp,percentVat=percentVat,percentDisc=percentDisc,percentSpDisc=percentSpDisc,records=records,clientRows=clientRows,fromDate=startDt,toDate=endDt,depotID=depot_id,depotName=depot_name,storeID=store_id,storeName=store_name,deliveryManID=out_st_delivery_man_id,deliveryManName=out_st_delivery_man_name,territoryID=out_st_territory_id,territoryName=out_st_territory_name,msoID=out_st_mso_id,msoName=out_st_mso_name,invoice_term=invoice_term,customerId=customerId,customerName=customerName,credit_type=credit_type,customer_cat=customer_cat,customer_sub_cat=customer_sub_cat,catName=catName,subCatName=subCatName,out_st_level1_id=out_st_level1_id,out_st_level2_id=out_st_level2_id,page=page,items_per_page=items_per_page)    


def outStCustomerWiseDetails2_downlaod():
    c_id=session.cid
    
    currentDate=datetime.datetime.strptime(str(current_date),'%Y-%m-%d')
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    depot_id=str(request.vars.depotID).strip()
    store_id=str(request.vars.storeID).strip()    
    out_st_delivery_man_id=str(request.vars.deliveryManID).strip()    
    out_st_territory_id=str(request.vars.territoryID).strip()    
    out_st_mso_id=str(request.vars.msoID).strip()    
    invoice_term=str(request.vars.invoice_term).strip()
    customerId=str(request.vars.customerId).strip()
    
    credit_type=str(request.vars.credit_type).strip()
    customer_cat=str(request.vars.customer_cat).strip() 
    customer_sub_cat=str(request.vars.customer_sub_cat).strip()    
    
    out_st_level1_id=str(request.vars.out_st_level1_id).strip()  
    out_st_level2_id=str(request.vars.out_st_level2_id).strip()  
    
    catName=''
    custCatRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_CATEGORY')&(db.sm_category_type.cat_type_id==customer_cat)).select(db.sm_category_type.cat_type_name, limitby=(0,1))
    if custCatRows:
        catName=custCatRows[0].cat_type_name        
    subCatName=''
    custSubCatRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_SUB_CATEGORY')&(db.sm_category_type.cat_type_id==customer_sub_cat)).select(db.sm_category_type.cat_type_name, limitby=(0,1))
    if custSubCatRows:
        subCatName=custSubCatRows[0].cat_type_name
    
    depot_name=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depot_name=depotRow[0].name
    
    store_name=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        store_name=storeRow[0].store_name
        
    out_st_delivery_man_name=''
    dpRow=db((db.sm_delivery_man.cid==c_id)&(db.sm_delivery_man.depot_id==depot_id)&(db.sm_delivery_man.d_man_id==out_st_delivery_man_id)).select(db.sm_delivery_man.name,limitby=(0,1))
    if dpRow:
        out_st_delivery_man_name=dpRow[0].name
        
    out_st_territory_name=''
    levelRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==out_st_territory_id)).select(db.sm_level.level_name,limitby=(0,1))
    if levelRow:
        out_st_territory_name=levelRow[0].level_name
        
    out_st_mso_name=''
    repRow=db((db.sm_rep.cid==c_id)&(db.sm_rep.rep_id==out_st_mso_id)).select(db.sm_rep.name,limitby=(0,1))
    if repRow:
        out_st_mso_name=repRow[0].name
        
    customerName=''
    clientRow=db((db.sm_client.cid==c_id)&(db.sm_client.depot_id==depot_id)&(db.sm_client.client_id==customerId)).select(db.sm_client.name,limitby=(0,1))
    if clientRow:
        customerName=clientRow[0].name
    
    try:        
        startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d').strftime('%Y-%m-%d')
    except:
        startDt=''                
        
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d').strftime('%Y-%m-%d')
    
    clientRows=db((db.sm_cp_approved.cid==c_id)&(db.sm_cp_approved.branch_id==depot_id)&(db.sm_cp_approved.status=='ACTIVE')).select(db.sm_cp_approved.client_id,db.sm_cp_approved.credit_amount)
    
    #--------------
    qset=db()
    qset=qset(db.sm_invoice_head.cid==c_id)        
    qset=qset(db.sm_invoice_head.depot_id==depot_id)
    qset=qset(db.sm_invoice_head.store_id==store_id)
    
    if startDt!='' and startDt!='':        
        qset=qset((db.sm_invoice_head.invoice_date>=startDt)&(db.sm_invoice_head.invoice_date<=endDt))
    else:
        qset=qset(db.sm_invoice_head.invoice_date<=endDt)
    
    qset=qset(db.sm_invoice_head.status=='Invoiced')
    qset=qset(db.sm_invoice_head.total_amount-(db.sm_invoice_head.return_tp+db.sm_invoice_head.return_vat-db.sm_invoice_head.return_discount)-db.sm_invoice_head.collection_amount!=0)
    
    if out_st_delivery_man_id!='':
        qset=qset(db.sm_invoice_head.d_man_id==out_st_delivery_man_id)
    if out_st_territory_id!='':
        qset=qset(db.sm_invoice_head.area_id==out_st_territory_id)
    if out_st_mso_id!='':
        qset=qset(db.sm_invoice_head.rep_id==out_st_mso_id)
    if invoice_term!='':
        qset=qset(db.sm_invoice_head.payment_mode==invoice_term)
    if customerId!='':
        qset=qset(db.sm_invoice_head.client_id==customerId)
        
    if credit_type!='':
        qset=qset(db.sm_invoice_head.credit_note==credit_type)
    if customer_cat!='':
        qset=qset(db.sm_invoice_head.cl_category_id==customer_cat)
    if customer_sub_cat!='':
        qset=qset(db.sm_invoice_head.cl_sub_category_id==customer_sub_cat)
      
    if out_st_level1_id!='':
        qset=qset(db.sm_invoice_head.level1_id==out_st_level1_id)
    if out_st_level2_id!='':
        qset=qset(db.sm_invoice_head.level2_id==out_st_level2_id)
        
    records=qset.select(db.sm_invoice_head.ALL,orderby=db.sm_invoice_head.client_name|db.sm_invoice_head.invoice_date)
    
    #====================
    p_totalInvTP=0
    p_totalInvVat=0
    p_totalInvDisc=0
    p_totalInvSp=0
    p_totalInvAmt=0
    percentTp=0
    percentVat=0
    percentDisc=0
    percentSpDisc=0
    
    for record in records:        
        p_invTp=record.actual_total_tp-(record.return_tp+record.return_sp_discount)
        p_invVat=record.vat_total_amount-record.return_vat
        p_invDiscount=record.discount-record.return_discount
        p_invSpDisc=record.sp_discount-record.return_sp_discount
        p_invNetAmt=p_invTp+p_invVat-(p_invDiscount+p_invSpDisc)
        
        p_outstanding=round(p_invNetAmt-record.collection_amount,2)
        if p_outstanding==0:
            continue
            
        p_totalInvTP+=p_invTp
        p_totalInvVat+=p_invVat
        p_totalInvDisc+=p_invDiscount
        p_totalInvSp+=p_invSpDisc
        p_totalInvAmt+=p_invNetAmt
        
    try:
        percentTp=p_totalInvTP/p_totalInvAmt*100
        percentVat=p_totalInvVat/p_totalInvAmt*100
        percentDisc=p_totalInvDisc/p_totalInvAmt*100
        percentSpDisc=p_totalInvSp/p_totalInvAmt*100
    except:
        percentTp=0
        percentVat=0
        percentDisc=0
        percentSpDisc=0
    #======================
    
    myString='6.11 A/R Outstanding: Cash/Cheque Instant Report\n'
    myString+='Inv Date From:,'+str(startDt)+'\n'
    myString+='To/ as of Date:'+','+str(endDt)+'\n'
    myString+='Inv Term:,'+str(invoice_term)+'\n'
    myString+='Branch ID:,'+str(depot_id)+'\n'
    myString+='Branch Name'+','+str(depot_name)+'\n'
    myString+='Store ID:,'+str(store_id)+'\n'
    myString+='Store Name'+','+str(store_name)+'\n'
    myString+='DP ID:,'+str(out_st_delivery_man_id)+'\n'
    myString+='DP Name'+','+str(out_st_delivery_man_name)+'\n'
    myString+='Territory ID:,'+str(out_st_territory_id)+'\n'
    myString+='Territory Name'+','+str(out_st_territory_name)+'\n'
    myString+='MSO ID:,'+str(out_st_mso_id)+'\n'
    myString+='MSO Name'+','+str(out_st_mso_name)+'\n'
    myString+='Customer ID:,'+str(customerId)+'\n'
    myString+='Customer Name'+','+str(customerName)+'\n'
    
    myString+='Credit Type:,'+str(credit_type)+'\n'    
    if catName=='':
        catName='ALL'
    if subCatName=='':
        subCatName='ALL'        
    myString+='Customer Category'+','+str(catName)+'\n'
    myString+='Customer Sub-Category'+','+str(subCatName)+'\n'
    
    myString+=str(session.level1Name)+','+str(out_st_level1_id)+'\n'
    myString+=str(session.level2Name)+','+str(out_st_level2_id)+'\n'
    
    totalInvTP=0
    totalInvVat=0
    totalInvDisc=0
    totalInvAmt=0
    totalInvSp=0
    totalOutsTP=0
    totalOutsVat=0
    totalOutsDisc=0
    totalOutST=0
    totalOutSp=0    
    sl=0
    
    preRecClient=''
    newRecClient=''
    totalRowFlag=0
    subTotalOutST=0
    newClient=''
    preClient=''
    myString+='SL,Cust.ID,Cust.Name,ShipmentNo,Inv.No,Date,CustomerType,InvoiceType,Invoice-TP,Invoice-Vat,Invoice-Disc,Invoice-SP,Invoice-Net,Adjusted,Outstanding-TP,Outstanding-Vat,Outstanding-Disc,Outstanding-SP,Outstanding-Net,Tr.Code,Remarks'+'\n'
    for row in records:
        
        #-----------------------        
        invoice_date=row.invoice_date
        shipmentNo=row.shipment_no
        invNo=str(session.prefix_invoice)+'INV-'+str(row.sl)
        client_id=row.client_id
        client_name=str(row.client_name).replace(',', ' ')
        payment_mode=row.payment_mode
        area_id=row.area_id
        market_name=str(row.market_name).replace(',', ' ')
        
        invoiceType=''
        cl_category_name=row.cl_category_name
        if row.payment_mode=='CASH':
            invoiceType=row.payment_mode
        else:
            invoiceType=row.credit_note
                                                                            
        #-------------
        invTp=row.actual_total_tp-(row.return_tp+row.return_sp_discount)
        invVat=row.vat_total_amount-row.return_vat
        invDiscount=row.discount-row.return_discount
        invSpDisc=row.sp_discount-row.return_sp_discount
        invNetAmt=invTp+invVat-(invDiscount+invSpDisc)
        
        adjust_amount=row.adjust_amount
        
        outstanding=round(invNetAmt-row.collection_amount,2)
        if outstanding==0:
            continue
        sl+=1
        
        try:
#             outTp=(invTp*outstanding)/invNetAmt
#             outVat=(invVat*outstanding)/invNetAmt
#             outDisc=(invDiscount*outstanding)/invNetAmt
#             outSp=(invSpDisc*outstanding)/invNetAmt
            outTp=outstanding*(percentTp/100)
            outVat=outstanding*(percentVat/100)
            outDisc=outstanding*(percentDisc/100)
            outSp=outstanding*(percentSpDisc/100)
        except:
            outTp=0
            outVat=0
            outDisc=0
            outSp=0
        
        totalInvTP+=invTp
        totalInvVat+=invVat
        totalInvDisc+=invDiscount
        totalInvSp+=invSpDisc
        totalInvAmt+=invNetAmt
        
        subTotalOutST+=outstanding
        totalOutST+=outstanding
        
        invoice_date=datetime.datetime.strptime(str(row.invoice_date),'%Y-%m-%d')
        agingDay=(currentDate-invoice_date).days
        
        if invNetAmt!=0:
            outstandingPercent=round((outstanding/invNetAmt*100),2)
        else:
            outstandingPercent=0
            
        #------------------------        
        myString+=str(sl)+','+str(client_id)+','+str(client_name)+','+str(shipmentNo)+','+str(invNo)+','+str(invoice_date)+','+str(cl_category_name)+','+str(invoiceType)+','+str(invTp)+','+\
        str(invVat)+','+str(invDiscount)+','+str(invSpDisc)+','+str(invNetAmt)+','+str(adjust_amount)+','+str(outTp)+','+str(outVat)+','+str(outDisc)+','+str(outSp)+','+str(outstanding)+','+\
        str(area_id)+',\n'
    
    #------------------------    
    myString+='\n\nSummary,,,,,,,,,,,,,,,,,,,,\n'
    
    myString+='Invoice TP,'+str(round(totalInvTP,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Invoice VAT,'+str(round(totalInvVat,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Invoice Discount,'+str(round(totalInvDisc,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Invoice SP.Disc,'+str(round(totalInvSp,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Invoice Net,'+str(round(totalInvAmt,2))+',,,,,,,,,,,,,,,,,,,\n\n'
    
    try:
        totalOutsTP=(totalInvTP*totalOutST)/totalInvAmt
        totalOutsVat=(totalInvVat*totalOutST)/totalInvAmt
        totalOutsDisc=(totalInvDisc*totalOutST)/totalInvAmt
        totalOutSp=(totalInvSp*totalOutST)/totalInvAmt
    except:
        totalOutsTP=0
        totalOutsVat=0
        totalOutsDisc=0
        totalOutSp=0
        
    myString+='Outstanding TP,'+str(round(totalOutsTP,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Outstanding VAT,'+str(round(totalOutsVat,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Outstanding Discount,'+str(round(totalOutsDisc,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Outstanding SP.Disc,'+str(round(totalOutSp,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Outstanding Net,'+str(round(totalOutST,2))+',,,,,,,,,,,,,,,,,,,\n'
    
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_custWiseDetails-2Outstanding.csv'   
    return str(myString)


def outStCustomerWiseDetails3():
    c_id=session.cid
    
    response.title='6.10 A/R Outstanding'
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    depot_id=str(request.vars.depotID).strip()
    store_id=str(request.vars.storeID).strip()    
    out_st_delivery_man_id=str(request.vars.deliveryManID).strip()    
    out_st_territory_id=str(request.vars.territoryID).strip()    
    out_st_mso_id=str(request.vars.msoID).strip()    
    invoice_term=str(request.vars.invoice_term).strip()
    customerId=str(request.vars.customerId).strip()
    
    credit_type=str(request.vars.credit_type).strip()
    customer_cat=str(request.vars.customer_cat).strip() 
    customer_sub_cat=str(request.vars.customer_sub_cat).strip()    
    
    out_st_level1_id=str(request.vars.out_st_level1_id).strip()  
    out_st_level2_id=str(request.vars.out_st_level2_id).strip()  
    
    catName=''
    custCatRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_CATEGORY')&(db.sm_category_type.cat_type_id==customer_cat)).select(db.sm_category_type.cat_type_name, limitby=(0,1))
    if custCatRows:
        catName=custCatRows[0].cat_type_name        
    subCatName=''
    custSubCatRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_SUB_CATEGORY')&(db.sm_category_type.cat_type_id==customer_sub_cat)).select(db.sm_category_type.cat_type_name, limitby=(0,1))
    if custSubCatRows:
        subCatName=custSubCatRows[0].cat_type_name
    
    depot_name=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depot_name=depotRow[0].name
    
    store_name=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        store_name=storeRow[0].store_name
        
    out_st_delivery_man_name=''
    dpRow=db((db.sm_delivery_man.cid==c_id)&(db.sm_delivery_man.depot_id==depot_id)&(db.sm_delivery_man.d_man_id==out_st_delivery_man_id)).select(db.sm_delivery_man.name,limitby=(0,1))
    if dpRow:
        out_st_delivery_man_name=dpRow[0].name
        
    out_st_territory_name=''
    levelRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==out_st_territory_id)).select(db.sm_level.level_name,limitby=(0,1))
    if levelRow:
        out_st_territory_name=levelRow[0].level_name
        
    out_st_mso_name=''
    repRow=db((db.sm_rep.cid==c_id)&(db.sm_rep.rep_id==out_st_mso_id)).select(db.sm_rep.name,limitby=(0,1))
    if repRow:
        out_st_mso_name=repRow[0].name
    
    customerName=''
    clientRow=db((db.sm_client.cid==c_id)&(db.sm_client.depot_id==depot_id)&(db.sm_client.client_id==customerId)).select(db.sm_client.name,limitby=(0,1))
    if clientRow:
        customerName=clientRow[0].name
        
    try:        
        startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d').strftime('%Y-%m-%d')
    except:
        startDt=''                
        
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d').strftime('%Y-%m-%d')
    
    clientRows=db((db.sm_cp_approved.cid==c_id)&(db.sm_cp_approved.branch_id==depot_id)&(db.sm_cp_approved.status=='ACTIVE')).select(db.sm_cp_approved.client_id,db.sm_cp_approved.credit_amount)
    
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    qset=db()
    qset=qset(db.sm_invoice_head.cid==c_id)
    qset=qset(db.sm_invoice_head.depot_id==depot_id)
    qset=qset(db.sm_invoice_head.store_id==store_id)
    if startDt!='' and startDt!='':        
        qset=qset((db.sm_invoice_head.invoice_date>=startDt)&(db.sm_invoice_head.invoice_date<=endDt))
    else:
        qset=qset(db.sm_invoice_head.invoice_date<=endDt)
    
    qset=qset(db.sm_invoice_head.status=='Invoiced')
    qset=qset(db.sm_invoice_head.total_amount-(db.sm_invoice_head.return_tp+db.sm_invoice_head.return_vat-db.sm_invoice_head.return_discount)-db.sm_invoice_head.collection_amount!=0)
    
    if out_st_delivery_man_id!='':
        qset=qset(db.sm_invoice_head.d_man_id==out_st_delivery_man_id)
    if out_st_territory_id!='':
        qset=qset(db.sm_invoice_head.area_id==out_st_territory_id)
    if out_st_mso_id!='':
        qset=qset(db.sm_invoice_head.rep_id==out_st_mso_id)
    if invoice_term!='':
        qset=qset(db.sm_invoice_head.payment_mode==invoice_term)
    if customerId!='':
        qset=qset(db.sm_invoice_head.client_id==customerId)
        
    if credit_type!='':
        qset=qset(db.sm_invoice_head.credit_note==credit_type)
    if customer_cat!='':
        qset=qset(db.sm_invoice_head.cl_category_id==customer_cat)
    if customer_sub_cat!='':
        qset=qset(db.sm_invoice_head.cl_sub_category_id==customer_sub_cat)
      
    if out_st_level1_id!='':
        qset=qset(db.sm_invoice_head.level1_id==out_st_level1_id)
    if out_st_level2_id!='':
        qset=qset(db.sm_invoice_head.level2_id==out_st_level2_id)
        
    records=qset.select(db.sm_invoice_head.ALL,orderby=db.sm_invoice_head.client_name|db.sm_invoice_head.invoice_date)
    
    #====================
    p_totalInvTP=0
    p_totalInvVat=0
    p_totalInvDisc=0
    p_totalInvSp=0
    p_totalInvAmt=0
    percentTp=0
    percentVat=0
    percentDisc=0
    percentSpDisc=0
    
    for record in records:        
        p_invTp=record.actual_total_tp-(record.return_tp+record.return_sp_discount)
        p_invVat=record.vat_total_amount-record.return_vat
        p_invDiscount=record.discount-record.return_discount
        p_invSpDisc=record.sp_discount-record.return_sp_discount
        p_invNetAmt=p_invTp+p_invVat-(p_invDiscount+p_invSpDisc)
        
        p_outstanding=round(p_invNetAmt-record.collection_amount,2)
        if p_outstanding==0:
            continue
            
        p_totalInvTP+=p_invTp
        p_totalInvVat+=p_invVat
        p_totalInvDisc+=p_invDiscount
        p_totalInvSp+=p_invSpDisc
        p_totalInvAmt+=p_invNetAmt
        
    try:
        percentTp=p_totalInvTP/p_totalInvAmt*100
        percentVat=p_totalInvVat/p_totalInvAmt*100
        percentDisc=p_totalInvDisc/p_totalInvAmt*100
        percentSpDisc=p_totalInvSp/p_totalInvAmt*100
    except:
        percentTp=0
        percentVat=0
        percentDisc=0
        percentSpDisc=0
    #======================
    
    return dict(percentTp=percentTp,percentVat=percentVat,percentDisc=percentDisc,percentSpDisc=percentSpDisc,records=records,clientRows=clientRows,fromDate=startDt,toDate=endDt,depotID=depot_id,depotName=depot_name,storeID=store_id,storeName=store_name,deliveryManID=out_st_delivery_man_id,deliveryManName=out_st_delivery_man_name,territoryID=out_st_territory_id,territoryName=out_st_territory_name,msoID=out_st_mso_id,msoName=out_st_mso_name,invoice_term=invoice_term,customerId=customerId,customerName=customerName,credit_type=credit_type,customer_cat=customer_cat,customer_sub_cat=customer_sub_cat,catName=catName,subCatName=subCatName,out_st_level1_id=out_st_level1_id,out_st_level2_id=out_st_level2_id,page=page,items_per_page=items_per_page)    


def outStCustomerWiseDetails3_downlaod():
    c_id=session.cid
    
    currentDate=datetime.datetime.strptime(str(current_date),'%Y-%m-%d')
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    depot_id=str(request.vars.depotID).strip()
    store_id=str(request.vars.storeID).strip()    
    out_st_delivery_man_id=str(request.vars.deliveryManID).strip()    
    out_st_territory_id=str(request.vars.territoryID).strip()    
    out_st_mso_id=str(request.vars.msoID).strip()    
    invoice_term=str(request.vars.invoice_term).strip()
    customerId=str(request.vars.customerId).strip()
    
    credit_type=str(request.vars.credit_type).strip()
    customer_cat=str(request.vars.customer_cat).strip() 
    customer_sub_cat=str(request.vars.customer_sub_cat).strip()    
    
    out_st_level1_id=str(request.vars.out_st_level1_id).strip()  
    out_st_level2_id=str(request.vars.out_st_level2_id).strip()  
    
    catName=''
    custCatRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_CATEGORY')&(db.sm_category_type.cat_type_id==customer_cat)).select(db.sm_category_type.cat_type_name, limitby=(0,1))
    if custCatRows:
        catName=custCatRows[0].cat_type_name        
    subCatName=''
    custSubCatRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_SUB_CATEGORY')&(db.sm_category_type.cat_type_id==customer_sub_cat)).select(db.sm_category_type.cat_type_name, limitby=(0,1))
    if custSubCatRows:
        subCatName=custSubCatRows[0].cat_type_name
    
    depot_name=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depot_name=depotRow[0].name
    
    store_name=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        store_name=storeRow[0].store_name
        
    out_st_delivery_man_name=''
    dpRow=db((db.sm_delivery_man.cid==c_id)&(db.sm_delivery_man.depot_id==depot_id)&(db.sm_delivery_man.d_man_id==out_st_delivery_man_id)).select(db.sm_delivery_man.name,limitby=(0,1))
    if dpRow:
        out_st_delivery_man_name=dpRow[0].name
        
    out_st_territory_name=''
    levelRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==out_st_territory_id)).select(db.sm_level.level_name,limitby=(0,1))
    if levelRow:
        out_st_territory_name=levelRow[0].level_name
        
    out_st_mso_name=''
    repRow=db((db.sm_rep.cid==c_id)&(db.sm_rep.rep_id==out_st_mso_id)).select(db.sm_rep.name,limitby=(0,1))
    if repRow:
        out_st_mso_name=repRow[0].name
        
    customerName=''
    clientRow=db((db.sm_client.cid==c_id)&(db.sm_client.depot_id==depot_id)&(db.sm_client.client_id==customerId)).select(db.sm_client.name,limitby=(0,1))
    if clientRow:
        customerName=clientRow[0].name
    
    try:        
        startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d').strftime('%Y-%m-%d')
    except:
        startDt=''                
        
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d').strftime('%Y-%m-%d')
    
    clientRows=db((db.sm_cp_approved.cid==c_id)&(db.sm_cp_approved.branch_id==depot_id)&(db.sm_cp_approved.status=='ACTIVE')).select(db.sm_cp_approved.client_id,db.sm_cp_approved.credit_amount)
    
    #--------------
    qset=db()
    qset=qset(db.sm_invoice_head.cid==c_id)        
    qset=qset(db.sm_invoice_head.depot_id==depot_id)
    qset=qset(db.sm_invoice_head.store_id==store_id)
    
    if startDt!='' and startDt!='':        
        qset=qset((db.sm_invoice_head.invoice_date>=startDt)&(db.sm_invoice_head.invoice_date<=endDt))
    else:
        qset=qset(db.sm_invoice_head.invoice_date<=endDt)
    
    qset=qset(db.sm_invoice_head.status=='Invoiced')
    qset=qset(db.sm_invoice_head.total_amount-(db.sm_invoice_head.return_tp+db.sm_invoice_head.return_vat-db.sm_invoice_head.return_discount)-db.sm_invoice_head.collection_amount!=0)
    
    if out_st_delivery_man_id!='':
        qset=qset(db.sm_invoice_head.d_man_id==out_st_delivery_man_id)
    if out_st_territory_id!='':
        qset=qset(db.sm_invoice_head.area_id==out_st_territory_id)
    if out_st_mso_id!='':
        qset=qset(db.sm_invoice_head.rep_id==out_st_mso_id)
    if invoice_term!='':
        qset=qset(db.sm_invoice_head.payment_mode==invoice_term)
    if customerId!='':
        qset=qset(db.sm_invoice_head.client_id==customerId)
        
    if credit_type!='':
        qset=qset(db.sm_invoice_head.credit_note==credit_type)
    if customer_cat!='':
        qset=qset(db.sm_invoice_head.cl_category_id==customer_cat)
    if customer_sub_cat!='':
        qset=qset(db.sm_invoice_head.cl_sub_category_id==customer_sub_cat)
      
    if out_st_level1_id!='':
        qset=qset(db.sm_invoice_head.level1_id==out_st_level1_id)
    if out_st_level2_id!='':
        qset=qset(db.sm_invoice_head.level2_id==out_st_level2_id)
        
    records=qset.select(db.sm_invoice_head.ALL,orderby=db.sm_invoice_head.client_name|db.sm_invoice_head.invoice_date)
    
    #====================
    p_totalInvTP=0
    p_totalInvVat=0
    p_totalInvDisc=0
    p_totalInvSp=0
    p_totalInvAmt=0
    percentTp=0
    percentVat=0
    percentDisc=0
    percentSpDisc=0
    
    for record in records:        
        p_invTp=record.actual_total_tp-(record.return_tp+record.return_sp_discount)
        p_invVat=record.vat_total_amount-record.return_vat
        p_invDiscount=record.discount-record.return_discount
        p_invSpDisc=record.sp_discount-record.return_sp_discount
        p_invNetAmt=p_invTp+p_invVat-(p_invDiscount+p_invSpDisc)
        
        p_outstanding=round(p_invNetAmt-record.collection_amount,2)
        if p_outstanding==0:
            continue
            
        p_totalInvTP+=p_invTp
        p_totalInvVat+=p_invVat
        p_totalInvDisc+=p_invDiscount
        p_totalInvSp+=p_invSpDisc
        p_totalInvAmt+=p_invNetAmt
        
    try:
        percentTp=p_totalInvTP/p_totalInvAmt*100
        percentVat=p_totalInvVat/p_totalInvAmt*100
        percentDisc=p_totalInvDisc/p_totalInvAmt*100
        percentSpDisc=p_totalInvSp/p_totalInvAmt*100
    except:
        percentTp=0
        percentVat=0
        percentDisc=0
        percentSpDisc=0
    #======================
    
    myString='6.10 A/R Outstanding\n'
    myString+='Inv Date From:,'+str(startDt)+'\n'
    myString+='To/ as of Date:'+','+str(endDt)+'\n'
    myString+='Inv Term:,'+str(invoice_term)+'\n'
    myString+='Branch ID:,'+str(depot_id)+'\n'
    myString+='Branch Name'+','+str(depot_name)+'\n'
    myString+='Store ID:,'+str(store_id)+'\n'
    myString+='Store Name'+','+str(store_name)+'\n'
    myString+='DP ID:,'+str(out_st_delivery_man_id)+'\n'
    myString+='DP Name'+','+str(out_st_delivery_man_name)+'\n'
    myString+='Territory ID:,'+str(out_st_territory_id)+'\n'
    myString+='Territory Name'+','+str(out_st_territory_name)+'\n'
    myString+='MSO ID:,'+str(out_st_mso_id)+'\n'
    myString+='MSO Name'+','+str(out_st_mso_name)+'\n'
    myString+='Customer ID:,'+str(customerId)+'\n'
    myString+='Customer Name'+','+str(customerName)+'\n'
    
    myString+='Credit Type:,'+str(credit_type)+'\n'    
    if catName=='':
        catName='ALL'
    if subCatName=='':
        subCatName='ALL'        
    myString+='Customer Category'+','+str(catName)+'\n'
    myString+='Customer Sub-Category'+','+str(subCatName)+'\n'
    
    myString+=str(session.level1Name)+','+str(out_st_level1_id)+'\n'
    myString+=str(session.level2Name)+','+str(out_st_level2_id)+'\n'
    
    totalInvTP=0
    totalInvVat=0
    totalInvDisc=0
    totalInvAmt=0
    totalInvSp=0
    totalOutsTP=0
    totalOutsVat=0
    totalOutsDisc=0
    totalOutST=0
    totalOutSp=0    
    sl=0
    
    preRecClient=''
    newRecClient=''
    totalRowFlag=0
    subTotalOutST=0
    newClient=''
    preClient=''
    myString+='SL,Date,ShipmentNo,Inv.No,Cust.ID,Cust.Name,MSOID,MSOName,Tr.Code,DPName,Terms,Invoice-TP,Invoice-Vat,Invoice-Disc,Invoice-SP,Invoice-Net,Adjusted,Outstanding-TP,Outstanding-Vat,Outstanding-Disc,Outstanding-SP,Outstanding-Net,Aging(Days),Outstanding%,Address/Market'+'\n'
    for row in records:
        
        #-----------------------
        
        invoice_date=row.invoice_date
        shipmentNo=row.shipment_no
        invNo=str(session.prefix_invoice)+'INV-'+str(row.sl)
        client_id=row.client_id
        client_name=str(row.client_name).replace(',', ' ')
        rep_id=row.rep_id
        rep_name=str(row.rep_name).replace(',', ' ')
        d_man_name=str(row.d_man_name).replace(',', ' ')
        payment_mode=row.payment_mode
        area_id=row.area_id
        market_name=str(row.market_name).replace(',', ' ')
        
        invoiceType=''
        cl_category_name=row.cl_category_name
        if row.payment_mode=='CASH':
            invoiceType=row.payment_mode
        else:
            invoiceType=row.credit_note
            
        #-------------
        invTp=row.actual_total_tp-(row.return_tp+row.return_sp_discount)
        invVat=row.vat_total_amount-row.return_vat
        invDiscount=row.discount-row.return_discount
        invSpDisc=row.sp_discount-row.return_sp_discount
        invNetAmt=invTp+invVat-(invDiscount+invSpDisc)
        
        adjust_amount=row.adjust_amount
        
        outstanding=round(invNetAmt-row.collection_amount,2)
        if outstanding==0:
            continue
        sl+=1
        
        try:
#             outTp=(invTp*outstanding)/invNetAmt
#             outVat=(invVat*outstanding)/invNetAmt
#             outDisc=(invDiscount*outstanding)/invNetAmt
#             outSp=(invSpDisc*outstanding)/invNetAmt
            outTp=outstanding*(percentTp/100)
            outVat=outstanding*(percentVat/100)
            outDisc=outstanding*(percentDisc/100)
            outSp=outstanding*(percentSpDisc/100)
        except:
            outTp=0
            outVat=0
            outDisc=0
            outSp=0
        
        totalInvTP+=invTp
        totalInvVat+=invVat
        totalInvDisc+=invDiscount
        totalInvSp+=invSpDisc
        totalInvAmt+=invNetAmt
        
        subTotalOutST+=outstanding
        totalOutST+=outstanding
        
        invoice_date=datetime.datetime.strptime(str(row.invoice_date),'%Y-%m-%d')
        agingDay=(currentDate-invoice_date).days
        
        if invNetAmt!=0:
            outstandingPercent=round((outstanding/invNetAmt*100),2)
        else:
            outstandingPercent=0
            
        #------------------------        
        myString+=str(sl)+','+str(invoice_date)+','+str(shipmentNo)+','+str(invNo)+','+str(client_id)+','+str(client_name)+','+str(rep_id)+','+str(rep_name)+','+str(area_id)+','+str(d_man_name)+','+str(invoiceType)+','+str(invTp)+','+\
        str(invVat)+','+str(invDiscount)+','+str(invSpDisc)+','+str(invNetAmt)+','+str(adjust_amount)+','+str(outTp)+','+str(outVat)+','+str(outDisc)+','+str(outSp)+','+str(outstanding)+','+\
        str(agingDay)+','+str(outstandingPercent)+','+str(market_name)+',\n'
    
    #------------------------    
    myString+='\n\nSummary,,,,,,,,,,,,,,,,,,,,\n'
    
    myString+='Invoice TP,'+str(round(totalInvTP,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Invoice VAT,'+str(round(totalInvVat,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Invoice Discount,'+str(round(totalInvDisc,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Invoice SP.Disc,'+str(round(totalInvSp,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Invoice Net,'+str(round(totalInvAmt,2))+',,,,,,,,,,,,,,,,,,,\n\n'
    
    try:
        totalOutsTP=(totalInvTP*totalOutST)/totalInvAmt
        totalOutsVat=(totalInvVat*totalOutST)/totalInvAmt
        totalOutsDisc=(totalInvDisc*totalOutST)/totalInvAmt
        totalOutSp=(totalInvSp*totalOutST)/totalInvAmt
    except:
        totalOutsTP=0
        totalOutsVat=0
        totalOutsDisc=0
        totalOutSp=0
        
    myString+='Outstanding TP,'+str(round(totalOutsTP,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Outstanding VAT,'+str(round(totalOutsVat,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Outstanding Discount,'+str(round(totalOutsDisc,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Outstanding SP.Disc,'+str(round(totalOutSp,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Outstanding Net,'+str(round(totalOutST,2))+',,,,,,,,,,,,,,,,,,,\n'
    
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_A/ROutstanding.csv'   
    return str(myString)
    

def outStInvoiceWise():
    c_id=session.cid
    
    response.title='6.1 Outstanding Invoice Wise'
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    depot_id=str(request.vars.depotID).strip()
    store_id=str(request.vars.storeID).strip()
    out_st_delivery_man_id=str(request.vars.deliveryManID).strip()
    out_st_territory_id=str(request.vars.territoryID).strip()
    out_st_mso_id=str(request.vars.msoID).strip()
    invoice_term=str(request.vars.invoice_term).strip()
    customerId=str(request.vars.customerId).strip()
    
    credit_type=str(request.vars.credit_type).strip()
    customer_cat=str(request.vars.customer_cat).strip() 
    customer_sub_cat=str(request.vars.customer_sub_cat).strip()  
    
    out_st_level1_id=str(request.vars.out_st_level1_id).strip()  
    out_st_level2_id=str(request.vars.out_st_level2_id).strip()  
    
    catName=''
    custCatRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_CATEGORY')&(db.sm_category_type.cat_type_id==customer_cat)).select(db.sm_category_type.cat_type_name, limitby=(0,1))
    if custCatRows:
        catName=custCatRows[0].cat_type_name        
    subCatName=''
    custSubCatRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_SUB_CATEGORY')&(db.sm_category_type.cat_type_id==customer_sub_cat)).select(db.sm_category_type.cat_type_name, limitby=(0,1))
    if custSubCatRows:
        subCatName=custSubCatRows[0].cat_type_name
    
    
    depot_name=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depot_name=depotRow[0].name
        
    store_name=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        store_name=storeRow[0].store_name
        
    out_st_delivery_man_name=''
    dpRow=db((db.sm_delivery_man.cid==c_id)&(db.sm_delivery_man.depot_id==depot_id)&(db.sm_delivery_man.d_man_id==out_st_delivery_man_id)).select(db.sm_delivery_man.name,limitby=(0,1))
    if dpRow:
        out_st_delivery_man_name=dpRow[0].name
        
    out_st_territory_name=''
    levelRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==out_st_territory_id)).select(db.sm_level.level_name,limitby=(0,1))
    if levelRow:
        out_st_territory_name=levelRow[0].level_name
        
    out_st_mso_name=''
    repRow=db((db.sm_rep.cid==c_id)&(db.sm_rep.rep_id==out_st_mso_id)).select(db.sm_rep.name,limitby=(0,1))
    if repRow:
        out_st_mso_name=repRow[0].name
        
    customerName=''
    clientRow=db((db.sm_client.cid==c_id)&(db.sm_client.depot_id==depot_id)&(db.sm_client.client_id==customerId)).select(db.sm_client.name,limitby=(0,1))
    if clientRow:
        customerName=clientRow[0].name
        
    try:        
        startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d').strftime('%Y-%m-%d')
    except:
        startDt=''                
    
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d').strftime('%Y-%m-%d')
    
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    
    qset=db()
    qset=qset(db.sm_invoice_head.cid==c_id)
    qset=qset(db.sm_invoice_head.depot_id==depot_id)
    qset=qset(db.sm_invoice_head.store_id==store_id)
    qset=qset(db.sm_invoice_head.status=='Invoiced')
    
    if startDt!='' and endDt!=None:
        qset=qset((db.sm_invoice_head.invoice_date>=startDt)&(db.sm_invoice_head.invoice_date<=endDt))
    else:
        qset=qset(db.sm_invoice_head.invoice_date<=endDt)
        
    qset=qset((db.sm_invoice_head.total_amount-(db.sm_invoice_head.return_tp+db.sm_invoice_head.return_vat-db.sm_invoice_head.return_discount))-db.sm_invoice_head.collection_amount!=0)
    
    if out_st_delivery_man_id!='':
        qset=qset(db.sm_invoice_head.d_man_id==out_st_delivery_man_id)
    if out_st_territory_id!='':
        qset=qset(db.sm_invoice_head.area_id==out_st_territory_id)
    if out_st_mso_id!='':
        qset=qset(db.sm_invoice_head.rep_id==out_st_mso_id)
    if invoice_term!='':
        qset=qset(db.sm_invoice_head.payment_mode==invoice_term)
    if customerId!='':
        qset=qset(db.sm_invoice_head.client_id==customerId)
        
    if credit_type!='':
        qset=qset(db.sm_invoice_head.credit_note==credit_type)
    if customer_cat!='':
        qset=qset(db.sm_invoice_head.cl_category_id==customer_cat)
    if customer_sub_cat!='':
        qset=qset(db.sm_invoice_head.cl_sub_category_id==customer_sub_cat)
        
    if out_st_level1_id!='':
        qset=qset(db.sm_invoice_head.level1_id==out_st_level1_id)
    if out_st_level2_id!='':
        qset=qset(db.sm_invoice_head.level2_id==out_st_level2_id)
        
    records=qset.select(db.sm_invoice_head.ALL,orderby=db.sm_invoice_head.client_name)
    
    #============================
    condStr="(cid = '"+c_id+"') AND (depot_id='"+depot_id+"') AND (store_id='"+store_id+"') AND (transaction_date <= '"+str(endDt)+"')"
    
    if out_st_delivery_man_id!='':
        condStr+=" AND (d_man_id='"+out_st_delivery_man_id+"')"        
    if out_st_territory_id!='':
        condStr+=" AND (area_id='"+out_st_territory_id+"')"        
    if out_st_mso_id!='':
        condStr+=" AND (rep_id='"+out_st_mso_id+"')"        
    if invoice_term!='':
        condStr+=" AND (payment_mode='"+invoice_term+"')"
    if customerId!='':
        condStr+=" AND (client_id='"+customerId+"')"
        
    if credit_type!='':
        condStr+=" AND (credit_note='"+credit_type+"')"
    if customer_cat!='':
        condStr+=" AND (cl_category_id='"+customer_cat+"')"
    if customer_sub_cat!='':
        condStr+=" AND (cl_sub_category_id='"+customer_sub_cat+"')"
        
    if out_st_level1_id!='':
        condStr+=" AND (level1_id='"+out_st_level1_id+"')"        
    if out_st_level2_id!='':
        condStr+=" AND (level2_id='"+out_st_level2_id+"')"
    
    totalRecords="SELECT depot_id,store_id,ROUND(SUM(trans_net_amt),2) as trans_net_amt, ROUND(SUM( tp_amt ),2) as tp_amt , ROUND(SUM( vat_amt ),2) as vat_amt , ROUND(SUM( disc_amt ),2) as disc_amt , ROUND(SUM( spdisc_amt ),2) as spdisc_amt , ROUND(SUM( adjust_amount ),2) as adjust_amount from sm_rpt_transaction WHERE ("+str(condStr)+") GROUP BY store_id"
    totalRecordList=db.executesql(totalRecords,as_dict = True)
    
    #====================    
    ostNet=0
    ostTp=0
    ostVat=0
    ostDisc=0
    ostSpDisc=0
    ostAdjust=0    
    for m in range(len(totalRecordList)):        
        ostNet=totalRecordList[m]['trans_net_amt']
        ostTp=totalRecordList[m]['tp_amt']
        ostVat=totalRecordList[m]['vat_amt']
        ostDisc=totalRecordList[m]['disc_amt']
        ostSpDisc=totalRecordList[m]['spdisc_amt']
        ostAdjust=totalRecordList[m]['adjust_amount']
        break
        
    try:
        percentTp=ostTp/ostNet*100
        percentVat=ostVat/ostNet*100
        percentDisc=ostDisc/ostNet*100
        percentSpDisc=ostSpDisc/ostNet*100
    except:
        percentTp=0
        percentVat=0
        percentDisc=0
        percentSpDisc=0
        
    #====================
#     p_totalInvTP=0
#     p_totalInvVat=0
#     p_totalInvDisc=0
#     p_totalInvSp=0
#     p_totalInvAmt=0
#     percentTp=0
#     percentVat=0
#     percentDisc=0
#     percentSpDisc=0
#     
#     for record in records:        
#         p_invTp=record.actual_total_tp-(record.return_tp+record.return_sp_discount)
#         p_invVat=record.vat_total_amount-record.return_vat
#         p_invDiscount=record.discount-record.return_discount
#         p_invSpDisc=record.sp_discount-record.return_sp_discount
#         p_invNetAmt=p_invTp+p_invVat-(p_invDiscount+p_invSpDisc)
#         
#         p_outstanding=round(p_invNetAmt-record.collection_amount,2)
#         if p_outstanding==0:
#             continue
#             
#         p_totalInvTP+=p_invTp
#         p_totalInvVat+=p_invVat
#         p_totalInvDisc+=p_invDiscount
#         p_totalInvSp+=p_invSpDisc
#         p_totalInvAmt+=p_invNetAmt
#         
#     try:
#         percentTp=p_totalInvTP/p_totalInvAmt*100
#         percentVat=p_totalInvVat/p_totalInvAmt*100
#         percentDisc=p_totalInvDisc/p_totalInvAmt*100
#         percentSpDisc=p_totalInvSp/p_totalInvAmt*100
#     except:
#         percentTp=0
#         percentVat=0
#         percentDisc=0
#         percentSpDisc=0
    #======================
    
    return dict(percentTp=percentTp,percentVat=percentVat,percentDisc=percentDisc,percentSpDisc=percentSpDisc,records=records,fromDate=startDt,toDate=endDt,depotID=depot_id,depotName=depot_name,storeID=store_id,storeName=store_name,deliveryManID=out_st_delivery_man_id,deliveryManName=out_st_delivery_man_name,territoryID=out_st_territory_id,territoryName=out_st_territory_name,msoID=out_st_mso_id,msoName=out_st_mso_name,invoice_term=invoice_term,customerId=customerId,customerName=customerName,credit_type=credit_type,customer_cat=customer_cat,customer_sub_cat=customer_sub_cat,catName=catName,subCatName=subCatName,out_st_level1_id=out_st_level1_id,out_st_level2_id=out_st_level2_id,page=page,items_per_page=items_per_page)    

def outStInvoiceWise_downlaod():
    c_id=session.cid
    
    currentDate=datetime.datetime.strptime(str(current_date),'%Y-%m-%d')
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    depot_id=str(request.vars.depotID).strip()
    store_id=str(request.vars.storeID).strip()
    out_st_delivery_man_id=str(request.vars.deliveryManID).strip()
    out_st_territory_id=str(request.vars.territoryID).strip()
    out_st_mso_id=str(request.vars.msoID).strip()
    invoice_term=str(request.vars.invoice_term).strip()
    customerId=str(request.vars.customerId).strip()
    
    credit_type=str(request.vars.credit_type).strip()
    customer_cat=str(request.vars.customer_cat).strip() 
    customer_sub_cat=str(request.vars.customer_sub_cat).strip()    
    
    out_st_level1_id=str(request.vars.out_st_level1_id).strip()  
    out_st_level2_id=str(request.vars.out_st_level2_id).strip()  
    
    catName=''
    custCatRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_CATEGORY')&(db.sm_category_type.cat_type_id==customer_cat)).select(db.sm_category_type.cat_type_name, limitby=(0,1))
    if custCatRows:
        catName=custCatRows[0].cat_type_name        
    subCatName=''
    custSubCatRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_SUB_CATEGORY')&(db.sm_category_type.cat_type_id==customer_sub_cat)).select(db.sm_category_type.cat_type_name, limitby=(0,1))
    if custSubCatRows:
        subCatName=custSubCatRows[0].cat_type_name
    
    depot_name=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depot_name=depotRow[0].name
    
    store_name=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        store_name=storeRow[0].store_name
        
    out_st_delivery_man_name=''
    dpRow=db((db.sm_delivery_man.cid==c_id)&(db.sm_delivery_man.depot_id==depot_id)&(db.sm_delivery_man.d_man_id==out_st_delivery_man_id)).select(db.sm_delivery_man.name,limitby=(0,1))
    if dpRow:
        out_st_delivery_man_name=dpRow[0].name
        
    out_st_territory_name=''
    levelRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==out_st_territory_id)).select(db.sm_level.level_name,limitby=(0,1))
    if levelRow:
        out_st_territory_name=levelRow[0].level_name
        
    out_st_mso_name=''
    repRow=db((db.sm_rep.cid==c_id)&(db.sm_rep.rep_id==out_st_mso_id)).select(db.sm_rep.name,limitby=(0,1))
    if repRow:
        out_st_mso_name=repRow[0].name
    
    customerName=''
    clientRow=db((db.sm_client.cid==c_id)&(db.sm_client.depot_id==depot_id)&(db.sm_client.client_id==customerId)).select(db.sm_client.name,limitby=(0,1))
    if clientRow:
        customerName=clientRow[0].name
        
    try:        
        startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d').strftime('%Y-%m-%d')
    except:
        startDt=''                
    
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d').strftime('%Y-%m-%d')
    
    #---------------end paging
    qset=db()
    qset=qset(db.sm_invoice_head.cid==c_id)
    
    if startDt!='' and startDt!=None:        
        qset=qset((db.sm_invoice_head.invoice_date>=startDt)&(db.sm_invoice_head.invoice_date<=endDt))
    else:
        qset=qset(db.sm_invoice_head.invoice_date<=endDt)
        
    qset=qset(db.sm_invoice_head.depot_id==depot_id)
    qset=qset(db.sm_invoice_head.store_id==store_id)
    qset=qset(db.sm_invoice_head.status=='Invoiced')    
    qset=qset((db.sm_invoice_head.total_amount-(db.sm_invoice_head.return_tp+db.sm_invoice_head.return_vat-db.sm_invoice_head.return_discount))-db.sm_invoice_head.collection_amount!=0)
    
    if out_st_delivery_man_id!='':
        qset=qset(db.sm_invoice_head.d_man_id==out_st_delivery_man_id)
    if out_st_territory_id!='':
        qset=qset(db.sm_invoice_head.area_id==out_st_territory_id)
    if out_st_mso_id!='':
        qset=qset(db.sm_invoice_head.rep_id==out_st_mso_id)
    if invoice_term!='':
        qset=qset(db.sm_invoice_head.payment_mode==invoice_term)
    if customerId!='':
        qset=qset(db.sm_invoice_head.client_id==customerId)
        
    if credit_type!='':
        qset=qset(db.sm_invoice_head.credit_note==credit_type)
    if customer_cat!='':
        qset=qset(db.sm_invoice_head.cl_category_id==customer_cat)
    if customer_sub_cat!='':
        qset=qset(db.sm_invoice_head.cl_sub_category_id==customer_sub_cat)
        
    if out_st_level1_id!='':
        qset=qset(db.sm_invoice_head.level1_id==out_st_level1_id)
    if out_st_level2_id!='':
        qset=qset(db.sm_invoice_head.level2_id==out_st_level2_id)
        
    records=qset.select(db.sm_invoice_head.ALL,orderby=db.sm_invoice_head.client_name)
    
    #============================
    condStr="(cid = '"+c_id+"') AND (depot_id='"+depot_id+"') AND (store_id='"+store_id+"') AND (transaction_date <= '"+str(endDt)+"')"
    
    if out_st_delivery_man_id!='':
        condStr+=" AND (d_man_id='"+out_st_delivery_man_id+"')"        
    if out_st_territory_id!='':
        condStr+=" AND (area_id='"+out_st_territory_id+"')"        
    if out_st_mso_id!='':
        condStr+=" AND (rep_id='"+out_st_mso_id+"')"        
    if invoice_term!='':
        condStr+=" AND (payment_mode='"+invoice_term+"')"
    if customerId!='':
        condStr+=" AND (client_id='"+customerId+"')"
        
    if credit_type!='':
        condStr+=" AND (credit_note='"+credit_type+"')"
    if customer_cat!='':
        condStr+=" AND (cl_category_id='"+customer_cat+"')"
    if customer_sub_cat!='':
        condStr+=" AND (cl_sub_category_id='"+customer_sub_cat+"')"
        
    if out_st_level1_id!='':
        condStr+=" AND (level1_id='"+out_st_level1_id+"')"        
    if out_st_level2_id!='':
        condStr+=" AND (level2_id='"+out_st_level2_id+"')"
    
    totalRecords="SELECT depot_id,store_id,ROUND(SUM(trans_net_amt),2) as trans_net_amt, ROUND(SUM( tp_amt ),2) as tp_amt , ROUND(SUM( vat_amt ),2) as vat_amt , ROUND(SUM( disc_amt ),2) as disc_amt , ROUND(SUM( spdisc_amt ),2) as spdisc_amt , ROUND(SUM( adjust_amount ),2) as adjust_amount from sm_rpt_transaction WHERE ("+str(condStr)+") GROUP BY store_id"
    totalRecordList=db.executesql(totalRecords,as_dict = True)
    
    #====================    
    ostNet=0
    ostTp=0
    ostVat=0
    ostDisc=0
    ostSpDisc=0
    ostAdjust=0    
    for m in range(len(totalRecordList)):        
        ostNet=totalRecordList[m]['trans_net_amt']
        ostTp=totalRecordList[m]['tp_amt']
        ostVat=totalRecordList[m]['vat_amt']
        ostDisc=totalRecordList[m]['disc_amt']
        ostSpDisc=totalRecordList[m]['spdisc_amt']
        ostAdjust=totalRecordList[m]['adjust_amount']
        break
        
    try:
        percentTp=ostTp/ostNet*100
        percentVat=ostVat/ostNet*100
        percentDisc=ostDisc/ostNet*100
        percentSpDisc=ostSpDisc/ostNet*100
    except:
        percentTp=0
        percentVat=0
        percentDisc=0
        percentSpDisc=0
        
    #====================
#     p_totalInvTP=0
#     p_totalInvVat=0
#     p_totalInvDisc=0
#     p_totalInvSp=0
#     p_totalInvAmt=0
#     percentTp=0
#     percentVat=0
#     percentDisc=0
#     percentSpDisc=0
#     
#     for record in records:        
#         p_invTp=record.actual_total_tp-(record.return_tp+record.return_sp_discount)
#         p_invVat=record.vat_total_amount-record.return_vat
#         p_invDiscount=record.discount-record.return_discount
#         p_invSpDisc=record.sp_discount-record.return_sp_discount
#         p_invNetAmt=p_invTp+p_invVat-(p_invDiscount+p_invSpDisc)
#         
#         p_outstanding=round(p_invNetAmt-record.collection_amount,2)
#         if p_outstanding==0:
#             continue
#             
#         p_totalInvTP+=p_invTp
#         p_totalInvVat+=p_invVat
#         p_totalInvDisc+=p_invDiscount
#         p_totalInvSp+=p_invSpDisc
#         p_totalInvAmt+=p_invNetAmt
#         
#     try:
#         percentTp=p_totalInvTP/p_totalInvAmt*100
#         percentVat=p_totalInvVat/p_totalInvAmt*100
#         percentDisc=p_totalInvDisc/p_totalInvAmt*100
#         percentSpDisc=p_totalInvSp/p_totalInvAmt*100
#     except:
#         percentTp=0
#         percentVat=0
#         percentDisc=0
#         percentSpDisc=0
    #======================
    
    myString='6.1 Invoice Wise Outstanding\n'
    myString+='Inv Date From:,'+str(startDt)+'\n'
    myString+='To/ as of Date:'+','+str(endDt)+'\n'
    myString+='Inv Term:,'+str(invoice_term)+'\n'
    myString+='Branch ID:,'+str(depot_id)+'\n'
    myString+='Branch Name'+','+str(depot_name)+'\n'
    myString+='Store ID:,'+str(store_id)+'\n'
    myString+='Store Name'+','+str(store_name)+'\n'
    myString+='DP ID:,'+str(out_st_delivery_man_id)+'\n'
    myString+='DP Name'+','+str(out_st_delivery_man_name)+'\n'
    myString+='Territory ID:,'+str(out_st_territory_id)+'\n'
    myString+='Territory Name'+','+str(out_st_territory_name)+'\n'
    myString+='MSO ID:,'+str(out_st_mso_id)+'\n'
    myString+='MSO Name'+','+str(out_st_mso_name)+'\n'
    myString+='Customer ID:,'+str(customerId)+'\n'
    myString+='Customer Name'+','+str(customerName)+'\n'
    
    myString+='Credit Type:,'+str(credit_type)+'\n'    
    if catName=='':
        catName='ALL'
    if subCatName=='':
        subCatName='ALL'        
    myString+='Customer Category'+','+str(catName)+'\n'
    myString+='Customer Sub-Category'+','+str(subCatName)+'\n'
    
    myString+=str(session.level1Name)+','+str(out_st_level1_id)+'\n'
    myString+=str(session.level2Name)+','+str(out_st_level2_id)+'\n'
    
    totalInvTP=0
    totalInvVat=0
    totalInvDisc=0
    totalInvAmt=0
    totalInvSp=0
    totalOutsTP=0
    totalOutsVat=0
    totalOutsDisc=0
    totalOutST=0
    totalOutSp=0
    
    sl=0
    myString+='SL,Date,Inv.No,Cust.ID,Cust.Name,Cust.Sub-Category ID,Cust.Sub-Category Name,MSO ID,MSO Name,DP ID,DP Name,Terms,Credit Type,Tr.Code,Market,Invoice-TP,Invoice-Vat,Invoice-Disc,Invoice-SP,Invoice-Net,Adjusted,Outstanding-TP,Outstanding-Vat,Outstanding-Disc,Outstanding-SP,Outstanding-Net,Aging,Oustanding%'+'\n'
    for row in records:
        
        depot_id=row.depot_id
        invoice_date=row.invoice_date
        invNo=str(session.prefix_invoice)+'INV'+str(depot_id)+'-'+str(row.sl)
        client_id=row.client_id
        client_name=str(row.client_name).replace(',', ' ')
        cl_sub_category_id=row.cl_sub_category_id
        cl_sub_category_name=str(row.cl_sub_category_name).replace(',', ' ')        
        rep_id=row.rep_id
        rep_name=str(row.rep_name).replace(',', ' ')
        d_man_id=row.d_man_id
        d_man_name=str(row.d_man_name).replace(',', ' ')
        payment_mode=row.payment_mode
        area_id=row.area_id
        market_name=str(row.market_name).replace(',', ' ')
        credit_note=row.credit_note
        
        invTp=row.actual_total_tp-(row.return_tp+row.return_sp_discount)
        invVat=row.vat_total_amount-row.return_vat
        invDiscount=row.discount-row.return_discount
        invSpDisc=row.sp_discount-row.return_sp_discount
        invNetAmt=invTp+invVat-(invDiscount+invSpDisc)
        
        adjust_amount=row.adjust_amount
        
        outstanding=round(invNetAmt-row.collection_amount,2)
        if outstanding==0:
            continue
        sl+=1
        try:
#             outTp=(invTp*outstanding)/invNetAmt
#             outVat=(invVat*outstanding)/invNetAmt
#             outDisc=(invDiscount*outstanding)/invNetAmt
#             outSp=(invSpDisc*outstanding)/invNetAmt
            
            outTp=outstanding*(percentTp/100)
            outVat=outstanding*(percentVat/100)
            outDisc=outstanding*(percentDisc/100)
            outSp=outstanding*(percentSpDisc/100)
            
        except:
            outTp=0
            outVat=0
            outDisc=0
            outSp=0
            
        totalInvTP+=invTp
        totalInvVat+=invVat
        totalInvDisc+=invDiscount
        totalInvSp+=invSpDisc
        totalInvAmt+=invNetAmt
        
        totalOutsTP+=outTp
        totalOutsVat+=outVat
        totalOutsDisc+=outDisc
        totalOutSp+=outSp
        totalOutST+=outstanding
        
        invoice_date=datetime.datetime.strptime(str(row.invoice_date),'%Y-%m-%d')
        agingDay=(currentDate-invoice_date).days
        
        if invNetAmt!=0:
            outstandingPercent=round((outstanding/invNetAmt*100),2)
        else:
            outstandingPercent=0
            
        #------------------------        
        myString+=str(sl)+','+str(invoice_date)+','+str(invNo)+','+str(client_id)+','+str(client_name)+','+str(cl_sub_category_id)+','+str(cl_sub_category_name)+','+str(rep_id)+','+str(rep_name)+','+str(d_man_id)+','+str(d_man_name)+','+str(payment_mode)+','+str(credit_note)+','+str(area_id)+','+str(market_name)+','+str(invTp)+','+\
        str(invVat)+','+str(invDiscount)+','+str(invSpDisc)+','+str(invNetAmt)+','+str(adjust_amount)+','+str(outTp)+','+str(outVat)+','+str(outDisc)+','+str(outSp)+','+str(outstanding)+','+\
        str(agingDay)+','+str(outstandingPercent)+'\n'
    
    myString+='\n\nSummary,,,,,,,,,,,,,,,,,,,,\n'
    
    myString+='Invoice TP,'+str(round(totalInvTP,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Invoice VAT,'+str(round(totalInvVat,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Invoice Discount,'+str(round(totalInvDisc,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Invoice SP.Disc,'+str(round(totalInvSp,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Invoice Net,'+str(round(totalInvAmt,2))+',,,,,,,,,,,,,,,,,,,\n\n'
    
#     try:
#         totalOutsTP=(totalInvTP*totalOutST)/totalInvAmt
#         totalOutsVat=(totalInvVat*totalOutST)/totalInvAmt
#         totalOutsDisc=(totalInvDisc*totalOutST)/totalInvAmt
#         totalOutSp=(totalInvSp*totalOutST)/totalInvAmt
#     except:
#         totalOutsTP=0
#         totalOutsVat=0
#         totalOutsDisc=0
#         totalOutSp=0
        
    myString+='Outstanding TP,'+str(round(totalOutsTP,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Outstanding VAT,'+str(round(totalOutsVat,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Outstanding Discount,'+str(round(totalOutsDisc,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Outstanding SP.Disc,'+str(round(totalOutSp,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Outstanding Net,'+str(round(totalOutST,2))+',,,,,,,,,,,,,,,,,,,\n'
    
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_invWiseOutstanding.csv'   
    return str(myString)
    
def outStInvoiceWise_AsOfDate():
    c_id=session.cid
    
    response.title='6.1 Outstanding Invoice Wise(As Of Date)'
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    depot_id=str(request.vars.depotID).strip()
    store_id=str(request.vars.storeID).strip()
    out_st_delivery_man_id=str(request.vars.deliveryManID).strip()
    out_st_territory_id=str(request.vars.territoryID).strip()
    out_st_mso_id=str(request.vars.msoID).strip()
    invoice_term=str(request.vars.invoice_term).strip()
    customerId=str(request.vars.customerId).strip()
    
    credit_type=str(request.vars.credit_type).strip()
    customer_cat=str(request.vars.customer_cat).strip() 
    customer_sub_cat=str(request.vars.customer_sub_cat).strip()  
    
    out_st_level1_id=str(request.vars.out_st_level1_id).strip()  
    out_st_level2_id=str(request.vars.out_st_level2_id).strip()  
    
    catName=''
    custCatRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_CATEGORY')&(db.sm_category_type.cat_type_id==customer_cat)).select(db.sm_category_type.cat_type_name, limitby=(0,1))
    if custCatRows:
        catName=custCatRows[0].cat_type_name        
    subCatName=''
    custSubCatRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_SUB_CATEGORY')&(db.sm_category_type.cat_type_id==customer_sub_cat)).select(db.sm_category_type.cat_type_name, limitby=(0,1))
    if custSubCatRows:
        subCatName=custSubCatRows[0].cat_type_name
    
    
    depot_name=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depot_name=depotRow[0].name
        
    store_name=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        store_name=storeRow[0].store_name
        
    out_st_delivery_man_name=''
    dpRow=db((db.sm_delivery_man.cid==c_id)&(db.sm_delivery_man.depot_id==depot_id)&(db.sm_delivery_man.d_man_id==out_st_delivery_man_id)).select(db.sm_delivery_man.name,limitby=(0,1))
    if dpRow:
        out_st_delivery_man_name=dpRow[0].name
        
    out_st_territory_name=''
    levelRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==out_st_territory_id)).select(db.sm_level.level_name,limitby=(0,1))
    if levelRow:
        out_st_territory_name=levelRow[0].level_name
        
    out_st_mso_name=''
    repRow=db((db.sm_rep.cid==c_id)&(db.sm_rep.rep_id==out_st_mso_id)).select(db.sm_rep.name,limitby=(0,1))
    if repRow:
        out_st_mso_name=repRow[0].name
        
    customerName=''
    clientRow=db((db.sm_client.cid==c_id)&(db.sm_client.depot_id==depot_id)&(db.sm_client.client_id==customerId)).select(db.sm_client.name,limitby=(0,1))
    if clientRow:
        customerName=clientRow[0].name
    
    startDt=''
    try:        
        endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d').strftime('%Y-%m-%d')
    except:
        endDt=''
        
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    
    qset=db()
    qset=qset(db.sm_report_as_of_date.cid==c_id)
    qset=qset(db.sm_report_as_of_date.depot_id==depot_id)
    qset=qset(db.sm_report_as_of_date.store_id==store_id)
    qset=qset(db.sm_report_as_of_date.report_date==endDt)
    
    qset=qset((db.sm_report_as_of_date.total_amount-(db.sm_report_as_of_date.return_tp+db.sm_report_as_of_date.return_vat-db.sm_report_as_of_date.return_discount))-db.sm_report_as_of_date.collection_amount!=0)
    
    if out_st_delivery_man_id!='':
        qset=qset(db.sm_report_as_of_date.d_man_id==out_st_delivery_man_id)
    if out_st_territory_id!='':
        qset=qset(db.sm_report_as_of_date.area_id==out_st_territory_id)
    if out_st_mso_id!='':
        qset=qset(db.sm_report_as_of_date.rep_id==out_st_mso_id)
    if invoice_term!='':
        qset=qset(db.sm_report_as_of_date.payment_mode==invoice_term)
    if customerId!='':
        qset=qset(db.sm_report_as_of_date.client_id==customerId)
        
    if credit_type!='':
        qset=qset(db.sm_report_as_of_date.credit_note==credit_type)
    if customer_cat!='':
        qset=qset(db.sm_report_as_of_date.cl_category_id==customer_cat)
    if customer_sub_cat!='':
        qset=qset(db.sm_report_as_of_date.cl_sub_category_id==customer_sub_cat)
        
    if out_st_level1_id!='':
        qset=qset(db.sm_report_as_of_date.level1_id==out_st_level1_id)
    if out_st_level2_id!='':
        qset=qset(db.sm_report_as_of_date.level2_id==out_st_level2_id)
        
    records=qset.select(db.sm_report_as_of_date.ALL,orderby=db.sm_report_as_of_date.client_name)
    
    process_date=''
    for rec in records:
        process_date=rec.process_date
        break
        
    #====================
    p_totalInvTP=0
    p_totalInvVat=0
    p_totalInvDisc=0
    p_totalInvSp=0
    p_totalInvAmt=0
    percentTp=0
    percentVat=0
    percentDisc=0
    percentSpDisc=0
    
    for record in records:        
        p_invTp=record.actual_total_tp-(record.return_tp+record.return_sp_discount)
        p_invVat=record.vat_total_amount-record.return_vat
        p_invDiscount=record.discount-record.return_discount
        p_invSpDisc=record.sp_discount-record.return_sp_discount
        p_invNetAmt=p_invTp+p_invVat-(p_invDiscount+p_invSpDisc)
        
        p_outstanding=round(p_invNetAmt-record.collection_amount,2)
        if p_outstanding==0:
            continue
            
        p_totalInvTP+=p_invTp
        p_totalInvVat+=p_invVat
        p_totalInvDisc+=p_invDiscount
        p_totalInvSp+=p_invSpDisc
        p_totalInvAmt+=p_invNetAmt
        
    try:
        percentTp=p_totalInvTP/p_totalInvAmt*100
        percentVat=p_totalInvVat/p_totalInvAmt*100
        percentDisc=p_totalInvDisc/p_totalInvAmt*100
        percentSpDisc=p_totalInvSp/p_totalInvAmt*100
    except:
        percentTp=0
        percentVat=0
        percentDisc=0
        percentSpDisc=0
    #======================
    
    return dict(percentTp=percentTp,percentVat=percentVat,percentDisc=percentDisc,percentSpDisc=percentSpDisc,process_date=process_date,records=records,fromDate=startDt,toDate=endDt,depotID=depot_id,depotName=depot_name,storeID=store_id,storeName=store_name,deliveryManID=out_st_delivery_man_id,deliveryManName=out_st_delivery_man_name,territoryID=out_st_territory_id,territoryName=out_st_territory_name,msoID=out_st_mso_id,msoName=out_st_mso_name,invoice_term=invoice_term,customerId=customerId,customerName=customerName,credit_type=credit_type,customer_cat=customer_cat,customer_sub_cat=customer_sub_cat,catName=catName,subCatName=subCatName,out_st_level1_id=out_st_level1_id,out_st_level2_id=out_st_level2_id,page=page,items_per_page=items_per_page)    

def outStInvoiceWise_AsOfDate_downlaod():
    c_id=session.cid
    
    currentDate=datetime.datetime.strptime(str(current_date),'%Y-%m-%d')
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    depot_id=str(request.vars.depotID).strip()
    store_id=str(request.vars.storeID).strip()
    out_st_delivery_man_id=str(request.vars.deliveryManID).strip()
    out_st_territory_id=str(request.vars.territoryID).strip()
    out_st_mso_id=str(request.vars.msoID).strip()
    invoice_term=str(request.vars.invoice_term).strip()
    customerId=str(request.vars.customerId).strip()
    
    credit_type=str(request.vars.credit_type).strip()
    customer_cat=str(request.vars.customer_cat).strip() 
    customer_sub_cat=str(request.vars.customer_sub_cat).strip()    
    
    out_st_level1_id=str(request.vars.out_st_level1_id).strip()  
    out_st_level2_id=str(request.vars.out_st_level2_id).strip()  
    
    catName=''
    custCatRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_CATEGORY')&(db.sm_category_type.cat_type_id==customer_cat)).select(db.sm_category_type.cat_type_name, limitby=(0,1))
    if custCatRows:
        catName=custCatRows[0].cat_type_name        
    subCatName=''
    custSubCatRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_SUB_CATEGORY')&(db.sm_category_type.cat_type_id==customer_sub_cat)).select(db.sm_category_type.cat_type_name, limitby=(0,1))
    if custSubCatRows:
        subCatName=custSubCatRows[0].cat_type_name
    
    depot_name=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depot_name=depotRow[0].name
    
    store_name=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        store_name=storeRow[0].store_name
        
    out_st_delivery_man_name=''
    dpRow=db((db.sm_delivery_man.cid==c_id)&(db.sm_delivery_man.depot_id==depot_id)&(db.sm_delivery_man.d_man_id==out_st_delivery_man_id)).select(db.sm_delivery_man.name,limitby=(0,1))
    if dpRow:
        out_st_delivery_man_name=dpRow[0].name
        
    out_st_territory_name=''
    levelRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==out_st_territory_id)).select(db.sm_level.level_name,limitby=(0,1))
    if levelRow:
        out_st_territory_name=levelRow[0].level_name
        
    out_st_mso_name=''
    repRow=db((db.sm_rep.cid==c_id)&(db.sm_rep.rep_id==out_st_mso_id)).select(db.sm_rep.name,limitby=(0,1))
    if repRow:
        out_st_mso_name=repRow[0].name
    
    customerName=''
    clientRow=db((db.sm_client.cid==c_id)&(db.sm_client.depot_id==depot_id)&(db.sm_client.client_id==customerId)).select(db.sm_client.name,limitby=(0,1))
    if clientRow:
        customerName=clientRow[0].name
        
    startDt=''
    try:        
        endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d').strftime('%Y-%m-%d')
    except:
        endDt=''
        
    #---------------end paging
    qset=db()
    qset=qset(db.sm_report_as_of_date.cid==c_id)
    qset=qset(db.sm_report_as_of_date.depot_id==depot_id)
    qset=qset(db.sm_report_as_of_date.store_id==store_id) 
    qset=qset(db.sm_report_as_of_date.report_date==endDt) 
    
    qset=qset((db.sm_report_as_of_date.total_amount-(db.sm_report_as_of_date.return_tp+db.sm_report_as_of_date.return_vat-db.sm_report_as_of_date.return_discount))-db.sm_report_as_of_date.collection_amount!=0)
    
    if out_st_delivery_man_id!='':
        qset=qset(db.sm_report_as_of_date.d_man_id==out_st_delivery_man_id)
    if out_st_territory_id!='':
        qset=qset(db.sm_report_as_of_date.area_id==out_st_territory_id)
    if out_st_mso_id!='':
        qset=qset(db.sm_report_as_of_date.rep_id==out_st_mso_id)
    if invoice_term!='':
        qset=qset(db.sm_report_as_of_date.payment_mode==invoice_term)
    if customerId!='':
        qset=qset(db.sm_report_as_of_date.client_id==customerId)
        
    if credit_type!='':
        qset=qset(db.sm_report_as_of_date.credit_note==credit_type)
    if customer_cat!='':
        qset=qset(db.sm_report_as_of_date.cl_category_id==customer_cat)
    if customer_sub_cat!='':
        qset=qset(db.sm_report_as_of_date.cl_sub_category_id==customer_sub_cat)
        
    if out_st_level1_id!='':
        qset=qset(db.sm_report_as_of_date.level1_id==out_st_level1_id)
    if out_st_level2_id!='':
        qset=qset(db.sm_report_as_of_date.level2_id==out_st_level2_id)
        
    records=qset.select(db.sm_report_as_of_date.ALL,orderby=db.sm_report_as_of_date.client_name)
    
    process_date=''
    for rec in records:
        process_date=rec.process_date
        break
    
    #====================
    p_totalInvTP=0
    p_totalInvVat=0
    p_totalInvDisc=0
    p_totalInvSp=0
    p_totalInvAmt=0
    percentTp=0
    percentVat=0
    percentDisc=0
    percentSpDisc=0
    
    for record in records:        
        p_invTp=record.actual_total_tp-(record.return_tp+record.return_sp_discount)
        p_invVat=record.vat_total_amount-record.return_vat
        p_invDiscount=record.discount-record.return_discount
        p_invSpDisc=record.sp_discount-record.return_sp_discount
        p_invNetAmt=p_invTp+p_invVat-(p_invDiscount+p_invSpDisc)
        
        p_outstanding=round(p_invNetAmt-record.collection_amount,2)
        if p_outstanding==0:
            continue
            
        p_totalInvTP+=p_invTp
        p_totalInvVat+=p_invVat
        p_totalInvDisc+=p_invDiscount
        p_totalInvSp+=p_invSpDisc
        p_totalInvAmt+=p_invNetAmt
        
    try:
        percentTp=p_totalInvTP/p_totalInvAmt*100
        percentVat=p_totalInvVat/p_totalInvAmt*100
        percentDisc=p_totalInvDisc/p_totalInvAmt*100
        percentSpDisc=p_totalInvSp/p_totalInvAmt*100
    except:
        percentTp=0
        percentVat=0
        percentDisc=0
        percentSpDisc=0
    #======================
    
    myString='6.1 Invoice Wise Outstanding (As Of Date)\n'    
    myString+='Date:'+','+str(endDt)+'\n'
    myString+='Time,'+str(process_date)[10:]+'\n'
    myString+='Inv Term:,'+str(invoice_term)+'\n'
    myString+='Branch ID:,'+str(depot_id)+'\n'
    myString+='Branch Name'+','+str(depot_name)+'\n'
    myString+='Store ID:,'+str(store_id)+'\n'
    myString+='Store Name'+','+str(store_name)+'\n'
    myString+='DP ID:,'+str(out_st_delivery_man_id)+'\n'
    myString+='DP Name'+','+str(out_st_delivery_man_name)+'\n'
    myString+='Territory ID:,'+str(out_st_territory_id)+'\n'
    myString+='Territory Name'+','+str(out_st_territory_name)+'\n'
    myString+='MSO ID:,'+str(out_st_mso_id)+'\n'
    myString+='MSO Name'+','+str(out_st_mso_name)+'\n'
    myString+='Customer ID:,'+str(customerId)+'\n'
    myString+='Customer Name'+','+str(customerName)+'\n'
    
    myString+='Credit Type:,'+str(credit_type)+'\n'    
    if catName=='':
        catName='ALL'
    if subCatName=='':
        subCatName='ALL'        
    myString+='Customer Category'+','+str(catName)+'\n'
    myString+='Customer Sub-Category'+','+str(subCatName)+'\n'
    
    myString+=str(session.level1Name)+','+str(out_st_level1_id)+'\n'
    myString+=str(session.level2Name)+','+str(out_st_level2_id)+'\n'
    
    
    
    totalInvTP=0
    totalInvVat=0
    totalInvDisc=0
    totalInvAmt=0
    totalInvSp=0
    totalOutsTP=0
    totalOutsVat=0
    totalOutsDisc=0
    totalOutST=0
    totalOutSp=0
    
    sl=0
    myString+='SL,Date,Inv.No,Cust.ID,Cust.Name,Cust.Sub-Category ID,Cust.Sub-Category Name,MSO ID,MSO Name,DP ID,DP Name,Terms,Tr.Code,Market,Invoice-TP,Invoice-Vat,Invoice-Disc,Invoice-SP,Invoice-Net,Adjusted,Outstanding-TP,Outstanding-Vat,Outstanding-Disc,Outstanding-SP,Outstanding-Net,Aging,Oustanding%'+'\n'
    for row in records:
        
        depot_id=row.depot_id
        invoice_date=row.invoice_date
        invNo=str(session.prefix_invoice)+'INV'+str(depot_id)+'-'+str(row.sl)
        client_id=row.client_id
        client_name=str(row.client_name).replace(',', ' ')
        cl_sub_category_id=row.cl_sub_category_id
        cl_sub_category_name=str(row.cl_sub_category_name).replace(',', ' ')        
        rep_id=row.rep_id
        rep_name=str(row.rep_name).replace(',', ' ')
        d_man_id=row.d_man_id
        d_man_name=str(row.d_man_name).replace(',', ' ')
        payment_mode=row.payment_mode
        area_id=row.area_id
        market_name=str(row.market_name).replace(',', ' ')
        
        invTp=row.actual_total_tp-(row.return_tp+row.return_sp_discount)
        invVat=row.vat_total_amount-row.return_vat
        invDiscount=row.discount-row.return_discount
        invSpDisc=row.sp_discount-row.return_sp_discount
        invNetAmt=invTp+invVat-(invDiscount+invSpDisc)
        
        adjust_amount=row.adjust_amount
        
        outstanding=round(invNetAmt-row.collection_amount,2)
        if outstanding==0:
            continue
        sl+=1
        try:
#             outTp=(invTp*outstanding)/invNetAmt
#             outVat=(invVat*outstanding)/invNetAmt
#             outDisc=(invDiscount*outstanding)/invNetAmt
#             outSp=(invSpDisc*outstanding)/invNetAmt
            
            outTp=outstanding*(percentTp/100)
            outVat=outstanding*(percentVat/100)
            outDisc=outstanding*(percentDisc/100)
            outSp=outstanding*(percentSpDisc/100)
            
        except:
            outTp=0
            outVat=0
            outDisc=0
            outSp=0
            
        totalInvTP+=invTp
        totalInvVat+=invVat
        totalInvDisc+=invDiscount
        totalInvSp+=invSpDisc
        totalInvAmt+=invNetAmt
        
        #totalOutsTP+=outTp
        #totalOutsVat+=outVat
        #totalOutsDisc+=outDisc
        #totalOutSp+=outSp
        totalOutST+=outstanding
        
        invoice_date=datetime.datetime.strptime(str(row.invoice_date),'%Y-%m-%d')
        agingDay=(currentDate-invoice_date).days
        
        if invNetAmt!=0:
            outstandingPercent=round((outstanding/invNetAmt*100),2)
        else:
            outstandingPercent=0
            
        #------------------------        
        myString+=str(sl)+','+str(invoice_date)+','+str(invNo)+','+str(client_id)+','+str(client_name)+','+str(cl_sub_category_id)+','+str(cl_sub_category_name)+','+str(rep_id)+','+str(rep_name)+','+str(d_man_id)+','+str(d_man_name)+','+str(payment_mode)+','+str(area_id)+','+str(market_name)+','+str(invTp)+','+\
        str(invVat)+','+str(invDiscount)+','+str(invSpDisc)+','+str(invNetAmt)+','+str(adjust_amount)+','+str(outTp)+','+str(outVat)+','+str(outDisc)+','+str(outSp)+','+str(outstanding)+','+\
        str(agingDay)+','+str(outstandingPercent)+'\n'
    
    myString+='\n\nSummary,,,,,,,,,,,,,,,,,,,,\n'
    
    myString+='Invoice TP,'+str(round(totalInvTP,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Invoice VAT,'+str(round(totalInvVat,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Invoice Discount,'+str(round(totalInvDisc,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Invoice SP.Disc,'+str(round(totalInvSp,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Invoice Net,'+str(round(totalInvAmt,2))+',,,,,,,,,,,,,,,,,,,\n\n'
    
    try:
        totalOutsTP=(totalInvTP*totalOutST)/totalInvAmt
        totalOutsVat=(totalInvVat*totalOutST)/totalInvAmt
        totalOutsDisc=(totalInvDisc*totalOutST)/totalInvAmt
        totalOutSp=(totalInvSp*totalOutST)/totalInvAmt
    except:
        totalOutsTP=0
        totalOutsVat=0
        totalOutsDisc=0
        totalOutSp=0
        
    myString+='Outstanding TP,'+str(round(totalOutsTP,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Outstanding VAT,'+str(round(totalOutsVat,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Outstanding Discount,'+str(round(totalOutsDisc,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Outstanding SP.Disc,'+str(round(totalOutSp,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Outstanding Net,'+str(round(totalOutST,2))+',,,,,,,,,,,,,,,,,,,\n'
    
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_invWiseOutstandingAsOfDate.csv'   
    return str(myString)
    

def outSt_summary_asOfDate_tr():
    c_id=session.cid
    
    response.title='Outstanding Summary (As Of Date)'
    
    toDate=request.vars.toDate
    
    depot_id=str(request.vars.depotID).strip()
    store_id=str(request.vars.storeID).strip()
    out_st_delivery_man_id=str(request.vars.deliveryManID).strip()
    out_st_territory_id=str(request.vars.territoryID).strip()
    out_st_mso_id=str(request.vars.msoID).strip()
    invoice_term=str(request.vars.invoice_term).strip()
    customerId=str(request.vars.customerId).strip()
    
    credit_type=str(request.vars.credit_type).strip()
    customer_cat=str(request.vars.customer_cat).strip() 
    customer_sub_cat=str(request.vars.customer_sub_cat).strip()  
    
    out_st_level1_id=str(request.vars.out_st_level1_id).strip()  
    out_st_level2_id=str(request.vars.out_st_level2_id).strip()  
    
    catName=''
    custCatRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_CATEGORY')&(db.sm_category_type.cat_type_id==customer_cat)).select(db.sm_category_type.cat_type_name, limitby=(0,1))
    if custCatRows:
        catName=custCatRows[0].cat_type_name        
    subCatName=''
    custSubCatRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_SUB_CATEGORY')&(db.sm_category_type.cat_type_id==customer_sub_cat)).select(db.sm_category_type.cat_type_name, limitby=(0,1))
    if custSubCatRows:
        subCatName=custSubCatRows[0].cat_type_name
        
    depot_name=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depot_name=depotRow[0].name
        
    store_name=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        store_name=storeRow[0].store_name
        
    out_st_delivery_man_name=''
    dpRow=db((db.sm_delivery_man.cid==c_id)&(db.sm_delivery_man.depot_id==depot_id)&(db.sm_delivery_man.d_man_id==out_st_delivery_man_id)).select(db.sm_delivery_man.name,limitby=(0,1))
    if dpRow:
        out_st_delivery_man_name=dpRow[0].name
        
    out_st_territory_name=''
    levelRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==out_st_territory_id)).select(db.sm_level.level_name,limitby=(0,1))
    if levelRow:
        out_st_territory_name=levelRow[0].level_name
        
    out_st_mso_name=''
    repRow=db((db.sm_rep.cid==c_id)&(db.sm_rep.rep_id==out_st_mso_id)).select(db.sm_rep.name,limitby=(0,1))
    if repRow:
        out_st_mso_name=repRow[0].name
        
    customerName=''
    clientRow=db((db.sm_client.cid==c_id)&(db.sm_client.depot_id==depot_id)&(db.sm_client.client_id==customerId)).select(db.sm_client.name,limitby=(0,1))
    if clientRow:
        customerName=clientRow[0].name
    
    startDt=''
    try:        
        endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d').strftime('%Y-%m-%d')
    except:
        endDt=''
        
    #--------------
    
    condStr="(cid = '"+c_id+"') AND (depot_id='"+depot_id+"') AND (store_id='"+store_id+"') AND (transaction_date <= '"+str(endDt)+"')"
    
    if out_st_delivery_man_id!='':
        condStr+=" AND (d_man_id='"+out_st_delivery_man_id+"')"        
    if out_st_territory_id!='':
        condStr+=" AND (area_id='"+out_st_territory_id+"')"        
    if out_st_mso_id!='':
        condStr+=" AND (rep_id='"+out_st_mso_id+"')"        
    if invoice_term!='':
        condStr+=" AND (payment_mode='"+invoice_term+"')"
    if customerId!='':
        condStr+=" AND (client_id='"+customerId+"')"
        
    if credit_type!='':
        condStr+=" AND (credit_note='"+credit_type+"')"
    if customer_cat!='':
        condStr+=" AND (cl_category_id='"+customer_cat+"')"
    if customer_sub_cat!='':
        condStr+=" AND (cl_sub_category_id='"+customer_sub_cat+"')"
        
    if out_st_level1_id!='':
        condStr+=" AND (level1_id='"+out_st_level1_id+"')"        
    if out_st_level2_id!='':
        condStr+=" AND (level2_id='"+out_st_level2_id+"')"
        
    invoiceRecords="SELECT depot_id,store_id,ROUND(SUM(trans_net_amt),2) as trans_net_amt, ROUND(SUM( tp_amt ),2) as tp_amt , ROUND(SUM( vat_amt ),2) as vat_amt , ROUND(SUM( disc_amt ),2) as disc_amt , ROUND(SUM( spdisc_amt ),2) as spdisc_amt , ROUND(SUM( adjust_amount ),2) as adjust_amount from sm_rpt_transaction WHERE ("+str(condStr)+" AND transaction_type ='INV') GROUP BY depot_id"
    invoiceRecordList=db.executesql(invoiceRecords,as_dict = True)
    
    returnRecords="SELECT depot_id,store_id,ROUND(SUM(trans_net_amt),2) as trans_net_amt, ROUND(SUM( tp_amt ),2) as tp_amt , ROUND(SUM( vat_amt ),2) as vat_amt , ROUND(SUM( disc_amt ),2) as disc_amt , ROUND(SUM( spdisc_amt ),2) as spdisc_amt , ROUND(SUM( adjust_amount ),2) as adjust_amount from sm_rpt_transaction WHERE ("+str(condStr)+" AND transaction_type like('RE%')) GROUP BY depot_id"
    returnRecordList=db.executesql(returnRecords,as_dict = True)
    
    paymentRecords="SELECT depot_id,store_id,ROUND(SUM(trans_net_amt),2) as trans_net_amt, ROUND(SUM( tp_amt ),2) as tp_amt , ROUND(SUM( vat_amt ),2) as vat_amt , ROUND(SUM( disc_amt ),2) as disc_amt , ROUND(SUM( spdisc_amt ),2) as spdisc_amt , ROUND(SUM( adjust_amount ),2) as adjust_amount from sm_rpt_transaction WHERE ("+str(condStr)+" AND transaction_type like('PAY%')) GROUP BY depot_id"
    paymentRecordList=db.executesql(paymentRecords,as_dict = True)
    
    totalRecords="SELECT depot_id,store_id,ROUND(SUM(trans_net_amt),2) as trans_net_amt, ROUND(SUM( tp_amt ),2) as tp_amt , ROUND(SUM( vat_amt ),2) as vat_amt , ROUND(SUM( disc_amt ),2) as disc_amt , ROUND(SUM( spdisc_amt ),2) as spdisc_amt , ROUND(SUM( adjust_amount ),2) as adjust_amount from sm_rpt_transaction WHERE ("+str(condStr)+") GROUP BY depot_id"
    recordList=db.executesql(totalRecords,as_dict = True)
    
    
    #return str(recordList)
    
    
    #====================
    invoiceNet=0
    invoiceTp=0
    invoiceVat=0
    invoiceDisc=0
    invoiceSpDisc=0
    
    retNet=0
    retTp=0
    retVat=0
    retDisc=0
    retSpDisc=0
    
    payNet=0
    payTp=0
    payVat=0
    payDisc=0
    paySpDisc=0
    payAdjust=0
    
    ostNet=0
    ostTp=0
    ostVat=0
    ostDisc=0
    ostSpDisc=0
    ostAdjust=0
    
    for i in range(len(invoiceRecordList)):        
        invoiceNet=invoiceRecordList[i]['trans_net_amt']
        invoiceTp=invoiceRecordList[i]['tp_amt']
        invoiceVat=invoiceRecordList[i]['vat_amt']
        invoiceDisc=invoiceRecordList[i]['disc_amt']
        invoiceSpDisc=invoiceRecordList[i]['spdisc_amt']
        break
    
    for j in range(len(returnRecordList)):        
        retNet=returnRecordList[j]['trans_net_amt']
        retTp=returnRecordList[j]['tp_amt']
        retVat=returnRecordList[j]['vat_amt']
        retDisc=returnRecordList[j]['disc_amt']
        retSpDisc=returnRecordList[j]['spdisc_amt']
        break
        
    for k in range(len(paymentRecordList)):        
        payNet=paymentRecordList[k]['trans_net_amt']
        payTp=paymentRecordList[k]['tp_amt']
        payVat=paymentRecordList[k]['vat_amt']
        payDisc=paymentRecordList[k]['disc_amt']
        paySpDisc=paymentRecordList[k]['spdisc_amt']
        payAdjust=paymentRecordList[k]['adjust_amount']
        break
        
    for m in range(len(recordList)):        
        ostNet=recordList[m]['trans_net_amt']
        ostTp=recordList[m]['tp_amt']
        ostVat=recordList[m]['vat_amt']
        ostDisc=recordList[m]['disc_amt']
        ostSpDisc=recordList[m]['spdisc_amt']
        ostAdjust=recordList[m]['adjust_amount']
        break
        
    return dict(invoiceNet=invoiceNet,invoiceTp=invoiceTp,invoiceVat=invoiceVat,invoiceDisc=invoiceDisc,invoiceSpDisc=invoiceSpDisc,retNet=retNet,retTp=retTp,retVat=retVat,retDisc=retDisc,retSpDisc=retSpDisc,payNet=payNet,payTp=payTp,payVat=payVat,payDisc=payDisc,paySpDisc=paySpDisc,payAdjust=payAdjust,ostNet=ostNet,ostTp=ostTp,ostVat=ostVat,ostDisc=ostDisc,ostSpDisc=ostSpDisc,ostAdjust=ostAdjust,toDate=endDt,depotID=depot_id,depotName=depot_name,storeID=store_id,storeName=store_name,deliveryManID=out_st_delivery_man_id,deliveryManName=out_st_delivery_man_name,territoryID=out_st_territory_id,territoryName=out_st_territory_name,msoID=out_st_mso_id,msoName=out_st_mso_name,invoice_term=invoice_term,customerId=customerId,customerName=customerName,credit_type=credit_type,customer_cat=customer_cat,customer_sub_cat=customer_sub_cat,catName=catName,subCatName=subCatName,out_st_level1_id=out_st_level1_id,out_st_level2_id=out_st_level2_id)    

def outSt_summary_asOfDate_tr_downlaod():
    c_id=session.cid
    
    currentDate=datetime.datetime.strptime(str(current_date),'%Y-%m-%d')
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    depot_id=str(request.vars.depotID).strip()
    store_id=str(request.vars.storeID).strip()
    out_st_delivery_man_id=str(request.vars.deliveryManID).strip()
    out_st_territory_id=str(request.vars.territoryID).strip()
    out_st_mso_id=str(request.vars.msoID).strip()
    invoice_term=str(request.vars.invoice_term).strip()
    customerId=str(request.vars.customerId).strip()
    
    credit_type=str(request.vars.credit_type).strip()
    customer_cat=str(request.vars.customer_cat).strip() 
    customer_sub_cat=str(request.vars.customer_sub_cat).strip()    
    
    out_st_level1_id=str(request.vars.out_st_level1_id).strip()  
    out_st_level2_id=str(request.vars.out_st_level2_id).strip()  
    
    catName=''
    custCatRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_CATEGORY')&(db.sm_category_type.cat_type_id==customer_cat)).select(db.sm_category_type.cat_type_name, limitby=(0,1))
    if custCatRows:
        catName=custCatRows[0].cat_type_name        
    subCatName=''
    custSubCatRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_SUB_CATEGORY')&(db.sm_category_type.cat_type_id==customer_sub_cat)).select(db.sm_category_type.cat_type_name, limitby=(0,1))
    if custSubCatRows:
        subCatName=custSubCatRows[0].cat_type_name
    
    depot_name=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depot_name=depotRow[0].name
    
    store_name=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        store_name=storeRow[0].store_name
        
    out_st_delivery_man_name=''
    dpRow=db((db.sm_delivery_man.cid==c_id)&(db.sm_delivery_man.depot_id==depot_id)&(db.sm_delivery_man.d_man_id==out_st_delivery_man_id)).select(db.sm_delivery_man.name,limitby=(0,1))
    if dpRow:
        out_st_delivery_man_name=dpRow[0].name
        
    out_st_territory_name=''
    levelRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==out_st_territory_id)).select(db.sm_level.level_name,limitby=(0,1))
    if levelRow:
        out_st_territory_name=levelRow[0].level_name
        
    out_st_mso_name=''
    repRow=db((db.sm_rep.cid==c_id)&(db.sm_rep.rep_id==out_st_mso_id)).select(db.sm_rep.name,limitby=(0,1))
    if repRow:
        out_st_mso_name=repRow[0].name
    
    customerName=''
    clientRow=db((db.sm_client.cid==c_id)&(db.sm_client.depot_id==depot_id)&(db.sm_client.client_id==customerId)).select(db.sm_client.name,limitby=(0,1))
    if clientRow:
        customerName=clientRow[0].name
        
    startDt=''
    try:        
        endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d').strftime('%Y-%m-%d')
    except:
        endDt=''
        
    #---------------end paging
    qset=db()
    qset=qset(db.sm_report_as_of_date.cid==c_id)
    qset=qset(db.sm_report_as_of_date.depot_id==depot_id)
    qset=qset(db.sm_report_as_of_date.store_id==store_id) 
    qset=qset(db.sm_report_as_of_date.report_date==endDt) 
    
    qset=qset((db.sm_report_as_of_date.total_amount-(db.sm_report_as_of_date.return_tp+db.sm_report_as_of_date.return_vat-db.sm_report_as_of_date.return_discount))-db.sm_report_as_of_date.collection_amount!=0)
    
    if out_st_delivery_man_id!='':
        qset=qset(db.sm_report_as_of_date.d_man_id==out_st_delivery_man_id)
    if out_st_territory_id!='':
        qset=qset(db.sm_report_as_of_date.area_id==out_st_territory_id)
    if out_st_mso_id!='':
        qset=qset(db.sm_report_as_of_date.rep_id==out_st_mso_id)
    if invoice_term!='':
        qset=qset(db.sm_report_as_of_date.payment_mode==invoice_term)
    if customerId!='':
        qset=qset(db.sm_report_as_of_date.client_id==customerId)
        
    if credit_type!='':
        qset=qset(db.sm_report_as_of_date.credit_note==credit_type)
    if customer_cat!='':
        qset=qset(db.sm_report_as_of_date.cl_category_id==customer_cat)
    if customer_sub_cat!='':
        qset=qset(db.sm_report_as_of_date.cl_sub_category_id==customer_sub_cat)
        
    if out_st_level1_id!='':
        qset=qset(db.sm_report_as_of_date.level1_id==out_st_level1_id)
    if out_st_level2_id!='':
        qset=qset(db.sm_report_as_of_date.level2_id==out_st_level2_id)
        
    records=qset.select(db.sm_report_as_of_date.ALL,orderby=db.sm_report_as_of_date.sl)
    
    process_date=''
    for rec in records:
        process_date=rec.process_date
        break
    
    #====================
    p_totalInvTP=0
    p_totalInvVat=0
    p_totalInvDisc=0
    p_totalInvSp=0
    p_totalInvAmt=0
    percentTp=0
    percentVat=0
    percentDisc=0
    percentSpDisc=0
    
    for record in records:        
        p_invTp=record.actual_total_tp-(record.return_tp+record.return_sp_discount)
        p_invVat=record.vat_total_amount-record.return_vat
        p_invDiscount=record.discount-record.return_discount
        p_invSpDisc=record.sp_discount-record.return_sp_discount
        p_invNetAmt=p_invTp+p_invVat-(p_invDiscount+p_invSpDisc)
        
        p_outstanding=round(p_invNetAmt-record.collection_amount,2)
        if p_outstanding==0:
            continue
            
        p_totalInvTP+=p_invTp
        p_totalInvVat+=p_invVat
        p_totalInvDisc+=p_invDiscount
        p_totalInvSp+=p_invSpDisc
        p_totalInvAmt+=p_invNetAmt
        
    try:
        percentTp=p_totalInvTP/p_totalInvAmt*100
        percentVat=p_totalInvVat/p_totalInvAmt*100
        percentDisc=p_totalInvDisc/p_totalInvAmt*100
        percentSpDisc=p_totalInvSp/p_totalInvAmt*100
    except:
        percentTp=0
        percentVat=0
        percentDisc=0
        percentSpDisc=0
    #======================
    
    myString='6.1 Invoice Wise Outstanding (As Of Date)\n'    
    myString+='Date:'+','+str(endDt)+'\n'
    myString+='Time,'+str(process_date)[10:]+'\n'
    myString+='Inv Term:,'+str(invoice_term)+'\n'
    myString+='Branch ID:,'+str(depot_id)+'\n'
    myString+='Branch Name'+','+str(depot_name)+'\n'
    myString+='Store ID:,'+str(store_id)+'\n'
    myString+='Store Name'+','+str(store_name)+'\n'
    myString+='DP ID:,'+str(out_st_delivery_man_id)+'\n'
    myString+='DP Name'+','+str(out_st_delivery_man_name)+'\n'
    myString+='Territory ID:,'+str(out_st_territory_id)+'\n'
    myString+='Territory Name'+','+str(out_st_territory_name)+'\n'
    myString+='MSO ID:,'+str(out_st_mso_id)+'\n'
    myString+='MSO Name'+','+str(out_st_mso_name)+'\n'
    myString+='Customer ID:,'+str(customerId)+'\n'
    myString+='Customer Name'+','+str(customerName)+'\n'
    
    myString+='Credit Type:,'+str(credit_type)+'\n'    
    if catName=='':
        catName='ALL'
    if subCatName=='':
        subCatName='ALL'        
    myString+='Customer Category'+','+str(catName)+'\n'
    myString+='Customer Sub-Category'+','+str(subCatName)+'\n'
    
    myString+=str(session.level1Name)+','+str(out_st_level1_id)+'\n'
    myString+=str(session.level2Name)+','+str(out_st_level2_id)+'\n'
    
    
    
    totalInvTP=0
    totalInvVat=0
    totalInvDisc=0
    totalInvAmt=0
    totalInvSp=0
    totalOutsTP=0
    totalOutsVat=0
    totalOutsDisc=0
    totalOutST=0
    totalOutSp=0
    
    sl=0
    myString+='SL,Date,Inv.No,Cust.ID,Cust.Name,Cust.Sub-Category ID,Cust.Sub-Category Name,MSO ID,MSO Name,DP ID,DP Name,Terms,Tr.Code,Market,Invoice-TP,Invoice-Vat,Invoice-Disc,Invoice-SP,Invoice-Net,Adjusted,Outstanding-TP,Outstanding-Vat,Outstanding-Disc,Outstanding-SP,Outstanding-Net,Aging,Oustanding%'+'\n'
    for row in records:
        
        depot_id=row.depot_id
        invoice_date=row.invoice_date
        invNo=str(session.prefix_invoice)+'INV'+str(depot_id)+'-'+str(row.sl)
        client_id=row.client_id
        client_name=str(row.client_name).replace(',', ' ')
        cl_sub_category_id=row.cl_sub_category_id
        cl_sub_category_name=str(row.cl_sub_category_name).replace(',', ' ')        
        rep_id=row.rep_id
        rep_name=str(row.rep_name).replace(',', ' ')
        d_man_id=row.d_man_id
        d_man_name=str(row.d_man_name).replace(',', ' ')
        payment_mode=row.payment_mode
        area_id=row.area_id
        market_name=str(row.market_name).replace(',', ' ')
        
        invTp=row.actual_total_tp-(row.return_tp+row.return_sp_discount)
        invVat=row.vat_total_amount-row.return_vat
        invDiscount=row.discount-row.return_discount
        invSpDisc=row.sp_discount-row.return_sp_discount
        invNetAmt=invTp+invVat-(invDiscount+invSpDisc)
        
        adjust_amount=row.adjust_amount
        
        outstanding=round(invNetAmt-row.collection_amount,2)
        if outstanding==0:
            continue
        sl+=1
        try:
#             outTp=(invTp*outstanding)/invNetAmt
#             outVat=(invVat*outstanding)/invNetAmt
#             outDisc=(invDiscount*outstanding)/invNetAmt
#             outSp=(invSpDisc*outstanding)/invNetAmt
            
            outTp=outstanding*(percentTp/100)
            outVat=outstanding*(percentVat/100)
            outDisc=outstanding*(percentDisc/100)
            outSp=outstanding*(percentSpDisc/100)
            
        except:
            outTp=0
            outVat=0
            outDisc=0
            outSp=0
            
        totalInvTP+=invTp
        totalInvVat+=invVat
        totalInvDisc+=invDiscount
        totalInvSp+=invSpDisc
        totalInvAmt+=invNetAmt
        
        #totalOutsTP+=outTp
        #totalOutsVat+=outVat
        #totalOutsDisc+=outDisc
        #totalOutSp+=outSp
        totalOutST+=outstanding
        
        invoice_date=datetime.datetime.strptime(str(row.invoice_date),'%Y-%m-%d')
        agingDay=(currentDate-invoice_date).days
        
        if invNetAmt!=0:
            outstandingPercent=round((outstanding/invNetAmt*100),2)
        else:
            outstandingPercent=0
            
        #------------------------        
        myString+=str(sl)+','+str(invoice_date)+','+str(invNo)+','+str(client_id)+','+str(client_name)+','+str(cl_sub_category_id)+','+str(cl_sub_category_name)+','+str(rep_id)+','+str(rep_name)+','+str(d_man_id)+','+str(d_man_name)+','+str(payment_mode)+','+str(area_id)+','+str(market_name)+','+str(invTp)+','+\
        str(invVat)+','+str(invDiscount)+','+str(invSpDisc)+','+str(invNetAmt)+','+str(adjust_amount)+','+str(outTp)+','+str(outVat)+','+str(outDisc)+','+str(outSp)+','+str(outstanding)+','+\
        str(agingDay)+','+str(outstandingPercent)+'\n'
    
    myString+='\n\nSummary,,,,,,,,,,,,,,,,,,,,\n'
    
    myString+='Invoice TP,'+str(round(totalInvTP,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Invoice VAT,'+str(round(totalInvVat,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Invoice Discount,'+str(round(totalInvDisc,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Invoice SP.Disc,'+str(round(totalInvSp,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Invoice Net,'+str(round(totalInvAmt,2))+',,,,,,,,,,,,,,,,,,,\n\n'
    
    try:
        totalOutsTP=(totalInvTP*totalOutST)/totalInvAmt
        totalOutsVat=(totalInvVat*totalOutST)/totalInvAmt
        totalOutsDisc=(totalInvDisc*totalOutST)/totalInvAmt
        totalOutSp=(totalInvSp*totalOutST)/totalInvAmt
    except:
        totalOutsTP=0
        totalOutsVat=0
        totalOutsDisc=0
        totalOutSp=0
        
    myString+='Outstanding TP,'+str(round(totalOutsTP,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Outstanding VAT,'+str(round(totalOutsVat,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Outstanding Discount,'+str(round(totalOutsDisc,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Outstanding SP.Disc,'+str(round(totalOutSp,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Outstanding Net,'+str(round(totalOutST,2))+',,,,,,,,,,,,,,,,,,,\n'
    
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_OutstandingAsOfDateSummary.csv'   
    return str(myString)


def outStInvoiceWise_AsOfDate_tr():
    c_id=session.cid
    
    response.title='6.1A Outstanding Invoice wise (As Of Date)'
    
    toDate=request.vars.toDate
    
    depot_id=str(request.vars.depotID).strip()
    store_id=str(request.vars.storeID).strip()
    out_st_delivery_man_id=str(request.vars.deliveryManID).strip()
    out_st_territory_id=str(request.vars.territoryID).strip()
    out_st_mso_id=str(request.vars.msoID).strip()
    invoice_term=str(request.vars.invoice_term).strip()
    customerId=str(request.vars.customerId).strip()
    
    credit_type=str(request.vars.credit_type).strip()
    customer_cat=str(request.vars.customer_cat).strip() 
    customer_sub_cat=str(request.vars.customer_sub_cat).strip()  
    
    out_st_level1_id=str(request.vars.out_st_level1_id).strip()  
    out_st_level2_id=str(request.vars.out_st_level2_id).strip()  
    
    catName=''
    custCatRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_CATEGORY')&(db.sm_category_type.cat_type_id==customer_cat)).select(db.sm_category_type.cat_type_name, limitby=(0,1))
    if custCatRows:
        catName=custCatRows[0].cat_type_name        
    subCatName=''
    custSubCatRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_SUB_CATEGORY')&(db.sm_category_type.cat_type_id==customer_sub_cat)).select(db.sm_category_type.cat_type_name, limitby=(0,1))
    if custSubCatRows:
        subCatName=custSubCatRows[0].cat_type_name
        
    depot_name=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depot_name=depotRow[0].name
        
    store_name=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        store_name=storeRow[0].store_name
        
    out_st_delivery_man_name=''
    dpRow=db((db.sm_delivery_man.cid==c_id)&(db.sm_delivery_man.depot_id==depot_id)&(db.sm_delivery_man.d_man_id==out_st_delivery_man_id)).select(db.sm_delivery_man.name,limitby=(0,1))
    if dpRow:
        out_st_delivery_man_name=dpRow[0].name
        
    out_st_territory_name=''
    levelRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==out_st_territory_id)).select(db.sm_level.level_name,limitby=(0,1))
    if levelRow:
        out_st_territory_name=levelRow[0].level_name
        
    out_st_mso_name=''
    repRow=db((db.sm_rep.cid==c_id)&(db.sm_rep.rep_id==out_st_mso_id)).select(db.sm_rep.name,limitby=(0,1))
    if repRow:
        out_st_mso_name=repRow[0].name
        
    customerName=''
    clientRow=db((db.sm_client.cid==c_id)&(db.sm_client.depot_id==depot_id)&(db.sm_client.client_id==customerId)).select(db.sm_client.name,limitby=(0,1))
    if clientRow:
        customerName=clientRow[0].name
    
    startDt=''
    try:        
        endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d').strftime('%Y-%m-%d')
    except:
        endDt=''
        
    #--------------
    
    condStr="(cid = '"+c_id+"') AND (depot_id='"+depot_id+"') AND (store_id='"+store_id+"') AND (transaction_date <= '"+str(endDt)+"')"
    
    if out_st_delivery_man_id!='':
        condStr+=" AND (d_man_id='"+out_st_delivery_man_id+"')"        
    if out_st_territory_id!='':
        condStr+=" AND (area_id='"+out_st_territory_id+"')"        
    if out_st_mso_id!='':
        condStr+=" AND (rep_id='"+out_st_mso_id+"')"        
    if invoice_term!='':
        condStr+=" AND (payment_mode='"+invoice_term+"')"
    if customerId!='':
        condStr+=" AND (client_id='"+customerId+"')"
        
    if credit_type!='':
        condStr+=" AND (credit_note='"+credit_type+"')"
    if customer_cat!='':
        condStr+=" AND (cl_category_id='"+customer_cat+"')"
    if customer_sub_cat!='':
        condStr+=" AND (cl_sub_category_id='"+customer_sub_cat+"')"
        
    if out_st_level1_id!='':
        condStr+=" AND (level1_id='"+out_st_level1_id+"')"        
    if out_st_level2_id!='':
        condStr+=" AND (level2_id='"+out_st_level2_id+"')"
        
    detailRecords="SELECT * from (SELECT cid, depot_id, depot_name, store_id, store_name, inv_rowid, inv_sl, invoice_date, transaction_date, ROUND(SUM(trans_net_amt),6) as trans_net_amt, ROUND(SUM( tp_amt ),6) as tp_amt , ROUND(SUM( vat_amt ),6) as vat_amt , ROUND(SUM( disc_amt ),6) as disc_amt , ROUND(SUM( spdisc_amt ),6) as spdisc_amt , ROUND(SUM( adjust_amount ),6) as adjust_amount , delivery_date, payment_mode, credit_note, client_id, client_name, cl_category_id, cl_category_name, cl_sub_category_id, cl_sub_category_name, client_limit_amt, rep_id, rep_name, market_id, market_name, d_man_id, d_man_name, level0_id, level0_name, level1_id, level1_name, level2_id, level2_name, area_id, area_name, shipment_no FROM sm_rpt_transaction WHERE ("+str(condStr)+") GROUP BY inv_rowid ORDER BY client_name) rptview WHERE rptview.trans_net_amt!=0"
    recordList=db.executesql(detailRecords,as_dict = True)    
    #====================
    
    totalRecords="SELECT depot_id,store_id,ROUND(SUM(trans_net_amt),2) as trans_net_amt, ROUND(SUM( tp_amt ),2) as tp_amt , ROUND(SUM( vat_amt ),2) as vat_amt , ROUND(SUM( disc_amt ),2) as disc_amt , ROUND(SUM( spdisc_amt ),2) as spdisc_amt , ROUND(SUM( adjust_amount ),2) as adjust_amount from sm_rpt_transaction WHERE ("+str(condStr)+") GROUP BY store_id"
    totalRecordList=db.executesql(totalRecords,as_dict = True)
    
    #=================
    salesNet=0
#     invoiceRecords="SELECT depot_id,store_id,ROUND(SUM(trans_net_amt),2) as trans_net_amt from sm_rpt_transaction WHERE ("+str(condStr)+" AND transaction_type ='INV') GROUP BY store_id"
#     invoiceRecordList=db.executesql(invoiceRecords,as_dict = True)
#     
#     returnRecords="SELECT depot_id,store_id,ROUND(SUM(trans_net_amt),2) as trans_net_amt from sm_rpt_transaction WHERE ("+str(condStr)+" AND transaction_type like('RE%')) GROUP BY store_id"
#     returnRecordList=db.executesql(returnRecords,as_dict = True)
#     
#     #====================
#     invoiceNet=0    
#     retNet=0    
#     for i in range(len(invoiceRecordList)):        
#         invoiceNet=invoiceRecordList[i]['trans_net_amt']        
#         break
#         
#     for j in range(len(returnRecordList)):        
#         retNet=returnRecordList[j]['trans_net_amt']        
#         break
#     
#     salesNet=invoiceNet-(retNet*(-1))
    
    #====================    
    ostNet=0
    ostTp=0
    ostVat=0
    ostDisc=0
    ostSpDisc=0
    ostAdjust=0    
    for m in range(len(totalRecordList)):        
        ostNet=totalRecordList[m]['trans_net_amt']
        ostTp=totalRecordList[m]['tp_amt']
        ostVat=totalRecordList[m]['vat_amt']
        ostDisc=totalRecordList[m]['disc_amt']
        ostSpDisc=totalRecordList[m]['spdisc_amt']
        ostAdjust=totalRecordList[m]['adjust_amount']
        break
        
    try:
        percentTp=ostTp/ostNet*100
        percentVat=ostVat/ostNet*100
        percentDisc=ostDisc/ostNet*100
        percentSpDisc=ostSpDisc/ostNet*100
    except:
        percentTp=0
        percentVat=0
        percentDisc=0
        percentSpDisc=0
        
    return dict(percentTp=percentTp,percentVat=percentVat,percentDisc=percentDisc,percentSpDisc=percentSpDisc,salesNet=salesNet,recordList=recordList,toDate=endDt,depotID=depot_id,depotName=depot_name,storeID=store_id,storeName=store_name,deliveryManID=out_st_delivery_man_id,deliveryManName=out_st_delivery_man_name,territoryID=out_st_territory_id,territoryName=out_st_territory_name,msoID=out_st_mso_id,msoName=out_st_mso_name,invoice_term=invoice_term,customerId=customerId,customerName=customerName,credit_type=credit_type,customer_cat=customer_cat,customer_sub_cat=customer_sub_cat,catName=catName,subCatName=subCatName,out_st_level1_id=out_st_level1_id,out_st_level2_id=out_st_level2_id)    

def outStInvoiceWise_AsOfDate_tr_downlaod():
    c_id=session.cid
    
    currentDate=datetime.datetime.strptime(str(current_date),'%Y-%m-%d')
    
    response.title='6.1A Outstanding Invoice wise (As Of Date)'
    
    toDate=request.vars.toDate
    
    depot_id=str(request.vars.depotID).strip()
    store_id=str(request.vars.storeID).strip()
    out_st_delivery_man_id=str(request.vars.deliveryManID).strip()
    out_st_territory_id=str(request.vars.territoryID).strip()
    out_st_mso_id=str(request.vars.msoID).strip()
    invoice_term=str(request.vars.invoice_term).strip()
    customerId=str(request.vars.customerId).strip()
    
    credit_type=str(request.vars.credit_type).strip()
    customer_cat=str(request.vars.customer_cat).strip() 
    customer_sub_cat=str(request.vars.customer_sub_cat).strip()  
    
    out_st_level1_id=str(request.vars.out_st_level1_id).strip()  
    out_st_level2_id=str(request.vars.out_st_level2_id).strip()  
    
    catName=''
    custCatRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_CATEGORY')&(db.sm_category_type.cat_type_id==customer_cat)).select(db.sm_category_type.cat_type_name, limitby=(0,1))
    if custCatRows:
        catName=custCatRows[0].cat_type_name        
    subCatName=''
    custSubCatRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_SUB_CATEGORY')&(db.sm_category_type.cat_type_id==customer_sub_cat)).select(db.sm_category_type.cat_type_name, limitby=(0,1))
    if custSubCatRows:
        subCatName=custSubCatRows[0].cat_type_name
        
    depot_name=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depot_name=depotRow[0].name
        
    store_name=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        store_name=storeRow[0].store_name
        
    out_st_delivery_man_name=''
    dpRow=db((db.sm_delivery_man.cid==c_id)&(db.sm_delivery_man.depot_id==depot_id)&(db.sm_delivery_man.d_man_id==out_st_delivery_man_id)).select(db.sm_delivery_man.name,limitby=(0,1))
    if dpRow:
        out_st_delivery_man_name=dpRow[0].name
        
    out_st_territory_name=''
    levelRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==out_st_territory_id)).select(db.sm_level.level_name,limitby=(0,1))
    if levelRow:
        out_st_territory_name=levelRow[0].level_name
        
    out_st_mso_name=''
    repRow=db((db.sm_rep.cid==c_id)&(db.sm_rep.rep_id==out_st_mso_id)).select(db.sm_rep.name,limitby=(0,1))
    if repRow:
        out_st_mso_name=repRow[0].name
        
    customerName=''
    clientRow=db((db.sm_client.cid==c_id)&(db.sm_client.depot_id==depot_id)&(db.sm_client.client_id==customerId)).select(db.sm_client.name,limitby=(0,1))
    if clientRow:
        customerName=clientRow[0].name
    
    startDt=''
    try:        
        endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d').strftime('%Y-%m-%d')
    except:
        endDt=''
        
    #--------------
    
    condStr="(cid = '"+c_id+"') AND (depot_id='"+depot_id+"') AND (store_id='"+store_id+"') AND (transaction_date <= '"+str(endDt)+"')"
    
    if out_st_delivery_man_id!='':
        condStr+=" AND (d_man_id='"+out_st_delivery_man_id+"')"        
    if out_st_territory_id!='':
        condStr+=" AND (area_id='"+out_st_territory_id+"')"        
    if out_st_mso_id!='':
        condStr+=" AND (rep_id='"+out_st_mso_id+"')"        
    if invoice_term!='':
        condStr+=" AND (payment_mode='"+invoice_term+"')"
    if customerId!='':
        condStr+=" AND (client_id='"+customerId+"')"
        
    if credit_type!='':
        condStr+=" AND (credit_note='"+credit_type+"')"
    if customer_cat!='':
        condStr+=" AND (cl_category_id='"+customer_cat+"')"
    if customer_sub_cat!='':
        condStr+=" AND (cl_sub_category_id='"+customer_sub_cat+"')"
        
    if out_st_level1_id!='':
        condStr+=" AND (level1_id='"+out_st_level1_id+"')"        
    if out_st_level2_id!='':
        condStr+=" AND (level2_id='"+out_st_level2_id+"')"
        
    detailRecords="SELECT * from (SELECT cid, depot_id, depot_name, store_id, store_name, inv_rowid, inv_sl, invoice_date, transaction_date, ROUND(SUM(trans_net_amt),6) as trans_net_amt, ROUND(SUM( tp_amt ),6) as tp_amt , ROUND(SUM( vat_amt ),6) as vat_amt , ROUND(SUM( disc_amt ),6) as disc_amt , ROUND(SUM( spdisc_amt ),6) as spdisc_amt , ROUND(SUM( adjust_amount ),6) as adjust_amount , delivery_date, payment_mode, credit_note, client_id, client_name, cl_category_id, cl_category_name, cl_sub_category_id, cl_sub_category_name, client_limit_amt, rep_id, rep_name, market_id, market_name, d_man_id, d_man_name, level0_id, level0_name, level1_id, level1_name, level2_id, level2_name, area_id, area_name, shipment_no FROM sm_rpt_transaction WHERE ("+str(condStr)+") GROUP BY inv_rowid ORDER BY client_name) rptview WHERE rptview.trans_net_amt!=0"
    recordList=db.executesql(detailRecords,as_dict = True)    
    #====================
    
    totalRecords="SELECT depot_id,store_id,ROUND(SUM(trans_net_amt),2) as trans_net_amt, ROUND(SUM( tp_amt ),2) as tp_amt , ROUND(SUM( vat_amt ),2) as vat_amt , ROUND(SUM( disc_amt ),2) as disc_amt , ROUND(SUM( spdisc_amt ),2) as spdisc_amt , ROUND(SUM( adjust_amount ),2) as adjust_amount from sm_rpt_transaction WHERE ("+str(condStr)+") GROUP BY store_id"
    totalRecordList=db.executesql(totalRecords,as_dict = True)
    
    #====================    
    ostNet=0
    ostTp=0
    ostVat=0
    ostDisc=0
    ostSpDisc=0
    ostAdjust=0    
    for m in range(len(totalRecordList)):        
        ostNet=totalRecordList[m]['trans_net_amt']
        ostTp=totalRecordList[m]['tp_amt']
        ostVat=totalRecordList[m]['vat_amt']
        ostDisc=totalRecordList[m]['disc_amt']
        ostSpDisc=totalRecordList[m]['spdisc_amt']
        ostAdjust=totalRecordList[m]['adjust_amount']
        break
        
    try:
        percentTp=ostTp/ostNet*100
        percentVat=ostVat/ostNet*100
        percentDisc=ostDisc/ostNet*100
        percentSpDisc=ostSpDisc/ostNet*100
    except:
        percentTp=0
        percentVat=0
        percentDisc=0
        percentSpDisc=0
    #======================
    
    myString='6.1A Invoice Wise Outstanding (As Of Date)\n'    
    myString+='Date:'+','+str(endDt)+'\n'    
    myString+='Inv Term:,'+str(invoice_term)+'\n'
    myString+='Branch ID:,'+str(depot_id)+'\n'
    myString+='Branch Name'+','+str(depot_name)+'\n'
    myString+='Store ID:,'+str(store_id)+'\n'
    myString+='Store Name'+','+str(store_name)+'\n'
    myString+='DP ID:,'+str(out_st_delivery_man_id)+'\n'
    myString+='DP Name'+','+str(out_st_delivery_man_name)+'\n'
    myString+='Territory ID:,'+str(out_st_territory_id)+'\n'
    myString+='Territory Name'+','+str(out_st_territory_name)+'\n'
    myString+='MSO ID:,'+str(out_st_mso_id)+'\n'
    myString+='MSO Name'+','+str(out_st_mso_name)+'\n'
    myString+='Customer ID:,'+str(customerId)+'\n'
    myString+='Customer Name'+','+str(customerName)+'\n'
    
    myString+='Credit Type:,'+str(credit_type)+'\n'    
    if catName=='':
        catName='ALL'
    if subCatName=='':
        subCatName='ALL'        
    myString+='Customer Category'+','+str(catName)+'\n'
    myString+='Customer Sub-Category'+','+str(subCatName)+'\n'
    
    myString+=str(session.level1Name)+','+str(out_st_level1_id)+'\n'
    myString+=str(session.level2Name)+','+str(out_st_level2_id)+'\n'
    
    totalInvTP=0
    totalInvVat=0
    totalInvDisc=0
    totalInvAmt=0
    totalInvSp=0
    totalOutsTP=0
    totalOutsVat=0
    totalOutsDisc=0
    totalOutST=0
    totalOutSp=0
    
    sl=0
    myString+='SL,Date,Inv.No,Cust.ID,Cust.Name,Cust.Sub-Category ID,Cust.Sub-Category Name,MSO ID,MSO Name,DP ID,DP Name,Terms,Credit Type,Tr.Code,Market,Outstanding-TP,Outstanding-Vat,Outstanding-Disc,Outstanding-SP,Outstanding-Net,Aging'+'\n'
    
    for i in range(len(recordList)):
        
        dictData=recordList[i]
        
        depot_id=dictData['depot_id']
        invoice_date=dictData['invoice_date']
        invNo=str(session.prefix_invoice)+'INV'+str(depot_id)+'-'+str(dictData['inv_sl'])
        client_id=dictData['client_id']
        client_name=str(dictData['client_name']).replace(',', ' ')
        cl_sub_category_id=dictData['cl_sub_category_id']
        cl_sub_category_name=str(dictData['cl_sub_category_name']).replace(',', ' ')        
        rep_id=dictData['rep_id']
        rep_name=str(dictData['rep_name']).replace(',', ' ')
        d_man_id=dictData['d_man_id']
        d_man_name=str(dictData['d_man_name']).replace(',', ' ')
        payment_mode=dictData['payment_mode']
        area_id=dictData['area_id']
        market_name=str(dictData['market_name']).replace(',', ' ')
        credit_note=dictData['credit_note']
        
        outstanding=round(dictData['trans_net_amt'],2)    
        
        if outstanding==0:
            continue;
        
        try:
            outTp=outstanding*(percentTp/100)
            outVat=outstanding*(percentVat/100)
            outDisc=outstanding*(percentDisc/100)
            outSp=outstanding*(percentSpDisc/100)
        except:
            outTp=0
            outVat=0
            outDisc=0
            outSp=0
            
        totalOutsTP+=outTp
        totalOutsVat+=outVat
        totalOutsDisc+=outDisc
        totalOutSp+=outSp
        totalOutST+=outstanding
        
        invoice_date=datetime.datetime.strptime(str(invoice_date),'%Y-%m-%d')
        agingDay=(currentDate-invoice_date).days
        
        #------------------------        
        myString+=str(sl)+','+str(invoice_date)+','+str(invNo)+','+str(client_id)+','+str(client_name)+','+str(cl_sub_category_id)+','+str(cl_sub_category_name)+','+str(rep_id)+','+str(rep_name)+','+str(d_man_id)+','+str(d_man_name)+','+str(payment_mode)+','+str(credit_note)+','+str(area_id)+','+str(market_name)+','+str(outTp)+','+str(outVat)+','+str(outDisc)+','+str(outSp)+','+str(outstanding)+','+\
        str(agingDay)+'\n'
    
    myString+='\n\nSummary,,,,,,,,,,,,,,,,,,,,\n'
    
        
    myString+='Outstanding TP,'+str(round(totalOutsTP,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Outstanding VAT,'+str(round(totalOutsVat,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Outstanding Discount,'+str(round(totalOutsDisc,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Outstanding SP.Disc,'+str(round(totalOutSp,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Outstanding Net,'+str(round(totalOutST,2))+',,,,,,,,,,,,,,,,,,,\n'
    
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_invWiseOutstandingAsOfDate.csv'   
    return str(myString)

def outStInvoiceWise_AsOfDate_bak():
    c_id=session.cid
    
    response.title='6.1 Outstanding Invoice Wise(As Of Date)'
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    depot_id=str(request.vars.depotID).strip()
    store_id=str(request.vars.storeID).strip()
    out_st_delivery_man_id=str(request.vars.deliveryManID).strip()
    out_st_territory_id=str(request.vars.territoryID).strip()
    out_st_mso_id=str(request.vars.msoID).strip()
    invoice_term=str(request.vars.invoice_term).strip()
    customerId=str(request.vars.customerId).strip()
    
    credit_type=str(request.vars.credit_type).strip()
    customer_cat=str(request.vars.customer_cat).strip() 
    customer_sub_cat=str(request.vars.customer_sub_cat).strip()  
    
    out_st_level1_id=str(request.vars.out_st_level1_id).strip()  
    out_st_level2_id=str(request.vars.out_st_level2_id).strip()  
    
    catName=''
    custCatRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_CATEGORY')&(db.sm_category_type.cat_type_id==customer_cat)).select(db.sm_category_type.cat_type_name, limitby=(0,1))
    if custCatRows:
        catName=custCatRows[0].cat_type_name        
    subCatName=''
    custSubCatRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_SUB_CATEGORY')&(db.sm_category_type.cat_type_id==customer_sub_cat)).select(db.sm_category_type.cat_type_name, limitby=(0,1))
    if custSubCatRows:
        subCatName=custSubCatRows[0].cat_type_name
        
    depot_name=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depot_name=depotRow[0].name
        
    store_name=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        store_name=storeRow[0].store_name
        
    out_st_delivery_man_name=''
    dpRow=db((db.sm_delivery_man.cid==c_id)&(db.sm_delivery_man.depot_id==depot_id)&(db.sm_delivery_man.d_man_id==out_st_delivery_man_id)).select(db.sm_delivery_man.name,limitby=(0,1))
    if dpRow:
        out_st_delivery_man_name=dpRow[0].name
        
    out_st_territory_name=''
    levelRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==out_st_territory_id)).select(db.sm_level.level_name,limitby=(0,1))
    if levelRow:
        out_st_territory_name=levelRow[0].level_name
        
    out_st_mso_name=''
    repRow=db((db.sm_rep.cid==c_id)&(db.sm_rep.rep_id==out_st_mso_id)).select(db.sm_rep.name,limitby=(0,1))
    if repRow:
        out_st_mso_name=repRow[0].name
        
    customerName=''
    clientRow=db((db.sm_client.cid==c_id)&(db.sm_client.depot_id==depot_id)&(db.sm_client.client_id==customerId)).select(db.sm_client.name,limitby=(0,1))
    if clientRow:
        customerName=clientRow[0].name
        
    try:        
        startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d').strftime('%Y-%m-%d')
    except:
        startDt=''                
    
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d').strftime('%Y-%m-%d')
    
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    
    #------------- Invoice
    qset=db()
    qset=qset(db.sm_invoice_head.cid==c_id)
    qset=qset(db.sm_invoice_head.depot_id==depot_id)
    qset=qset(db.sm_invoice_head.store_id==store_id)
    qset=qset(db.sm_invoice_head.status=='Invoiced')
    qset=qset(db.sm_invoice_head.invoice_date<=endDt)
    
    if out_st_delivery_man_id!='':
        qset=qset(db.sm_invoice_head.d_man_id==out_st_delivery_man_id)
    if out_st_territory_id!='':
        qset=qset(db.sm_invoice_head.area_id==out_st_territory_id)
    if out_st_mso_id!='':
        qset=qset(db.sm_invoice_head.rep_id==out_st_mso_id)
    if invoice_term!='':
        qset=qset(db.sm_invoice_head.payment_mode==invoice_term)
    if customerId!='':
        qset=qset(db.sm_invoice_head.client_id==customerId)
        
    if credit_type!='':
        qset=qset(db.sm_invoice_head.credit_note==credit_type)
    if customer_cat!='':
        qset=qset(db.sm_invoice_head.cl_category_id==customer_cat)
    if customer_sub_cat!='':
        qset=qset(db.sm_invoice_head.cl_sub_category_id==customer_sub_cat)
        
    if out_st_level1_id!='':
        qset=qset(db.sm_invoice_head.level1_id==out_st_level1_id)
    if out_st_level2_id!='':
        qset=qset(db.sm_invoice_head.level2_id==out_st_level2_id)
        
    records=qset.select(db.sm_invoice_head.ALL,orderby=db.sm_invoice_head.sl)
        
    #---------- Collection
    qset2=db()
    qset2=qset2(db.sm_payment_collection.cid==c_id)
    qset2=qset2(db.sm_payment_collection.depot_id==depot_id)
    qset2=qset2(db.sm_payment_collection.store_id==store_id)
    qset2=qset2(db.sm_payment_collection.status=='Posted')
    qset2=qset2(db.sm_payment_collection.collection_date<=endDt)    
    
    if out_st_delivery_man_id!='':
        qset2=qset2(db.sm_payment_collection.d_man_id==out_st_delivery_man_id)
    if out_st_territory_id!='':
        qset2=qset2(db.sm_payment_collection.area_id==out_st_territory_id)
    if out_st_mso_id!='':
        qset2=qset2(db.sm_payment_collection.rep_id==out_st_mso_id)
    if invoice_term!='':
        qset2=qset2(db.sm_payment_collection.payment_mode==invoice_term)
    if customerId!='':
        qset2=qset2(db.sm_payment_collection.client_id==customerId)
        
    if credit_type!='':
        qset2=qset2(db.sm_payment_collection.credit_note==credit_type)
    if customer_cat!='':
        qset2=qset2(db.sm_payment_collection.cl_category_id==customer_cat)
    if customer_sub_cat!='':
        qset2=qset2(db.sm_payment_collection.cl_sub_category_id==customer_sub_cat)
        
    if out_st_level1_id!='':
        qset2=qset2(db.sm_payment_collection.level1_id==out_st_level1_id)
    if out_st_level2_id!='':
        qset2=qset2(db.sm_payment_collection.level2_id==out_st_level2_id)
        
    #--------------------
    collectionList=[]
    transactionCause1=['','COLLECTION ERROR','ENTRY ERROR']
    qset2A=qset2(db.sm_payment_collection.transaction_cause.belongs(transactionCause1))
    records2A=qset2A.select(db.sm_payment_collection.head_rowid,db.sm_payment_collection.collection_amount.sum(),groupby=db.sm_payment_collection.head_rowid,orderby=db.sm_payment_collection.head_rowid)
    for rec2A in records2A:
        head_rowid=rec2A.sm_payment_collection.head_rowid
        collection_amount=float(rec2A[db.sm_payment_collection.collection_amount.sum()])
        collectionList.append({'headId':head_rowid,'collectionAmt':collection_amount,'adjustAmt':0})
        
    #--------------------
    adjustmentList=[]
    transactionCause2=['VAT AIT','RETURN GOODS','BAD DEBTS']
    qset2B=qset2(db.sm_payment_collection.transaction_cause.belongs(transactionCause2))
    records2B=qset2B.select(db.sm_payment_collection.head_rowid,db.sm_payment_collection.collection_amount.sum(),groupby=db.sm_payment_collection.head_rowid,orderby=db.sm_payment_collection.head_rowid)
        
    for rec2B in records2B:
        head_rowid=rec2B.sm_payment_collection.head_rowid
        adjust_amount=float(rec2B[db.sm_payment_collection.collection_amount.sum()])
        
        index2=-1
        try:
            index2=str(map(itemgetter('headId'), collectionList).index(head_rowid))    
        except:
            index2=-1
            
        if (index2!=-1):
            dictData2=collectionList[int(index2)]            
            dictData2['adjustAmt']=adjust_amount
        else:
            adjustmentList.append({'headId':head_rowid,'collectionAmt':0,'adjustAmt':adjust_amount})
            
    collectionAdjustList=[]
    collectionAdjustList=collectionList+adjustmentList
    
    #====================
    p_collectionAdjustList=[]
    p_collectionAdjustList=collectionList+adjustmentList
    
    p_totalInvTP=0
    p_totalInvVat=0
    p_totalInvDisc=0
    p_totalInvSp=0
    p_totalInvAmt=0
    percentTp=0
    percentVat=0
    percentDisc=0
    percentSpDisc=0
    
    for record in records:
        p_headId=record.id
        p_invTp=record.actual_total_tp-(record.return_tp+record.return_sp_discount)
        p_invVat=record.vat_total_amount-record.return_vat
        p_invDiscount=record.discount-record.return_discount
        p_invSpDisc=record.sp_discount-record.return_sp_discount
        p_invNetAmt=p_invTp+p_invVat-(p_invDiscount+p_invSpDisc)
        
        #       <!--collection and adjustment data-->
        collection_amount=0
        adjust_amount=0
        
        list_index=-1
        try:
            list_index=str(map(itemgetter('headId'), p_collectionAdjustList).index(p_headId)) 
        except:
            list_index=-1
        
        if (list_index!=-1):
            listDictData=p_collectionAdjustList[int(list_index)]        
            collection_amount=float(listDictData['collectionAmt'])
            adjust_amount=float(listDictData['adjustAmt'])
            
            del p_collectionAdjustList[int(list_index)]
        
       #<!--end collection and adjustment data-->
        
        p_outstanding=round(p_invNetAmt-(collection_amount+adjust_amount),2)
        if p_outstanding==0:
            continue
            
        p_totalInvTP+=p_invTp
        p_totalInvVat+=p_invVat
        p_totalInvDisc+=p_invDiscount
        p_totalInvSp+=p_invSpDisc
        p_totalInvAmt+=p_invNetAmt
    
    #----------- 
    try:
        percentTp=p_totalInvTP/p_totalInvAmt*100
        percentVat=p_totalInvVat/p_totalInvAmt*100
        percentDisc=p_totalInvDisc/p_totalInvAmt*100
        percentSpDisc=p_totalInvSp/p_totalInvAmt*100
    except:
        percentTp=0
        percentVat=0
        percentDisc=0
        percentSpDisc=0
    #======================
    
    return dict(percentTp=percentTp,percentVat=percentVat,percentDisc=percentDisc,percentSpDisc=percentSpDisc,records=records,collectionAdjustList=collectionAdjustList,fromDate=startDt,toDate=endDt,depotID=depot_id,depotName=depot_name,storeID=store_id,storeName=store_name,deliveryManID=out_st_delivery_man_id,deliveryManName=out_st_delivery_man_name,territoryID=out_st_territory_id,territoryName=out_st_territory_name,msoID=out_st_mso_id,msoName=out_st_mso_name,invoice_term=invoice_term,customerId=customerId,customerName=customerName,credit_type=credit_type,customer_cat=customer_cat,customer_sub_cat=customer_sub_cat,catName=catName,subCatName=subCatName,out_st_level1_id=out_st_level1_id,out_st_level2_id=out_st_level2_id,page=page,items_per_page=items_per_page)    
    

def outStInvoiceWise_AsOfDate_downlaod_bak():
    c_id=session.cid
    
    currentDate=datetime.datetime.strptime(str(current_date),'%Y-%m-%d')
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    depot_id=str(request.vars.depotID).strip()
    store_id=str(request.vars.storeID).strip()
    out_st_delivery_man_id=str(request.vars.deliveryManID).strip()
    out_st_territory_id=str(request.vars.territoryID).strip()
    out_st_mso_id=str(request.vars.msoID).strip()
    invoice_term=str(request.vars.invoice_term).strip()
    customerId=str(request.vars.customerId).strip()
    
    credit_type=str(request.vars.credit_type).strip()
    customer_cat=str(request.vars.customer_cat).strip() 
    customer_sub_cat=str(request.vars.customer_sub_cat).strip()    
    
    out_st_level1_id=str(request.vars.out_st_level1_id).strip()  
    out_st_level2_id=str(request.vars.out_st_level2_id).strip()  
    
    catName=''
    custCatRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_CATEGORY')&(db.sm_category_type.cat_type_id==customer_cat)).select(db.sm_category_type.cat_type_name, limitby=(0,1))
    if custCatRows:
        catName=custCatRows[0].cat_type_name        
    subCatName=''
    custSubCatRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_SUB_CATEGORY')&(db.sm_category_type.cat_type_id==customer_sub_cat)).select(db.sm_category_type.cat_type_name, limitby=(0,1))
    if custSubCatRows:
        subCatName=custSubCatRows[0].cat_type_name
    
    depot_name=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depot_name=depotRow[0].name
    
    store_name=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        store_name=storeRow[0].store_name
        
    out_st_delivery_man_name=''
    dpRow=db((db.sm_delivery_man.cid==c_id)&(db.sm_delivery_man.depot_id==depot_id)&(db.sm_delivery_man.d_man_id==out_st_delivery_man_id)).select(db.sm_delivery_man.name,limitby=(0,1))
    if dpRow:
        out_st_delivery_man_name=dpRow[0].name
        
    out_st_territory_name=''
    levelRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==out_st_territory_id)).select(db.sm_level.level_name,limitby=(0,1))
    if levelRow:
        out_st_territory_name=levelRow[0].level_name
        
    out_st_mso_name=''
    repRow=db((db.sm_rep.cid==c_id)&(db.sm_rep.rep_id==out_st_mso_id)).select(db.sm_rep.name,limitby=(0,1))
    if repRow:
        out_st_mso_name=repRow[0].name
    
    customerName=''
    clientRow=db((db.sm_client.cid==c_id)&(db.sm_client.depot_id==depot_id)&(db.sm_client.client_id==customerId)).select(db.sm_client.name,limitby=(0,1))
    if clientRow:
        customerName=clientRow[0].name
        
    try:        
        startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d').strftime('%Y-%m-%d')
    except:
        startDt=''                
    
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d').strftime('%Y-%m-%d')
    
    #---------------end paging
    
    #------------- Invoice
    qset=db()
    qset=qset(db.sm_invoice_head.cid==c_id)
    qset=qset(db.sm_invoice_head.depot_id==depot_id)
    qset=qset(db.sm_invoice_head.store_id==store_id)
    qset=qset(db.sm_invoice_head.status=='Invoiced')
    qset=qset(db.sm_invoice_head.invoice_date<=endDt)
    
    if out_st_delivery_man_id!='':
        qset=qset(db.sm_invoice_head.d_man_id==out_st_delivery_man_id)
    if out_st_territory_id!='':
        qset=qset(db.sm_invoice_head.area_id==out_st_territory_id)
    if out_st_mso_id!='':
        qset=qset(db.sm_invoice_head.rep_id==out_st_mso_id)
    if invoice_term!='':
        qset=qset(db.sm_invoice_head.payment_mode==invoice_term)
    if customerId!='':
        qset=qset(db.sm_invoice_head.client_id==customerId)
        
    if credit_type!='':
        qset=qset(db.sm_invoice_head.credit_note==credit_type)
    if customer_cat!='':
        qset=qset(db.sm_invoice_head.cl_category_id==customer_cat)
    if customer_sub_cat!='':
        qset=qset(db.sm_invoice_head.cl_sub_category_id==customer_sub_cat)
        
    if out_st_level1_id!='':
        qset=qset(db.sm_invoice_head.level1_id==out_st_level1_id)
    if out_st_level2_id!='':
        qset=qset(db.sm_invoice_head.level2_id==out_st_level2_id)
        
    records=qset.select(db.sm_invoice_head.ALL,orderby=db.sm_invoice_head.sl)
    
    #---------- Collection
    qset2=db()
    qset2=qset2(db.sm_payment_collection.cid==c_id)
    qset2=qset2(db.sm_payment_collection.depot_id==depot_id)
    qset2=qset2(db.sm_payment_collection.store_id==store_id)
    qset2=qset2(db.sm_payment_collection.status=='Posted')
    qset2=qset2(db.sm_payment_collection.collection_date<=endDt)    
    
    if out_st_delivery_man_id!='':
        qset2=qset2(db.sm_payment_collection.d_man_id==out_st_delivery_man_id)
    if out_st_territory_id!='':
        qset2=qset2(db.sm_payment_collection.area_id==out_st_territory_id)
    if out_st_mso_id!='':
        qset2=qset2(db.sm_payment_collection.rep_id==out_st_mso_id)
    if invoice_term!='':
        qset2=qset2(db.sm_payment_collection.payment_mode==invoice_term)
    if customerId!='':
        qset2=qset2(db.sm_payment_collection.client_id==customerId)
        
    if credit_type!='':
        qset2=qset2(db.sm_payment_collection.credit_note==credit_type)
    if customer_cat!='':
        qset2=qset2(db.sm_payment_collection.cl_category_id==customer_cat)
    if customer_sub_cat!='':
        qset2=qset2(db.sm_payment_collection.cl_sub_category_id==customer_sub_cat)
        
    if out_st_level1_id!='':
        qset2=qset2(db.sm_payment_collection.level1_id==out_st_level1_id)
    if out_st_level2_id!='':
        qset2=qset2(db.sm_payment_collection.level2_id==out_st_level2_id)
        
    #--------------------
    collectionList=[]
    transactionCause1=['','COLLECTION ERROR','ENTRY ERROR']
    qset2A=qset2(db.sm_payment_collection.transaction_cause.belongs(transactionCause1))
    records2A=qset2A.select(db.sm_payment_collection.head_rowid,db.sm_payment_collection.collection_amount.sum(),groupby=db.sm_payment_collection.head_rowid,orderby=db.sm_payment_collection.head_rowid)
    for rec2A in records2A:
        head_rowid=rec2A.sm_payment_collection.head_rowid
        collection_amount=float(rec2A[db.sm_payment_collection.collection_amount.sum()])
        collectionList.append({'headId':head_rowid,'collectionAmt':collection_amount,'adjustAmt':0})
    
    #--------------------    
    adjustmentList=[]
    transactionCause2=['VAT AIT','RETURN GOODS','BAD DEBTS']
    qset2B=qset2(db.sm_payment_collection.transaction_cause.belongs(transactionCause2))
    records2B=qset2B.select(db.sm_payment_collection.head_rowid,db.sm_payment_collection.collection_amount.sum(),groupby=db.sm_payment_collection.head_rowid,orderby=db.sm_payment_collection.head_rowid)
    for rec2B in records2B:
        head_rowid=rec2B.sm_payment_collection.head_rowid
        adjust_amount=float(rec2B[db.sm_payment_collection.collection_amount.sum()])
        
        index2=-1
        try:
            index2=str(map(itemgetter('headId'), collectionList).index(head_rowid))    
        except:
            index2=-1
            
        if (index2!=-1):
            dictData2=collectionList[int(index2)]            
            dictData2['adjustAmt']=adjust_amount
        else:
            adjustmentList.append({'headId':head_rowid,'collectionAmt':0,'adjustAmt':adjust_amount})
            
    collectionAdjustList=[]
    collectionAdjustList=collectionList+adjustmentList
    #---------------------------------------------    
    
    #====================
    p_collectionAdjustList=[]
    p_collectionAdjustList=collectionList+adjustmentList
    
    p_totalInvTP=0
    p_totalInvVat=0
    p_totalInvDisc=0
    p_totalInvSp=0
    p_totalInvAmt=0
    percentTp=0
    percentVat=0
    percentDisc=0
    percentSpDisc=0
    
    for record in records:
        p_headId=record.id
        p_invTp=record.actual_total_tp-(record.return_tp+record.return_sp_discount)
        p_invVat=record.vat_total_amount-record.return_vat
        p_invDiscount=record.discount-record.return_discount
        p_invSpDisc=record.sp_discount-record.return_sp_discount
        p_invNetAmt=p_invTp+p_invVat-(p_invDiscount+p_invSpDisc)
        
        #       <!--collection and adjustment data-->
        collection_amount=0
        adjust_amount=0
        
        list_index=-1
        try:
            list_index=str(map(itemgetter('headId'), p_collectionAdjustList).index(p_headId)) 
        except:
            list_index=-1
        
        if (list_index!=-1):
            listDictData=p_collectionAdjustList[int(list_index)]        
            collection_amount=float(listDictData['collectionAmt'])
            adjust_amount=float(listDictData['adjustAmt'])
            
            del p_collectionAdjustList[int(list_index)]
        
       #<!--end collection and adjustment data-->
        
        p_outstanding=round(p_invNetAmt-(collection_amount+adjust_amount),2)
        if p_outstanding==0:
            continue
            
        p_totalInvTP+=p_invTp
        p_totalInvVat+=p_invVat
        p_totalInvDisc+=p_invDiscount
        p_totalInvSp+=p_invSpDisc
        p_totalInvAmt+=p_invNetAmt
    
    #----------- 
    try:
        percentTp=p_totalInvTP/p_totalInvAmt*100
        percentVat=p_totalInvVat/p_totalInvAmt*100
        percentDisc=p_totalInvDisc/p_totalInvAmt*100
        percentSpDisc=p_totalInvSp/p_totalInvAmt*100
    except:
        percentTp=0
        percentVat=0
        percentDisc=0
        percentSpDisc=0
    #======================
    
    
    myString='6.1 Invoice Wise Outstanding (As Of Date)\n'
    myString+='Inv Date From:,'+str(startDt)+'\n'
    myString+='To/ as of Date:'+','+str(endDt)+'\n'
    myString+='Inv Term:,'+str(invoice_term)+'\n'
    myString+='Branch ID:,'+str(depot_id)+'\n'
    myString+='Branch Name'+','+str(depot_name)+'\n'
    myString+='Store ID:,'+str(store_id)+'\n'
    myString+='Store Name'+','+str(store_name)+'\n'
    myString+='DP ID:,'+str(out_st_delivery_man_id)+'\n'
    myString+='DP Name'+','+str(out_st_delivery_man_name)+'\n'
    myString+='Territory ID:,'+str(out_st_territory_id)+'\n'
    myString+='Territory Name'+','+str(out_st_territory_name)+'\n'
    myString+='MSO ID:,'+str(out_st_mso_id)+'\n'
    myString+='MSO Name'+','+str(out_st_mso_name)+'\n'
    myString+='Customer ID:,'+str(customerId)+'\n'
    myString+='Customer Name'+','+str(customerName)+'\n'
    
    myString+='Credit Type:,'+str(credit_type)+'\n'    
    if catName=='':
        catName='ALL'
    if subCatName=='':
        subCatName='ALL'        
    myString+='Customer Category'+','+str(catName)+'\n'
    myString+='Customer Sub-Category'+','+str(subCatName)+'\n'
    
    myString+=str(session.level1Name)+','+str(out_st_level1_id)+'\n'
    myString+=str(session.level2Name)+','+str(out_st_level2_id)+'\n'
    
    totalInvTP=0
    totalInvVat=0
    totalInvDisc=0
    totalInvAmt=0
    totalInvSp=0
    totalOutsTP=0
    totalOutsVat=0
    totalOutsDisc=0
    totalOutST=0
    totalOutSp=0
    
    sl=0
    myString+='SL,Date,Inv.No,Cust.ID,Cust.Name,Cust.Sub-Category ID,Cust.Sub-Category Name,MSO ID,MSO Name,DP ID,DP Name,Terms,Tr.Code,Market,Invoice-TP,Invoice-Vat,Invoice-Disc,Invoice-SP,Invoice-Net,Adjusted,Outstanding-TP,Outstanding-Vat,Outstanding-Disc,Outstanding-SP,Outstanding-Net,Aging,Oustanding%'+'\n'
    for row in records:
        headId=row.id
        depot_id=row.depot_id
        invoice_date=row.invoice_date
        invNo=str(session.prefix_invoice)+'INV'+str(depot_id)+'-'+str(row.sl)
        client_id=row.client_id
        client_name=str(row.client_name).replace(',', ' ')
        cl_sub_category_id=row.cl_sub_category_id
        cl_sub_category_name=str(row.cl_sub_category_name).replace(',', ' ')        
        rep_id=row.rep_id
        rep_name=str(row.rep_name).replace(',', ' ')
        d_man_id=row.d_man_id
        d_man_name=str(row.d_man_name).replace(',', ' ')
        payment_mode=row.payment_mode
        area_id=row.area_id
        market_name=str(row.market_name).replace(',', ' ')
        
        invTp=row.actual_total_tp-(row.return_tp+row.return_sp_discount)
        invVat=row.vat_total_amount-row.return_vat
        invDiscount=row.discount-row.return_discount
        invSpDisc=row.sp_discount-row.return_sp_discount
        invNetAmt=invTp+invVat-(invDiscount+invSpDisc)
        
        #-----------------
        collection_amount=0
        adjust_amount=0
        
        list_index=-1
        try:
            list_index=str(map(itemgetter('headId'), collectionAdjustList).index(headId)) 
        except:
            list_index=-1
            
        if (list_index!=-1):
            listDictData=collectionAdjustList[int(list_index)]        
            collection_amount=float(listDictData['collectionAmt'])
            adjust_amount=float(listDictData['adjustAmt'])
            
            del collectionAdjustList[int(list_index)]
            
        #end collection and adjustment data-->
        
        #outstanding=round(invNetAmt-collection_amount,2)
        outstanding=round(invNetAmt-(collection_amount+adjust_amount),2)
        if outstanding==0:
            continue
        sl+=1
        try:
#             outTp=(invTp*outstanding)/invNetAmt
#             outVat=(invVat*outstanding)/invNetAmt
#             outDisc=(invDiscount*outstanding)/invNetAmt
#             outSp=(invSpDisc*outstanding)/invNetAmt
            
            outTp=outstanding*(percentTp/100)
            outVat=outstanding*(percentVat/100)
            outDisc=outstanding*(percentDisc/100)
            outSp=outstanding*(percentSpDisc/100)
            
        except:
            outTp=0
            outVat=0
            outDisc=0
            outSp=0
        
        totalInvTP+=invTp
        totalInvVat+=invVat
        totalInvDisc+=invDiscount
        totalInvSp+=invSpDisc
        totalInvAmt+=invNetAmt
        
        #totalOutsTP+=outTp
        #totalOutsVat+=outVat
        #totalOutsDisc+=outDisc
        #totalOutSp+=outSp
        totalOutST+=outstanding
        
        invoice_date=datetime.datetime.strptime(str(row.invoice_date),'%Y-%m-%d')
        agingDay=(currentDate-invoice_date).days
        
        if invNetAmt!=0:
            outstandingPercent=round((outstanding/invNetAmt*100),2)
        else:
            outstandingPercent=0
            
        #------------------------        
        myString+=str(sl)+','+str(invoice_date)+','+str(invNo)+','+str(client_id)+','+str(client_name)+','+str(cl_sub_category_id)+','+str(cl_sub_category_name)+','+str(rep_id)+','+str(rep_name)+','+str(d_man_id)+','+str(d_man_name)+','+str(payment_mode)+','+str(area_id)+','+str(market_name)+','+str(invTp)+','+\
        str(invVat)+','+str(invDiscount)+','+str(invSpDisc)+','+str(invNetAmt)+','+str(adjust_amount)+','+str(outTp)+','+str(outVat)+','+str(outDisc)+','+str(outSp)+','+str(outstanding)+','+\
        str(agingDay)+','+str(outstandingPercent)+'\n'
    
    myString+='\n\nSummary,,,,,,,,,,,,,,,,,,,,\n'
    
    myString+='Invoice TP,'+str(round(totalInvTP,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Invoice VAT,'+str(round(totalInvVat,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Invoice Discount,'+str(round(totalInvDisc,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Invoice SP.Disc,'+str(round(totalInvSp,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Invoice Net,'+str(round(totalInvAmt,2))+',,,,,,,,,,,,,,,,,,,\n\n'
    
    try:
        totalOutsTP=(totalInvTP*totalOutST)/totalInvAmt
        totalOutsVat=(totalInvVat*totalOutST)/totalInvAmt
        totalOutsDisc=(totalInvDisc*totalOutST)/totalInvAmt
        totalOutSp=(totalInvSp*totalOutST)/totalInvAmt
    except:
        totalOutsTP=0
        totalOutsVat=0
        totalOutsDisc=0
        totalOutSp=0
        
    myString+='Outstanding TP,'+str(round(totalOutsTP,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Outstanding VAT,'+str(round(totalOutsVat,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Outstanding Discount,'+str(round(totalOutsDisc,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Outstanding SP.Disc,'+str(round(totalOutSp,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Outstanding Net,'+str(round(totalOutST,2))+',,,,,,,,,,,,,,,,,,,\n'
    
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_invWiseOutstandingAsOfDate.csv'   
    return str(myString)
    
    
#---------------Transit Dispute

def tansitDisputeList():
    c_id=session.cid
    
    response.title='Transit Dispute List'
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    depot_id=str(request.vars.depotID).strip()
    store_id=str(request.vars.storeID).strip()
    
    depotName=str(request.vars.depotName).strip()
    storeName=str(request.vars.storeName).strip()
    
    startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d')    
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d')+datetime.timedelta(days=1)
    
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    qset=db()
    qset=qset(db.sm_transaction_dispute.cid==c_id)
    qset=qset((db.sm_transaction_dispute.dispute_date>=startDt)&(db.sm_transaction_dispute.dispute_date<endDt))
    qset=qset(db.sm_transaction_dispute.depot_id==depot_id)
    qset=qset(db.sm_transaction_dispute.store_id==store_id)
    qset=qset(db.sm_transaction_dispute.status=='Resolved')    
    records=qset.select(db.sm_transaction_dispute.store_id,db.sm_transaction_dispute.store_name.max(),db.sm_transaction_dispute.item_id,db.sm_transaction_dispute.item_name.max(),db.sm_transaction_dispute.price,db.sm_transaction_dispute.quantity.sum(),orderby=db.sm_transaction_dispute.item_id,groupby=db.sm_transaction_dispute.store_id|db.sm_transaction_dispute.store_name|db.sm_transaction_dispute.item_id|db.sm_transaction_dispute.item_name|db.sm_transaction_dispute.price,limitby=limitby)
    
    return dict(records=records,fromDate=fromDate,toDate=toDate,depotID=depot_id,depotName=depotName,storeID=store_id,storeName=storeName,page=page,items_per_page=items_per_page)    

def downloadTransitDisputeList():
    c_id=session.cid
    
    response.title='Download Transit Dispute List'
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
        
    depot_id=str(request.vars.depotID).strip()
    store_id=str(request.vars.storeID).strip()
    
    depotName=str(request.vars.depotName).strip()
    storeName=str(request.vars.storeName).strip()
    
    startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d')    
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d')+datetime.timedelta(days=1)
    
  
    qset=db()
    qset=qset(db.sm_transaction_dispute.cid==c_id)
    qset=qset((db.sm_transaction_dispute.dispute_date>=startDt)&(db.sm_transaction_dispute.dispute_date<endDt))
    qset=qset(db.sm_transaction_dispute.depot_id==depot_id)
    qset=qset(db.sm_transaction_dispute.store_id==store_id)
    qset=qset(db.sm_transaction_dispute.status=='Resolved')
    records=qset.select(db.sm_transaction_dispute.store_id,db.sm_transaction_dispute.store_name.max(),db.sm_transaction_dispute.item_id,db.sm_transaction_dispute.item_name.max(),db.sm_transaction_dispute.price,db.sm_transaction_dispute.quantity.sum(),orderby=db.sm_transaction_dispute.item_id,groupby=db.sm_transaction_dispute.store_id|db.sm_transaction_dispute.store_name|db.sm_transaction_dispute.item_id|db.sm_transaction_dispute.item_name|db.sm_transaction_dispute.price)
    
    #REmove , from record.Cause , means new column in excel
    myString='Date From,'+fromDate+'\n'
    myString+='Date To,'+toDate+'\n'
    myString+='Depot/Branch,'+depot_id+'|'+depotName+'\n'
    myString+='Store,'+store_id+'|'+storeName+'\n\n'
        
    myString+='Product ID,Name,Store ID,Store Name,Qty,TP,TP Amount\n'
    for rec in records:
        item_id=rec.sm_transaction_dispute.item_id
        item_name=rec[db.sm_transaction_dispute.item_name.max()]
        store_id=rec.sm_transaction_dispute.store_id
        store_name=rec[db.sm_transaction_dispute.store_name.max()]
        quantity=rec[db.sm_transaction_dispute.quantity.sum()]     
        price=rec.sm_transaction_dispute.price
        
        myString+=str(item_id)+','+str(item_name)+','+str(store_id)+','+store_name+','+str(quantity)+','+str(price)+','+str(quantity*price)+'\n'
        
    #Save as csv
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_issue_list.csv'   
    return str(myString) 


def tansitDisputeItemWise():
    c_id=session.cid
    
    response.title='Transit Dispute Item Wise'
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    depot_id=str(request.vars.depotID).strip()
    store_id=str(request.vars.storeID).strip()
    
    depotName=str(request.vars.depotName).strip()
    storeName=str(request.vars.storeName).strip()
    
    startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d')    
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d')+datetime.timedelta(days=1)
    
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    qset=db()
    qset=qset(db.sm_transaction_dispute.cid==c_id)
    qset=qset(db.sm_transaction_dispute.depot_id==depot_id)
    qset=qset(db.sm_transaction_dispute.store_id==store_id)
    qset=qset((db.sm_transaction_dispute.dispute_date>=startDt)&(db.sm_transaction_dispute.dispute_date<endDt))    
    qset=qset(db.sm_transaction_dispute.status=='Resolved')
    
    records=qset.select(db.sm_transaction_dispute.store_id,db.sm_transaction_dispute.store_name.max(),db.sm_transaction_dispute.item_id,db.sm_transaction_dispute.item_name.max(),db.sm_transaction_dispute.batch_id,db.sm_transaction_dispute.expiary_date,db.sm_transaction_dispute.price,db.sm_transaction_dispute.quantity.sum(),orderby=db.sm_transaction_dispute.item_id|db.sm_transaction_dispute.batch_id,groupby=db.sm_transaction_dispute.store_id|db.sm_transaction_dispute.item_id|db.sm_transaction_dispute.batch_id|db.sm_transaction_dispute.expiary_date|db.sm_transaction_dispute.price,limitby=limitby)
    
    return dict(records=records,fromDate=fromDate,toDate=toDate,depotID=depot_id,depotName=depotName,storeID=store_id,storeName=storeName,page=page,items_per_page=items_per_page)    

def downloadTansitDisputeItemWise():
    c_id=session.cid
    
    response.title='Download Transit Dispute Item Wise'
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
        
    depot_id=str(request.vars.depotID).strip()
    store_id=str(request.vars.storeID).strip()
    
    depotName=str(request.vars.depotName).strip()
    storeName=str(request.vars.storeName).strip()
    
    startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d')    
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d')+datetime.timedelta(days=1)
  
    qset=db()
    qset=qset(db.sm_transaction_dispute.cid==c_id)
    qset=qset(db.sm_transaction_dispute.depot_id==depot_id)
    qset=qset(db.sm_transaction_dispute.store_id==store_id)
    qset=qset((db.sm_transaction_dispute.dispute_date>=startDt)&(db.sm_transaction_dispute.dispute_date<endDt))    
    qset=qset(db.sm_transaction_dispute.status=='Resolved')
    
    records=qset.select(db.sm_transaction_dispute.store_id,db.sm_transaction_dispute.store_name.max(),db.sm_transaction_dispute.item_id,db.sm_transaction_dispute.item_name.max(),db.sm_transaction_dispute.batch_id,db.sm_transaction_dispute.expiary_date,db.sm_transaction_dispute.price,db.sm_transaction_dispute.quantity.sum(),orderby=db.sm_transaction_dispute.item_id|db.sm_transaction_dispute.batch_id,groupby=db.sm_transaction_dispute.store_id|db.sm_transaction_dispute.item_id|db.sm_transaction_dispute.batch_id|db.sm_transaction_dispute.expiary_date|db.sm_transaction_dispute.price)
   
    #REmove , from record.Cause , means new column in excel
    myString='Date From,'+fromDate+'\n'
    myString+='Date To,'+toDate+'\n'
    myString+='Depot/Branch,'+depot_id+'|'+depotName+'\n'
    myString+='Store,'+store_id+'|'+storeName+'\n\n'
        
    myString+='Product ID,Name,Store ID,Store Name,Qty,Batch,Expiry Date,TP,TP Amount\n'
    for rec in records:
        item_id=rec.sm_transaction_dispute.item_id
        item_name=rec[db.sm_transaction_dispute.item_name.max()]
        store_id=rec.sm_transaction_dispute.store_id
        store_name=rec[db.sm_transaction_dispute.store_name.max()]
        quantity=rec[db.sm_transaction_dispute.quantity.sum()]
        batch_id=rec.sm_transaction_dispute.batch_id
        expiary_date=rec.sm_transaction_dispute.expiary_date        
        price=rec.sm_transaction_dispute.price
                
        myString+=str(item_id)+','+str(item_name)+','+str(store_id)+','+store_name+','+str(quantity)+','+str(batch_id)+','+str(expiary_date)+','+str(price)+','+str(quantity*price)+'\n'
        
    #Save as csv
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_transit_dispute_item_wise.csv'   
    return str(myString)  


#----------issue
def issueList():
    c_id=session.cid
    
    response.title='Issue List'
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    depot_id=str(request.vars.depotID).strip()
    store_id=str(request.vars.storeID).strip()
    
    depotName=str(request.vars.depotName).strip()
    storeName=str(request.vars.storeName).strip()
    
    startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d')    
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d')+datetime.timedelta(days=1)
    
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    qset=db()
    qset=qset(db.sm_issue.cid==c_id)
    qset=qset(db.sm_issue.depot_id==depot_id)
    qset=qset(db.sm_issue.store_id==store_id)
    qset=qset((db.sm_issue.issue_date>=startDt)&(db.sm_issue.issue_date<endDt))    
    qset=qset(db.sm_issue.status=='Posted')
    
    records=qset.select(db.sm_issue.store_id,db.sm_issue.store_name.max(),db.sm_issue.item_id,db.sm_issue.item_name.max(),db.sm_issue.dist_rate,db.sm_issue.quantity.sum(),orderby=db.sm_issue.item_name,groupby=db.sm_issue.store_id|db.sm_issue.item_id|db.sm_issue.dist_rate,limitby=limitby)
    
    return dict(records=records,fromDate=fromDate,toDate=toDate,depotID=depot_id,depotName=depotName,storeID=store_id,storeName=storeName,page=page,items_per_page=items_per_page)    

def downloadIssueList():
    c_id=session.cid
    
    response.title='Download Issue List'
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
        
    depot_id=str(request.vars.depotID).strip()
    store_id=str(request.vars.storeID).strip()
    
    depotName=str(request.vars.depotName).strip()
    storeName=str(request.vars.storeName).strip()
    
    startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d')    
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d')+datetime.timedelta(days=1)
    
  
    qset=db()
    qset=qset(db.sm_issue.cid==c_id)
    qset=qset((db.sm_issue.issue_date>=startDt)&(db.sm_issue.issue_date<endDt))
    qset=qset(db.sm_issue.depot_id==depot_id)
    qset=qset(db.sm_issue.store_id==store_id)
    qset=qset(db.sm_issue.status=='Posted')
    
    records=qset.select(db.sm_issue.store_id,db.sm_issue.store_name.max(),db.sm_issue.item_id,db.sm_issue.item_name.max(),db.sm_issue.dist_rate,db.sm_issue.quantity.sum(),orderby=db.sm_issue.item_name,groupby=db.sm_issue.store_id|db.sm_issue.item_id|db.sm_issue.dist_rate)
    #REmove , from record.Cause , means new column in excel
    myString='Date From,'+fromDate+'\n'
    myString+='Date To,'+toDate+'\n'
    myString+='Depot/Branch,'+depot_id+'|'+depotName+'\n'
    myString+='Store,'+store_id+'|'+storeName+'\n\n'
        
    myString+='Product ID,Name,Store ID,Store Name,Qty,TP,TP Amount\n'
    for rec in records:
        item_id=rec.sm_issue.item_id
        item_name=rec[db.sm_issue.item_name.max()]
        store_id=rec.sm_issue.store_id
        store_name=rec[db.sm_issue.store_name.max()]
        quantity=rec[db.sm_issue.quantity.sum()]     
        price=rec.sm_issue.dist_rate
        
        myString+=str(item_id)+','+str(item_name)+','+str(store_id)+','+store_name+','+str(quantity)+','+str(price)+','+str(quantity*price)+'\n'
        
    #Save as csv
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_issue_list.csv'   
    return str(myString) 

def issueItemWise():
    c_id=session.cid
    
    response.title='Issue Item Wise'
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    depot_id=str(request.vars.depotID).strip()
    store_id=str(request.vars.storeID).strip()
    
    depotName=str(request.vars.depotName).strip()
    storeName=str(request.vars.storeName).strip()
    
    startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d')    
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d')+datetime.timedelta(days=1)
    
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    qset=db()
    qset=qset(db.sm_issue.cid==c_id)
    qset=qset((db.sm_issue.issue_date>=startDt)&(db.sm_issue.issue_date<endDt))
    qset=qset(db.sm_issue.depot_id==depot_id)
    qset=qset(db.sm_issue.store_id==store_id)
    qset=qset(db.sm_issue.status=='Posted')
    
    records=qset.select(db.sm_issue.store_id,db.sm_issue.store_name.max(),db.sm_issue.item_id,db.sm_issue.item_name.max(),db.sm_issue.batch_id,db.sm_issue.expiary_date,db.sm_issue.dist_rate,db.sm_issue.quantity.sum(),orderby=db.sm_issue.item_id|db.sm_issue.batch_id,groupby=db.sm_issue.store_id|db.sm_issue.item_id|db.sm_issue.batch_id|db.sm_issue.expiary_date|db.sm_issue.dist_rate,limitby=limitby)
    
    return dict(records=records,fromDate=fromDate,toDate=toDate,depotID=depot_id,depotName=depotName,storeID=store_id,storeName=storeName,page=page,items_per_page=items_per_page)    

def downloadIssueItemWise():
    c_id=session.cid
    
    response.title='Download issue Item Wise'
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
        
    depot_id=str(request.vars.depotID).strip()
    store_id=str(request.vars.storeID).strip()
    
    depotName=str(request.vars.depotName).strip()
    storeName=str(request.vars.storeName).strip()
    
    startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d')    
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d')+datetime.timedelta(days=1)
  
    qset=db()
    qset=qset(db.sm_issue.cid==c_id)
    qset=qset((db.sm_issue.issue_date>=startDt)&(db.sm_issue.issue_date<endDt))
    qset=qset(db.sm_issue.depot_id==depot_id)
    qset=qset(db.sm_issue.store_id==store_id)
    qset=qset(db.sm_issue.status=='Posted')
    
    records=qset.select(db.sm_issue.store_id,db.sm_issue.store_name.max(),db.sm_issue.item_id,db.sm_issue.item_name.max(),db.sm_issue.batch_id,db.sm_issue.expiary_date,db.sm_issue.dist_rate,db.sm_issue.quantity.sum(),orderby=db.sm_issue.item_id|db.sm_issue.batch_id,groupby=db.sm_issue.store_id|db.sm_issue.item_id|db.sm_issue.batch_id|db.sm_issue.expiary_date|db.sm_issue.dist_rate)
    
   
    #REmove , from record.Cause , means new column in excel
    myString='Date From,'+fromDate+'\n'
    myString+='Date To,'+toDate+'\n'
    myString+='Depot/Branch,'+depot_id+'|'+depotName+'\n'
    myString+='Store,'+store_id+'|'+storeName+'\n\n'
        
    myString+='Product ID,Name,Store ID,Store Name,Qty,Batch,Expiry Date,TP,TP Amount\n'
    for rec in records:
        item_id=rec.sm_issue.item_id
        item_name=rec[db.sm_issue.item_name.max()]
        store_id=rec.sm_issue.store_id
        store_name=rec[db.sm_issue.store_name.max()]
        quantity=rec[db.sm_issue.quantity.sum()]
        batch_id=rec.sm_issue.batch_id
        expiary_date=rec.sm_issue.expiary_date        
        price=rec.sm_issue.dist_rate
        
        
        myString+=str(item_id)+','+str(item_name)+','+str(store_id)+','+store_name+','+str(quantity)+','+str(batch_id)+','+str(expiary_date)+','+str(price)+','+str(quantity*price)+'\n'
        
    #Save as csv
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_issue_item_wise.csv'   
    return str(myString)  


##-------------- issue

def transferDetails():
    c_id=session.cid
    
    response.title='25.2 Transfer Details'
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    depot_id=str(request.vars.depotID).strip()
    store_id=str(request.vars.storeID).strip()
    
    to_depot_id=str(request.vars.to_depot_id).strip()
    to_depot_name=''
    toDepotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==to_depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if toDepotRow:
        to_depot_name=toDepotRow[0].name
        
    depotName=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depotName=depotRow[0].name
        
    storeName=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        storeName=storeRow[0].store_name
    
    startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d')    
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d')
    
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    recItemList=[]
    
    qset=db()
    qset=qset(db.sm_issue.cid==c_id)
    qset=qset(db.sm_issue.depot_id==depot_id)
    qset=qset(db.sm_issue.store_id==store_id)
    qset=qset((db.sm_issue.issue_date>=startDt)&(db.sm_issue.issue_date<=endDt))    
    qset=qset(db.sm_issue.status=='Posted')
    if to_depot_id!='':
        qset=qset(db.sm_issue.issued_to==to_depot_id)
        
    records=qset.select(db.sm_issue.item_id,db.sm_issue.item_name.max(),orderby=db.sm_issue.item_name,groupby=db.sm_issue.item_id)
    
    for row in records:
        item_id=row.sm_issue.item_id
        item_name=row[db.sm_issue.item_name.max()]
        
        recDetailList=[]
        hQty=0
        hTp=0
        
        qset1=db()
        qset1=qset1(db.sm_issue.cid==c_id)
        qset1=qset1(db.sm_issue.depot_id==depot_id)
        qset1=qset1(db.sm_issue.store_id==store_id)
        qset1=qset1((db.sm_issue.issue_date>=startDt)&(db.sm_issue.issue_date<=endDt))
        qset1=qset1(db.sm_issue.item_id==item_id)        
        qset1=qset1(db.sm_issue.status=='Posted')
        if to_depot_id!='':
            qset1=qset1(db.sm_issue.issued_to==to_depot_id)
            
        adjReceiptRow=qset1.select(db.sm_issue.depot_id,db.sm_issue.sl,db.sm_issue.issue_date,db.sm_issue.store_id,db.sm_issue.store_name,db.sm_issue.issued_to,db.sm_issue.depot_to_name,db.sm_issue.dist_rate,db.sm_issue.quantity,orderby=db.sm_issue.sl)
        
        for drow in adjReceiptRow:
            depot_id=drow.depot_id
            sl=drow.sl
            issue_date=drow.issue_date
            store_id=drow.store_id
            store_name=drow.store_name
            issued_to=drow.issued_to
            depot_to_name=drow.depot_to_name
            quantity=drow.quantity
            price=drow.dist_rate
            tp=quantity*price
            hQty+=quantity
            hTp+=quantity*price
            
            slStr=str(session.prefix_invoice)+'TR'+str(depot_id)+'-'+str(sl)
            
            dictDetData={'slNo':str(slStr),'recDate':issue_date,'trFrom':store_id,'trFromName':store_name,'trToDepot':issued_to,'trToDepotName':depot_to_name,'qty':str(quantity),'recTp':str(tp)}
            recDetailList.append(dictDetData)
        
        dictHeadData={'ItemID':item_id,'itemName':item_name,'hQty':hQty,'hTp':hTp,'rDetails':recDetailList}
        recItemList.append(dictHeadData)    
        
    return dict(recItemList=recItemList,fromDate=fromDate,toDate=toDate,depotID=depot_id,depotName=depotName,storeID=store_id,storeName=storeName,to_depot_id=to_depot_id,to_depot_name=to_depot_name,page=page,items_per_page=items_per_page)    


def transferDetails_download():
    c_id=session.cid
    
    response.title='Download-Transfer Details'
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    depot_id=str(request.vars.depotID).strip()
    store_id=str(request.vars.storeID).strip()
    
    to_depot_id=str(request.vars.to_depot_id).strip()
    to_depot_name=''
    toDepotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==to_depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if toDepotRow:
        to_depot_name=toDepotRow[0].name
        
    depotName=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depotName=depotRow[0].name
        
    storeName=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        storeName=storeRow[0].store_name
    
    startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d')    
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d')
    
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    recItemList=[]
    
    
    qset=db()
    qset=qset(db.sm_issue.cid==c_id)
    qset=qset(db.sm_issue.depot_id==depot_id)
    qset=qset(db.sm_issue.store_id==store_id)
    qset=qset((db.sm_issue.issue_date>=startDt)&(db.sm_issue.issue_date<=endDt))    
    qset=qset(db.sm_issue.status=='Posted')
    if to_depot_id!='':
        qset=qset(db.sm_issue.issued_to==to_depot_id)
        
    records=qset.select(db.sm_issue.item_id,db.sm_issue.item_name.max(),orderby=db.sm_issue.item_name,groupby=db.sm_issue.item_id)
    
    for row in records:
        item_id=row.sm_issue.item_id
        item_name=row[db.sm_issue.item_name.max()]
        
        recDetailList=[]
        hQty=0
        hTp=0
        
        qset1=db()
        qset1=qset1(db.sm_issue.cid==c_id)
        qset1=qset1(db.sm_issue.depot_id==depot_id)
        qset1=qset1(db.sm_issue.store_id==store_id)
        qset1=qset1((db.sm_issue.issue_date>=startDt)&(db.sm_issue.issue_date<=endDt))
        qset1=qset1(db.sm_issue.item_id==item_id)        
        qset1=qset1(db.sm_issue.status=='Posted')
        if to_depot_id!='':
            qset1=qset1(db.sm_issue.issued_to==to_depot_id)
            
        adjReceiptRow=qset1.select(db.sm_issue.depot_id,db.sm_issue.sl,db.sm_issue.issue_date,db.sm_issue.store_id,db.sm_issue.store_name,db.sm_issue.issued_to,db.sm_issue.depot_to_name,db.sm_issue.dist_rate,db.sm_issue.quantity,orderby=db.sm_issue.sl)
        
        for drow in adjReceiptRow:
            depot_id=drow.depot_id
            sl=drow.sl
            issue_date=drow.issue_date
            store_id=drow.store_id
            store_name=drow.store_name
            issued_to=drow.issued_to
            depot_to_name=drow.depot_to_name
            quantity=drow.quantity
            price=drow.dist_rate
            tp=quantity*price
            hQty+=quantity
            hTp+=quantity*price
            
            slStr=str(session.prefix_invoice)+'TR'+str(depot_id)+'-'+str(sl)
            
            dictDetData={'slNo':str(slStr),'recDate':issue_date,'trFrom':store_id,'trFromName':store_name,'trToDepot':issued_to,'trToDepotName':depot_to_name,'qty':str(quantity),'recTp':str(tp)}
            recDetailList.append(dictDetData)
        
        dictHeadData={'ItemID':item_id,'itemName':item_name,'hQty':hQty,'hTp':hTp,'rDetails':recDetailList}
        recItemList.append(dictHeadData)    
    
    
    #------------------------------------
    myString='25.2 Transfer Details\n'
    myString+='Date From:,'+str(startDt)+'\n'
    myString+='To Date:'+','+str(endDt)+'\n'
    myString+='Branch ID:,'+str(depot_id)+'\n'
    myString+='Branch Name'+','+str(depotName)+'\n'
    myString+='Store ID:,'+str(store_id)+'\n'
    myString+='Store Name'+','+str(storeName)+'\n'
    myString+='Transfer To ID:'+','+str(to_depot_id)+'\n'
    myString+='Transfer To Name:'+','+str(to_depot_name)+'\n'
    
    totalQty=0
    totalTp=0
    
    myString+='Item Id,Item Name,Transfer No,Date,From Location,To Location,Quantity,Trade Price'+'\n'
    for i in range(len(recItemList)):
        dictData=recItemList[i]
        
        ItemID=dictData['ItemID']
        itemName=str(dictData['itemName']).replace(',', ' ')
        hQty=dictData['hQty']
        totalQty+=hQty
        
        hTp=float(dictData['hTp'])
        totalTp+=hTp
          
        myString+=str(ItemID)+','+str(itemName)+',,,,,'+str(hQty)+','+str(hTp)+'\n'
        
        detailList=dictData['rDetails']
        for j in range(len(detailList)):
            dictDetData=detailList[j]
            
            slNo=dictDetData['slNo']
            recDate=dictDetData['recDate']
            
            trFrom=dictDetData['trFrom']
            trFromName=str(dictDetData['trFromName']).replace(',', ' ')
            trToDepot=dictDetData['trToDepot']
            trToDepotName=dictDetData['trToDepotName']
            
            qty=dictDetData['qty']
            recTp=dictDetData['recTp']
            
            myString+=',,'+str(slNo)+','+str(recDate)+','+str(trFrom)+':'+str(trFromName)+','+str(trToDepot)+':'+str(trToDepotName)+','+str(qty)+','+str(recTp)+'\n'
            
        #------------------------ 
        
    myString+='Total,,,,,,'+str(totalQty)+','+str(totalTp)+'\n'
    
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_transferDetails.csv'   
    return str(myString)

    
def transferSummeryItemWise():
    c_id=session.cid
    
    response.title='25.3 Transfer Summary Item Wise'
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    depot_id=str(request.vars.depotID).strip()
    store_id=str(request.vars.storeID).strip()
    
    to_depot_id=str(request.vars.to_depot_id).strip()
    to_depot_name=''
    toDepotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==to_depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if toDepotRow:
        to_depot_name=toDepotRow[0].name
        
    depotName=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depotName=depotRow[0].name
        
    storeName=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        storeName=storeRow[0].store_name
        
    startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d')    
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d')
    
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    
    qset=db()
    qset=qset(db.sm_issue.cid==c_id)
    qset=qset(db.sm_issue.depot_id==depot_id)
    qset=qset(db.sm_issue.store_id==store_id)
    qset=qset((db.sm_issue.issue_date>=startDt)&(db.sm_issue.issue_date<=endDt))    
    qset=qset(db.sm_issue.status=='Posted')
    if to_depot_id!='':
        qset=qset(db.sm_issue.issued_to==to_depot_id)
        
    records=qset.select(db.sm_issue.item_id,db.sm_issue.item_name.max(),db.sm_issue.dist_rate,db.sm_issue.quantity.sum(),orderby=db.sm_issue.item_name|db.sm_issue.dist_rate,groupby=db.sm_issue.item_id|db.sm_issue.dist_rate)
    
    return dict(records=records,fromDate=fromDate,toDate=toDate,depotID=depot_id,depotName=depotName,storeID=store_id,storeName=storeName,to_depot_id=to_depot_id,to_depot_name=to_depot_name,page=page,items_per_page=items_per_page)    


def transferSummeryItemWise_download():
    c_id=session.cid
    
    response.title='Transfer Summary Item Wise download'
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    depot_id=str(request.vars.depotID).strip()
    store_id=str(request.vars.storeID).strip()
    
    to_depot_id=str(request.vars.to_depot_id).strip()
    to_depot_name=''
    toDepotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==to_depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if toDepotRow:
        to_depot_name=toDepotRow[0].name
        
    depotName=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depotName=depotRow[0].name
        
    storeName=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        storeName=storeRow[0].store_name
        
    startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d')    
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d')
    
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    
    qset=db()
    qset=qset(db.sm_issue.cid==c_id)
    qset=qset(db.sm_issue.depot_id==depot_id)
    qset=qset(db.sm_issue.store_id==store_id)
    qset=qset((db.sm_issue.issue_date>=startDt)&(db.sm_issue.issue_date<=endDt))    
    qset=qset(db.sm_issue.status=='Posted')
    if to_depot_id!='':
        qset=qset(db.sm_issue.issued_to==to_depot_id)
        
    #records=qset.select(db.sm_issue.item_id,db.sm_issue.item_name,db.sm_issue.quantity.sum(),db.sm_issue.dist_rate,orderby=db.sm_issue.item_name|db.sm_issue.dist_rate,groupby=db.sm_issue.item_id|db.sm_issue.dist_rate)
    records=qset.select(db.sm_issue.item_id,db.sm_issue.item_name.max(),db.sm_issue.dist_rate,db.sm_issue.quantity.sum(),orderby=db.sm_issue.item_name|db.sm_issue.dist_rate,groupby=db.sm_issue.item_id|db.sm_issue.dist_rate)
    
    
    myString='25.3 IC Transfer Summary (Item Wise)\n'
    myString+='Date From:,'+str(startDt)+'\n'
    myString+='To Date:'+','+str(endDt)+'\n'
    myString+='Branch ID:,'+str(depot_id)+'\n'
    myString+='Branch Name'+','+str(depotName)+'\n'
    myString+='Store ID:,'+str(store_id)+'\n'
    myString+='Store Name'+','+str(storeName)+'\n'
    myString+='Transfer To ID:'+','+str(to_depot_id)+'\n'
    myString+='Transfer To Name:'+','+str(to_depot_name)+'\n'
    
    totalQty=0
    totalTP=0
    
    myString+='Item Id,Item Name,Trade Price,Quantity,Total Amount'+'\n'
    for row in records:
        item_id=row.sm_issue.item_id
        item_name=str(row[db.sm_issue.item_name.max()]).replace(',', ' ') 
        dist_rate=row.sm_issue.dist_rate
        qty=row[db.sm_issue.quantity.sum()]
        
        totalQty+=qty
        
        price=qty*row.sm_issue.dist_rate
                
        totalTP+=price
        
        #------------------------        
        myString+=str(item_id)+','+str(item_name)+','+str(dist_rate)+','+str(qty)+','+str(price)+'\n'
        
    myString+='Total,,,'+str(totalQty)+','+str(totalTP)+'\n'
    
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_transferSumamryItemwise.csv'   
    return str(myString)


def transferSummeryItemWise_internal():
    c_id=session.cid
    
    response.title='Transfer Summary Item Wise'
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    depot_id=str(request.vars.depotID).strip()
    store_id=str(request.vars.storeID).strip()
    
    depotName=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depotName=depotRow[0].name
        
    storeName=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        storeName=storeRow[0].store_name
        
    startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d')    
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d')+datetime.timedelta(days=1)
    
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    damageHeadList=[]
    
    qset=db()
    qset=qset(db.sm_damage.cid==c_id)
    qset=qset((db.sm_damage.damage_date>=startDt)&(db.sm_damage.damage_date<endDt))
    qset=qset(db.sm_damage.depot_id==depot_id)
    qset=qset(db.sm_damage.store_id==store_id)
    qset=qset(db.sm_damage.transfer_type=='TRANSFER')
    qset=qset(db.sm_damage.status=='Posted') 
    
    records=qset.select(db.sm_damage.item_id,db.sm_damage.item_name,db.sm_damage.quantity,db.sm_damage.dist_rate,orderby=db.sm_damage.item_id)
    
    return dict(records=records,fromDate=fromDate,toDate=toDate,depotID=depot_id,depotName=depotName,storeID=store_id,storeName=storeName,page=page,items_per_page=items_per_page)    


def transferSummery():
    c_id=session.cid
    
    response.title='25.1 Transfer Summary'
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    depot_id=str(request.vars.depotID).strip()
    store_id=str(request.vars.storeID).strip()
    
    to_depot_id=str(request.vars.to_depot_id).strip()
    to_depot_name=''
    toDepotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==to_depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if toDepotRow:
        to_depot_name=toDepotRow[0].name
        
    depotName=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depotName=depotRow[0].name
        
    storeName=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        storeName=storeRow[0].store_name
        
    startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d')    
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d')
    
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    
    condStr=" cid='"+str(c_id)+"' and depot_id='"+str(depot_id)+"' and store_id='"+str(store_id)+"' and (issue_date>='"+str(startDt)+"' and issue_date<='"+str(endDt)+"') and status='Posted'"
    if to_depot_id!='':
        condStr+=" and issued_to='"+str(to_depot_id)+"'"
        
    sqlStr="select depot_id,sl,MAX(issue_date) as issue_date,MAX(store_id) as store_id,MAX(store_name) as store_name,MAX(issued_to) as issued_to,MAX(depot_to_name) as depot_to_name,sum(quantity) as qty,sum(quantity*dist_rate) as price from sm_issue where "+str(condStr)+" group by depot_id,sl order by sl "
    recordList=db.executesql(sqlStr,as_dict = True) 
    
    return dict(recordList=recordList,fromDate=fromDate,toDate=toDate,depotID=depot_id,depotName=depotName,storeID=store_id,storeName=storeName,to_depot_id=to_depot_id,to_depot_name=to_depot_name,page=page,items_per_page=items_per_page)    


def transferSummery_download():
    c_id=session.cid
    
    response.title='Transfer Summary'
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    depot_id=str(request.vars.depotID).strip()
    store_id=str(request.vars.storeID).strip()
    
    to_depot_id=str(request.vars.to_depot_id).strip()
    to_depot_name=''
    toDepotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==to_depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if toDepotRow:
        to_depot_name=toDepotRow[0].name
        
    depotName=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depotName=depotRow[0].name
        
    storeName=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        storeName=storeRow[0].store_name
        
    startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d')    
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d')+datetime.timedelta(days=1)
    
    #--------------
    condStr=" cid='"+str(c_id)+"' and depot_id='"+str(depot_id)+"' and store_id='"+str(store_id)+"' and (issue_date>='"+str(startDt)+"' and issue_date<='"+str(endDt)+"') and status='Posted'"
    if to_depot_id!='':
        condStr+=" and issued_to='"+str(to_depot_id)+"'"
        
    #sqlStr="select depot_id,sl,issue_date,store_id,store_name,issued_to,depot_to_name,sum(quantity) as qty,sum(quantity*dist_rate) as price from sm_issue where "+str(condStr)+" group by sl order by sl "
    sqlStr="select depot_id,sl,MAX(issue_date) as issue_date,MAX(store_id) as store_id,MAX(store_name) as store_name,MAX(issued_to) as issued_to,MAX(depot_to_name) as depot_to_name,sum(quantity) as qty,sum(quantity*dist_rate) as price from sm_issue where "+str(condStr)+" group by depot_id,sl order by sl "
    recordList=db.executesql(sqlStr,as_dict = True) 
    
    myString='25.1 IC Transfer Summary\n'
    myString+='Date From:,'+str(startDt)+'\n'
    myString+='To Date:'+','+str(endDt)+'\n'
    myString+='Branch ID:,'+str(depot_id)+'\n'
    myString+='Branch Name:'+','+str(depotName)+'\n'
    myString+='Store ID:,'+str(store_id)+'\n'
    myString+='Store Name:'+','+str(storeName)+'\n'
    myString+='Transfer To ID:'+','+str(to_depot_id)+'\n'
    myString+='Transfer To Name:'+','+str(to_depot_name)+'\n'
    
    totalQty=0
    totalTP=0
    
    myString+='Transfer No,Date,From Location,To Location,Quantity,Trade Price'+'\n'
    for i in range(len(recordList)):
        dictData=recordList[i]
        depot_id=dictData['depot_id']        
        trNo=str(session.prefix_invoice)+'TR'+str(depot_id)+'-'+str(dictData['sl'])
        issue_date=dictData['issue_date']
        store_id=dictData['store_id']
        store_name=str(dictData['store_name']).replace(',', ' ') 
        issued_to=dictData['issued_to']
        depot_to_name=str(dictData['depot_to_name']).replace(',', ' ') 
        qty=dictData['qty']
        price=dictData['price']
        
        totalQty+=qty        
        
        totalTP+=price
        
        #------------------------        
        myString+=str(trNo)+','+str(issue_date)+','+str(store_id)+':'+str(store_name)+','+str(issued_to)+':'+str(depot_to_name)+','+str(qty)+','+str(price)+'\n'
        
    myString+='Total,,,,'+str(totalQty)+','+str(totalTP)+'\n'
    
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_transferSumamry.csv'   
    return str(myString)

def transferSumDetails():
    c_id=session.cid
    
    response.title='25.4 Transfer Summary and Details'
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    depot_id=str(request.vars.depotID).strip()
    store_id=str(request.vars.storeID).strip()
    
    to_depot_id=str(request.vars.to_depot_id).strip()
    to_depot_name=''
    toDepotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==to_depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if toDepotRow:
        to_depot_name=toDepotRow[0].name
        
    depotName=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depotName=depotRow[0].name
        
    storeName=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        storeName=storeRow[0].store_name
        
    startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d')    
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d')
    
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    headList=[]
    
    qset=db()
    qset=qset(db.sm_issue_head.cid==c_id)
    qset=qset(db.sm_issue_head.depot_id==depot_id)
    qset=qset(db.sm_issue_head.store_id==store_id)
    qset=qset((db.sm_issue_head.issue_date>=startDt)&(db.sm_issue_head.issue_date<=endDt))
    qset=qset(db.sm_issue_head.status=='Posted')
    if to_depot_id!='':
        qset=qset(db.sm_issue_head.issued_to==to_depot_id)
        
    records=qset.select(db.sm_issue_head.ALL,orderby=db.sm_issue_head.issue_date)
    
    for row in records:
        sl=row.sl        
        store_id=row.store_id
        store_name=row.store_name
        issue_date=row.issue_date
        issued_to=row.issued_to
        depot_to_name=row.depot_to_name
        
        try:
            issue_date=issue_date.strftime('%d-%b-%y')
        except:
            issue_date=''
            
        detailList=[]
        hQty=0
        hPrice=0
        detailsRow=db((db.sm_issue.cid==c_id)&(db.sm_issue.depot_id==depot_id)&(db.sm_issue.sl==sl)).select(db.sm_issue.item_id,db.sm_issue.item_name,db.sm_issue.store_id,db.sm_issue.store_name,db.sm_issue.quantity,db.sm_issue.dist_rate,orderby=db.sm_issue.item_id)
        for drow in detailsRow:
            item_id=drow.item_id
            item_name=drow.item_name
            
            quantity=drow.quantity
            price=drow.dist_rate
            
            tprice=quantity*price
            
            hQty+=quantity
            hPrice+=tprice
            
            dictDetData={'itemId':item_id,'itemName':item_name,'storeId':store_id,'storeName':store_name,'qty':str(quantity),'tPrice':str(tprice)}
            detailList.append(dictDetData)
            
        dictHeadData={'slNo':str(session.prefix_invoice)+"TR"+str(depot_id)+"-"+str(sl),'issueDate':str(issue_date),'issued_to_id':issued_to,'depot_to_name':depot_to_name,'hQty':str(hQty),'hPrice':str(hPrice),'dDetails':detailList}
        headList.append(dictHeadData)
        
    return dict(headList=headList,fromDate=fromDate,toDate=toDate,depotID=depot_id,depotName=depotName,storeID=store_id,storeName=storeName,to_depot_id=to_depot_id,to_depot_name=to_depot_name,page=page,items_per_page=items_per_page)    

def transferSumDetails_download():
    c_id=session.cid
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    depot_id=str(request.vars.depotID).strip()
    store_id=str(request.vars.storeID).strip()
    
    to_depot_id=str(request.vars.to_depot_id).strip()
    to_depot_name=''
    toDepotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==to_depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if toDepotRow:
        to_depot_name=toDepotRow[0].name
        
    depotName=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depotName=depotRow[0].name
        
    storeName=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        storeName=storeRow[0].store_name
        
    startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d')    
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d')
    
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    headList=[]
    
    qset=db()
    qset=qset(db.sm_issue_head.cid==c_id)
    qset=qset(db.sm_issue_head.depot_id==depot_id)
    qset=qset(db.sm_issue_head.store_id==store_id)
    qset=qset((db.sm_issue_head.issue_date>=startDt)&(db.sm_issue_head.issue_date<=endDt))    
    qset=qset(db.sm_issue_head.status=='Posted')
    if to_depot_id!='':
        qset=qset(db.sm_issue_head.issued_to==to_depot_id)
        
    records=qset.select(db.sm_issue_head.ALL,orderby=db.sm_issue_head.issue_date)
    
    for row in records:
        sl=row.sl        
        store_id=row.store_id
        store_name=row.store_name
        issue_date=row.issue_date
        issued_to=row.issued_to
        depot_to_name=row.depot_to_name
        
        try:
            issue_date=issue_date.strftime('%d-%b-%y')
        except:
            issue_date=''
            
        detailList=[]
        hQty=0
        hPrice=0
        detailsRow=db((db.sm_issue.cid==c_id)&(db.sm_issue.depot_id==depot_id)&(db.sm_issue.sl==sl)).select(db.sm_issue.item_id,db.sm_issue.item_name,db.sm_issue.store_id,db.sm_issue.store_name,db.sm_issue.quantity,db.sm_issue.dist_rate,orderby=db.sm_issue.item_id)
        for drow in detailsRow:
            item_id=drow.item_id
            item_name=drow.item_name
            
            quantity=drow.quantity
            price=drow.dist_rate
            
            tprice=quantity*price
            
            hQty+=quantity
            hPrice+=tprice
            
            dictDetData={'itemId':item_id,'itemName':item_name,'storeId':store_id,'storeName':store_name,'qty':str(quantity),'tPrice':str(tprice)}
            detailList.append(dictDetData)
            
        dictHeadData={'slNo':str(session.prefix_invoice)+"GR"+str(depot_id)+"-"+str(sl),'issueDate':str(issue_date),'issued_to_id':issued_to,'depot_to_name':depot_to_name,'hQty':str(hQty),'hPrice':str(hPrice),'dDetails':detailList}
        headList.append(dictHeadData)
        
    #-----------------
    myString='25.4 IC Transfer Summery And Details\n'
    myString+='Date From:,'+str(startDt)+'\n'
    myString+='To Date:'+','+str(endDt)+'\n'
    myString+='Branch ID:,'+str(depot_id)+'\n'
    myString+='Branch Name'+','+str(depotName)+'\n'
    myString+='Store ID:,'+str(store_id)+'\n'
    myString+='Store Name'+','+str(storeName)+'\n'
    myString+='Transfer To ID:'+','+str(to_depot_id)+'\n'
    myString+='Transfer To Name:'+','+str(to_depot_name)+'\n'
    
    totalTP=0    
    myString+='Transfer No,Date,Item & Description,,Transfer From,Qty,Trade Price'+'\n'
    
    for i in range(len(headList)):
        dictData=headList[i]
        
        slNo=dictData['slNo']
        issueDate=dictData['issueDate']
        issued_to_id=str(dictData['issued_to_id']).replace(',', ' ')
        depot_to_name=str(dictData['depot_to_name']).replace(',', ' ')
        hQty=dictData['hQty']
        hPrice=dictData['hPrice']
        
        totalTP+=float(hPrice)
        
        if i>0:
            myString+='\n'            
        myString+=str(slNo)+','+str(issueDate)+',To Location:'+str(issued_to_id)+'|'+str(depot_to_name)+',,,'+str(hQty)+','+str(hPrice)+'\n'
        
        detailList=dictData['dDetails']
        for j in range(len(detailList)):
            dictDetData=detailList[j]
            
            itemId=dictDetData['itemId']
            itemName=str(dictDetData['itemName']).replace(',', ' ')
            storeId=dictDetData['storeId']
            storeName=str(dictDetData['storeName']).replace(',', ' ')
            qty=dictDetData['qty']
            tPrice=dictDetData['tPrice']
            
            #------------------------        
            myString+=',,'+str(itemId)+','+str(itemName)+','+str(storeId)+':'+str(storeName)+','+str(qty)+','+str(tPrice)+'\n'
        
    myString+=',,,,,Total Trade Price,'+str(totalTP)+'\n'
    
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_transferSumamryDetails.csv'   
    return str(myString)


def transferSummery_internal():
    c_id=session.cid
    
    response.title='Transfer Summary'
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    depot_id=str(request.vars.depotID).strip()
    store_id=str(request.vars.storeID).strip()
    
    depotName=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depotName=depotRow[0].name
        
    storeName=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        storeName=storeRow[0].store_name
        
    startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d')    
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d')+datetime.timedelta(days=1)
    
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    damageHeadList=[]
    
    qset=db()
    qset=qset(db.sm_damage.cid==c_id)
    qset=qset((db.sm_damage.damage_date>=startDt)&(db.sm_damage.damage_date<endDt))
    qset=qset(db.sm_damage.depot_id==depot_id)
    qset=qset(db.sm_damage.store_id==store_id)
    qset=qset(db.sm_damage.transfer_type=='TRANSFER')
    qset=qset(db.sm_damage.status=='Posted') 
    
    records=qset.select(db.sm_damage.sl,db.sm_damage.damage_date,db.sm_damage.store_id,db.sm_damage.store_name,db.sm_damage.store_id_to,db.sm_damage.store_name_to,db.sm_damage.quantity,db.sm_damage.dist_rate,orderby=db.sm_damage.damage_date)
    
    return dict(records=records,fromDate=fromDate,toDate=toDate,depotID=depot_id,depotName=depotName,storeID=store_id,storeName=storeName,page=page,items_per_page=items_per_page)    
    
def transferSummery_internal_download():
    c_id=session.cid
    
    response.title='Transfer Summary'
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    depot_id=str(request.vars.depotID).strip()
    store_id=str(request.vars.storeID).strip()
    
    depotName=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depotName=depotRow[0].name
        
    storeName=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        storeName=storeRow[0].store_name
        
    startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d')    
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d')+datetime.timedelta(days=1)
    
    #--------------
    damageHeadList=[]
    
    qset=db()
    qset=qset(db.sm_damage.cid==c_id)
    qset=qset((db.sm_damage.damage_date>=startDt)&(db.sm_damage.damage_date<endDt))
    qset=qset(db.sm_damage.depot_id==depot_id)
    qset=qset(db.sm_damage.store_id==store_id)
    qset=qset(db.sm_damage.transfer_type=='TRANSFER')
    qset=qset(db.sm_damage.status=='Posted') 
    
    records=qset.select(db.sm_damage.sl,db.sm_damage.damage_date,db.sm_damage.store_id,db.sm_damage.store_name,db.sm_damage.store_id_to,db.sm_damage.store_name_to,db.sm_damage.quantity,db.sm_damage.dist_rate,orderby=db.sm_damage.damage_date)
    
    myString='25.1 IC Transfer Summary\n'
    myString+='Date From:,'+str(startDt)+'\n'
    myString+='To Date:'+','+str(endDt)+'\n'
    myString+='Branch ID:,'+str(depot_id)+'\n'
    myString+='Branch Name'+','+str(depotName)+'\n'
    myString+='Store ID:,'+str(store_id)+'\n'
    myString+='Store Name'+','+str(storeName)+'\n'
    
    totalQty=0
    totalTP=0
    
    myString+='Transfer No,Date,From Location,To Location,Quantity,Trade Price'+'\n'
    for row in records:
        
        trNo=str(session.prefix_invoice)+'TR-'+str(row.sl)
        damage_date=row.damage_date        
        store_id=str(row.store_id)
        store_name=str(row.store_name).replace(',', ' ')        
        store_id_to=row.store_id_to
        store_name_to=str(row.store_name_to).replace(',', ' ')
        
        quantity=row.quantity
        totalQty+=quantity        
        
        tpAmt=quantity*row.dist_rate
        totalTP+=tpAmt
        
        #------------------------        
        myString+=str(trNo)+','+str(damage_date)+','+str(store_id)+':'+str(store_name)+','+str(store_id_to)+':'+str(store_name_to)+','+str(quantity)+','+str(tpAmt)+'\n'
        
    myString+='Total,,,,'+str(totalQty)+','+str(totalTP)+'\n'
    
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_transferSumamry.csv'   
    return str(myString)


def transferBranchToBranchPreview():
    c_id=session.cid
    
    response.title='Preview-Transfer Branch to Branch Note'
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    depot_id=str(request.vars.depotID).strip()
    store_id=str(request.vars.storeID).strip()
    
    fromDepotID=str(request.vars.fromDepotID).strip()
    depotNameFrom=''
    depotRowFrom=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==fromDepotID)).select(db.sm_depot.name,limitby=(0,1))
    if depotRowFrom:
        depotNameFrom=depotRowFrom[0].name
        
    depotName=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,db.sm_depot.field1,limitby=(0,1))
    if depotRow:
        depotName=depotRow[0].name
        
    storeName=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        storeName=storeRow[0].store_name
        
    startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d')    
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d')
    
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    qset=db()
    qset=qset(db.sm_issue_head.cid==c_id)
    qset=qset(db.sm_issue_head.depot_id==depot_id)
    qset=qset(db.sm_issue_head.store_id==store_id)
    
    qset=qset((db.sm_issue_head.issue_date>=startDt)& (db.sm_issue_head.issue_date<=endDt))
    qset=qset(db.sm_issue_head.status=='Posted')
    
    records=qset.select(db.sm_issue_head.ALL,orderby=db.sm_issue_head.sl)
    
    data_List=[]
    
    for rec in records:
        depotId=rec.depot_id
        sl=rec.sl
        store_id=rec.store_id
        store_name=rec.store_name        
        status=rec.status        
        issued_to=rec.issued_to
        depot_to_name=rec.depot_to_name
        issue_date=rec.issue_date
        note=rec.note        
        ref_sl=rec.req_sl        
        cause=rec.transaction_cause
        updatedBy=rec.updated_by
        
        receive_date=''
        recRows=db((db.sm_receive_head.cid==c_id)& (db.sm_receive_head.receive_from==depotId) & (db.sm_receive_head.ref_sl==sl) & (db.sm_receive_head.status=='Posted')).select(db.sm_receive_head.receive_date,limitby=(0,1))
        if recRows:
            receive_date=recRows[0].receive_date.strftime('%d-%b-%Y')
            
        detDictList=[]
        mCartonTotal=0
        detailRows=db((db.sm_issue.cid==c_id)& (db.sm_issue.depot_id==depotId) & (db.sm_issue.sl==sl)).select(db.sm_issue.ALL,orderby=db.sm_issue.item_name)
        for dRow in detailRows:        
            item_id=dRow.item_id
            item_name=dRow.item_name
            batch_id=dRow.batch_id            
            quantity=dRow.quantity
            bonus_qty=dRow.bonus_qty            
            dist_rate=dRow.dist_rate
            short_note=dRow.short_note 
            expiary_date=dRow.expiary_date           
            item_unit=dRow.item_unit            
            item_carton=dRow.item_carton
            
            try:
                mCarton=round(float(quantity)/item_carton,2)
            except:
                mCarton=0
                
            mCartonTotal+=mCarton
            
            #------------------------
            vdDict= {'item_id': item_id,'item_name': item_name,'batch_id':batch_id,'item_unit':item_unit,'item_carton':item_carton,'expiary_date':expiary_date,'store_id':store_id,'store_name':store_name,'issued_to':issued_to,'depot_to_name':depot_to_name,'quantity': quantity,'price': dist_rate,'short_note': short_note}
            detDictList.append(vdDict)
            
        vhDict={'depot_id':depotId,'depot_name':depotName,'sl':sl,'store_id':store_id,'store_name':store_name,'issue_date':issue_date,'receive_date':receive_date,'status':status,'issued_to':issued_to,'depot_to_name':depot_to_name,'note':note,'ref_sl':ref_sl,'cause':cause,'updatedBy':updatedBy,'mCartonTotal':mCartonTotal,'vdList':detDictList}
        data_List.append(vhDict)
        
    return dict(data_List=data_List,fromDate=fromDate,toDate=toDate,depotID=depot_id,depotName=depotName,storeID=store_id,storeName=storeName,fromDepotID=fromDepotID,depotNameFrom=depotNameFrom,page=page,items_per_page=items_per_page)    


def transferInternalPreview():
    c_id=session.cid
    
    response.title='Preview-Internal Transfer Note'
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    depot_id=str(request.vars.depotID).strip()
    store_id=str(request.vars.storeID).strip()
    
    fromDepotID=str(request.vars.fromDepotID).strip()
    depotNameFrom=''
    depotRowFrom=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==fromDepotID)).select(db.sm_depot.name,limitby=(0,1))
    if depotRowFrom:
        depotNameFrom=depotRowFrom[0].name
        
    depotName=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,db.sm_depot.field1,limitby=(0,1))
    if depotRow:
        depotName=depotRow[0].name
        
    storeName=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        storeName=storeRow[0].store_name
        
    startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d')    
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d')
    
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    qset=db()
    qset=qset(db.sm_damage_head.cid==c_id)
    qset=qset(db.sm_damage_head.depot_id==depot_id)
    qset=qset(db.sm_damage_head.store_id==store_id)
    qset=qset(db.sm_damage_head.transfer_type=='TRANSFER')
    qset=qset((db.sm_damage_head.damage_date>=startDt)& (db.sm_damage_head.damage_date<=endDt))
    qset=qset(db.sm_damage_head.status=='Posted')
    
    records=qset.select(db.sm_damage_head.ALL,orderby=db.sm_damage_head.type_sl)
    
    data_List=[]
    
    for rec in records:
        depotId=rec.depot_id
        type_sl=rec.type_sl
        store_id=rec.store_id
        store_name=rec.store_name        
        status=rec.status        
        issued_to=rec.store_id_to
        depot_to_name=rec.store_name_to
        issue_date=rec.damage_date
        note=rec.note        
        ref_sl=rec.sl   
        cause=rec.adjustment_reference
        updatedBy=rec.updated_by
        
        detDictList=[]
        mCartonTotal=0
        detailRows=db((db.sm_damage.cid==c_id)& (db.sm_damage.depot_id==depotId) & (db.sm_damage.transfer_type=='TRANSFER') & (db.sm_damage.type_sl==type_sl)).select(db.sm_damage.ALL,orderby=db.sm_damage.item_name)
        for dRow in detailRows:        
            item_id=dRow.item_id
            item_name=dRow.item_name
            batch_id=dRow.batch_id            
            quantity=dRow.quantity
                    
            dist_rate=dRow.dist_rate
            short_note=dRow.short_note 
            expiary_date=dRow.expiary_date           
            item_unit=dRow.item_unit            
            item_carton=dRow.item_carton
            
            try:
                mCarton=round(float(quantity)/item_carton,2)
            except:
                mCarton=0
                
            mCartonTotal+=mCarton
            
            #------------------------
            vdDict= {'item_id': item_id,'item_name': item_name,'batch_id':batch_id,'item_unit':item_unit,'item_carton':item_carton,'expiary_date':expiary_date,'store_id':store_id,'store_name':store_name,'issued_to':issued_to,'depot_to_name':depot_to_name,'quantity': quantity,'price': dist_rate,'short_note': short_note}
            detDictList.append(vdDict)
            
        vhDict={'depot_id':depotId,'depot_name':depotName,'type_sl':type_sl,'store_id':store_id,'store_name':store_name,'issue_date':issue_date,'status':status,'issued_to':issued_to,'depot_to_name':depot_to_name,'note':note,'ref_sl':ref_sl,'cause':cause,'updatedBy':updatedBy,'mCartonTotal':mCartonTotal,'vdList':detDictList}
        data_List.append(vhDict)
        
    
    return dict(data_List=data_List,fromDate=fromDate,toDate=toDate,depotID=depot_id,depotName=depotName,storeID=store_id,storeName=storeName,fromDepotID=fromDepotID,depotNameFrom=depotNameFrom,page=page,items_per_page=items_per_page)    



def receiptDetails():
    c_id=session.cid
    
    response.title='24.2 Receipt Details'
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    depot_id=str(request.vars.depotID).strip()
    store_id=str(request.vars.storeID).strip()
    
    fromDepotID=str(request.vars.fromDepotID).strip()
    depotNameFrom=''
    depotRowFrom=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==fromDepotID)).select(db.sm_depot.name,limitby=(0,1))
    if depotRowFrom:
        depotNameFrom=depotRowFrom[0].name
    
    depotName=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depotName=depotRow[0].name
        
    storeName=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        storeName=storeRow[0].store_name
        
    startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d')    
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d')
    
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    recItemList=[]
    
    
    qset=db()
    qset=qset(db.sm_receive.cid==c_id)
    qset=qset(db.sm_receive.depot_id==depot_id)
    qset=qset(db.sm_receive.store_id==store_id)
    if fromDepotID!='':
        qset=qset(db.sm_receive.receive_from==fromDepotID)
        
    qset=qset((db.sm_receive.receive_date>=startDt)&(db.sm_receive.receive_date<=endDt))    
    qset=qset(db.sm_receive.status=='Posted')
    records=qset.select(db.sm_receive.item_id,db.sm_receive.item_name.max(),orderby=db.sm_receive.item_name,groupby=db.sm_receive.item_id)
    
    for row in records:
        item_id=row.sm_receive.item_id
        item_name=row[db.sm_receive.item_name.max()]
        
        recDetailList=[]
        hQty=0
        hTp=0
        
        qset1=db()
        qset1=qset1(db.sm_receive.cid==c_id)
        qset1=qset1(db.sm_receive.depot_id==depot_id)
        qset1=qset1(db.sm_receive.store_id==store_id)
        if fromDepotID!='':
            qset1=qset1(db.sm_receive.receive_from==fromDepotID)
             
        qset1=qset1((db.sm_receive.receive_date>=startDt)&(db.sm_receive.receive_date<=endDt))
        qset1=qset1(db.sm_receive.item_id==item_id)
        qset1=qset1(db.sm_receive.status=='Posted')        
        adjReceiptRow=qset1.select(db.sm_receive.sl,db.sm_receive.receive_date,db.sm_receive.receive_from,db.sm_receive.depot_from_name.max(),db.sm_receive.depot_id,db.sm_receive.depot_name.max(),db.sm_receive.dist_rate,db.sm_receive.quantity.sum(),groupby=db.sm_receive.sl|db.sm_receive.receive_date|db.sm_receive.receive_from|db.sm_receive.depot_id|db.sm_receive.dist_rate,orderby=db.sm_receive.sl)
        
        for drow in adjReceiptRow:
            sl=drow.sm_receive.sl
            receive_date=drow.sm_receive.receive_date
            receive_from=drow.sm_receive.receive_from
            depot_from_name=drow[db.sm_receive.depot_from_name.max()]
            depot_id=drow.sm_receive.depot_id
            depot_name=drow[db.sm_receive.depot_name.max()]
            quantity=drow[db.sm_receive.quantity.sum()]
            price=drow.sm_receive.dist_rate
            tp=quantity*price
            hQty+=quantity
            hTp+=quantity*price
            
            slStr=str(session.prefix_invoice)+'GR'+str(depot_id)+'-'+str(sl)
            
            dictDetData={'slNo':str(slStr),'recDate':receive_date,'receFromDepot':receive_from,'receFromDepotName':depot_from_name,'receToDepot':depot_id,'receToDepotName':depot_name,'qty':str(quantity),'recTp':str(tp)}
            recDetailList.append(dictDetData)
            
        dictHeadData={'ItemID':item_id,'itemName':item_name,'hQty':hQty,'hTp':hTp,'rDetails':recDetailList}
        recItemList.append(dictHeadData)    
    
    return dict(recItemList=recItemList,fromDate=fromDate,toDate=toDate,depotID=depot_id,depotName=depotName,storeID=store_id,storeName=storeName,fromDepotID=fromDepotID,depotNameFrom=depotNameFrom,page=page,items_per_page=items_per_page)    

def receiptDetails_download():
    c_id=session.cid
    
    response.title='Download-Receipt Details'
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    depot_id=str(request.vars.depotID).strip()
    store_id=str(request.vars.storeID).strip()
    
    fromDepotID=str(request.vars.fromDepotID).strip()
    depotNameFrom=''
    depotRowFrom=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==fromDepotID)).select(db.sm_depot.name,limitby=(0,1))
    if depotRowFrom:
        depotNameFrom=depotRowFrom[0].name
    
    depotName=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depotName=depotRow[0].name
        
    storeName=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        storeName=storeRow[0].store_name
        
    startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d')    
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d')
    
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    recItemList=[]
    
    
    qset=db()
    qset=qset(db.sm_receive.cid==c_id)
    qset=qset(db.sm_receive.depot_id==depot_id)
    qset=qset(db.sm_receive.store_id==store_id)
    if fromDepotID!='':
        qset=qset(db.sm_receive.receive_from==fromDepotID)
    
    qset=qset((db.sm_receive.receive_date>=startDt)&(db.sm_receive.receive_date<=endDt))    
    qset=qset(db.sm_receive.status=='Posted')
    records=qset.select(db.sm_receive.item_id,db.sm_receive.item_name.max(),orderby=db.sm_receive.item_name,groupby=db.sm_receive.item_id)
    
    for row in records:
        item_id=row.sm_receive.item_id
        item_name=row[db.sm_receive.item_name.max()]
        
        recDetailList=[]
        hQty=0
        hTp=0
        
        qset1=db()
        qset1=qset1(db.sm_receive.cid==c_id)
        qset1=qset1(db.sm_receive.depot_id==depot_id)
        qset1=qset1(db.sm_receive.store_id==store_id)
        if fromDepotID!='':
            qset1=qset1(db.sm_receive.receive_from==fromDepotID)
            
        qset1=qset1((db.sm_receive.receive_date>=startDt)&(db.sm_receive.receive_date<=endDt))
        qset1=qset1(db.sm_receive.item_id==item_id)
        qset1=qset1(db.sm_receive.status=='Posted')        
        adjReceiptRow=qset1.select(db.sm_receive.sl,db.sm_receive.receive_date,db.sm_receive.receive_from,db.sm_receive.depot_from_name.max(),db.sm_receive.depot_id,db.sm_receive.depot_name.max(),db.sm_receive.dist_rate,db.sm_receive.quantity.sum(),groupby=db.sm_receive.sl|db.sm_receive.receive_date|db.sm_receive.receive_from|db.sm_receive.depot_id|db.sm_receive.dist_rate,orderby=db.sm_receive.sl)
        
        for drow in adjReceiptRow:
            sl=drow.sm_receive.sl
            receive_date=drow.sm_receive.receive_date
            receive_from=drow.sm_receive.receive_from
            depot_from_name=drow[db.sm_receive.depot_from_name.max()]
            depot_id=drow.sm_receive.depot_id
            depot_name=drow[db.sm_receive.depot_name.max()]
            quantity=drow[db.sm_receive.quantity.sum()]
            price=drow.sm_receive.dist_rate
            tp=quantity*price
            hQty+=quantity
            hTp+=quantity*price
            
            slStr=str(session.prefix_invoice)+'GR'+str(depot_id)+'-'+str(sl)
            
            dictDetData={'slNo':str(slStr),'recDate':receive_date,'receFromDepot':receive_from,'receFromDepotName':depot_from_name,'receToDepot':depot_id,'receToDepotName':depot_name,'qty':str(quantity),'recTp':str(tp)}
            recDetailList.append(dictDetData)
            
        dictHeadData={'ItemID':item_id,'itemName':item_name,'hQty':hQty,'hTp':hTp,'rDetails':recDetailList}
        recItemList.append(dictHeadData)    
        
    
    #------------------------------------
    myString='24.2 IC Receipt Details\n'
    myString+='Date From:,'+str(startDt)+'\n'
    myString+='To Date:'+','+str(endDt)+'\n'
    myString+='Branch ID:,'+str(depot_id)+'\n'
    myString+='Branch Name'+','+str(depotName)+'\n'
    myString+='Store ID:,'+str(store_id)+'\n'
    myString+='Store Name'+','+str(storeName)+'\n'
    myString+='Receipt From ID:,`'+str(fromDepotID)+'\n'
    myString+='Receipt From Name'+','+str(depotNameFrom)+'\n'
    
    totalQty=0
    totalTp=0
    
    myString+='Item Id,Item Name,Date,Receipt From,Receipt To,Quantity,Trade Price'+'\n'
    for i in range(len(recItemList)):
        dictData=recItemList[i]
        
        ItemID=dictData['ItemID']
        itemName=str(dictData['itemName']).replace(',', ' ')
        hQty=dictData['hQty']
        totalQty+=hQty
        
        hTp=float(dictData['hTp'])
        totalTp+=hTp
                                                   
        myString+=str(ItemID)+','+str(itemName)+',,,,'+str(hQty)+','+str(hTp)+'\n'
        
        detailList=dictData['rDetails']
        for j in range(len(detailList)):
            dictDetData=detailList[j]
            
            slNo=dictDetData['slNo']
            recDate=dictDetData['recDate']
            receFromDepot=dictDetData['receFromDepot']
            receFromDepotName=str(dictDetData['receFromDepotName']).replace(',', ' ')
            receToDepot=dictDetData['receToDepot']
            receToDepotName=str(dictDetData['receToDepotName']).replace(',', ' ')
            qty=dictDetData['qty']
            recTp=dictDetData['recTp']
            
            myString+=','+str(slNo)+','+str(recDate)+','+str(hTp)+':'+str(receFromDepot)+':'+str(receFromDepotName)+','+str(receToDepot)+':'+str(receToDepotName)+','+str(qty)+','+str(recTp)+'\n'
        
        #------------------------ 
        
    myString+='Total,,,,,'+str(totalQty)+','+str(totalTp)+'\n'
    
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_receiptDetails.csv'   
    return str(myString)
    
def receiptSummery():
    c_id=session.cid
    
    response.title='24.1 Receipt Summary'
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    depot_id=str(request.vars.depotID).strip()
    store_id=str(request.vars.storeID).strip()
    
    fromDepotID=str(request.vars.fromDepotID).strip()
    depotNameFrom=''
    depotRowFrom=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==fromDepotID)).select(db.sm_depot.name,limitby=(0,1))
    if depotRowFrom:
        depotNameFrom=depotRowFrom[0].name
    
    depotName=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depotName=depotRow[0].name
        
    storeName=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        storeName=storeRow[0].store_name
        
    startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d')    
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d')
    
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    
    condStr=" cid='"+str(c_id)+"' and depot_id='"+str(depot_id)+"' and store_id='"+str(store_id)+"' and (receive_date>='"+str(startDt)+"' and receive_date<='"+str(endDt)+"') and status='Posted'"
    if fromDepotID!='':
        condStr+=" and receive_from='"+fromDepotID+"'"
        
    sqlStr="select depot_id,MAX(depot_name) as depot_name,sl,MAX(receive_date) as receive_date,MAX(receive_from) as receive_from,MAX(depot_from_name) as depot_from_name,MAX(status) as status,sum(quantity) as qty,sum(quantity*dist_rate) as price from sm_receive where "+str(condStr)+" group by depot_id,sl order by sl "
    recordList=db.executesql(sqlStr,as_dict = True) 
    
    return dict(recordList=recordList,fromDate=fromDate,toDate=toDate,depotID=depot_id,depotName=depotName,storeID=store_id,fromDepotID=fromDepotID,depotNameFrom=depotNameFrom,storeName=storeName,page=page,items_per_page=items_per_page)    
    
def receiptSummery_download():
    c_id=session.cid
    
    response.title='Download-Receipt Summary'
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    depot_id=str(request.vars.depotID).strip()
    store_id=str(request.vars.storeID).strip()
    
    fromDepotID=str(request.vars.fromDepotID).strip()
    depotNameFrom=''
    depotRowFrom=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==fromDepotID)).select(db.sm_depot.name,limitby=(0,1))
    if depotRowFrom:
        depotNameFrom=depotRowFrom[0].name
    
    depotName=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depotName=depotRow[0].name
        
    storeName=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        storeName=storeRow[0].store_name
        
    startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d')    
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d')
    
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    
    condStr=" cid='"+str(c_id)+"' and depot_id='"+str(depot_id)+"' and store_id='"+str(store_id)+"' and (receive_date>='"+str(startDt)+"' and receive_date<='"+str(endDt)+"') and status='Posted'"
    if fromDepotID!='':
        condStr+=" and receive_from='"+fromDepotID+"'"
        
    sqlStr="select depot_id,MAX(depot_name) as depot_name,sl,MAX(receive_date) as receive_date,MAX(receive_from) as receive_from,MAX(depot_from_name) as depot_from_name,MAX(status) as status,sum(quantity) as qty,sum(quantity*dist_rate) as price from sm_receive where "+str(condStr)+" group by depot_id,sl order by sl "
    recordList=db.executesql(sqlStr,as_dict = True) 
    
    #------------------------------------
    myString='24.1 Receipt Summary\n'
    myString+='Date From:,'+str(startDt)+'\n'
    myString+='To Date:'+','+str(endDt)+'\n'
    myString+='Branch ID:,'+str(depot_id)+'\n'
    myString+='Branch Name'+','+str(depotName)+'\n'
    myString+='Store ID:,'+str(store_id)+'\n'
    myString+='Store Name'+','+str(storeName)+'\n'
    myString+='Receipt From ID:,`'+str(fromDepotID)+'\n'
    myString+='Receipt From Name'+','+str(depotNameFrom)+'\n'
    
    totalQty=0
    totalTP=0
    slRow=0
    
    myString+='Sl,Rpt. Date,Receipt No,Receipt From,Receipt To,Status,Trade Price'+'\n'
    for i in range(len(recordList)):
        dictData=recordList[i]
        
        slRow+=1
        receive_date=dictData['receive_date']   
        trNo=str(session.prefix_invoice)+'GR'+str(dictData['depot_id'])+'-'+str(dictData['sl'])
        receive_from=dictData['receive_from']
        depot_from_name=str(dictData['depot_from_name']).replace(',', ' ')
        
        depot_id=dictData['depot_id']
        depot_name=dictData['depot_name']
        
        status=dictData['status']
        
        price=dictData['price']
        
        totalTP+=price
        
        #------------------------        
        myString+=str(slRow)+','+str(receive_date)+','+str(trNo)+','+str(receive_from)+':'+str(depot_from_name)+','+str(depot_id)+':'+str(depot_name)+','+str(status)+','+str(price)+'\n'
        
    myString+='Total Trade Price,,,,,,'+str(totalTP)+'\n'
    
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_receiptSumamry.csv'   
    return str(myString)

def receiveSummeryItemWise():
    c_id=session.cid
    
    response.title='24.3 Receive Summary Item Wise'
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    depot_id=str(request.vars.depotID).strip()
    store_id=str(request.vars.storeID).strip()
    
    fromDepotID=str(request.vars.fromDepotID).strip()
    depotNameFrom=''
    depotRowFrom=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==fromDepotID)).select(db.sm_depot.name,limitby=(0,1))
    if depotRowFrom:
        depotNameFrom=depotRowFrom[0].name
        
    depotName=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depotName=depotRow[0].name
        
    storeName=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        storeName=storeRow[0].store_name
        
    startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d')    
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d')
    
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    
    qset=db()
    qset=qset(db.sm_receive.cid==c_id)
    qset=qset(db.sm_receive.depot_id==depot_id)
    qset=qset(db.sm_receive.store_id==store_id)
    if fromDepotID!='':
        qset=qset(db.sm_receive.receive_from==fromDepotID)
        
    qset=qset((db.sm_receive.receive_date>=startDt)&(db.sm_receive.receive_date<=endDt))    
    qset=qset(db.sm_receive.status=='Posted')
    records=qset.select(db.sm_receive.item_id,db.sm_receive.item_name.max(),db.sm_receive.dist_rate,db.sm_receive.quantity.sum(),orderby=db.sm_receive.item_name|db.sm_receive.dist_rate,groupby=db.sm_receive.item_id|db.sm_receive.dist_rate)
    
    return dict(records=records,fromDate=fromDate,toDate=toDate,depotID=depot_id,depotName=depotName,storeID=store_id,storeName=storeName,fromDepotID=fromDepotID,depotNameFrom=depotNameFrom,page=page,items_per_page=items_per_page)    
    
def receiveSummeryItemWise_download():
    c_id=session.cid
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    depot_id=str(request.vars.depotID).strip()
    store_id=str(request.vars.storeID).strip()
    
    fromDepotID=str(request.vars.fromDepotID).strip()
    depotNameFrom=''
    depotRowFrom=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==fromDepotID)).select(db.sm_depot.name,limitby=(0,1))
    if depotRowFrom:
        depotNameFrom=depotRowFrom[0].name
    
    depotName=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depotName=depotRow[0].name
        
    storeName=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        storeName=storeRow[0].store_name
        
    startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d')    
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d')
    
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    
    qset=db()
    qset=qset(db.sm_receive.cid==c_id)
    qset=qset(db.sm_receive.depot_id==depot_id)
    qset=qset(db.sm_receive.store_id==store_id)
    if fromDepotID!='':
        qset=qset(db.sm_receive.receive_from==fromDepotID)
        
    qset=qset((db.sm_receive.receive_date>=startDt)&(db.sm_receive.receive_date<=endDt))    
    qset=qset(db.sm_receive.status=='Posted')
    records=qset.select(db.sm_receive.item_id,db.sm_receive.item_name.max(),db.sm_receive.dist_rate,db.sm_receive.quantity.sum(),orderby=db.sm_receive.item_name|db.sm_receive.dist_rate,groupby=db.sm_receive.item_id|db.sm_receive.dist_rate)
    
    #-----------
    myString='24.3 Receipt Summary (Item Wise)\n'
    myString+='Date From:,'+str(startDt)+'\n'
    myString+='To Date:'+','+str(endDt)+'\n'
    myString+='Branch ID:,'+str(depot_id)+'\n'
    myString+='Branch Name'+','+str(depotName)+'\n'
    myString+='Store ID:,'+str(store_id)+'\n'
    myString+='Store Name'+','+str(storeName)+'\n'
    myString+='Receipt From ID:,`'+str(fromDepotID)+'\n'
    myString+='Receipt From Name'+','+str(depotNameFrom)+'\n'
    
    totalQty=0
    totalTP=0
    
    myString+='Item Id,Item Name,Trade Price,Quantity,Total Amount'+'\n'
    for row in records:
        item_id=row.sm_receive.item_id
        item_name=str(row[db.sm_receive.item_name.max()]).replace(',', ' ') 
        dist_rate=row.sm_receive.dist_rate
        qty=row[db.sm_receive.quantity.sum()]
        
        totalQty+=qty
        
        price=qty*row.sm_receive.dist_rate
                
        totalTP+=price
        
        #------------------------        
        myString+=str(item_id)+','+str(item_name)+','+str(dist_rate)+','+str(qty)+','+str(price)+'\n'
        
    myString+='Total,,,'+str(totalQty)+','+str(totalTP)+'\n'
    
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_receiptSumamryItemwise.csv'   
    return str(myString)
    
def receiptSumDetails():
    c_id=session.cid
    
    response.title='24.4 Receipt Summary And Details'
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    depot_id=str(request.vars.depotID).strip()
    store_id=str(request.vars.storeID).strip()
    
    fromDepotID=str(request.vars.fromDepotID).strip()
    depotNameFrom=''
    depotRowFrom=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==fromDepotID)).select(db.sm_depot.name,limitby=(0,1))
    if depotRowFrom:
        depotNameFrom=depotRowFrom[0].name
    
    depotName=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depotName=depotRow[0].name
        
    storeName=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        storeName=storeRow[0].store_name
        
    startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d')    
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d')
    
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    headList=[]
    
    qset=db()
    qset=qset(db.sm_receive_head.cid==c_id)
    qset=qset(db.sm_receive_head.depot_id==depot_id)
    qset=qset(db.sm_receive_head.store_id==store_id)
    if fromDepotID!='':
        qset=qset(db.sm_receive_head.receive_from==fromDepotID)
        
    qset=qset((db.sm_receive_head.receive_date>=startDt)&(db.sm_receive_head.receive_date<=endDt))    
    qset=qset(db.sm_receive_head.status=='Posted')
    records=qset.select(db.sm_receive_head.ALL,orderby=db.sm_receive_head.receive_date)
    
    for row in records:
        sl=row.sl        
        store_id=row.store_id
        store_name=row.store_name
        receive_date=row.receive_date
        receive_from=row.receive_from
        depot_from_name=row.depot_from_name
        
        try:
            receive_date=receive_date.strftime('%d-%b-%y')
        except:
            receive_date=''
            
        detailList=[]
        hQty=0
        hPrice=0
        detailsRow=db((db.sm_receive.cid==c_id)&(db.sm_receive.depot_id==depot_id)&(db.sm_receive.sl==sl)).select(db.sm_receive.item_id,db.sm_receive.item_name,db.sm_receive.store_id,db.sm_receive.store_name,db.sm_receive.quantity,db.sm_receive.dist_rate,orderby=db.sm_receive.item_id)
        for drow in detailsRow:
            item_id=drow.item_id
            item_name=drow.item_name
            
            quantity=drow.quantity
            price=drow.dist_rate
            
            tprice=quantity*price
            
            hQty+=quantity
            hPrice+=tprice
            
            dictDetData={'itemId':item_id,'itemName':item_name,'storeId':store_id,'storeName':store_name,'qty':str(quantity),'tPrice':str(tprice)}
            detailList.append(dictDetData)
            
        dictHeadData={'slNo':str(session.prefix_invoice)+"GR"+str(depot_id)+"-"+str(sl),'receiveDate':str(receive_date),'receiveFromID':receive_from,'receiveFromName':depot_from_name,'hQty':str(hQty),'hPrice':str(hPrice),'dDetails':detailList}
        headList.append(dictHeadData)
        
    return dict(headList=headList,fromDate=fromDate,toDate=toDate,depotID=depot_id,depotName=depotName,storeID=store_id,storeName=storeName,fromDepotID=fromDepotID,depotNameFrom=depotNameFrom,page=page,items_per_page=items_per_page)    

def receiptSumDetails_download():
    c_id=session.cid
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    depot_id=str(request.vars.depotID).strip()
    store_id=str(request.vars.storeID).strip()
    
    fromDepotID=str(request.vars.fromDepotID).strip()
    depotNameFrom=''
    depotRowFrom=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==fromDepotID)).select(db.sm_depot.name,limitby=(0,1))
    if depotRowFrom:
        depotNameFrom=depotRowFrom[0].name
        
    depotName=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depotName=depotRow[0].name
        
    storeName=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        storeName=storeRow[0].store_name
        
    startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d')    
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d')
    
    #--------------
    headList=[]
    
    qset=db()
    qset=qset(db.sm_receive_head.cid==c_id)
    qset=qset(db.sm_receive_head.depot_id==depot_id)
    qset=qset(db.sm_receive_head.store_id==store_id)
    if fromDepotID!='':
        qset=qset(db.sm_receive_head.receive_from==fromDepotID)
    qset=qset((db.sm_receive_head.receive_date>=startDt)&(db.sm_receive_head.receive_date<=endDt))    
    qset=qset(db.sm_receive_head.status=='Posted')
    records=qset.select(db.sm_receive_head.ALL,orderby=db.sm_receive_head.receive_date)
    
    for row in records:
        sl=row.sl        
        store_id=row.store_id
        store_name=row.store_name
        receive_date=row.receive_date
        receive_from=row.receive_from
        depot_from_name=row.depot_from_name
        
        try:
            receive_date=receive_date.strftime('%d-%b-%y')
        except:
            receive_date=''
            
        detailList=[]
        hQty=0
        hPrice=0
        detailsRow=db((db.sm_receive.cid==c_id)&(db.sm_receive.depot_id==depot_id)&(db.sm_receive.sl==sl)).select(db.sm_receive.item_id,db.sm_receive.item_name,db.sm_receive.store_id,db.sm_receive.store_name,db.sm_receive.quantity,db.sm_receive.dist_rate,orderby=db.sm_receive.item_id)
        for drow in detailsRow:
            item_id=drow.item_id
            item_name=drow.item_name
            
            quantity=drow.quantity
            price=drow.dist_rate
            
            tprice=quantity*price
            
            hQty+=quantity
            hPrice+=tprice
            
            dictDetData={'itemId':item_id,'itemName':item_name,'storeId':store_id,'storeName':store_name,'qty':str(quantity),'tPrice':str(tprice)}
            detailList.append(dictDetData)
            
        dictHeadData={'slNo':str(session.prefix_invoice)+"GR"+str(depot_id)+"-"+str(sl),'receiveDate':str(receive_date),'receiveFromID':receive_from,'receiveFromName':depot_from_name,'hQty':str(hQty),'hPrice':str(hPrice),'dDetails':detailList}
        headList.append(dictHeadData)
        
    #-----------------
    myString='24.4 Receipt Summery And Details\n'
    myString+='Date From:,'+str(startDt)+'\n'
    myString+='To Date:'+','+str(endDt)+'\n'
    myString+='Branch ID:,'+str(depot_id)+'\n'
    myString+='Branch Name'+','+str(depotName)+'\n'
    myString+='Store ID:,'+str(store_id)+'\n'
    myString+='Store Name'+','+str(storeName)+'\n'
    myString+='Receipt From ID:,`'+str(fromDepotID)+'\n'
    myString+='Receipt From Name'+','+str(depotNameFrom)+'\n'
    
    totalTP=0    
    myString+='Receipt No,Receipt Date,Item & Description,,Receipt To,Qty,Trade Price'+'\n'
    
    for i in range(len(headList)):
        dictData=headList[i]
        
        slNo=dictData['slNo']
        receiveDate=dictData['receiveDate']
        receiveFromID=str(dictData['receiveFromID']).replace(',', ' ')
        receiveFromName=str(dictData['receiveFromName']).replace(',', ' ')
        hQty=dictData['hQty']
        hPrice=dictData['hPrice']
        
        totalTP+=float(hPrice)
        
        if i>0:
            myString+='\n'            
        myString+=str(slNo)+','+str(receiveDate)+',Receipt From:'+str(receiveFromID)+'|'+str(receiveFromName)+',,,'+str(hQty)+','+str(hPrice)+'\n'
        
        detailList=dictData['dDetails']
        for j in range(len(detailList)):
            dictDetData=detailList[j]
            
            itemId=dictDetData['itemId']
            itemName=str(dictDetData['itemName']).replace(',', ' ')
            storeId=dictDetData['storeId']
            storeName=str(dictDetData['storeName']).replace(',', ' ')
            qty=dictDetData['qty']
            tPrice=dictDetData['tPrice']
            
            #------------------------        
            myString+=',,'+str(itemId)+','+str(itemName)+','+str(storeId)+':'+str(storeName)+','+str(qty)+','+str(tPrice)+'\n'
        
    myString+=',,,,,Total Trade Price,'+str(totalTP)+'\n'
    
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_receiptSumamryDetails.csv'   
    return str(myString)


def grNotePreview():
    c_id=session.cid
    
    response.title='Preview-GR Note'
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    depot_id=str(request.vars.depotID).strip()
    store_id=str(request.vars.storeID).strip()
    
    fromDepotID=str(request.vars.fromDepotID).strip()
    depotNameFrom=''
    depotRowFrom=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==fromDepotID)).select(db.sm_depot.name,limitby=(0,1))
    if depotRowFrom:
        depotNameFrom=depotRowFrom[0].name
        
    depotName=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depotName=depotRow[0].name
        
    storeName=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        storeName=storeRow[0].store_name
        
    startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d')    
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d')
    
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    
    qset=db()
    qset=qset(db.sm_receive_head.cid==c_id)
    qset=qset(db.sm_receive_head.depot_id==depot_id)
    qset=qset(db.sm_receive_head.store_id==store_id)
    if fromDepotID!='':
        qset=qset(db.sm_receive_head.receive_from==fromDepotID)
    
    qset=qset((db.sm_receive_head.receive_date>=startDt)& (db.sm_receive_head.receive_date<=endDt))
    qset=qset(db.sm_receive_head.status=='Posted')
    
    records=qset.select(db.sm_receive_head.ALL,orderby=db.sm_receive_head.sl)
    
    data_List=[]
    
    for rec in records:
        depotId=rec.depot_id
        sl=rec.sl
        store_id=rec.store_id
        store_name=rec.store_name        
        status=rec.status        
        receive_from=rec.receive_from
        depot_from_name=rec.depot_from_name
        receive_date=rec.receive_date
        note=rec.note
        discount=rec.total_discount
        ref_sl=rec.ref_sl        
        cause=rec.transaction_cause
        updatedBy=rec.updated_by
        
        detDictList=[]
        mCartonTotal=0
        detailRows=db((db.sm_receive.cid==c_id)& (db.sm_receive.depot_id==depotId) & (db.sm_receive.sl==sl)).select(db.sm_receive.ALL,orderby=db.sm_receive.item_name)
        for dRow in detailRows:        
            item_id=dRow.item_id
            item_name=dRow.item_name
            batch_id=dRow.batch_id            
            quantity=dRow.quantity
            bonus_qty=dRow.bonus_qty            
            dist_rate=dRow.dist_rate
            short_note=dRow.short_note 
            expiary_date=dRow.expiary_date           
            item_unit=dRow.item_unit            
            item_carton=dRow.item_carton
            
            try:
                mCarton=round(float(quantity)/item_carton,2)
            except:
                mCarton=0
                
            mCartonTotal+=mCarton
            
            #------------------------
            vdDict= {'item_id': item_id,'item_name': item_name,'batch_id':batch_id,'item_unit':item_unit,'item_carton':item_carton,'expiary_date':expiary_date,'store_id':store_id,'store_name':store_name,'quantity': quantity,'price': dist_rate,'short_note': short_note}
            detDictList.append(vdDict)
            
        vhDict={'depot_id':depotId,'depot_name':depotName,'sl':sl,'store_id':store_id,'store_name':store_name,'receive_date':receive_date,'status':status,'receive_from':receive_from,'depot_from_name':depot_from_name,'note':note,'ref_sl':ref_sl,'cause':cause,'updatedBy':updatedBy,'mCartonTotal':mCartonTotal,'vdList':detDictList}
        data_List.append(vhDict)
        
    
    return dict(data_List=data_List,fromDate=fromDate,toDate=toDate,depotID=depot_id,depotName=depotName,storeID=store_id,storeName=storeName,fromDepotID=fromDepotID,depotNameFrom=depotNameFrom,page=page,items_per_page=items_per_page)    


def adjustmentSumDetails():
    c_id=session.cid
    
    response.title='23.4 Adjustment Summary And Details'
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    depot_id=str(request.vars.depotID).strip()
    store_id=str(request.vars.storeID).strip()
    
    depotName=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depotName=depotRow[0].name
        
    storeName=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        storeName=storeRow[0].store_name
        
    startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d')    
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d')
    
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    damageHeadList=[]
    
    qset=db()
    qset=qset(db.sm_damage_head.cid==c_id)
    qset=qset(db.sm_damage_head.depot_id==depot_id)
    qset=qset(db.sm_damage_head.store_id==store_id)
    qset=qset((db.sm_damage_head.damage_date>=startDt)&(db.sm_damage_head.damage_date<=endDt))
    
    qset=qset(db.sm_damage_head.transfer_type=='ADJUSTMENT')
    qset=qset(db.sm_damage_head.status=='Posted')    
    
    records=qset.select(db.sm_damage_head.ALL,orderby=db.sm_damage_head.damage_date,limitby=limitby)
    
    for row in records:
        sl=row.sl
        type_sl=row.type_sl
        store_id=row.store_id
        store_name=row.store_name
        damage_date=row.damage_date
        adjustment_reference=row.adjustment_reference
        adjustment_type_head=row.note
        
        try:
            damage_date=damage_date.strftime('%d-%b-%y')
        except:
            damage_date=''
            
        damageDetailList=[]
        hQty=0
        hPrice=0
        adjDetailsRow=db((db.sm_damage.cid==c_id)&(db.sm_damage.depot_id==depot_id)&(db.sm_damage.sl==sl)).select(db.sm_damage.item_id,db.sm_damage.item_name,db.sm_damage.adjustment_type,db.sm_damage.store_id,db.sm_damage.store_name,db.sm_damage.quantity,db.sm_damage.dist_rate,orderby=db.sm_damage.item_id)
        for drow in adjDetailsRow:
            item_id=drow.item_id
            item_name=drow.item_name
            adjustment_type=drow.adjustment_type
            
            qty=drow.quantity
            price=drow.dist_rate
            
            if adjustment_type=='Decrease':
                quantity=qty*(-1)                
            else:
                quantity=qty
                
            cost_adj=quantity*price
            
            hQty+=quantity
            hPrice+=cost_adj
                  
            dictDetData={'itemId':item_id,'itemName':item_name,'adjType':adjustment_type,'storeId':store_id,'storeName':store_name,'qty':str(quantity),'costAdj':str(cost_adj)}
            damageDetailList.append(dictDetData)
            
        dictHeadData={'AdjNo':str(session.prefix_invoice)+"AD-"+str(type_sl),'damageDate':str(damage_date),'adjRef':adjustment_reference,'adjType':adjustment_type_head,'hQty':str(hQty),'hPrice':str(hPrice),'dDetails':damageDetailList}
        damageHeadList.append(dictHeadData)    
        
    
    return dict(damageHeadList=damageHeadList,fromDate=fromDate,toDate=toDate,depotID=depot_id,depotName=depotName,storeID=store_id,storeName=storeName,page=page,items_per_page=items_per_page)    

def adjustmentSumDetails_download():
    c_id=session.cid
    
    response.title='Adjustment Summary And Details'
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    depot_id=str(request.vars.depotID).strip()
    store_id=str(request.vars.storeID).strip()
    
    depotName=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depotName=depotRow[0].name
        
    storeName=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        storeName=storeRow[0].store_name
        
    startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d')    
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d')+datetime.timedelta(days=1)
    
    #--------------
    damageHeadList=[]
    
    qset=db()
    qset=qset(db.sm_damage_head.cid==c_id)
    qset=qset((db.sm_damage_head.damage_date>=startDt)&(db.sm_damage_head.damage_date<endDt))
    qset=qset(db.sm_damage_head.depot_id==depot_id)
    qset=qset(db.sm_damage_head.store_id==store_id)
    qset=qset(db.sm_damage_head.transfer_type=='ADJUSTMENT')
    qset=qset(db.sm_damage_head.status=='Posted')    
    
    records=qset.select(db.sm_damage_head.ALL,orderby=db.sm_damage_head.damage_date)
    
    for row in records:
        sl=row.sl
        type_sl=row.type_sl
        store_id=row.store_id
        store_name=row.store_name
        damage_date=row.damage_date
        adjustment_reference=row.adjustment_reference
        adjustment_type_head=row.note
        
        try:
            damage_date=damage_date.strftime('%d-%b-%y')
        except:
            damage_date=''
        
        damageDetailList=[]
        hQty=0
        hPrice=0
        adjDetailsRow=db((db.sm_damage.cid==c_id)&(db.sm_damage.depot_id==depot_id)&(db.sm_damage.sl==sl)).select(db.sm_damage.item_id,db.sm_damage.item_name,db.sm_damage.adjustment_type,db.sm_damage.store_id,db.sm_damage.store_name,db.sm_damage.quantity,db.sm_damage.dist_rate,orderby=db.sm_damage.item_id)
        for drow in adjDetailsRow:
            item_id=drow.item_id
            item_name=drow.item_name
            adjustment_type=drow.adjustment_type
            
            qty=drow.quantity
            price=drow.dist_rate
                        
            if adjustment_type=='Decrease':
                quantity=qty*(-1)                
            else:
                quantity=qty
            
            cost_adj=quantity*price
            
            hQty+=quantity
            hPrice+=cost_adj
                  
            dictDetData={'itemId':item_id,'itemName':item_name,'adjType':adjustment_type,'storeId':store_id,'storeName':store_name,'qty':str(quantity),'costAdj':str(cost_adj)}
            damageDetailList.append(dictDetData)
            
        dictHeadData={'AdjNo':str(session.prefix_invoice)+"AD-"+str(type_sl),'damageDate':str(damage_date),'adjRef':adjustment_reference,'adjType':adjustment_type_head,'hQty':str(hQty),'hPrice':str(hPrice),'dDetails':damageDetailList}
        damageHeadList.append(dictHeadData)    
        
    
    myString='23.4 IC Adjustment Summary And Details\n'
    myString+='Date From:,'+str(startDt)+'\n'
    myString+='To Date:'+','+str(endDt)+'\n'
    myString+='Branch ID:,'+str(depot_id)+'\n'
    myString+='Branch Name'+','+str(depotName)+'\n'
    myString+='Store ID:,'+str(store_id)+'\n'
    myString+='Store Name'+','+str(storeName)+'\n'
    
    totalAdj=0    
    myString+='Adj. No,Adj. Date,ItemID, Description,Adj. Location,Type,Qty,Cost Adj.'+'\n'
    
    for i in range(len(damageHeadList)):
        dictData=damageHeadList[i]
        
        AdjNo=dictData['AdjNo']
        damageDate=dictData['damageDate']
        adjRef=str(dictData['adjRef']).replace(',', ' ')
        adjType=str(dictData['adjType']).replace(',', ' ')
        hQty=dictData['hQty']
        hPrice=dictData['hPrice']
        
        
        totalAdj+=float(hPrice)
        
        if i>0:
            myString+='\n'            
        myString+=str(AdjNo)+','+str(damageDate)+',,Cause:'+str(adjRef)+',,'+str(adjType)+','+str(hQty)+','+str(hPrice)+'\n'
        
        detailList=dictData['dDetails']
        for j in range(len(detailList)):
            dictDetData=detailList[j]
            
            itemId=dictDetData['itemId']
            itemName=str(dictDetData['itemName']).replace(',', ' ')
            storeId=dictDetData['storeId']
            storeName=str(dictDetData['storeName']).replace(',', ' ')
            adjType=str(dictDetData['adjType']).replace(',', ' ')
            qty=dictDetData['qty']
            costAdj=dictDetData['costAdj']
            
            #------------------------        
            myString+=',,'+str(itemId)+','+str(itemName)+','+str(storeId)+':'+str(storeName)+','+str(adjType)+','+str(qty)+','+str(costAdj)+'\n'
        
    myString+=',,,,,,Total Trade Price,'+str(totalAdj)+'\n'
    
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_AdjustmentSumamryDetails.csv'   
    return str(myString)

def adjustmentSummery():
    c_id=session.cid
    
    response.title='23.1 Adjustment Summary'
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    depot_id=str(request.vars.depotID).strip()
    store_id=str(request.vars.storeID).strip()
    adjustment_cause=str(request.vars.adjustment_cause).strip()
    
    depotName=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depotName=depotRow[0].name
        
    storeName=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        storeName=storeRow[0].store_name
        
    startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d')    
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d')
    
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    
    condStr=" cid='"+str(c_id)+"' and depot_id='"+str(depot_id)+"' and store_id='"+str(store_id)+"' and (damage_date>='"+str(startDt)+"' and damage_date<='"+str(endDt)+"') and transfer_type='ADJUSTMENT' and status='Posted'"
    if adjustment_cause!='':
        condStr+=" and adjustment_reference='"+str(adjustment_cause)+"'"
        
    sqlStr="select depot_id,type_sl,store_id,MAX(store_name) as store_name,MAX(damage_date) as damage_date,MAX(adjustment_reference) as adjustment_reference,MAX(adjustment_type) as adjustment_type,sum(quantity) as qty,sum(quantity*dist_rate) as price from sm_damage where "+str(condStr)+" group by depot_id,type_sl,store_id order by type_sl "
    recordList=db.executesql(sqlStr,as_dict = True) 
    
    return dict(recordList=recordList,fromDate=fromDate,toDate=toDate,depotID=depot_id,depotName=depotName,storeID=store_id,storeName=storeName,adjustment_cause=adjustment_cause,page=page,items_per_page=items_per_page)    


def adjustmentSummery_download():
    c_id=session.cid
    
    response.title='Download-Adjustment Summary'
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    depot_id=str(request.vars.depotID).strip()
    store_id=str(request.vars.storeID).strip()
    adjustment_cause=str(request.vars.adjustment_cause).strip()
    
    depotName=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depotName=depotRow[0].name
        
    storeName=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        storeName=storeRow[0].store_name
        
    startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d')    
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d')+datetime.timedelta(days=1)
    
    #--------------
    
    condStr=" cid='"+str(c_id)+"' and depot_id='"+str(depot_id)+"' and store_id='"+str(store_id)+"' and (damage_date>='"+str(startDt)+"' and damage_date<='"+str(endDt)+"') and transfer_type='ADJUSTMENT' and status='Posted'"
    if adjustment_cause!='':
        condStr+=" and adjustment_reference='"+str(adjustment_cause)+"'"
        
    sqlStr="select depot_id,type_sl,store_id,MAX(store_name) as store_name,MAX(damage_date) as damage_date,MAX(adjustment_reference) as adjustment_reference,MAX(adjustment_type) as adjustment_type,sum(quantity) as qty,sum(quantity*dist_rate) as price from sm_damage where "+str(condStr)+" group by depot_id,type_sl,store_id order by type_sl "
    recordList=db.executesql(sqlStr,as_dict = True) 
    
    
    myString='23.1 IC Adjustment Summary\n'
    myString+='Date From:,'+str(startDt)+'\n'
    myString+='To Date:'+','+str(endDt)+'\n'
    myString+='Branch ID:,'+str(depot_id)+'\n'
    myString+='Branch Name'+','+str(depotName)+'\n'
    myString+='Store ID:,'+str(store_id)+'\n'
    myString+='Store Name'+','+str(storeName)+'\n'
    myString+='Cause of Adjustment'+','+str(adjustment_cause)+'\n'
    
    totalAdj=0    
    myString+='Adj. No,Date,Adj. Description,Type,Qty,Cost Adj.'+'\n'
    
    for i in range(len(recordList)):
        dictData=recordList[i]
        
        AdjNo=str(session.prefix_invoice)+'AD'+str(dictData['depot_id'])+'-'+str(dictData['type_sl'])
        
        damageDate=dictData['damage_date']
        adjRef=str(dictData['adjustment_reference']).replace(',', ' ')
        adjType=str(dictData['adjustment_type']).replace(',', ' ')
        hQty=dictData['qty']
        
        hPrice=0
        if dictData['adjustment_type']=='Decrease':
            hPrice=float(dictData['price'])*(-1)
            hQty=hQty*(-1)
        else:
            hPrice=float(dictData['price'])
            
        totalAdj+=float(hPrice)
                 
        myString+=str(AdjNo)+','+str(damageDate)+',Cause:'+str(adjRef)+','+str(adjType)+','+str(hQty)+','+str(hPrice)+'\n'
        
        
        
    myString+=',,,,Total Trade Price,'+str(totalAdj)+'\n'
    
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_AdjustmentSumamry.csv'   
    return str(myString)
    
def adjustmentDetails():
    c_id=session.cid
    
    response.title='23.2 Adjustment Details'
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    depot_id=str(request.vars.depotID).strip()
    store_id=str(request.vars.storeID).strip()
    
    depotName=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depotName=depotRow[0].name
        
    storeName=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        storeName=storeRow[0].store_name
        
    startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d')    
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d')
    
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    recItemList=[]
    
    qset=db()
    qset=qset(db.sm_damage.cid==c_id)
    qset=qset(db.sm_damage.depot_id==depot_id)
    qset=qset(db.sm_damage.store_id==store_id)
    qset=qset((db.sm_damage.damage_date>=startDt)&(db.sm_damage.damage_date<=endDt))    
    qset=qset(db.sm_damage.transfer_type=='ADJUSTMENT')
    qset=qset(db.sm_damage.status=='Posted')
    
    records=qset.select(db.sm_damage.item_id,db.sm_damage.item_name.max(),orderby=db.sm_damage.item_name,groupby=db.sm_damage.item_id)
    
    for row in records:
        item_id=row.sm_damage.item_id
        item_name=row[db.sm_damage.item_name.max()]
        
        recDetailList=[]
        hQty=0
        hTp=0
        
        qset1=db()
        qset1=qset1(db.sm_damage.cid==c_id)
        qset1=qset1(db.sm_damage.depot_id==depot_id)
        qset1=qset1(db.sm_damage.store_id==store_id)
        qset1=qset1((db.sm_damage.damage_date>=startDt)&(db.sm_damage.damage_date<=endDt))        
        qset1=qset1(db.sm_damage.item_id==item_id)
        qset1=qset1(db.sm_damage.transfer_type=='ADJUSTMENT')
        qset1=qset1(db.sm_damage.status=='Posted')        
        adjReceiptRow=qset1.select(db.sm_damage.depot_id,db.sm_damage.type_sl,db.sm_damage.damage_date,db.sm_damage.store_id,db.sm_damage.store_name,db.sm_damage.adjustment_type,db.sm_damage.quantity,db.sm_damage.dist_rate,orderby=db.sm_damage.type_sl)
        
        for drow in adjReceiptRow:
            depot_id=drow.depot_id
            type_sl=drow.type_sl
            damage_date=drow.damage_date
            store_id=drow.store_id
            store_name=drow.store_name
            adjustment_type=drow.adjustment_type
            quantity=drow.quantity
            
            if adjustment_type=='Decrease':
                quantity=quantity*(-1)                                
            else:
                pass
                
            price=drow.dist_rate
            tp=quantity*price
            hQty+=quantity
            hTp+=quantity*price
            
            slStr=str(session.prefix_invoice)+'AD'+str(depot_id)+'-'+str(type_sl)
            
            dictDetData={'slNo':str(slStr),'recDate':damage_date,'trFrom':store_id,'trFromName':store_name,'adjType':adjustment_type,'qty':str(quantity),'recTp':str(tp)}
            recDetailList.append(dictDetData)
            
        dictHeadData={'ItemID':item_id,'itemName':item_name,'hQty':hQty,'hTp':hTp,'rDetails':recDetailList}
        recItemList.append(dictHeadData)    
        
    return dict(recItemList=recItemList,fromDate=fromDate,toDate=toDate,depotID=depot_id,depotName=depotName,storeID=store_id,storeName=storeName,page=page,items_per_page=items_per_page)    


def adjustmentDetails_download():
    c_id=session.cid
    
    response.title='Download-Adjustment Details'
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    depot_id=str(request.vars.depotID).strip()
    store_id=str(request.vars.storeID).strip()
    
    depotName=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depotName=depotRow[0].name
        
    storeName=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        storeName=storeRow[0].store_name
    
    startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d')    
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d')
    
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    recItemList=[]
    
    qset=db()
    qset=qset(db.sm_damage.cid==c_id)
    qset=qset(db.sm_damage.depot_id==depot_id)
    qset=qset(db.sm_damage.store_id==store_id)
    qset=qset((db.sm_damage.damage_date>=startDt)&(db.sm_damage.damage_date<=endDt))    
    qset=qset(db.sm_damage.transfer_type=='ADJUSTMENT')
    qset=qset(db.sm_damage.status=='Posted')
    
    records=qset.select(db.sm_damage.item_id,db.sm_damage.item_name.max(),orderby=db.sm_damage.item_name,groupby=db.sm_damage.item_id)
    
    for row in records:
        item_id=row.sm_damage.item_id
        item_name=row[db.sm_damage.item_name.max()]
        
        recDetailList=[]
        hQty=0
        hTp=0
        
        qset1=db()
        qset1=qset1(db.sm_damage.cid==c_id)
        qset1=qset1(db.sm_damage.depot_id==depot_id)
        qset1=qset1(db.sm_damage.store_id==store_id)
        qset1=qset1((db.sm_damage.damage_date>=startDt)&(db.sm_damage.damage_date<=endDt))        
        qset1=qset1(db.sm_damage.item_id==item_id)
        qset1=qset1(db.sm_damage.transfer_type=='ADJUSTMENT')
        qset1=qset1(db.sm_damage.status=='Posted')        
        adjReceiptRow=qset1.select(db.sm_damage.depot_id,db.sm_damage.type_sl,db.sm_damage.damage_date,db.sm_damage.store_id,db.sm_damage.store_name,db.sm_damage.adjustment_type,db.sm_damage.quantity,db.sm_damage.dist_rate,orderby=db.sm_damage.type_sl)
        
        for drow in adjReceiptRow:
            depot_id=drow.depot_id
            type_sl=drow.type_sl
            damage_date=drow.damage_date
            store_id=drow.store_id
            store_name=drow.store_name
            adjustment_type=drow.adjustment_type
            quantity=drow.quantity
            
            if adjustment_type=='Decrease':
                quantity=quantity*(-1)                                
            else:
                pass
            
            price=drow.dist_rate
            tp=quantity*price
            hQty+=quantity
            hTp+=quantity*price
            
            slStr=str(session.prefix_invoice)+'AD'+str(depot_id)+'-'+str(type_sl)
            
            dictDetData={'slNo':str(slStr),'recDate':damage_date,'trFrom':store_id,'trFromName':store_name,'adjType':adjustment_type,'qty':str(quantity),'recTp':str(tp)}
            recDetailList.append(dictDetData)
            
        dictHeadData={'ItemID':item_id,'itemName':item_name,'hQty':hQty,'hTp':hTp,'rDetails':recDetailList}
        recItemList.append(dictHeadData)    
        
    #------------------------------------    
    myString='23.2 Adjustment Details\n'
    myString+='Date From:,'+str(startDt)+'\n'
    myString+='To Date:'+','+str(endDt)+'\n'
    myString+='Branch ID:,'+str(depot_id)+'\n'
    myString+='Branch Name'+','+str(depotName)+'\n'
    myString+='Store ID:,'+str(store_id)+'\n'
    myString+='Store Name'+','+str(storeName)+'\n'
    
    totalQty=0
    totalTp=0
    
    myString+='Item Id,Item Name,Adj. No,Date,Location,Type,Quantity,Trade Price'+'\n'
    for i in range(len(recItemList)):
        dictData=recItemList[i]
        
        ItemID=dictData['ItemID']
        itemName=str(dictData['itemName']).replace(',', ' ')
        
        
        hQty=dictData['hQty']
        totalQty+=hQty
        
        hTp=float(dictData['hTp'])
        totalTp+=hTp
        
        myString+=str(ItemID)+','+str(itemName)+',,,,,'+str(hQty)+','+str(hTp)+'\n'
        
        detailList=dictData['rDetails']
        for j in range(len(detailList)):
            dictDetData=detailList[j]
            
            slNo=dictDetData['slNo']
            recDate=dictDetData['recDate']
            
            trFrom=dictDetData['trFrom']
            trFromName=str(dictDetData['trFromName']).replace(',', ' ')
            adjType=dictDetData['adjType']
            
            qty=dictDetData['qty']
            recTp=dictDetData['recTp']
            
            myString+=',,'+str(slNo)+','+str(recDate)+','+str(trFrom)+':'+str(trFromName)+','+str(adjType)+','+str(qty)+','+str(recTp)+'\n'
            
        #------------------------ 
        
    myString+='Total,,,,,,'+str(totalQty)+','+str(totalTp)+'\n'
    
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_AdjustmentDetails.csv'   
    return str(myString)
    

def adjustmentSummeryItemWise():
    c_id=session.cid
    
    response.title='23.3 Adjustment Summary Item Wise'
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    depot_id=str(request.vars.depotID).strip()
    store_id=str(request.vars.storeID).strip()
    
    depotName=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depotName=depotRow[0].name
        
    storeName=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        storeName=storeRow[0].store_name
        
    startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d')    
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d')
    
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    
    qset=db()
    qset=qset(db.sm_damage.cid==c_id)
    qset=qset(db.sm_damage.depot_id==depot_id)
    qset=qset(db.sm_damage.store_id==store_id)
    qset=qset((db.sm_damage.damage_date>=startDt)&(db.sm_damage.damage_date<=endDt))
    qset=qset(db.sm_damage.transfer_type=='ADJUSTMENT')
    qset=qset(db.sm_damage.status=='Posted')
    records=qset.select(db.sm_damage.item_id,db.sm_damage.item_name.max(),db.sm_damage.dist_rate,db.sm_damage.adjustment_type,db.sm_damage.quantity.sum(),orderby=db.sm_damage.item_name|db.sm_damage.dist_rate,groupby=db.sm_damage.item_id|db.sm_damage.dist_rate|db.sm_damage.adjustment_type)
    
    return dict(records=records,fromDate=fromDate,toDate=toDate,depotID=depot_id,depotName=depotName,storeID=store_id,storeName=storeName,page=page,items_per_page=items_per_page)    

def adjustmentSummeryItemWise_download():
    c_id=session.cid
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    depot_id=str(request.vars.depotID).strip()
    store_id=str(request.vars.storeID).strip()
    
    depotName=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depotName=depotRow[0].name
        
    storeName=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        storeName=storeRow[0].store_name
        
    startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d')    
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d')
    
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    
    qset=db()
    qset=qset(db.sm_damage.cid==c_id)
    qset=qset(db.sm_damage.depot_id==depot_id)
    qset=qset(db.sm_damage.store_id==store_id)
    qset=qset((db.sm_damage.damage_date>=startDt)&(db.sm_damage.damage_date<=endDt))
    qset=qset(db.sm_damage.transfer_type=='ADJUSTMENT')
    qset=qset(db.sm_damage.status=='Posted')
    #records=qset.select(db.sm_damage.item_id,db.sm_damage.item_name,db.sm_damage.adjustment_type,db.sm_damage.quantity.sum(),db.sm_damage.dist_rate,orderby=db.sm_damage.item_name|db.sm_damage.dist_rate,groupby=db.sm_damage.item_id|db.sm_damage.dist_rate|db.sm_damage.adjustment_type)
    records=qset.select(db.sm_damage.item_id,db.sm_damage.item_name.max(),db.sm_damage.dist_rate,db.sm_damage.adjustment_type,db.sm_damage.quantity.sum(),orderby=db.sm_damage.item_name|db.sm_damage.dist_rate,groupby=db.sm_damage.item_id|db.sm_damage.dist_rate|db.sm_damage.adjustment_type)
    
    
    #------------------------
    myString='23.3 Adjustment Summery (Item Wise)\n'
    myString+='Date From:,'+str(startDt)+'\n'
    myString+='To Date:'+','+str(endDt)+'\n'
    myString+='Branch ID:,'+str(depot_id)+'\n'
    myString+='Branch Name'+','+str(depotName)+'\n'
    myString+='Store ID:,'+str(store_id)+'\n'
    myString+='Store Name'+','+str(storeName)+'\n'
    
    totalQty=0
    totalTP=0
    
    myString+='Item Id,Item Name,Trade Price,Type,Quantity,Total Amount'+'\n'
    for row in records:
        item_id=row.sm_damage.item_id
        item_name=str(row[db.sm_damage.item_name.max()]).replace(',', ' ') 
        adjustment_type=row.sm_damage.adjustment_type
        dist_rate=row.sm_damage.dist_rate
        qty=row[db.sm_damage.quantity.sum()]
        
        if adjustment_type=='Decrease':
            qty=qty*(-1)                                
        else:
            pass
        
        totalQty+=qty
        
        price=qty*row.sm_damage.dist_rate
                
        totalTP+=price
        
        #------------------------
        myString+=str(item_id)+','+str(item_name)+','+str(dist_rate)+','+str(adjustment_type)+','+str(qty)+','+str(price)+'\n'
        
    myString+='Total,,,,'+str(totalQty)+','+str(totalTP)+'\n'
    
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_adjustmentSumamryItemwise.csv'   
    return str(myString)
    

def adjustmentPreview():
    c_id=session.cid
    
    response.title='Preview-IC Adjustment'
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    depot_id=str(request.vars.depotID).strip()
    store_id=str(request.vars.storeID).strip()
    
    fromDepotID=str(request.vars.fromDepotID).strip()
    depotNameFrom=''
    depotRowFrom=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==fromDepotID)).select(db.sm_depot.name,limitby=(0,1))
    if depotRowFrom:
        depotNameFrom=depotRowFrom[0].name
        
    depotName=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,db.sm_depot.field1,limitby=(0,1))
    if depotRow:
        depotName=depotRow[0].name
        
    storeName=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        storeName=storeRow[0].store_name
        
    startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d')    
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d')
    
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    qset=db()
    qset=qset(db.sm_damage_head.cid==c_id)
    qset=qset(db.sm_damage_head.depot_id==depot_id)
    qset=qset(db.sm_damage_head.store_id==store_id)
    qset=qset(db.sm_damage_head.transfer_type=='ADJUSTMENT')
    qset=qset((db.sm_damage_head.damage_date>=startDt)& (db.sm_damage_head.damage_date<=endDt))
    qset=qset(db.sm_damage_head.status=='Posted')
    
    records=qset.select(db.sm_damage_head.ALL,orderby=db.sm_damage_head.type_sl)
    
    data_List=[]
    
    for rec in records:
        depotId=rec.depot_id
        rowId=rec.sl
        status=rec.status
        damage_date=rec.damage_date
        note=rec.note
        store_id=rec.store_id
        store_name=rec.store_name
        store_id_to=rec.store_id_to
        store_name_to=rec.store_name_to    
        type_sl=rec.type_sl
        cause=rec.adjustment_reference
        updatedBy=rec.updated_by
        
        detDictList=[]
        mCartonTotal=0
        detailRows=db((db.sm_damage.cid==c_id)& (db.sm_damage.depot_id==depotId) & (db.sm_damage.transfer_type=='ADJUSTMENT') & (db.sm_damage.type_sl==type_sl)).select(db.sm_damage.ALL,orderby=db.sm_damage.item_name)
        for dRow in detailRows:        
            item_id=dRow.item_id
            item_name=dRow.item_name
            adjustment_type=dRow.adjustment_type
            batch_id=dRow.batch_id            
            quantity=dRow.quantity
                    
            dist_rate=dRow.dist_rate
            short_note=dRow.short_note 
            expiary_date=dRow.expiary_date           
            item_unit=dRow.item_unit            
            item_carton=dRow.item_carton
            
            try:
                mCarton=round(float(quantity)/item_carton,2)
            except:
                mCarton=0
                
            mCartonTotal+=mCarton
            
            #------------------------
            vdDict= {'item_id': item_id,'item_name': item_name,'adjustment_type': adjustment_type,'batch_id':batch_id,'item_unit':item_unit,'expiary_date':expiary_date,'store_id':store_id,'store_name':store_name,'quantity': quantity,'price': dist_rate}
            detDictList.append(vdDict)
            
        vhDict={'depot_id':depotId,'depot_name':depotName,'rowId':rowId,'type_sl':type_sl,'store_id':store_id,'store_name':store_name,'damage_date':damage_date,'status':status,'store_id_to':store_id_to,'store_name_to':store_name_to,'note':note,'cause':cause,'updatedBy':updatedBy,'mCartonTotal':mCartonTotal,'vdList':detDictList}
        data_List.append(vhDict)
    
    return dict(data_List=data_List,fromDate=fromDate,toDate=toDate,depotID=depot_id,depotName=depotName,storeID=store_id,storeName=storeName,fromDepotID=fromDepotID,depotNameFrom=depotNameFrom,page=page,items_per_page=items_per_page)    


def stockStatusWithoutBatch():
    c_id=session.cid
    
    response.title='Stock status without batch'
    
    depot_id=str(request.vars.depotID).strip()
    store_id=str(request.vars.storeID).strip()
    
    depotName=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depotName=depotRow[0].name
        
    storeName=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        storeName=storeRow[0].store_name
        
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    qset=db()
    qset=qset(db.sm_depot_stock_balance.cid==c_id)
    qset=qset(db.sm_depot_stock_balance.depot_id==depot_id)
    qset=qset(db.sm_depot_stock_balance.store_id==store_id)
    qset=qset(db.sm_depot_stock_balance.quantity>0)
    
    qset=qset(db.sm_item.cid==c_id)
    qset=qset(db.sm_depot_stock_balance.item_id==db.sm_item.item_id)
    
    records=qset.select(db.sm_item.category_id,db.sm_item.item_id,db.sm_item.name.max(),db.sm_item.unit_type.max(),db.sm_item.price,db.sm_item.item_carton.max(),db.sm_depot_stock_balance.quantity.sum(),orderby=db.sm_item.category_id|db.sm_item.name,groupby=db.sm_item.category_id|db.sm_item.item_id|db.sm_item.price)
    
    return dict(records=records,depotID=depot_id,depotName=depotName,storeID=store_id,storeName=storeName,page=page,items_per_page=items_per_page)    

def downloadStockStatusWithoutBatch():
    c_id=session.cid
    
    response.title='Download Stock Status batch wise'
        
    depot_id=str(request.vars.depotID).strip()
    store_id=str(request.vars.storeID).strip()
    
    depotName=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depotName=depotRow[0].name
        
    storeName=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        storeName=storeRow[0].store_name
    
    
    qset=db()
    qset=qset(db.sm_depot_stock_balance.cid==c_id)
    qset=qset(db.sm_depot_stock_balance.depot_id==depot_id)
    qset=qset(db.sm_depot_stock_balance.store_id==store_id)
    qset=qset(db.sm_depot_stock_balance.quantity>0)
    
    qset=qset(db.sm_item.cid==c_id)
    qset=qset(db.sm_depot_stock_balance.item_id==db.sm_item.item_id)
    
    #records=qset.select(db.sm_depot_stock_balance.batch_id,db.sm_depot_stock_balance.quantity.sum(),db.sm_item.item_id,db.sm_item.name,db.sm_item.category_id,db.sm_item.unit_type,db.sm_item.item_carton,db.sm_item.price,orderby=db.sm_item.category_id|db.sm_item.name,groupby=db.sm_item.item_id)
    records=qset.select(db.sm_item.category_id,db.sm_item.item_id,db.sm_item.name.max(),db.sm_item.unit_type.max(),db.sm_item.price,db.sm_item.item_carton.max(),db.sm_depot_stock_balance.quantity.sum(),orderby=db.sm_item.category_id|db.sm_item.name,groupby=db.sm_item.category_id|db.sm_item.item_id|db.sm_item.price)
    
    #REmove , from record.Cause , means new column in excel
    myString='Depot/Branch,'+depot_id+'|'+depotName+'\n'
    myString+='Store,'+store_id+'|'+storeName+'\n\n'
    
    myString+='Group,Product ID,Name,Unit,Status,Qty,TP,TP*Qty,M.CartonUnit\n'
    for rec in records:
        category_id=rec.sm_item.category_id
        item_id=rec.sm_item.item_id
        name=rec[db.sm_item.name.max()]
        unit_type=rec[db.sm_item.unit_type.max()]        
        status='ACTIVE'
        quantity=rec[db.sm_depot_stock_balance.quantity.sum()]        
        price=rec.sm_item.price
        
        if rec[db.sm_item.item_carton.max()]>0:            
            mCarton=round(round(rec[db.sm_depot_stock_balance.quantity.sum()],2)/rec[db.sm_item.item_carton.max()],2)
        else:
            mCarton=0
            
        myString+=str(category_id)+','+str(item_id)+','+str(name)+','+str(unit_type)+','+status+','+str(quantity)+','+str(price)+','+str(quantity*price)+','+str(mCarton)+'\n'
        
    #Save as csv
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_stock_status_without_batch_wise.csv'   
    return str(myString)    

def stockStatusWithoutBatchStoreall():
    c_id=session.cid
    
    response.title='Stock status without batch Store All'
    
    depot_id=str(request.vars.depotID).strip()
    
    depotName=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depotName=depotRow[0].name
        
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    qset=db()
    qset=qset(db.sm_depot_stock_balance.cid==c_id)
    qset=qset(db.sm_depot_stock_balance.depot_id==depot_id)
    qset=qset(db.sm_depot_stock_balance.quantity>0)
    
    qset=qset(db.sm_item.cid==c_id)
    qset=qset(db.sm_depot_stock_balance.item_id==db.sm_item.item_id)
    
    records=qset.select(db.sm_depot_stock_balance.store_id,db.sm_depot_stock_balance.store_name.max(),db.sm_item.category_id,db.sm_item.item_id,db.sm_item.name.max(),db.sm_item.unit_type.max(),db.sm_item.item_carton.max(),db.sm_item.price,db.sm_depot_stock_balance.quantity.sum(),orderby=db.sm_depot_stock_balance.store_id|db.sm_item.category_id|db.sm_item.name,groupby=db.sm_depot_stock_balance.store_id|db.sm_item.category_id|db.sm_item.item_id|db.sm_item.price)
    
    return dict(records=records,depotID=depot_id,depotName=depotName,page=page,items_per_page=items_per_page)    
    

def downloadStockStatusWithoutBatchStoreall():
    c_id=session.cid
    
    response.title='Download Stock Status batch wise Stroe all'
        
    depot_id=str(request.vars.depotID).strip()
        
    depotName=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depotName=depotRow[0].name
        
    qset=db()
    qset=qset(db.sm_depot_stock_balance.cid==c_id)
    qset=qset(db.sm_depot_stock_balance.depot_id==depot_id)
    qset=qset(db.sm_depot_stock_balance.quantity>0)
    
    qset=qset(db.sm_item.cid==c_id)
    qset=qset(db.sm_depot_stock_balance.item_id==db.sm_item.item_id)
    
    records=qset.select(db.sm_depot_stock_balance.store_id,db.sm_depot_stock_balance.store_name.max(),db.sm_item.category_id,db.sm_item.item_id,db.sm_item.name.max(),db.sm_item.unit_type.max(),db.sm_item.item_carton.max(),db.sm_item.price,db.sm_depot_stock_balance.quantity.sum(),orderby=db.sm_depot_stock_balance.store_id|db.sm_item.category_id|db.sm_item.name,groupby=db.sm_depot_stock_balance.store_id|db.sm_item.category_id|db.sm_item.item_id|db.sm_item.price)
    
    #REmove , from record.Cause , means new column in excel
    myString='Depot/Branch,'+depot_id+'|'+depotName+'\n'
    myString+='Store,ALL\n\n'
    
    myString+='Group,Product ID,Name,Unit,Status,Qty,TP,TP*Qty,M.CartonUnit\n'
    
    preStore=''
    for rec in records:        
        store_id=rec.sm_depot_stock_balance.store_id
        store_name=rec[db.sm_depot_stock_balance.store_name.max()]
        if store_name!=preStore:
            preStore=store_name     
            myString+='Store,'+str(store_id)+':'+str(store_name)+'\n'
            
        category_id=rec.sm_item.category_id
        item_id=rec.sm_item.item_id
        name=rec[db.sm_item.name.max()]
        unit_type=rec[db.sm_item.unit_type.max()]        
        status='ACTIVE'
        quantity=rec[db.sm_depot_stock_balance.quantity.sum()]        
        price=rec.sm_item.price
        
        if rec[db.sm_item.item_carton.max()]>0:
            mCarton=round(round(rec[db.sm_depot_stock_balance.quantity.sum()],2)/rec[db.sm_item.item_carton.max()],2)
        else:
            mCarton=0
            
        myString+=str(category_id)+','+str(item_id)+','+str(name)+','+str(unit_type)+','+status+','+str(quantity)+','+str(price)+','+str(quantity*price)+','+str(mCarton)+'\n'
        
    #Save as csv
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_stock_status_without_batch_wiseStoreAll.csv'   
    return str(myString)    
    

def stockStatusWithBatch():
    c_id=session.cid
    
    response.title='Stock Status with Batch'
    
    depot_id=str(request.vars.depotID).strip()
    store_id=str(request.vars.storeID).strip()
    
    depotName=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depotName=depotRow[0].name
        
    storeName=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        storeName=storeRow[0].store_name
        
    
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    
    qset=db()
    qset=qset(db.sm_depot_stock_balance.cid==c_id)
    qset=qset(db.sm_depot_stock_balance.depot_id==depot_id)
    qset=qset(db.sm_depot_stock_balance.store_id==store_id)
    qset=qset(db.sm_depot_stock_balance.quantity>0)
    
    qset=qset(db.sm_item.cid==c_id)
    qset=qset(db.sm_depot_stock_balance.item_id==db.sm_item.item_id)
    
    records=qset.select(db.sm_item.item_id,db.sm_item.name.max(),db.sm_depot_stock_balance.batch_id,db.sm_item.unit_type.max(),db.sm_item.price,db.sm_item.item_carton.max(),db.sm_depot_stock_balance.expiary_date.max(),db.sm_depot_stock_balance.quantity.sum(),orderby=db.sm_item.name|db.sm_item.item_id|db.sm_depot_stock_balance.batch_id,groupby=db.sm_item.item_id|db.sm_depot_stock_balance.batch_id|db.sm_item.price)
    
    return dict(records=records,depotID=depot_id,depotName=depotName,storeID=store_id,storeName=storeName,page=page,items_per_page=items_per_page)    
    

def downloadStockStatusWithBatch():
    c_id=session.cid
    
    response.title='Download Stock Status with Batch'
        
    depot_id=str(request.vars.depotID).strip()
    store_id=str(request.vars.storeID).strip()
    
    depotName=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depotName=depotRow[0].name
        
    storeName=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        storeName=storeRow[0].store_name
        
    
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    
    qset=db()
    qset=qset(db.sm_depot_stock_balance.cid==c_id)
    qset=qset(db.sm_depot_stock_balance.depot_id==depot_id)
    qset=qset(db.sm_depot_stock_balance.store_id==store_id)
    qset=qset(db.sm_depot_stock_balance.quantity>0)
    
    qset=qset(db.sm_item.cid==c_id)
    qset=qset(db.sm_depot_stock_balance.item_id==db.sm_item.item_id)
    
    records=qset.select(db.sm_item.item_id,db.sm_item.name.max(),db.sm_depot_stock_balance.batch_id,db.sm_item.unit_type.max(),db.sm_item.price,db.sm_item.item_carton.max(),db.sm_depot_stock_balance.expiary_date.max(),db.sm_depot_stock_balance.quantity.sum(),orderby=db.sm_item.name|db.sm_item.item_id|db.sm_depot_stock_balance.batch_id,groupby=db.sm_item.item_id|db.sm_depot_stock_balance.batch_id|db.sm_item.price)
    
    #------------
    myString='IC Stock Status- Batch Wise\n'
    myString+='Depot/Branch,'+depot_id+'|'+depotName+'\n'
    myString+='Store,'+store_id+'|'+storeName+'\n\n'
        
    myString+='Product ID,Name,Batch,Unit,Status,Qty,TP,TP*Qty,M.Carton,Exp. Date\n'
    
    item_carton=0
    item_cartonTotal=0
    for rec in records:
        item_id=rec.sm_item.item_id
        name=rec[db.sm_item.name.max()]
        batch_id=rec.sm_depot_stock_balance.batch_id
        unit_type=rec[db.sm_item.unit_type.max()]
        
        quantity=rec[db.sm_depot_stock_balance.quantity.sum()]        
        price=rec.sm_item.price
        
        if quantity>0 and rec[db.sm_item.item_carton.max()]>0 :
            item_carton=round(round(quantity,2)/rec[db.sm_item.item_carton.max()],2)
            item_cartonTotal+=item_carton
                
        expiary_date=rec[db.sm_depot_stock_balance.expiary_date.max()]
        
        currentDate=datetime.datetime.strptime(str(current_date),'%Y-%m-%d')
        if datetime.datetime.strptime(str(rec[db.sm_depot_stock_balance.expiary_date.max()]),'%Y-%m-%d')< currentDate:
            status='INACTIVE'
        else:
            status='ACTIVE'
            
        myString+=str(item_id)+','+str(name)+','+str(batch_id)+','+str(unit_type)+','+status+','+str(quantity)+','+str(price)+','+str(quantity*price)+','+str(item_carton)+','+str(expiary_date)+'\n'
    
    myString+='\nTotal M.Carton:'+str(item_cartonTotal)    
    
    #Save as csv
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_stock_status_batch_wise.csv'   
    return str(myString)    


def stockStatusWithBatchall():
    c_id=session.cid
    
    response.title='Stock Status with Batch Store All'
    
    depot_id=str(request.vars.depotID).strip()
    store_id=str(request.vars.storeID).strip()
    
    depotName=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depotName=depotRow[0].name
        
    storeName=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        storeName=storeRow[0].store_name
    
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    
    qset=db()
    qset=qset(db.sm_depot_stock_balance.cid==c_id)
    qset=qset(db.sm_depot_stock_balance.depot_id==depot_id)
    #qset=qset(db.sm_depot_stock_balance.store_id==store_id)
    qset=qset(db.sm_depot_stock_balance.quantity>0)
    
    qset=qset(db.sm_item.cid==c_id)
    qset=qset(db.sm_depot_stock_balance.item_id==db.sm_item.item_id)
    
    #records=qset.select(db.sm_depot_stock_balance.store_id,db.sm_depot_stock_balance.store_name,db.sm_item.item_id,db.sm_item.name,db.sm_depot_stock_balance.batch_id,db.sm_item.unit_type,db.sm_item.item_carton,db.sm_depot_stock_balance.expiary_date,db.sm_item.price,db.sm_depot_stock_balance.quantity.sum(),orderby=db.sm_depot_stock_balance.store_id|db.sm_item.name|db.sm_item.item_id|db.sm_depot_stock_balance.batch_id,groupby=db.sm_depot_stock_balance.store_id|db.sm_item.item_id|db.sm_depot_stock_balance.batch_id)
    records=qset.select(db.sm_depot_stock_balance.store_id,db.sm_depot_stock_balance.store_name.max(),db.sm_item.item_id,db.sm_item.name.max(),db.sm_depot_stock_balance.batch_id,db.sm_item.unit_type.max(),db.sm_item.item_carton.max(),db.sm_depot_stock_balance.expiary_date.max(),db.sm_item.price,db.sm_depot_stock_balance.quantity.sum(),orderby=db.sm_depot_stock_balance.store_id|db.sm_item.name|db.sm_item.item_id|db.sm_depot_stock_balance.batch_id,groupby=db.sm_depot_stock_balance.store_id|db.sm_item.item_id|db.sm_depot_stock_balance.batch_id|db.sm_item.price)
    
    return dict(records=records,depotID=depot_id,depotName=depotName,storeID=store_id,storeName=storeName,page=page,items_per_page=items_per_page)    
    

def stp_generator():
    c_id=session.cid
    
    response.title='STP Generator'
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    depot_id=str(request.vars.depotID).strip()
    store_id=str(request.vars.storeID).strip()
    
    depotName=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depotName=depotRow[0].name
        
    storeName=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        storeName=storeRow[0].store_name
        
    try:
        startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d').strftime('%Y-%m-%d') 
        endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d').strftime('%Y-%m-%d')
    except:
        startDt=''
        endDt=''
        
    #--------------    
    saleTotal=0    
    creditTotal=0    
    cashRecTotal=0
    cashPendingTotal=0    
    
    #-----------
    qset=db()
    qset=qset(db.sm_invoice_head.cid==c_id)
    qset=qset(db.sm_invoice_head.depot_id==depot_id)
    qset=qset(db.sm_invoice_head.store_id==store_id)
    qset=qset((db.sm_invoice_head.invoice_date>=startDt)&(db.sm_invoice_head.invoice_date<=endDt))    
    qset=qset(db.sm_invoice_head.status=='Invoiced') 
    qset=qset(db.sm_invoice_head.sl!=0)
    
    #--------- Invoice Total
    records1=qset.select(db.sm_invoice_head.cid,db.sm_invoice_head.actual_total_tp.sum(),db.sm_invoice_head.total_amount.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_vat.sum(),db.sm_invoice_head.return_discount.sum(),db.sm_invoice_head.return_sp_discount.sum(), groupby=db.sm_invoice_head.cid)
    for row1 in records1:
        acTpAmount=row1[db.sm_invoice_head.actual_total_tp.sum()]
        
        #totalAmount=row1[db.sm_invoice_head.total_amount.sum()]
        return_tp=row1[db.sm_invoice_head.return_tp.sum()]
        #return_vat=row1[db.sm_invoice_head.return_vat.sum()]
        #return_discount=row1[db.sm_invoice_head.return_discount.sum()]    
        return_sp=row1[db.sm_invoice_head.return_sp_discount.sum()]
        
        #return_total=return_tp+return_vat-return_discount
        #saleTotal=round(totalAmount-return_total,2)
        
        saleTotal=round(acTpAmount-(return_tp+return_sp),2)
        
        
    #----- Credit Total
    qset2=qset(db.sm_invoice_head.payment_mode=='CREDIT')
    records2=qset2.select(db.sm_invoice_head.cid,db.sm_invoice_head.actual_total_tp.sum(),db.sm_invoice_head.total_amount.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_vat.sum(),db.sm_invoice_head.return_discount.sum(),db.sm_invoice_head.return_sp_discount.sum(),groupby=db.sm_invoice_head.cid)
    for row2 in records2:        
        #totalAmount=row2[db.sm_invoice_head.total_amount.sum()]
        #return_tp=row2[db.sm_invoice_head.return_tp.sum()]
        #return_vat=row2[db.sm_invoice_head.return_vat.sum()]
        #return_discount=row2[db.sm_invoice_head.return_discount.sum()]
        #return_total=return_tp+return_vat-return_discount
        #creditTotal=round(totalAmount-return_total,2)
        
        acTpAmount=row2[db.sm_invoice_head.actual_total_tp.sum()]
        return_tp=row2[db.sm_invoice_head.return_tp.sum()]
        return_sp=row2[db.sm_invoice_head.return_sp_discount.sum()]
        creditTotal=round(acTpAmount-(return_tp+return_sp),2)
        
    #----- Cash Collection
    qset3=qset((db.sm_invoice_head.payment_mode=='CASH')&(db.sm_invoice_head.collection_amount>0))
    records3=qset3.select(db.sm_invoice_head.cid,db.sm_invoice_head.collection_amount.sum(),groupby=db.sm_invoice_head.cid)
    for row3 in records3:
        totalAmount=row3[db.sm_invoice_head.collection_amount.sum()]
        
        cashRecTotal=round(totalAmount,2)
        
    #----- Cash Collection
    qset4=qset((db.sm_invoice_head.payment_mode=='CASH')&(db.sm_invoice_head.inv_pending_flag==1))
    records4=qset4.select(db.sm_invoice_head.cid,db.sm_invoice_head.actual_total_tp.sum(),db.sm_invoice_head.total_amount.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_vat.sum(),db.sm_invoice_head.return_discount.sum(),db.sm_invoice_head.return_sp_discount.sum(),groupby=db.sm_invoice_head.cid)
    for row4 in records4:
        #totalAmount=row4[db.sm_invoice_head.total_amount.sum()]
        #return_tp=row4[db.sm_invoice_head.return_tp.sum()]
        #return_vat=row4[db.sm_invoice_head.return_vat.sum()]
        #return_discount=row4[db.sm_invoice_head.return_discount.sum()]
        #return_total=return_tp+return_vat-return_discount
        #cashPendingTotal=round(totalAmount-return_total,2)
        
        acTpAmount=row4[db.sm_invoice_head.actual_total_tp.sum()]
        return_tp=row4[db.sm_invoice_head.return_tp.sum()]
        return_sp=row4[db.sm_invoice_head.return_sp_discount.sum()]
        cashPendingTotal=round(acTpAmount-(return_tp+return_sp),2)
        
    return dict(fromDate=fromDate,toDate=toDate,depotID=depot_id,depotName=depotName,storeID=store_id,storeName=storeName,saleTotal=saleTotal,creditTotal=creditTotal,cashRecTotal=cashRecTotal,cashPendingTotal=cashPendingTotal)    


def stp_generator_download():
    c_id=session.cid
    
    response.title='Download-STP Generator'
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    depot_id=str(request.vars.depotID).strip()
    store_id=str(request.vars.storeID).strip()
    
    depotName=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depotName=depotRow[0].name
        
    storeName=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        storeName=storeRow[0].store_name
        
    try:
        startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d').strftime('%Y-%m-%d') 
        endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d').strftime('%Y-%m-%d')
    except:
        startDt=''
        endDt=''
        
    #--------------    
    saleTotal=0    
    creditTotal=0    
    cashRecTotal=0
    cashPendingTotal=0    
        
    #-----------
    qset=db()
    qset=qset(db.sm_invoice_head.cid==c_id)
    qset=qset(db.sm_invoice_head.depot_id==depot_id)
    qset=qset(db.sm_invoice_head.store_id==store_id)
    qset=qset((db.sm_invoice_head.invoice_date>=startDt)&(db.sm_invoice_head.invoice_date<=endDt))    
    qset=qset(db.sm_invoice_head.status=='Invoiced') 
    qset=qset(db.sm_invoice_head.sl!=0)
    
    #--------- Invoice Total
    records1=qset.select(db.sm_invoice_head.cid,db.sm_invoice_head.actual_total_tp.sum(),db.sm_invoice_head.total_amount.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_vat.sum(),db.sm_invoice_head.return_discount.sum(),db.sm_invoice_head.return_sp_discount.sum(), groupby=db.sm_invoice_head.cid)
    for row1 in records1:
        acTpAmount=row1[db.sm_invoice_head.actual_total_tp.sum()]
        
        #totalAmount=row1[db.sm_invoice_head.total_amount.sum()]
        return_tp=row1[db.sm_invoice_head.return_tp.sum()]
        #return_vat=row1[db.sm_invoice_head.return_vat.sum()]
        #return_discount=row1[db.sm_invoice_head.return_discount.sum()]    
        return_sp=row1[db.sm_invoice_head.return_sp_discount.sum()]
        
        #return_total=return_tp+return_vat-return_discount
        #saleTotal=round(totalAmount-return_total,2)
        
        saleTotal=round(acTpAmount-(return_tp+return_sp),2)
        
        
    #----- Credit Total
    qset2=qset(db.sm_invoice_head.payment_mode=='CREDIT')
    records2=qset2.select(db.sm_invoice_head.cid,db.sm_invoice_head.actual_total_tp.sum(),db.sm_invoice_head.total_amount.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_vat.sum(),db.sm_invoice_head.return_discount.sum(),db.sm_invoice_head.return_sp_discount.sum(),groupby=db.sm_invoice_head.cid)
    for row2 in records2:        
        #totalAmount=row2[db.sm_invoice_head.total_amount.sum()]
        #return_tp=row2[db.sm_invoice_head.return_tp.sum()]
        #return_vat=row2[db.sm_invoice_head.return_vat.sum()]
        #return_discount=row2[db.sm_invoice_head.return_discount.sum()]
        #return_total=return_tp+return_vat-return_discount
        #creditTotal=round(totalAmount-return_total,2)
        
        acTpAmount=row2[db.sm_invoice_head.actual_total_tp.sum()]
        return_tp=row2[db.sm_invoice_head.return_tp.sum()]
        return_sp=row2[db.sm_invoice_head.return_sp_discount.sum()]
        creditTotal=round(acTpAmount-(return_tp+return_sp),2)
        
    #----- Cash Collection
    qset3=qset((db.sm_invoice_head.payment_mode=='CASH')&(db.sm_invoice_head.collection_amount>0))
    records3=qset3.select(db.sm_invoice_head.cid,db.sm_invoice_head.collection_amount.sum(),groupby=db.sm_invoice_head.cid)
    for row3 in records3:
        totalAmount=row3[db.sm_invoice_head.collection_amount.sum()]
        
        cashRecTotal=round(totalAmount,2)
        
    #----- Cash Collection
    qset4=qset((db.sm_invoice_head.payment_mode=='CASH')&(db.sm_invoice_head.inv_pending_flag==1))
    records4=qset4.select(db.sm_invoice_head.cid,db.sm_invoice_head.actual_total_tp.sum(),db.sm_invoice_head.total_amount.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_vat.sum(),db.sm_invoice_head.return_discount.sum(),db.sm_invoice_head.return_sp_discount.sum(),groupby=db.sm_invoice_head.cid)
    for row4 in records4:
        #totalAmount=row4[db.sm_invoice_head.total_amount.sum()]
        #return_tp=row4[db.sm_invoice_head.return_tp.sum()]
        #return_vat=row4[db.sm_invoice_head.return_vat.sum()]
        #return_discount=row4[db.sm_invoice_head.return_discount.sum()]
        #return_total=return_tp+return_vat-return_discount
        #cashPendingTotal=round(totalAmount-return_total,2)
        
        acTpAmount=row4[db.sm_invoice_head.actual_total_tp.sum()]
        return_tp=row4[db.sm_invoice_head.return_tp.sum()]
        return_sp=row4[db.sm_invoice_head.return_sp_discount.sum()]
        cashPendingTotal=round(acTpAmount-(return_tp+return_sp),2)
        
    #----------------------------------------
    myString='4.1 STP Generator\n'
    myString+='Date From:,'+str(startDt)+'\n'
    myString+='To Date:'+','+str(endDt)+'\n'
    myString+='Branch ID:,'+str(depot_id)+'\n'
    myString+='Branch Name'+','+str(depotName)+'\n'
    myString+='Store ID:,'+str(store_id)+'\n'
    myString+='Store Name'+','+str(storeName)+'\n'
    
    myString+='Product,Date From,Date To,Sold,Transit,Pending,Net Sales'+'\n'
    
    #------------------------    
    soldAmt=cashRecTotal+creditTotal
    
    myString+=str(session.depot_short_name)+','+str(fromDate)+','+str(toDate)+','+str(soldAmt)+','+str(saleTotal-(soldAmt+cashPendingTotal))+','+str(cashPendingTotal)+','+str(saleTotal)+'\n'
    
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_stp_generator.csv'   
    return str(myString)




#----------------------
def stp_item_wise_sales_distribution():
    c_id=session.cid
    
    response.title='STP-Item Wise Sales Distribution'
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    depot_id=str(request.vars.depotID).strip()
    store_id=str(request.vars.storeID).strip()
    
    depotName=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depotName=depotRow[0].name
        
    storeName=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        storeName=storeRow[0].store_name
    
    try:
        startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d').strftime('%Y-%m-%d') 
        endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d').strftime('%Y-%m-%d')
    except:
        startDt=''
        endDt=''
        
    #--------------    
    saleTotal=0    
    creditTotal=0    
    cashRecTotal=0
    cashPendingTotal=0    
    
    #-----------
    qset=db()
    qset=qset(db.sm_invoice_head.cid==c_id)
    qset=qset(db.sm_invoice_head.depot_id==depot_id)
    qset=qset(db.sm_invoice_head.store_id==store_id)
    qset=qset((db.sm_invoice_head.invoice_date>=startDt)&(db.sm_invoice_head.invoice_date<=endDt))    
    qset=qset(db.sm_invoice_head.status=='Invoiced')
    qset=qset(db.sm_invoice_head.sl!=0)
    
    #--------- Invoice Total
    records1=qset.select(db.sm_invoice_head.cid,db.sm_invoice_head.actual_total_tp.sum(),db.sm_invoice_head.total_amount.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_vat.sum(),db.sm_invoice_head.return_discount.sum(),db.sm_invoice_head.return_sp_discount.sum(), groupby=db.sm_invoice_head.cid)
    for row1 in records1:
        acTpAmount=row1[db.sm_invoice_head.actual_total_tp.sum()]
        
        #totalAmount=row1[db.sm_invoice_head.total_amount.sum()]
        return_tp=row1[db.sm_invoice_head.return_tp.sum()]
        #return_vat=row1[db.sm_invoice_head.return_vat.sum()]
        #return_discount=row1[db.sm_invoice_head.return_discount.sum()]    
        return_sp=row1[db.sm_invoice_head.return_sp_discount.sum()]
        
        #return_total=return_tp+return_vat-return_discount
        #saleTotal=round(totalAmount-return_total,2)
        
        saleTotal=round(acTpAmount-(return_tp+return_sp),2)
        
        
    #----- Credit Total
    qset2=qset(db.sm_invoice_head.payment_mode=='CREDIT')
    records2=qset2.select(db.sm_invoice_head.cid,db.sm_invoice_head.actual_total_tp.sum(),db.sm_invoice_head.total_amount.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_vat.sum(),db.sm_invoice_head.return_discount.sum(),db.sm_invoice_head.return_sp_discount.sum(),groupby=db.sm_invoice_head.cid)
    for row2 in records2:        
        #totalAmount=row2[db.sm_invoice_head.total_amount.sum()]
        #return_tp=row2[db.sm_invoice_head.return_tp.sum()]
        #return_vat=row2[db.sm_invoice_head.return_vat.sum()]
        #return_discount=row2[db.sm_invoice_head.return_discount.sum()]
        #return_total=return_tp+return_vat-return_discount
        #creditTotal=round(totalAmount-return_total,2)
        
        acTpAmount=row2[db.sm_invoice_head.actual_total_tp.sum()]
        return_tp=row2[db.sm_invoice_head.return_tp.sum()]
        return_sp=row2[db.sm_invoice_head.return_sp_discount.sum()]
        creditTotal=round(acTpAmount-(return_tp+return_sp),2)
        
    #----- Cash Collection
    qset3=qset((db.sm_invoice_head.payment_mode=='CASH')&(db.sm_invoice_head.collection_amount>0))
    records3=qset3.select(db.sm_invoice_head.cid,db.sm_invoice_head.collection_amount.sum(),groupby=db.sm_invoice_head.cid)
    for row3 in records3:
        totalAmount=row3[db.sm_invoice_head.collection_amount.sum()]
        
        cashRecTotal=round(totalAmount,2)
        
    #----- Cash Collection
    qset4=qset((db.sm_invoice_head.payment_mode=='CASH')&(db.sm_invoice_head.inv_pending_flag==1))
    records4=qset4.select(db.sm_invoice_head.cid,db.sm_invoice_head.actual_total_tp.sum(),db.sm_invoice_head.total_amount.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_vat.sum(),db.sm_invoice_head.return_discount.sum(),db.sm_invoice_head.return_sp_discount.sum(),groupby=db.sm_invoice_head.cid)
    for row4 in records4:
        #totalAmount=row4[db.sm_invoice_head.total_amount.sum()]
        #return_tp=row4[db.sm_invoice_head.return_tp.sum()]
        #return_vat=row4[db.sm_invoice_head.return_vat.sum()]
        #return_discount=row4[db.sm_invoice_head.return_discount.sum()]
        #return_total=return_tp+return_vat-return_discount
        #cashPendingTotal=round(totalAmount-return_total,2)
        
        acTpAmount=row4[db.sm_invoice_head.actual_total_tp.sum()]
        return_tp=row4[db.sm_invoice_head.return_tp.sum()]
        return_sp=row4[db.sm_invoice_head.return_sp_discount.sum()]
        cashPendingTotal=round(acTpAmount-(return_tp+return_sp),2)
        
    #=========================================== Item Wise sales distribution    
    records=qset((db.sm_invoice.cid==c_id) & (db.sm_invoice.depot_id==depot_id)&(db.sm_invoice_head.sl==db.sm_invoice.sl)).select(db.sm_invoice.item_id,db.sm_invoice.item_name.max(),db.sm_invoice.actual_tp,db.sm_invoice.quantity.sum(),db.sm_invoice.bonus_qty.sum(),db.sm_invoice.return_qty.sum(),db.sm_invoice.return_bonus_qty.sum(),orderby=db.sm_invoice.item_name|~db.sm_invoice.actual_tp,groupby=db.sm_invoice.item_id|db.sm_invoice.actual_tp)      
    
    stockDictList=[]
    stockRows=db((db.sm_depot_stock_balance.cid==c_id)&(db.sm_depot_stock_balance.depot_id==depot_id)&(db.sm_depot_stock_balance.store_id==store_id)).select(db.sm_depot_stock_balance.item_id,db.sm_depot_stock_balance.quantity.sum(),orderby=db.sm_depot_stock_balance.item_id,groupby=db.sm_depot_stock_balance.item_id)
    for stockRow in stockRows:
        item_id=stockRow.sm_depot_stock_balance.item_id
        stock_qty=stockRow[db.sm_depot_stock_balance.quantity.sum()]
        
        stockDictList.append({'item_id':item_id,'stock_qty':stock_qty})
    
    
    return dict(records=records,stockDictList=stockDictList,fromDate=fromDate,toDate=toDate,depotID=depot_id,depotName=depotName,storeID=store_id,storeName=storeName,saleTotal=saleTotal,creditTotal=creditTotal,cashRecTotal=cashRecTotal,cashPendingTotal=cashPendingTotal)    


#----------------------
def stp_item_wise_sales_distribution_download():
    c_id=session.cid
    
    response.title='Download-STP-Item Wise Sales Distribution'
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    depot_id=str(request.vars.depotID).strip()
    store_id=str(request.vars.storeID).strip()
    
    depotName=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depotName=depotRow[0].name
        
    storeName=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        storeName=storeRow[0].store_name
    
    try:
        startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d').strftime('%Y-%m-%d') 
        endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d').strftime('%Y-%m-%d')
    except:
        startDt=''
        endDt=''
        
    #--------------    
    saleTotal=0    
    creditTotal=0    
    cashRecTotal=0
    cashPendingTotal=0    
    
    #-----------
    qset=db()
    qset=qset(db.sm_invoice_head.cid==c_id)
    qset=qset(db.sm_invoice_head.depot_id==depot_id)
    qset=qset(db.sm_invoice_head.store_id==store_id)
    qset=qset((db.sm_invoice_head.invoice_date>=startDt)&(db.sm_invoice_head.invoice_date<=endDt))    
    qset=qset(db.sm_invoice_head.status=='Invoiced') 
    qset=qset(db.sm_invoice_head.sl!=0)
    
    #--------- Invoice Total
    records1=qset.select(db.sm_invoice_head.cid,db.sm_invoice_head.actual_total_tp.sum(),db.sm_invoice_head.total_amount.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_vat.sum(),db.sm_invoice_head.return_discount.sum(),db.sm_invoice_head.return_sp_discount.sum(), groupby=db.sm_invoice_head.cid)
    for row1 in records1:
        acTpAmount=row1[db.sm_invoice_head.actual_total_tp.sum()]
        
        #totalAmount=row1[db.sm_invoice_head.total_amount.sum()]
        return_tp=row1[db.sm_invoice_head.return_tp.sum()]
        #return_vat=row1[db.sm_invoice_head.return_vat.sum()]
        #return_discount=row1[db.sm_invoice_head.return_discount.sum()]    
        return_sp=row1[db.sm_invoice_head.return_sp_discount.sum()]
        
        #return_total=return_tp+return_vat-return_discount
        #saleTotal=round(totalAmount-return_total,2)
        
        saleTotal=round(acTpAmount-(return_tp+return_sp),2)
        
        
    #----- Credit Total
    qset2=qset(db.sm_invoice_head.payment_mode=='CREDIT')
    records2=qset2.select(db.sm_invoice_head.cid,db.sm_invoice_head.actual_total_tp.sum(),db.sm_invoice_head.total_amount.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_vat.sum(),db.sm_invoice_head.return_discount.sum(),db.sm_invoice_head.return_sp_discount.sum(),groupby=db.sm_invoice_head.cid)
    for row2 in records2:        
        #totalAmount=row2[db.sm_invoice_head.total_amount.sum()]
        #return_tp=row2[db.sm_invoice_head.return_tp.sum()]
        #return_vat=row2[db.sm_invoice_head.return_vat.sum()]
        #return_discount=row2[db.sm_invoice_head.return_discount.sum()]
        #return_total=return_tp+return_vat-return_discount
        #creditTotal=round(totalAmount-return_total,2)
        
        acTpAmount=row2[db.sm_invoice_head.actual_total_tp.sum()]
        return_tp=row2[db.sm_invoice_head.return_tp.sum()]
        return_sp=row2[db.sm_invoice_head.return_sp_discount.sum()]
        creditTotal=round(acTpAmount-(return_tp+return_sp),2)
        
    #----- Cash Collection
    qset3=qset((db.sm_invoice_head.payment_mode=='CASH')&(db.sm_invoice_head.collection_amount>0))
    records3=qset3.select(db.sm_invoice_head.cid,db.sm_invoice_head.collection_amount.sum(),groupby=db.sm_invoice_head.cid)
    for row3 in records3:
        totalAmount=row3[db.sm_invoice_head.collection_amount.sum()]
        
        cashRecTotal=round(totalAmount,2)
        
    #----- Cash Collection
    qset4=qset((db.sm_invoice_head.payment_mode=='CASH')&(db.sm_invoice_head.inv_pending_flag==1))
    records4=qset4.select(db.sm_invoice_head.cid,db.sm_invoice_head.actual_total_tp.sum(),db.sm_invoice_head.total_amount.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_vat.sum(),db.sm_invoice_head.return_discount.sum(),db.sm_invoice_head.return_sp_discount.sum(),groupby=db.sm_invoice_head.cid)
    for row4 in records4:
        #totalAmount=row4[db.sm_invoice_head.total_amount.sum()]
        #return_tp=row4[db.sm_invoice_head.return_tp.sum()]
        #return_vat=row4[db.sm_invoice_head.return_vat.sum()]
        #return_discount=row4[db.sm_invoice_head.return_discount.sum()]
        #return_total=return_tp+return_vat-return_discount
        #cashPendingTotal=round(totalAmount-return_total,2)
        
        acTpAmount=row4[db.sm_invoice_head.actual_total_tp.sum()]
        return_tp=row4[db.sm_invoice_head.return_tp.sum()]
        return_sp=row4[db.sm_invoice_head.return_sp_discount.sum()]
        cashPendingTotal=round(acTpAmount-(return_tp+return_sp),2)
        
    #=========================================== Item Wise sales distribution    
    records=qset((db.sm_invoice.cid==c_id) & (db.sm_invoice.depot_id==depot_id)&(db.sm_invoice_head.sl==db.sm_invoice.sl)).select(db.sm_invoice.item_id,db.sm_invoice.item_name.max(),db.sm_invoice.actual_tp,db.sm_invoice.quantity.sum(),db.sm_invoice.bonus_qty.sum(),db.sm_invoice.return_qty.sum(),db.sm_invoice.return_bonus_qty.sum(),orderby=db.sm_invoice.item_name|~db.sm_invoice.actual_tp,groupby=db.sm_invoice.item_id|db.sm_invoice.actual_tp)      
    
    stockDictList=[]
    stockRows=db((db.sm_depot_stock_balance.cid==c_id)&(db.sm_depot_stock_balance.depot_id==depot_id)&(db.sm_depot_stock_balance.store_id==store_id)).select(db.sm_depot_stock_balance.item_id,db.sm_depot_stock_balance.quantity.sum(),orderby=db.sm_depot_stock_balance.item_id,groupby=db.sm_depot_stock_balance.item_id)
    for stockRow in stockRows:
        item_id=stockRow.sm_depot_stock_balance.item_id
        stock_qty=stockRow[db.sm_depot_stock_balance.quantity.sum()]
        
        stockDictList.append({'item_id':item_id,'stock_qty':stock_qty})
    
    
    #----------------------------------------
    myString='4.2 STP Generator & Item Wise Sales Distribution\n'
    myString+='Date From:,'+str(startDt)+'\n'
    myString+='To Date:'+','+str(endDt)+'\n'
    myString+='Branch ID:,'+str(depot_id)+'\n'
    myString+='Branch Name'+','+str(depotName)+'\n'
    myString+='Store ID:,'+str(store_id)+'\n'
    myString+='Store Name'+','+str(storeName)+'\n\n'
    
    myString+='STP Generator'+'\n'    
    myString+='Product,Date From,Date To,Sold,Transit,Pending,Net Sales'+'\n'    
    #------------------------    
    soldAmt=cashRecTotal+creditTotal    
    myString+=str(session.depot_short_name)+','+str(fromDate)+','+str(toDate)+','+str(soldAmt)+','+str(saleTotal-(soldAmt+cashPendingTotal))+','+str(cashPendingTotal)+','+str(saleTotal)+'\n\n\n'
    
    myString+='Item Wise Sales Distribution'+'\n'    
    myString+='Item ID,Description,Unit Price (TP),Stock Qty,Sales Qty,Bonus Qty,Sales Amount'+'\n'    
    
    #------------------------
    saleAmtTotal=0
    for record in records:
        item_id=record.sm_invoice.item_id
        item_name=str(record[db.sm_invoice.item_name.max()]).replace(',', '')
        #price=record.sm_invoice.price
        actual_tp=record.sm_invoice.actual_tp
        
        stock_qty=0
        for j in range(len(stockDictList)):
            dictDate=stockDictList[j]
            if dictDate['item_id']==record.sm_invoice.item_id:
                stock_qty=dictDate['stock_qty']
                break
        
        saleQty=record[db.sm_invoice.quantity.sum()]-record[db.sm_invoice.return_qty.sum()]
        bonusQty=record[db.sm_invoice.bonus_qty.sum()]-record[db.sm_invoice.return_bonus_qty.sum()]
        
        saleAmt=saleQty*record.sm_invoice.actual_tp
        
        saleAmtTotal+=saleAmt
        
        myString+=str(item_id)+','+str(item_name)+','+str(actual_tp)+','+str(stock_qty)+','+str(saleQty)+','+str(bonusQty)+','+str(saleAmt)+'\n'
    
    myString+='Total,,,,,,'+str(saleAmtTotal)+'\n'
    
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_stp_item_wise_sales_distribution.csv'   
    return str(myString)
    
#----------------------Set Deafault Store
def set_default_store():
    task_id='rm_analysis_view'
    access_permission=check_role(task_id)
    if (access_permission==False ):
        session.flash='Access is Denied'
        redirect (URL('default','home'))
        
    response.title='Set Default Store'
    
    c_id=session.cid
    
    btn_set_store=request.vars.btn_set_store
    
    if (btn_set_store):        
        depot=str(request.vars.depot_id)
        store=str(request.vars.store_id)
        
        if depot=='' or store=='':
            response.flash='Required Branch and Store'
        else:
            if len(depot.split('|'))>1:
                depot_id=depot.split('|')[0]
            else:
                depot_id=depot
            
            if len(store.split('|'))>1:
                store_id=store.split('|')[0]
            else:
                store_id=store
                
            session.report_store_id=''
            session.report_store_name=''
            storeRows = db((db.sm_depot_store.cid == c_id) & (db.sm_depot_store.depot_id == depot_id) & (db.sm_depot_store.store_id == store_id)).select(db.sm_depot_store.store_name,limitby=(0, 1))
            if not storeRows:
                response.flash='Invalid Branch Store'
            else:
                store_name=storeRows[0].store_name
                
                session.report_store_id=store_id
                session.report_store_name=store_name
                
                response.flash='Default Store set successfully'
    
    #-------------------
    return dict()




# ======================Nadira
# http://127.0.0.1:8000/skf/report/outStInvoiceWise_AsOfDate_trNAD?credit_type=&customerId=&customer_cat=&customer_sub_cat=&deliveryManID=&depotID=170&invoice_term=&msoID=&out_st_level1_id=&out_st_level2_id=&storeID=170140&territoryID=&toDate=2016-09-29
# http://a002.businesssolutionapps.com/skf/report/outStInvoiceWise_AsOfDate_trNAD?credit_type=&customerId=&customer_cat=&customer_sub_cat=&deliveryManID=&depotID=170&invoice_term=&msoID=&out_st_level1_id=&out_st_level2_id=&storeID=170140&territoryID=&toDate=2016-09-29
def outStInvoiceWise_AsOfDate_trNAD():
    c_id=session.cid
    
    response.title='6.1A Outstanding Invoice wise (As Of Date)'
    
    toDate=request.vars.toDate
    
    depot_id=str(request.vars.depotID).strip()
    store_id=str(request.vars.storeID).strip()
    out_st_delivery_man_id=str(request.vars.deliveryManID).strip()
    out_st_territory_id=str(request.vars.territoryID).strip()
    out_st_mso_id=str(request.vars.msoID).strip()
    invoice_term=str(request.vars.invoice_term).strip()
    customerId=str(request.vars.customerId).strip()
    
    credit_type=str(request.vars.credit_type).strip()
    customer_cat=str(request.vars.customer_cat).strip() 
    customer_sub_cat=str(request.vars.customer_sub_cat).strip()  
    
    out_st_level1_id=str(request.vars.out_st_level1_id).strip()  
    out_st_level2_id=str(request.vars.out_st_level2_id).strip()  
    
    catName=''
    custCatRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_CATEGORY')&(db.sm_category_type.cat_type_id==customer_cat)).select(db.sm_category_type.cat_type_name, limitby=(0,1))
    if custCatRows:
        catName=custCatRows[0].cat_type_name        
    subCatName=''
    custSubCatRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_SUB_CATEGORY')&(db.sm_category_type.cat_type_id==customer_sub_cat)).select(db.sm_category_type.cat_type_name, limitby=(0,1))
    if custSubCatRows:
        subCatName=custSubCatRows[0].cat_type_name
        
    depot_name=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depot_name=depotRow[0].name
        
    store_name=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        store_name=storeRow[0].store_name
        
    out_st_delivery_man_name=''
    dpRow=db((db.sm_delivery_man.cid==c_id)&(db.sm_delivery_man.depot_id==depot_id)&(db.sm_delivery_man.d_man_id==out_st_delivery_man_id)).select(db.sm_delivery_man.name,limitby=(0,1))
    if dpRow:
        out_st_delivery_man_name=dpRow[0].name
        
    out_st_territory_name=''
    levelRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==out_st_territory_id)).select(db.sm_level.level_name,limitby=(0,1))
    if levelRow:
        out_st_territory_name=levelRow[0].level_name
        
    out_st_mso_name=''
    repRow=db((db.sm_rep.cid==c_id)&(db.sm_rep.rep_id==out_st_mso_id)).select(db.sm_rep.name,limitby=(0,1))
    if repRow:
        out_st_mso_name=repRow[0].name
        
    customerName=''
    clientRow=db((db.sm_client.cid==c_id)&(db.sm_client.depot_id==depot_id)&(db.sm_client.client_id==customerId)).select(db.sm_client.name,limitby=(0,1))
    if clientRow:
        customerName=clientRow[0].name
    
    startDt=''
    try:        
        endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d').strftime('%Y-%m-%d')
    except:
        endDt=''
        
    #--------------
    
    condStr="(cid = '"+c_id+"') AND (depot_id='"+depot_id+"') AND (store_id='"+store_id+"') AND (transaction_date <= '"+str(endDt)+"')"
    
    if out_st_delivery_man_id!='':
        condStr+=" AND (d_man_id='"+out_st_delivery_man_id+"')"        
    if out_st_territory_id!='':
        condStr+=" AND (area_id='"+out_st_territory_id+"')"        
    if out_st_mso_id!='':
        condStr+=" AND (rep_id='"+out_st_mso_id+"')"        
    if invoice_term!='':
        condStr+=" AND (payment_mode='"+invoice_term+"')"
    if customerId!='':
        condStr+=" AND (client_id='"+customerId+"')"
        
    if credit_type!='':
        condStr+=" AND (credit_note='"+credit_type+"')"
    if customer_cat!='':
        condStr+=" AND (cl_category_id='"+customer_cat+"')"
    if customer_sub_cat!='':
        condStr+=" AND (cl_sub_category_id='"+customer_sub_cat+"')"
        
    if out_st_level1_id!='':
        condStr+=" AND (level1_id='"+out_st_level1_id+"')"        
    if out_st_level2_id!='':
        condStr+=" AND (level2_id='"+out_st_level2_id+"')"
        
    detailRecords="SELECT * from (SELECT cid, depot_id, depot_name, store_id, store_name, inv_rowid, inv_sl, invoice_date, transaction_date, ROUND(SUM(trans_net_amt),6) as trans_net_amt, ROUND(SUM( tp_amt ),6) as tp_amt , ROUND(SUM( vat_amt ),6) as vat_amt , ROUND(SUM( disc_amt ),6) as disc_amt , ROUND(SUM( spdisc_amt ),6) as spdisc_amt , ROUND(SUM( adjust_amount ),6) as adjust_amount , delivery_date, payment_mode, credit_note, client_id, client_name, cl_category_id, cl_category_name, cl_sub_category_id, cl_sub_category_name, client_limit_amt, rep_id, rep_name, market_id, market_name, d_man_id, d_man_name, level0_id, level0_name, level1_id, level1_name, level2_id, level2_name, area_id, area_name, shipment_no FROM sm_rpt_transaction WHERE ("+str(condStr)+") GROUP BY inv_rowid ORDER BY client_name) rptview WHERE rptview.trans_net_amt!=0"
    recordList=db.executesql(detailRecords,as_dict = True)    
    #====================
    
   
    
    #====================    
    ostNet=0
    ostTp=0
    ostVat=0
    ostDisc=0
    ostSpDisc=0
    ostAdjust=0  
    rowSL=0 
    myString='SL  ,  Date  ,  Invoice No  ,  Cust. ID  ,  Cust. Name ,   Sub-Category ,   MSOID  ,  MSOName   , DPID  ,  DPName   , Terms  ,  Tr. Code ,   Market  ,   OutStanding  ,  Aging  ,  Outst %\n'

    for i in range(len(recordList)):
        dictData=recordList[i]
        rowSL+=1   
        invoice_date=datetime.datetime.strptime(str(dictData['invoice_date']),'%Y-%m-%d')
        aging=''#(current_date-invoice_date).days
        myString=myString+str(rowSL)+','+str(dictData['invoice_date'].strftime('%d-%b-%y'))+','+str(session.prefix_invoice)+'INV'+str(dictData['depot_id'])+'-'+str(dictData['inv_sl'])+','+str(dictData['client_id'])+','+str(dictData['client_name'])+','+str(dictData['cl_sub_category_name'])+','+str(dictData['rep_id'])+','+str(dictData['rep_name'])+','+str(dictData['d_man_id'])+','+str(dictData['d_man_name'])+','+str(dictData['credit_note'])+','+str(dictData['area_id'])+','+str(dictData['market_name'])+','+str(dictData['trans_net_amt'])+','+str(aging)+'\n'
        

    
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=outStInvoiceWise_AsOfDate_trNAD.csv'   
    return str(myString)
   